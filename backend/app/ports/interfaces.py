from abc import ABC, abstractmethod
from typing import Protocol

from app.shared.schemas import (
    ApprovalRequest,
    FeedbackEntry,
    ImageDraft,
    NormalizedItem,
    PostDraft,
    PublishedPost,
    SourceItem,
    TrendCandidate,
)


class StoragePort(ABC):
    @abstractmethod
    def save_raw_items(self, items: list[SourceItem]) -> str:
        raise NotImplementedError

    @abstractmethod
    def save_normalized_items(self, items: list[NormalizedItem]) -> str:
        raise NotImplementedError

    @abstractmethod
    def save_trend_candidates(self, items: list[TrendCandidate]) -> str:
        raise NotImplementedError

    @abstractmethod
    def save_post_drafts(self, items: list[PostDraft]) -> str:
        raise NotImplementedError

    @abstractmethod
    def save_image_drafts(self, items: list[ImageDraft]) -> str:
        raise NotImplementedError

    @abstractmethod
    def read_latest_post_drafts(self) -> list[PostDraft]:
        raise NotImplementedError

    @abstractmethod
    def save_published_post(self, post: PublishedPost) -> str:
        raise NotImplementedError

    @abstractmethod
    def save_feedback(self, feedback: FeedbackEntry) -> str:
        raise NotImplementedError


class VectorStorePort(ABC):
    @abstractmethod
    def upsert_topics(self, items: list[TrendCandidate]) -> None:
        raise NotImplementedError


class SourceClientPort(Protocol):
    def fetch(self) -> list[SourceItem]:
        ...


class PromptProviderPort(Protocol):
    def get(self, prompt_name: str) -> str:
        ...
