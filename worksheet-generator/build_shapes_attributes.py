#!/usr/bin/env python3
"""Kindergarten Math - Shapes & Their Attributes (Learning Made Simple).

Page 1: What Makes a Triangle? (Learn + Find the Triangles)
US Letter portrait. Vector-drawn shapes for mathematical accuracy.

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
GREEN_CHECK = HexColor("#3FA46A")

# ---------------------------------------------------------------------------
# Canonical logo lockup — VERBATIM copy of generate_worksheet.py::draw_logo,
# the approved Addition Within 5 master. Colors are the master's exact values.
# Do not redraw, rescale internals, or reinterpret. (x, y) is the caller's
# placement only; all internal geometry/spacing is fixed.
# ---------------------------------------------------------------------------
_LOGO_TEAL = HexColor("#007C70")
_LOGO_INK = HexColor("#202A33")
_LOGO_GOLD = HexColor("#F4B63E")


# ---------------------------------------------------------------------------
# Brand header / footer (Learning Made Simple standard)
# ---------------------------------------------------------------------------
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
    # Complete canonical logo lockup (icon + wordmark), as in the approved
    # Addition Within 5 master. Placed at the Shapes header's left slot.
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
# Vector shape helpers
# ---------------------------------------------------------------------------
def _poly(pdf, pts, fill_color, x, y, w=118, h=105):
    p = pdf.beginPath()
    p.moveTo(x + pts[0][0], y + pts[0][1])
    for px, py in pts[1:]:
        p.lineTo(x + px, y + py)
    p.close()
    pdf.setFillColor(fill_color)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.drawPath(p, stroke=1, fill=1)


def _shape_card(pdf, x, y, w=118, h=105):
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, y, w, h, 10, stroke=1, fill=1)


def _check_badge(pdf, cx, cy, r=11):
    pdf.setFillColor(GREEN_CHECK)
    pdf.circle(cx, cy, r, stroke=0, fill=1)
    pdf.setStrokeColor(white)
    pdf.setLineWidth(2.5)
    pdf.setLineCap(1)
    p = pdf.beginPath()
    p.moveTo(cx - 5, cy)
    p.lineTo(cx - 1, cy - 4)
    p.lineTo(cx + 6, cy + 5)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineCap(0)


# ---------------------------------------------------------------------------
# Page 1 -- What Makes a Triangle?
# ---------------------------------------------------------------------------
def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "What Makes a Triangle?", "Shapes & Their Attributes")

    # ---- Section 1: Learn ----
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 614, "Learn")

    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 598 - 170, 532, 170, 12, stroke=1, fill=1)

    # three clearly different triangles
    learn_cards = [(66, 478), (236, 478), (406, 478)]
    learn_shapes = [
        # upright
        ([(70, 85), (20, 15), (120, 15)], HexColor("#3FB6B2")),
        # rotated (pointing right)
        ([(125, 60), (18, 92), (18, 28)], HexColor("#F2765C")),
        # small
        ([(70, 72), (42, 28), (98, 28)], HexColor("#9B7BC8")),
    ]
    for (lx, ly), (pts, color) in zip(learn_cards, learn_shapes):
        _shape_card(pdf, lx, ly, 140, 100)
        _poly(pdf, pts, color, lx, ly)

    # three facts as ONE shared attribute row (applies to all triangles):
    # a single tinted strip, not aligned under individual examples
    pdf.setFillColor(HexColor("#EAF5EC"))
    pdf.setStrokeColor(HexColor("#BFE0C6"))
    pdf.setLineWidth(1.2)
    pdf.roundRect(60, 430, 492, 34, 10, stroke=1, fill=1)
    facts = ["3 straight sides", "3 corners", "closed shape"]
    pdf.setFillColor(HexColor("#2E7D4F"))
    pdf.setFont("Helvetica-Bold", 13)
    for i, fact in enumerate(facts):
        cx = 166 + i * 140
        _check_badge(pdf, cx - 53, 447)
        pdf.drawString(cx - 36, 443, fact)

    # ---- Section 2: Find the Triangles ----
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 396, "Find the Triangles")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 374, "Circle all the triangles.")

    pdf.setFillColor(HexColor("#FDFBF7"))
    pdf.setStrokeColor(HexColor("#E3D9C2"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 358 - 270, 532, 270, 12, stroke=1, fill=1)

    CW, CH = 118, 105
    cols = [53, 183, 313, 443]
    rows = [238, 122]

    def tri_upright(x, y):
        return ([(59, 88), (18, 18), (100, 18)], HexColor("#3FB6B2"))

    def tri_rotated(x, y):
        return ([(100, 52), (20, 88), (20, 16)], HexColor("#F2994A"))

    def tri_small_tilted(x, y):
        return ([(30, 80), (90, 66), (56, 26)], HexColor("#9B7BC8"))

    def tri_tall(x, y):
        return ([(59, 94), (36, 14), (82, 14)], HexColor("#7BC96F"))

    def open_three_sided(x, y):
        # polyline with a visible gap: NOT a closed triangle
        p = pdf.beginPath()
        p.moveTo(x + 24, y + 24)
        p.lineTo(x + 59, y + 88)
        p.lineTo(x + 96, y + 30)
        pdf.setStrokeColor(HexColor("#E86A5E"))
        pdf.setLineWidth(5)
        pdf.setLineCap(1)
        pdf.drawPath(p, stroke=1, fill=0)
        pdf.setLineCap(0)

    def quad(x, y):
        return ([(25, 24), (93, 24), (80, 82), (38, 82)], HexColor("#6FA8DC"))

    def curved_side(x, y):
        # triangle with one side bulging outward (curved)
        p = pdf.beginPath()
        p.moveTo(x + 24, y + 24)
        p.lineTo(x + 59, y + 88)
        p.curveTo(x + 95, y + 80, x + 105, y + 55, x + 94, y + 24)
        p.close()
        pdf.setFillColor(HexColor("#F2A4B8"))
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.drawPath(p, stroke=1, fill=1)

    def pentagon(x, y):
        pts = []
        for k in range(5):
            ang = math.radians(90 + k * 72)
            pts.append((59 + 40 * math.cos(ang), 54 + 40 * math.sin(ang)))
        return (pts, HexColor("#F2C14E"))

    # mixed 2x4 arrangement: T, quad, T, open / curved, T, pentagon, T
    cells = [
        ("tri", tri_upright), ("poly", quad),
        ("tri", tri_small_tilted), ("open", open_three_sided),
        ("curved", curved_side), ("tri", tri_rotated),
        ("poly", pentagon), ("tri", tri_tall),
    ]
    for i, (kind, fn) in enumerate(cells):
        col, row = i % 4, i // 4
        x, y = cols[col], rows[row]
        _shape_card(pdf, x, y, CW, CH)
        if kind in ("tri", "poly"):
            pts, color = fn(x, y)
            _poly(pdf, pts, color, x, y)
        else:
            fn(x, y)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Which Shapes Belong?
# Section 1: Find the Squares (3 true squares varied + rectangle, rhombus,
#   irregular-quad distractors).
# Section 2: Find the Rectangles (3 elongated rectangles + trapezoid,
#   parallelogram, pentagon distractors).
# ---------------------------------------------------------------------------
def _rot_rect_pts(cx, cy, w, h, angle_deg):
    a = math.radians(angle_deg)
    ca, sa = math.cos(a), math.sin(a)
    pts = []
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        dx, dy = sx * w / 2, sy * h / 2
        pts.append((cx + dx * ca - dy * sa, cy + dx * sa + dy * ca))
    return pts


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Which Shapes Belong?", "Shapes & Their Attributes")

    CW2, CH2 = 148, 96
    cols = [68, 232, 396]

    # ---- Section 1: Find the Squares ----
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 628, "Find the Squares")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 606, "Circle all the squares.")
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 590 - 240, 532, 240, 12, stroke=1, fill=1)

    def sq_rows(y0):
        return [y0, y0 - 108]

    s1_shapes = []
    # true squares: axis-aligned, rotated 45deg (diamond, still a square),
    # small rotated 15deg
    s1_shapes.append(("sq", [(46, 20), (102, 20), (102, 76), (46, 76)],
                       HexColor("#3FB6B2")))
    s1_shapes.append(("diamond-not-square",
                       [(74, 90), (100, 48), (74, 6), (48, 48)],
                       HexColor("#F2C14E")))
    s1_shapes.append(("sq15", "rot15sq", HexColor("#9B7BC8")))
    s1_shapes.append(("rect", [(34, 28), (114, 28), (114, 68), (34, 68)],
                       HexColor("#6FA8DC")))
    s1_shapes.append(("sq45", "rot45sq", HexColor("#F2765C")))
    s1_shapes.append(("irregular",
                       [(30, 18), (115, 28), (100, 78), (40, 70)],
                       HexColor("#F2A4B8")))
    # mixed: row1 = square, rhombus, small square / row2 = rectangle,
    # rotated square, irregular quad
    order1 = [0, 1, 2, 3, 4, 5]
    for i, idx in enumerate(order1):
        col, row = i % 3, i // 3
        x, y = cols[col], sq_rows(470)[row]
        _shape_card(pdf, x, y, CW2, CH2)
        kind = s1_shapes[idx][0]
        if kind == "sq45":
            pts = [(74 + 36 * math.cos(math.radians(90 + k * 90)),
                    48 + 36 * math.sin(math.radians(90 + k * 90)))
                   for k in range(4)]
            _poly(pdf, pts, s1_shapes[idx][2], x, y)
        elif kind == "sq15":
            pts = _rot_rect_pts(74, 48, 40, 40, 15)
            _poly(pdf, pts, s1_shapes[idx][2], x, y)
        else:
            _poly(pdf, s1_shapes[idx][1], s1_shapes[idx][2], x, y)

    # ---- Section 2: Find the Rectangles ----
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 332, "Find the Rectangles")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 310, "Circle all the rectangles.")
    pdf.setFillColor(HexColor("#FDFBF7"))
    pdf.setStrokeColor(HexColor("#E3D9C2"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 294 - 234, 532, 234, 12, stroke=1, fill=1)

    pentagon_pts = [(74 + 40 * math.cos(math.radians(90 + k * 72)),
                     48 + 40 * math.sin(math.radians(90 + k * 72)))
                    for k in range(5)]
    s2_shapes = [
        ("trapezoid", [(30, 22), (118, 22), (100, 74), (48, 74)],
         HexColor("#F2765C")),
        ("rect", [(30, 28), (118, 28), (118, 68), (30, 68)],
         HexColor("#7BC96F")),
        ("parallelogram", [(35, 22), (115, 22), (95, 74), (15, 74)],
         HexColor("#9B7BC8")),
        ("rect-vert", [(54, 8), (94, 8), (94, 88), (54, 88)],
         HexColor("#F2994A")),
        ("pentagon", pentagon_pts, HexColor("#F2C14E")),
        ("rect-tilt", "rot15rect", HexColor("#6FA8DC")),
    ]
    # mixed: row1 = trapezoid, rectangle, parallelogram /
    # row2 = tall rectangle, pentagon, tilted rectangle
    order2 = [0, 1, 2, 3, 4, 5]
    for i, idx in enumerate(order2):
        col, row = i % 3, i // 3
        x, y = cols[col], [178, 70][row]
        _shape_card(pdf, x, y, CW2, CH2)
        kind = s2_shapes[idx][0]
        if kind == "rect-tilt":
            pts = _rot_rect_pts(74, 48, 86, 38, 15)
            _poly(pdf, pts, s2_shapes[idx][2], x, y)
        else:
            _poly(pdf, s2_shapes[idx][1], s2_shapes[idx][2], x, y)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- What Can Change? Three rows: color (triangles), size (squares),
# direction (rectangles). Each row: prompt with Yes/No bubbles (answer: Yes).
# Takeaway box at the bottom.
# ---------------------------------------------------------------------------
def _radio(pdf, cx, cy, label):
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.circle(cx, cy, 10, stroke=1, fill=0)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(cx + 16, cy - 5, label)


def _prompt_row(pdf, cy, text):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    pdf.setFont("Helvetica-Bold", 13.5)
    tw = stringWidth(text, "Helvetica-Bold", 13.5)
    yw = 20 + 16 + stringWidth("Yes", "Helvetica-Bold", 13)
    nw = 20 + 16 + stringWidth("No", "Helvetica-Bold", 13)
    total = tw + 24 + yw + 30 + nw
    x = PAGE_WIDTH / 2 - total / 2
    pdf.setFillColor(NAVY)
    pdf.drawString(x, cy - 5, text)
    x += tw + 24
    _radio(pdf, x + 10, cy, "Yes")
    x += yw + 30
    _radio(pdf, x + 10, cy, "No")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "What Can Change?", "Shapes & Their Attributes")

    rows = [
        {
            "title": "Color Can Change",
            "prompt": "Are they all triangles?",
            "tint": (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
            "shapes": [
                ([(64, 66), (16, 12), (112, 12)], HexColor("#3FB6B2")),
                ([(64, 66), (16, 12), (112, 12)], HexColor("#F2765C")),
                ([(64, 66), (16, 12), (112, 12)], HexColor("#9B7BC8")),
            ],
        },
        {
            "title": "Size Can Change",
            "prompt": "Are they all squares?",
            "tint": (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
            "shapes": [
                ("sq34", HexColor("#3FB6B2")),
                ("sq50", HexColor("#3FB6B2")),
                ("sq64", HexColor("#3FB6B2")),
            ],
        },
        {
            "title": "Direction Can Change",
            "prompt": "Are they all rectangles?",
            "tint": (HexColor("#F2F7F2"), HexColor("#C4DCC4")),
            "shapes": [
                ([(16, 19), (112, 19), (112, 59), (16, 59)],
                 HexColor("#3FB6B2")),
                ([(44, 5), (84, 5), (84, 73), (44, 73)],
                 HexColor("#F2765C")),
                ("rot96x36", HexColor("#9B7BC8")),
            ],
        },
    ]

    tops = [620, 453, 286]
    for (title, prompt, tint, shapes), top in zip(
            [(r["title"], r["prompt"], r["tint"], r["shapes"]) for r in rows],
            tops):
        fill, border = tint
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 155, 532, 155, 12, stroke=1, fill=1)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawString(60, top - 20, title)
        for j, (kind, color) in enumerate(shapes):
            x = 94 + j * 148
            y = top - 110
            _shape_card(pdf, x, y, 128, 78)
            if kind == "sq34":
                s = 34
                _poly(pdf, [(64 - s / 2, 39 - s / 2), (64 + s / 2, 39 - s / 2),
                            (64 + s / 2, 39 + s / 2), (64 - s / 2, 39 + s / 2)],
                      color, x, y)
            elif kind == "sq50":
                s = 50
                _poly(pdf, [(64 - s / 2, 39 - s / 2), (64 + s / 2, 39 - s / 2),
                            (64 + s / 2, 39 + s / 2), (64 - s / 2, 39 + s / 2)],
                      color, x, y)
            elif kind == "sq64":
                s = 64
                _poly(pdf, [(64 - s / 2, 39 - s / 2), (64 + s / 2, 39 - s / 2),
                            (64 + s / 2, 39 + s / 2), (64 - s / 2, 39 + s / 2)],
                      color, x, y)
            elif kind == "rot96x36":
                _poly(pdf, _rot_rect_pts(64, 39, 96, 36, 18), color, x, y)
            else:
                _poly(pdf, kind, color, x, y)
        _prompt_row(pdf, top - 155 + 25, prompt)

    # takeaway box
    pdf.setFillColor(HexColor("#FFF7E0"))
    pdf.setStrokeColor(HexColor("#E8C96A"))
    pdf.setLineWidth(1.6)
    pdf.roundRect(60, 55, 492, 60, 12, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(PAGE_WIDTH / 2, 95,
                          "Color, size, and direction can change.")
    pdf.setFillColor(TEAL)
    pdf.drawCentredString(PAGE_WIDTH / 2, 73, "The shape can stay the same!")

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Build & Draw Shapes. Three drawing activities with attribute
# clue chips and large blank drawing boxes. (1) triangle (2) rectangle
# (3) shape challenge -> square.
# ---------------------------------------------------------------------------
def _chip(pdf, x, y, text):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    pdf.setFont("Helvetica-Bold", 11)
    w = stringWidth(text, "Helvetica-Bold", 11) + 22
    pdf.setFillColor(HexColor("#EFF6F3"))
    pdf.setStrokeColor(HexColor("#9CC3B4"))
    pdf.setLineWidth(1.2)
    pdf.roundRect(x, y, w, 24, 12, stroke=1, fill=1)
    pdf.setFillColor(HexColor("#2E7D4F"))
    pdf.drawCentredString(x + w / 2, y + 8, text)
    return w


def _draw_box(pdf, x, y, w, h):
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.roundRect(x, y, w, h, 10, stroke=1, fill=1)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Build & Draw Shapes", "Shapes & Their Attributes")

    activities = [
        ("TRIANGLE", ["3 sides", "3 corners", "closed"],
         "Draw a closed shape with 3 straight sides and 3 corners."),
        ("RECTANGLE", ["4 sides", "4 corners", "4 square corners", "closed"],
         "Draw a closed shape with 4 straight sides and 4 square corners."),
        ("SHAPE CHALLENGE",
         ["4 straight sides", "4 corners", "all sides the same length"],
         "Draw the shape."),
    ]
    tints = [
        (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
        (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
        (HexColor("#F2F7F2"), HexColor("#C4DCC4")),
    ]
    tops = [636, 444, 252]
    for (label, chips, prompt), (fill, border), top in zip(
            activities, tints, tops):
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 180, 532, 180, 12, stroke=1, fill=1)
        # header row: label + clue chips
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(60, top - 24, label)
        cx = 60 + 150
        for chip in chips:
            cx += _chip(pdf, cx, top - 32, chip) + 10
        # prompt
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 13)
        pdf.drawString(60, top - 52, prompt)
        # generous drawing box
        _draw_box(pdf, 60, top - 180 + 14, 492, 98)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    ("What Makes a Triangle?", build_p1_page, True),  # APPROVED 2026-10-07
    ("Which Shapes Belong?", build_p2_page, True),  # APPROVED 2026-10-07
    ("What Can Change?", build_p3_page, True),  # APPROVED 2026-10-07
    ("Build & Draw Shapes", build_p4_page, True),  # APPROVED 2026-10-07
]


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "math",
                       "shapes-attributes", "shapes-attributes-review.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "sa_tmp_%d.pdf" % i)
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
