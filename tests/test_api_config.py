import os
import sys
import json
import tempfile
import shutil
import unittest

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from utils.api_config import APIConfig, APIProvider  # noqa: E402


class TestAPIConfig(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.tmpdir, "api_config.json")
        self.sample_config = {
            "provider": "lmstudio",
            "openai": {"api_key": "sk-test", "base_url": "https://api.openai.com/v1", "model": "gpt-3.5-turbo"},
            "anthropic": {"api_key": "ant-test", "base_url": "https://api.anthropic.com", "model": "claude-3-sonnet"},
            "lmstudio": {"base_url": "http://localhost:1234/v1", "model": "qwen2-0.5b-instruct"},
            "ollama": {"base_url": "http://localhost:11434/v1", "model": "llama2"},
            "custom": {"base_url": "", "model": ""},
        }
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.sample_config, f)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_load_config_from_file(self):
        cfg = APIConfig(self.config_path)
        self.assertEqual(cfg.get_provider(), "lmstudio")

    def test_default_config_when_missing(self):
        missing = os.path.join(self.tmpdir, "nope.json")
        cfg = APIConfig(missing)
        self.assertEqual(cfg.get_provider(), "lmstudio")

    def test_set_provider_persists(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("openai")
        self.assertEqual(cfg.get_provider(), "openai")
        # Reload from disk to confirm persistence
        cfg2 = APIConfig(self.config_path)
        self.assertEqual(cfg2.get_provider(), "openai")

    def test_get_api_url_openai(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("openai")
        self.assertEqual(cfg.get_api_url(), "https://api.openai.com/v1/chat/completions")

    def test_get_api_url_anthropic(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("anthropic")
        self.assertEqual(cfg.get_api_url(), "https://api.anthropic.com/v1/messages")

    def test_get_api_url_ollama(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("ollama")
        self.assertEqual(cfg.get_api_url(), "http://localhost:11434/v1/chat/completions")

    def test_get_api_url_empty_base(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("custom")
        self.assertEqual(cfg.get_api_url(), "")

    def test_get_headers_with_api_key(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("openai")
        headers = cfg.get_headers()
        self.assertEqual(headers["Authorization"], "Bearer sk-test")
        self.assertEqual(headers["Content-Type"], "application/json")

    def test_get_headers_anthropic(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("anthropic")
        headers = cfg.get_headers()
        self.assertEqual(headers["x-api-key"], "ant-test")
        self.assertEqual(headers["anthropic-version"], "2023-06-01")

    def test_get_headers_no_api_key(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("lmstudio")
        headers = cfg.get_headers()
        self.assertNotIn("Authorization", headers)

    def test_parse_response_openai(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("openai")
        data = {"choices": [{"message": {"content": "hello"}}]}
        self.assertEqual(cfg.parse_response(data), "hello")

    def test_parse_response_anthropic(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("anthropic")
        data = {"content": [{"type": "text", "text": "hi"}]}
        self.assertEqual(cfg.parse_response(data), "hi")

    def test_parse_response_ollama_choices(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("ollama")
        data = {"choices": [{"message": {"content": "ollama hi"}}]}
        self.assertEqual(cfg.parse_response(data), "ollama hi")

    def test_parse_response_ollama_message_format(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("ollama")
        data = {"message": {"content": "legacy hi"}}
        self.assertEqual(cfg.parse_response(data), "legacy hi")

    def test_parse_response_invalid(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("openai")
        self.assertIsNone(cfg.parse_response("not a dict"))
        self.assertIsNone(cfg.parse_response({}))

    def test_build_payload(self):
        cfg = APIConfig(self.config_path)
        cfg.set_provider("openai")
        payload = cfg.build_payload([{"role": "user", "content": "hi"}], temperature=0.5, max_tokens=100)
        self.assertEqual(payload["model"], "gpt-3.5-turbo")
        self.assertEqual(payload["temperature"], 0.5)
        self.assertEqual(payload["max_tokens"], 100)

    def test_api_provider_enum(self):
        self.assertEqual(APIProvider.OPENAI.value, "openai")
        self.assertEqual(APIProvider.OLLAMA.value, "ollama")

    def test_set_api_config(self):
        cfg = APIConfig(self.config_path)
        cfg.set_api_config("lmstudio", model="new-model")
        self.assertEqual(cfg.get_model(), "new-model")


if __name__ == "__main__":
    unittest.main()
