"""Focused regression checks for the approved Shape Safari integration."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GAME_ID = "shape-safari"
GAME_PATH = ROOT / "games" / GAME_ID / "shape-safari-game__5.html"


class ShapeSafariGameTests(unittest.TestCase):
    def test_approved_game_is_byte_identical(self):
        self.assertEqual(
            hashlib.sha256(GAME_PATH.read_bytes()).hexdigest(),
            "8d4f82007be53a2ea0035ac3613688b92b433891d652f51b4ae5db1dafa5454e",
        )

    def test_catalog_registers_the_approved_analytics_contract(self):
        catalog = json.loads((ROOT / "catalog/games.json").read_text(encoding="utf-8"))
        game = next(game for game in catalog["games"] if game["id"] == GAME_ID)
        self.assertEqual(game["playHref"], "/games/shape-safari/")
        self.assertEqual(game["ageRange"], "Kindergarten")
        self.assertEqual(
            game["analytics"]["difficulties"],
            {
                "easy": "Easy: Basic shapes",
                "medium": "Medium: More shapes and objects",
                "challenge": "Challenge: Puzzles, turns, and counting",
            },
        )
        self.assertEqual(
            game["analytics"]["categories"],
            {
                "shape-identification": "Shape identification",
                "shape-orientation": "Shape orientation",
                "open-closed": "Open and closed shapes",
                "complete-shapes": "Complete shapes",
                "shape-counting": "Shape counting",
            },
        )

    def test_wrapper_uses_the_clean_route_and_v1_bridge(self):
        wrapper = (ROOT / "games" / GAME_ID / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="https://simplelearningresources.com/games/shape-safari/"', wrapper)
        self.assertIn('src="shape-safari-game__5.html"', wrapper)
        self.assertIn('data-game-id="shape-safari"', wrapper)
        self.assertNotIn("adsbygoogle", wrapper)
        game_source = GAME_PATH.read_text(encoding="utf-8")
        self.assertIn('source:"lms-game-analytics",version:1', game_source)
        self.assertIn('eventType:"ready"', game_source)
        self.assertIn('eventType:"start"', game_source)
        self.assertIn('eventType:"complete"', game_source)


if __name__ == "__main__":
    unittest.main()
