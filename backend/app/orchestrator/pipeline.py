from pathlib import Path
from dataclasses import dataclass
from app.adapters.source.static_client import StaticSourceClient
from app.adapters.storage.file_store import JsonFileStore
from app.adapters.vector.chroma_store import ChromaVectorStore
from app.modules.fetcher import SourceFetcher
from app.modules.image_generator import ImageGenerator
from app.modules.normalizer import NormalizerDeduper
from app.modules.post_generator import PostGenerator
from app.modules.ranker import TrendRanker
from app.prompts.registry import FilePromptProvider
from app.shared.config import settings


@dataclass
class PipelineResult:
    status: str
    detail: str
    raw_count: int
    normalized_count: int
    trend_count: int
    post_count: int
    image_count: int


class PipelineOrchestrator:
    def __init__(self) -> None:
        self.store = JsonFileStore(settings.storage_path)
        self.vector_store = ChromaVectorStore(settings.chroma_path)
        self.fetcher = SourceFetcher(clients=[StaticSourceClient()])
        self.normalizer = NormalizerDeduper()
        self.ranker = TrendRanker(audience_keywords=["agent", "ai", "llm", "automation"])
        self.post_generator = PostGenerator(FilePromptProvider(Path("app/prompts")))
        self.image_generator = ImageGenerator()

    def run(self) -> PipelineResult:
        raw_items = self.fetcher.run()
        normalized_items = self.normalizer.run(raw_items)
        trends = self.ranker.run(normalized_items)
        posts = self.post_generator.run(trends)
        images = self.image_generator.run(posts)

        self.store.save_raw_items(raw_items)
        self.store.save_normalized_items(normalized_items)
        self.store.save_trend_candidates(trends)
        self.store.save_post_drafts(posts)
        self.store.save_image_drafts(images)
        self.vector_store.upsert_topics(trends)

        return PipelineResult(
            status="ok",
            detail="Phase 2+3 baseline pipeline completed.",
            raw_count=len(raw_items),
            normalized_count=len(normalized_items),
            trend_count=len(trends),
            post_count=len(posts),
            image_count=len(images),
        )
