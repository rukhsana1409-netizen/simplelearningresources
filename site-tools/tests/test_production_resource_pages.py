"""Focused production clean-resource migration tests."""

from __future__ import annotations

import re
import sys
import unittest
import urllib.request
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "site-tools"))

from catalog_lib import extract_live_registry, load_resources  # noqa: E402
from validate_production_resource_pages import validate  # noqa: E402


class ProductionResourcePageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resources = [resource for resource in load_resources() if resource["status"] == "published"]
        cls.runtime = extract_live_registry(REPOSITORY_ROOT / "directory.js")

    def test_all_published_resources_have_clean_production_pages(self):
        result = validate()
        self.assertEqual(result["validatedPageCount"], 65)
        self.assertEqual(result["retiredExcludedCount"], 1)

    def test_runtime_uses_clean_urls_and_retains_legacy_urls(self):
        self.assertEqual(len(self.runtime), 65)
        for resource in self.runtime:
            self.assertEqual(resource["previewHref"], f"resources/{resource['slug']}/")
            self.assertEqual(
                resource["legacyPreviewHref"],
                f"resource-preview.html?resource={resource['id']}",
            )

    def test_legacy_preview_canonicalizes_to_clean_runtime_url(self):
        source = (REPOSITORY_ROOT / "resource-preview.html").read_text(encoding="utf-8")
        self.assertIn("window.setIndexableCanonicalUrl(resource.previewHref);", source)
        self.assertNotIn("location.replace(resource.previewHref)", source)

    def test_more_fewer_skill_navigation_policy_is_preserved(self):
        source = (REPOSITORY_ROOT / "directory.js").read_text(encoding="utf-8")
        self.assertIn('"href":"skill-directory.html?skill=more-fewer-same"', source)

    def test_active_static_pages_do_not_link_to_legacy_resource_previews(self):
        for path in REPOSITORY_ROOT.glob("*.html"):
            if path.name == "resource-preview.html":
                continue
            with self.subTest(path=path.name):
                self.assertNotIn(
                    "resource-preview.html?resource=",
                    path.read_text(encoding="utf-8"),
                )

    def test_representative_clean_and_legacy_urls_serve(self):
        urls = (
            "resources/trace-numbers-1-20/",
            "resources/more-fewer-same-1-10/",
            "resources/phrases-i-can-use/",
            "resources/learn-my-letters-a-z/",
            "resource-preview.html?resource=more-fewer-same-1-10",
        )
        for relative_url in urls:
            with self.subTest(url=relative_url):
                with urllib.request.urlopen(f"http://localhost:8000/{relative_url}", timeout=5) as response:
                    self.assertEqual(response.status, 200)

    def test_active_loader_cache_version_is_consistent(self):
        references = []
        for path in REPOSITORY_ROOT.glob("*.html"):
            references.extend(re.findall(r'directory\.js\?v=\d+', path.read_text(encoding="utf-8")))
        references.extend(
            re.findall(r'directory\.js\?v=\d+', (REPOSITORY_ROOT / "nav.js").read_text(encoding="utf-8"))
        )
        self.assertEqual(len(references), 7)
        self.assertEqual(set(references), {"directory.js?v=25"})


if __name__ == "__main__":
    unittest.main()
