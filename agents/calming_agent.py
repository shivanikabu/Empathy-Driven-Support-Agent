from agents.base_agent import BaseAgent
from models.agent_models import CalmingResponse

class CalmingAgent(BaseAgent):
    """Agent for generating empathetic preambles"""
    
    def __init__(self):
        super().__init__("Calming Agent")
    
    def execute(self, emotion_data: dict = None) -> CalmingResponse:
        """Generate empathetic preamble"""
        preamble = "I understand your frustration, and I'm here to help resolve this for you."
        detail = f"Empathetic preamble generated: '{preamble}'"
        
        return CalmingResponse(
            agent_name=self.name,
            detail=detail,
            preamble=preamble
        )
