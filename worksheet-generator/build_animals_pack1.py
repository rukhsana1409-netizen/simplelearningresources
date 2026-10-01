"""Animals (Pack 1) -- Preschool Thinking & Our World / Animals.

A 5-page pack about familiar animals:
  P1 Meet the Animals        -- match 8 animals to their names (2 groups of 4)
  P2 Farm, Pet or Wild?      -- cut-and-paste: sort 9 animals into 3 homes
  P3 Big or Small?           -- cut-and-paste: sort 8 animals by size
  P4 How Do Animals Move?    -- match 5 animals to how they move
  P5 Which One Does NOT Belong? -- circle the odd one out (4 rows)

Uses the reusable animal library (assets/animal-library/). All embeds are
JPEG copies so the PDF stays pushable via the GitHub blob API.

LOCKS (2026-10-01): all 5 pages user-approved and LOCKED -- never rebuilt.
P1 final (single-column matching, 86pt illustrations, shuffled names).
P2 final (Farm/Pet/Wild cut-and-paste). P3 final (Big/Small headings only).
P4 final (movement matching). P5 final (odd-one-out sets, positions 4/1/3/2).
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

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "animal-library")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "thinking", "animals",
                   "animals-prototype.pdf")


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
    pdf.drawString(title_x, PAGE_HEIGHT - 116, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    rule_y = PAGE_HEIGHT - 131
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
def img(pdf, name, cx, top, w, h=None):
    """Draw an animal-library image centered at cx, top edge at `top`."""
    h = h or w
    pdf.drawImage(os.path.join(ASSETS, name),
                  cx - w / 2, top - h, width=w, height=h,
                  preserveAspectRatio=True, anchor="c")


def vdivider(pdf, x, y0, y1):
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(1.5)
    pdf.line(x, y0, x, y1)


def paste_slot(pdf, x, top, w, h):
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1.4)
    pdf.setDash(7, 5)
    pdf.roundRect(x, top - h, w, h, 10, stroke=1, fill=0)
    pdf.setDash()


def cut_card(pdf, x, top, w, h, image, label, img_h=62, label_size=13):
    pdf.setStrokeColor(HexColor("#8A9BA8"))
    pdf.setLineWidth(1.2)
    pdf.setDash(6, 4)
    pdf.roundRect(x, top - h, w, h, 8, stroke=1, fill=0)
    pdf.setDash()
    img(pdf, image, x + w / 2, top - 8, w - 24, img_h)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", label_size)
    pdf.drawCentredString(x + w / 2, top - h + 10, label)


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


# -- small vector icons for the cut-and-paste category zones -----------------
def icon_barn(pdf, cx, cy):
    s = 21
    pdf.setFillColor(HexColor("#C0392B"))
    pdf.rect(cx - s, cy - s * 0.75, 2 * s, s * 1.35, stroke=0, fill=1)
    p = pdf.beginPath()
    p.moveTo(cx - s - 5, cy + s * 0.6)
    p.lineTo(cx, cy + s * 1.45)
    p.lineTo(cx + s + 5, cy + s * 0.6)
    p.close()
    pdf.setFillColor(HexColor("#922B21"))
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.rect(cx - s * 0.32, cy - s * 0.75, s * 0.64, s * 0.85,
             stroke=0, fill=1)


def icon_house(pdf, cx, cy):
    s = 21
    pdf.setFillColor(HexColor("#2E86C1"))
    pdf.rect(cx - s, cy - s * 0.75, 2 * s, s * 1.35, stroke=0, fill=1)
    p = pdf.beginPath()
    p.moveTo(cx - s - 5, cy + s * 0.6)
    p.lineTo(cx, cy + s * 1.45)
    p.lineTo(cx + s + 5, cy + s * 0.6)
    p.close()
    pdf.setFillColor(HexColor("#1A5276"))
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.circle(cx, cy + s * 0.05, s * 0.34, stroke=0, fill=1)


def icon_tree(pdf, cx, cy):
    pdf.setFillColor(HexColor("#229954"))
    for wdt, yb in [(46, -6), (34, 12)]:
        p = pdf.beginPath()
        p.moveTo(cx - wdt / 2, cy + yb)
        p.lineTo(cx, cy + yb + 30)
        p.lineTo(cx + wdt / 2, cy + yb)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#7D4E2D"))
    pdf.rect(cx - 5, cy - 30, 10, 26, stroke=0, fill=1)


def zone_band(pdf, top, h, tint, border, icon_fn, word, slot_xs, slot_w=100,
              slot_h=75, word_size=19):
    y = top - h
    pdf.setFillColor(tint)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.5)
    pdf.roundRect(MARGIN, y, PAGE_WIDTH - 2 * MARGIN, h, 14,
                  stroke=1, fill=1)
    icon_fn(pdf, 88, y + h / 2)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", word_size)
    pdf.drawString(122, y + h / 2 - 7, word)
    slot_top = y + (h + slot_h) / 2
    for sx in slot_xs:
        paste_slot(pdf, sx, slot_top, slot_w, slot_h)
    return y


# ---------------------------------------------------------------------------
# Page 1: Meet the Animals -- one simple matching activity (redesigned
# 2026-10-01 v2, refined v3): a single vertical column of 6 animal pictures
# on the left, a shuffled vertical column of the 6 names on the right, a
# clearly visible teal matching dot beside every animal and beside every
# word, and a large clean blank middle for drawing lines. No word sits
# close enough to an animal to read as its label; no answer is directly
# across from its animal. With 6 rows the illustrations are ~40% larger
# than the 8-row version so each animal is instantly recognizable in print.
# ---------------------------------------------------------------------------
P1_ANIMALS = ["Dog", "Cat", "Cow", "Horse", "Lion", "Elephant"]
P1_IMAGES = {"Dog": "lib-dog.jpg", "Cat": "lib-cat.jpg",
             "Cow": "lib-cow.jpg", "Horse": "lib-horse.jpg",
             "Lion": "lib-lion.jpg", "Elephant": "style-test-elephant.jpg"}
# Shuffled so nothing matches straight across.
P1_NAMES = ["Cat", "Horse", "Dog", "Elephant", "Cow", "Lion"]
P1_ROW_TOPS = [604, 512, 420, 328, 236, 144]
P1_IMG = 86
P1_PIC_CX, P1_DOT_L, P1_DOT_R, P1_NAME_CX = 140, 205, 407, 472


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Animals", "Meet the Animals")
    draw_instruction(pdf, "Draw a line to match each animal to its name.")
    vdivider(pdf, 306, 110, 614)
    for k, top in enumerate(P1_ROW_TOPS):
        animal = P1_ANIMALS[k]
        img(pdf, P1_IMAGES[animal], P1_PIC_CX, top, P1_IMG)
        cy = top - P1_IMG / 2
        pdf.setFillColor(TEAL)
        pdf.circle(P1_DOT_L, cy, 7, stroke=0, fill=1)
        pdf.circle(P1_DOT_R, cy, 7, stroke=0, fill=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 19)
        pdf.drawCentredString(P1_NAME_CX, cy - 7, P1_NAMES[k])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2: Farm, Pet or Wild? -- cut-and-paste.
# ---------------------------------------------------------------------------
P2_ZONES = [
    ("Farm", icon_barn, HexColor("#FDEDEC"), HexColor("#E6A9A3"),
     [("lib-chicken.jpg", "Chicken"), ("lib-sheep.jpg", "Sheep"),
      ("lib-goat.jpg", "Goat")]),
    ("Pet", icon_house, HexColor("#EBF5FB"), HexColor("#A9CCE3"),
     [("style-test-rabbit.jpg", "Rabbit"), ("lib-hamster.jpg", "Hamster"),
      ("lib-goldfish.jpg", "Goldfish")]),
    ("Wild", icon_tree, HexColor("#EAFAF1"), HexColor("#A9DFBF"),
     [("lib-tiger.jpg", "Tiger"), ("lib-bear.jpg", "Bear"),
      ("lib-zebra.jpg", "Zebra")]),
]
P2_ZONE_TOPS = [608, 526, 444]
P2_SLOT_XS = [235, 350, 465]
# Shuffled cut-out order (no two cards from the same zone side by side).
P2_CARDS = [("lib-chicken.jpg", "Chicken"), ("style-test-rabbit.jpg", "Rabbit"),
            ("lib-tiger.jpg", "Tiger"), ("lib-sheep.jpg", "Sheep"),
            ("lib-hamster.jpg", "Hamster"), ("lib-zebra.jpg", "Zebra"),
            ("lib-goat.jpg", "Goat"), ("lib-goldfish.jpg", "Goldfish"),
            ("lib-bear.jpg", "Bear")]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Animals", "Farm, Pet or Wild?")
    draw_instruction(pdf, "Cut out the animals. Paste each one where it belongs!")
    for z, top in zip(P2_ZONES, P2_ZONE_TOPS):
        word, icon_fn, tint, border, _animals = z
        zone_band(pdf, top, 78, tint, border, icon_fn, word, P2_SLOT_XS,
                  slot_w=96, slot_h=62)
    cut_divider(pdf, 362)
    card_w, card_h = 140, 96
    xs = [75, 236, 397]
    tops = [350, 250, 150]
    for k, (image, label) in enumerate(P2_CARDS):
        col, row = k % 3, k // 3
        cut_card(pdf, xs[col], tops[row], card_w, card_h, image, label,
                 img_h=60, label_size=12)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3: Big or Small? -- cut-and-paste (revised 2026-10-01 per user
# review: thumbnail icons beside BIG/SMALL removed; headings alone).
# ---------------------------------------------------------------------------
P3_BIG = [("style-test-elephant.jpg", "Elephant"),
          ("lib-giraffe.jpg", "Giraffe"), ("lib-hippo.jpg", "Hippo"),
          ("lib-rhino.jpg", "Rhino")]
P3_SMALL = [("lib-mouse.jpg", "Mouse"), ("lib-butterfly.jpg", "Butterfly"),
            ("lib-ladybug.jpg", "Ladybug"), ("lib-ant.jpg", "Ant")]
# Shuffled cut-out order.
P3_CARDS = [("lib-mouse.jpg", "Mouse"), ("lib-giraffe.jpg", "Giraffe"),
            ("lib-ant.jpg", "Ant"), ("lib-hippo.jpg", "Hippo"),
            ("lib-butterfly.jpg", "Butterfly"), ("lib-rhino.jpg", "Rhino"),
            ("lib-ladybug.jpg", "Ladybug"),
            ("style-test-elephant.jpg", "Elephant")]


def _p3_panel(pdf, x, top, w, h, tint, border, word, slot_xs,
              slot_top1, slot_top2):
    y = top - h
    pdf.setFillColor(tint)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.5)
    pdf.roundRect(x, y, w, h, 14, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 21)
    pdf.drawCentredString(x + w / 2, top - 40, word)
    for sx in slot_xs:
        paste_slot(pdf, sx, slot_top1, 105, 80)
    for sx in slot_xs:
        paste_slot(pdf, sx, slot_top2, 105, 80)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Animals", "Big or Small?")
    draw_instruction(pdf, "Cut out the animals. Paste each one in the right box!")
    pw = 256
    _p3_panel(pdf, MARGIN, 610, pw, 242,
              HexColor("#FEF9E7"), HexColor("#F0D27A"),
              "BIG",
              [MARGIN + 22, MARGIN + 139], 548, 458)
    _p3_panel(pdf, PAGE_WIDTH - MARGIN - pw, 610, pw, 242,
              HexColor("#F4ECF7"), HexColor("#CDB4E8"),
              "SMALL",
              [PAGE_WIDTH - MARGIN - pw + 22, PAGE_WIDTH - MARGIN - pw + 139],
              548, 458)
    cut_divider(pdf, 348)
    card_w, card_h = 122, 102
    xs = [47, 179, 311, 443]
    tops = [332, 222]
    for k, (image, label) in enumerate(P3_CARDS):
        col, row = k % 4, k // 4
        cut_card(pdf, xs[col], tops[row], card_w, card_h, image, label,
                 img_h=58, label_size=12)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4: How Do Animals Move? -- match each animal to how it moves.
# ---------------------------------------------------------------------------
P4_ANIMALS = [("lib-eagle-fly.jpg", "Eagle"),
              ("style-test-fish.jpg", "Fish"),
              ("lib-frog-hop.jpg", "Frog"),
              ("lib-cheetah-run.jpg", "Cheetah"),
              ("lib-monkey-swing.jpg", "Monkey")]
P4_MOVES = ["Swim", "Hop", "Fly", "Swing", "Run"]
P4_ROW_TOPS = [588, 483, 378, 273, 168]
P4_IMG = 92


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Animals", "How Do Animals Move?")
    draw_instruction(pdf, "Draw a line to match each animal to how it moves.")
    vdivider(pdf, 306, 90, 605)
    for k, top in enumerate(P4_ROW_TOPS):
        image, label = P4_ANIMALS[k]
        img(pdf, image, 150, top, P4_IMG)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(150, top - P4_IMG - 14, label)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 23)
        pdf.drawCentredString(462, top - P4_IMG / 2 - 8, P4_MOVES[k])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5: Which One Does NOT Belong? -- circle the odd one out.
# (Revised 2026-10-01 per user review: four preschool-obvious sets, all
# from the approved library, odd positions 4/1/3/2.)
#   Row 1: 3 farm animals + 1 wild animal      -> Lion (4th)
#   Row 2: 3 animals that fly + 1 that cannot  -> Fish (1st)
#   Row 3: 3 pets + 1 wild animal              -> Bear (3rd)
#   Row 4: 3 large animals + 1 very small      -> Mouse (2nd)
# ---------------------------------------------------------------------------
P5_ROWS = [
    [("lib-cow.jpg", "Cow"), ("lib-pig.jpg", "Pig"),
     ("lib-sheep.jpg", "Sheep"), ("lib-lion.jpg", "Lion")],
    [("style-test-fish.jpg", "Fish"), ("lib-eagle-fly.jpg", "Eagle"),
     ("lib-butterfly.jpg", "Butterfly"), ("lib-bee.jpg", "Bee")],
    [("lib-dog.jpg", "Dog"), ("lib-cat.jpg", "Cat"),
     ("lib-bear.jpg", "Bear"), ("style-test-rabbit.jpg", "Rabbit")],
    [("style-test-elephant.jpg", "Elephant"), ("lib-mouse.jpg", "Mouse"),
     ("lib-hippo.jpg", "Hippo"), ("lib-giraffe.jpg", "Giraffe")],
]
P5_ROW_TOPS = [592, 462, 332, 202]
P5_XS = [106, 239, 372, 505]
P5_IMG = 100


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Animals", "Which One Does NOT Belong?")
    draw_instruction(pdf, "Look at each row. Circle the animal that does not belong!")
    for row, top in zip(P5_ROWS, P5_ROW_TOPS):
        for k, (image, label) in enumerate(row):
            img(pdf, image, P5_XS[k], top, P5_IMG)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawCentredString(P5_XS[k], top - P5_IMG - 12, label)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    # LOCKED 2026-10-01: user approved "Meet the Animals" (final) -- do not change.
    ("Meet the Animals", build_p1_page, True),
    # LOCKED 2026-10-01: user approved "Farm, Pet or Wild?" -- do not change.
    ("Farm, Pet or Wild?", build_p2_page, True),
    # LOCKED 2026-10-01: user approved "Big or Small?" -- do not change.
    ("Big or Small?", build_p3_page, True),
    # LOCKED 2026-10-01: user approved "How Do Animals Move?" -- do not change.
    ("How Do Animals Move?", build_p4_page, True),
    # LOCKED 2026-10-01: user approved "Which One Does NOT Belong?" -- do not change.
    ("Which One Does NOT Belong?", build_p5_page, True),
]


def main():
    tmpdir = tempfile.mkdtemp(prefix="an1-")
    if not os.path.exists(OUT):
        ordered = []
        for k, (title, builder, _locked) in enumerate(PAGES):
            p = os.path.join(tmpdir, f"page-{k}.pdf")
            builder(p)
            ordered.append(p)
            print(f"built page: {title} -> {p}")
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        subprocess.run(["pdfunite", *ordered, OUT], check=True)
        print(f"built {len(ordered)} page(s) -> {OUT}")
        return
    splitdir = tempfile.mkdtemp(prefix="an1-split-")
    subprocess.run(["pdfseparate", OUT, os.path.join(splitdir, "p-%d.pdf")],
                   check=True)
    n_existing = len([f for f in os.listdir(splitdir) if f.endswith(".pdf")])
    n_locked = sum(1 for _, _, locked in PAGES if locked)
    if not (n_locked <= n_existing <= len(PAGES)):
        raise SystemExit(
            f"page mismatch: prototype has {n_existing} pages, "
            f"{n_locked} locked / {len(PAGES)} total pages configured")
    ordered = []
    for k, (title, builder, locked) in enumerate(PAGES):
        if locked:
            ordered.append(os.path.join(splitdir, f"p-{k + 1}.pdf"))
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
