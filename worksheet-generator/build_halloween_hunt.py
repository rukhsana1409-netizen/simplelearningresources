#!/usr/bin/env python3
"""Halloween Fun & Learning (Preschool & Kindergarten), extra page:
Halloween Alphabet Hunt, A to Z.

A 6x5 letter grid holds all 26 uppercase letters exactly once, in
mixed-up order, plus 4 friendly Halloween pictures as decoration.
The child finds and circles each letter, then marks it on the A-Z
checklist at the bottom (A-M, then N-Z). Large letters, spacious
cells, minimal text. The Halloween ABC matching page is untouched.
"""
import os
import string

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

from build_phonics_az import draw_header, draw_footer

PAGE_WIDTH, PAGE_HEIGHT = letter
OUT_DIR = os.path.expanduser("~/workspace/your_files/halloween-fun-learning")
ASSETS = os.path.join(OUT_DIR, "assets")

TEAL = HexColor("#1F8A8A")
NAVY = HexColor("#1F3A5F")
INK = HexColor("#202A33")
TINTS = [HexColor("#FFF1DE"), HexColor("#F0EAF8"), HexColor("#E7F4F2")]

# Grid rows, top to bottom. ("L", letter) or ("P", image file).
GRID = [
    [("L", "M"), ("L", "S"), ("P", "bat-trim.jpg"),
     ("L", "A"), ("L", "T"), ("L", "R")],
    [("L", "Z"), ("L", "K"), ("P", "pumpkin-trim.jpg"),
     ("L", "E"), ("L", "W"), ("L", "Q")],
    [("L", "H"), ("L", "D"), ("L", "U"), ("P", "ghost-trim.jpg"),
     ("L", "B"), ("L", "X")],
    [("L", "L"), ("L", "O"), ("L", "F"), ("L", "J"),
     ("P", "cat-trim.jpg"), ("L", "N")],
    [("L", "V"), ("L", "Y"), ("L", "P"), ("L", "C"),
     ("L", "I"), ("L", "G")],
]

LETTERS = [v for row in GRID for kind, v in row if kind == "L"]
assert sorted(LETTERS) == list(string.ascii_uppercase), \
    f"grid letters must be A-Z exactly once, got {sorted(LETTERS)}"
assert len(LETTERS) == 26


def build_hunt():
    path = os.path.join(OUT_DIR, "page-alphabet-hunt.pdf")
    pdf = canvas.Canvas(path, pagesize=letter)
    draw_header(pdf, "Halloween Alphabet Hunt", "Preschool & Kindergarten")

    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(60, 625, "Find each letter. Circle it. Check it off.")

    # Letter grid: 6 columns x 5 rows, cells 76x80 on an 80x84 pitch.
    grid_x, grid_top = 66, 600
    cell_w, cell_h, pitch_x, pitch_y = 76, 80, 80, 84
    for r, row in enumerate(GRID):
        y = grid_top - (r + 1) * pitch_y
        for c, (kind, val) in enumerate(row):
            x = grid_x + c * pitch_x
            pdf.setFillColor(TINTS[(r + c) % 3])
            pdf.setStrokeColor(HexColor("#FFFFFF"))
            pdf.setLineWidth(1)
            pdf.roundRect(x, y, cell_w, cell_h, 10, stroke=0, fill=1)
            if kind == "L":
                pdf.setFillColor(NAVY)
                pdf.setFont("Helvetica-Bold", 40)
                pdf.drawCentredString(x + cell_w / 2, y + 26, val)
            else:
                pdf.drawImage(os.path.join(ASSETS, val),
                              x + (cell_w - 64) / 2, y + (cell_h - 64) / 2,
                              width=64, height=64, preserveAspectRatio=True,
                              mask="auto")

    # Checklist: A-M, then N-Z, in two rows of 13 boxes.
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(60, 158, "Check off each letter you find:")
    box_w, box_h, pitch = 36, 30, 37
    box_x0 = 72
    for r, letters in enumerate([string.ascii_uppercase[:13],
                                 string.ascii_uppercase[13:]]):
        y = 112 - r * 35
        for i, ltr in enumerate(letters):
            x = box_x0 + i * pitch
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(1.5)
            pdf.roundRect(x, y, box_w, box_h, 6, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawCentredString(x + box_w / 2 - 2, y + 9, ltr)
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(1.2)
            pdf.rect(x + box_w - 12, y + box_h - 12, 9, 9,
                     stroke=1, fill=0)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()
    print(f"wrote {path}")


if __name__ == "__main__":
    build_hunt()
