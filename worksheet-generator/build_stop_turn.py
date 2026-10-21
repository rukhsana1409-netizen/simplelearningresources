#!/usr/bin/env python3
"""Pushes & Pulls: Stop or Turn! (Kindergarten Science, one page).

A one-page engineering add-on that completes Michigan K-PS2-2 —
analyze data to determine whether a design solution works as
intended to change the speed or direction of an object with a push
or a pull — which the five-page Pushes & Pulls investigations only
began. (K-2-ETS1-1/2/3 ride along: define the problem, sketch the
design, test and judge it.)

The child:
  1. CHOOSES a job — STOP the ball (it rolls too far) or TURN the
     ball (it must reach a flag off to the side) — and circles one.
  2. DRAWS a design built from everyday things (blocks, books,
     cardboard, a pillow).
  3. BUILDS it and TESTS it 3 times under fair-test rules (same
     ball, same ramp or same gentle push, same start), circling
     WORKED / NOT YET for each trial and circling one actual
     observation for that roll (It stopped! / It turned! / It kept
     going!) — real data, honestly recorded either way.
  4. EXPLAINS whether the design worked, scribed by an adult; if
     it did not work, changing the design and testing again is the
     engineering move.

No separate parent guide: the fair-test protocol and facilitation
notes are printed briefly on the page, with the objective and
answers as website resource-page text.
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
                      "assets", "stop-or-turn")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "science",
                       "stop-or-turn")
PACK_TITLE = "Pushes & Pulls"
STEM = "stop-or-turn"

RULE = HexColor("#9DB8C4")
PANEL_FILL = HexColor("#F2F8F8")
BROWN = HexColor("#8A5A2B")

STOP_IMG = os.path.join(ASSETS, "st-stop.jpg")
TURN_IMG = os.path.join(ASSETS, "st-turn.jpg")


def _adult(pdf, lines, top=80, step=13):
    pdf.setFillColor(INK)
    for i, line in enumerate(lines):
        pdf.setFont("Helvetica-Bold", 11.5 if i == 0 else 11)
        pdf.drawCentredString(PAGE_WIDTH / 2, top - i * step, line)


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


def _mat_icon(pdf, cx, cy, kind):
    if kind == "blocks":
        pdf.setStrokeColor(BROWN)
        pdf.setLineWidth(1.7)
        pdf.rect(cx - 14, cy - 2, 15, 15, stroke=1, fill=0)
        pdf.rect(cx + 1, cy - 13, 15, 15, stroke=1, fill=0)
    elif kind == "books":
        pdf.setStrokeColor(BROWN)
        pdf.setLineWidth(1.7)
        pdf.rect(cx - 13, cy - 13, 10, 26, stroke=1, fill=0)
        pdf.rect(cx - 1, cy - 13, 10, 26, stroke=1, fill=0)
        pdf.line(cx - 13, cy + 8, cx - 3, cy + 8)
        pdf.line(cx - 1, cy + 8, cx + 9, cy + 8)
    elif kind == "cardboard":
        pdf.setFillColor(HexColor("#C89B6A"))
        pdf.setStrokeColor(BROWN)
        pdf.setLineWidth(1.6)
        pdf.rect(cx - 15, cy - 11, 30, 22, stroke=1, fill=1)
        pdf.line(cx - 15, cy, cx + 15, cy)
    elif kind == "pillow":
        pdf.setStrokeColor(TEAL)
        pdf.setLineWidth(1.8)
        p = pdf.beginPath()
        p.roundRect(cx - 15, cy - 10, 30, 20, 8)
        pdf.drawPath(p, stroke=1, fill=0)
        pdf.circle(cx, cy, 2.2, stroke=1, fill=0)


def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Stop or Turn!")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 19)
    pdf.drawCentredString(PAGE_WIDTH / 2, 616,
                          "Choose a job. Build it. Test it!")
    # 1 — choose the job
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(63, 590, "1. CHOOSE your job \u2014 circle one:")
    for label, img, x, fy in (("STOP the ball", STOP_IMG, 63, 0.45),
                              ("TURN the ball", TURN_IMG, 315, 0.42)):
        _panel(pdf, x, 448, 234, 128)
        _img_fill(pdf, img, x + 12, 494, 210, 72, focus_y=fy)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(x + 117, 464, label)
    # 2 — draw the design (+ materials hints)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(63, 424, "2. DRAW your design:")
    mats = [("blocks", "BLOCKS"), ("books", "BOOKS"),
            ("cardboard", "CARDBOARD"), ("pillow", "PILLOW")]
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(238, 421, "You can use:")
    for k, (kind, word) in enumerate(mats):
        cx = 330 + k * 56
        _mat_icon(pdf, cx, 424, kind)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 7.5)
        pdf.drawCentredString(cx, 402, word)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.4)
    p = pdf.beginPath()
    p.roundRect(63, 276, 486, 114, 12)
    pdf.drawPath(p, stroke=1, fill=0)
    # 3 — test three times, circling a verdict and an observation
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(63, 256, "3. TEST it 3 times. Circle what happened:")
    for k in range(3):
        x = 63 + k * 170
        _panel(pdf, x, 116, 152, 132)
        pdf.setFillColor(TEAL)
        pdf.circle(x + 17, 234, 10, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(x + 17, 230, str(k + 1))
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(x + 36, 229, "What happened?")
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.3)
        pdf.circle(x + 17, 206, 6, stroke=1, fill=0)
        pdf.circle(x + 90, 206, 6, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(x + 27, 202, "WORKED!")
        pdf.drawString(x + 100, 202, "NOT YET")
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawString(x + 10, 181, "I saw:")
        for j, obs in enumerate(("It stopped!", "It turned!",
                                 "It kept going!")):
            cy = 165 - j * 17
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(1.2)
            pdf.circle(x + 16, cy, 5.5, stroke=1, fill=0)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(x + 27, cy - 4, obs)
    # 4 — explain
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(63, 100, "4. Tell a grown-up: Did it work?")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(300, 98, 549, 98)
    _adult(pdf, [
        "Adult: Fair test \u2014 same ball, same ramp or same gentle "
        "push, rolled the",
        "same way all 3 times. Circle what your child saw each "
        "time. If it did",
        "not work, change the design and test again: that is what "
        "engineers do.",
    ])
    draw_footer(pdf)
    pdf.save()


PAGES = [page1]


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
        p = f"/tmp/st-p{i}.pdf"
        fn(p)
        print("preview page", i, "->", p)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if mode == "build":
        build_pack()
    else:
        preview()
