from fastapi import APIRouter, HTTPException

from app.adapters.storage.file_store import JsonFileStore
from app.modules.review import ReviewService
from app.shared.config import settings
from app.shared.schemas import ApprovalRequest

router = APIRouter(prefix="/review", tags=["review"])


def _service() -> ReviewService:
    return ReviewService(JsonFileStore(settings.storage_path))


@router.get("/drafts")
def list_drafts() -> list[dict]:
    drafts = _service().list_drafts()
    return [d.model_dump() for d in drafts]


@router.post("/approve")
def approve_draft(request: ApprovalRequest) -> dict:
    try:
        published = _service().approve(request)
        return published.model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
