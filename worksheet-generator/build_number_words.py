#!/usr/bin/env python3
"""Kindergarten Math - Number Words 1-20 (Learning Made Simple).

Supplemental Kindergarten practice (number words are not a direct K.CC
requirement; K.CC.A.3 covers numerals). Recognition before writing;
1-10 before 11-20.

Page 1: Match the Number Words (Numbers 1-10).
US Letter portrait.

Canonical logo: verbatim generate_worksheet.py::draw_logo (Addition Within 5
master). Do not redraw or approximate.

Only Page 1 exists; it is in review (locked=False).
"""
import os

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PAGE_WIDTH, PAGE_HEIGHT = letter  # 612 x 792

_FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "assets", "fonts")
pdfmetrics.registerFont(TTFont("Andika-Bold",
                                os.path.join(_FONTS_DIR, "Andika-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Andika",
                                os.path.join(_FONTS_DIR, "Andika-Regular.ttf")))
WORD_FONT = "Andika-Bold"  # rounded child-friendly print (SIL OFL)

# ---------------------------------------------------------------------------
# Single-stroke tracing letters (cap 725 / x-height 508 / 1000-unit em).
# Drawn as dashed centerline paths: no doubled outlines, clean open
# counters, immediately readable. Letters needed for One..Ten.
# ---------------------------------------------------------------------------
import math as _math


def _arc_pts(cx, cy, rx, ry, a0, a1, n=24):
    return [(cx + rx * _math.cos(_math.radians(a)),
             cy + ry * _math.sin(_math.radians(a)))
            for a in (a0 + (a1 - a0) * i / n for i in range(n + 1))]


def _epts(cx, cy, rx, ry, n=20):
    return [(cx + rx * _math.cos(2 * _math.pi * i / n),
             cy + ry * _math.sin(2 * _math.pi * i / n))
            for i in range(n + 1)]


_TRACE_LETTERS = {
    # each entry: (strokes, advance)
    "O": ([_epts(300, 362, 230, 330)], 600),
    "n": ([[(60, 0), (60, 508)],
           [(60, 508), (150, 500), (240, 440), (300, 340), (320, 200),
            (320, 0)]], 380),
    "e": ([_arc_pts(195, 255, 115, 235, 50, 310), [(110, 255), (345, 255)]],
          380),
    "T": ([[(60, 725), (540, 725)], [(300, 725), (300, 0)]], 600),
    "w": ([[(40, 508), (130, 0), (220, 300), (310, 0), (400, 508)]], 440),
    "o": ([_epts(190, 254, 150, 230)], 380),
    "h": ([[(60, 0), (60, 725)],
           [(60, 380), (170, 370), (260, 300), (310, 180), (320, 0)]],
          380),
    "r": ([[(60, 0), (60, 508)], [(60, 380), (160, 430), (260, 420)]],
          320),
    "F": ([[(80, 0), (80, 725)], [(80, 725), (460, 725)],
           [(80, 420), (380, 420)]], 520),
    "u": ([[(60, 508), (60, 150), (100, 40), (180, 0), (280, 30),
            (320, 150), (320, 508)]], 380),
    "i": ([[(160, 0), (160, 508)], _epts(160, 625, 45, 45)], 320),
    "v": ([[(40, 508), (190, 0), (340, 508)]], 380),
    "S": ([[(420, 600), (300, 700), (150, 660), (90, 540), (150, 430),
            (300, 380), (420, 300), (430, 170), (340, 60), (180, 30),
            (70, 90)]], 500),
    "x": ([[(60, 508), (320, 0)], [(60, 0), (320, 508)]], 380),
    "E": ([[(420, 725), (80, 725), (80, 0), (420, 0)],
           [(80, 362), (340, 362)]], 480),
    "g": ([_epts(190, 220, 150, 200),
           [(335, 300), (345, 120), (310, -40), (230, -130),
            (130, -120)]], 380),
    "N": ([[(60, 0), (60, 725)], [(60, 725), (420, 0)],
           [(420, 0), (420, 725)]], 480),
    "t": ([[(160, 0), (160, 650)], [(60, 480), (260, 480)]], 320),
}


def _trace_word(pdf, x, y, word, font_size):
    s = font_size / 1000.0
    caph, xh = 725 * s, 508 * s
    # one consistent writing-strip width for every row; the traced word
    # stays left-positioned with blank practice space after it
    strip_w = 170
    x0, x1 = x - 10, x + strip_w
    # light, spacious handwriting guides
    pdf.setLineWidth(1)
    pdf.setStrokeColor(HexColor("#C3CDD8"))
    pdf.setDash()
    pdf.line(x0, y + caph, x1, y + caph)
    pdf.setStrokeColor(HexColor("#D5DDE5"))
    pdf.setDash(8, 6)
    pdf.line(x0, y + xh, x1, y + xh)
    pdf.setStrokeColor(HexColor("#C3CDD8"))
    pdf.setDash()
    pdf.line(x0, y, x1, y)
    # clean dashed centerline letters - clearly visible but lighter than print
    pdf.setStrokeColor(HexColor("#4F7396"))
    pdf.setLineWidth(max(1.6, font_size * 0.055))
    pdf.setLineCap(1)
    pdf.setLineJoin(1)
    pdf.setDash(9, 3)
    cx = x
    for ch in word:
        strokes, adv = _TRACE_LETTERS[ch]
        for pts in strokes:
            p = pdf.beginPath()
            p.moveTo(cx + pts[0][0] * s, y + pts[0][1] * s)
            for px, py in pts[1:]:
                p.lineTo(cx + px * s, y + py * s)
            if pts[0] == pts[-1]:
                p.close()
            pdf.drawPath(p, stroke=1, fill=0)
        cx += adv * s
    pdf.setDash()
    pdf.setLineCap(0)
    pdf.setLineJoin(0)

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
# Page 1 -- Number Words (1-10): read + trace
# ---------------------------------------------------------------------------
WORDS_10 = ["One", "Two", "Three", "Four", "Five",
            "Six", "Seven", "Eight", "Nine", "Ten"]


def _print_word(pdf, x, y, word, font_size):
    pdf.setFont(WORD_FONT, font_size)
    pdf.setFillColor(NAVY)
    pdf.drawString(x, y, word)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Number Words", "Numbers 1\u201310")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 628,
                          "Read the number word. Trace it. Write it.")

    for i, word in enumerate(WORDS_10):
        top = 608 - i * 54
        if i % 2 == 1:
            pdf.setFillColor(HexColor("#F7FAFC"))
            pdf.setStrokeColor(HexColor("#F7FAFC"))
            pdf.roundRect(40, top - 54, 532, 54, 10, stroke=0, fill=1)
        cy = top - 27
        pdf.setFillColor(TEAL_DARK)
        pdf.setFont("Helvetica-Bold", 28)
        pdf.drawCentredString(80, cy - 11, str(i + 1))
        _print_word(pdf, 165, cy - 11, word, 30)
        _trace_word(pdf, 400, cy - 15, word, 38)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Which Number Word? (1-10): recognition, no tracing
# ---------------------------------------------------------------------------
P2_ITEMS = [
    (1, ["Two", "One", "Nine"]),
    (3, ["Three", "Six", "One"]),
    (4, ["Seven", "Four", "Two"]),
    (6, ["Four", "Ten", "Six"]),
    (8, ["Six", "Nine", "Eight"]),
    (10, ["Five", "Ten", "Eight"]),
]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Which Number Word?", "Numbers 1\u201310")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 624,
                          "Circle the correct number word.")

    for i, (num, choices) in enumerate(P2_ITEMS):
        top = 600 - i * 86
        if i % 2 == 1:
            pdf.setFillColor(HexColor("#F7FAFC"))
            pdf.setStrokeColor(HexColor("#F7FAFC"))
            pdf.roundRect(40, top - 86, 532, 86, 12, stroke=0, fill=1)
        cy = top - 43
        pdf.setFillColor(TEAL_DARK)
        pdf.setFont("Helvetica-Bold", 34)
        pdf.drawCentredString(85, cy - 13, str(num))
        for c, word in enumerate(choices):
            px = 140 + c * 148
            pdf.setFillColor(white)
            pdf.setStrokeColor(HexColor("#C9D6E2"))
            pdf.setLineWidth(1.6)
            pdf.roundRect(px, cy - 27, 136, 54, 27, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont(WORD_FONT, 20)
            pdf.drawCentredString(px + 68, cy - 8, word)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    ("Number Words", build_p1_page, True),  # APPROVED 2026-10-08
    ("Which Number Word?", build_p2_page, True),  # APPROVED 2026-10-08
]


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "math",
                       "number-words-1-20", "number-words-1-20-review.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "nw_tmp_%d.pdf" % i)
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
