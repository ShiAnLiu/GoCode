import requests
from typing import Dict, List, Any, Optional
from utils.api_config import APIConfig, APIProvider

class AIClient:
    def __init__(self, config_path: str = None):
        self.config = APIConfig(config_path)
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 2000) -> Dict[str, Any]:
        try:
            url = self.config.get_api_url()
            headers = self.config.get_headers()
            payload = self.config.build_payload(messages, temperature, max_tokens)
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                content = self.config.parse_response(result)
                
                return {
                    "success": True,
                    "content": content
                }
            else:
                return {
                    "error": f"API调用失败: {response.status_code}",
                    "success": False
                }
                
        except Exception as e:
            return {
                "error": f"API调用失败: {str(e)}",
                "success": False
            }
    
    def set_provider(self, provider: str):
        self.config.set_provider(provider)
    
    def configure(self, provider: str, **kwargs):
        self.config.set_api_config(provider, **kwargs)
    
    def get_provider(self) -> str:
        return self.config.get_provider()
