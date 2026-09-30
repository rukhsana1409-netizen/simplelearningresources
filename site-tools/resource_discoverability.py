"""Pure derivations for future catalog-generated resource pages."""

from __future__ import annotations

from typing import Any


DEFAULT_LANGUAGE = "en"


def resource_page_href(resource: dict[str, Any]) -> str:
    return f"resources/{resource['routing']['slug']}/"


def page_label(resource: dict[str, Any], page_index: int) -> str:
    page = resource["pages"][page_index]
    return page.get("label") or f"Page {page_index + 1}"


def default_preview_alt(resource: dict[str, Any], page_index: int) -> str:
    override = resource["pages"][page_index].get("previewAlt")
    return override or f"Preview of {page_label(resource, page_index)} from {resource['title']}"


def default_social_image(resource: dict[str, Any]) -> str:
    return resource["seo"].get("socialImage") or (
        f"{resource['assets']['previewDirectory']}/page-01.png"
    )


def effective_language(resource: dict[str, Any]) -> str:
    return resource.get("language", DEFAULT_LANGUAGE)


def effective_resource_type(resource: dict[str, Any]) -> str:
    override = resource.get("resourceType")
    if override:
        return override
    return "worksheet" if len(resource["pages"]) == 1 else "worksheet-pack"


def is_public_page_eligible(resource: dict[str, Any]) -> bool:
    return resource.get("status") == "published"


def related_resource_ids(
    resource: dict[str, Any], resources: list[dict[str, Any]], limit: int = 4
) -> list[str]:
    override = resource.get("relatedResources")
    if override is not None:
        return override[:limit]

    candidates = [
        candidate
        for candidate in resources
        if is_public_page_eligible(candidate) and candidate["id"] != resource["id"]
    ]
    candidates.sort(
        key=lambda candidate: (
            candidate["taxonomy"]["topic"] != resource["taxonomy"]["topic"],
            candidate["taxonomy"]["subject"] != resource["taxonomy"]["subject"],
            candidate["taxonomy"]["grade"] != resource["taxonomy"]["grade"],
            candidate["ordering"]["catalog"],
            candidate["id"],
        )
    )
    return [candidate["id"] for candidate in candidates[:limit]]
