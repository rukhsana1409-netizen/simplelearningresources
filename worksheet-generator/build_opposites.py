"""Build the Opposites prototype (Pages 1-3).

Preschool Reading & Language:
- Page 1 (Match the Opposites): 4 familiar opposite pairs across two
  columns (big ball / small ball, hot sun / cold snowflake,
  open door / closed door, up arrow / down arrow). The child draws a
  line to match the opposites. Right column shuffled so no pair sits
  across. No picture names.
- Page 2 (More Practice): 4 familiar opposite pairs across two
  columns (happy face / sad face, day sun / night moon,
  clean shirt / dirty shirt, tall giraffe / short mouse). Same
  match-the-opposites activity. Right column shuffled. No picture
  names.
- Page 3 (Find the Opposite): 4 rows. Each row shows one large
  target picture on the left and 2 picture choices on the right; the
  child circles the opposite. Pairs: loud/quiet, fast/slow,
  awake/asleep, light/heavy. The distractor in each row is the
  target picture itself, so the contrast is unambiguous.
  Correct-answer side alternates row to row. No picture names.

Prototype only: these 3 pages for review. Do not extend without approval.
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

TITLE = "Opposites"
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
_CONVERT_DIR = os.path.join("/tmp", "opposites_jpg")
_CONVERTED = {}


def asset_path(stem):
    """Build-time conversion: PNG -> print-sized JPEG for embedding."""
    if stem in _CONVERTED:
        return _CONVERTED[stem]
    path = os.path.join(ASSETS, "opposites", f"{stem}.png")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No illustration asset for {stem!r}")
    from PIL import Image
    os.makedirs(_CONVERT_DIR, exist_ok=True)
    dst = os.path.join(_CONVERT_DIR, f"{stem}.jpg")
    im = Image.open(path).convert("RGB")
    im.thumbnail((600, 600), Image.LANCZOS)
    im.save(dst, "JPEG", quality=82)
    _CONVERTED[stem] = dst
    return dst


def draw_picture(pdf, stem, cx, cy, box):
    img = ImageReader(asset_path(stem))
    pdf.drawImage(img, cx - box / 2, cy - box / 2, width=box, height=box,
                  preserveAspectRatio=True, anchor="c", mask="auto")


# Page 1: match the opposites. Left column fixed, right column shuffled
# so no pair sits across.
# Pairs: big ball/small ball, hot sun/cold snowflake,
# open door/closed door, up arrow/down arrow.
PAGE1_LEFT = ["x-big-ball", "x-hot-sun", "x-open-door", "x-up-arrow"]
PAGE1_RIGHT = ["x-cold-snowflake", "x-closed-door", "x-down-arrow",
               "x-small-ball"]
PAGE1_YS = [500, 380, 260, 140]
PAGE1_LEFT_CX = 190
PAGE1_RIGHT_CX = 422
PAGE1_BOX = 108


def draw_page1(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Match the Opposites",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Draw a line to match the opposites.",
    )
    for stem, cy in zip(PAGE1_LEFT, PAGE1_YS):
        draw_picture(pdf, stem, PAGE1_LEFT_CX, cy, PAGE1_BOX)
    for stem, cy in zip(PAGE1_RIGHT, PAGE1_YS):
        draw_picture(pdf, stem, PAGE1_RIGHT_CX, cy, PAGE1_BOX)
    draw_footer(pdf)
    pdf.showPage()


# Page 2: match the opposites. Left column fixed, right column shuffled
# so no pair sits across.
# Pairs: happy/sad, day/night, clean/dirty, tall/short.
PAGE2_LEFT = ["x-happy-face", "x-day-sun", "x-clean-shirt",
              "x-tall-giraffe"]
PAGE2_RIGHT = ["x-night-moon", "x-dirty-shirt", "x-short-mouse",
               "x-sad-face"]
PAGE2_YS = [500, 380, 260, 140]
PAGE2_LEFT_CX = 190
PAGE2_RIGHT_CX = 422
PAGE2_BOX = 108


def draw_page2(pdf):
    draw_header(pdf, {"title": f"{TITLE}: More Practice",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Draw a line to match the opposites.",
    )
    for stem, cy in zip(PAGE2_LEFT, PAGE2_YS):
        draw_picture(pdf, stem, PAGE2_LEFT_CX, cy, PAGE2_BOX)
    for stem, cy in zip(PAGE2_RIGHT, PAGE2_YS):
        draw_picture(pdf, stem, PAGE2_RIGHT_CX, cy, PAGE2_BOX)
    draw_footer(pdf)
    pdf.showPage()


# Page 3: find the opposite. Each row: one large target on the left,
# 2 choices on the right (the opposite + the target picture itself as
# the distractor). Correct-answer side alternates by row.
# Pairs: loud/quiet, fast/slow, awake/asleep, light/heavy.
PAGE3_ROWS = [
    ("x-loud-megaphone", ["x-quiet-shh", "x-loud-megaphone"]),
    ("x-fast-car", ["x-fast-car", "x-slow-snail"]),
    ("x-awake-face", ["x-asleep-face", "x-awake-face"]),
    ("x-light-feather", ["x-light-feather", "x-heavy-rock"]),
]
PAGE3_YS = [495, 375, 255, 135]
PAGE3_TARGET_CX = 140
PAGE3_TARGET_BOX = 112
PAGE3_CHOICE_CXS = [370, 512]
PAGE3_CHOICE_BOX = 96


def draw_page3(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Find the Opposite",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Circle the picture that is the opposite.",
    )
    for (target, choices), cy in zip(PAGE3_ROWS, PAGE3_YS):
        draw_picture(pdf, target, PAGE3_TARGET_CX, cy, PAGE3_TARGET_BOX)
        for stem, cx in zip(choices, PAGE3_CHOICE_CXS):
            draw_picture(pdf, stem, cx, cy, PAGE3_CHOICE_BOX)
    draw_footer(pdf)
    pdf.showPage()


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "opposites-prototype.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    draw_page2(pdf)
    draw_page3(pdf)
    pdf.save()
    print(f"wrote {out} (3 pages)")


if __name__ == "__main__":
    main()
