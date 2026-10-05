"""Focused compatibility tests for the Step 3 generated runtime catalog."""

from __future__ import annotations

import sys
import unittest
import urllib.request
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "site-tools"))

from catalog_lib import extract_live_registry, load_resources, load_site, load_taxonomy, taxonomy_indexes  # noqa: E402
from shadow_catalog import published_resources, runtime_resource, topic_records  # noqa: E402


class Step3RuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory_source = (REPOSITORY_ROOT / "directory.js").read_text(encoding="utf-8")
        cls.preview_source = (REPOSITORY_ROOT / "resource-preview.html").read_text(encoding="utf-8")
        cls.site = load_site()
        cls.taxonomy = load_taxonomy()
        cls.catalog = published_resources(load_resources())
        cls.indexes = taxonomy_indexes(cls.taxonomy)
        cls.runtime = [runtime_resource(resource, cls.indexes, cls.site) for resource in cls.catalog]

    def test_synchronous_public_api_and_generated_block_are_present(self):
        self.assertIn("BEGIN GENERATED CATALOG COMPATIBILITY DATA", self.directory_source)
        for statement in (
            "window.worksheetResources=worksheetResources;",
            "window.worksheetResourcesById=worksheetResourcesById;",
            "window.searchWorksheetResources=searchWorksheetResources;",
            "window.resolveWorksheetAssetUrl=resolveWorksheetAssetUrl;",
        ):
            self.assertIn(statement, self.directory_source)
        self.assertEqual(len(extract_live_registry(REPOSITORY_ROOT / "directory.js")), 64)

    def test_search_data_and_matching_behavior(self):
        def search(query="", **filters):
            query = query.strip().lower()
            return [
                resource for resource in self.runtime
                if all(not value or resource[field].lower() == value.strip().lower() for field, value in filters.items())
                and (not query or any(query in str(value).lower() for value in (
                    resource["title"], resource["grade"], resource["subject"],
                    resource["topic"], resource["skill"], *resource["keywords"],
                )))
            ]

        self.assertEqual([item["id"] for item in search("rocket")], ["connect-the-dots-1-20"])
        self.assertEqual([item["id"] for item in search("asking for help")], ["i-can-ask-for-help"])
        self.assertEqual([item["id"] for item in search("zigzags")], ["pre-writing-lines-strokes"])
        self.assertEqual([item["id"] for item in search("playground phrases")], ["phrases-i-can-use"])
        alphabet = search(grade="Preschool", subject="Reading & Language", topic="Alphabet")
        self.assertEqual([item["id"] for item in alphabet], [
            "learn-my-letters-a-z", "trace-my-letters-a-z",
            "match-big-little-letters-a-z", "abc-order-missing-letters",
        ])

    def test_singleton_and_multi_resource_topic_routes(self):
        topics = {
            (item["grade"], item["subject"], item["topic"]): item
            for item in topic_records(self.catalog, self.taxonomy, self.indexes, self.site)
        }
        singleton = topics[("Preschool", "Communication & Life Skills", "WH Questions")]
        self.assertEqual(singleton["resourceCount"], 1)
        self.assertEqual(singleton["linkHref"], "resources/wh-questions/")
        multi = topics[("Preschool", "Reading & Language", "Alphabet")]
        self.assertEqual(multi["resourceCount"], 4)
        self.assertEqual(
            multi["linkHref"],
            "topic.html?grade=Preschool&subject=Reading%20%26%20Language&topic=Alphabet",
        )
        early_writing = topics[("Preschool", "Reading & Language", "Early Writing")]
        self.assertEqual(early_writing["resourceCount"], 1)
        self.assertEqual(
            early_writing["linkHref"],
            "resources/pre-writing-lines-strokes/",
        )
        conversation = topics[("Preschool", "Communication & Life Skills", "Conversation & Play")]
        self.assertEqual(conversation["resourceCount"], 1)
        self.assertEqual(
            conversation["linkHref"],
            "resources/phrases-i-can-use/",
        )

    def test_page_labels_and_preview_download_contract(self):
        resources = {resource["id"]: resource for resource in self.runtime}
        self.assertEqual(resources["wh-questions"]["pageLabels"][0], "Learn: the WH Words")
        self.assertEqual(resources["my-first-reading-stories"]["pageLabels"][-1], "Ben's Lost Shoe")
        self.assertEqual(resources["pre-writing-lines-strokes"]["pageLabels"], [
            "Straight Lines", "Zigzags & Steps", "Curves & Waves", "Twisty Paths & Loops",
        ])
        self.assertEqual(resources["phrases-i-can-use"]["pageLabels"], [
            "At the Playground", "In the Classroom", "Playing With a Friend", "I Can Speak Up",
        ])
        story = resources["my-first-reading-stories"]
        self.assertEqual(story["previewHref"], "resources/my-first-reading-stories/")
        self.assertEqual(story["pages"][0]["pdfUrl"], "https://assets.simplelearningresources.com/worksheets/preschool/reading/my-first-reading-stories/my-first-reading-stories/page-01.pdf")
        self.assertIn('downloadLink.href = `${page.pdfUrl}?download=1`;', self.preview_source)
        self.assertIn('document.getElementById("download-complete").href = `${resource.pdfUrl}?download=1`;', self.preview_source)

    def test_representative_pages_serve_with_clean_and_legacy_urls(self):
        urls = (
            "math.html", "reading.html", "communication.html", "worksheets.html",
            "topic.html?grade=Preschool&subject=Reading%20%26%20Language&topic=Alphabet",
            "resources/wh-questions/",
            "resources/my-first-reading-stories/",
            "resources/preschool-patterns/",
            "resource-preview.html?resource=wh-questions",
        )
        for relative_url in urls:
            with self.subTest(url=relative_url):
                with urllib.request.urlopen(f"http://localhost:8000/{relative_url}", timeout=5) as response:
                    self.assertEqual(response.status, 200)
                    source = response.read().decode("utf-8")
                    if relative_url.startswith("resources/"):
                        self.assertIn("resource-pages.js", source)
                        self.assertIn('class="resource-page-main"', source)
                    else:
                        self.assertTrue("nav.js" in source or "directory.js" in source)


if __name__ == "__main__":
    unittest.main()
