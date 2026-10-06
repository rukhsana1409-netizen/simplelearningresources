# Build the Place Value: Tens & Ones pack (Kindergarten Math).
# Focus: numbers 11-19 are 1 ten and some ones. Pure vector reportlab output.
# Pages carry a (title, builder, locked) flag. Approved pages are NEVER
# rebuilt differently: builders for locked pages are frozen.
#
# Usage: ../.venv/bin/python build_place_value.py

import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

PAGE_WIDTH = 612
PAGE_HEIGHT = 792

TEAL = HexColor("#0E7C7B")
TEAL_DARK = HexColor("#0B6362")
INK = HexColor("#1F2A37")
NAVY = HexColor("#1F3A5F")
CORAL = HexColor("#F7A072")
SOFT_BLUE = HexColor("#8AB6E6")
# Place-value palette: soft pastels with dark outlines for print clarity
TENS = HexColor("#A9C9EE")
TENS_DARK = HexColor("#7FA8DC")
ONES = HexColor("#F9B98C")


def draw_logo(pdf, x, y):
    pdf.setFillColor(TEAL)
    pdf.circle(x, y, 9, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#F2C14E"))
    pdf.circle(x + 7, y + 11, 5, fill=1, stroke=0)
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1.6)
    pdf.line(x, y - 9, x - 8, y - 20)
    pdf.line(x, y - 9, x + 8, y - 20)
    pdf.line(x, y - 9, x, y - 21)


def draw_header(pdf, page_title, subtitle):
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, fill=1, stroke=0)
    draw_logo(pdf, 78, 720)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(96, 728, "LEARNING")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(96, 714, "MADE SIMPLE")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1)
    pdf.line(196, 700, 196, 742)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(212, 726, page_title)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(212, 706, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    pdf.line(40, 688, PAGE_WIDTH - 40, 688)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(40, 668, "Name:")
    pdf.line(82, 666, 300, 666)
    pdf.drawString(330, 668, "Date:")
    pdf.line(368, 666, 540, 666)


def draw_instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630, text)


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF2F1"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, 18, "Learning Made Simple")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(0.8)
    pdf.line(190, 8, 190, 30)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_WIDTH / 2, 18, "Made with love for little learners.")
    pdf.drawRightString(PAGE_WIDTH - 40, 18, "\u00a9 2026 Learning Made Simple")


def draw_panel(pdf, x, top, w, h):
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - h, w, h, 12, stroke=1, fill=1)


def draw_ten_rod(pdf, x, y, seg=18, h=22):
    """Base-ten rod: 1 group of ten, soft light blue. x,y = bottom-left."""
    w = 10 * seg
    pdf.setFillColor(TENS)
    pdf.roundRect(x, y, w, h, 4, stroke=0, fill=1)
    pdf.setStrokeColor(TENS_DARK)
    pdf.setLineWidth(1.2)
    for i in range(1, 10):
        pdf.line(x + i * seg, y + 2, x + i * seg, y + h - 2)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.roundRect(x, y, w, h, 4, stroke=1, fill=0)


def draw_ones(pdf, x, y, n, size=20, gap=5, fill=ONES):
    """Row of n unit squares. fill=None draws empty (coloring) squares."""
    for i in range(n):
        ox = x + i * (size + gap)
        if fill is not None:
            pdf.setFillColor(fill)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(1.4)
            pdf.rect(ox, y, size, size, stroke=1, fill=1)
        else:
            pdf.setFillColor(white)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(1.8)
            pdf.rect(ox, y, size, size, stroke=1, fill=1)


def draw_ones_grid(pdf, cx, y_top, n, cols=3, size=18, gap=5, fill=ONES):
    """Compact vertical grid of n unit squares, centered on cx, from y_top down."""
    rows = (n + cols - 1) // cols
    gw = cols * size + (cols - 1) * gap
    x0 = cx - gw / 2
    for i in range(n):
        r, c = divmod(i, cols)
        ox = x0 + c * (size + gap)
        oy = y_top - (r + 1) * size - r * gap
        if fill is not None:
            pdf.setFillColor(fill)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(1.4)
            pdf.rect(ox, oy, size, size, stroke=1, fill=1)
        else:
            pdf.setFillColor(white)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(1.8)
            pdf.rect(ox, oy, size, size, stroke=1, fill=1)


def write_box(pdf, cx, cy, w=44, h=48):
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.8)
    pdf.roundRect(cx - w / 2, cy - h / 2, w, h, 8, stroke=1, fill=1)


def centered_row(pdf, items, cx, cy):
    """items: ("t", text, size) | ("b", w, h) blank box
    | ("v", value, w, h) box with a completed value. Drawn centered."""
    gap = 8
    widths = []
    for it in items:
        if it[0] == "t":
            pdf.setFont("Helvetica-Bold", it[2])
            widths.append(pdf.stringWidth(it[1], "Helvetica-Bold", it[2]))
        elif it[0] == "b":
            widths.append(it[1])
        else:
            widths.append(it[2])
    total = sum(widths) + gap * (len(items) - 1)
    x = cx - total / 2
    for it, w in zip(items, widths):
        if it[0] == "t":
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", it[2])
            pdf.drawString(x, cy - it[2] * 0.35, it[1])
        elif it[0] == "b":
            write_box(pdf, x + w / 2, cy, it[1], it[2])
        else:
            value, bw, bh = it[1], it[2], it[3]
            write_box(pdf, x + w / 2, cy, bw, bh)
            pdf.setFillColor(TEAL)
            fs = int(bh * 0.45)
            pdf.setFont("Helvetica-Bold", fs)
            pdf.drawCentredString(x + w / 2, cy - fs * 0.38, str(value))
        x += w + gap


# ---------------------------------------------------------------------------
# Page 1 -- Build Numbers with Tens & Ones
# ---------------------------------------------------------------------------
P1_PRACTICE = [12, 15, 17, 19]


def draw_p1_example(pdf):
    x, w, top, h = 40, 532, 606, 104
    draw_panel(pdf, x, top, w, h)
    cy = top - h / 2
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x + 18, top - 24, "EXAMPLE")
    # model: 1 ten rod above, 3 ones below (matches practice panels)
    draw_ten_rod(pdf, x + 60, cy + 2, seg=15, h=20)
    draw_ones(pdf, x + 60, cy - 42, 3, size=18)
    # completed sentence with answer boxes, matching the practice pattern
    centered_row(pdf, [("t", "1 ten and", 18), ("v", "3", 38, 42),
                        ("t", "ones =", 18), ("v", "13", 50, 42)],
                  x + 390, cy)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Build Numbers with Tens & Ones",
                "Place Value: Tens & Ones")
    draw_instruction(pdf, "Count the tens and ones. Write the numbers.")
    draw_p1_example(pdf)

    xs = (40, 316)
    tops = (496, 300)
    for k, number in enumerate(P1_PRACTICE):
        x = xs[k % 2]
        top = tops[k // 2]
        ones = number - 10
        draw_panel(pdf, x, top, 256, 180)
        draw_ten_rod(pdf, x + 38, top - 54)
        ow = ones * 25 - 5
        draw_ones(pdf, x + (256 - ow) / 2, top - 94, ones)
        centered_row(pdf, [("t", "1 ten and", 14), ("b", 40, 44),
                            ("t", "ones =", 14), ("b", 48, 44)],
                      x + 128, top - 140)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Count Tens & Ones (ten frames)
# ---------------------------------------------------------------------------
P2_NUMBERS = [11, 14, 17, 12, 15, 18, 13, 16, 19, 14]


def draw_ten_frame(pdf, x, y, n_dots, cell=22, dot_color=ONES):
    """5x2 ten frame, bottom-left (x, y); dots fill left-to-right, top row first."""
    for r in range(2):
        for c in range(5):
            pdf.setFillColor(white)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(1.4)
            pdf.rect(x + c * cell, y + (1 - r) * cell, cell, cell,
                     stroke=1, fill=1)
    for i in range(n_dots):
        r, c = divmod(i, 5)
        pdf.setFillColor(dot_color)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.0)
        pdf.circle(x + c * cell + cell / 2, y + (1 - r) * cell + cell / 2,
                   cell * 0.36, stroke=1, fill=1)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Count Tens & Ones", "Place Value: Tens & Ones")
    draw_instruction(pdf, "Count the dots. Write the number.")

    # clean horizontal rows: full ten frame + ones frame + answer box
    col_x = (44, 316)
    rows_cy = (570, 482, 394, 306, 218)
    cell = 20
    for k, number in enumerate(P2_NUMBERS):
        x0 = col_x[k % 2]
        cy = rows_cy[k // 2]
        ones = number - 10
        draw_ten_frame(pdf, x0, cy - cell, 10, cell=cell, dot_color=TENS)
        draw_ten_frame(pdf, x0 + 5 * cell + 6, cy - cell, ones,
                       cell=cell, dot_color=ONES)
        write_box(pdf, x0 + 10 * cell + 40, cy, 48, 54)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Count the Blocks (vertical rods)
# ---------------------------------------------------------------------------
P3_NUMBERS = [13, 16, 19, 11, 15, 17]


def draw_ten_rod_v(pdf, x, y, seg=15, w=22, divider_lw=1.2,
                   outline_lw=1.6):
    """Vertical ten rod: 10 segments stacked. x,y = bottom-left."""
    h = 10 * seg
    pdf.setFillColor(TENS)
    pdf.roundRect(x, y, w, h, 4, stroke=0, fill=1)
    pdf.setStrokeColor(TENS_DARK)
    pdf.setLineWidth(divider_lw)
    for i in range(1, 10):
        pdf.line(x + 2, y + i * seg, x + w - 2, y + i * seg)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(outline_lw)
    pdf.roundRect(x, y, w, h, 4, stroke=1, fill=0)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Count the Blocks", "Place Value: Tens & Ones")
    draw_instruction(pdf, "Count the tens and ones. Write the number.")

    xs = (40, 316)
    tops = (600, 420, 240)
    for k, number in enumerate(P3_NUMBERS):
        x = xs[k % 2]
        top = tops[k // 2]
        ones = number - 10
        draw_panel(pdf, x, top, 256, 170)
        rod_cy = top - 85
        draw_ten_rod_v(pdf, x + 36, top - 160)
        # neat 2-column ones block, vertically centered with the rod
        rows = (ones + 1) // 2
        grid_h = rows * 22 - 4
        draw_ones_grid(pdf, x + 104, rod_cy + grid_h / 2, ones,
                       cols=2, size=18, gap=4)
        write_box(pdf, x + 207, rod_cy, 54, 58)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# Page 4 -- Tens & Ones (place-value boxes)
# ---------------------------------------------------------------------------
P4_NUMBERS = [12, 15, 18, 14, 11, 17]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Tens & Ones", "Place Value: Tens & Ones")
    draw_instruction(pdf, "Write each digit in the Tens and Ones boxes.")

    xs = (40, 316)
    tops = (600, 422, 244)
    for k, number in enumerate(P4_NUMBERS):
        x = xs[k % 2]
        top = tops[k // 2]
        draw_panel(pdf, x, top, 256, 170)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawCentredString(x + 128, top - 46, str(number))
        # Tens | Ones boxes with labels (kept large)
        for j, label in enumerate(("Tens", "Ones")):
            bx = x + 51 + j * (70 + 14)
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawCentredString(bx + 35, top - 74, label)
            write_box(pdf, bx + 35, top - 122, 70, 70)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Match the Number (cut and paste)
# ---------------------------------------------------------------------------
P5_NUMBERS = [12, 18, 14, 11, 19, 16]
P5_SHUFFLED = [16, 12, 19, 11, 14, 18]


def draw_scissors(pdf, x, y, s=10):
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.circle(x, y, s * 0.3, stroke=1, fill=0)
    pdf.circle(x + s * 0.5, y + s * 0.7, s * 0.3, stroke=1, fill=0)
    pdf.line(x + s * 0.2, y + s * 0.1, x + s * 1.4, y - s * 0.45)
    pdf.line(x + s * 0.62, y + s * 0.5, x + s * 1.4, y - s * 0.45)


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Match the Number", "Place Value: Tens & Ones")
    draw_instruction(pdf, "Count the blocks. Match the number.")

    xs = (40, 316)
    tops = (604, 452, 300)
    for k, number in enumerate(P5_NUMBERS):
        x = xs[k % 2]
        top = tops[k // 2]
        ones = number - 10
        draw_panel(pdf, x, top, 256, 140)
        rod_cy = top - 70
        draw_ten_rod_v(pdf, x + 40, top - 130, seg=12, w=20)
        rows = (ones + 1) // 2
        grid_h = rows * 20 - 4
        draw_ones_grid(pdf, x + 108, rod_cy + grid_h / 2, ones,
                       cols=2, size=16, gap=4)
        # large blank paste box (dashed)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.8)
        pdf.setDash(6, 4)
        pdf.roundRect(x + 162, rod_cy - 34, 68, 68, 8, stroke=1, fill=0)
        pdf.setDash()

    # cut-out area: 6 shuffled numeral cards with dashed cut borders
    pdf.setStrokeColor(HexColor("#9AA8B8"))
    pdf.setLineWidth(1.4)
    pdf.setDash(6, 4)
    pdf.roundRect(60, 58, 492, 74, 10, stroke=1, fill=0)
    pdf.setDash()
    draw_scissors(pdf, 74, 146, s=10)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(94, 142, "CUT OUT THE NUMBERS")
    for i, number in enumerate(P5_SHUFFLED):
        cx0 = 89 + i * (64 + 10)
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.4)
        pdf.setDash(4, 3)
        pdf.roundRect(cx0, 72, 64, 52, 6, stroke=1, fill=1)
        pdf.setDash()
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawCentredString(cx0 + 32, 88, str(number))

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 6 -- Is the Number Correct?
# ---------------------------------------------------------------------------
# (tens, ones, printed_number, is_correct)
P6_PROBLEMS = [
    (1, 5, 15, True),
    (1, 3, 14, False),
    (2, 0, 20, True),
    (1, 7, 16, False),
    (1, 2, 12, True),
    (1, 8, 19, False),
]


def draw_ten_blocks_v(pdf, x, y, n=10, w=26, bh=11, gap=2):
    """Vertical stack of n separate, countable blocks. x,y = bottom-left."""
    for i in range(n):
        pdf.setFillColor(TENS)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.roundRect(x, y + i * (bh + gap), w, bh, 2, stroke=1, fill=1)


def build_p6_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Is the Number Correct?", "Place Value: Tens & Ones")
    draw_instruction(pdf, "Count the blocks. Is the number correct? "
                          "Circle Yes or No.")

    # horizontal flow inside each card: ten-stack -> ones -> number -> Yes/No
    xs = (40, 316)
    tops = (600, 420, 240)
    for k, (tens, ones, printed, _correct) in enumerate(P6_PROBLEMS):
        x = xs[k % 2]
        top = tops[k // 2]
        draw_panel(pdf, x, top, 256, 170)
        baseline = top - 150  # stacks and ones share one baseline
        # ten rod(s): one continuous vertical rod with 9 thin dividers
        sx = x + 30
        for t in range(tens):
            draw_ten_rod_v(pdf, sx + t * (26 + 8), baseline, seg=12,
                           w=26, divider_lw=1.4, outline_lw=1.8)
        stack_end = sx + tens * 26 + (tens - 1) * 8
        # ones immediately right of the stack(s), bottom-aligned
        if ones:
            rows = (ones + 1) // 2
            grid_h = rows * 20 - 4
            draw_ones_grid(pdf, stack_end + 12 + 20, baseline + grid_h,
                           ones, cols=2, size=16, gap=4)
        # printed number with Yes / No below it, at the right
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawCentredString(x + 198, top - 62, str(printed))
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(x + 173, top - 104, "Yes")
        pdf.drawCentredString(x + 223, top - 104, "No")

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# Driver
PAGES = [
    # (title, builder, locked) -- all in review
    ("Build Numbers with Tens & Ones", build_p1_page, True),
    ("Count Tens & Ones", build_p2_page, True),
    ("Count the Blocks", build_p3_page, True),
    ("Tens & Ones", build_p4_page, True),
    ("Match the Number", build_p5_page, True),
    ("Is the Number Correct?", build_p6_page, True),
]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "worksheets", "kindergarten", "math",
                           "place-value")
    os.makedirs(out_dir, exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "pv_tmp_%d.pdf" % i)
        builder(tmp)
        pages.append(tmp)
        print("built page: %s" % title)
    from pypdf import PdfWriter
    writer = PdfWriter()
    for p in pages:
        writer.append(p)
    final = os.path.join(out_dir, "place-value-review.pdf")
    with open(final, "wb") as f:
        writer.write(f)
    print("merged %d page(s) -> %s" % (len(pages), final))


if __name__ == "__main__":
    main()
