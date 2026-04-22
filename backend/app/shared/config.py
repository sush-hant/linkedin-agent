from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "LinkedIn AI Trend Agent"
    app_version: str = "0.2.0-phase5"
    environment: str = "local"
    storage_root: str = "data"
    chroma_path: str = "chroma"

    @property
    def storage_path(self) -> Path:
        return Path(self.storage_root)


settings = Settings()
