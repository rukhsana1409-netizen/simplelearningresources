import json
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPOSITORY_ROOT / "worksheet-generator" / "content" / "3d-shapes.json"


class ThreeDimensionalShapesConfigTests(unittest.TestCase):
    def test_pack_matches_the_canonical_five_page_shapes_progression(self):
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        self.assertEqual(data["template"], "3d-shapes-pack")
        self.assertEqual(data["filename"], "3d-shapes.pdf")
        self.assertEqual(data["title"], "3D Shapes")
        self.assertEqual(
            [page["type"] for page in data["pages"]],
            ["introduce", "identify", "match", "classify", "around-us"],
        )
        self.assertEqual(
            [page["activity"]["title"] for page in data["pages"]],
            [
                "3D Shapes",
                "Find the Shape",
                "Match Shapes & Objects",
                "Which Shape Is It?",
                "Shapes Around Us",
            ],
        )

    def test_pack_uses_recognition_activities_without_perspective_tracing(self):
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        serialized_pages = json.dumps(data["pages"]).lower()
        self.assertNotIn("trace", serialized_pages)
        self.assertNotIn("draw your own", serialized_pages)
        self.assertEqual(
            [item["object"] for item in data["pages"][4]["activity"]["items"]],
            ["ball", "block", "traffic cone", "can", "box"],
        )

    def test_pack_uses_all_five_core_shapes_and_canonical_asset_contract(self):
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        serialized_pages = json.dumps(data["pages"])
        for shape in ("sphere", "cube", "cone", "cylinder", "rectangular prism"):
            self.assertIn(shape, serialized_pages)
        self.assertEqual(
            data["asset_output"],
            {
                "resource_id": "3d-shapes",
                "expected_page_count": 5,
                "page_pdf_directory": "worksheets/preschool/math/shapes/3d-shapes",
                "preview_directory": "thumbnails/preschool/math/shapes/3d-shapes",
                "preview_dpi": 144,
            },
        )


if __name__ == "__main__":
    unittest.main()
