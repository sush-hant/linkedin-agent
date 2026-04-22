import importlib.util
import json
import unittest
from unittest.mock import patch

PYDANTIC_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if PYDANTIC_AVAILABLE:
    from app.adapters.llm.openai_client import OpenAIClient


@unittest.skipUnless(PYDANTIC_AVAILABLE, "pydantic is required for llm adapter tests")
class LLMAdapterTests(unittest.TestCase):
    @patch("app.adapters.llm.openai_client.request.urlopen")
    def test_openai_client_parses_response(self, mock_urlopen) -> None:
        class _Resp:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                return False

            def read(self):
                return json.dumps({"choices": [{"message": {"content": "hello"}}]}).encode("utf-8")

        mock_urlopen.return_value = _Resp()
        client = OpenAIClient(api_key="test", model="gpt-4o-mini")
        out = client.generate_post("sys", "user")
        self.assertEqual(out, "hello")


if __name__ == "__main__":
    unittest.main()
