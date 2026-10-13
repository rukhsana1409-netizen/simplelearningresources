"""Asset-integrity checks for the approved Blending & Segmenting pack."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pymupdf


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BUNDLE = REPOSITORY_ROOT / "worksheets/kindergarten/reading/phonological-awareness/blending-segmenting.pdf"
PAGE_DIRECTORY = BUNDLE.with_suffix("")
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/kindergarten/reading/phonological-awareness/blending-segmenting"
EXPECTED_BUNDLE_MD5 = "ccf97ca0baeeadbd5b7909792b6473d5"
EXPECTED_BUNDLE_SHA256 = "ac45685a0cde24a57a987bcf4c8a2667f01411d708c0f738d40d06cbd8f99ee6"
EXPECTED_PAGE_SHA256 = (
    "078fa5e5ffac6437209256515819eb5e9ad73684ff5e71e871bb588bc2060178",
    "557135c172cec4914270f9907ba79e54cddb94499389a9d33cfe2056cf914709",
    "8a9626b870f90af12a71263f020381bba2f23cc740ed969d5efe1b072f7ababd",
    "0532264c5e9564a9a80481364f9b0def5429325a5524b36720ce51b6d54136cf",
    "4ea903ab74d24c3281748e06d4de94dd6498d1f3e400cff4acfb93fd69872223",
)


class BlendingSegmentingAssetsTests(unittest.TestCase):
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
