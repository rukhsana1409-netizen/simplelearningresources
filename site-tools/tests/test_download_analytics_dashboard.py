import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "site-tools" / "generate_download_analytics_metadata.py"
SPEC = importlib.util.spec_from_file_location("generate_download_analytics_metadata", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(ROOT / "site-tools"))
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class DownloadAnalyticsDashboardTests(unittest.TestCase):
    def test_generated_metadata_matches_all_published_resources(self):
        metadata = MODULE.build_metadata()
        resources = [resource for resource in MODULE.load_resources() if resource["status"] == "published"]
        self.assertEqual(len(metadata), len(resources))
        self.assertNotIn("analytics-deployment-check", metadata)
        for resource in resources:
            self.assertEqual(metadata[resource["id"]]["title"], resource["title"])
            self.assertEqual(len(metadata[resource["id"]]["pages"]), len(resource["pages"]))

    def test_committed_metadata_is_idempotent(self):
        metadata = MODULE.build_metadata()
        expected = json.dumps(metadata, ensure_ascii=False, indent=2)
        committed = MODULE.OUTPUT.read_text(encoding="utf-8")
        self.assertEqual(
            committed,
            f"// Generated from catalog/resources. Do not edit.\nexport const RESOURCE_METADATA = Object.freeze({expected});\n",
        )
        public_payload = json.loads(MODULE.PUBLIC_OUTPUT.read_text(encoding="utf-8"))
        self.assertEqual(public_payload, MODULE.build_public_payload(metadata))

    def test_newly_published_resource_is_added_without_manual_metadata_edit(self):
        resources = MODULE.load_resources()
        new_resource = {
            "id": "future-published-resource",
            "title": "Future Published Resource",
            "status": "published",
            "ordering": {"catalog": 9999},
            "pages": [{"label": "First Activity"}, {"label": "Second Activity"}],
        }
        metadata = MODULE.build_metadata([*resources, new_resource])
        self.assertEqual(metadata["future-published-resource"], {
            "title": "Future Published Resource",
            "pages": ["First Activity", "Second Activity"],
        })
        public_payload = MODULE.build_public_payload(metadata)
        self.assertIn("future-published-resource", public_payload["resources"])
        self.assertEqual(public_payload["resourceCount"], len(metadata))

    def test_long_ago_historical_id_uses_current_catalog_label(self):
        metadata = MODULE.build_metadata()
        self.assertEqual(metadata["long-ago"]["title"], "Long Ago & Me")

    def test_production_runtime_generation_also_refreshes_dashboard_metadata(self):
        source = (ROOT / "site-tools" / "generate_production_runtime.py").read_text(encoding="utf-8")
        self.assertIn("analytics_resource_count = write_metadata()", source)
        self.assertIn("analytics_resource_count != resource_count", source)

    def test_dashboard_is_enabled_after_access_is_verified(self):
        config = (ROOT / "cloudflare" / "download-analytics" / "wrangler.toml").read_text(encoding="utf-8")
        self.assertIn('DASHBOARD_ENABLED = "true"', config)
        self.assertIn('binding = "ANALYTICS_SQL"', config)


if __name__ == "__main__":
    unittest.main()
