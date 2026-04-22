import importlib.util
import unittest

PYDANTIC_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if PYDANTIC_AVAILABLE:
    from datetime import datetime, timedelta, timezone
    from pathlib import Path

    from app.modules.image_generator import ImageGenerator
    from app.modules.normalizer import NormalizerDeduper
    from app.modules.post_generator import PostGenerator
    from app.modules.ranker import TrendRanker
    from app.prompts.registry import FilePromptProvider
    from app.shared.schemas import SourceItem, TrendCandidate


class _FakeLLM:
    def __init__(self) -> None:
        self.last_user_prompt = ""

    def generate_post(self, system_prompt: str, user_prompt: str) -> str:
        _ = system_prompt
        self.last_user_prompt = user_prompt
        return f"LLM_OUTPUT::{user_prompt[:30]}"


@unittest.skipUnless(PYDANTIC_AVAILABLE, "pydantic is required for module tests")
class ModuleTests(unittest.TestCase):
    def test_normalizer_dedupes_duplicate_title_and_url(self) -> None:
        now = datetime.now(timezone.utc)
        item = SourceItem(
            source="s1",
            title="AI Agents are growing",
            url="https://example.com/a",
            summary="x",
            published_at=now,
            fetched_at=now,
        )
        items = [item, item]
        normalized = NormalizerDeduper().run(items)
        self.assertEqual(len(normalized), 1)

    def test_ranker_orders_recent_higher(self) -> None:
        now = datetime.now(timezone.utc)
        source_items = [
            SourceItem(
                source="s1",
                title="AI Agent release",
                url="https://example.com/new",
                summary="agent update",
                published_at=now - timedelta(hours=2),
                fetched_at=now,
            ),
            SourceItem(
                source="s1",
                title="Older AI note",
                url="https://example.com/old",
                summary="ai old",
                published_at=now - timedelta(hours=48),
                fetched_at=now,
            ),
        ]
        normalized = NormalizerDeduper().run(source_items)
        ranker = TrendRanker(audience_keywords=["ai", "agent"])
        ranked = ranker.run(normalized)
        self.assertGreaterEqual(ranked[0].trend_score, ranked[1].trend_score)

        # novelty impact: many related ids should reduce score
        low_novelty = ranker.run(normalized, related_lookup=lambda _text: ["x1", "x2", "x3", "x4", "x5"])
        self.assertLessEqual(low_novelty[0].trend_score, ranked[0].trend_score)

    def test_post_and_image_generators(self) -> None:
        now = datetime.now(timezone.utc)
        trend = TrendCandidate(
            topic_id="t1",
            title="AI Agents for GTM",
            summary="new wave",
            supporting_urls=["https://example.com/t"],
            trend_score=0.8,
            generated_at=now,
        )
        provider = FilePromptProvider(Path("app/prompts"))
        fake_llm = _FakeLLM()
        drafts = PostGenerator(provider, llm_client=fake_llm).run(
            [trend],
            max_topics=1,
            related_topics={"t1": ["a1", "a2"]},
        )
        self.assertEqual(len(drafts), 3)
        self.assertTrue(drafts[0].content.startswith("LLM_OUTPUT::"))
        self.assertIn("Related trend ids: a1, a2", fake_llm.last_user_prompt)

        images = ImageGenerator().run(drafts)
        self.assertEqual(len(images), 3)


if __name__ == "__main__":
    unittest.main()
