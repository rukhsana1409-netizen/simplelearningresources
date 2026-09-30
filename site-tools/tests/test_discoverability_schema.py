"""Focused tests for Discoverability Phase 1 catalog fields and derivations."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "site-tools"))

from catalog_lib import (  # noqa: E402
    CatalogValidationError,
    load_resources,
    load_site,
    load_taxonomy,
    validate_catalog,
)
from resource_discoverability import (  # noqa: E402
    default_preview_alt,
    default_social_image,
    effective_language,
    effective_resource_type,
    is_public_page_eligible,
    related_resource_ids,
)


class DiscoverabilitySchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = load_site()
        cls.taxonomy = load_taxonomy()
        cls.resources = load_resources()
        cls.by_id = {resource["id"]: resource for resource in cls.resources}

    def assert_invalid(self, resources, message):
        with self.assertRaisesRegex(CatalogValidationError, message):
            validate_catalog(self.site, self.taxonomy, resources)

    def test_all_published_resources_have_required_discoverability_fields(self):
        published = [resource for resource in self.resources if resource["status"] == "published"]
        self.assertEqual(len(published), 44)
        for resource in published:
            with self.subTest(resource=resource["id"]):
                self.assertEqual(resource["routing"]["slug"], resource["id"])
                self.assertIsInstance(resource["routing"]["aliases"], list)
                self.assertRegex(resource["publication"]["publishedAt"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertRegex(resource["publication"]["updatedAt"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertTrue(resource["description"].strip())
                self.assertTrue(resource["learningFocus"])
                self.assertTrue(resource["seo"]["title"].strip())
                self.assertTrue(resource["seo"]["description"].strip())

    def test_technical_defaults_are_derived_without_catalog_duplication(self):
        story = self.by_id["my-first-reading-stories"]
        counting = self.by_id["counting-objects-1-5"]
        self.assertEqual(effective_language(story), "en")
        self.assertEqual(effective_resource_type(story), "worksheet-pack")
        self.assertEqual(default_social_image(story), f"{story['assets']['previewDirectory']}/page-01.png")
        self.assertEqual(
            default_preview_alt(story, 0),
            "Preview of The Red Cat from My First Reading Stories",
        )
        self.assertEqual(
            default_preview_alt(counting, 0),
            "Preview of Page 1 from Counting Objects 1-5",
        )

    def test_related_resources_are_deterministic_and_allow_a_curated_override(self):
        story = self.by_id["my-first-reading-stories"]
        related = related_resource_ids(story, self.resources, limit=3)
        self.assertNotIn(story["id"], related)
        self.assertEqual(related, related_resource_ids(story, list(reversed(self.resources)), limit=3))
        overridden = copy.deepcopy(story)
        overridden["relatedResources"] = ["beginning-sounds", "parts-of-a-book"]
        self.assertEqual(
            related_resource_ids(overridden, self.resources, limit=3),
            ["beginning-sounds", "parts-of-a-book"],
        )

    def test_retired_resources_never_qualify_for_public_pages(self):
        self.assertFalse(is_public_page_eligible(self.by_id["story-comprehension"]))
        self.assertTrue(is_public_page_eligible(self.by_id["my-first-reading-stories"]))

    def test_missing_invalid_and_duplicate_slugs_fail(self):
        missing = copy.deepcopy(self.resources)
        del missing[0]["routing"]
        self.assert_invalid(missing, "routing")

        changed = copy.deepcopy(self.resources)
        published = next(resource for resource in changed if resource["status"] == "published")
        published["routing"]["slug"] = "changed-published-slug"
        self.assert_invalid(changed, "immutable")

        duplicate = copy.deepcopy(self.resources)
        published = [resource for resource in duplicate if resource["status"] == "published"]
        published[1]["routing"]["aliases"] = [published[0]["routing"]["slug"]]
        self.assert_invalid(duplicate, "Duplicate routing slugs or aliases")

        reserved = copy.deepcopy(self.resources)
        published = next(resource for resource in reserved if resource["status"] == "published")
        published["routing"]["aliases"] = ["search"]
        self.assert_invalid(reserved, "reserved route")

    def test_invalid_dates_and_missing_authored_fields_fail(self):
        invalid_date = copy.deepcopy(self.resources)
        published = next(resource for resource in invalid_date if resource["status"] == "published")
        published["publication"]["updatedAt"] = "2026-02-30"
        self.assert_invalid(invalid_date, "publication.updatedAt")

        reversed_dates = copy.deepcopy(self.resources)
        published = next(resource for resource in reversed_dates if resource["status"] == "published")
        published["publication"]["publishedAt"] = "2026-09-30"
        published["publication"]["updatedAt"] = "2026-09-29"
        self.assert_invalid(reversed_dates, "before publication")

        future_date = copy.deepcopy(self.resources)
        published = next(resource for resource in future_date if resource["status"] == "published")
        published["publication"]["publishedAt"] = "2999-01-01"
        published["publication"]["updatedAt"] = "2999-01-01"
        self.assert_invalid(future_date, "future")

        missing_focus = copy.deepcopy(self.resources)
        published = next(resource for resource in missing_focus if resource["status"] == "published")
        published["learningFocus"] = []
        self.assert_invalid(missing_focus, "learningFocus")

        missing_seo = copy.deepcopy(self.resources)
        published = next(resource for resource in missing_seo if resource["status"] == "published")
        published["seo"]["description"] = ""
        self.assert_invalid(missing_seo, "seo.description")


if __name__ == "__main__":
    unittest.main()
