"""Asset-contract checks for the approved Grade 1 shapes pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/shapes-and-their-attributes/shapes-and-their-attributes.pdf"
ANSWER_KEY = REPOSITORY_ROOT / "worksheets/grade-1/math/shapes-and-their-attributes/shapes-and-their-attributes-answer-key.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/shapes-and-their-attributes/shapes-and-their-attributes"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/shapes-and-fractions/shapes-and-their-attributes"
APPROVED_PAGE_HASHES = [
    "d2bedc92969467339dec86818ccf57f54c69583c5ca1df24c3383c0e1023381a",
    "505599142d967e15ade9cfc57e487729f7a98694d455f97694e6e738c1f892e8",
    "96a713da57fe7fc9fc8455aa1420552162b0e2b59decd3fa0bde0fd4a31a53e2",
    "30d55b97c3ab139789670059e3ee9faacb8a2240eee6957285be66cb59f4aff7",
    "bcf650753518870d82fc6b72d7dc7fddd09954c2c0b43423632e86ec9ff298d1",
]


class ShapesAndTheirAttributesAssetTests(unittest.TestCase):
    def test_approved_bundle_and_answer_key_hashes(self):
        self.assertEqual(hashlib.sha256(BUNDLE.read_bytes()).hexdigest(), "5143c6f242afc4252b9ed2f5532ba31c46baf2e060e9f22c3950485628bc01c9")
        self.assertEqual(hashlib.sha256(ANSWER_KEY.read_bytes()).hexdigest(), "bf4784d5693ebf70a34641849be6951562b3673c731f87b8ab0981e10f351470")

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 5)
            for page_number in range(1, 6):
                with self.subTest(page=page_number):
                    expected = bundle[page_number - 1].get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
                    with pymupdf.open(PAGE_DIRECTORY / f"page-{page_number:02d}.pdf") as page_pdf:
                        self.assertEqual(page_pdf.page_count, 1)
                        actual_page = page_pdf[0].get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
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

    def test_publisher_contract_includes_all_twelve_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/shapes-and-their-attributes.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 12)
        self.assertEqual(len({asset.object_key for asset in assets}), 12)


if __name__ == "__main__":
    unittest.main()
