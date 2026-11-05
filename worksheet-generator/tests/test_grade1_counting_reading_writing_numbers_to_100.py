"""Asset-contract checks for the approved Grade 1 numbers-to-100 pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/numbers-to-100/counting-reading-writing-numbers-to-100.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/numbers-to-100/counting-reading-writing-numbers-to-100"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/numbers-and-place-value/counting-reading-writing-numbers-to-100"
APPROVED_PAGE_HASHES = [
    "7072af60e5fd26ce46395665ba40dad28dbc16c7cd211aa983ca3d81abc20d03",
    "17b3bc6be0dc4842e5e652b99bdc545418c97e9771c0b66debfc4e95991820e8",
    "08ffda4291d8c3fd930eae1faa5f52487004450b080c179d857f73dfa672718c",
    "02385e9d015289b4959e0ea99c2f97d4f23279444bba3c2551dd34c6ab9351d0",
]


class CountingReadingWritingNumbersAssetTests(unittest.TestCase):
    def test_approved_bundle_hash(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "34c668350598fc849bfa63a19ba5c8c6dc1c4b048bde6ed777882f9ad5a86261",
        )

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 4)
            for page_number in range(1, 5):
                with self.subTest(page=page_number):
                    expected = bundle[page_number - 1].get_pixmap(
                        dpi=144, colorspace=pymupdf.csRGB, alpha=False
                    )
                    with pymupdf.open(PAGE_DIRECTORY / f"page-{page_number:02d}.pdf") as page_pdf:
                        self.assertEqual(page_pdf.page_count, 1)
                        actual_page = page_pdf[0].get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                        self.assertEqual(actual_page.samples, expected.samples)
                    actual_preview = pymupdf.Pixmap(PREVIEW_DIRECTORY / f"page-{page_number:02d}.png")
                    self.assertEqual((actual_preview.width, actual_preview.height), (1224, 1584))
                    self.assertEqual(actual_preview.samples, expected.samples)

    def test_individual_page_pdfs_are_approved_handoff_files(self):
        actual_pages = [
            hashlib.sha256((PAGE_DIRECTORY / f"page-{page_number:02d}.pdf").read_bytes()).hexdigest()
            for page_number in range(1, 5)
        ]
        self.assertEqual(actual_pages, APPROVED_PAGE_HASHES)

    def test_publisher_contract_has_no_answer_key_and_nine_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/counting-reading-writing-numbers-to-100.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertNotIn("answer_key_pdf", config)
        self.assertEqual(config["asset_output"]["expected_page_count"], 4)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 9)
        self.assertEqual(len({asset.object_key for asset in assets}), 9)


if __name__ == "__main__":
    unittest.main()
