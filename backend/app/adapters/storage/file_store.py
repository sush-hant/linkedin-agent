import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from app.ports.interfaces import StoragePort
from app.shared.schemas import (
    FeedbackEntry,
    ImageDraft,
    NormalizedItem,
    PostDraft,
    PublishedPost,
    SourceItem,
    TrendCandidate,
)


@dataclass
class JsonFileStore(StoragePort):
    root_dir: Path

    def _write(self, folder: str, payload: list[dict] | dict) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        target_dir = self.root_dir / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / f"{timestamp}.json"
        file_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return str(file_path)

    def _latest_json(self, folder: str) -> Path | None:
        target_dir = self.root_dir / folder
        if not target_dir.exists():
            return None
        files = sorted(target_dir.glob("*.json"))
        return files[-1] if files else None

    def save_raw_items(self, items: list[SourceItem]) -> str:
        return self._write("raw", [item.model_dump() for item in items])

    def save_normalized_items(self, items: list[NormalizedItem]) -> str:
        return self._write("normalized", [item.model_dump() for item in items])

    def save_trend_candidates(self, items: list[TrendCandidate]) -> str:
        return self._write("trends", [item.model_dump() for item in items])

    def save_post_drafts(self, items: list[PostDraft]) -> str:
        return self._write("drafts/posts", [item.model_dump() for item in items])

    def save_image_drafts(self, items: list[ImageDraft]) -> str:
        return self._write("drafts/images", [item.model_dump() for item in items])

    def read_latest_post_drafts(self) -> list[PostDraft]:
        latest = self._latest_json("drafts/posts")
        if not latest:
            return []
        payload = json.loads(latest.read_text(encoding="utf-8"))
        return [PostDraft.model_validate(item) for item in payload]

    def save_published_post(self, post: PublishedPost) -> str:
        return self._write("published", post.model_dump())

    def save_feedback(self, feedback: FeedbackEntry) -> str:
        return self._write("metrics", feedback.model_dump())
