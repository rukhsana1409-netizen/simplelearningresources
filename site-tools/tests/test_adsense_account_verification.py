"""Verify the AdSense account ownership tag across production HTML."""

from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ADSENSE_ACCOUNT_TAG = '<meta name="google-adsense-account" content="ca-pub-7543692368591799">'
ADSENSE_AUTO_ADS_TAG = (
    '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?'
    'client=ca-pub-7543692368591799" crossorigin="anonymous"></script>'
)


class AdsenseAccountVerificationTests(unittest.TestCase):
    def test_every_production_page_contains_the_account_tag_once(self):
        pages = sorted(REPOSITORY_ROOT.glob("*.html")) + sorted(
            (REPOSITORY_ROOT / "resources").glob("*/index.html")
        )
        self.assertEqual(len(pages), 164)
        for page in pages:
            source = page.read_text(encoding="utf-8")
            with self.subTest(page=page.relative_to(REPOSITORY_ROOT)):
                self.assertEqual(source.count(ADSENSE_ACCOUNT_TAG), 1)
                self.assertEqual(source.count(ADSENSE_AUTO_ADS_TAG), 1)
                head = source.split("</head>", 1)[0]
                self.assertIn(ADSENSE_ACCOUNT_TAG, head)
                self.assertIn(ADSENSE_AUTO_ADS_TAG, head)

    def test_page_generators_emit_the_account_and_auto_ads_tags(self):
        generators = (
            REPOSITORY_ROOT / "site-tools" / "static_resource_pages.py",
            REPOSITORY_ROOT / "site-tools" / "generate_seasonal_collections.py",
        )
        for generator_path in generators:
            generator = generator_path.read_text(encoding="utf-8")
            with self.subTest(generator=generator_path.relative_to(REPOSITORY_ROOT)):
                self.assertEqual(generator.count(ADSENSE_ACCOUNT_TAG), 1)
                self.assertEqual(generator.count(ADSENSE_AUTO_ADS_TAG), 1)


if __name__ == "__main__":
    unittest.main()
