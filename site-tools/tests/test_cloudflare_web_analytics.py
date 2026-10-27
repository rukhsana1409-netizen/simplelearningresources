"""Verify Cloudflare Web Analytics across production HTML."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "site-tools"))

from static_resource_pages import CLOUDFLARE_BEACON_TAG  # noqa: E402


BEACON_TAG = (
    '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
    'data-cf-beacon=\'{"token":"a6fe9e891acb4cffadbe27263f7ec4bd"}\'></script>'
)


class CloudflareWebAnalyticsTests(unittest.TestCase):
    def test_every_production_page_contains_the_beacon_once(self):
        pages = sorted(REPOSITORY_ROOT.glob("*.html")) + sorted(
            (REPOSITORY_ROOT / "resources").glob("*/index.html")
        )
        self.assertEqual(len(pages), 133)
        for page in pages:
            source = page.read_text(encoding="utf-8")
            with self.subTest(page=page.relative_to(REPOSITORY_ROOT)):
                self.assertEqual(source.count(BEACON_TAG), 1)
                self.assertLess(source.index(BEACON_TAG), source.index("</body>"))

    def test_resource_page_generator_emits_the_beacon(self):
        self.assertEqual(CLOUDFLARE_BEACON_TAG, BEACON_TAG)


if __name__ == "__main__":
    unittest.main()
