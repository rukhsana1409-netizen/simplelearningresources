"""Build the Match Big & Little Letters resource (A-Z).

Preschool Reading & Language: children draw a line from each uppercase
letter to its matching lowercase letter. Lowercase order is shuffled so
answers never sit directly across from their uppercase match, and no
matching pair shares a badge color (so children match by letter shape,
not by color).

Five pairs per page; the final U-Z page holds six pairs.
"""

import os
import sys

from reportlab.lib.colors import white
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_worksheet import (
    BLUE,
    CORAL,
    GOLD,
    GREEN,
    INK,
    MARGIN,
    ORANGE,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    PURPLE,
    TEAL,
    TEAL_DARK,
    draw_footer,
    draw_header,
)

TITLE = "Match Big & Little Letters"

# (uppercase rows top-to-bottom, shuffled lowercase rows, badge colors)
# Colors are arranged so no pair shares a color and no row shares a
# color across columns.
PAGES = [
    {
        "focus": "A\u2013E",
        "upper": ["A", "B", "C", "D", "E"],
        "upper_colors": [CORAL, ORANGE, GOLD, GREEN, BLUE],
        "lower": ["e", "a", "d", "b", "c"],
        "lower_colors": [PURPLE, TEAL, BLUE, CORAL, GREEN],
    },
    {
        "focus": "F\u2013J",
        "upper": ["F", "G", "H", "I", "J"],
        "upper_colors": [PURPLE, CORAL, BLUE, GREEN, ORANGE],
        "lower": ["i", "f", "j", "h", "g"],
        "lower_colors": [GOLD, TEAL, GREEN, PURPLE, BLUE],
    },
    {
        "focus": "K\u2013O",
        "upper": ["K", "L", "M", "N", "O"],
        "upper_colors": [TEAL, GOLD, CORAL, BLUE, PURPLE],
        "lower": ["n", "k", "o", "l", "m"],
        "lower_colors": [GREEN, ORANGE, BLUE, CORAL, GOLD],
    },
    {
        "focus": "P\u2013T",
        "upper": ["P", "Q", "R", "S", "T"],
        "upper_colors": [ORANGE, PURPLE, TEAL, CORAL, GREEN],
        "lower": ["s", "p", "t", "q", "r"],
        "lower_colors": [BLUE, GOLD, CORAL, TEAL, PURPLE],
    },
    {
        "focus": "U\u2013Z",
        "upper": ["U", "V", "W", "X", "Y", "Z"],
        "upper_colors": [BLUE, GOLD, GREEN, CORAL, PURPLE, ORANGE],
        "lower": ["w", "z", "u", "y", "v", "x"],
        "lower_colors": [TEAL, CORAL, PURPLE, GOLD, GREEN, BLUE],
    },
]

LEFT_X = 175
RIGHT_X = PAGE_WIDTH - 175
BADGE_R = 42
ROW_YS = [505, 410, 315, 220, 125]
# The final U-Z page holds six pairs; badges shrink slightly so all rows
# fit with the same clean spacing everywhere else unchanged.
BADGE_R_6 = 38
ROW_YS_6 = [505, 421, 337, 253, 169, 85]

def draw_badge(pdf, cx, cy, letter, bg, r=BADGE_R, font_size=56):
    pdf.setFillColor(bg)
    pdf.circle(cx, cy, r, fill=1, stroke=0)
    # soft highlight for a playful look
    pdf.setFillColor(white)
    pdf.setFillAlpha(0.18)
    pdf.circle(cx - 12, cy + 14, 13, fill=1, stroke=0)
    pdf.setFillAlpha(1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawCentredString(cx, cy - font_size * 0.357, letter)


def draw_match_page(pdf, spec):
    data = {
        "title": f"{TITLE}: {spec['focus']}",
        "subtitle": "Preschool Reading & Language",
    }
    draw_header(pdf, data)

    # Minimal instruction.
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Draw a line from each BIG letter to its little match.",
    )

    # Column labels.
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(LEFT_X, 560, "BIG")
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(RIGHT_X, 560, "little")

    six = len(spec["upper"]) == 6
    row_ys = ROW_YS_6 if six else ROW_YS
    badge_r = BADGE_R_6 if six else BADGE_R
    font_size = 50 if six else 56
    for i, y in enumerate(row_ys):
        draw_badge(pdf, LEFT_X, y, spec["upper"][i], spec["upper_colors"][i],
                   r=badge_r, font_size=font_size)
        draw_badge(pdf, RIGHT_X, y, spec["lower"][i], spec["lower_colors"][i],
                   r=badge_r, font_size=font_size)

    draw_footer(pdf)
    pdf.showPage()


def build(out_path):
    pdf = canvas.Canvas(out_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    for spec in PAGES:
        draw_match_page(pdf, spec)
    pdf.save()
    print(f"wrote {out_path} ({len(PAGES)} pages)")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "match-big-little-letters-prototype.pdf",
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build(out)
