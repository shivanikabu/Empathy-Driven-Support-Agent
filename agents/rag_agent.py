from agents.base_agent import BaseAgent
from models.agent_models import RAGResponse
from services.vector_db_service import VectorDBService

class RAGAgent(BaseAgent):
    """Agent for retrieving relevant documents"""
    
    def __init__(self, vector_db_service: VectorDBService):
        super().__init__("RAG Agent")
        self.vector_db = vector_db_service
    
    def execute(self, query: str) -> RAGResponse:
        """Retrieve documents from vector database"""
        documents = []
        
        if not self.vector_db or not self.vector_db.collection:
            detail = "ERROR: Vector database not initialized!"
            return RAGResponse(
                agent_name=self.name,
                detail=detail,
                documents=[]
            )
        
        try:
            documents = self.vector_db.get_all_documents()
            
            if documents:
                detail = f"✓ Retrieved ALL {len(documents)} document chunks for complete context"
            else:
                detail = "ERROR: No documents in database. Please upload and process PDF documents."
        
        except Exception as e:
            detail = f"ERROR: {str(e)}"
        
        return RAGResponse(
            agent_name=self.name,
            detail=detail,
            documents=documents
        )
