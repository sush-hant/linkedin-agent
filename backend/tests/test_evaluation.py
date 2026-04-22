import importlib.util
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

PYDANTIC_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if PYDANTIC_AVAILABLE:
    from app.adapters.storage.file_store import JsonFileStore
    from app.modules.evaluation import EvaluationService
    from app.shared.schemas import FeedbackEntry, PublishedPost


@unittest.skipUnless(PYDANTIC_AVAILABLE, "pydantic is required for evaluation tests")
class EvaluationTests(unittest.TestCase):
    def test_summary_calculation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = JsonFileStore(Path(tmp))
            store.save_published_post(
                PublishedPost(
                    published_id="p1",
                    draft_id="d1",
                    topic_id="t1",
                    content="c",
                    hashtags=["#AI"],
                    citations=["https://example.com"],
                    approved_at=datetime.now(timezone.utc),
                )
            )
            store.save_feedback(
                FeedbackEntry(
                    published_id="p1",
                    impressions=100,
                    comments=5,
                    reposts=2,
                    saves=3,
                    quality="good",
                    notes="solid",
                    recorded_at=datetime.now(timezone.utc),
                )
            )

            summary = EvaluationService(store).summary()
            self.assertEqual(summary.total_published, 1)
            self.assertEqual(summary.total_feedback_entries, 1)
            self.assertEqual(summary.top_published_id, "p1")
            self.assertGreater(summary.avg_engagement_rate, 0)


if __name__ == "__main__":
    unittest.main()
