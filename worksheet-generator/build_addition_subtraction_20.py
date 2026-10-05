# Build the Addition & Subtraction Within 20 pack (Kindergarten Math).
# Pure vector reportlab output -- no image assets.
# Pages carry a (title, builder, locked) flag. Approved pages are NEVER
# rebuilt differently: builders for locked pages are frozen.
#
# Usage: ../.venv/bin/python build_addition_subtraction.py

import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

PAGE_WIDTH = 612
PAGE_HEIGHT = 792

TEAL = HexColor("#0E7C7B")
TEAL_DARK = HexColor("#0B6362")
INK = HexColor("#1F2A37")
NAVY = HexColor("#1F3A5F")
AMBER = HexColor("#D9A021")
CORAL = HexColor("#F7A072")
SOFT_BLUE = HexColor("#8AB6E6")

PACK_TITLE = "Addition & Subtraction Within 20"


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


def draw_header(pdf, pack_title, page_title):
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
    pdf.drawString(212, 726, pack_title)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(212, 706, page_title)
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


def draw_eq_answer(pdf, cx, cy, a, b, op="+", box_w=56, box_h=64, size=28):
    """Draw 'a op b = [box]' centered at (cx, cy); op in {+, -}."""
    pdf.setFont("Helvetica-Bold", size)
    eq_text = "%d %s %d =" % (a, op, b)
    eq_w = pdf.stringWidth(eq_text, "Helvetica-Bold", size)
    gap = 10
    total = eq_w + gap + box_w
    tx = cx - total / 2
    pdf.setFillColor(INK)
    pdf.drawString(tx, cy - 10, eq_text)
    bx = tx + eq_w + gap
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.8)
    pdf.roundRect(bx, cy - box_h / 2, box_w, box_h, 8, stroke=1, fill=1)


# ---------------------------------------------------------------------------
# Page 1 -- Addition Within 20
# ---------------------------------------------------------------------------
P1_PROBLEMS = [
    (8, 5), (12, 3),
    (9, 7), (6, 9),
    (14, 4), (11, 8),
    (7, 6), (13, 5),
]


def draw_p1_example(pdf, n_blue, n_coral):
    # small worked visual: two dot groups joined into an addition equation
    x, w, top, h = 40, 532, 606, 84
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - h, w, h, 12, stroke=1, fill=1)
    cy = top - h / 2
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x + 18, top - 22, "EXAMPLE")
    total = n_blue + n_coral
    r, sp = (11, 30) if total <= 6 else (8, 20)
    pdf.setFont("Helvetica-Bold", 20)
    eq_text = "=  %d + %d = %d" % (n_blue, n_coral, total)
    eq_w = pdf.stringWidth(eq_text, "Helvetica-Bold", 20)
    plus_w = pdf.stringWidth("+", "Helvetica-Bold", 20)
    g1, g2 = n_blue * sp, n_coral * sp
    content = g1 + 14 + plus_w + 14 + g2 + 14 + eq_w
    sx = x + (w - content) / 2
    for i in range(n_blue):
        pdf.setFillColor(SOFT_BLUE)
        pdf.circle(sx + r + i * sp, cy - 6, r, fill=1, stroke=0)
    px = sx + g1 + 14
    pdf.setFillColor(INK)
    pdf.drawString(px, cy - 13, "+")
    cx0 = px + plus_w + 14
    for i in range(n_coral):
        pdf.setFillColor(CORAL)
        pdf.circle(cx0 + r + i * sp, cy - 6, r, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.drawString(cx0 + g2 + 14, cy - 13, eq_text)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Addition Within 20", "Solve the Addition Equations.")
    draw_instruction(pdf, "Solve. Write the answer.")
    draw_p1_example(pdf, 9, 6)

    box_w, box_h = 256, 100
    xs = (40, 316)
    tops = (498, 390, 282, 174)
    for k, (a, b) in enumerate(P1_PROBLEMS):
        x = xs[k % 2]
        top = tops[k // 2]
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        draw_eq_answer(pdf, x + box_w / 2, top - box_h / 2, a, b)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Subtraction Within 20
# ---------------------------------------------------------------------------
P2_PROBLEMS = [
    (14, 6), (18, 9),
    (12, 4), (20, 5),
    (16, 8), (11, 3),
    (15, 15), (13, 7),
]


def draw_p2_example(pdf, total, crossed):
    # small worked visual: dots with some crossed out -> subtraction equation
    x, w, top, h = 40, 532, 606, 84
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - h, w, h, 12, stroke=1, fill=1)
    cy = top - h / 2
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x + 18, top - 22, "EXAMPLE")
    r, sp = (11, 30) if total <= 8 else (8, 20)
    pdf.setFont("Helvetica-Bold", 20)
    eq_text = "=  %d \u2212 %d = %d" % (total, crossed, total - crossed)
    eq_w = pdf.stringWidth(eq_text, "Helvetica-Bold", 20)
    dots_w = total * sp
    content = dots_w + 14 + eq_w
    sx = x + (w - content) / 2
    for i in range(total):
        cxd = sx + r + i * sp
        pdf.setFillColor(CORAL)
        pdf.circle(cxd, cy - 6, r, fill=1, stroke=0)
        if i >= total - crossed:
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(2)
            pdf.line(cxd - 7, cy - 13, cxd + 7, cy + 1)
            pdf.line(cxd - 7, cy + 1, cxd + 7, cy - 13)
    pdf.setFillColor(INK)
    pdf.drawString(sx + dots_w + 14, cy - 13, eq_text)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Subtraction Within 20", "Solve the Subtraction Equations.")
    draw_instruction(pdf, "Solve. Write the answer.")
    draw_p2_example(pdf, 12, 5)

    box_w, box_h = 256, 100
    xs = (40, 316)
    tops = (498, 390, 282, 174)
    for k, (a, b) in enumerate(P2_PROBLEMS):
        x = xs[k % 2]
        top = tops[k // 2]
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        draw_eq_answer(pdf, x + box_w / 2, top - box_h / 2, a, b,
                       op="\u2212")

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Fact Families Within 20
# ---------------------------------------------------------------------------
def draw_token_eq(pdf, tokens, cx, cy, size=26, box_w=52, box_h=60):
    # tokens: list of ("t", text) or ("b", value|None); centered at (cx, cy)
    pdf.setFont("Helvetica-Bold", size)
    gap = 8
    widths = []
    for kind, val in tokens:
        if kind == "t":
            widths.append(pdf.stringWidth(val, "Helvetica-Bold", size))
        else:
            widths.append(box_w)
    total = sum(widths) + gap * (len(tokens) - 1)
    x = cx - total / 2
    for (kind, val), w in zip(tokens, widths):
        if kind == "t":
            pdf.setFillColor(INK)
            pdf.drawString(x, cy - 9, val)
        else:
            pdf.setFillColor(white)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(1.8)
            pdf.roundRect(x, cy - box_h / 2, box_w, box_h, 8,
                          stroke=1, fill=1)
            if val is not None:
                pdf.setFillColor(INK)
                pdf.drawCentredString(x + box_w / 2, cy - 9, str(val))
        x += w + gap


def draw_fact_bond(pdf, cx, cy, whole, p1, p2):
    pdf.setFillColor(TEAL)
    pdf.circle(cx, cy + 20, 16, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(cx, cy + 15, str(whole))
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1.6)
    pdf.line(cx - 10, cy + 8, cx - 26, cy - 8)
    pdf.line(cx + 10, cy + 8, cx + 26, cy - 8)
    for ox, v in ((-32, p1), (32, p2)):
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.4)
        pdf.circle(cx + ox, cy - 18, 13, fill=1, stroke=1)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(cx + ox, cy - 22, str(v))


P3_FAMILIES = [
    (15, 9, 6, [("t", "9 + 6 ="), ("b", None)],
     [("t", "15 \u2212 9 ="), ("b", None)]),
    (18, 10, 8, [("t", "18 \u2212 10 ="), ("b", None)],
     [("t", "10 + 8 ="), ("b", None)]),
    (13, 7, 6, [("t", "7 + 6 ="), ("b", None)],
     [("t", "13 \u2212 7 ="), ("b", None)]),
    (20, 12, 8, [("t", "12 + 8 ="), ("b", None)],
     [("t", "20 \u2212 12 ="), ("b", None)]),
]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Fact Families Within 20", "Write the Related Facts.")
    draw_instruction(pdf, "Look at the number bond. Write the two facts.")

    tops = (600, 470, 340, 210)
    for k, (whole, p1, p2, eq1, eq2) in enumerate(P3_FAMILIES):
        top = tops[k]
        x, w, h = 40, 532, 110
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - h, w, h, 12, stroke=1, fill=1)
        cy = top - h / 2
        draw_fact_bond(pdf, x + 80, cy, whole, p1, p2)
        draw_token_eq(pdf, eq1, x + 265, cy, size=24,
                      box_w=48, box_h=54)
        draw_token_eq(pdf, eq2, x + 435, cy, size=24,
                      box_w=48, box_h=54)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Missing Numbers Within 20
# ---------------------------------------------------------------------------
P4_PROBLEMS = [
    [("t", "8 +"), ("b", None), ("t", "= 13")],
    [("t", "16 \u2212"), ("b", None), ("t", "= 9")],
    [("b", None), ("t", "+ 7 = 15")],
    [("t", "20 \u2212"), ("b", None), ("t", "= 12")],
    [("b", None), ("t", "\u2212 5 = 11")],
    [("t", "9 +"), ("b", None), ("t", "= 17")],
    [("t", "14 \u2212"), ("b", None), ("t", "= 14")],
    [("b", None), ("t", "+ 9 = 18")],
]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Missing Numbers Within 20", "Find the Missing Number.")
    draw_instruction(pdf, "Write the missing number.")

    box_w, box_h = 256, 100
    xs = (40, 316)
    tops = (600, 463, 327, 190)
    for k, tokens in enumerate(P4_PROBLEMS):
        x = xs[k % 2]
        top = tops[k // 2]
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        draw_token_eq(pdf, tokens, x + box_w / 2, top - box_h / 2,
                      size=26, box_w=52, box_h=60)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Addition or Subtraction?
# ---------------------------------------------------------------------------
P5_STORIES = [
    ["12 birds on a wire.", "5 more land.", "How many birds?"],
    ["18 balloons in the sky.", "6 balloons pop.", "How many are left?"],
    ["7 green frogs.", "8 brown frogs.", "How many frogs in all?"],
    ["15 fish in the tank.", "9 swim away.", "How many stay?"],
]


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Addition or Subtraction?", "Read. Choose. Solve.")
    draw_instruction(pdf, "Read the story. Write the equation and solve.")

    box_w, box_h = 256, 250
    xs = (40, 316)
    tops = (610, 344)
    for k, lines in enumerate(P5_STORIES):
        x = xs[k % 2]
        top = tops[k // 2]
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - box_h, box_w, box_h, 12, stroke=1, fill=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 14)
        ty = top - 40
        for line in lines:
            pdf.drawString(x + 22, ty, line)
            ty -= 23
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x + 22, top - 136, "MY EQUATION:")
        # number boxes + a smaller operator box (+ or -) + answer box
        pdf.setFont("Helvetica-Bold", 22)
        gap = 8
        nb, ob = 44, 34
        eq_w = pdf.stringWidth("=", "Helvetica-Bold", 22)
        total = 3 * nb + ob + eq_w + 4 * gap
        bx = x + box_w / 2 - total / 2
        ey = top - 182
        for i in range(3):
            w = ob if i == 1 else nb
            pdf.setFillColor(white)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(1.8)
            pdf.roundRect(bx, ey - 28, w, 56, 8, stroke=1, fill=1)
            bx += w + gap
        pdf.setFillColor(INK)
        pdf.drawString(bx, ey - 8, "=")
        bx += eq_w + gap
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.8)
        pdf.roundRect(bx, ey - 28, nb, 56, 8, stroke=1, fill=1)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    # (title, builder, locked) -- ALL 5 PAGES APPROVED & LOCKED 2026-10-05
    ("Addition Within 20", build_p1_page, True),
    ("Subtraction Within 20", build_p2_page, True),
    ("Fact Families Within 20", build_p3_page, True),
    ("Missing Numbers Within 20", build_p4_page, True),
    ("Addition or Subtraction?", build_p5_page, True),
]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "worksheets", "kindergarten", "math",
                           "addition-subtraction-20")
    os.makedirs(out_dir, exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "as20_tmp_%d.pdf" % i)
        builder(tmp)
        pages.append(tmp)
        print("built page: %s" % title)
    from pypdf import PdfWriter
    writer = PdfWriter()
    for p in pages:
        writer.append(p)
    final = os.path.join(out_dir, "addition-subtraction-review.pdf")
    with open(final, "wb") as f:
        writer.write(f)
    print("merged %d page(s) -> %s" % (len(pages), final))


if __name__ == "__main__":
    main()
