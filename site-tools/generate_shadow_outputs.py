"""Generate isolated Step 2 catalog artifacts."""

from shadow_catalog import SHADOW_ROOT, generate


if __name__ == "__main__":
    metadata = generate()
    print(
        f"SHADOW generated root={SHADOW_ROOT.relative_to(SHADOW_ROOT.parent.parent)} "
        f"resources={metadata['publishedResourceCount']} "
        f"contracts={metadata['publisherContractCount']} sitemap={metadata['sitemapUrlCount']}"
    )
