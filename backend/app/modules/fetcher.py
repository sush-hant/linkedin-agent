from dataclasses import dataclass

from app.ports.interfaces import SourceClientPort
from app.shared.schemas import SourceItem


@dataclass
class SourceFetcher:
    clients: list[SourceClientPort]

    def run(self) -> list[SourceItem]:
        items: list[SourceItem] = []
        for client in self.clients:
            try:
                items.extend(client.fetch())
            except Exception:
                # keep pipeline resilient: failed source should not block successful sources
                continue
        return items
