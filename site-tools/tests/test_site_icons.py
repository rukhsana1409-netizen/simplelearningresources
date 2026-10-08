"""Focused tests for the approved site icon assets and references."""

from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

from PIL import Image


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
APPROVED_SOURCE_SHA256 = "cb3888333337381b435377cf30674fb7a837811cc256c2aa8feca5ee6ef27c17"
ICON_REFERENCES = (
    "/favicon.ico",
    "/favicon-16x16.png",
    "/favicon-32x32.png",
    "/site-icon-192x192.png",
    "/apple-touch-icon.png",
)


class SiteIconTests(unittest.TestCase):
    def test_approved_source_is_preserved_exactly(self):
        source = REPOSITORY_ROOT / "site-icon-source.png"
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), APPROVED_SOURCE_SHA256)
        with Image.open(source) as image:
            self.assertEqual(image.size, (1254, 1254))
            self.assertEqual(image.mode, "RGB")

    def test_generated_icon_dimensions_and_ico_frames(self):
        expected_png_sizes = {
            "favicon-16x16.png": (16, 16),
            "favicon-32x32.png": (32, 32),
            "apple-touch-icon.png": (180, 180),
            "site-icon-192x192.png": (192, 192),
        }
        for filename, expected_size in expected_png_sizes.items():
            with self.subTest(filename=filename), Image.open(REPOSITORY_ROOT / filename) as image:
                self.assertEqual(image.format, "PNG")
                self.assertEqual(image.size, expected_size)
        with Image.open(REPOSITORY_ROOT / "favicon.ico") as icon:
            self.assertEqual(icon.format, "ICO")
            self.assertEqual(set(icon.ico.sizes()), {(16, 16), (32, 32), (48, 48)})

    def test_every_production_html_page_references_the_shared_icons_once(self):
        pages = sorted(REPOSITORY_ROOT.glob("*.html")) + sorted(
            (REPOSITORY_ROOT / "resources").glob("*/index.html")
        )
        self.assertEqual(len(pages), 93)
        for page in pages:
            source = page.read_text(encoding="utf-8")
            with self.subTest(page=page.relative_to(REPOSITORY_ROOT)):
                self.assertNotIn("favicon.svg", source)
                for reference in ICON_REFERENCES:
                    self.assertEqual(source.count(reference), 1)

    def test_every_header_uses_the_approved_logo_asset(self):
        pages = sorted(REPOSITORY_ROOT.glob("*.html")) + sorted(
            (REPOSITORY_ROOT / "resources").glob("*/index.html")
        )
        expected = (
            '<img class="logo-mark" src="/site-icon-source.png" '
            'alt="" width="34" height="34">'
        )
        for page in pages:
            source = page.read_text(encoding="utf-8")
            with self.subTest(page=page.relative_to(REPOSITORY_ROOT)):
                self.assertEqual(source.count(expected), 1)
                self.assertNotIn('<span class="logo-mark">L</span>', source)

    def test_shared_logo_css_preserves_the_header_footprint(self):
        source = (REPOSITORY_ROOT / "style.css").read_text(encoding="utf-8")
        self.assertIn(
            ".logo-mark { display:block; flex:0 0 auto; width:34px; height:34px; object-fit:contain; }",
            source,
        )
        self.assertIn(".logo-mark { width:32px; height:32px; }", source)


if __name__ == "__main__":
    unittest.main()
