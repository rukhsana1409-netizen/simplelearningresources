import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pymupdf


GENERATOR_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GENERATOR_DIR))

from bundle_assets import (
    BundleAssetContract,
    _inherit_destination_permissions,
    generate_bundle_assets,
)


class BundleAssetContractTests(unittest.TestCase):
    def test_builds_zero_padded_page_paths(self):
        contract = BundleAssetContract.from_dict(
            {
                "resource_id": "example-pack",
                "expected_page_count": 12,
                "page_pdf_directory": "worksheets/example-pack",
                "preview_directory": "thumbnails/example-pack",
            }
        )

        self.assertEqual(contract.page_pdf_path(1), Path("worksheets/example-pack/page-01.pdf"))
        self.assertEqual(contract.page_pdf_path(12), Path("worksheets/example-pack/page-12.pdf"))
        self.assertEqual(contract.preview_path(1), Path("thumbnails/example-pack/page-01.png"))

    def test_rejects_parent_directory_traversal(self):
        with self.assertRaisesRegex(ValueError, "relative path"):
            BundleAssetContract.from_dict(
                {
                    "resource_id": "example-pack",
                    "expected_page_count": 1,
                    "page_pdf_directory": "../outside",
                    "preview_directory": "thumbnails/example-pack",
                }
            )


class BundleAssetGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.bundle_path = self.root / "bundle.pdf"
        document = pymupdf.open()
        for label in ("Page one", "Page two"):
            page = document.new_page(width=612, height=792)
            page.insert_text((72, 72), label, fontsize=24)
        document.save(self.bundle_path)
        document.close()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_generates_single_page_pdfs_and_consistent_previews(self):
        contract = BundleAssetContract.from_dict(
            {
                "resource_id": "example-pack",
                "expected_page_count": 2,
                "page_pdf_directory": "worksheets/example-pack",
                "preview_directory": "thumbnails/example-pack",
            }
        )

        assets = generate_bundle_assets(self.bundle_path, contract, self.root)

        self.assertEqual(len(assets), 2)
        self.assertEqual({asset.preview_dimensions for asset in assets}, {(1224, 1584)})
        for asset in assets:
            with pymupdf.open(asset.page_pdf_path) as page_document:
                self.assertEqual(page_document.page_count, 1)
            preview = pymupdf.Pixmap(asset.preview_path)
            self.assertEqual((preview.width, preview.height), asset.preview_dimensions)
            self.assertGreater(asset.page_pdf_path.stat().st_size, 0)
            self.assertGreater(asset.preview_path.stat().st_size, 0)

    def test_rejects_an_unexpected_bundle_page_count(self):
        contract = BundleAssetContract.from_dict(
            {
                "resource_id": "example-pack",
                "expected_page_count": 3,
                "page_pdf_directory": "worksheets/example-pack",
                "preview_directory": "thumbnails/example-pack",
            }
        )

        with self.assertRaisesRegex(ValueError, "expected 3 pages but found 2"):
            generate_bundle_assets(self.bundle_path, contract, self.root)

        self.assertFalse((self.root / "worksheets").exists())
        self.assertFalse((self.root / "thumbnails").exists())


class DestinationPermissionTests(unittest.TestCase):
    def test_resets_only_the_final_file_acl_on_windows(self):
        final_path = Path(r"C:\assets\page-01.pdf")

        with patch("bundle_assets.os.name", "nt"), patch(
            "bundle_assets.subprocess.run"
        ) as run:
            _inherit_destination_permissions(final_path)

        run.assert_called_once_with(
            ["icacls", str(final_path), "/reset"],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_does_not_change_permissions_on_non_windows_platforms(self):
        with patch("bundle_assets.os.name", "posix"), patch(
            "bundle_assets.subprocess.run"
        ) as run:
            _inherit_destination_permissions(Path("/assets/page-01.pdf"))

        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
