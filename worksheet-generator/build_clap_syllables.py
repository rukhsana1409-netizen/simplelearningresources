"""Build the 2-page Clap the Syllables prototype.

Preschool Reading & Language:
- Page 1 (Count the Claps): 5 large familiar pictures. The child says
  each word, claps its word parts, then circles 1, 2, or 3.
  No picture names.
- Page 2 (Sort the Claps): 6 different large pictures in a picture bank.
  The child says each word, claps its parts, then draws a line to the
  matching box (1 clap / 2 claps / 3 claps). No picture names.

Prototype only: these 2 pages for review. Do not extend without approval.
"""

import os
import sys

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_worksheet import (
    BORDER,
    INK,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    PALE_TEAL,
    TEAL_DARK,
    draw_footer,
    draw_header,
)

TITLE = "Clap the Syllables"
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
_CONVERT_DIR = os.path.join("/tmp", "clap_syllables_jpg")
_CONVERTED = {}


def asset_path(stem):
    """Build-time conversion: WebP/PNG -> print-sized JPEG for embedding."""
    if stem in _CONVERTED:
        return _CONVERTED[stem]
    candidates = [
        os.path.join(ASSETS, "letters", f"{stem}.webp"),
        os.path.join(ASSETS, "rhyming", f"{stem}.png"),
        os.path.join(ASSETS, "syllables", f"{stem}.png"),
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


# Page 1: (stem, syllable count); counts mixed 1/2/3 across rows.
PAGE1_ROWS = [
    ("c-cat", 1),
    ("x-rabbit", 2),
    ("x-banana", 3),
    ("f-fish", 1),
    ("x-apple", 2),
]
PAGE1_YS = [498, 396, 294, 192, 90]
PAGE1_PIC_CX = 150
PAGE1_BOX = 96
PAGE1_CIRCLE_CXS = [340, 430, 520]
PAGE1_CIRCLE_D = 46


def draw_page1(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Count the Claps",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Say the word. Clap the word parts. Circle 1, 2, or 3.",
    )
    for (stem, _count), cy in zip(PAGE1_ROWS, PAGE1_YS):
        draw_picture(pdf, stem, PAGE1_PIC_CX, cy, PAGE1_BOX)
        for num, cx in zip((1, 2, 3), PAGE1_CIRCLE_CXS):
            r = PAGE1_CIRCLE_D / 2
            pdf.setFillColor(PALE_TEAL)
            pdf.setStrokeColor(TEAL_DARK)
            pdf.setLineWidth(2.5)
            pdf.circle(cx, cy, r, fill=1, stroke=1)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawCentredString(cx, cy - 8, str(num))
    draw_footer(pdf)
    pdf.showPage()


# Page 2: picture bank (2 rows x 3) plus three sort boxes below.
# 1 clap -> ball, book; 2 claps -> tiger, apple; 3 claps -> elephant,
# banana. Mixed so same-answer pictures never sit side by side.
PAGE2_BANK = [
    "x-ball", "x-apple", "x-elephant",
    "x-banana", "b-book", "x-tiger",
]
PAGE2_BANK_CXS = [140, 306, 472]
PAGE2_BANK_YS = [470, 340]
PAGE2_BANK_BOX = 96
PAGE2_BOX_CXS = [140, 306, 472]
PAGE2_BOX_CY = 165
PAGE2_BOX_W = 150
PAGE2_BOX_H = 118
PAGE2_BOX_LABELS = [("1", "clap"), ("2", "claps"), ("3", "claps")]


def draw_page2(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Sort the Claps",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Say each word and clap its parts. Draw a line to the right box.",
    )
    for i, stem in enumerate(PAGE2_BANK):
        cx = PAGE2_BANK_CXS[i % 3]
        cy = PAGE2_BANK_YS[i // 3]
        draw_picture(pdf, stem, cx, cy, PAGE2_BANK_BOX)
    for cx, (num, word) in zip(PAGE2_BOX_CXS, PAGE2_BOX_LABELS):
        x0 = cx - PAGE2_BOX_W / 2
        y0 = PAGE2_BOX_CY - PAGE2_BOX_H / 2
        pdf.setFillColor(PALE_TEAL)
        pdf.setStrokeColor(TEAL_DARK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(x0, y0, PAGE2_BOX_W, PAGE2_BOX_H, 14, fill=1, stroke=1)
        pdf.setFillColor(TEAL_DARK)
        pdf.setFont("Helvetica-Bold", 30)
        pdf.drawCentredString(cx, PAGE2_BOX_CY + 6, num)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(cx, PAGE2_BOX_CY - 26, word)
    draw_footer(pdf)
    pdf.showPage()


# Page 3: more counting practice. All pictures differ from Pages 1-2.
# (stem, syllable count); counts mixed 1/2/3 across rows.
PAGE3_ROWS = [
    ("d-dog", 1),
    ("x-pencil", 2),
    ("x-butterfly", 3),
    ("m-moon", 1),
    ("x-lemon", 2),
]


def draw_page3(pdf):
    draw_header(pdf, {"title": "Count the Claps: More Practice",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Say the word. Clap the word parts. Circle 1, 2, or 3.",
    )
    for (stem, _count), cy in zip(PAGE3_ROWS, PAGE1_YS):
        draw_picture(pdf, stem, PAGE1_PIC_CX, cy, PAGE1_BOX)
        for num, cx in zip((1, 2, 3), PAGE1_CIRCLE_CXS):
            r = PAGE1_CIRCLE_D / 2
            pdf.setFillColor(PALE_TEAL)
            pdf.setStrokeColor(TEAL_DARK)
            pdf.setLineWidth(2.5)
            pdf.circle(cx, cy, r, fill=1, stroke=1)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawCentredString(cx, cy - 8, str(num))
    draw_footer(pdf)
    pdf.showPage()


# Page 4: match pictures with the same number of syllables.
# Left column fixed, right column shuffled so no pair sits across.
# Pairs: star/hat (1 clap), turtle/candle (2 claps), piano/dinosaur
# (3 claps), cow/egg (1 clap).
PAGE4_LEFT = ["x-star", "x-turtle", "x-piano", "x-cow"]
PAGE4_RIGHT = ["x-candle", "h-hat", "x-dinosaur", "x-egg"]
PAGE4_YS = [496, 378, 260, 142]
PAGE4_LEFT_CX = 170
PAGE4_RIGHT_CX = 445
PAGE4_BOX = 108


def draw_page4(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Match the Same Beats",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Clap each word. Draw a line to match the same beats.",
    )
    for stem, cy in zip(PAGE4_LEFT, PAGE4_YS):
        draw_picture(pdf, stem, PAGE4_LEFT_CX, cy, PAGE4_BOX)
    for stem, cy in zip(PAGE4_RIGHT, PAGE4_YS):
        draw_picture(pdf, stem, PAGE4_RIGHT_CX, cy, PAGE4_BOX)
    draw_footer(pdf)
    pdf.showPage()


# Page 5: mixed review. One instruction: circle the 2-clap pictures.
# 1 clap -> duck, pig; 2 claps -> baby, table, robot, pumpkin;
# 3 claps -> camera, hamburger. None appear on Pages 1-4.
PAGE5_PICS = [
    "d-duck", "x-baby", "x-camera", "x-table",
    "x-pig", "x-robot", "x-hamburger", "x-pumpkin",
]
PAGE5_CXS = [103.5, 238.5, 373.5, 508.5]
PAGE5_YS = [455, 285]
PAGE5_BOX = 110


def draw_page5(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Clap & Circle",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Circle the pictures with 2 claps.",
    )
    for i, stem in enumerate(PAGE5_PICS):
        cx = PAGE5_CXS[i % 4]
        cy = PAGE5_YS[i // 4]
        draw_picture(pdf, stem, cx, cy, PAGE5_BOX)
    draw_footer(pdf)
    pdf.showPage()


def build():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "clap-syllables-prototype.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    pdf.setAuthor("Learning Made Simple")
    draw_page1(pdf)
    draw_page2(pdf)
    draw_page3(pdf)
    draw_page4(pdf)
    draw_page5(pdf)
    pdf.save()
    print(f"wrote {out} (5 pages)")


if __name__ == "__main__":
    build()
