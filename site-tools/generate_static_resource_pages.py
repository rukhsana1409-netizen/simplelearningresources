"""Generate Discoverability Phase 2 static resource pages in shadow mode."""

from static_resource_pages import SHADOW_ROOT, generate


if __name__ == "__main__":
    manifest = generate()
    print(
        "STATIC SHADOW generated "
        f"root={SHADOW_ROOT.relative_to(SHADOW_ROOT.parent.parent)} "
        f"pages={manifest['publishedResourceCount']} "
        f"retired_excluded={manifest['retiredResourceCount']} "
        f"pattern={manifest['cleanUrlPattern']}"
    )
