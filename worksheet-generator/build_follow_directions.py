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

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
GOLD = HexColor("#F4B63E")
INK = HexColor("#202A33")
RULE = HexColor("#9FD3D1")
BORDER = HexColor("#B9D7D2")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "follow-directions")


def draw_logo(pdf, x, y):
    """Vector-only Learning Made Simple mark and wordmark (established
    brand header, as in Learn My Letters)."""
    pdf.setFillColor(TEAL)
    pdf.circle(x + 18, y + 26, 7, fill=1, stroke=0)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(x + 18, y + 18, x + 18, y + 4)
    pdf.line(x + 18, y + 14, x + 6, y + 5)
    pdf.line(x + 18, y + 14, x + 30, y + 5)
    pdf.setLineWidth(1.3)
    pdf.line(x + 2, y + 4, x + 18, y)
    pdf.line(x + 18, y, x + 34, y + 4)
    pdf.setFillColor(GOLD)
    pdf.circle(x + 18, y + 39, 3.5, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(x + 43, y + 24, "LEARNING")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(x + 43, y + 10, "MADE SIMPLE")


def draw_header(pdf, title, subtitle):
    """Established brand header (Learn My Letters style): teal top strip,
    vector logo + wordmark, divider, two-line teal title, teal rule."""
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, fill=1, stroke=0)
    draw_logo(pdf, MARGIN, PAGE_HEIGHT - 86)
    divider_x = 210
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1)
    pdf.line(divider_x, PAGE_HEIGHT - 46, divider_x, PAGE_HEIGHT - 106)
    title_x = divider_x + 19
    prefix, focus = title.split(": ", 1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(title_x, PAGE_HEIGHT - 67, prefix + ":")
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(title_x, PAGE_HEIGHT - 98, focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11.5)
    pdf.drawString(title_x, PAGE_HEIGHT - 116, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    pdf.line(MARGIN, PAGE_HEIGHT - 131, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 131)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(MARGIN, PAGE_HEIGHT - 160, "Name:")
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.9)
    pdf.line(MARGIN + 37, PAGE_HEIGHT - 163, 315, PAGE_HEIGHT - 163)
    pdf.setFillColor(INK)
    pdf.drawString(430, PAGE_HEIGHT - 160, "Date:")
    pdf.setStrokeColor(BORDER)
    pdf.line(463, PAGE_HEIGHT - 163, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 163)


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
PAGE1_YS = [500, 374, 248, 122]


def draw_page1(pdf):
    draw_header(pdf, f"{TITLE}: One-Step Directions",
                "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 588, "Follow the directions.")
    for (instruction, stems), cy in zip(PAGE1_ROWS, PAGE1_YS):
        x, w, h = 36, 540, 112
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
    pdf.drawCentredString(PAGE_WIDTH / 2, 588, "Listen. Follow the directions.")
    for (instruction, stems), cy in zip(PAGE2_ROWS, PAGE1_YS):
        x, w, h = 36, 540, 112
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
