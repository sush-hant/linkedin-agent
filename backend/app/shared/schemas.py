from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


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
