import os
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "LinkedIn AI Trend Agent"
    app_version: str = "0.5.0-phase12"
    environment: str = "local"
    storage_root: str = "data"
    chroma_path: str = "chroma"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    openai_embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    agent_api_key: str = os.getenv("AGENT_API_KEY", "dev-key")
    require_auth: bool = os.getenv("REQUIRE_AUTH", "true").lower() == "true"
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    rss_feeds: list[str] = [
        "https://feeds.feedburner.com/venturebeat/SZYF",
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://www.marktechpost.com/feed/",
        "https://openai.com/news/rss.xml",
    ]

    @property
    def storage_path(self) -> Path:
        return Path(self.storage_root)


settings = Settings()
