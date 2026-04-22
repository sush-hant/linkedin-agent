from dataclasses import dataclass
from hashlib import sha256

from app.shared.schemas import ImageDraft, PostDraft


@dataclass
class ImageGenerator:
    def run(self, drafts: list[PostDraft]) -> list[ImageDraft]:
        images: list[ImageDraft] = []
        for draft in drafts:
            image_id = sha256(f"{draft.draft_id}|image".encode()).hexdigest()[:12]
            images.append(
                ImageDraft(
                    image_id=image_id,
                    draft_id=draft.draft_id,
                    prompt=f"Modern LinkedIn hero visual for: {draft.content.splitlines()[0]}",
                    file_path=f"data/images/{image_id}.png",
                    size="1200x627",
                )
            )
        return images
