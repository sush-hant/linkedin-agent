from dataclasses import dataclass

from app.ports.interfaces import VectorStorePort
from app.shared.schemas import TrendCandidate


@dataclass
class ChromaVectorStore(VectorStorePort):
    persist_directory: str

    def upsert_topics(self, items: list[TrendCandidate]) -> None:
        """
        Phase 1 placeholder.

        Implementation in Phase 2:
        - initialize persistent Chroma client
        - upsert topic embeddings and metadata
        """
        _ = (self.persist_directory, items)
