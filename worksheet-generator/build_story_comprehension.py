"""Build the Story & Comprehension prototype (Pages 1-2).

Preschool Reading & Language:
- Page 1 (Look and Answer): 3 spacious sections. Each section has one
  large, simple scene and one very concrete question with exactly 2
  large picture answer choices. The answer is directly visible in the
  scene — no inference. Sections: girl eating an apple ("What is she
  eating?" — cake / apple); boy holding a ball ("What is he holding?" —
  ball / shoe); cat sleeping ("Who is sleeping?" — dog / cat).
- Page 2 (Picture Sequencing): 3 separate everyday sequences, each with
  3 large pictures shown out of order. A large empty box under each
  picture is for the child to write 1, 2, or 3. Sequences: washing
  hands (dirty -> washing -> clean); getting dressed (clothes pile ->
  pulling on shirt -> dressed); eating a snack (whole cookie ->
  bitten cookie -> crumbs).
- Page 3 (Look and Answer, set 2): same activity as Page 1 with new
  everyday scenes. Girl drinking milk ("What is she drinking?" — juice
  / milk); boy playing with a ball ("What is he playing with?" — ball
  / book); dog sleeping in a bed ("Where is the dog sleeping?" —
  chair / bed).
- Page 4 (What Happens Next?): 3 rows. Each row shows one clear
  starting picture/action, an arrow, and 2 large picture choices for
  what logically happens next. Child drops a glass of water (cake /
  spill); dark rain cloud (rain falling / sunny beach); child puts
  toothpaste on toothbrush (playing with a ball / brushing teeth).
- Page 5 (Draw What Happens Next?): 2 large story sections. Each
  shows 2 pictures in order, an arrow, and one large empty drawing
  box where the child draws what happens next. Small seed ->
  small sprout (draw a bigger plant/flower next); empty cup ->
  water being poured into the cup (draw a full cup next).

Prototype only: these 5 pages for review. Do not extend without approval.
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
    white,
)

TITLE = "Story & Comprehension"
BASE = os.path.dirname(os.path.abspath(__file__))
ASSET_DIRS = [
    os.path.join(BASE, "assets", "story-comprehension"),
    os.path.join(BASE, "assets", "letters"),
]
_CONVERT_DIR = os.path.join("/tmp", "story_comprehension_jpg")
_CONVERTED = {}


def asset_path(stem):
    """Resolve a PNG/WEBP asset stem to a path reportlab can read."""
    for d in ASSET_DIRS:
        for ext in (".png", ".webp"):
            src = os.path.join(d, stem + ext)
            if src in _CONVERTED:
                return _CONVERTED[src]
            if not os.path.exists(src):
                continue
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
    raise FileNotFoundError(f"asset not found: {stem}")


def draw_picture(pdf, stem, cx, cy, box):
    img = ImageReader(asset_path(stem))
    pdf.drawImage(img, cx - box / 2, cy - box / 2, width=box, height=box,
                  preserveAspectRatio=True, anchor="c", mask="auto")


# Page 1: Look and Answer. Each section shows one large scene and one
# concrete question with exactly 2 large picture choices. The answer
# is directly visible in the scene — no inference.
PAGE1_SECTIONS = [
    ("s-girl-apple", "What is she eating?", ["c-cake", "s-apple"]),
    ("s-boy-ball", "What is he holding?", ["s-ball", "w-shoe"]),
    ("s-cat-sleep", "Who is sleeping?", ["d-dog", "c-cat"]),
]
PAGE1_YS = [485, 315, 145]


def draw_look_section(pdf, cy, scene, question, choices):
    """Draw one look-and-answer section."""
    x, w, h = 36, 540, 150
    y = cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
    draw_picture(pdf, scene, 140, cy, 120)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(245, cy + 42, question)
    for stem, cx in zip(choices, (380, 490)):
        draw_picture(pdf, stem, cx, cy - 12, 95)


def draw_page1(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Look and Answer",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 580,
        "Look at the picture. Circle the answer.",
    )
    for (scene, question, choices), cy in zip(PAGE1_SECTIONS, PAGE1_YS):
        draw_look_section(pdf, cy, scene, question, choices)
    draw_footer(pdf)
    pdf.showPage()


# Page 2: Picture Sequencing. 3 everyday sequences, each with 3 large
# pictures shown out of order. A large empty box under each picture
# is for the child to write 1, 2, or 3.
PAGE2_SEQS = [
    ["s-hands-washing", "s-hands-clean", "s-hands-dirty"],
    ["s-dressing", "s-dressed", "s-clothes-pile"],
    ["s-cookie-whole", "s-cookie-crumbs", "s-cookie-bitten"],
]
PAGE2_YS = [485, 315, 145]
PAGE2_CXS = [166, 306, 446]


def draw_seq_row(pdf, cy, stems):
    """Draw one sequencing row: 3 pictures with empty number boxes."""
    x, w, h = 36, 540, 150
    y = cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
    for stem, cx in zip(stems, PAGE2_CXS):
        draw_picture(pdf, stem, cx, cy + 22, 95)
        bx, bw = cx - 23, 46
        by = y + 14
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(bx, by, bw, bw, 10, fill=1, stroke=1)


def draw_page2(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Picture Sequencing",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 580,
        "Write 1, 2, and 3 to show what happens first, next, and last.",
    )
    for seq, cy in zip(PAGE2_SEQS, PAGE2_YS):
        draw_seq_row(pdf, cy, seq)
    draw_footer(pdf)
    pdf.showPage()


# Page 3: Look and Answer (set 2). Same activity as Page 1 with new
# everyday scenes: girl drinking milk; boy playing with a ball;
# dog sleeping in a bed.
PAGE3_SECTIONS = [
    ("s-girl-milk", "What is she drinking?", ["s-juice", "s-milk"]),
    ("s-boy-playball", "What is he playing with?", ["s-ball", "b-book"]),
    ("s-dog-bed", "Where is the dog sleeping?", ["s-chair", "s-bed"]),
]
PAGE3_YS = [485, 315, 145]


def draw_page3(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Look and Answer",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 580,
        "Look at the picture. Circle the answer.",
    )
    for (scene, question, choices), cy in zip(PAGE3_SECTIONS, PAGE3_YS):
        draw_look_section(pdf, cy, scene, question, choices)
    draw_footer(pdf)
    pdf.showPage()


# Page 4: What Happens Next? Each row shows one clear starting
# picture/action on the left, an arrow, and 2 large picture choices
# for what logically happens next. Correct position varies by row.
PAGE4_SETS = [
    ("s-drop-glass", ["c-cake", "s-spill"]),
    ("s-dark-cloud", ["s-rain-falling", "s-beach"]),
    ("s-toothpaste-brush", ["s-boy-playball", "s-brushing"]),
]
PAGE4_YS = [485, 315, 145]


def draw_cause_row(pdf, cy, story, choices):
    """Draw one cause-and-effect row."""
    x, w, h = 36, 540, 150
    y = cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
    draw_picture(pdf, story, 150, cy, 110)
    # Arrow between the story and the choices.
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(4)
    pdf.setLineCap(1)
    pdf.line(235, cy, 280, cy)
    pdf.line(280, cy, 268, cy + 10)
    pdf.line(280, cy, 268, cy - 10)
    for stem, cx in zip(choices, (380, 490)):
        draw_picture(pdf, stem, cx, cy, 95)


def draw_page4(pdf):
    draw_header(pdf, {"title": f"{TITLE}: What Happens Next?",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 580,
        "Circle what happens next.",
    )
    for (story, choices), cy in zip(PAGE4_SETS, PAGE4_YS):
        draw_cause_row(pdf, cy, story, choices)
    draw_footer(pdf)
    pdf.showPage()


# Page 5: Draw What Happens Next? 2 large story sections. Each shows
# 2 pictures in order, an arrow, and one large empty drawing box where
# the child draws what happens next. No answer choices.
# Each entry is (stem, box_size): the seed is deliberately small.
PAGE5_SEQS = [
    [("s-seed-small", 70), ("s-sprout", 120)],
    [("s-cup-empty", 120), ("s-cup-pouring", 120)],
]
PAGE5_YS = [428, 183]


def draw_draw_row(pdf, cy, items):
    """Draw one draw-what-happens-next section."""
    x, w, h = 36, 540, 225
    y = cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
    for (stem, size), cx in zip(items, (150, 310)):
        draw_picture(pdf, stem, cx, cy + 20, size)
    # Arrow between the two story pictures.
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(4)
    pdf.setLineCap(1)
    pdf.line(215, cy + 20, 260, cy + 20)
    pdf.line(260, cy + 20, 248, cy + 30)
    pdf.line(260, cy + 20, 248, cy + 10)
    # Large empty drawing box.
    bx, bw, bh = 395, 150, 150
    by = cy - bh / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(bx, by, bw, bh, 12, fill=1, stroke=1)


def draw_page5(pdf):
    draw_header(pdf, {"title": f"{TITLE}: Draw What Happens Next?",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 580,
        "Draw what happens next.",
    )
    for seq, cy in zip(PAGE5_SEQS, PAGE5_YS):
        draw_draw_row(pdf, cy, seq)
    draw_footer(pdf)
    pdf.showPage()


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "story-comprehension-prototype.pdf",
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
