import os
import sys
import shutil
import tempfile
import unittest

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from core.acceptance import AcceptanceManager  # noqa: E402


class TestAcceptanceManager(unittest.TestCase):
    def setUp(self):
        self.project_dir = tempfile.mkdtemp()
        self.mgr = AcceptanceManager(self.project_dir)

    def tearDown(self):
        shutil.rmtree(self.project_dir, ignore_errors=True)

    def _analysis(self, criteria):
        return {
            "success": True,
            "analysis": {
                "requirement_breakdown": [],
                "functional_specs": [],
                "technical_requirements": [],
                "acceptance_criteria": criteria,
            },
        }

    def test_analyze_acceptance_criteria(self):
        criteria = self.mgr._analyze_acceptance_criteria(self._analysis(["功能正常", "性能达标"]))
        self.assertEqual(len(criteria), 2)
        self.assertEqual(criteria[0]["id"], 1)
        self.assertEqual(criteria[0]["description"], "功能正常")
        self.assertEqual(criteria[0]["status"], "待验证")

    def test_analyze_criteria_failed_analysis(self):
        criteria = self.mgr._analyze_acceptance_criteria({"success": False})
        self.assertEqual(criteria, [])

    def test_verify_tests_all_pass(self):
        test_results = {
            "success": True,
            "unit_tests": {"success": True},
            "boundary_tests": {"success": True},
            "integration_tests": {"success": True},
        }
        verification = self.mgr._verify_tests(test_results)
        self.assertTrue(verification["all_tests"])

    def test_verify_tests_some_fail(self):
        test_results = {
            "success": True,
            "unit_tests": {"success": True},
            "boundary_tests": {"success": False},
            "integration_tests": {"success": True},
        }
        verification = self.mgr._verify_tests(test_results)
        self.assertFalse(verification["all_tests"])

    def test_verify_tests_overall_failure(self):
        verification = self.mgr._verify_tests({"success": False})
        self.assertFalse(verification["all_tests"])

    def test_generate_acceptance_report_pass(self):
        analysis = self._analysis(["功能正常"])
        test_results = {
            "success": True,
            "unit_tests": {"success": True},
            "boundary_tests": {"success": True},
            "integration_tests": {"success": True},
        }
        result = self.mgr.generate_acceptance_report(analysis, test_results)
        self.assertTrue(result["success"])
        self.assertEqual(result["acceptance_status"], "通过")
        self.assertTrue(os.path.exists(result["report_path"]))
        with open(result["report_path"], encoding="utf-8") as f:
            content = f.read()
        self.assertIn("验收报告", content)
        self.assertIn("通过", content)

    def test_generate_acceptance_report_fail(self):
        analysis = self._analysis(["功能正常"])
        test_results = {
            "success": True,
            "unit_tests": {"success": False},
            "boundary_tests": {"success": False},
            "integration_tests": {"success": False},
        }
        result = self.mgr.generate_acceptance_report(analysis, test_results)
        self.assertTrue(result["success"])
        self.assertEqual(result["acceptance_status"], "未通过")

    def test_get_current_date_format(self):
        date_str = self.mgr._get_current_date()
        self.assertRegex(date_str, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")


if __name__ == "__main__":
    unittest.main()
