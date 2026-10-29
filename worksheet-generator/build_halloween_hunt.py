#!/usr/bin/env python3
"""Halloween Fun & Learning (Preschool & Kindergarten), extra page:
Halloween Alphabet Hunt, A to Z (corrected version).

The hunt grid holds ONLY letters: all 26 uppercase letters exactly
once, in mixed-up order, in rows of 7, 7, 6, 6. The four friendly
Halloween pictures sit OUTSIDE the grid as small decorations in a row
below it. The A-Z checklist at the bottom (A-M, then N-Z) is enlarged:
bigger boxes, bigger letters, bigger checkboxes. The Halloween ABC
matching page is untouched.
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

# Hunt grid rows, top to bottom: 7, 7, 6, 6 = 26 letters.
GRID = [
    ["M", "S", "A", "T", "R", "Z", "K"],
    ["E", "W", "Q", "H", "D", "U", "B"],
    ["X", "L", "O", "F", "J", "N"],
    ["V", "Y", "P", "C", "I", "G"],
]
# Small decorations outside the grid, left to right.
DECORATIONS = ["bat-trim.jpg", "pumpkin-trim.jpg",
               "ghost-trim.jpg", "cat-trim.jpg"]

GRID_LETTERS = [ltr for row in GRID for ltr in row]
assert sorted(GRID_LETTERS) == list(string.ascii_uppercase), \
    f"grid must hold A-Z exactly once, got {sorted(GRID_LETTERS)}"
assert len(GRID_LETTERS) == 26
CHECKLIST = [string.ascii_uppercase[:13], string.ascii_uppercase[13:]]
assert sorted("".join(CHECKLIST)) == list(string.ascii_uppercase)


def build_hunt():
    path = os.path.join(OUT_DIR, "page-alphabet-hunt.pdf")
    pdf = canvas.Canvas(path, pagesize=letter)
    draw_header(pdf, "Halloween Alphabet Hunt", "Preschool & Kindergarten")

    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(60, 625, "Find each letter. Circle it. Check it off.")

    # Hunt grid: letters only. 7 columns max, cells 66x84 on a 70x88 pitch.
    grid_top = 600
    cell_w, cell_h, pitch_x, pitch_y = 66, 84, 70, 88
    full_w = 7 * pitch_x
    for r, row in enumerate(GRID):
        y = grid_top - (r + 1) * pitch_y
        row_x0 = 61 + (full_w - len(row) * pitch_x) / 2
        for c, ltr in enumerate(row):
            x = row_x0 + c * pitch_x
            pdf.setFillColor(TINTS[(r + c) % 3])
            pdf.setStrokeColor(HexColor("#FFFFFF"))
            pdf.setLineWidth(1)
            pdf.roundRect(x, y, cell_w, cell_h, 10, stroke=0, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 42)
            pdf.drawCentredString(x + cell_w / 2, y + 28, ltr)

    # Small Halloween decorations outside the grid, in a centered row.
    deco_size, deco_gap = 52, 40
    deco_y = 184
    deco_total = len(DECORATIONS) * deco_size + \
        (len(DECORATIONS) - 1) * deco_gap
    deco_x0 = (PAGE_WIDTH - deco_total) / 2
    for i, img in enumerate(DECORATIONS):
        x = deco_x0 + i * (deco_size + deco_gap)
        pdf.drawImage(os.path.join(ASSETS, img), x, deco_y,
                      width=deco_size, height=deco_size,
                      preserveAspectRatio=True, mask="auto")

    # Enlarged checklist: A-M, then N-Z. Letter plus a big checkbox
    # side by side in each box.
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(60, 168, "Check off each letter you find:")
    box_w = (PAGE_WIDTH - 120) / 13
    box_h = 40
    for r, letters in enumerate(CHECKLIST):
        y = 116 - r * 44
        for i, ltr in enumerate(letters):
            x = 60 + i * box_w
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(1.5)
            pdf.rect(x, y, box_w, box_h, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawCentredString(x + 11, y + 13, ltr)
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(1.5)
            pdf.rect(x + 22, y + 14, 12, 12, stroke=1, fill=0)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()
    print(f"wrote {path}")
    print(f"grid letters: {len(GRID_LETTERS)} unique, "
          f"checklist letters: {sum(len(r) for r in CHECKLIST)} unique")


if __name__ == "__main__":
    build_hunt()
