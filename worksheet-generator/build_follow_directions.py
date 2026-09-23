"""Follow the Directions (Prototype) — Preschool Communication & Life Skills.

Page 1 (One-Step Directions): 4 spacious rows, each with one very short
one-step instruction and 3 large familiar pictures. Tasks: circle the cat,
cross out the ball, put a line under the apple, circle the big star.

Prototype only: Page 1 for review. Do not extend without approval.
"""

import os

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

PAGE_WIDTH, PAGE_HEIGHT = 612, 792
TITLE = "Follow the Directions"

TEAL = HexColor("#0E7C7B")
INK = HexColor("#1F2A37")
RULE = HexColor("#9FD3D1")

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "follow-directions")


def draw_header(pdf, title, subtitle):
    """Roomier header treatment (standard for new worksheets): taller bar
    and extra padding so the logo, title, and subtitle never feel cramped."""
    pdf.setFillColor(TEAL)
    pdf.rect(0, 728, PAGE_WIDTH, 64, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(48, 776, "LEARNING")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(48, 760, "MADE SIMPLE")
    pdf.setStrokeColor(white)
    pdf.setLineWidth(1)
    pdf.line(218, 738, 218, 786)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(234, 770, title)
    pdf.setFont("Helvetica", 10.5)
    pdf.drawString(234, 754, subtitle)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.5)
    pdf.line(36, 714, 576, 714)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(36, 692, "Name:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1)
    pdf.line(82, 690, 360, 690)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(420, 692, "Date:")
    pdf.line(462, 690, 576, 690)


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF4F3"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#0E7C7B"))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(56, 19, "Learning Made Simple")
    pdf.setStrokeColor(HexColor("#9FD3D1"))
    pdf.setLineWidth(1.5)
    pdf.line(200, 10, 200, 34)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(320, 19, "Made with love for little learners.")
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(556, 19, "\u00a9 2026 Learning Made Simple")


def draw_picture(pdf, stem, cx, cy, size, width=None):
    from PIL import Image as PILImage
    path = os.path.join(ASSETS, stem + ".png")
    if width is None:
        w = h = size
    else:
        iw, ih = PILImage.open(path).size
        w, h = width, width * ih / iw
    pdf.drawImage(path, cx - w / 2, cy - h / 2, w, h,
                  preserveAspectRatio=True, mask="auto")


# Pencil row: the long pencil renders at exactly twice the length of the
# short pencil, at identical thickness, so the child compares length only.
PENCIL_WIDTHS = {"fd-long-pencil": 160, "fd-short-pencil": 80}


# Page 1: One-Step Directions. Each row: one short instruction + 3 large
# pictures with clear room for the child to mark.
PAGE1_ROWS = [
    ("Circle the cat.", ["fd-dog", "fd-cat", "fd-bird"]),
    ("Cross out the ball.", ["fd-car", "fd-teddy", "fd-ball"]),
    ("Put a line under the apple.", ["fd-apple", "fd-banana", "fd-orange"]),
    ("Circle the big star.", ["fd-small-star", "fd-big-star", "fd-big-circle"]),
]
PAGE1_YS = [539, 410, 282, 153]


def draw_page1(pdf):
    draw_header(pdf, f"{TITLE}: One-Step Directions",
                "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640, "Follow the directions.")
    for (instruction, stems), cy in zip(PAGE1_ROWS, PAGE1_YS):
        x, w, h = 36, 540, 115
        y = cy - h / 2
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawString(52, cy + 5, instruction)
        for stem, cx in zip(stems, (312, 423, 534)):
            draw_picture(pdf, stem, cx, cy, 82)
    draw_footer(pdf)
    pdf.showPage()


# Page 2 (Listen for the Clue): one-step directions containing one
# describing clue (big/small, long/short, simple colors). 2-3 very
# familiar pictures per row so the answer is immediately understandable.
# This page tests whether the child understands the whole direction.
PAGE2_ROWS = [
    ("Circle the big ball.", ["fd-ball", "fd-small-ball"]),
    ("Cross out the small apple.", ["fd-apple", "fd-small-apple"]),
    ("Put a line under the red flower.",
     ["fd-blue-flower", "fd-yellow-flower", "fd-red-flower"]),
    ("Circle the long pencil.", ["fd-long-pencil", "fd-short-pencil"]),
]
PAGE2_XS = {2: (375, 490), 3: (312, 423, 534)}


def draw_page2(pdf):
    draw_header(pdf, f"{TITLE}: Listen for the Clue",
                "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640, "Listen. Follow the directions.")
    for (instruction, stems), cy in zip(PAGE2_ROWS, PAGE1_YS):
        x, w, h = 36, 540, 115
        y = cy - h / 2
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawString(52, cy + 5, instruction)
        xs = (365, 500) if "pencil" in stems[0] else PAGE2_XS[len(stems)]
        for stem, cx in zip(stems, xs):
            draw_picture(pdf, stem, cx, cy, 82,
                         width=PENCIL_WIDTHS.get(stem))
    draw_footer(pdf)
    pdf.showPage()


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "communication",
        "follow-directions", "follow-directions-prototype.pdf",
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    draw_page2(pdf)
    pdf.save()
    print(f"wrote {out} (2 pages)")


if __name__ == "__main__":
    main()
