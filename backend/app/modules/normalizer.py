from dataclasses import dataclass
from hashlib import sha256

from app.shared.schemas import NormalizedItem, SourceItem


@dataclass
class NormalizerDeduper:
    def run(self, items: list[SourceItem]) -> list[NormalizedItem]:
        deduped: dict[str, SourceItem] = {}
        for item in items:
            key = f"{item.url}|{item.title.strip().lower()}"
            deduped[key] = item

        normalized: list[NormalizedItem] = []
        for item in deduped.values():
            topic_hint = item.title.split(":")[0].strip().lower()
            item_id = sha256(f"{item.source}|{item.url}".encode()).hexdigest()[:12]
            normalized.append(
                NormalizedItem(
                    item_id=item_id,
                    source=item.source,
                    title=item.title,
                    url=item.url,
                    summary=item.summary,
                    published_at=item.published_at,
                    fetched_at=item.fetched_at,
                    topic_hint=topic_hint,
                )
            )
        return normalized
