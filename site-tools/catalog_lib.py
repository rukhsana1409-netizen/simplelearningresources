"""Shared loading, validation, and legacy-registry parity helpers."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
CATALOG_ROOT = REPOSITORY_ROOT / "catalog"
RESOURCE_ROOT = CATALOG_ROOT / "resources"
VALID_STATUSES = {"draft", "review", "published", "retired"}
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LANGUAGE_PATTERN = re.compile(r"^[a-z]{2}(?:-[A-Z]{2})?$")
RESERVED_RESOURCE_ROUTES = {
    "404", "api", "assets", "grade", "grades", "index", "search",
    "skill", "skills", "topic", "topics",
}


class CatalogValidationError(ValueError):
    """Raised when authoritative catalog data violates its contract."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CatalogValidationError(f"Cannot read JSON {path}: {error}") from error


def load_site() -> dict[str, Any]:
    return load_json(CATALOG_ROOT / "site.json")


def load_taxonomy() -> dict[str, list[dict[str, Any]]]:
    taxonomy_root = CATALOG_ROOT / "taxonomy"
    return {
        name: load_json(taxonomy_root / f"{name}.json")
        for name in ("grades", "subjects", "topics", "skills")
    }


def load_navigation() -> dict[str, Any]:
    return load_json(CATALOG_ROOT / "navigation.json")


def load_resources() -> list[dict[str, Any]]:
    resources = []
    for path in sorted(RESOURCE_ROOT.rglob("*.json")):
        resource = load_json(path)
        resource["_path"] = path.relative_to(REPOSITORY_ROOT).as_posix()
        resources.append(resource)
    return resources


def taxonomy_indexes(taxonomy: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "grades": {item["id"]: item for item in taxonomy["grades"]},
        "subjects": {item["id"]: item for item in taxonomy["subjects"]},
        "topics": {
            (item["grade"], item["subject"], item["id"]): item
            for item in taxonomy["topics"]
        },
        "skills": {
            (item["grade"], item["subject"], item["topic"], item["id"]): item
            for item in taxonomy["skills"]
        },
    }


def _require_string(value: Any, field: str, resource_id: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CatalogValidationError(f"{resource_id}: {field} must be a nonempty string")
    return value


def _validate_taxonomy_collection(
    name: str, items: list[dict[str, Any]], required_fields: tuple[str, ...]
) -> None:
    if not isinstance(items, list):
        raise CatalogValidationError(f"taxonomy/{name}.json must contain an array")
    keys = []
    orders = []
    key_fields = {
        "grades": ("id",),
        "subjects": ("id",),
        "topics": ("grade", "subject", "id"),
        "skills": ("grade", "subject", "topic", "id"),
    }[name]
    order_scope = {
        "grades": (),
        "subjects": (),
        "topics": ("grade", "subject"),
        "skills": ("grade", "subject", "topic"),
    }[name]
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise CatalogValidationError(f"taxonomy/{name}.json item {index} must be an object")
        missing = [field for field in required_fields if field not in item]
        if missing:
            raise CatalogValidationError(
                f"taxonomy/{name}.json item {index} is missing: {', '.join(missing)}"
            )
        if not ID_PATTERN.fullmatch(str(item["id"])):
            raise CatalogValidationError(f"taxonomy/{name}.json has invalid id: {item['id']}")
        if set(item) != set(required_fields):
            raise CatalogValidationError(
                f"taxonomy/{name}.json item {index} has unsupported or missing fields"
            )
        _require_string(item["label"], "label", f"taxonomy/{name}[{index}]")
        if not isinstance(item["order"], int) or item["order"] < 1:
            raise CatalogValidationError(f"taxonomy/{name}.json item {index} has invalid order")
        keys.append(tuple(item[field] for field in key_fields))
        orders.append((*tuple(item[field] for field in order_scope), item["order"]))
    duplicates = [key for key, count in Counter(keys).items() if count > 1]
    if duplicates:
        raise CatalogValidationError(f"taxonomy/{name}.json has duplicate keys: {duplicates}")
    duplicate_orders = [key for key, count in Counter(orders).items() if count > 1]
    if duplicate_orders:
        raise CatalogValidationError(
            f"taxonomy/{name}.json has duplicate scoped ordering: {duplicate_orders}"
        )


def validate_catalog(
    site: dict[str, Any],
    taxonomy: dict[str, list[dict[str, Any]]],
    resources: list[dict[str, Any]],
    repository_root: Path = REPOSITORY_ROOT,
) -> dict[str, int]:
    schema = load_json(CATALOG_ROOT / "schema" / "resource.schema.json")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise CatalogValidationError("resource.schema.json must use JSON Schema draft 2020-12")
    if set(site) != {"schemaVersion", "canonicalOrigin", "assetOrigin", "legacyResourcePath", "compatibility"}:
        raise CatalogValidationError("site.json has unsupported or missing fields")
    for field in ("canonicalOrigin", "assetOrigin", "legacyResourcePath"):
        _require_string(site.get(field), f"site.{field}", "site")
    if site.get("schemaVersion") != 1:
        raise CatalogValidationError("site.schemaVersion must equal 1")
    compatibility = site.get("compatibility")
    if not isinstance(compatibility, dict) or set(compatibility) != {
        "singletonTopicLinks", "topicRouteOverrides", "directory", "sitemap"
    }:
        raise CatalogValidationError("site.compatibility has unsupported or missing fields")
    if compatibility["singletonTopicLinks"] is not True:
        raise CatalogValidationError("Step 2 requires current singleton topic links")
    if not isinstance(compatibility["topicRouteOverrides"], dict):
        raise CatalogValidationError("site.compatibility.topicRouteOverrides must be an object")
    directory_config = compatibility["directory"]
    if not isinstance(directory_config, dict) or set(directory_config) != {
        "gradePaths", "subjectPaths", "subjectLegacyKeys"
    }:
        raise CatalogValidationError("site.compatibility.directory has unsupported or missing fields")
    for field in ("gradePaths", "subjectPaths", "subjectLegacyKeys"):
        values = directory_config[field]
        if not isinstance(values, dict) or any(
            not isinstance(key, str) or not isinstance(value, str) or not value
            for key, value in values.items()
        ):
            raise CatalogValidationError(
                f"site.compatibility.directory.{field} must be a string map"
            )
        if len(values.values()) != len(set(values.values())):
            raise CatalogValidationError(
                f"site.compatibility.directory.{field} contains duplicate values"
            )
    sitemap_config = compatibility["sitemap"]
    if not isinstance(sitemap_config, dict) or set(sitemap_config) != {
        "staticPaths", "subjectOrder", "skillPaths"
    }:
        raise CatalogValidationError("site.compatibility.sitemap has unsupported or missing fields")
    for field in ("staticPaths", "subjectOrder", "skillPaths"):
        values = sitemap_config[field]
        if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
            raise CatalogValidationError(f"site.compatibility.sitemap.{field} must be a string array")
        if len(values) != len(set(values)):
            raise CatalogValidationError(f"site.compatibility.sitemap.{field} contains duplicates")

    _validate_taxonomy_collection("grades", taxonomy["grades"], ("id", "label", "order"))
    _validate_taxonomy_collection("subjects", taxonomy["subjects"], ("id", "label", "order"))
    _validate_taxonomy_collection(
        "topics", taxonomy["topics"], ("id", "grade", "subject", "label", "order")
    )
    _validate_taxonomy_collection(
        "skills",
        taxonomy["skills"],
        ("id", "grade", "subject", "topic", "label", "order"),
    )
    indexes = taxonomy_indexes(taxonomy)
    navigation = load_navigation()
    if set(navigation) != {"schemaVersion", "preschoolMath"} or navigation.get("schemaVersion") != 1:
        raise CatalogValidationError("navigation.json has unsupported or missing fields")
    preschool_math = navigation["preschoolMath"]
    if not isinstance(preschool_math, dict) or set(preschool_math) != {
        "numbersCounting", "additionalSubjectCards"
    }:
        raise CatalogValidationError("navigation.preschoolMath has unsupported or missing fields")
    directory_config = compatibility["directory"]
    if set(directory_config["gradePaths"]) != set(indexes["grades"]):
        raise CatalogValidationError("directory gradePaths must cover every taxonomy grade")
    if set(directory_config["subjectPaths"]) != set(indexes["subjects"]):
        raise CatalogValidationError("directory subjectPaths must cover every taxonomy subject")
    if set(directory_config["subjectLegacyKeys"]) != set(indexes["subjects"]):
        raise CatalogValidationError("directory subjectLegacyKeys must cover every taxonomy subject")
    for topic_item in taxonomy["topics"]:
        if topic_item["grade"] not in indexes["grades"] or topic_item["subject"] not in indexes["subjects"]:
            raise CatalogValidationError(
                f"taxonomy topic {topic_item['id']} has an unknown grade or subject"
            )
    for skill_item in taxonomy["skills"]:
        topic_key = (skill_item["grade"], skill_item["subject"], skill_item["topic"])
        if topic_key not in indexes["topics"]:
            raise CatalogValidationError(
                f"taxonomy skill {skill_item['id']} has an unknown topic mapping"
            )

    ids: list[str] = []
    catalog_orders: list[int] = []
    canonical_paths: list[str] = []
    bundle_paths: list[str] = []
    page_pdf_paths: list[str] = []
    preview_paths: list[str] = []

    for resource in resources:
        resource_id = _require_string(resource.get("id"), "id", resource.get("_path", "resource"))
        allowed_fields = {
            "schemaVersion", "id", "status", "routing", "publication", "title",
            "description", "learningFocus", "adultGuidance", "language", "resourceType",
            "relatedResources", "taxonomy", "keywords", "pages", "assets", "seo",
            "source", "ordering", "legacy", "_path",
        }
        if resource.get("status") == "retired":
            allowed_fields.add("retiredReason")
        required_fields = {
            "schemaVersion", "id", "status", "routing", "publication", "title",
            "description", "learningFocus", "taxonomy", "keywords", "pages", "assets",
            "seo", "source", "ordering", "legacy", "_path",
        }
        if resource.get("status") == "retired":
            required_fields.add("retiredReason")
        unsupported = set(resource) - allowed_fields
        missing = required_fields - set(resource)
        if unsupported or missing:
            raise CatalogValidationError(
                f"{resource_id}: resource has unsupported or missing fields: "
                f"{sorted(unsupported | missing)}"
            )
        if not ID_PATTERN.fullmatch(resource_id):
            raise CatalogValidationError(f"{resource_id}: id must be lowercase kebab-case")
        if resource.get("schemaVersion") != 2:
            raise CatalogValidationError(f"{resource_id}: schemaVersion must equal 2")
        status = resource.get("status")
        if status not in VALID_STATUSES:
            raise CatalogValidationError(f"{resource_id}: unsupported status {status!r}")
        if status == "retired":
            _require_string(resource.get("retiredReason"), "retiredReason", resource_id)
        _require_string(resource.get("title"), "title", resource_id)
        _require_string(resource.get("description"), "description", resource_id)

        routing = resource.get("routing")
        if not isinstance(routing, dict) or set(routing) != {"slug", "aliases"}:
            raise CatalogValidationError(f"{resource_id}: routing has unsupported or missing fields")
        slug = _require_string(routing.get("slug"), "routing.slug", resource_id)
        aliases = routing.get("aliases")
        if not ID_PATTERN.fullmatch(slug):
            raise CatalogValidationError(f"{resource_id}: routing.slug must be lowercase kebab-case")
        if not isinstance(aliases, list) or any(
            not isinstance(alias, str) or not ID_PATTERN.fullmatch(alias) for alias in aliases
        ):
            raise CatalogValidationError(f"{resource_id}: routing.aliases must contain kebab-case slugs")
        if len(aliases) != len(set(aliases)) or slug in aliases:
            raise CatalogValidationError(f"{resource_id}: routing aliases must be unique and exclude slug")
        for route in [slug, *aliases]:
            if route in RESERVED_RESOURCE_ROUTES:
                raise CatalogValidationError(f"{resource_id}: routing uses reserved route {route!r}")
        if status == "published" and slug != resource_id:
            raise CatalogValidationError(
                f"{resource_id}: published routing.slug is immutable and must equal the resource id"
            )

        publication = resource.get("publication")
        if not isinstance(publication, dict) or set(publication) != {"publishedAt", "updatedAt"}:
            raise CatalogValidationError(
                f"{resource_id}: publication has unsupported or missing fields"
            )
        parsed_dates: dict[str, date | None] = {}
        for field in ("publishedAt", "updatedAt"):
            value = publication.get(field)
            if value is None and status in {"draft", "review"}:
                parsed_dates[field] = None
                continue
            try:
                parsed_dates[field] = date.fromisoformat(value) if isinstance(value, str) else None
            except ValueError as error:
                raise CatalogValidationError(
                    f"{resource_id}: publication.{field} must be a valid ISO date"
                ) from error
            if parsed_dates[field] is None:
                raise CatalogValidationError(
                    f"{resource_id}: publication.{field} is required for {status} resources"
                )
        if parsed_dates["publishedAt"] and parsed_dates["updatedAt"] < parsed_dates["publishedAt"]:
            raise CatalogValidationError(
                f"{resource_id}: publication.updatedAt cannot be before publication"
            )
        if status == "published" and any(
            value is not None and value > date.today() for value in parsed_dates.values()
        ):
            raise CatalogValidationError(
                f"{resource_id}: published resource dates cannot be in the future"
            )

        learning_focus = resource.get("learningFocus")
        if not isinstance(learning_focus, list) or not learning_focus or any(
            not isinstance(item, str) or not item.strip() for item in learning_focus
        ):
            raise CatalogValidationError(
                f"{resource_id}: learningFocus must contain nonempty strings"
            )
        if len({item.casefold() for item in learning_focus}) != len(learning_focus):
            raise CatalogValidationError(f"{resource_id}: learningFocus contains duplicates")
        if "adultGuidance" in resource:
            _require_string(resource["adultGuidance"], "adultGuidance", resource_id)
        if "language" in resource and not LANGUAGE_PATTERN.fullmatch(resource["language"]):
            raise CatalogValidationError(f"{resource_id}: language must be a valid language tag")
        if resource.get("resourceType", "worksheet") not in {"worksheet", "worksheet-pack"}:
            raise CatalogValidationError(f"{resource_id}: resourceType is unsupported")
        related_resources = resource.get("relatedResources")
        if related_resources is not None and (
            not isinstance(related_resources, list)
            or any(not isinstance(item, str) or not ID_PATTERN.fullmatch(item) for item in related_resources)
            or len(related_resources) != len(set(related_resources))
        ):
            raise CatalogValidationError(
                f"{resource_id}: relatedResources must contain unique resource ids"
            )

        classification = resource.get("taxonomy")
        if not isinstance(classification, dict):
            raise CatalogValidationError(f"{resource_id}: taxonomy must be an object")
        if set(classification) != {"grade", "subject", "topic", "skills"}:
            raise CatalogValidationError(f"{resource_id}: taxonomy has unsupported or missing fields")
        grade = classification.get("grade")
        subject = classification.get("subject")
        topic = classification.get("topic")
        skills = classification.get("skills")
        if grade not in indexes["grades"]:
            raise CatalogValidationError(f"{resource_id}: unknown grade {grade!r}")
        if subject not in indexes["subjects"]:
            raise CatalogValidationError(f"{resource_id}: unknown subject {subject!r}")
        if (grade, subject, topic) not in indexes["topics"]:
            raise CatalogValidationError(
                f"{resource_id}: topic {topic!r} is not mapped to {grade}/{subject}"
            )
        if not isinstance(skills, list) or not skills:
            raise CatalogValidationError(f"{resource_id}: taxonomy.skills must be nonempty")
        for skill in skills:
            if (grade, subject, topic, skill) not in indexes["skills"]:
                raise CatalogValidationError(
                    f"{resource_id}: skill {skill!r} is not mapped to {grade}/{subject}/{topic}"
                )

        keywords = resource.get("keywords")
        if not isinstance(keywords, list) or not keywords or any(
            not isinstance(keyword, str) or not keyword.strip() for keyword in keywords
        ):
            raise CatalogValidationError(f"{resource_id}: keywords must contain nonempty strings")
        if len({keyword.casefold() for keyword in keywords}) != len(keywords):
            raise CatalogValidationError(f"{resource_id}: keywords contain duplicates")

        pages = resource.get("pages")
        if not isinstance(pages, list) or not pages:
            raise CatalogValidationError(f"{resource_id}: pages must be a nonempty array")
        for page_number, page in enumerate(pages, start=1):
            if not isinstance(page, dict):
                raise CatalogValidationError(f"{resource_id}: page {page_number} must be an object")
            if set(page) - {"label", "previewAlt"}:
                raise CatalogValidationError(
                    f"{resource_id}: page {page_number} contains unsupported fields"
                )
            if "label" in page:
                _require_string(page["label"], f"pages[{page_number}].label", resource_id)
            if "previewAlt" in page:
                _require_string(page["previewAlt"], f"pages[{page_number}].previewAlt", resource_id)

        assets = resource.get("assets")
        if not isinstance(assets, dict):
            raise CatalogValidationError(f"{resource_id}: assets must be an object")
        if set(assets) != {"bundlePdf", "pagePdfDirectory", "previewDirectory", "preview"}:
            raise CatalogValidationError(f"{resource_id}: assets has unsupported or missing fields")
        bundle = _require_string(assets.get("bundlePdf"), "assets.bundlePdf", resource_id)
        page_directory = _require_string(
            assets.get("pagePdfDirectory"), "assets.pagePdfDirectory", resource_id
        )
        preview_directory = _require_string(
            assets.get("previewDirectory"), "assets.previewDirectory", resource_id
        )
        preview = assets.get("preview")
        if preview != {"width": 1224, "height": 1584, "dpi": 144, "format": "png"}:
            raise CatalogValidationError(
                f"{resource_id}: preview contract must be 1224x1584, 144 DPI PNG"
            )

        seo = resource.get("seo")
        if not isinstance(seo, dict) or set(seo) - {"title", "description", "socialImage"} or not {"title", "description"}.issubset(seo):
            raise CatalogValidationError(f"{resource_id}: seo has unsupported or missing fields")
        _require_string(seo.get("title"), "seo.title", resource_id)
        _require_string(seo.get("description"), "seo.description", resource_id)
        if "socialImage" in seo:
            _require_string(seo["socialImage"], "seo.socialImage", resource_id)

        ordering = resource.get("ordering")
        if not isinstance(ordering, dict) or set(ordering) != {"catalog", "withinTopic"}:
            raise CatalogValidationError(f"{resource_id}: ordering has unsupported or missing fields")
        if not isinstance(ordering.get("catalog"), int) or ordering["catalog"] < 1:
            raise CatalogValidationError(f"{resource_id}: ordering.catalog must be an integer")
        if not isinstance(ordering.get("withinTopic"), int) or ordering["withinTopic"] < 1:
            raise CatalogValidationError(f"{resource_id}: ordering.withinTopic must be an integer")

        source = resource.get("source")
        if not isinstance(source, dict):
            raise CatalogValidationError(f"{resource_id}: source must be an object")
        if set(source) != {"type", "publisherContract", "generatorConfig"}:
            raise CatalogValidationError(f"{resource_id}: source has unsupported or missing fields")
        if source.get("type") not in {"generated", "approved-bundle"}:
            raise CatalogValidationError(f"{resource_id}: source.type is invalid")
        generator_config = source.get("generatorConfig")
        if source["type"] == "generated" and not isinstance(generator_config, str):
            raise CatalogValidationError(f"{resource_id}: generated source requires generatorConfig")
        if source["type"] == "approved-bundle" and generator_config is not None:
            raise CatalogValidationError(
                f"{resource_id}: approved-bundle source must not define generatorConfig"
            )
        contract_path = _require_string(
            source.get("publisherContract"), "source.publisherContract", resource_id
        )
        if not (repository_root / contract_path).is_file():
            raise CatalogValidationError(
                f"{resource_id}: publisher contract is missing: {contract_path}"
            )

        legacy = resource.get("legacy")
        if not isinstance(legacy, dict):
            raise CatalogValidationError(f"{resource_id}: legacy must be an object")
        if set(legacy) != {"previewHref", "backHref", "backLabel"}:
            raise CatalogValidationError(f"{resource_id}: legacy has unsupported or missing fields")
        _require_string(legacy.get("previewHref"), "legacy.previewHref", resource_id)
        _require_string(legacy.get("backHref"), "legacy.backHref", resource_id)
        _require_string(legacy.get("backLabel"), "legacy.backLabel", resource_id)
        expected_preview_href = f"resource-preview.html?resource={resource_id}"
        if legacy["previewHref"] != expected_preview_href:
            raise CatalogValidationError(
                f"{resource_id}: legacy.previewHref must equal {expected_preview_href}"
            )

        expected_catalog_path = (
            f"catalog/resources/{grade}/{subject}/{topic}/{resource_id}.json"
        )
        if resource["_path"] != expected_catalog_path:
            raise CatalogValidationError(
                f"{resource_id}: definition path must be {expected_catalog_path}"
            )

        ids.append(resource_id)
        catalog_orders.append(ordering["catalog"])
        canonical_paths.append(f"resources/{slug}/")
        bundle_paths.append(bundle)
        for page_number in range(1, len(pages) + 1):
            page_pdf_paths.append(f"{page_directory}/page-{page_number:02d}.pdf")
            preview_paths.append(f"{preview_directory}/page-{page_number:02d}.png")

        for relative_path in [bundle, *page_pdf_paths[-len(pages):], *preview_paths[-len(pages):]]:
            path = repository_root / relative_path
            if not path.is_file() or path.stat().st_size == 0:
                raise CatalogValidationError(f"{resource_id}: asset is missing or empty: {relative_path}")

    resource_ids = set(ids)
    routes = [
        route
        for resource in resources
        for route in [resource["routing"]["slug"], *resource["routing"]["aliases"]]
    ]
    duplicate_routes = [route for route, count in Counter(routes).items() if count > 1]
    if duplicate_routes:
        raise CatalogValidationError(f"Duplicate routing slugs or aliases: {duplicate_routes}")
    for resource in resources:
        related = resource.get("relatedResources", [])
        unknown = [item for item in related if item not in resource_ids]
        if unknown:
            raise CatalogValidationError(
                f"{resource['id']}: relatedResources contains unknown ids: {unknown}"
            )
        if resource["id"] in related:
            raise CatalogValidationError(
                f"{resource['id']}: relatedResources cannot include the resource itself"
            )
    for group_name, cards in preschool_math.items():
        if not isinstance(cards, list) or not cards:
            raise CatalogValidationError(f"navigation.preschoolMath.{group_name} must be nonempty")
        for card in cards:
            if not isinstance(card, dict) or card.get("type") not in {"skill", "topic", "resource"}:
                raise CatalogValidationError(f"navigation card in {group_name} has an invalid type")
            if card["type"] == "resource":
                if set(card) != {"type", "resource"} or card.get("resource") not in resource_ids:
                    raise CatalogValidationError(f"navigation references invalid resource {card.get('resource')}")
            elif card["type"] == "skill":
                if set(card) != {"type", "skill", "description", "href"}:
                    raise CatalogValidationError("navigation skill card has unsupported or missing fields")
                _require_string(card.get("description"), "description", "navigation skill card")
                _require_string(card.get("href"), "href", "navigation skill card")
                if not any(
                    key[0] == "preschool" and key[1] == "math" and key[3] == card.get("skill")
                    for key in indexes["skills"]
                ):
                    raise CatalogValidationError(f"navigation references unknown math skill {card.get('skill')}")
            else:
                if set(card) != {"type", "topic", "description"}:
                    raise CatalogValidationError("navigation topic card has unsupported or missing fields")
                _require_string(card.get("description"), "description", "navigation topic card")
                if ("preschool", "math", card.get("topic")) not in indexes["topics"]:
                    raise CatalogValidationError(f"navigation references unknown math topic {card.get('topic')}")

    for route_key, href in compatibility["topicRouteOverrides"].items():
        parts = route_key.split("/")
        if len(parts) != 3 or tuple(parts) not in indexes["topics"]:
            raise CatalogValidationError(f"topicRouteOverrides references unknown topic {route_key}")
        _require_string(href, "href", f"topicRouteOverrides.{route_key}")

    duplicate_checks = {
        "resource ids": ids,
        "catalog ordering": catalog_orders,
        "canonical paths": canonical_paths,
        "bundle paths": bundle_paths,
        "page PDF paths": page_pdf_paths,
        "preview paths": preview_paths,
    }
    for label, values in duplicate_checks.items():
        duplicates = [value for value, count in Counter(values).items() if count > 1]
        if duplicates:
            raise CatalogValidationError(f"Duplicate {label}: {duplicates}")

    return dict(Counter(resource["status"] for resource in resources))


def _split_top_level_objects(source: str) -> list[str]:
    objects: list[str] = []
    depth = 0
    start = None
    quote = None
    escaped = False
    for index, character in enumerate(source):
        if quote:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
            continue
        if character in {'"', "'", "`"}:
            quote = character
        elif character == "{":
            if depth == 0:
                start = index
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0 and start is not None:
                objects.append(source[start : index + 1])
                start = None
    if depth != 0 or quote:
        raise CatalogValidationError("Cannot parse worksheetResourceDefinitions")
    return objects


def _js_string(obj: str, field: str) -> str:
    match = re.search(rf'(?:^|[{{,])\s*(?:{re.escape(field)}|"{re.escape(field)}")\s*:\s*("(?:\\.|[^"\\])*")', obj)
    if not match:
        raise CatalogValidationError(f"Legacy registry object is missing {field}: {obj[:100]}")
    return json.loads(match.group(1))


def _js_optional_string(obj: str, field: str) -> str | None:
    match = re.search(rf'(?:^|[{{,])\s*(?:{re.escape(field)}|"{re.escape(field)}")\s*:\s*("(?:\\.|[^"\\])*")', obj)
    return json.loads(match.group(1)) if match else None


def _js_integer(obj: str, field: str) -> int:
    match = re.search(rf'(?:^|[{{,])\s*(?:{re.escape(field)}|"{re.escape(field)}")\s*:\s*(\d+)', obj)
    if not match:
        raise CatalogValidationError(f"Legacy registry object is missing {field}")
    return int(match.group(1))


def _js_string_array(obj: str, field: str) -> list[str] | None:
    array = re.search(
        rf'(?:^|[{{,])\s*(?:{re.escape(field)}|"{re.escape(field)}")\s*:\s*(\[(?:\s*"(?:\\.|[^"\\])*"\s*,?)*\])',
        obj,
    )
    if array:
        return json.loads(array.group(1))
    if field == "pageLabels" and re.search(r"pageLabels\s*:\s*Array\.from\(\{length:26\}", obj):
        return [f"Letter {chr(65 + index)}" for index in range(26)]
    return None


def extract_live_registry(directory_path: Path) -> list[dict[str, Any]]:
    source = directory_path.read_text(encoding="utf-8")
    start = source.index("const worksheetResourceDefinitions = [")
    start = source.index("[", start) + 1
    end = source.index("\n];\nconst preschoolMathResourceSeoMetadata", start)
    objects = _split_top_level_objects(source[start:end])

    seo: dict[str, dict[str, str]] = {}
    for match in re.finditer(
        r'"([a-z0-9-]+)"\s*:\s*\{seoTitle:("(?:\\.|[^"\\])*"),seoDescription:("(?:\\.|[^"\\])*")\}',
        source,
    ):
        seo[match.group(1)] = {
            "title": json.loads(match.group(2)),
            "description": json.loads(match.group(3)),
        }

    resources = []
    for order, obj in enumerate(objects, start=1):
        resource_id = _js_string(obj, "id")
        page_count = _js_integer(obj, "pageCount")
        define_pages = re.search(
            r'pages\s*:\s*defineWorksheetPages\(\d+,\s*("(?:\\.|[^"\\])*")\s*,\s*("(?:\\.|[^"\\])*")\)',
            obj,
        )
        if define_pages:
            page_pdf_directory = json.loads(define_pages.group(1))
            preview_directory = json.loads(define_pages.group(2))
        else:
            explicit = re.search(r'"?pages"?\s*:\s*\[(.*)\]\s*,\s*"?backHref"?', obj)
            if not explicit:
                raise CatalogValidationError(f"Cannot parse pages for {resource_id}")
            page_pdf = re.search(r'"pdfPath"\s*:\s*"([^"]+/page-01\.pdf)"', explicit.group(1))
            preview = re.search(r'"previewPath"\s*:\s*"([^"]+/page-01\.png)"', explicit.group(1))
            if not page_pdf or not preview:
                raise CatalogValidationError(f"Cannot parse explicit pages for {resource_id}")
            page_pdf_directory = page_pdf.group(1).rsplit("/", 1)[0]
            preview_directory = preview.group(1).rsplit("/", 1)[0]
        if resource_id not in seo:
            raise CatalogValidationError(f"Legacy registry SEO metadata is missing for {resource_id}")
        resources.append(
            {
                "id": resource_id,
                "slug": _js_optional_string(obj, "slug") or resource_id,
                "title": _js_string(obj, "title"),
                "description": _js_string(obj, "description"),
                "grade": _js_string(obj, "grade"),
                "subject": _js_string(obj, "subject"),
                "topic": _js_string(obj, "topic"),
                "skill": _js_string(obj, "skill"),
                "keywords": _js_string_array(obj, "keywords"),
                "bundlePdf": _js_string(obj, "pdfPath"),
                "thumbnailPath": _js_string(obj, "thumbnailPath"),
                "pageCount": page_count,
                "pageLabels": _js_string_array(obj, "pageLabels"),
                "pagePdfDirectory": page_pdf_directory,
                "previewDirectory": preview_directory,
                "backHref": _js_string(obj, "backHref"),
                "backLabel": _js_string(obj, "backLabel"),
                "previewHref": _js_optional_string(obj, "previewHref") or f"resource-preview.html?resource={resource_id}",
                "legacyPreviewHref": _js_optional_string(obj, "legacyPreviewHref") or f"resource-preview.html?resource={resource_id}",
                "seo": seo[resource_id],
                "order": order,
            }
        )
    return resources


def load_publisher_contracts(content_root: Path) -> dict[str, dict[str, Any]]:
    contracts: dict[str, dict[str, Any]] = {}
    for path in sorted(content_root.glob("*.json")):
        data = load_json(path)
        output = data.get("asset_output")
        if not output:
            continue
        resource_id = output.get("resource_id")
        if resource_id in contracts:
            raise CatalogValidationError(f"Duplicate publisher contract for {resource_id}")
        contracts[resource_id] = {
            "path": path.relative_to(REPOSITORY_ROOT).as_posix(),
            "filename": data.get("filename"),
            "pageCount": output.get("expected_page_count"),
            "pagePdfDirectory": output.get("page_pdf_directory"),
            "previewDirectory": output.get("preview_directory"),
            "previewDpi": output.get("preview_dpi", 144),
            "hasGeneratorTemplate": bool(data.get("template")),
        }
    return contracts
