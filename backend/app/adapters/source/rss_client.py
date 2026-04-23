from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from time import sleep
from urllib.request import urlopen
from xml.etree import ElementTree as ET

from app.ports.interfaces import SourceClientPort
from app.shared.schemas import SourceItem


@dataclass
class RSSSourceClient(SourceClientPort):
    feed_url: str
    source_name: str
    timeout_seconds: int = 10
    max_retries: int = 3

    def _parse_datetime(self, raw: str | None) -> datetime:
        if not raw:
            return datetime.now(timezone.utc)
        try:
            dt = parsedate_to_datetime(raw)
            return dt.astimezone(timezone.utc)
        except (TypeError, ValueError):
            return datetime.now(timezone.utc)

    def _parse_feed(self, xml_payload: bytes) -> list[SourceItem]:
        root = ET.fromstring(xml_payload)
        now = datetime.now(timezone.utc)
        rows: list[SourceItem] = []

        for node in root.findall(".//item"):
            title = (node.findtext("title") or "").strip()
            link = (node.findtext("link") or "").strip()
            summary = (node.findtext("description") or "").strip()
            published = self._parse_datetime(node.findtext("pubDate"))

            if not title or not link.startswith(("http://", "https://")):
                continue

            rows.append(
                SourceItem(
                    source=self.source_name,
                    title=title,
                    url=link,
                    summary=summary[:1000],
                    published_at=published,
                    fetched_at=now,
                )
            )
        return rows

    def fetch(self) -> list[SourceItem]:
        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                with urlopen(self.feed_url, timeout=self.timeout_seconds) as response:  # noqa: S310
                    payload = response.read()
                return self._parse_feed(payload)
            except Exception as exc:
                last_error = exc
                if attempt < self.max_retries - 1:
                    sleep(0.5 * (attempt + 1))
        if last_error:
            raise last_error
        return []
