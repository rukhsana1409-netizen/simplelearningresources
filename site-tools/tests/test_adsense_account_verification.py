"""Verify the AdSense account ownership tag across production HTML."""

from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ADSENSE_ACCOUNT_TAG = '<meta name="google-adsense-account" content="ca-pub-7543692368591799">'


class AdsenseAccountVerificationTests(unittest.TestCase):
    def test_every_production_page_contains_the_account_tag_once(self):
        pages = sorted(REPOSITORY_ROOT.glob("*.html")) + sorted(
            (REPOSITORY_ROOT / "resources").glob("*/index.html")
        )
        self.assertEqual(len(pages), 123)
        for page in pages:
            source = page.read_text(encoding="utf-8")
            with self.subTest(page=page.relative_to(REPOSITORY_ROOT)):
                self.assertEqual(source.count(ADSENSE_ACCOUNT_TAG), 1)
                head = source.split("</head>", 1)[0]
                self.assertIn(ADSENSE_ACCOUNT_TAG, head)

    def test_resource_page_generator_emits_the_account_tag(self):
        generator = (REPOSITORY_ROOT / "site-tools" / "static_resource_pages.py").read_text(
            encoding="utf-8"
        )
        self.assertEqual(generator.count(ADSENSE_ACCOUNT_TAG), 1)


if __name__ == "__main__":
    unittest.main()
