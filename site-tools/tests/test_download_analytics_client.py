import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class DownloadAnalyticsClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = (ROOT / "download-analytics.js").read_text(encoding="utf-8")
        cls.legacy = (ROOT / "resource-preview.html").read_text(encoding="utf-8")
        cls.clean_page_template = (ROOT / "site-tools" / "static_resource_pages.py").read_text(encoding="utf-8")

    def test_shared_script_tracks_only_intentional_pdf_download_controls(self):
        self.assertIn('endsWith(".pdf")', self.script)
        self.assertIn('/\\/page-(\\d{2})\\.pdf$/i', self.script)
        self.assertIn('window.worksheetResourcesById?.[resourceId]', self.script)
        self.assertIn('if (!link.hasAttribute("download")) return null;', self.script)
        self.assertIn('version: 2', self.script)
        self.assertIn('downloadType: "pack-download"', self.script)
        self.assertIn('downloadType: "page-download"', self.script)
        self.assertIn('downloadType: "supporting-download"', self.script)
        self.assertIn('navigator.sendBeacon', self.script)
        self.assertIn('keepalive: true', self.script)
        self.assertIn('credentials: "omit"', self.script)
        self.assertEqual(self.script.count('document.addEventListener("click"'), 1)
        self.assertNotIn("preventDefault", self.script)

    def test_preview_links_are_not_download_controls_and_guides_remain_distinct(self):
        self.assertIn('url.pathname === new URL(resource.pdfUrl, window.location.href).pathname', self.script)
        self.assertIn('link.matches(".resource-primary-action, #download-complete, #download")', self.script)
        self.assertIn('"https://assets.simplelearningresources.com"', self.script)
        sample = (ROOT / "resources" / "story-elements" / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="resource-preview-link"', sample)
        self.assertNotIn('class="resource-preview-link" download', sample)
        self.assertIn('class="answer-key-download"', sample)

    def test_every_published_resource_uses_download_semantics_consistently(self):
        resource_pages = sorted((ROOT / "resources").glob("*/index.html"))
        for page in resource_pages:
            html = page.read_text(encoding="utf-8")
            for marker in ('class="resource-primary-action"', 'class="page-download"', 'class="answer-key-download"'):
                for fragment in html.split(marker)[1:]:
                    opening_tag = fragment.split(">", 1)[0]
                    self.assertIn(" download", opening_tag, f"{page.as_posix()} {marker}")
            for fragment in html.split('class="resource-preview-link"')[1:]:
                opening_tag = fragment.split(">", 1)[0]
                self.assertNotIn(" download", opening_tag, page.as_posix())

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
        published_count = json.loads((ROOT / "download-analytics-catalog.json").read_text(encoding="utf-8"))["resourceCount"]
        self.assertEqual(len(resource_pages), published_count)
        for page in resource_pages:
            self.assertEqual(
                page.read_text(encoding="utf-8").count('<script src="../../download-analytics.js" defer></script>'),
                1,
                page.as_posix(),
            )


if __name__ == "__main__":
    unittest.main()
