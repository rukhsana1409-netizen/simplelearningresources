"""Build Learning WH Questions (Communication & Life Skills) — prototype.

Page 1 (Learn: the WH Words.): a visual teaching/reference page, not
a test. Five clearly separated, spacious rows introduce WHO, WHAT,
WHERE, WHEN, and WHY. Each row shows the question word large and
prominent, its simple meaning underneath, and one large full-bleed
illustration. The child points and says the words.

An adult reads the words aloud; the activity does not depend on
independent reading.

Page 2 (Practice: Who Is It.) is WHO practice: three questions, each
with three large pictures of people doing different actions. All
choices are people, so the child must understand the complete
question — not just pick the only person, object, or place.
"""

from __future__ import annotations

import io
import os

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792
TITLE = "Learn: the WH Words."
PAGE2_TITLE = "Practice: Who Is It?"
PAGE2_INSTRUCTION = "Listen to the question. Circle the person."

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
GOLD = HexColor("#F4B63E")
INK = HexColor("#202A33")
BORDER = HexColor("#B9D7D2")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "wh-questions")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "communication",
                   "wh-questions", "wh-questions-prototype.pdf")


def draw_logo(pdf, x, y):
    """Vector-only Learning Made Simple mark and wordmark (established
    brand header, as in Learn My Letters)."""
    pdf.setFillColor(TEAL)
    pdf.circle(x + 18, y + 26, 7, fill=1, stroke=0)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(x + 18, y + 18, x + 18, y + 4)
    pdf.line(x + 18, y + 14, x + 6, y + 5)
    pdf.line(x + 18, y + 14, x + 30, y + 5)
    pdf.setLineWidth(1.3)
    pdf.line(x + 2, y + 4, x + 18, y)
    pdf.line(x + 18, y, x + 34, y + 4)
    pdf.setFillColor(GOLD)
    pdf.circle(x + 18, y + 39, 3.5, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(x + 43, y + 24, "LEARNING")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(x + 43, y + 10, "MADE SIMPLE")


def draw_header(pdf, title, subtitle):
    """Established brand header (Learn My Letters style): teal top strip,
    vector logo + wordmark, divider, two-line teal title, teal rule."""
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, fill=1, stroke=0)
    draw_logo(pdf, MARGIN, PAGE_HEIGHT - 86)
    divider_x = 210
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1)
    pdf.line(divider_x, PAGE_HEIGHT - 46, divider_x, PAGE_HEIGHT - 106)
    title_x = divider_x + 19
    if ": " in title:
        prefix, focus = title.split(": ", 1)
    else:
        prefix, focus = "", title
    if prefix:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(title_x, PAGE_HEIGHT - 67, prefix + ":")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(title_x, PAGE_HEIGHT - 98, focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11.5)
    pdf.drawString(title_x, PAGE_HEIGHT - 116, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    pdf.line(MARGIN, PAGE_HEIGHT - 131, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 131)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(MARGIN, PAGE_HEIGHT - 160, "Name:")
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.9)
    pdf.line(MARGIN + 37, PAGE_HEIGHT - 163, 315, PAGE_HEIGHT - 163)
    pdf.setFillColor(INK)
    pdf.drawString(430, PAGE_HEIGHT - 160, "Date:")
    pdf.setStrokeColor(BORDER)
    pdf.line(463, PAGE_HEIGHT - 163, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 163)


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF4F3"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#0E7C7B"))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(56, 19, "Learning Made Simple")
    pdf.setStrokeColor(HexColor("#9FD3D1"))
    pdf.setLineWidth(1.5)
    pdf.line(200, 10, 200, 34)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(320, 19, "Made with love for little learners.")
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(556, 19, "\u00a9 2026 Learning Made Simple")


# New-page images are embedded downscaled to 1100px wide: still sharp
# at print size, and it keeps the PDF small enough for the GitHub
# blob API. Full-resolution masters stay in assets/.
MAX_EMBED_WIDTH = 1100


def draw_fit_picture(pdf, stem, cx, cy, w, h, pad=10):
    """Illustration scaled down inside its card with comfortable white
    space around the subject — the complete artwork stays visible,
    no banner-style cropping."""
    path = os.path.join(ASSETS, stem + ".png")
    img = Image.open(path)
    if img.width > MAX_EMBED_WIDTH:
        img = img.resize(
            (MAX_EMBED_WIDTH,
             int(img.height * MAX_EMBED_WIDTH / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    src = ImageReader(buf)
    iw, ih = img.size
    scale = min((w - 2 * pad) / iw, (h - 2 * pad) / ih)
    dw, dh = iw * scale, ih * scale
    pdf.drawImage(src, cx - dw / 2, cy - dh / 2, dw, dh,
                  preserveAspectRatio=True, mask="auto")


def draw_cover_picture(pdf, stem, cy, x, w, h, r=12):
    """Full-bleed illustration clipped cleanly inside its rounded card.
    The image covers the card (tighter crop) so the subject stays
    large and immediately readable."""
    path = os.path.join(ASSETS, stem + ".png")
    img = Image.open(path)
    if img.width > MAX_EMBED_WIDTH:
        img = img.resize(
            (MAX_EMBED_WIDTH,
             int(img.height * MAX_EMBED_WIDTH / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    src = ImageReader(buf)
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    cx = x + w / 2
    pdf.saveState()
    p = pdf.beginPath()
    p.roundRect(x + 1.5, cy - h / 2 + 1.5, w - 3, h - 3, r - 1.5)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.drawImage(src, cx - dw / 2, cy - dh / 2, dw, dh,
                  preserveAspectRatio=True, mask="auto")
    pdf.restoreState()


# Page 1 rows: (asset stem, WH word, simple meaning).
PAGE1_ROWS = [
    ("whq-who-person", "WHO", "Person"),
    ("whq-what-thing", "WHAT", "Thing or Action"),
    ("whq-where-place", "WHERE", "Place"),
    ("whq-when-time", "WHEN", "Time"),
    ("whq-why-reason", "WHY", "Reason"),
]

# Per-asset crop bands as (y0, y1) fractions of the source height.
# Each band keeps its subject 100% complete with a comfortable margin
# while trimming empty sky/ground so the picture fills its card.
PAGE1_CROPS = {
    "whq-who-person": (0.061, 0.956),
    "whq-what-thing": (0.152, 0.847),
    "whq-where-place": (0.25, 0.727),
    "whq-when-time": (0.143, 0.875),
    "whq-why-reason": (0.03, 0.93),
}

# Displayed picture height inside each 88pt card.
PAGE1_PIC_H = 80


def draw_band_picture(pdf, stem, cx, cy):
    """Illustration cropped to its PAGE1_CROPS band (subject complete)
    and drawn at PAGE1_PIC_H tall, centered in its card."""
    path = os.path.join(ASSETS, stem + ".png")
    img = Image.open(path)
    if img.width > MAX_EMBED_WIDTH:
        img = img.resize(
            (MAX_EMBED_WIDTH,
             int(img.height * MAX_EMBED_WIDTH / img.width)), Image.LANCZOS)
    y0f, y1f = PAGE1_CROPS[stem]
    img = img.crop((0, int(img.height * y0f), img.width, int(img.height * y1f)))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    src = ImageReader(buf)
    iw, ih = img.size
    scale = PAGE1_PIC_H / ih
    dw, dh = iw * scale, ih * scale
    pdf.drawImage(src, cx - dw / 2, cy - dh / 2, dw, dh,
                  preserveAspectRatio=True, mask="auto")


def draw_page1(pdf):
    draw_header(pdf, TITLE, "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 596, "WH words help us ask questions.")
    row_h, gap = 88, 12
    top = 560
    for i, (asset, word, meaning) in enumerate(PAGE1_ROWS):
        cy = top - i * (row_h + gap) - row_h / 2
        # WH word + meaning as one left block, vertically centered
        # with its illustration card
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 30)
        pdf.drawString(44, cy + 2, word)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 16)
        pdf.drawString(44, cy - 19, meaning)
        # illustration card, pulled closer to the text so each word
        # and picture clearly belong together; band-cropped artwork
        # fills the card with the subject complete
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(200, cy - row_h / 2, 352, row_h, 12, fill=1, stroke=1)
        draw_band_picture(pdf, asset, 200 + 352 / 2, cy)
    draw_footer(pdf)
    pdf.showPage()


# Page 2 questions: (question text, [answer-position-varied choice stems]).
PAGE2_QUESTIONS = [
    ("1. Who is eating?",
     ["whq-p2-boy-sleep", "whq-p2-girl-apple", "whq-p2-grandma-read1"]),
    ("2. Who is brushing teeth?",
     ["whq-p2-girl-banana", "whq-p2-baby-sleep", "whq-p2-boy-brush"]),
    ("3. Who is reading?",
     ["whq-p2-grandma-read2", "whq-p2-boy-rope", "whq-p2-girl-milk"]),
]

PAGE2_CARD_W, PAGE2_CARD_H = 168, 112


def draw_page2(pdf):
    draw_header(pdf, PAGE2_TITLE, "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 596, PAGE2_INSTRUCTION)
    row_h, gap = 160, 14
    top = 560
    card_xs = [MARGIN, MARGIN + PAGE2_CARD_W + 14,
               MARGIN + 2 * (PAGE2_CARD_W + 14)]
    for i, (question, stems) in enumerate(PAGE2_QUESTIONS):
        row_top = top - i * (row_h + gap)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawCentredString(PAGE_WIDTH / 2, row_top - 24, question)
        card_cy = row_top - 38 - PAGE2_CARD_H / 2
        for x, stem in zip(card_xs, stems):
            pdf.setFillColor(white)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(2.5)
            pdf.roundRect(x, card_cy - PAGE2_CARD_H / 2,
                          PAGE2_CARD_W, PAGE2_CARD_H, 12, fill=1, stroke=1)
            draw_cover_picture(pdf, stem, card_cy, x,
                               PAGE2_CARD_W, PAGE2_CARD_H)
    draw_footer(pdf)
    pdf.showPage()


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pdf = canvas.Canvas(OUT, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_page1(pdf)
    draw_page2(pdf)
    pdf.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
