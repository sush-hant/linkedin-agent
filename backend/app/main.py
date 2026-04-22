from fastapi import FastAPI

from app.api.routes.feedback import router as feedback_router
from app.api.routes.health import router as health_router
from app.api.routes.pipeline import router as pipeline_router
from app.api.routes.review import router as review_router
from app.shared.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.include_router(health_router)
    app.include_router(pipeline_router)
    app.include_router(review_router)
    app.include_router(feedback_router)
    return app


app = create_app()
