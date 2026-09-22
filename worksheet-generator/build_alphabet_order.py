"""Build the 2-page Alphabet Order & Missing Letters prototype.

Preschool Reading & Language:
- Page 1 (ABC Order): small groups of large scrambled letter cards; the
  child writes them in ABC order in the numbered answer boxes.
- Page 2 (Missing Letters): short alphabet sequences with one missing
  letter; the child writes the missing letter in the generous box.

Prototype only: these 2 pages for review. Do not extend without approval.
"""

import os
import sys

from reportlab.lib.colors import white
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_worksheet import (
    BLUE,
    BORDER,
    CORAL,
    GOLD,
    GREEN,
    INK,
    MARGIN,
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

TITLE = "ABC Order & Missing Letters"

# Page 1: scrambled card groups (letters shown out of order on purpose).
GROUPS = [
    {"cards": ["C", "A", "B"], "colors": [CORAL, TEAL, GOLD]},
    {"cards": ["E", "D", "F"], "colors": [PURPLE, BLUE, GREEN]},
    {"cards": ["H", "G", "I"], "colors": [ORANGE, CORAL, TEAL]},
]
CARD = 76
CARD_GAP = 24

# Page 2: short sequences, one missing letter each (None = writing box).
SEQUENCES = [
    {"items": ["A", "B", None, "D"], "colors": [CORAL, ORANGE, None, GREEN]},
    {"items": ["E", None, "G", "H"], "colors": [PURPLE, None, TEAL, BLUE]},
    {"items": [None, "J", "K", "L"], "colors": [None, GOLD, CORAL, GREEN]},
    {"items": ["M", "N", "O", None], "colors": [TEAL, PURPLE, ORANGE, None]},
]
SEQ_GAP = 96
WRITE_BOX = 78


def draw_card(pdf, cx, cy, letter, bg):
    """A colorful movable-looking letter card."""
    x, y = cx - CARD / 2, cy - CARD / 2
    pdf.setFillColor(bg)
    pdf.roundRect(x, y, CARD, CARD, 16, fill=1, stroke=0)
    # soft highlight for a playful look
    pdf.setFillColor(white)
    pdf.setFillAlpha(0.18)
    pdf.circle(cx - 14, cy + 15, 12, fill=1, stroke=0)
    pdf.setFillAlpha(1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 52)
    pdf.drawCentredString(cx, cy - 19, letter)


def draw_answer_box(pdf, cx, cy, number):
    """Dashed empty box where the child writes the next letter in order."""
    x, y = cx - CARD / 2, cy - CARD / 2
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(2.5)
    pdf.setDash(8, 6)
    pdf.roundRect(x, y, CARD, CARD, 16, fill=0, stroke=1)
    pdf.setDash()
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(x + 10, y + CARD - 22, str(number))


def draw_group_badge(pdf, number, cy):
    pdf.setFillColor(TEAL)
    pdf.circle(MARGIN + 14, cy, 14, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(MARGIN + 14, cy - 6, str(number))


def draw_order_page(pdf):
    draw_header(pdf, {"title": f"{TITLE}: ABC Order",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Put the letters in ABC order. Write them in the boxes.",
    )

    group_w = 3 * CARD + 2 * CARD_GAP
    start_x = (PAGE_WIDTH - group_w) / 2 + CARD / 2
    for gi, group in enumerate(GROUPS):
        cards_y = 520 - gi * 155
        answers_y = cards_y - 100
        draw_group_badge(pdf, gi + 1, cards_y)
        for i, (letter, color) in enumerate(zip(group["cards"], group["colors"])):
            cx = start_x + i * (CARD + CARD_GAP)
            draw_card(pdf, cx, cards_y, letter, color)
            draw_answer_box(pdf, cx, answers_y, i + 1)

    draw_footer(pdf)
    pdf.showPage()


def draw_write_box(pdf, cx, cy):
    """Generous dashed box for writing the missing letter."""
    x, y = cx - WRITE_BOX / 2, cy - WRITE_BOX / 2
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(2.5)
    pdf.setDash(8, 6)
    pdf.roundRect(x, y, WRITE_BOX, WRITE_BOX, 16, fill=0, stroke=1)
    pdf.setDash()


def draw_missing_page(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Missing Letters",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596, "Write the missing letter in the box.")

    for ri, seq in enumerate(SEQUENCES):
        cy = 478 - ri * 112
        n = len(seq["items"])
        start_x = (PAGE_WIDTH - (n - 1) * SEQ_GAP) / 2
        for i, (letter, color) in enumerate(zip(seq["items"], seq["colors"])):
            cx = start_x + i * SEQ_GAP
            if letter is None:
                draw_write_box(pdf, cx, cy)
            else:
                pdf.setFillColor(color)
                pdf.setFont("Helvetica-Bold", 60)
                pdf.drawCentredString(cx, cy - 22, letter)

    draw_footer(pdf)
    pdf.showPage()


def build():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "alphabet-order-missing-letters-prototype.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    pdf.setAuthor("Learning Made Simple")
    draw_order_page(pdf)
    draw_missing_page(pdf)
    pdf.save()
    print(f"wrote {out} (2 pages)")


if __name__ == "__main__":
    build()
