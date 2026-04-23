import importlib.util
import unittest
from unittest.mock import patch

PYDANTIC_AVAILABLE = importlib.util.find_spec("pydantic") is not None

if PYDANTIC_AVAILABLE:
    from app.adapters.source.rss_client import RSSSourceClient
    from app.modules.fetcher import SourceFetcher


class _BadClient:
    def fetch(self):
        raise RuntimeError("boom")


class _GoodClient:
    def fetch(self):
        return []


@unittest.skipUnless(PYDANTIC_AVAILABLE, "pydantic is required for source adapter tests")
class SourceAdapterTests(unittest.TestCase):
    def test_fetcher_is_resilient_to_client_failures(self) -> None:
        fetcher = SourceFetcher(clients=[_BadClient(), _GoodClient()])
        result = fetcher.run()
        self.assertEqual(result, [])

    def test_rss_client_parses_items(self) -> None:
        xml_payload = b"""
        <rss><channel>
            <item>
                <title>AI Agent update</title>
                <link>https://example.com/item1</link>
                <description>Summary one</description>
                <pubDate>Wed, 22 Apr 2026 10:00:00 GMT</pubDate>
            </item>
            <item>
                <title></title>
                <link>invalid</link>
                <description>bad row</description>
            </item>
        </channel></rss>
        """
        client = RSSSourceClient(feed_url="https://example.com/rss", source_name="rss:test")
        items = client._parse_feed(xml_payload)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].title, "AI Agent update")

    @patch("app.adapters.source.rss_client.urlopen")
    def test_rss_fetch_calls_urlopen(self, mock_urlopen) -> None:
        class _Resp:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                return False

            def read(self):
                return (
                    b"<rss><channel><item><title>T</title><link>https://example.com/a</link>"
                    b"<description>D</description></item></channel></rss>"
                )

        mock_urlopen.return_value = _Resp()

        client = RSSSourceClient(feed_url="https://example.com/rss", source_name="rss:test")
        items = client.fetch()
        self.assertEqual(len(items), 1)


if __name__ == "__main__":
    unittest.main()
