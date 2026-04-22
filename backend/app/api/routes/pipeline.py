from fastapi import APIRouter

from app.orchestrator.pipeline import PipelineOrchestrator

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/run")
def run_pipeline() -> dict:
    result = PipelineOrchestrator().run()
    return result.__dict__
