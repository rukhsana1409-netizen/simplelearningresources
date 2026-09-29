"""Compare generated production registry data with the committed pre-Step-3 runtime."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from catalog_lib import REPOSITORY_ROOT, CatalogValidationError, extract_live_registry
from generate_production_runtime import END_MARKER, START_MARKER


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


def split_previous(source: str) -> tuple[str, str]:
    start = source.index("const worksheetResourceDefinitions = [")
    end = source.index("const preschoolMathTopicSeoMetadata=", start)
    return source[:start], source[end:]


def split_generated(source: str) -> tuple[str, str]:
    start = source.index(START_MARKER)
    end = source.index(END_MARKER, start) + len(END_MARKER)
    while end < len(source) and source[end] in "\r\n":
        end += 1
    return source[:start], source[end:]


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
    previous_prefix, previous_suffix = split_previous(previous_source)
    current_prefix, current_suffix = split_generated(current_source)
    if previous_prefix != current_prefix:
        raise CatalogValidationError("directory.js changed before the generated resource block")
    if previous_suffix != current_suffix:
        raise CatalogValidationError("directory.js behavior changed after the generated resource block")
    required_api = (
        "window.worksheetResources=worksheetResources;",
        "window.worksheetResourcesById=worksheetResourcesById;",
        "window.searchWorksheetResources=searchWorksheetResources;",
        "window.resolveWorksheetAssetUrl=resolveWorksheetAssetUrl;",
    )
    missing = [statement for statement in required_api if statement not in current_suffix]
    if missing:
        raise CatalogValidationError(f"Synchronous runtime API is missing: {missing}")
    print(
        f"PRODUCTION RUNTIME PARITY exact baseline={args.baseline_ref} "
        f"resources={len(current)} behavior_suffix=unchanged api=4"
    )


if __name__ == "__main__":
    main()
