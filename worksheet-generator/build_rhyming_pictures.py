"""Build the 2-page Rhyming Pictures prototype.

Preschool Reading & Language:
- Page 1 (Match the Rhymes): 4 large pictures on each side (rhyming
  pairs split across sides, shuffled). The child draws lines between
  pictures that rhyme. No picture names.
- Page 2 (Which One Rhymes?): 4 large target pictures; beside each are
  2 picture choices. The child circles the picture that rhymes.
  No picture names.

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

TITLE = "Rhyming Pictures"
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "letters")
_CONVERT_DIR = os.path.join("/tmp", "rhyming_pictures_jpg")
_CONVERTED = {}


def asset_path(stem):
    """Build-time conversion: WebP -> print-sized JPEG for embedding."""
    if stem in _CONVERTED:
        return _CONVERTED[stem]
    path = os.path.join(ASSETS, f"{stem}.webp")
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


# Page 1: rhyming pairs, left side fixed order, right side shuffled so no
# pair sits directly across. (stem, rhyme partner stem)
PAGE1_LEFT = ["c-cat", "d-dog", "c-cake", "k-key"]
PAGE1_RIGHT = ["s-snake", "t-tree", "h-hat", "f-frog"]
PAGE1_YS = [498, 388, 278, 168]
PAGE1_LEFT_CX = 170
PAGE1_RIGHT_CX = 445


def draw_page1(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Match the Rhymes",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Draw a line between the pictures that rhyme.",
    )
    for stem, cy in zip(PAGE1_LEFT, PAGE1_YS):
        draw_picture(pdf, stem, PAGE1_LEFT_CX, cy, 92)
    for stem, cy in zip(PAGE1_RIGHT, PAGE1_YS):
        draw_picture(pdf, stem, PAGE1_RIGHT_CX, cy, 92)
    draw_footer(pdf)
    pdf.showPage()


# Page 2: (target stem, [left choice, right choice]); correct choice
# side varies down the page.
PAGE2_ROWS = [
    ("h-hat", ["c-cat", "d-dog"]),      # cat rhymes (left)
    ("f-frog", ["f-fish", "d-dog"]),    # dog rhymes (right)
    ("s-snake", ["c-cake", "b-bear"]),  # cake rhymes (left)
    ("t-tree", ["m-moon", "k-key"]),    # key rhymes (right)
]
PAGE2_YS = [510, 400, 290, 180]
TARGET_CX = 140
CHOICE_CXS = [350, 475]


def draw_page2(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Which One Rhymes?",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Circle the picture that rhymes.",
    )
    for (target, choices), cy in zip(PAGE2_ROWS, PAGE2_YS):
        draw_picture(pdf, target, TARGET_CX, cy, 92)
        for cx, stem in zip(CHOICE_CXS, choices):
            draw_picture(pdf, stem, cx, cy, 80)
    draw_footer(pdf)
    pdf.showPage()


def build():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "rhyming-pictures-prototype.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    pdf.setAuthor("Learning Made Simple")
    draw_page1(pdf)
    draw_page2(pdf)
    pdf.save()
    print(f"wrote {out} (2 pages)")


if __name__ == "__main__":
    build()
