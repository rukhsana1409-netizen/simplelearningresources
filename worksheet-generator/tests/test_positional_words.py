import json
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPOSITORY_ROOT / "worksheet-generator" / "content" / "positional-words.json"


class PositionalWordsConfigTests(unittest.TestCase):
    def test_pack_matches_the_canonical_five_page_progression(self):
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        self.assertEqual(data["template"], "positional-words-pack")
        self.assertEqual(data["filename"], "positional-words.pdf")
        self.assertEqual(data["title"], "Positional Words")
        self.assertEqual(
            [page["type"] for page in data["pages"]],
            ["introduce", "above-below", "in-on-under", "next-to-between", "review"],
        )
        self.assertEqual(
            [page["activity"]["title"] for page in data["pages"]],
            ["Position Words", "Above or Below?", "In, On & Under", "Next To & Between", "Where Is It?"],
        )
        self.assertEqual(data["pages"][1]["subtitle"], "Learn where things are.")
        self.assertEqual(data["pages"][3]["subtitle"], "Practice next to and between.")

    def test_pack_covers_the_required_position_words_without_drawing_tasks(self):
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        serialized_pages = json.dumps(data["pages"]).lower()
        for word in ("above", "below", "in", "on", "under", "next to", "between"):
            self.assertIn(word, serialized_pages)
        self.assertNotIn("trace", serialized_pages)
        self.assertNotIn("draw", serialized_pages)

    def test_pack_uses_the_canonical_asset_contract(self):
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        self.assertEqual(len(data["pages"]), 5)
        self.assertEqual(
            data["asset_output"],
            {
                "resource_id": "positional-words",
                "expected_page_count": 5,
                "page_pdf_directory": "worksheets/preschool/math/shapes/positional-words",
                "preview_directory": "thumbnails/preschool/math/shapes/positional-words",
                "preview_dpi": 144,
            },
        )


if __name__ == "__main__":
    unittest.main()
