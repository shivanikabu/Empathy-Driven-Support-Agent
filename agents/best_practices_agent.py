from agents.base_agent import BaseAgent
from typing import Dict, Any

class BestPracticesAgent(BaseAgent):
    """Agent for adding technical best practices"""
    
    def __init__(self):
        super().__init__("Best Practices Agent")
    
    def execute(self) -> Dict[str, Any]:
        """Add best practices enhancement flag"""
        detail = "Enhanced response with step-by-step guidance, warnings, and industry best practices."
        
        return {
            "agent": self.name,
            "enhancement": "best_practices",
            "detail": detail
        }
