#!/usr/bin/env python3
"""Kindergarten Math - Compose Shapes (Learning Made Simple).

Page 1: Put Shapes Together (TEACH -> TRY).
US Letter portrait. Vector-drawn shapes for mathematical accuracy.

Canonical logo: verbatim generate_worksheet.py::draw_logo (Addition Within 5
master). Do not redraw or approximate.

Only Page 1 exists; it is in review (locked=False).
"""
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
# Shape helpers
# ---------------------------------------------------------------------------
def _filled_poly(pdf, pts, fill_color, lw=2.5):
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(fill_color)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(lw)
    pdf.drawPath(p, stroke=1, fill=1)


def _outline_poly(pdf, pts, lw=2.5):
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(lw)
    pdf.drawPath(p, stroke=1, fill=1)


def _arrow(pdf, x1, x2, cy):
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(3)
    pdf.setLineCap(1)
    pdf.line(x1, cy, x2, cy)
    pdf.line(x2, cy, x2 - 12, cy - 7)
    pdf.line(x2, cy, x2 - 12, cy + 7)
    pdf.setLineCap(0)


def _white_card(pdf, x, y, w, h):
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, y, w, h, 10, stroke=1, fill=1)


# ---------------------------------------------------------------------------
# Page 1 -- Put Shapes Together
# ---------------------------------------------------------------------------
TEAL_SHAPE = HexColor("#3FB6B2")
CORAL = HexColor("#F2765C")
PURPLE = HexColor("#9B7BC8")
GREEN = HexColor("#7BC96F")
TEAL_LT = HexColor("#CDE9E8")
CORAL_LT = HexColor("#FBD9CF")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Put Shapes Together", "Compose Shapes")

    # ---- EXAMPLE ----
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 630, "Example")
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 614 - 120, 532, 120, 12, stroke=1, fill=1)

    # two equal right triangles (legs 78)
    t1 = [(80, 522), (158, 522), (80, 600)]
    t2 = [(190, 522), (268, 522), (190, 600)]
    _filled_poly(pdf, t1, TEAL_SHAPE)
    _filled_poly(pdf, t2, CORAL)
    _arrow(pdf, 292, 330, 561)
    # completed square with visible dividing diagonal (two-tone halves)
    sq = [(350, 522), (428, 522), (428, 600), (350, 600)]
    _filled_poly(pdf, [(350, 522), (428, 522), (350, 600)], TEAL_LT, lw=1)
    _filled_poly(pdf, [(428, 600), (428, 522), (350, 600)], CORAL_LT, lw=1)
    p = pdf.beginPath()
    p.moveTo(*sq[0])
    for pt in sq[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.line(350, 600, 428, 522)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 503, "2 triangles can make a square.")

    # ---- PRACTICE ----
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 470, "Practice")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 454,
                          "Draw a line to show how the shapes fit together.")

    problems = [
        # 2 triangles -> square
        {
            "pieces": [([(70, 0), (132, 0), (70, 62)], TEAL_SHAPE),
                       ([(160, 0), (222, 0), (160, 62)], CORAL)],
            "target": [(0, 0), (62, 0), (62, 62), (0, 62)],
            "tw": 62, "th": 62,
        },
        # 2 squares -> rectangle
        {
            "pieces": [([(70, 0), (132, 0), (132, 62), (70, 62)], GREEN),
                       ([(160, 0), (222, 0), (222, 62), (160, 62)], PURPLE)],
            "target": [(0, 0), (124, 0), (124, 62), (0, 62)],
            "tw": 124, "th": 62,
        },
        # 2 triangles -> larger triangle (two 55-leg right triangles joined
        # along a leg make exactly this isosceles triangle)
        {
            "pieces": [([(70, 0), (125, 0), (70, 55)], TEAL_SHAPE),
                       ([(142, 0), (197, 0), (142, 55)], CORAL)],
            "target": [(-55, 0), (55, 0), (0, 55)],
            "tw": 110, "th": 55,
        },
    ]
    tints = [
        (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
        (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
        (HexColor("#F2F7F2"), HexColor("#C4DCC4")),
    ]
    tops = [438, 308, 178]
    for prob, (fill, border), top in zip(problems, tints, tops):
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 122, 532, 122, 12, stroke=1, fill=1)
        cy = top - 61
        # pieces on the left
        for pts, color in prob["pieces"]:
            shifted = [(x, y + cy - 31) for x, y in pts]
            _filled_poly(pdf, shifted, color)
        _arrow(pdf, 248, 282, cy)
        # target work area on the right (centered on the shape's true bbox)
        _white_card(pdf, 310, top - 112, 222, 100)
        xs = [x for x, y in prob["target"]]
        ys = [y for x, y in prob["target"]]
        tx = 310 + 111 - (min(xs) + max(xs)) / 2
        ty = cy - (min(ys) + max(ys)) / 2
        _outline_poly(pdf, [(tx + x, ty + y) for x, y in prob["target"]])

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Build New Shapes. Example: 4 small squares -> big square.
# Practice: how many small shapes make each big shape? (counting compositions)
# ---------------------------------------------------------------------------
GREEN_LT = HexColor("#D6EFD3")
PURPLE_LT = HexColor("#DED3EF")


def _quad_square(pdf, x, y, s, fills):
    h = s / 2
    _filled_poly(pdf, [(x, y), (x + h, y), (x + h, y + h), (x, y + h)],
                 fills[0], lw=1)
    _filled_poly(pdf, [(x + h, y), (x + s, y), (x + s, y + h), (x + h, y + h)],
                 fills[1], lw=1)
    _filled_poly(pdf, [(x, y + h), (x + h, y + h), (x + h, y + s), (x, y + s)],
                 fills[2], lw=1)
    _filled_poly(pdf, [(x + h, y + h), (x + s, y + h), (x + s, y + s),
                       (x + h, y + s)], fills[3], lw=1)
    p = pdf.beginPath()
    p.moveTo(x, y)
    p.lineTo(x + s, y)
    p.lineTo(x + s, y + s)
    p.lineTo(x, y + s)
    p.close()
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineWidth(2)
    pdf.line(x + h, y, x + h, y + s)
    pdf.line(x, y + h, x + s, y + h)


def _four_triangles(pdf, cx, cy, side, fills):
    import math
    h = side * math.sqrt(3) / 2
    ax, ay = cx - side / 2, cy - h / 2
    bx, by = cx + side / 2, cy - h / 2
    cxp, cyp = cx, cy + h / 2
    mab = ((ax + bx) / 2, (ay + by) / 2)
    mbc = ((bx + cxp) / 2, (by + cyp) / 2)
    mca = ((cxp + ax) / 2, (cyp + ay) / 2)
    for tri, f in zip([[(ax, ay), mab, mca],
                       [mab, (bx, by), mbc],
                       [mca, mbc, (cxp, cyp)],
                       [mab, mbc, mca]], fills):
        _filled_poly(pdf, tri, f, lw=1)
    p = pdf.beginPath()
    p.moveTo(ax, ay)
    p.lineTo(bx, by)
    p.lineTo(cxp, cyp)
    p.close()
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineWidth(2)
    pdf.line(*mab, *mbc)
    pdf.line(*mbc, *mca)
    pdf.line(*mca, *mab)


def _house(pdf, cx, cy, w, sq_fill, roof_fill, outline=True):
    hw = w / 2
    sh = w  # square part height
    rh = w / 2  # roof height
    y0 = cy - (sh + rh) / 2
    _filled_poly(pdf, [(cx - hw, y0), (cx + hw, y0),
                       (cx + hw, y0 + sh), (cx - hw, y0 + sh)], sq_fill, lw=1)
    _filled_poly(pdf, [(cx - hw, y0 + sh), (cx + hw, y0 + sh),
                       (cx, y0 + sh + rh)], roof_fill, lw=1)
    if outline:
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        p = pdf.beginPath()
        p.moveTo(cx - hw, y0)
        p.lineTo(cx + hw, y0)
        p.lineTo(cx + hw, y0 + sh)
        p.lineTo(cx, y0 + sh + rh)
        p.lineTo(cx - hw, y0 + sh)
        p.close()
        pdf.drawPath(p, stroke=1, fill=0)
        pdf.setLineWidth(2)
        pdf.line(cx - hw, y0 + sh, cx + hw, y0 + sh)


def _number_box(pdf, x, y, s):
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.setDash(6, 4)
    pdf.roundRect(x, y, s, s, 10, stroke=1, fill=1)
    pdf.setDash()


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Build New Shapes", "Compose Shapes")

    # ---- EXAMPLE ----
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 630, "Example")
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 494, 532, 120, 12, stroke=1, fill=1)
    for i, col in enumerate([TEAL_SHAPE, CORAL, GREEN, PURPLE]):
        x = 70 + i * 54
        _filled_poly(pdf, [(x, 530), (x + 44, 530),
                           (x + 44, 574), (x, 574)], col)
    _arrow(pdf, 300, 338, 555)
    _quad_square(pdf, 362, 518, 80,
                 [TEAL_LT, CORAL_LT, GREEN_LT, PURPLE_LT])
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 502,
                          "4 small squares can make a big square.")

    # ---- PRACTICE ----
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 470, "Practice")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 448,
                          "How many small shapes make the big shape? "
                          "Write the number.")

    tints = [
        (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
        (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
        (HexColor("#F2F7F2"), HexColor("#C4DCC4")),
    ]
    for i, top in enumerate([434, 306, 178]):
        fill, border = tints[i]
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 120, 532, 120, 12, stroke=1, fill=1)
        cy = top - 60
        _white_card(pdf, 60, top - 110, 260, 100)
        if i == 0:
            # big square from 4 small squares
            _quad_square(pdf, 190 - 46, cy - 46, 92,
                         [TEAL_LT, CORAL_LT, GREEN_LT, PURPLE_LT])
        elif i == 1:
            # big triangle from 4 small triangles
            _four_triangles(pdf, 190, cy, 104,
                            [TEAL_LT, CORAL_LT, GREEN_LT, PURPLE_LT])
        else:
            # house from 1 square + 1 triangle
            _house(pdf, 190, cy, 60, GREEN_LT, CORAL_LT)
        _number_box(pdf, 440, cy - 38, 76)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Choose the Shapes. Circle the set of smaller shapes that can be
# put together to make the target. Correct side randomized per problem.
# ---------------------------------------------------------------------------
def _two_tone_square_triangles(pdf, x, y, s):
    """Square of side s split by a diagonal into two triangle halves."""
    _filled_poly(pdf, [(x, y), (x + s, y), (x, y + s)], TEAL_LT, lw=1)
    _filled_poly(pdf, [(x + s, y + s), (x + s, y), (x, y + s)], CORAL_LT, lw=1)
    p = pdf.beginPath()
    p.moveTo(x, y)
    p.lineTo(x + s, y)
    p.lineTo(x + s, y + s)
    p.lineTo(x, y + s)
    p.close()
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineWidth(2)
    pdf.line(x, y + s, x + s, y)


def _two_tone_rect_squares(pdf, x, y, w, h):
    """Rectangle w x h split into two equal squares."""
    _filled_poly(pdf, [(x, y), (x + w / 2, y),
                       (x + w / 2, y + h), (x, y + h)], TEAL_LT, lw=1)
    _filled_poly(pdf, [(x + w / 2, y), (x + w, y),
                       (x + w, y + h), (x + w / 2, y + h)], CORAL_LT, lw=1)
    p = pdf.beginPath()
    p.moveTo(x, y)
    p.lineTo(x + w, y)
    p.lineTo(x + w, y + h)
    p.lineTo(x, y + h)
    p.close()
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineWidth(2)
    pdf.line(x + w / 2, y, x + w / 2, y + h)


def _two_tone_iso_triangle(pdf, cx, y, base, hgt):
    """Isosceles triangle split by a vertical midline into two right halves."""
    _filled_poly(pdf, [(cx - base / 2, y), (cx, y), (cx, y + hgt)],
                 TEAL_LT, lw=1)
    _filled_poly(pdf, [(cx + base / 2, y), (cx, y), (cx, y + hgt)],
                 CORAL_LT, lw=1)
    p = pdf.beginPath()
    p.moveTo(cx - base / 2, y)
    p.lineTo(cx + base / 2, y)
    p.lineTo(cx, y + hgt)
    p.close()
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineWidth(2)
    pdf.line(cx, y, cx, y + hgt)


def _set_label(pdf, x, y, letter):
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(x, y, letter)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Choose the Shapes", "Compose Shapes")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 612,
                          "Which set can make the big shape? Circle it.")

    tints = [
        (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
        (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
        (HexColor("#F2F7F2"), HexColor("#C4DCC4")),
    ]
    for i, top in enumerate([592, 430, 268]):
        fill, border = tints[i]
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 150, 532, 150, 12, stroke=1, fill=1)
        cy = top - 75
        # target card (left)
        _white_card(pdf, 60, top - 130, 135, 110)
        # answer set cards
        _white_card(pdf, 212, top - 130, 165, 110)
        _white_card(pdf, 392, top - 130, 165, 110)
        _set_label(pdf, 224, top - 44, "A")
        # rows 1 & 3: lift the B label clear of the tall teal triangle
        _set_label(pdf, 404, top - 44 if i == 1 else top - 34, "B")

        if i == 0:
            # target: square
            _outline_poly(pdf, [(127 - 42, cy - 42), (127 + 42, cy - 42),
                                (127 + 42, cy + 42), (127 - 42, cy + 42)])
            # B (right) is correct: 2 matching right triangles, shown
            # separately (join along hypotenuses -> exact square)
            _filled_poly(pdf, [(398.5, cy - 36), (470.5, cy - 36),
                               (398.5, cy + 36)], TEAL_SHAPE)
            _filled_poly(pdf, [(478.5, cy - 36), (550.5, cy - 36),
                               (478.5, cy + 36)], CORAL)
            # A (left) is wrong: triangle + circle cannot make a square
            _filled_poly(pdf, [(250, cy - 30), (310, cy - 30),
                               (250, cy + 30)], PURPLE)
            pdf.setFillColor(GREEN)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(2.5)
            pdf.circle(340, cy, 28, stroke=1, fill=1)
        elif i == 1:
            # target: rectangle
            _outline_poly(pdf, [(67, cy - 30), (187, cy - 30),
                                (187, cy + 30), (67, cy + 30)])
            # A (left) is correct: 2 equal squares, shown separately
            # (side by side -> exact 116x58 rectangle)
            _filled_poly(pdf, [(232.5, cy - 29), (290.5, cy - 29),
                               (290.5, cy + 29), (232.5, cy + 29)], TEAL_SHAPE)
            _filled_poly(pdf, [(298.5, cy - 29), (356.5, cy - 29),
                               (356.5, cy + 29), (298.5, cy + 29)], CORAL)
            # B (right) is wrong: two triangles cannot make this rectangle
            _filled_poly(pdf, [(430, cy - 28), (482, cy - 28),
                               (430, cy + 24)], TEAL_SHAPE)
            _filled_poly(pdf, [(496, cy - 28), (548, cy - 28),
                               (496, cy + 24)], CORAL)
        else:
            # target: larger triangle
            _outline_poly(pdf, [(127 - 62, cy - 31), (127 + 62, cy - 31),
                                (127, cy + 31)])
            # B (right) is correct: the 2 component right triangles, shown
            # separately (join along vertical legs -> exact base-124
            # height-62 target triangle)
            _filled_poly(pdf, [(408.5, cy - 31), (470.5, cy - 31),
                               (408.5, cy + 31)], TEAL_SHAPE)
            _filled_poly(pdf, [(478.5, cy - 31), (540.5, cy - 31),
                               (478.5, cy + 31)], CORAL)
            # A (left) is wrong: two squares cannot make the triangle
            _filled_poly(pdf, [(242, cy - 28), (294, cy - 28),
                               (294, cy + 24), (242, cy + 24)], GREEN)
            _filled_poly(pdf, [(302, cy - 28), (354, cy - 28),
                               (354, cy + 24), (302, cy + 24)], PURPLE)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    ("Put Shapes Together", build_p1_page, True),  # APPROVED 2026-10-07
    ("Build New Shapes", build_p2_page, True),  # APPROVED 2026-10-07
    ("Choose the Shapes", build_p3_page, True),  # APPROVED 2026-10-07
]


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "math",
                       "compose-shapes", "compose-shapes-review.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "cs_tmp_%d.pdf" % i)
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
