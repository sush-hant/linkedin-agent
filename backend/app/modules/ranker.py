from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256

from app.shared.schemas import NormalizedItem, TrendCandidate


@dataclass
class TrendRanker:
    audience_keywords: list[str]

    def _recency_score(self, published_at: datetime) -> float:
        hours_old = max((datetime.now(timezone.utc) - published_at).total_seconds() / 3600, 0)
        return max(0.0, 1.0 - min(hours_old / 72, 1.0))

    def _audience_fit(self, text: str) -> float:
        text_lower = text.lower()
        matched = sum(1 for k in self.audience_keywords if k.lower() in text_lower)
        return min(matched / max(len(self.audience_keywords), 1), 1.0)

    def _novelty_score(self, related_ids: list[str]) -> float:
        # More related ids => lower novelty. 0 related means maximum novelty.
        return max(0.0, 1.0 - min(len(related_ids) / 5.0, 1.0))

    def run(
        self,
        items: list[NormalizedItem],
        related_lookup: Callable[[str], list[str]] | None = None,
    ) -> list[TrendCandidate]:
        candidates: list[TrendCandidate] = []
        for item in items:
            recency = self._recency_score(item.published_at)
            momentum = 0.6
            base_text = f"{item.title}\n{item.summary}\n{item.topic_hint}"
            audience_fit = self._audience_fit(base_text)
            related_ids = related_lookup(base_text) if related_lookup else []
            novelty = self._novelty_score(related_ids)

            score = min(1.0, 0.30 * recency + 0.30 * momentum + 0.20 * audience_fit + 0.20 * novelty)
            topic_id = sha256(f"{item.topic_hint}|{item.url}".encode()).hexdigest()[:12]
            candidates.append(
                TrendCandidate(
                    topic_id=topic_id,
                    title=item.title,
                    summary=item.summary,
                    supporting_urls=[item.url],
                    trend_score=score,
                    generated_at=datetime.now(timezone.utc),
                )
            )
        return sorted(candidates, key=lambda c: c.trend_score, reverse=True)
