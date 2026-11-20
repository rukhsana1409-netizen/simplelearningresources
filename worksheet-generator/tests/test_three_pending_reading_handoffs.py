from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[2]
RESOURCES = (
    {
        "id": "story-retelling",
        "bundle": ROOT / "worksheets/kindergarten/reading/reading-comprehension/story-retelling.pdf",
        "bundle_hash": "63c67f39d9d83db392f7e4fc224edb22b6602e871c55f4f691acdc9ad0425537",
        "pages": ROOT / "worksheets/kindergarten/reading/reading-comprehension/story-retelling",
        "previews": ROOT / "thumbnails/kindergarten/reading/reading-comprehension/story-retelling",
        "supporting": ROOT / "worksheets/kindergarten/reading/reading-comprehension/story-retelling-answer-key.pdf",
    },
    {
        "id": "poetry-and-feeling-words",
        "bundle": ROOT / "worksheets/grade-1/reading/poetry-and-feeling-words/poetry-and-feeling-words.pdf",
        "bundle_hash": "cbdcf4b2a3748b1eee73f6c7968e2ed529eed48936a4c982bae07444adf0e46f",
        "pages": ROOT / "worksheets/grade-1/reading/poetry-and-feeling-words/poetry-and-feeling-words",
        "previews": ROOT / "thumbnails/grade-1/reading/reading-comprehension/poetry-and-feeling-words",
        "supporting": ROOT / "worksheets/grade-1/reading/poetry-and-feeling-words/poetry-and-feeling-words-parent-guide.pdf",
    },
    {
        "id": "who-is-telling-the-story",
        "bundle": ROOT / "worksheets/grade-1/reading/who-is-telling-the-story/who-is-telling-the-story.pdf",
        "bundle_hash": "93203e8fd4b5046c0e3c8b628aa671799c24d585a57d53110ef9fbfa0ade3787",
        "pages": ROOT / "worksheets/grade-1/reading/who-is-telling-the-story/who-is-telling-the-story",
        "previews": ROOT / "thumbnails/grade-1/reading/reading-comprehension/who-is-telling-the-story",
        "supporting": ROOT / "worksheets/grade-1/reading/who-is-telling-the-story/who-is-telling-the-story-parent-guide.pdf",
    },
)


class ThreePendingReadingHandoffsTests(unittest.TestCase):
    def test_locked_bundles_and_supporting_pdfs_are_present(self) -> None:
        for resource in RESOURCES:
            with self.subTest(resource=resource["id"]):
                digest = hashlib.sha256(resource["bundle"].read_bytes()).hexdigest()
                self.assertEqual(resource["bundle_hash"], digest)
                self.assertGreater(resource["supporting"].stat().st_size, 0)

    def test_pages_and_previews_match_each_locked_bundle(self) -> None:
        for resource in RESOURCES:
            with pymupdf.open(resource["bundle"]) as bundle:
                self.assertEqual(5, bundle.page_count, resource["id"])
                for number, bundle_page in enumerate(bundle, start=1):
                    page_path = resource["pages"] / f"page-{number:02d}.pdf"
                    preview_path = resource["previews"] / f"page-{number:02d}.png"
                    with self.subTest(resource=resource["id"], page=number):
                        with pymupdf.open(page_path) as page_pdf:
                            self.assertEqual(1, page_pdf.page_count)
                            actual_page = page_pdf[0].get_pixmap(
                                dpi=144, colorspace=pymupdf.csRGB, alpha=False
                            )
                        expected_page = bundle_page.get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                        preview = pymupdf.Pixmap(preview_path)
                        self.assertEqual(expected_page.samples, actual_page.samples)
                        self.assertEqual(expected_page.samples, preview.samples)
                        self.assertEqual((1224, 1584), (preview.width, preview.height))


if __name__ == "__main__":
    unittest.main()
