"""Generate production clean resource pages and their catalog-driven sitemap."""

from __future__ import annotations

import shutil
from html import escape
from pathlib import Path

from catalog_lib import REPOSITORY_ROOT, load_resources, load_site, load_taxonomy, taxonomy_indexes, validate_catalog
from shadow_catalog import absolute_url, published_resources, sitemap_paths, topic_records
from resource_discoverability import resource_page_href
from static_resource_pages import SHADOW_ROOT, generate as generate_shadow_pages


PRODUCTION_RESOURCE_ROOT = REPOSITORY_ROOT / "resources"
PRODUCTION_STYLESHEET = REPOSITORY_ROOT / "resource-pages.css"
PRODUCTION_SCRIPT = REPOSITORY_ROOT / "resource-pages.js"
PRODUCTION_SITEMAP = REPOSITORY_ROOT / "sitemap.xml"
CRAWLABLE_INDEX_PAGE = REPOSITORY_ROOT / "worksheets.html"
CRAWLABLE_INDEX_START = "<!-- BEGIN GENERATED CRAWLABLE SITE INDEX -->"
CRAWLABLE_INDEX_END = "<!-- END GENERATED CRAWLABLE SITE INDEX -->"


def _replace_resource_root(source_root: Path, destination_root: Path) -> None:
    resolved = destination_root.resolve()
    expected = (REPOSITORY_ROOT / "resources").resolve()
    if resolved != expected:
        raise ValueError(f"Unsafe production resource output path: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)
    shutil.copytree(source_root, resolved)


def _sitemap_paths() -> list[str]:
    site, taxonomy, resources = load_site(), load_taxonomy(), load_resources()
    validate_catalog(site, taxonomy, resources)
    published = published_resources(resources)
    indexes = taxonomy_indexes(taxonomy)
    topics = topic_records(published, taxonomy, indexes, site)
    return sitemap_paths(published, topics, taxonomy, site)


def _write_sitemap(paths: list[str]) -> int:
    site = load_site()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        *[f"  <url><loc>{escape(absolute_url(site, path))}</loc></url>" for path in paths],
        "</urlset>",
    ]
    PRODUCTION_SITEMAP.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return len(paths)


def _root_href(path: str) -> str:
    return f"/{path}" if path else "/"


def _visible_resource_directory() -> tuple[list[str], int]:
    site, taxonomy, resources = load_site(), load_taxonomy(), load_resources()
    published = published_resources(resources)
    indexes = taxonomy_indexes(taxonomy)
    topics = topic_records(published, taxonomy, indexes, site)
    topics_by_key = {
        (topic["grade"], topic["subject"], topic["topic"]): topic
        for topic in topics
    }
    directory = site["compatibility"]["directory"]
    lines = [
        '<section class="catalog-resource-index" aria-labelledby="catalog-resource-index-title">',
        '    <div class="catalog-resource-index-header">',
        '        <p class="eyebrow">RESOURCE DIRECTORY</p>',
        '        <h2 id="catalog-resource-index-title">Browse worksheets by topic</h2>',
        '        <p>Choose a grade, subject, and topic to find every published worksheet.</p>',
        '    </div>',
        '    <div class="catalog-resource-grades">',
    ]
    link_count = 0
    for grade in sorted(taxonomy["grades"], key=lambda item: item["order"]):
        grade_resources = [resource for resource in published if resource["taxonomy"]["grade"] == grade["id"]]
        if not grade_resources:
            continue
        lines.extend((
            '        <section class="catalog-resource-grade">',
            f'            <h3><a href="/{escape(directory["gradePaths"][grade["id"]], quote=True)}">{escape(grade["label"])}</a></h3>',
            '            <div class="catalog-resource-subjects">',
        ))
        for subject in sorted(taxonomy["subjects"], key=lambda item: item["order"]):
            subject_resources = [
                resource for resource in grade_resources
                if resource["taxonomy"]["subject"] == subject["id"]
            ]
            if not subject_resources:
                continue
            lines.extend((
                '                <section class="catalog-resource-subject">',
                f'                    <h4><a href="/{escape(directory["subjectPaths"][subject["id"]], quote=True)}">{escape(subject["label"])}</a></h4>',
            ))
            for topic in sorted(taxonomy["topics"], key=lambda item: item["order"]):
                if topic["grade"] != grade["id"] or topic["subject"] != subject["id"]:
                    continue
                topic_resources = [
                    resource for resource in subject_resources
                    if resource["taxonomy"]["topic"] == topic["id"]
                ]
                if not topic_resources:
                    continue
                record = topics_by_key[(grade["label"], subject["label"], topic["label"])]
                lines.extend((
                    '                    <div class="catalog-resource-topic">',
                    f'                        <h5><a href="/{escape(record["listingHref"], quote=True)}">{escape(topic["label"])}</a></h5>',
                    '                        <ul>',
                ))
                for resource in sorted(topic_resources, key=lambda item: item["ordering"]["catalog"]):
                    lines.append(
                        f'                            <li><a href="/{escape(resource_page_href(resource), quote=True)}">{escape(resource["title"])}</a></li>'
                    )
                    link_count += 1
                lines.extend(('                        </ul>', '                    </div>'))
            lines.extend(('                </section>',))
        lines.extend(('            </div>', '        </section>'))
    lines.extend(('    </div>', '</section>'))
    return lines, link_count


def _write_crawlable_site_index(paths: list[str]) -> tuple[int, int]:
    source = CRAWLABLE_INDEX_PAGE.read_text(encoding="utf-8")
    if source.count(CRAWLABLE_INDEX_START) != 1 or source.count(CRAWLABLE_INDEX_END) != 1:
        raise ValueError("worksheets.html must contain one generated crawlable-index block")
    links = []
    for path in paths:
        href = _root_href(path)
        label = path or "Home"
        links.append(f'            <li><a href="{escape(href, quote=True)}">{escape(label)}</a></li>')
    visible_directory, visible_resource_link_count = _visible_resource_directory()
    block = "\n".join([
        CRAWLABLE_INDEX_START,
        "<!-- Generated by site-tools/generate_production_resource_pages.py. Do not edit this block by hand. -->",
        *visible_directory,
        "<noscript>",
        '    <nav aria-label="Complete site index">',
        "        <h2>Complete site index</h2>",
        "        <ul>",
        *links,
        "        </ul>",
        "    </nav>",
        "</noscript>",
        CRAWLABLE_INDEX_END,
    ])
    before, remainder = source.split(CRAWLABLE_INDEX_START, 1)
    _, after = remainder.split(CRAWLABLE_INDEX_END, 1)
    CRAWLABLE_INDEX_PAGE.write_text(before + block + after, encoding="utf-8", newline="\n")
    return len(links), visible_resource_link_count


def generate() -> dict:
    manifest = generate_shadow_pages(SHADOW_ROOT)
    _replace_resource_root(SHADOW_ROOT / "resources", PRODUCTION_RESOURCE_ROOT)
    PRODUCTION_STYLESHEET.write_bytes((SHADOW_ROOT / "resource-pages.css").read_bytes())
    PRODUCTION_SCRIPT.write_bytes((SHADOW_ROOT / "resource-pages.js").read_bytes())
    paths = _sitemap_paths()
    sitemap_count = _write_sitemap(paths)
    crawlable_link_count, visible_resource_link_count = _write_crawlable_site_index(paths)
    return {
        "resourcePageCount": manifest["publishedResourceCount"],
        "retiredExcludedCount": manifest["retiredResourceCount"],
        "sitemapUrlCount": sitemap_count,
        "crawlableLinkCount": crawlable_link_count,
        "visibleResourceLinkCount": visible_resource_link_count,
    }


if __name__ == "__main__":
    result = generate()
    print(
        "PRODUCTION RESOURCE PAGES generated "
        f"pages={result['resourcePageCount']} "
        f"retired_excluded={result['retiredExcludedCount']} "
        f"sitemap={result['sitemapUrlCount']} "
        f"crawlable_links={result['crawlableLinkCount']} "
        f"visible_resource_links={result['visibleResourceLinkCount']}"
    )
