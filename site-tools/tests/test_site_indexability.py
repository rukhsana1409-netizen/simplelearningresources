"""Focused tests for sitemap indexability and crawlable link coverage."""

from __future__ import annotations

import contextlib
import http.server
import sys
import threading
import unittest
import urllib.request
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "site-tools"))

from validate_site_indexability import sitemap_urls, validate  # noqa: E402


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


class SiteIndexabilityTests(unittest.TestCase):
    def test_every_sitemap_url_is_indexable_canonical_and_inbound_linked(self):
        counts = validate()
        self.assertEqual(counts["sitemapUrlCount"], 103)
        self.assertEqual(counts["statusOkCount"], 103)
        self.assertEqual(counts["indexableCount"], 103)
        self.assertEqual(counts["canonicalCount"], 103)
        self.assertEqual(counts["inboundLinkedCount"], 103)

    def test_every_sitemap_url_returns_http_200(self):
        handler = lambda *args, **kwargs: QuietHandler(  # noqa: E731
            *args, directory=str(REPOSITORY_ROOT), **kwargs
        )
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for public_url in sitemap_urls():
                relative = public_url.removeprefix("https://simplelearningresources.com")
                with self.subTest(url=public_url):
                    with contextlib.closing(
                        urllib.request.urlopen(
                            f"http://127.0.0.1:{server.server_port}{relative}", timeout=5
                        )
                    ) as response:
                        self.assertEqual(response.status, 200)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_invalid_query_variants_are_noindex_after_runtime_validation(self):
        topic = (REPOSITORY_ROOT / "topic.html").read_text(encoding="utf-8")
        skill = (REPOSITORY_ROOT / "skill-directory.html").read_text(encoding="utf-8")
        noindex_statement = 'document.querySelector(\'meta[name="robots"]\').content = "noindex,follow";'
        self.assertIn("if (!resources.length) {", topic)
        self.assertIn(noindex_statement, topic)
        self.assertIn("if (!directory) {", skill)
        self.assertIn(noindex_statement, skill)


if __name__ == "__main__":
    unittest.main()
