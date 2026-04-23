from fastapi import APIRouter, Depends

from app.adapters.storage.file_store import JsonFileStore
from app.api.deps import require_api_key
from app.modules.evaluation import EvaluationService
from app.shared.config import settings

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.get("/summary", dependencies=[Depends(require_api_key)])
def evaluation_summary() -> dict:
    service = EvaluationService(JsonFileStore(settings.storage_path))
    return service.summary().model_dump()
