import json
from typing import Dict, List, Any
from utils.ai_client import AIClient

class RequirementAnalyzer:
    def __init__(self, config_path: str = None):
        self.ai_client = AIClient(config_path)
    
    def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        try:
            messages = [
                {
                    "role": "system",
                    "content": "你是一位专业的需求分析师，擅长将用户需求拆解为详细的功能规格。请对用户提供的需求进行深度分析，包括：1. 需求拆解，2. 功能规格，3. 技术要求，4. 验收标准。"
                },
                {
                    "role": "user",
                    "content": f"请分析以下需求：\n{requirements}"
                }
            ]
            
            result = self.ai_client.chat(messages)
            
            if result.get("success"):
                analysis_text = result["content"]
                analysis_result = self._parse_analysis(analysis_text)
                return analysis_result
            else:
                return {
                    "error": result.get("error", "未知错误"),
                    "success": False
                }
                
        except Exception as e:
            return {
                "error": f"需求分析失败: {str(e)}",
                "success": False
            }
    
    def _parse_analysis(self, analysis_text: str) -> Dict[str, Any]:
        sections = {
            "requirement_breakdown": [],
            "functional_specs": [],
            "technical_requirements": [],
            "acceptance_criteria": []
        }
        
        lines = analysis_text.split("\n")
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if "需求拆解" in line or "Requirement Breakdown" in line:
                current_section = "requirement_breakdown"
            elif "功能规格" in line or "Functional Specs" in line:
                current_section = "functional_specs"
            elif "技术要求" in line or "Technical Requirements" in line:
                current_section = "technical_requirements"
            elif "验收标准" in line or "Acceptance Criteria" in line:
                current_section = "acceptance_criteria"
            elif current_section and line.startswith(("- ", "* ", "1.", "2.", "3.")):
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
        if not analysis_result.get("success"):
            print("分析结果无效，无法生成需求文档")
            return False
        
        try:
            analysis = analysis_result.get("analysis", {})
            
            document = "# 需求分析文档\n\n"
            
            document += "## 需求拆解\n"
            for item in analysis.get("requirement_breakdown", []):
                document += f"- {item}\n"
            document += "\n"
            
            document += "## 功能规格\n"
            for item in analysis.get("functional_specs", []):
                document += f"- {item}\n"
            document += "\n"
            
            document += "## 技术要求\n"
            for item in analysis.get("technical_requirements", []):
                document += f"- {item}\n"
            document += "\n"
            
            document += "## 验收标准\n"
            for item in analysis.get("acceptance_criteria", []):
                document += f"- {item}\n"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(document)
            
            return True
        except Exception as e:
            print(f"生成需求文档失败: {e}")
            return False
    
    def set_provider(self, provider: str):
        self.ai_client.set_provider(provider)
    
    def configure_provider(self, provider: str, **kwargs):
        self.ai_client.configure(provider, **kwargs)
