from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "worksheets/grade-1/reading/two-books-one-topic/two-books-one-topic.pdf"
PAGES = ROOT / "worksheets/grade-1/reading/two-books-one-topic/two-books-one-topic"
PREVIEWS = ROOT / "thumbnails/grade-1/reading/informational-reading/two-books-one-topic"
PARENT_GUIDE = ROOT / "worksheets/grade-1/reading/two-books-one-topic/two-books-one-topic-parent-guide.pdf"


class TwoBooksOneTopicTests(unittest.TestCase):
    def test_locked_bundle_and_parent_guide_hashes(self) -> None:
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "e72aa8353e504cb88606a7d366203d0d39a4b6d7353e3a259835c5d4beccbbea",
        )
        self.assertEqual(
            hashlib.sha256(PARENT_GUIDE.read_bytes()).hexdigest(),
            "14246ac3077492bd7f6d53ed4c92f6f4d9cddfac1ceb54cccddb1c976ecda19b",
        )

    def test_pages_and_previews_match_the_locked_bundle(self) -> None:
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 5)
            for number, bundle_page in enumerate(bundle, start=1):
                with self.subTest(page=number):
                    expected = bundle_page.get_pixmap(
                        dpi=144, colorspace=pymupdf.csRGB, alpha=False
                    )
                    with pymupdf.open(PAGES / f"page-{number:02d}.pdf") as page_pdf:
                        self.assertEqual(page_pdf.page_count, 1)
                        actual = page_pdf[0].get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                    preview = pymupdf.Pixmap(PREVIEWS / f"page-{number:02d}.png")
                    self.assertEqual(expected.samples, actual.samples)
                    self.assertEqual(expected.samples, preview.samples)
                    self.assertEqual((preview.width, preview.height), (1224, 1584))


if __name__ == "__main__":
    unittest.main()
