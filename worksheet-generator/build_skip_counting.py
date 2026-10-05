"""Skip Counting -- Kindergarten Math.

Page 1 (only): Skip Counting by 2s -- Learn the Pattern.
A cheerful teaching/reference page for the 2s sequence. No questions.

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
AMBER = HexColor("#C9821A")
MARGIN = 40

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "kindergarten", "math", "skip-counting",
                   "skip-counting-review.pdf")

PACK_TITLE = "Skip Counting"


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
# Page 1 -- Skip Counting by 2s: Learn the Pattern (teaching/reference)
# ---------------------------------------------------------------------------
def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Counting by 2s \u2014 Learn the Pattern")
    draw_instruction(pdf, "Count by 2s \u2014 say it like a song!")

    def strip(x, cy, seq, cell_w, cell_h, number_size, number_color,
              border_color, border_width=1.6):
        n = len(seq)
        strip_w = n * cell_w
        sy = cy - cell_h / 2
        for i in range(n):
            pdf.setFillColor(white)
            pdf.rect(x + i * cell_w, sy, cell_w, cell_h, fill=1, stroke=0)
        pdf.setFillColor(number_color)
        pdf.setFont("Helvetica-Bold", number_size)
        for i, value in enumerate(seq):
            if value is not None:
                pdf.drawCentredString(x + (i + 0.5) * cell_w, cy - 8,
                                      str(value))
        pdf.setStrokeColor(border_color)
        pdf.setLineWidth(border_width)
        pdf.roundRect(x, sy, strip_w, cell_h, 10, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        for i in range(1, n):
            pdf.line(x + i * cell_w, sy + 3, x + i * cell_w,
                     sy + cell_h - 3)

    # prominent teaching pattern: ONE connected box, 2 rows x 5 columns
    cols, rows = 5, 2
    cell_w, cell_h = 68, 64
    box_w, box_h = cols * cell_w, rows * cell_h
    bx = (PAGE_WIDTH - box_w) / 2
    by = 452
    pdf.setFillColor(white)
    pdf.rect(bx, by, box_w, box_h, fill=1, stroke=0)
    numbers = ([2, 4, 6, 8, 10], [12, 14, 16, 18, 20])
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 28)
    for r in range(rows):
        for c in range(cols):
            cx = bx + (c + 0.5) * cell_w
            cy = by + box_h - (r + 0.5) * cell_h
            pdf.drawCentredString(cx, cy - 10, str(numbers[r][c]))
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.roundRect(bx, by, box_w, box_h, 12, stroke=1, fill=0)
    pdf.setLineWidth(1.2)
    for c in range(1, cols):
        pdf.line(bx + c * cell_w, by + 4, bx + c * cell_w, by + box_h - 4)
    pdf.line(bx + 4, by + cell_h, bx + box_w - 4, by + cell_h)

    # simple practice below -- numbers 2-20 only, varied missing positions
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 380, "Fill in the missing numbers.")

    strip(176, 300, (2, 4, None, 8, 10), 52, 62, 22, INK, INK)
    strip(176, 205, (None, 8, 10, 12, 14), 52, 62, 22, INK, INK)
    strip(176, 110, (12, 14, 16, None, 20), 52, 62, 22, INK, INK)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Counting by 5s: Learn the Pattern (same structure as Page 1)
# ---------------------------------------------------------------------------
def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Counting by 5s \u2014 Learn the Pattern")
    draw_instruction(pdf, "Count by 5s \u2014 say it like a song!")

    def strip(x, cy, seq, cell_w, cell_h, number_size, number_color,
              border_color, border_width=1.6):
        n = len(seq)
        strip_w = n * cell_w
        sy = cy - cell_h / 2
        for i in range(n):
            pdf.setFillColor(white)
            pdf.rect(x + i * cell_w, sy, cell_w, cell_h, fill=1, stroke=0)
        pdf.setFillColor(number_color)
        pdf.setFont("Helvetica-Bold", number_size)
        for i, value in enumerate(seq):
            if value is not None:
                pdf.drawCentredString(x + (i + 0.5) * cell_w, cy - 8,
                                      str(value))
        pdf.setStrokeColor(border_color)
        pdf.setLineWidth(border_width)
        pdf.roundRect(x, sy, strip_w, cell_h, 10, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        for i in range(1, n):
            pdf.line(x + i * cell_w, sy + 3, x + i * cell_w,
                     sy + cell_h - 3)

    # prominent teaching chart: ONE connected box, 2 rows x 5 columns
    cols, rows = 5, 2
    cell_w, cell_h = 68, 64
    box_w, box_h = cols * cell_w, rows * cell_h
    bx = (PAGE_WIDTH - box_w) / 2
    by = 452
    pdf.setFillColor(white)
    pdf.rect(bx, by, box_w, box_h, fill=1, stroke=0)
    numbers = ([5, 10, 15, 20, 25], [30, 35, 40, 45, 50])
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 28)
    for r in range(rows):
        for c in range(cols):
            cx = bx + (c + 0.5) * cell_w
            cy = by + box_h - (r + 0.5) * cell_h
            pdf.drawCentredString(cx, cy - 10, str(numbers[r][c]))
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.roundRect(bx, by, box_w, box_h, 12, stroke=1, fill=0)
    pdf.setLineWidth(1.2)
    for c in range(1, cols):
        pdf.line(bx + c * cell_w, by + 4, bx + c * cell_w, by + box_h - 4)
    pdf.line(bx + 4, by + cell_h, bx + box_w - 4, by + cell_h)

    # simple practice below -- multiples of 5 up to 50, varied positions
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 380, "Fill in the missing numbers.")

    strip(176, 300, (5, 10, None, 20, 25), 52, 62, 22, INK, INK)
    strip(176, 205, (None, 20, 25, 30, 35), 52, 62, 22, INK, INK)
    strip(176, 110, (30, 35, 40, None, 50), 52, 62, 22, INK, INK)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Counting by 10s: Learn the Pattern (same structure)
# ---------------------------------------------------------------------------
def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Counting by 10s \u2014 Learn the Pattern")
    draw_instruction(pdf, "Count by 10s \u2014 say it like a song!")

    def strip(x, cy, seq, cell_w, cell_h, number_size, number_color,
              border_color, border_width=1.6):
        n = len(seq)
        strip_w = n * cell_w
        sy = cy - cell_h / 2
        for i in range(n):
            pdf.setFillColor(white)
            pdf.rect(x + i * cell_w, sy, cell_w, cell_h, fill=1, stroke=0)
        pdf.setFillColor(number_color)
        pdf.setFont("Helvetica-Bold", number_size)
        for i, value in enumerate(seq):
            if value is not None:
                pdf.drawCentredString(x + (i + 0.5) * cell_w, cy - 8,
                                      str(value))
        pdf.setStrokeColor(border_color)
        pdf.setLineWidth(border_width)
        pdf.roundRect(x, sy, strip_w, cell_h, 10, stroke=1, fill=0)
        pdf.setLineWidth(1.2)
        for i in range(1, n):
            pdf.line(x + i * cell_w, sy + 3, x + i * cell_w,
                     sy + cell_h - 3)

    # prominent teaching chart: ONE connected box, 2 rows x 5 columns
    cols, rows = 5, 2
    cell_w, cell_h = 68, 64
    box_w, box_h = cols * cell_w, rows * cell_h
    bx = (PAGE_WIDTH - box_w) / 2
    by = 452
    pdf.setFillColor(white)
    pdf.rect(bx, by, box_w, box_h, fill=1, stroke=0)
    numbers = ([10, 20, 30, 40, 50], [60, 70, 80, 90, 100])
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 28)
    for r in range(rows):
        for c in range(cols):
            cx = bx + (c + 0.5) * cell_w
            cy = by + box_h - (r + 0.5) * cell_h
            pdf.drawCentredString(cx, cy - 10, str(numbers[r][c]))
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.roundRect(bx, by, box_w, box_h, 12, stroke=1, fill=0)
    pdf.setLineWidth(1.2)
    for c in range(1, cols):
        pdf.line(bx + c * cell_w, by + 4, bx + c * cell_w, by + box_h - 4)
    pdf.line(bx + 4, by + cell_h, bx + box_w - 4, by + cell_h)

    # simple practice below -- multiples of 10 up to 100, varied positions
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 380, "Fill in the missing numbers.")

    strip(176, 300, (10, 20, None, 40, 50), 52, 62, 22, INK, INK)
    strip(176, 205, (None, 40, 50, 60, 70), 52, 62, 22, INK, INK)
    strip(176, 110, (60, 70, 80, None, 100), 52, 62, 22, INK, INK)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    # (title, builder, locked) -- ALL 3 PAGES APPROVED & LOCKED 2026-10-05
    ("Counting by 2s \u2014 Learn the Pattern", build_p1_page, True),
    ("Counting by 5s \u2014 Learn the Pattern", build_p2_page, True),
    ("Counting by 10s \u2014 Learn the Pattern", build_p3_page, True),
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="skip-counting-") as tmp:
        parts = []
        for idx, (title, builder, locked) in enumerate(PAGES, start=1):
            path = os.path.join(tmp, "page-%d.pdf" % idx)
            builder(path)
            parts.append(path)
            print("built page %d: %s" % (idx, title))
        cmd = ["pdfunite"] + parts + [OUT]
        subprocess.run(cmd, check=True, capture_output=True)
    print("merged %d page(s) -> %s" % (len(parts), OUT))


if __name__ == "__main__":
    main()
