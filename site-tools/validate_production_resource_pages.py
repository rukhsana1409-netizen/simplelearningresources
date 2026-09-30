"""Validate production clean resource pages against the Phase 2 shadow output."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

from catalog_lib import REPOSITORY_ROOT, CatalogValidationError, load_resources, load_site
from resource_discoverability import resource_page_href
from static_resource_pages import SHADOW_ROOT, validate_output


def validate() -> dict[str, int]:
    shadow_counts = validate_output(SHADOW_ROOT)
    resources = load_resources()
    published = [resource for resource in resources if resource["status"] == "published"]
    retired = [resource for resource in resources if resource["status"] == "retired"]
    production_root = REPOSITORY_ROOT / "resources"
    pages = sorted(production_root.glob("*/index.html"))
    if len(pages) != len(published):
        raise CatalogValidationError(
            f"Production resource page count differs: pages={len(pages)} published={len(published)}"
        )
    for resource in published:
        relative = Path(resource_page_href(resource)) / "index.html"
        production_page = REPOSITORY_ROOT / relative
        shadow_page = SHADOW_ROOT / relative
        if not production_page.is_file() or production_page.read_bytes() != shadow_page.read_bytes():
            raise CatalogValidationError(f"Production resource page differs from shadow: {resource['id']}")
        source = production_page.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', source):
            if href.startswith(("#", "https://assets.simplelearningresources.com/")):
                continue
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            clean_path = parsed.path.lstrip("/")
            if not clean_path:
                target = REPOSITORY_ROOT / "index.html"
            elif clean_path.endswith("/"):
                target = REPOSITORY_ROOT / clean_path / "index.html"
            elif parsed.path.startswith("/"):
                target = REPOSITORY_ROOT / clean_path
            else:
                target = production_page.parent / parsed.path
            if not target.exists():
                raise CatalogValidationError(
                    f"{resource['id']}: internal link target does not exist: {href}"
                )
    for resource in retired:
        if (production_root / resource["routing"]["slug"]).exists():
            raise CatalogValidationError(f"Retired resource has a production page: {resource['id']}")
    for filename in ("resource-pages.css", "resource-pages.js"):
        if (REPOSITORY_ROOT / filename).read_bytes() != (SHADOW_ROOT / filename).read_bytes():
            raise CatalogValidationError(f"Production supporting file differs from shadow: {filename}")

    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_root = ET.parse(REPOSITORY_ROOT / "sitemap.xml").getroot()
    locations = [element.text for element in sitemap_root.findall("s:url/s:loc", namespace)]
    site = load_site()
    expected_resource_urls = {
        f"{site['canonicalOrigin']}/{resource_page_href(resource)}" for resource in published
    }
    actual_resource_urls = {url for url in locations if "/resources/" in url}
    if actual_resource_urls != expected_resource_urls:
        raise CatalogValidationError("Production sitemap clean resource URLs differ from catalog")
    if any("resource-preview.html?resource=" in url for url in locations):
        raise CatalogValidationError("Production sitemap still contains legacy resource preview URLs")
    return {
        "validatedPageCount": len(pages),
        "retiredExcludedCount": len(retired),
        "sitemapUrlCount": len(locations),
        "shadowValidatedPageCount": shadow_counts["validatedPageCount"],
    }


if __name__ == "__main__":
    counts = validate()
    print(
        "PRODUCTION RESOURCE PAGES VALID "
        f"pages={counts['validatedPageCount']} "
        f"retired_excluded={counts['retiredExcludedCount']} "
        f"sitemap={counts['sitemapUrlCount']}"
    )
