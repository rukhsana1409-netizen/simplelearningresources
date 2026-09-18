"""Validate and publish canonical worksheet assets to Cloudflare R2."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

import pymupdf

from bundle_assets import BundleAssetContract


BUCKET_NAME = "learning-made-simple-assets"
PRODUCTION_ASSET_BASE_URL = "https://assets.simplelearningresources.com"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIRECTORY = Path(__file__).resolve().parent / "content"
REQUIRED_CREDENTIALS = (
    "R2_ACCOUNT_ID",
    "R2_ACCESS_KEY_ID",
    "R2_SECRET_ACCESS_KEY",
)
PAGE_ASSET_BACKFILL_RESOURCE_IDS = frozenset({
    "2d-shapes",
    "addition-facts-within-5",
    "addition-to-5",
    "counting-objects-1-10",
    "counting-objects-1-5",
    "counting-objects-11-20",
    "more-fewer-same-1-10",
    "number-order-1-10",
    "number-order-11-20",
    "number-recognition-1-5",
    "number-recognition-6-10",
    "number-recognition-11-15",
    "number-recognition-16-20",
    "simple-addition-subtraction-stories",
    "subtracting-within-5",
    "subtraction-facts-within-5",
})


@dataclass(frozen=True)
class UploadAsset:
    resource_id: str
    page_number: int | None
    local_path: Path
    object_key: str
    mime_type: str


class ObjectMismatchError(RuntimeError):
    """An existing R2 object does not exactly match its local source."""

    def __init__(self, object_key: str, details: list[str], result: dict[str, int]):
        self.result = result.copy()
        counts = " ".join(f"{name}={value}" for name, value in self.result.items())
        super().__init__(
            f"Existing R2 object differs for {object_key}: {', '.join(details)}; {counts}"
        )


class ProductionVerificationIncomplete(RuntimeError):
    """R2 reconciliation succeeded, but production verification was interrupted."""

    def __init__(self, object_key: str, result: dict[str, int]):
        self.result = result.copy()
        hostname = urlparse(PRODUCTION_ASSET_BASE_URL).hostname or PRODUCTION_ASSET_BASE_URL
        counts = " ".join(f"{name}={value}" for name, value in self.result.items())
        super().__init__(
            f"Production verification could not resolve or reach hostname={hostname}; "
            f"object_key={object_key}; {counts}. R2 objects are intact and production "
            "verification was incomplete."
        )


def mime_type_for_path(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return "application/pdf"
    if suffix == ".png":
        return "image/png"
    raise ValueError(f"Unsupported upload type: {path}")


def _repository_file(repository_root: Path, relative_path: Path) -> Path:
    repository_root = repository_root.resolve()
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError(f"Upload path must be repository-relative: {relative_path}")
    resolved = (repository_root / relative_path).resolve()
    if resolved != repository_root and repository_root not in resolved.parents:
        raise ValueError(f"Upload path leaves repository: {relative_path}")
    return resolved


def _upload_asset(
    repository_root: Path,
    resource_id: str,
    page_number: int | None,
    relative_path: Path,
) -> UploadAsset:
    local_path = _repository_file(repository_root, relative_path)
    return UploadAsset(
        resource_id=resource_id,
        page_number=page_number,
        local_path=local_path,
        object_key=relative_path.as_posix(),
        mime_type=mime_type_for_path(relative_path),
    )


def _load_contract(config_path: Path) -> tuple[dict, BundleAssetContract]:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    asset_output = data.get("asset_output")
    if asset_output is None:
        raise ValueError(f"Canonical asset_output is missing: {config_path}")
    return data, BundleAssetContract.from_dict(asset_output)


def _canonical_config_paths() -> list[Path]:
    paths = []
    for path in sorted(CONTENT_DIRECTORY.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        resource_id = (data.get("asset_output") or {}).get("resource_id")
        if resource_id in PAGE_ASSET_BACKFILL_RESOURCE_IDS:
            paths.append(path)
    if len(paths) != 16:
        raise ValueError(f"Expected 16 canonical resource configs but found {len(paths)}.")
    return paths


def _page_assets(
    repository_root: Path, contract: BundleAssetContract
) -> list[UploadAsset]:
    assets: list[UploadAsset] = []
    for page_number in range(1, contract.expected_page_count + 1):
        assets.append(
            _upload_asset(
                repository_root,
                contract.resource_id,
                page_number,
                contract.page_pdf_path(page_number),
            )
        )
        assets.append(
            _upload_asset(
                repository_root,
                contract.resource_id,
                page_number,
                contract.preview_path(page_number),
            )
        )
    return assets


def collect_resource_assets(repository_root: Path, config_path: Path) -> list[UploadAsset]:
    data, contract = _load_contract(config_path)
    bundle_relative_path = contract.page_pdf_directory.with_suffix(".pdf")
    if bundle_relative_path.name != data.get("filename"):
        raise ValueError(
            f"Bundle path does not match filename for {contract.resource_id}: "
            f"{bundle_relative_path} != {data.get('filename')}"
        )
    assets = [
        _upload_asset(
            repository_root,
            contract.resource_id,
            None,
            bundle_relative_path,
        )
    ]
    assets.extend(_page_assets(repository_root, contract))
    validate_assets(assets, expected_page_count=contract.expected_page_count)
    return assets


def collect_backfill_assets(repository_root: Path) -> list[UploadAsset]:
    assets: list[UploadAsset] = []
    for config_path in _canonical_config_paths():
        _, contract = _load_contract(config_path)
        assets.extend(_page_assets(repository_root, contract))
    validate_assets(assets)
    pdf_count = sum(asset.mime_type == "application/pdf" for asset in assets)
    png_count = sum(asset.mime_type == "image/png" for asset in assets)
    if pdf_count != 77 or png_count != 77 or len(assets) != 154:
        raise ValueError(
            "Backfill must contain exactly 77 page PDFs and 77 PNG previews; "
            f"found PDFs={pdf_count}, PNGs={png_count}, total={len(assets)}."
        )
    if any(asset.page_number is None for asset in assets):
        raise ValueError("Backfill page-assets-only allowlist contains a bundle PDF.")
    return assets


def validate_unique_keys(assets: Iterable[UploadAsset]) -> None:
    seen: set[str] = set()
    for asset in assets:
        if asset.object_key in seen:
            raise ValueError(f"Duplicate object key: {asset.object_key}")
        seen.add(asset.object_key)


def validate_assets(
    assets: list[UploadAsset], expected_page_count: int | None = None
) -> None:
    if not assets:
        raise ValueError("Upload allowlist is empty.")
    validate_unique_keys(assets)
    page_numbers: dict[tuple[str, str], list[int]] = {}
    for asset in assets:
        if not asset.local_path.is_file() or asset.local_path.stat().st_size == 0:
            raise ValueError(f"Upload asset is missing or empty: {asset.local_path}")
        try:
            expected_key = asset.local_path.resolve().relative_to(REPOSITORY_ROOT).as_posix()
        except ValueError as error:
            raise ValueError(f"Upload asset is outside the repository: {asset.local_path}") from error
        if asset.object_key != expected_key:
            raise ValueError(
                f"Object key must match the repository-relative local path: "
                f"{asset.object_key} != {expected_key}"
            )
        if asset.object_key.startswith("/") or ".." in Path(asset.object_key).parts:
            raise ValueError(f"Unsafe object key: {asset.object_key}")
        if asset.mime_type == "application/pdf":
            with pymupdf.open(asset.local_path) as document:
                if asset.page_number is not None and document.page_count != 1:
                    raise ValueError(
                        f"Individual page PDF must contain one page: {asset.local_path}"
                    )
        elif asset.mime_type == "image/png":
            preview = pymupdf.Pixmap(asset.local_path)
            if (preview.width, preview.height) != (1224, 1584):
                raise ValueError(
                    f"Preview must be 1224x1584: {asset.local_path} is "
                    f"{preview.width}x{preview.height}"
                )
        if asset.page_number is not None:
            kind = "pdf" if asset.mime_type == "application/pdf" else "png"
            page_numbers.setdefault((asset.resource_id, kind), []).append(asset.page_number)
    for (resource_id, kind), numbers in page_numbers.items():
        expected = list(range(1, max(numbers) + 1))
        if sorted(numbers) != expected:
            raise ValueError(f"Non-sequential {kind} pages for {resource_id}: {sorted(numbers)}")
        if expected_page_count is not None and len(numbers) != expected_page_count:
            raise ValueError(
                f"Expected {expected_page_count} {kind} pages for {resource_id}, "
                f"found {len(numbers)}."
            )


def load_credentials() -> dict[str, str]:
    missing = [name for name in REQUIRED_CREDENTIALS if not os.environ.get(name, "").strip()]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")
    return {
        "account_id": os.environ["R2_ACCOUNT_ID"].strip(),
        "access_key_id": os.environ["R2_ACCESS_KEY_ID"].strip(),
        "secret_access_key": os.environ["R2_SECRET_ACCESS_KEY"].strip(),
    }


def create_r2_client(credentials: dict[str, str]):
    try:
        import boto3
        from botocore.config import Config
    except ImportError as error:
        raise RuntimeError(
            "Publishing dependencies are missing. Install with: "
            "python -m pip install -r worksheet-generator/requirements-publish.txt"
        ) from error
    return boto3.client(
        "s3",
        endpoint_url=(
            f"https://{credentials['account_id']}.r2.cloudflarestorage.com"
        ),
        aws_access_key_id=credentials["access_key_id"],
        aws_secret_access_key=credentials["secret_access_key"],
        region_name="auto",
        config=Config(retries={"max_attempts": 4, "mode": "standard"}),
    )


def _normalized_content_type(value: str | None) -> str:
    return (value or "").split(";", 1)[0].strip().lower()


def _local_md5(path: Path) -> str:
    digest = hashlib.md5(usedforsecurity=False)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _metadata_mismatches(asset: UploadAsset, metadata: dict) -> list[str]:
    mismatches = []
    expected_size = asset.local_path.stat().st_size
    actual_size = metadata.get("ContentLength")
    if actual_size != expected_size:
        mismatches.append(f"size expected={expected_size} actual={actual_size}")
    actual_type = _normalized_content_type(metadata.get("ContentType"))
    if actual_type != asset.mime_type:
        mismatches.append(
            f"MIME type expected={asset.mime_type} actual={actual_type or 'missing'}"
        )
    actual_etag = str(metadata.get("ETag", "")).strip('"').lower()
    expected_etag = _local_md5(asset.local_path)
    if actual_etag != expected_etag:
        mismatches.append(f"ETag expected={expected_etag} actual={actual_etag or 'missing'}")
    return mismatches


def _head_object(client, asset: UploadAsset) -> dict | None:
    try:
        return client.head_object(Bucket=BUCKET_NAME, Key=asset.object_key)
    except Exception as error:
        response = getattr(error, "response", {})
        code = str(response.get("Error", {}).get("Code", ""))
        if code in {"404", "NoSuchKey", "NotFound"}:
            return None
        raise


def _request_with_retry(request: Request, attempts: int = 4):
    for attempt in range(attempts):
        try:
            return urlopen(request, timeout=30)
        except HTTPError as error:
            if error.code < 500 or attempt == attempts - 1:
                raise
        except URLError:
            if attempt == attempts - 1:
                raise
        time.sleep(2**attempt)
    raise AssertionError("HTTP retry loop exited unexpectedly.")


def _verify_nonempty_response(asset: UploadAsset, request: Request) -> tuple[str | None, str]:
    with _request_with_retry(request) as response:
        if response.status != 200:
            raise RuntimeError(f"Expected HTTP 200 for {asset.object_key}, got {response.status}.")
        actual_type = _normalized_content_type(response.headers.get("Content-Type"))
        if actual_type != asset.mime_type:
            raise RuntimeError(
                f"Wrong Content-Type for {asset.object_key}: {actual_type or 'missing'}"
            )
        if not response.read(1):
            raise RuntimeError(f"Production response is empty: {asset.object_key}")
        return response.headers.get("ETag"), response.headers.get(
            "Content-Disposition", ""
        )


def verify_production_asset(asset: UploadAsset) -> None:
    url = f"{PRODUCTION_ASSET_BASE_URL}/{quote(asset.object_key, safe='/')}"
    etag, _ = _verify_nonempty_response(asset, Request(url, method="GET"))
    if not etag:
        raise RuntimeError(f"Production response is missing ETag: {asset.object_key}")
    if asset.mime_type == "application/pdf":
        _, disposition = _verify_nonempty_response(
            asset, Request(f"{url}?download=1", method="GET")
        )
        if "attachment" not in disposition.lower():
            raise RuntimeError(
                f"Download response is missing attachment disposition: {asset.object_key}"
            )
    request = Request(url, headers={"If-None-Match": etag}, method="GET")
    try:
        with _request_with_retry(request) as response:
            if response.status not in (200, 304):
                raise RuntimeError(
                    f"Unexpected cache revalidation status for {asset.object_key}: "
                    f"{response.status}"
                )
    except HTTPError as error:
        if error.code != 304:
            raise


def verify_production_assets(assets: Iterable[UploadAsset]) -> int:
    verified = 0
    for asset in assets:
        verify_production_asset(asset)
        verified += 1
    return verified


def _new_result(asset_count: int) -> dict[str, int]:
    return {
        "planned": asset_count,
        "already_correct": 0,
        "uploaded": 0,
        "failed": 0,
        "production_verified": 0,
    }


def _reconcile_r2_assets(client, assets: list[UploadAsset], upload_missing: bool) -> dict[str, int]:
    result = _new_result(len(assets))
    for asset in assets:
        metadata = _head_object(client, asset)
        if metadata is not None:
            mismatches = _metadata_mismatches(asset, metadata)
            if mismatches:
                result["failed"] += 1
                raise ObjectMismatchError(asset.object_key, mismatches, result)
            result["already_correct"] += 1
            continue
        if not upload_missing:
            result["failed"] += 1
            raise ObjectMismatchError(asset.object_key, ["object is missing"], result)
        with asset.local_path.open("rb") as stream:
            client.put_object(
                Bucket=BUCKET_NAME,
                Key=asset.object_key,
                Body=stream,
                ContentType=asset.mime_type,
            )
        published_metadata = _head_object(client, asset)
        if published_metadata is None:
            result["failed"] += 1
            raise ObjectMismatchError(
                asset.object_key, ["object is missing after upload"], result
            )
        mismatches = _metadata_mismatches(asset, published_metadata)
        if mismatches:
            result["failed"] += 1
            raise ObjectMismatchError(asset.object_key, mismatches, result)
        result["uploaded"] += 1
    return result


def publish_assets(
    assets: list[UploadAsset], apply: bool, verify_only: bool = False
) -> dict[str, int]:
    validate_assets(assets)
    if apply and verify_only:
        raise ValueError("--apply and --verify-only cannot be used together.")
    if not apply and not verify_only:
        for asset in assets:
            print(
                f"DRY-RUN {asset.mime_type} {asset.local_path.relative_to(REPOSITORY_ROOT)} "
                f"-> r2://{BUCKET_NAME}/{asset.object_key}"
            )
        return _new_result(len(assets))

    credentials = load_credentials()
    client = create_r2_client(credentials)
    result = _reconcile_r2_assets(client, assets, upload_missing=apply)

    for asset in assets:
        try:
            verify_production_asset(asset)
        except URLError as error:
            result["failed"] += 1
            raise ProductionVerificationIncomplete(asset.object_key, result) from error
        result["production_verified"] += 1
    return result


def _generate_resource(config_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(Path(__file__).with_name("generate_worksheet.py")), str(config_path)],
        check=True,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)
    resource = subparsers.add_parser("resource", help="Publish one canonical resource.")
    resource.add_argument("config", type=Path)
    resource.add_argument("--generate", action="store_true")
    resource_execution = resource.add_mutually_exclusive_group()
    resource_execution.add_argument("--apply", action="store_true")
    resource_execution.add_argument("--verify-only", action="store_true")
    backfill = subparsers.add_parser("backfill", help="Publish canonical page assets.")
    backfill.add_argument("--page-assets-only", action="store_true")
    backfill_execution = backfill.add_mutually_exclusive_group()
    backfill_execution.add_argument("--apply", action="store_true")
    backfill_execution.add_argument("--verify-only", action="store_true")
    return parser


def main() -> None:
    args = _parser().parse_args()
    if args.mode == "resource":
        config_path = args.config.resolve()
        if args.generate:
            _generate_resource(config_path)
        assets = collect_resource_assets(REPOSITORY_ROOT, config_path)
    else:
        if not args.page_assets_only:
            raise SystemExit("backfill requires --page-assets-only")
        assets = collect_backfill_assets(REPOSITORY_ROOT)
    try:
        result = publish_assets(
            assets, apply=args.apply, verify_only=args.verify_only
        )
    except (ObjectMismatchError, ProductionVerificationIncomplete) as error:
        print(f"ERROR {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(
        f"SUMMARY mode={args.mode} planned={result['planned']} "
        f"already_correct={result['already_correct']} uploaded={result['uploaded']} "
        f"failed={result['failed']} production_verified={result['production_verified']} "
        f"apply={args.apply} verify_only={args.verify_only}"
    )


if __name__ == "__main__":
    main()
