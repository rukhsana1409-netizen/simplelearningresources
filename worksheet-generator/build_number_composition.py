"""Number Composition & Decomposition -- Kindergarten Math.

Page 1 (only): Break Apart 5.
Visual part-part-whole: 5 squares split into two color groups.
No number bonds, no + equations on this introductory page.

REVIEW BUILD -- do not lock, finalize, commit or push until user approves.
"""

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
AMBER = HexColor("#E8A93D")
MARGIN = 40

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "kindergarten", "math", "number-composition",
                   "number-composition-review.pdf")

PACK_TITLE = "Number Composition & Decomposition"


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
# Page 1 -- Break Apart 5
# ---------------------------------------------------------------------------
P1_PARTS = [(0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0)]


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Break Apart 5")
    draw_instruction(pdf, "Count each part. Write how many.")

    box_w, box_h = 256, 150
    xs = (40, 316)
    tops = (600, 432, 264)
    sq = 44
    for k, (n_teal, n_amber) in enumerate(P1_PARTS):
        x = xs[k % 2]
        top = tops[k // 2]
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # connected strip of 5 squares, split into two color groups
        sx = x + (box_w - 5 * sq) / 2
        sy = top - 22 - sq
        for i in range(5):
            pdf.setFillColor(TEAL if i < n_teal else AMBER)
            pdf.rect(sx + i * sq, sy, sq, sq, fill=1, stroke=0)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.roundRect(sx, sy, 5 * sq, sq, 8, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        for i in range(1, 5):
            pdf.line(sx + i * sq, sy + 3, sx + i * sq, sy + sq - 3)
        # sentence with two color-matched writing boxes
        cy = top - 112
        pdf.setFont("Helvetica", 15)
        box1_w = 38
        and_w = pdf.stringWidth("and ", "Helvetica", 15)
        box2_w = 38
        tail = " make 5."
        total = box1_w + 6 + and_w + 6 + box2_w + 8 + \
            pdf.stringWidth(tail, "Helvetica", 15)
        bx = x + (box_w - total) / 2
        for j, color in enumerate((TEAL, AMBER)):
            ox = bx + j * (box1_w + 6 + and_w + 6)
            pdf.setFillColor(white)
            pdf.setStrokeColor(color)
            pdf.setLineWidth(1.8)
            pdf.roundRect(ox, cy - 20, 38, 40, 8, stroke=1, fill=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 15)
        pdf.drawString(bx + box1_w + 6, cy - 5, "and ")
        pdf.drawString(bx + box1_w + 6 + and_w + 6 + box2_w + 8, cy - 5, tail)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Number Bonds to 5
# ---------------------------------------------------------------------------
# (left_part, right_part); None = blank for the child. First bond is a
# worked example introducing the structure.
P2_BONDS = [
    (2, 3, True),
    (0, None, False),
    (None, 4, False),
    (3, None, False),
    (None, 1, False),
    (5, None, False),
]


def draw_bond(pdf, x, top, left, right, is_example, whole=5,
              r_whole=27, r_part=25):
    pcx = x + 128
    # whole
    pdf.setFillColor(TEAL)
    pdf.circle(pcx, top - 48, r_whole, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawCentredString(pcx, top - 57, str(whole))
    # connectors to the parts
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(2)
    pdf.line(pcx - 15, top - 71, x + 86, top - 90)
    pdf.line(pcx + 15, top - 71, x + 170, top - 90)
    # parts
    for cx, value in ((x + 74, left), (x + 182, right)):
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.circle(cx, top - 115, r_part, fill=1, stroke=1)
        if value is not None:
            pdf.setFillColor(TEAL if is_example else INK)
            pdf.setFont("Helvetica-Bold", 24)
            pdf.drawCentredString(cx, top - 123, str(value))


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Number Bonds to 5")
    draw_instruction(pdf, "5 is the whole. Write the missing part.")

    box_w, box_h = 256, 150
    xs = (40, 316)
    tops = (600, 432, 264)
    for k, (left, right, is_example) in enumerate(P2_BONDS):
        x = xs[k % 2]
        top = tops[k // 2]
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        if is_example:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawCentredString(x + box_w / 2, top - 20, "EXAMPLE")
        draw_bond(pdf, x, top - (8 if is_example else 0),
                  left, right, is_example)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Ways to Make 5
# ---------------------------------------------------------------------------
def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Ways to Make 5")
    draw_instruction(pdf, "Show different ways to make 5.")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 608, "The two parts make 5.")

    box_w, box_h = 256, 150
    xs = (40, 316)
    tops = (588, 420, 252)
    for k in range(6):
        x = xs[k % 2]
        top = tops[k // 2]
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # whole 5, both parts blank for the child
        draw_bond(pdf, x, top, None, None, False, r_part=28)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Make 5: Addition Equations
# ---------------------------------------------------------------------------
P4_PROBLEMS = [
    (0, None),
    (None, 4),
    (3, None),
    (None, 1),
    (2, None),
    (None, 0),
]


def draw_equation(pdf, cx, cy, left, right, box_w=54, box_h=62, size=26):
    pdf.setFont("Helvetica-Bold", size)
    plus_w = pdf.stringWidth("+", "Helvetica-Bold", size)
    eq_w = pdf.stringWidth("= 5", "Helvetica-Bold", size)
    gap = 8
    total = 2 * box_w + plus_w + eq_w + 4 * gap
    bx = cx - total / 2
    box1_x = bx
    plus_x = bx + box_w + gap
    box2_x = plus_x + plus_w + gap
    eq_x = box2_x + box_w + gap
    for ox, value in ((box1_x, left), (box2_x, right)):
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.roundRect(ox, cy - box_h / 2, box_w, box_h, 8, stroke=1, fill=1)
        if value is not None:
            pdf.setFillColor(INK)
            pdf.drawCentredString(ox + box_w / 2, cy - 9, str(value))
    pdf.setFillColor(INK)
    pdf.drawString(plus_x, cy - 9, "+")
    pdf.drawString(eq_x, cy - 9, "= 5")


def draw_mini_bond(pdf, x, top, left, right):
    # small completed bond for card 1; fits ABOVE the equation zone
    pcx = x + 128
    pdf.setFillColor(TEAL)
    pdf.circle(pcx, top - 23, 13, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(pcx, top - 28, "5")
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1.6)
    pdf.line(pcx - 8, top - 34, x + 105, top - 43)
    pdf.line(pcx + 8, top - 34, x + 151, top - 43)
    for cx, value in ((x + 100, left), (x + 156, right)):
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.4)
        pdf.circle(cx, top - 52, 11, fill=1, stroke=1)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawCentredString(cx, top - 56, str(value))


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Make 5: Addition Equations")
    draw_instruction(pdf, "Write the missing number to make 5.")

    box_w, box_h = 256, 165
    xs = (40, 316)
    tops = (600, 423, 246)
    for k, (left, right) in enumerate(P4_PROBLEMS):
        x = xs[k % 2]
        top = tops[k // 2]
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        if k == 0:
            # first card: mini bond example above; equation layout untouched
            draw_mini_bond(pdf, x, top, 0, 5)
        # ONE identical equation template for every card
        draw_equation(pdf, x + box_w / 2, top - 101, left, right)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Break Apart 6
# ---------------------------------------------------------------------------
P5_PARTS = [(0, 6), (1, 5), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0)]


# Page 5 activity colors (bars + matching box outlines only)
P5_BLUE = HexColor("#8AB6E6")
P5_CORAL = HexColor("#F7A072")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Break Apart 6")
    draw_instruction(pdf, "Count each part. Write how many.")

    box_w, box_h = 256, 118
    xs = (40, 316)
    tops = (600, 474, 348, 222)
    sq = 38
    for k, (n_teal, n_amber) in enumerate(P5_PARTS):
        # 2-column grid; the 7th panel is centered on its row
        if k == 6:
            x = (PAGE_WIDTH - box_w) / 2
        else:
            x = xs[k % 2]
        top = tops[k // 2]
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # connected strip of 6 squares, split into two color groups
        sx = x + (box_w - 6 * sq) / 2
        sy = top - 18 - sq
        for i in range(6):
            pdf.setFillColor(P5_BLUE if i < n_teal else P5_CORAL)
            pdf.rect(sx + i * sq, sy, sq, sq, fill=1, stroke=0)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.roundRect(sx, sy, 6 * sq, sq, 8, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        for i in range(1, 6):
            pdf.line(sx + i * sq, sy + 3, sx + i * sq, sy + sq - 3)
        # sentence with two color-matched writing boxes
        cy = top - 92
        pdf.setFont("Helvetica", 15)
        box_wd = 38
        and_w = pdf.stringWidth("and ", "Helvetica", 15)
        tail = " make 6."
        total = box_wd + 6 + and_w + 6 + box_wd + 8 + \
            pdf.stringWidth(tail, "Helvetica", 15)
        bx = x + (box_w - total) / 2
        for j, color in enumerate((P5_BLUE, P5_CORAL)):
            ox = bx + j * (box_wd + 6 + and_w + 6)
            pdf.setFillColor(white)
            pdf.setStrokeColor(color)
            pdf.setLineWidth(1.8)
            pdf.roundRect(ox, cy - 20, 38, 40, 8, stroke=1, fill=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 15)
        pdf.drawString(bx + box_wd + 6, cy - 5, "and ")
        pdf.drawString(bx + box_wd + 6 + and_w + 6 + box_wd + 8, cy - 5, tail)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 6 -- Number Bonds to 6
# ---------------------------------------------------------------------------
P6_BONDS = [
    (2, 4, True),
    (0, None, False),
    (None, 5, False),
    (4, None, False),
    (None, 3, False),
    (6, None, False),
]


def build_p6_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Number Bonds to 6")
    draw_instruction(pdf, "6 is the whole. Write the missing part.")

    box_w, box_h = 256, 150
    xs = (40, 316)
    tops = (600, 432, 264)
    for k, (left, right, is_example) in enumerate(P6_BONDS):
        x = xs[k % 2]
        top = tops[k // 2]
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        if is_example:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawCentredString(x + box_w / 2, top - 20, "EXAMPLE")
        draw_bond(pdf, x, top - (8 if is_example else 0),
                  left, right, is_example, whole=6)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Pages 8-10 -- Number Bonds to 8, 9, 10 (one page per number)
# ---------------------------------------------------------------------------
def _build_bonds_page(path, subtitle, whole, bonds):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, subtitle)
    draw_instruction(pdf, "%d is the whole. Write the missing part." % whole)

    box_w, box_h = 256, 150
    xs = (40, 316)
    tops = (600, 432, 264)
    for k, (left, right, is_example) in enumerate(bonds):
        x = xs[k % 2]
        top = tops[k // 2]
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        if is_example:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawCentredString(x + box_w / 2, top - 20, "EXAMPLE")
        draw_bond(pdf, x, top - (8 if is_example else 0),
                  left, right, is_example, whole=whole)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# every distinct pair for 8: 0+8, 1+7, 2+6, 3+5, 4+4
P8_BONDS = [
    (3, 5, True),
    (None, 7, False),   # 1 and 7
    (2, None, False),   # 2 and 6
    (4, None, False),   # 4 and 4
    (None, 5, False),   # 3 and 5
    (0, None, False),   # 0 and 8
]


def build_p8_page(path):
    _build_bonds_page(path, "Number Bonds to 8", 8, P8_BONDS)


# every distinct pair for 9: 0+9, 1+8, 2+7, 3+6, 4+5
P9_BONDS = [
    (4, 5, True),
    (None, 8, False),   # 1 and 8
    (2, None, False),   # 2 and 7
    (None, 6, False),   # 3 and 6
    (7, None, False),   # 7 and 2
    (0, None, False),   # 0 and 9
]


def build_p9_page(path):
    _build_bonds_page(path, "Number Bonds to 9", 9, P9_BONDS)


# every distinct pair for 10: 0+10, 1+9, 2+8, 3+7, 4+6, 5+5
P10_BONDS = [
    (5, 5, True),
    (None, 9, False),   # 1 and 9
    (2, None, False),   # 2 and 8
    (None, 7, False),   # 3 and 7
    (4, None, False),   # 4 and 6
    (0, None, False),   # 0 and 10
]


def build_p10_page(path):
    _build_bonds_page(path, "Number Bonds to 10", 10, P10_BONDS)


# ---------------------------------------------------------------------------
# Page 7 -- Break Apart 7 & 8
# ---------------------------------------------------------------------------
# (number, teal_part, amber_part)
P7_BARS = [
    (7, 1, 6), (7, 2, 5), (7, 3, 4), (7, 0, 7),
    (8, 1, 7), (8, 2, 6), (8, 4, 4), (8, 0, 8),
]


def _break_apart_bar(pdf, x, top, box_w, whole, n_teal, sq):
    n = whole
    sx = x + (box_w - n * sq) / 2
    sy = top - 16 - sq
    for i in range(n):
        pdf.setFillColor(TEAL if i < n_teal else AMBER)
        pdf.rect(sx + i * sq, sy, sq, sq, fill=1, stroke=0)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.roundRect(sx, sy, n * sq, sq, 8, stroke=1, fill=0)
    pdf.setLineWidth(1.2)
    for i in range(1, n):
        pdf.line(sx + i * sq, sy + 3, sx + i * sq, sy + sq - 3)
    # sentence with two color-matched writing boxes
    cy = top - 88
    pdf.setFont("Helvetica", 15)
    box_w2 = 34
    and_w = pdf.stringWidth("and ", "Helvetica", 15)
    tail = " make %d." % whole
    total = box_w2 + 6 + and_w + 6 + box_w2 + 8 + \
        pdf.stringWidth(tail, "Helvetica", 15)
    bx = x + (box_w - total) / 2
    for j, color in enumerate((TEAL, AMBER)):
        ox = bx + j * (box_w2 + 6 + and_w + 6)
        pdf.setFillColor(white)
        pdf.setStrokeColor(color)
        pdf.setLineWidth(1.8)
        pdf.roundRect(ox, cy - 18, box_w2, 36, 8, stroke=1, fill=1)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 15)
    pdf.drawString(bx + box_w2 + 6, cy - 4, "and ")
    pdf.drawString(bx + box_w2 + 6 + and_w + 6 + box_w2 + 8, cy - 4, tail)


def build_p7_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Break Apart 7 & 8")
    draw_instruction(pdf, "Count each part. Write how many.")

    box_w, box_h = 256, 120
    sq = 28
    for s, label in enumerate(("Break Apart 7", "Break Apart 8")):
        x = 40 + s * 276
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawCentredString(x + box_w / 2, 604, label)
        for k in range(4):
            whole, n_teal, n_amber = P7_BARS[s * 4 + k]
            top = 576 - k * 130
            pdf.setFillColor(HexColor("#F7FAFC"))
            pdf.setStrokeColor(HexColor("#D5DEE8"))
            pdf.setLineWidth(1.4)
            pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1,
                          fill=1)
            _break_apart_bar(pdf, x, top, box_w, whole, n_teal, sq)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 8 -- Break Apart 9 & 10
# ---------------------------------------------------------------------------
# (number, teal_part, amber_part)
P8_BARS = [
    (9, 1, 8), (9, 2, 7), (9, 4, 5), (9, 0, 9),
    (10, 1, 9), (10, 2, 8), (10, 5, 5), (10, 0, 10),
]


def build_p8_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Break Apart 9 & 10")
    draw_instruction(pdf, "Count each part. Write how many.")

    box_w, box_h = 256, 120
    sq = 24  # 10 squares must fit the card
    for s, label in enumerate(("Break Apart 9", "Break Apart 10")):
        x = 40 + s * 276
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawCentredString(x + box_w / 2, 604, label)
        for k in range(4):
            whole, n_teal, n_amber = P8_BARS[s * 4 + k]
            top = 576 - k * 130
            pdf.setFillColor(HexColor("#F7FAFC"))
            pdf.setStrokeColor(HexColor("#D5DEE8"))
            pdf.setLineWidth(1.4)
            pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1,
                          fill=1)
            _break_apart_bar(pdf, x, top, box_w, whole, n_teal, sq)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 9 -- Number Bonds to 7 & 8 (supported: one part given)
# ---------------------------------------------------------------------------
# (left_part, right_part, is_example); None = blank for the child
P9_SECTIONS = [
    ("Number Bonds to 7", 7, [
        (2, 5, True),
        (3, None, False),   # 3 and 4
        (None, 6, False),   # 1 and 6
        (0, None, False),   # 0 and 7
    ]),
    ("Number Bonds to 8", 8, [
        (4, 4, True),
        (2, None, False),   # 2 and 6
        (None, 7, False),   # 1 and 7
        (0, None, False),   # 0 and 8
    ]),
]


def _draw_bond_sm(pdf, x, top, left, right, is_example, whole):
    pcx = x + 128
    if is_example:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawCentredString(pcx, top - 16, "EXAMPLE")
    # whole
    pdf.setFillColor(TEAL)
    pdf.circle(pcx, top - 52, 23, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(pcx, top - 60, str(whole))
    # connectors to the parts
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(2)
    pdf.line(pcx - 13, top - 72, x + 88, top - 82)
    pdf.line(pcx + 13, top - 72, x + 168, top - 82)
    # parts
    for cx, value in ((x + 76, left), (x + 180, right)):
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.circle(cx, top - 98, 21, fill=1, stroke=1)
        if value is not None:
            pdf.setFillColor(TEAL if is_example else INK)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawCentredString(cx, top - 105, str(value))


def build_p9_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Number Bonds to 7 & 8")
    draw_instruction(pdf, "The top number is the whole. Write the missing part.")

    box_w, box_h = 256, 128
    for s, (label, whole, bonds) in enumerate(P9_SECTIONS):
        x = 40 + s * 276
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawCentredString(x + box_w / 2, 608, label)
        for k, (left, right, is_example) in enumerate(bonds):
            top = 586 - k * 135
            pdf.setFillColor(HexColor("#F7FAFC"))
            pdf.setStrokeColor(HexColor("#D5DEE8"))
            pdf.setLineWidth(1.4)
            pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1,
                          fill=1)
            _draw_bond_sm(pdf, x, top, left, right, is_example, whole)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 10 -- Number Bonds to 9 & 10 (supported: one part given)
# ---------------------------------------------------------------------------
P10_SECTIONS = [
    ("Number Bonds to 9", 9, [
        (4, 5, True),
        (2, None, False),   # 2 and 7
        (None, 8, False),   # 1 and 8
        (0, None, False),   # 0 and 9
    ]),
    ("Number Bonds to 10", 10, [
        (5, 5, True),
        (4, None, False),   # 4 and 6
        (None, 9, False),   # 1 and 9
        (0, None, False),   # 0 and 10
    ]),
]


def build_p10_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Number Bonds to 9 & 10")
    draw_instruction(pdf, "The top number is the whole. Write the missing part.")

    box_w, box_h = 256, 128
    for s, (label, whole, bonds) in enumerate(P10_SECTIONS):
        x = 40 + s * 276
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawCentredString(x + box_w / 2, 608, label)
        for k, (left, right, is_example) in enumerate(bonds):
            top = 586 - k * 135
            pdf.setFillColor(HexColor("#F7FAFC"))
            pdf.setStrokeColor(HexColor("#D5DEE8"))
            pdf.setLineWidth(1.4)
            pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1,
                          fill=1)
            _draw_bond_sm(pdf, x, top, left, right, is_example, whole)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 11 -- Ways to Make 7-10 (independent: both parts blank)
# ---------------------------------------------------------------------------
P11_WHOLES = (7, 7, 8, 8, 9, 9, 10, 10)


def build_p11_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Ways to Make 7-10")
    draw_instruction(pdf, "Write two parts that make the whole.")

    box_w, box_h = 256, 128
    xs = (40, 316)
    tops = (586, 451, 316, 181)
    for k, whole in enumerate(P11_WHOLES):
        x = xs[k % 2]
        top = tops[k // 2]
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        _draw_bond_sm(pdf, x, top, None, None, False, whole)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    # (title, builder, locked) -- pages 1-6 APPROVED & LOCKED 2026-10-05
    ("Break Apart 5", build_p1_page, True),
    ("Number Bonds to 5", build_p2_page, True),
    ("Ways to Make 5", build_p3_page, True),
    ("Make 5: Addition Equations", build_p4_page, True),
    ("Break Apart 6", build_p5_page, True),
    ("Number Bonds to 6", build_p6_page, True),
    ("Break Apart 7 & 8", build_p7_page, True),  # APPROVED 2026-10-08
    ("Break Apart 9 & 10", build_p8_page, True),  # APPROVED 2026-10-08
    ("Number Bonds to 7 & 8", build_p9_page, True),  # APPROVED 2026-10-08
    ("Number Bonds to 9 & 10", build_p10_page, True),  # APPROVED 2026-10-08
    ("Ways to Make 7-10", build_p11_page, True),  # APPROVED 2026-10-08
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="number-composition-") as tmp:
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
