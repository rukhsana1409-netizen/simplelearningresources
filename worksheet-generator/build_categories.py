"""Build the Categories prototype (Pages 1-2).

Preschool Reading & Language - Words & Vocabulary:
- Page 1 (Animals or Food?): two large labeled category areas (ANIMALS
  and FOOD), each holding two pictures with one picture in the wrong
  area. The child circles the ANIMALS wherever they are.
- Page 2 (Odd One Out): 3 simple rows of 4 large familiar pictures.
  Each row has 3 from one obvious category and 1 clearly different.
  The child circles the one that does not belong.

Prototype only: these 2 pages for review. Do not extend without approval.
"""

import os
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_worksheet import (
    INK,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    draw_footer,
    draw_header,
)

TITLE = "Categories"
BASE = os.path.dirname(os.path.abspath(__file__))
ASSET_DIRS = [
    os.path.join(BASE, "assets", "categories"),
    os.path.join(BASE, "assets", "letters"),
]
_CONVERT_DIR = os.path.join("/tmp", "categories_jpg")
_CONVERTED = {}


def asset_path(stem):
    """Resolve an asset stem to a JPEG/PNG path reportlab can read.

    Looks in assets/categories first, then assets/letters.
    """
    if stem in _CONVERTED:
        return _CONVERTED[stem]
    for d in ASSET_DIRS:
        for ext in (".png", ".webp"):
            src = os.path.join(d, stem + ext)
            if not os.path.exists(src):
                continue
            try:
                ImageReader(src)
                _CONVERTED[stem] = src
                return src
            except Exception:
                pass
            from PIL import Image

            os.makedirs(_CONVERT_DIR, exist_ok=True)
            dst = os.path.join(_CONVERT_DIR, stem + ".jpg")
            Image.open(src).convert("RGB").save(dst, "JPEG", quality=92)
            _CONVERTED[stem] = dst
            return dst
    raise FileNotFoundError(f"asset not found: {stem}")


def draw_picture(pdf, stem, cx, cy, maxw, maxh):
    """Draw a picture fitted inside maxw x maxh, centered on cx, cy."""
    img = ImageReader(asset_path(stem))
    iw, ih = img.getSize()
    scale = min(maxw / iw, maxh / ih)
    w, h = iw * scale, ih * scale
    x, y = cx - w / 2, cy - h / 2
    pdf.drawImage(img, x, y, width=w, height=h,
                  preserveAspectRatio=True, anchor="c", mask="auto")
    return x, y, w, h


def draw_category_box(pdf, cx, cy, w, h, label, stems):
    """Draw a large labeled category area holding two pictures side by side."""
    x, y = cx - w / 2, cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, y, w, h, 18, fill=1, stroke=1)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(cx, y + h - 36, label)
    # Two pictures side by side below the label.
    draw_picture(pdf, stems[0], cx - 62, y + h / 2 - 12, 95, 95)
    draw_picture(pdf, stems[1], cx + 62, y + h / 2 - 12, 95, 95)


def draw_instruction(pdf, y, text):
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, y, text)


def draw_page1(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Animals or Food?",
                      "subtitle": "Preschool Reading & Language"})
    draw_instruction(pdf, 575, "Circle the ANIMALS.")
    # Two large category areas; one picture in each area is a mismatch.
    draw_category_box(pdf, 165, 470, 250, 190, "ANIMALS", ["d-dog", "c-apple"])
    draw_category_box(pdf, 447, 470, 250, 190, "FOOD", ["c-banana", "c-cat"])
    # Row 1: Toys / Clothes.
    draw_instruction(pdf, 340, "Circle the TOYS.")
    draw_row(pdf, 275, ["c-ball", "c-shirt", "c-kite", "h-hat"], h=100,
             pic=85)
    # Row 2: Things We Ride / Animals.
    draw_instruction(pdf, 190, "Circle what we RIDE.")
    draw_row(pdf, 125, ["c-car", "c-bird", "c-bus", "c-rabbit"], h=100,
             pic=85)
    draw_footer(pdf)
    pdf.showPage()


def draw_row(pdf, cy, stems, h=130, pic=110):
    """Draw one row: a panel with 4 large pictures."""
    x, w = 36, 540
    y = cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
    for i, stem in enumerate(stems):
        draw_picture(pdf, stem, 121 + i * 122, cy, pic, pic)


def draw_page2(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Odd One Out",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Circle the one that does not belong.",
    )
    draw_row(pdf, 475, ["b-bear", "d-duck", "f-fish", "c-cake"])
    draw_row(pdf, 320, ["f-frog", "c-cookie", "c-pizza", "c-grapes"])
    draw_row(pdf, 165, ["g-goat", "c-icecream", "s-snake", "x-fox"])
    draw_footer(pdf)
    pdf.showPage()


def main():
    out = os.path.join(
        BASE, "..", "worksheets", "preschool", "reading", "letters",
        "categories-prototype.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    draw_page2(pdf)
    pdf.save()
    print(f"wrote {out} (2 pages)")


if __name__ == "__main__":
    main()
