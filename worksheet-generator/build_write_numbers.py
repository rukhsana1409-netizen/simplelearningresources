#!/usr/bin/env python3
"""Kindergarten Math - Write Numbers 0-20 (Learning Made Simple).

Page 1: Write Numbers 0-10 (trace -> independent writing).
US Letter portrait. Hand-built single-stroke dashed tracing numerals for
proper numeral-formation practice (K.CC.A.3).

Canonical logo: verbatim generate_worksheet.py::draw_logo (Addition Within 5
master, via build_shapes_attributes.py reference). Do not redraw.

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
# the approved Addition Within 5 master (via build_shapes_attributes.py).
# Do not redraw, rescale internals, or reinterpret.
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


def draw_instruction(pdf, text, y=640, size=15):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(PAGE_WIDTH / 2, y, text)


# ---------------------------------------------------------------------------
# Single-stroke tracing numerals (500 x 700 box, baseline at y=0).
# Drawn as dashed centerline paths: clean, open, immediately readable.
# ---------------------------------------------------------------------------
def _epts(cx, cy, rx, ry, n=28):
    return [(cx + rx * math.cos(2 * math.pi * i / n),
             cy + ry * math.sin(2 * math.pi * i / n))
            for i in range(n + 1)]


def _arc_pts(cx, cy, rx, ry, a0, a1, n=24):
    return [(cx + rx * math.cos(math.radians(a)),
             cy + ry * math.sin(math.radians(a)))
            for a in (a0 + (a1 - a0) * i / n for i in range(n + 1))]


def _bez(p0, p1, p2, p3, n=12):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def _chain(*segs):
    pts = []
    for s in segs:
        pts.extend(s[1:] if pts else s)
    return pts


_TRACE_DIGITS = {
    # each entry: list of strokes; each stroke is a list of (x, y) points
    "0": [_epts(250, 350, 165, 300)],
    "1": [[(170, 540), (250, 700)], [(250, 700), (250, 0)]],
    "2": [_chain(_arc_pts(265, 460, 145, 215, 170, -30, 20),
                   _bez((391, 352), (300, 220), (200, 110), (130, 0), 10)),
          [(130, 0), (430, 0)]],
    "3": [_chain(_bez((150, 560), (200, 670), (300, 700), (380, 630)),
                   _bez((380, 630), (400, 540), (330, 470), (250, 440))),
          _chain(_bez((250, 440), (340, 420), (400, 360), (390, 270)),
                   _bez((390, 270), (370, 180), (280, 130), (180, 150)),
                   _bez((180, 150), (140, 160), (120, 180), (115, 210), 6))],
    "4": [[(340, 700), (150, 430), (450, 430)], [(340, 700), (340, 0)]],
    "5": [[(430, 700), (200, 700), (190, 530)],
          _chain(_bez((190, 530), (190, 460), (270, 435), (340, 400), 8),
                   _bez((340, 400), (405, 360), (400, 260), (345, 195), 10),
                   _bez((345, 195), (285, 135), (195, 140), (150, 205), 8))],
    "6": [_chain(_bez((360, 620), (320, 690), (240, 700), (170, 660), 10),
                   _bez((170, 660), (100, 600), (95, 480), (110, 380), 10),
                   _bez((110, 380), (130, 260), (200, 180), (290, 170), 10),
                   _bez((290, 170), (360, 180), (385, 250), (360, 320), 10),
                   _bez((360, 320), (320, 370), (240, 375), (180, 340), 10))],
    "7": [[(110, 700), (430, 700)], [(430, 700), (230, 0)]],
    "8": [_epts(250, 520, 140, 160), _epts(250, 200, 165, 185)],
    "9": [_epts(250, 490, 155, 180), [(400, 640), (400, 0)]],
}
_DIGIT_ADV = 460  # advance per digit, in box units


def _trace_number(pdf, tx, baseline_y, text, height_px):
    """Draw dashed tracing numeral(s) with baseline at baseline_y."""
    s = height_px / 700.0
    pdf.setStrokeColor(HexColor("#4F7396"))
    pdf.setLineWidth(max(1.6, height_px * 0.055))
    pdf.setLineCap(1)
    pdf.setLineJoin(1)
    pdf.setDash(9, 3)
    cx = tx
    for ch in text:
        for pts in _TRACE_DIGITS[ch]:
            p = pdf.beginPath()
            p.moveTo(cx + pts[0][0] * s, baseline_y + pts[0][1] * s)
            for px, py in pts[1:]:
                p.lineTo(cx + px * s, baseline_y + py * s)
            if pts[0] == pts[-1]:
                p.close()
            pdf.drawPath(p, stroke=1, fill=0)
        cx += _DIGIT_ADV * s
    pdf.setDash()
    pdf.setLineCap(0)
    pdf.setLineJoin(0)
    return cx - tx  # width drawn


def _guide_strip(pdf, x0, x1, top, h):
    """Three-line handwriting guide: solid top, dashed middle, solid base."""
    base = top - h
    mid = top - h / 2
    pdf.setLineWidth(1)
    pdf.setStrokeColor(HexColor("#C3CDD8"))
    pdf.setDash()
    pdf.line(x0, top, x1, top)
    pdf.line(x0, base, x1, base)
    pdf.setStrokeColor(HexColor("#D5DDE5"))
    pdf.setDash(8, 6)
    pdf.line(x0, mid, x1, mid)
    pdf.setDash()
    return base


# ---------------------------------------------------------------------------
# Page 1 -- Write Numbers 0-10: model -> trace -> independent writing
# ---------------------------------------------------------------------------
P1_NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Write Numbers 0-20", "Write Numbers 0-10")
    draw_instruction(pdf, "Trace the number. Then write it yourself.")

    row_h = 48
    digit_h = 40
    x0, x1 = 40, 572
    for i, num in enumerate(P1_NUMBERS):
        top = 600 - i * row_h
        base = _guide_strip(pdf, x0, x1, top - 4, digit_h + 4)
        # model numeral (solid print), sized to match the tracing numeral
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 42)
        pdf.drawString(58, base, num)
        # dashed tracing numeral
        w = _trace_number(pdf, 150, base, num, digit_h)
        # small "trace" cue arrow? no - keep clean; blank writing space follows

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Write Numbers 11-20: model -> trace -> independent writing
# ---------------------------------------------------------------------------
P2_NUMBERS = ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Write Numbers 0-20", "Write Numbers 11-20")
    draw_instruction(pdf, "Trace the number. Then write it yourself.")

    row_h = 53
    digit_h = 40
    x0, x1 = 40, 572
    for i, num in enumerate(P2_NUMBERS):
        top = 600 - i * row_h
        base = _guide_strip(pdf, x0, x1, top - 4, digit_h + 4)
        # model numeral (solid print), sized to match the tracing numeral
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 42)
        pdf.drawString(58, base, num)
        # dashed tracing numeral
        _trace_number(pdf, 150, base, num, digit_h)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Missing Numbers 0-20: independent application, no tracing.
# Original design: numbers 0-20 as tiles along a gentle snake path;
# given tiles are filled, blank tiles have handwriting guides for the child
# to write the missing numeral independently.
# ---------------------------------------------------------------------------
P3_BLANKS = {1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 19}  # 11 blanks, balanced


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Write Numbers 0-20", "Missing Numbers 0-20")
    draw_instruction(pdf, "Write the missing numbers.")

    tw, th = 66, 78
    gap = (532 - 7 * tw) / 6.0
    rows_y = (520, 360, 200)  # tile-center y for rows 1..3

    def tile_center(num):
        if num <= 6:
            r, c = 0, num
        elif num <= 13:
            r, c = 1, num - 7
        else:
            r, c = 2, num - 14
        x = 40 + c * (tw + gap)
        return (x + tw / 2.0, rows_y[r], x, rows_y[r] - th / 2.0)

    # dotted left-to-right connectors within each row (no snake, no verticals)
    pdf.setStrokeColor(HexColor("#C3CDD8"))
    pdf.setLineWidth(1.4)
    pdf.setDash(2, 5)
    pdf.setLineCap(1)
    for start in (0, 7, 14):
        p = pdf.beginPath()
        cx0, cy0, _, _ = tile_center(start)
        p.moveTo(cx0, cy0)
        for num in range(start + 1, start + 7):
            cx, cy, _, _ = tile_center(num)
            p.lineTo(cx, cy)
        pdf.drawPath(p, stroke=1, fill=0)
    pdf.setDash()

    for num in range(21):
        cx, cy, x, y = tile_center(num)
        blank = num in P3_BLANKS
        if blank:
            pdf.setFillColor(white)
            pdf.setStrokeColor(HexColor("#8AA5B8"))
            pdf.setLineWidth(1.4)
            pdf.setDash(5, 4)
        else:
            pdf.setFillColor(HexColor("#EAF2F2"))
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(1.4)
            pdf.setDash()
        pdf.roundRect(x, y, tw, th, 12, stroke=1, fill=1)
        pdf.setDash()
        if blank:
            # mini handwriting guides inside the blank tile
            gx0, gx1 = x + 10, x + tw - 10
            pdf.setLineWidth(1)
            pdf.setStrokeColor(HexColor("#C3CDD8"))
            pdf.line(gx0, cy + 17, gx1, cy + 17)
            pdf.line(gx0, cy - 17, gx1, cy - 17)
            pdf.setStrokeColor(HexColor("#D5DDE5"))
            pdf.setDash(6, 5)
            pdf.line(gx0, cy, gx1, cy)
            pdf.setDash()
        else:
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 38)
            pdf.drawCentredString(cx, cy - 13, str(num))

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    ("Write Numbers 0-10", build_p1_page, True),  # APPROVED 2026-10-08
    ("Write Numbers 11-20", build_p2_page, True),  # APPROVED 2026-10-08
    ("Missing Numbers 0-20", build_p3_page, True),  # APPROVED 2026-10-08
]


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "math",
                       "write-numbers-0-20", "write-numbers-0-20-review.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "wn_tmp_%d.pdf" % i)
        builder(tmp)
        print("built page %d: %s" % (i + 1, title))
        if i == 0:
            import shutil
            shutil.copy(tmp, out)
    print("wrote -> %s" % out)


if __name__ == "__main__":
    main()
