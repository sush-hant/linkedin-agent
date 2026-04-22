from fastapi import APIRouter

from app.adapters.storage.file_store import JsonFileStore
from app.modules.evaluation import EvaluationService
from app.shared.config import settings

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.get("/summary")
def evaluation_summary() -> dict:
    service = EvaluationService(JsonFileStore(settings.storage_path))
    return service.summary().model_dump()
