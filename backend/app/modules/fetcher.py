from dataclasses import dataclass

from app.ports.interfaces import SourceClientPort
from app.shared.schemas import SourceItem


@dataclass
class SourceFetcher:
    clients: list[SourceClientPort]

    def run(self) -> list[SourceItem]:
        items: list[SourceItem] = []
        for client in self.clients:
            items.extend(client.fetch())
        return items
