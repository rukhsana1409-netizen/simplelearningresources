"""Build the Picture & Word Matching prototype (Pages 1-5).

Preschool Reading & Language:
- Page 1 (Match the Word): 5 large colorful familiar pictures on the
  left, their simple words on the right in mixed order. The child draws
  a line from each picture to its word. Pictures: frog, bird, tree,
  flower, cake.
- Page 2 (Circle the Word): 5 different large pictures, each with
  2 simple word choices on the right. The child circles the matching
  word. Pictures: lion, bus, shoe, cookie, kite. Correct side varies.
- Page 3 (Match More Words): 5 NEW picture -> word pairs, same match
  activity. Pictures: monkey, penguin, pizza, ice cream, boat.
- Page 4 (Circle More Words): 5 NEW pictures, each with 2 simple word
  choices. Pictures: horse, octopus, donut, train, umbrella.
  Correct side varies.
- Page 5 (Word Review): 6 NEW pictures with 6 words in mixed order;
  draw lines to match. Pictures: sheep, owl, grapes, sandwich,
  crayon, lamp.

Pages 1-2 approved: do not change them. Pages 3-5 for review.
"""

import os
import sys

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

TITLE = "Picture & Word Matching"
ASSETS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "picture-word"
)
_CONVERT_DIR = os.path.join("/tmp", "picture_word_jpg")
_CONVERTED = {}


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


def draw_picture(pdf, stem, cx, cy, box):
    img = ImageReader(asset_path(stem))
    pdf.drawImage(img, cx - box / 2, cy - box / 2, width=box, height=box,
                  preserveAspectRatio=True, anchor="c", mask="auto")


# Page 1: match picture -> word. Right column shuffled so no pair sits
# across from its picture.
PAGE1_PICS = ["x-frog", "x-bird", "x-tree", "x-flower", "x-cake"]
PAGE1_WORDS = ["TREE", "CAKE", "FROG", "BIRD", "FLOWER"]
PAGE1_YS = [500, 405, 310, 215, 120]
PAGE1_PIC_CX = 170
PAGE1_WORD_CX = 445
PAGE1_BOX = 100


def draw_page1(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Match the Word",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Draw a line from each picture to its word.",
    )
    pdf.setFont("Helvetica-Bold", 30)
    for stem, cy in zip(PAGE1_PICS, PAGE1_YS):
        draw_picture(pdf, stem, PAGE1_PIC_CX, cy, PAGE1_BOX)
    for word, cy in zip(PAGE1_WORDS, PAGE1_YS):
        pdf.drawCentredString(PAGE1_WORD_CX, cy - 10, word)
    draw_footer(pdf)
    pdf.showPage()


# Page 2: circle the matching word. Each row: one large picture on the
# left, 2 simple word choices on the right; correct side varies by row.
PAGE2_ROWS = [
    ("x-lion", ["LION", "BEAR"]),
    ("x-bus", ["CAR", "BUS"]),
    ("x-shoe", ["SHOE", "HAT"]),
    ("x-cookie", ["CAKE", "COOKIE"]),
    ("x-kite", ["KITE", "BALL"]),
]
PAGE2_YS = [500, 405, 310, 215, 120]
PAGE2_PIC_CX = 150
PAGE2_BOX = 100
PAGE2_WORD_CXS = [375, 520]


def draw_page2(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Circle the Word",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Circle the word that matches the picture.",
    )
    pdf.setFont("Helvetica-Bold", 26)
    for (stem, words), cy in zip(PAGE2_ROWS, PAGE2_YS):
        draw_picture(pdf, stem, PAGE2_PIC_CX, cy, PAGE2_BOX)
        for word, cx in zip(words, PAGE2_WORD_CXS):
            pdf.drawCentredString(cx, cy - 9, word)
    draw_footer(pdf)
    pdf.showPage()


# Page 3: match picture -> word with 5 NEW pairs. Right column shuffled
# so no pair sits across from its picture.
PAGE3_PICS = ["x-monkey", "x-penguin", "x-pizza", "x-ice-cream", "x-boat"]
PAGE3_WORDS = ["PIZZA", "BOAT", "MONKEY", "PENGUIN", "ICE CREAM"]
PAGE3_YS = [500, 405, 310, 215, 120]
PAGE3_PIC_CX = 170
PAGE3_WORD_CX = 445
PAGE3_BOX = 100


def draw_page3(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Match More Words",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Draw a line from each picture to its word.",
    )
    pdf.setFont("Helvetica-Bold", 30)
    for stem, cy in zip(PAGE3_PICS, PAGE3_YS):
        draw_picture(pdf, stem, PAGE3_PIC_CX, cy, PAGE3_BOX)
    for word, cy in zip(PAGE3_WORDS, PAGE3_YS):
        pdf.drawCentredString(PAGE3_WORD_CX, cy - 10, word)
    draw_footer(pdf)
    pdf.showPage()


# Page 4: circle the matching word with 5 NEW pictures. Correct side
# varies by row.
PAGE4_ROWS = [
    ("x-horse", ["HORSE", "DOG"]),
    ("x-octopus", ["CRAB", "OCTOPUS"]),
    ("x-donut", ["DONUT", "PIE"]),
    ("x-train", ["PLANE", "TRAIN"]),
    ("x-umbrella", ["UMBRELLA", "COAT"]),
]
PAGE4_YS = [500, 405, 310, 215, 120]
PAGE4_PIC_CX = 150
PAGE4_BOX = 100
PAGE4_WORD_CXS = [375, 520]


def draw_page4(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Circle More Words",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Circle the word that matches the picture.",
    )
    pdf.setFont("Helvetica-Bold", 26)
    for (stem, words), cy in zip(PAGE4_ROWS, PAGE4_YS):
        draw_picture(pdf, stem, PAGE4_PIC_CX, cy, PAGE4_BOX)
        for word, cx in zip(words, PAGE4_WORD_CXS):
            pdf.drawCentredString(cx, cy - 9, word)
    draw_footer(pdf)
    pdf.showPage()


# Page 5: mixed review - 6 NEW pictures with 6 words in mixed order;
# draw lines to match. No pair sits across from its picture.
PAGE5_PICS = ["x-sheep", "x-owl", "x-grapes",
              "x-sandwich", "x-crayon", "x-lamp"]
PAGE5_WORDS = ["LAMP", "SHEEP", "SANDWICH", "CRAYON", "OWL", "GRAPES"]
PAGE5_YS = [500, 418, 336, 254, 172, 90]
PAGE5_PIC_CX = 170
PAGE5_WORD_CX = 445
PAGE5_BOX = 88


def draw_page5(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Word Review",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Draw a line from each picture to its word.",
    )
    pdf.setFont("Helvetica-Bold", 26)
    for stem, cy in zip(PAGE5_PICS, PAGE5_YS):
        draw_picture(pdf, stem, PAGE5_PIC_CX, cy, PAGE5_BOX)
    for word, cy in zip(PAGE5_WORDS, PAGE5_YS):
        pdf.drawCentredString(PAGE5_WORD_CX, cy - 9, word)
    draw_footer(pdf)
    pdf.showPage()


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "picture-word-matching-prototype.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    draw_page2(pdf)
    draw_page3(pdf)
    draw_page4(pdf)
    draw_page5(pdf)
    pdf.save()
    print(f"wrote {out} (5 pages)")


if __name__ == "__main__":
    main()
