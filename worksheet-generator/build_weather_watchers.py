#!/usr/bin/env python3
"""Weather Watchers — Weather & Climate (Kindergarten Science).

Michigan K-ESS2-1 (observe and describe weather; notice patterns over
time), K-ESS3-2 (how to stay safe in severe weather), and K-PS3-1/2
(sunlight warms surfaces; shade and cover reduce warming). Follows the
RCS-aligned science roadmap: observe -> record -> compare -> explain.

Accuracy rules honored:
  - Page 1 records the child's REAL week — nothing is prefilled.
  - Page 2 uses an explicitly pretend calendar; the data are counted
    exactly (Sunny 5, Cloudy 4, Rainy 3, Snowy 2; most = Sunny,
    fewest = Snowy — both unique, no ties).
  - Page 3 compares the SAME surface (two identical ice cubes on the
    same kind of plate) in sun vs shade; it is a looking-only
    investigation — no touching hot surfaces, and no claim that
    different materials share temperatures.
  - Page 4 measures AIR temperature with illustrated thermometers
    (red higher = warmer air) and explicitly separates that from
    sunlight heating a surface (Page 3). No scale numbers to read.
  - Page 5 safety advice is accurate: in thunder, go inside a building
    or hard-top car, never under a tree or an open shelter; in snow,
    dress fully warm and walk slowly on ice holding a grown-up's hand.

No separate parent guide: adult steps are printed on each page, and
the objective / answers / facilitation notes live in the website
resource-page text.

Page map:
  1 My Week of Weather   — 5-day real observation chart (draw the sky,
                           circle the weather, circle warm/cool)
  2 Weather Detectives   — pretend 14-day calendar; count each kind,
                           circle most and fewest
  3 Sunlight & Shade     — two ice cubes, sun vs shade: predict, test,
                           draw the result
  4 Weather Measurements — warmer/cooler; illustrated thermometers;
                           match scenes, morning/afternoon observation
  5 Stay Safe in Stormy Weather — thunderstorm + snowstorm choices
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
                      "assets", "weather-watchers")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "science",
                       "weather-watchers")
PACK_TITLE = "Weather Watchers"
STEM = "weather-watchers"

MARGIN = 60
RULE = HexColor("#9DB8C4")
LIGHT = HexColor("#EAF3F1")
GOLD = HexColor("#F4B63E")
SKY = HexColor("#7FB3D9")
GREY = HexColor("#8A9BA8")
BLUE = HexColor("#2E6FB7")
RED = HexColor("#D64541")

SUNSHADE = os.path.join(ASSETS, "ww-sun-shade.jpg")
SAFE_INSIDE = os.path.join(ASSETS, "ww-safe-inside.jpg")
TREE = os.path.join(ASSETS, "ww-tree.jpg")
CAR = os.path.join(ASSETS, "ww-car.jpg")
SHELTER = os.path.join(ASSETS, "ww-shelter.jpg")
WARM_CLOTHES = os.path.join(ASSETS, "ww-warm-clothes.jpg")
SHORTS = os.path.join(ASSETS, "ww-shorts-snow.jpg")
HOLD_HAND = os.path.join(ASSETS, "ww-hold-hand.jpg")
RUN_ICE = os.path.join(ASSETS, "ww-run-ice.jpg")


def _adult(pdf, lines, top=74, step=18):
    pdf.setFillColor(INK)
    for i, line in enumerate(lines):
        pdf.setFont("Helvetica-Bold", 11.5 if i == 0 else 11)
        pdf.drawCentredString(PAGE_WIDTH / 2, top - i * step, line)


def _instruction(pdf, text, y=616, size=20):
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


PANEL_FILL = HexColor("#F2F8F8")


def _panel(pdf, x, y, w, h, r=12):
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.3)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.drawPath(p, stroke=1, fill=1)


# ------------------------------------------------------------- icons
def _cloud(pdf, cx, cy, s, color=GREY):
    pdf.setFillColor(color)
    pdf.circle(cx - 0.32 * s, cy, 0.30 * s, stroke=0, fill=1)
    pdf.circle(cx + 0.05 * s, cy + 0.16 * s, 0.40 * s, stroke=0, fill=1)
    pdf.circle(cx + 0.38 * s, cy, 0.28 * s, stroke=0, fill=1)
    pdf.rect(cx - 0.60 * s, cy - 0.28 * s, 1.24 * s, 0.30 * s,
             stroke=0, fill=1)


def wx_icon(pdf, cx, cy, kind, s=30):
    """Weather symbol centered at (cx, cy); s ~ overall size."""
    if kind == "sunny":
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
    elif kind == "cloudy":
        _cloud(pdf, cx, cy, s * 1.05)
    elif kind == "rainy":
        _cloud(pdf, cx, cy + s * 0.22, s * 0.95)
        pdf.setStrokeColor(BLUE)
        pdf.setLineWidth(3)
        for dx in (-0.34, 0.0, 0.34):
            pdf.line(cx + dx * s, cy - s * 0.18,
                     cx + dx * s - s * 0.10, cy - s * 0.52)
    elif kind == "snowy":
        _cloud(pdf, cx, cy + s * 0.22, s * 0.95)
        pdf.setStrokeColor(SKY)
        pdf.setLineWidth(2)
        for dx in (-0.34, 0.0, 0.34):
            fx, fy = cx + dx * s, cy - s * 0.36
            for a in (0, 60, 120):
                rad = math.radians(a)
                pdf.line(fx - math.cos(rad) * s * 0.13,
                         fy - math.sin(rad) * s * 0.13,
                         fx + math.cos(rad) * s * 0.13,
                         fy + math.sin(rad) * s * 0.13)


def thermometer(pdf, cx, top, height, frac, label=None):
    """Illustrated thermometer: red column rises to frac of the tube."""
    tube_w = 22
    x = cx - tube_w / 2
    y = top - height
    pdf.setFillColor(white)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(2)
    p = pdf.beginPath()
    p.roundRect(x, y, tube_w, height, 10)
    pdf.drawPath(p, stroke=1, fill=1)
    bulb_r = 21
    bulb_cy = y - 8
    pdf.setFillColor(white)
    pdf.circle(cx, bulb_cy, bulb_r, stroke=1, fill=1)
    red_h = (height - 14) * frac
    pdf.setFillColor(RED)
    pdf.rect(x + 5, y + 5, tube_w - 10, red_h, stroke=0, fill=1)
    pdf.circle(cx, bulb_cy, bulb_r - 6, stroke=0, fill=1)
    if label:
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawCentredString(cx, bulb_cy - bulb_r - 18, label)


# ---------------------------------------------------------------- Page 1
def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Week of Weather")
    _instruction(pdf, "Look outside every day. Record the real weather!")
    x0, col_w = 116, 86
    label_w = x0 - (MARGIN + 6)
    # header row
    hy = 556
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13.5)
    for d in range(5):
        cx = x0 + d * col_w + col_w / 2
        pdf.drawCentredString(cx, hy + 8, f"Day {d + 1}")
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(1)
        pdf.line(cx - 26, hy - 8, cx + 26, hy - 8)
        pdf.setFillColor(TEAL)
    rows = [("Draw the\nsky", 446, 94), ("Circle the\nweather", 330, 116),
            ("Warm or\ncool?", 276, 48)]
    for label, ry, rh in rows:
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 11)
        lines = label.split("\n")
        for j, ln in enumerate(lines):
            pdf.drawCentredString(MARGIN + 6 + label_w / 2,
                                  ry + rh / 2 + 6 - j * 14, ln)
    for d in range(5):
        x = x0 + d * col_w
        _frame(pdf, x + 3, 446, col_w - 6, 94, r=8)
        _frame(pdf, x + 3, 330, col_w - 6, 116, r=8)
        kinds = ["sunny", "cloudy", "rainy", "snowy"]
        for k, kind in enumerate(kinds):
            ix = x + col_w / 2 + (-20 if k % 2 == 0 else 20)
            iy = 330 + 87 if k < 2 else 330 + 29
            wx_icon(pdf, ix, iy, kind, s=24)
        # warm / cool pills
        for word, dy in (("WARM", 276 + 25), ("COOL", 276 + 1)):
            pass
        pdf.setFillColor(LIGHT)
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(1.1)
        for word, py in (("WARM", 282), ("COOL", 252)):
            p = pdf.beginPath()
            p.roundRect(x + 8, py, col_w - 16, 24, 12)
            pdf.drawPath(p, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 11.5)
            pdf.drawCentredString(x + col_w / 2, py + 7, word)
            pdf.setFillColor(LIGHT)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14.5)
    pdf.drawString(MARGIN + 6, 216, "This week I noticed:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(196, 214, PAGE_WIDTH - MARGIN - 6, 214)
    _adult(pdf, [
        "Adult: One column per day, all week. Look outside together: "
        "draw the sky,",
        "circle the weather you really see, and circle how the air "
        "feels. Write the",
        "day's name on the short line. Nothing is filled in ahead "
        "\u2014 your child's",
        "records are the data. Scribe their exact words for "
        "\u201cI noticed.\u201d",
    ], top=172, step=16)
    draw_footer(pdf)
    pdf.save()


WEEK = [
    ["sunny", "sunny", "cloudy", "rainy", "sunny", "cloudy", "snowy"],
    ["cloudy", "sunny", "rainy", "sunny", "cloudy", "rainy", "snowy"],
]
COUNTS = {"sunny": 5, "cloudy": 4, "rainy": 3, "snowy": 2}


# ---------------------------------------------------------------- Page 2
def page2(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Weather Detectives")
    _instruction(pdf, "Count the days on this pretend calendar!")
    # --- Section 1: the calendar panel
    _panel(pdf, 60, 462, 492, 140)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawString(74, 586, "A pretend calendar \u2014 two weeks")
    gx, cw, ch = 76, 66, 50
    days = ["M", "T", "W", "T", "F", "S", "S"]
    for w in range(2):
        for d in range(7):
            x = gx + d * cw
            y = 520 - w * 52
            _frame(pdf, x + 2, y + 2, cw - 4, ch - 4, r=8)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 9.5)
            pdf.drawString(x + 8, y + ch - 15, days[d])
            wx_icon(pdf, x + cw / 2, y + 20, WEEK[w][d], s=26)
    # --- Section 2: counting questions, tidy 2 x 2 of mini-panels
    kinds = [("sunny", "Sunny"), ("cloudy", "Cloudy"),
             ("rainy", "Rainy"), ("snowy", "Snowy")]
    positions = [(63, 380), (309, 380), (63, 306), (309, 306)]
    for (kind, name), (px, py) in zip(kinds, positions):
        pdf.setFillColor(white)
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(1.3)
        p = pdf.beginPath()
        p.roundRect(px, py, 240, 64, 10)
        pdf.drawPath(p, stroke=1, fill=1)
        wx_icon(pdf, px + 34, py + 32, kind, s=38)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(px + 64, py + 25, name)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 9.5)
        pdf.drawCentredString(px + 206, py + 55, "How many?")
        _frame(pdf, px + 184, py + 10, 44, 40, r=8)
    # --- Sections 3 & 4: MOST and FEWEST panels
    for label, py in (("Which weather happened MOST?", 208),
                      ("Which weather happened FEWEST?", 110)):
        _panel(pdf, 60, py, 492, 88)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 15.5)
        pdf.drawString(74, py + 72, label)
        for k, (kind, _name) in enumerate(kinds):
            cx = 130 + k * 118
            pdf.setStrokeColor(RULE)
            pdf.setLineWidth(1.3)
            pdf.circle(cx, py + 34, 27, stroke=1, fill=0)
            wx_icon(pdf, cx, py + 34, kind, s=34)
    _adult(pdf, [
        "Adult: This calendar is pretend, for counting practice. "
        "Counts: sunny 5,",
        "cloudy 4, rainy 3, snowy 2. Talk about the pattern: "
        "\u201cMost days were",
        "sunny. Snow came on only two days.\u201d",
    ], top=94, step=15)
    draw_footer(pdf)
    pdf.save()



# ---------------------------------------------------------------- Page 3
def page3(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Sunlight & Shade")
    _instruction(pdf, "Two ice cubes: one in the sun, one in the shade!")
    _img_fill(pdf, SUNSHADE, MARGIN + 56, 420, 440, 170)
    # predict
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15.5)
    pdf.drawString(MARGIN + 6, 388, "PREDICT: Which cube will melt first? Circle it.")
    for label, x in (("SUNNY side", 66), ("SHADY side", 316)):
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(1.3)
        p = pdf.beginPath()
        p.roundRect(x, 330, 230, 42, 21)
        pdf.drawPath(p, stroke=1, fill=0)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(x + 115, 344, label)
        pdf.setFillColor(NAVY)
    # record boxes
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15.5)
    pdf.drawString(MARGIN + 6, 302,
                   "TEST & RECORD: Wait 15 minutes. Draw both cubes now.")
    for label, x in (("SUN cube", 66), ("SHADE cube", 316)):
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawString(x, 272, label)
        _frame(pdf, x, 130, 230, 132)
    _adult(pdf, [
        "Adult: Use two cubes the SAME size, on the same kind of "
        "plate, started at",
        "the same time \u2014 one in sunshine, one in shade. This is a "
        "looking-only",
        "investigation: never touch sun-heated surfaces to test them. "
        "Record what",
        "your child actually sees, then ask: \u201cWhat happened? "
        "Why do you think so?\u201d",
    ], top=104, step=16)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 4
def _thermo_mini(pdf, cx, ry, high):
    """Small thermometer glyph; ry is the row's top reference."""
    tube_w, tube_h = 13, 30
    x = cx - tube_w / 2
    top = ry + 40
    y = top - tube_h
    pdf.setFillColor(white)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.6)
    p = pdf.beginPath()
    p.roundRect(x, y, tube_w, tube_h, 6)
    pdf.drawPath(p, stroke=1, fill=1)
    bulb_cy = y - 5
    pdf.circle(cx, bulb_cy, 11, stroke=1, fill=1)
    frac = 0.82 if high else 0.30
    pdf.setFillColor(RED)
    pdf.rect(x + 3, y + 3, tube_w - 6, (tube_h - 6) * frac,
             stroke=0, fill=1)
    pdf.circle(cx, bulb_cy, 6.5, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(cx, ry - 29, "WARMER" if high else "COOLER")
    # circle-me ring around the whole glyph
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.2)
    pdf.circle(cx, ry + 12, 30, stroke=1, fill=0)


def page4(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Weather Measurements")
    _instruction(pdf, "A thermometer tells how warm the air is!")
    # teaching pair
    for cx, frac, word, kind in ((186, 0.30, "COOL air", "snowy"),
                                 (426, 0.85, "WARM air", "sunny")):
        _frame(pdf, cx - 92, 444, 184, 150, r=12)
        thermometer(pdf, cx - 38, 578, 92, frac)
        wx_icon(pdf, cx + 42, 532, kind, s=46)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14.5)
        pdf.drawCentredString(cx + 42, 472, word)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 424,
                          "The red climbs higher when the air is warmer.")
    # scene rows: circle the mini thermometer that matches
    scenes = [("snowy", "Snowy morning"), ("sunny", "Sunny beach day"),
              ("snowy", "Frosty window"), ("sunny", "Hot picnic day")]
    for i, (kind, caption) in enumerate(scenes):
        ry = 360 - i * 74
        wx_icon(pdf, 104, ry + 12, kind, s=40)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14.5)
        pdf.drawString(140, ry + 6, caption)
        _thermo_mini(pdf, 392, ry, False)
        _thermo_mini(pdf, 492, ry, True)
    _adult(pdf, [
        "Adult: These thermometers have no numbers \u2014 just compare: "
        "red higher",
        "means warmer AIR (different from sunlight warming a surface, "
        "Page 3).",
        "Answers: snowy \u2014 cooler; beach day \u2014 warmer; frosty "
        "\u2014 cooler; picnic \u2014 warmer.",
    ], top=96, step=16)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 5
def page5(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Stay Safe in Stormy Weather")
    _instruction(pdf, "Circle the SAFE choice in each picture pair!")
    cards = [
        ("Thunder! You are playing outside.", SAFE_INSIDE, TREE),
        ("Lightning is flashing!", CAR, SHELTER),
        ("Snow is falling hard.", WARM_CLOTHES, SHORTS),
        ("The sidewalk is icy.", HOLD_HAND, RUN_ICE),
    ]
    focus = {SAFE_INSIDE: 0.55, TREE: 0.72, CAR: 0.78, SHELTER: 0.65,
             WARM_CLOTHES: 0.65, SHORTS: 0.36, HOLD_HAND: 0.80,
             RUN_ICE: 0.52}
    xs = [63, 309]
    ys = [372, 128]
    for i, (title, img_a, img_b) in enumerate(cards):
        px = xs[i % 2]
        py = ys[i // 2]
        _panel(pdf, px, py, 240, 234)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(px + 12, py + 208, title)
        _img_fill(pdf, img_a, px + 9, py + 14, 106, 172,
                  focus_x=focus.get(img_a, 0.5))
        _img_fill(pdf, img_b, px + 125, py + 14, 106, 172,
                  focus_x=focus.get(img_b, 0.5))
    _adult(pdf, [
        "Adult: Thunder and lightning \u2014 go inside a building or "
        "a hard-top car.",
        "Never shelter under a tree or an open picnic shelter. In "
        "snow, dress",
        "warmly from head to toe, and walk slowly on ice holding a "
        "grown-up's hand.",
    ], top=110, step=16)
    draw_footer(pdf)
    pdf.save()



PAGES = [page1, page2, page3, page4, page5]


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
        p = f"/tmp/ww-p{i}.pdf"
        fn(p)
        print("preview page", i, "->", p)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if mode == "build":
        build_pack()
    else:
        preview()
