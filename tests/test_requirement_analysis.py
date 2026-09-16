import os
import sys
import unittest

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from core.requirement_analysis import RequirementAnalyzer  # noqa: E402


class TestRequirementParser(unittest.TestCase):
    def setUp(self):
        self.analyzer = RequirementAnalyzer.__new__(RequirementAnalyzer)

    def test_parse_with_all_sections(self):
        text = (
            "需求拆解\n"
            "- 用户登录\n"
            "- 数据展示\n"
            "功能规格\n"
            "1. 支持邮箱登录\n"
            "2. 支持密码重置\n"
            "技术要求\n"
            "- Python 3.8+\n"
            "验收标准\n"
            "* 登录成功率99%\n"
        )
        result = self.analyzer._parse_analysis(text)
        self.assertTrue(result["success"])
        analysis = result["analysis"]
        self.assertEqual(analysis["requirement_breakdown"], ["用户登录", "数据展示"])
        self.assertEqual(analysis["functional_specs"], ["支持邮箱登录", "支持密码重置"])
        self.assertEqual(analysis["technical_requirements"], ["Python 3.8+"])
        self.assertEqual(analysis["acceptance_criteria"], ["登录成功率99%"])

    def test_parse_no_sections_fallback(self):
        text = "这是一段没有明确章节的分析内容。"
        result = self.analyzer._parse_analysis(text)
        self.assertTrue(result["success"])
        self.assertEqual(result["analysis"]["requirement_breakdown"], [text])

    def test_parse_empty(self):
        result = self.analyzer._parse_analysis("")
        self.assertTrue(result["success"])
        # Empty text with no sections -> fallback to raw text (empty)
        self.assertIn("raw_analysis", result)

    def test_generate_requirement_document(self, tmp_path=None):
        import tempfile
        result = {
            "success": True,
            "analysis": {
                "requirement_breakdown": ["登录"],
                "functional_specs": ["邮箱登录"],
                "technical_requirements": ["Python"],
                "acceptance_criteria": ["成功"],
            },
        }
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            out = f.name
        try:
            ok = self.analyzer.generate_requirement_document(result, out)
            self.assertTrue(ok)
            with open(out, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("需求分析文档", content)
            self.assertIn("邮箱登录", content)
        finally:
            os.unlink(out)

    def test_generate_document_failure_on_bad_result(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            out = f.name
        try:
            ok = self.analyzer.generate_requirement_document({"success": False}, out)
            self.assertFalse(ok)
        finally:
            os.unlink(out)


if __name__ == "__main__":
    unittest.main()
