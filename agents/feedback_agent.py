from agents.base_agent import BaseAgent
from models.agent_models import FeedbackResponse

class FeedbackAgent(BaseAgent):
    """Agent for calculating convergence score"""
    
    def __init__(self):
        super().__init__("Feedback Agent")
    
    def execute(self, quality_score: float, risk_weight: float, 
                accuracy_weight: float, latency_weight: float, 
                cost_weight: float, token_count: int) -> FeedbackResponse:
        """Calculate convergence score and provide feedback"""
        
        convergence_score = (
            risk_weight * 0.9 +
            accuracy_weight * quality_score +
            latency_weight * 0.75 +
            cost_weight * (1.0 - min(token_count / 10000, 1.0))
        ) / (risk_weight + accuracy_weight + latency_weight + cost_weight)
        
        recommendation = "Proceed" if convergence_score >= 0.7 else "Refine"
        detail = f"Convergence score: {convergence_score:.3f}. Meets threshold: {'Yes' if convergence_score >= 0.7 else 'No'}. Recommendation: {recommendation}."
        
        return FeedbackResponse(
            agent_name=self.name,
            detail=detail,
            convergence_score=convergence_score,
            recommendation=recommendation
        )
