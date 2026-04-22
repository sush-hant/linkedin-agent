from dataclasses import dataclass

from app.ports.interfaces import StoragePort
from app.shared.schemas import FeedbackEntry


@dataclass
class FeedbackService:
    store: StoragePort

    def record(self, feedback: FeedbackEntry) -> str:
        return self.store.save_feedback(feedback)

    def quality_multiplier(self, quality: str) -> float:
        mapping = {"poor": 0.9, "average": 1.0, "good": 1.1}
        return mapping.get(quality, 1.0)
