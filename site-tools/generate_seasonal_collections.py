"""Generate static seasonal collection pages from the authoritative catalog."""

from __future__ import annotations

from html import escape
from pathlib import Path

from catalog_lib import (
    REPOSITORY_ROOT,
    load_collections,
    load_resources,
    load_site,
    load_taxonomy,
    validate_catalog,
)
from resource_discoverability import resource_page_href
from shadow_catalog import published_resources


CLOUDFLARE_BEACON = (
    '<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
    'data-cf-beacon=\'{"token":"a6fe9e891acb4cffadbe27263f7ec4bd"}\'></script>'
)


def render_collection_page(collection: dict, resources: list[dict], site: dict) -> str:
    resources_by_id = {resource["id"]: resource for resource in resources}
    group_markup = []
    for group in collection["groups"]:
        members = [resources_by_id[resource_id] for resource_id in group["resources"]]
        if not members:
            continue
        links = "\n".join(
            f'                    <li><a href="{escape(resource_page_href(resource), quote=True)}">{escape(resource["title"])}</a></li>'
            for resource in members
        )
        group_markup.append(f"""            <div class="directory-section">
                <h2>{escape(group['label'])}</h2>
                <ul>
{links}
                </ul>
            </div>""")
    if not group_markup:
        raise ValueError(f"Collection {collection['id']} has no published resource groups")
    canonical = f"{site['canonicalOrigin'].rstrip('/')}/{collection['path']}"
    groups = "\n".join(group_markup)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-adsense-account" content="ca-pub-7543692368591799">
    <link rel="icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="192x192" href="/site-icon-192x192.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="canonical" href="{escape(canonical, quote=True)}">
    <meta name="description" content="{escape(collection['description'], quote=True)}">
    <link rel="stylesheet" href="style.css">
    <script src="nav.js" defer></script>
    <title>{escape(collection['label'])} | Learning Made Simple</title>
</head>
<body>
<nav class="main-nav">
    <div class="logo"><img class="logo-mark" src="/site-icon-source.png" alt="" width="34" height="34"><span>Learning Made Simple</span></div>
    <div class="nav-links">
        <a href="index.html">Home</a>
        <div class="dropdown"><a href="worksheets.html">Resources</a><div class="dropdown-menu"><a href="worksheets.html">All Resources</a><a href="math.html">Math</a><a href="reading.html">Reading &amp; Language</a><a href="communication.html">Communication &amp; Life Skills</a><a href="science.html">Science &amp; Discovery</a><a href="thinking-world.html">Thinking &amp; Our World</a><a href="social-studies.html">Social Studies</a><a href="seasonal.html">Seasonal &amp; Holidays</a></div></div>
        <div class="dropdown"><a href="preschool.html">By Grade</a><div class="dropdown-menu"><a href="preschool.html">Preschool</a><a href="kindergarten.html">Kindergarten</a><a href="grade-1.html">Grade 1</a><a href="grade-2.html">Grade 2</a></div></div>
        <a href="about.html">About</a><a href="contact.html">Contact</a>
    </div>
</nav>
<section class="library">
    <div class="library-header"><h1>{escape(collection['label'])}</h1></div>
    <div class="directory-grid subject-directory">
{groups}
    </div>
</section>
<footer><div class="footer-content"><div class="footer-brand"><h3>Learning Made Simple</h3><p>Simple resources. Meaningful learning.</p></div><div class="footer-links"><div><h4>Explore</h4><a href="index.html">Home</a><a href="worksheets.html">All Resources</a><a href="about.html">About</a><a href="contact.html">Contact</a></div><div><h4>Information</h4><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Use</a><a href="disclaimer.html">Disclaimer</a></div></div></div><div class="footer-bottom"><p>&copy; 2026 Learning Made Simple. All rights reserved.</p></div></footer>
<!-- Cloudflare Web Analytics -->
{CLOUDFLARE_BEACON}
<!-- End Cloudflare Web Analytics -->
</body>
</html>
"""


def generate() -> int:
    site = load_site()
    taxonomy = load_taxonomy()
    resources = load_resources()
    validate_catalog(site, taxonomy, resources)
    published = published_resources(resources)
    collections = load_collections()["collections"]
    for collection in collections:
        output = REPOSITORY_ROOT / collection["path"]
        output.write_text(render_collection_page(collection, published, site), encoding="utf-8", newline="\n")
    return len(collections)


if __name__ == "__main__":
    print(f"GENERATED collection pages={generate()}")
