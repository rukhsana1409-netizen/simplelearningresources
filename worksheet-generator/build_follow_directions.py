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
    pdf.drawString(56, 774, "LEARNING")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(56, 762, "MADE SIMPLE")
    pdf.setStrokeColor(white)
    pdf.setLineWidth(1)
    pdf.line(200, 738, 200, 786)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(216, 770, title)
    pdf.setFont("Helvetica", 10.5)
    pdf.drawString(216, 754, subtitle)
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


def draw_picture(pdf, stem, cx, cy, size):
    path = os.path.join(ASSETS, stem + ".png")
    pdf.drawImage(path, cx - size / 2, cy - size / 2, size, size,
                  preserveAspectRatio=True, mask="auto")


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
    pdf.save()
    print(f"wrote {out} (1 page)")


if __name__ == "__main__":
    main()
