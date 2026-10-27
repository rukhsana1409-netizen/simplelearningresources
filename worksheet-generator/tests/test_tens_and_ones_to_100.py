"""Asset-contract checks for the approved Grade 1 tens-and-ones pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/tens-and-ones/tens-and-ones.pdf"
ANSWER_KEY = REPOSITORY_ROOT / "worksheets/grade-1/math/tens-and-ones/tens-and-ones-answer-key.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/tens-and-ones/tens-and-ones"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/tens-and-ones/tens-and-ones"


class TensAndOnesTo100AssetTests(unittest.TestCase):
    def test_approved_bundle_and_answer_key_hashes(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "9b8b009d9422b7f95598efdbf92b2b7a65e1198595f493a44019e478e299811c",
        )
        self.assertEqual(
            hashlib.sha256(ANSWER_KEY.read_bytes()).hexdigest(),
            "1d13889cd51a4a41c75c57f80cacc6fbd0b31a48219a691e46ea84e46c93b0cb",
        )

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 5)
            for page_number in range(1, 6):
                page_path = PAGE_DIRECTORY / f"page-{page_number:02d}.pdf"
                preview_path = PREVIEW_DIRECTORY / f"page-{page_number:02d}.png"
                with self.subTest(page=page_number):
                    with pymupdf.open(page_path) as page_pdf:
                        self.assertEqual(page_pdf.page_count, 1)
                        expected = bundle[page_number - 1].get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                        actual_page = page_pdf[0].get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                        self.assertEqual(actual_page.samples, expected.samples)
                    actual_preview = pymupdf.Pixmap(preview_path)
                    self.assertEqual((actual_preview.width, actual_preview.height), (1224, 1584))
                    self.assertEqual(actual_preview.samples, expected.samples)

    def test_publisher_contract_includes_all_twelve_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/tens-and-ones-to-100.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 12)
        self.assertEqual(len({asset.object_key for asset in assets}), 12)


if __name__ == "__main__":
    unittest.main()
