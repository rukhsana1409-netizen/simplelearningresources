"""Asset-contract checks for the approved Grade 1 data pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/organize-and-interpret-data/organize-and-interpret-data.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/organize-and-interpret-data/organize-and-interpret-data"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/data-and-graphing/organize-and-interpret-data"
APPROVED_PAGE_HASHES = [
    "ec3cc0f92508ee910ad2f5d2ebd8ca08980db6bd2bb13c8309f1f730e5a18a07",
    "6d963656c7dc50f4b7876ccea1521f1a3805ad592f98824e98af56ac0979c788",
    "213dbba81c07ef0896968786a11ec151e7b9e84bd4b50fd769f78f88c0a04122",
    "8f67e3a1f49bbf9cbf44029f930d377d3ca2aca23ea66dcc755608f6f8029706",
    "971d74a5922f5bb3978e7b24656becc0b5ad7ba3f839aee01872048948e37174",
]


class OrganizeAndInterpretDataAssetTests(unittest.TestCase):
    def test_approved_bundle_hash(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "001afecd7294810b92308ad993b882cb103c63a87daafb9299f28d281784113a",
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
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/organize-and-interpret-data.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertNotIn("answer_key_pdf", config)
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 11)
        self.assertEqual(len({asset.object_key for asset in assets}), 11)


if __name__ == "__main__":
    unittest.main()
