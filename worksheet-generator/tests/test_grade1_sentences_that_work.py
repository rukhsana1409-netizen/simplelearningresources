"""Asset-contract checks for the approved Grade 1 sentences pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/reading/sentences-that-work/sentences-that-work.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/reading/sentences-that-work/sentences-that-work"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/reading/grammar-and-sentences/sentences-that-work"
PARENT_GUIDE = REPOSITORY_ROOT / "worksheets/grade-1/reading/sentences-that-work/sentences-that-work-parent-guide.pdf"
APPROVED_PAGE_HASHES = [
    "f82c9b0cce17624680ade73848cde8707d3756db2734ee6eb010115804da08ab",
    "58b508a9463d81f283dd4a050b05fcaf586c231bd7e5a36f85e2b0e474be8fb2",
    "f0186ccb3ee9d94127d4bfccff135b9c72b7d5fbb11f8058db8ef14674cdf933",
    "a69d1625544d4cd9de18a880f216acdd8128e91edd0cc12bea04c99d710cf7bf",
    "576911055dbd66aae89fd013420e6e23e91d6aec0fe317614a86835b73ec37c8",
]


class SentencesThatWorkAssetTests(unittest.TestCase):
    def test_approved_pdf_hashes(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "849dfb478ed5f38bb36c1e996dac24b6a68b41a7d98acba571d21a73a545a95f",
        )
        self.assertEqual(
            hashlib.sha256(PARENT_GUIDE.read_bytes()).hexdigest(),
            "d2eb45948612f9848f2f634dbdc9d47d04c4cf27f029f4b804ffcd8ed6935164",
        )
        self.assertEqual(
            [
                hashlib.sha256((PAGE_DIRECTORY / f"page-{number:02d}.pdf").read_bytes()).hexdigest()
                for number in range(1, 6)
            ],
            APPROVED_PAGE_HASHES,
        )

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 5)
            for number in range(1, 6):
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

    def test_publisher_contract_contains_twelve_unique_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/sentences-that-work.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        self.assertEqual(config["answer_key_pdf"], PARENT_GUIDE.relative_to(REPOSITORY_ROOT).as_posix())
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 12)
        self.assertEqual(len({asset.object_key for asset in assets}), 12)


if __name__ == "__main__":
    unittest.main()
