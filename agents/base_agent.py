from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute agent logic"""
        pass
