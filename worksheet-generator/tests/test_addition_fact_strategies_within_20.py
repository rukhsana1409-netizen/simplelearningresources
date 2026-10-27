"""Asset-contract checks for the approved Grade 1 addition-strategies pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/addition-strategies/addition-strategies.pdf"
ANSWER_KEY = REPOSITORY_ROOT / "worksheets/grade-1/math/addition-strategies/addition-strategies-answer-key.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/addition-strategies/addition-strategies"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/addition-strategies/addition-strategies"


class AdditionFactStrategiesWithin20AssetTests(unittest.TestCase):
    def test_approved_bundle_and_answer_key_hashes(self):
        self.assertEqual(hashlib.sha256(BUNDLE.read_bytes()).hexdigest(), "aef2fdff6c38d6787b3e777ba5ce15539b31fb9e9b2c63a520bbe755c0e6adc2")
        self.assertEqual(hashlib.sha256(ANSWER_KEY.read_bytes()).hexdigest(), "0387ad256d70e2a735384d65a019bf87d63e8dd67c26de0152961a17948e0540")

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

    def test_publisher_contract_includes_all_twelve_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/addition-fact-strategies-within-20.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 12)
        self.assertEqual(len({asset.object_key for asset in assets}), 12)


if __name__ == "__main__":
    unittest.main()
