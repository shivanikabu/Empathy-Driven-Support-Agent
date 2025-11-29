import json
import boto3
from typing import Tuple, Optional

class AWSService:
    """Service for AWS Bedrock interactions"""
    
    def __init__(self):
        self.client: Optional[boto3.client] = None
        self.session: Optional[boto3.Session] = None
        self.region: Optional[str] = None
        
    def connect(self, access_key: str, secret_key: str, region: str) -> Tuple[bool, str]:
        """Connect to AWS Bedrock"""
        try:
            self.session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            self.client = self.session.client('bedrock-runtime')
            self.region = region
            return True, "AWS Connected Successfully"
        except Exception as e:
            return False, f"AWS Connection Failed: {str(e)}"
    
    def is_connected(self) -> bool:
        """Check if AWS is connected"""
        return self.client is not None
    
    def invoke_model(self, prompt: str, max_tokens: int = 4000, 
                     temperature: float = 0.7, model_id: str = None) -> str:
        """Invoke Claude model on Bedrock"""
        if not self.client:
            raise Exception("AWS Bedrock not connected")
        
        if model_id is None:
            from config.settings import ModelConfig
            model_id = ModelConfig.BEDROCK_MODEL_ID
        
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        
        response = self.client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
