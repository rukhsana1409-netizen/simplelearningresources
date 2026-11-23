from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[2]
PACKS = (
    {
        "id": "word-meanings",
        "bundle": ROOT / "worksheets/grade-1/reading/word-meanings/word-meanings.pdf",
        "pages": ROOT / "worksheets/grade-1/reading/word-meanings/word-meanings",
        "previews": ROOT / "thumbnails/grade-1/reading/vocabulary/word-meanings",
        "guide": ROOT / "worksheets/grade-1/reading/word-meanings/word-meanings-parent-guide.pdf",
        "bundle_hash": "73f68ef2510eecbaf86f5b456f9a0da94ebbff609eb07ab38d7ba893182a9477",
        "guide_hash": "6241b8ba9552f100dc63815d2819bf7cd249054c94ad38f156e3e5bc569a42de",
    },
    {
        "id": "joining-words-and-sentence-types",
        "bundle": ROOT / "worksheets/grade-1/reading/joining-words-and-sentence-types/joining-words-and-sentence-types.pdf",
        "pages": ROOT / "worksheets/grade-1/reading/joining-words-and-sentence-types/joining-words-and-sentence-types",
        "previews": ROOT / "thumbnails/grade-1/reading/grammar-and-sentences/joining-words-and-sentence-types",
        "guide": ROOT / "worksheets/grade-1/reading/joining-words-and-sentence-types/joining-words-and-sentence-types-parent-guide.pdf",
        "bundle_hash": "f2d09fde6fb8bf161d345783e44618be5ca70ed0c58dcb1a7e514c4a043ab9c6",
        "guide_hash": "21028636002b37f89963075ed2e0de488a647ca1321f8dc2e01cce4016355157",
    },
)


class Grade1WordMeaningAndSentenceTests(unittest.TestCase):
    def test_locked_bundle_and_parent_guide_hashes(self) -> None:
        for pack in PACKS:
            with self.subTest(resource=pack["id"]):
                self.assertEqual(hashlib.sha256(pack["bundle"].read_bytes()).hexdigest(), pack["bundle_hash"])
                self.assertEqual(hashlib.sha256(pack["guide"].read_bytes()).hexdigest(), pack["guide_hash"])

    def test_pages_and_previews_match_the_locked_bundles(self) -> None:
        for pack in PACKS:
            with pymupdf.open(pack["bundle"]) as bundle:
                self.assertEqual(bundle.page_count, 5)
                for number, bundle_page in enumerate(bundle, start=1):
                    with self.subTest(resource=pack["id"], page=number):
                        expected = bundle_page.get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
                        with pymupdf.open(pack["pages"] / f"page-{number:02d}.pdf") as page_pdf:
                            self.assertEqual(page_pdf.page_count, 1)
                            self.assertEqual(tuple(page_pdf[0].rect), (0.0, 0.0, 612.0, 792.0))
                            actual = page_pdf[0].get_pixmap(dpi=144, colorspace=pymupdf.csRGB, alpha=False)
                        preview = pymupdf.Pixmap(pack["previews"] / f"page-{number:02d}.png")
                        self.assertEqual(expected.samples, actual.samples)
                        self.assertEqual(expected.samples, preview.samples)
                        self.assertEqual((preview.width, preview.height), (1224, 1584))


if __name__ == "__main__":
    unittest.main()
