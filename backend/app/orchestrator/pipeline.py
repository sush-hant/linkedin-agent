from dataclasses import dataclass
from pathlib import Path

from app.adapters.storage.file_store import JsonFileStore
from app.adapters.vector.chroma_store import ChromaVectorStore
from app.shared.config import settings


@dataclass
class PipelineResult:
    status: str
    detail: str


class PipelineOrchestrator:
    """
    Phase 1 orchestration skeleton.

    Future phases can inject fetcher/ranker/generator modules through constructor
    without changing this public API.
    """

    def __init__(self) -> None:
        self.store = JsonFileStore(Path(settings.storage_root))
        self.vector_store = ChromaVectorStore(settings.chroma_path)

    def run(self) -> PipelineResult:
        return PipelineResult(
            status="ok",
            detail="Phase 1 skeleton ready: contracts, adapters, and prompt registry wired.",
        )
