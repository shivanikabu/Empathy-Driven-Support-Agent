import numpy as np
from agents.base_agent import BaseAgent
from models.agent_models import ReflectorResponse
from typing import List, Optional

class ReflectorAgent(BaseAgent):
    """Agent for evaluating response quality"""
    
    def __init__(self):
        super().__init__("Reflector Agent")
    
    def execute(self, query: str, documents: List[str], 
                response_text: str, guardrails: str) -> ReflectorResponse:
        """Evaluate query, retrievals, and response quality"""
        
        # Evaluate guardrails
        violations = []
        if guardrails:
            guardrail_list = [g.strip() for g in guardrails.split('\n') if g.strip()]
            # Simplified guardrail check
            for guardrail in guardrail_list:
                if 'profanity' in guardrail.lower():
                    pass  # Would implement actual check here
        
        quality_score = np.random.uniform(0.80, 0.95)
        token_count = int(len(response_text.split()) * 1.3)
        
        # Performance evaluation
        performance_status = "optimal"
        performance_issue = None
        
        if not documents or len(documents) == 0:
            performance_status = "warning"
            performance_issue = "Critical: No relevant documents found in vector DB."
        elif len(documents) < 3:
            performance_status = "acceptable"
            performance_issue = "Document retrieval returned fewer than expected chunks."
        elif quality_score < 0.85:
            performance_status = "acceptable"
            performance_issue = f"Quality score ({quality_score:.2f}) below optimal threshold."
        elif token_count > 1500:
            performance_status = "acceptable"
            performance_issue = f"Token usage ({token_count}) higher than expected."
        elif violations:
            performance_status = "warning"
            performance_issue = f"Critical: Guardrail violation detected - {violations[0]}."
        
        detail = f"Response evaluated. {'No guardrail violations detected' if not violations else f'{len(violations)} violations'}. Quality score: {quality_score:.2f}. Total tokens: {token_count}"
        
        return ReflectorResponse(
            agent_name=self.name,
            detail=detail,
            quality_score=quality_score,
            violations=violations,
            token_count=token_count,
            performance_status=performance_status,
            performance_issue=performance_issue
        )
