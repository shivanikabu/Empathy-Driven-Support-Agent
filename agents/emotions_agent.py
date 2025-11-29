from agents.base_agent import BaseAgent
from models.agent_models import EmotionsResponse

class EmotionsAgent(BaseAgent):
    """Agent for analyzing emotional content"""
    
    def __init__(self):
        super().__init__("Emotions Agent")
    
    def execute(self, query: str, persona: str) -> EmotionsResponse:
        """Analyze emotional intensity"""
        intensity = 7 if persona == "angry customer" else 5
        emotion = "frustration" if persona == "angry customer" else "confusion"
        detail = f"Emotional analysis: {emotion.capitalize()} detected. Intensity: {intensity}/10."
        
        return EmotionsResponse(
            agent_name=self.name,
            detail=detail,
            emotion=emotion,
            intensity=intensity
        )
