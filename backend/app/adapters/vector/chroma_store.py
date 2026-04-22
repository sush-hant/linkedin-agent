import hashlib
from dataclasses import dataclass

from app.ports.interfaces import VectorStorePort
from app.shared.schemas import TrendCandidate


@dataclass
class ChromaVectorStore(VectorStorePort):
    persist_directory: str
    collection_name: str = "trend_topics"

    def __post_init__(self) -> None:
        self.available = False
        self.collection = None
        try:
            import chromadb

            client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = client.get_or_create_collection(self.collection_name)
            self.available = True
        except Exception:
            # Keep pipeline functional even if chromadb dependency/runtime is unavailable.
            self.available = False

    def _embed_text(self, text: str, dim: int = 64) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values = list(digest)
        vector = []
        while len(vector) < dim:
            for val in values:
                vector.append(val / 255.0)
                if len(vector) == dim:
                    break
        return vector

    def upsert_topics(self, items: list[TrendCandidate]) -> None:
        if not self.available or not self.collection or not items:
            return

        ids = [item.topic_id for item in items]
        documents = [f"{item.title}\n{item.summary}" for item in items]
        embeddings = [self._embed_text(doc) for doc in documents]
        metadatas = [{"score": item.trend_score, "generated_at": str(item.generated_at)} for item in items]

        self.collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    def query_related(self, text: str, limit: int = 5) -> list[str]:
        if not self.available or not self.collection or not text.strip():
            return []

        result = self.collection.query(query_embeddings=[self._embed_text(text)], n_results=limit)
        ids = result.get("ids", [])
        return ids[0] if ids else []
