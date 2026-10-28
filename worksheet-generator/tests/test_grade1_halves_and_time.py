"""Asset-contract checks for the approved Grade 1 halves and time packs."""

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


PACKS = {
    "halves-and-fourths": {
        "bundle": REPOSITORY_ROOT / "worksheets/grade-1/math/halves-and-fourths/halves-and-fourths.pdf",
        "bundle_hash": "bb9ebb8217c14c3ce9e772fcee5a54aefd4017aa8e3238735de9de839b60f270",
        "answer_key": REPOSITORY_ROOT / "worksheets/grade-1/math/halves-and-fourths/halves-and-fourths-answer-key.pdf",
        "answer_key_hash": "9fe96f848900791d3248739ed9582d0eeacee3742e106207c2431b97be4eaf60",
        "pages": REPOSITORY_ROOT / "worksheets/grade-1/math/halves-and-fourths/halves-and-fourths",
        "previews": REPOSITORY_ROOT / "thumbnails/grade-1/math/shapes-and-fractions/halves-and-fourths",
        "page_hashes": [
            "035e069d8afac784c43c0468256187c55277dee871eead6809a09a9a7b052cd4",
            "2f8a1020da5150878211829406bdee4b575a5360ecc9dd550a1ea3d1cdbf43fe",
            "97fb578c530a2612e30ffa01a6ad45b8b8e4e0098d44efc3d880a6b2a036b59c",
            "27aced3b8ecbbd2a64122d0ccb2db8d4dfc1a8167553b7eafb5e9c7dafa4e9db",
            "bd8deba37160333dc8efc17be1adc3ee37d5e6db3ca0b3f1eaf0ae0b0599d6b6",
        ],
        "asset_count": 12,
    },
    "time-hours-half-hours": {
        "bundle": REPOSITORY_ROOT / "worksheets/grade-1/math/time-hours-half-hours/time-hours-half-hours.pdf",
        "bundle_hash": "744ab3c63c9fb2170a9262bffccb3523502a2e2744ed6c7f8f3816329d540261",
        "pages": REPOSITORY_ROOT / "worksheets/grade-1/math/time-hours-half-hours/time-hours-half-hours",
        "previews": REPOSITORY_ROOT / "thumbnails/grade-1/math/time/time-hours-half-hours",
        "page_hashes": [
            "8dc26b533ab96b9d612f55e38700ed47124c37acfddb05096947702bfcef982b",
            "3e42768ea33a51f1625482808e7810c1201262d851a397e2b5265270ccef819e",
            "c985a1bdb60071284f50ee13364f1d955018fedb838cd067f6581a46de0df2ce",
            "c31b7d9eed040bce87bc7c86ec3836b64ff1a253331bbf02a0a5f8915b02f6de",
            "7f1b1d5702f9cc0e37c285a222505521bf784034637a0b170f2e9e8d5051041d",
        ],
        "asset_count": 11,
    },
}


class Grade1HalvesAndTimeAssetTests(unittest.TestCase):
    def test_approved_artifact_hashes(self):
        for resource_id, pack in PACKS.items():
            with self.subTest(resource=resource_id):
                self.assertEqual(hashlib.sha256(pack["bundle"].read_bytes()).hexdigest(), pack["bundle_hash"])
                if "answer_key" in pack:
                    self.assertEqual(
                        hashlib.sha256(pack["answer_key"].read_bytes()).hexdigest(),
                        pack["answer_key_hash"],
                    )

    def test_pages_and_previews_match_the_approved_bundles(self):
        for resource_id, pack in PACKS.items():
            with pymupdf.open(pack["bundle"]) as bundle:
                self.assertEqual(bundle.page_count, 5)
                for page_number in range(1, 6):
                    with self.subTest(resource=resource_id, page=page_number):
                        expected = bundle[page_number - 1].get_pixmap(
                            dpi=144, colorspace=pymupdf.csRGB, alpha=False
                        )
                        with pymupdf.open(pack["pages"] / f"page-{page_number:02d}.pdf") as page_pdf:
                            self.assertEqual(page_pdf.page_count, 1)
                            actual_page = page_pdf[0].get_pixmap(
                                dpi=144, colorspace=pymupdf.csRGB, alpha=False
                            )
                            self.assertEqual(actual_page.samples, expected.samples)
                        actual_preview = pymupdf.Pixmap(pack["previews"] / f"page-{page_number:02d}.png")
                        self.assertEqual((actual_preview.width, actual_preview.height), (1224, 1584))
                        self.assertEqual(actual_preview.samples, expected.samples)

    def test_individual_page_pdfs_are_the_approved_handoff_files(self):
        for resource_id, pack in PACKS.items():
            with self.subTest(resource=resource_id):
                actual = [
                    hashlib.sha256((pack["pages"] / f"page-{page_number:02d}.pdf").read_bytes()).hexdigest()
                    for page_number in range(1, 6)
                ]
                self.assertEqual(actual, pack["page_hashes"])

    def test_publisher_contracts_include_the_expected_assets(self):
        for resource_id, pack in PACKS.items():
            with self.subTest(resource=resource_id):
                config_path = REPOSITORY_ROOT / f"worksheet-generator/content/{resource_id}.json"
                config = json.loads(config_path.read_text(encoding="utf-8"))
                self.assertEqual(config["asset_output"]["expected_page_count"], 5)
                assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
                self.assertEqual(len(assets), pack["asset_count"])
                self.assertEqual(len({asset.object_key for asset in assets}), pack["asset_count"])
                if resource_id == "time-hours-half-hours":
                    self.assertNotIn("answer_key_pdf", config)


if __name__ == "__main__":
    unittest.main()
