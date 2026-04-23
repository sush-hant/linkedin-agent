from dataclasses import dataclass

from app.ports.interfaces import StoragePort
from app.shared.schemas import EvaluationSummary, FeedbackEntry


@dataclass
class EvaluationService:
    store: StoragePort

    def _quality_to_score(self, quality: str) -> float:
        mapping = {"poor": 0.0, "average": 0.5, "good": 1.0}
        return mapping.get(quality, 0.5)

    def _engagement_rate(self, row: FeedbackEntry) -> float:
        if row.impressions <= 0:
            return 0.0
        return (row.comments + row.reposts + row.saves) / row.impressions

    def summary(self) -> EvaluationSummary:
        published = self.store.list_published_posts()
        feedback = self.store.list_feedback_entries()

        if not feedback:
            return EvaluationSummary(
                total_published=len(published),
                total_feedback_entries=0,
                avg_quality_score=0.0,
                avg_engagement_rate=0.0,
                top_published_id=published[-1].published_id if published else None,
            )

        quality_scores = [self._quality_to_score(row.quality) for row in feedback]
        engagement_rates = [self._engagement_rate(row) for row in feedback]

        best_row = max(feedback, key=self._engagement_rate)

        return EvaluationSummary(
            total_published=len(published),
            total_feedback_entries=len(feedback),
            avg_quality_score=sum(quality_scores) / len(quality_scores),
            avg_engagement_rate=sum(engagement_rates) / len(engagement_rates),
            top_published_id=best_row.published_id,
        )
