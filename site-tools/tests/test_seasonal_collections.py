"""Regression tests for catalog-driven seasonal collections and Halloween Alphabet Hunt."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "site-tools"))
sys.path.insert(0, str(ROOT / "worksheet-generator"))

from catalog_lib import load_collections, load_resources  # noqa: E402
from publish_assets import collect_resource_assets  # noqa: E402


RESOURCE_ID = "halloween-alphabet-hunt"
BUNDLE = ROOT / "worksheets/seasonal/halloween/halloween-alphabet-hunt/halloween-alphabet-hunt-pack.pdf"
PAGE_DIRECTORY = ROOT / "worksheets/seasonal/halloween/halloween-alphabet-hunt/halloween-alphabet-hunt-pack"
PREVIEW_DIRECTORY = ROOT / "thumbnails/seasonal/halloween/halloween-alphabet-hunt"
CONFIG = ROOT / "worksheet-generator/content/halloween-alphabet-hunt.json"
EXPECTED_BUNDLE_SHA256 = "dd4d578f1b3995debf78314a8245083248ee1f038289240f2b25eb242cdc3efc"
EXPECTED_PAGE_SHA256 = [
    "509d7df46d0921506586107f66358a0a8263b5022e2e5061596cc5c8a0d372c0",
    "3bb8b536fa8b397cfff16809f20d2328ca38d206da67cba17f82b54a054bd878",
    "3b2162a4c9130233e4423273478c729966009a9cba04c75366bf9e8aa6559dbc",
    "b5078151531cabb54431ded47ed0a6015f66b686866e456cf39e7f73c4140e9c",
    "65e3f39127b57cd2e488fb12f80a620ca924d60fdee040078f4f4ec718b077e9",
    "e19eb92cf0cb77703bd99bee6924237f89cef8c5d80091f6da4ce4a3441deacd",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SeasonalCollectionTests(unittest.TestCase):
    def test_collection_references_one_canonical_resource(self):
        collections = load_collections()
        self.assertEqual(collections["schemaVersion"], 1)
        seasonal = collections["collections"][0]
        self.assertEqual(seasonal["id"], "seasonal-holidays")
        self.assertEqual(seasonal["path"], "seasonal.html")
        self.assertEqual(seasonal["groups"], [{
            "id": "halloween",
            "label": "Halloween",
            "description": "Friendly Halloween learning activities with clear, age-appropriate practice.",
            "resources": [RESOURCE_ID],
        }])
        resources = {resource["id"]: resource for resource in load_resources()}
        resource = resources[RESOURCE_ID]
        self.assertEqual(resource["collections"], ["halloween"])
        self.assertEqual(resource["routing"]["slug"], RESOURCE_ID)
        self.assertEqual(resource["taxonomy"], {
            "grade": "preschool",
            "subject": "reading-language",
            "topic": "alphabet",
            "skills": ["letter-recognition", "letter-matching", "alphabet-order"],
        })

    def test_seasonal_page_and_primary_navigation_are_generated(self):
        page = (ROOT / "seasonal.html").read_text(encoding="utf-8")
        nav = (ROOT / "nav.js").read_text(encoding="utf-8")
        self.assertIn('<link rel="canonical" href="https://simplelearningresources.com/seasonal.html">', page)
        self.assertIn('<h1>Seasonal &amp; Holidays</h1>', page)
        self.assertIn('<h2>Halloween</h2>', page)
        self.assertIn('href="resources/halloween-alphabet-hunt/"', page)
        self.assertNotIn('<p class="eyebrow">RESOURCE COLLECTIONS</p>', page)
        self.assertNotIn('<div class="library-header"><h1>Seasonal &amp; Holidays</h1><p>', page)
        self.assertNotIn('<h2>Halloween</h2>\n                <p>', page)
        self.assertNotIn("Resources coming soon", page)
        self.assertEqual(nav.count('href=\\"seasonal.html\\">Seasonal &amp; Holidays'), 1)

    def test_bundle_pages_previews_and_publisher_assets_match(self):
        self.assertEqual(sha256(BUNDLE), EXPECTED_BUNDLE_SHA256)
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 6)
            for page_number, expected_hash in enumerate(EXPECTED_PAGE_SHA256, start=1):
                page_pdf_path = PAGE_DIRECTORY / f"page-{page_number:02d}.pdf"
                preview_path = PREVIEW_DIRECTORY / f"page-{page_number:02d}.png"
                self.assertEqual(sha256(page_pdf_path), expected_hash)
                with pymupdf.open(page_pdf_path) as individual:
                    self.assertEqual(individual.page_count, 1)
                    expected = bundle[page_number - 1].get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
                    actual_page = individual[0].get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
                    preview = pymupdf.Pixmap(preview_path)
                    self.assertEqual(actual_page.samples, expected.samples)
                    self.assertEqual((preview.width, preview.height), (1224, 1584))
                    self.assertEqual(preview.samples, expected.samples)
        assets = collect_resource_assets(ROOT, CONFIG)
        self.assertEqual(len(assets), 13)
        self.assertEqual(sum(asset.mime_type == "application/pdf" for asset in assets), 7)
        self.assertEqual(sum(asset.mime_type == "image/png" for asset in assets), 6)


if __name__ == "__main__":
    unittest.main()
