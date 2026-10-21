#!/usr/bin/env python3
"""Maps, Globes & Places Near Us (Kindergarten Social
Studies, 5 pages).

Pack 4 of the approved Kindergarten Social Studies roadmap
("Myself and Others"), covering the Geography expectations:
a globe is a model of Earth, maps show places from above,
using a simple school map, places and their purposes, and
how the environment meets human needs.

Framing rules (from the approved brief and roadmap):
  * The school map (P3) is drawn as clean vector art so the
    routes are exact and traceable; it pairs with a real
    walk, and the adult line notes every school's map is
    different.
  * Page 4 goes beyond Our Community (preschool), which
    matched buildings: here children match each PLACE to
    its PURPOSE — what we do there.
  * The coloring Earth (P1) is a stylized picture for
    coloring land and water, not a geographic reference.

  P1 A Globe Is a Model of Earth — Earth from space beside
     a classroom globe; color a picture of Earth (water
     blue, land green) and mark where we live.
  P2 A Map Is a Drawing from Above — match side views of a
     house, a tree, and a car to their views from above.
  P3 My School Map — trace two dashed routes from the
     classroom: to the library and to the playground.
  P4 Where Do We Go? — match library, park, grocery store,
     and post office to what we do there.
  P5 How Our Environment Helps Us — match farm, trees, and
     lake to what each gives us (food; shade and homes;
     water).

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
                      "assets", "maps-globes")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "social-studies",
                       "maps-globes")
PACK_TITLE = "Maps, Globes & Places Near Us"
STEM = "maps-globes"

RULE = HexColor("#9DB8C4")
PANEL_FILL = HexColor("#F2F8F8")
WHITE = HexColor("#FFFFFF")
GOLD = HexColor("#F4B63E")
MAP_GREEN = HexColor("#DDEED3")
HALL_FILL = HexColor("#F7EEDD")
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


def _star(pdf, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.381966
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(fill)
    pdf.drawPath(p, stroke=0, fill=1)


def _img_contain(pdf, path, x, y, w, h, r=8):
    """Draw the COMPLETE image inside a white card, scaled
    proportionally and centered — never cropped."""
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


def _view_panel(pdf, x, y, w, h, img, label):
    _panel(pdf, x, y, w, h)
    _img_contain(pdf, img, x + 8, y + 28, w - 16, h - 36)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(x + w / 2, y + 9, label)
    pdf.setFillColor(NAVY)
    pdf.circle(x + (w + 6 if x < 300 else -6), y + h / 2, 4.5,
               stroke=0, fill=1)

def _match_panel(pdf, x, y, w, h, img, label, label_size=12.5,
                 focus_y=0.5):
    _panel(pdf, x, y, w, h)
    _img_fill(pdf, img, x + 8, y + 28, w - 16, h - 36,
              focus_y=focus_y)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", label_size)
    pdf.drawCentredString(x + w / 2, y + 9, label)
    pdf.setFillColor(NAVY)
    pdf.circle(x + (w + 6 if x < 300 else -6), y + h / 2, 4.5,
               stroke=0, fill=1)


def _blob(pdf, pts):
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)


def _coloring_earth(pdf, cx, cy, r):
    """A stylized picture of Earth for coloring: continent
    outlines inside an ocean circle, all left white."""
    pdf.saveState()
    p = pdf.beginPath()
    p.circle(cx, cy, r)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.setFillColor(WHITE)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.5)
    pdf.setLineJoin(1)
    blobs = [
        [(-58, 36), (-40, 50), (-18, 44), (-12, 28), (-22, 16),
         (-36, 22), (-50, 14), (-60, 24)],
        [(-30, 0), (-15, 4), (-12, -14), (-19, -32), (-27, -44),
         (-35, -26), (-36, -8)],
        [(4, 24), (22, 30), (36, 14), (33, -8), (22, -25),
         (9, -20), (1, 0)],
        [(14, 42), (38, 52), (62, 44), (68, 26), (50, 20),
         (34, 28), (20, 32)],
        [(44, -22), (60, -19), (64, -31), (50, -38), (42, -31)],
    ]
    for blob in blobs:
        _blob(pdf, [(cx + dx * r / 68, cy + dy * r / 68)
                    for dx, dy in blob])
    pdf.restoreState()
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(2)
    pdf.circle(cx, cy, r, stroke=1, fill=0)


def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "A Globe Is a Model of Earth")
    _instruction(pdf, "A globe is a small model of Earth.")
    _img_fill(pdf, A("mg-earth-space"), 51, 402, 240, 168)
    _img_fill(pdf, A("mg-globe"), 321, 402, 240, 168)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(171, 382, "EARTH")
    pdf.drawCentredString(441, 382, "A GLOBE")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 356,
                          "Both show Earth's land and water.")
    _panel(pdf, 51, 112, 510, 224)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 312,
                          "Color this picture of Earth.")
    _coloring_earth(pdf, 168, 200, 76)
    pdf.setFillColor(HexColor("#7FB3D9"))
    pdf.rect(300, 256, 22, 22, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#7CB668"))
    pdf.rect(300, 218, 22, 22, stroke=0, fill=1)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawString(332, 262, "WATER \u2014 color it blue.")
    pdf.drawString(332, 224, "LAND \u2014 color it green.")
    _star(pdf, 311, 186, 10, GOLD)
    pdf.setFillColor(INK)
    pdf.drawString(332, 192, "Draw a star on the land.")
    pdf.drawString(332, 174, "We live on land!")
    _adult(pdf, [
        "Adult: Earth is the planet we live on. A globe is a",
        "model \u2014 a small copy that shows the same land and water.",
    ], top=92)
    draw_footer(pdf)
    pdf.save()


def page2(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "A Map Is a Drawing from Above")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 19)
    pdf.drawCentredString(PAGE_WIDTH / 2, 622,
                          "Many maps show places as if we are")
    pdf.drawCentredString(PAGE_WIDTH / 2, 598,
                          "looking down from above.")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(146, 562, "FROM THE SIDE")
    pdf.drawCentredString(466, 562, "FROM ABOVE")
    rows = [424, 296, 168]
    left = [(A("mg-side-house"), "A house"),
            (A("mg-side-tree"), "A tree"),
            (A("mg-side-car"), "A car")]
    right = [(A("mg-top-car"), "A car"),
             (A("mg-top-house"), "A house"),
             (A("mg-top-tree"), "A tree")]
    for (img, label), y in zip(left, rows):
        _view_panel(pdf, 51, y, 190, 116, img, label)
    for (img, label), y in zip(right, rows):
        _view_panel(pdf, 371, y, 190, 116, img, label)
    _adult(pdf, [
        "Adult: A map is a drawing that shows things from",
        "above \u2014 the way a bird sees them. From above we see",
        "a roof, the top of a car, and the top of a tree.",
    ], top=110)
    draw_footer(pdf)
    pdf.save()


def page3(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My School Map")
    _instruction(pdf, "Trace the two paths.")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 590,
                          "Start at your classroom. "
                          "Follow the lines.")
    pdf.setFillColor(WHITE)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.8)
    p = pdf.beginPath()
    p.roundRect(51, 262, 510, 300, 12)
    pdf.drawPath(p, stroke=1, fill=1)
    # playground
    pdf.setFillColor(MAP_GREEN)
    p = pdf.beginPath()
    p.roundRect(376, 290, 160, 250, 8)
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.6)
    pdf.line(406, 470, 418, 508)
    pdf.line(442, 470, 430, 508)
    pdf.line(406, 508, 442, 508)
    pdf.line(418, 489, 430, 489)
    pdf.line(413, 470, 435, 470)
    pdf.line(472, 356, 472, 402)
    pdf.line(472, 388, 484, 388)
    pdf.line(472, 374, 484, 374)
    pdf.line(484, 402, 518, 366)
    pdf.line(518, 366, 518, 358)
    pdf.setFillColor(HexColor("#7CB668"))
    pdf.circle(520, 452, 13, stroke=0, fill=1)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(450, 520, "PLAYGROUND")
    # building
    pdf.setFillColor(HALL_FILL)
    pdf.rect(86, 290, 260, 250, stroke=0, fill=1)
    pdf.setFillColor(WHITE)
    pdf.rect(86, 440, 260, 100, stroke=0, fill=1)
    pdf.rect(86, 290, 260, 100, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(2)
    pdf.rect(86, 290, 260, 250, stroke=1, fill=0)
    pdf.setLineWidth(1.4)
    pdf.line(216, 440, 216, 540)
    pdf.line(216, 290, 216, 390)
    pdf.line(86, 440, 346, 440)
    pdf.line(86, 390, 346, 390)
    pdf.setStrokeColor(WHITE)
    pdf.setLineWidth(4)
    pdf.line(174, 440, 202, 440)
    pdf.line(256, 440, 284, 440)
    pdf.line(346, 400, 346, 428)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.4)
    pdf.line(176, 440, 176, 464)
    p = pdf.beginPath()
    p.arc(152, 416, 200, 464, startAng=0, extent=90)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.line(282, 440, 282, 464)
    p = pdf.beginPath()
    p.arc(258, 416, 306, 464, startAng=90, extent=90)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.line(346, 428, 322, 428)
    p = pdf.beginPath()
    p.arc(322, 404, 370, 452, startAng=180, extent=90)
    pdf.drawPath(p, stroke=1, fill=0)
    # room labels and icons
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawCentredString(151, 518, "CLASSROOM")
    pdf.drawCentredString(281, 518, "LIBRARY")
    pdf.drawCentredString(151, 366, "CAFETERIA")
    pdf.drawCentredString(281, 366, "ART ROOM")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawCentredString(120, 398, "HALLWAY")
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.4)
    pdf.rect(131, 490, 40, 20, stroke=1, fill=0)
    pdf.line(137, 490, 137, 482)
    pdf.line(165, 490, 165, 482)
    pdf.rect(257, 484, 22, 30, stroke=1, fill=0)
    pdf.rect(281, 484, 22, 30, stroke=1, fill=0)
    pdf.setFillColor(HexColor("#C8402A"))
    pdf.circle(151, 330, 11, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#7CB668"))
    pdf.circle(155, 342, 4, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#E8C87E"))
    pdf.circle(281, 330, 11, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#C8402A"))
    pdf.circle(277, 334, 2.6, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#3C3B6E"))
    pdf.circle(286, 328, 2.6, stroke=0, fill=1)
    # two full paths from the classroom marker: DASHED all the
    # way to the library, DOTTED all the way to the playground.
    # In the shared doorway and hallway they run side by side
    # so each style stays readable end to end, in grayscale too.
    pdf.setStrokeColor(GRAY)
    pdf.setLineCap(1)
    pdf.setLineWidth(3)
    pdf.setDash(0.1, 5.5)
    p = pdf.beginPath()
    p.moveTo(192, 465)
    p.lineTo(192, 412)
    p.lineTo(436, 412)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineWidth(2.6)
    pdf.setDash(6, 4)
    p = pdf.beginPath()
    p.moveTo(180, 465)
    p.lineTo(180, 424)
    p.lineTo(270, 424)
    p.lineTo(270, 466)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setDash()
    pdf.setFillColor(NAVY)
    pdf.circle(186, 465, 5.5, stroke=0, fill=1)
    _star(pdf, 270, 472, 9, GOLD)
    _star(pdf, 445, 412, 9, GOLD)
    # key for the two line styles, on the playground corner
    pdf.setFillColor(WHITE)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    p = pdf.beginPath()
    p.roundRect(388, 296, 140, 54, 6)
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(400, 336, "KEY")
    pdf.setStrokeColor(GRAY)
    pdf.setLineWidth(2.6)
    pdf.setDash(6, 4)
    pdf.line(400, 321, 434, 321)
    pdf.setLineWidth(3)
    pdf.setDash(0.1, 5.5)
    pdf.line(400, 307, 434, 307)
    pdf.setDash()
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(442, 317, "LIBRARY")
    pdf.drawString(442, 303, "PLAYGROUND")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawCentredString(122, 452, "YOU ARE HERE")
    # compass
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.circle(528, 524, 13, stroke=1, fill=0)
    pdf.setFillColor(NAVY)
    p = pdf.beginPath()
    p.moveTo(528, 533)
    p.lineTo(524, 524)
    p.lineTo(532, 524)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawCentredString(528, 514, "N")
    _adult(pdf, [
        "Adult: Take a real walk with this map \u2014 trace a path,",
        "then walk it together. Every school's map is different;",
        "talk about the rooms in your child's own school.",
    ], top=222)
    draw_footer(pdf)
    pdf.save()


def _place_panel(pdf, x, y, img, lines):
    _panel(pdf, x, y, 190, 96)
    _img_fill(pdf, img, x + 8, y + 8, 78, 80, r=8)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 12)
    for i, line in enumerate(lines):
        pdf.drawString(x + 96, y + 58 - i * 17, line)
    pdf.setFillColor(NAVY)
    pdf.circle(x + (196 if x < 300 else -6), y + 48, 4.5,
               stroke=0, fill=1)


def page4(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Where Do We Go?")
    _instruction(pdf, "Match each place to what we do there.")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(146, 566, "PLACES")
    pdf.drawCentredString(466, 566, "WHAT WE DO THERE")
    rows = [448, 340, 232, 124]
    left = [(A("mg-place-library"), ["LIBRARY"]),
            (A("mg-place-park"), ["PARK"]),
            (A("mg-place-grocery"), ["GROCERY", "STORE"]),
            (A("mg-place-post"), ["POST", "OFFICE"])]
    right = [(A("mg-do-buy"), ["BUY FOOD"]),
             (A("mg-do-mail"), ["MAIL A", "LETTER"]),
             (A("mg-do-read"), ["READ", "BOOKS"]),
             (A("mg-do-play"), ["PLAY", "OUTSIDE"])]
    for (img, lines), y in zip(left, rows):
        _place_panel(pdf, 51, y, img, lines)
    for (img, lines), y in zip(right, rows):
        _place_panel(pdf, 371, y, img, lines)
    _adult(pdf, [
        "Adult: Places may look different where you live. Talk",
        "about the library, park, store, and post office near",
        "your home \u2014 and what your family does at each one.",
    ], top=100)
    draw_footer(pdf)
    pdf.save()


def page5(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "How Our Environment Helps Us")
    _instruction(pdf, "Draw a line from each place to its gift.")
    rows = [440, 312, 184]
    left = [(A("mg-env-farm"), "A FARM"),
            (A("mg-env-trees"), "TREES"),
            (A("mg-env-lake"), "A LAKE")]
    right = [(A("mg-gift-water"), "WATER TO DRINK"),
             (A("mg-gift-food"), "FOOD TO EAT"),
             (A("mg-gift-shade"), "SHADE AND HOMES")]
    for (img, label), y in zip(left, rows):
        _match_panel(pdf, 51, y, 200, 118, img, label)
    for (img, label), y, fy in zip(right, rows, [0.5, 0.5, 0.8]):
        _match_panel(pdf, 361, y, 200, 118, img, label, focus_y=fy)
    _adult(pdf, [
        "Adult: Our environment gives us food, shade, homes",
        "for animals, and water. Which of these gifts does",
        "your family use every day?",
    ], top=110)
    draw_footer(pdf)
    pdf.save()


BUILDERS = [page1, page2, page3, page4, page5]


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
        fn(f"/tmp/mg-p{i}.pdf")
    print("previews in /tmp/mg-pN.pdf")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        preview()
    else:
        build_pack()
