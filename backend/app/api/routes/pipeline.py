from fastapi import APIRouter, Depends

from app.api.deps import require_api_key
from app.orchestrator.pipeline import PipelineOrchestrator

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/run", dependencies=[Depends(require_api_key)])
def run_pipeline() -> dict:
    result = PipelineOrchestrator().run()
    return result.__dict__
