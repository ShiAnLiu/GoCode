import os
import json
from typing import Dict, Optional
from enum import Enum

class APIProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LMSTUDIO = "lmstudio"
    OLLAMA = "ollama"
    CUSTOM = "custom"

class APIConfig:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'api_config.json')
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        default_config = {
            "provider": "lmstudio",
            "openai": {
                "api_key": "",
                "base_url": "https://api.openai.com/v1",
                "model": "gpt-3.5-turbo"
            },
            "anthropic": {
                "api_key": "",
                "base_url": "https://api.anthropic.com",
                "model": "claude-3-sonnet-20240229"
            },
            "lmstudio": {
                "base_url": "http://localhost:1234/v1",
                "model": "qwen2-0.5b-instruct"
            },
            "ollama": {
                "base_url": "http://localhost:11434/v1",
                "model": "llama2"
            },
            "custom": {
                "base_url": "",
                "model": ""
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return default_config
    
    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def get_provider(self) -> str:
        return self.config.get("provider", "lmstudio")
    
    def set_provider(self, provider: str):
        self.config["provider"] = provider
        self.save_config()
    
    def get_api_url(self) -> str:
        provider = self.get_provider()
        provider_config = self.config.get(provider, {})
        base_url = provider_config.get("base_url", "")
        
        if provider == "lmstudio":
            return f"{base_url}/chat/completions"
        elif provider == "ollama":
            return f"{base_url}/chat/completions"
        elif provider == "openai":
            return f"{base_url}/chat/completions"
        elif provider == "anthropic":
            return base_url
        elif provider == "custom":
            return base_url
        return base_url
    
    def get_model(self) -> str:
        provider = self.get_provider()
        provider_config = self.config.get(provider, {})
        return provider_config.get("model", "")
    
    def get_api_key(self) -> Optional[str]:
        provider = self.get_provider()
        provider_config = self.config.get(provider, {})
        return provider_config.get("api_key")
    
    def set_api_config(self, provider: str, **kwargs):
        if provider not in self.config:
            self.config[provider] = {}
        
        for key, value in kwargs.items():
            self.config[provider][key] = value
        
        self.save_config()
    
    def get_headers(self) -> Dict[str, str]:
        provider = self.get_provider()
        headers = {"Content-Type": "application/json"}
        
        api_key = self.get_api_key()
        if api_key:
            if provider == "openai":
                headers["Authorization"] = f"Bearer {api_key}"
            elif provider == "anthropic":
                headers["x-api-key"] = api_key
                headers["anthropic-version"] = "2023-06-01"
        
        return headers
    
    def build_payload(self, messages: list, temperature: float = 0.7, max_tokens: int = 2000) -> Dict:
        provider = self.get_provider()
        model = self.get_model()
        
        if provider == "anthropic":
            return {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens
            }
        else:
            return {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
    
    def parse_response(self, response_data: Dict) -> Optional[str]:
        provider = self.get_provider()
        
        try:
            if provider == "anthropic":
                return response_data.get("content", [{}])[0].get("text", "")
            else:
                return response_data["choices"][0]["message"]["content"]
        except Exception:
            return None
