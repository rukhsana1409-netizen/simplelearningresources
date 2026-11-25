import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "deploy-download-analytics.yml"


class DownloadAnalyticsDeploymentTests(unittest.TestCase):
    def test_catalog_or_worker_changes_trigger_a_verified_worker_deploy(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("branches: [main]", workflow)
        self.assertIn("catalog/resources/**", workflow)
        self.assertIn("download-analytics-catalog.json", workflow)
        self.assertIn("cloudflare/download-analytics/**", workflow)
        self.assertIn("python -m unittest", workflow)
        self.assertIn("cloudflare/download-analytics/test/client.test.mjs", workflow)
        self.assertIn("cloudflare/download-analytics/test/worker.test.mjs", workflow)
        self.assertIn("wrangler@4.165.0 deploy", workflow)
        self.assertIn("CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}", workflow)
        self.assertIn("CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}", workflow)
        self.assertIn("cancel-in-progress: false", workflow)

    def test_workflow_has_read_only_repository_permissions(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertNotIn("contents: write", workflow)


if __name__ == "__main__":
    unittest.main()
