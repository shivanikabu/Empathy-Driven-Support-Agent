from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class AgentResponse:
    """Base response structure for all agents"""
    agent_name: str
    detail: str
    
@dataclass
class PlannerResponse(AgentResponse):
    """Planner agent response"""
    persona: str
    sentiment: str
    
@dataclass
class OrchestrationResponse(AgentResponse):
    """Orchestration agent response"""
    agent_flow: List[str]
    
@dataclass
class RAGResponse(AgentResponse):
    """RAG agent response"""
    documents: List[str]
    
@dataclass
class EmotionsResponse(AgentResponse):
    """Emotions agent response"""
    emotion: str
    intensity: int
    
@dataclass
class CalmingResponse(AgentResponse):
    """Calming agent response"""
    preamble: str
    
@dataclass
class ReflectorResponse(AgentResponse):
    """Reflector agent response"""
    quality_score: float
    violations: List[str]
    token_count: int
    performance_status: str
    performance_issue: Optional[str]
    
@dataclass
class ResponseAgentResponse(AgentResponse):
    """Response agent response"""
    response: str
    
@dataclass
class FeedbackResponse(AgentResponse):
    """Feedback agent response"""
    convergence_score: float
    recommendation: str
    
@dataclass
class AgentFlowResult:
    """Complete agent flow execution result"""
    agents_executed: List[Dict[str, Any]]
    final_response: str
    persona: str
