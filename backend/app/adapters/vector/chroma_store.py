import hashlib
import json
import os
from dataclasses import dataclass
from time import sleep
from urllib import request

from app.ports.interfaces import VectorStorePort
from app.shared.schemas import TrendCandidate


@dataclass
class ChromaVectorStore(VectorStorePort):
    persist_directory: str
    collection_name: str = "trend_topics"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

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

    def _deterministic_embed(self, text: str, dim: int = 64) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values = list(digest)
        vector = []
        while len(vector) < dim:
            for val in values:
                vector.append(val / 255.0)
                if len(vector) == dim:
                    break
        return vector

    def _openai_embed(self, text: str) -> list[float]:
        payload = {
            "model": self.embedding_model,
            "input": text,
        }

        last_error: Exception | None = None
        for attempt in range(3):
            try:
                req = request.Request(
                    url="https://api.openai.com/v1/embeddings",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {self.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                    method="POST",
                )
                with request.urlopen(req, timeout=30) as resp:  # noqa: S310
                    body = json.loads(resp.read().decode("utf-8"))
                return body["data"][0]["embedding"]
            except Exception as exc:
                last_error = exc
                if attempt < 2:
                    sleep(0.5 * (attempt + 1))

        if last_error:
            raise last_error
        raise RuntimeError("Embedding generation failed")

    def _embed_text(self, text: str, dim: int = 64) -> list[float]:
        if self.openai_api_key:
            try:
                return self._openai_embed(text)
            except Exception:
                pass
        return self._deterministic_embed(text, dim)

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
