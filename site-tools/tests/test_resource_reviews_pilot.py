"""Focused tests for the opt-in worksheet review pilot."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "site-tools"))

from generate_production_resource_pages import load_review_pilot_config  # noqa: E402
from static_resource_pages import generate, validate_output  # noqa: E402


PILOT_ID = "adding-tens-and-ones"
API_ORIGIN = "https://lms-resource-reviews.rukhsana1409.workers.dev"
TEST_SITE_KEY = "1x00000000000000000000AA"


class ResourceReviewPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary_directory = tempfile.TemporaryDirectory()
        cls.output_root = Path(cls.temporary_directory.name) / "resource-pages-shadow"
        cls.manifest = generate(
            cls.output_root,
            review_resource_ids=frozenset({PILOT_ID}),
            review_api_origin=API_ORIGIN,
            turnstile_site_key=TEST_SITE_KEY,
        )
        cls.validation = validate_output(cls.output_root)
        cls.pilot = (cls.output_root / "resources" / PILOT_ID / "index.html").read_text(encoding="utf-8")
        cls.control = (cls.output_root / "resources" / "counting-to-120" / "index.html").read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.temporary_directory.cleanup()

    def test_only_explicit_pilot_receives_shared_component(self):
        self.assertEqual(self.manifest["reviewPilotResourceIds"], [PILOT_ID])
        self.assertIn('class="resource-reviews"', self.pilot)
        self.assertIn(f'data-review-resource-id="{PILOT_ID}"', self.pilot)
        self.assertIn(f'data-review-api-origin="{API_ORIGIN}"', self.pilot)
        self.assertIn(f'data-turnstile-sitekey="{TEST_SITE_KEY}"', self.pilot)
        self.assertNotIn('class="resource-reviews"', self.control)
        self.assertNotIn("resource-reviews.js", self.control)

    def test_production_pilot_config_is_single_resource_and_enabled(self):
        config = load_review_pilot_config()
        self.assertTrue(config["enabled"])
        self.assertEqual(config["resourceIds"], [PILOT_ID])
        self.assertEqual(config["apiOrigin"], API_ORIGIN)
        self.assertEqual(
            config["turnstileSiteKey"],
            "0x4AAAAAAF6VtzPnQmHV0vy3",
        )

    def test_enabled_production_pilot_requires_turnstile_sitekey(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "pilot-config.json"
            config = {
                "schemaVersion": 1,
                "enabled": True,
                "resourceIds": [PILOT_ID],
                "apiOrigin": API_ORIGIN,
                "turnstileSiteKey": "",
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "requires a Turnstile sitekey"):
                load_review_pilot_config(config_path)
            config["turnstileSiteKey"] = TEST_SITE_KEY
            config_path.write_text(json.dumps(config), encoding="utf-8")
            self.assertTrue(load_review_pilot_config(config_path)["enabled"])

    def test_nonpilot_pages_are_byte_identical_when_pilot_is_generated(self):
        with tempfile.TemporaryDirectory() as directory:
            baseline_root = Path(directory) / "baseline" / "resource-pages-shadow"
            generate(baseline_root)
            for pilot_path in (self.output_root / "resources").glob("*/index.html"):
                if pilot_path.parent.name == "adding-tens-and-ones":
                    continue
                relative = pilot_path.relative_to(self.output_root)
                self.assertEqual(pilot_path.read_bytes(), (baseline_root / relative).read_bytes(), relative.as_posix())

    def test_component_is_below_previews_and_before_supporting_content(self):
        positions = [
            self.pilot.index('id="pages-heading"'),
            self.pilot.index('id="resource-reviews-heading"'),
            self.pilot.index('id="learning-focus-heading"'),
        ]
        self.assertEqual(positions, sorted(positions))

    def test_accessible_form_contract_and_limits_are_present(self):
        self.assertIn('<fieldset class="review-stars">', self.pilot)
        self.assertEqual(self.pilot.count('type="radio" name="rating"'), 5)
        self.assertIn('maxlength="50"', self.pilot)
        self.assertIn('maxlength="500"', self.pilot)
        self.assertIn('aria-live="polite"', self.pilot)
        self.assertIn("For adults: use a first name or nickname only", self.pilot)
        self.assertIn("Your rating will be reviewed before it appears publicly", self.pilot)

    def test_existing_previews_downloads_and_analytics_remain_present(self):
        self.assertEqual(self.pilot.count('class="resource-page-preview"'), 7)
        self.assertIn("Download Complete Pack", self.pilot)
        self.assertIn('<script src="../../download-analytics.js" defer></script>', self.pilot)
        self.assertIn('<script src="../../resource-reviews.js" defer></script>', self.pilot)
        self.assertEqual(self.validation["validatedPageCount"], self.manifest["publishedResourceCount"])

    def test_shared_client_is_safe_and_uses_public_api_contract(self):
        script = (self.output_root / "resource-reviews.js").read_text(encoding="utf-8")
        self.assertIn("IntersectionObserver", script)
        self.assertIn('slice(0, 10)', script)
        self.assertIn('ratingCount) || data.ratingCount <= 0', script)
        self.assertIn('crypto.randomUUID()', script)
        self.assertIn('turnstile.reset(widgetId)', script)
        self.assertIn('retry: "never"', script)
        self.assertIn('"refresh-expired": "manual"', script)
        self.assertIn('"refresh-timeout": "manual"', script)
        self.assertIn('Verification is ready. Try Submit again.', script)
        self.assertNotIn('finally {\n                resetTurnstile();', script)
        self.assertIn("void ensureTurnstile();", script)
        self.assertNotIn('form.addEventListener("focusin", ensureTurnstile', script)
        self.assertIn('/v1/resources/', script)
        self.assertIn('Thank you. Your rating was submitted for approval.', script)
        self.assertNotIn("innerHTML", script)
        self.assertNotIn("Be the first", script)
        css = (self.output_root / "resource-pages.css").read_text(encoding="utf-8")
        self.assertIn(".review-approved-summary[hidden],.review-list[hidden]", css)
        self.assertIn("align-content:start", css)
        self.assertIn(".review-form-grid > label > span", css)
        self.assertIn(".review-star-options label:has(~ label input:checked)", css)
        self.assertIn("@media (max-width:520px)", css)
        self.assertIn(".review-form-grid { grid-template-columns:1fr; }", css)
        self.assertIn(".review-submit { width:100%; }", css)

    def test_submit_copy_is_concise_and_moderation_message_remains(self):
        self.assertIn('<button class="review-submit" type="submit">Submit</button>', self.pilot)
        self.assertNotIn("Submit for approval", self.pilot)
        self.assertIn("Your rating will be reviewed before it appears publicly", self.pilot)

    def test_privacy_policy_describes_moderation_security_and_retention(self):
        privacy = (REPOSITORY_ROOT / "privacy.html").read_text(encoding="utf-8")
        self.assertIn("<h2>Worksheet Ratings and Reviews</h2>", privacy)
        self.assertIn("Every submission is reviewed before it appears publicly", privacy)
        self.assertIn("do not affect the public average", privacy)
        self.assertIn("Cloudflare Turnstile and limited request-rate", privacy)
        self.assertIn(
            "does not intentionally\n            store IP addresses, email addresses, or visitor identifiers",
            privacy,
        )
        self.assertIn("automatically deleted after 90 days", privacy)
        self.assertIn("hello@simplelearningresources.com", privacy)

    def test_pilot_configuration_is_required_and_validated(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "resource-pages-shadow"
            with self.assertRaisesRegex(ValueError, "API origin and Turnstile"):
                generate(root, review_resource_ids=frozenset({PILOT_ID}))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "resource-pages-shadow"
            with self.assertRaisesRegex(ValueError, "not published"):
                generate(
                    root,
                    review_resource_ids=frozenset({"not-a-resource"}),
                    review_api_origin=API_ORIGIN,
                    turnstile_site_key=TEST_SITE_KEY,
                )


if __name__ == "__main__":
    unittest.main()
