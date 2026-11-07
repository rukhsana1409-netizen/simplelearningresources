"""Focused integration checks for the catalog-driven learning-games directory."""

from __future__ import annotations

import hashlib
import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GAME_ID = "big-or-small"
GAME_PATH = ROOT / "games" / GAME_ID / "big-or-small-game__5.html"


class LearningGamesTests(unittest.TestCase):
    def test_approved_game_is_byte_identical(self):
        self.assertEqual(
            hashlib.sha256(GAME_PATH.read_bytes()).hexdigest(),
            "78ad3b9f296f05179e28221ddba317e6ee8f14a09ab4186891e8498649b4c367",
        )

    def test_catalog_drives_the_games_directory(self):
        catalog = json.loads((ROOT / "catalog/games.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["schemaVersion"], 1)
        self.assertEqual([game["id"] for game in catalog["games"]], [GAME_ID, "number-chomp"])
        game = catalog["games"][0]
        self.assertEqual(game["ageRange"], "Preschool and Kindergarten")
        self.assertEqual(game["playHref"], "/games/big-or-small/")
        directory = (ROOT / "games.html").read_text(encoding="utf-8")
        self.assertIn("Free Learning Games", directory)
        self.assertIn("Big or Small?", directory)
        self.assertIn('href="/games/big-or-small/"', directory)
        self.assertIn("Preschool and Kindergarten", directory)
        self.assertIn("Number Chomp!", directory)
        self.assertIn('href="/games/number-chomp/"', directory)

    def test_homepage_features_the_game_once(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertEqual(homepage.count('id="home-games-title"'), 1)
        self.assertIn("Free Learning Games", homepage)
        self.assertIn('href="games/big-or-small/">Play Now</a>', homepage)
        self.assertIn('href="games.html">View All Games', homepage)
        self.assertIn('src="games/big-or-small/big-or-small-preview.png"', homepage)
        self.assertIn('href="games/number-chomp/">Play Now</a>', homepage)
        self.assertIn('src="games/number-chomp/number-chomp-preview.png"', homepage)

    def test_game_wrapper_is_indexable_ad_free_and_loads_the_approved_game(self):
        source = (ROOT / "games/big-or-small/index.html").read_text(encoding="utf-8")
        self.assertIn('<link rel="canonical" href="https://simplelearningresources.com/games/big-or-small/">', source)
        self.assertIn('src="big-or-small-game__5.html"', source)
        self.assertIn('src="/game-analytics.js"', source)
        self.assertIn('data-game-id="big-or-small"', source)
        self.assertNotIn("adsbygoogle", source)
        self.assertNotIn("google-adsense-account", source)

    def test_navigation_and_sitemap_include_games(self):
        nav_source = (ROOT / "nav.js").read_text(encoding="utf-8")
        match = re.search(r'const generatedPrimaryNavigation=("(?:\\.|[^"])*");', nav_source)
        self.assertIsNotNone(match)
        markup = json.loads(match.group(1))
        self.assertEqual(markup.count('href="games.html">Free Learning Games</a>'), 1)
        sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = [element.text for element in sitemap.findall("s:url/s:loc", namespace)]
        self.assertEqual(locations.count("https://simplelearningresources.com/games.html"), 1)
        self.assertEqual(locations.count("https://simplelearningresources.com/games/big-or-small/"), 1)
        self.assertEqual(locations.count("https://simplelearningresources.com/games/number-chomp/"), 1)

    def test_game_analytics_collects_only_aggregate_game_events(self):
        source = (ROOT / "game-analytics.js").read_text(encoding="utf-8")
        self.assertIn("/game-event", source)
        self.assertIn('"view"', source)
        self.assertIn('"start"', source)
        self.assertIn('"complete"', source)
        for forbidden in ("email", "name", "cookie", "localStorage", "sessionStorage", "userAgent"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
