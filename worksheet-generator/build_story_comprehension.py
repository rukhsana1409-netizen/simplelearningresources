"""Build the Story & Comprehension prototype (Pages 1-2).

Preschool Reading & Language:
- Page 1 (First and Last): 3 simple picture sequences, each showing
  3 clearly ordered events. The child circles what happens FIRST only.
  Sequences: seed -> sprout -> flower; egg -> chick -> hen;
  caterpillar -> cocoon -> butterfly.
- Page 2 (What Comes Next?): 3 spacious rows. Each row shows 2 pictures
  telling the beginning of a simple event, followed by 2 picture
  choices. The child circles what logically happens next.
  Rows: seed + watering can -> flower / shoe;
  toothbrush + toothpaste -> brushing teeth / cake;
  dark cloud + rain -> rainbow / snowman.
  Correct choice position varies by row.

Prototype only: these 2 pages for review. Do not extend without approval.
"""

import os
import sys

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_worksheet import (
    INK,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    draw_footer,
    draw_header,
    white,
)

TITLE = "Story & Comprehension"
BASE = os.path.dirname(os.path.abspath(__file__))
ASSET_DIRS = [
    os.path.join(BASE, "assets", "story-comprehension"),
    os.path.join(BASE, "assets", "letters"),
]
_CONVERT_DIR = os.path.join("/tmp", "story_comprehension_jpg")
_CONVERTED = {}


def asset_path(stem):
    """Resolve a PNG/WEBP asset stem to a path reportlab can read."""
    for d in ASSET_DIRS:
        for ext in (".png", ".webp"):
            src = os.path.join(d, stem + ext)
            if src in _CONVERTED:
                return _CONVERTED[src]
            if not os.path.exists(src):
                continue
            try:
                ImageReader(src)
                _CONVERTED[src] = src
                return src
            except Exception:
                pass
            from PIL import Image

            os.makedirs(_CONVERT_DIR, exist_ok=True)
            dst = os.path.join(_CONVERT_DIR, stem + ".jpg")
            Image.open(src).convert("RGB").save(dst, "JPEG", quality=92)
            _CONVERTED[src] = dst
            return dst
    raise FileNotFoundError(f"asset not found: {stem}")


def draw_picture(pdf, stem, cx, cy, box):
    img = ImageReader(asset_path(stem))
    pdf.drawImage(img, cx - box / 2, cy - box / 2, width=box, height=box,
                  preserveAspectRatio=True, anchor="c", mask="auto")


# Page 1: first and last. Each row is a 3-picture story in order.
PAGE1_SEQS = [
    ["s-seed", "s-sprout", "s-flower"],
    ["s-egg", "s-chick", "s-hen"],
    ["s-caterpillar", "s-cocoon", "s-butterfly"],
]
PAGE1_YS = [478, 309, 140]
PAGE1_CXS = [166, 306, 446]
PAGE1_BOX = 100


def draw_seq_panel(pdf, cy, stems):
    """Draw one sequence panel: 3 pictures left-to-right with arrows."""
    x, w, h = 36, 540, 150
    y = cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
    for stem, cx in zip(stems, PAGE1_CXS):
        draw_picture(pdf, stem, cx, cy, PAGE1_BOX)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(236, cy - 10, "→")
    pdf.drawCentredString(376, cy - 10, "→")


def draw_page1(pdf):
    draw_header(pdf, {"title": f"{TITLE}: First and Last",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 580,
        "Circle what happens FIRST.",
    )
    for seq, cy in zip(PAGE1_SEQS, PAGE1_YS):
        draw_seq_panel(pdf, cy, seq)
    draw_footer(pdf)
    pdf.showPage()


# Page 2: what comes next? Each row: 2 story pictures, an arrow,
# then 2 picture choices. Correct choice position varies by row.
PAGE2_SETS = [
    (["s-seed", "s-watering"], ["w-shoe", "s-flower"]),
    (["s-toothbrush", "s-toothpaste"], ["s-brushing", "c-cake"]),
    (["s-cloud", "s-rain"], ["w-snowman", "s-rainbow"]),
]
PAGE2_YS = [478, 309, 140]
PAGE2_STORY_CXS = [130, 235]
PAGE2_CHOICE_CXS = [420, 525]
PAGE2_BOX = 95


def draw_next_row(pdf, cy, story, choices):
    """Draw one 'what comes next' row."""
    x, w, h = 36, 540, 150
    y = cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
    for stem, cx in zip(story, PAGE2_STORY_CXS):
        draw_picture(pdf, stem, cx, cy, PAGE2_BOX)
    # Arrow between the story and the choices.
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(4)
    pdf.setLineCap(1)
    pdf.line(300, cy, 345, cy)
    pdf.line(345, cy, 333, cy + 10)
    pdf.line(345, cy, 333, cy - 10)
    for stem, cx in zip(choices, PAGE2_CHOICE_CXS):
        draw_picture(pdf, stem, cx, cy, PAGE2_BOX)


def draw_page2(pdf):
    draw_header(pdf, {"title": f"{TITLE}: What Comes Next?",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 580,
        "Circle what comes next.",
    )
    for (story, choices), cy in zip(PAGE2_SETS, PAGE2_YS):
        draw_next_row(pdf, cy, story, choices)
    draw_footer(pdf)
    pdf.showPage()


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "story-comprehension-prototype.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    draw_page2(pdf)
    pdf.save()
    print(f"wrote {out} (2 pages)")


if __name__ == "__main__":
    main()
