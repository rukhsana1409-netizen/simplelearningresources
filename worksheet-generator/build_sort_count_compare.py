# Build the Sort, Count & Compare pack (Kindergarten Math).
# Page 1: Sort Into Groups -- cut-and-paste classification.
# Pure vector reportlab output + approved watercolor JPG assets.
#
# Usage: ../.venv/bin/python build_sort_count_compare.py

import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

PAGE_WIDTH = 612
PAGE_HEIGHT = 792

TEAL = HexColor("#0E7C7B")
TEAL_DARK = HexColor("#0B6362")
INK = HexColor("#1F2A37")
NAVY = HexColor("#1F3A5F")
CUT_GRAY = HexColor("#8A9BA8")
DASH_TEAL = HexColor("#9CCBC6")

SCC_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "assets", "sort-count-compare")
CW_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "assets", "compare-weight")
ANIMAL_LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "assets", "animal-library")

TINTS = [
    (HexColor("#FDE9EE"), HexColor("#F3C6D3")),  # pink
    (HexColor("#FDF4DC"), HexColor("#EDD9A8")),  # yellow
    (HexColor("#E4F1FB"), HexColor("#B9D6EC")),  # blue
    (HexColor("#E5F5EA"), HexColor("#BDE3C9")),  # green
    (HexColor("#F0E9F8"), HexColor("#D3C2EA")),  # purple
]


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


def _place_illustration(pdf, asset_dir, img_name, card_x, card_y,
                        card_w=84, card_h=84, pad=8, dashed_cut=False):
    from PIL import Image as PILImage
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.2)
    pdf.roundRect(card_x, card_y, card_w, card_h, 10, stroke=1, fill=1)
    path = os.path.join(asset_dir, img_name)
    iw, ih = PILImage.open(path).size
    scale = min((card_w - 2 * pad) / iw, (card_h - 2 * pad) / ih)
    dw, dh = iw * scale, ih * scale
    pdf.drawImage(path, card_x + (card_w - dw) / 2,
                  card_y + (card_h - dh) / 2, dw, dh)
    if dashed_cut:
        pdf.setStrokeColor(CUT_GRAY)
        pdf.setLineWidth(1.6)
        pdf.setDash(6, 4)
        pdf.roundRect(card_x, card_y, card_w, card_h, 10, stroke=1, fill=0)
        pdf.setDash()


def scissors(pdf, x, y, s=9):
    pdf.setStrokeColor(CUT_GRAY)
    pdf.setLineWidth(1.6)
    pdf.line(x - s * 1.5, y - s * 0.9, x + s * 0.8, y + s * 0.45)
    pdf.line(x - s * 1.5, y + s * 0.9, x + s * 0.8, y - s * 0.45)
    pdf.circle(x - s * 1.7, y - s * 1.15, s * 0.34, stroke=1, fill=0)
    pdf.circle(x - s * 1.7, y + s * 1.15, s * 0.34, stroke=1, fill=0)


def cut_divider(pdf, y, label):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    pdf.setStrokeColor(DASH_TEAL)
    pdf.setLineWidth(1.2)
    pdf.setDash(8, 5)
    pdf.line(40 + 34, y, PAGE_WIDTH - 40, y)
    pdf.setDash()
    scissors(pdf, 40 + 16, y)
    pdf.setFont("Helvetica-Bold", 13)
    tw = stringWidth(label, "Helvetica-Bold", 13)
    pdf.setFillColor(white)
    pdf.setStrokeColor(white)
    pdf.roundRect(PAGE_WIDTH / 2 - tw / 2 - 10, y - 12, tw + 20, 20, 8,
                  stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.drawCentredString(PAGE_WIDTH / 2, y - 5, label)


# ---------------------------------------------------------------------------
# Page 1 -- Sort Into Groups (cut-and-paste classification).
# Groups: Things We Wear (sweater cue) / Things We Eat (sandwich cue).
# Cut cards (mixed): shirt, apple, shoe, banana, hat, carrot, socks,
# strawberry -> wear: shirt, shoe, hat, socks / eat: apple, banana, carrot,
# strawberry.
# ---------------------------------------------------------------------------
GROUPS = [
    ("Things We Wear", "scc-jacket.jpg", TINTS[2]),  # blue
    ("Things We Eat", "scc-cue-eat.jpg", TINTS[3]),    # green
]

# (asset_dir, img_name) in mixed display order
CUT_CARDS = [
    (SCC_ASSETS, "scc-shirt.jpg"),
    (CW_ASSETS, "cw2-apple.jpg"),
    (CW_ASSETS, "cw2-shoe.jpg"),
    (SCC_ASSETS, "scc-banana.jpg"),
    (CW_ASSETS, "cw3-hat.jpg"),
    (SCC_ASSETS, "scc-carrot.jpg"),
    (SCC_ASSETS, "scc-socks.jpg"),
    (CW_ASSETS, "cw-strawberry.jpg"),
]

PANEL_W, PANEL_H = 260, 252
CARD = 84


def _group_panel(pdf, x, top, label, cue_name, tint):
    fill, border = tint
    pdf.setFillColor(fill)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - PANEL_H, PANEL_W, PANEL_H, 12, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(x + PANEL_W / 2, top - 28, label)
    # visual cue badge (illustration directly in the circle, no inner card)
    from PIL import Image as PILImage
    cx = x + PANEL_W / 2
    cy = top - 88
    pdf.setFillColor(white)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.6)
    pdf.circle(cx, cy, 44, stroke=1, fill=1)
    path = os.path.join(SCC_ASSETS, cue_name)
    iw, ih = PILImage.open(path).size
    scale = min(66 / iw, 50 / ih)
    dw, dh = iw * scale, ih * scale
    pdf.drawImage(path, cx - dw / 2, cy - dh / 2, dw, dh)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Sort Into Groups", "Sort, Count & Compare")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 612,
                          "Cut out the pictures. Paste them into the correct group.")

    for i, (label, cue, tint) in enumerate(GROUPS):
        _group_panel(pdf, 40 + i * 272, 596, label, cue, tint)

    cut_divider(pdf, 322, "Cut and Paste")

    for i, (adir, img) in enumerate(CUT_CARDS):
        col, row = i % 4, i // 4
        cx = 40 + col * 133 + (133 - CARD) / 2
        cy = 214 - row * 100
        _place_illustration(pdf, adir, img, cx, cy, CARD, CARD, pad=8,
                            dashed_cut=True)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Sort & Count. 9 mixed objects from 3 categories; the child sorts
# mentally, counts each category, and writes the number.
# Grid (row-major, mixed): cat, apple, shoe / banana, dog, carrot /
# hat, strawberry, rabbit.
# Correct: Animals = 3, Food = 4, Things We Wear = 2.
# ---------------------------------------------------------------------------
P2_GRID = [
    (ANIMAL_LIB, "lib-cat.jpg"),
    (CW_ASSETS, "cw2-apple.jpg"),
    (CW_ASSETS, "cw2-shoe.jpg"),
    (SCC_ASSETS, "scc-banana.jpg"),
    (ANIMAL_LIB, "lib-dog.jpg"),
    (SCC_ASSETS, "scc-carrot.jpg"),
    (CW_ASSETS, "cw3-hat.jpg"),
    (CW_ASSETS, "cw-strawberry.jpg"),
    (ANIMAL_LIB, "lib-rabbit.jpg"),
]

P2_ANSWERS = [
    ("Animals", ANIMAL_LIB, "lib-cat.jpg", TINTS[2]),
    ("Food", CW_ASSETS, "cw2-apple.jpg", TINTS[1]),
    ("Things We Wear", CW_ASSETS, "cw2-shoe.jpg", TINTS[3]),
]

P2_CARD_W, P2_CARD_H = 150, 90


def _big_number_box(pdf, x, y, w=72, h=62):
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.roundRect(x, y, w, h, 8, stroke=1, fill=1)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Sort & Count", "Sort, Count & Compare")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 612,
                          "Look at the pictures. Count each group. Write the number.")

    # picture collection panel
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 594 - 326, 532, 326, 12, stroke=1, fill=1)
    for i, (adir, img) in enumerate(P2_GRID):
        col, row = i % 3, i // 3
        _place_illustration(pdf, adir, img, 62 + col * 170, 486 - row * 104,
                            P2_CARD_W, P2_CARD_H, pad=8)

    # three answer areas (labels + large writing boxes only; no example
    # pictures, so nothing can be mistaken for an extra object to count)
    for i, (label, cdir, cue, tint) in enumerate(P2_ANSWERS):
        x = 40 + i * 186
        top = 240
        fill, border = tint
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - 138, 160, 138, 12, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawCentredString(x + 80, 198, label)
        _big_number_box(pdf, x + 44, 118)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Make a Picture Graph. Mixed collection of 9 school items
# (4 pencils, 3 crayons, 2 erasers); below, a 3-column block graph
# (Pencils | Crayons | Erasers) with 4 large empty stacked boxes per column
# and number markings 1-4 at the left. The child colors one box per item.
# Grid (row-major, mixed): P, C, P / E, P, C / C, E, P.
# Correct: Pencils = 4 boxes, Crayons = 3 boxes, Erasers = 2 boxes.
# ---------------------------------------------------------------------------
P3_PENCIL = (CW_ASSETS, "cw-pencil.jpg")
P3_CRAYON = (SCC_ASSETS, "scc-crayon.jpg")
P3_ERASER = (SCC_ASSETS, "scc-eraser.jpg")

P3_GRID = [
    P3_PENCIL, P3_CRAYON, P3_PENCIL,
    P3_ERASER, P3_PENCIL, P3_CRAYON,
    P3_CRAYON, P3_ERASER, P3_PENCIL,
]

P3_COLS = [
    ("Pencils", P3_PENCIL),
    ("Crayons", P3_CRAYON),
    ("Erasers", P3_ERASER),
]

GRAPH_BOX_W, GRAPH_SECT_H = 62, 44


def _graph_bar(pdf, x, y_bottom):
    # one continuous vertical bar divided into 4 equal coloring sections
    h = 4 * GRAPH_SECT_H
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.roundRect(x, y_bottom, GRAPH_BOX_W, h, 8, stroke=1, fill=1)
    pdf.setLineWidth(1.2)
    for s in range(1, 4):
        yy = y_bottom + s * GRAPH_SECT_H
        pdf.line(x + 1, yy, x + GRAPH_BOX_W - 1, yy)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Make a Picture Graph", "Sort, Count & Compare")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 612,
                          "Count each kind. Color one box for each picture.")

    # mixed collection panel: 596..328
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 596 - 268, 532, 268, 12, stroke=1, fill=1)
    for i, (adir, img) in enumerate(P3_GRID):
        col, row = i % 3, i // 3
        _place_illustration(pdf, adir, img, 98 + col * 150, 512 - row * 84,
                            116, 68, pad=8)

    # block graph panel: 312..60
    pdf.setFillColor(HexColor("#FDFBF7"))
    pdf.setStrokeColor(HexColor("#E3D9C2"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 312 - 252, 532, 252, 12, stroke=1, fill=1)

    # number markings 1-4 along the left side, centered on each bar section
    # (1 at the bottom: boxes are colored bottom-up like building a tower)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12)
    for s in range(4):
        cy = 72 + s * GRAPH_SECT_H + GRAPH_SECT_H / 2
        pdf.drawCentredString(58, cy - 4, str(s + 1))

    # three columns: icon + label header, 4 stacked empty boxes
    from PIL import Image as PILImage
    from reportlab.pdfbase.pdfmetrics import stringWidth
    pdf.setFont("Helvetica-Bold", 13)
    for c, (label, (adir, img)) in enumerate(P3_COLS):
        cx = 128.7 + c * 177.3
        # header: small picture + label, centered as a unit
        cpath = os.path.join(adir, img)
        iw, ih = PILImage.open(cpath).size
        sc = min(36 / iw, 30 / ih)
        dw, dh = iw * sc, ih * sc
        lw = stringWidth(label, "Helvetica-Bold", 13)
        ux = cx - (dw + 8 + lw) / 2
        pdf.drawImage(cpath, ux, 268, dw, dh)
        pdf.setFillColor(NAVY)
        pdf.drawString(ux + dw + 8, 276, label)
        # continuous bar of 4 touching coloring sections (bottom-up)
        _graph_bar(pdf, cx - GRAPH_BOX_W / 2, 72)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Read the Graph. Completed "Favorite Fruits" bar graph:
# Apple = 5, Banana = 3, Orange = 4, Strawberry = 2. Four questions below.
# Correct: 1) 5 · 2) Apple · 3) Strawberry · 4) 1.
# ---------------------------------------------------------------------------
P4_BARS = [
    ("Apple", CW_ASSETS, "cw2-apple.jpg", HexColor("#D94F4F"), 5),
    ("Banana", SCC_ASSETS, "scc-banana.jpg", HexColor("#F2C14E"), 3),
    ("Orange", CW_ASSETS, "cw2-orange.jpg", HexColor("#EF9B3F"), 4),
    ("Strawberry", CW_ASSETS, "cw-strawberry.jpg", HexColor("#EC6E9C"), 2),
]
P4_QUESTIONS = [
    "How many apples?",
    "Which fruit has the most?",
    "Which fruit has the fewest?",
    "How many more oranges than bananas?",
]

P4_BLOCK_H = 34
P4_BAR_W = 64
P4_BASE_Y = 350
P4_BAR_XS = [120, 230, 340, 450]


def _p4_bar(pdf, x, value, color):
    # rounded outline, bottom `value` blocks filled, dividers at each level
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.roundRect(x, P4_BASE_Y, P4_BAR_W, 5 * P4_BLOCK_H, 8, stroke=1, fill=1)
    if value > 0:
        pdf.setFillColor(color)
        pdf.setStrokeColor(color)
        pdf.setLineWidth(1)
        pdf.rect(x + 2, P4_BASE_Y + 2, P4_BAR_W - 4,
                 value * P4_BLOCK_H - 3, stroke=1, fill=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.1)
    for k in range(1, 5):
        yy = P4_BASE_Y + k * P4_BLOCK_H
        pdf.line(x + 1, yy, x + P4_BAR_W - 1, yy)


def build_p4_page(path):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from PIL import Image as PILImage
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Read the Graph", "Sort, Count & Compare")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 612,
                          "Look at the graph. Answer the questions.")

    # graph panel
    pdf.setFillColor(HexColor("#FDFBF7"))
    pdf.setStrokeColor(HexColor("#E3D9C2"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 590 - 340, 532, 340, 12, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 566, "Fruit Graph")

    # scale gridlines + numbers 0-5 (drawn before bars)
    pdf.setStrokeColor(HexColor("#E8EDF3"))
    pdf.setLineWidth(1)
    pdf.setFont("Helvetica", 11)
    for k in range(6):
        yy = P4_BASE_Y + k * P4_BLOCK_H
        pdf.line(100, yy, 545, yy)
        pdf.setFillColor(NAVY)
        pdf.drawRightString(88, yy - 4, str(k))

    # bars + fruit pictures + labels
    for i, (label, adir, img, color, value) in enumerate(P4_BARS):
        x = P4_BAR_XS[i]
        _p4_bar(pdf, x, value, color)
        cpath = os.path.join(adir, img)
        iw, ih = PILImage.open(cpath).size
        sc = min(48 / iw, 38 / ih)
        dw, dh = iw * sc, ih * sc
        pdf.drawImage(cpath, x + P4_BAR_W / 2 - dw / 2, 308, dw, dh)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(x + P4_BAR_W / 2, 284, label)

    # questions
    pdf.setFont("Helvetica-Bold", 13.5)
    qy = 208
    for q in P4_QUESTIONS:
        pdf.setFillColor(NAVY)
        pdf.drawString(60, qy, q)
        tw = stringWidth(q, "Helvetica-Bold", 13.5)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.6)
        pdf.line(60 + tw + 14, qy - 6, 552, qy - 6)
        qy -= 46

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Sort & Graph Challenge (final mixed review). 10 NEW mixed pictures
# (no repeats of Page 2 objects):
# elephant, duck, fish, turtle / pear, grapes, cupcake / jacket, dress, boots.
# Table: Animals = 4, Food = 3, Things We Wear = 3.
# Questions: 1) Animals 2) Food and Things We Wear 3) draw a food.
# ---------------------------------------------------------------------------
P5_GRID = [
    (ANIMAL_LIB, "lib-elephant.jpg"),
    (SCC_ASSETS, "scc-pear.jpg"),
    (SCC_ASSETS, "scc-jacket.jpg"),
    (ANIMAL_LIB, "lib-fish.jpg"),
    (SCC_ASSETS, "scc-grapes.jpg"),
    (SCC_ASSETS, "scc-dress.jpg"),
    (ANIMAL_LIB, "lib-duck.jpg"),
    (CW_ASSETS, "cw2-cupcake.jpg"),
    (CW_ASSETS, "cw2-boot.jpg"),
    (ANIMAL_LIB, "lib-turtle.jpg"),
]

P5_CATS = ["Animals", "Food", "Things We Wear"]
P5_CXS = [300, 405, 510]


def build_p5_page(path):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Sort & Graph Challenge", "Sort, Count & Compare")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 612,
                          "Sort and count the pictures. Then answer the questions.")

    # mixed picture collection: 592..400
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 592 - 192, 532, 192, 12, stroke=1, fill=1)
    for i, (adir, img) in enumerate(P5_GRID):
        col, row = i % 5, i // 5
        _place_illustration(pdf, adir, img, 47 + col * 106, 502 - row * 88,
                            94, 76, pad=7)

    # counting table: 384..290
    pdf.setFillColor(HexColor("#FDFBF7"))
    pdf.setStrokeColor(HexColor("#E3D9C2"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 384 - 94, 532, 94, 12, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12.5)
    for cx, cat in zip(P5_CXS, P5_CATS):
        pdf.drawCentredString(cx, 360, cat)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(60, 319, "How many?")
    for cx in P5_CXS:
        _big_number_box(pdf, cx - 31, 300, w=62, h=48)

    # questions
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)

    q1 = "1. Which group has the most?"
    pdf.drawString(60, 262, q1)
    pdf.line(60 + stringWidth(q1, "Helvetica-Bold", 13.5) + 14, 256, 552, 256)

    q2 = "2. Which two groups have the same number?"
    pdf.drawString(60, 218, q2)
    pdf.line(60, 176, 250, 176)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawCentredString(281, 178, "and")
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.line(312, 176, 552, 176)

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawString(60, 146, "3. Draw one more food.")
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.roundRect(60, 54, 492, 76, 10, stroke=1, fill=1)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver (P1 only for now)
# ---------------------------------------------------------------------------
PAGES = [
    # (title, builder, locked)
    ("Sort Into Groups", build_p1_page, True),  # APPROVED 2026-10-07
    ("Sort & Count", build_p2_page, True),  # APPROVED 2026-10-07
    ("Make a Picture Graph", build_p3_page, True),  # APPROVED 2026-10-07
    ("Read the Graph", build_p4_page, True),  # APPROVED 2026-10-07
    ("Sort & Graph Challenge", build_p5_page, True),  # APPROVED 2026-10-07
]


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "math",
                       "sort-count-compare", "sort-count-compare-review.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "scc_tmp_%d.pdf" % i)
        builder(tmp)
        pages.append(tmp)
        print("built page: %s" % title)
    from pypdf import PdfWriter
    writer = PdfWriter()
    for p in pages:
        writer.append(p)
    with open(out, "wb") as f:
        writer.write(f)
    print("merged %d page(s) -> %s" % (len(pages), out))


if __name__ == "__main__":
    main()
