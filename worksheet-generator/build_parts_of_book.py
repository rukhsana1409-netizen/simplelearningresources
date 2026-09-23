"""Build the Parts of a Book prototype (Pages 1-2).

Preschool Reading & Language - Print Awareness:
- Page 1 (Front and Back): one large book shown from the FRONT and
  from the BACK, side by side. The child circles the FRONT cover and
  draws a box around the BACK cover. Front has the big title; back has
  the blurb box and barcode. Title/blurb/barcode are overlaid crisply
  with reportlab; cover art is AI-generated with blank areas for them.
- Page 2 (Find the Title): one very large book cover with a big title
  and a small author name. The child circles the TITLE - the big name
  of the story.

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

TITLE = "Parts of a Book"
ASSETS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "parts-of-book"
)
_CONVERT_DIR = os.path.join("/tmp", "parts_of_book_jpg")
_CONVERTED = {}
GRAY_LINE = HexColor("#9aa5b1")


def asset_path(stem):
    """Resolve a PNG asset stem to a JPEG/PNG path reportlab can read."""
    src = os.path.join(ASSETS, stem + ".png")
    if src in _CONVERTED:
        return _CONVERTED[src]
    try:
        ImageReader(src)
        _CONVERTED[src] = src
        return src
    except Exception:
        pass
    from PIL import Image

    os.makedirs(_CONVERT_DIR, exist_ok=True)
    dst = os.path.join(_CONVERT_DIR, stem + ".jpg")
    Image.open(src).convert("RGB").save(dst, "JPEG", quality=92)
    _CONVERTED[src] = dst
    return dst


def draw_cover(pdf, stem, cx, cy, maxw, maxh):
    """Draw a book cover fitted inside maxw x maxh, centered on cx, cy.

    Returns the (x, y, w, h) rect actually drawn, for placing overlays.
    """
    img = ImageReader(asset_path(stem))
    iw, ih = img.getSize()
    scale = min(maxw / iw, maxh / ih)
    w, h = iw * scale, ih * scale
    x, y = cx - w / 2, cy - h / 2
    pdf.drawImage(img, x, y, width=w, height=h,
                  preserveAspectRatio=True, anchor="c", mask="auto")
    return x, y, w, h


def draw_part_label(pdf, cx, y, text):
    """Draw one large label (e.g. FRONT COVER) under a book illustration."""
    bw, bh = 210, 58
    x = cx - bw / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, y, bw, bh, 14, fill=1, stroke=1)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(x + bw / 2, y + 20, text)


def draw_blurb_and_barcode(pdf, x, y, w, h):
    """Overlay a white blurb box with gray text lines and a barcode on a
    back cover, positioned relative to the drawn cover rect."""
    # Blurb box: centered, middle of the cover.
    bw, bh = w * 0.72, h * 0.30
    bx, by = x + (w - bw) / 2, y + h * 0.30
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.roundRect(bx, by, bw, bh, 8, fill=1, stroke=1)
    # Fake text lines inside the blurb box.
    pdf.setFillColor(GRAY_LINE)
    pdf.setStrokeColor(GRAY_LINE)
    for i in range(4):
        ly = by + bh - 22 - i * 20
        lw = bw - 36 - (14 if i == 3 else 0)
        pdf.roundRect(bx + 18, ly - 4, lw, 8, 4, fill=1, stroke=0)
    # Barcode box: bottom-right of the cover.
    cw, ch = w * 0.30, h * 0.11
    cx0, cy0 = x + w - cw - w * 0.08, y + h * 0.06
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.rect(cx0, cy0, cw, ch, fill=1, stroke=1)
    pdf.setFillColor(INK)
    bar_widths = [3, 2, 4, 2, 3, 5, 2, 3, 2, 4, 3, 2, 5, 3]
    bx0 = cx0 + 6
    for bw_ in bar_widths:
        if bx0 + bw_ > cx0 + cw - 6:
            break
        pdf.rect(bx0, cy0 + 5, bw_, ch - 10, fill=1, stroke=0)
        bx0 += bw_ + 3


def draw_page1(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Front and Back",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "This is the FRONT cover. This is the BACK cover.",
    )
    # Front cover with its big title.
    fx, fy, fw, fh = draw_cover(pdf, "b-book-front", 170, 330, 220, 330)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(fx + fw / 2, fy + fh - fh * 0.18, "MY DINO BOOK")
    draw_part_label(pdf, 170, 100, "FRONT COVER")
    # Back cover with blurb box and barcode.
    bx, by, bw, bh = draw_cover(pdf, "b-book-back", 442, 330, 220, 330)
    draw_blurb_and_barcode(pdf, bx, by, bw, bh)
    draw_part_label(pdf, 442, 100, "BACK COVER")
    draw_footer(pdf)
    pdf.showPage()


def draw_page2(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Find the Title",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Circle the TITLE. The title is the big name of the story.",
    )
    cx, cy = PAGE_WIDTH / 2, 320
    x, y, w, h = draw_cover(pdf, "b-cover-title", cx, cy, 330, 400)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 26)
    title_y = y + h - h * 0.17
    pdf.drawCentredString(x + w / 2, title_y, "THE HAPPY BEAR")
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(x + w / 2, title_y - 28, "by Anna Lee")
    draw_footer(pdf)
    pdf.showPage()


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "parts-of-book-prototype.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    draw_page2(pdf)
    pdf.save()
    print(f"wrote {out} (2 pages)")


if __name__ == "__main__":
    main()
