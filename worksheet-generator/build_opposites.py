"""Build the Page 1 Opposites prototype.

Preschool Reading & Language:
- Page 1 (Match the Opposites): 4 familiar opposite pairs across two
  columns (big fish / small fish, hot sun / cold snowflake,
  full glass / empty glass, up arrow / down arrow). The child draws a
  line to match the opposites. Right column shuffled so no pair sits
  across. No picture names.

Prototype only: this 1 page for review. Do not extend without approval.
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
# Pairs: big fish/small fish, hot sun/cold snowflake,
# full glass/empty glass, up arrow/down arrow.
PAGE1_LEFT = ["x-big-fish", "x-hot-sun", "x-full-glass", "x-up-arrow"]
PAGE1_RIGHT = ["x-cold-snowflake", "x-empty-glass", "x-down-arrow",
               "x-small-fish"]
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


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "opposites-prototype.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    pdf.save()
    print(f"wrote {out} (1 page)")


if __name__ == "__main__":
    main()
