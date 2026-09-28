"""Build Learning WH Questions (Communication & Life Skills) — prototype.

Page 1 (Learn: the WH Words.): a visual teaching/reference page, not
a test. Five clearly separated, spacious rows introduce WHO, WHAT,
WHERE, WHEN, and WHY. Each row shows the question word large and
prominent, its simple meaning underneath, and one large full-bleed
illustration. The child points and says the words.

An adult reads the words aloud; the activity does not depend on
independent reading.
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


def draw_page1(pdf):
    draw_header(pdf, TITLE, "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 596, "Say the words.")
    row_h, gap = 80, 20
    top = 556
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
        # large illustration card on the right
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(250, cy - row_h / 2, 326, row_h, 12, fill=1, stroke=1)
        draw_cover_picture(pdf, asset, cy, 250, 326, row_h)
    draw_footer(pdf)
    pdf.showPage()


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pdf = canvas.Canvas(OUT, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_page1(pdf)
    pdf.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
