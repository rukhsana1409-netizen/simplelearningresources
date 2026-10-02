"""Generate and validate Discoverability Phase 2 shadow resource pages."""

from __future__ import annotations

import hashlib
import json
import shutil
from html import escape
from pathlib import Path
from typing import Any
from urllib.parse import quote

from catalog_lib import (
    REPOSITORY_ROOT,
    load_resources,
    load_site,
    load_taxonomy,
    taxonomy_indexes,
    validate_catalog,
)
from resource_discoverability import (
    default_preview_alt,
    default_social_image,
    effective_language,
    effective_resource_type,
    is_public_page_eligible,
    page_label,
    related_resource_ids,
    resource_page_href,
)


SHADOW_ROOT = REPOSITORY_ROOT / "tmp" / "resource-pages-shadow"
TEMPLATE_ROOT = REPOSITORY_ROOT / "site-tools" / "templates"
GENERATOR_VERSION = 1
RELATED_RESOURCE_LIMIT = 4


class StaticPageValidationError(ValueError):
    """Raised when generated shadow pages do not match the authoritative catalog."""


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _absolute_url(origin: str, path: str) -> str:
    return f"{origin.rstrip('/')}/{path.lstrip('/')}"


def clean_resource_path(resource: dict[str, Any]) -> str:
    return resource_page_href(resource)


def clean_resource_url(resource: dict[str, Any], site: dict[str, Any]) -> str:
    return _absolute_url(site["canonicalOrigin"], clean_resource_path(resource))


def _topic_href(resource: dict[str, Any], indexes: dict[str, Any]) -> str:
    taxonomy = resource["taxonomy"]
    grade = indexes["grades"][taxonomy["grade"]]["label"]
    subject = indexes["subjects"][taxonomy["subject"]]["label"]
    topic = indexes["topics"][(taxonomy["grade"], taxonomy["subject"], taxonomy["topic"])]["label"]
    return "topic.html?grade={}&subject={}&topic={}".format(
        quote(grade, safe=""), quote(subject, safe=""), quote(topic, safe="")
    )


def _labels(resource: dict[str, Any], indexes: dict[str, Any]) -> dict[str, Any]:
    taxonomy = resource["taxonomy"]
    return {
        "grade": indexes["grades"][taxonomy["grade"]]["label"],
        "subject": indexes["subjects"][taxonomy["subject"]]["label"],
        "topic": indexes["topics"][(taxonomy["grade"], taxonomy["subject"], taxonomy["topic"])]["label"],
        "skills": [
            indexes["skills"][(taxonomy["grade"], taxonomy["subject"], taxonomy["topic"], skill)]["label"]
            for skill in taxonomy["skills"]
        ],
    }


def _json_script(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


def structured_data(
    resource: dict[str, Any],
    site: dict[str, Any],
    labels: dict[str, Any],
    indexes: dict[str, Any],
) -> dict[str, Any]:
    canonical = clean_resource_url(resource, site)
    social_image = _absolute_url(site["assetOrigin"], default_social_image(resource))
    breadcrumb_items = [
        ("Home", _absolute_url(site["canonicalOrigin"], "")),
        (labels["grade"], _absolute_url(site["canonicalOrigin"], site["compatibility"]["directory"]["gradePaths"][resource["taxonomy"]["grade"]])),
        (labels["subject"], _absolute_url(site["canonicalOrigin"], site["compatibility"]["directory"]["subjectPaths"][resource["taxonomy"]["subject"]])),
        (labels["topic"], _absolute_url(site["canonicalOrigin"], _topic_href(resource, indexes))),
        (resource["title"], canonical),
    ]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": resource["seo"]["title"],
                "description": resource["seo"]["description"],
                "inLanguage": effective_language(resource),
                "datePublished": resource["publication"]["publishedAt"],
                "dateModified": resource["publication"]["updatedAt"],
                "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
                "mainEntity": {"@id": f"{canonical}#resource"},
            },
            {
                "@type": "LearningResource",
                "@id": f"{canonical}#resource",
                "url": canonical,
                "name": resource["title"],
                "description": resource["description"],
                "inLanguage": effective_language(resource),
                "educationalLevel": labels["grade"],
                "learningResourceType": effective_resource_type(resource),
                "about": [labels["topic"], *labels["skills"]],
                "image": social_image,
                "datePublished": resource["publication"]["publishedAt"],
                "dateModified": resource["publication"]["updatedAt"],
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": position,
                        "name": name,
                        "item": url,
                    }
                    for position, (name, url) in enumerate(breadcrumb_items, start=1)
                ],
            },
        ],
    }


def render_page(
    resource: dict[str, Any],
    resources: list[dict[str, Any]],
    site: dict[str, Any],
    taxonomy: dict[str, list[dict[str, Any]]],
) -> tuple[str, list[str]]:
    indexes = taxonomy_indexes(taxonomy)
    labels = _labels(resource, indexes)
    canonical = clean_resource_url(resource, site)
    asset_origin = site["assetOrigin"]
    social_image = _absolute_url(asset_origin, default_social_image(resource))
    related_ids = related_resource_ids(resource, resources, RELATED_RESOURCE_LIMIT)
    by_id = {item["id"]: item for item in resources}
    related = [by_id[resource_id] for resource_id in related_ids]
    page_count = len(resource["pages"])
    complete_download_label = "Download Worksheet" if page_count == 1 else "Download Complete Pack"
    bundle_url = _absolute_url(asset_origin, resource["assets"]["bundlePdf"])
    grade_href = site["compatibility"]["directory"]["gradePaths"][resource["taxonomy"]["grade"]]
    subject_href = site["compatibility"]["directory"]["subjectPaths"][resource["taxonomy"]["subject"]]
    topic_href = _topic_href(resource, indexes)

    preview_cards = []
    for index in range(page_count):
        number = index + 1
        label = page_label(resource, index)
        alt = default_preview_alt(resource, index)
        preview_url = _absolute_url(asset_origin, f"{resource['assets']['previewDirectory']}/page-{number:02d}.png")
        pdf_url = _absolute_url(asset_origin, f"{resource['assets']['pagePdfDirectory']}/page-{number:02d}.pdf")
        loading = "eager" if index == 0 else "lazy"
        preview_cards.append(f"""        <article class="resource-page-preview">
        <h3>{escape(label)}</h3>
        <a class="resource-preview-link" href="{escape(pdf_url, quote=True)}" aria-label="Open {escape(label, quote=True)} PDF">
          <img src="{escape(preview_url, quote=True)}" alt="{escape(alt, quote=True)}" width="{resource['assets']['preview']['width']}" height="{resource['assets']['preview']['height']}" loading="{loading}" decoding="async">
        </a>
        <a class="page-download" href="{escape(pdf_url, quote=True)}?download=1" download>Download {escape(label)}</a>
      </article>""")

    learning_items = "\n".join(f"          <li>{escape(item)}</li>" for item in resource["learningFocus"])
    guidance = ""
    if resource.get("adultGuidance"):
        guidance = f"""
      <section class="resource-support-card" aria-labelledby="adult-guidance-heading">
        <h2 id="adult-guidance-heading">For adults</h2>
        <p>{escape(resource['adultGuidance'])}</p>
      </section>"""
    related_markup = ""
    if related:
        related_items = "\n".join(
            f'        <li><a href="/{clean_resource_path(item)}"><strong>{escape(item["title"])}</strong><span>{escape(item["description"])}</span></a></li>'
            for item in related
        )
        related_markup = f"""
    <section class="resource-related-section" aria-labelledby="related-heading">
      <h2 id="related-heading">Related resources</h2>
      <ul class="resource-related-list">
{related_items}
      </ul>
    </section>"""

    page_gallery_class = "page-preview-gallery page-preview-gallery--large" if page_count > 8 else "page-preview-gallery"
    preview_intro = (
        f"Browse all {page_count} pages. Preview or download each activity separately."
        if page_count > 8
        else f"Preview and download each of the {page_count} worksheet pages."
        if page_count > 1
        else "Preview the worksheet before downloading."
    )

    structured = structured_data(resource, site, labels, indexes)
    html = f"""<!doctype html>
<html lang="{escape(effective_language(resource), quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/site-icon-192x192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <title>{escape(resource['seo']['title'])}</title>
  <meta name="description" content="{escape(resource['seo']['description'], quote=True)}">
  <link rel="canonical" href="{escape(canonical, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(resource['seo']['title'], quote=True)}">
  <meta property="og:description" content="{escape(resource['seo']['description'], quote=True)}">
  <meta property="og:url" content="{escape(canonical, quote=True)}">
  <meta property="og:image" content="{escape(social_image, quote=True)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(resource['seo']['title'], quote=True)}">
  <meta name="twitter:description" content="{escape(resource['seo']['description'], quote=True)}">
  <meta name="twitter:image" content="{escape(social_image, quote=True)}">
  <link rel="stylesheet" href="/style.css">
  <link rel="stylesheet" href="../../resource-pages.css">
  <script src="../../resource-pages.js" defer></script>
  <script type="application/ld+json">{_json_script(structured)}</script>
</head>
<body class="static-resource-page">
  <a class="resource-skip-link" href="#main-content">Skip to main content</a>
  <nav class="main-nav" aria-label="Primary navigation">
    <a class="logo" href="/index.html"><span class="logo-mark">L</span><span>Learning Made Simple</span></a>
    <button class="mobile-menu-toggle" type="button" aria-label="Open navigation menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <div class="nav-links">
      <a href="/index.html">Home</a>
      <div class="dropdown"><a href="/worksheets.html">Resources</a><div class="dropdown-menu"><a href="/worksheets.html">All Resources</a><a href="/math.html">Math</a><a href="/reading.html">Reading &amp; Language</a><a href="/communication.html">Communication &amp; Life Skills</a><a href="/science.html">Science &amp; Discovery</a><a href="/thinking-world.html">Thinking &amp; Our World</a></div></div>
      <div class="dropdown"><a href="/preschool.html">By Grade</a><div class="dropdown-menu"><a href="/preschool.html">Preschool</a><a href="/kindergarten.html">Kindergarten</a><a href="/grade-1.html">Grade 1</a><a href="/grade-2.html">Grade 2</a></div></div>
      <a href="/about.html">About</a>
      <a href="/contact.html">Contact</a>
    </div>
  </nav>
  <main id="main-content" class="resource-page-main">
  <nav class="resource-breadcrumb" aria-label="Breadcrumb">
    <ol>
      <li><a href="/">Home</a></li>
      <li><a href="/{escape(grade_href, quote=True)}">{escape(labels['grade'])}</a></li>
      <li><a href="/{escape(subject_href, quote=True)}">{escape(labels['subject'])}</a></li>
      <li><a href="/{escape(topic_href, quote=True)}">{escape(labels['topic'])}</a></li>
      <li aria-current="page">{escape(resource['title'])}</li>
    </ol>
  </nav>
    <article>
      <header class="resource-page-hero">
        <p class="eyebrow">{escape(labels['grade'])} &bull; {escape(labels['subject'])}</p>
        <h1>{escape(resource['title'])}</h1>
        <p class="resource-page-summary">{escape(resource['description'])}</p>
        <ul class="resource-context-tags" aria-label="Resource details">
          <li>{escape(labels['topic'])}</li>
          <li>{escape(', '.join(labels['skills']))}</li>
          <li>{page_count} {"page" if page_count == 1 else "pages"}</li>
        </ul>
        <a class="resource-primary-action" href="{escape(bundle_url, quote=True)}?download=1" download>{complete_download_label}</a>
      </header>
      <section class="resource-preview-section" aria-labelledby="pages-heading">
        <div class="resource-section-heading">
          <h2 id="pages-heading">Worksheet pages</h2>
          <p>{preview_intro}</p>
        </div>
        <div class="{page_gallery_class}" aria-label="Worksheet page previews">
{chr(10).join(preview_cards)}
        </div>
      </section>
      <div class="resource-support-grid">
        <section class="resource-support-card" aria-labelledby="learning-focus-heading">
          <h2 id="learning-focus-heading">Learning focus</h2>
          <ul>
{learning_items}
          </ul>
        </section>
        <section class="resource-support-card" aria-labelledby="resource-details-heading">
          <h2 id="resource-details-heading">Resource details</h2>
          <dl class="resource-details">
            <dt>Grade</dt><dd>{escape(labels['grade'])}</dd>
            <dt>Subject</dt><dd>{escape(labels['subject'])}</dd>
            <dt>Topic</dt><dd>{escape(labels['topic'])}</dd>
            <dt>Skills</dt><dd>{escape(', '.join(labels['skills']))}</dd>
            <dt>Pages</dt><dd>{page_count}</dd>
          </dl>
        </section>{guidance}
      </div>{related_markup}
    </article>
  </main>
  <footer>
    <div class="footer-content">
      <div class="footer-brand"><h3>Learning Made Simple</h3><p>Simple resources. Meaningful learning.</p></div>
      <div class="footer-links">
        <div><h4>Explore</h4><a href="/index.html">Home</a><a href="/worksheets.html">All Resources</a><a href="/about.html">About</a><a href="/contact.html">Contact</a></div>
        <div><h4>Information</h4><a href="/privacy.html">Privacy Policy</a><a href="/terms.html">Terms of Use</a><a href="/disclaimer.html">Disclaimer</a></div>
      </div>
    </div>
    <div class="footer-bottom"><p>&copy; 2026 Learning Made Simple. All rights reserved.</p></div>
  </footer>
</body>
</html>
"""
    return html, related_ids


def _safe_output_root(output_root: Path) -> Path:
    resolved = output_root.resolve()
    if resolved.name != "resource-pages-shadow":
        raise ValueError(f"Shadow output directory must be named resource-pages-shadow: {resolved}")
    return resolved


def generate(output_root: Path = SHADOW_ROOT) -> dict[str, Any]:
    resolved_root = _safe_output_root(output_root)
    if resolved_root.exists():
        shutil.rmtree(resolved_root)
    resolved_root.mkdir(parents=True)
    supporting_files = []
    for filename in ("resource-pages.css", "resource-pages.js"):
        source = TEMPLATE_ROOT / filename
        if not source.is_file():
            raise FileNotFoundError(f"Static resource page template is missing: {source}")
        destination = resolved_root / filename
        destination.write_bytes(source.read_bytes())
        supporting_files.append(filename)
    site, taxonomy, resources = load_site(), load_taxonomy(), load_resources()
    counts = validate_catalog(site, taxonomy, resources)
    published = sorted(
        (resource for resource in resources if is_public_page_eligible(resource)),
        key=lambda resource: resource["ordering"]["catalog"],
    )
    entries = []
    for resource in published:
        html, related_ids = render_page(resource, resources, site, taxonomy)
        relative_path = Path("resources") / resource["routing"]["slug"] / "index.html"
        destination = resolved_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html, encoding="utf-8", newline="\n")
        entries.append({
            "resourceId": resource["id"],
            "slug": resource["routing"]["slug"],
            "cleanPath": relative_path.as_posix(),
            "canonicalUrl": clean_resource_url(resource, site),
            "relatedResourceIds": related_ids,
            "sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
        })
    manifest = {
        "schemaVersion": 1,
        "generatorVersion": GENERATOR_VERSION,
        "cleanUrlPattern": "/resources/{slug}/",
        "publishedResourceCount": len(published),
        "retiredResourceCount": counts.get("retired", 0),
        "supportingFiles": supporting_files,
        "resources": entries,
    }
    _write_json(resolved_root / "manifest.json", manifest)
    review_ids = [
        "trace-numbers-1-20",
        "learn-my-letters-a-z",
        "phrases-i-can-use",
        "pre-writing-lines-strokes",
    ]
    by_id = {entry["resourceId"]: entry for entry in entries}
    _write_json(resolved_root / "review-report.json", {
        "schemaVersion": 1,
        "purpose": "Discoverability Phase 2 shadow review",
        "productionFilesChanged": False,
        "representativePages": [by_id[resource_id] for resource_id in review_ids],
    })
    return manifest


def _require(source: str, expected: str, resource_id: str, field: str) -> None:
    if expected not in source:
        raise StaticPageValidationError(f"{resource_id}: generated page is missing {field}")


def validate_output(output_root: Path = SHADOW_ROOT) -> dict[str, int]:
    resolved_root = _safe_output_root(output_root)
    site, taxonomy, resources = load_site(), load_taxonomy(), load_resources()
    validate_catalog(site, taxonomy, resources)
    indexes = taxonomy_indexes(taxonomy)
    published = sorted(
        (resource for resource in resources if is_public_page_eligible(resource)),
        key=lambda resource: resource["ordering"]["catalog"],
    )
    published_ids = {resource["id"] for resource in published}
    manifest = json.loads((resolved_root / "manifest.json").read_text(encoding="utf-8"))
    entries = manifest.get("resources")
    if not isinstance(entries, list) or len(entries) != len(published):
        raise StaticPageValidationError("Manifest resource count does not match published catalog")
    if manifest.get("publishedResourceCount") != len(published):
        raise StaticPageValidationError("Manifest published count is incorrect")
    if manifest.get("supportingFiles") != ["resource-pages.css", "resource-pages.js"]:
        raise StaticPageValidationError("Manifest supporting files are incorrect")
    for filename in manifest["supportingFiles"]:
        if not (resolved_root / filename).is_file():
            raise StaticPageValidationError(f"Shadow supporting file is missing: {filename}")
    clean_paths = [entry.get("cleanPath") for entry in entries]
    if len(clean_paths) != len(set(clean_paths)):
        raise StaticPageValidationError("Generated clean paths are not unique")
    if {entry.get("resourceId") for entry in entries} != published_ids:
        raise StaticPageValidationError("Manifest resource ids do not match published catalog")
    generated_pages = sorted((resolved_root / "resources").glob("*/index.html"))
    if len(generated_pages) != len(published):
        raise StaticPageValidationError("Generated page count does not match published catalog")

    by_id = {resource["id"]: resource for resource in resources}
    for entry in entries:
        resource = by_id[entry["resourceId"]]
        expected_clean_path = f"resources/{resource['routing']['slug']}/index.html"
        if entry.get("slug") != resource["routing"]["slug"] or entry.get("cleanPath") != expected_clean_path:
            raise StaticPageValidationError(
                f"{resource['id']}: manifest clean path does not match catalog routing"
            )
        path = resolved_root / entry["cleanPath"]
        source = path.read_text(encoding="utf-8")
        canonical = clean_resource_url(resource, site)
        labels = _labels(resource, indexes)
        if entry.get("canonicalUrl") != canonical:
            raise StaticPageValidationError(
                f"{resource['id']}: manifest canonical does not match catalog routing"
            )
        _require(source, f"<title>{escape(resource['seo']['title'])}</title>", resource["id"], "SEO title")
        _require(source, escape(resource["seo"]["description"], quote=True), resource["id"], "SEO description")
        _require(source, f'<link rel="canonical" href="{canonical}">', resource["id"], "canonical")
        _require(source, f'<meta property="og:url" content="{canonical}">', resource["id"], "Open Graph URL")
        _require(source, f'<meta property="og:title" content="{escape(resource["seo"]["title"], quote=True)}">', resource["id"], "Open Graph title")
        social_image = _absolute_url(site["assetOrigin"], default_social_image(resource))
        _require(source, f'<meta property="og:image" content="{social_image}">', resource["id"], "Open Graph image")
        _require(source, f"<h1>{escape(resource['title'])}</h1>", resource["id"], "H1")
        _require(source, escape(resource["description"]), resource["id"], "summary")
        for focus in resource["learningFocus"]:
            _require(source, escape(focus), resource["id"], "learning focus")
        for label in [labels["grade"], labels["subject"], labels["topic"], *labels["skills"]]:
            _require(source, escape(label), resource["id"], "taxonomy label")
        if source.count('class="resource-page-preview"') != len(resource["pages"]):
            raise StaticPageValidationError(
                f"{resource['id']}: generated preview count does not match catalog pages"
            )
        for index in range(len(resource["pages"])):
            number = index + 1
            label = page_label(resource, index)
            alt = default_preview_alt(resource, index)
            preview_path = f"{resource['assets']['previewDirectory']}/page-{number:02d}.png"
            pdf_path = f"{resource['assets']['pagePdfDirectory']}/page-{number:02d}.pdf"
            _require(source, escape(label), resource["id"], f"page {number} label")
            _require(source, escape(alt, quote=True), resource["id"], f"page {number} alt text")
            _require(source, _absolute_url(site["assetOrigin"], preview_path), resource["id"], f"page {number} preview")
            _require(source, _absolute_url(site["assetOrigin"], pdf_path), resource["id"], f"page {number} download")
        _require(source, _absolute_url(site["assetOrigin"], resource["assets"]["bundlePdf"]), resource["id"], "bundle download")
        structured = structured_data(resource, site, labels, indexes)
        _require(source, _json_script(structured), resource["id"], "structured data")
        expected_related = related_resource_ids(resource, resources, RELATED_RESOURCE_LIMIT)
        if entry.get("relatedResourceIds") != expected_related:
            raise StaticPageValidationError(
                f"{resource['id']}: related resources do not match catalog derivation"
            )
        if not set(entry["relatedResourceIds"]).issubset(published_ids):
            raise StaticPageValidationError(f"{resource['id']}: related resource is not published")
        expected_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
        if entry.get("sha256") != expected_hash:
            raise StaticPageValidationError(f"{resource['id']}: manifest hash does not match page")

    retired_slugs = {
        resource["routing"]["slug"] for resource in resources if resource["status"] == "retired"
    }
    if any((resolved_root / "resources" / slug).exists() for slug in retired_slugs):
        raise StaticPageValidationError("A retired resource received a static page")
    return {
        "validatedPageCount": len(generated_pages),
        "publishedResourceCount": len(published),
        "retiredResourceCount": len(retired_slugs),
    }
