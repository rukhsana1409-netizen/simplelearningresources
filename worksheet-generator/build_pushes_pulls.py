#!/usr/bin/env python3
"""Pushes & Pulls — My Motion Investigations (Kindergarten Science).

Michigan K-PS2-1 / K-PS2-2: pushes and pulls change how objects move;
the strength and direction of a push changes the motion. Every page is
built around a real, adult-supervised investigation with household
objects; the page carries the recording, measuring, and communicating.

Accuracy rules honored (per the approved brief):
  - Page 2 compares DIFFERENT objects on a ramp: distances are recorded
    as observations only; nothing attributes them to push strength.
  - Page 3 uses the SAME object on the SAME surface for gentle vs
    strong pushes; results are recorded, never pre-printed as fact.
  - Page 4 is predict -> test -> record, with the child's own arrows.

No separate parent guide: adult steps are printed on each page, and the
objective / facilitation notes live in the website resource-page text.

Page map:
  1 Push or Pull?          — identify the force in 4 unambiguous scenes
  2 Let's Roll!            — ramp investigation; draw each object, color
                             how many cubes far it rolled
  3 Gentle Push, Strong Push — same ball, same floor; two measured trials
                             and an adult-scribed "I noticed"
  4 Change the Direction   — predict with an arrow, test, record the arrow
  5 My Motion Discovery    — child's question, test drawing, observation
                             drawing, dictated conclusion
"""
import os
import sys

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_phonics_az import (  # noqa: E402
    INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL, draw_footer, draw_header,
)

MARGIN = 60
RULE = HexColor("#9DB8C4")
LIGHT = HexColor("#EAF3F1")

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "pushes-and-pulls")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "science",
                       "pushes-and-pulls")
PACK_TITLE = "Pushes & Pulls"
STEM = "pushes-and-pulls"

CART = os.path.join(ASSETS, "pp-push-cart.jpg")
WAGON = os.path.join(ASSETS, "pp-pull-wagon.jpg")
BOX = os.path.join(ASSETS, "pp-push-box.jpg")
SLED = os.path.join(ASSETS, "pp-pull-sled.jpg")
RAMP = os.path.join(ASSETS, "pp-ramp.jpg")
FLOOR_PUSH = os.path.join(ASSETS, "pp-floor-push.jpg")
TOPDOWN = os.path.join(ASSETS, "pp-topdown.jpg")


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
    """Draw an image aspect-filled into a rect, clipped to rounded corners."""
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


def _frame(pdf, x, y, w, h):
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.4)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, 12)
    pdf.drawPath(p, stroke=1, fill=0)


def _word_pair(pdf, cx, y):
    """PUSH / PULL circuable word pills centered at cx."""
    for word, dx in (("PUSH", -62), ("PULL", 62)):
        wpt = 104
        x = cx + dx - wpt / 2
        pdf.setFillColor(LIGHT)
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(1.2)
        p = pdf.beginPath()
        p.roundRect(x, y, wpt, 40, 20)
        pdf.drawPath(p, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 19)
        pdf.drawCentredString(cx + dx, y + 13, word)


def _cube_strip(pdf, x, y, n=10, cell=27):
    """A row of n empty squares to color: how many cubes far?"""
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.2)
    for i in range(n):
        pdf.rect(x + i * cell, y, cell, cell, stroke=1, fill=0)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 10.5)
    pdf.drawString(x, y - 15, "Color one square for each cube.")


# ---------------------------------------------------------------- Page 1
def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Push or Pull?")
    _instruction(pdf, "Look at each picture. Circle PUSH or PULL!")
    scenes = [(CART, 0.45), (WAGON, 0.5), (BOX, 0.5), (SLED, 0.5)]
    fw, fh = 236, 176
    xs = [63, 313]
    ys = [402, 156]
    for i, (img, fx) in enumerate(scenes):
        x = xs[i % 2]
        y = ys[i // 2]
        _img_fill(pdf, img, x, y, fw, fh, focus_x=fx)
        _word_pair(pdf, x + fw / 2, y - 56)
    _adult(pdf, [
        "Adult: Ask for each picture: \u201cIs the child pushing or "
        "pulling? How can you tell?\u201d",
        "A push moves an object away from the child. A pull moves "
        "an object",
        "toward the child \u2014 the wagon and the sled are pulled "
        "along behind.",
    ], top=84, step=16)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 2
def page2(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Let's Roll!")
    _instruction(pdf, "Build a ramp. Roll 3 things. Record how far!")
    _img_fill(pdf, RAMP, 356, 452, 200, 138)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 12.5)
    steps = [
        "You need: a board or big book,",
        "books to lift one end, cubes,",
        "and 3 things that roll.",
        "",
        "1. Put one thing at the top.",
        "2. Let go \u2014 no push! It rolls.",
        "3. Measure with cubes.",
        "4. Draw it. Color its squares.",
    ]
    for i, s in enumerate(steps):
        pdf.drawString(MARGIN + 6, 574 - i * 18, s)
    # chart
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(MARGIN + 6, 424, "What I rolled")
    pdf.drawString(238, 424, "How far it rolled (in cubes)")
    rows_y = [330, 238, 146]
    for ry in rows_y:
        _frame(pdf, MARGIN + 6, ry, 150, 78)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 10.5)
        pdf.drawCentredString(MARGIN + 6 + 75, ry + 62, "Draw it here")
        _cube_strip(pdf, 238, ry + 26, n=10, cell=27)
    _adult(pdf, [
        "Adult: Same ramp, same starting spot at the top for every "
        "roll \u2014",
        "and always just let go, with no extra push. Different "
        "objects roll",
        "different distances; that is the observation. Ask: "
        "\u201cWhich rolled farthest?\u201d",
    ], top=92, step=16)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 3
def page3(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Gentle Push, Strong Push")
    _instruction(pdf, "Same ball. Same floor. Two pushes!")
    _img_fill(pdf, FLOOR_PUSH, 376, 466, 180, 124)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 12.5)
    lines = [
        "Use the SAME ball on the",
        "SAME floor both times.",
        "",
        "Push 1: gentle.",
        "Measure with cubes.",
        "Push 2: stronger.",
        "Measure again.",
    ]
    for i, s in enumerate(lines):
        pdf.drawString(MARGIN + 6, 566 - i * 19, s)
    trials = [("Push 1 \u2014 GENTLE", 372), ("Push 2 \u2014 STRONG", 268)]
    for label, ty in trials:
        pdf.setFillColor(white)
        pdf.setStrokeColor(TEAL)
        pdf.setLineWidth(1.4)
        p = pdf.beginPath()
        p.roundRect(MARGIN + 6, ty, 196, 36, 18)
        pdf.drawPath(p, stroke=1, fill=0)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 14.5)
        pdf.drawCentredString(MARGIN + 6 + 98, ty + 12, label)
        _cube_strip(pdf, 280, ty + 4, n=10, cell=27)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(MARGIN + 6, 224, "I noticed:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(MARGIN + 6, 196, PAGE_WIDTH - MARGIN - 6, 196)
    pdf.line(MARGIN + 6, 168, PAGE_WIDTH - MARGIN - 6, 168)
    _adult(pdf, [
        "Adult: Mark where the ball starts so both pushes begin at "
        "the same spot.",
        "Write your child's exact words for \u201cI noticed.\u201d "
        "There is no printed answer \u2014 the",
        "measurements your child made are the result.",
    ], top=118)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 4
def _arrow_box(pdf, x, y, w, h, label=None, ball_side="left"):
    if label:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawCentredString(x + w / 2, y + h + 8, label)
    _frame(pdf, x, y, w, h)
    # a small ball at the push side: the child's arrow starts here
    bx = x + 34 if ball_side == "left" else x + w - 34
    pdf.setFillColor(HexColor("#D64541"))
    pdf.circle(bx, y + h / 2, 13, stroke=0, fill=1)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(x + w / 2, y + 8, "Draw your arrow here")


def _side_chip(pdf, x, y, w, h, trial, from_left):
    """Diagram chip: which side the push comes from."""
    _frame(pdf, x, y, w, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(x + w / 2, y + h - 24, trial)
    cy = y + h / 2 - 4
    pdf.setFillColor(HexColor("#D64541"))
    if from_left:
        ball_cx = x + w - 30
        pdf.circle(ball_cx, cy, 15, stroke=0, fill=1)
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(3)
        pdf.line(x + 14, cy, ball_cx - 22, cy)
        pdf.line(ball_cx - 22, cy, ball_cx - 32, cy + 6)
        pdf.line(ball_cx - 22, cy, ball_cx - 32, cy - 6)
    else:
        ball_cx = x + 30
        pdf.circle(ball_cx, cy, 15, stroke=0, fill=1)
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(3)
        pdf.line(ball_cx + 22, cy, x + w - 14, cy)
        pdf.line(ball_cx + 22, cy, ball_cx + 32, cy + 6)
        pdf.line(ball_cx + 22, cy, ball_cx + 32, cy - 6)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(x + w / 2, y + 9,
                          "from the left" if from_left else "from the right")


def page4(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Change the Direction")
    _instruction(pdf, "Push the same ball from two sides!")
    _img_fill(pdf, TOPDOWN, MARGIN + 56, 392, 440, 198)
    # column headers (Trial 1 row)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(118, 374, "Push from this side")
    pdf.drawCentredString(268, 374, "PREDICT \u2014 my arrow")
    pdf.drawCentredString(450, 374, "RECORD \u2014 what happened")
    rows = [(278, "TRIAL 1", True, "left"), (150, "TRIAL 2", False, "right")]
    for ry, trial, from_left, ball_side in rows:
        if trial == "TRIAL 2":
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(MARGIN + 6, ry + 96, "Trial 2 \u2014 from the other side")
        _side_chip(pdf, MARGIN + 6, ry, 104, 88, trial, from_left)
        _arrow_box(pdf, 182, ry, 172, 88, ball_side=ball_side)
        _arrow_box(pdf, 366, ry, 172, 88, ball_side=ball_side)
    _adult(pdf, [
        "Adult: Use the SAME ball both times. Trial 1 pushes it from "
        "the left;",
        "Trial 2 pushes it from the right. Predict first, then push, "
        "then record.",
    ], top=108, step=17)
    draw_footer(pdf)
    pdf.save()


# ---------------------------------------------------------------- Page 5
def page5(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Motion Discovery")
    _instruction(pdf, "Ask a question. Test it. Tell what you found!")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15.5)
    pdf.drawString(MARGIN + 6, 574, "My question:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(158, 572, PAGE_WIDTH - MARGIN - 6, 572)
    boxes = [("What I tested", MARGIN + 6), ("What I saw", 320)]
    for label, bx in boxes:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 14.5)
        pdf.drawString(bx, 534, label)
        _frame(pdf, bx, 296, 246, 224)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15.5)
    pdf.drawString(MARGIN + 6, 262, "I found out:")
    pdf.setStrokeColor(RULE)
    pdf.line(MARGIN + 6, 232, PAGE_WIDTH - MARGIN - 6, 232)
    pdf.line(MARGIN + 6, 202, PAGE_WIDTH - MARGIN - 6, 202)
    _adult(pdf, [
        "Adult: Question ideas: \u201cWill a heavy box move?\u201d "
        "\u201cWhat rolls down the ramp?\u201d",
        "Test together with safe household objects. Write your "
        "child's question and their",
        "exact words for \u201cI found out.\u201d Drawing is the record; "
        "talking is the science.",
    ], top=150)
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
    tmp = "/tmp"
    for i, fn in enumerate(PAGES, start=1):
        p = os.path.join(tmp, f"pp-p{i}.pdf")
        fn(p)
        print("preview page", i, "->", p)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if mode == "build":
        build_pack()
    else:
        preview()
