from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "worksheets/kindergarten/science/materials-motion/pushes-and-pulls.pdf"
PAGE_DIR = ROOT / "worksheets/kindergarten/science/materials-motion/pushes-and-pulls"
PREVIEW_DIR = ROOT / "thumbnails/kindergarten/science/materials-motion/pushes-and-pulls"


class PushesAndPullsAssetsTests(unittest.TestCase):
    def test_approved_bundle_and_derived_assets(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "8bd74fdeffb37cfca3af3d08036c8eaf325aa204e13ee566f4532dfd4c015435",
        )
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 5)
            for index in range(5):
                expected = bundle[index].get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
                page_path = PAGE_DIR / f"page-{index + 1:02d}.pdf"
                preview_path = PREVIEW_DIR / f"page-{index + 1:02d}.png"
                with pymupdf.open(page_path) as page_pdf:
                    self.assertEqual(page_pdf.page_count, 1)
                    actual_page = page_pdf[0].get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
                actual_preview = pymupdf.Pixmap(preview_path)
                self.assertEqual((actual_preview.width, actual_preview.height), (1224, 1584))
                self.assertEqual(actual_page.samples, expected.samples)
                self.assertEqual(actual_preview.samples, expected.samples)


if __name__ == "__main__":
    unittest.main()
