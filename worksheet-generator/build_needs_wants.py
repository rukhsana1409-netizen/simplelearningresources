#!/usr/bin/env python3
"""Needs, Wants & Working (Kindergarten Social Studies, 5 pages).

Pack 1 of the approved Kindergarten Social Studies roadmap
("Myself and Others"), covering the Economics expectations:
needs versus wants, why people work, and goods and services.

Framing rules (from the approved brief):
  * Needs are essential; wants are things we would like. Wants
    are NEVER presented as bad.
  * Page 3 must not imply every family has enough money for
    everything: money goes first to needs; a want is a choice
    for when there is money left.
  * Jobs vocabulary is NOT retaught — Our Community (preschool)
    owns workers, tools, and helpers. Page 3 uses generic
    grown-ups working.

  P1 What People Need — the four human needs (food, water,
     shelter/home, clothing) as four big pictured panels.
  P2 Needs or Wants? — cut-and-paste sort, 4 needs + 4 wants,
     mixed across both cut-out rows.
  P3 Why Do People Work? — visual sequence WORK → EARN → BUY,
     then a "needs first" band with the want as a sometimes.
  P4 Goods or Services? — teaching page: goods are things we
     can hold; services are work people do for us; hero picture
     plus three pictured examples on each side.
  P5 Goods or Services? Sort — cut-and-paste application with
     unambiguous examples (apple/book/ball vs doctor/haircut/
     bus driver). Answers live in the website resource-page
     text, not on the worksheets.

No separate parent guide (guide-less draft-review workflow).
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
                      "assets", "needs-wants")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "social-studies",
                       "needs-wants-working")
PACK_TITLE = "Needs, Wants & Working"
STEM = "needs-wants-working"

RULE = HexColor("#9DB8C4")
PANEL_FILL = HexColor("#F2F8F8")
WHITE = HexColor("#FFFFFF")


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


def _scissors(pdf, cx, cy):
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.6)
    pdf.circle(cx - 5, cy - 5, 3.6, stroke=1, fill=0)
    pdf.circle(cx + 5, cy - 5, 3.6, stroke=1, fill=0)
    pdf.line(cx - 3, cy - 2, cx + 6, cy + 7)
    pdf.line(cx + 3, cy - 2, cx - 6, cy + 7)


def _instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 19)
    pdf.drawCentredString(PAGE_WIDTH / 2, 616, text)


def _work_box(pdf, x, head, box_y, box_h, slots):
    _panel(pdf, x, box_y, 234, box_h)
    pdf.setFillColor(TEAL)
    p = pdf.beginPath()
    p.roundRect(x + 10, box_y + box_h - 38, 214, 28, 8)
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(x + 117, box_y + box_h - 30, head)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    for sx, sy, sw, sh in slots:
        pdf.setDash(4, 3)
        pdf.rect(x + sx, sy, sw, sh, stroke=1, fill=0)
        pdf.setDash()


def _cut_frame(pdf, frame_y, frame_h, chips):
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.4)
    pdf.setDash(6, 4)
    p = pdf.beginPath()
    p.roundRect(51, frame_y, 510, frame_h, 12)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setDash()
    _scissors(pdf, 66, frame_y + frame_h - 8)
    for img, cx, cy, cw, ch in chips:
        _img_fill(pdf, img, cx, cy, cw, ch, r=8)


SORT_ADULT_2 = [
    "Adult: NEEDS are things people must have to live. WANTS are",
    "things people would like \u2014 wants are not bad, they are just",
    "not must-haves. Let your child explain each choice first.",
]
SORT_ADULT_5 = [
    "Adult: For each picture ask: Can I hold it, or is it work",
    "someone does for me? Let your child explain each choice",
    "before gluing. Answers are on the website page.",
]


def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What People Need")
    _instruction(pdf, "People need these things to live and be healthy.")
    cells = [("nw-needs-food", "FOOD", 63, 402),
             ("nw-needs-water", "WATER", 315, 402),
             ("nw-needs-home", "A HOME", 63, 182),
             ("nw-needs-clothes", "CLOTHES", 315, 182)]
    for img, label, x, y in cells:
        _panel(pdf, x, y, 234, 186)
        _img_fill(pdf, A(img), x + 10, y + 44, 214, 132)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawCentredString(x + 117, y + 16, label)
    _adult(pdf, [
        "Adult: Needs are things every person must have to live and stay",
        "healthy. Talk about each picture together: What foods do we need?",
        "Where does our water come from? Who lives in our home?",
    ])
    draw_footer(pdf)
    pdf.save()


def page2(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Needs or Wants?")
    _instruction(pdf, "Cut out the pictures. Glue each one in the right box.")
    slots = [(8, 474, 104, 72), (118, 474, 104, 72),
             (8, 394, 104, 72), (118, 394, 104, 72)]
    for head, x in (("NEEDS", 63), ("WANTS", 315)):
        _work_box(pdf, x, head, 386, 204, slots)
    chips = [
        (A("nw-want-teddy"), 63, 264, 104, 72),
        (A("nw-needs-food"), 189, 264, 104, 72),
        (A("nw-want-balloons"), 315, 264, 104, 72),
        (A("nw-needs-water"), 441, 264, 104, 72),
        (A("nw-needs-home"), 63, 184, 104, 72),
        (A("nw-want-toycar"), 189, 184, 104, 72),
        (A("nw-needs-clothes"), 315, 184, 104, 72),
        (A("nw-want-icecream"), 441, 184, 104, 72),
    ]
    _cut_frame(pdf, 168, 184, chips)
    _adult(pdf, SORT_ADULT_2, top=140)
    draw_footer(pdf)
    pdf.save()


def page3(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Why Do People Work?")
    _instruction(pdf, "Grown-ups work. Follow the pictures!")
    steps = [("nw-work", "WORK", "Grown-ups do jobs"),
             ("nw-earn", "EARN", "They earn money"),
             ("nw-shop", "BUY", "Money buys needs")]
    for i, (img, cap, sub) in enumerate(steps):
        x = 63 + i * 168
        _panel(pdf, x, 420, 150, 166)
        _img_fill(pdf, A(img), x + 10, 470, 130, 106)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(x + 75, 448, cap)
        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(x + 75, 434, sub)
        if i < 2:
            ax = x + 156
            pdf.setFillColor(TEAL)
            p = pdf.beginPath()
            p.moveTo(ax, 496)
            p.lineTo(ax + 12, 503)
            p.lineTo(ax, 510)
            p.close()
            pdf.drawPath(p, stroke=0, fill=1)
    _panel(pdf, 63, 216, 486, 164)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 352,
                          "First, money buys what we NEED.")
    for j, img in enumerate(("nw-needs-food", "nw-needs-home",
                             "nw-needs-clothes")):
        _img_fill(pdf, A(img), 120 + j * 105, 272, 90, 60, r=8)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(90, 248, "Sometimes, if there is money left,")
    pdf.drawString(90, 232, "a family may choose a want too.")
    _img_fill(pdf, A("nw-want-teddy"), 452, 222, 56, 56, r=8)
    _adult(pdf, [
        "Adult: People work to earn money. Families use money first for",
        "the things they need. Not every family can buy everything \u2014 a",
        "want is a choice for when there is money left after needs.",
    ])
    draw_footer(pdf)
    pdf.save()


def page4(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Goods or Services?")
    _instruction(pdf, "Goods we can hold. Services are work people do.")
    sides = [
        ("GOODS", "nw-goods", "Things we can hold:",
         [("nw-g-apple", "APPLE"), ("nw-g-book", "BOOK"),
          ("nw-g-ball", "BALL")], "Bread is a good.", 63),
        ("SERVICES", "nw-service", "Work people do for us:",
         [("nw-s-doctor", "DOCTOR"), ("nw-s-bus", "BUS DRIVER"),
          ("nw-s-mail", "MAIL CARRIER")], "A haircut is a service.", 315),
    ]
    for head, hero, caption, minis, sentence, x in sides:
        _panel(pdf, x, 250, 234, 340)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawCentredString(x + 117, 562, head)
        _img_fill(pdf, A(hero), x + 10, 430, 214, 122)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x + 14, 410, caption)
        for j, (img, label) in enumerate(minis):
            mx = x + 14 + j * 72
            _img_fill(pdf, A(img), mx, 344, 62, 48, r=8)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 8.5)
            pdf.drawCentredString(mx + 31, 330, label)
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(1)
        pdf.line(x + 14, 306, x + 220, 306)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Oblique", 12.5)
        pdf.drawCentredString(x + 117, 282, sentence)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 190,
                          "Look around your home. What goods can you find?")
    _adult(pdf, [
        "Adult: GOODS are things we can hold, carry, and keep \u2014 bread, a",
        "book, shoes. SERVICES are work people do for us \u2014 a haircut, a",
        "doctor's help, a bus ride. Ask: Can you hold it, or is it work?",
    ])
    draw_footer(pdf)
    pdf.save()


def page5(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Goods or Services? Sort")
    _instruction(pdf, "Cut out the pictures. Glue each one in the right box.")
    slots = [(42, 488, 150, 50), (42, 430, 150, 50), (42, 372, 150, 50)]
    for head, x in (("GOODS", 63), ("SERVICES", 315)):
        _work_box(pdf, x, head, 366, 224, slots)
    chips = [
        (A("nw-g-apple"), 63, 278, 150, 50),
        (A("nw-s-doctor"), 231, 278, 150, 50),
        (A("nw-g-ball"), 399, 278, 150, 50),
        (A("nw-service"), 63, 214, 150, 50),
        (A("nw-g-book"), 231, 214, 150, 50),
        (A("nw-s-bus"), 399, 214, 150, 50),
    ]
    _cut_frame(pdf, 186, 158, chips)
    _adult(pdf, SORT_ADULT_5, top=152)
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
        p = f"/tmp/nw-p{i}.pdf"
        fn(p)
        print("preview page", i, "->", p)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if mode == "build":
        build_pack()
    else:
        preview()
