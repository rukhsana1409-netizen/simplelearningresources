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
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
_CONVERT_DIR = os.path.join("/tmp", "rhyming_pictures_jpg")
_CONVERTED = {}


def asset_path(stem):
    """Build-time conversion: WebP/PNG -> print-sized JPEG for embedding."""
    if stem in _CONVERTED:
        return _CONVERTED[stem]
    candidates = [
        os.path.join(ASSETS, "letters", f"{stem}.webp"),
        os.path.join(ASSETS, "rhyming", f"{stem}.png"),
    ]
    path = next((p for p in candidates if os.path.exists(p)), None)
    if path is None:
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
PAGE1_YS = [496, 378, 260, 142]
PAGE1_LEFT_CX = 170
PAGE1_RIGHT_CX = 445
PAGE1_BOX = 108


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
        draw_picture(pdf, stem, PAGE1_LEFT_CX, cy, PAGE1_BOX)
    for stem, cy in zip(PAGE1_RIGHT, PAGE1_YS):
        draw_picture(pdf, stem, PAGE1_RIGHT_CX, cy, PAGE1_BOX)
    draw_footer(pdf)
    pdf.showPage()


# Page 2: (target stem, [left choice, right choice]); correct choice
# side varies down the page. All pictures are different from page 1;
# no rhyme pair repeats. New illustrations (x-*) drawn in the approved
# style sit in assets/rhyming/.
PAGE2_ROWS = [
    ("h-house", ["x-mouse", "d-duck"]),    # mouse rhymes (left)
    ("x-truck", ["t-train", "d-duck"]),    # duck rhymes (right)
    ("x-rain", ["t-train", "m-moon"]),     # train rhymes (left)
    ("x-spoon", ["h-house", "m-moon"]),    # moon rhymes (right)
]
PAGE2_YS = [506, 388, 270, 152]
TARGET_CX = 140
TARGET_BOX = 108
CHOICE_CXS = [350, 475]
CHOICE_BOX = 96


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
        draw_picture(pdf, target, TARGET_CX, cy, TARGET_BOX)
        for cx, stem in zip(CHOICE_CXS, choices):
            draw_picture(pdf, stem, cx, cy, CHOICE_BOX)
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
