from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class SourceItem(BaseModel):
    source: str
    title: str
    url: HttpUrl
    summary: str
    published_at: datetime
    fetched_at: datetime


class NormalizedItem(BaseModel):
    item_id: str
    source: str
    title: str
    url: HttpUrl
    summary: str
    published_at: datetime
    fetched_at: datetime
    topic_hint: str


class TrendCandidate(BaseModel):
    topic_id: str = Field(..., description="Stable topic identifier")
    title: str
    summary: str
    supporting_urls: list[HttpUrl]
    trend_score: float = Field(..., ge=0, le=1)
    generated_at: datetime


class PostDraft(BaseModel):
    draft_id: str
    topic_id: str
    style: str = Field(..., description="educational | contrarian | tactical")
    content: str
    hashtags: list[str]
    citations: list[HttpUrl]


class ImageDraft(BaseModel):
    image_id: str
    draft_id: str
    prompt: str
    file_path: str
    size: str = Field(default="1200x627")


class ApprovalRequest(BaseModel):
    draft_id: str
    edited_content: str | None = None


class PublishedPost(BaseModel):
    published_id: str
    draft_id: str
    topic_id: str
    content: str
    hashtags: list[str]
    citations: list[HttpUrl]
    approved_at: datetime


class FeedbackEntry(BaseModel):
    published_id: str
    impressions: int = 0
    comments: int = 0
    reposts: int = 0
    saves: int = 0
    quality: Literal["poor", "average", "good"]
    notes: str = ""
    recorded_at: datetime
