#!/usr/bin/env python3
"""Taking Care of Our Earth (Kindergarten Science, Michigan K-ESS3-3).

Three pages on communicating solutions that reduce humans' impact
on the land, water, air, and other living things:

  Page 1 Helps or Hurts the Earth? — cut-and-paste sort of six
    illustrated actions. HELPS: recycling a bottle, planting a
    seedling, watering flowers with care. HURTS: litter dropped on
    grass, a bottle tossed into a pond, a tap left running with
    water spilling over. Every scene is a single unambiguous
    action.
  Page 2 Finish the Fix — four distinct problems, each with two
    illustrated action choices; the child circles the solution.
    (1) A dripping tap (a leak) -> a grown-up fixes it with a
    wrench / a child plays and ignores it. (2) Litter at a pond ->
    put it in a bin / toss it into the pond. (3) A hose left
    running, water pooling away -> turn the hose off / splash and
    play in the wasted water. (4) Lights blazing in an empty sunny
    room -> switch the light off / turn another lamp on.
  Page 3 My Earth Care Solution — problem-solving and
    communication, not a generic promise: the child names a REAL
    problem (idea-starter pictures reuse Page 2's problem scenes),
    draws themselves carrying out one practical action, and
    explains how the action helps, scribed by an adult.

No separate parent guide: brief adult guidance is printed on each
page, and the objective / answers / facilitation notes live in the
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

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "earth-care")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "science",
                       "earth-care")
PACK_PREFIX = "Taking Care of"
PACK_TITLE = "Our Earth"
STEM = "earth-care"

RULE = HexColor("#9DB8C4")
PANEL_FILL = HexColor("#F2F8F8")

RECYCLE = os.path.join(ASSETS, "ec-recycle.jpg")
PLANT = os.path.join(ASSETS, "ec-plant.jpg")
WATER = os.path.join(ASSETS, "ec-water-flowers.jpg")
LITTER = os.path.join(ASSETS, "ec-litter-grass.jpg")
POND_BOTTLE = os.path.join(ASSETS, "ec-pond-bottle.jpg")
TAP_RUN = os.path.join(ASSETS, "ec-tap-running.jpg")

P_TAP = os.path.join(ASSETS, "ec-problem-tap.jpg")
P_LITTER = os.path.join(ASSETS, "ec-problem-litter-pond.jpg")
P_HOSE = os.path.join(ASSETS, "ec-problem-hose.jpg")
P_LIGHTS = os.path.join(ASSETS, "ec-problem-lights.jpg")

FIX_WRENCH = os.path.join(ASSETS, "ec-fix-wrench.jpg")
IGNORE_PLAY = os.path.join(ASSETS, "ec-ignore-play.jpg")
FIX_BIN = os.path.join(ASSETS, "ec-fix-bin.jpg")
TOSS_POND = os.path.join(ASSETS, "ec-toss-pond.jpg")
FIX_HOSE = os.path.join(ASSETS, "ec-fix-hose-off.jpg")
PLAY_SPLASH = os.path.join(ASSETS, "ec-play-splash.jpg")
FIX_LIGHT = os.path.join(ASSETS, "ec-fix-light-off.jpg")
LAMP_ON = os.path.join(ASSETS, "ec-lamp-on.jpg")


def _adult(pdf, lines, top=92, step=14):
    pdf.setFillColor(INK)
    for i, line in enumerate(lines):
        pdf.setFont("Helvetica-Bold", 11.5 if i == 0 else 11)
        pdf.drawCentredString(PAGE_WIDTH / 2, top - i * step, line)


def _instruction(pdf, text, y=616, size=19):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(PAGE_WIDTH / 2, y, text)


def _img_fill(pdf, path, x, y, w, h, focus_x=0.5, focus_y=0.5, r=12):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx = x + (w - dw) * focus_x
    dy = y + (h - dh) * focus_y
    pdf.saveState()
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.drawImage(ImageReader(path), dx, dy, dw, dh,
                  preserveAspectRatio=False, mask="auto")
    pdf.restoreState()
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.5)
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


def _scissors(pdf, x, y):
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.2)
    pdf.circle(x, y + 4, 3.4, stroke=1, fill=0)
    pdf.circle(x, y - 4, 3.4, stroke=1, fill=0)
    pdf.line(x + 3, y + 6, x + 13, y - 5)
    pdf.line(x + 3, y - 6, x + 13, y + 5)


# ---------------------------------------------------------------- Page 1
def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_PREFIX, PACK_TITLE)
    _instruction(pdf, "Cut out the pictures. Sort them!")
    cols = [("HELPS the Earth", 63), ("HURTS the Earth", 315)]
    for label, cx in cols:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawCentredString(cx + 117, 586, label)
        for k in range(3):
            y = 474 - k * 64
            pdf.setStrokeColor(RULE)
            pdf.setLineWidth(1.2)
            pdf.setDash(5, 4)
            p = pdf.beginPath()
            p.roundRect(cx, y, 234, 54, 10)
            pdf.drawPath(p, stroke=1, fill=0)
            pdf.setDash()
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(63, 330, "CUT-OUT AREA")
    _scissors(pdf, 184, 330)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.2)
    pdf.setDash(5, 4)
    p = pdf.beginPath()
    p.roundRect(63, 132, 486, 184, 12)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setDash()
    chips = [RECYCLE, PLANT, WATER, TAP_RUN, POND_BOTTLE, LITTER]
    for i, img in enumerate(chips):
        row, col = divmod(i, 3)
        x = 73 + col * 158
        y = 232 - row * 86
        _img_fill(pdf, img, x, y, 148, 72, r=8)
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(1.1)
        pdf.setDash(4, 3)
        p = pdf.beginPath()
        p.roundRect(x - 4, y - 4, 156, 80, 10)
        pdf.drawPath(p, stroke=1, fill=0)
        pdf.setDash()
    _adult(pdf, [
        "Adult: Talk through each picture first \u2014 what is "
        "happening, and who does",
        "it help or hurt? Sort answers: HELPS \u2014 recycling, "
        "planting, watering",
        "flowers. HURTS \u2014 littering, a bottle in the pond, "
        "water running away.",
    ], top=124, step=13)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 2
def page2(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_PREFIX, PACK_TITLE)
    _instruction(pdf, "Circle the picture that FIXES the problem!")
    rows = [
        (P_TAP, FIX_WRENCH, IGNORE_PLAY),
        (P_LITTER, FIX_BIN, TOSS_POND),
        (P_HOSE, FIX_HOSE, PLAY_SPLASH),
        (P_LIGHTS, FIX_LIGHT, LAMP_ON),
    ]
    for r, (problem, a, b) in enumerate(rows):
        y = 500 - r * 116
        _img_fill(pdf, problem, 63, y, 190, 100)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 21)
        pdf.drawCentredString(268, y + 40, "\u2192")
        for k, img in enumerate((a, b)):
            _img_fill(pdf, img, 291 + k * 136, y + 4, 124, 92)
    _adult(pdf, [
        "Adult: Name each problem together first (a leak, litter, "
        "wasted water,",
        "lights nobody needs). Fixes: tell a grown-up \u2014 they "
        "fix the leak; put",
        "litter in a bin; turn the hose off; switch the light off.",
    ], top=80, step=13)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 3
def page3(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_PREFIX, PACK_TITLE)
    _instruction(pdf, "Think of a problem. Draw your fix!")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawString(63, 590, "Ideas to help you think:")
    for k, img in enumerate((P_LITTER, P_TAP, P_LIGHTS)):
        _img_fill(pdf, img, 63 + k * 170, 486, 152, 92)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14.5)
    pdf.drawString(63, 458, "My problem is:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(176, 456, 549, 456)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14.5)
    pdf.drawString(63, 428, "DRAW you fixing the problem:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.4)
    p = pdf.beginPath()
    p.roundRect(63, 198, 486, 216, 12)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14.5)
    pdf.drawString(63, 170, "My action helps because:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(63, 142, 549, 142)
    pdf.line(63, 114, 549, 114)
    _adult(pdf, [
        "Adult: Help your child pick a REAL problem they have seen "
        "\u2014 at home, at",
        "school, or at the park. They draw themselves fixing it, "
        "then explain HOW",
        "the action helps the land, water, air, or living things. "
        "Scribe their words.",
    ], top=88, step=13)
    draw_footer(pdf)
    pdf.save()


PAGES = [page1, page2, page3]


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
        p = f"/tmp/ec-p{i}.pdf"
        fn(p)
        print("preview page", i, "->", p)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if mode == "build":
        build_pack()
    else:
        preview()
