"""Living & Non-Living -- Preschool Science & Discovery.

A 5-page pack introducing living vs non-living things to preschoolers:
  P1 Living & Non-Living        -- teaching poster (NOT an activity)
  P2 Living or Non-Living?      -- circle the living things (12 pictures)
  P3 Living or Non-Living? Sort  -- cut-and-paste sort (8 cards)
  P4 What Does It Need?         -- circle what the rabbit needs (8 choices)
  P5 Which One Does NOT Belong? -- odd-one-out rows (4x4)

Uses assets/living-nonliving/ (new watercolor illustrations in the Plants
pack style) plus a few approved plant-library illustrations (air, water,
toy car, shoe, flower). All embeds are JPEG so the PDF stays pushable.

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

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "living-nonliving")
PLANT_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "assets", "plant-library")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "science", "living-nonliving",
                   "living-nonliving.pdf")

GREEN_FILL = "#E9F5E9"
GREEN_BORDER = "#7CBF7C"
GREEN_DARK = HexColor("#2E7D32")
GREY_FILL = "#F1F3F6"
GREY_BORDER = "#9AA5B1"
GREY_DARK = HexColor("#5A6B7C")


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


def draw_instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630, text)


# ---------------------------------------------------------------------------
# Shared drawing helpers
# ---------------------------------------------------------------------------
def img(pdf, name, cx, top, w, h=None, plant=False):
    base = PLANT_ASSETS if plant else ASSETS
    h = h or w
    pdf.drawImage(os.path.join(base, name),
                  cx - w / 2, top - h, width=w, height=h,
                  preserveAspectRatio=True, anchor="c")


def bullet(pdf, cx, y, text, dot_color, size=15):
    pdf.setFont("Helvetica-Bold", size)
    tw = pdf.stringWidth(text, "Helvetica-Bold", size)
    pdf.setFillColor(dot_color)
    pdf.circle(cx - tw / 2 - 14, y + 5, 5, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.drawCentredString(cx, y, text)


def bullet_col(pdf, x_start, y_tops, texts, dot_color, size=15):
    """Left-aligned column of bullets starting at x_start."""
    pdf.setFont("Helvetica-Bold", size)
    for y, text in zip(y_tops, texts):
        pdf.setFillColor(dot_color)
        pdf.circle(x_start, y + 5, 5, fill=1, stroke=0)
        pdf.setFillColor(INK)
        pdf.drawString(x_start + 14, y, text)


def paste_slot(pdf, x, top, w, h):
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1.4)
    pdf.setDash(7, 5)
    pdf.roundRect(x, top - h, w, h, 10, stroke=1, fill=0)
    pdf.setDash()


def cut_card(pdf, x, top, w, h, image, label, plant=False, img_h=58,
             label_size=13):
    pdf.setStrokeColor(HexColor("#8A9BA8"))
    pdf.setLineWidth(1.2)
    pdf.setDash(6, 4)
    pdf.roundRect(x, top - h, w, h, 8, stroke=1, fill=0)
    pdf.setDash()
    img(pdf, image, x + w / 2, top - 6, w - 28, img_h, plant=plant)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", label_size)
    pdf.drawCentredString(x + w / 2, top - h + 11, label)


def scissors(pdf, x, y, s=9):
    pdf.setStrokeColor(HexColor("#8A9BA8"))
    pdf.setLineWidth(1.6)
    pdf.line(x - s * 1.5, y - s * 0.9, x + s * 0.8, y + s * 0.45)
    pdf.line(x - s * 1.5, y + s * 0.9, x + s * 0.8, y - s * 0.45)
    pdf.circle(x - s * 1.7, y - s * 1.15, s * 0.34, stroke=1, fill=0)
    pdf.circle(x - s * 1.7, y + s * 1.15, s * 0.34, stroke=1, fill=0)


def cut_divider(pdf, y):
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1.2)
    pdf.setDash(8, 5)
    pdf.line(MARGIN + 34, y, PAGE_WIDTH - MARGIN, y)
    pdf.setDash()
    scissors(pdf, MARGIN + 16, y)


def choice(pdf, cx, top, image, label, plant=False, img_size=88):
    img(pdf, image, cx, top, img_size, img_size, plant=plant)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(cx, top - img_size - 18, label)


PACK_TITLE = "Living & Non-Living"


# ---------------------------------------------------------------------------
# Page 1: teaching poster -- two large sections, not an activity.
# ---------------------------------------------------------------------------
def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Living and Non-Living Things")
    draw_instruction(pdf, "Let\u2019s learn about living and non-living things!")

    # LIVING THINGS panel
    pdf.setFillColor(HexColor(GREEN_FILL))
    pdf.setStrokeColor(HexColor(GREEN_BORDER))
    pdf.setLineWidth(2.5)
    pdf.roundRect(40, 365, 532, 235, 16, stroke=1, fill=1)
    pdf.setFillColor(GREEN_DARK)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(306, 578, "LIVING THINGS")
    img(pdf, "ln-child.jpg", 140, 562, 100, 120)
    img(pdf, "ln-tree.jpg", 306, 560, 115, 115)
    img(pdf, "ln-bird.jpg", 472, 560, 115, 115)
    # two balanced columns, left-aligned within each column
    bullet_col(pdf, 155, (428, 402), ["Grow", "Need air"], GREEN_DARK)
    bullet_col(pdf, 336, (428, 402),
               ["Need water and food", "Change as they grow"], GREEN_DARK)

    # NON-LIVING THINGS panel
    pdf.setFillColor(HexColor(GREY_FILL))
    pdf.setStrokeColor(HexColor(GREY_BORDER))
    pdf.setLineWidth(2.5)
    pdf.roundRect(40, 110, 532, 235, 16, stroke=1, fill=1)
    pdf.setFillColor(GREY_DARK)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(306, 323, "NON-LIVING THINGS")
    img(pdf, "ln-ball.jpg", 140, 307, 115, 115)
    img(pdf, "ln-chair.jpg", 306, 307, 115, 115)
    img(pdf, "plant-toycar.jpg", 472, 307, 115, 115, plant=True)
    # neat centered stack -- all three on the panel's vertical axis
    bullet(pdf, 306, 186, "Do not grow", GREY_DARK)
    bullet(pdf, 306, 162, "Do not need food or water", GREY_DARK)
    bullet(pdf, 306, 138, "Do not need air", GREY_DARK)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2: circle the living things -- 12 large pictures, shuffled.
# ---------------------------------------------------------------------------
# (image, plant-library?, living?)
P2_ITEMS = [
    [("ln-fish.jpg", False, True), ("ln-ball.jpg", False, False),
     ("ln-child.jpg", False, True), ("ln-chair.jpg", False, False)],
    [("ln-teddy.jpg", False, False), ("ln-tree.jpg", False, True),
     ("plant-shoe.jpg", True, False), ("ln-butterfly.jpg", False, True)],
    [("plant-toycar.jpg", True, False), ("ln-bird.jpg", False, True),
     ("ln-house.jpg", False, False), ("plant-flower.jpg", True, True)],
]
P2_XS = [107, 240, 373, 506]
P2_TOPS = [588, 438, 288]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Living or Non-Living?")
    draw_instruction(pdf, "Circle the living things.")
    for r, top in enumerate(P2_TOPS):
        for c, x in enumerate(P2_XS):
            name, plant, _living = P2_ITEMS[r][c]
            img(pdf, name, x, top, 112, 112, plant=plant)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3: cut-and-paste sort -- 8 cards into LIVING / NON-LIVING areas.
# ---------------------------------------------------------------------------
# (image, label, plant-library?, living?) -- mixed so no pattern emerges
P3_CARDS = [
    ("ln-snail.jpg", "Snail", False, True),
    ("ln-book.jpg", "Book", False, False),
    ("ln-bicycle.jpg", "Bicycle", False, False),
    ("ln-tree.jpg", "Tree", False, True),
    ("plant-flower.jpg", "Flower", True, True),
    ("ln-clock.jpg", "Clock", False, False),
    ("ln-dog.jpg", "Dog", False, True),
    ("ln-blocks.jpg", "Toy Blocks", False, False),
]
P3_XS = [40, 164, 288, 412]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Living or Non-Living? Sort")
    draw_instruction(pdf, "Cut out the pictures. Paste them where they belong.")

    # LIVING sort area
    pdf.setFillColor(HexColor(GREEN_FILL))
    pdf.setStrokeColor(HexColor(GREEN_BORDER))
    pdf.setLineWidth(2.5)
    pdf.roundRect(40, 315, 252, 285, 16, stroke=1, fill=1)
    pdf.setFillColor(GREEN_DARK)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(166, 578, "LIVING")
    for sx in (52, 172):
        for stop in (548, 438):
            paste_slot(pdf, sx, stop, 108, 100)

    # NON-LIVING sort area
    pdf.setFillColor(HexColor(GREY_FILL))
    pdf.setStrokeColor(HexColor(GREY_BORDER))
    pdf.setLineWidth(2.5)
    pdf.roundRect(320, 315, 252, 285, 16, stroke=1, fill=1)
    pdf.setFillColor(GREY_DARK)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(446, 578, "NON-LIVING")
    for sx in (332, 452):
        for stop in (548, 438):
            paste_slot(pdf, sx, stop, 108, 100)

    # cut line + 8 cards
    cut_divider(pdf, 290)
    for k, (name, label, plant, _living) in enumerate(P3_CARDS):
        row, col = divmod(k, 4)
        top = 258 if row == 0 else 156
        cut_card(pdf, P3_XS[col], top, 118, 92, name, label, plant=plant)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4: circle what the rabbit needs -- 8 picture choices around a rabbit.
# ---------------------------------------------------------------------------
# (image, label, plant-library?, correct?) -- correct answers scattered
P4_TOP = [("ln-tv.jpg", "Television", False, False),
          ("plant-water.jpg", "Water", True, True),
          ("ln-blocks.jpg", "Blocks", False, False)]
P4_MID = [(107, "plant-shoe.jpg", "Shoe", True, False),
          (505, "ln-food.jpg", "Food", False, True)]
P4_BOTTOM = [("plant-air.jpg", "Air", True, True),
             ("ln-teddy.jpg", "Toy", False, False),
             ("ln-shelter.jpg", "Shelter", False, True)]
P4_XS = [107, 306, 505]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Does It Need?")
    draw_instruction(pdf, "Circle what the rabbit needs to live.")
    # central rabbit -- large, clearly the main subject
    img(pdf, "ln-rabbit.jpg", 306, 478, 225, 250)
    # top row of choices
    for (name, label, plant, _ok), x in zip(P4_TOP, P4_XS):
        choice(pdf, x, 590, name, label, plant=plant)
    # middle side choices
    for x, name, label, plant, _ok in P4_MID:
        choice(pdf, x, 400, name, label, plant=plant)
    # bottom row of choices
    for (name, label, plant, _ok), x in zip(P4_BOTTOM, P4_XS):
        choice(pdf, x, 215, name, label, plant=plant)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5: odd one out -- 4 rows x 4 pictures, odd position varies 1,3,2,4.
# ---------------------------------------------------------------------------
# (image, plant-library?) -- odd item: R1 ball, R2 flower, R3 clock, R4 cat
P5_ROWS = [
    [("ln-ball.jpg", False), ("ln-dog.jpg", False),
     ("ln-bird.jpg", False), ("ln-tree.jpg", False)],
    [("ln-chair.jpg", False), ("plant-shoe.jpg", True),
     ("plant-flower.jpg", True), ("plant-toycar.jpg", True)],
    [("ln-fish.jpg", False), ("ln-clock.jpg", False),
     ("ln-butterfly.jpg", False), ("ln-child.jpg", False)],
    [("ln-book.jpg", False), ("ln-cup.jpg", False),
     ("ln-teddy.jpg", False), ("ln-cat.jpg", False)],
]
P5_XS = [107, 240, 373, 506]
P5_TOPS = [588, 468, 348, 228]


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Which One Does NOT Belong?")
    draw_instruction(pdf,
                     "Look at each row. Circle the one that does NOT belong.")
    # subtle row dividers
    pdf.setStrokeColor(HexColor("#E3E8EE"))
    pdf.setLineWidth(1)
    for y in (528, 408, 288):
        pdf.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
    for r, top in enumerate(P5_TOPS):
        for c, x in enumerate(P5_XS):
            name, plant = P5_ROWS[r][c]
            img(pdf, name, x, top, 96, 96, plant=plant)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    # (title, builder, locked) -- ALL 5 PAGES APPROVED by user 2026-10-02.
    # Do not redesign, regenerate, reposition, resize or replace anything.
    ("Living & Non-Living", build_p1_page, True),
    ("Living or Non-Living?", build_p2_page, True),
    ("Living or Non-Living? Sort", build_p3_page, True),
    ("What Does It Need?", build_p4_page, True),
    ("Which One Does NOT Belong?", build_p5_page, True),
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="living-nonliving-")
    splitdir = tempfile.mkdtemp(prefix="living-nonliving-split-")
    # Split the existing prototype so locked pages are preserved byte-exact.
    if os.path.exists(OUT):
        subprocess.run(["pdfseparate", OUT,
                        os.path.join(splitdir, "p-%d.pdf")], check=True)
        n_existing = len([f for f in os.listdir(splitdir)
                          if f.endswith(".pdf")])
    else:
        n_existing = 0
    n_locked = sum(1 for _t, _b, l in PAGES if l)
    if not (n_existing == 0 or n_locked <= n_existing <= len(PAGES)):
        raise SystemExit(
            f"page mismatch: prototype has {n_existing} pages, "
            f"{n_locked} locked / {len(PAGES)} total pages configured")
    ordered = []
    li = 0
    for k, (title, builder, locked) in enumerate(PAGES):
        if locked:
            li += 1
            if li <= n_existing:
                ordered.append(os.path.join(splitdir, f"p-{li}.pdf"))
                continue
            # locked but no existing page yet: build once, then it is locked
            p = os.path.join(tmpdir, f"newpage-{k}.pdf")
            builder(p)
            ordered.append(p)
            print(f"built locked page: {title} -> {p}")
        else:
            p = os.path.join(tmpdir, f"newpage-{k}.pdf")
            builder(p)
            ordered.append(p)
            print(f"rebuilt page: {title} -> {p}")
    merged = OUT + ".new"
    subprocess.run(["pdfunite", *ordered, merged], check=True)
    os.replace(merged, OUT)
    print(f"merged {len(ordered)} page(s) ({n_locked} locked) -> {OUT}")


if __name__ == "__main__":
    main()
