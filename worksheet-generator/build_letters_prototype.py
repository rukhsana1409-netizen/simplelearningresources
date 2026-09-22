"""Prototype: Learn My Letters A-Z (pages for A, B, C only).

Standalone builder that reuses the Learning Made Simple branding (header,
footer, palette) from generate_worksheet.py. Embeds original illustrations
generated for this prototype; touches no existing worksheet files.
"""

from __future__ import annotations

import glob
import os
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_worksheet import (  # noqa: E402
    BLUE,
    BORDER,
    CORAL,
    GOLD,
    GREEN,
    INK,
    MARGIN,
    MUTED,
    ORANGE,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    PALE_TEAL,
    PURPLE,
    TEAL,
    TEAL_DARK,
    draw_footer,
    draw_header,
)

LIGHT_GOLD = HexColor("#FDF3DC")
LIGHT_CORAL = HexColor("#FCEDEA")
LIGHT_BLUE = HexColor("#E9F3FA")
LIGHT_PURPLE = HexColor("#F0EAF7")

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "letters")

PAGES = [
    {
        "upper": "A",
        "lower": "a",
        "words": [("ant", "Ant"), ("alligator", "Alligator"), ("astronaut", "Astronaut")],
        "find_title": "Find the A's!",
        "find_instruction": "Put a cross on every A.",
        "find_letters": ["A", "b", "C", "a", "B", "A", "c", "a"],
    },
    {
        "upper": "B",
        "lower": "b",
        "words": [("banana", "Banana"), ("bear", "Bear"), ("book", "Book")],
        "find_title": "Find the B's!",
        "find_instruction": "Circle every B.",
        "find_letters": ["B", "a", "C", "b", "A", "B", "c", "b"],
    },
    {
        "upper": "C",
        "lower": "c",
        "words": [("cat", "Cat"), ("cake", "Cake"), ("cloud", "Cloud")],
        "find_title": "Find the C's!",
        "find_instruction": "Draw a box around every C.",
        "find_letters": ["C", "a", "B", "c", "A", "c", "C", "b"],
    },
]

FIND_FILLS = [PALE_TEAL, LIGHT_GOLD, LIGHT_BLUE, LIGHT_CORAL,
              LIGHT_PURPLE, white, PALE_TEAL, LIGHT_GOLD]


def asset_path(stem: str) -> str:
    path = os.path.join(ASSETS, f"{stem}.webp")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No illustration asset for {stem!r}")
    return path


def draw_big_letters(pdf: canvas.Canvas, upper: str, lower: str) -> None:
    """Huge two-tone uppercase + lowercase pair, centered."""
    size = 96
    pdf.setFont("Helvetica-Bold", size)
    upper_text = upper + " "
    w_upper = stringWidth(upper_text, "Helvetica-Bold", size)
    w_lower = stringWidth(lower, "Helvetica-Bold", size)
    start_x = PAGE_WIDTH / 2 - (w_upper + w_lower) / 2
    baseline = 532
    pdf.setFillColor(TEAL_DARK)
    pdf.drawString(start_x, baseline, upper_text)
    pdf.setFillColor(TEAL)
    pdf.drawString(start_x + w_upper, baseline, lower)


def draw_word_row(pdf: canvas.Canvas, page: dict) -> None:
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(MARGIN, 486, f"Words that begin with {page['upper']}")
    box = 155.0
    xs = [MARGIN, MARGIN + 188.5, MARGIN + 377.0]
    img_y = 318.0
    for (stem, label), x in zip(page["words"], xs):
        img = ImageReader(asset_path(f"{page['upper'].lower()}-{stem}"))
        pdf.drawImage(img, x, img_y, width=box, height=box,
                      preserveAspectRatio=True, anchor="c", mask="auto")
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(x + box / 2, 298, label)


def draw_find_activity(pdf: canvas.Canvas, page: dict) -> None:
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(MARGIN, 252, page["find_title"])
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawString(MARGIN, 232, page["find_instruction"])
    letters = page["find_letters"]
    centers_x = [MARGIN + 66.5 + i * 133 for i in range(4)]
    for row in range(2):
        cy = 178 - row * 86
        for col in range(4):
            index = row * 4 + col
            cx = centers_x[col]
            pdf.setFillColor(FIND_FILLS[index % len(FIND_FILLS)])
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(2)
            pdf.circle(cx, cy, 38, fill=1, stroke=1)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 34)
            pdf.drawCentredString(cx, cy - 12, letters[index])


def build(out_path: str) -> None:
    data = {
        "title": "Learn My Letters: ABC",
        "subtitle": "Preschool Reading & Language",
        "template": "letters-prototype",
    }
    pdf = canvas.Canvas(out_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle("Learn My Letters ABC Prototype | Learning Made Simple")
    for page in PAGES:
        draw_header(pdf, data)
        draw_big_letters(pdf, page["upper"], page["lower"])
        draw_word_row(pdf, page)
        draw_find_activity(pdf, page)
        draw_footer(pdf)
        pdf.showPage()
    pdf.save()
    print(f"wrote {out_path}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "learn-my-letters-abc-prototype.pdf",
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build(out)
