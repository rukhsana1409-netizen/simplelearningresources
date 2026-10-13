"""Asset-integrity checks for the approved Letter Sounds A–Z pack."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pymupdf


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BUNDLE = REPOSITORY_ROOT / "worksheets/kindergarten/reading/phonics-word-recognition/letter-sounds-a-z.pdf"
PAGE_DIRECTORY = BUNDLE.with_suffix("")
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/kindergarten/reading/phonics-word-recognition/letter-sounds-a-z"
EXPECTED_BUNDLE_MD5 = "7466bc29d31b14c809c7da6e2a42a1a8"
EXPECTED_BUNDLE_SHA256 = "697ccd4fd7bf7a8520aefdebb9b979060b8284a98b21e998b6378e51fab902da"
EXPECTED_PAGE_SHA256 = (
    "afffe575cd701e63af1c299fdae7c753c7f53eb8cc4d97d4d4fe14a7abbca953",
    "06a8e29b597104de420bfe1af0dede4d9454996e5ed64d63ef1b17510f24a09f",
    "8be655a56ea74c34af0a991c00a283c78bd0963cb2fd8df96665192985ee087a",
    "86c1ebbcc09528dd88454f4ebb2aee983f0e0d94b0e0c2eb5268e7ea99a3f925",
    "fd0864ed165f7696e1fcbbb8414d60b521586a506cfe9d2038faf2c265f54858",
    "7a30c2cf79bd04ef6eaf34d59ea1b5b3ea293a003021dbe336ebf30bac0e84f7",
)


class LetterSoundsAssetsTests(unittest.TestCase):
    def test_approved_bundle_and_individual_files_are_preserved(self):
        bundle_bytes = BUNDLE.read_bytes()
        self.assertEqual(hashlib.md5(bundle_bytes).hexdigest(), EXPECTED_BUNDLE_MD5)
        self.assertEqual(hashlib.sha256(bundle_bytes).hexdigest(), EXPECTED_BUNDLE_SHA256)
        for page_number, expected_sha256 in enumerate(EXPECTED_PAGE_SHA256, start=1):
            page_path = PAGE_DIRECTORY / f"page-{page_number:02d}.pdf"
            self.assertEqual(hashlib.sha256(page_path.read_bytes()).hexdigest(), expected_sha256)

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 6)
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
