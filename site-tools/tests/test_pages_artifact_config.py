"""Focused regression checks for the GitHub Pages artifact allowlist."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPOSITORY_ROOT / "_config.yml"
MAX_ARTIFACT_BYTES = 100 * 1024 * 1024


def excluded_paths() -> tuple[str, ...]:
    paths = []
    for line in CONFIG_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            paths.append(stripped[2:])
    return tuple(paths)


def is_excluded(relative_path: str, exclusions: tuple[str, ...]) -> bool:
    return any(
        relative_path == prefix or relative_path.startswith(f"{prefix}/")
        for prefix in exclusions
    )


class PagesArtifactConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exclusions = excluded_paths()
        cls.tracked_files = subprocess.run(
            ["git", "ls-files"],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()

    def test_development_directories_are_excluded(self):
        for path in ("catalog", "cloudflare", "site-tools", "worksheet-generator"):
            with self.subTest(path=path):
                self.assertIn(path, self.exclusions)

    def test_cdn_backed_asset_trees_are_excluded(self):
        for path in (
            "worksheets/grade-1",
            "worksheets/kindergarten",
            "worksheets/seasonal",
            "thumbnails/grade-1",
            "thumbnails/kindergarten",
            "thumbnails/seasonal",
        ):
            with self.subTest(path=path):
                self.assertIn(path, self.exclusions)

    def test_public_site_and_legacy_number_assets_remain_packaged(self):
        required = (
            "index.html",
            "privacy.html",
            "directory.js",
            "download-analytics.js",
            "download-analytics-catalog.json",
            "sitemap.xml",
            "resources/adding-tens-and-ones/index.html",
            "games/big-or-small/index.html",
            "worksheets/preschool/math/number-recognition/number-1.pdf",
            "worksheets/preschool/math/number-recognition/number-10.pdf",
        )
        for path in required:
            with self.subTest(path=path):
                self.assertIn(path, self.tracked_files)
                self.assertFalse(is_excluded(path, self.exclusions))

    def test_generated_resource_pages_reference_cdn_assets(self):
        pages = sorted((REPOSITORY_ROOT / "resources").glob("*/index.html"))
        self.assertEqual(len(pages), 142)
        for page in pages:
            source = page.read_text(encoding="utf-8")
            with self.subTest(page=page.parent.name):
                self.assertIn("https://assets.simplelearningresources.com/", source)
                self.assertNotIn('src="../../thumbnails/', source)
                self.assertNotIn('href="../../worksheets/', source)

    def test_runtime_catalog_resolves_assets_to_the_production_cdn(self):
        source = (REPOSITORY_ROOT / "directory.js").read_text(encoding="utf-8")
        self.assertIn(
            'window.worksheetAssetBaseUrl="https://assets.simplelearningresources.com"',
            source,
        )
        self.assertIn("previewUrl:resolveWorksheetAssetUrl(page.previewPath)", source)
        self.assertIn("pdfUrl:resolveWorksheetAssetUrl(page.pdfPath)", source)

    def test_estimated_pages_artifact_has_safety_margin(self):
        included_bytes = sum(
            (REPOSITORY_ROOT / path).stat().st_size
            for path in self.tracked_files
            if (REPOSITORY_ROOT / path).is_file()
            and not is_excluded(path, self.exclusions)
        )
        self.assertLess(included_bytes, MAX_ARTIFACT_BYTES)


if __name__ == "__main__":
    unittest.main()
