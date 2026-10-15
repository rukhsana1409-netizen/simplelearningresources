"""Asset-integrity checks for the approved Building Simple Sentences pack."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pymupdf


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BUNDLE_PATH = REPOSITORY_ROOT / "worksheets/kindergarten/reading/writing-language/building-simple-sentences.pdf"
PAGE_DIRECTORY = BUNDLE_PATH.with_suffix("")
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/kindergarten/reading/writing-language/building-simple-sentences"
EXPECTED_SHA256 = "778a6ac5a59b8dfc29ec0a347c37d6bb9190f3053a59cd1797fda701b468d499"


class BuildingSimpleSentencesAssetsTests(unittest.TestCase):
    def test_approved_bundle_is_preserved(self):
        self.assertEqual(hashlib.sha256(BUNDLE_PATH.read_bytes()).hexdigest(), EXPECTED_SHA256)
        with pymupdf.open(BUNDLE_PATH) as bundle:
            self.assertEqual(bundle.page_count, 5)
            self.assertEqual(
                {(page.rect.width, page.rect.height) for page in bundle},
                {(612.0, 792.0)},
            )

    def test_individual_pages_and_previews_match_the_bundle(self):
        with pymupdf.open(BUNDLE_PATH) as bundle:
            for page_index in range(bundle.page_count):
                page_number = page_index + 1
                with self.subTest(page=page_number):
                    expected = bundle[page_index].get_pixmap(
                        dpi=144, colorspace=pymupdf.csRGB, alpha=False
                    )
                    preview = pymupdf.Pixmap(
                        PREVIEW_DIRECTORY / f"page-{page_number:02d}.png"
                    )
                    self.assertEqual((preview.width, preview.height), (1224, 1584))
                    self.assertEqual(preview.samples, expected.samples)
                    with pymupdf.open(
                        PAGE_DIRECTORY / f"page-{page_number:02d}.pdf"
                    ) as page_pdf:
                        self.assertEqual(page_pdf.page_count, 1)
                        rendered = page_pdf[0].get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                        self.assertEqual(rendered.samples, expected.samples)


if __name__ == "__main__":
    unittest.main()
