import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "site-tools"))
SPEC = importlib.util.spec_from_file_location("report_download_analytics", ROOT / "site-tools" / "report_download_analytics.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class DownloadAnalyticsReportTests(unittest.TestCase):
    def test_query_uses_cloudflare_interval_literal_syntax(self):
        source = (ROOT / "site-tools" / "report_download_analytics.py").read_text(encoding="utf-8")
        self.assertIn("INTERVAL '{days}' DAY", source)

    def test_builds_resource_and_page_totals(self):
        resources = [{
            "id": "sample-resource",
            "title": "Sample Resource",
            "status": "published",
            "ordering": {"catalog": 1},
            "pages": [{"label": "First"}, {"label": "Second"}],
        }]
        rows = [
            {"resource_id": "sample-resource", "download_type": "pack", "page_number": 0, "clicks": 4},
            {"resource_id": "sample-resource", "download_type": "page", "page_number": 1, "clicks": 3},
            {"resource_id": "sample-resource", "download_type": "page", "page_number": 2, "clicks": 2},
        ]
        summary, pages = MODULE.build_reports(rows, resources)
        self.assertEqual(summary, [{
            "resource_id": "sample-resource",
            "resource_name": "Sample Resource",
            "full_pack_clicks": 4,
            "individual_page_clicks": 5,
            "total_clicks": 9,
        }])
        self.assertEqual([page["clicks"] for page in pages], [3, 2])
        self.assertEqual([page["page_name"] for page in pages], ["First", "Second"])

    def test_ignores_unknown_resources_and_invalid_page_numbers(self):
        resources = [{
            "id": "known",
            "title": "Known",
            "status": "published",
            "ordering": {"catalog": 1},
            "pages": [{"label": "Only"}],
        }]
        rows = [
            {"resource_id": "unknown", "download_type": "pack", "page_number": 0, "clicks": 10},
            {"resource_id": "known", "download_type": "page", "page_number": 2, "clicks": 10},
        ]
        summary, pages = MODULE.build_reports(rows, resources)
        self.assertEqual(summary[0]["total_clicks"], 0)
        self.assertEqual(pages[0]["clicks"], 0)

    def test_controlled_deployment_events_are_reported_separately(self):
        rows = [
            {"resource_id": "analytics-deployment-check", "download_type": "pack", "page_number": 0, "clicks": 1},
            {"resource_id": "published-resource", "download_type": "pack", "page_number": 0, "clicks": 8},
        ]
        self.assertEqual(MODULE.build_validation_report(rows), [{
            "resource_id": "analytics-deployment-check",
            "event_class": "controlled_deployment_test",
            "clicks": 1,
            "included_in_worksheet_totals": "no",
        }])


if __name__ == "__main__":
    unittest.main()
