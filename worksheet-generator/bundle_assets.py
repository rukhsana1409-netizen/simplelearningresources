"""Derive individual page PDFs and web previews from a finished bundle PDF."""

from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

import pymupdf


DEFAULT_PREVIEW_DPI = 144


def _inherit_destination_permissions(path: Path) -> None:
    """Reset a published Windows file to its destination directory's inherited ACL."""
    if os.name != "nt":
        return
    subprocess.run(
        ["icacls", str(path), "/reset"],
        check=True,
        capture_output=True,
        text=True,
    )


def _validated_relative_directory(value: object, field_name: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty relative path.")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field_name} must be a repository-relative path without parent traversal.")
    return path


@dataclass(frozen=True)
class BundleAssetContract:
    resource_id: str
    expected_page_count: int
    page_pdf_directory: Path
    preview_directory: Path
    preview_dpi: int = DEFAULT_PREVIEW_DPI

    @classmethod
    def from_dict(cls, values: dict) -> "BundleAssetContract":
        resource_id = values.get("resource_id")
        if not isinstance(resource_id, str) or not resource_id.strip():
            raise ValueError("resource_id must be a nonempty string.")
        expected_page_count = values.get("expected_page_count")
        if not isinstance(expected_page_count, int) or expected_page_count < 1:
            raise ValueError("expected_page_count must be a positive integer.")
        preview_dpi = values.get("preview_dpi", DEFAULT_PREVIEW_DPI)
        if not isinstance(preview_dpi, int) or preview_dpi < 72 or preview_dpi > 300:
            raise ValueError("preview_dpi must be an integer between 72 and 300.")
        return cls(
            resource_id=resource_id,
            expected_page_count=expected_page_count,
            page_pdf_directory=_validated_relative_directory(
                values.get("page_pdf_directory"), "page_pdf_directory"
            ),
            preview_directory=_validated_relative_directory(
                values.get("preview_directory"), "preview_directory"
            ),
            preview_dpi=preview_dpi,
        )

    def page_pdf_path(self, page_number: int) -> Path:
        return self.page_pdf_directory / f"page-{page_number:02d}.pdf"

    def preview_path(self, page_number: int) -> Path:
        return self.preview_directory / f"page-{page_number:02d}.png"


@dataclass(frozen=True)
class GeneratedPageAsset:
    page_number: int
    page_pdf_path: Path
    preview_path: Path
    preview_dimensions: tuple[int, int]


def _validate_generated_assets(
    pdf_paths: list[Path], preview_paths: list[Path]
) -> tuple[int, int]:
    dimensions: set[tuple[int, int]] = set()
    for pdf_path in pdf_paths:
        if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
            raise ValueError(f"Generated page PDF is missing or empty: {pdf_path}")
        with pymupdf.open(pdf_path) as document:
            if document.page_count != 1:
                raise ValueError(f"Generated page PDF must contain exactly one page: {pdf_path}")
    for preview_path in preview_paths:
        if not preview_path.is_file() or preview_path.stat().st_size == 0:
            raise ValueError(f"Generated preview is missing or empty: {preview_path}")
        preview = pymupdf.Pixmap(preview_path)
        if preview.width < 1 or preview.height < 1:
            raise ValueError(f"Generated preview is unreadable: {preview_path}")
        dimensions.add((preview.width, preview.height))
    if len(dimensions) != 1:
        raise ValueError(f"Generated previews must have consistent dimensions: {sorted(dimensions)}")
    return dimensions.pop()


def generate_bundle_assets(
    bundle_pdf_path: Path,
    contract: BundleAssetContract,
    repository_root: Path,
) -> list[GeneratedPageAsset]:
    repository_root = repository_root.resolve()
    bundle_pdf_path = bundle_pdf_path.resolve()
    if not bundle_pdf_path.is_file():
        raise FileNotFoundError(f"Bundle PDF not found: {bundle_pdf_path}")

    with pymupdf.open(bundle_pdf_path) as bundle:
        if bundle.page_count != contract.expected_page_count:
            raise ValueError(
                f"Bundle {contract.resource_id} expected {contract.expected_page_count} pages "
                f"but found {bundle.page_count}."
            )

        with TemporaryDirectory(prefix="bundle-assets-", dir=repository_root) as temporary_name:
            temporary_root = Path(temporary_name)
            temporary_pdf_directory = temporary_root / "pdf"
            temporary_preview_directory = temporary_root / "preview"
            temporary_pdf_directory.mkdir()
            temporary_preview_directory.mkdir()
            temporary_pdf_paths: list[Path] = []
            temporary_preview_paths: list[Path] = []

            for page_index in range(bundle.page_count):
                page_number = page_index + 1
                pdf_path = temporary_pdf_directory / f"page-{page_number:02d}.pdf"
                preview_path = temporary_preview_directory / f"page-{page_number:02d}.png"

                page_document = pymupdf.open()
                page_document.insert_pdf(bundle, from_page=page_index, to_page=page_index)
                page_document.set_metadata(bundle.metadata)
                page_document.save(pdf_path, garbage=4, deflate=True)
                page_document.close()

                pixmap = bundle[page_index].get_pixmap(
                    dpi=contract.preview_dpi,
                    colorspace=pymupdf.csRGB,
                    alpha=False,
                )
                pixmap.save(preview_path)
                temporary_pdf_paths.append(pdf_path)
                temporary_preview_paths.append(preview_path)

            preview_dimensions = _validate_generated_assets(
                temporary_pdf_paths, temporary_preview_paths
            )

            final_pdf_directory = repository_root / contract.page_pdf_directory
            final_preview_directory = repository_root / contract.preview_directory
            final_pdf_directory.mkdir(parents=True, exist_ok=True)
            final_preview_directory.mkdir(parents=True, exist_ok=True)
            generated_assets: list[GeneratedPageAsset] = []

            for page_number, (temporary_pdf, temporary_preview) in enumerate(
                zip(temporary_pdf_paths, temporary_preview_paths), start=1
            ):
                final_pdf = repository_root / contract.page_pdf_path(page_number)
                final_preview = repository_root / contract.preview_path(page_number)
                temporary_pdf.replace(final_pdf)
                temporary_preview.replace(final_preview)
                _inherit_destination_permissions(final_pdf)
                _inherit_destination_permissions(final_preview)
                generated_assets.append(
                    GeneratedPageAsset(
                        page_number=page_number,
                        page_pdf_path=final_pdf,
                        preview_path=final_preview,
                        preview_dimensions=preview_dimensions,
                    )
                )

    return generated_assets
