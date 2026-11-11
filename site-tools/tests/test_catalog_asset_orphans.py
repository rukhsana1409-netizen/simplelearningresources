"""Ensure tracked worksheet assets are declared by the resource catalog."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "site-tools"))

from catalog_lib import load_resources  # noqa: E402


LEGACY_ASSET_ALLOWLIST = {
    "worksheets/math-worksheets.pdf",
    *{
        f"worksheets/preschool/math/number-recognition/number-{number}.pdf"
        for number in range(1, 11)
    },
}


def tracked_worksheet_assets() -> set[str]:
    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return {
        path
        for path in tracked
        if (
            (path.startswith("worksheets/") and path.endswith(".pdf"))
            or (path.startswith("thumbnails/") and path.endswith(".png"))
        )
    }


def catalog_assets() -> set[str]:
    declared: set[str] = set()
    for resource in load_resources():
        assets = resource["assets"]
        declared.add(assets["bundlePdf"])
        if assets.get("answerKeyPdf"):
            declared.add(assets["answerKeyPdf"])
        for page_number in range(1, len(resource["pages"]) + 1):
            declared.add(f"{assets['pagePdfDirectory']}/page-{page_number:02}.pdf")
            declared.add(f"{assets['previewDirectory']}/page-{page_number:02}.png")
    return declared


class CatalogAssetOrphanTests(unittest.TestCase):
    def test_tracked_worksheet_assets_are_cataloged_or_explicitly_legacy(self):
        orphaned = sorted(
            tracked_worksheet_assets() - catalog_assets() - LEGACY_ASSET_ALLOWLIST
        )
        self.assertEqual(orphaned, [])


if __name__ == "__main__":
    unittest.main()
