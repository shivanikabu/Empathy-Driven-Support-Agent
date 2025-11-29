from agents.base_agent import BaseAgent
from models.agent_models import OrchestrationResponse
from typing import List

class OrchestrationAgent(BaseAgent):
    """Agent for routing to appropriate agent combinations"""
    
    def __init__(self):
        super().__init__("Orchestration Agent")
    
    def execute(self, persona: str) -> OrchestrationResponse:
        """Determine agent flow based on persona"""
        if persona == "simple query":
            agent_flow = ["RAG Agent", "Reflector Agent", "Response Agent", "Feedback Agent"]
            detail = f"Standard RAG flow selected for '{persona}'. Delegating to RAG Agent."
        
        elif persona in ["angry customer", "confused customer"]:
            agent_flow = ["Emotions Agent", "Calming Agent", "RAG Agent", 
                         "Reflector Agent", "Response Agent", "Feedback Agent"]
            detail = f"Emotional support flow activated. Delegating to Emotions → Calming → RAG Agents."
        
        else:  # precision ask
            agent_flow = ["RAG Agent", "Best Practices Agent", "Reflector Agent", 
                         "Response Agent", "Feedback Agent"]
            detail = f"Best practices flow selected. Delegating to RAG + Best Practices Agents."
        
        return OrchestrationResponse(
            agent_name=self.name,
            detail=detail,
            agent_flow=agent_flow
        )
