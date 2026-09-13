import os
import sys
import json
import shutil
import tempfile
import unittest

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from core.project_init import ProjectInitializer  # noqa: E402


class TestProjectInitializer(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.mkdtemp()
        self.project_name = "test_project"

    def tearDown(self):
        shutil.rmtree(self.workspace, ignore_errors=True)

    def test_initialize_creates_structure(self):
        init = ProjectInitializer(self.workspace, self.project_name)
        self.assertTrue(init.initialize())
        project_dir = os.path.join(self.workspace, self.project_name)
        for d in ["src", "tests", "docs", "config", "scripts", "assets"]:
            self.assertTrue(os.path.isdir(os.path.join(project_dir, d)), f"Missing dir: {d}")
        for d in ["core", "utils", "api", "ui"]:
            self.assertTrue(os.path.isdir(os.path.join(project_dir, "src", d)), f"Missing src subdir: {d}")

    def test_initialize_creates_package_inits(self):
        init = ProjectInitializer(self.workspace, self.project_name)
        init.initialize()
        project_dir = os.path.join(self.workspace, self.project_name)
        for sub in ["", "core", "utils", "api", "ui"]:
            init_path = os.path.join(project_dir, "src", sub, "__init__.py")
            self.assertTrue(os.path.exists(init_path), f"Missing __init__.py at src/{sub}")

    def test_initialize_creates_files(self):
        init = ProjectInitializer(self.workspace, self.project_name)
        init.initialize()
        project_dir = os.path.join(self.workspace, self.project_name)
        self.assertTrue(os.path.exists(os.path.join(project_dir, "README.md")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "requirements.txt")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "src", "main.py")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "config", "project_config.json")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, ".gitignore")))

    def test_project_config_content(self):
        init = ProjectInitializer(self.workspace, self.project_name)
        init.initialize()
        project_dir = os.path.join(self.workspace, self.project_name)
        with open(os.path.join(project_dir, "config", "project_config.json")) as f:
            config = json.load(f)
        self.assertEqual(config["project_name"], self.project_name)
        self.assertEqual(config["version"], "0.1.0")

    def test_git_initialized(self):
        init = ProjectInitializer(self.workspace, self.project_name)
        init.initialize()
        project_dir = os.path.join(self.workspace, self.project_name)
        self.assertTrue(os.path.isdir(os.path.join(project_dir, ".git")))


if __name__ == "__main__":
    unittest.main()
