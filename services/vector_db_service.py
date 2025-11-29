import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime

class VectorDBService:
    """Service for vector database operations"""
    
    def __init__(self):
        self.client: Optional[chromadb.Client] = None
        self.collection = None
        self.embedding_model: Optional[SentenceTransformer] = None
        
    def initialize(self, collection_name: str = "documents", 
                   model_name: str = "all-MiniLM-L6-v2") -> None:
        """Initialize ChromaDB and embedding model"""
        self.client = chromadb.Client()
        self.embedding_model = SentenceTransformer(model_name)
        
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except:
            self.collection = self.client.create_collection(name=collection_name)
    
    def clear(self) -> Tuple[bool, str]:
        """Clear all documents from the database"""
        try:
            if self.client and self.collection:
                self.client.delete_collection(name=self.collection.name)
                self.collection = self.client.create_collection(name="documents")
                return True, "Vector database cleared successfully"
            return False, "Database not initialized"
        except Exception as e:
            return False, f"Error clearing database: {str(e)}"
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Add documents to the vector database"""
        try:
            if not self.collection or not self.embedding_model:
                return False, "Database not initialized"
            embeddings = [self.embedding_model.encode(doc).tolist() for doc in documents]
            
            # Generate IDs
            timestamp_ms = int(datetime.now().timestamp() * 1000)
            ids = [f"doc_{i}_{timestamp_ms}" for i in range(len(documents))]
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas or [{} for _ in documents],
                ids=ids
            )
            
            return True, f"Added {len(documents)} documents successfully"
        except Exception as e:
            return False, f"Error adding documents: {str(e)}"
    
    def get_all_documents(self) -> List[str]:
        """Retrieve all documents from the database"""
        try:
            if not self.collection:
                return []
            
            results = self.collection.get()
            if results and 'documents' in results:
                return results['documents']
            return []
        except Exception as e:
            print(f"Error retrieving documents: {str(e)}")
            return []
    
    def query_documents(self, query: str, n_results: int = 10) -> List[str]:
        """Query documents by similarity"""
        try:
            if not self.collection or not self.embedding_model:
                return []
            
            query_embedding = self.embedding_model.encode(query).tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            if results and 'documents' in results:
                return results['documents'][0]
            return []
        except Exception as e:
            print(f"Error querying documents: {str(e)}")
            return []
    
    def get_document_count(self) -> int:
        """Get the number of documents in the database"""
        try:
            if not self.collection:
                return 0
            results = self.collection.get()
            if results and 'documents' in results:
                return len(results['documents'])
            return 0
        except:
            return 0