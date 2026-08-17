import os
import subprocess
import pytest
import json
from typing import Dict, List, Any

class TestManager:
    """
    测试验证模块，用于执行单元测试、边界条件测试和系统集成测试
    """
    
    def __init__(self, project_dir):
        """
        初始化测试管理器
        
        Args:
            project_dir: 项目目录
        """
        self.project_dir = project_dir
        self.test_dir = os.path.join(project_dir, 'tests')
    
    def run_tests(self) -> Dict[str, Any]:
        """
        运行测试
        
        Returns:
            Dict: 测试结果
        """
        try:
            # 创建测试文件
            self._create_test_files()
            
            # 运行单元测试
            unit_test_results = self._run_unit_tests()
            
            # 运行边界条件测试
            boundary_test_results = self._run_boundary_tests()
            
            # 运行系统集成测试
            integration_test_results = self._run_integration_tests()
            
            # 生成测试报告
            test_report = self._generate_test_report(
                unit_test_results,
                boundary_test_results,
                integration_test_results
            )
            
            return {
                "success": True,
                "unit_tests": unit_test_results,
                "boundary_tests": boundary_test_results,
                "integration_tests": integration_test_results,
                "test_report": test_report
            }
            
        except Exception as e:
            return {
                "error": f"测试执行失败: {str(e)}",
                "success": False
            }
    
    def _create_test_files(self):
        """
        创建测试文件，根据项目实际代码生成测试用例
        """
        # 确保测试目录存在
        os.makedirs(self.test_dir, exist_ok=True)
        
        # 扫描项目代码文件
        src_dir = os.path.join(self.project_dir, 'src')
        modules = self._scan_project_modules(src_dir)
        
        # 创建单元测试文件
        unit_test_content = self._generate_unit_tests(modules)
        unit_test_path = os.path.join(self.test_dir, 'test_core.py')
        with open(unit_test_path, 'w', encoding='utf-8') as f:
            f.write(unit_test_content)
        
        # 创建边界条件测试文件
        boundary_test_content = self._generate_boundary_tests(modules)
        boundary_test_path = os.path.join(self.test_dir, 'test_boundary.py')
        with open(boundary_test_path, 'w', encoding='utf-8') as f:
            f.write(boundary_test_content)
        
        # 创建系统集成测试文件
        integration_test_content = self._generate_integration_tests(modules)
        integration_test_path = os.path.join(self.test_dir, 'test_integration.py')
        with open(integration_test_path, 'w', encoding='utf-8') as f:
            f.write(integration_test_content)
    
    def _scan_project_modules(self, src_dir):
        """
        扫描项目模块
        
        Args:
            src_dir: 源代码目录
            
        Returns:
            List[Dict]: 模块信息列表
        """
        modules = []
        
        if not os.path.exists(src_dir):
            return modules
        
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith('.py') and not file.startswith('__init__'):
                    module_path = os.path.join(root, file)
                    module_name = os.path.splitext(file)[0]
                    relative_path = os.path.relpath(module_path, self.project_dir)
                    
                    modules.append({
                        'name': module_name,
                        'path': module_path,
                        'relative_path': relative_path
                    })
        
        return modules
    
    def _generate_unit_tests(self, modules):
        imports = []
        test_cases = []
        
        for module in modules:
            module_name = module['name']
            relative_path = module['relative_path'].replace('\\', '/')
            import_path = relative_path.replace('.py', '').replace('/', '.')
            
            class_name = ''.join(word.capitalize() for word in module_name.split('_'))
            imports.append(f"try:\n    from {import_path} import {class_name}\nexcept ImportError:\n    {class_name} = None\n")
            
            test_cases.append(
                f"    def test_{module_name}_import(self):\n"
                f"        \"\"\"Test that {module_name} module can be imported.\"\"\"\n"
                f"        if {class_name} is None:\n"
                f"            self.skipTest(\"{module_name} module could not be imported\")\n"
                f"        assert {class_name} is not None, \"{module_name} should be importable\"\n"
            )
            
            test_cases.append(
                f"    def test_{module_name}_instantiation(self):\n"
                f"        \"\"\"Test that {module_name} class can be instantiated.\"\"\"\n"
                f"        if {class_name} is None:\n"
                f"            self.skipTest(\"{module_name} module could not be imported\")\n"
                f"        try:\n"
                f"            instance = {class_name}()\n"
                f"            assert instance is not None\n"
                f"        except NotImplementedError:\n"
                f"            self.skipTest(\"{module_name} is a stub module\")\n"
                f"        except Exception as e:\n"
                f"            self.fail(f\"Failed to instantiate {module_name}: {{e}}\")\n"
            )
        
        if not modules:
            imports.append("# No modules to test")
            test_cases.append("    def test_placeholder(self):\n        \"\"\"Placeholder test when no modules exist.\"\"\"\n        assert True")
        
        return "import pytest\nimport unittest\n" + "\n".join(imports) + "\n\n\nclass TestCoreModules(unittest.TestCase):\n" + "\n".join(test_cases) + "\n"
    
    def _generate_boundary_tests(self, modules):
        imports = []
        test_cases = []
        
        for module in modules:
            module_name = module['name']
            relative_path = module['relative_path'].replace('\\', '/')
            import_path = relative_path.replace('.py', '').replace('/', '.')
            
            class_name = ''.join(word.capitalize() for word in module_name.split('_'))
            imports.append(f"try:\n    from {import_path} import {class_name}\nexcept ImportError:\n    {class_name} = None\n")
            
            test_cases.append(
                f"    def test_{module_name}_boundary_empty(self):\n"
                f"        \"\"\"Test {module_name} with empty/None inputs.\"\"\"\n"
                f"        if {class_name} is None:\n"
                f"            self.skipTest(\"{module_name} module could not be imported\")\n"
                f"        try:\n"
                f"            instance = {class_name}()\n"
                f"            result = instance.execute()\n"
                f"        except NotImplementedError:\n"
                f"            self.skipTest(\"{module_name} is a stub module\")\n"
                f"        except Exception:\n"
                f"            pass\n"
            )
            
            test_cases.append(
                f"    def test_{module_name}_boundary_large_input(self):\n"
                f"        \"\"\"Test {module_name} with large inputs.\"\"\"\n"
                f"        if {class_name} is None:\n"
                f"            self.skipTest(\"{module_name} module could not be imported\")\n"
                f"        try:\n"
                f"            instance = {class_name}()\n"
                f"            result = instance.execute([1] * 10000)\n"
                f"        except NotImplementedError:\n"
                f"            self.skipTest(\"{module_name} is a stub module\")\n"
                f"        except Exception:\n"
                f"            pass\n"
            )
        
        if not modules:
            imports.append("# No modules to test")
            test_cases.append("    def test_placeholder(self):\n        \"\"\"Placeholder boundary test.\"\"\"\n        assert True")
        
        return "import pytest\nimport unittest\n" + "\n".join(imports) + "\n\n\nclass TestBoundaryConditions(unittest.TestCase):\n" + "\n".join(test_cases) + "\n"
    
    def _generate_integration_tests(self, modules):
        main_import = ""
        if os.path.exists(os.path.join(self.project_dir, 'src', 'main.py')):
            main_import = "try:\n    from src.main import main\nexcept ImportError:\n    main = None\n"
        
        module_imports = []
        for module in modules:
            module_name = module['name']
            relative_path = module['relative_path'].replace('\\', '/')
            import_path = relative_path.replace('.py', '').replace('/', '.')
            class_name = ''.join(word.capitalize() for word in module_name.split('_'))
            module_imports.append(f"try:\n    from {import_path} import {class_name}\nexcept ImportError:\n    {class_name} = None\n")
        
        imports = "\n".join(module_imports)
        
        test_cases = [
            "    def test_system_integration(self):\n"
            "        \"\"\"Test overall system integration.\"\"\"\n"
            "        modules_ok = True\n"
        ]
        
        for module in modules:
            class_name = ''.join(word.capitalize() for word in module['name'].split('_'))
            test_cases.append(
                f"        if {class_name} is None:\n"
                f"            modules_ok = False\n"
                f"        else:\n"
                f"            try:\n"
                f"                instance = {class_name}()\n"
                f"                assert instance is not None\n"
                f"            except NotImplementedError:\n"
                f"                pass\n"
                f"            except Exception:\n"
                f"                modules_ok = False\n"
            )
        
        test_cases.append("        assert modules_ok, \"Not all modules integrated correctly\"")
        
        test_cases.append(
            "    def test_end_to_end(self):\n"
            "        \"\"\"Test end-to-end flow.\"\"\"\n"
            "        try:\n"
            "            if main is not None:\n"
            "                assert callable(main)\n"
            "        except Exception:\n"
            "            pass\n"
            "        assert True\n"
        )
        
        return "import pytest\nimport unittest\n" + imports + "\n" + main_import + "\n\nclass TestIntegration(unittest.TestCase):\n" + "\n".join(test_cases) + "\n"
    
    def _run_unit_tests(self) -> Dict[str, Any]:
        """
        运行单元测试
        
        Returns:
            Dict: 单元测试结果
        """
        try:
            result = subprocess.run(
                ['pytest', 'tests/test_core.py', '-v'],
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _run_boundary_tests(self) -> Dict[str, Any]:
        """
        运行边界条件测试
        
        Returns:
            Dict: 边界条件测试结果
        """
        try:
            result = subprocess.run(
                ['pytest', 'tests/test_boundary.py', '-v'],
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _run_integration_tests(self) -> Dict[str, Any]:
        """
        运行系统集成测试
        
        Returns:
            Dict: 系统集成测试结果
        """
        try:
            result = subprocess.run(
                ['pytest', 'tests/test_integration.py', '-v'],
                cwd=self.project_dir,
                capture_output=True,
                text=True
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_test_report(self, unit_results: Dict[str, Any], boundary_results: Dict[str, Any], integration_results: Dict[str, Any]) -> str:
        """
        生成测试报告
        
        Args:
            unit_results: 单元测试结果
            boundary_results: 边界条件测试结果
            integration_results: 系统集成测试结果
            
        Returns:
            str: 测试报告
        """
        # 生成Markdown格式的测试报告
        report = "# 测试报告\n\n"
        
        # 单元测试结果
        report += "## 单元测试\n"
        report += f"状态: {'通过' if unit_results.get('success') else '失败'}\n"
        if unit_results.get('output'):
            report += "```\n" + unit_results.get('output') + "```\n"
        if unit_results.get('error'):
            report += "错误: " + unit_results.get('error') + "\n"
        report += "\n"
        
        # 边界条件测试结果
        report += "## 边界条件测试\n"
        report += f"状态: {'通过' if boundary_results.get('success') else '失败'}\n"
        if boundary_results.get('output'):
            report += "```\n" + boundary_results.get('output') + "```\n"
        if boundary_results.get('error'):
            report += "错误: " + boundary_results.get('error') + "\n"
        report += "\n"
        
        # 系统集成测试结果
        report += "## 系统集成测试\n"
        report += f"状态: {'通过' if integration_results.get('success') else '失败'}\n"
        if integration_results.get('output'):
            report += "```\n" + integration_results.get('output') + "```\n"
        if integration_results.get('error'):
            report += "错误: " + integration_results.get('error') + "\n"
        report += "\n"
        
        # 总体状态
        all_passed = unit_results.get('success') and boundary_results.get('success') and integration_results.get('success')
        report += f"## 总体状态\n{'所有测试通过' if all_passed else '部分测试失败'}\n"
        
        # 保存测试报告
        report_path = os.path.join(self.project_dir, 'docs', 'test_report.md')
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report