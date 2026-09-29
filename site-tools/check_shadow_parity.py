"""Verify Step 2 shadow artifacts against unchanged production inputs."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from catalog_lib import REPOSITORY_ROOT, CatalogValidationError, extract_live_registry, load_resources, load_site, load_taxonomy, taxonomy_indexes, validate_catalog
from shadow_catalog import SHADOW_ROOT, absolute_url, catalog_digest, generate, published_resources, topic_query


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def production_runtime(resource: dict, site: dict) -> dict:
    pages = []
    for number in range(1, resource["pageCount"] + 1):
        preview_path = f"{resource['previewDirectory']}/page-{number:02d}.png"
        pdf_path = f"{resource['pagePdfDirectory']}/page-{number:02d}.pdf"
        pages.append({
            "number": number, "previewPath": preview_path, "pdfPath": pdf_path,
            "previewUrl": f"{site['assetOrigin']}/{preview_path}",
            "pdfUrl": f"{site['assetOrigin']}/{pdf_path}",
        })
    return {
        "id": resource["id"], "title": resource["title"], "description": resource["description"],
        "grade": resource["grade"], "subject": resource["subject"], "topic": resource["topic"],
        "skill": resource["skill"], "keywords": resource["keywords"], "pdfPath": resource["bundlePdf"],
        "thumbnailPath": resource["thumbnailPath"], "pageCount": resource["pageCount"],
        "pageLabels": resource["pageLabels"], "pages": pages, "backHref": resource["backHref"],
        "backLabel": resource["backLabel"], "seoTitle": resource["seo"]["title"],
        "seoDescription": resource["seo"]["description"],
        "pdfUrl": f"{site['assetOrigin']}/{resource['bundlePdf']}",
        "thumbnailUrl": f"{site['assetOrigin']}/{resource['thumbnailPath']}",
        "previewHref": resource["previewHref"],
        "canonicalUrl": absolute_url(site, resource["previewHref"]),
        "meta": f"{resource['grade']} • {resource['subject']} • {resource['topic']} • {resource['skill']}".upper(),
    }


def xml_locations(path: Path) -> list[str]:
    root = ET.parse(path).getroot()
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [element.text for element in root.findall("s:url/s:loc", namespace)]


def contract_assets(contract: dict) -> list[str]:
    output = contract["asset_output"]
    page_directory = output["page_pdf_directory"]
    preview_directory = output["preview_directory"]
    paths = [f"{page_directory}.pdf"]
    for number in range(1, output["expected_page_count"] + 1):
        paths.extend((f"{page_directory}/page-{number:02d}.pdf", f"{preview_directory}/page-{number:02d}.png"))
    return paths


def main() -> None:
    generate()
    site, taxonomy, catalog_resources = load_site(), load_taxonomy(), load_resources()
    validate_catalog(site, taxonomy, catalog_resources)
    published = published_resources(catalog_resources)
    live = extract_live_registry(REPOSITORY_ROOT / "directory.js")
    shadow_runtime = load_json(SHADOW_ROOT / "runtime" / "registry.json")["resources"]
    expected_runtime = [production_runtime(resource, site) for resource in live]
    if shadow_runtime != expected_runtime:
        differences = []
        for expected, actual in zip(expected_runtime, shadow_runtime):
            for field in expected:
                if expected[field] != actual.get(field):
                    differences.append(f"{expected['id']}.{field}: production={expected[field]!r} shadow={actual.get(field)!r}")
        raise CatalogValidationError("Runtime shadow parity failed:\n" + "\n".join(differences))

    directory_source = (REPOSITORY_ROOT / "directory.js").read_text(encoding="utf-8")
    required_fragments = (
        'resources.length===1?resources[0].previewHref:topicRoute(grade,subject,topic)',
        'topic==="Numbers & Counting"?"numbers-counting.html"',
        'topic==="Early Addition & Subtraction"?"skill-directory.html?skill=addition"',
    )
    missing_fragments = [fragment for fragment in required_fragments if fragment not in directory_source]
    if missing_fragments:
        raise CatalogValidationError(f"Production topic routing changed: missing {missing_fragments}")
    by_topic = defaultdict(list)
    for resource in live:
        by_topic[(resource["grade"], resource["subject"], resource["topic"])].append(resource)
    shadow_topics = load_json(SHADOW_ROOT / "runtime" / "topics.json")["topics"]
    overrides = site["compatibility"]["topicRouteOverrides"]
    indexes = taxonomy_indexes(taxonomy)
    topic_by_labels = {}
    for topic in taxonomy["topics"]:
        grade_label = indexes["grades"][topic["grade"]]["label"]
        subject_label = indexes["subjects"][topic["subject"]]["label"]
        topic_by_labels[(grade_label, subject_label, topic["label"])] = topic
    for shadow_topic in shadow_topics:
        key = (shadow_topic["grade"], shadow_topic["subject"], shadow_topic["topic"])
        members = by_topic[key]
        taxonomy_topic = topic_by_labels[key]
        route_key = f"{taxonomy_topic['grade']}/{taxonomy_topic['subject']}/{taxonomy_topic['id']}"
        canonical_href = topic_query(*key)
        listing_href = overrides.get(route_key, canonical_href)
        expected_link = members[0]["previewHref"] if len(members) == 1 else (listing_href if members else None)
        expected = {
            "resourceIds": [member["id"] for member in members], "resourceCount": len(members),
            "listingHref": listing_href, "linkHref": expected_link,
            "canonicalHref": canonical_href, "canonicalUrl": absolute_url(site, canonical_href),
            "isSingletonDirect": len(members) == 1,
        }
        for field, value in expected.items():
            if shadow_topic[field] != value:
                raise CatalogValidationError(f"Topic parity failed for {key}.{field}: {shadow_topic[field]!r} != {value!r}")

    publisher_fields = ("filename", "asset_output")
    publisher_differences = []
    for resource in published:
        shadow_contract = load_json(SHADOW_ROOT / "publisher" / "contracts" / f"{resource['id']}.json")
        production_contract = load_json(REPOSITORY_ROOT / resource["source"]["publisherContract"])
        for field in publisher_fields:
            if shadow_contract[field] != production_contract.get(field):
                publisher_differences.append(
                    f"{resource['id']}.{field}: production={production_contract.get(field)!r} "
                    f"shadow={shadow_contract[field]!r}"
                )
        if contract_assets(shadow_contract) != contract_assets(production_contract):
            publisher_differences.append(f"{resource['id']}: publisher asset behavior differs")
    if publisher_differences:
        raise CatalogValidationError(
            "Publisher parity failed:\n" + "\n".join(publisher_differences)
        )

    production_sitemap = xml_locations(REPOSITORY_ROOT / "sitemap.xml")
    shadow_sitemap = xml_locations(SHADOW_ROOT / "sitemap.xml")
    if shadow_sitemap != production_sitemap:
        missing = [url for url in production_sitemap if url not in shadow_sitemap]
        extra = [url for url in shadow_sitemap if url not in production_sitemap]
        raise CatalogValidationError(
            f"Sitemap parity failed: missing={missing} extra={extra} order_equal={set(shadow_sitemap) == set(production_sitemap)}"
        )

    metadata = load_json(SHADOW_ROOT / "catalog-version.json")
    if metadata["catalogSha256"] != catalog_digest() or metadata["urlSemantics"] != "legacy-query":
        raise CatalogValidationError("Catalog/version metadata is stale or has changed URL semantics")
    print(
        "SHADOW PARITY exact "
        f"resources={len(shadow_runtime)} fields={len(shadow_runtime[0])} "
        f"topics={len(shadow_topics)} singletons={sum(topic['isSingletonDirect'] for topic in shadow_topics)} "
        f"contracts={len(published)} sitemap={len(shadow_sitemap)} url_semantics=legacy-query"
    )


if __name__ == "__main__":
    main()
