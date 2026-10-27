"""Asset-contract checks for the approved Grade 1 addition word-problems pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/addition-word-problems/addition-word-problems.pdf"
ANSWER_KEY = REPOSITORY_ROOT / "worksheets/grade-1/math/addition-word-problems/addition-word-problems-answer-key.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/addition-word-problems/addition-word-problems"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/addition-word-problems/addition-word-problems"


class AdditionWordProblemsWithin20AssetTests(unittest.TestCase):
    def test_approved_bundle_and_answer_key_hashes(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "8de83a6f5db8325723367c9116a45f11f9a2a6d5c20be4e50da282fecd027f90",
        )
        self.assertEqual(
            hashlib.sha256(ANSWER_KEY.read_bytes()).hexdigest(),
            "dfb1b9e501052e51cfb3d8c37229e367d68cc6d9261b5a4e747c475bc2ce62d7",
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
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/addition-word-problems-within-20.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        self.assertEqual(
            config["answer_key_pdf"],
            "worksheets/grade-1/math/addition-word-problems/addition-word-problems-answer-key.pdf",
        )
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 12)
        self.assertEqual(len({asset.object_key for asset in assets}), 12)


if __name__ == "__main__":
    unittest.main()
