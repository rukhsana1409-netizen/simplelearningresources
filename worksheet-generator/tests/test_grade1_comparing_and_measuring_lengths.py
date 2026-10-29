"""Asset-contract checks for the approved Grade 1 length pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/comparing-and-measuring-lengths/comparing-and-measuring-lengths.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/comparing-and-measuring-lengths/comparing-and-measuring-lengths"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/measurement/comparing-and-measuring-lengths"
APPROVED_PAGE_HASHES = [
    "0d00ed8ad74fdb499058bdb104bc848ed79df9c6d9ad55146206d5dc3acb3802",
    "220195d073ad9351f01a8b74410e6cfdcfd278ee2920f6ce4ecc5a5786ebf3da",
    "0c8228ebf961ce34a225549b3b0371ff1b5fe074d56a7ab1638332315dc55885",
    "a6bf63eea31a74b3e3728f11878e7651f4bb71559a8a9c5a09c9d730ae42475b",
    "b3d16f2ca660b0ae0135d927e0ca100406f7e21f21284b265758374e52b9e7da",
]


class ComparingAndMeasuringLengthsAssetTests(unittest.TestCase):
    def test_approved_bundle_hash(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "da169bf16c5f0e83668b2367c7bc261df162a5af7c5b95eb70d1a035dd1e4157",
        )

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 5)
            for page_number in range(1, 6):
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

    def test_individual_page_pdfs_are_the_approved_handoff_files(self):
        actual = [
            hashlib.sha256((PAGE_DIRECTORY / f"page-{page_number:02d}.pdf").read_bytes()).hexdigest()
            for page_number in range(1, 6)
        ]
        self.assertEqual(actual, APPROVED_PAGE_HASHES)

    def test_publisher_contract_has_no_answer_key_and_eleven_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/comparing-and-measuring-lengths.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertNotIn("answer_key_pdf", config)
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 11)
        self.assertEqual(len({asset.object_key for asset in assets}), 11)


if __name__ == "__main__":
    unittest.main()
