import os
import json
from typing import Dict, List, Any

class AcceptanceManager:
    """
    验收模块，用于生成验收报告，确认产品功能完整性与正确性
    """
    
    def __init__(self, project_dir):
        """
        初始化验收管理器
        
        Args:
            project_dir: 项目目录
        """
        self.project_dir = project_dir
    
    def generate_acceptance_report(self, requirement_analysis: Dict[str, Any], test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成验收报告
        
        Args:
            requirement_analysis: 需求分析结果
            test_results: 测试结果
            
        Returns:
            Dict: 验收结果
        """
        try:
            # 分析需求与测试结果
            acceptance_criteria = self._analyze_acceptance_criteria(requirement_analysis)
            test_verification = self._verify_tests(test_results)
            
            # 生成验收报告
            report = self._generate_report(acceptance_criteria, test_verification)
            
            # 保存验收报告
            report_path = os.path.join(self.project_dir, 'docs', 'acceptance_report.md')
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            # 确认验收状态
            acceptance_status = self._determine_acceptance_status(acceptance_criteria, test_verification)
            
            return {
                "success": True,
                "acceptance_status": acceptance_status,
                "report": report,
                "report_path": report_path
            }
            
        except Exception as e:
            return {
                "error": f"生成验收报告失败: {str(e)}",
                "success": False
            }
    
    def _analyze_acceptance_criteria(self, requirement_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        分析验收标准
        
        Args:
            requirement_analysis: 需求分析结果
            
        Returns:
            List[Dict]: 验收标准列表
        """
        if not requirement_analysis.get("success"):
            return []
        
        analysis = requirement_analysis.get("analysis", {})
        acceptance_criteria = analysis.get("acceptance_criteria", [])
        
        # 结构化验收标准
        criteria = []
        for i, criterion in enumerate(acceptance_criteria, 1):
            criteria.append({
                "id": i,
                "description": criterion,
                "status": "待验证"
            })
        
        return criteria
    
    def _verify_tests(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证测试结果
        
        Args:
            test_results: 测试结果
            
        Returns:
            Dict: 测试验证结果
        """
        if not test_results.get("success"):
            return{"unit_tests": False,"boundary_tests": False,"integration_tests" : False,"all_tests": False}
        
        unit_success = test_results.get("unit_tests", {}).get("success", False)
        boundary_success = test_results.get("boundary_tests", {}).get("success", False)
        integration_success = test_results.get("integration_tests", {}).get("success", False)
        
        all_tests = unit_success and boundary_success and integration_success
        
        return {
            "unit_tests": unit_success,
            "boundary_tests": boundary_success,
            "integration_tests": integration_success,
            "all_tests": all_tests
        }
    
    def _generate_report(self, acceptance_criteria: List[Dict[str, Any]], test_verification: Dict[str, Any]) -> str:
        """
        生成验收报告
        
        Args:
            acceptance_criteria: 验收标准列表
            test_verification: 测试验证结果
            
        Returns:
            str: 验收报告
        """
        # 生成Markdown格式的验收报告
        report = "# 验收报告\n\n"
        
        # 项目信息
        report += "## 项目信息\n"
        report += f"项目目录: {self.project_dir}\n"
        report += f"验收日期: {self._get_current_date()}\n"
        report += "\n"
        
        # 验收标准
        report += "## 验收标准\n"
        for criterion in acceptance_criteria:
            report += f"### 标准 {criterion['id']}\n"
            report += f"**描述**: {criterion['description']}\n"
            report += f"**状态**: {criterion['status']}\n\n"
        report += "\n"
        
        # 测试验证结果
        report += "## 测试验证结果\n"
        report += f"**单元测试**: {'通过' if test_verification.get('unit_tests') else '失败'}\n"
        report += f"**边界条件测试**: {'通过' if test_verification.get('boundary_tests') else '失败'}\n"
        report += f"**系统集成测试**: {'通过' if test_verification.get('integration_tests') else '失败'}\n"
        report += f"**所有测试**: {'通过' if test_verification.get('all_tests') else '失败'}\n"
        report += "\n"
        
        # 验收结论
        report += "## 验收结论\n"
        if test_verification.get('all_tests'):
            report += "项目通过验收，所有功能符合需求规格。\n"
        else:
            report += "项目未通过验收，部分功能不符合需求规格，需要进一步改进。\n"
        
        return report
    
    def _determine_acceptance_status(self, acceptance_criteria: List[Dict[str, Any]], test_verification: Dict[str, Any]) -> str:
        """
        确定验收状态
        
        Args:
            acceptance_criteria: 验收标准列表
            test_verification: 测试验证结果
            
        Returns:
            str: 验收状态
        """
        if test_verification.get('all_tests'):
            return "通过"
        else:
            return "未通过"
    
    def _get_current_date(self) -> str:
        """
        获取当前日期
        
        Returns:
            str: 当前日期
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
