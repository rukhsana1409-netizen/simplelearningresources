"""Build the Story & Comprehension prototype (Pages 1-2).

Preschool Reading & Language:
- Page 1 (First and Last): 3 picture story sequences, left to right.
  The child circles what comes FIRST and draws a box around what
  comes LAST. Sequences: seed -> sprout -> flower;
  egg -> chick -> hen; caterpillar -> cocoon -> butterfly.
- Page 2 (What Comes Next?): 3 mini stories, each told in 2 pictures
  followed by 3 picture choices. The child circles what comes next.
  Stories: boy kicks ball; girl draws a sun; ice cream melts in the sun.
  Correct position varies by row.

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
)

TITLE = "Story & Comprehension"
ASSETS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "story-comprehension"
)
_CONVERT_DIR = os.path.join("/tmp", "story_comprehension_jpg")
_CONVERTED = {}


def asset_path(stem):
    """Resolve a PNG asset stem to a JPEG/PNG path reportlab can read."""
    src = os.path.join(ASSETS, stem + ".png")
    if src in _CONVERTED:
        return _CONVERTED[src]
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
PAGE1_YS = [460, 300, 140]
PAGE1_CXS = [130, 305, 480]
PAGE1_BOX = 95


def draw_page1(pdf):
    draw_header(pdf, {"title": f"{TITLE}: First and Last",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Circle what comes FIRST. Draw a box around what comes LAST.",
    )
    for seq, cy in zip(PAGE1_SEQS, PAGE1_YS):
        for stem, cx in zip(seq, PAGE1_CXS):
            draw_picture(pdf, stem, cx, cy, PAGE1_BOX)
    draw_footer(pdf)
    pdf.showPage()


# Page 2: what comes next? Each row: 2 story panels, an arrow, then
# 3 picture choices. Correct choice position varies by row.
PAGE2_SETS = [
    (["w-kick1", "w-kick2"], ["w-catch", "w-cat", "w-fish"]),
    (["w-draw1", "w-draw2"], ["w-sandwich", "w-sun-done", "w-shoe"]),
    (["w-ice1", "w-ice2"], ["w-snowman", "w-tree", "w-cone-empty"]),
]
PAGE2_YS = [465, 290, 115]
PAGE2_STORY_CXS = [85, 197]
PAGE2_ARROW_X1 = 132
PAGE2_ARROW_X2 = 165
PAGE2_CHOICE_CXS = [320, 425, 530]
PAGE2_BOX = 72


def draw_page2(pdf):
    draw_header(pdf, {"title": f"{TITLE}: What Comes Next?",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Circle what comes next.",
    )
    for (story, choices), cy in zip(PAGE2_SETS, PAGE2_YS):
        for stem, cx in zip(story, PAGE2_STORY_CXS):
            draw_picture(pdf, stem, cx, cy, PAGE2_BOX)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(4)
        pdf.setLineCap(1)
        pdf.line(PAGE2_ARROW_X1, cy, PAGE2_ARROW_X2, cy)
        pdf.line(PAGE2_ARROW_X2, cy, PAGE2_ARROW_X2 - 12, cy + 10)
        pdf.line(PAGE2_ARROW_X2, cy, PAGE2_ARROW_X2 - 12, cy - 10)
        for stem, cx in zip(choices, PAGE2_CHOICE_CXS):
            draw_picture(pdf, stem, cx, cy, PAGE2_BOX)
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
