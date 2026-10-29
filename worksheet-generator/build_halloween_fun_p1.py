#!/usr/bin/env python3
"""Halloween Fun & Learning (Preschool & Kindergarten), Page 1 draft:
Halloween ABC beginning-sound matching.

Four friendly Halloween pictures (bat, pumpkin, ghost, cat) in the left
column; four big beginning letters (P, C, G, B) in mixed order in the
right column. The child draws a line from each picture to its first
letter. Minimal text, large activity areas, cheerful original art.
No answers printed on the page.
"""
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

from build_phonics_az import draw_header, draw_footer

PAGE_WIDTH, PAGE_HEIGHT = letter
OUT_DIR = os.path.expanduser("~/workspace/your_files/halloween-fun-learning")
ASSETS = os.path.join(OUT_DIR, "assets")

TEAL = HexColor("#1F8A8A")
NAVY = HexColor("#1F3A5F")
GOLD = HexColor("#F4B63E")
FRAME_FILL = HexColor("#FFF4E0")
INK = HexColor("#202A33")

# (picture file, picture word) top to bottom, left column.
PICTURES = [
    ("bat.jpg", "bat"),
    ("pumpkin.jpg", "pumpkin"),
    ("ghost.jpg", "ghost"),
    ("cat.jpg", "cat"),
]
# Letters top to bottom, right column (mixed order, none beside its match).
LETTERS = ["P", "C", "G", "B"]

# Internal answer check: picture word -> its beginning letter.
ANSWERS = {"bat": "B", "pumpkin": "P", "ghost": "G", "cat": "C"}
for _word, _letter in ANSWERS.items():
    assert _letter in LETTERS, f"letter {_letter} missing from tiles"
    assert _word in [w for _, w in PICTURES]
assert len(set(LETTERS)) == 4, "letters must be distinct"


def build_page1():
    path = os.path.join(OUT_DIR, "page-1.pdf")
    pdf = canvas.Canvas(path, pagesize=letter)
    draw_header(pdf, "Halloween ABC", "Preschool & Kindergarten")

    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(60, 625, "Match each picture to its first letter.")

    pic_x, tile_x = 60, 400
    size = 120
    # Row bottoms, top to bottom: 480, 345, 210, 75.
    row_bottoms = [480, 345, 210, 75]
    for (img, _word), y in zip(PICTURES, row_bottoms):
        pdf.setFillColor(FRAME_FILL)
        pdf.setStrokeColor(GOLD)
        pdf.setLineWidth(2)
        pdf.roundRect(pic_x - 6, y - 6, size + 12, size + 12, 12,
                      stroke=1, fill=1)
        pdf.drawImage(os.path.join(ASSETS, img), pic_x, y,
                      width=size, height=size, preserveAspectRatio=True,
                      mask="auto")
    for ltr, y in zip(LETTERS, row_bottoms):
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(TEAL)
        pdf.setLineWidth(2.5)
        pdf.roundRect(tile_x, y, size, size, 12, stroke=1, fill=1)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 72)
        pdf.drawCentredString(tile_x + size / 2, y + 32, ltr)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()
    print(f"wrote {path}")


if __name__ == "__main__":
    build_page1()
