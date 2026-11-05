"""Asset-contract checks for the approved Grade 1 counting-patterns pack."""

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


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/counting-patterns-10-more-less/counting-patterns-10-more-less.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/counting-patterns-10-more-less/counting-patterns-10-more-less"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/numbers-and-place-value/counting-patterns-10-more-less"
APPROVED_PAGE_HASHES = [
    "5fd45ee313c435592b1c3c2af62f0f4387840b2be00ec247d4f4c5ff4f79cb48",
    "6206063e3bc586b12c03d80ca5d422412564449ceefff936f2b5e2d389c76293",
    "84950fea51a0e7f08611bed721b25d6e592f62998ce602fcb3a7c5a2a367b5e4",
    "81e234d2dfd0f84a7dd666a23c94d05e038e1e7b26f5fbb510be99a1b3129125",
    "d7d2c2026e4a57ec97f66661eb07d28238e48499076d8692b9b4eec37713d9e7",
]


class CountingPatternsAssetTests(unittest.TestCase):
    def test_approved_bundle_hash(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "3c05b166154052d9fa75f3c5fd4b72b7f328eb6297a8b76585f451acec59c6d1",
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

    def test_individual_page_pdfs_are_approved_handoff_files(self):
        actual_pages = [
            hashlib.sha256((PAGE_DIRECTORY / f"page-{page_number:02d}.pdf").read_bytes()).hexdigest()
            for page_number in range(1, 6)
        ]
        self.assertEqual(actual_pages, APPROVED_PAGE_HASHES)

    def test_publisher_contract_has_no_answer_key_and_eleven_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/counting-patterns-10-more-less.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertNotIn("answer_key_pdf", config)
        self.assertEqual(config["asset_output"]["expected_page_count"], 5)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 11)
        self.assertEqual(len({asset.object_key for asset in assets}), 11)


if __name__ == "__main__":
    unittest.main()
