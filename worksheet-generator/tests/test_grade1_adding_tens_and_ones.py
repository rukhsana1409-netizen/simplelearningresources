"""Asset-contract checks for the approved Grade 1 addition pack."""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

import pymupdf


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "worksheet-generator"))

from publish_assets import collect_resource_assets  # noqa: E402


BUNDLE = REPOSITORY_ROOT / "worksheets/grade-1/math/adding-tens-and-ones/adding-tens-and-ones.pdf"
PAGE_DIRECTORY = REPOSITORY_ROOT / "worksheets/grade-1/math/adding-tens-and-ones/adding-tens-and-ones"
PREVIEW_DIRECTORY = REPOSITORY_ROOT / "thumbnails/grade-1/math/addition/adding-tens-and-ones"
APPROVED_PAGE_HASHES = [
    "ef235efaf044e47bec787f925a90ea5013c6c6d9ed3d9ccd29394988f127e7ed",
    "80963ee7070da84e95176c6fe66ff531aee0bcd7d195ba1972356550e478366f",
    "f6935b9f82062e7e01f0a650a94a7f74b24dc02b4208132ddac55fa58eff594c",
    "2d5f70f181762ddf03eae878312025d84130fe7a6524a6fe0ad9104c0b03ae36",
    "2bb1511227b46b426f87ee615b0d769bfe0e1cea9d1a85ecc15904c84b32e629",
    "92d8e762d52aa203d707c8adff2e824ffed045ce99586c8724695348e1ee9f30",
    "51c2109c69a18d0702717e62107fd1bafe0a6194d4280429cbf3c9c7a25004ed",
]


class AddingTensAndOnesAssetTests(unittest.TestCase):
    def test_approved_bundle_hash(self):
        self.assertEqual(
            hashlib.sha256(BUNDLE.read_bytes()).hexdigest(),
            "3578ddf0ec265aec63e67e275ea584f82ae0cb7b51771fa9ab96ac71dc97617a",
        )

    def test_pages_and_previews_match_the_approved_bundle(self):
        with pymupdf.open(BUNDLE) as bundle:
            self.assertEqual(bundle.page_count, 7)
            for page_number in range(1, 8):
                with self.subTest(page=page_number):
                    expected = bundle[page_number - 1].get_pixmap(
                        dpi=144, colorspace=pymupdf.csRGB, alpha=False
                    )
                    with pymupdf.open(PAGE_DIRECTORY / f"page-{page_number:02d}.pdf") as page_pdf:
                        self.assertEqual(page_pdf.page_count, 1)
                        actual_page = page_pdf[0].get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                        self.assertEqual(actual_page.samples, expected.samples)
                    actual_preview = pymupdf.Pixmap(PREVIEW_DIRECTORY / f"page-{page_number:02d}.png")
                    self.assertEqual((actual_preview.width, actual_preview.height), (1224, 1584))
                    self.assertEqual(actual_preview.samples, expected.samples)

    def test_individual_page_pdfs_are_the_approved_handoff_files(self):
        actual = [
            hashlib.sha256((PAGE_DIRECTORY / f"page-{page_number:02d}.pdf").read_bytes()).hexdigest()
            for page_number in range(1, 8)
        ]
        self.assertEqual(actual, APPROVED_PAGE_HASHES)

    def test_publisher_contract_has_no_answer_key_and_fifteen_assets(self):
        config_path = REPOSITORY_ROOT / "worksheet-generator/content/adding-tens-and-ones.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertNotIn("answer_key_pdf", config)
        self.assertEqual(config["asset_output"]["expected_page_count"], 7)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
        self.assertEqual(len(assets), 15)
        self.assertEqual(len({asset.object_key for asset in assets}), 15)


if __name__ == "__main__":
    unittest.main()
