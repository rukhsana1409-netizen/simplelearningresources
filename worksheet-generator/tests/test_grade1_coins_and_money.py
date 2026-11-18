"""Asset and taxonomy checks for the approved Grade 1 coins-and-money pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/coins-and-money/coins-and-money.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/coins-and-money/coins-and-money"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/money/coins-and-money"
PARENT_GUIDE = REPOSITORY_ROOT / "worksheets/grade-1/math/coins-and-money/coins-and-money-parent-guide.pdf"
APPROVED_PAGE_HASHES = [
    "6990428f21276fac3f5acc957072b7ed1f3bc67946c8f42cd78d34114b1b84c3",
    "27b0d0c996db21a761c2a0498367c12f6eb17aa2fdbeea10f4296955c10e97d1",
    "d13dde57da32c6637e696f80f9f915f301d2f9e6a12b19b15fd8d002f37f183d",
    "583613c2ce4c1f2f2796a6bb1b3cf64222f57dbb22c0091e3abc5515ebcad913",
    "f6c0f646cedf66b37a3fee78ecf3f9d3bac283e7a7fbcdaae369abfd0a7e1b35",
    "475babb6c542619e69eb03ddc5549f6c520eea0a9c2b732962251541baf4f925",
]


class CoinsAndMoneyAssetTests(unittest.TestCase):
    def test_approved_pdf_hashes(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "07b66aa622f1d75f58f809009b67458b54953a240a154faa72a7a2df8fb763f5",
        )
        self.assertEqual(
            hashlib.sha256(PARENT_GUIDE.read_bytes()).hexdigest(),
            "2e0b6cfce82f9f1038a48a492c15b75f718d270e8202e7c6824898fecfcc63d6",
        )
        self.assertEqual(
            [
                hashlib.sha256((PAGE_DIRECTORY / f"page-{number:02d}.pdf").read_bytes()).hexdigest()
                for number in range(1, 7)
            ],
            APPROVED_PAGE_HASHES,
        )

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 6)
            for number in range(1, 7):
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

    def test_publisher_contract_contains_fourteen_unique_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/coins-and-money.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["asset_output"]["expected_page_count"], 6)
        self.assertEqual(config["answer_key_pdf"], PARENT_GUIDE.relative_to(REPOSITORY_ROOT).as_posix())
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 14)
        self.assertEqual(len({asset.object_key for asset in assets}), 14)


if __name__ == "__main__":
    unittest.main()
