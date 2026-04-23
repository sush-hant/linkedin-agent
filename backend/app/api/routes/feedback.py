from fastapi import APIRouter, Depends

from app.adapters.storage.file_store import JsonFileStore
from app.api.deps import require_api_key
from app.modules.feedback import FeedbackService
from app.shared.config import settings
from app.shared.schemas import FeedbackEntry

router = APIRouter(prefix="/feedback", tags=["feedback"])


def _service() -> FeedbackService:
    return FeedbackService(JsonFileStore(settings.storage_path))


@router.post("/record", dependencies=[Depends(require_api_key)])
def record_feedback(entry: FeedbackEntry) -> dict[str, str]:
    path = _service().record(entry)
    return {"status": "ok", "path": path}
