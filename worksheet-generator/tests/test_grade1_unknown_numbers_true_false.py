"""Asset-contract checks for the approved Grade 1 equations pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/unknown-numbers-true-false/unknown-numbers-true-false.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/unknown-numbers-true-false/unknown-numbers-true-false"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/mathematical-thinking/unknown-numbers-true-false"
APPROVED_PAGE_HASHES = [
    "ea5ef1e6cf595272d0b05679071c7a58ab8eb1db9544f4cfdb15572ecca5ad4c",
    "f2ad8ff0904b57abf9d9be37b06b6c65244bd9677d27da753e66b9e57e2ca5db",
    "fc5f43b0700626d63ecfe4b84c34aa2f50ddd5213e8534913a3614a47ff78006",
    "bfa0ad55745a58341d648f3833d1c2fd2b8d81c626129576d641d5c906442f69",
    "8ce26d2af7dfe2f71d63f3535a71f76c715e579e8448ce12dba8bb7be42b4972",
]


class UnknownNumbersTrueFalseAssetTests(unittest.TestCase):
    def test_approved_bundle_hash(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "f0d707dda5412299e8e5fc384859ed62622e96404b5bd02f29f21ac6c7f7f819",
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
                    preview = pymupdf.Pixmap(PREVIEW_DIRECTORY / f"page-{page_number:02d}.png")
                    self.assertEqual((preview.width, preview.height), (1224, 1584))
                    self.assertEqual(preview.samples, expected.samples)

    def test_individual_page_pdfs_are_the_approved_handoff_files(self):
        actual = [
            hashlib.sha256((PAGE_DIRECTORY / f"page-{page_number:02d}.pdf").read_bytes()).hexdigest()
            for page_number in range(1, 6)
        ]
        self.assertEqual(actual, APPROVED_PAGE_HASHES)

    def test_publisher_contract_has_no_answer_key_and_eleven_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/unknown-numbers-true-false.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertNotIn("answer_key_pdf", config)
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 11)
        self.assertEqual(len({asset.object_key for asset in assets}), 11)


if __name__ == "__main__":
    unittest.main()
