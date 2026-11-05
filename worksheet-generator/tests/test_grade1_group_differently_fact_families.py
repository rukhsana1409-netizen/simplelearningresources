"""Asset-contract checks for the approved Grade 1 supplementary practice pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/properties-fact-families-supplement/group-differently-fact-families.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/properties-fact-families-supplement/group-differently-fact-families"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/addition/group-differently-fact-families"
APPROVED_PAGE_HASHES = [
    "f2483e75a3f53df85e7872060b2f43f444370a89d7605dd21d6707efbdfbd353",
    "b4731f48d019e79aa2e11a92d88409310f6ae3379c6ec67f819158186c80b4a2",
]


class GroupDifferentlyFactFamiliesAssetTests(unittest.TestCase):
    def test_approved_bundle_hash(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "0ced128ffb8900b1b0fc076000929ab31642a7189ef97505749d312bc06a91a0",
        )

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 2)
            for page_number in range(1, 3):
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
        actual = [
            hashlib.sha256((PAGE_DIRECTORY / f"page-{page_number:02d}.pdf").read_bytes()).hexdigest()
            for page_number in range(1, 3)
        ]
        self.assertEqual(actual, APPROVED_PAGE_HASHES)

    def test_publisher_contract_has_no_answer_key_and_five_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/group-differently-fact-families.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertNotIn("answer_key_pdf", config)
        self.assertEqual(config["asset_output"]["expected_page_count"], 2)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 5)
        self.assertEqual(len({asset.object_key for asset in assets}), 5)


if __name__ == "__main__":
    unittest.main()
