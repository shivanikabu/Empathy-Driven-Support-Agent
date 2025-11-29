# ============================================================================
# FILE: backend.py (REFACTORED)
# Main backend orchestrator using modular components
# ============================================================================

from typing import List, Dict, Any
from services.aws_service import AWSService
from services.langfuse_service import LangfuseService
from services.vector_db_service import VectorDBService
from services.document_processor import DocumentProcessor
from agents.planner_agent import PlannerAgent
from agents.orchestration_agent import OrchestrationAgent
from agents.rag_agent import RAGAgent
from agents.emotions_agent import EmotionsAgent
from agents.calming_agent import CalmingAgent
from agents.best_practices_agent import BestPracticesAgent
from agents.reflector_agent import ReflectorAgent
from agents.response_agent import ResponseAgent
from agents.feedback_agent import FeedbackAgent
from models.agent_models import AgentFlowResult

class AgentBackend:
    """Refactored backend orchestrator"""
    
    def __init__(self):
        # Initialize services
        self.aws_service = AWSService()
        self.langfuse_service = LangfuseService()
        self.vector_db_service = VectorDBService()
        self.document_processor = DocumentProcessor()
        
        # Initialize agents (lazy loading where needed)
        self.planner_agent = PlannerAgent()
        self.orchestration_agent = OrchestrationAgent()
        self.emotions_agent = EmotionsAgent()
        self.calming_agent = CalmingAgent()
        self.best_practices_agent = BestPracticesAgent()
        self.feedback_agent = FeedbackAgent()
        
        # These agents need service dependencies
        self.rag_agent = None
        self.response_agent = None
        self.reflector_agent = None
        
    def connect_aws(self, aws_access_key: str, aws_secret_key: str, aws_region: str):
        """Connect to AWS and initialize dependent agents"""
        success, message = self.aws_service.connect(aws_access_key, aws_secret_key, aws_region)
        if success:
            self.vector_db_service.initialize()
            self.rag_agent = RAGAgent(self.vector_db_service)
            self.response_agent = ResponseAgent(self.aws_service)
            self.reflector_agent = ReflectorAgent()
        return success, message
    
    def connect_langfuse(self, public_key: str, secret_key: str, host: str):
        """Connect to Langfuse"""
        return self.langfuse_service.connect(public_key, secret_key, host)
    
    def process_documents(self, uploaded_files):
        """Process and store PDF documents"""
        try:
            # Clear existing documents
            self.vector_db_service.clear()
            
            all_paragraphs = []
            all_metadatas = []
            
            for uploaded_file in uploaded_files:
                success, message, paragraphs = self.document_processor.extract_text_from_pdf(uploaded_file)
                
                if not success:
                    continue
                
                # Add to batch
                for idx, para in enumerate(paragraphs):
                    all_paragraphs.append(para)
                    all_metadatas.append({
                        "source": uploaded_file.name,
                        "chunk_index": idx + 1,
                        "chunk_type": "paragraph",
                        "char_count": len(para)
                    })
            
            if all_paragraphs:
                success, message = self.vector_db_service.add_documents(all_paragraphs, all_metadatas)
                if success:
                    return True, f"✓ Successfully processed {len(uploaded_files)} PDF file(s) → {len(all_paragraphs)} chunks stored"
                return False, message
            else:
                return False, "No valid text content found in PDF files."
        
        except Exception as e:
            return False, f"Error processing documents: {str(e)}"
    
    def clear_vector_db(self):
        """Clear vector database"""
        return self.vector_db_service.clear()
    
    @property
    def vector_db(self):
        """Property to maintain compatibility with existing code"""
        return self.vector_db_service.collection
    
    def execute_agentic_flow(self, query: str, risk_weight: float, 
                            accuracy_weight: float, latency_weight: float, 
                            cost_weight: float, guardrails: str) -> Dict[str, Any]:
        """Execute complete agentic flow"""
        
        agents_executed = []
        
        # Step 1: Planner Agent
        planner_result = self.planner_agent.execute(query)
        agents_executed.append({
            "agent": "Planner Agent",
            "emoji": "🧠",
            "action": "Analyzing query sentiment",
            "detail": planner_result.detail
        })
        persona = planner_result.persona
        
        # Step 2: Orchestration Agent
        orchestration_result = self.orchestration_agent.execute(persona)
        agents_executed.append({
            "agent": "Orchestration Agent",
            "emoji": "🎯",
            "action": "Routing to appropriate agents",
            "detail": orchestration_result.detail
        })
        agent_flow = orchestration_result.agent_flow
        
        # Initialize variables
        calming_preamble = None
        best_practices = False
        documents = []
        final_response = ""
        quality_score = 0.85
        token_count = 0
        
        # Execute agent flow
        for agent_name in agent_flow:
            if agent_name == "Emotions Agent":
                emotion_result = self.emotions_agent.execute(query, persona)
                agents_executed.append({
                    "agent": "Emotions Agent",
                    "emoji": "💭",
                    "action": "Analyzing emotional content",
                    "detail": emotion_result.detail
                })
            
            elif agent_name == "Calming Agent":
                calming_result = self.calming_agent.execute()
                calming_preamble = calming_result.preamble
                agents_executed.append({
                    "agent": "Calming Agent",
                    "emoji": "🕊️",
                    "action": "Generating empathetic response",
                    "detail": calming_result.detail
                })
            
            elif agent_name == "RAG Agent":
                rag_result = self.rag_agent.execute(query)
                documents = rag_result.documents
                agents_executed.append({
                    "agent": "RAG Agent",
                    "emoji": "📚",
                    "action": "Retrieving relevant documents",
                    "detail": rag_result.detail
                })
            
            elif agent_name == "Best Practices Agent":
                bp_result = self.best_practices_agent.execute()
                best_practices = True
                agents_executed.append({
                    "agent": "Best Practices Agent",
                    "emoji": "⭐",
                    "action": "Enhancing with best practices",
                    "detail": bp_result["detail"]
                })
            
            elif agent_name == "Response Agent":
                response_result = self.response_agent.execute(
                    query, documents, persona, calming_preamble, best_practices
                )
                final_response = response_result.response
                agents_executed.append({
                    "agent": "Response Agent",
                    "emoji": "✍️",
                    "action": "Building final response",
                    "detail": response_result.detail
                })
            
            elif agent_name == "Reflector Agent":
                reflector_result = self.reflector_agent.execute(
                    query, documents, final_response, guardrails
                )
                agents_executed.append({
                    "agent": "Reflector Agent",
                    "emoji": "🤔",
                    "action": "Evaluating response quality",
                    "detail": reflector_result.detail,
                    "performance_status": reflector_result.performance_status,
                    "performance_issue": reflector_result.performance_issue
                })
                quality_score = reflector_result.quality_score
                token_count = reflector_result.token_count
            
            elif agent_name == "Feedback Agent":
                feedback_result = self.feedback_agent.execute(
                    quality_score, risk_weight, accuracy_weight, 
                    latency_weight, cost_weight, token_count
                )
                agents_executed.append({
                    "agent": "Feedback Agent",
                    "emoji": "📊",
                    "action": "Calculating convergence score",
                    "detail": feedback_result.detail
                })
        
        return {
            "agents_executed": agents_executed,
            "final_response": final_response,
            "persona": persona
        }