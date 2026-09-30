"""Generate production clean resource pages and their catalog-driven sitemap."""

from __future__ import annotations

import shutil
from html import escape
from pathlib import Path

from catalog_lib import REPOSITORY_ROOT, load_resources, load_site, load_taxonomy, taxonomy_indexes, validate_catalog
from shadow_catalog import absolute_url, published_resources, sitemap_paths, topic_records
from static_resource_pages import SHADOW_ROOT, generate as generate_shadow_pages


PRODUCTION_RESOURCE_ROOT = REPOSITORY_ROOT / "resources"
PRODUCTION_STYLESHEET = REPOSITORY_ROOT / "resource-pages.css"
PRODUCTION_SCRIPT = REPOSITORY_ROOT / "resource-pages.js"
PRODUCTION_SITEMAP = REPOSITORY_ROOT / "sitemap.xml"


def _replace_resource_root(source_root: Path, destination_root: Path) -> None:
    resolved = destination_root.resolve()
    expected = (REPOSITORY_ROOT / "resources").resolve()
    if resolved != expected:
        raise ValueError(f"Unsafe production resource output path: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    shutil.copytree(source_root, resolved)


def _write_sitemap() -> int:
    site, taxonomy, resources = load_site(), load_taxonomy(), load_resources()
    validate_catalog(site, taxonomy, resources)
    published = published_resources(resources)
    indexes = taxonomy_indexes(taxonomy)
    topics = topic_records(published, taxonomy, indexes, site)
    paths = sitemap_paths(published, topics, taxonomy, site)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        *[f"  <url><loc>{escape(absolute_url(site, path))}</loc></url>" for path in paths],
        "</urlset>",
    ]
    PRODUCTION_SITEMAP.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return len(paths)


def generate() -> dict:
    manifest = generate_shadow_pages(SHADOW_ROOT)
    _replace_resource_root(SHADOW_ROOT / "resources", PRODUCTION_RESOURCE_ROOT)
    PRODUCTION_STYLESHEET.write_bytes((SHADOW_ROOT / "resource-pages.css").read_bytes())
    PRODUCTION_SCRIPT.write_bytes((SHADOW_ROOT / "resource-pages.js").read_bytes())
    sitemap_count = _write_sitemap()
    return {
        "resourcePageCount": manifest["publishedResourceCount"],
        "retiredExcludedCount": manifest["retiredResourceCount"],
        "sitemapUrlCount": sitemap_count,
    }


if __name__ == "__main__":
    result = generate()
    print(
        "PRODUCTION RESOURCE PAGES generated "
        f"pages={result['resourcePageCount']} "
        f"retired_excluded={result['retiredExcludedCount']} "
        f"sitemap={result['sitemapUrlCount']}"
    )
