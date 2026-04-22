from fastapi import APIRouter

from app.adapters.storage.file_store import JsonFileStore
from app.modules.feedback import FeedbackService
from app.shared.config import settings
from app.shared.schemas import FeedbackEntry

router = APIRouter(prefix="/feedback", tags=["feedback"])


def _service() -> FeedbackService:
    return FeedbackService(JsonFileStore(settings.storage_path))


@router.post("/record")
def record_feedback(entry: FeedbackEntry) -> dict[str, str]:
    path = _service().record(entry)
    return {"status": "ok", "path": path}
