"""Validate sitemap status, indexability, canonicals, and static inbound links."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlsplit

from catalog_lib import REPOSITORY_ROOT, CatalogValidationError, load_site


class PageSignals(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonicals: list[str] = []
        self.robots: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = {name.lower(): value or "" for name, value in attributes}
        if tag.lower() == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href", ""))
        elif tag.lower() == "meta" and attrs.get("name", "").lower() == "robots":
            self.robots.append(attrs.get("content", ""))
        elif tag.lower() == "a" and "href" in attrs:
            self.links.append(attrs["href"])


def sitemap_urls() -> list[str]:
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.parse(REPOSITORY_ROOT / "sitemap.xml").getroot()
    return [element.text or "" for element in root.findall("s:url/s:loc", namespace)]


def local_page(url: str) -> Path:
    path = urlsplit(url).path
    if path == "/":
        return REPOSITORY_ROOT / "index.html"
    if path.endswith("/"):
        return REPOSITORY_ROOT / path.lstrip("/") / "index.html"
    return REPOSITORY_ROOT / path.lstrip("/")


def page_signals(url: str) -> PageSignals:
    path = local_page(url)
    if not path.is_file():
        raise CatalogValidationError(f"Sitemap URL does not map to a live file: {url}")
    parser = PageSignals()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def validate() -> dict[str, int]:
    site = load_site()
    origin = site["canonicalOrigin"].rstrip("/")
    urls = sitemap_urls()
    if not urls or len(urls) != len(set(urls)):
        raise CatalogValidationError("Sitemap must contain unique URLs")

    inbound: dict[str, set[str]] = {url: set() for url in urls}
    for url in urls:
        if not url.startswith(f"{origin}/") and url != f"{origin}/":
            raise CatalogValidationError(f"Sitemap URL uses the wrong origin: {url}")
        signals = page_signals(url)
        if len(signals.canonicals) != 1:
            raise CatalogValidationError(
                f"Sitemap URL must expose exactly one canonical: {url} count={len(signals.canonicals)}"
            )
        resolved_canonical = urljoin(url, signals.canonicals[0])
        if resolved_canonical != url:
            raise CatalogValidationError(
                f"Sitemap canonical mismatch: url={url} canonical={resolved_canonical}"
            )
        directives = ",".join(signals.robots).lower()
        if "noindex" in directives or "nofollow" in directives:
            raise CatalogValidationError(f"Sitemap URL is not indexable: {url} robots={directives}")
        for href in signals.links:
            if href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue
            target = urldefrag(urljoin(url, href))[0]
            if target in inbound and target != url:
                inbound[target].add(url)

    orphans = [url for url, sources in inbound.items() if not sources]
    if orphans:
        raise CatalogValidationError(f"Sitemap URLs lack static inbound links: {orphans}")
    return {
        "sitemapUrlCount": len(urls),
        "statusOkCount": len(urls),
        "indexableCount": len(urls),
        "canonicalCount": len(urls),
        "inboundLinkedCount": len(urls),
    }


if __name__ == "__main__":
    counts = validate()
    print(
        "SITE INDEXABILITY VALID "
        f"urls={counts['sitemapUrlCount']} "
        f"status_200={counts['statusOkCount']} "
        f"indexable={counts['indexableCount']} "
        f"canonical={counts['canonicalCount']} "
        f"inbound_linked={counts['inboundLinkedCount']}"
    )
