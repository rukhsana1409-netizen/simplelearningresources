#!/usr/bin/env python3
"""Kindergarten Math - Positional Words (Learning Made Simple).

K.G.A.1: describe objects using names of shapes AND positional words
(above, below, beside, next to, in front of, behind).
Genuine progression from the Preschool Positional Words pack (which used
everyday objects and recognition-only tasks): shapes as subjects,
statement completion, and follow-the-direction drawing tasks.

Page 1: Above & Below.
US Letter portrait.

Canonical logo: verbatim generate_worksheet.py::draw_logo (Addition Within 5
master). Do not redraw or approximate.

Only Page 1 exists; it is in review (locked=False).
"""
import math
import os

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = letter  # 612 x 792

TEAL = HexColor("#1F8A8A")
TEAL_DARK = HexColor("#14707A")
NAVY = HexColor("#1F3A5F")
INK = HexColor("#2B3A4A")

# ---------------------------------------------------------------------------
# Canonical logo lockup — VERBATIM copy of generate_worksheet.py::draw_logo,
# the approved Addition Within 5 master. Do not redraw or reinterpret.
# ---------------------------------------------------------------------------
_LOGO_TEAL = HexColor("#007C70")
_LOGO_INK = HexColor("#202A33")
_LOGO_GOLD = HexColor("#F4B63E")


def draw_logo(pdf, x, y):
    """Draw a compact, vector-only Learning Made Simple mark and wordmark."""
    pdf.setFillColor(_LOGO_TEAL)
    pdf.circle(x + 18, y + 26, 7, fill=1, stroke=0)
    pdf.setStrokeColor(_LOGO_TEAL)
    pdf.setLineWidth(2)
    pdf.line(x + 18, y + 18, x + 18, y + 4)
    pdf.line(x + 18, y + 14, x + 6, y + 5)
    pdf.line(x + 18, y + 14, x + 30, y + 5)
    pdf.setLineWidth(1.3)
    pdf.line(x + 2, y + 4, x + 18, y)
    pdf.line(x + 18, y, x + 34, y + 4)
    pdf.setFillColor(_LOGO_GOLD)
    pdf.circle(x + 18, y + 39, 3.5, fill=1, stroke=0)
    pdf.setFillColor(_LOGO_TEAL)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(x + 43, y + 24, "LEARNING")
    pdf.setFillColor(_LOGO_INK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(x + 43, y + 10, "MADE SIMPLE")


def draw_header(pdf, title, subtitle):
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, stroke=0, fill=1)
    draw_logo(pdf, 60, PAGE_HEIGHT - 86)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1)
    pdf.line(218, PAGE_HEIGHT - 88, 218, PAGE_HEIGHT - 48)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(234, PAGE_HEIGHT - 68, title)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(234, PAGE_HEIGHT - 90, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.6)
    pdf.line(60, PAGE_HEIGHT - 104, PAGE_WIDTH - 60, PAGE_HEIGHT - 104)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(60, PAGE_HEIGHT - 126, "Name:")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.2)
    pdf.line(104, PAGE_HEIGHT - 128, 372, PAGE_HEIGHT - 128)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(400, PAGE_HEIGHT - 126, "Date:")
    pdf.line(440, PAGE_HEIGHT - 128, PAGE_WIDTH - 60, PAGE_HEIGHT - 128)


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF2F2"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, stroke=0, fill=1)
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(60, 26, "Learning Made Simple")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1)
    pdf.line(218, 14, 218, 34)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_WIDTH / 2 + 20, 25,
                          "Made with love for little learners.")
    pdf.setFont("Helvetica", 8.5)
    pdf.drawRightString(PAGE_WIDTH - 60, 25, "\u00a9 2026 Learning Made Simple")


# ---------------------------------------------------------------------------
# Shape helpers (flat, colorful)
# ---------------------------------------------------------------------------
def _poly(pdf, pts, fill):
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(fill)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.drawPath(p, stroke=1, fill=1)


def _circle(pdf, cx, cy, r, fill):
    pdf.setFillColor(fill)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.circle(cx, cy, r, stroke=1, fill=1)


def _triangle(pdf, cx, cy, s, fill):
    _poly(pdf, [(cx - s / 2, cy - s / 2), (cx + s / 2, cy - s / 2),
                (cx, cy + s / 2)], fill)


def _square(pdf, cx, cy, s, fill):
    _poly(pdf, [(cx - s / 2, cy - s / 2), (cx + s / 2, cy - s / 2),
                (cx + s / 2, cy + s / 2), (cx - s / 2, cy + s / 2)], fill)


def _rect(pdf, cx, cy, w, h, fill):
    _poly(pdf, [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2),
                (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], fill)


def _hexagon(pdf, cx, cy, r, fill):
    pts = [(cx + r * math.cos(math.pi / 2 + i * math.pi / 3),
            cy + r * math.sin(math.pi / 2 + i * math.pi / 3))
           for i in range(6)]
    _poly(pdf, pts, fill)


def _dashed_shape(pdf, kind, cx, cy, s):
    pdf.setStrokeColor(HexColor("#8A99AB"))
    pdf.setLineWidth(2)
    pdf.setDash(7, 5)
    if kind == "triangle":
        pts = [(cx - s / 2, cy - s / 2), (cx + s / 2, cy - s / 2),
               (cx, cy + s / 2)]
    else:
        pts = [(cx - s / 2, cy - s / 2), (cx + s / 2, cy - s / 2),
               (cx + s / 2, cy + s / 2), (cx - s / 2, cy + s / 2)]
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setDash()


CORAL = HexColor("#F2765C")
PURPLE = HexColor("#9B7BC8")
TEAL_S = HexColor("#3FB6B2")
GREEN = HexColor("#7BC96F")
AMBER = HexColor("#F5B942")


# ---------------------------------------------------------------------------
# Page 1 -- Above & Below
# ---------------------------------------------------------------------------
def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Above & Below", "Positional Words")

    # ---- EXAMPLE ----
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 542, 532, 106, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, 624, "Example:")
    _triangle(pdf, 150, 616, 44, TEAL_S)
    _square(pdf, 150, 572, 42, PURPLE)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    x = 240
    for seg, color, bold in [("The triangle is ", NAVY, False),
                             ("above", TEAL_DARK, True),
                             (" the square.", NAVY, False)]:
        pdf.setFillColor(color)
        pdf.setFont("Helvetica-Bold" if bold else "Helvetica", 15)
        pdf.drawString(x, 590, seg)
        x += pdf.stringWidth(seg, "Helvetica-Bold" if bold else "Helvetica",
                             15)

    # ---- PRACTICE A: complete the sentence ----
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 522,
                          "Complete the sentence. Circle above or below.")

    rows = [
        # (top_shape, bottom_shape, subject, landmark, correct)
        ("circle", "square", "circle", "square", "above"),
        ("triangle", "hexagon", "hexagon", "triangle", "below"),
    ]
    for i, (ts, bs, subj, land, correct) in enumerate(rows):
        top = 506 - i * 108
        fill = HexColor("#F7FAFC") if i % 2 == 0 else HexColor("#FDFBF7")
        border = HexColor("#D5DEE8") if i % 2 == 0 else HexColor("#E3D9C2")
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 100, 532, 100, 12, stroke=1, fill=1)
        cy = top - 50
        draw = {"circle": lambda: _circle(pdf, 115, cy + 25, 25, CORAL),
                "square": lambda: _square(pdf, 115, cy - 25, 48, PURPLE),
                "triangle": lambda: _triangle(pdf, 115, cy + 25, 52, TEAL_S),
                "hexagon": lambda: _hexagon(pdf, 115, cy - 25, 27, AMBER)}
        draw[ts]()
        draw[bs]()
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(200, cy + 20,
                       "The %s is ______ the %s." % (subj, land))
        for c, word in enumerate(["above", "below"]):
            px = 230 + c * 150
            pdf.setFillColor(white)
            pdf.setStrokeColor(HexColor("#C9D6E2"))
            pdf.setLineWidth(1.6)
            pdf.roundRect(px, cy - 44, 130, 44, 22, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawCentredString(px + 65, cy - 29, word)

    # ---- PRACTICE B: follow the direction ----
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 278,
                          "Follow the direction. Draw the shape.")
    pdf.setFillColor(HexColor("#F2F7F2"))
    pdf.setStrokeColor(HexColor("#C4DCC4"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 66, 532, 196, 12, stroke=1, fill=1)
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1)
    pdf.line(306, 78, 306, 250)

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(173, 238, "Draw a triangle below the circle.")
    _circle(pdf, 173, 196, 28, CORAL)

    pdf.setFillColor(NAVY)
    pdf.drawCentredString(439, 238, "Draw a square above the circle.")
    _circle(pdf, 439, 122, 28, TEAL_S)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Beside / Next To
# ---------------------------------------------------------------------------
def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Beside / Next To", "Positional Words")

    # ---- EXAMPLE ----
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 542, 532, 106, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, 624, "Example:")
    _circle(pdf, 140, 595, 26, CORAL)
    _square(pdf, 218, 595, 50, PURPLE)
    pdf.setFillColor(NAVY)
    x = 300
    for seg, color, bold in [("The circle is ", NAVY, False),
                             ("beside", TEAL_DARK, True),
                             (" the square.", NAVY, False)]:
        pdf.setFillColor(color)
        pdf.setFont("Helvetica-Bold" if bold else "Helvetica", 15)
        pdf.drawString(x, 602, seg)
        x += pdf.stringWidth(seg, "Helvetica-Bold" if bold else "Helvetica",
                             15)
    pdf.setFillColor(HexColor("#33465C"))
    pdf.setFont("Helvetica-Oblique", 12.5)
    pdf.drawString(300, 578, "Beside means next to.")

    # ---- PRACTICE A: complete the sentence ----
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 522,
                          "Complete the sentence. Circle the word.")
    rows = [
        # (left_shape, right_shape, subject, landmark, distractor)
        ("triangle", "rectangle", "triangle", "rectangle", "above"),
        ("circle", "hexagon", "circle", "hexagon", "below"),
    ]
    for i, (ls, rs, subj, land, distract) in enumerate(rows):
        top = 506 - i * 108
        fill = HexColor("#F7FAFC") if i % 2 == 0 else HexColor("#FDFBF7")
        border = HexColor("#D5DEE8") if i % 2 == 0 else HexColor("#E3D9C2")
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 100, 532, 100, 12, stroke=1, fill=1)
        cy = top - 50
        draw = {"circle": lambda X: _circle(pdf, X, cy, 25, CORAL),
                "square": lambda X: _square(pdf, X, cy, 48, PURPLE),
                "triangle": lambda X: _triangle(pdf, X, cy, 52, TEAL_S),
                "hexagon": lambda X: _hexagon(pdf, X, cy, 27, AMBER),
                "rectangle": lambda X: _rect(pdf, X, cy, 64, 42, GREEN)}
        draw[ls](95)
        draw[rs](180)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(250, cy + 20,
                       "The %s is ______ the %s." % (subj, land))
        for c, word in enumerate(["beside", distract]):
            px = 270 + c * 150
            pdf.setFillColor(white)
            pdf.setStrokeColor(HexColor("#C9D6E2"))
            pdf.setLineWidth(1.6)
            pdf.roundRect(px, cy - 44, 130, 44, 22, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawCentredString(px + 65, cy - 29, word)

    # ---- PRACTICE B: follow the direction ----
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 278,
                          "Follow the direction. Draw the shape.")
    pdf.setFillColor(HexColor("#F2F7F2"))
    pdf.setStrokeColor(HexColor("#C4DCC4"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 66, 532, 196, 12, stroke=1, fill=1)
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1)
    pdf.line(306, 78, 306, 250)

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(173, 238, "Draw a circle beside the square.")
    _square(pdf, 120, 155, 56, PURPLE)

    pdf.setFillColor(NAVY)
    pdf.drawCentredString(439, 238, "Draw a triangle next to the circle.")
    _circle(pdf, 500, 155, 28, TEAL_S)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- In Front Of & Behind
# ---------------------------------------------------------------------------
def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "In Front Of & Behind", "Positional Words")

    # ---- EXAMPLE: overlap makes depth unmistakable ----
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 542, 532, 106, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, 624, "Example:")
    # back shape first, front shape overlapping it
    _rect(pdf, 135, 595, 72, 52, GREEN)
    _triangle(pdf, 182, 595, 62, TEAL_S)
    pdf.setFillColor(NAVY)
    x = 280
    for seg, color, bold in [("The triangle is ", NAVY, False),
                             ("in front of", TEAL_DARK, True),
                             (" the rectangle.", NAVY, False)]:
        pdf.setFillColor(color)
        pdf.setFont("Helvetica-Bold" if bold else "Helvetica", 15)
        pdf.drawString(x, 602, seg)
        x += pdf.stringWidth(seg, "Helvetica-Bold" if bold else "Helvetica",
                             15)
    pdf.setFillColor(HexColor("#33465C"))
    pdf.setFont("Helvetica-Oblique", 12.5)
    pdf.drawString(280, 578, "The rectangle is behind the triangle.")

    # ---- PRACTICE A: complete the sentence ----
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 522,
                          "Complete the sentence. Circle the word.")
    rows = [
        # (back, front, subject, landmark, correct)
        ("circle", "square", "circle", "square", "behind"),
        ("triangle", "hexagon", "hexagon", "triangle", "in front of"),
    ]
    for i, (back, front, subj, land, correct) in enumerate(rows):
        top = 506 - i * 108
        fill = HexColor("#F7FAFC") if i % 2 == 0 else HexColor("#FDFBF7")
        border = HexColor("#D5DEE8") if i % 2 == 0 else HexColor("#E3D9C2")
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 100, 532, 100, 12, stroke=1, fill=1)
        cy = top - 50
        draw = {"circle": lambda X: _circle(pdf, X, cy, 25, CORAL),
                "square": lambda X: _square(pdf, X, cy, 52, PURPLE),
                "triangle": lambda X: _triangle(pdf, X, cy, 56, TEAL_S),
                "hexagon": lambda X: _hexagon(pdf, X, cy, 28, AMBER)}
        draw[back](90)
        draw[front](125)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(240, cy + 20,
                       "The %s is ______ the %s." % (subj, land))
        for c, word in enumerate(["in front of", "behind"]):
            px = 250 + c * 165
            pdf.setFillColor(white)
            pdf.setStrokeColor(HexColor("#C9D6E2"))
            pdf.setLineWidth(1.6)
            pdf.roundRect(px, cy - 44, 150, 44, 22, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawCentredString(px + 75, cy - 29, word)

    # ---- PRACTICE B: follow the direction ----
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 278,
                          "Follow the direction. Draw the shape.")
    pdf.setFillColor(HexColor("#F2F7F2"))
    pdf.setStrokeColor(HexColor("#C4DCC4"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 66, 532, 196, 12, stroke=1, fill=1)
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1)
    pdf.line(306, 78, 306, 250)

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(173, 238, "Draw a circle behind the square.")
    _square(pdf, 150, 155, 60, PURPLE)

    pdf.setFillColor(NAVY)
    pdf.drawCentredString(439, 238, "Draw a triangle in front of the rectangle.")
    _rect(pdf, 460, 155, 72, 52, GREEN)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Where Is It? (mixed review)
# ---------------------------------------------------------------------------
def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Where Is It?", "Positional Words")

    # ---- SECTION A: circle the true sentence ----
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 624,
                          "Look at the shapes. Circle the true sentence.")

    items = [
        # (shapes_draw_fn, sentences, correct_idx)
        ("ab1", ["The circle is below the square.",
                 "The circle is above the square."], 1),
        ("ab2", ["The hexagon is beside the circle.",
                 "The hexagon is below the circle."], 0),
        ("ab3", ["The triangle is in front of the rectangle.",
                 "The triangle is behind the rectangle."], 1),
    ]
    for i, (key, sentences, correct) in enumerate(items):
        top = 600 - i * 108
        fill = ["#F7FAFC", "#FDFBF7", "#F7FAFC"][i]
        border = ["#D5DEE8", "#E3D9C2", "#D5DEE8"][i]
        pdf.setFillColor(HexColor(fill))
        pdf.setStrokeColor(HexColor(border))
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 100, 532, 100, 12, stroke=1, fill=1)
        cy = top - 50
        if key == "ab1":
            _circle(pdf, 110, cy + 24, 23, CORAL)
            _square(pdf, 110, cy - 26, 44, PURPLE)
        elif key == "ab2":
            _hexagon(pdf, 100, cy, 27, AMBER)
            _circle(pdf, 165, cy, 25, CORAL)
        else:
            _triangle(pdf, 95, cy, 56, TEAL_S)
            _rect(pdf, 142, cy, 66, 46, GREEN)
        for s, sent in enumerate(sentences):
            sy = cy + 20 - s * 44
            pdf.setFillColor(white)
            pdf.setStrokeColor(HexColor("#C9D6E2"))
            pdf.setLineWidth(1.4)
            pdf.roundRect(215, sy - 17, 340, 36, 18, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica", 13)
            pdf.drawString(235, sy - 5, sent)

    # ---- SECTION B: follow three directions (strongest task) ----
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 264,
                          "Follow the directions. Draw the shapes.")
    pdf.setFillColor(HexColor("#F2F7F2"))
    pdf.setStrokeColor(HexColor("#C4DCC4"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 60, 532, 188, 12, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(60, 228, "1.  Draw a circle above the square.")
    pdf.drawString(60, 210, "2.  Draw a triangle beside the circle.")
    pdf.drawString(60, 192, "3.  Draw a hexagon below the square.")
    _square(pdf, 200, 125, 58, PURPLE)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    ("Above & Below", build_p1_page, True),  # APPROVED 2026-10-08
    ("Beside / Next To", build_p2_page, True),  # APPROVED 2026-10-08
    ("In Front Of & Behind", build_p3_page, True),  # APPROVED 2026-10-08
    ("Where Is It?", build_p4_page, True),  # APPROVED 2026-10-08
]


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "math",
                       "positional-words-k", "positional-words-k-review.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "pwk_tmp_%d.pdf" % i)
        builder(tmp)
        pages.append(tmp)
        print("built page: %s" % title)
    from pypdf import PdfWriter
    writer = PdfWriter()
    for p in pages:
        writer.append(p)
    with open(out, "wb") as f:
        writer.write(f)
    print("merged %d page(s) -> %s" % (len(pages), out))


if __name__ == "__main__":
    main()
