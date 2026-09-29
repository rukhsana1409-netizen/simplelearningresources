"""Compare generated production registry data with the committed pre-Step-3 runtime."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from catalog_lib import REPOSITORY_ROOT, CatalogValidationError, extract_live_registry


def git_file(reference: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{reference}:{path}"], cwd=REPOSITORY_ROOT,
        check=True, capture_output=True, text=True, encoding="utf-8",
    )
    return result.stdout


def registry_from_source(source: str) -> list[dict]:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", encoding="utf-8", delete=False) as handle:
        handle.write(source)
        path = Path(handle.name)
    try:
        return extract_live_registry(path)
    finally:
        path.unlink()


def runtime_core(source: str) -> str:
    start = source.index("const requiredWorksheetResourceFields=")
    end = source.index("const renderDirectory = () => {", start)
    return source[start:end]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-ref", default="HEAD")
    args = parser.parse_args()
    previous_source = git_file(args.baseline_ref, "directory.js")
    current_source = (REPOSITORY_ROOT / "directory.js").read_text(encoding="utf-8")
    previous = registry_from_source(previous_source)
    current = registry_from_source(current_source)
    if previous != current:
        raise CatalogValidationError("Generated production registry differs from the pre-Step-3 registry")
    if runtime_core(previous_source) != runtime_core(current_source):
        raise CatalogValidationError("Synchronous resource/search runtime behavior changed")
    required_api = (
        "window.worksheetResources=worksheetResources;",
        "window.worksheetResourcesById=worksheetResourcesById;",
        "window.searchWorksheetResources=searchWorksheetResources;",
        "window.resolveWorksheetAssetUrl=resolveWorksheetAssetUrl;",
    )
    missing = [statement for statement in required_api if statement not in current_source]
    if missing:
        raise CatalogValidationError(f"Synchronous runtime API is missing: {missing}")
    print(
        f"PRODUCTION RUNTIME PARITY exact baseline={args.baseline_ref} "
        f"resources={len(current)} runtime_core=unchanged api=4"
    )


if __name__ == "__main__":
    main()
