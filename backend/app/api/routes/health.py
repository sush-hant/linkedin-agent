from fastapi import APIRouter

from app.shared.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/config")
def runtime_config() -> dict[str, str]:
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "environment": settings.environment,
        "storage_root": settings.storage_root,
        "chroma_path": settings.chroma_path,
    }
