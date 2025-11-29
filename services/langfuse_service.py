from langfuse import Langfuse
from typing import Tuple, Optional

class LangfuseService:
    """Service for Langfuse observability"""
    
    def __init__(self):
        self.client: Optional[Langfuse] = None
        
    def connect(self, public_key: str, secret_key: str, host: str) -> Tuple[bool, str]:
        """Connect to Langfuse"""
        try:
            self.client = Langfuse(
                public_key=public_key,
                secret_key=secret_key,
                host=host
            )
            return True, "Langfuse Connected Successfully"
        except Exception as e:
            return False, f"Langfuse Connection Failed: {str(e)}"
    
    def is_connected(self) -> bool:
        """Check if Langfuse is connected"""
        return self.client is not None

