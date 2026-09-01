import os
import json
from typing import Dict, List, Any


class DevelopmentManager:
    """
    开发实施模块，用于执行模块化规划和代码开发
    """

    def __init__(self, project_dir):
        """
        初始化开发管理器

        Args:
            project_dir: 项目目录
        """
        self.project_dir = project_dir
        self.src_dir = os.path.join(project_dir, 'src')

    def develop(self, requirement_analysis: Dict[str, Any]):
        """
        执行开发实施

        Args:
            requirement_analysis: 需求分析结果

        Returns:
            Dict: 开发结果
        """
        try:
            # 执行模块化规划
            modules = self._modularize(requirement_analysis)

            # 为每个模块生成伪代码
            pseudocode = self._generate_pseudocode(modules)

            # 按优先级顺序实现代码
            implementation = self._implement_code(modules, pseudocode)

            return {
                "success": True,
                "modules": modules,
                "pseudocode": pseudocode,
                "implementation": implementation
            }

        except Exception as e:
            return {
                "error": f"开发实施失败: {str(e)}",
                "success": False
            }

    def _modularize(self, requirement_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        执行模块化规划

        Args:
            requirement_analysis: 需求分析结果

        Returns:
            List[Dict]: 模块列表
        """
        if not requirement_analysis.get("success"):
            return []

        analysis = requirement_analysis.get("analysis", {})
        functional_specs = analysis.get("functional_specs", [])

        # 简单的模块化逻辑
        # 实际项目中可能需要更复杂的模块化策略
        modules = []
        module_id = 1

        for spec in functional_specs:
            module = {
                "id": module_id,
                "name": f"module_{module_id}",
                "description": spec,
                "priority": module_id,  # 简单的优先级分配
                "dependencies": []
            }
            modules.append(module)
            module_id += 1

        # 保存模块规划
        config_dir = os.path.join(self.project_dir, 'config')
        os.makedirs(config_dir, exist_ok=True)
        modules_path = os.path.join(config_dir, 'modules.json')
        with open(modules_path, 'w', encoding='utf-8') as f:
            json.dump(modules, f, indent=2, ensure_ascii=False)

        return modules

    def _generate_pseudocode(self, modules: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        为每个模块生成伪代码

        Args:
            modules: 模块列表

        Returns:
            Dict: 模块伪代码映射
        """
        pseudocode = {}

        for module in modules:
            module_name = module["name"]
            description = module["description"]

            # 生成伪代码
            code = f"""# {module_name}
# 功能: {description}

# 导入依赖
import ...

# 类定义
class {module_name.capitalize()}:
    def __init__(self):
        # 初始化
        pass

    def method1(self, param1, param2):
        # 方法1实现
        pass

    def method2(self):
        # 方法2实现
        pass

# 函数定义
def function1():
    # 函数1实现
    pass

def function2():
    # 函数2实现
    pass

# 主逻辑
if __name__ == "__main__":
    # 测试代码
    pass
"""

            pseudocode[module_name] = code

            # 保存伪代码文件
            pseudocode_dir = os.path.join(self.project_dir, 'docs', 'pseudocode')
            os.makedirs(pseudocode_dir, exist_ok=True)
            pseudocode_path = os.path.join(pseudocode_dir, f"{module_name}.txt")

            with open(pseudocode_path, 'w', encoding='utf-8') as f:
                f.write(code)

        return pseudocode

    def _implement_code(self, modules: List[Dict[str, Any]], pseudocode: Dict[str, str]) -> Dict[str, str]:
        implementation = {}

        sorted_modules = sorted(modules, key=lambda x: x["priority"])

        core_dir = os.path.join(self.src_dir, 'core')
        utils_dir = os.path.join(self.src_dir, 'utils')
        api_dir = os.path.join(self.src_dir, 'api')
        ui_dir = os.path.join(self.src_dir, 'ui')
        os.makedirs(core_dir, exist_ok=True)
        os.makedirs(utils_dir, exist_ok=True)
        os.makedirs(api_dir, exist_ok=True)
        os.makedirs(ui_dir, exist_ok=True)
        os.makedirs(self.src_dir, exist_ok=True)

        # 确保所有包目录有__init__.py
        for d in [self.src_dir, core_dir, utils_dir, api_dir, ui_dir]:
            init_path = os.path.join(d, '__init__.py')
            if not os.path.exists(init_path):
                with open(init_path, 'w', encoding='utf-8') as f:
                    pass

        for module in sorted_modules:
            module_name = module["name"]
            module_path = os.path.join(core_dir, f"{module_name}.py")
            description = module.get("description", f"Module {module_name}")

            code = self._generate_module_code(module_name, description, pseudocode.get(module_name, ""))

            with open(module_path, 'w', encoding='utf-8') as f:
                f.write(code)

            implementation[module_name] = module_path
            print(f"已实现模块: {module_name}")

        init_path = os.path.join(core_dir, '__init__.py')
        existing_init_content = ""
        if os.path.exists(init_path):
            # 读取现有内容，保留用户的手工编辑
            try:
                with open(init_path, 'r', encoding='utf-8') as f:
                    existing_init_content = f.read()
            except Exception:
                pass

        # 生成新导出列表
        new_imports = []
        new_exports = []
        for module in modules:
            module_name = module["name"]
            class_name = ''.join(word.capitalize() for word in module_name.split('_'))
            # 只导出新模块，避免重复
            if class_name not in existing_init_content:
                new_imports.append(f"from .{module_name} import {class_name}")
            new_exports.append(class_name)

        if existing_init_content and not existing_init_content.strip().startswith('# AUTO'):
            # 有用户手工编辑过的内容，追加新模块
            extra = "\n" + "\n".join(new_imports) + "\n\n"
            # 更新 __all__ 列表
            all_start = existing_init_content.find('__all__')
            if all_start != -1:
                before = existing_init_content[:all_start]
                all_line_start = existing_init_content.find('[', all_start)
                all_line_end = existing_init_content.find(']', all_line_start)
                if all_line_end != -1:
                    old_exports_str = existing_init_content[all_line_start:all_line_end + 1]
                    # 合并导出
                    try:
                        import ast
                        old_exports = ast.literal_eval(old_exports_str)
                        merged = list(dict.fromkeys(list(old_exports) + new_exports))
                        new_all_line = f"__all__ = {merged}\n"
                        existing_init_content = before + new_all_line
                    except Exception:
                        # 无法解析则直接追加
                        existing_init_content += "\n" + "\n".join(new_imports) + f"\n__all__ = {new_exports}\n"
            else:
                existing_init_content += "\n" + "\n".join(new_imports) + f"\n__all__ = {new_exports}\n"
            final_content = existing_init_content
        else:
            # 是自动生成的，可以覆盖
            final_content = "# AUTO-GENERATED by gocode - do not edit manually\n"
            final_content += "\n".join(new_imports)
            final_content += f"\n__all__ = {new_exports}\n"

        with open(init_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        main_path = os.path.join(self.src_dir, 'main.py')
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_main_file(modules))

        return implementation

    def _generate_module_code(self, module_name: str, description: str, pseudocode: str) -> str:
        class_name = ''.join(word.capitalize() for word in module_name.split('_'))
        docstring = description if description else f"AUTO-GENERATED: Module {module_name}"

        method_names = self._extract_method_names(pseudocode)

        code = f'"""{docstring}"""\n\n'
        code += 'from typing import Any, Dict, List, Optional\n\n\n'
        code += f'class {class_name}:\n'
        code += f'    """{docstring}"""\n\n'
        code += f'    def __init__(self, **kwargs: Any) -> None:\n'
        code += f'        self.config = kwargs\n'
        code += f'        self._initialized = False\n'
        code += f'        self._data: Dict[str, Any] = {{}}\n\n'

        if method_names:
            for i, method_name in enumerate(method_names):
                code += f'    def {method_name}(self, *args: Any, **kwargs: Any) -> Any:\n'
                code += f'        """TODO: Implement {method_name} for {module_name}."""\n'
                code += f'        raise NotImplementedError(\n'
                code += f'            f"{class_name}.{method_name}() is not implemented yet"\n'
                code += f'        )\n\n'
        else:
            code += f'    def execute(self, *args: Any, **kwargs: Any) -> Any:\n'
            code += f'        """Main execution method for {module_name}."""\n'
            code += f'        raise NotImplementedError(\n'
            code += f'            f"{class_name}.execute() is not implemented yet"\n'
            code += f'        )\n\n'

        code += f'\n\ndef create_{module_name}(**kwargs: Any) -> "{class_name}":\n'
        code += f'    """Factory function for {module_name}."""\n'
        code += f'    return {class_name}(**kwargs)\n'

        return code

    def _extract_method_names(self, pseudocode: str) -> List[str]:
        methods = []
        for line in pseudocode.split('\n'):
            stripped = line.strip()
            if stripped.startswith('def ') and '(' in stripped:
                method_name = stripped[4:stripped.index('(')].strip()
                if method_name and method_name not in methods and method_name != '__init__':
                    methods.append(method_name)
        return methods

    def _generate_main_file(self, modules: List[Dict[str, Any]]) -> str:
        import_lines = []
        instantiations = []
        for module in modules:
            class_name = ''.join(word.capitalize() for word in module['name'].split('_'))
            import_lines.append(f'from src.core.{module["name"]} import {class_name}')
            instantiations.append(f'{class_name}()')

        imports_str = '\n'.join(import_lines)
        init_str = ', '.join(instantiations)

        return f'''"""Main entry point - AUTO-GENERATED by gocode."""

import os
import sys

# Ensure project root is on sys.path when running this file directly
# Supports both: `python -m src.main` (from project root) and `python src/main.py`
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_CURRENT_DIR)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

{imports_str}


def main():
    """Initialize and run all modules."""
    modules = [{init_str}]

    for module in modules:
        print(f"Initialized: {{type(module).__name__}}")

    print("All modules initialized successfully.")


if __name__ == "__main__":
    main()
'''