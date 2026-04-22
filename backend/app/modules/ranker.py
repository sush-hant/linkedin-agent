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

    def run(self, items: list[NormalizedItem]) -> list[TrendCandidate]:
        candidates: list[TrendCandidate] = []
        for item in items:
            recency = self._recency_score(item.published_at)
            momentum = 0.6  # Phase 2 baseline constant; Phase 3+ uses cross-source frequency.
            audience_fit = self._audience_fit(f"{item.title} {item.summary} {item.topic_hint}")
            score = min(1.0, 0.4 * recency + 0.35 * momentum + 0.25 * audience_fit)
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
