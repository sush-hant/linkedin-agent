import importlib.util
import tempfile
import unittest
from datetime import datetime, timezone

PYDANTIC_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if PYDANTIC_AVAILABLE:
    from app.adapters.storage.file_store import JsonFileStore
    from app.modules.feedback import FeedbackService
    from app.modules.post_generator import PostGenerator
    from app.modules.review import ReviewService
    from app.prompts.registry import FilePromptProvider
    from app.shared.schemas import ApprovalRequest, FeedbackEntry, TrendCandidate


@unittest.skipUnless(PYDANTIC_AVAILABLE, "pydantic is required for review/feedback tests")
class ReviewFeedbackTests(unittest.TestCase):
    def test_approve_and_record_feedback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = JsonFileStore(root_dir=__import__("pathlib").Path(tmp))
            trend = TrendCandidate(
                topic_id="topic1",
                title="AI Agents in Sales",
                summary="Rapid growth in AI SDR tooling",
                supporting_urls=["https://example.com/trend"],
                trend_score=0.9,
                generated_at=datetime.now(timezone.utc),
            )
            drafts = PostGenerator(FilePromptProvider(__import__("pathlib").Path("app/prompts"))).run([trend], 1)
            store.save_post_drafts(drafts)

            review = ReviewService(store)
            listed = review.list_drafts()
            self.assertGreater(len(listed), 0)

            published = review.approve(ApprovalRequest(draft_id=listed[0].draft_id))
            self.assertEqual(published.draft_id, listed[0].draft_id)

            feedback_service = FeedbackService(store)
            result_path = feedback_service.record(
                FeedbackEntry(
                    published_id=published.published_id,
                    impressions=100,
                    comments=5,
                    reposts=2,
                    saves=4,
                    quality="good",
                    notes="Great conversation quality",
                    recorded_at=datetime.now(timezone.utc),
                )
            )
            self.assertTrue(result_path.endswith(".json"))
            self.assertAlmostEqual(feedback_service.quality_multiplier("good"), 1.1)


if __name__ == "__main__":
    unittest.main()
