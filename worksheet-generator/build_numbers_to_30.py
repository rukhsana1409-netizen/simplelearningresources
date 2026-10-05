"""Numbers to 30 & Counting On -- Kindergarten Math.

Page 1 (only): Number Detective -- Numbers 0-30.
A light Kindergarten review of numeral recognition 0-30 in random order.
No tracing, no number writing, no counting objects.

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
MARGIN = 40

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "kindergarten", "math", "numbers-to-30",
                   "numbers-to-30-review.pdf")

PACK_TITLE = "Numbers to 100 & Counting On"


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
# Page 1 -- My 1-100 Number Chart (teaching/reference)
# ---------------------------------------------------------------------------
def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My 1\u2013100 Number Chart")
    draw_instruction(pdf, "Count from 1 to 100. What patterns do you notice?")

    x0, top = MARGIN, 600
    cell_w = (PAGE_WIDTH - 2 * MARGIN) / 10
    cell_h = 53
    # subtle alternating row bands
    for r in range(10):
        if r % 2 == 1:
            pdf.setFillColor(HexColor("#F7FAFC"))
            pdf.setStrokeColor(HexColor("#F7FAFC"))
            pdf.rect(x0, top - (r + 1) * cell_h, cell_w * 10, cell_h,
                     fill=1, stroke=0)
    # numerals
    for r in range(10):
        for c in range(10):
            value = r * 10 + c + 1
            cx = x0 + (c + 0.5) * cell_w
            cy = top - r * cell_h - cell_h / 2
            pdf.setFillColor(TEAL if value % 10 == 0 else INK)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawCentredString(cx, cy - 7, str(value))
    # grid lines
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1)
    for c in range(11):
        x = x0 + c * cell_w
        pdf.line(x, top - 10 * cell_h, x, top)
    for r in range(11):
        y = top - r * cell_h
        pdf.line(x0, y, x0 + 10 * cell_w, y)
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1.6)
    pdf.rect(x0, top - 10 * cell_h, cell_w * 10, cell_h * 10,
             fill=0, stroke=1)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Number Detective: Numbers 0-30 (unchanged, was Page 1)
# ---------------------------------------------------------------------------
# Fixed random order (seed 2015): 30 numbers from 0-30 (23 omitted;
# it is not a target). Perfect 5 x 6 grid, no two targets adjacent.
ORDER = [21, 17, 5, 22, 6, 14,
         3, 7, 12, 0, 18, 15,
         8, 10, 9, 26, 11, 19,
         25, 13, 16, 24, 29, 27,
         30, 4, 1, 28, 20, 2]

PROMPTS = [
    ("Circle", 27),
    ("Put a box around", 14),
    ("Color", 30),
    ("Underline", 22),
    ("Put a star beside", 24),
    ("Circle", 8),
]


def prompt_chip(pdf, x, top, w, h, action, number):
    pdf.setFillColor(HexColor("#EAF4F3"))
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - h, w, h, 10, stroke=1, fill=1)
    pdf.setFont("Helvetica", 13)
    aw = pdf.stringWidth(action, "Helvetica", 13)
    pdf.setFont("Helvetica-Bold", 20)
    nw = pdf.stringWidth(str(number), "Helvetica-Bold", 20)
    gap = 8
    total = aw + gap + nw
    sx = x + (w - total) / 2
    cy = top - h / 2
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(sx, cy - 5, action)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(sx + aw + gap, cy - 7, str(number))


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Number Detective \u2014 Numbers 0\u201330")
    draw_instruction(pdf, "Be a number detective! Find each number and mark it.")

    # 6 target prompts in 2 rows of 3
    for k, (action, number) in enumerate(PROMPTS):
        x = (40, 222, 404)[k % 3]
        top = 596 if k < 3 else 532
        prompt_chip(pdf, x, top, 168, 48, action, number)

    # number field: perfect 5 x 6 grid, generous even spacing.
    col_w = (PAGE_WIDTH - 2 * MARGIN) / 6
    tops = (460, 394, 328, 262, 196)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 30)
    for i, value in enumerate(ORDER):
        r, c = divmod(i, 6)
        cx = MARGIN + col_w * (c + 0.5)
        cy = tops[r] - 33
        pdf.drawCentredString(cx, cy - 10, str(value))

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Count On!
# ---------------------------------------------------------------------------
P3_STARTS = [16, 19, 28, 37, 49, 58, 69, 89]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Count On!")
    draw_instruction(pdf, "Start with the number. Write the next 4 numbers.")

    box_w, box_h = 260, 125
    xs = (40, 312)
    tops = (600, 472, 344, 216)
    for k, start in enumerate(P3_STARTS):
        x = xs[k % 2]
        top = tops[k // 2]
        cy = top - box_h / 2
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # starting number: visually distinct teal badge
        pdf.setFillColor(TEAL)
        pdf.circle(x + 31, cy, 21, fill=1, stroke=0)
        pdf.setFillColor(white)
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawCentredString(x + 31, cy - 8, str(start))
        # four large answer boxes for comfortable handwriting
        for b in range(4):
            bx = x + 60 + b * 49
            pdf.setFillColor(white)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(1.6)
            pdf.roundRect(bx, cy - 34, 43, 68, 8, stroke=1, fill=1)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Before & After
# ---------------------------------------------------------------------------
P4_NUMBERS = [17, 30, 42, 50, 63, 70, 84, 90]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Before & After")
    draw_instruction(pdf, "Write the number before and the number after.")

    box_w, box_h = 260, 125
    xs = (40, 312)
    tops = (600, 472, 344, 216)
    for k, number in enumerate(P4_NUMBERS):
        x = xs[k % 2]
        top = tops[k // 2]
        cy = top - box_h / 2
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # connected 3-cell strip: [blank][given][blank]
        strip_w, cell_w, cell_h = 168, 56, 68
        sx = x + (box_w - strip_w) / 2
        sy = cy - cell_h / 2
        for i in range(3):
            pdf.setFillColor(HexColor("#E3F2F0") if i == 1 else white)
            pdf.rect(sx + i * cell_w, sy, cell_w, cell_h, fill=1, stroke=0)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawCentredString(sx + cell_w * 1.5, cy - 9, str(number))
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.roundRect(sx, sy, strip_w, cell_h, 8, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        pdf.line(sx + cell_w, sy + 3, sx + cell_w, sy + cell_h - 3)
        pdf.line(sx + 2 * cell_w, sy + 3, sx + 2 * cell_w, sy + cell_h - 3)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- What's Missing?
# ---------------------------------------------------------------------------
# Each sequence has exactly one missing number (None).
P5_SEQS = [
    (23, 24, None, 26),
    (48, None, 50, 51),
    (None, 67, 68, 69),
    (78, 79, None, 81),
    (35, None, 37, 38),
    (89, 90, None, 92),
    (None, 55, 56, 57),
    (96, 97, 98, None),
]


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What's Missing?")
    draw_instruction(pdf, "Fill in the missing number.")

    box_w, box_h = 260, 125
    xs = (40, 312)
    tops = (600, 472, 344, 216)
    strip_w, cell_w, cell_h = 208, 52, 64
    for k, seq in enumerate(P5_SEQS):
        x = xs[k % 2]
        top = tops[k // 2]
        cy = top - box_h / 2
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # connected 4-cell strip
        sx = x + (box_w - strip_w) / 2
        sy = cy - cell_h / 2
        for i in range(4):
            pdf.setFillColor(white)
            pdf.rect(sx + i * cell_w, sy, cell_w, cell_h, fill=1, stroke=0)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 24)
        for i, value in enumerate(seq):
            if value is not None:
                pdf.drawCentredString(sx + (i + 0.5) * cell_w, cy - 8,
                                      str(value))
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.roundRect(sx, sy, strip_w, cell_h, 8, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        for i in (1, 2, 3):
            pdf.line(sx + i * cell_w, sy + 3, sx + i * cell_w,
                     sy + cell_h - 3)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 6 -- Count Back!
# ---------------------------------------------------------------------------
P6_STARTS = [25, 31, 42, 50, 63, 70, 84, 91]


def build_p6_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Count Back!")
    draw_instruction(pdf, "Write the 4 numbers that come before each number.")

    box_w, box_h = 260, 125
    xs = (40, 312)
    tops = (600, 472, 344, 216)
    strip_w, cell_w, cell_h = 240, 48, 64
    for k, start in enumerate(P6_STARTS):
        x = xs[k % 2]
        top = tops[k // 2]
        cy = top - box_h / 2
        # activity panel
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        # connected 5-cell strip: 4 blanks, given number in rightmost cell
        sx = x + (box_w - strip_w) / 2
        sy = cy - cell_h / 2
        for i in range(5):
            pdf.setFillColor(HexColor("#E3F2F0") if i == 4 else white)
            pdf.rect(sx + i * cell_w, sy, cell_w, cell_h, fill=1, stroke=0)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawCentredString(sx + 4.5 * cell_w, cy - 8, str(start))
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.roundRect(sx, sy, strip_w, cell_h, 8, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        for i in (1, 2, 3, 4):
            pdf.line(sx + i * cell_w, sy + 3, sx + i * cell_w,
                     sy + cell_h - 3)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    # (title, builder, locked) -- ALL PAGES APPROVED & LOCKED 2026-10-05
    ("My 1\u2013100 Number Chart", build_p1_page, True),
    ("Number Detective \u2014 Numbers 0\u201330", build_p2_page, True),
    ("Count On!", build_p3_page, True),
    ("Before & After", build_p4_page, True),
    ("What's Missing?", build_p5_page, True),
    ("Count Back!", build_p6_page, True),
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="numbers-to-30-")
    ordered = []
    for k, (title, builder, locked) in enumerate(PAGES):
        p = os.path.join(tmpdir, f"page-{k + 1}.pdf")
        builder(p)
        ordered.append(p)
        print(f"built page {k + 1}: {title} -> {p}")
    subprocess.run(["pdfunite"] + ordered + [OUT], check=True)
    print(f"merged {len(ordered)} page(s) -> {OUT}")


if __name__ == "__main__":
    main()
