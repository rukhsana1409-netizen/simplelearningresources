"""Comparing Numbers -- Kindergarten Math.

Page 1 (only): Which Has More? Which Has Fewer?
Picture comparison: circle the group with more / fewer. Quantities 1-10.
No >, <, = symbols. No equations.

REVIEW BUILD -- do not lock, finalize, commit or push until user approves.
"""

import math
import os
import subprocess
import tempfile

from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
INK = HexColor("#202A33")
NAVY = HexColor("#1E3A5F")
MARGIN = 40

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "kindergarten", "math", "comparing-numbers",
                   "comparing-numbers-review.pdf")

PACK_TITLE = "Comparing Numbers"


# ---------------------------------------------------------------------------
# Brand header / footer / instruction (Learn My Letters style)
# ---------------------------------------------------------------------------
def draw_logo(pdf, x, y):
    pdf.setFillColor(TEAL)
    pdf.circle(x + 18, y + 26, 7, fill=1, stroke=0)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(x + 18, y + 18, x + 18, y + 4)
    pdf.line(x + 18, y + 14, x + 6, y + 5)
    pdf.line(x + 18, y + 14, x + 30, y + 5)
    pdf.setLineWidth(1.3)
    pdf.line(x + 10, y + 8, x + 26, y + 8)
    pdf.setFillColor(HexColor("#F4B63E"))
    pdf.circle(x + 18, y + 38, 4, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(x + 38, y + 30, "LEARNING")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(x + 38, y + 16, "MADE SIMPLE")


def draw_header(pdf, title, subtitle):
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
    size = 30
    pdf.setFont("Helvetica-Bold", size)
    max_w = PAGE_WIDTH - MARGIN - title_x
    while pdf.stringWidth(focus, "Helvetica-Bold", size) > max_w and size > 18:
        size -= 1
        pdf.setFont("Helvetica-Bold", size)
    pdf.drawString(title_x, PAGE_HEIGHT - 98, focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(title_x, PAGE_HEIGHT - 122, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    rule_y = PAGE_HEIGHT - 137
    pdf.line(MARGIN, rule_y, PAGE_WIDTH - MARGIN, rule_y)
    return rule_y


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF4F3"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#0E7C7B"))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(MARGIN, 26, "Learning Made Simple")
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1)
    pdf.line(190, 18, 190, 34)
    pdf.setFillColor(HexColor("#0E7C7B"))
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_WIDTH / 2 + 20, 26,
                          "Made with love for little learners.")
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(PAGE_WIDTH - MARGIN, 26,
                        "\u00a9 2026 Learning Made Simple")


def draw_instruction(pdf, text, size=15):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630, text)


# ---------------------------------------------------------------------------
# Simple vector objects (all drawn at the same size within a question)
# ---------------------------------------------------------------------------
def draw_apple(pdf, cx, cy, r):
    pdf.setFillColor(HexColor("#D94F3D"))
    pdf.circle(cx, cy, r, fill=1, stroke=0)
    pdf.setStrokeColor(HexColor("#8A5A2B"))
    pdf.setLineWidth(2.5)
    pdf.line(cx, cy + r * 0.8, cx + 2, cy + r * 1.3)
    pdf.setFillColor(HexColor("#4E9B47"))
    p = pdf.beginPath()
    p.moveTo(cx + 2, cy + r * 1.05)
    p.lineTo(cx + 11, cy + r * 1.2)
    p.lineTo(cx + 4, cy + r * 0.9)
    p.close()
    pdf.drawPath(p, fill=1, stroke=0)


def draw_star(pdf, cx, cy, r):
    p = pdf.beginPath()
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rad = r if i % 2 == 0 else r * 0.45
        x, y = cx + rad * math.cos(ang), cy + rad * math.sin(ang)
        if i == 0:
            p.moveTo(x, y)
        else:
            p.lineTo(x, y)
    p.close()
    pdf.setFillColor(HexColor("#F4B63E"))
    pdf.drawPath(p, fill=1, stroke=0)


def draw_ball(pdf, cx, cy, r):
    pdf.setFillColor(HexColor("#2A9D8F"))
    pdf.circle(cx, cy, r, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.circle(cx - r * 0.32, cy + r * 0.32, r * 0.2, fill=1, stroke=0)


def draw_heart(pdf, cx, cy, r):
    pdf.setFillColor(HexColor("#E86A92"))
    pdf.circle(cx - r * 0.36, cy + r * 0.18, r * 0.44, fill=1, stroke=0)
    pdf.circle(cx + r * 0.36, cy + r * 0.18, r * 0.44, fill=1, stroke=0)
    p = pdf.beginPath()
    p.moveTo(cx - r * 0.74, cy + r * 0.12)
    p.lineTo(cx + r * 0.74, cy + r * 0.12)
    p.lineTo(cx, cy - r * 0.78)
    p.close()
    pdf.drawPath(p, fill=1, stroke=0)


def draw_flower(pdf, cx, cy, r):
    pdf.setFillColor(HexColor("#B565D8"))
    for k in range(5):
        ang = math.radians(k * 72 - 90)
        pdf.circle(cx + r * 0.55 * math.cos(ang),
                   cy + r * 0.55 * math.sin(ang), r * 0.5, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#F4B63E"))
    pdf.circle(cx, cy, r * 0.36, fill=1, stroke=0)


DRAW = {
    "apple": draw_apple,
    "star": draw_star,
    "ball": draw_ball,
    "heart": draw_heart,
    "flower": draw_flower,
}


# ---------------------------------------------------------------------------
# Page 1 -- Which Has More? Which Has Fewer?
# ---------------------------------------------------------------------------
# (object, left_count, right_count, ask_more?)
P1_PROBLEMS = [
    ("apple", 4, 7, True),
    ("star", 8, 5, False),
    ("ball", 6, 3, True),
    ("heart", 6, 9, False),
    ("flower", 8, 7, True),
    ("apple", 5, 2, False),
]


def draw_group(pdf, kind, count, cx, grid_top):
    # top-aligned neat rows: every group starts on the same line so only
    # the quantity itself varies, never the alignment
    cols = min(count, 5)
    cell = 24
    r = 11
    y0 = grid_top - r - 2
    for i in range(count):
        gx = cx + (i % cols - (cols - 1) / 2) * cell
        gy = y0 - (i // cols) * cell
        DRAW[kind](pdf, gx, gy, r)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Which Has More? Which Has Fewer?")
    draw_instruction(pdf, "Circle the group with more or fewer.")

    box_w, box_h = 256, 165
    xs = (40, 316)
    tops = (600, 422, 244)
    for k, (kind, left_n, right_n, ask_more) in enumerate(P1_PROBLEMS):
        x = xs[k % 2]
        top = tops[k // 2]
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # question label
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawCentredString(
            x + box_w / 2, top - 24,
            "Circle the group with " + ("MORE." if ask_more else "FEWER."))
        # divider between the two groups
        mid = x + box_w / 2
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.2)
        pdf.line(mid, top - 38, mid, top - box_h + 12)
        # the two groups, top-aligned in neat rows with room to circle
        grid_top = top - 46
        draw_group(pdf, kind, left_n, x + box_w / 4, grid_top)
        draw_group(pdf, kind, right_n, x + 3 * box_w / 4, grid_top)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Which Number Is Greater? Which Is Smaller?
# ---------------------------------------------------------------------------
# (left, right, ask_greater?)
P2_PROBLEMS = [
    (3, 8, True),
    (9, 4, False),
    (7, 2, True),
    (5, 10, False),
    (7, 8, True),
    (10, 9, False),
    (9, 5, True),
    (2, 6, False),
]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Which Number Is Greater? Which Is Smaller?")
    draw_instruction(pdf, "Circle the greater or smaller number.")

    box_w, box_h = 256, 120
    xs = (40, 316)
    tops = (600, 472, 344, 216)
    for k, (left_n, right_n, ask_greater) in enumerate(P2_PROBLEMS):
        x = xs[k % 2]
        top = tops[k // 2]
        cy = top - box_h / 2
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # question label
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawCentredString(
            x + box_w / 2, top - 24,
            "Circle the " + ("GREATER" if ask_greater else "SMALLER")
            + " number.")
        # divider between the two numerals
        mid = x + box_w / 2
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.2)
        pdf.line(mid, top - 38, mid, top - box_h + 12)
        # two large numerals with generous circling space
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 44)
        pdf.drawCentredString(x + box_w / 4, cy - 22, str(left_n))
        pdf.drawCentredString(x + 3 * box_w / 4, cy - 22, str(right_n))

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Greater Than, Less Than, Equal To (teaching/reference)
# ---------------------------------------------------------------------------
P3_SYMBOLS = [
    (">", "greater than", "8 > 5"),
    ("<", "less than", "3 < 7"),
    ("=", "equal to", "6 = 6"),
]

P3_PRACTICE = [
    (4, 9),
    (7, 7),
    (6, 2),
]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Greater Than, Less Than, Equal To")
    draw_instruction(pdf, "Meet the comparison symbols!")

    # teaching rows: symbol badge + word + clear number example
    for k, (symbol, word, example) in enumerate(P3_SYMBOLS):
        top = 590 - k * 118
        cy = top - 52
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(MARGIN, top - 104, PAGE_WIDTH - 2 * MARGIN, 104, 12,
                      stroke=1, fill=1)
        # prominent symbol in a teal badge
        pdf.setFillColor(TEAL)
        pdf.circle(MARGIN + 72, cy, 30, fill=1, stroke=0)
        pdf.setFillColor(white)
        pdf.setFont("Helvetica-Bold", 40)
        pdf.drawCentredString(MARGIN + 72, cy - 14, symbol)
        # the word
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(MARGIN + 125, cy - 8, word)
        # the example equation
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 38)
        pdf.drawCentredString(MARGIN + 400, cy - 13, example)

    # simple visual explanation of the open side
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 218,
        "Tip: The wide side faces the greater number.")

    # guided practice: write the symbol in the middle cell
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 182, "Write >, <, or = in the box.")

    cell_w, cell_h = 48, 64
    for k, (left_n, right_n) in enumerate(P3_PRACTICE):
        x = 60 + k * 174
        cy = 118
        sy = cy - cell_h / 2
        for i in range(3):
            pdf.setFillColor(white)
            pdf.rect(x + i * cell_w, sy, cell_w, cell_h, fill=1, stroke=0)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawCentredString(x + 0.5 * cell_w, cy - 9, str(left_n))
        pdf.drawCentredString(x + 2.5 * cell_w, cy - 9, str(right_n))
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.roundRect(x, sy, 3 * cell_w, cell_h, 8, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        pdf.line(x + cell_w, sy + 3, x + cell_w, sy + cell_h - 3)
        pdf.line(x + 2 * cell_w, sy + 3, x + 2 * cell_w, sy + cell_h - 3)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Choose the Symbol
# ---------------------------------------------------------------------------
P4_PROBLEMS = [
    (4, 9),
    (7, 7),
    (6, 2),
    (3, 8),
    (10, 4),
    (5, 5),
    (2, 7),
    (9, 3),
]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Choose the Symbol")
    draw_instruction(pdf, "Write >, <, or = in the box.")

    box_w, box_h = 256, 120
    xs = (40, 316)
    tops = (600, 472, 344, 216)
    cell_w, cell_h = 48, 64
    for k, (left_n, right_n) in enumerate(P4_PROBLEMS):
        x = xs[k % 2]
        top = tops[k // 2]
        cy = top - box_h / 2
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # connected 3-cell strip: number | blank | number
        sx = x + (box_w - 3 * cell_w) / 2
        sy = cy - cell_h / 2
        for i in range(3):
            pdf.setFillColor(white)
            pdf.rect(sx + i * cell_w, sy, cell_w, cell_h, fill=1, stroke=0)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawCentredString(sx + 0.5 * cell_w, cy - 9, str(left_n))
        pdf.drawCentredString(sx + 2.5 * cell_w, cy - 9, str(right_n))
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.roundRect(sx, sy, 3 * cell_w, cell_h, 8, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        pdf.line(sx + cell_w, sy + 3, sx + cell_w, sy + cell_h - 3)
        pdf.line(sx + 2 * cell_w, sy + 3, sx + 2 * cell_w, sy + cell_h - 3)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Compare Numbers to 20
# ---------------------------------------------------------------------------
P5_PROBLEMS = [
    (12, 18),
    (15, 15),
    (19, 11),
    (14, 17),
    (20, 13),
    (16, 16),
    (11, 19),
    (18, 12),
]


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Compare Numbers to 20")
    draw_instruction(pdf, "Write >, <, or = in the box.")

    box_w, box_h = 256, 120
    xs = (40, 316)
    tops = (600, 472, 344, 216)
    cell_w, cell_h = 48, 64
    for k, (left_n, right_n) in enumerate(P5_PROBLEMS):
        x = xs[k % 2]
        top = tops[k // 2]
        cy = top - box_h / 2
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # connected 3-cell strip: number | blank | number
        sx = x + (box_w - 3 * cell_w) / 2
        sy = cy - cell_h / 2
        for i in range(3):
            pdf.setFillColor(white)
            pdf.rect(sx + i * cell_w, sy, cell_w, cell_h, fill=1, stroke=0)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawCentredString(sx + 0.5 * cell_w, cy - 9, str(left_n))
        pdf.drawCentredString(sx + 2.5 * cell_w, cy - 9, str(right_n))
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.roundRect(sx, sy, 3 * cell_w, cell_h, 8, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        pdf.line(sx + cell_w, sy + 3, sx + cell_w, sy + cell_h - 3)
        pdf.line(sx + 2 * cell_w, sy + 3, sx + 2 * cell_w, sy + cell_h - 3)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    # (title, builder, locked) -- ALL 5 PAGES APPROVED & LOCKED 2026-10-05
    ("Which Has More? Which Has Fewer?", build_p1_page, True),
    ("Which Number Is Greater? Which Is Smaller?", build_p2_page, True),
    ("Greater Than, Less Than, Equal To", build_p3_page, True),
    ("Choose the Symbol", build_p4_page, True),
    ("Compare Numbers to 20", build_p5_page, True),
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="comparing-numbers-") as tmp:
        parts = []
        for idx, (title, builder, locked) in enumerate(PAGES, start=1):
            path = os.path.join(tmp, "page-%d.pdf" % idx)
            builder(path)
            parts.append(path)
            print("built page %d: %s" % (idx, title))
        subprocess.run(["pdfunite"] + parts + [OUT], check=True,
                       capture_output=True)
    print("merged %d page(s) -> %s" % (len(parts), OUT))


if __name__ == "__main__":
    main()
