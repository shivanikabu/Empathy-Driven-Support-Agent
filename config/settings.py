class AppConfig:
    """Application configuration"""
    APP_TITLE = "AI Agents Enterprise Toolkit"
    PAGE_LAYOUT = "wide"
    AWS_DEFAULT_REGION = "us-east-1"
    LANGFUSE_DEFAULT_HOST = "https://cloud.langfuse.com"
    
class ModelConfig:
    """Model configuration"""
    BEDROCK_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7
    
class VectorDBConfig:
    """Vector database configuration"""
    COLLECTION_NAME = "documents"
    MIN_PARAGRAPH_LENGTH = 50
    
class UIConfig:
    """UI styling configuration"""
    COLORS = {
        "planner": "#E3F2FD",
        "orchestration": "#F3E5F5",
        "rag": "#FFF9C4",
        "emotions": "#FFE0B2",
        "best_practices": "#E1F5FE",
        "reflector": "#F8BBD0",
        "response": "#C8E6C9",
        "default": "#D1C4E9"
    }
