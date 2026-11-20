from __future__ import annotations

import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class AboutCreatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.about = (ROOT / "about.html").read_text(encoding="utf-8")
        cls.home = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.styles = (ROOT / "style.css").read_text(encoding="utf-8")

    def test_about_page_contains_approved_creator_content(self) -> None:
        self.assertIn('id="meet-the-creator"', self.about)
        self.assertIn("Hi, I'm Rukhsana Parveen, the mom behind Learning Made Simple!", self.about)
        self.assertIn("How Our Resources Are Created", self.about)
        self.assertIn("background in software engineering and quality assurance", self.about)
        self.assertIn("guided by Michigan's academic standards", self.about)
        self.assertNotIn("certified teacher", self.about.lower())
        self.assertNotIn("officially endorsed", self.about.lower())
        self.assertNotIn("—", self.about)

    def test_creator_illustration_is_accessible_and_preserves_its_ratio(self) -> None:
        self.assertIn('src="images/about/meet-the-creator.png"', self.about)
        self.assertIn('alt="Illustration of Rukhsana working on learning resources at a laptop"', self.about)
        image = ROOT / "images/about/meet-the-creator.png"
        self.assertTrue(image.is_file())
        with image.open("rb") as source:
            self.assertEqual(source.read(8), b"\x89PNG\r\n\x1a\n")
            length = struct.unpack(">I", source.read(4))[0]
            self.assertEqual(source.read(4), b"IHDR")
            width, height = struct.unpack(">II", source.read(8))
        self.assertGreater(length, 0)
        self.assertEqual((width, height), (1254, 1254))
        self.assertIn(".creator-illustration { display:block; width:100%; height:auto;", self.styles)

    def test_mobile_layout_places_the_illustration_above_the_copy(self) -> None:
        self.assertIn(".creator-introduction { grid-template-columns:1fr;", self.styles)
        self.assertIn(".creator-illustration { grid-row:1;", self.styles)
        self.assertIn(".creator-copy { grid-row:2;", self.styles)
        self.assertIn(".creator-opening { white-space:nowrap;", self.styles)
        self.assertIn(".creator-opening { white-space:normal;", self.styles)

    def test_homepage_has_one_natural_creator_link(self) -> None:
        link = 'href="about.html#meet-the-creator"'
        self.assertEqual(self.home.count(link), 1)
        self.assertIn("Meet the Creator", self.home)


if __name__ == "__main__":
    unittest.main()
