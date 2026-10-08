#!/usr/bin/env python3
"""Kindergarten Math - 2D & 3D Shapes (Learning Made Simple).

Page 1: Flat or Solid? (reference groups + 6 classification questions).
US Letter portrait. Flat shapes drawn truly flat; solid shapes with depth.

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
def _flat_poly(pdf, pts, fill_color):
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(fill_color)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.drawPath(p, stroke=1, fill=1)


def _flat_circle(pdf, cx, cy, r, fill_color):
    pdf.setFillColor(fill_color)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.circle(cx, cy, r, stroke=1, fill=1)


def _shaded_poly(pdf, pts, fill_color, lw=2):
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(fill_color)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(lw)
    pdf.drawPath(p, stroke=1, fill=1)


def _sphere(pdf, cx, cy, r, base, light, dark):
    pdf.setFillColor(base)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.circle(cx, cy, r, stroke=1, fill=1)
    # soft curved shading toward the bottom
    pdf.saveState()
    pdf.setFillColor(dark)
    pdf.setFillAlpha(0.35)
    pdf.ellipse(cx - r * 0.68, cy - r * 0.92,
                cx + r * 0.68, cy - r * 0.12, stroke=0, fill=1)
    pdf.restoreState()
    # soft curved highlight, upper left
    pdf.saveState()
    pdf.setStrokeColor(light)
    pdf.setLineWidth(r * 0.30)
    pdf.setLineCap(1)
    hr = r * 0.60
    pdf.arc(cx - hr, cy - hr, cx + hr, cy + hr, startAng=105, extent=60)
    pdf.setLineCap(0)
    pdf.restoreState()


def _cube_3d(pdf, x, y, s, fill, light, mid):
    d = s * 0.36
    _shaded_poly(pdf, [(x, y + s), (x + d, y + s + d),
                       (x + s + d, y + s + d), (x + s, y + s)], light)
    _shaded_poly(pdf, [(x + s, y), (x + s + d, y + d),
                       (x + s + d, y + s + d), (x + s, y + s)], mid)
    _shaded_poly(pdf, [(x, y), (x + s, y), (x + s, y + s), (x, y + s)], fill)


def _cylinder_3d(pdf, x, y, w, h, fill, dark, light):
    ry = w * 0.22
    pdf.setFillColor(dark)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.ellipse(x, y, x + w, y + 2 * ry, stroke=1, fill=1)
    _shaded_poly(pdf, [(x, y + ry), (x + w, y + ry),
                       (x + w, y + h), (x, y + h)], fill, lw=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.line(x, y + ry, x, y + h)
    pdf.line(x + w, y + ry, x + w, y + h)
    pdf.setFillColor(light)
    pdf.ellipse(x, y + h - ry, x + w, y + h + ry, stroke=1, fill=1)


def _cone_3d(pdf, cx, yb, w, h, fill, dark):
    _shaded_poly(pdf, [(cx - w / 2, yb), (cx + w / 2, yb), (cx, yb + h)],
                 fill)
    ry = w * 0.20
    pdf.setFillColor(dark)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.ellipse(cx - w / 2, yb - ry, cx + w / 2, yb + ry, stroke=1, fill=1)


def _prism_3d(pdf, x, y, w, h, fill, light, mid):
    d = h * 0.45
    _shaded_poly(pdf, [(x, y + h), (x + d, y + h + d),
                       (x + w + d, y + h + d), (x + w, y + h)], light)
    _shaded_poly(pdf, [(x + w, y), (x + w + d, y + d),
                       (x + w + d, y + h + d), (x + w, y + h)], mid)
    _shaded_poly(pdf, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill)


def _radio(pdf, cx, cy, label):
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.circle(cx, cy, 10, stroke=1, fill=0)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(cx + 16, cy - 5, label)


# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
F_TEAL = HexColor("#7FCDCA")
F_CORAL = HexColor("#F5A58C")
F_PURPLE = HexColor("#BBA3DC")
S_TEAL, S_TEAL_LT, S_TEAL_DK = (HexColor("#3FB6B2"), HexColor("#EAF7F6"),
                              HexColor("#1F6B68"))
S_GREEN, S_GREEN_LT, S_GREEN_DK = (HexColor("#7BC96F"), HexColor("#D6EFD3"),
                                   HexColor("#5FB856"))
S_CORAL, S_CORAL_LT, S_CORAL_DK = (HexColor("#F2765C"), HexColor("#FBD9CF"),
                                    HexColor("#E0654B"))
S_PURP, S_PURP_DK = HexColor("#9B7BC8"), HexColor("#7E5FAE")
S_BLUE, S_BLUE_LT, S_BLUE_DK = (HexColor("#5B9BD5"), HexColor("#C4DDF3"),
                                HexColor("#4A86C4"))
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets",
                      "shapes-2d-3d")


# ---------------------------------------------------------------------------
# Page 1 -- Flat or Solid?
# ---------------------------------------------------------------------------
def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Flat or Solid?", "2D & 3D Shapes")

    # ---- REFERENCE GROUPS ----
    for gx, tint in [(40, (HexColor("#F7FAFC"), HexColor("#D5DEE8"))),
                     (316, (HexColor("#FDFBF7"), HexColor("#E3D9C2")))]:
        fill, border = tint
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(gx, 486, 256, 154, 12, stroke=1, fill=1)

    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(60, 618, "FLAT SHAPES")
    pdf.drawString(336, 618, "SOLID SHAPES")

    # flat: circle, triangle, square — truly flat
    _flat_circle(pdf, 100, 567, 27, F_TEAL)
    _flat_poly(pdf, [(143, 540), (197, 540), (170, 594)], F_CORAL)
    _flat_poly(pdf, [(213, 540), (267, 540), (267, 594), (213, 594)],
               F_PURPLE)
    # solid: sphere, cube, cylinder — clear depth
    _sphere(pdf, 376, 567, 27, S_TEAL, S_TEAL_LT, S_TEAL_DK)
    _cube_3d(pdf, 423, 544, 46, S_GREEN, S_GREEN_LT, S_GREEN_DK)
    _cylinder_3d(pdf, 494, 540, 46, 56, S_CORAL, S_CORAL_DK, S_CORAL_LT)

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Oblique", 11.5)
    pdf.drawCentredString(168, 502, "Flat like paper.")
    pdf.drawCentredString(444, 502, "Solid like blocks.")

    # small secondary name labels under each reference shape
    pdf.setFont("Helvetica-Bold", 10.5)
    for lx, name in [(100, "circle"), (170, "triangle"), (240, "square"),
                     (376, "sphere"), (446, "cube"), (517, "cylinder")]:
        pdf.drawCentredString(lx, 518, name)

    # ---- PRACTICE ----
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 464,
                          "Is the shape flat or solid? Circle the answer.")

    items = [
        ("triangle", "flat"), ("sphere", "solid"),
        ("square", "flat"), ("cylinder", "solid"),
        ("circle", "flat"), ("cube", "solid"),
    ]
    tints = [
        (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
        (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
        (HexColor("#F2F7F2"), HexColor("#C4DCC4")),
    ]
    for row in range(3):
        top = 444 - row * 128
        fill, border = tints[row]
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 118, 532, 118, 12, stroke=1, fill=1)
        cy = top - 59
        for col in range(2):
            kind = items[row * 2 + col][0]
            sx = 110 + col * 272
            rx = 200 + col * 272
            if kind == "circle":
                _flat_circle(pdf, sx, cy, 32, F_TEAL)
            elif kind == "triangle":
                _flat_poly(pdf, [(sx - 32, cy - 32), (sx + 32, cy - 32),
                                 (sx, cy + 32)], F_CORAL)
            elif kind == "square":
                _flat_poly(pdf, [(sx - 32, cy - 32), (sx + 32, cy - 32),
                                 (sx + 32, cy + 32), (sx - 32, cy + 32)],
                           F_PURPLE)
            elif kind == "sphere":
                _sphere(pdf, sx, cy, 32, S_TEAL, S_TEAL_LT, S_TEAL_DK)
            elif kind == "cube":
                _cube_3d(pdf, sx - 28, cy - 28, 56, S_GREEN, S_GREEN_LT,
                         S_GREEN_DK)
            elif kind == "cylinder":
                _cylinder_3d(pdf, sx - 26, cy - 32, 52, 64, S_CORAL,
                             S_CORAL_DK, S_CORAL_LT)
            _radio(pdf, rx, cy + 18, "Flat")
            _radio(pdf, rx, cy - 18, "Solid")

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- 3D Shapes Around Us
# ---------------------------------------------------------------------------
def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "3D Shapes Around Us", "2D & 3D Shapes")

    # ---- REFERENCE ROW: five clean geometric shapes with names ----
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 556, 532, 92, 12, stroke=1, fill=1)

    xs = [93, 199.4, 305.8, 412.2, 518.6]
    _sphere(pdf, xs[0], 612, 20, S_TEAL, S_TEAL_LT, S_TEAL_DK)
    _cube_3d(pdf, xs[1] - 17, 595, 34, S_GREEN, S_GREEN_LT, S_GREEN_DK)
    _cylinder_3d(pdf, xs[2] - 16, 592, 32, 40, S_CORAL, S_CORAL_DK,
                 S_CORAL_LT)
    _cone_3d(pdf, xs[3], 592, 36, 40, S_PURP, S_PURP_DK)
    _prism_3d(pdf, xs[4] - 26, 597, 52, 30, S_BLUE, S_BLUE_LT, S_BLUE_DK)

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 10.5)
    for x, name in zip(xs, ["sphere", "cube", "cylinder", "cone",
                            "rectangular prism"]):
        pdf.drawCentredString(x, 570, name)

    # ---- PRACTICE ----
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 534,
                          "What 3D shape is it like? Circle the answer.")

    items = [
        ("obj-ball.jpg", "sphere", "cube"),
        ("obj-block.jpg", "cube", "sphere"),
        ("obj-can.jpg", "cylinder", "sphere"),
        ("obj-partyhat.jpg", "cone", "cylinder"),
        ("obj-box.jpg", "rectangular prism", "cube"),
    ]
    tints = [
        (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
        (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
        (HexColor("#F2F7F2"), HexColor("#C4DCC4")),
        (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
        (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
    ]
    for i, (img, correct, alt) in enumerate(items):
        top = 514 - i * 90
        fill, border = tints[i]
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 84, 532, 84, 12, stroke=1, fill=1)
        cy = top - 42
        pdf.setFillColor(white)
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1)
        pdf.roundRect(60, cy - 40, 80, 80, 10, stroke=1, fill=1)
        pdf.drawImage(os.path.join(ASSETS, img), 64, cy - 36, width=72,
                      height=72, preserveAspectRatio=True, anchor="c",
                      mask="auto")
        _radio(pdf, 210, cy, correct)
        _radio(pdf, 392, cy, alt)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Find the 3D Shapes (centered shape helpers + rotation)
# ---------------------------------------------------------------------------
def _draw_sphere_c(pdf, cx, cy, r):
    _sphere(pdf, cx, cy, r, S_TEAL, S_TEAL_LT, S_TEAL_DK)


def _draw_cube_c(pdf, cx, cy, s):
    d = s * 0.36
    _cube_3d(pdf, cx - (s + d) / 2, cy - (s + d) / 2, s,
             S_GREEN, S_GREEN_LT, S_GREEN_DK)


def _draw_cyl_c(pdf, cx, cy, w, h):
    _cylinder_3d(pdf, cx - w / 2, cy - h / 2, w, h,
                 S_CORAL, S_CORAL_DK, S_CORAL_LT)


def _draw_cone_c(pdf, cx, cy, w, h):
    _cone_3d(pdf, cx, cy - h / 2, w, h, S_PURP, S_PURP_DK)


def _draw_prism_c(pdf, cx, cy, w, h):
    d = h * 0.45
    _prism_3d(pdf, cx - (w + d) / 2, cy - (h + d) / 2, w, h,
              S_BLUE, S_BLUE_LT, S_BLUE_DK)


def _draw_item(pdf, kind, cx, cy, size, angle):
    def body():
        if kind == "cone":
            _draw_cone_c(pdf, cx, cy, 44 * size, 52 * size)
        elif kind == "cylinder":
            _draw_cyl_c(pdf, cx, cy, 34 * size, 46 * size)
        elif kind == "sphere":
            _draw_sphere_c(pdf, cx, cy, 26 * size)
        elif kind == "cube":
            _draw_cube_c(pdf, cx, cy, 40 * size)
        elif kind == "prism":
            _draw_prism_c(pdf, cx, cy, size[0], size[1])
    if angle:
        pdf.saveState()
        pdf.translate(cx, cy)
        pdf.rotate(angle)
        pdf.translate(-cx, -cy)
        body()
        pdf.restoreState()
    else:
        body()


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Find the 3D Shapes", "2D & 3D Shapes")

    sections = [
        ("Find all the cones. Circle them.", [
            ("cone", 0, 0, 1.0, 0), ("sphere", 1, 0, 1.0, 0),
            ("cone", 2, 0, 0.85, 28), ("cube", 0, 1, 1.0, 0),
            ("cylinder", 1, 1, 1.0, 0), ("cone", 2, 1, 1.1, -32),
        ]),
        ("Find all the cylinders. Circle them.", [
            ("cylinder", 0, 0, 1.0, 0), ("cone", 1, 0, 1.0, 0),
            ("cylinder", 2, 0, 0.9, 30), ("sphere", 0, 1, 0.95, 0),
            ("cylinder", 1, 1, 1.05, -28), ("cube", 2, 1, 1.0, 0),
        ]),
        ("Find all the rectangular prisms. Circle them.", [
            ("prism", 0, 0, (72, 26), 0), ("sphere", 1, 0, 1.0, 0),
            ("prism", 2, 0, (54, 30), 24), ("cylinder", 0, 1, 0.95, 0),
            ("prism", 1, 1, (66, 30), -20), ("cone", 2, 1, 0.9, 0),
        ]),
    ]
    tints = [
        (HexColor("#F7FAFC"), HexColor("#D5DEE8")),
        (HexColor("#FDFBF7"), HexColor("#E3D9C2")),
        (HexColor("#F2F7F2"), HexColor("#C4DCC4")),
    ]
    for s, (instruction, items) in enumerate(sections):
        top = 616 - s * 186
        fill, border = tints[s]
        pdf.setFillColor(fill)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 160, 532, 160, 12, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawCentredString(PAGE_WIDTH / 2, top + 12, instruction)
        for kind, col, row, size, angle in items:
            cx = 128.7 + col * 177.3
            cy = top - 40 - row * 80
            _draw_item(pdf, kind, cx, cy, size, angle)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    ("Flat or Solid?", build_p1_page, True),  # APPROVED 2026-10-08
    ("3D Shapes Around Us", build_p2_page, True),  # APPROVED 2026-10-08
    ("Find the 3D Shapes", build_p3_page, True),  # APPROVED 2026-10-08
]


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "math",
                       "shapes-2d-3d", "shapes-2d-3d-review.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "s23d_tmp_%d.pdf" % i)
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
