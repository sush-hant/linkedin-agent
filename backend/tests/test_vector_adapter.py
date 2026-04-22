import importlib.util
import unittest

PYDANTIC_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if PYDANTIC_AVAILABLE:
    from datetime import datetime, timezone

    from app.adapters.vector.chroma_store import ChromaVectorStore
    from app.shared.schemas import TrendCandidate


@unittest.skipUnless(PYDANTIC_AVAILABLE, "pydantic is required for vector adapter tests")
class VectorAdapterTests(unittest.TestCase):
    def test_embed_shape_is_stable(self) -> None:
        store = ChromaVectorStore("chroma-test")
        vec = store._embed_text("hello world", dim=64)
        self.assertEqual(len(vec), 64)

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
