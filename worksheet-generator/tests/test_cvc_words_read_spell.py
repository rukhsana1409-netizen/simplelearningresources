"""Asset-integrity checks for the approved CVC Words Read & Spell pack."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pymupdf


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BUNDLE = REPOSITORY_ROOT / "worksheets/kindergarten/reading/phonics-word-recognition/cvc-words-read-spell.pdf"
PAGE_DIRECTORY = BUNDLE.with_suffix("")
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/kindergarten/reading/phonics-word-recognition/cvc-words-read-spell"
EXPECTED_BUNDLE_MD5 = "aa5c1c6924f6456ec6df8c9b461f5e8d"
EXPECTED_BUNDLE_SHA256 = "58b5cd6fef22a622e6cdbec12c7774081d351408443746e9e78081d75cd01505"
EXPECTED_PAGE_SHA256 = (
    "dadb05f991572c9eb0338cd95b1d71cf33c2abb81238de77f6c2f9ae43f35124",
    "52b9a74e9ea772cfcfd85916d79f1801d3ebe75c30e104557c9e780c45608a66",
    "7902bb3b042344c75443ffd21afd2386f2ff8c5087aed6f44f1b0a52b154cf06",
    "0550c009970089055107ee9ccd6e4202d0f5fc5be5887565c1d724336f2cfa17",
    "e8abb27c8bfa74c1094e295c1c5f761aa11dec99b0afbbdfc0524788036b6f1a",
)


class CvcWordsReadSpellAssetsTests(unittest.TestCase):
    def test_approved_bundle_and_individual_files_are_preserved(self):
        bundle_bytes = BUNDLE.read_bytes()
        self.assertEqual(hashlib.md5(bundle_bytes).hexdigest(), EXPECTED_BUNDLE_MD5)
        self.assertEqual(hashlib.sha256(bundle_bytes).hexdigest(), EXPECTED_BUNDLE_SHA256)
        for page_number, expected_sha256 in enumerate(EXPECTED_PAGE_SHA256, start=1):
            page_path = PAGE_DIRECTORY / f"page-{page_number:02d}.pdf"
            self.assertEqual(hashlib.sha256(page_path.read_bytes()).hexdigest(), expected_sha256)

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 5)
            for page_index in range(bundle.page_count):
                page_number = page_index + 1
                expected = bundle[page_index].get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
                preview = pymupdf.Pixmap(PREVIEW_DIRECTORY / f"page-{page_number:02d}.png")
                self.assertEqual((preview.width, preview.height), (1224, 1584))
                self.assertEqual(preview.samples, expected.samples)
                with pymupdf.open(PAGE_DIRECTORY / f"page-{page_number:02d}.pdf") as page_pdf:
                    self.assertEqual(page_pdf.page_count, 1)
                    rendered = page_pdf[0].get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
                    self.assertEqual(rendered.samples, expected.samples)


if __name__ == "__main__":
    unittest.main()
