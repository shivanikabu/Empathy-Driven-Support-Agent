from agents.base_agent import BaseAgent
from models.agent_models import ResponseAgentResponse
from services.aws_service import AWSService
from typing import List, Optional

class ResponseAgent(BaseAgent):
    """Agent for building final response using LLM"""
    
    def __init__(self, aws_service: AWSService):
        super().__init__("Response Agent")
        self.aws_service = aws_service
    
    def execute(self, query: str, documents: List[str], persona: str,
                calming_preamble: Optional[str] = None, 
                best_practices: bool = False) -> ResponseAgentResponse:
        """Build final response using AWS Bedrock"""
        
        if not self.aws_service.is_connected():
            return ResponseAgentResponse(
                agent_name=self.name,
                detail="AWS Bedrock connection required",
                response="[Error: AWS Bedrock not connected]"
            )
        
        try:
            # Check for document display request
            query_lower = query.lower()
            if any(term in query_lower for term in ['display document', 'show document', 
                                                      'what documents', 'document content']):
                if documents:
                    response = f"I found {len(documents)} document chunks:\n\n"
                    for i, doc in enumerate(documents[:10], 1):
                        response += f"**Chunk {i}:**\n{doc[:400]}{'...' if len(doc) > 400 else ''}\n\n"
                    if len(documents) > 10:
                        response += f"... and {len(documents) - 10} more chunks."
                else:
                    response = "No documents uploaded yet."
                
                return ResponseAgentResponse(
                    agent_name=self.name,
                    detail=f"Document display response generated.",
                    response=response
                )
            
            # Prepare context
            if documents:
                context_text = "\n\n---\n\n".join(documents)
                detail_prefix = f"Using COMPLETE context: ALL {len(documents)} document chunks"
            else:
                context_text = "No document context available."
                detail_prefix = "WARNING: No document context available"
            
            # Build prompt based on persona
            if persona in ["angry customer", "confused customer"]:
                system_prompt = "You are an empathetic customer support agent."
            elif persona == "precision ask":
                system_prompt = "You are a technical expert."
            else:
                system_prompt = "You are a helpful assistant."
            
            prompt = f"""{system_prompt}

COMPLETE DOCUMENT CONTEXT:
{context_text}

Customer query: {query}

INSTRUCTIONS:
- Use the COMPLETE document context to answer
- Provide comprehensive, well-structured answer
- Reference specific information from context
"""
            
            # Call AWS Bedrock
            final_response = self.aws_service.invoke_model(prompt)
            
            # Add calming preamble if provided
            if calming_preamble:
                final_response = f"{calming_preamble}\n\n{final_response}"
            
            detail = f"{detail_prefix} | Final response: {len(final_response)} characters"
            
            return ResponseAgentResponse(
                agent_name=self.name,
                detail=detail,
                response=final_response
            )
            
        except Exception as e:
            return ResponseAgentResponse(
                agent_name=self.name,
                detail=f"Bedrock API Error: {str(e)}",
                response=f"[Error calling Bedrock: {str(e)}]"
            )

