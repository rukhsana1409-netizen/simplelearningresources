"""Animals & Their World (Pack 2) -- Preschool Thinking & Our World / Animals.

A 5-page pack about where animals live and animal families:
  P1 Animal Habitats  -- match 5 animals to where they live
  P2 Animal Babies     -- match 5 animals to their babies
  P3 Animal Homes      -- match 5 animals to their homes
  P4 Where Do They Belong? -- cut-and-paste: Farm / Ocean / Forest
  P5 Find the Baby!    -- circle the baby in each row (4 rows)

Uses the reusable animal library (assets/animal-library/). All embeds are
JPEG copies so the PDF stays pushable via the GitHub blob API.

Minimal reading, one obvious task per page, generous cut-and-paste room.
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
                      "assets", "animal-library")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "thinking", "animals",
                   "animals-and-their-world-prototype.pdf")


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


def icon_wave(pdf, cx, cy):
    pdf.setStrokeColor(HexColor("#2E86C1"))
    pdf.setLineWidth(3)
    for dy in (-12, 0, 12):
        p = pdf.beginPath()
        p.moveTo(cx - 24, cy + dy)
        p.curveTo(cx - 12, cy + dy - 10, cx - 4, cy + dy - 10,
                  cx + 8, cy + dy)
        p.curveTo(cx + 20, cy + dy + 10, cx + 24, cy + dy + 10,
                  cx + 30, cy + dy)
        pdf.drawPath(p, stroke=1, fill=0)


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
# Shared 5-row matching page (animals on the left, shuffled matches right)
# ---------------------------------------------------------------------------
ROW_TOPS = [590, 485, 380, 275, 170]
LEFT_IMG, LEFT_CX = 88, 130
RIGHT_CX = 440


def matching_page(path, title, subtitle, instruction, left_items,
                  right_items, right_w=150, right_h=88,
                  right_label_size=14):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, title, subtitle)
    draw_instruction(pdf, instruction)
    vdivider(pdf, 306, 92, 605)
    for k, top in enumerate(ROW_TOPS):
        limage, llabel = left_items[k]
        rimage, rlabel = right_items[k]
        img(pdf, limage, LEFT_CX, top, LEFT_IMG)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawCentredString(LEFT_CX, top - LEFT_IMG - 14, llabel)
        img(pdf, rimage, RIGHT_CX, top, right_w, right_h)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", right_label_size)
        pdf.drawCentredString(RIGHT_CX, top - right_h - 14, rlabel)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PACK_TITLE = "Animals & Their World"


# ---------------------------------------------------------------------------
# Page 1: Animal Habitats -- match each animal to where it lives.
# ---------------------------------------------------------------------------
P1_LEFT = [("lib-polar-bear.jpg", "Polar Bear"), ("lib-camel.jpg", "Camel"),
           ("lib-shark.jpg", "Shark"), ("lib-frog.jpg", "Frog"),
           ("lib-owl.jpg", "Owl")]
P1_RIGHT = [("lib-habitat-desert.jpg", "Desert"),
            ("lib-habitat-ocean.jpg", "Ocean"),
            ("lib-habitat-forest.jpg", "Forest"),
            ("lib-habitat-ice.jpg", "Ice"),
            ("lib-habitat-pond.jpg", "Pond")]


def build_p1_page(path):
    matching_page(path, PACK_TITLE, "Animal Habitats",
                  "Draw a line to match each animal to where it lives.",
                  P1_LEFT, P1_RIGHT)


# ---------------------------------------------------------------------------
# Page 2: Animal Babies -- match each animal to its baby.
# (Revised 2026-10-01 per user review: illustrations enlarged ~27% on both
# sides. Uses its own builder so the approved P1/P3 shared matching_page
# layout is not touched.)
# ---------------------------------------------------------------------------
P2_LEFT = [("lib-cow.jpg", "Cow"), ("lib-sheep.jpg", "Sheep"),
           ("lib-horse.jpg", "Horse"), ("lib-pig.jpg", "Pig"),
           ("lib-duck.jpg", "Duck")]
P2_RIGHT = [("lib-lamb.jpg", "Lamb"), ("lib-piglet.jpg", "Piglet"),
            ("lib-duckling.jpg", "Duckling"), ("lib-calf.jpg", "Calf"),
            ("lib-foal.jpg", "Foal")]
P2_ROW_TOPS = [604, 496, 388, 280, 172]
P2_IMG = 112
P2_LEFT_CX, P2_RIGHT_CX = 130, 440


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Animal Babies")
    draw_instruction(pdf, "Draw a line to match each animal to its baby.")
    vdivider(pdf, 306, 60, 610)
    for k, top in enumerate(P2_ROW_TOPS):
        limage, llabel = P2_LEFT[k]
        rimage, rlabel = P2_RIGHT[k]
        img(pdf, limage, P2_LEFT_CX, top, P2_IMG)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawCentredString(P2_LEFT_CX, top - P2_IMG - 12, llabel)
        img(pdf, rimage, P2_RIGHT_CX, top, P2_IMG)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(P2_RIGHT_CX, top - P2_IMG - 12, rlabel)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3: Animal Homes -- match each animal to its home.
# ---------------------------------------------------------------------------
P3_LEFT = [("lib-bird.jpg", "Bird"), ("lib-bee.jpg", "Bee"),
           ("lib-dog.jpg", "Dog"), ("style-test-rabbit.jpg", "Rabbit"),
           ("lib-chicken.jpg", "Chicken")]
P3_RIGHT = [("lib-hive.jpg", "Hive"), ("lib-doghouse.jpg", "Doghouse"),
            ("lib-burrow.jpg", "Burrow"), ("lib-coop.jpg", "Coop"),
            ("lib-nest.jpg", "Nest")]


def build_p3_page(path):
    matching_page(path, PACK_TITLE, "Animal Homes",
                  "Draw a line to match each animal to its home.",
                  P3_LEFT, P3_RIGHT, right_w=110)


# ---------------------------------------------------------------------------
# Page 4: Where Do They Belong? -- cut-and-paste: Farm / Ocean / Forest.
# ---------------------------------------------------------------------------
P4_ZONES = [
    ("Farm", icon_barn, HexColor("#FDEDEC"), HexColor("#E6A9A3")),
    ("Ocean", icon_wave, HexColor("#EBF5FB"), HexColor("#A9CCE3")),
    ("Forest", icon_tree, HexColor("#EAFAF1"), HexColor("#A9DFBF")),
]
P4_ZONE_TOPS = [608, 526, 444]
P4_SLOT_XS = [235, 350, 465]
# Shuffled cut-out order (revised 2026-10-01 per user review): categories are
# mixed both horizontally and vertically so the sorting answer is not
# revealed by the grid. Grid reads:
#   Row 1: Cow | Owl | Whale
#   Row 2: Shark | Chicken | Bear
#   Row 3: Deer | Pig | Fish
P4_CARDS = [("lib-cow.jpg", "Cow"), ("lib-owl.jpg", "Owl"),
            ("lib-whale.jpg", "Whale"), ("lib-shark.jpg", "Shark"),
            ("lib-chicken.jpg", "Chicken"), ("lib-bear.jpg", "Bear"),
            ("lib-deer.jpg", "Deer"), ("lib-pig.jpg", "Pig"),
            ("style-test-fish.jpg", "Fish")]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Where Do They Belong?")
    draw_instruction(pdf, "Cut out the animals. Paste each one where it belongs!")
    for z, top in zip(P4_ZONES, P4_ZONE_TOPS):
        word, icon_fn, tint, border = z
        zone_band(pdf, top, 78, tint, border, icon_fn, word, P4_SLOT_XS,
                  slot_w=96, slot_h=62)
    cut_divider(pdf, 362)
    card_w, card_h = 140, 96
    xs = [75, 236, 397]
    tops = [350, 250, 150]
    for k, (image, label) in enumerate(P4_CARDS):
        col, row = k % 3, k // 3
        cut_card(pdf, xs[col], tops[row], card_w, card_h, image, label,
                 img_h=60, label_size=12)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5: Find the Baby! -- circle the baby in each row.
# (Redesigned 2026-10-01 per user review, v3: arrows removed entirely --
# they suggested an answer. Each of the 4 sections now reads as an adult
# question cue on the left with 3 large, equally prominent baby choices
# to its right. Nothing points at or emphasizes any answer.
# Correct-answer columns vary: 0, 2, 1, 0.)
# ---------------------------------------------------------------------------
P5_ROWS = [
    (("lib-lion.jpg", "Lion"),
     [("lib-cub.jpg", "Cub"), ("lib-lamb.jpg", "Lamb"),
      ("lib-piglet.jpg", "Piglet")]),
    (("lib-penguin.jpg", "Penguin"),
     [("lib-foal.jpg", "Foal"), ("lib-duckling.jpg", "Duckling"),
      ("lib-chick.jpg", "Chick")]),
    (("lib-kangaroo.jpg", "Kangaroo"),
     [("lib-calf.jpg", "Calf"), ("lib-joey.jpg", "Joey"),
      ("lib-lamb.jpg", "Lamb")]),
    (("lib-frog.jpg", "Frog"),
     [("lib-tadpole.jpg", "Tadpole"), ("lib-piglet.jpg", "Piglet"),
      ("lib-foal.jpg", "Foal")]),
]
P5_ROW_TOPS = [602, 464, 326, 188]
P5_PARENT_CX = 105
P5_CHOICE_XS = [242, 366, 490]
P5_PARENT_IMG, P5_CHOICE_IMG = 115, 105


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Find the Baby!")
    draw_instruction(pdf, "Look at each row. Circle the baby!")
    for (pimage, plabel), choices, top in zip(
            [r[0] for r in P5_ROWS], [r[1] for r in P5_ROWS], P5_ROW_TOPS):
        img(pdf, pimage, P5_PARENT_CX, top, P5_PARENT_IMG)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(P5_PARENT_CX, top - P5_PARENT_IMG - 15, plabel)
        for cx, (cimage, clabel) in zip(P5_CHOICE_XS, choices):
            img(pdf, cimage, cx, top, P5_CHOICE_IMG)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawCentredString(cx, top - P5_CHOICE_IMG - 14, clabel)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    # LOCKED 2026-10-01: user approved "Animal Habitats" -- do not change.
    ("Animal Habitats", build_p1_page, True),
    # LOCKED 2026-10-01: user approved "Animal Babies" (final) -- do not change.
    ("Animal Babies", build_p2_page, True),
    # LOCKED 2026-10-01: user approved "Animal Homes" -- do not change.
    ("Animal Homes", build_p3_page, True),
    # LOCKED 2026-10-01: user approved "Where Do They Belong?" (final) -- do not change.
    ("Where Do They Belong?", build_p4_page, True),
    # LOCKED 2026-10-01: user approved "Find the Baby!" (final) -- do not change.
    ("Find the Baby!", build_p5_page, True),
]


def main():
    tmpdir = tempfile.mkdtemp(prefix="an2-")
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
    splitdir = tempfile.mkdtemp(prefix="an2-split-")
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
