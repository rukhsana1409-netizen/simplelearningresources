"""Generate the synchronous directory.js resource compatibility block from the catalog."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from urllib.parse import quote

from catalog_lib import REPOSITORY_ROOT, load_navigation, load_resources, load_site, load_taxonomy, taxonomy_indexes, validate_catalog
from shadow_catalog import catalog_digest, published_resources


DIRECTORY_PATH = REPOSITORY_ROOT / "directory.js"
NAVIGATION_PATH = REPOSITORY_ROOT / "nav.js"
START_MARKER = "// BEGIN GENERATED CATALOG COMPATIBILITY DATA"
END_MARKER = "// END GENERATED CATALOG COMPATIBILITY DATA"
NAV_START_MARKER = "// BEGIN GENERATED PRIMARY NAVIGATION"
NAV_END_MARKER = "// END GENERATED PRIMARY NAVIGATION"


def js_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def resource_line(resource: dict, indexes: dict) -> str:
    classification = resource["taxonomy"]
    assets = resource["assets"]
    grade = indexes["grades"][classification["grade"]]["label"]
    subject = indexes["subjects"][classification["subject"]]["label"]
    topic = indexes["topics"][(classification["grade"], classification["subject"], classification["topic"])]["label"]
    skill = indexes["skills"][(classification["grade"], classification["subject"], classification["topic"], classification["skills"][0])]["label"]
    values = [
        ("id", resource["id"]), ("title", resource["title"]),
        ("description", resource["description"]), ("grade", grade),
        ("subject", subject), ("topic", topic), ("skill", skill),
    ]
    fields = [f"{key}:{js_string(value)}" for key, value in values]
    fields.append(f"keywords:{json.dumps(resource['keywords'], ensure_ascii=False, separators=(',', ':'))}")
    fields.extend((
        f"pdfPath:{js_string(assets['bundlePdf'])}",
        f"thumbnailPath:{js_string(assets['previewDirectory'] + '/page-01.png')}",
        f"pageCount:{len(resource['pages'])}",
    ))
    labels = [page.get("label") for page in resource["pages"]]
    if any(labels):
        fields.append(f"pageLabels:{json.dumps(labels, ensure_ascii=False, separators=(',', ':'))}")
    fields.append(
        f"pages:defineWorksheetPages({len(resource['pages'])},{js_string(assets['pagePdfDirectory'])},{js_string(assets['previewDirectory'])})"
    )
    fields.extend((
        f"backHref:{js_string(resource['legacy']['backHref'])}",
        f"backLabel:{js_string(resource['legacy']['backLabel'])}",
    ))
    return "  {" + ",".join(fields) + "},"


def seo_map(name: str, resources: list[dict]) -> list[str]:
    lines = [f"const {name}=Object.freeze({{"]
    for index, resource in enumerate(resources):
        suffix = "," if index < len(resources) - 1 else ""
        lines.append(
            f"  {js_string(resource['id'])}:{{seoTitle:{js_string(resource['seo']['title'])},"
            f"seoDescription:{js_string(resource['seo']['description'])}}}{suffix}"
        )
    lines.append("});")
    return lines


def directory_taxonomy(taxonomy: dict, site: dict) -> dict:
    compatibility = site["compatibility"]
    directory = compatibility["directory"]
    grades = sorted(taxonomy["grades"], key=lambda item: item["order"])
    subjects = sorted(taxonomy["subjects"], key=lambda item: item["order"])
    subject_keys = directory["subjectLegacyKeys"]
    topics = {}
    for subject in subjects:
        legacy_subject = subject_keys[subject["id"]]
        topics[legacy_subject] = {}
        for grade in grades:
            labels = [
                topic["label"]
                for topic in sorted(taxonomy["topics"], key=lambda item: item["order"])
                if topic["grade"] == grade["id"] and topic["subject"] == subject["id"]
            ]
            topics[legacy_subject][grade["id"]] = "|".join(labels)
    topic_indexes = {
        (topic["grade"], topic["subject"], topic["id"]): topic
        for topic in taxonomy["topics"]
    }
    route_overrides = {}
    for route_key, href in compatibility["topicRouteOverrides"].items():
        grade_id, subject_id, topic_id = route_key.split("/")
        topic = topic_indexes[(grade_id, subject_id, topic_id)]
        route_overrides[f"{grade_id}|{subject_keys[subject_id]}|{topic['label']}"] = href
    return {
        "grades": {grade["id"]: grade["label"] for grade in grades},
        "subjectNames": {subject_keys[subject["id"]]: subject["label"] for subject in subjects},
        "topics": topics,
        "subjectFiles": {
            path: subject_keys[subject_id]
            for subject_id, path in directory["subjectPaths"].items()
        },
        "gradeFiles": {path: grade_id for grade_id, path in directory["gradePaths"].items()},
        "skills": sorted(taxonomy["skills"], key=lambda item: (
            next(grade["order"] for grade in grades if grade["id"] == item["grade"]),
            next(subject["order"] for subject in subjects if subject["id"] == item["subject"]),
            topic_indexes[(item["grade"], item["subject"], item["topic"])]["order"],
            item["order"],
        )),
        "topicRouteOverrides": route_overrides,
    }


def directory_navigation(resources: list[dict], taxonomy: dict, site: dict, indexes: dict) -> dict:
    navigation = load_navigation()["preschoolMath"]
    resources_by_id = {resource["id"]: resource for resource in resources}
    skills = {
        item["id"]: item
        for item in taxonomy["skills"]
        if item["grade"] == "preschool" and item["subject"] == "math"
    }
    topics = {
        item["id"]: item
        for item in taxonomy["topics"]
        if item["grade"] == "preschool" and item["subject"] == "math"
    }
    overrides = directory_taxonomy(taxonomy, site)["topicRouteOverrides"]

    def resolve(card: dict) -> dict:
        if card["type"] == "resource":
            resource = resources_by_id[card["resource"]]
            return {"title": resource["title"], "description": resource["description"], "href": resource["legacy"]["previewHref"]}
        if card["type"] == "skill":
            return {"title": skills[card["skill"]]["label"], "description": card["description"], "href": card["href"]}
        topic = topics[card["topic"]]
        key = f"preschool|math|{topic['label']}"
        href = overrides.get(key, "topic.html?grade=Preschool&subject=Math&topic=" + quote(topic["label"], safe=""))
        return {"title": topic["label"], "description": card["description"], "href": href}

    numbers = [resolve(card) for card in navigation["numbersCounting"]]
    return {
        "numbersCountingSkills": numbers,
        "preschoolMathSkills": [*numbers, *[resolve(card) for card in navigation["additionalSubjectCards"]]],
    }
def render_block() -> str:
    site, taxonomy, resources = load_site(), load_taxonomy(), load_resources()
    validate_catalog(site, taxonomy, resources)
    indexes = taxonomy_indexes(taxonomy)
    published = published_resources(resources)
    by_subject = {
        subject: [resource for resource in published if resource["taxonomy"]["subject"] == subject]
        for subject in ("math", "reading-language", "communication-life-skills")
    }
    lines = [
        f"{START_MARKER} sha256={catalog_digest()}",
        "// Generated by site-tools/generate_production_runtime.py. Do not edit this block by hand.",
        "const worksheetResourceDefinitions = [",
        *[resource_line(resource, indexes) for resource in published],
        "];",
        *seo_map("preschoolMathResourceSeoMetadata", by_subject["math"]),
        *seo_map("preschoolReadingResourceSeoMetadata", by_subject["reading-language"]),
        *seo_map("preschoolCommunicationResourceSeoMetadata", by_subject["communication-life-skills"]),
        "const worksheetDirectoryTaxonomy=Object.freeze(" + json.dumps(
            directory_taxonomy(taxonomy, site), ensure_ascii=False, separators=(",", ":")
        ) + ");",
        "const worksheetDirectoryNavigation=Object.freeze(" + json.dumps(
            directory_navigation(published, taxonomy, site, indexes),
            ensure_ascii=False, separators=(",", ":")
        ) + ");",
        END_MARKER,
    ]
    return "\n".join(lines)


def render_primary_navigation(taxonomy: dict, site: dict) -> str:
    directory = site["compatibility"]["directory"]
    subjects = sorted(taxonomy["subjects"], key=lambda item: item["order"])
    grades = sorted(taxonomy["grades"], key=lambda item: item["order"])
    subject_links = "".join(
        f'<a href="{directory["subjectPaths"][subject["id"]]}">{escape(subject["label"])}</a>'
        for subject in subjects
    )
    grade_links = "".join(
        f'<a href="{directory["gradePaths"][grade["id"]]}">{escape(grade["label"])}</a>'
        for grade in grades
    )
    markup = (
        '<a href="index.html">Home</a>'
        '<div class="dropdown"><a href="worksheets.html">Resources</a><div class="dropdown-menu">'
        f'<a href="worksheets.html">All Resources</a>{subject_links}</div></div>'
        '<div class="dropdown"><a href="preschool.html">By Grade</a><div class="dropdown-menu">'
        f'{grade_links}</div></div><a href="about.html">About</a><a href="contact.html">Contact</a>'
    )
    return (
        f"{NAV_START_MARKER} sha256={catalog_digest()}\n"
        "// Generated by site-tools/generate_production_runtime.py. Do not edit this block by hand.\n"
        f"const generatedPrimaryNavigation={json.dumps(markup, ensure_ascii=False)};\n"
        f"{NAV_END_MARKER}"
    )


def replace_navigation(source: str, generated: str) -> str:
    if NAV_START_MARKER in source:
        start = source.index(NAV_START_MARKER)
        end = source.index(NAV_END_MARKER, start) + len(NAV_END_MARKER)
        source = source[:start] + generated + source[end:]
    else:
        source = generated + "\n" + source
    if "        links.innerHTML = generatedPrimaryNavigation;" in source:
        return source
    template_start = source.index("        links.innerHTML = `")
    template_end = source.index("`;", template_start) + 2
    return source[:template_start] + "        links.innerHTML = generatedPrimaryNavigation;" + source[template_end:]


def replace_block(source: str, generated: str) -> str:
    if START_MARKER in source:
        start = source.index(START_MARKER)
        end = source.index(END_MARKER, start) + len(END_MARKER)
    else:
        start = source.index("const worksheetResourceDefinitions = [")
        end = source.index("const preschoolMathTopicSeoMetadata=", start)
        while end > start and source[end - 1] in "\r\n":
            end -= 1
    return source[:start] + generated + source[end:]


def main() -> None:
    site, taxonomy = load_site(), load_taxonomy()
    source = DIRECTORY_PATH.read_text(encoding="utf-8")
    DIRECTORY_PATH.write_text(replace_block(source, render_block()), encoding="utf-8", newline="\n")
    nav_source = NAVIGATION_PATH.read_text(encoding="utf-8")
    NAVIGATION_PATH.write_text(
        replace_navigation(nav_source, render_primary_navigation(taxonomy, site)),
        encoding="utf-8", newline="\n",
    )
    resource_count = len(published_resources(load_resources()))
    print(
        f"GENERATED production runtime resources={resource_count} "
        f"paths={DIRECTORY_PATH.name},{NAVIGATION_PATH.name}"
    )


if __name__ == "__main__":
    main()
