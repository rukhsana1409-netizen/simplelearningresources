import hashlib
import os
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

GENERATOR_DIR = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = GENERATOR_DIR.parent
sys.path.insert(0, str(GENERATOR_DIR))

from publish_assets import (
    BUCKET_NAME,
    ObjectMismatchError,
    ProductionVerificationIncomplete,
    UploadAsset,
    collect_backfill_assets,
    collect_resource_assets,
    load_credentials,
    mime_type_for_path,
    publish_assets,
    validate_unique_keys,
)


class PublishingSafetyTests(unittest.TestCase):
    def _pilot_pdf_asset(self):
        local_path = (
            REPOSITORY_ROOT
            / "worksheets/preschool/math/counting/counting-objects-1-10/page-01.pdf"
        )
        return UploadAsset(
            resource_id="counting-objects-1-10",
            page_number=1,
            local_path=local_path,
            object_key=local_path.relative_to(REPOSITORY_ROOT).as_posix(),
            mime_type="application/pdf",
        )

    def _matching_metadata(self, asset):
        digest = hashlib.md5(asset.local_path.read_bytes(), usedforsecurity=False).hexdigest()
        return {
            "ContentLength": asset.local_path.stat().st_size,
            "ContentType": asset.mime_type,
            "ETag": f'"{digest}"',
        }

    def test_resource_allowlist_uses_exact_bundle_and_page_keys(self):
        config = GENERATOR_DIR / "content/counting-objects-1-10.json"

        assets = collect_resource_assets(REPOSITORY_ROOT, config)

        self.assertEqual(len(assets), 11)
        self.assertEqual(
            assets[0].object_key,
            "worksheets/preschool/math/counting/counting-objects-1-10.pdf",
        )
        self.assertIsNone(assets[0].page_number)
        self.assertEqual(
            {asset.object_key for asset in assets[1:]},
            {
                f"{root}/preschool/math/counting/counting-objects-1-10/page-{page:02d}.{extension}"
                for root, extension in (("worksheets", "pdf"), ("thumbnails", "png"))
                for page in range(1, 6)
            },
        )

    def test_backfill_allowlist_contains_only_expected_page_assets(self):
        assets = collect_backfill_assets(REPOSITORY_ROOT)

        self.assertEqual(len(assets), 154)
        self.assertEqual(sum(asset.mime_type == "application/pdf" for asset in assets), 77)
        self.assertEqual(sum(asset.mime_type == "image/png" for asset in assets), 77)
        self.assertEqual(len({asset.object_key for asset in assets}), 154)
        self.assertTrue(all("/page-" in asset.object_key for asset in assets))
        self.assertTrue(all(asset.page_number is not None for asset in assets))

    def test_mime_type_is_derived_strictly_from_supported_extensions(self):
        self.assertEqual(mime_type_for_path(Path("page-01.pdf")), "application/pdf")
        self.assertEqual(mime_type_for_path(Path("page-01.png")), "image/png")
        with self.assertRaisesRegex(ValueError, "Unsupported upload type"):
            mime_type_for_path(Path("page-01.jpg"))

    def test_duplicate_object_keys_are_rejected(self):
        asset = UploadAsset(
            resource_id="example",
            page_number=1,
            local_path=Path("page-01.pdf"),
            object_key="worksheets/example/page-01.pdf",
            mime_type="application/pdf",
        )
        with self.assertRaisesRegex(ValueError, "Duplicate object key"):
            validate_unique_keys([asset, asset])

    def test_dry_run_never_reads_credentials_or_creates_an_upload_client(self):
        local_path = (
            REPOSITORY_ROOT
            / "worksheets/preschool/math/counting/counting-objects-1-10/page-01.pdf"
        )
        asset = UploadAsset(
            resource_id="example",
            page_number=1,
            local_path=local_path,
            object_key="worksheets/preschool/math/counting/counting-objects-1-10/page-01.pdf",
            mime_type="application/pdf",
        )
        with patch("publish_assets.load_credentials") as credentials, patch(
            "publish_assets.create_r2_client"
        ) as create_client, redirect_stdout(StringIO()):
            result = publish_assets([asset], apply=False)

        self.assertEqual(
            result,
            {
                "planned": 1,
                "already_correct": 0,
                "uploaded": 0,
                "failed": 0,
                "production_verified": 0,
            },
        )
        credentials.assert_not_called()
        create_client.assert_not_called()

    def test_missing_credentials_report_names_without_values(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(
                RuntimeError,
                "R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY",
            ):
                load_credentials()

    def test_already_correct_object_is_skipped(self):
        asset = self._pilot_pdf_asset()
        client = MagicMock(spec=["put_object", "head_object"])
        client.head_object.return_value = self._matching_metadata(asset)
        credentials = {
            "account_id": "account",
            "access_key_id": "key",
            "secret_access_key": "secret",
        }
        with patch("publish_assets.load_credentials", return_value=credentials), patch(
            "publish_assets.create_r2_client", return_value=client
        ), patch("publish_assets.verify_production_asset"):
            result = publish_assets([asset], apply=True)

        self.assertEqual(result["already_correct"], 1)
        self.assertEqual(result["uploaded"], 0)
        self.assertEqual(result["production_verified"], 1)
        client.put_object.assert_not_called()

    def test_missing_object_is_uploaded(self):
        class MissingObjectError(Exception):
            response = {"Error": {"Code": "404"}}

        asset = self._pilot_pdf_asset()
        client = MagicMock(spec=["put_object", "head_object"])
        client.head_object.side_effect = [
            MissingObjectError(),
            self._matching_metadata(asset),
        ]
        credentials = {
            "account_id": "account",
            "access_key_id": "key",
            "secret_access_key": "secret",
        }
        with patch("publish_assets.load_credentials", return_value=credentials), patch(
            "publish_assets.create_r2_client", return_value=client
        ), patch("publish_assets.verify_production_asset"):
            result = publish_assets([asset], apply=True)

        self.assertEqual(result["already_correct"], 0)
        self.assertEqual(result["uploaded"], 1)
        client.put_object.assert_called_once()
        self.assertEqual([call[0] for call in client.method_calls], [
            "head_object",
            "put_object",
            "head_object",
        ])

    def test_mismatched_existing_object_stops_without_overwrite(self):
        asset = self._pilot_pdf_asset()
        client = MagicMock(spec=["put_object", "head_object"])
        metadata = self._matching_metadata(asset)
        metadata["ContentLength"] += 1
        client.head_object.return_value = metadata
        with patch("publish_assets.load_credentials", return_value={
            "account_id": "account",
            "access_key_id": "key",
            "secret_access_key": "secret",
        }), patch("publish_assets.create_r2_client", return_value=client):
            with self.assertRaisesRegex(ObjectMismatchError, asset.object_key):
                publish_assets([asset], apply=True)

        client.put_object.assert_not_called()

    def test_dns_failure_is_reported_after_r2_reconciliation(self):
        asset = self._pilot_pdf_asset()
        client = MagicMock(spec=["put_object", "head_object"])
        client.head_object.return_value = self._matching_metadata(asset)
        with patch("publish_assets.load_credentials", return_value={
            "account_id": "account",
            "access_key_id": "key",
            "secret_access_key": "secret",
        }), patch("publish_assets.create_r2_client", return_value=client), patch(
            "publish_assets.verify_production_asset",
            side_effect=__import__("urllib.error").error.URLError("DNS failed"),
        ):
            with self.assertRaises(ProductionVerificationIncomplete) as caught:
                publish_assets([asset], apply=True)

        message = str(caught.exception)
        self.assertIn("assets.simplelearningresources.com", message)
        self.assertIn(asset.object_key, message)
        self.assertIn("already_correct=1", message)
        self.assertIn("R2 objects are intact", message)
        client.put_object.assert_not_called()

    def test_verify_only_performs_zero_put_calls(self):
        asset = self._pilot_pdf_asset()
        client = MagicMock(spec=["put_object", "head_object"])
        client.head_object.return_value = self._matching_metadata(asset)
        with patch("publish_assets.load_credentials", return_value={
            "account_id": "account",
            "access_key_id": "key",
            "secret_access_key": "secret",
        }), patch("publish_assets.create_r2_client", return_value=client), patch(
            "publish_assets.verify_production_asset"
        ):
            result = publish_assets([asset], apply=False, verify_only=True)

        self.assertEqual(result["already_correct"], 1)
        self.assertEqual(result["uploaded"], 0)
        self.assertEqual(result["production_verified"], 1)
        client.put_object.assert_not_called()
        client.head_object.assert_called_once_with(
            Bucket=BUCKET_NAME, Key=asset.object_key
        )


if __name__ == "__main__":
    unittest.main()
