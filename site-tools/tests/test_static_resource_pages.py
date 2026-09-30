"""Focused tests for Discoverability Phase 2 shadow resource pages."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "site-tools"))

from catalog_lib import load_resources, load_site, load_taxonomy  # noqa: E402
from static_resource_pages import generate, validate_output  # noqa: E402


class StaticResourcePageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary_directory = tempfile.TemporaryDirectory()
        cls.output_root = Path(cls.temporary_directory.name) / "resource-pages-shadow"
        cls.production_snapshot = {
            path.relative_to(REPOSITORY_ROOT).as_posix(): path.read_bytes()
            for path in (REPOSITORY_ROOT / "resources").rglob("*") if path.is_file()
        }
        cls.result = generate(cls.output_root)
        cls.validation = validate_output(cls.output_root)
        cls.resources = load_resources()

    @classmethod
    def tearDownClass(cls):
        cls.temporary_directory.cleanup()

    def page_source(self, resource_id: str) -> str:
        return (
            self.output_root / "resources" / resource_id / "index.html"
        ).read_text(encoding="utf-8")

    def test_generates_exactly_one_page_per_published_resource(self):
        published = [resource for resource in self.resources if resource["status"] == "published"]
        retired = [resource for resource in self.resources if resource["status"] == "retired"]
        pages = list((self.output_root / "resources").glob("*/index.html"))
        self.assertEqual(len(published), 45)
        self.assertEqual(len(pages), 45)
        self.assertEqual(self.result["publishedResourceCount"], 45)
        self.assertEqual(self.validation["validatedPageCount"], 45)
        for resource in retired:
            self.assertFalse((self.output_root / "resources" / resource["routing"]["slug"]).exists())

    def test_manifest_maps_unique_clean_urls_to_catalog_resources(self):
        manifest = json.loads((self.output_root / "manifest.json").read_text(encoding="utf-8"))
        entries = manifest["resources"]
        self.assertEqual(len({entry["resourceId"] for entry in entries}), 45)
        self.assertEqual(len({entry["cleanPath"] for entry in entries}), 45)
        self.assertTrue(all(entry["cleanPath"].startswith("resources/") for entry in entries))
        self.assertTrue(all(entry["cleanPath"].endswith("/index.html") for entry in entries))

    def test_page_contains_semantic_content_metadata_and_accessible_assets(self):
        source = self.page_source("phrases-i-can-use")
        self.assertIn('<main id="main-content" class="resource-page-main">', source)
        self.assertIn("<h1>Phrases I Can Use</h1>", source)
        self.assertIn("Use simple phrases to join activities", source)
        self.assertIn("At the Playground", source)
        self.assertIn("Download At the Playground", source)
        self.assertIn("Preview of At the Playground from Phrases I Can Use", source)
        self.assertIn("https://simplelearningresources.com/resources/phrases-i-can-use/", source)
        self.assertIn('type="application/ld+json"', source)
        self.assertIn('property="og:image"', source)
        self.assertIn('<link rel="stylesheet" href="/style.css">', source)
        self.assertIn('<link rel="stylesheet" href="../../resource-pages.css">', source)
        self.assertIn('<script src="../../resource-pages.js" defer></script>', source)

    def test_visual_hierarchy_places_download_and_previews_before_supporting_copy(self):
        source = self.page_source("phrases-i-can-use")
        positions = [
            source.index('class="resource-primary-action"'),
            source.index('id="pages-heading"'),
            source.index('id="learning-focus-heading"'),
            source.index('id="related-heading"'),
        ]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Download Complete Pack", source)
        self.assertIn('class="main-nav"', source)
        self.assertIn('class="mobile-menu-toggle"', source)
        self.assertIn('class="footer-content"', source)

    def test_one_page_and_multi_page_resources_use_catalog_page_contracts(self):
        one_page = self.page_source("trace-numbers-1-20")
        multi_page = self.page_source("learn-my-letters-a-z")
        self.assertEqual(one_page.count('class="resource-page-preview"'), 1)
        self.assertEqual(multi_page.count('class="resource-page-preview"'), 26)
        self.assertIn("Download Worksheet", one_page)
        self.assertIn("Download Complete Pack", multi_page)
        self.assertIn("Download Letter Z", multi_page)
        self.assertIn("page-preview-gallery--large", multi_page)

    def test_shadow_styles_include_responsive_preview_and_navigation_rules(self):
        css = (self.output_root / "resource-pages.css").read_text(encoding="utf-8")
        javascript = (self.output_root / "resource-pages.js").read_text(encoding="utf-8")
        self.assertIn(".resource-page-preview img", css)
        self.assertIn("max-width:100%", css)
        self.assertIn("@media (max-width:768px)", css)
        self.assertIn(".resource-primary-action", css)
        self.assertIn("mobile-menu-open", javascript)

    def test_related_resources_are_clean_links_to_published_resources(self):
        manifest = json.loads((self.output_root / "manifest.json").read_text(encoding="utf-8"))
        published_ids = {entry["resourceId"] for entry in manifest["resources"]}
        for entry in manifest["resources"]:
            self.assertNotIn(entry["resourceId"], entry["relatedResourceIds"])
            self.assertTrue(set(entry["relatedResourceIds"]).issubset(published_ids))
            source = (self.output_root / entry["cleanPath"]).read_text(encoding="utf-8")
            for related_id in entry["relatedResourceIds"]:
                self.assertIn(f'/resources/{related_id}/', source)

    def test_generation_is_deterministic_and_idempotent(self):
        first = {
            path.relative_to(self.output_root).as_posix(): path.read_bytes()
            for path in self.output_root.rglob("*") if path.is_file()
        }
        generate(self.output_root)
        second = {
            path.relative_to(self.output_root).as_posix(): path.read_bytes()
            for path in self.output_root.rglob("*") if path.is_file()
        }
        self.assertEqual(first, second)

    def test_shadow_generation_does_not_write_production_files(self):
        site = load_site()
        taxonomy = load_taxonomy()
        self.assertEqual(site["legacyResourcePath"], "resource-preview.html")
        self.assertEqual(len(taxonomy["topics"]), 148)
        current_snapshot = {
            path.relative_to(REPOSITORY_ROOT).as_posix(): path.read_bytes()
            for path in (REPOSITORY_ROOT / "resources").rglob("*") if path.is_file()
        }
        self.assertEqual(current_snapshot, self.production_snapshot)


if __name__ == "__main__":
    unittest.main()
