#!/usr/bin/env python3
"""Long Ago & Me (Kindergarten Social Studies, 4 pages).

Pack 5 of the approved Kindergarten Social Studies roadmap
("Myself and Others"), covering the History expectations:
sequencing one's own past, learning about the past from
sources (photos, elders' stories, saved objects), comparing
life then and now, and comparing a school day long ago with
today — always from visible evidence on the page.

Framing rules (from the approved brief and roadmap):
  * Page 1 is completed WITH the family at home: the frames
    are drawing spaces sized to hold a pasted photo instead.
  * Page 4's SAME/DIFFERENT statements are answerable only
    from what the two scenes visibly show (children learning
    in both; a big screen and a heating stove in only one).
  * The modern car on Page 3 reuses the approved side-view
    car from Maps, Globes & Places Near Us.

  P1 When I Was Little — timeline: baby → toddler → now,
     with a draw-or-paste frame for each stage.
  P2 How Do We Learn About Long Ago? — three source cards
     (old photos, elders' stories, saved things); circle
     the small pictures that can teach us about long ago.
  P3 Then & Now — match candle→lamp, horse-and-carriage→
     car, letter→phone.
  P4 A School Day Long Ago — two scenes; circle SAME or
     DIFFERENT for three read-aloud statements.

No separate parent guide (guide-less draft-review workflow).
Answers and guidance live in the website resource-page text.
"""
import math
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
                      "assets", "long-ago")
MG_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "assets", "maps-globes")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "social-studies",
                       "long-ago")
PACK_TITLE = "Long Ago & Me"
STEM = "long-ago"

RULE = HexColor("#9DB8C4")
PANEL_FILL = HexColor("#F2F8F8")
WHITE = HexColor("#FFFFFF")
GRAY = HexColor("#5A6B73")


def A(name):
    return os.path.join(ASSETS, name + ".jpg")


def _adult(pdf, lines, top=84, step=13):
    pdf.setFillColor(INK)
    for i, line in enumerate(lines):
        pdf.setFont("Helvetica-Bold", 11.5 if i == 0 else 11)
        pdf.drawCentredString(PAGE_WIDTH / 2, top - i * step, line)


def _img_fill(pdf, path, x, y, w, h, focus_x=0.5, focus_y=0.5, r=10):
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
    pdf.setLineWidth(1.4)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.drawPath(p, stroke=1, fill=0)


def _img_contain(pdf, path, x, y, w, h, r=8):
    with Image.open(path) as im:
        iw, ih = im.size
    pdf.setFillColor(WHITE)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.drawPath(p, stroke=0, fill=1)
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx = x + (w - dw) / 2
    dy = y + (h - dh) / 2
    pdf.saveState()
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.drawImage(ImageReader(path), dx, dy, dw, dh,
                  preserveAspectRatio=False, mask="auto")
    pdf.restoreState()
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


def _instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 19)
    pdf.drawCentredString(PAGE_WIDTH / 2, 616, text)


def _match_panel(pdf, x, y, w, h, img, label, label_size=12.5,
                 contain=False):
    _panel(pdf, x, y, w, h)
    if contain:
        _img_contain(pdf, img, x + 8, y + 28, w - 16, h - 36)
    else:
        _img_fill(pdf, img, x + 8, y + 28, w - 16, h - 36)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", label_size)
    pdf.drawCentredString(x + w / 2, y + 9, label)
    pdf.setFillColor(NAVY)
    pdf.circle(x + (w + 6 if x < 300 else -6), y + h / 2, 4.5,
               stroke=0, fill=1)


def _circle_img(pdf, path, cx, cy, r):
    pdf.saveState()
    p = pdf.beginPath()
    p.circle(cx, cy, r)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.drawImage(ImageReader(path), cx - r, cy - r, 2 * r, 2 * r,
                  preserveAspectRatio=False, mask="auto")
    pdf.restoreState()
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.4)
    pdf.circle(cx, cy, r, stroke=1, fill=0)


def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "When I Was Little")
    _instruction(pdf, "I am growing and changing!")
    stages = [
        (A("la-stage-baby"), "BABY", ["I was a baby."]),
        (A("la-stage-toddler"), "TODDLER", ["Then I grew", "bigger."]),
        (A("la-stage-now"), "NOW", ["Now I am in", "kindergarten!"]),
    ]
    for i, (img, label, caption) in enumerate(stages):
        x = 51 + i * 175
        _panel(pdf, x, 236, 160, 336)
        _circle_img(pdf, img, x + 80, 528, 30)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(x + 80, 484, label)
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.4)
        pdf.setDash(6, 4)
        p = pdf.beginPath()
        p.roundRect(x + 13, 322, 134, 148, 8)
        pdf.drawPath(p, stroke=1, fill=0)
        pdf.setDash()
        pdf.setFillColor(GRAY)
        pdf.setFont("Helvetica", 9.5)
        pdf.drawCentredString(x + 80, 402, "Draw or paste")
        pdf.drawCentredString(x + 80, 389, "a photo here")
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 11.5)
        for j, line in enumerate(caption):
            pdf.drawCentredString(x + 80, 296 - j * 15, line)
        if i < 2:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawCentredString(x + 167, 398, "\u2192")
    _adult(pdf, [
        "Adult: Families, complete this page together at home.",
        "Draw or paste a photo for each time, and talk about",
        "how your child has grown and changed.",
    ], top=150)
    draw_footer(pdf)
    pdf.save()


def page2(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "How Do We Learn About Long Ago?")
    _instruction(pdf, "We can learn about long ago.")
    cards = [
        (A("la-source-photos"), "OLD PHOTOS", "Pictures from long ago."),
        (A("la-source-stories"), "STORIES", "Stories from long ago."),
        (A("la-source-things"), "SAVED THINGS", "Things from long ago."),
    ]
    for i, (img, label, caption) in enumerate(cards):
        x = 51 + i * 175
        _panel(pdf, x, 356, 160, 224)
        _img_fill(pdf, img, x + 8, 442, 144, 130)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawCentredString(x + 80, 418, label)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawCentredString(x + 80, 388, caption)
    _panel(pdf, 51, 118, 510, 208)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 296,
                          "Circle the pictures that can teach us "
                          "about long ago.")
    items = [
        (A("la-item-robot"), "A NEW TOY"),
        (A("la-item-photo"), "AN OLD PHOTO"),
        (A("la-source-things"), "SAVED THINGS"),
        (A("la-source-stories"), "A STORY"),
    ]
    for i, (img, label) in enumerate(items):
        x = 66 + i * 125
        _img_contain(pdf, img, x, 172, 105, 104)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawCentredString(x + 52, 150, label)
    _adult(pdf, [
        "Adult: Long ago means the time before now. Photos,",
        "stories from elders, and saved things show us what",
        "life was like then.",
    ], top=92)
    draw_footer(pdf)
    pdf.save()


def page3(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Then & Now")
    _instruction(pdf, "Draw a line from THEN to NOW.")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(146, 566, "THEN \u2014 LONG AGO")
    pdf.drawCentredString(466, 566, "NOW \u2014 TODAY")
    rows = [424, 296, 168]
    left = [(A("la-then-candle"), "A CANDLE"),
            (A("la-then-carriage"), "A HORSE AND CARRIAGE"),
            (A("la-then-letter"), "A LETTER")]
    car = os.path.join(MG_ASSETS, "mg-side-car.jpg")
    right = [(car, "A CAR"),
             (A("la-now-phone"), "A PHONE"),
             (A("la-now-lamp"), "A LAMP")]
    for (img, label), y in zip(left, rows):
        _match_panel(pdf, 51, y, 190, 116, img, label,
                     label_size=11.5 if len(label) > 12 else 12.5,
                     contain=True)
    for (img, label), y in zip(right, rows):
        _match_panel(pdf, 371, y, 190, 116, img, label, contain=True)
    _adult(pdf, [
        "Adult: Long ago, people used candles for light,",
        "horses to travel, and letters to talk far away.",
        "What do we use today?",
    ], top=110)
    draw_footer(pdf)
    pdf.save()


def page4(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "A School Day Long Ago")
    _instruction(pdf, "Look at the two school days.")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(173, 552, "LONG AGO")
    pdf.drawCentredString(439, 552, "TODAY")
    _img_fill(pdf, A("la-school-then"), 51, 336, 245, 200)
    _img_fill(pdf, A("la-school-now"), 316, 336, 245, 200)
    rows = [
        ("Children learn at school.", "SAME"),
        ("There is a big screen.", "DIFFERENT"),
        ("A stove heats the room.", "DIFFERENT"),
    ]
    for i, (statement, _ans) in enumerate(rows):
        y = 268 - i * 56
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawString(61, y + 8, statement)
        for j, word in enumerate(("SAME", "DIFFERENT")):
            w = 66 if word == "SAME" else 96
            x = 372 + j * 104
            pdf.setStrokeColor(NAVY)
            pdf.setLineWidth(1.3)
            pdf.setFillColor(WHITE)
            p = pdf.beginPath()
            p.roundRect(x, y, w, 30, 15)
            pdf.drawPath(p, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawCentredString(x + w / 2, y + 10, word)
    _adult(pdf, [
        "Adult: Read each sentence aloud. Circle SAME if it",
        "is true for both school days, DIFFERENT if it is",
        "true for only one. Talk about what you can see.",
    ], top=104)
    draw_footer(pdf)
    pdf.save()


BUILDERS = [page1, page2, page3, page4]


def build_pack():
    os.makedirs(OUT_DIR, exist_ok=True)
    singles = []
    for i, fn in enumerate(BUILDERS, 1):
        p = os.path.join(OUT_DIR, f"{STEM}-page-{i:02d}.pdf")
        fn(p)
        singles.append(p)
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for p in singles:
        for pg in PdfReader(p).pages:
            w.add_page(pg)
    out = os.path.join(OUT_DIR, f"{STEM}-review.pdf")
    with open(out, "wb") as fh:
        w.write(fh)
    print("built", out)


def preview():
    for i, fn in enumerate(BUILDERS, 1):
        fn(f"/tmp/la-p{i}.pdf")
    print("previews in /tmp/la-pN.pdf")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        preview()
    else:
        build_pack()
