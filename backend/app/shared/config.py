from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "LinkedIn AI Trend Agent"
    app_version: str = "0.1.0-phase1"
    environment: str = "local"
    storage_root: str = "data"
    chroma_path: str = "chroma"


settings = Settings()
