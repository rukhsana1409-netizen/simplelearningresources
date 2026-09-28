"""Build My First Reading Stories (Reading & Language) — prototype.

Approved 4-page content plan (2026-09-28). One mini-story per page,
2-3 very short sentences, one large full-scene illustration, 3 easy
comprehension questions with 3 large picture choices each. Questions
test understanding of the actual story, not general knowledge. No
sequencing, "what happens next", drawing, or beginning/middle/end
(those belong in a separate Early Comprehension Skills resource).

Page 1 — "The Red Cat" (extremely easy), revised 2026-09-28:
  "The cat is red. The cat has a blue ball. The cat plays with the ball."
  1. What color is the cat? (blue cat / RED CAT / green cat)
  2. What does the cat have? (red hat / yellow shoe / BLUE BALL)
  3. What color is the ball? (BLUE BALL / red ball / green ball)
The Q1 red cat is clearly true-red, consistent with the story scene.

Page 2 — "The Dog and the Duck" (extremely easy):
  "The dog runs in the park. The dog sees a yellow duck.
   The duck is by the pond."
  1. Where is the dog? 2. What color is the duck? 3. Where is the duck?

Page 3 — "Mia and Her Kite" (slightly more challenging):
  "Mia has a big red kite. She runs fast in the park.
   The kite flies high in the sky."
  1. What does Mia have? 2. Where does the kite fly?
  3. What color is the kite?

Page 4 — "Ben's Lost Shoe" (slightly more challenging):
  "Ben lost his blue shoe. He looks under the bed.
   Ben finds his shoe and puts it on."
  1. What did Ben lose? 2. Where does Ben find his shoe?
  3. What does Ben do with his shoe?

Only Page 1 is built for now; pages are added one at a time after
the user's review and approval.
"""

from __future__ import annotations

import io
import os

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792

PACK_TITLE = "My First Reading Stories"
SUBTITLE = "Preschool Reading & Language"
INSTRUCTION = "Listen to the story. Circle the answer."

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
GOLD = HexColor("#F4B63E")
INK = HexColor("#202A33")
BORDER = HexColor("#B9D7D2")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "reading-stories")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "reading",
                   "my-first-reading-stories",
                   "my-first-reading-stories-prototype.pdf")


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
    if ": " in title:
        prefix, focus = title.split(": ", 1)
    else:
        prefix, focus = "", title
    if prefix:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(title_x, PAGE_HEIGHT - 67, prefix + ":")
    pdf.setFillColor(TEAL)
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


# New-page images are embedded downscaled to 1100px wide: still sharp
# at print size, and it keeps the PDF small enough for the GitHub
# blob API. Full-resolution masters stay in assets/.
MAX_EMBED_WIDTH = 1100


def draw_cover_picture(pdf, stem, cy, x, w, h, r=12):
    """Full-bleed illustration clipped cleanly inside its rounded card."""
    path = os.path.join(ASSETS, stem + ".png")
    img = Image.open(path)
    if img.width > MAX_EMBED_WIDTH:
        img = img.resize(
            (MAX_EMBED_WIDTH,
             int(img.height * MAX_EMBED_WIDTH / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    src = ImageReader(buf)
    iw, ih = img.size
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    pdf.saveState()
    p = pdf.beginPath()
    p.roundRect(x, cy - h / 2, w, h, r)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.drawImage(src, x - (dw - w) / 2, cy - dh / 2, dw, dh,
                  preserveAspectRatio=True, mask="auto")
    pdf.restoreState()
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, cy - h / 2, w, h, r, fill=0, stroke=1)


# ---------------------------------------------------------------- Page 1

P1_STORY_TITLE = "The Red Cat"
P1_STORY_LINES = ("The cat is red. The cat has a blue ball.",
                  "The cat plays with the ball.")
P1_SCENE = "mfrs-p1-scene"

P1_QUESTIONS = [
    ("1. What color is the cat?",
     ["mfrs-p1-cat-blue", "mfrs-p1-cat-red", "mfrs-p1-cat-green"]),
    ("2. What does the cat have?",
     ["mfrs-p1-hat-red", "mfrs-p1-shoe-yellow", "mfrs-p1-ball-blue"]),
    ("3. What color is the ball?",
     ["mfrs-p1-ball-blue2", "mfrs-p1-ball-red", "mfrs-p1-ball-green"]),
]

P1_SCENE_W, P1_SCENE_H = 470, 140
P1_CARD_W, P1_CARD_H = 160, 60
P1_ROW_TOPS = (354, 250, 146)
P1_LABEL_TO_CARD = 20
# Soft tinted box framing the story section (scene + story text) so it
# reads as distinct from the questions below.
P1_BOX_X, P1_BOX_W = 36, 540
P1_BOX_TOP, P1_BOX_BOTTOM = 602, 396
P1_BOX_FILL = HexColor("#EAF4F3")
P1_BOX_BORDER = HexColor("#9FD3D1")


def draw_page1(pdf):
    draw_header(pdf, f"{PACK_TITLE}: {P1_STORY_TITLE}", SUBTITLE)
    # Soft story box: groups the scene and story text apart from the
    # questions below.
    pdf.setFillColor(P1_BOX_FILL)
    pdf.setStrokeColor(P1_BOX_BORDER)
    pdf.setLineWidth(1.2)
    pdf.roundRect(P1_BOX_X, P1_BOX_BOTTOM, P1_BOX_W,
                  P1_BOX_TOP - P1_BOX_BOTTOM, 14, fill=1, stroke=1)
    # Large story scene.
    scene_cx = PAGE_WIDTH / 2
    scene_cy = 594 - P1_SCENE_H / 2
    draw_cover_picture(pdf, P1_SCENE, scene_cy,
                       scene_cx - P1_SCENE_W / 2, P1_SCENE_W, P1_SCENE_H)
    # Story text, large and easy to read.
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(PAGE_WIDTH / 2, 430, P1_STORY_LINES[0])
    pdf.drawCentredString(PAGE_WIDTH / 2, 406, P1_STORY_LINES[1])
    # Instruction.
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 380, INSTRUCTION)
    # Question rows.
    card_xs = [MARGIN + 26,
               MARGIN + 26 + P1_CARD_W + 14,
               MARGIN + 26 + 2 * (P1_CARD_W + 14)]
    for row_top, (question, stems) in zip(P1_ROW_TOPS, P1_QUESTIONS):
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(PAGE_WIDTH / 2, row_top, question)
        card_cy = row_top - P1_LABEL_TO_CARD - P1_CARD_H / 2
        for x, stem in zip(card_xs, stems):
            draw_cover_picture(pdf, stem, card_cy, x,
                               P1_CARD_W, P1_CARD_H)
    draw_footer(pdf)
    pdf.showPage()


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pdf = canvas.Canvas(OUT, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_page1(pdf)
    pdf.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
