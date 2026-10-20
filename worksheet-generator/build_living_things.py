#!/usr/bin/env python3
"""Living Things — Needs, Habitats & Environmental Changes
(Kindergarten Science).

Michigan K-LS1-1 (patterns of what plants and animals need to
survive), K-ESS3-1 (the relationship between an animal's needs and
the place it lives), K-ESS2-2 (how living things change the
environment to meet their needs). Step-up from the preschool packs:
preschool covered single-organism needs recognition, habitat/home
matching, and life-cycle ordering; this pack adds comparison,
need-to-evidence reasoning, environmental change, and real
longitudinal observation.

Accuracy rules honored:
  - Page 1: WATER and AIR are the shared needs; SUNLIGHT is
    plant-only (plants make their own food from sunlight, water and
    air); FOOD-TO-EAT is animal-only (animals eat food). Sunlight is
    never presented as an animal need, and plants are never said to
    eat.
  - Page 2: one habitat, three needs, evidence inside the scene
    (water to swim and keep skin wet, insects to eat, plants to hide
    under) — not animal-to-habitat matching.
  - Page 3: beaver dam (stream slowed, pond formed), worms (tunnels,
    mixed soil, castings), tree roots (sidewalk slabs lifted) — the
    child circles what is NEW in each AFTER picture. The bird/nest
    example from the original brief was replaced by tree roots at the
    user's direction, which also covers plants changing the
    environment under K-ESS2-2.
  - Page 4: a reusable real-plant observation sheet; dates, drawings
    and cube measurements are the child's own — nothing prefilled,
    no growth amount promised or printed.

No separate parent guide: adult steps are printed on each page, and
the objective / answers / facilitation notes live in the website
resource-page text.

Page map:
  1 What Do They Both Need? — cut-and-paste needs sort: plant / both
                              / animal (bean plant vs dog)
  2 Why This Habitat?       — pond scene; draw lines from three need
                              cards to the evidence in the scene;
                              dictated "because" sentence
  3 Living Things Change Places — before/after strips (beaver, worm,
                              tree roots); circle what is new
  4 Watch It Grow           — reusable bean-plant observation sheet:
                              date, drawing, cube height strip
"""
import math
import os
import sys

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_phonics_az import (  # noqa: E402
    INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL, draw_footer, draw_header,
)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "living-things")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "science",
                       "living-things")
PACK_TITLE = "Living Things"
STEM = "living-things"

MARGIN = 60
RULE = HexColor("#9DB8C4")
LIGHT = HexColor("#EAF3F1")
PANEL_FILL = HexColor("#F2F8F8")
GOLD = HexColor("#F4B63E")
BLUE = HexColor("#2E6FB7")
BROWN = HexColor("#8A5A2B")
GREEN = HexColor("#3E7C4F")

PLANT = os.path.join(ASSETS, "lt-plant.jpg")
DOG = os.path.join(ASSETS, "lt-dog.jpg")
POND = os.path.join(ASSETS, "lt-pond.jpg")
BEAVER_B = os.path.join(ASSETS, "lt-beaver-before.jpg")
BEAVER_A = os.path.join(ASSETS, "lt-beaver-after.jpg")
WORM_B = os.path.join(ASSETS, "lt-worm-before.jpg")
WORM_A = os.path.join(ASSETS, "lt-worm-after.jpg")
ROOTS_B = os.path.join(ASSETS, "lt-roots-before.jpg")
ROOTS_A = os.path.join(ASSETS, "lt-roots-after.jpg")


def _adult(pdf, lines, top=74, step=16):
    pdf.setFillColor(INK)
    for i, line in enumerate(lines):
        pdf.setFont("Helvetica-Bold", 11.5 if i == 0 else 11)
        pdf.drawCentredString(PAGE_WIDTH / 2, top - i * step, line)


def _instruction(pdf, text, y=616, size=19):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(PAGE_WIDTH / 2, y, text)


def _img_fill(pdf, path, x, y, w, h, focus_x=0.5, focus_y=0.5):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx = x + (w - dw) * focus_x
    dy = y + (h - dh) * focus_y
    pdf.saveState()
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, 14)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.drawImage(ImageReader(path), dx, dy, dw, dh,
                  preserveAspectRatio=False, mask="auto")
    pdf.restoreState()
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.6)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, 14)
    pdf.drawPath(p, stroke=1, fill=0)


def _frame(pdf, x, y, w, h, r=12):
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.4)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.drawPath(p, stroke=1, fill=0)


def _panel(pdf, x, y, w, h, r=12):
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.3)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.drawPath(p, stroke=1, fill=1)


# ------------------------------------------------------------- chip icons
def chip_icon(pdf, cx, cy, kind, s=30):
    if kind == "sun":
        pdf.setStrokeColor(GOLD)
        pdf.setLineWidth(3)
        for a in range(0, 360, 45):
            rad = math.radians(a)
            pdf.line(cx + math.cos(rad) * s * 0.42,
                     cy + math.sin(rad) * s * 0.42,
                     cx + math.cos(rad) * s * 0.62,
                     cy + math.sin(rad) * s * 0.62)
        pdf.setFillColor(GOLD)
        pdf.circle(cx, cy, s * 0.34, stroke=0, fill=1)
    elif kind == "water":
        pdf.setFillColor(BLUE)
        p = pdf.beginPath()
        p.moveTo(cx, cy + s * 0.55)
        p.curveTo(cx - s * 0.42, cy + s * 0.05, cx - s * 0.34,
                  cy - s * 0.30, cx - s * 0.17, cy - s * 0.38)
        p.curveTo(cx - s * 0.05, cy - s * 0.46, cx + s * 0.05,
                  cy - s * 0.46, cx + s * 0.17, cy - s * 0.38)
        p.curveTo(cx + s * 0.34, cy - s * 0.30, cx + s * 0.42,
                  cy + s * 0.05, cx, cy + s * 0.55)
        pdf.drawPath(p, stroke=0, fill=1)
    elif kind == "air":
        pdf.setStrokeColor(HexColor("#7A93B8"))
        pdf.setLineWidth(3)
        for j, dy in enumerate((0.28, 0.0, -0.28)):
            y = cy + dy * s
            p = pdf.beginPath()
            p.moveTo(cx - s * 0.45, y)
            p.curveTo(cx - s * 0.1, y + s * 0.22, cx + s * 0.25,
                      y + s * 0.22, cx + s * 0.38, y)
            p.curveTo(cx + s * 0.45, y - s * 0.14, cx + s * 0.28,
                      y - s * 0.20, cx + s * 0.18, y - s * 0.10)
            pdf.drawPath(p, stroke=1, fill=0)
    elif kind == "food":
        pdf.setFillColor(BROWN)
        for dx, dy in ((-0.16, 0.16), (0.10, 0.22), (0.0, 0.02),
                       (-0.24, 0.0), (0.22, 0.02)):
            pdf.circle(cx + dx * s, cy + dy * s, s * 0.11,
                       stroke=0, fill=1)
        pdf.setStrokeColor(BROWN)
        pdf.setLineWidth(3.4)
        p = pdf.beginPath()
        p.moveTo(cx - s * 0.48, cy + s * 0.05)
        p.curveTo(cx - s * 0.3, cy - s * 0.42, cx + s * 0.3,
                  cy - s * 0.42, cx + s * 0.48, cy + s * 0.05)
        pdf.drawPath(p, stroke=1, fill=0)
    elif kind == "bug":
        pdf.setFillColor(GREEN)
        pdf.circle(cx, cy - s * 0.05, s * 0.30, stroke=0, fill=1)
        pdf.circle(cx, cy + s * 0.34, s * 0.17, stroke=0, fill=1)
        pdf.setStrokeColor(GREEN)
        pdf.setLineWidth(2.4)
        for dx in (-0.30, 0.30):
            for dy in (0.10, -0.10, -0.28):
                pdf.line(cx + dx * s * 0.8, cy + dy * s,
                         cx + dx * s * 1.25, cy + (dy - 0.12) * s)
    elif kind == "hide":
        pdf.setFillColor(GREEN)
        for ang in (-28, 0, 28):
            rad = math.radians(ang)
            ex = cx + math.sin(rad) * s * 0.45
            ey = cy + math.cos(rad) * s * 0.45
            pdf.setStrokeColor(GREEN)
            pdf.setLineWidth(3)
            pdf.line(cx, cy - s * 0.4, ex, ey - s * 0.1)
            pdf.circle(ex, ey, s * 0.16, stroke=0, fill=1)


def _scissors(pdf, x, y):
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.circle(x - 5, y - 5, 4.5, stroke=1, fill=0)
    pdf.circle(x + 5, y - 5, 4.5, stroke=1, fill=0)
    pdf.line(x - 3, y - 2, x + 7, y + 9)
    pdf.line(x + 3, y - 2, x - 7, y + 9)


# ---------------------------------------------------------------- Page 1
def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Do They Both Need?")
    _instruction(pdf, "Cut out the needs. Paste each one where it belongs!")
    for label, img, x in (("BEAN PLANT", PLANT, 63), ("DOG", DOG, 319)):
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawCentredString(x + 115, 598, label)
        _img_fill(pdf, img, x, 452, 230, 132)
    # sorting trays
    trays = [("Only the PLANT", 63, 152), ("BOTH need it", 219, 174),
             ("Only the DOG", 397, 152)]
    for label, x, w in trays:
        _panel(pdf, x, 268, w, 168)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawCentredString(x + w / 2, 414, label)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(66, 240, "Both need:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(142, 238, 549, 238)
    # cut-out area
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.4)
    pdf.setDash(5, 4)
    p = pdf.beginPath()
    p.roundRect(63, 118, 486, 96, 10)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setDash()
    _scissors(pdf, 84, 190)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 10.5)
    _lbl = "CUT-OUT AREA"
    pdf.drawString(539 - pdf.stringWidth(_lbl, "Helvetica-Bold", 10.5),
                   196, _lbl)
    chips = [("water", "WATER"), ("air", "AIR"), ("sun", "SUN"),
             ("food", "FOOD")]
    for k, (kind, word) in enumerate(chips):
        x = 146 + k * 84
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.1)
        pdf.setDash(4, 3)
        p = pdf.beginPath()
        p.roundRect(x, 128, 68, 68, 10)
        pdf.drawPath(p, stroke=1, fill=0)
        pdf.setDash()
        chip_icon(pdf, x + 34, 170, kind, s=30)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawCentredString(x + 34, 138, word)
    _adult(pdf, [
        "Adult: WATER and AIR belong in BOTH \u2014 the plant and the "
        "dog both need",
        "them. SUN belongs with the PLANT: a plant makes its own food "
        "from sunlight.",
        "FOOD belongs with the DOG: animals eat food. Scribe your "
        "child's words",
        "after \u201cBoth need:\u201d",
    ], top=100, step=14)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 2
def page2(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Why This Habitat?")
    _instruction(pdf, "Draw a line from each need to the pond!")
    _img_fill(pdf, POND, 60, 388, 492, 216)
    cards = [("water", "WATER"), ("bug", "FOOD"),
             ("hide", "A SAFE PLACE")]
    for k, (kind, word) in enumerate(cards):
        y = 296 - k * 74
        _panel(pdf, 63, y, 150, 64)
        chip_icon(pdf, 92, y + 32, kind, s=30)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(112, y + 26, word)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawString(232, 330, "The pond is a good home")
    pdf.drawString(232, 310, "for the frog because:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(232, 282, 549, 282)
    pdf.line(232, 252, 549, 252)
    _adult(pdf, [
        "Adult: The frog needs water to swim in and keep its skin "
        "wet, bugs to",
        "eat, and plants to hide under. Check that each line lands on "
        "its evidence",
        "in the picture \u2014 the water, a bug, the lily pads. Then "
        "scribe your child's",
        "exact words after \u201cbecause:\u201d",
    ], top=104, step=16)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 3
def page3(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Living Things Change Places")
    _instruction(pdf, "Circle what is NEW in each AFTER picture!")
    strips = [
        ("The beaver builds a dam.", BEAVER_B, BEAVER_A),
        ("The worms work in the soil.", WORM_B, WORM_A),
        ("The tree's roots grow and grow.", ROOTS_B, ROOTS_A),
    ]
    for i, (title, before, after) in enumerate(strips):
        top = 592 - i * 146
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(63, top, title)
        y = top - 110
        _img_fill(pdf, before, 63, y, 168, 96)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawCentredString(243, y + 40, "\u2192")
        _img_fill(pdf, after, 256, y, 240, 96)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 9.5)
        pdf.drawString(63, y - 15, "BEFORE")
        pdf.drawString(256, y - 15, "AFTER")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(63, 140, "Tell a grown-up: what changed?")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(63, 118, 549, 118)
    _adult(pdf, [
        "Adult: The dam slows the stream and makes a pond. The worms "
        "tunnel and",
        "mix the soil. The tree's roots lift the sidewalk slabs. "
        "Scribe your child's",
        "own words for what changed in each place.",
    ], top=92, step=16)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 4
def page4(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Watch It Grow")
    _instruction(pdf, "Plant a seed. Draw it and measure it each time!")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawString(63, 600, "My seed:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(128, 598, 300, 598)
    pdf.setFillColor(NAVY)
    pdf.drawString(330, 600, "Planted on:")
    pdf.line(416, 598, 549, 598)
    for r in range(4):
        yb = 476 - r * 120
        _panel(pdf, 63, yb, 486, 114)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(75, yb + 94, "Date:")
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(1)
        pdf.line(112, yb + 92, 210, yb + 92)
        _frame(pdf, 75, yb + 8, 245, 76)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(348, yb + 66, "How tall?")
        pdf.drawString(348, yb + 50, "Color the cubes.")
        for cnum in range(12):
            x = 348 + cnum * 16
            pdf.setStrokeColor(RULE)
            pdf.setLineWidth(1.1)
            pdf.rect(x, yb + 14, 15, 15, stroke=1, fill=0)
    _adult(pdf, [
        "Adult: A bean seed in a clear cup works well. Each visit: "
        "write the date,",
        "draw the plant just as it looks, then stack cubes beside it "
        "and color one",
        "cube for each cube in the tower. Record only what you really "
        "see.",
    ], top=92, step=16)
    draw_footer(pdf)
    pdf.save()


PAGES = [page1, page2, page3, page4]


def build_pack():
    os.makedirs(OUT_DIR, exist_ok=True)
    individual = []
    for i, fn in enumerate(PAGES, start=1):
        p = os.path.join(OUT_DIR, f"{STEM}-page-{i:02d}.pdf")
        fn(p)
        individual.append(p)
        print("built page", i)
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for p in individual:
        for pg in PdfReader(p).pages:
            w.add_page(pg)
    bundle = os.path.join(OUT_DIR, f"{STEM}-review.pdf")
    with open(bundle, "wb") as fh:
        w.write(fh)
    print("bundle:", bundle)


def preview():
    for i, fn in enumerate(PAGES, start=1):
        p = f"/tmp/lt-p{i}.pdf"
        fn(p)
        print("preview page", i, "->", p)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if mode == "build":
        build_pack()
    else:
        preview()
