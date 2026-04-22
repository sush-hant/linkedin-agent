from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.ports.interfaces import SourceClientPort
from app.shared.schemas import SourceItem


@dataclass
class StaticSourceClient(SourceClientPort):
    name: str = "static"

    def fetch(self) -> list[SourceItem]:
        now = datetime.now(timezone.utc)
        return [
            SourceItem(
                source=self.name,
                title="AI Agents: coding copilots move to production",
                url="https://example.com/ai-agents-production",
                summary="Teams are evaluating reliability patterns for autonomous coding flows.",
                published_at=now - timedelta(hours=8),
                fetched_at=now,
            ),
            SourceItem(
                source=self.name,
                title="Multimodal AI assistants for enterprise workflows",
                url="https://example.com/multimodal-assistants",
                summary="Vendors are shipping document+voice agents for operations teams.",
                published_at=now - timedelta(hours=20),
                fetched_at=now,
            ),
        ]
