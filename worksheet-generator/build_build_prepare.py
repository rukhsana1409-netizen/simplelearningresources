#!/usr/bin/env python3
"""Weather Watchers: Build & Prepare (Kindergarten Science add-on).

A two-page companion to Weather Watchers, built so the approved
five-page pack stays locked. It completes two Michigan expectations
Weather Watchers only began:

  Page 1 Check the Forecast! — K-ESS3-2's forecasting half: the
    purpose of a weather forecast is to PREPARE. A simple picture
    forecast (rainy and windy tomorrow) drives two unambiguous
    choices: wear the raincoat (not sunny clothes, not snow
    clothes); take the umbrella (not sunglasses, not a sled).
  Page 2 Build a Shade — K-PS3-2 (with K-2-ETS1-2): design and build
    a structure that reduces sunlight's warming. The child draws the
    design, checks off real materials, builds the shade over one
    ice cube (twin cube in full sun, exactly as Weather Watchers
    Page 3), draws both cubes after about 15 minutes, and dictates
    whether the shade worked. Any result is data; nothing is
    pre-printed.

No separate parent guide: adult steps are printed on each page,
and the objective / answers / facilitation notes live in the
website resource-page text.
"""
import os
import sys

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_phonics_az import (  # noqa: E402
    INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL, draw_footer, draw_header,
)
from build_weather_watchers import wx_icon  # noqa: E402

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "build-prepare")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "science",
                       "build-and-prepare")
PACK_TITLE = "Weather Watchers"
STEM = "build-and-prepare"

RULE = HexColor("#9DB8C4")
PANEL_FILL = HexColor("#F2F8F8")
BROWN = HexColor("#8A5A2B")
WIND = HexColor("#7A93B8")

RAINCOAT = os.path.join(ASSETS, "bp-raincoat.jpg")
SUNNY = os.path.join(ASSETS, "bp-sunny.jpg")
SNOW = os.path.join(ASSETS, "bp-snow-outfit.jpg")
UMBRELLA = os.path.join(ASSETS, "bp-umbrella.jpg")
SUNGLASSES = os.path.join(ASSETS, "bp-sunglasses.jpg")
SLED = os.path.join(ASSETS, "bp-sled.jpg")
TOYS_IN = os.path.join(ASSETS, "bp-toys-in.jpg")
TOYS_OUT = os.path.join(ASSETS, "bp-toys-out.jpg")


def _adult(pdf, lines, top=104, step=14):
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


def _panel(pdf, x, y, w, h, r=12):
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.3)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.drawPath(p, stroke=1, fill=1)


def _frame(pdf, x, y, w, h, r=12):
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.4)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.drawPath(p, stroke=1, fill=0)


# ---------------------------------------------------------------- Page 1
def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Build & Prepare")
    _instruction(pdf, "Check the forecast! Circle what you need.")
    # forecast card
    _panel(pdf, 63, 490, 486, 112)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(84, 586, "TOMORROW'S FORECAST")
    wx_icon(pdf, 140, 534, "rainy", s=42)
    pdf.setStrokeColor(WIND)
    pdf.setLineWidth(3)
    for dy in (10, -10):
        p = pdf.beginPath()
        p.moveTo(200, 534 + dy)
        p.curveTo(218, 546 + dy, 236, 546 + dy, 246, 536 + dy)
        p.curveTo(252, 530 + dy, 244, 526 + dy, 238, 530 + dy)
        pdf.drawPath(p, stroke=1, fill=0)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 21)
    pdf.drawString(268, 548, "Rainy and windy")
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(268, 522, "all day long!")
    rows = [
        ("What will you WEAR?", 470,
         [(RAINCOAT, 0.42), (SUNNY, 0.5), (SNOW, 0.5)]),
        ("What will you TAKE?", 344,
         [(UMBRELLA, 0.5), (SUNGLASSES, 0.5), (SLED, 0.5)]),
    ]
    for label, ly, choices in rows:
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(63, ly, label)
        for k, (img, fy) in enumerate(choices):
            _img_fill(pdf, img, 63 + k * 170, ly - 94, 152, 88,
                      focus_y=fy)
    # storm preparation question (separate third activity)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.2)
    pdf.line(63, 236, 549, 236)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(63, 216,
                   "A storm is coming. What should we do BEFORE it "
                   "starts?")
    _img_fill(pdf, TOYS_IN, 63, 108, 232, 96)
    _img_fill(pdf, TOYS_OUT, 317, 108, 232, 96, focus_y=0.35)
    _adult(pdf, [
        "Adult: Forecast answers: the raincoat and the umbrella. Storm "
        "answer:",
        "bring the outdoor toys INSIDE before the storm starts "
        "\u2014 toys left out",
        "can blow away or break. Getting ready first is why we check "
        "forecasts.",
    ], top=92, step=13)
    draw_footer(pdf)
    pdf.save()


# ------------------------------------------------------------- materials
def _material_icon(pdf, cx, cy, kind):
    if kind == "cardboard":
        pdf.setFillColor(HexColor("#C89B6A"))
        pdf.setStrokeColor(BROWN)
        pdf.setLineWidth(1.6)
        pdf.rect(cx - 15, cy - 11, 30, 22, stroke=1, fill=1)
        pdf.line(cx - 15, cy, cx + 15, cy)
    elif kind == "paper":
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(1.6)
        pdf.rect(cx - 12, cy - 15, 24, 30, stroke=1, fill=1)
        pdf.setStrokeColor(RULE)
        pdf.line(cx - 7, cy + 6, cx + 7, cy + 6)
        pdf.line(cx - 7, cy - 1, cx + 7, cy - 1)
        pdf.line(cx - 7, cy - 8, cx + 4, cy - 8)
    elif kind == "cloth":
        pdf.setFillColor(HexColor("#E58AA0"))
        p = pdf.beginPath()
        p.moveTo(cx - 16, cy + 10)
        p.curveTo(cx - 6, cy + 2, cx - 2, cy + 16, cx + 6, cy + 8)
        p.curveTo(cx + 12, cy + 2, cx + 14, cy + 10, cx + 16, cy + 6)
        p.lineTo(cx + 16, cy - 12)
        p.curveTo(cx + 6, cy - 6, cx - 6, cy - 18, cx - 16, cy - 10)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
    elif kind == "sticks":
        pdf.setStrokeColor(BROWN)
        pdf.setLineWidth(3.2)
        pdf.line(cx - 10, cy - 13, cx - 4, cy + 13)
        pdf.line(cx, cy - 14, cx + 1, cy + 14)
        pdf.line(cx + 10, cy - 13, cx + 5, cy + 13)
    elif kind == "box":
        pdf.setStrokeColor(BROWN)
        pdf.setLineWidth(1.8)
        pdf.line(cx - 13, cy - 3, cx, cy - 10)
        pdf.line(cx, cy - 10, cx + 13, cy - 3)
        pdf.line(cx + 13, cy - 3, cx + 13, cy + 8)
        pdf.line(cx + 13, cy + 8, cx, cy + 15)
        pdf.line(cx, cy + 15, cx - 13, cy + 8)
        pdf.line(cx - 13, cy + 8, cx - 13, cy - 3)
        pdf.line(cx, cy + 3, cx, cy - 10)
        pdf.line(cx, cy + 3, cx + 13, cy - 3)
        pdf.line(cx, cy + 3, cx - 13, cy - 3)


# ---------------------------------------------------------------- Page 2
def page2(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Build & Prepare")
    _instruction(pdf, "The sun warms an ice cube. Build a shade!")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14.5)
    pdf.drawString(63, 590, "DRAW your shade:")
    _frame(pdf, 63, 316, 267, 262)
    _panel(pdf, 348, 316, 201, 262)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14.5)
    pdf.drawString(366, 552, "I used:")
    mats = [("cardboard", "CARDBOARD"), ("paper", "PAPER"),
            ("cloth", "CLOTH"), ("sticks", "STICKS"), ("box", "A BOX")]
    for k, (kind, word) in enumerate(mats):
        y = 512 - k * 42
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.4)
        pdf.rect(366, y - 9, 18, 18, stroke=1, fill=0)
        _material_icon(pdf, 410, y, kind)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(434, y - 4, word)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14.5)
    pdf.drawString(63, 290, "After 15 minutes, DRAW both cubes:")
    for label, x in (("Under MY shade", 63), ("In the sun", 312)):
        _frame(pdf, x, 168, 237, 108)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(x + 12, 258, label)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(63, 140, "Tell a grown-up: Did your shade work?")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(63, 118, 549, 118)
    _adult(pdf, [
        "Adult: Use two same-size ice cubes on identical trays, in "
        "the same outdoor",
        "area. Put one under your child's shade and the other in "
        "direct sunlight.",
        "After about 15 minutes, draw both cubes and scribe your "
        "child's words.",
        "Record what really happened, even if the shade did not "
        "work.",
    ], top=98, step=14)
    draw_footer(pdf)
    pdf.save()


PAGES = [page1, page2]


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
        p = f"/tmp/bp-p{i}.pdf"
        fn(p)
        print("preview page", i, "->", p)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if mode == "build":
        build_pack()
    else:
        preview()
