"""Plants -- Preschool Science & Discovery / Plants & Nature.

A 5-page pack introducing plants to preschoolers:
  P1 Parts of a Plant        -- teaching page: labeled plant with leader lines
  P2 Parts of a Plant: Match -- draw a line to match part pictures to words
  P3 What Do Plants Need?    -- circle what a plant needs to grow
  P4 Plant Life Cycle        -- cut-and-paste sequencing (4 stages)
  P5 My Plant                -- draw your own plant (pot with soil provided)

Uses the plant library (assets/plant-library/). All embeds are JPEG copies
so the PDF stays pushable via the GitHub blob API.

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
                      "assets", "plant-library")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "science", "plants",
                   "plants-prototype.pdf")


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


def label_with_leader(pdf, text, lx, ly, align, tx, ty):
    """Draw a part label with a clean leader line to the target point."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    if align == "right":
        pdf.drawRightString(lx, ly, text)
        sx = lx - pdf.stringWidth(text, "Helvetica-Bold", 15) - 10
    elif align == "left":
        pdf.drawString(lx, ly, text)
        sx = lx + pdf.stringWidth(text, "Helvetica-Bold", 15) + 10
    else:
        pdf.drawCentredString(lx, ly, text)
        sx = lx
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.3)
    pdf.line(sx, ly + 4, tx, ty)
    pdf.setFillColor(TEAL)
    pdf.circle(tx, ty, 3.2, fill=1, stroke=0)


PACK_TITLE = "Plants"


# ---------------------------------------------------------------------------
# Page 1: Parts of a Plant -- teaching page with leader-line labels.
# ---------------------------------------------------------------------------
def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Parts of a Plant")
    draw_instruction(pdf, "Look at the plant. Can you find each part?")
    # Large plant, the visual focus of the page. plant-full.jpg is a tight
    # portrait crop (1070x1277); part positions are fractions of the fitted
    # rect: flower top-center, leaves mid-right, stem center, roots bottom.
    # Enlarged and lowered slightly so the teaching content fills the page
    # more generously while keeping clear spacing.
    pw, ph = 310, 370
    pcx, ptop = 292, 622
    img(pdf, "plant-full.jpg", pcx, ptop, pw, ph)
    fx = lambda f: pcx - pw / 2 + f * pw
    fy = lambda f: ptop - f * ph
    label_with_leader(pdf, "Flower", 520, fy(0.09), "right", fx(0.50), fy(0.09))
    label_with_leader(pdf, "Leaves", 520, fy(0.38), "right", fx(0.68), fy(0.38))
    label_with_leader(pdf, "Stem", 520, fy(0.56), "right", fx(0.50), fy(0.56))
    label_with_leader(pdf, "Roots", 60, fy(0.90), "left", fx(0.50), fy(0.90))
    # The seed sits apart at the bottom: every plant starts as a seed.
    img(pdf, "plant-seed.jpg", 92, 278, 86)
    label_with_leader(pdf, "Seed", 92, 164, "center", 92, 196)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2: Parts of a Plant -- Match.
# Left pictures top-to-bottom: Flower, Leaf, Stem, Roots, Seed.
# Right words shuffled so no correct word sits directly across.
# ---------------------------------------------------------------------------
P2_LEFT = [("plant-flower.jpg", "Flower"), ("plant-leaf.jpg", "Leaf"),
           ("plant-stem.jpg", "Stem"), ("plant-roots.jpg", "Roots"),
           ("plant-seed.jpg", "Seed")]
P2_RIGHT_WORDS = ["Roots", "Seed", "Leaf", "Flower", "Stem"]
P2_ROW_TOPS = [590, 485, 380, 275, 170]
P2_LEFT_CX, P2_RIGHT_CX = 130, 440


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Parts of a Plant: Match")
    draw_instruction(pdf, "Draw a line to match each part to its name.")
    vdivider(pdf, 306, 92, 605)
    for k, top in enumerate(P2_ROW_TOPS):
        limage, llabel = P2_LEFT[k]
        img(pdf, limage, P2_LEFT_CX, top, 88)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawCentredString(P2_LEFT_CX, top - 88 - 14, llabel)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(P2_RIGHT_CX, top - 44, P2_RIGHT_WORDS[k])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3: What Do Plants Need? -- circle the correct choices.
# Correct: Sunlight, Water, Soil, Air. Distractors: Candy, Toy Car, Shoe.
# ---------------------------------------------------------------------------
P3_TOP = [("plant-candy.jpg", "Candy"), ("plant-sun.jpg", "Sunlight"),
          ("plant-toycar.jpg", "Toy Car"), ("plant-water.jpg", "Water")]
P3_TOP_XS = [105, 241, 377, 513]
P3_BOTTOM = [("plant-shoe.jpg", "Shoe"), ("plant-soil.jpg", "Soil"),
             ("plant-air.jpg", "Air")]
P3_BOTTOM_XS = [173, 306, 439]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Do Plants Need?")
    draw_instruction(pdf, "Circle what a plant needs to grow.")
    # Healthy plant in the center, large and prominent.
    img(pdf, "plant-full.jpg", 306, 488, 148, 205)
    for xs, items, top in ((P3_TOP_XS, P3_TOP, 592),
                           (P3_BOTTOM_XS, P3_BOTTOM, 262)):
        for cx, (image, label) in zip(xs, items):
            img(pdf, image, cx, top, 96)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawCentredString(cx, top - 96 - 14, label)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4: Plant Life Cycle -- cut-and-paste sequencing.
# Order: Seed -> Sprout -> Young Plant -> Flowering Plant.
# ---------------------------------------------------------------------------
P4_STAGES = [("plant-seed.jpg", "Seed"),
             ("plant-sprout.jpg", "Sprout"),
             ("plant-young.jpg", "Young Plant"),
             ("plant-full.jpg", "Flowering Plant")]
# Shuffled cut-out order so the sequence is not given away.
P4_CARDS = [("plant-young.jpg", "Young Plant"),
            ("plant-seed.jpg", "Seed"),
            ("plant-full.jpg", "Flowering Plant"),
            ("plant-sprout.jpg", "Sprout")]
P4_XS = [43, 179, 315, 451]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Plant Life Cycle")
    draw_instruction(pdf, "Cut out the pictures. Paste them in order!")
    # Four numbered sequence boxes.
    box_top, box_h, box_w = 600, 112, 118
    for k, x in enumerate(P4_XS):
        paste_slot(pdf, x, box_top, box_w, box_h)
        pdf.setFillColor(TEAL)
        pdf.circle(x + 20, box_top - 20, 13, fill=1, stroke=0)
        pdf.setFillColor(white)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(x + 20, box_top - 26, str(k + 1))
        if k < 3:
            ax = x + box_w + 9
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(2.5)
            pdf.line(ax, box_top - box_h / 2 - 8, ax + 14,
                     box_top - box_h / 2)
            pdf.line(ax, box_top - box_h / 2 + 8, ax + 14,
                     box_top - box_h / 2)
    # Cut-out cards below.
    cut_divider(pdf, 452)
    card_top, card_h, card_w = 436, 128, 118
    for k, (image, label) in enumerate(P4_CARDS):
        cut_card(pdf, P4_XS[k], card_top, card_w, card_h, image, label,
                 img_h=76, label_size=12)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5: My Plant -- draw your own plant.
# ---------------------------------------------------------------------------
def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Plant")
    draw_instruction(pdf, "Draw your own plant. Add a stem, leaves and a flower.")
    # Generous open drawing area with the pot of soil waiting at the bottom.
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1.6)
    pdf.setDash(9, 6)
    pdf.roundRect(60, 96, PAGE_WIDTH - 120, 508, 16, stroke=1, fill=0)
    pdf.setDash()
    img(pdf, "plant-pot.jpg", 306, 296, 250)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Parts of a Plant", build_p1_page, True),          # APPROVED by user 2026-10-01 — locked, no changes
    ("Parts of a Plant: Match", build_p2_page, True),   # APPROVED by user 2026-10-01 — locked, no changes
    ("What Do Plants Need?", build_p3_page, True),      # APPROVED by user 2026-10-01 — locked, no changes
    ("Plant Life Cycle", build_p4_page, True),          # APPROVED by user 2026-10-01 — locked, no changes
    ("My Plant", build_p5_page, True),                  # APPROVED by user 2026-10-01 — locked, no changes
]


def main():
    tmpdir = tempfile.mkdtemp(prefix="plants-")
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
    splitdir = tempfile.mkdtemp(prefix="plants-split-")
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
