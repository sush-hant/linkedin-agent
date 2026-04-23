from fastapi import Header, HTTPException, status

from app.shared.config import settings


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not settings.require_auth:
        return
    if not x_api_key or x_api_key != settings.agent_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
