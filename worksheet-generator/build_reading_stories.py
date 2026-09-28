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

Page 2 — "The Dog and the Duck" (extremely easy), built 2026-09-28:
  "The dog runs in the park. The dog sees a yellow duck.
   The duck is by the pond."
  1. Where is the dog? (kitchen / bedroom / PARK)
  2. What color is the duck? (YELLOW DUCK / green duck / brown duck)
  3. Where is the duck? (on the bed / BY THE POND / in the kitchen)

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
P1_ROW_TOPS = (350, 246, 142)
P1_LABEL_TO_CARD = 20
# Soft tinted box framing the story section (scene + story text) so it
# reads as distinct from the questions below.
P1_BOX_X, P1_BOX_W = 36, 540
P1_BOX_TOP, P1_BOX_BOTTOM = 602, 396
P1_BOX_FILL = HexColor("#EAF4F3")
P1_BOX_BORDER = HexColor("#9FD3D1")


# ---------------------------------------------------------------- Page 2

P2_STORY_TITLE = "The Dog and the Duck"
P2_STORY_LINES = ("The dog runs in the park.",
                  "The dog sees a yellow duck.",
                  "The duck is by the pond.")
P2_SCENE = "mfrs-p2-scene"

P2_QUESTIONS = [
    ("1. Where is the dog?",
     ["mfrs-p2-dog-kitchen", "mfrs-p2-dog-bedroom", "mfrs-p2-dog-park"]),
    ("2. What color is the duck?",
     ["mfrs-p2-duck-yellow", "mfrs-p2-duck-green", "mfrs-p2-duck-brown"]),
    ("3. Where is the duck?",
     ["mfrs-p2-duck-bed", "mfrs-p2-duck-pond", "mfrs-p2-duck-kitchen"]),
]


# ---------------------------------------------------------------- Page 3

P3_STORY_TITLE = "Mia and Her Kite"
P3_STORY_LINES = ("Mia has a big red kite.",
                  "She runs fast in the park.",
                  "The kite flies high in the sky.")
P3_SCENE = "mfrs-p3-scene"

P3_QUESTIONS = [
    ("1. What does Mia have?",
     ["mfrs-p3-red-kite", "mfrs-p3-blue-ball", "mfrs-p3-green-hat"]),
    ("2. Where does the kite fly?",
     ["mfrs-p3-kite-sky", "mfrs-p3-kite-pond", "mfrs-p3-kite-house"]),
    ("3. What color is the kite?",
     ["mfrs-p3-red-kite", "mfrs-p3-blue-kite", "mfrs-p3-yellow-kite"]),
]


# ---------------------------------------------------------------- Page 4

P4_STORY_TITLE = "Ben's Lost Shoe"
P4_STORY_LINES = ("Ben lost his blue shoe.",
                  "He looks under the bed.",
                  "Ben finds his shoe and puts it on.")
P4_SCENE = "mfrs-p4-scene"

P4_QUESTIONS = [
    ("1. What did Ben lose?",
     ["mfrs-p4-blue-shoe", "mfrs-p4-red-sock", "mfrs-p4-green-hat"]),
    ("2. Where does Ben find his shoe?",
     ["mfrs-p4-shoe-under-bed", "mfrs-p4-shoe-in-box",
      "mfrs-p4-shoe-on-chair"]),
    ("3. What does Ben do with his shoe?",
     ["mfrs-p4-shoe-put-on", "mfrs-p4-shoe-throw", "mfrs-p4-shoe-wash"]),
]


def draw_story_page(pdf, cfg):
    draw_header(pdf, f"{PACK_TITLE}: {cfg['title']}", SUBTITLE)
    # Soft story box: groups the scene and story text apart from the
    # questions below.
    pdf.setFillColor(P1_BOX_FILL)
    pdf.setStrokeColor(P1_BOX_BORDER)
    pdf.setLineWidth(1.2)
    pdf.roundRect(P1_BOX_X, cfg["box_bottom"], P1_BOX_W,
                  cfg["box_top"] - cfg["box_bottom"], 14, fill=1, stroke=1)
    # Large story scene.
    scene_cx = PAGE_WIDTH / 2
    scene_cy = cfg["box_top"] - 8 - cfg["scene_h"] / 2
    draw_cover_picture(pdf, cfg["scene"], scene_cy,
                       scene_cx - P1_SCENE_W / 2, P1_SCENE_W, cfg["scene_h"])
    # Story text, large and easy to read.
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", cfg["text_size"])
    text_y = cfg["text_top"]
    for line in cfg["story_lines"]:
        pdf.drawCentredString(PAGE_WIDTH / 2, text_y, line)
        text_y -= cfg["text_leading"]
    # Instruction.
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, cfg["instruction_y"], INSTRUCTION)
    # Question rows.
    card_w, card_h = cfg["card_w"], cfg["card_h"]
    card_xs = [MARGIN + 26,
               MARGIN + 26 + card_w + 14,
               MARGIN + 26 + 2 * (card_w + 14)]
    label_to_card = cfg["label_to_card"]
    for row_top, (question, stems) in zip(cfg["row_tops"], cfg["questions"]):
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(PAGE_WIDTH / 2, row_top, question)
        card_cy = row_top - label_to_card - card_h / 2
        for x, stem in zip(card_xs, stems):
            draw_cover_picture(pdf, stem, card_cy, x, card_w, card_h)
    draw_footer(pdf)
    pdf.showPage()


PAGE_CONFIGS = [
    # Page 1 — approved, locked. Values kept exactly as the approved v6.
    dict(title=P1_STORY_TITLE, scene=P1_SCENE, scene_h=140,
         story_lines=P1_STORY_LINES, text_size=20, text_top=430,
         text_leading=24, box_top=602, box_bottom=396, instruction_y=372,
         row_tops=P1_ROW_TOPS, card_w=P1_CARD_W, card_h=P1_CARD_H,
         label_to_card=P1_LABEL_TO_CARD, questions=P1_QUESTIONS),
    # Page 2 — revised 2026-09-28: spacing redistributed per user
    # (28pt story→instruction, 10pt instruction→Q1, 16pt between rows).
    dict(title=P2_STORY_TITLE, scene=P2_SCENE, scene_h=112,
         story_lines=P2_STORY_LINES, text_size=19, text_top=466,
         text_leading=23, box_top=610, box_bottom=406, instruction_y=376,
         row_tops=(351, 246, 141), card_w=160, card_h=60,
         label_to_card=18, questions=P2_QUESTIONS),
    # Page 3 — "Mia and Her Kite" (2026-09-28): 24pt Name/Date→panel,
    # 15pt story→instruction, 11pt instruction→Q1, 8pt question→cards,
    # 17pt between rows, ~29pt above footer.
    dict(title=P3_STORY_TITLE, scene=P3_SCENE, scene_h=140,
         story_lines=P3_STORY_LINES, text_size=19, text_top=436,
         text_leading=23, box_top=608, box_bottom=378, instruction_y=359,
         row_tops=(333, 237, 141), card_w=160, card_h=60,
         label_to_card=8, questions=P3_QUESTIONS),
    # Page 4 — "Ben's Lost Shoe" (2026-09-28): same design, spacing and
    # visual style as Page 3.
    dict(title=P4_STORY_TITLE, scene=P4_SCENE, scene_h=140,
         story_lines=P4_STORY_LINES, text_size=19, text_top=436,
         text_leading=23, box_top=608, box_bottom=378, instruction_y=359,
         row_tops=(333, 237, 141), card_w=160, card_h=60,
         label_to_card=8, questions=P4_QUESTIONS),
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pdf = canvas.Canvas(OUT, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    for cfg in PAGE_CONFIGS:
        draw_story_page(pdf, cfg)
    pdf.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
