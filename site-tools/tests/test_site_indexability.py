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

from catalog_lib import load_resources, load_site  # noqa: E402
from validate_site_indexability import sitemap_urls, validate  # noqa: E402


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


class SiteIndexabilityTests(unittest.TestCase):
    def test_every_sitemap_url_is_indexable_canonical_and_inbound_linked(self):
        counts = validate()
        published_count = len(
            [resource for resource in load_resources() if resource["status"] == "published"]
        )
        static_count = len(load_site()["compatibility"]["sitemap"]["staticPaths"])
        expected_count = static_count + published_count
        self.assertEqual(counts["sitemapUrlCount"], expected_count)
        self.assertEqual(counts["statusOkCount"], expected_count)
        self.assertEqual(counts["indexableCount"], expected_count)
        self.assertEqual(counts["canonicalCount"], expected_count)
        self.assertEqual(counts["inboundLinkedCount"], expected_count)
        self.assertEqual(counts["resourceVisibleInboundLinkedCount"], published_count)

    def test_query_directories_are_noindex_and_excluded_from_sitemap(self):
        urls = sitemap_urls()
        self.assertFalse(any("topic.html?" in url for url in urls))
        self.assertFalse(any("skill-directory.html?" in url for url in urls))
        for filename in ("topic.html", "skill-directory.html"):
            source = (REPOSITORY_ROOT / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertEqual(
                    source.count('<meta name="robots" content="noindex,follow">'),
                    1,
                )
                self.assertNotIn("setIndexableCanonicalUrl", source)

    def test_unfinished_grade_two_page_is_noindex(self):
        grade_two = (REPOSITORY_ROOT / "grade-2.html").read_text(encoding="utf-8")
        self.assertIn('<meta name="robots" content="noindex,follow">', grade_two)
        self.assertIn(
            '<link rel="canonical" href="https://simplelearningresources.com/grade-2.html">',
            grade_two,
        )

    def test_populated_hubs_are_canonical_and_in_sitemap_once(self):
        urls = sitemap_urls()
        for filename in ("kindergarten.html", "science.html", "thinking-world.html"):
            public_url = f"https://simplelearningresources.com/{filename}"
            with self.subTest(url=public_url):
                self.assertEqual(urls.count(public_url), 1)
                source = (REPOSITORY_ROOT / filename).read_text(encoding="utf-8")
                self.assertEqual(
                    source.count(f'<link rel="canonical" href="{public_url}">'),
                    1,
                )

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
