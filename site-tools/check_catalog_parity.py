"""Require exact parity between the new catalog and the current production registry."""

from __future__ import annotations

from collections import Counter

from catalog_lib import (
    CATALOG_ROOT,
    REPOSITORY_ROOT,
    CatalogValidationError,
    extract_live_registry,
    load_publisher_contracts,
    load_resources,
    load_site,
    load_taxonomy,
    taxonomy_indexes,
    validate_catalog,
)


def _catalog_record(resource, indexes, site):
    classification = resource["taxonomy"]
    grade = classification["grade"]
    subject = classification["subject"]
    topic = classification["topic"]
    skill_id = classification["skills"][0]
    grade_label = indexes["grades"][grade]["label"]
    subject_label = indexes["subjects"][subject]["label"]
    topic_label = indexes["topics"][(grade, subject, topic)]["label"]
    skill_label = indexes["skills"][(grade, subject, topic, skill_id)]["label"]
    assets = resource["assets"]
    page_labels = [page.get("label") for page in resource["pages"]]
    if not any(page_labels):
        page_labels = None
    return {
        "id": resource["id"],
        "title": resource["title"],
        "description": resource["description"],
        "grade": grade_label,
        "subject": subject_label,
        "topic": topic_label,
        "skill": skill_label,
        "keywords": resource["keywords"],
        "bundlePdf": assets["bundlePdf"],
        "thumbnailPath": f"{assets['previewDirectory']}/page-01.png",
        "pageCount": len(resource["pages"]),
        "pageLabels": page_labels,
        "pagePdfDirectory": assets["pagePdfDirectory"],
        "previewDirectory": assets["previewDirectory"],
        "backHref": resource["legacy"]["backHref"],
        "backLabel": resource["legacy"]["backLabel"],
        "previewHref": resource["legacy"]["previewHref"],
        "seo": resource["seo"],
        "order": resource["ordering"]["catalog"],
        "pdfUrl": f"{site['assetOrigin']}/{assets['bundlePdf']}",
        "thumbnailUrl": f"{site['assetOrigin']}/{assets['previewDirectory']}/page-01.png",
    }


def _live_record(resource, site):
    return {
        **resource,
        "pdfUrl": f"{site['assetOrigin']}/{resource['bundlePdf']}",
        "thumbnailUrl": f"{site['assetOrigin']}/{resource['thumbnailPath']}",
    }


def main() -> None:
    site = load_site()
    taxonomy = load_taxonomy()
    resources = load_resources()
    counts = validate_catalog(site, taxonomy, resources)
    indexes = taxonomy_indexes(taxonomy)
    published = sorted(
        (resource for resource in resources if resource["status"] == "published"),
        key=lambda resource: resource["ordering"]["catalog"],
    )
    retired = [resource for resource in resources if resource["status"] == "retired"]
    live = extract_live_registry(REPOSITORY_ROOT / "directory.js")

    if len(published) != 41 or len(live) != 41:
        raise CatalogValidationError(
            f"Expected exact 41-resource parity; catalog={len(published)} registry={len(live)}"
        )
    catalog_ids = [resource["id"] for resource in published]
    live_ids = [resource["id"] for resource in live]
    if catalog_ids != live_ids:
        raise CatalogValidationError(
            f"Published resource IDs/order differ: catalog={catalog_ids} registry={live_ids}"
        )

    compared_fields = (
        "id", "title", "description", "grade", "subject", "topic", "skill",
        "keywords", "bundlePdf", "thumbnailPath", "pageCount", "pageLabels",
        "pagePdfDirectory", "previewDirectory", "backHref", "backLabel",
        "previewHref", "seo", "order", "pdfUrl", "thumbnailUrl",
    )
    differences = []
    for catalog_resource, live_resource in zip(published, live):
        catalog_record = _catalog_record(catalog_resource, indexes, site)
        live_record = _live_record(live_resource, site)
        for field in compared_fields:
            if catalog_record[field] != live_record[field]:
                differences.append(
                    f"{catalog_resource['id']}.{field}: "
                    f"catalog={catalog_record[field]!r} registry={live_record[field]!r}"
                )
    if differences:
        raise CatalogValidationError("Catalog parity failed:\n" + "\n".join(differences))

    contracts = load_publisher_contracts(REPOSITORY_ROOT / "worksheet-generator" / "content")
    resource_by_id = {resource["id"]: resource for resource in resources}
    contract_differences = []
    for resource_id, contract in contracts.items():
        resource = resource_by_id.get(resource_id)
        if resource is None:
            contract_differences.append(f"{resource_id}: publisher contract has no catalog resource")
            continue
        assets = resource["assets"]
        expected = {
            "path": resource["source"]["publisherContract"],
            "filename": assets["bundlePdf"].rsplit("/", 1)[-1],
            "pageCount": len(resource["pages"]),
            "pagePdfDirectory": assets["pagePdfDirectory"],
            "previewDirectory": assets["previewDirectory"],
            "previewDpi": assets["preview"]["dpi"],
        }
        for field, expected_value in expected.items():
            if contract[field] != expected_value:
                contract_differences.append(
                    f"{resource_id}.{field}: catalog={expected_value!r} contract={contract[field]!r}"
                )
    if contract_differences:
        raise CatalogValidationError(
            "Publisher contract parity failed:\n" + "\n".join(contract_differences)
        )

    statuses = Counter(resource["status"] for resource in resources)
    if statuses != Counter({"published": 41, "retired": 1}):
        raise CatalogValidationError(f"Unexpected publication states: {dict(statuses)}")
    if len(retired) != 1 or retired[0]["id"] != "story-comprehension":
        raise CatalogValidationError("The original Story & Comprehension resource must be retired")

    print(
        "PARITY exact "
        f"published={counts.get('published', 0)} retired={counts.get('retired', 0)} "
        f"registry={len(live)} contracts={len(contracts)} fields={len(compared_fields)}"
    )


if __name__ == "__main__":
    main()
