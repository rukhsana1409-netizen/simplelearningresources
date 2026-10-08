#!/usr/bin/env python3
"""Kindergarten Math - Building with 3D Shapes (Learning Made Simple).

Page 1: What Shapes Built It? (Example + 3 counting problems).
US Letter portrait. Simple vector 3D shapes (cube, rectangular prism,
cylinder, cone) drawn with front/top/side faces.

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
# 2D helpers
# ---------------------------------------------------------------------------
def _poly(pdf, pts, fill_color, lw=2):
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(fill_color)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(lw)
    pdf.drawPath(p, stroke=1, fill=1)


def _white_card(pdf, x, y, w, h):
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, y, w, h, 10, stroke=1, fill=1)


def _number_box(pdf, x, y, s):
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.setDash(6, 4)
    pdf.roundRect(x, y, s, s, 10, stroke=1, fill=1)
    pdf.setDash()


# ---------------------------------------------------------------------------
# Simple 3D shapes (front/top/side faces). (x, y) = front-bottom-left.
# ---------------------------------------------------------------------------
C_TEAL, C_TEAL_LT, C_TEAL_DK = (HexColor("#3FB6B2"), HexColor("#CDE9E8"),
                                HexColor("#2FA8A4"))
C_GREEN, C_GREEN_LT, C_GREEN_DK = (HexColor("#7BC96F"), HexColor("#D6EFD3"),
                                   HexColor("#5FB856"))
C_PURPLE, C_PURPLE_LT, C_PURPLE_DK = (HexColor("#9B7BC8"),
                                      HexColor("#DED3EF"), HexColor("#8666B3"))
C_CORAL, C_CORAL_LT, C_CORAL_DK = (HexColor("#F2765C"), HexColor("#FBD9CF"),
                                   HexColor("#E0654B"))


def _cube_3d(pdf, x, y, s, fill, light, mid):
    d = s * 0.36
    _poly(pdf, [(x, y + s), (x + d, y + s + d),
                (x + s + d, y + s + d), (x + s, y + s)], light)
    _poly(pdf, [(x + s, y), (x + s + d, y + d),
                (x + s + d, y + s + d), (x + s, y + s)], mid)
    _poly(pdf, [(x, y), (x + s, y), (x + s, y + s), (x, y + s)], fill)


def _prism_3d(pdf, x, y, w, h, fill, light, mid):
    d = min(w, h) * 0.42
    _poly(pdf, [(x, y + h), (x + d, y + h + d),
                (x + w + d, y + h + d), (x + w, y + h)], light)
    _poly(pdf, [(x + w, y), (x + w + d, y + d),
                (x + w + d, y + h + d), (x + w, y + h)], mid)
    _poly(pdf, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill)


def _cylinder_3d(pdf, x, y, w, h, fill, dark, light):
    ry = w * 0.22
    pdf.setFillColor(dark)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.ellipse(x, y, x + w, y + 2 * ry, stroke=1, fill=1)
    _poly(pdf, [(x, y + ry), (x + w, y + ry),
                (x + w, y + h), (x, y + h)], fill, lw=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.line(x, y + ry, x, y + h)
    pdf.line(x + w, y + ry, x + w, y + h)
    pdf.setFillColor(light)
    pdf.ellipse(x, y + h - ry, x + w, y + h + ry, stroke=1, fill=1)


def _cone_3d(pdf, x, y, w, h, fill, dark):
    ry = w * 0.13
    pdf.setFillColor(dark)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.ellipse(x, y, x + w, y + 2 * ry, stroke=1, fill=1)
    _poly(pdf, [(x, y + ry), (x + w, y + ry), (x + w / 2, y + h)], fill, lw=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.line(x, y + ry, x + w / 2, y + h)
    pdf.line(x + w, y + ry, x + w / 2, y + h)


# ---------------------------------------------------------------------------
# Page 1 -- What Shapes Built It?
# ---------------------------------------------------------------------------
def _shape_key(pdf):
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 578, 532, 76, 12, stroke=1, fill=1)
    items = [
        ("cube", lambda px, py: _cube_3d(pdf, px, py, 34, C_TEAL, C_TEAL_LT,
                                         C_TEAL_DK)),
        ("rectangular prism", lambda px, py: _prism_3d(pdf, px, py, 54, 26,
                                                       C_GREEN, C_GREEN_LT,
                                                       C_GREEN_DK)),
        ("cone", lambda px, py: _cone_3d(pdf, px, py, 36, 32, C_CORAL,
                                         C_CORAL_DK)),
    ]
    for (name, draw), cx in zip(items, [129, 306, 483]):
        if name == "cube":
            draw(cx - 23, 606)
        elif name == "rectangular prism":
            draw(cx - 32, 606)
        else:
            draw(cx - 18, 606)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawCentredString(cx, 590, name)


# ---------------------------------------------------------------------------
# Page 1 -- What Shapes Built It?
# Reference row + Example (structure + its separate pieces) + Practice
# (circle the shapes used to build each structure; one distractor per row).
# ---------------------------------------------------------------------------
def _choice_card(pdf, x, y, draw_fn):
    _white_card(pdf, x, y, 84, 74)
    draw_fn(x + 42, y + 8)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "What Shapes Built It?", "Building with 3D Shapes")

    _shape_key(pdf)

    # ---- EXAMPLE ----
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 570, "Example")
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 394, 532, 160, 12, stroke=1, fill=1)
    # stairs: 1 rectangular prism + 2 cubes
    _white_card(pdf, 60, 402, 220, 128)
    _prism_3d(pdf, 85, 404, 150, 26, C_GREEN, C_GREEN_LT, C_GREEN_DK)
    _cube_3d(pdf, 85, 430, 42, C_TEAL, C_TEAL_LT, C_TEAL_DK)
    _cube_3d(pdf, 85, 472, 42, C_PURPLE, C_PURPLE_LT, C_PURPLE_DK)
    # the shape TYPES used
    _prism_3d(pdf, 330, 448, 70, 24, C_GREEN, C_GREEN_LT, C_GREEN_DK)
    _cube_3d(pdf, 448, 448, 36, C_TEAL, C_TEAL_LT, C_TEAL_DK)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(430, 414, "These shapes can build the structure.")

    # ---- PRACTICE ----
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(60, 378, "Practice")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 356,
                          "Look at each structure. "
                          "Circle the shapes used to build it.")

    tints = [
        (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
        (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
        (HexColor("#F2F7F2"), HexColor("#C4DCC4")),
    ]
    problems = [
        {  # house: prism walls + cone roof; distractor: cube
            "structure": lambda top: (
                _prism_3d(pdf, 102, top - 78, 96, 30, C_GREEN, C_GREEN_LT,
                          C_GREEN_DK),
                _cone_3d(pdf, 108, top - 48, 84, 38, C_CORAL, C_CORAL_DK)),
            "choices": [
                lambda cx, by: _prism_3d(pdf, cx - 32, by, 64, 24, C_GREEN,
                                         C_GREEN_LT, C_GREEN_DK),
                lambda cx, by: _cone_3d(pdf, cx - 19, by, 38, 32, C_CORAL,
                                        C_CORAL_DK),
                lambda cx, by: _cube_3d(pdf, cx - 18, by, 36, C_TEAL,
                                        C_TEAL_LT, C_TEAL_DK),
            ],
        },
        {  # table: prism top + 2 cube legs; distractor: cone
            "structure": lambda top: (
                _cube_3d(pdf, 96, top - 78, 30, C_TEAL, C_TEAL_LT,
                         C_TEAL_DK),
                _cube_3d(pdf, 174, top - 78, 30, C_TEAL, C_TEAL_LT,
                         C_TEAL_DK),
                _prism_3d(pdf, 90, top - 48, 120, 24, C_GREEN, C_GREEN_LT,
                          C_GREEN_DK)),
            "choices": [
                lambda cx, by: _cube_3d(pdf, cx - 18, by, 36, C_TEAL,
                                        C_TEAL_LT, C_TEAL_DK),
                lambda cx, by: _prism_3d(pdf, cx - 32, by, 64, 24, C_GREEN,
                                         C_GREEN_LT, C_GREEN_DK),
                lambda cx, by: _cone_3d(pdf, cx - 19, by, 38, 32, C_CORAL,
                                        C_CORAL_DK),
            ],
        },
        {  # tower: cube + cone roof; distractor: rectangular prism
            "structure": lambda top: (
                _cube_3d(pdf, 129, top - 78, 42, C_TEAL, C_TEAL_LT,
                         C_TEAL_DK),
                _cone_3d(pdf, 125, top - 36, 50, 26, C_CORAL, C_CORAL_DK)),
            "choices": [
                lambda cx, by: _cone_3d(pdf, cx - 19, by, 38, 32, C_CORAL,
                                        C_CORAL_DK),
                lambda cx, by: _cube_3d(pdf, cx - 18, by, 36, C_TEAL,
                                        C_TEAL_LT, C_TEAL_DK),
                lambda cx, by: _prism_3d(pdf, cx - 32, by, 64, 24, C_GREEN,
                                         C_GREEN_LT, C_GREEN_DK),
            ],
        },
    ]
    for i, top in enumerate([340, 242, 144]):
        fill, border = tints[i]
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 90, 532, 90, 12, stroke=1, fill=1)
        _white_card(pdf, 60, top - 82, 200, 74)
        problems[i]["structure"](top)
        for j, choice in enumerate(problems[i]["choices"]):
            _choice_card(pdf, 296 + j * 92, top - 82,
                         lambda cx, by, c=choice: c(cx, by))

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Page 2 -- What Shape Is Missing? Complete structure | same structure with
# one piece missing (dashed outline) | 3 shape choices. Circle the missing one.
# ---------------------------------------------------------------------------
def _dashed_poly(pdf, pts):
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.setDash(6, 4)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setDash()


def _dashed_cube(pdf, x, y, s):
    d = s * 0.36
    _dashed_poly(pdf, [(x, y + s), (x + d, y + s + d),
                       (x + s + d, y + s + d), (x + s, y + s)])
    _dashed_poly(pdf, [(x, y), (x + s, y), (x + s, y + s), (x, y + s)])


def _dashed_cone(pdf, x, y, w, h):
    ry = w * 0.13
    _dashed_poly(pdf, [(x, y + ry), (x + w, y + ry), (x + w / 2, y + h)])
    p = pdf.beginPath()
    p.moveTo(x, y + ry)
    p.curveTo(x, y + ry - ry * 1.2, x + w, y + ry - ry * 1.2, x + w, y + ry)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.setDash(6, 4)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setDash()


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "What Shape Is Missing?", "Building with 3D Shapes")

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 612,
                          "Look at the structure. "
                          "What shape is missing? Circle it.")

    tints = [
        (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
        (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
        (HexColor("#F2F7F2"), HexColor("#C4DCC4")),
    ]

    def choice_shapes(kind, cx, by):
        if kind == "cube":
            _cube_3d(pdf, cx - 17, by, 34, C_TEAL, C_TEAL_LT, C_TEAL_DK)
        elif kind == "prism":
            _prism_3d(pdf, cx - 25, by, 46, 22, C_GREEN, C_GREEN_LT,
                      C_GREEN_DK)
        else:
            _cone_3d(pdf, cx - 19, by, 38, 32, C_CORAL, C_CORAL_DK)

    problems = [
        {  # sofa: prism + cube; the cube is missing
            "complete": lambda dx=0: (
                _prism_3d(pdf, 76+dx, 470, 100, 30, C_GREEN, C_GREEN_LT,
                          C_GREEN_DK),
                _cube_3d(pdf, 76+dx, 500, 40, C_TEAL, C_TEAL_LT, C_TEAL_DK)),
            "incomplete": lambda dx=156: (
                _prism_3d(pdf, 76+dx, 470, 100, 30, C_GREEN, C_GREEN_LT,
                          C_GREEN_DK),
                _dashed_cube(pdf, 76+dx, 500, 40)),
            "choices": ["cone", "cube", "prism"],
        },
        {  # house: prism + cone roof; the cone is missing
            "complete": lambda dx=0: (
                _prism_3d(pdf, 78+dx, 308, 96, 30, C_GREEN, C_GREEN_LT,
                          C_GREEN_DK),
                _cone_3d(pdf, 87+dx, 338, 80, 52, C_CORAL, C_CORAL_DK)),
            "incomplete": lambda dx=156: (
                _prism_3d(pdf, 78+dx, 308, 96, 30, C_GREEN, C_GREEN_LT,
                          C_GREEN_DK),
                _dashed_cone(pdf, 87+dx, 338, 80, 52)),
            "choices": ["cone", "cube", "prism"],
        },
        {  # table: prism top + 2 cube legs; one leg is missing
            "complete": lambda dx=0: (
                _cube_3d(pdf, 92+dx, 146, 30, C_TEAL, C_TEAL_LT, C_TEAL_DK),
                _cube_3d(pdf, 162+dx, 146, 30, C_TEAL, C_TEAL_LT, C_TEAL_DK),
                _prism_3d(pdf, 67+dx, 176, 120, 24, C_GREEN, C_GREEN_LT,
                          C_GREEN_DK)),
            "incomplete": lambda dx=156: (
                _cube_3d(pdf, 92+dx, 146, 30, C_TEAL, C_TEAL_LT, C_TEAL_DK),
                _dashed_cube(pdf, 162+dx, 146, 30),
                _prism_3d(pdf, 67+dx, 176, 120, 24, C_GREEN, C_GREEN_LT,
                          C_GREEN_DK)),
            "choices": ["prism", "cone", "cube"],
        },
    ]
    for i, top in enumerate([592, 430, 268]):
        fill, border = tints[i]
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 150, 532, 150, 12, stroke=1, fill=1)
        _white_card(pdf, 56, top - 130, 140, 110)
        _white_card(pdf, 212, top - 130, 140, 110)
        problems[i]["complete"]()
        problems[i]["incomplete"]()
        for j, kind in enumerate(problems[i]["choices"]):
            cx0 = 370 + j * 68
            _white_card(pdf, cx0, top - 121, 62, 74)
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(cx0 + 9, top - 60, "ABC"[j])
            choice_shapes(kind, cx0 + 31, top - 111)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    ("What Shapes Built It?", build_p1_page, True),  # APPROVED 2026-10-07
    ("What Shape Is Missing?", build_p2_page, True),  # APPROVED 2026-10-08
]


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "math",
                       "building-3d-shapes", "building-3d-shapes-review.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "b3d_tmp_%d.pdf" % i)
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
