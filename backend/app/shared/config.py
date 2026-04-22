from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "LinkedIn AI Trend Agent"
    app_version: str = "0.3.0-phase6"
    environment: str = "local"
    storage_root: str = "data"
    chroma_path: str = "chroma"
    rss_feeds: list[str] = [
        "https://feeds.feedburner.com/venturebeat/SZYF",
        "https://techcrunch.com/category/artificial-intelligence/feed/",
    ]

    @property
    def storage_path(self) -> Path:
        return Path(self.storage_root)


settings = Settings()
