"""Earth & Space -- Preschool Science & Discovery.

A 5-page pack introducing the solar system to preschoolers:
  P1 Meet Our Solar System   -- teaching page: Sun + 8 planets in order
  P2 Planets in Order        -- cut-and-paste the planets in order from Sun
  P3 Which Planet Is It?     -- draw a line: planet to name (5 planets)
  P4 Our Planet Earth        -- cut-and-paste Land/Water/Air/Plants&Animals
  P5 Earth or Space?         -- cut-and-paste sort into EARTH / SPACE

Uses assets/earth-space/ (new clean 2D illustrations) plus approved
illustrations from plant-library (air) and living-nonliving
(tree, fish, house, flower). All embeds are JPEG so the PDF stays pushable.

REVIEW BUILD -- do not lock, finalize, commit or push until user approves.
"""

import os
import subprocess
import tempfile

from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
INK = HexColor("#202A33")
NAVY = HexColor("#1E3A5F")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "earth-space")
LN_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "assets", "living-nonliving")
PLANT_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "assets", "plant-library")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "science", "earth-space",
                   "earth-space.pdf")

SPACE_FILL = "#E8EDF7"
SPACE_BORDER = "#8FA0C8"
SPACE_DARK = HexColor("#3D4E7A")
EARTH_FILL = "#E6F2EA"
EARTH_BORDER = "#7CBF7C"
EARTH_DARK = HexColor("#2E7D32")


# ---------------------------------------------------------------------------
# Brand header / footer / instruction (Learn My Letters style, with the
# corrected title/subtitle breathing room from the Living & Non-Living pack)
# ---------------------------------------------------------------------------
def draw_logo(pdf, x, y):
    pdf.setFillColor(TEAL)
    pdf.circle(x + 18, y + 26, 7, fill=1, stroke=0)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(x + 18, y + 18, x + 18, y + 4)
    pdf.line(x + 18, y + 14, x + 6, y + 5)
    pdf.line(x + 18, y + 14, x + 30, y + 5)
    pdf.setLineWidth(1.3)
    pdf.line(x + 10, y + 8, x + 26, y + 8)
    pdf.setFillColor(HexColor("#F4B63E"))
    pdf.circle(x + 18, y + 38, 4, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(x + 38, y + 30, "LEARNING")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(x + 38, y + 16, "MADE SIMPLE")


def draw_header(pdf, title, subtitle):
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, fill=1, stroke=0)
    draw_logo(pdf, MARGIN, PAGE_HEIGHT - 86)
    divider_x = 210
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1)
    pdf.line(divider_x, PAGE_HEIGHT - 46, divider_x, PAGE_HEIGHT - 106)
    title_x = divider_x + 19
    if ": " in title:
        prefix, focus = title.split(": ", 1)
    else:
        prefix, focus = "", title
    if prefix:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(title_x, PAGE_HEIGHT - 67, prefix + ":")
    pdf.setFillColor(TEAL)
    size = 30
    pdf.setFont("Helvetica-Bold", size)
    max_w = PAGE_WIDTH - MARGIN - title_x
    while pdf.stringWidth(focus, "Helvetica-Bold", size) > max_w and size > 18:
        size -= 1
        pdf.setFont("Helvetica-Bold", size)
    pdf.drawString(title_x, PAGE_HEIGHT - 98, focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(title_x, PAGE_HEIGHT - 122, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    rule_y = PAGE_HEIGHT - 137
    pdf.line(MARGIN, rule_y, PAGE_WIDTH - MARGIN, rule_y)
    return rule_y


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF4F3"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#0E7C7B"))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(MARGIN, 26, "Learning Made Simple")
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1)
    pdf.line(190, 18, 190, 34)
    pdf.setFillColor(HexColor("#0E7C7B"))
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_WIDTH / 2 + 20, 26,
                          "Made with love for little learners.")
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(PAGE_WIDTH - MARGIN, 26,
                        "\u00a9 2026 Learning Made Simple")


def draw_instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630, text)


# ---------------------------------------------------------------------------
# Shared drawing helpers
# ---------------------------------------------------------------------------
def img(pdf, name, cx, top, w, h=None, src="es"):
    base = {"es": ASSETS, "ln": LN_ASSETS, "plant": PLANT_ASSETS}[src]
    h = h or w
    pdf.drawImage(os.path.join(base, name),
                  cx - w / 2, top - h, width=w, height=h,
                  preserveAspectRatio=True, anchor="c")


def planet_label(pdf, cx, y, text, size=13):
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(cx, y, text)


def paste_slot(pdf, x, top, w, h):
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1.4)
    pdf.setDash(7, 5)
    pdf.roundRect(x, top - h, w, h, 10, stroke=1, fill=0)
    pdf.setDash()


def cut_card(pdf, x, top, w, h, image, label, src="es", img_h=58,
             label_size=13):
    pdf.setStrokeColor(HexColor("#8A9BA8"))
    pdf.setLineWidth(1.2)
    pdf.setDash(6, 4)
    pdf.roundRect(x, top - h, w, h, 8, stroke=1, fill=0)
    pdf.setDash()
    img(pdf, image, x + w / 2, top - 6, w - 28, img_h, src=src)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", label_size)
    pdf.drawCentredString(x + w / 2, top - h + 11, label)


def scissors(pdf, x, y, s=9):
    pdf.setStrokeColor(HexColor("#8A9BA8"))
    pdf.setLineWidth(1.6)
    pdf.line(x - s * 1.5, y - s * 0.9, x + s * 0.8, y + s * 0.45)
    pdf.line(x - s * 1.5, y + s * 0.9, x + s * 0.8, y - s * 0.45)
    pdf.circle(x - s * 1.7, y - s * 1.15, s * 0.34, stroke=1, fill=0)
    pdf.circle(x - s * 1.7, y + s * 1.15, s * 0.34, stroke=1, fill=0)


def cut_divider(pdf, y):
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1.2)
    pdf.setDash(8, 5)
    pdf.line(MARGIN + 34, y, PAGE_WIDTH - MARGIN, y)
    pdf.setDash()
    scissors(pdf, MARGIN + 16, y)


PACK_TITLE = "Earth & Space"

# (file, label, src) in order from the Sun
PLANETS = [
    ("es-mercury.jpg", "Mercury", "es"),
    ("es-venus.jpg", "Venus", "es"),
    ("es-earth.jpg", "Earth", "es"),
    ("es-mars.jpg", "Mars", "es"),
    ("es-jupiter.jpg", "Jupiter", "es"),
    ("es-saturn.jpg", "Saturn", "es"),
    ("es-uranus.jpg", "Uranus", "es"),
    ("es-neptune.jpg", "Neptune", "es"),
]


# ---------------------------------------------------------------------------
# Page 1: Meet Our Solar System -- teaching page.
# ---------------------------------------------------------------------------
def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Meet Our Solar System")
    draw_instruction(pdf, "Meet the Sun and the 8 planets!")

    # Sun -- the largest visual
    img(pdf, "es-sun.jpg", 100, 600, 160)
    planet_label(pdf, 100, 425, "Sun", 14)

    # inner planets -- shared bottom line, one label baseline
    inner = [("es-mercury.jpg", "Mercury", 227, 75),
             ("es-venus.jpg", "Venus", 320, 90),
             ("es-earth.jpg", "Earth", 425, 100),
             ("es-mars.jpg", "Mars", 527, 85)]
    for name, label, cx, s in inner:
        img(pdf, name, cx, 505 + s, s)
        planet_label(pdf, cx, 480, label)

    # outer planets -- shared bottom line, one label baseline
    outer = [("es-jupiter.jpg", "Jupiter", 107, 135),
             ("es-saturn.jpg", "Saturn", 260, 155),
             ("es-uranus.jpg", "Uranus", 401, 110),
             ("es-neptune.jpg", "Neptune", 516, 105)]
    for name, label, cx, s in outer:
        img(pdf, name, cx, 220 + s, s)
        planet_label(pdf, cx, 195, label)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2: Planets in Order -- cut-and-paste, Sun already placed.
# ---------------------------------------------------------------------------
# shuffled card order (file, label)
P2_CARDS = [
    ("es-mars.jpg", "Mars"), ("es-neptune.jpg", "Neptune"),
    ("es-venus.jpg", "Venus"), ("es-jupiter.jpg", "Jupiter"),
    ("es-saturn.jpg", "Saturn"), ("es-mercury.jpg", "Mercury"),
    ("es-earth.jpg", "Earth"), ("es-uranus.jpg", "Uranus"),
]
P2_XS = [195, 305, 415, 525]
P2_CARD_XS = [40, 164, 288, 412]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Planets in Order")
    draw_instruction(pdf,
                     "Cut out the planets. Paste them in order from the Sun.")

    # Sun already in place
    img(pdf, "es-sun.jpg", 85, 595, 100)
    planet_label(pdf, 85, 478, "Sun", 14)

    # 8 numbered placement spaces, moving outward from the Sun
    for row, top in enumerate((590, 478)):
        for c, x in enumerate(P2_XS):
            n = row * 4 + c + 1
            pdf.setStrokeColor(HexColor("#9CCBC6"))
            pdf.setLineWidth(1.6)
            pdf.setDash(7, 5)
            pdf.circle(x, top - 44, 44, stroke=1, fill=0)
            pdf.setDash()
            pdf.setFillColor(HexColor("#B9C6D4"))
            pdf.setFont("Helvetica-Bold", 17)
            pdf.drawCentredString(x, top - 50, str(n))

    # cut-out planet cards
    cut_divider(pdf, 365)
    for k, (name, label) in enumerate(P2_CARDS):
        row, col = divmod(k, 4)
        top = 340 if row == 0 else 240
        cut_card(pdf, P2_CARD_XS[col], top, 118, 90, name, label,
                 img_h=60)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3: Which Planet Is It? -- draw a line to the name.
# ---------------------------------------------------------------------------
# left planets (file) vs shuffled right names -- no straight-across matches
P3_PLANETS = ["es-jupiter.jpg", "es-saturn.jpg", "es-earth.jpg",
              "es-mars.jpg", "es-neptune.jpg"]
P3_NAMES = ["Earth", "Neptune", "Jupiter", "Saturn", "Mars"]
P3_TOPS = [600, 502, 404, 306, 208]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Which Planet Is It?")
    draw_instruction(pdf, "Draw a line to match each planet to its name.")
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(1.5)
    pdf.line(306, 90, 306, 612)
    for k, top in enumerate(P3_TOPS):
        img(pdf, P3_PLANETS[k], 150, top, 100)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(460, top - 58, P3_NAMES[k])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4: Our Planet Earth -- cut-and-paste Land/Water/Air/Plants & Animals.
# ---------------------------------------------------------------------------
P4_CARDS = [
    ("es-land.jpg", "Land", "es", 13),
    ("es-water.jpg", "Water", "es", 13),
    ("plant-air.jpg", "Air", "plant", 13),
    ("es-life.jpg", "Plants & Animals", "es", 12),
]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Our Planet Earth")
    draw_instruction(pdf, "Cut out the pictures. Paste them on Earth.")
    # large central Earth
    img(pdf, "es-earth.jpg", 306, 600, 340)
    # 4 paste slots overlaid on the Earth in a symmetric 2x2
    for sx in (169, 313):
        for stop in (567, 437):
            paste_slot(pdf, sx, stop, 130, 130)
    # cut-out cards
    cut_divider(pdf, 185)
    for k, (name, label, src, lsize) in enumerate(P4_CARDS):
        cut_card(pdf, 40 + k * 124, 160, 118, 88, name, label, src=src,
                 img_h=56, label_size=lsize)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5: Earth or Space? -- cut-and-paste sort.
# ---------------------------------------------------------------------------
# (file, label, src, earth?) -- mixed so no pattern emerges
P5_CARDS = [
    ("es-rocket.jpg", "Rocket", "es", False),
    ("es-tree.jpg", "Tree", "es", True),
    ("es-moon.jpg", "Moon", "es", False),
    ("es-fish.jpg", "Fish", "es", True),
    ("es-house.jpg", "House", "es", True),
    ("es-saturn.jpg", "Saturn", "es", False),
    ("es-flower.jpg", "Flower", "es", True),
    ("es-astronaut.jpg", "Astronaut", "es", False),
]
P5_XS = [40, 164, 288, 412]


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Earth or Space?")
    draw_instruction(pdf, "Cut out the pictures. Paste them where they belong.")

    # EARTH sort area
    pdf.setFillColor(HexColor(EARTH_FILL))
    pdf.setStrokeColor(HexColor(EARTH_BORDER))
    pdf.setLineWidth(2.5)
    pdf.roundRect(40, 315, 252, 285, 16, stroke=1, fill=1)
    pdf.setFillColor(EARTH_DARK)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(166, 578, "EARTH")
    for sx in (52, 172):
        for stop in (548, 438):
            paste_slot(pdf, sx, stop, 108, 100)

    # SPACE sort area
    pdf.setFillColor(HexColor(SPACE_FILL))
    pdf.setStrokeColor(HexColor(SPACE_BORDER))
    pdf.setLineWidth(2.5)
    pdf.roundRect(320, 315, 252, 285, 16, stroke=1, fill=1)
    pdf.setFillColor(SPACE_DARK)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(446, 578, "SPACE")
    for sx in (332, 452):
        for stop in (548, 438):
            paste_slot(pdf, sx, stop, 108, 100)

    # cut line + 8 cards
    cut_divider(pdf, 290)
    for k, (name, label, src, _earth) in enumerate(P5_CARDS):
        row, col = divmod(k, 4)
        top = 258 if row == 0 else 156
        cut_card(pdf, P5_XS[col], top, 118, 92, name, label, src=src)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    # (title, builder, locked) -- ALL 5 PAGES APPROVED & LOCKED 2026-10-02
    ("Meet Our Solar System", build_p1_page, True),
    ("Planets in Order", build_p2_page, True),
    ("Which Planet Is It?", build_p3_page, True),
    ("Our Planet Earth", build_p4_page, True),
    ("Earth or Space?", build_p5_page, True),
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="earth-space-")
    ordered = []
    for k, (title, builder, locked) in enumerate(PAGES):
        p = os.path.join(tmpdir, f"page-{k + 1}.pdf")
        builder(p)
        ordered.append(p)
        print(f"built page {k + 1}: {title} -> {p}")
    merged = OUT + ".new"
    subprocess.run(["pdfunite", *ordered, merged], check=True)
    os.replace(merged, OUT)
    print(f"merged {len(ordered)} page(s) -> {OUT}")


if __name__ == "__main__":
    main()
