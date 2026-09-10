import requests
from typing import Dict, List, Any
from utils.api_config import APIConfig


class AIClient:
    def __init__(self, config_path: str = None):
        self.config = APIConfig(config_path)

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 2000) -> Dict[str, Any]:
        try:
            url = self.config.get_api_url()
            headers = self.config.get_headers()
            payload = self.config.build_payload(messages, temperature, max_tokens)

            response = requests.post(url, json=payload, headers=headers, timeout=60)

            if response.status_code == 200:
                try:
                    result = response.json()
                except (ValueError, requests.exceptions.JSONDecodeError):
                    return {
                        "error": "API返回了无效的JSON响应",
                        "success": False
                    }
                content = self.config.parse_response(result)

                if content is None:
                    return {
                        "error": "无法解析API响应内容",
                        "success": False
                    }

                return {
                    "success": True,
                    "content": content
                }
            else:
                error_msg = response.text[:500] if response.text else f"HTTP {response.status_code}"
                return {
                    "error": f"API调用失败: {response.status_code} - {error_msg}",
                    "success": False
                }

        except requests.exceptions.ConnectionError:
            return {
                "error": "无法连接到API服务器，请检查网络和API地址",
                "success": False
            }
        except requests.exceptions.Timeout:
            return {
                "error": "API请求超时，请稍后重试",
                "success": False
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": f"API请求失败: {str(e)}",
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
