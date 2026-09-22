"""Build the 2-page Match Big & Little Letters prototype (A-E, F-J).

Preschool Reading & Language: children draw a line from each uppercase
letter to its matching lowercase letter. Lowercase order is shuffled so
answers never sit directly across from their uppercase match, and no
matching pair shares a badge color (so children match by letter shape,
not by color).

Prototype only: pages for A-E and F-J.
"""

import math
import os
import sys

from reportlab.lib.colors import Color, HexColor, white
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
]

LEFT_X = 175
RIGHT_X = PAGE_WIDTH - 175
BADGE_R = 42
ROW_YS = [505, 410, 315, 220, 125]

SOFT = [  # pale confetti colors (hex, alpha)
    ("#E98779", 0.30), ("#F4B63E", 0.35), ("#007C70", 0.25), ("#AA91C4", 0.28),
    ("#82B7D8", 0.30), ("#72AE72", 0.30), ("#E9A25D", 0.32),
]


def _with_alpha(hexstr, alpha):
    base = HexColor(hexstr)
    return Color(base.red, base.green, base.blue, alpha=alpha)


def draw_sparkle(pdf, x, y, r, color, alpha=0.35):
    """Small 4-point star decoration."""
    pdf.setFillColor(_with_alpha(color, alpha))
    ir = r * 0.30
    pts = []
    for k in range(8):
        ang = math.pi / 2 + k * math.pi / 4
        rad = r if k % 2 == 0 else ir
        pts.append((x + rad * math.cos(ang), y + rad * math.sin(ang)))
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.drawPath(p, fill=1, stroke=0)


def draw_dot(pdf, x, y, r, color, alpha=0.30):
    pdf.setFillColor(_with_alpha(color, alpha))
    pdf.circle(x, y, r, fill=1, stroke=0)


def draw_decorations(pdf):
    """Playful confetti around the margins; the middle stays clear for lines."""
    spots = [
        # (x, y, kind, size, color_index)
        (70, 560, "sparkle", 12, 1), (92, 470, "dot", 7, 0),
        (62, 380, "dot", 9, 3), (95, 285, "sparkle", 10, 5),
        (68, 190, "dot", 7, 2), (90, 90, "sparkle", 11, 6),
        (542, 560, "dot", 8, 4), (520, 465, "sparkle", 12, 0),
        (550, 375, "dot", 7, 1), (522, 280, "sparkle", 10, 2),
        (545, 185, "dot", 9, 5), (520, 90, "sparkle", 11, 3),
        (300, 590, "dot", 6, 6), (330, 590, "sparkle", 8, 4),
    ]
    for x, y, kind, size, ci in spots:
        color, alpha = SOFT[ci]
        if kind == "sparkle":
            draw_sparkle(pdf, x, y, size, color, alpha)
        else:
            draw_dot(pdf, x, y, size, color, alpha)


def draw_badge(pdf, cx, cy, letter, bg):
    pdf.setFillColor(bg)
    pdf.circle(cx, cy, BADGE_R, fill=1, stroke=0)
    # soft highlight for a playful look
    pdf.setFillColor(white)
    pdf.setFillAlpha(0.18)
    pdf.circle(cx - 12, cy + 14, 13, fill=1, stroke=0)
    pdf.setFillAlpha(1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 56)
    pdf.drawCentredString(cx, cy - 20, letter)


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

    draw_decorations(pdf)

    for i, y in enumerate(ROW_YS):
        draw_badge(pdf, LEFT_X, y, spec["upper"][i], spec["upper_colors"][i])
        draw_badge(pdf, RIGHT_X, y, spec["lower"][i], spec["lower_colors"][i])

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
