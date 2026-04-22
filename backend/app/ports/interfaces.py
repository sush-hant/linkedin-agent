from abc import ABC, abstractmethod
from typing import Protocol

from app.shared.schemas import ImageDraft, PostDraft, TrendCandidate


class StoragePort(ABC):
    @abstractmethod
    def save_trend_candidates(self, items: list[TrendCandidate]) -> str:
        raise NotImplementedError

    @abstractmethod
    def save_post_drafts(self, items: list[PostDraft]) -> str:
        raise NotImplementedError

    @abstractmethod
    def save_image_drafts(self, items: list[ImageDraft]) -> str:
        raise NotImplementedError


class VectorStorePort(ABC):
    @abstractmethod
    def upsert_topics(self, items: list[TrendCandidate]) -> None:
        raise NotImplementedError


class PromptProviderPort(Protocol):
    def get(self, prompt_name: str) -> str:
        ...
