import os
import requests
from typing import Dict, List, Any
from utils.ai_client import AIClient

class ResourceAcquirer:
    def __init__(self, config_path: str = None):
        self.ai_client = AIClient(config_path)
    
    def acquire_resources(self, requirements: str, output_dir: str) -> Dict[str, Any]:
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            resource_needs = self._identify_resource_needs(requirements)
            network_resources = self._crawl_resources(resource_needs, output_dir)
            
            missing_resources = [r for r in resource_needs if r not in network_resources]
            created_resources = []
            
            if missing_resources:
                created_resources = self._create_resources(missing_resources, output_dir)
            
            still_missing = [r for r in missing_resources if r not in created_resources]
            user_provided_resources = []
            
            if still_missing:
                user_provided_resources = self._request_user_resources(still_missing)
            
            return {
                "success": True,
                "network_resources": network_resources,
                "created_resources": created_resources,
                "user_provided_resources": user_provided_resources,
                "missing_resources": still_missing
            }
            
        except Exception as e:
            return {
                "error": f"资源获取失败: {str(e)}",
                "success": False
            }
    
    def _identify_resource_needs(self, requirements: str) -> List[str]:
        messages = [
            {
                "role": "system",
                "content": "你是一位专业的资源分析师，擅长识别项目所需的各类资源。请根据用户需求，识别出项目可能需要的所有资源，包括但不限于：图片、图标、文档、代码库、第三方依赖等。"
            },
            {
                "role": "user",
                "content": f"请识别以下项目需求中可能需要的资源：\n{requirements}"
            }
        ]
        
        result = self.ai_client.chat(messages, max_tokens=1000)
        
        if result.get("success"):
            resource_text = result["content"]
            resources = []
            lines = resource_text.split("\n")
            for line in lines:
                line = line.strip()
                if line and (line.startswith(("- ", "* ")) or (line[:1].isdigit() and "." in line[:3])):
                    if line.startswith(("- ", "* ")):
                        resource = line[2:]
                    elif line[0].isdigit() and "." in line:
                        resource = line.split(".", 1)[1].strip()
                    else:
                        resource = line
                    resources.append(resource)
            
            return resources
        else:
            return []
    
    def _crawl_resources(self, resource_needs: List[str], output_dir: str) -> List[str]:
        acquired_resources = []
        
        for resource in resource_needs:
            try:
                print(f"尝试获取资源: {resource}")
                
                resource_file = os.path.join(output_dir, f"{resource.replace(' ', '_').replace('/', '_')}.txt")
                
                try:
                    search_url = f"https://www.google.com/search?q={requests.utils.quote(resource + ' tutorial documentation')}"
                    headers = {"User-Agent": "Mozilla/5.0 (compatible; gocode-bot/1.0)"}
                    response = requests.get(search_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200 and len(response.text) > 100:
                        with open(resource_file, 'w', encoding='utf-8') as f:
                            f.write(f"Resource: {resource}\n")
                            f.write(f"Source: web search\n")
                            f.write(f"Status: Found reference content online\n")
                        acquired_resources.append(resource)
                        print(f"  成功获取资源: {resource}")
                    else:
                        with open(resource_file, 'w', encoding='utf-8') as f:
                            f.write(f"Resource: {resource}\n")
                            f.write(f"Source: placeholder (web search unavailable)\n")
                            f.write(f"Note: Web search returned no results, will attempt AI generation\n")
                        print(f"  网络搜索无结果，将由AI补充: {resource}")
                except requests.RequestException:
                    with open(resource_file, 'w', encoding='utf-8') as f:
                        f.write(f"Resource: {resource}\n")
                        f.write(f"Source: placeholder (network unavailable)\n")
                        f.write(f"Note: Network access failed, will attempt AI generation\n")
                    print(f"  网络不可用，将由AI补充: {resource}")
                
            except Exception as e:
                print(f"获取资源 {resource} 失败: {e}")
        
        return acquired_resources
    
    def _create_resources(self, resource_needs: List[str], output_dir: str) -> List[str]:
        created_resources = []
        
        for resource in resource_needs:
            try:
                messages = [
                    {
                        "role": "system",
                        "content": "你是一位专业的资源创作专家，擅长根据需求创建各类资源。请根据用户需求，创作所需的资源内容。"
                    },
                    {
                        "role": "user",
                        "content": f"请创作以下资源：\n{resource}"
                    }
                ]
                
                result = self.ai_client.chat(messages, max_tokens=1000)
                
                if result.get("success"):
                    resource_content = result["content"]
                    
                    resource_file = os.path.join(output_dir, f"{resource.replace(' ', '_')}_created.txt")
                    with open(resource_file, 'w', encoding='utf-8') as f:
                        f.write(resource_content)
                    
                    created_resources.append(resource)
                    print(f"成功创作资源: {resource}")
                else:
                    print(f"创作资源 {resource} 失败: API调用失败")
                    
            except Exception as e:
                print(f"创作资源 {resource} 失败: {e}")
        
        return created_resources
    
    def _request_user_resources(self, resource_needs: List[str]) -> List[str]:
        user_provided = []
        
        print("以下资源无法自动获取，请用户提供：")
        for resource in resource_needs:
            print(f"- {resource}")
            user_provided.append(resource)
        
        return user_provided
    
    def set_provider(self, provider: str):
        self.ai_client.set_provider(provider)
    
    def configure_provider(self, provider: str, **kwargs):
        self.ai_client.configure(provider, **kwargs)
