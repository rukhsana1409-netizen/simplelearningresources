"""Focused regression checks for the approved Number Chomp integration."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GAME_ID = "number-chomp"
GAME_PATH = ROOT / "games" / GAME_ID / "number-chomp-game__1.html"


class NumberChompGameTests(unittest.TestCase):
    def test_approved_game_is_byte_identical(self):
        self.assertEqual(
            hashlib.sha256(GAME_PATH.read_bytes()).hexdigest(),
            "3f08c8e0944a18b0df2e7d219580d2544c435cf18ec103b9ec378b1a20c5daba",
        )

    def test_catalog_and_wrapper_use_the_clean_game_route(self):
        catalog = json.loads((ROOT / "catalog/games.json").read_text(encoding="utf-8"))
        game = next(game for game in catalog["games"] if game["id"] == GAME_ID)
        self.assertEqual(game["playHref"], "/games/number-chomp/")
        self.assertEqual(game["ageRange"], "Kindergarten and Grade 1")
        wrapper = (ROOT / "games/number-chomp/index.html").read_text(encoding="utf-8")
        self.assertIn('href="https://simplelearningresources.com/games/number-chomp/"', wrapper)
        self.assertIn('src="number-chomp-game__1.html"', wrapper)
        self.assertIn('data-game-id="number-chomp"', wrapper)
        self.assertNotIn("adsbygoogle", wrapper)

    def test_approved_game_exposes_the_complete_play_flow(self):
        source = GAME_PATH.read_text(encoding="utf-8")
        for element_id in ("snd", "restart", "next", "done", "again", "change"):
            self.assertIn(f'id="{element_id}"', source)
        self.assertIn('class="lvl ', source)
        self.assertIn('data-lv="easy"', source)
        self.assertIn('data-lv="med"', source)
        self.assertIn('data-lv="hard"', source)
        self.assertIn("You chomped all 20 questions!", source)

    def test_shared_analytics_tracks_level_selection_as_a_start(self):
        source = (ROOT / "game-analytics.js").read_text(encoding="utf-8")
        self.assertIn('querySelectorAll("[data-lv]")', source)


if __name__ == "__main__":
    unittest.main()
