import json
import requests
from typing import Dict, List, Any

class RequirementAnalyzer:
    """
    需求分析模块，通过本地LM Studio服务对用户需求进行深度分析与拆解
    """
    
    def __init__(self, lm_studio_url="http://localhost:1234/v1/chat/completions"):
        """
        初始化需求分析器
        
        Args:
            lm_studio_url: LM Studio API地址
        """
        self.lm_studio_url = lm_studio_url
    
    def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """
        分析用户需求
        
        Args:
            requirements: 用户需求文本
            
        Returns:
            Dict: 分析结果，包含需求拆解、功能规格等
        """
        try:
            # 构建请求数据
            payload = {
                "model": "qwen2-0.5b-instruct",  # 使用LM Studio中加载的模型
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一位专业的需求分析师，擅长将用户需求拆解为详细的功能规格。请对用户提供的需求进行深度分析，包括：1. 需求拆解，2. 功能规格，3. 技术要求，4. 验收标准。"
                    },
                    {
                        "role": "user",
                        "content": f"请分析以下需求：\n{requirements}"
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            # 发送请求到LM Studio
            response = requests.post(
                self.lm_studio_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            # 解析响应
            if response.status_code == 200:
                result = response.json()
                analysis_text = result["choices"][0]["message"]["content"]
                
                # 解析分析结果
                analysis_result = self._parse_analysis(analysis_text)
                return analysis_result
            else:
                return {
                    "error": f"LM Studio API调用失败: {response.status_code}",
                    "success": False
                }
                
        except Exception as e:
            return {
                "error": f"需求分析失败: {str(e)}",
                "success": False
            }
    
    def _parse_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """
        解析分析结果文本
        
        Args:
            analysis_text: LM Studio返回的分析文本
            
        Returns:
            Dict: 结构化的分析结果
        """
        # 简单的解析逻辑，实际项目中可能需要更复杂的解析
        sections = {
            "requirement_breakdown": [],
            "functional_specs": [],
            "technical_requirements": [],
            "acceptance_criteria": []
        }
        
        # 按部分分割文本
        lines = analysis_text.split("\n")
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 识别部分标题
            if "需求拆解" in line or "Requirement Breakdown" in line:
                current_section = "requirement_breakdown"
            elif "功能规格" in line or "Functional Specs" in line:
                current_section = "functional_specs"
            elif "技术要求" in line or "Technical Requirements" in line:
                current_section = "technical_requirements"
            elif "验收标准" in line or "Acceptance Criteria" in line:
                current_section = "acceptance_criteria"
            elif current_section and line.startswith(("- ", "* ", "1.", "2.", "3.")):
                # 提取项目内容
                if line.startswith(("- ", "* ")):
                    item = line[2:]
                elif line[0].isdigit() and "." in line:
                    item = line.split(".", 1)[1].strip()
                else:
                    item = line
                
                sections[current_section].append(item)
        
        return {
            "success": True,
            "analysis": sections,
            "raw_analysis": analysis_text
        }
    
    def generate_requirement_document(self, analysis_result: Dict[str, Any], output_path: str):
        """
        生成需求文档
        
        Args:
            analysis_result: 分析结果
            output_path: 输出文件路径
        """
        if not analysis_result.get("success"):
            print("分析结果无效，无法生成需求文档")
            return False
        
        try:
            analysis = analysis_result.get("analysis", {})
            
            # 生成Markdown格式的需求文档
            document = "# 需求分析文档\n\n"
            
            # 需求拆解
            document += "## 需求拆解\n"
            for item in analysis.get("requirement_breakdown", []):
                document += f"- {item}\n"
            document += "\n"
            
            # 功能规格
            document += "## 功能规格\n"
            for item in analysis.get("functional_specs", []):
                document += f"- {item}\n"
            document += "\n"
            
            # 技术要求
            document += "## 技术要求\n"
            for item in analysis.get("technical_requirements", []):
                document += f"- {item}\n"
            document += "\n"
            
            # 验收标准
            document += "## 验收标准\n"
            for item in analysis.get("acceptance_criteria", []):
                document += f"- {item}\n"
            
            # 写入文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(document)
            
            return True
        except Exception as e:
            print(f"生成需求文档失败: {e}")
            return False
