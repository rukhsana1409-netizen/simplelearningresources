"""Validate the modular Learning Made Simple resource catalog."""

from catalog_lib import load_resources, load_site, load_taxonomy, validate_catalog


def main() -> None:
    resources = load_resources()
    counts = validate_catalog(load_site(), load_taxonomy(), resources)
    print(
        "VALID catalog "
        f"total={len(resources)} published={counts.get('published', 0)} "
        f"draft={counts.get('draft', 0)} review={counts.get('review', 0)} "
        f"retired={counts.get('retired', 0)}"
    )


if __name__ == "__main__":
    main()
