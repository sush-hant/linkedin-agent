import importlib.util
import json
import unittest
from unittest.mock import patch

PYDANTIC_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if PYDANTIC_AVAILABLE:
    from datetime import datetime, timezone

    from app.adapters.vector.chroma_store import ChromaVectorStore
    from app.shared.schemas import TrendCandidate


@unittest.skipUnless(PYDANTIC_AVAILABLE, "pydantic is required for vector adapter tests")
class VectorAdapterTests(unittest.TestCase):
    def test_embed_shape_is_stable(self) -> None:
        store = ChromaVectorStore("chroma-test", openai_api_key="")
        vec = store._embed_text("hello world", dim=64)
        self.assertEqual(len(vec), 64)

    @patch("app.adapters.vector.chroma_store.request.urlopen")
    def test_openai_embedding_path(self, mock_urlopen) -> None:
        class _Resp:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                return False

            def read(self):
                return json.dumps({"data": [{"embedding": [0.1, 0.2, 0.3]}]}).encode("utf-8")

        mock_urlopen.return_value = _Resp()
        store = ChromaVectorStore("chroma-test", openai_api_key="test-key")
        vec = store._embed_text("hello")
        self.assertEqual(vec, [0.1, 0.2, 0.3])

    def test_upsert_noop_when_unavailable(self) -> None:
        store = ChromaVectorStore("chroma-test")
        store.available = False
        trend = TrendCandidate(
            topic_id="t1",
            title="AI Agents",
            summary="Summary",
            supporting_urls=["https://example.com"],
            trend_score=0.9,
            generated_at=datetime.now(timezone.utc),
        )
        store.upsert_topics([trend])
        related = store.query_related("AI Agents", limit=3)
        self.assertEqual(related, [])


if __name__ == "__main__":
    unittest.main()
