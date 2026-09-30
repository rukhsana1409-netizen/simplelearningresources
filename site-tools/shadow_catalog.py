"""Generate deterministic Step 2 artifacts without touching production outputs."""

from __future__ import annotations

import hashlib
import json
import shutil
from collections import defaultdict
from html import escape
from pathlib import Path
from urllib.parse import quote

from catalog_lib import CATALOG_ROOT, REPOSITORY_ROOT, load_resources, load_site, load_taxonomy, taxonomy_indexes, validate_catalog
from resource_discoverability import resource_page_href


SHADOW_ROOT = REPOSITORY_ROOT / "tmp" / "catalog-shadow"


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def absolute_url(site: dict, relative: str) -> str:
    return f"{site['canonicalOrigin'].rstrip('/')}/{relative}" if relative else f"{site['canonicalOrigin'].rstrip('/')}/"


def topic_query(grade_label: str, subject_label: str, topic_label: str) -> str:
    return "topic.html?grade={}&subject={}&topic={}".format(
        quote(grade_label, safe=""), quote(subject_label, safe=""), quote(topic_label, safe="")
    )


def published_resources(resources: list[dict]) -> list[dict]:
    return sorted(
        (resource for resource in resources if resource["status"] == "published"),
        key=lambda resource: resource["ordering"]["catalog"],
    )


def runtime_resource(resource: dict, indexes: dict, site: dict) -> dict:
    classification = resource["taxonomy"]
    grade = indexes["grades"][classification["grade"]]["label"]
    subject = indexes["subjects"][classification["subject"]]["label"]
    topic = indexes["topics"][(classification["grade"], classification["subject"], classification["topic"])]["label"]
    skill = indexes["skills"][(classification["grade"], classification["subject"], classification["topic"], classification["skills"][0])]["label"]
    assets = resource["assets"]
    labels = [page.get("label") for page in resource["pages"]]
    page_labels = labels if any(labels) else None
    pages = []
    for number in range(1, len(resource["pages"]) + 1):
        preview_path = f"{assets['previewDirectory']}/page-{number:02d}.png"
        pdf_path = f"{assets['pagePdfDirectory']}/page-{number:02d}.pdf"
        pages.append({
            "number": number,
            "previewPath": preview_path,
            "pdfPath": pdf_path,
            "previewUrl": f"{site['assetOrigin']}/{preview_path}",
            "pdfUrl": f"{site['assetOrigin']}/{pdf_path}",
        })
    preview_href = resource_page_href(resource)
    return {
        "id": resource["id"], "title": resource["title"], "description": resource["description"],
        "grade": grade, "subject": subject, "topic": topic, "skill": skill,
        "keywords": resource["keywords"], "pdfPath": assets["bundlePdf"],
        "thumbnailPath": f"{assets['previewDirectory']}/page-01.png", "pageCount": len(pages),
        "pageLabels": page_labels, "pages": pages, "backHref": resource["legacy"]["backHref"],
        "backLabel": resource["legacy"]["backLabel"], "seoTitle": resource["seo"]["title"],
        "seoDescription": resource["seo"]["description"],
        "pdfUrl": f"{site['assetOrigin']}/{assets['bundlePdf']}",
        "thumbnailUrl": f"{site['assetOrigin']}/{assets['previewDirectory']}/page-01.png",
        "previewHref": preview_href, "canonicalUrl": absolute_url(site, preview_href),
        "meta": f"{grade} • {subject} • {topic} • {skill}".upper(),
    }


def topic_records(resources: list[dict], taxonomy: dict, indexes: dict, site: dict) -> list[dict]:
    by_topic = defaultdict(list)
    for resource in resources:
        key = (resource["taxonomy"]["grade"], resource["taxonomy"]["subject"], resource["taxonomy"]["topic"])
        by_topic[key].append(resource)
    overrides = site["compatibility"]["topicRouteOverrides"]
    records = []
    for topic in taxonomy["topics"]:
        key = (topic["grade"], topic["subject"], topic["id"])
        members = sorted(by_topic[key], key=lambda item: item["ordering"]["catalog"])
        grade_label = indexes["grades"][topic["grade"]]["label"]
        subject_label = indexes["subjects"][topic["subject"]]["label"]
        canonical_href = topic_query(grade_label, subject_label, topic["label"])
        route_key = "/".join(key)
        listing_href = overrides.get(route_key, canonical_href)
        link_href = resource_page_href(members[0]) if len(members) == 1 else listing_href
        records.append({
            "grade": grade_label, "subject": subject_label, "topic": topic["label"],
            "resourceIds": [member["id"] for member in members], "resourceCount": len(members),
            "listingHref": listing_href, "linkHref": link_href if members else None,
            "canonicalHref": canonical_href, "canonicalUrl": absolute_url(site, canonical_href),
            "isSingletonDirect": len(members) == 1,
        })
    return records


def publisher_contract(resource: dict) -> dict:
    assets = resource["assets"]
    return {
        "filename": assets["bundlePdf"].rsplit("/", 1)[-1],
        "asset_output": {
            "resource_id": resource["id"],
            "expected_page_count": len(resource["pages"]),
            "page_pdf_directory": assets["pagePdfDirectory"],
            "preview_directory": assets["previewDirectory"],
            "preview_dpi": assets["preview"]["dpi"],
        },
    }


def sitemap_paths(resources: list[dict], topics: list[dict], taxonomy: dict, site: dict) -> list[str]:
    config = site["compatibility"]["sitemap"]
    paths = list(config["staticPaths"])
    overrides = set(site["compatibility"]["topicRouteOverrides"])
    subject_rank = {subject: rank for rank, subject in enumerate(config["subjectOrder"])}
    grade_ids = {item["label"]: item["id"] for item in taxonomy["grades"]}
    subject_ids = {item["label"]: item["id"] for item in taxonomy["subjects"]}
    topic_orders = {
        (item["grade"], item["subject"], item["label"]): item["order"]
        for item in taxonomy["topics"]
    }
    topic_ids = {
        (item["grade"], item["subject"], item["label"]): item["id"]
        for item in taxonomy["topics"]
    }
    populated = [topic for topic in topics if topic["resourceCount"]]
    populated.sort(key=lambda topic: (
        subject_rank.get(subject_ids[topic["subject"]], 999),
        topic_orders[(grade_ids[topic["grade"]], subject_ids[topic["subject"]], topic["topic"])],
    ))
    for topic in populated:
        grade_id = grade_ids[topic["grade"]]
        subject_id = subject_ids[topic["subject"]]
        topic_id = topic_ids[(grade_id, subject_id, topic["topic"])]
        if f"{grade_id}/{subject_id}/{topic_id}" not in overrides:
            paths.append(topic["canonicalHref"])
    paths.extend(config["skillPaths"])
    resources_by_subject = sorted(resources, key=lambda resource: (
        subject_rank.get(resource["taxonomy"]["subject"], 999), resource["ordering"]["catalog"]
    ))
    paths.extend(resource_page_href(resource) for resource in resources_by_subject)
    return paths


def catalog_digest() -> str:
    digest = hashlib.sha256()
    paths = [CATALOG_ROOT / "site.json", CATALOG_ROOT / "schema" / "resource.schema.json"]
    paths.extend(sorted((CATALOG_ROOT / "taxonomy").glob("*.json")))
    paths.extend(sorted((CATALOG_ROOT / "resources").rglob("*.json")))
    for path in paths:
        digest.update(path.relative_to(REPOSITORY_ROOT).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def generate(shadow_root: Path = SHADOW_ROOT) -> dict:
    resolved_root = shadow_root.resolve()
    expected_parent = (REPOSITORY_ROOT / "tmp").resolve()
    if resolved_root.parent != expected_parent or resolved_root.name != "catalog-shadow":
        raise ValueError(f"Unsafe shadow output path: {resolved_root}")
    if resolved_root.exists():
        shutil.rmtree(resolved_root)
    site, taxonomy, resources = load_site(), load_taxonomy(), load_resources()
    counts = validate_catalog(site, taxonomy, resources)
    indexes = taxonomy_indexes(taxonomy)
    published = published_resources(resources)
    runtime = [runtime_resource(resource, indexes, site) for resource in published]
    topics = topic_records(published, taxonomy, indexes, site)
    write_json(resolved_root / "runtime" / "registry.json", {"schemaVersion": 1, "resources": runtime})
    write_json(resolved_root / "runtime" / "topics.json", {"schemaVersion": 1, "topics": topics})
    write_json(resolved_root / "runtime" / "taxonomy.json", {"schemaVersion": 1, **taxonomy})
    for resource in published:
        write_json(resolved_root / "publisher" / "contracts" / f"{resource['id']}.json", publisher_contract(resource))
    paths = sitemap_paths(published, topics, taxonomy, site)
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.extend(f"  <url><loc>{escape(absolute_url(site, path))}</loc></url>" for path in paths)
    xml.append("</urlset>")
    (resolved_root / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")
    metadata = {
        "schemaVersion": 1, "generatorVersion": 1, "catalogSha256": catalog_digest(),
        "publishedResourceCount": len(published), "retiredResourceCount": counts.get("retired", 0),
        "publisherContractCount": len(published), "sitemapUrlCount": len(paths),
        "urlSemantics": "clean-path", "resourcePath": "resources/{slug}/",
    }
    write_json(resolved_root / "catalog-version.json", metadata)
    output_paths = sorted(
        path.relative_to(resolved_root).as_posix()
        for path in resolved_root.rglob("*")
        if path.is_file()
    )
    output_paths = sorted([*output_paths, "manifest.json"])
    write_json(resolved_root / "manifest.json", {
        "schemaVersion": 1,
        "outputs": output_paths,
    })
    return metadata
