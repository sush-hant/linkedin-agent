import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from app.ports.interfaces import StoragePort
from app.shared.schemas import ImageDraft, PostDraft, TrendCandidate


@dataclass
class JsonFileStore(StoragePort):
    root_dir: Path

    def _write(self, folder: str, payload: list[dict]) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        target_dir = self.root_dir / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / f"{timestamp}.json"
        file_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        return str(file_path)

    def save_trend_candidates(self, items: list[TrendCandidate]) -> str:
        return self._write("trends", [item.model_dump() for item in items])

    def save_post_drafts(self, items: list[PostDraft]) -> str:
        return self._write("drafts/posts", [item.model_dump() for item in items])

    def save_image_drafts(self, items: list[ImageDraft]) -> str:
        return self._write("drafts/images", [item.model_dump() for item in items])
