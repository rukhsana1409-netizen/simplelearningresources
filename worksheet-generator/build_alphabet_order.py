"""Build the 2-page ABC Order & Missing Letters resource (final).

Preschool Reading & Language:
- Page 1 (ABC Order): five rows of scrambled letter tiles; the child
  writes them in ABC order in the dashed answer boxes.
- Page 2 (Missing Letters): four short sequences with one missing
  letter each; the child writes the missing letter in the box.
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

# Page 1: scrambled tile groups (letters shown out of order on purpose).
GROUPS = [
    {"cards": ["C", "A", "B"], "colors": [CORAL, TEAL, GOLD]},
    {"cards": ["F", "D", "E"], "colors": [PURPLE, BLUE, GREEN]},
    {"cards": ["I", "G", "H"], "colors": [ORANGE, CORAL, TEAL]},
    {"cards": ["L", "J", "K"], "colors": [GOLD, PURPLE, BLUE]},
    {"cards": ["O", "M", "N"], "colors": [GREEN, ORANGE, PURPLE]},
]
TILE = 68
TILE_GAP = 14
ROW_LEFT = 48          # left edge of the scrambled tiles
ARROW_CX = 310         # center of the arrow between tiles and answer boxes
BOX_LEFT = 340         # left edge of the answer boxes
ROW_YS = [520, 420, 320, 220, 120]

# Page 2: short sequences, one missing letter each (None = writing box).
SEQUENCES = [
    {"items": ["A", "B", None, "D"], "colors": [CORAL, ORANGE, None, GREEN]},
    {"items": ["E", None, "G", "H"], "colors": [PURPLE, None, TEAL, BLUE]},
    {"items": [None, "J", "K", "L"], "colors": [None, GOLD, CORAL, GREEN]},
    {"items": ["M", "N", "O", None], "colors": [TEAL, PURPLE, ORANGE, None]},
]
SEQ_GAP = 96
WRITE_BOX = 78


def draw_tile(pdf, cx, cy, letter, bg):
    """A colorful movable-looking letter tile."""
    x, y = cx - TILE / 2, cy - TILE / 2
    pdf.setFillColor(bg)
    pdf.roundRect(x, y, TILE, TILE, 14, fill=1, stroke=0)
    # soft highlight for a playful look
    pdf.setFillColor(white)
    pdf.setFillAlpha(0.18)
    pdf.circle(cx - 12, cy + 13, 11, fill=1, stroke=0)
    pdf.setFillAlpha(1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 46)
    pdf.drawCentredString(cx, cy - 17, letter)


def draw_answer_box(pdf, cx, cy):
    """Large empty dashed box where the child writes the next letter."""
    x, y = cx - TILE / 2, cy - TILE / 2
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(2.5)
    pdf.setDash(8, 6)
    pdf.roundRect(x, y, TILE, TILE, 14, fill=0, stroke=1)
    pdf.setDash()


def draw_arrow(pdf, cx, cy):
    """Simple arrow pointing from the tiles to the answer boxes."""
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setFillColor(TEAL_DARK)
    pdf.setLineWidth(4)
    pdf.setLineCap(1)
    pdf.line(cx - 18, cy, cx + 12, cy)
    p = pdf.beginPath()
    p.moveTo(cx + 22, cy)
    p.lineTo(cx + 8, cy - 9)
    p.lineTo(cx + 8, cy + 9)
    p.close()
    pdf.drawPath(p, fill=1, stroke=0)


def draw_order_page(pdf):
    draw_header(pdf, {"title": f"{TITLE}: ABC Order",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Put the letters in ABC order. Write them in the boxes.",
    )

    for gi, group in enumerate(GROUPS):
        cy = ROW_YS[gi]
        for i, (letter, color) in enumerate(zip(group["cards"], group["colors"])):
            cx = ROW_LEFT + TILE / 2 + i * (TILE + TILE_GAP)
            draw_tile(pdf, cx, cy, letter, color)
        draw_arrow(pdf, ARROW_CX, cy)
        for i in range(3):
            cx = BOX_LEFT + TILE / 2 + i * (TILE + TILE_GAP)
            draw_answer_box(pdf, cx, cy)

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
        "abc-order-missing-letters.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} | Learning Made Simple")
    pdf.setAuthor("Learning Made Simple")
    draw_order_page(pdf)
    draw_missing_page(pdf)
    pdf.save()
    print(f"wrote {out} (2 pages)")


if __name__ == "__main__":
    build()
