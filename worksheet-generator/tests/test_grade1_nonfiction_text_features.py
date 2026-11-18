"""Asset-contract checks for the approved Grade 1 nonfiction text-features pack."""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

import pymupdf


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "worksheet-generator"))

from publish_assets import collect_resource_assets  # noqa: E402


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/reading/nonfiction-text-features/nonfiction-text-features.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/reading/nonfiction-text-features/nonfiction-text-features"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/reading/informational-reading/nonfiction-text-features"
PARENT_GUIDE = REPOSITORY_ROOT / "worksheets/grade-1/reading/nonfiction-text-features/nonfiction-text-features-parent-guide.pdf"
APPROVED_PAGE_HASHES = [
    "52d785d9c57eab4f6b2ea9a906007326dc3bff0ada0e58f954df0bf3f613cf19",
    "8950c5847372a9c56b2bd148942d4e9cd959c0744be7d33eb3d0aa551aed0d07",
    "986775bad3e693e5c8c3763566a0d3b20c3be39c8cbaadc66e14e2f074028080",
    "0a741593a22f3ae69ca5a3b4b3ed5f6e927195506000770ff7098771a80de2e1",
]


class NonfictionTextFeaturesAssetTests(unittest.TestCase):
    def test_approved_pdf_hashes(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "1f2a50bb9e0554303f70480346017663d212fb9fdd179298162610ce2c7fd783",
        )
        self.assertEqual(
            hashlib.sha256(PARENT_GUIDE.read_bytes()).hexdigest(),
            "5fd805da3ea6062dfa37b8150394e693edc7a02bec56670fa7c213bd982680cb",
        )
        self.assertEqual(
            [
                hashlib.sha256((PAGE_DIRECTORY / f"page-{number:02d}.pdf").read_bytes()).hexdigest()
                for number in range(1, 5)
            ],
            APPROVED_PAGE_HASHES,
        )

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 4)
            for number in range(1, 5):
                with self.subTest(page=number):
                    expected = bundle[number - 1].get_pixmap(
                        dpi=144, colorspace=pymupdf.csRGB, alpha=False
                    )
                    with pymupdf.open(PAGE_DIRECTORY / f"page-{number:02d}.pdf") as page_pdf:
                        actual = page_pdf[0].get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                    preview = pymupdf.Pixmap(PREVIEW_DIRECTORY / f"page-{number:02d}.png")
                    self.assertEqual(actual.samples, expected.samples)
                    self.assertEqual((preview.width, preview.height), (1224, 1584))
                    self.assertEqual(preview.samples, expected.samples)

    def test_publisher_contract_contains_ten_unique_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/nonfiction-text-features.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["asset_output"]["expected_page_count"], 4)
        self.assertEqual(config["answer_key_pdf"], PARENT_GUIDE.relative_to(REPOSITORY_ROOT).as_posix())
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 10)
        self.assertEqual(len({asset.object_key for asset in assets}), 10)


if __name__ == "__main__":
    unittest.main()
