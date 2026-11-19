"""Asset-contract checks for the approved Grade 1 nouns and verbs pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/reading/nouns-and-verbs-in-action/nouns-and-verbs-in-action.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/reading/nouns-and-verbs-in-action/nouns-and-verbs-in-action"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/reading/grammar-and-sentences/nouns-and-verbs-in-action"
PARENT_GUIDE = REPOSITORY_ROOT / "worksheets/grade-1/reading/nouns-and-verbs-in-action/nouns-and-verbs-in-action-parent-guide.pdf"
APPROVED_PAGE_HASHES = [
    "58259fd1da70b16ff8139bc138febf0de09c33b6cff3c1f11752891827b95390",
    "272c3129a868120c46281c657e2a9e1ce4a765ba2d03a96b9b40be6caea7152a",
    "dc50750fdc8c67dac8308fa23e7908e8eec4bcbadc54e192ea3055a82efaabf7",
    "c850806c2e321ef3fa6f0562224d0f0f10a8fb59db90ccc0282b5d17dcd58474",
    "f65439c86b1c81d0cc936e1a7b530f2e51d51b27b7e93b90befd76fd7cc1cc41",
]


class NounsAndVerbsInActionAssetTests(unittest.TestCase):
    def test_approved_pdf_hashes(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "989efeedfb79767caa09ea3d9df6d65fe7f2733e3073eaa290d14b52279e617c",
        )
        self.assertEqual(
            hashlib.sha256(PARENT_GUIDE.read_bytes()).hexdigest(),
            "a0da13e8ab3207e81d6d135c33a2b99f8d9e425065a00c7dddf925d54ec8a836",
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
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/nouns-and-verbs-in-action.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        self.assertEqual(config["answer_key_pdf"], PARENT_GUIDE.relative_to(REPOSITORY_ROOT).as_posix())
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 12)
        self.assertEqual(len({asset.object_key for asset in assets}), 12)


if __name__ == "__main__":
    unittest.main()
