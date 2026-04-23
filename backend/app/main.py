from collections import deque
from dataclasses import dataclass
from time import time

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.routes.evaluation import router as evaluation_router
from app.api.routes.feedback import router as feedback_router
from app.api.routes.health import router as health_router
from app.api.routes.pipeline import router as pipeline_router
from app.api.routes.review import router as review_router
from app.shared.config import settings


@dataclass
class _RateBucket:
    timestamps: deque[float]


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, per_minute: int) -> None:
        super().__init__(app)
        self.per_minute = per_minute
        self.buckets: dict[str, _RateBucket] = {}

    async def dispatch(self, request: Request, call_next):
        client = request.client.host if request.client else "unknown"
        now = time()
        bucket = self.buckets.setdefault(client, _RateBucket(deque()))

        while bucket.timestamps and now - bucket.timestamps[0] > 60:
            bucket.timestamps.popleft()

        if len(bucket.timestamps) >= self.per_minute:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)

        bucket.timestamps.append(now)
        return await call_next(request)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.add_middleware(InMemoryRateLimitMiddleware, per_minute=settings.rate_limit_per_minute)

    app.include_router(health_router)
    app.include_router(pipeline_router)
    app.include_router(review_router)
    app.include_router(feedback_router)
    app.include_router(evaluation_router)
    return app


app = create_app()
