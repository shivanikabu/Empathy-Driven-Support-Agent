from agents.base_agent import BaseAgent
from models.agent_models import PlannerResponse

class PlannerAgent(BaseAgent):
    """Agent for analyzing query sentiment and determining persona"""
    
    def __init__(self):
        super().__init__("Planner Agent")
    
    def execute(self, query: str) -> PlannerResponse:
        """Analyze query and determine persona"""
        query_lower = query.lower()
        
        # Angry customer detection
        if any(phrase in query_lower for phrase in [
            'how many time', 'how many times', 'annoyed', 'am annoyed',
            'asking again and again', 'disappointed', 'frustrated', 
            'upset', 'terrible', 'worst', 'hate'
        ]):
            persona = "angry customer"
            sentiment = "negative"
            detail = f"Detected persona: '{persona}'. Sentiment: {sentiment}. High frustration detected."
        
        # Confused customer detection
        elif any(phrase in query_lower for phrase in [
            'tried before', 'did not work', 'didn\'t work', 'not working',
            'confused', 'don\'t understand', 'unclear', 'lost'
        ]):
            persona = "confused customer"
            sentiment = "negative"
            detail = f"Detected persona: '{persona}'. Sentiment: {sentiment}. Confusion detected."
        
        # Precision queries
        elif any(phrase in query_lower for phrase in [
            'can you tell me exactly', 'can you tell me clearly', 
            'precisely', 'specific', 'detailed', 'step by step'
        ]):
            persona = "precision ask"
            sentiment = "neutral"
            detail = f"Detected persona: '{persona}'. Technical complexity: High."
        
        # Simple query
        else:
            persona = "simple query"
            sentiment = "positive"
            detail = f"Detected persona: '{persona}'. Sentiment score: 0.65 (positive). Complexity: Low."
        
        return PlannerResponse(
            agent_name=self.name,
            detail=detail,
            persona=persona,
            sentiment=sentiment
        )
