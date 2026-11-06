"""Asset-contract checks for the five approved Muse handoffs integrated together."""

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


RESOURCES = {
    "build-and-compose-shapes": {
        "bundle": "worksheets/grade-1/math/build-and-compose-shapes/build-and-compose-shapes.pdf",
        "pages": "worksheets/grade-1/math/build-and-compose-shapes/build-and-compose-shapes",
        "previews": "thumbnails/grade-1/math/shapes-and-fractions/build-and-compose-shapes",
        "count": 1,
        "sha256": "776b051caec904e01fd0632406f68069fe09590898657782dd09f46570635e89",
    },
    "sounds-in-words": {
        "bundle": "worksheets/grade-1/reading/sounds-in-words/sounds-in-words.pdf",
        "pages": "worksheets/grade-1/reading/sounds-in-words/sounds-in-words",
        "previews": "thumbnails/grade-1/reading/phonics-and-word-reading/sounds-in-words",
        "count": 4,
        "sha256": "91d80cf39c2a22d7f9785ecf4955d86a3886d75d4bf9856479835c43cbd44e31",
    },
    "word-detectives": {
        "bundle": "worksheets/grade-1/reading/word-detectives/word-detectives.pdf",
        "pages": "worksheets/grade-1/reading/word-detectives/word-detectives",
        "previews": "thumbnails/grade-1/reading/phonics-and-word-reading/word-detectives",
        "count": 5,
        "sha256": "e340fdac14bc51161e1b57fd9e7a6d2a7f93bf271405aa7930ab15dab3e29fe5",
    },
    "prepositions": {
        "bundle": "worksheets/grade-1/reading/prepositions/prepositions.pdf",
        "pages": "worksheets/grade-1/reading/prepositions/prepositions",
        "previews": "thumbnails/grade-1/reading/grammar-and-sentences/prepositions",
        "count": 1,
        "sha256": "867cf313792586c06b93adb49cc5d85899f5b52ac3535b77b9f5bfd16d8dbce8",
    },
    "oops-say-it-again": {
        "bundle": "worksheets/kindergarten/communication/oops-say-it-again/oops-say-it-again.pdf",
        "pages": "worksheets/kindergarten/communication/oops-say-it-again/oops-say-it-again",
        "previews": "thumbnails/kindergarten/communication/oops-say-it-again/oops-say-it-again",
        "count": 4,
        "sha256": "ab8f1b4d4313bc4f1867b39eae963052dd4d50b705b05d4e5af4ae3ae2a0e209",
    },
}


class FiveApprovedHandoffAssetTests(unittest.TestCase):
    def test_approved_bundle_hashes_and_letter_page_counts(self):
        for resource_id, resource in RESOURCES.items():
            with self.subTest(resource=resource_id):
                bundle_path = REPOSITORY_ROOT / resource["bundle"]
                self.assertEqual(hashlib.sha256(bundle_path.read_bytes()).hexdigest(), resource["sha256"])
                with pymupdf.open(bundle_path) as bundle:
                    self.assertEqual(bundle.page_count, resource["count"])
                    self.assertEqual({(page.rect.width, page.rect.height) for page in bundle}, {(612.0, 792.0)})

    def test_individual_pages_and_previews_match_bundles(self):
        for resource_id, resource in RESOURCES.items():
            with pymupdf.open(REPOSITORY_ROOT / resource["bundle"]) as bundle:
                for page_number in range(1, resource["count"] + 1):
                    with self.subTest(resource=resource_id, page=page_number):
                        expected = bundle[page_number - 1].get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                        page_path = REPOSITORY_ROOT / resource["pages"] / f"page-{page_number:02d}.pdf"
                        with pymupdf.open(page_path) as page_pdf:
                            self.assertEqual(page_pdf.page_count, 1)
                            actual_page = page_pdf[0].get_pixmap(
                                dpi=144, colorspace=pymupdf.csRGB, alpha=False
                            )
                            self.assertEqual(actual_page.samples, expected.samples)
                        preview_path = REPOSITORY_ROOT / resource["previews"] / f"page-{page_number:02d}.png"
                        actual_preview = pymupdf.Pixmap(preview_path)
                        self.assertEqual((actual_preview.width, actual_preview.height), (1224, 1584))
                        self.assertEqual(actual_preview.samples, expected.samples)

    def test_publisher_contracts_have_expected_asset_counts_and_no_answer_keys(self):
        for resource_id, resource in RESOURCES.items():
            with self.subTest(resource=resource_id):
                config_path = REPOSITORY_ROOT / "worksheet-generator/content" / f"{resource_id}.json"
                config = json.loads(config_path.read_text(encoding="utf-8"))
                self.assertNotIn("answer_key_pdf", config)
                self.assertEqual(config["asset_output"]["expected_page_count"], resource["count"])
                assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
                self.assertEqual(len(assets), 1 + resource["count"] * 2)
                self.assertEqual(len({asset.object_key for asset in assets}), len(assets))


if __name__ == "__main__":
    unittest.main()
