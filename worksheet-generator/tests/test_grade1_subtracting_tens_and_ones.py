"""Asset-contract checks for the approved Grade 1 subtraction pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/subtracting-tens-and-ones/subtracting-tens-ones.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/subtracting-tens-and-ones/subtracting-tens-ones"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/subtraction/subtracting-tens-and-ones"
APPROVED_PAGE_HASHES = [
    "85023ee3c3f24dcc396028a7f7d517fa8a12c06bac6633358775a3d390db508e",
    "2ae204c2b48a6e2a06d56a3f053f30310363ba96d063c0be4408241e89acdac3",
    "1d3718df939265ecfb4609d4fc81a65b4645f8208195c4ec9e2fbcf9a6272028",
    "c701cede02dae44419c2377bb8de9203be6f63de6fba11c2067d93f15b302b53",
    "243b031fffe09ae89bdda8faecdfe9beba782bbdf5499310003dbb36ed107941",
]


class SubtractingTensAndOnesAssetTests(unittest.TestCase):
    def test_approved_bundle_hash(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "69b1083d107c074d68116804f05d2ff05b2658a0f6a0dad4372e311aa83617a5",
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
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/subtracting-tens-and-ones.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertNotIn("answer_key_pdf", config)
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 11)
        self.assertEqual(len({asset.object_key for asset in assets}), 11)


if __name__ == "__main__":
    unittest.main()
