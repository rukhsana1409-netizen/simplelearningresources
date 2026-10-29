import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class DownloadAnalyticsClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = (ROOT / "download-analytics.js").read_text(encoding="utf-8")
        cls.legacy = (ROOT / "resource-preview.html").read_text(encoding="utf-8")
        cls.clean_page_template = (ROOT / "site-tools" / "static_resource_pages.py").read_text(encoding="utf-8")

    def test_shared_script_tracks_pdf_links_by_url(self):
        self.assertIn('endsWith(".pdf")', self.script)
        self.assertIn('/\\/page-(\\d{2})\\.pdf$/i', self.script)
        self.assertIn('window.worksheetResourcesById?.[resourceId]', self.script)
        self.assertNotIn('link.matches(".page-download")', self.script)
        self.assertIn('downloadType: "pack"', self.script)
        self.assertIn('downloadType: "page"', self.script)
        self.assertIn('downloadType: "supporting"', self.script)
        self.assertIn('navigator.sendBeacon', self.script)
        self.assertIn('keepalive: true', self.script)
        self.assertIn('credentials: "omit"', self.script)
        self.assertEqual(self.script.count('document.addEventListener("click"'), 1)
        self.assertNotIn("preventDefault", self.script)

    def test_pdf_preview_links_are_covered_without_counting_supporting_guides_as_packs(self):
        self.assertIn('url.pathname === new URL(resource.pdfUrl, window.location.href).pathname', self.script)
        self.assertIn('link.matches(".resource-primary-action, #download-complete")', self.script)
        self.assertIn('"https://assets.simplelearningresources.com"', self.script)
        sample = (ROOT / "resources" / "story-elements" / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="resource-preview-link"', sample)
        self.assertIn('class="answer-key-download"', sample)

    def test_tracking_uses_the_approved_workers_dev_endpoint(self):
        self.assertIn(
            'const DOWNLOAD_ANALYTICS_ENDPOINT = "https://lms-download-analytics.rukhsana1409.workers.dev/download";',
            self.script,
        )
        self.assertIn('if (!DOWNLOAD_ANALYTICS_ENDPOINT) return;', self.script)

    def test_clean_and_legacy_pages_load_shared_download_script(self):
        self.assertEqual(self.clean_page_template.count('<script src="../../download-analytics.js" defer></script>'), 1)
        self.assertEqual(self.legacy.count('<script src="download-analytics.js" defer></script>'), 1)
        resource_pages = sorted((ROOT / "resources").glob("*/index.html"))
        self.assertEqual(len(resource_pages), 116)
        for page in resource_pages:
            self.assertEqual(
                page.read_text(encoding="utf-8").count('<script src="../../download-analytics.js" defer></script>'),
                1,
                page.as_posix(),
            )


if __name__ == "__main__":
    unittest.main()
