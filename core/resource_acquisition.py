import os
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any
from core.requirement_analysis import RequirementAnalyzer

class ResourceAcquirer:
    """
    资源获取模块，用于自动获取项目所需资源
    """
    
    def __init__(self, lm_studio_url="http://localhost:1234/v1/chat/completions"):
        """
        初始化资源获取器
        
        Args:
            lm_studio_url: LM Studio API地址
        """
        self.lm_studio_url = lm_studio_url
        self.analyzer = RequirementAnalyzer(lm_studio_url)
    
    def acquire_resources(self, requirements: str, output_dir: str) -> Dict[str, Any]:
        """
        获取项目所需资源
        
        Args:
            requirements: 用户需求文本
            output_dir: 资源输出目录
            
        Returns:
            Dict: 资源获取结果
        """
        try:
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 分析需求，确定所需资源
            resource_needs = self._identify_resource_needs(requirements)
            
            # 尝试从网络获取资源
            network_resources = self._crawl_resources(resource_needs, output_dir)
            
            # 对于未获取到的资源，尝试使用LM Studio创作
            missing_resources = [r for r in resource_needs if r not in network_resources]
            created_resources = []
            
            if missing_resources:
                created_resources = self._create_resources(missing_resources, output_dir)
            
            # 对于仍未获取到的资源，触发用户资源请求
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
        """
        识别项目所需资源
        
        Args:
            requirements: 用户需求文本
            
        Returns:
            List[str]: 资源需求列表
        """
        # 构建请求数据
        payload = {
            "model": "qwen2-0.5b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位专业的资源分析师，擅长识别项目所需的各类资源。请根据用户需求，识别出项目可能需要的所有资源，包括但不限于：图片、图标、文档、代码库、第三方依赖等。"
                },
                {
                    "role": "user",
                    "content": f"请识别以下项目需求中可能需要的资源：\n{requirements}"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        # 发送请求到LM Studio
        response = requests.post(
            self.lm_studio_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            resource_text = result["choices"][0]["message"]["content"]
            
            # 解析资源列表
            resources = []
            lines = resource_text.split("\n")
            for line in lines:
                line = line.strip()
                if line and line.startswith(("- ", "* ", "1.", "2.", "3.")):
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
        """
        爬取网络资源
        
        Args:
            resource_needs: 资源需求列表
            output_dir: 输出目录
            
        Returns:
            List[str]: 成功获取的资源列表
        """
        acquired_resources = []
        
        for resource in resource_needs:
            try:
                # 简单的网络爬虫实现
                # 实际项目中可能需要更复杂的爬虫逻辑
                print(f"尝试获取资源: {resource}")
                
                # 这里只是模拟爬虫行为
                # 实际项目中应该根据资源类型选择合适的爬虫策略
                acquired_resources.append(resource)
                
                # 创建一个占位文件
                resource_file = os.path.join(output_dir, f"{resource.replace(' ', '_')}.txt")
                with open(resource_file, 'w', encoding='utf-8') as f:
                    f.write(f"Resource: {resource}\nAcquired from web crawl")
                
            except Exception as e:
                print(f"获取资源 {resource} 失败: {e}")
        
        return acquired_resources
    
    def _create_resources(self, resource_needs: List[str], output_dir: str) -> List[str]:
        """
        使用LM Studio创作资源
        
        Args:
            resource_needs: 资源需求列表
            output_dir: 输出目录
            
        Returns:
            List[str]: 成功创作的资源列表
        """
        created_resources = []
        
        for resource in resource_needs:
            try:
                # 构建请求数据
                payload = {
                    "model": "qwen2-0.5b-instruct",
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一位专业的资源创作专家，擅长根据需求创建各类资源。请根据用户需求，创作所需的资源内容。"
                        },
                        {
                            "role": "user",
                            "content": f"请创作以下资源：\n{resource}"
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
                
                # 发送请求到LM Studio
                response = requests.post(
                    self.lm_studio_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    resource_content = result["choices"][0]["message"]["content"]
                    
                    # 保存创作的资源
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
        """
        触发用户资源请求
        
        Args:
            resource_needs: 资源需求列表
            
        Returns:
            List[str]: 用户提供的资源列表
        """
        user_provided = []
        
        print("以下资源无法自动获取，请用户提供：")
        for resource in resource_needs:
            print(f"- {resource}")
            # 实际项目中应该有更复杂的用户交互逻辑
            # 这里只是模拟用户提供资源
            user_provided.append(resource)
        
        return user_provided
