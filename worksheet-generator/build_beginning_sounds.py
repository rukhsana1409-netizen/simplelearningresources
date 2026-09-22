"""Build the 2-page Beginning Sounds prototype.

Preschool Reading & Language:
- Page 1 (What Sound?): 5 large pictures of familiar objects/animals;
  beside each picture are 2 large letter choices. The child circles the
  letter the word begins with.
- Page 2 (Match the Sound): 4 large target letters and 4 pictures in
  mixed order. The child draws a line from each picture to its
  beginning letter.

Prototype only: these 2 pages for review. Do not extend without approval.
"""

import os
import sys

from reportlab.lib.colors import white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_worksheet import (
    BLUE,
    CORAL,
    GOLD,
    GREEN,
    INK,
    MUTED,
    ORANGE,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    PURPLE,
    TEAL,
    TEAL_DARK,
    draw_footer,
    draw_header,
)

TITLE = "Beginning Sounds"
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "letters")
_CONVERT_DIR = os.path.join("/tmp", "beginning_sounds_jpg")
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


def draw_picture(pdf, stem, word, cx, cy, box, label_size=12, show_label=True):
    img = ImageReader(asset_path(stem))
    pdf.drawImage(img, cx - box / 2, cy - box / 2, width=box, height=box,
                  preserveAspectRatio=True, anchor="c", mask="auto")
    if show_label:
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica-Bold", label_size)
        pdf.drawCentredString(cx, cy - box / 2 - 16, word)


def draw_letter_badge(pdf, cx, cy, letter, bg, r=34, font_size=44):
    pdf.setFillColor(bg)
    pdf.circle(cx, cy, r, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFillAlpha(0.18)
    pdf.circle(cx - r * 0.28, cy + r * 0.33, r * 0.30, fill=1, stroke=0)
    pdf.setFillAlpha(1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawCentredString(cx, cy - font_size * 0.357, letter)


# Page 1: (asset stem, word, correct letter, [left letter, right letter],
#          [left color, right color]).
PAGE1_ROWS = [
    ("d-dog", "dog", "D", ["D", "P"], [CORAL, TEAL]),
    ("s-sun", "sun", "S", ["T", "S"], [BLUE, GOLD]),
    ("c-cat", "cat", "C", ["R", "C"], [PURPLE, GREEN]),
    ("h-hat", "hat", "H", ["H", "K"], [ORANGE, TEAL]),
    ("b-banana", "banana", "B", ["D", "B"], [PURPLE, CORAL]),
]
PAGE1_YS = [518, 412, 306, 200, 94]
PIC_CX = 135
CHOICE_CXS = [350, 470]


def draw_page1(pdf):
    draw_header(pdf, {"title": f"{TITLE}: What Sound?",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "What sound does it start with? Circle the letter.",
    )
    for (stem, word, _correct, letters, colors), cy in zip(PAGE1_ROWS, PAGE1_YS):
        draw_picture(pdf, stem, word, PIC_CX, cy + 8, 80)
        for cx, letter, color in zip(CHOICE_CXS, letters, colors):
            draw_letter_badge(pdf, cx, cy, letter, color)
    draw_footer(pdf)
    pdf.showPage()


# Page 2: target letters (left) and pictures in mixed order (right).
PAGE2_LETTERS = [
    ("B", CORAL),
    ("P", TEAL),
    ("T", GOLD),
    ("M", PURPLE),
]
PAGE2_PICTURES = [
    ("m-moon", "moon"),
    ("b-bear", "bear"),
    ("p-pizza", "pizza"),
    ("t-train", "train"),
]
PAGE2_YS = [498, 388, 278, 168]
LETTER_CX = 170
PICTURE_CX = 445


def draw_page2(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Match the Sound",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Draw a line from each picture to its first sound.",
    )
    for (letter, color), cy in zip(PAGE2_LETTERS, PAGE2_YS):
        draw_letter_badge(pdf, LETTER_CX, cy, letter, color, r=40, font_size=52)
    for (stem, word), cy in zip(PAGE2_PICTURES, PAGE2_YS):
        draw_picture(pdf, stem, word, PICTURE_CX, cy, 84, show_label=False)
    draw_footer(pdf)
    pdf.showPage()


def build():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "beginning-sounds-prototype.pdf",
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
