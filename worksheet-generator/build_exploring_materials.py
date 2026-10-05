"""Exploring Materials -- Preschool Science & Discovery.

A 5-page pack introducing material properties to preschoolers:
  P1 Meet Material Properties -- teaching: Hard/Soft, Rough/Smooth, Bendy/Stiff
  P2 Hard or Soft?             -- circle the property (8 familiar objects)
  P3 Rough or Smooth?          -- circle the property (8 familiar objects)
  P4 What Can It Do?           -- cut-and-paste: BEND / STRETCH / STAY STIFF
  P5 Choose the Best Material  -- circle the better material for a purpose

Uses assets/exploring-materials/ (new clean 2D illustrations) plus the
approved teddy illustration from living-nonliving. All embeds are JPEG so
the PDF stays pushable.

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
                      "assets", "exploring-materials")
LN_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "assets", "living-nonliving")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "science", "exploring-materials",
                   "exploring-materials.pdf")

PACK_TITLE = "Exploring Materials"


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


def draw_instruction(pdf, text, size=16):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630, text)


# ---------------------------------------------------------------------------
# Shared drawing helpers
# ---------------------------------------------------------------------------
def img(pdf, name, cx, top, w, h=None, src="em"):
    base = {"em": ASSETS, "ln": LN_ASSETS}[src]
    h = h or w
    pdf.drawImage(os.path.join(base, name),
                  cx - w / 2, top - h, width=w, height=h,
                  preserveAspectRatio=True, anchor="c")


def word(pdf, cx, y, text, size=13):
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(cx, y, text)


def paste_slot(pdf, x, top, w, h):
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1.4)
    pdf.setDash(7, 5)
    pdf.roundRect(x, top - h, w, h, 10, stroke=1, fill=0)
    pdf.setDash()


def cut_card(pdf, x, top, w, h, image, label, src="em", img_h=58,
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


def circle_option(pdf, cx, y, text, r=15, size=12):
    """A circle-the-answer option: outline circle with the word beneath."""
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.circle(cx, y, r, stroke=1, fill=0)
    word(pdf, cx, y - r - 17, text, size)


# ---------------------------------------------------------------------------
# Page 1 -- Meet Material Properties (teaching)
# ---------------------------------------------------------------------------
P1_PAIRS = [
    # (word, image, src, fill, border)
    (("HARD", "em-block.jpg", "em"), ("SOFT", "ln-teddy.jpg", "ln"),
     "#EAF1FB", "#8FA0C8"),
    (("ROUGH", "em-sandpaper.jpg", "em"), ("SMOOTH", "em-marble.jpg", "em"),
     "#FEF3E2", "#E0B96A"),
    (("BENDY", "em-rubberband.jpg", "em"), ("STIFF", "em-ruler.jpg", "em"),
     "#E9F7EF", "#7CBF7C"),
]


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Meet Material Properties")
    draw_instruction(pdf, "We can describe things by how they feel and "
                          "what they can do.", size=15)

    tops = (600, 415, 230)
    for (w1, w2, fill, border), top in zip(P1_PAIRS, tops):
        for x, (label, image, src) in zip((44, 316), (w1, w2)):
            pdf.setFillColor(HexColor(fill))
            pdf.setStrokeColor(HexColor(border))
            pdf.setLineWidth(1.6)
            pdf.roundRect(x, top - 170, 252, 170, 14, stroke=1, fill=1)
            word(pdf, x + 126, top - 32, label, 19)
            img(pdf, image, x + 126, top - 52, 128, 105, src=src)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Pages 2 & 3 -- circle the property
# ---------------------------------------------------------------------------
P2_ITEMS = [
    ("em-rock.jpg", "em", "HARD"), ("ln-teddy.jpg", "ln", "SOFT"),
    ("em-spoon.jpg", "em", "HARD"), ("em-pillow.jpg", "em", "SOFT"),
    ("em-block.jpg", "em", "HARD"), ("em-sponge.jpg", "em", "SOFT"),
    ("em-toycar.jpg", "em", "HARD"), ("em-cotton.jpg", "em", "SOFT"),
]

P3_ITEMS = [
    ("em-pinecone.jpg", "em", "ROUGH"), ("em-ball.jpg", "em", "SMOOTH"),
    ("em-bark.jpg", "em", "ROUGH"), ("em-balloon.jpg", "em", "SMOOTH"),
    ("em-rock.jpg", "em", "ROUGH"), ("em-plate.jpg", "em", "SMOOTH"),
    ("em-coconut.jpg", "em", "ROUGH"), ("em-spoon.jpg", "em", "SMOOTH"),
]


def build_choice_page(path, subtitle, instruction, items, opt_a, opt_b,
                      card_w=128, opt_dx=30, circ_r=15, opt_size=12):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, subtitle)
    draw_instruction(pdf, instruction, size=15)

    xs = (106, 239, 372, 505)
    for k, (image, src, _answer) in enumerate(items):
        cx = xs[k % 4]
        top = 600 if k < 4 else 350
        pdf.setFillColor(HexColor("#F7FAFC"))
        pdf.setStrokeColor(HexColor("#D5DEE8"))
        pdf.setLineWidth(1.2)
        pdf.roundRect(cx - card_w / 2, top - 225, card_w, 225, 12,
                      stroke=1, fill=1)
        img(pdf, image, cx, top - 12, 100, 92, src=src)
        circle_option(pdf, cx - opt_dx, top - 162, opt_a,
                      r=circ_r, size=opt_size)
        circle_option(pdf, cx + opt_dx, top - 162, opt_b,
                      r=circ_r, size=opt_size)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def build_p2_page(path):
    build_choice_page(path, "Hard or Soft?",
                      "Look at each picture. Circle HARD or SOFT.",
                      P2_ITEMS, "HARD", "SOFT")


def build_p3_page(path):
    build_choice_page(path, "Rough or Smooth?",
                      "Look at each picture. Circle ROUGH or SMOOTH.",
                      P3_ITEMS, "ROUGH", "SMOOTH",
                      card_w=134, opt_dx=31, circ_r=14, opt_size=13)


# ---------------------------------------------------------------------------
# Page 4 -- What Can It Do? (cut-and-paste sort)
# ---------------------------------------------------------------------------
P4_COLUMNS = [
    ("BEND", "em-scarf.jpg"),
    ("STRETCH", "em-rubberband.jpg"),
    ("STAY STIFF", "em-block.jpg"),
]

# (image, label) in shuffled cut-out order
P4_CARDS = [
    ("em-scarf.jpg", "scarf"),
    ("em-sock.jpg", "sock"),
    ("em-block.jpg", "wooden block"),
    ("em-paper.jpg", "paper"),
    ("em-rubberband.jpg", "rubber band"),
    ("em-spoon.jpg", "spoon"),
]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Can It Do?")
    draw_instruction(pdf, "Cut out the pictures. Paste each where it belongs.",
                     size=15)

    for k, (label, icon) in enumerate(P4_COLUMNS):
        cx = (133, 306, 479)[k]
        img(pdf, icon, cx, 605, 78, 68)
        word(pdf, cx, 508, label, 16)
        for top in (480, 365):
            paste_slot(pdf, cx - 65, top, 130, 100)

    cut_divider(pdf, 185)
    xs = (44, 130, 216, 302, 388, 474)
    for x, (image, label) in zip(xs, P4_CARDS):
        cut_card(pdf, x, 160, 80, 105, image, label,
                 img_h=55, label_size=10.5)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Choose the Best Material
# ---------------------------------------------------------------------------
P5_PROBLEMS = [
    (("Which material is best", "for filling a soft pillow?"),
     ("em-cotton.jpg", "cotton"), ("em-rocks.jpg", "rocks")),
    (("Which material is best", "for making a strong chair?"),
     ("em-board.jpg", "wood"), ("em-paper.jpg", "paper")),
    (("Which material is best", "for keeping rain off?"),
     ("em-plastic.jpg", "plastic"), ("em-paper.jpg", "paper")),
    (("Which material is best", "for drying your hands?"),
     ("em-towel.jpg", "towel"), ("em-rock.jpg", "rock")),
]


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Choose the Best Material")
    draw_instruction(pdf, "Which is the best choice? Circle it.", size=15)

    tops = (596, 464, 332, 200)
    for ((line1, line2), (img_a, lab_a), (img_b, lab_b)), top in zip(
            P5_PROBLEMS, tops):
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(MARGIN, top - 50, line1)
        pdf.drawString(MARGIN, top - 72, line2)
        for cx, image, label in ((360, img_a, lab_a), (505, img_b, lab_b)):
            pdf.setStrokeColor(HexColor("#9CCBC6"))
            pdf.setLineWidth(1.4)
            pdf.setDash(7, 5)
            pdf.circle(cx, top - 62, 54, stroke=1, fill=0)
            pdf.setDash()
            img(pdf, image, cx, top - 22, 88, 80)
            word(pdf, cx, top - 132, label, 14)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    # (title, builder, locked) -- ALL 5 PAGES APPROVED & LOCKED 2026-10-05
    ("Meet Material Properties", build_p1_page, True),
    ("Hard or Soft?", build_p2_page, True),
    ("Rough or Smooth?", build_p3_page, True),
    ("What Can It Do?", build_p4_page, True),
    ("Choose the Best Material", build_p5_page, True),
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="exploring-materials-")
    ordered = []
    for k, (title, builder, locked) in enumerate(PAGES):
        p = os.path.join(tmpdir, f"page-{k + 1}.pdf")
        builder(p)
        ordered.append(p)
        print(f"built page {k + 1}: {title} -> {p}")
    subprocess.run(["pdfunite"] + ordered + [OUT], check=True)
    print(f"merged {len(ordered)} page(s) -> {OUT}")


if __name__ == "__main__":
    main()
