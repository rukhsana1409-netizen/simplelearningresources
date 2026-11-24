from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "site-tools"))

from catalog_lib import load_resources  # noqa: E402


RESOURCE_ID = "pronouns"
BUNDLE = ROOT / "worksheets/grade-1/reading/pronouns/pronouns.pdf"
PAGES = ROOT / "worksheets/grade-1/reading/pronouns/pronouns"
PREVIEWS = ROOT / "thumbnails/grade-1/reading/grammar-and-sentences/pronouns"
APPROVED_PREVIEWS = ROOT / "worksheets/grade-1/reading/pronouns"
GUIDE = ROOT / "worksheets/grade-1/reading/pronouns/pronouns-parent-guide.pdf"
BUILDER = ROOT / "worksheet-generator/build_pronouns.py"


class Grade1PronounsTests(unittest.TestCase):
    def test_locked_pdf_and_preview_hashes(self) -> None:
        expected_hashes = {
            BUNDLE: "35106634c15c44dab74f6a20e5e32dad9ee1deff2be2ceca1cad0b665dc2001b",
            GUIDE: "7941d5d774ccdd9961c80434fe67716141f5ac760f2679329264dc5e7c6e3fea",
            BUILDER: "2919a80a0ee76b4778963fe32a7af338f924ab7177c385b958e43d8ab01df058",
            PAGES / "page-01.pdf": "84f53f1f0ea58ce172df8cd9fbe330840404d01d3c1383037d9801ba9da9b490",
            PAGES / "page-02.pdf": "e27fc2e44f18c820c90c0069d4a4a66523ff3f9e01a800beec8d491fe392cfcb",
            PAGES / "page-03.pdf": "88d881eabf1bb4d2af7acd7fc3308243aafc07bb00e630163dbf1725fd7be674",
            PAGES / "page-04.pdf": "039789b93cc6ab919a949769cf5bd04058941d77c6ca2ec4cfc8ff683e2c12fc",
            PAGES / "page-05.pdf": "f008f09779c0b82f1f1cc462f2bd5d5b7aa487a8f354f08606f27d5a88a72dcd",
            APPROVED_PREVIEWS / "preview-1.png": "eea47faaa20ca0304296e001646dc054bfc7d53e96ff2e67da95cb0a79a63af2",
            APPROVED_PREVIEWS / "preview-2.png": "d583c4a6d1b5cb916760adb919550e1eee123af129ebd9a9ad39133288a16288",
            APPROVED_PREVIEWS / "preview-3.png": "6f8e5d240dc7697e17025b4caf666d4f2805bbeae57834981c360250f543fc60",
            APPROVED_PREVIEWS / "preview-4.png": "966d9dd0949af8543baa0706905bd27fd5647916bd158bf07a3c4f35624e8ec4",
            APPROVED_PREVIEWS / "preview-5.png": "152be95edf90abd89961b40412ddcc2c8194f8a95f3a689788adcb2f67666d64",
            APPROVED_PREVIEWS / "preview-6.png": "693724e71836482fac8718e492b4b36ac331947a536d9858ae818298a2853e18",
        }
        for path, expected in expected_hashes.items():
            with self.subTest(path=path.name):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected)

    def test_pages_match_bundle_and_previews_keep_approved_dimensions(self) -> None:
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 5)
            for number, bundle_page in enumerate(bundle, start=1):
                with self.subTest(page=number):
                    expected = bundle_page.get_pixmap(dpi=400, colorspace=pymupdf.csRGB, alpha=False)
                    with pymupdf.open(PAGES / f"page-{number:02d}.pdf") as page_pdf:
                        self.assertEqual(page_pdf.page_count, 1)
                        self.assertEqual(tuple(page_pdf[0].rect), (0.0, 0.0, 612.0, 792.0))
                        actual = page_pdf[0].get_pixmap(dpi=400, colorspace=pymupdf.csRGB, alpha=False)
                    self.assertEqual(expected.samples, actual.samples)
                    preview = pymupdf.Pixmap(PREVIEWS / f"page-{number:02d}.png")
                    self.assertEqual((preview.width, preview.height), (1224, 1584))

    def test_catalog_registration_uses_stable_resource_contract(self) -> None:
        resource = next(item for item in load_resources() if item["id"] == RESOURCE_ID)
        self.assertEqual(resource["routing"]["slug"], RESOURCE_ID)
        self.assertEqual(resource["taxonomy"]["topic"], "grammar-and-sentences")
        self.assertEqual(resource["ordering"], {"catalog": 158, "withinTopic": 5})
        self.assertEqual(resource["assets"]["answerKeyPdf"], GUIDE.relative_to(ROOT).as_posix())
        self.assertEqual(resource["assets"]["preview"], {
            "width": 1224,
            "height": 1584,
            "dpi": 144,
            "format": "png",
        })


if __name__ == "__main__":
    unittest.main()
