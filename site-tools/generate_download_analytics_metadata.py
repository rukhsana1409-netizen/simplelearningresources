"""Generate the private dashboard's display metadata from the authoritative catalog."""

from __future__ import annotations

import json
from pathlib import Path

from catalog_lib import REPOSITORY_ROOT, load_resources


OUTPUT = REPOSITORY_ROOT / "cloudflare" / "download-analytics" / "src" / "resource-metadata.mjs"


def build_metadata(resources: list[dict] | None = None) -> dict[str, dict[str, object]]:
    catalog = load_resources() if resources is None else resources
    resources = sorted(
        (resource for resource in catalog if resource["status"] == "published"),
        key=lambda resource: resource["ordering"]["catalog"],
    )
    return {
        resource["id"]: {
            "title": resource["title"],
            "pages": [
                page.get("label", f"Page {page_number}")
                for page_number, page in enumerate(resource["pages"], start=1)
            ],
        }
        for resource in resources
    }


def write_metadata() -> int:
    metadata = build_metadata()
    payload = json.dumps(metadata, ensure_ascii=False, indent=2)
    OUTPUT.write_text(f"// Generated from catalog/resources. Do not edit.\nexport const RESOURCE_METADATA = Object.freeze({payload});\n", encoding="utf-8")
    return len(metadata)


def main() -> None:
    resource_count = write_metadata()
    print(f"DOWNLOAD ANALYTICS METADATA generated resources={resource_count} output={OUTPUT.relative_to(REPOSITORY_ROOT)}")


if __name__ == "__main__":
    main()
