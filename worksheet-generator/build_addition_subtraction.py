# Build the Addition & Subtraction Within 5 pack (Kindergarten Math).
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

PACK_TITLE = "Addition & Subtraction Within 5"


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
# Page 1 -- Addition Within 5
# ---------------------------------------------------------------------------
P1_PROBLEMS = [
    (1, 2), (2, 2),
    (3, 1), (2, 3),
    (4, 1), (0, 4),
    (1, 4), (3, 2),
]


def draw_p1_example(pdf):
    # one small worked visual: two groups of dots joined into 2 + 3 = 5
    x, w, top, h = 40, 532, 606, 84
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - h, w, h, 12, stroke=1, fill=1)
    cy = top - h / 2
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x + 18, top - 22, "EXAMPLE")
    # dots: 2 teal + 3 coral
    dx = x + 110
    for i in range(2):
        pdf.setFillColor(SOFT_BLUE)
        pdf.circle(dx + i * 30, cy - 8, 11, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(dx + 70, cy - 16, "+")
    for i in range(3):
        pdf.setFillColor(CORAL)
        pdf.circle(dx + 110 + i * 30, cy - 8, 11, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.drawString(dx + 210, cy - 16, "=")
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(dx + 244, cy - 16, "2 + 3 = 5")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Addition Within 5", "Solve the Addition Equations.")
    draw_instruction(pdf, "Solve. Write the answer.")
    draw_p1_example(pdf)

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
# Page 2 -- Subtraction Within 5
# ---------------------------------------------------------------------------
P2_PROBLEMS = [
    (5, 2), (4, 1),
    (3, 3), (5, 4),
    (2, 0), (4, 3),
    (5, 1), (3, 1),
]


def draw_p2_example(pdf):
    # one small worked visual: 5 dots, 2 crossed out -> 5 - 2 = 3
    x, w, top, h = 40, 532, 606, 84
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - h, w, h, 12, stroke=1, fill=1)
    cy = top - h / 2
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x + 18, top - 22, "EXAMPLE")
    dx = x + 110
    for i in range(5):
        pdf.setFillColor(CORAL)
        pdf.circle(dx + i * 30, cy - 8, 11, fill=1, stroke=0)
        if i >= 3:
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(2)
            cxd = dx + i * 30
            cyd = cy - 8
            pdf.line(cxd - 8, cyd - 8, cxd + 8, cyd + 8)
            pdf.line(cxd - 8, cyd + 8, cxd + 8, cyd - 8)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(dx + 170, cy - 16, "=  5 \u2212 2 = 3")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Subtraction Within 5", "Solve the Subtraction Equations.")
    draw_instruction(pdf, "Solve. Write the answer.")
    draw_p2_example(pdf)

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
# Page 3 -- Fact Families Within 5
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
    (5, 2, 3, [("t", "2 + 3 ="), ("b", None)],
     [("t", "5 \u2212 2 ="), ("b", None)]),
    (4, 1, 3, [("t", "4 \u2212 1 ="), ("b", None)],
     [("t", "1 + 3 ="), ("b", None)]),
    (5, 1, 4, [("t", "1 + 4 ="), ("b", None)],
     [("t", "5 \u2212 4 ="), ("b", None)]),
    (3, 1, 2, [("t", "3 \u2212 1 ="), ("b", None)],
     [("t", "1 + 2 ="), ("b", None)]),
]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Fact Families Within 5", "Write the Related Facts.")
    draw_instruction(pdf, "Look at the number bond. Write the two facts.")

    tops = (600, 482, 364, 246)
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
# Page 4 -- Missing Numbers Within 5
# ---------------------------------------------------------------------------
P4_PROBLEMS = [
    [("t", "2 +"), ("b", None), ("t", "= 5")],
    [("t", "5 \u2212"), ("b", None), ("t", "= 3")],
    [("b", None), ("t", "+ 1 = 4")],
    [("t", "4 \u2212"), ("b", None), ("t", "= 2")],
    [("b", None), ("t", "\u2212 2 = 1")],
    [("t", "3 +"), ("b", None), ("t", "= 4")],
    [("t", "5 \u2212"), ("b", None), ("t", "= 0")],
    [("b", None), ("t", "+ 2 = 5")],
]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Missing Numbers Within 5", "Find the Missing Number.")
    draw_instruction(pdf, "Write the missing number.")

    box_w, box_h = 256, 100
    xs = (40, 316)
    tops = (600, 492, 384, 276)
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
    ["3 birds sit in a tree.", "2 more birds come.", "How many birds now?"],
    ["5 fish are swimming.", "1 fish swims away.", "How many are left?"],
    ["2 red apples on the table.", "Sara brings 2 more.", "How many apples?"],
    ["4 ducks in the pond.", "3 ducks walk away.", "How many stay?"],
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
    ("Addition Within 5", build_p1_page, True),
    ("Subtraction Within 5", build_p2_page, True),
    ("Fact Families Within 5", build_p3_page, True),
    ("Missing Numbers Within 5", build_p4_page, True),
    ("Addition or Subtraction?", build_p5_page, True),
]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "worksheets", "kindergarten", "math",
                           "addition-subtraction")
    os.makedirs(out_dir, exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "as_tmp_%d.pdf" % i)
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
