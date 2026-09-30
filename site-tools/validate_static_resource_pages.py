"""Validate Discoverability Phase 2 shadow static resource pages."""

from static_resource_pages import validate_output


if __name__ == "__main__":
    counts = validate_output()
    print(
        "STATIC SHADOW VALID "
        f"pages={counts['validatedPageCount']} "
        f"published={counts['publishedResourceCount']} "
        f"retired_excluded={counts['retiredResourceCount']}"
    )
