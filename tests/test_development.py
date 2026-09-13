import os
import sys
import shutil
import tempfile
import unittest

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from core.development import DevelopmentManager  # noqa: E402


class TestDevelopmentManager(unittest.TestCase):
    def setUp(self):
        self.project_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.project_dir, ignore_errors=True)

    def _analysis(self, specs):
        return {
            "success": True,
            "analysis": {
                "requirement_breakdown": [],
                "functional_specs": specs,
                "technical_requirements": [],
                "acceptance_criteria": [],
            },
        }

    def test_modularize_creates_modules(self):
        mgr = DevelopmentManager(self.project_dir)
        modules = mgr._modularize(self._analysis(["创建用户", "删除用户"]))
        self.assertEqual(len(modules), 2)
        self.assertEqual(modules[0]["name"], "module_1")
        self.assertEqual(modules[1]["name"], "module_2")

    def test_modularize_empty(self):
        mgr = DevelopmentManager(self.project_dir)
        modules = mgr._modularize(self._analysis([]))
        self.assertEqual(modules, [])

    def test_generate_module_code_has_class(self):
        mgr = DevelopmentManager(self.project_dir)
        code = mgr._generate_module_code("user_manager", "用户管理", "")
        self.assertIn("class UserManager:", code)
        self.assertIn("def execute", code)
        self.assertIn("raise NotImplementedError", code)

    def test_generate_module_code_with_methods(self):
        pseudocode = "def method1(self, a):\n    pass\ndef method2(self):\n    pass"
        mgr = DevelopmentManager(self.project_dir)
        code = mgr._generate_module_code("m", "desc", pseudocode)
        self.assertIn("def method1", code)
        self.assertIn("def method2", code)

    def test_develop_creates_module_files(self):
        mgr = DevelopmentManager(self.project_dir)
        result = mgr.develop(self._analysis(["功能A", "功能B"]))
        self.assertTrue(result["success"])
        self.assertEqual(len(result["modules"]), 2)
        self.assertTrue(os.path.exists(os.path.join(self.project_dir, "src", "core", "module_1.py")))
        self.assertTrue(os.path.exists(os.path.join(self.project_dir, "src", "core", "module_2.py")))

    def test_develop_creates_main_py(self):
        mgr = DevelopmentManager(self.project_dir)
        mgr.develop(self._analysis(["功能A"]))
        main_path = os.path.join(self.project_dir, "src", "main.py")
        self.assertTrue(os.path.exists(main_path))
        with open(main_path) as f:
            content = f.read()
        self.assertIn("from src.core.module_1 import Module1", content)

    def test_develop_creates_init_exports(self):
        mgr = DevelopmentManager(self.project_dir)
        mgr.develop(self._analysis(["功能A", "功能B"]))
        init_path = os.path.join(self.project_dir, "src", "core", "__init__.py")
        with open(init_path) as f:
            content = f.read()
        self.assertIn("Module1", content)
        self.assertIn("Module2", content)

    def test_generated_module_compiles(self):
        mgr = DevelopmentManager(self.project_dir)
        mgr.develop(self._analysis(["功能A"]))
        module_path = os.path.join(self.project_dir, "src", "core", "module_1.py")
        with open(module_path) as f:
            code = f.read()
        compile(code, module_path, "exec")

    def test_extract_method_names(self):
        mgr = DevelopmentManager(self.project_dir)
        pseudo = "def foo(self):\n    pass\ndef bar(self, x):\n    pass\n    def baz(self):\n        pass"
        methods = mgr._extract_method_names(pseudo)
        self.assertEqual(methods, ["foo", "bar", "baz"])


if __name__ == "__main__":
    unittest.main()
