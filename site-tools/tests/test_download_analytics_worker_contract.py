import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class DownloadAnalyticsWorkerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.worker = (ROOT / "cloudflare" / "download-analytics" / "src" / "worker.mjs").read_text(encoding="utf-8")
        cls.config = (ROOT / "cloudflare" / "download-analytics" / "wrangler.toml").read_text(encoding="utf-8")

    def test_worker_accepts_only_the_production_origin_and_expected_event_fields(self):
        self.assertIn('const ALLOWED_ORIGIN = "https://simplelearningresources.com";', self.worker)
        self.assertIn('["version", "resourceId", "downloadType", "pageNumber"]', self.worker)
        self.assertIn('const MAX_BODY_BYTES = 1024;', self.worker)
        self.assertIn('url.pathname !== "/download"', self.worker)

    def test_worker_does_not_read_or_store_visitor_identifiers(self):
        lowered = self.worker.lower()
        for forbidden in ("cf-connecting-ip", "user-agent", "cookie", "referer", "visitorid"):
            self.assertNotIn(forbidden, lowered)
        self.assertIn('indexes: [analyticsEvent.resourceId]', self.worker)
        self.assertIn('blobs: [analyticsEvent.downloadType]', self.worker)
        self.assertIn('doubles: [analyticsEvent.pageNumber]', self.worker)

    def test_wrangler_uses_workers_dev_and_analytics_engine_without_paid_configuration(self):
        self.assertIn('workers_dev = true', self.config)
        self.assertIn('dataset = "lms_download_clicks"', self.config)
        self.assertNotIn("route", self.config)
        self.assertNotIn("paid", self.config.lower())


if __name__ == "__main__":
    unittest.main()
