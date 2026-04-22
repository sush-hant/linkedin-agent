from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256

from app.ports.interfaces import StoragePort
from app.shared.schemas import ApprovalRequest, ImageDraft, PostDraft, PublishedPost


@dataclass
class ReviewService:
    store: StoragePort

    def list_drafts(self) -> list[PostDraft]:
        return self.store.read_latest_post_drafts()

    def list_images(self) -> list[ImageDraft]:
        return self.store.read_latest_image_drafts()

    def approve(self, request: ApprovalRequest) -> PublishedPost:
        drafts = self.store.read_latest_post_drafts()
        selected = next((d for d in drafts if d.draft_id == request.draft_id), None)
        if not selected:
            raise ValueError(f"Draft not found: {request.draft_id}")

        content = request.edited_content or selected.content
        published_id = sha256(f"{selected.draft_id}|approved".encode()).hexdigest()[:12]
        published = PublishedPost(
            published_id=published_id,
            draft_id=selected.draft_id,
            topic_id=selected.topic_id,
            content=content,
            hashtags=selected.hashtags,
            citations=selected.citations,
            approved_at=datetime.now(timezone.utc),
        )
        self.store.save_published_post(published)
        return published
