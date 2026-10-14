"""Asset-integrity checks for the three approved Kindergarten literacy packs."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pymupdf


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PACKS = (
    (
        "common-words-read-learn",
        REPOSITORY_ROOT / "worksheets/kindergarten/reading/phonics-word-recognition/common-words-read-learn.pdf",
        REPOSITORY_ROOT / "thumbnails/kindergarten/reading/phonics-word-recognition/common-words-read-learn",
        "7f7d2433fe7cd30ffdbca9ae2620f8f4cdefa33676ac365c8a3434d44abe69e6",
    ),
    (
        "understanding-print-sentences",
        REPOSITORY_ROOT / "worksheets/kindergarten/reading/alphabet-print-concepts/understanding-print-sentences.pdf",
        REPOSITORY_ROOT / "thumbnails/kindergarten/reading/alphabet-print-concepts/understanding-print-sentences",
        "b848118d8d89d2febcf6526e133b7c9379dedf408af412ab7cd065dc657b60eb",
    ),
    (
        "emergent-decodable-reading",
        REPOSITORY_ROOT / "worksheets/kindergarten/reading/fluency/emergent-decodable-reading.pdf",
        REPOSITORY_ROOT / "thumbnails/kindergarten/reading/fluency/emergent-decodable-reading",
        "3f7b9a82f54823de90db8980f9f260da9b11d6fb995edd9c1ce3f22c1947a4a5",
    ),
)


class KindergartenLiteracyPackAssetsTests(unittest.TestCase):
    def test_approved_bundles_are_preserved(self):
        for resource_id, bundle_path, _, expected_sha256 in PACKS:
            with self.subTest(resource=resource_id):
                self.assertEqual(hashlib.sha256(bundle_path.read_bytes()).hexdigest(), expected_sha256)
                with pymupdf.open(bundle_path) as bundle:
                    self.assertEqual(bundle.page_count, 5)
                    self.assertEqual({(page.rect.width, page.rect.height) for page in bundle}, {(612.0, 792.0)})

    def test_individual_pages_and_previews_match_the_bundles(self):
        for resource_id, bundle_path, preview_directory, _ in PACKS:
            page_directory = bundle_path.with_suffix("")
            with pymupdf.open(bundle_path) as bundle:
                for page_index in range(bundle.page_count):
                    page_number = page_index + 1
                    with self.subTest(resource=resource_id, page=page_number):
                        expected = bundle[page_index].get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                        preview = pymupdf.Pixmap(preview_directory / f"page-{page_number:02d}.png")
                        self.assertEqual((preview.width, preview.height), (1224, 1584))
                        self.assertEqual(preview.samples, expected.samples)
                        with pymupdf.open(page_directory / f"page-{page_number:02d}.pdf") as page_pdf:
                            self.assertEqual(page_pdf.page_count, 1)
                            rendered = page_pdf[0].get_pixmap(
                                dpi=144, colorspace=pymupdf.csRGB, alpha=False
                            )
                            self.assertEqual(rendered.samples, expected.samples)


if __name__ == "__main__":
    unittest.main()
