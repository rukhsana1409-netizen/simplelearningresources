#!/usr/bin/env python3
"""Grade 1 Reading - Sentences That Work: Capitals and End Marks.

Resource 16 in the approved and locked Grade 1 Reading and
Language Arts roadmap (audit 2026-11-05). Plan approved
2026-11-18. Placement: Grade 1 / Reading & Language /
Grammar and Sentences. Standards RF.1.1(a), L.1.2(a),
L.1.2(b), L.1.2(c):
RF.1.1(a) covers spotting what makes a group of words a
sentence (first word, capital, end mark). L.1.2(a) covers
capitalizing names of people and dates. L.1.2(b) covers
end punctuation (period, question mark, exclamation
point). L.1.2(c) covers commas in dates and in lists.
Pages 4 and 5 give children practice producing simple
sentences, which supports L.1.1(j), but this pack does not
teach the full scope of L.1.1(j). Resource 23 (Joining
Words and Sentence Types) completes L.1.1(j) with sentence
types, expansion, and compound sentences.

Progression: identify a complete sentence (Page 1), fix
capitals and end marks (Page 2), fix names, dates, and
commas in dates (Page 3), build a clear sentence from word
cards, adding the commas in a list (Page 4), and write two
sentences of their own about a picture (Page 5).

Pages:
  P1: Is It a Sentence? Four pictures, each with a complete
      sentence and a fragment. The child circles the words
      that tell a whole idea. Answers: The dog runs. /
      Mia reads a book. / Ben kicks the ball. / The birds
      sing.
  P2: Start Big, End with a Mark. Four sentences shown in
      lowercase with no end mark, each with a picture. The
      child rewrites each one with a capital and the right
      end mark. Answers: The sun is up. / Where is my red
      ball? / I love my new bike! / Sam can jump high. The
      bike picture shows a child excited about a new bike,
      so the exclamation point is visually meaningful.
  P3: Names and Dates. Four sentences with a person's name
      and a date, missing capitals and the comma in the
      date. The name and date words are bold in the broken
      sentence so the child sees what to fix. Answers: Mia
      likes to read on Sunday. / Ben was born on March 3,
      2026. / Ava and Noah play on Friday. / School starts
      on August 24, 2026.
  P4: Build a Clear Sentence. Three sets of mixed-up word
      cards, each with a picture. The child puts the words
      in order and writes the clear sentence. The list
      sentence has NO commas on its word cards: the child
      must insert the commas when writing. Answers: The cat
      sits on the mat. / Leo eats an apple. / I see a cat,
      a dog, and a bird.
  P5: Write Your Own Sentences. A large park picture and
      two generous, separate writing areas. The child writes
      two sentences of their own about the picture, then
      checks three things: capital, end mark, whole idea.

No printable answer key. The Parent Guide is the only
extra download and carries the answers. No em dash
anywhere in the student pages or the guide.

Illustrations (v3, 2026-11-19): the geometric vector
scenes are retired. All pictures are original watercolor
storybook JPEGs in OUT_DIR (p1-*.jpg, p2-*.jpg, p3-*.jpg,
p4-*.jpg, park-scene-v2.jpg), embedded with _draw_image.
JPEGs embed as DCT, so the PDF stays small. The park is
shown whole (3:2) rather than cropped, so Page 5 uses a
taller park and slightly shorter writing areas.

Shared design code (logo, header, footer) is imported
verbatim from build_phonics_az.py. Do not fork it here.
Header title is drawn at 18pt and the subtitle at 14pt;
both end inside the teal rule.
"""
import hashlib
import math
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter as _letter  # noqa: F401
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from build_phonics_az import (NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              draw_footer, draw_header, draw_logo)

TITLE = "Sentences That Work"
SUBTITLE = "Grade 1 Reading | Sentences That Work"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")
SKY = HexColor("#D6EAF8")
SKY_DARK = HexColor("#7FB3D5")
GRASS = HexColor("#A8D5A2")
GRASS_DARK = HexColor("#7CB87A")
SUN = HexColor("#F7C948")
LEAF = HexColor("#4CAF50")
LEAF_DARK = HexColor("#388E3C")
TRUNK = HexColor("#8D6E63")
BROWN = HexColor("#6D4C41")
SKIN = HexColor("#F2C29B")
SKIN_DARK = HexColor("#E8A87C")
HAIR_BROWN = HexColor("#5D4037")
HAIR_BLACK = HexColor("#212121")
SHIRT_BLUE = HexColor("#42A5F5")
SHIRT_RED = HexColor("#EF5350")
SHIRT_GREEN = HexColor("#66BB6A")
SHIRT_PURPLE = HexColor("#AB47BC")
PANTS_BLUE = HexColor("#1E88E5")
DRESS_PINK = HexColor("#F48FB1")
DOG_BROWN = HexColor("#A1887F")
DOG_DARK = HexColor("#6D4C41")
CAT_ORANGE = HexColor("#FFB74D")
CAT_DARK = HexColor("#F57C00")
BIRD_BLUE = HexColor("#42A5F5")
BIRD_YELLOW = HexColor("#FFCA28")
APPLE_RED = HexColor("#E53935")
BALL_RED = HexColor("#E53935")
BALL_BLUE = HexColor("#1E88E5")
BALL_YELLOW = HexColor("#FDD835")
KITE_RED = HexColor("#EF5350")
KITE_BLUE = HexColor("#42A5F5")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "sentences-that-work")
IMG_DIR = OUT_DIR  # watercolor illustration JPEGs live beside the PDFs


def _draw_image(pdf, path, cx, cy, w, h):
    """Draw a JPEG illustration centred at (cx, cy), fitted
    inside a w-by-h box while preserving its aspect ratio.
    The picture is centred in the box; any leftover space
    stays empty. JPEGs embed as DCT, so the PDF stays small."""
    from PIL import Image as _PILImage
    with _PILImage.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    pdf.drawImage(path, cx - dw / 2, cy - dh / 2,
                  width=dw, height=dh, preserveAspectRatio=True,
                  mask="auto")


def _adult_line(pdf, text):
    """Centred adult line at y=74. Splits into two lines if
    the text would run past the page edges."""
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica-Bold", 10.5)
    if stringWidth(text, "Helvetica-Bold", 10.5) <= 560:
        pdf.drawCentredString(PAGE_WIDTH / 2, 74, text)
        return
    words = text.split(" ")
    best = None
    for i in range(2, len(words) - 1):
        w1 = stringWidth(" ".join(words[:i]), "Helvetica-Bold",
                         10.5)
        w2 = stringWidth(" ".join(words[i:]), "Helvetica-Bold",
                         10.5)
        if best is None or max(w1, w2) < best[0]:
            best = (max(w1, w2), i)
    i = best[1]
    pdf.drawCentredString(PAGE_WIDTH / 2, 80,
                          " ".join(words[:i]))
    pdf.drawCentredString(PAGE_WIDTH / 2, 64,
                          " ".join(words[i:]))


def _page_title(pdf, title, instruction):
    """Page title at 642 and instruction line(s) below it.
    Returns the y of the top of the content area: 606 for a
    one-line instruction, 592 for a two-line instruction."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, title)
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 12)
    if "\n" in instruction:
        line1, line2 = instruction.split("\n", 1)
        pdf.drawCentredString(PAGE_WIDTH / 2, 624, line1)
        pdf.drawCentredString(PAGE_WIDTH / 2, 606, line2)
        return 592
    pdf.drawCentredString(PAGE_WIDTH / 2, 624, instruction)
    return 606


def _panel(pdf, x, y, w, h):
    """A light rounded panel. (x, y) is the bottom-left corner."""
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(x, y, w, h, 14, stroke=1, fill=1)


def _header(pdf):
    draw_header(pdf, TITLE, SUBTITLE, title_size=18,
                subtitle_size=14)


def _ruled_line(pdf, x1, x2, y):
    """A single ruled writing line."""
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.line(x1, y, x2, y)


def _mixed_width(segments, size):
    w = 0
    for text, bold in segments:
        w += stringWidth(text, "Helvetica-Bold" if bold else "Helvetica",
                         size)
    return w


def _draw_mixed_centred(pdf, segments, cy, y, size=12):
    x = cy - _mixed_width(segments, size) / 2
    for text, bold in segments:
        pdf.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        pdf.setFillColor(NAVY)
        pdf.drawString(x, y, text)
        x += stringWidth(text,
                         "Helvetica-Bold" if bold else "Helvetica",
                         size)
    return x


def _draw_mixed_left(pdf, segments, x, y, size=12):
    for text, bold in segments:
        pdf.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        pdf.setFillColor(NAVY)
        pdf.drawString(x, y, text)
        x += stringWidth(text,
                         "Helvetica-Bold" if bold else "Helvetica",
                         size)
    return x


def _circle_choice(pdf, cx, cy, r=8):
    """A small empty circle the child can circle or tick."""
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.4)
    pdf.circle(cx, cy, r, stroke=1, fill=0)


def _ground(pdf, cx, y, w=100):
    """A soft ground line under a small scene."""
    pdf.setStrokeColor(GRASS_DARK)
    pdf.setLineWidth(2)
    pdf.line(cx - w / 2, y, cx + w / 2, y)


def _icon_star(pdf, cx, cy, r=6, color=GOLD):
    """A small five-point star, used for sparkles and
    excitement."""
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang),
                    cy + rr * math.sin(ang)))
    pdf.setFillColor(color)
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)


def _face(pdf, cx, cy, hair, skin=SKIN, r=13):
    """A polished child face: skin, natural hair with a curved
    hairline, eyes with pupils, eyebrows, a smile, and rosy
    cheeks. The face is the same on every page so the children
    look like the same friends throughout the pack."""
    pdf.setFillColor(skin)
    pdf.circle(cx, cy, r, stroke=0, fill=1)
    pdf.setFillColor(hair)
    p = pdf.beginPath()
    p.moveTo(cx - r, cy + 1)
    p.curveTo(cx - r - 1, cy + r + 2, cx - r * 0.35, cy + r + 2,
              cx, cy + r + 1)
    p.curveTo(cx + r * 0.35, cy + r + 2, cx + r + 1, cy + r + 2,
              cx + r, cy + 1)
    p.curveTo(cx + r * 0.72, cy + r * 0.42, cx + r * 0.32,
              cy + r * 0.52, cx, cy + r * 0.48)
    p.curveTo(cx - r * 0.32, cy + r * 0.52, cx - r * 0.72,
              cy + r * 0.42, cx - r, cy + 1)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    for ex in (cx - r * 0.38, cx + r * 0.38):
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.circle(ex, cy + 1, 3.4, stroke=0, fill=1)
        pdf.setFillColor(NAVY)
        pdf.circle(ex + 0.9, cy + 1, 1.8, stroke=0, fill=1)
    pdf.setStrokeColor(hair)
    pdf.setLineWidth(1.4)
    pdf.line(cx - r * 0.56, cy + r * 0.52, cx - r * 0.2,
             cy + r * 0.58)
    pdf.line(cx + r * 0.2, cy + r * 0.58, cx + r * 0.56,
             cy + r * 0.52)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.4)
    pdf.arc(cx - 5, cy - 8, cx + 5, cy - 1, 200, 340)
    pdf.setFillColor(HexColor("#F8BBD0"))
    pdf.circle(cx - r * 0.62, cy - 3, 2.6, stroke=0, fill=1)
    pdf.circle(cx + r * 0.62, cy - 3, 2.6, stroke=0, fill=1)


def _limb(pdf, x1, y1, x2, y2, color, width=4.5):
    """A limb as a thick line with rounded ends, so arms and
    legs look soft and natural instead of stick-like."""
    pdf.setStrokeColor(color)
    pdf.setLineWidth(width)
    pdf.setLineCap(1)
    pdf.line(x1, y1, x2, y2)
    pdf.setLineCap(0)


def _shoe(pdf, cx, cy, color=NAVY):
    """A small shoe: a rounded ellipse at the end of a leg."""
    pdf.setFillColor(color)
    pdf.ellipse(cx - 4, cy - 2.5, cx + 5, cy + 2.5, stroke=0,
                fill=1)


def _shirt(pdf, cx, cy, shirt, h=24):
    """A shirt torso: a rounded body with a collar and short
    sleeves."""
    pdf.setFillColor(shirt)
    pdf.roundRect(cx - 11, cy - h, 22, h + 4, 6, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.circle(cx, cy + 2, 3, stroke=0, fill=1)
    pdf.setFillColor(shirt)
    pdf.circle(cx - 12, cy - 4, 4.5, stroke=0, fill=1)
    pdf.circle(cx + 12, cy - 4, 4.5, stroke=0, fill=1)


def _dress(pdf, cx, cy, color, h=24):
    """A dress torso: a bodice that flares to a rounded hem."""
    pdf.setFillColor(color)
    p = pdf.beginPath()
    p.moveTo(cx - 9, cy + 4)
    p.lineTo(cx + 9, cy + 4)
    p.curveTo(cx + 12, cy - h * 0.4, cx + 15, cy - h * 0.8,
              cx + 13, cy - h)
    p.curveTo(cx + 6, cy - h - 3, cx - 6, cy - h - 3, cx - 13,
              cy - h)
    p.curveTo(cx - 15, cy - h * 0.8, cx - 12, cy - h * 0.4,
              cx - 9, cy + 4)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.circle(cx, cy + 2, 3, stroke=0, fill=1)


def _child_head(pdf, cx, cy, hair=HAIR_BROWN, skin=SKIN):
    """Kept for compatibility: a polished face."""
    _face(pdf, cx, cy, hair, skin=skin)


def _child_body(pdf, cx, cy, shirt, h=26):
    """Kept for compatibility: a shirt torso with legs."""
    _shirt(pdf, cx, cy, shirt, h=h)
    _limb(pdf, cx - 4, cy - h, cx - 4, cy - h - 12, PANTS_BLUE, 5)
    _limb(pdf, cx + 4, cy - h, cx + 4, cy - h - 12, PANTS_BLUE, 5)


# ---------------------------------------------------------------------------
# Vector scenes. Each draws centred near (cx, cy) inside a small
# box about 110 wide and 70 tall, unless noted. Keep every scene
# simple, colorful, and unambiguous: the child must be able to
# tell what is happening from the picture alone.
# ---------------------------------------------------------------------------
def _scene_dog_run(pdf, cx, cy):
    """A friendly brown dog running to the right: a long body,
    a head with a snout and a floppy ear, a raised wagging
    tail, and four legs caught mid-stride."""
    _ground(pdf, cx, cy - 26)
    pdf.setFillColor(DOG_BROWN)
    p = pdf.beginPath()
    p.moveTo(cx - 30, cy + 2)
    p.curveTo(cx - 30, cy + 12, cx - 18, cy + 14, cx - 6, cy + 12)
    p.curveTo(cx + 6, cy + 10, cx + 12, cy + 6, cx + 12, cy - 2)
    p.curveTo(cx + 12, cy - 10, cx - 2, cy - 12, cx - 14, cy - 10)
    p.curveTo(cx - 26, cy - 8, cx - 32, cy - 4, cx - 30, cy + 2)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(DOG_BROWN)
    pdf.circle(cx + 20, cy + 12, 11, stroke=0, fill=1)
    pdf.setFillColor(DOG_BROWN)
    pdf.ellipse(cx + 24, cy + 6, cx + 36, cy + 14, stroke=0, fill=1)
    pdf.setFillColor(DOG_DARK)
    pdf.ellipse(cx + 33, cy + 8, cx + 38, cy + 13, stroke=0, fill=1)
    pdf.setFillColor(DOG_DARK)
    p = pdf.beginPath()
    p.moveTo(cx + 14, cy + 18)
    p.curveTo(cx + 12, cy + 26, cx + 18, cy + 28, cx + 20, cy + 20)
    p.curveTo(cx + 20, cy + 16, cx + 17, cy + 15, cx + 14, cy + 18)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(DOG_DARK)
    pdf.setLineWidth(4)
    pdf.setLineCap(1)
    p = pdf.beginPath()
    p.moveTo(cx - 28, cy + 8)
    p.curveTo(cx - 40, cy + 14, cx - 42, cy + 24, cx - 34, cy + 26)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineCap(0)
    _limb(pdf, cx - 22, cy - 8, cx - 28, cy - 24, DOG_DARK, 4.5)
    _limb(pdf, cx - 10, cy - 10, cx - 14, cy - 24, DOG_DARK, 4.5)
    _limb(pdf, cx + 2, cy - 10, cx + 10, cy - 24, DOG_DARK, 4.5)
    _limb(pdf, cx + 10, cy - 8, cx + 18, cy - 22, DOG_DARK, 4.5)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.circle(cx + 23, cy + 15, 3, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.circle(cx + 24, cy + 15, 1.7, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.3)
    pdf.arc(cx + 24, cy + 2, cx + 32, cy + 8, 200, 340)


def _scene_girl_read(pdf, cx, cy):
    """Mia, a girl sitting cross-legged and reading an open
    book. Long dark hair, a pink dress, both hands holding
    the book, eyes looking down at the pages with a soft
    smile. The clearest picture on the page."""
    _ground(pdf, cx, cy - 26)
    pdf.setFillColor(HAIR_BLACK)
    pdf.ellipse(cx - 15, cy + 2, cx - 6, cy + 26, stroke=0, fill=1)
    pdf.ellipse(cx + 6, cy + 2, cx + 15, cy + 26, stroke=0, fill=1)
    _face(pdf, cx, cy + 14, HAIR_BLACK)
    pdf.setFillColor(DRESS_PINK)
    p = pdf.beginPath()
    p.moveTo(cx - 9, cy + 4)
    p.lineTo(cx + 9, cy + 4)
    p.curveTo(cx + 13, cy - 6, cx + 16, cy - 14, cx + 14, cy - 20)
    p.curveTo(cx + 6, cy - 24, cx - 6, cy - 24, cx - 14, cy - 20)
    p.curveTo(cx - 16, cy - 14, cx - 13, cy - 6, cx - 9, cy + 4)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.circle(cx, cy + 2, 3, stroke=0, fill=1)
    _limb(pdf, cx - 14, cy - 20, cx - 20, cy - 26, SKIN, 4.5)
    _limb(pdf, cx + 14, cy - 20, cx + 20, cy - 26, SKIN, 4.5)
    _shoe(pdf, cx - 20, cy - 26, color=NAVY)
    _shoe(pdf, cx + 20, cy - 26, color=NAVY)
    _limb(pdf, cx - 8, cy - 2, cx - 14, cy - 14, SKIN, 4)
    _limb(pdf, cx + 8, cy - 2, cx + 14, cy - 14, SKIN, 4)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.2)
    p = pdf.beginPath()
    p.moveTo(cx - 17, cy - 12)
    p.lineTo(cx, cy - 6)
    p.lineTo(cx + 17, cy - 12)
    p.lineTo(cx + 17, cy - 24)
    p.lineTo(cx - 17, cy - 24)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.2)
    pdf.line(cx, cy - 6, cx, cy - 24)
    pdf.line(cx - 12, cy - 12, cx - 4, cy - 12)
    pdf.line(cx - 12, cy - 16, cx - 4, cy - 16)
    pdf.line(cx - 12, cy - 20, cx - 4, cy - 20)
    pdf.line(cx + 4, cy - 12, cx + 12, cy - 12)
    pdf.line(cx + 4, cy - 16, cx + 12, cy - 16)
    pdf.line(cx + 4, cy - 20, cx + 12, cy - 20)


def _scene_boy_kick(pdf, cx, cy):
    """Ben, a boy kicking a red ball. He stands on one leg,
    the other leg swung forward to the ball, arms out for
    balance, eyes on the ball, with motion lines behind it."""
    _ground(pdf, cx, cy - 26)
    _face(pdf, cx - 8, cy + 16, HAIR_BROWN)
    _shirt(pdf, cx - 8, cy + 4, SHIRT_BLUE, h=22)
    _limb(pdf, cx - 18, cy + 0, cx - 28, cy + 10, SKIN, 4)
    _limb(pdf, cx + 2, cy + 0, cx + 10, cy + 8, SKIN, 4)
    _limb(pdf, cx - 12, cy - 18, cx - 16, cy - 26, PANTS_BLUE, 5)
    _shoe(pdf, cx - 16, cy - 26, color=NAVY)
    _limb(pdf, cx - 4, cy - 18, cx + 8, cy - 22, PANTS_BLUE, 5)
    _shoe(pdf, cx + 10, cy - 22, color=NAVY)
    pdf.setFillColor(BALL_RED)
    pdf.circle(cx + 20, cy - 20, 9, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.ellipse(cx + 13, cy - 26, cx + 21, cy - 14, stroke=0,
                fill=1)
    pdf.setStrokeColor(BALL_RED)
    pdf.setLineWidth(1.4)
    pdf.line(cx + 4, cy - 16, cx + 8, cy - 16)
    pdf.line(cx + 2, cy - 22, cx + 6, cy - 22)


def _scene_birds(pdf, cx, cy):
    """Two songbirds on a leafy branch: a blue bird and a
    yellow bird, each with a round body, a wing, a beak, a
    tail, and thin legs gripping the branch."""
    pdf.setStrokeColor(TRUNK)
    pdf.setLineWidth(5)
    pdf.setLineCap(1)
    pdf.line(cx - 32, cy - 12, cx + 32, cy - 6)
    pdf.setLineCap(0)
    pdf.setFillColor(LEAF)
    pdf.circle(cx - 30, cy + 14, 15, stroke=0, fill=1)
    pdf.circle(cx + 28, cy + 16, 14, stroke=0, fill=1)
    pdf.circle(cx, cy + 26, 16, stroke=0, fill=1)
    pdf.circle(cx - 8, cy + 10, 10, stroke=0, fill=1)
    for bx, col, wing in ((cx - 15, BIRD_BLUE, HexColor("#1E88E5")),
                          (cx + 15, BIRD_YELLOW,
                           HexColor("#FFB300"))):
        pdf.setFillColor(col)
        pdf.ellipse(bx - 10, cy - 4, bx + 10, cy + 10, stroke=0,
                    fill=1)
        pdf.circle(bx + 8, cy + 8, 6, stroke=0, fill=1)
        pdf.setFillColor(wing)
        pdf.ellipse(bx - 9, cy - 2, bx + 1, cy + 7, stroke=0,
                    fill=1)
        pdf.setFillColor(HexColor("#FF9800"))
        p = pdf.beginPath()
        p.moveTo(bx + 13, cy + 7)
        p.lineTo(bx + 20, cy + 5)
        p.lineTo(bx + 13, cy + 3)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
        pdf.setFillColor(col)
        p = pdf.beginPath()
        p.moveTo(bx - 8, cy - 2)
        p.lineTo(bx - 16, cy - 8)
        p.lineTo(bx - 10, cy + 2)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.circle(bx + 9, cy + 9, 2.4, stroke=0, fill=1)
        pdf.setFillColor(NAVY)
        pdf.circle(bx + 10, cy + 9, 1.3, stroke=0, fill=1)
        pdf.setStrokeColor(TRUNK)
        pdf.setLineWidth(1.4)
        pdf.line(bx - 2, cy - 4, bx - 2, cy - 9)
        pdf.line(bx + 3, cy - 4, bx + 3, cy - 9)


def _scene_sun(pdf, cx, cy):
    """A warm smiling sun with soft rays and rosy cheeks."""
    pdf.setFillColor(SUN)
    pdf.circle(cx, cy, 16, stroke=0, fill=1)
    pdf.setStrokeColor(SUN)
    pdf.setLineWidth(3.5)
    pdf.setLineCap(1)
    for i in range(8):
        ang = i * math.pi / 4
        x1 = cx + 20 * math.cos(ang)
        y1 = cy + 20 * math.sin(ang)
        x2 = cx + 28 * math.cos(ang)
        y2 = cy + 28 * math.sin(ang)
        pdf.line(x1, y1, x2, y2)
    pdf.setLineCap(0)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.circle(cx - 5, cy + 3, 3, stroke=0, fill=1)
    pdf.circle(cx + 5, cy + 3, 3, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.circle(cx - 4, cy + 3, 1.7, stroke=0, fill=1)
    pdf.circle(cx + 6, cy + 3, 1.7, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.4)
    pdf.arc(cx - 6, cy - 8, cx + 6, cy, 200, 340)
    pdf.setFillColor(HexColor("#F8BBD0"))
    pdf.circle(cx - 9, cy - 2, 2.6, stroke=0, fill=1)
    pdf.circle(cx + 9, cy - 2, 2.6, stroke=0, fill=1)
    _ground(pdf, cx, cy - 30)


def _scene_ball(pdf, cx, cy):
    """A big beach ball on the grass, with red, blue, yellow,
    and white panels and a shine."""
    _ground(pdf, cx, cy - 24)
    pdf.setFillColor(BALL_RED)
    pdf.circle(cx, cy + 2, 20, stroke=0, fill=1)
    pdf.setFillColor(BALL_BLUE)
    p = pdf.beginPath()
    p.moveTo(cx, cy + 2)
    p.curveTo(cx - 4, cy - 12, cx - 2, cy - 18, cx + 8, cy - 18)
    p.curveTo(cx + 12, cy - 8, cx + 10, cy - 2, cx, cy + 2)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(BALL_YELLOW)
    p = pdf.beginPath()
    p.moveTo(cx, cy + 2)
    p.curveTo(cx + 12, cy + 4, cx + 18, cy + 10, cx + 14, cy + 18)
    p.curveTo(cx + 6, cy + 20, cx, cy + 12, cx, cy + 2)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.ellipse(cx - 10, cy + 6, cx - 2, cy + 16, stroke=0, fill=1)
    pdf.setFillColor(LEAF)
    for dx, dy in ((-24, -18), (24, -16), (-30, -20), (30, -20)):
        pdf.ellipse(cx + dx - 2, cy + dy, cx + dx + 2, cy + dy + 8,
                    stroke=0, fill=1)


def _scene_bike(pdf, cx, cy):
    """A child thrilled about a brand-new red bike: a proper
    bicycle with spoked wheels, a frame, handlebars with a
    gift bow, and a seat, and the child beside it with both
    arms thrown up, a big open smile, and sparkles in the
    air. The excitement is the reason for the exclamation
    point."""
    _ground(pdf, cx, cy - 28)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(2.2)
    pdf.circle(cx - 26, cy - 20, 10, stroke=1, fill=0)
    pdf.circle(cx + 12, cy - 20, 10, stroke=1, fill=0)
    pdf.setLineWidth(1.1)
    for wx in (cx - 26, cx + 12):
        pdf.line(wx - 10, cy - 20, wx + 10, cy - 20)
        pdf.line(wx, cy - 30, wx, cy - 10)
        pdf.line(wx - 7, cy - 27, wx + 7, cy - 13)
        pdf.line(wx - 7, cy - 13, wx + 7, cy - 27)
    pdf.setStrokeColor(CORAL)
    pdf.setLineWidth(2.6)
    pdf.line(cx - 26, cy - 20, cx - 8, cy - 20)
    pdf.line(cx - 8, cy - 20, cx, cy - 6)
    pdf.line(cx, cy - 6, cx + 12, cy - 20)
    pdf.line(cx, cy - 6, cx - 4, cy - 20)
    pdf.line(cx, cy - 6, cx - 14, cy - 2)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(2.2)
    pdf.line(cx - 14, cy - 2, cx - 18, cy - 6)
    pdf.line(cx - 4, cy - 20, cx + 2, cy - 20)
    pdf.setFillColor(CORAL)
    pdf.ellipse(cx - 6, cy - 3, cx + 4, cy + 1, stroke=0, fill=1)
    pdf.setFillColor(GOLD)
    p = pdf.beginPath()
    p.moveTo(cx - 16, cy - 4)
    p.lineTo(cx - 24, cy + 2)
    p.lineTo(cx - 24, cy - 8)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    p = pdf.beginPath()
    p.moveTo(cx - 16, cy - 4)
    p.lineTo(cx - 8, cy + 2)
    p.lineTo(cx - 8, cy - 8)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    _face(pdf, cx + 28, cy + 22, HAIR_BROWN)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.ellipse(cx + 22, cy + 12, cx + 34, cy + 18, stroke=0,
                fill=1)
    pdf.setFillColor(NAVY)
    pdf.arc(cx + 23, cy + 11, cx + 33, cy + 18, 180, 360)
    _limb(pdf, cx + 18, cy + 12, cx + 6, cy + 28, SKIN, 4)
    _limb(pdf, cx + 38, cy + 12, cx + 50, cy + 28, SKIN, 4)
    _shirt(pdf, cx + 28, cy + 10, SHIRT_GREEN, h=20)
    _limb(pdf, cx + 24, cy - 10, cx + 22, cy - 26, PANTS_BLUE, 5)
    _shoe(pdf, cx + 22, cy - 26, color=NAVY)
    _limb(pdf, cx + 32, cy - 10, cx + 34, cy - 26, PANTS_BLUE, 5)
    _shoe(pdf, cx + 34, cy - 26, color=NAVY)
    pdf.setFillColor(GOLD)
    for sx, sy in ((cx + 6, cy + 32), (cx + 50, cy + 32),
                   (cx + 28, cy + 40)):
        _icon_star(pdf, sx, sy, r=5, color=GOLD)


def _scene_jump(pdf, cx, cy):
    """Sam, a boy jumping high in the air: knees bent, both
    arms up, a big smile, motion lines under his shoes and
    stars around him, clearly off the ground."""
    _limb(pdf, cx - 8, cy + 10, cx - 20, cy + 26, SKIN, 4)
    _limb(pdf, cx + 8, cy + 10, cx + 20, cy + 26, SKIN, 4)
    _face(pdf, cx, cy + 20, HAIR_BLACK)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.ellipse(cx - 6, cy + 10, cx + 6, cy + 16, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.arc(cx - 5, cy + 9, cx + 5, cy + 16, 180, 360)
    _shirt(pdf, cx, cy + 8, SHIRT_RED, h=20)
    _limb(pdf, cx - 5, cy - 12, cx - 12, cy - 22, PANTS_BLUE, 5)
    _shoe(pdf, cx - 13, cy - 22, color=NAVY)
    _limb(pdf, cx + 5, cy - 12, cx + 12, cy - 18, PANTS_BLUE, 5)
    _shoe(pdf, cx + 13, cy - 18, color=NAVY)
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.6)
    pdf.line(cx - 18, cy - 26, cx - 10, cy - 26)
    pdf.line(cx + 8, cy - 28, cx + 16, cy - 28)
    _ground(pdf, cx, cy - 30)
    pdf.setFillColor(GOLD)
    _icon_star(pdf, cx - 30, cy + 28, r=5, color=GOLD)
    _icon_star(pdf, cx + 30, cy + 26, r=5, color=GOLD)


def _scene_cake(pdf, cx, cy):
    """A birthday cake on a plate: two pink-frosted layers,
    frosting drips, three striped candles with bright flames,
    and colorful sprinkles."""
    _ground(pdf, cx, cy - 26)
    pdf.setFillColor(HexColor("#E3F2FD"))
    pdf.ellipse(cx - 30, cy - 26, cx + 30, cy - 18, stroke=0,
                fill=1)
    pdf.setFillColor(HexColor("#FFF8E1"))
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.1)
    pdf.roundRect(cx - 24, cy - 18, 48, 14, 3, stroke=1, fill=1)
    pdf.setFillColor(DRESS_PINK)
    pdf.roundRect(cx - 20, cy - 4, 40, 12, 3, stroke=0, fill=1)
    pdf.setFillColor(DRESS_PINK)
    for dx in (-16, -8, 0, 8, 16):
        pdf.circle(cx + dx, cy - 4, 3, stroke=0, fill=1)
    for dx, col in ((-16, GOLD), (0, TEAL), (16, CORAL)):
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.rect(cx + dx - 2, cy + 8, 4, 10, stroke=0, fill=1)
        pdf.setStrokeColor(BOX_STROKE)
        pdf.setLineWidth(0.8)
        pdf.line(cx + dx - 2, cy + 11, cx + dx + 2, cy + 11)
        pdf.line(cx + dx - 2, cy + 15, cx + dx + 2, cy + 15)
        pdf.setFillColor(GOLD)
        p = pdf.beginPath()
        p.moveTo(cx + dx, cy + 24)
        p.curveTo(cx + dx - 3, cy + 20, cx + dx - 2, cy + 17,
                  cx + dx, cy + 17)
        p.curveTo(cx + dx + 2, cy + 17, cx + dx + 3, cy + 20,
                  cx + dx, cy + 24)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(CORAL)
    pdf.circle(cx - 12, cy - 11, 1.6, stroke=0, fill=1)
    pdf.circle(cx + 4, cy - 11, 1.6, stroke=0, fill=1)
    pdf.circle(cx + 12, cy - 11, 1.6, stroke=0, fill=1)


def _scene_kids_play(pdf, cx, cy):
    """Ava and Noah playing catch: Ava in a pink dress tosses
    a yellow ball through the air, and Noah in a blue shirt
    reaches out to catch it, both smiling."""
    _ground(pdf, cx, cy - 28)
    pdf.setFillColor(HAIR_BLACK)
    pdf.ellipse(cx - 36, cy + 2, cx - 28, cy + 24, stroke=0,
                fill=1)
    _face(pdf, cx - 24, cy + 12, HAIR_BLACK)
    _dress(pdf, cx - 24, cy, DRESS_PINK, h=20)
    _limb(pdf, cx - 32, cy - 16, cx - 34, cy - 26, SKIN, 4.5)
    _shoe(pdf, cx - 34, cy - 26, color=NAVY)
    _limb(pdf, cx - 16, cy - 16, cx - 14, cy - 26, SKIN, 4.5)
    _shoe(pdf, cx - 14, cy - 26, color=NAVY)
    _limb(pdf, cx - 32, cy - 2, cx - 38, cy + 8, SKIN, 4)
    _face(pdf, cx + 22, cy + 12, HAIR_BROWN)
    _shirt(pdf, cx + 22, cy, SHIRT_BLUE, h=20)
    _limb(pdf, cx + 14, cy - 16, cx + 12, cy - 26, PANTS_BLUE, 5)
    _shoe(pdf, cx + 12, cy - 26, color=NAVY)
    _limb(pdf, cx + 30, cy - 16, cx + 32, cy - 26, PANTS_BLUE, 5)
    _shoe(pdf, cx + 32, cy - 26, color=NAVY)
    _limb(pdf, cx + 14, cy - 2, cx + 6, cy + 8, SKIN, 4)
    _limb(pdf, cx + 30, cy - 2, cx + 34, cy + 8, SKIN, 4)
    pdf.setFillColor(BALL_YELLOW)
    pdf.circle(cx - 2, cy + 4, 8, stroke=0, fill=1)
    pdf.setFillColor(BALL_RED)
    pdf.ellipse(cx - 6, cy - 2, cx + 2, cy + 10, stroke=0, fill=1)


def _scene_school(pdf, cx, cy):
    """A friendly schoolhouse: cream walls, a red roof, a
    flag on top, a brown door with a knob, two windows with
    curtains, and stone steps."""
    _ground(pdf, cx, cy - 28)
    pdf.setFillColor(HexColor("#FFF3E0"))
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.2)
    pdf.rect(cx - 26, cy - 26, 52, 34, stroke=1, fill=1)
    pdf.setFillColor(CORAL)
    p = pdf.beginPath()
    p.moveTo(cx - 30, cy + 8)
    p.lineTo(cx, cy + 26)
    p.lineTo(cx + 30, cy + 8)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#BBDEFB"))
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1)
    pdf.rect(cx - 21, cy - 4, 11, 11, stroke=1, fill=1)
    pdf.rect(cx + 10, cy - 4, 11, 11, stroke=1, fill=1)
    pdf.setStrokeColor(BOX_STROKE)
    pdf.line(cx - 15.5, cy - 4, cx - 15.5, cy + 7)
    pdf.line(cx + 15.5, cy - 4, cx + 15.5, cy + 7)
    pdf.setFillColor(BROWN)
    pdf.rect(cx - 7, cy - 26, 14, 20, stroke=0, fill=1)
    pdf.setFillColor(GOLD)
    pdf.circle(cx + 4, cy - 16, 1.6, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#E0E0E0"))
    pdf.rect(cx - 11, cy - 28, 22, 3, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.6)
    pdf.line(cx, cy + 26, cx, cy + 40)
    pdf.setFillColor(TEAL)
    p = pdf.beginPath()
    p.moveTo(cx, cy + 40)
    p.lineTo(cx + 14, cy + 36)
    p.lineTo(cx, cy + 32)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)


def _scene_cat_mat(pdf, cx, cy):
    """A ginger cat sitting upright on a purple mat: pointed
    ears with pink insides, green eyes, a pink nose, white
    whiskers, a striped tail curled around its paws, and a
    mat with a stripe."""
    pdf.setFillColor(HexColor("#B39DDB"))
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(cx - 34, cy - 28, 68, 12, 5, stroke=1, fill=1)
    pdf.setFillColor(HexColor("#7E57C2"))
    pdf.roundRect(cx - 34, cy - 24, 68, 4, 2, stroke=0, fill=1)
    pdf.setFillColor(CAT_ORANGE)
    p = pdf.beginPath()
    p.moveTo(cx - 18, cy - 16)
    p.curveTo(cx - 22, cy + 2, cx - 16, cy + 8, cx - 4, cy + 8)
    p.curveTo(cx + 8, cy + 8, cx + 14, cy + 2, cx + 12, cy - 16)
    p.curveTo(cx + 4, cy - 20, cx - 10, cy - 20, cx - 18, cy - 16)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(CAT_ORANGE)
    pdf.circle(cx - 2, cy + 12, 11, stroke=0, fill=1)
    for ex, sgn in ((cx - 10, -1), (cx + 6, 1)):
        p = pdf.beginPath()
        p.moveTo(ex - 4 * sgn, cy + 18)
        p.lineTo(ex - 6 * sgn, cy + 28)
        p.lineTo(ex + 3 * sgn, cy + 20)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
        pdf.setFillColor(DRESS_PINK)
        p = pdf.beginPath()
        p.moveTo(ex - 3 * sgn, cy + 19)
        p.lineTo(ex - 5 * sgn, cy + 25)
        p.lineTo(ex + 1 * sgn, cy + 20)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
        pdf.setFillColor(CAT_ORANGE)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.circle(cx - 6, cy + 14, 2.8, stroke=0, fill=1)
    pdf.circle(cx + 3, cy + 14, 2.8, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#2E7D32"))
    pdf.circle(cx - 6, cy + 14, 1.5, stroke=0, fill=1)
    pdf.circle(cx + 3, cy + 14, 1.5, stroke=0, fill=1)
    pdf.setFillColor(DRESS_PINK)
    p = pdf.beginPath()
    p.moveTo(cx - 4, cy + 8)
    p.lineTo(cx, cy + 8)
    p.lineTo(cx - 2, cy + 5)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(HexColor("#FFFFFF"))
    pdf.setLineWidth(1)
    pdf.line(cx - 14, cy + 6, cx - 22, cy + 8)
    pdf.line(cx - 14, cy + 4, cx - 22, cy + 2)
    pdf.line(cx + 10, cy + 6, cx + 18, cy + 8)
    pdf.line(cx + 10, cy + 4, cx + 18, cy + 2)
    pdf.setStrokeColor(CAT_DARK)
    pdf.setLineWidth(3)
    pdf.setLineCap(1)
    p = pdf.beginPath()
    p.moveTo(cx + 12, cy - 14)
    p.curveTo(cx + 24, cy - 10, cx + 28, cy + 2, cx + 20, cy + 8)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineCap(0)
    pdf.setStrokeColor(CAT_DARK)
    pdf.setLineWidth(1.6)
    pdf.line(cx - 14, cy - 2, cx - 6, cy - 2)
    pdf.line(cx + 2, cy - 2, cx + 10, cy - 2)


def _scene_apple(pdf, cx, cy):
    """Leo, a boy in a green shirt, holding a shiny red apple
    up to his mouth and taking a bite, with a leaf and stem
    on the apple."""
    _ground(pdf, cx, cy - 28)
    _face(pdf, cx - 6, cy + 14, HAIR_BROWN)
    _shirt(pdf, cx - 6, cy + 2, SHIRT_GREEN, h=20)
    _limb(pdf, cx - 10, cy - 18, cx - 12, cy - 26, PANTS_BLUE, 5)
    _shoe(pdf, cx - 12, cy - 26, color=NAVY)
    _limb(pdf, cx - 2, cy - 18, cx, cy - 26, PANTS_BLUE, 5)
    _shoe(pdf, cx, cy - 26, color=NAVY)
    _limb(pdf, cx + 2, cy - 2, cx + 12, cy + 6, SKIN, 4)
    pdf.setFillColor(APPLE_RED)
    pdf.circle(cx + 16, cy + 8, 10, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.ellipse(cx + 10, cy + 12, cx + 14, cy + 16, stroke=0,
                fill=1)
    pdf.setFillColor(HexColor("#FFF3E0"))
    p = pdf.beginPath()
    p.moveTo(cx + 8, cy + 12)
    p.curveTo(cx + 6, cy + 8, cx + 8, cy + 4, cx + 12, cy + 4)
    p.curveTo(cx + 12, cy + 8, cx + 11, cy + 11, cx + 8, cy + 12)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(LEAF_DARK)
    pdf.setLineWidth(2)
    pdf.line(cx + 16, cy + 17, cx + 16, cy + 23)
    pdf.setFillColor(LEAF)
    pdf.ellipse(cx + 18, cy + 20, cx + 28, cy + 26, stroke=0,
                fill=1)


def _scene_animals(pdf, cx, cy):
    """A cat, a dog, and a bird in a row, for the list. Each
    animal is clearly different: the ginger cat sits upright
    with pointy ears, green eyes, and whiskers; the brown
    dog stands on four legs with floppy ears, a snout, and
    a wagging tail; the blue bird perches on a twig with a
    wing, a beak, and thin legs."""
    _ground(pdf, cx, cy - 26)
    pdf.setFillColor(CAT_ORANGE)
    p = pdf.beginPath()
    p.moveTo(cx - 42, cy - 16)
    p.curveTo(cx - 44, cy + 2, cx - 38, cy + 8, cx - 32, cy + 8)
    p.curveTo(cx - 26, cy + 8, cx - 22, cy + 2, cx - 22, cy - 16)
    p.curveTo(cx - 28, cy - 20, cx - 36, cy - 20, cx - 42, cy - 16)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(CAT_ORANGE)
    pdf.circle(cx - 32, cy + 12, 9, stroke=0, fill=1)
    for ex, sgn in ((cx - 39, -1), (cx - 26, 1)):
        p = pdf.beginPath()
        p.moveTo(ex - 3 * sgn, cy + 17)
        p.lineTo(ex - 5 * sgn, cy + 25)
        p.lineTo(ex + 2 * sgn, cy + 19)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
        pdf.setFillColor(DRESS_PINK)
        p = pdf.beginPath()
        p.moveTo(ex - 2 * sgn, cy + 18)
        p.lineTo(ex - 4 * sgn, cy + 23)
        p.lineTo(ex + 1 * sgn, cy + 19)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
        pdf.setFillColor(CAT_ORANGE)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.circle(cx - 35, cy + 13, 2.4, stroke=0, fill=1)
    pdf.circle(cx - 29, cy + 13, 2.4, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#2E7D32"))
    pdf.circle(cx - 35, cy + 13, 1.3, stroke=0, fill=1)
    pdf.circle(cx - 29, cy + 13, 1.3, stroke=0, fill=1)
    pdf.setFillColor(DRESS_PINK)
    p = pdf.beginPath()
    p.moveTo(cx - 34, cy + 9)
    p.lineTo(cx - 30, cy + 9)
    p.lineTo(cx - 32, cy + 7)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(HexColor("#FFFFFF"))
    pdf.setLineWidth(0.9)
    pdf.line(cx - 40, cy + 8, cx - 46, cy + 10)
    pdf.line(cx - 40, cy + 6, cx - 46, cy + 5)
    pdf.line(cx - 24, cy + 8, cx - 18, cy + 10)
    pdf.line(cx - 24, cy + 6, cx - 18, cy + 5)
    pdf.setStrokeColor(CAT_DARK)
    pdf.setLineWidth(2.6)
    pdf.setLineCap(1)
    p = pdf.beginPath()
    p.moveTo(cx - 22, cy - 14)
    p.curveTo(cx - 14, cy - 10, cx - 12, cy, cx - 16, cy + 6)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineCap(0)
    pdf.setFillColor(DOG_BROWN)
    p = pdf.beginPath()
    p.moveTo(cx - 6, cy + 2)
    p.curveTo(cx - 6, cy + 8, cx + 2, cy + 10, cx + 8, cy + 8)
    p.curveTo(cx + 14, cy + 6, cx + 14, cy, cx + 12, cy - 6)
    p.curveTo(cx + 4, cy - 10, cx - 4, cy - 6, cx - 6, cy + 2)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(DOG_BROWN)
    pdf.circle(cx + 14, cy + 8, 8, stroke=0, fill=1)
    pdf.setFillColor(DOG_BROWN)
    pdf.ellipse(cx + 17, cy + 3, cx + 26, cy + 9, stroke=0, fill=1)
    pdf.setFillColor(DOG_DARK)
    pdf.ellipse(cx + 23, cy + 4, cx + 27, cy + 8, stroke=0, fill=1)
    pdf.setFillColor(DOG_DARK)
    p = pdf.beginPath()
    p.moveTo(cx + 10, cy + 13)
    p.curveTo(cx + 8, cy + 20, cx + 13, cy + 22, cx + 15, cy + 15)
    p.curveTo(cx + 15, cy + 12, cx + 12, cy + 11, cx + 10, cy + 13)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    _limb(pdf, cx - 2, cy - 6, cx - 4, cy - 24, DOG_DARK, 4)
    _limb(pdf, cx + 4, cy - 8, cx + 2, cy - 24, DOG_DARK, 4)
    _limb(pdf, cx + 8, cy - 8, cx + 10, cy - 24, DOG_DARK, 4)
    _limb(pdf, cx + 12, cy - 6, cx + 16, cy - 22, DOG_DARK, 4)
    pdf.setStrokeColor(DOG_DARK)
    pdf.setLineWidth(2.6)
    pdf.setLineCap(1)
    p = pdf.beginPath()
    p.moveTo(cx - 6, cy + 4)
    p.curveTo(cx - 14, cy + 10, cx - 15, cy + 18, cx - 9, cy + 20)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineCap(0)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.circle(cx + 15, cy + 10, 2.6, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.circle(cx + 16, cy + 10, 1.4, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.1)
    pdf.arc(cx + 17, cy, cx + 23, cy + 5, 200, 340)
    pdf.setStrokeColor(TRUNK)
    pdf.setLineWidth(2.4)
    pdf.line(cx + 28, cy - 8, cx + 48, cy - 4)
    pdf.setFillColor(BIRD_BLUE)
    pdf.ellipse(cx + 30, cy, cx + 44, cy + 12, stroke=0, fill=1)
    pdf.circle(cx + 43, cy + 11, 5, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#1E88E5"))
    pdf.ellipse(cx + 31, cy + 2, cx + 38, cy + 9, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FF9800"))
    p = pdf.beginPath()
    p.moveTo(cx + 47, cy + 10)
    p.lineTo(cx + 53, cy + 8)
    p.lineTo(cx + 47, cy + 6)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(BIRD_BLUE)
    p = pdf.beginPath()
    p.moveTo(cx + 31, cy)
    p.lineTo(cx + 24, cy - 5)
    p.lineTo(cx + 33, cy + 3)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.circle(cx + 44, cy + 12, 2.2, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.circle(cx + 45, cy + 12, 1.2, stroke=0, fill=1)
    pdf.setStrokeColor(TRUNK)
    pdf.setLineWidth(1.3)
    pdf.line(cx + 34, cy, cx + 34, cy - 4)
    pdf.line(cx + 39, cy, cx + 39, cy - 4)
    pdf.setFillColor(HexColor("#FF9800"))
    p = pdf.beginPath()
    p.moveTo(cx + 48, cy + 11)
    p.lineTo(cx + 54, cy + 9)
    p.lineTo(cx + 48, cy + 7)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.circle(cx - 24, cy + 13, 1.5, stroke=0, fill=1)
    pdf.circle(cx + 20, cy + 9, 1.5, stroke=0, fill=1)
    pdf.circle(cx + 45, cy + 13, 1.4, stroke=0, fill=1)


def _scene_park(pdf, cx, cy, w=460, h=170):
    """A rich park picture for Page 5: a sunny sky with
    clouds and a red kite, a big apple tree with a bird, a
    swing set with a girl swinging, a slide with a boy
    sliding, a boy flying the kite, a dog chasing a ball, a
    butterfly, flowers, and a bench. Many clear actions
    inspire many different sentences. Drawn inside a box
    of width w and height h centred on (cx, cy)."""
    x0, y0 = cx - w / 2, cy - h / 2
    x1, y1 = cx + w / 2, cy + h / 2
    pdf.setFillColor(HexColor("#E3F2FD"))
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(x0, y0, w, h, 14, stroke=1, fill=1)
    pdf.setFillColor(GRASS)
    pdf.roundRect(x0, y0, w, 46, 8, stroke=0, fill=1)
    pdf.setFillColor(SUN)
    pdf.circle(x0 + 48, y1 - 30, 18, stroke=0, fill=1)
    pdf.setStrokeColor(SUN)
    pdf.setLineWidth(3)
    pdf.setLineCap(1)
    for i in range(8):
        ang = i * math.pi / 4
        pdf.line(x0 + 48 + 23 * math.cos(ang),
                 y1 - 30 + 23 * math.sin(ang),
                 x0 + 48 + 31 * math.cos(ang),
                 y1 - 30 + 31 * math.sin(ang))
    pdf.setLineCap(0)
    pdf.setFillColor(HexColor("#FFFFFF"))
    for ccx, ccy in ((x0 + 120, y1 - 18), (x0 + 300, y1 - 14),
                     (x0 + 400, y1 - 22)):
        pdf.circle(ccx, ccy, 9, stroke=0, fill=1)
        pdf.circle(ccx + 10, ccy + 3, 8, stroke=0, fill=1)
        pdf.circle(ccx - 10, ccy + 2, 7, stroke=0, fill=1)
    pdf.setFillColor(TRUNK)
    pdf.rect(x0 + 380, y0 + 42, 12, 58, stroke=0, fill=1)
    pdf.setFillColor(LEAF)
    pdf.circle(x0 + 386, y1 - 44, 32, stroke=0, fill=1)
    pdf.circle(x0 + 358, y1 - 30, 20, stroke=0, fill=1)
    pdf.circle(x0 + 414, y1 - 30, 20, stroke=0, fill=1)
    pdf.setFillColor(APPLE_RED)
    for ax, ay in ((x0 + 372, y1 - 46), (x0 + 398, y1 - 36),
                   (x0 + 386, y1 - 60)):
        pdf.circle(ax, ay, 4, stroke=0, fill=1)
    pdf.setFillColor(BIRD_BLUE)
    pdf.ellipse(x0 + 356, y1 - 70, x0 + 368, y1 - 60, stroke=0,
                fill=1)
    pdf.circle(x0 + 367, y1 - 60, 4, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FF9800"))
    p = pdf.beginPath()
    p.moveTo(x0 + 371, y1 - 60)
    p.lineTo(x0 + 376, y1 - 62)
    p.lineTo(x0 + 371, y1 - 64)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(2.4)
    pdf.line(x0 + 60, y0 + 46, x0 + 60, y0 + 118)
    pdf.line(x0 + 116, y0 + 46, x0 + 116, y0 + 118)
    pdf.line(x0 + 60, y0 + 118, x0 + 116, y0 + 118)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.6)
    pdf.line(x0 + 76, y0 + 118, x0 + 80, y0 + 88)
    pdf.line(x0 + 100, y0 + 118, x0 + 96, y0 + 88)
    pdf.setFillColor(CORAL)
    pdf.roundRect(x0 + 74, y0 + 82, 28, 6, 3, stroke=0, fill=1)
    pdf.setFillColor(HAIR_BLACK)
    pdf.ellipse(x0 + 76, y0 + 96, x0 + 84, y0 + 114, stroke=0,
                fill=1)
    _face(pdf, x0 + 88, y0 + 100, HAIR_BLACK, r=10)
    _dress(pdf, x0 + 88, y0 + 88, DRESS_PINK, h=16)
    _limb(pdf, x0 + 80, y0 + 74, x0 + 76, y0 + 64, SKIN, 4)
    _shoe(pdf, x0 + 76, y0 + 64, color=NAVY)
    _limb(pdf, x0 + 96, y0 + 74, x0 + 100, y0 + 64, SKIN, 4)
    _shoe(pdf, x0 + 100, y0 + 64, color=NAVY)
    _limb(pdf, x0 + 78, y0 + 90, x0 + 74, y0 + 100, SKIN, 3.5)
    _limb(pdf, x0 + 98, y0 + 90, x0 + 102, y0 + 100, SKIN, 3.5)
    pdf.setFillColor(KITE_RED)
    p = pdf.beginPath()
    p.moveTo(x0 + 220, y1 - 28)
    p.lineTo(x0 + 240, y1 - 48)
    p.lineTo(x0 + 220, y1 - 68)
    p.lineTo(x0 + 200, y1 - 48)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(BALL_YELLOW)
    p = pdf.beginPath()
    p.moveTo(x0 + 220, y1 - 48)
    p.lineTo(x0 + 230, y1 - 48)
    p.lineTo(x0 + 220, y1 - 58)
    p.lineTo(x0 + 210, y1 - 48)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.line(x0 + 220, y1 - 68, x0 + 196, y0 + 96)
    _face(pdf, x0 + 196, y0 + 88, HAIR_BROWN, r=11)
    _shirt(pdf, x0 + 196, y0 + 76, SHIRT_BLUE, h=18)
    _limb(pdf, x0 + 188, y0 + 60, x0 + 186, y0 + 46, PANTS_BLUE,
           5)
    _shoe(pdf, x0 + 186, y0 + 46, color=NAVY)
    _limb(pdf, x0 + 204, y0 + 60, x0 + 206, y0 + 46, PANTS_BLUE,
           5)
    _shoe(pdf, x0 + 206, y0 + 46, color=NAVY)
    _limb(pdf, x0 + 206, y0 + 78, x0 + 218, y0 + 92, SKIN, 4)
    pdf.setFillColor(CORAL)
    p = pdf.beginPath()
    p.moveTo(x0 + 300, y0 + 46)
    p.lineTo(x0 + 300, y0 + 92)
    p.lineTo(x0 + 312, y0 + 92)
    p.lineTo(x0 + 336, y0 + 46)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.rect(x0 + 296, y0 + 92, 4, 30, stroke=0, fill=1)
    pdf.setFillColor(TEAL)
    pdf.rect(x0 + 290, y0 + 122, 16, 4, stroke=0, fill=1)
    _face(pdf, x0 + 306, y0 + 112, HAIR_BROWN, r=10)
    _shirt(pdf, x0 + 306, y0 + 100, SHIRT_GREEN, h=14)
    _limb(pdf, x0 + 300, y0 + 88, x0 + 306, y0 + 76, PANTS_BLUE,
           5)
    _shoe(pdf, x0 + 306, y0 + 76, color=NAVY)
    _limb(pdf, x0 + 312, y0 + 88, x0 + 318, y0 + 76, PANTS_BLUE,
           5)
    _shoe(pdf, x0 + 318, y0 + 76, color=NAVY)
    pdf.setFillColor(DOG_BROWN)
    p = pdf.beginPath()
    p.moveTo(x0 + 250, y0 + 52)
    p.curveTo(x0 + 250, y0 + 60, x0 + 258, y0 + 62, x0 + 266,
              y0 + 60)
    p.curveTo(x0 + 274, y0 + 58, x0 + 276, y0 + 52, x0 + 274,
              y0 + 48)
    p.curveTo(x0 + 266, y0 + 44, x0 + 254, y0 + 46, x0 + 250,
              y0 + 52)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(DOG_BROWN)
    pdf.circle(x0 + 278, y0 + 60, 8, stroke=0, fill=1)
    pdf.setFillColor(DOG_BROWN)
    pdf.ellipse(x0 + 281, y0 + 56, x0 + 289, y0 + 61, stroke=0,
                fill=1)
    pdf.setFillColor(DOG_DARK)
    pdf.ellipse(x0 + 287, y0 + 57, x0 + 290, y0 + 60, stroke=0,
                fill=1)
    pdf.setFillColor(DOG_DARK)
    p = pdf.beginPath()
    p.moveTo(x0 + 272, y0 + 64)
    p.curveTo(x0 + 270, y0 + 70, x0 + 274, y0 + 72, x0 + 276,
              y0 + 67)
    p.curveTo(x0 + 276, y0 + 64, x0 + 274, y0 + 63, x0 + 272,
              y0 + 64)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(DOG_DARK)
    pdf.setLineWidth(2.4)
    pdf.setLineCap(1)
    p = pdf.beginPath()
    p.moveTo(x0 + 250, y0 + 54)
    p.curveTo(x0 + 242, y0 + 58, x0 + 241, y0 + 65, x0 + 246,
              y0 + 67)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setLineCap(0)
    _limb(pdf, x0 + 254, y0 + 46, x0 + 250, y0 + 40, DOG_DARK, 3.5)
    _limb(pdf, x0 + 262, y0 + 46, x0 + 264, y0 + 40, DOG_DARK, 3.5)
    _limb(pdf, x0 + 270, y0 + 46, x0 + 274, y0 + 40, DOG_DARK, 3.5)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.circle(x0 + 280, y0 + 62, 2.2, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.circle(x0 + 281, y0 + 62, 1.2, stroke=0, fill=1)
    pdf.setFillColor(BALL_YELLOW)
    pdf.circle(x0 + 300, y0 + 48, 7, stroke=0, fill=1)
    pdf.setFillColor(BALL_RED)
    pdf.ellipse(x0 + 297, y0 + 43, x0 + 303, y0 + 53, stroke=0,
                fill=1)
    pdf.setFillColor(HexColor("#CE93D8"))
    pdf.ellipse(x0 + 150, y1 - 30, x0 + 158, y1 - 20, stroke=0,
                fill=1)
    pdf.ellipse(x0 + 158, y1 - 30, x0 + 166, y1 - 20, stroke=0,
                fill=1)
    pdf.ellipse(x0 + 150, y1 - 40, x0 + 158, y1 - 30, stroke=0,
                fill=1)
    pdf.ellipse(x0 + 158, y1 - 40, x0 + 166, y1 - 30, stroke=0,
                fill=1)
    pdf.setFillColor(NAVY)
    pdf.circle(x0 + 158, y1 - 30, 2, stroke=0, fill=1)
    pdf.setFillColor(BROWN)
    pdf.rect(x0 + 330, y0 + 46, 44, 5, stroke=0, fill=1)
    pdf.rect(x0 + 330, y0 + 54, 44, 5, stroke=0, fill=1)
    pdf.rect(x0 + 334, y0 + 46, 4, 10, stroke=0, fill=1)
    pdf.rect(x0 + 366, y0 + 46, 4, 10, stroke=0, fill=1)
    for fx, col in ((x0 + 24, CORAL), (x0 + 44, GOLD),
                    (x0 + 140, CORAL), (x0 + 424, CORAL),
                    (x0 + 444, GOLD), (x0 + 240, GOLD)):
        pdf.setFillColor(col)
        pdf.circle(fx, y0 + 54, 4.5, stroke=0, fill=1)
        pdf.setFillColor(LEAF)
        pdf.ellipse(fx - 2, y0 + 46, fx + 2, y0 + 50, stroke=0,
                    fill=1)


# ---------------------------------------------------------------------------
# Page 1 -- Is It a Sentence?
# ---------------------------------------------------------------------------
P1_ITEMS = [
    (os.path.join(IMG_DIR, "p1-dog-running.jpg"),
     [("The dog runs.", True), ("The dog", False)]),
    (os.path.join(IMG_DIR, "p1-girl-reading.jpg"),
     [("Reads a book", False), ("Mia reads a book.", True)]),
    (os.path.join(IMG_DIR, "p1-boy-kicking.jpg"),
     [("Kicks the ball", False), ("Ben kicks the ball.", True)]),
    (os.path.join(IMG_DIR, "p1-two-birds.jpg"),
     [("The birds sing.", True), ("In the tree", False)]),
]


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Is It a Sentence?",
        "Look at each picture. Circle the words that tell a whole idea.")
    pw, ph, gap = 258, 160, 16
    xs = [40, 40 + pw + gap]
    ys = [top - ph, top - ph - gap - ph]
    for i, (image, options) in enumerate(P1_ITEMS):
        x = xs[i % 2]
        y = ys[i // 2]
        _panel(pdf, x, y, pw, ph)
        cx = x + pw / 2
        if "girl-reading" in image:
            # Mia's picture is a tall portrait. In the standard
            # box its lower edge reached the answer text, so
            # it is drawn a little smaller and higher here.
            _draw_image(pdf, image, cx, y + 118, 100, 80)
        else:
            _draw_image(pdf, image, cx, y + 110, 100, 92)
        oy = y + 58
        for text, _is_sentence in options:
            _circle_choice(pdf, x + 24, oy + 4)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica", 13)
            pdf.drawString(x + 40, oy, text)
            oy -= 26
    ry = 120
    _panel(pdf, 40, ry, 532, 118)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, ry + 94, "Remember")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, ry + 66,
        "A sentence tells a whole idea.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, ry + 42,
        "It tells us something that makes sense by itself.")
    _adult_line(pdf, "Ask: who is it about, and what happens?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Start Big, End with a Mark
# ---------------------------------------------------------------------------
P2_ROWS = [
    (os.path.join(IMG_DIR, "p2-sun.jpg"), "the sun is up", "The sun is up."),
    (os.path.join(IMG_DIR, "p2-red-ball.jpg"), "where is my red ball", "Where is my red ball?"),
    (os.path.join(IMG_DIR, "p2-child-bike.jpg"), "i love my new bike", "I love my new bike!"),
    (os.path.join(IMG_DIR, "p2-child-jumping.jpg"), "sam can jump high", "Sam can jump high."),
]


def _fix_row(pdf, y, h, image, broken, bold_parts=()):
    """One fix-it row: picture at left, broken sentence, and a
    ruled line for the rewrite. bold_parts is a set of words
    to draw bold (lowercase) so the child sees what to fix."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, image, 100, y + h / 2 + 2, 96, h - 8)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 14)
    if bold_parts:
        words = broken.split(" ")
        x = 160
        for w in words:
            bold = w.strip(".,") in bold_parts
            pdf.setFont("Helvetica-Bold" if bold else "Helvetica",
                        14)
            pdf.drawString(x, y + h - 38, w)
            x += stringWidth(w, "Helvetica-Bold" if bold else
                             "Helvetica", 14) + stringWidth(
                                 " ", "Helvetica", 14)
    else:
        pdf.drawString(160, y + h - 38, broken)
    _ruled_line(pdf, 160, 552, y + 30)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Start Big, End with a Mark",
        "Fix each sentence. Start with a big letter. "
        "End with the right mark.")
    rh, gap = 112, 12
    y = top - rh
    for image, broken, _fixed in P2_ROWS:
        _fix_row(pdf, y, rh, image, broken)
        y -= rh + gap
    _adult_line(pdf, "Say the sentence aloud, then write it "
                     "with a big letter and a mark.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Names and Dates
# ---------------------------------------------------------------------------
P3_ROWS = [
    (os.path.join(IMG_DIR, "p1-girl-reading.jpg"), "mia likes to read on sunday",
     {"mia", "sunday"}, "Mia likes to read on Sunday."),
    (os.path.join(IMG_DIR, "p3-birthday-cake.jpg"), "ben was born on march 3 2026",
     {"ben", "march"}, "Ben was born on March 3, 2026."),
    (os.path.join(IMG_DIR, "p3-kids-playing.jpg"), "ava and noah play on friday",
     {"ava", "noah", "friday"}, "Ava and Noah play on Friday."),
    (os.path.join(IMG_DIR, "p3-school-v2.jpg"), "school starts on august 24 2026",
     {"school", "august"}, "School starts on August 24, 2026."),
]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Names and Dates",
        "Fix each sentence. Names and dates start with a big letter.\n"
        "Add a comma between the day and year in full dates. "
        "End with the right mark.")
    rh, gap = 106, 12
    y = top - rh
    for image, broken, bold_parts, _fixed in P3_ROWS:
        _fix_row(pdf, y, rh, image, broken, bold_parts=bold_parts)
        y -= rh + gap
    _adult_line(pdf, "Names of people, days, and months all "
                     "start with a big letter.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Build a Clear Sentence
# ---------------------------------------------------------------------------
def _word_cards(pdf, x, y, words, size=12, max_w=392):
    """Draw word cards in a row, wrapping to a second line.
    Each card is a small rounded rectangle with the word in
    it. Returns the y of the next free line below the cards.
    The cards carry NO punctuation: for the list item, the
    child must insert the commas when writing."""
    cx = x
    top_y = y
    for w in words:
        ww = stringWidth(w, "Helvetica-Bold", size) + 18
        if cx + ww > x + max_w and cx > x:
            cx = x
            top_y -= 32
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(BOX_STROKE)
        pdf.setLineWidth(1.1)
        pdf.roundRect(cx, top_y - 22, ww, 26, 7, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", size)
        pdf.drawCentredString(cx + ww / 2, top_y - 14, w)
        cx += ww + 8
    return top_y - 34


P4_ITEMS = [
    (os.path.join(IMG_DIR, "p4-cat-mat.jpg"),
     ["mat", "The", "on", "cat", "sits", "the"],
     "The cat sits on the mat.", False),
    (os.path.join(IMG_DIR, "p4-boy-apple.jpg"),
     ["apple", "eats", "an", "Leo"],
     "Leo eats an apple.", False),
    (os.path.join(IMG_DIR, "p4-three-animals.jpg"),
     ["see", "I", "cat", "a", "dog", "a", "and", "bird", "a"],
     "I see a cat, a dog, and a bird.", True),
]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Build a Clear Sentence",
        "Put the words in order. Write a clear sentence.\n"
        "For a list, add a comma after each thing but the last.")
    ih, gap = 140, 14
    y = top - ih
    for image, words, _answer, is_list in P4_ITEMS:
        _panel(pdf, 40, y, 532, ih)
        _draw_image(pdf, image, 96, y + 76, 96, 124)
        _word_cards(pdf, 160, y + ih - 26, words)
        if is_list:
            pdf.setFillColor(ADULT_GREY)
            pdf.setFont("Helvetica-Oblique", 11)
            pdf.drawString(160, y + ih - 96, "Add the commas.")
        _ruled_line(pdf, 160, 552, y + 26)
        y -= ih + gap
    _adult_line(pdf, "Read the words aloud in order before writing.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Write Your Own Sentences
# ---------------------------------------------------------------------------
def _writing_area(pdf, y, h, label):
    """A generous writing area: a panel with a label and two
    ruled lines."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(56, y + h - 24, label)
    _ruled_line(pdf, 56, 556, y + h - 52)
    _ruled_line(pdf, 56, 556, y + h - 80)


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Write Your Own Sentences",
        "Look at the picture. Write two sentences about it.")
    # The park is a full 3:2 watercolor scene, so it is shown
    # whole (381 by 254) rather than cropped. The writing
    # areas stay generous (two ruled lines each) and the
    # self-check keeps its three boxes; the panel heights
    # are trimmed a little to make room for the taller park.
    _draw_image(pdf, os.path.join(IMG_DIR, "park-scene-v2.jpg"),
                PAGE_WIDTH / 2, top - 127, 381, 254)
    _writing_area(pdf, 254, 92, "Sentence 1")
    _writing_area(pdf, 156, 92, "Sentence 2")
    _panel(pdf, 40, 54, 532, 96)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 132,
                          "Check your sentences:")
    checks = ["Did I start with a capital?",
              "Did I end with a mark?",
              "Did I tell a whole idea?"]
    cy = 108
    for text in checks:
        pdf.setStrokeColor(BOX_STROKE)
        pdf.setLineWidth(1.4)
        pdf.rect(96, cy - 4, 13, 13, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(118, cy, text)
        cy -= 22
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Parent Guide
# ---------------------------------------------------------------------------
def _guide_header(pdf):
    """The brand header for the Parent Guide, without the
    Name and Date fields (this page is for the adult, not
    the child). Uses the short pack title so it fits."""
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, stroke=0, fill=1)
    draw_logo(pdf, 60, PAGE_HEIGHT - 86)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1)
    pdf.line(218, PAGE_HEIGHT - 88, 218, PAGE_HEIGHT - 48)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(234, PAGE_HEIGHT - 68, "Sentences That Work")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(234, PAGE_HEIGHT - 90, "Parent Guide")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.6)
    pdf.line(60, PAGE_HEIGHT - 104, PAGE_WIDTH - 60,
             PAGE_HEIGHT - 104)


def _wrap_lines(text, font, size, max_w):
    """Wrap a paragraph to the given width. Returns a list
    of lines."""
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _guide_text(pdf, x, y, text, font="Helvetica", size=12,
                max_w=500, leading=15):
    """Draw a wrapped paragraph. Returns the y below it."""
    for line in _wrap_lines(text, font, size, max_w):
        pdf.setFont(font, size)
        pdf.drawString(x, y, line)
        y -= leading
    return y


GUIDE_TITLE = "How to Use This Pack"
GUIDE_INTRO = ("This pack teaches your child what makes a "
               "sentence work: it tells a whole idea, starts "
               "with a capital letter, and ends with a mark.")
GUIDE_SECTIONS = [
    ("How to help", [
        "Page 1: ask, does it tell a whole idea?",
        "Page 2: say the sentence aloud, then write it with a "
        "big letter and a mark.",
        "Page 3: point to each name and date. They start with a "
        "big letter.",
        "Page 4: read the cards in order first. For the list, "
        "ask where the commas go.",
        "Page 5: let your child choose what to write.",
    ]),
    ("What your child learns", [
        "A sentence tells a whole idea and makes sense by "
        "itself. It starts with a capital and ends with a mark. "
        "Names and dates start with a big letter. Lists need "
        "commas.",
    ]),
    ("Answers", [
        ("Page 1", "The dog runs. / Mia reads a book. / Ben "
                   "kicks the ball. / The birds sing."),
        ("Page 2", "The sun is up. / Where is my red ball? / I "
                   "love my new bike! / Sam can jump high."),
        ("Page 3", "Mia likes to read on Sunday. / Ben was born "
                   "on March 3, 2026. / Ava and Noah play on "
                   "Friday. / School starts on August 24, 2026."),
        ("Page 4", "The cat sits on the mat. / Leo eats an "
                   "apple. / I see a cat, a dog, and a bird."),
        ("Page 5", "Two sentences of their own. Check for a "
                   "capital, an end mark, and a whole idea."),
    ]),
    ("Help a beginning writer", [
        "Let your child say the sentence aloud before writing it.",
        "Sound out words slowly. Spelling a word the way it "
        "sounds is fine.",
        "Praise the capital and the end mark first, then fix "
        "spelling together.",
        "Keep it short and cheerful. If the hand gets tired, "
        "take a break.",
    ]),
    ("If your child finds it hard", [
        "Page 4: lay the cards in order first, then write. Count "
        "the things and ask where each comma goes.",
    ]),
]


def build_parent_guide(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _guide_header(pdf)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 656, GUIDE_TITLE)
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 586, 532, 54, 14, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    y = _guide_text(pdf, 56, 622, GUIDE_INTRO, size=12,
                    max_w=500, leading=15)
    y = 574
    for heading, items in GUIDE_SECTIONS:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(40, y, heading)
        y -= 17
        pdf.setFillColor(NAVY)
        if heading == "Answers":
            for label, text in items:
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(56, y, label + ":")
                lw = stringWidth(label + ": ", "Helvetica-Bold",
                                 12)
                y = _guide_text(pdf, 56 + lw, y, text, size=12,
                                max_w=500 - lw, leading=15)
                y -= 2
        else:
            for para in items:
                y = _guide_text(pdf, 56, y, para, size=12,
                                max_w=500, leading=15)
                y -= 1
        y -= 10
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 58,
        "Grade 1 Reading: Sentences That Work. "
        "For parents, not for the child.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _build_bundle(path):
    from reportlab.pdfgen import canvas as _canvas
    tmp = []
    builders = [build_p1_page, build_p2_page, build_p3_page,
                build_p4_page, build_p5_page]
    for i, builder in enumerate(builders):
        p = os.path.join(OUT_DIR, "_tmp_p%d.pdf" % (i + 1))
        builder(p)
        tmp.append(p)
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in tmp:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    with open(path, "wb") as f:
        writer.write(f)
    for p in tmp:
        os.remove(p)


def main():
    from pypdf import PdfReader, PdfWriter
    os.makedirs(OUT_DIR, exist_ok=True)
    bundle = os.path.join(OUT_DIR, "sentences-that-work.pdf")
    guide = os.path.join(
        OUT_DIR, "sentences-that-work-parent-guide.pdf")
    review = os.path.join(
        OUT_DIR, "sentences-that-work-review.pdf")
    _build_bundle(bundle)
    build_parent_guide(guide)
    writer = PdfWriter()
    for src in (bundle, guide):
        for page in PdfReader(src).pages:
            writer.add_page(page)
    with open(review, "wb") as f:
        writer.write(f)
    # Individual per-page PDFs, split losslessly from the final
    # bundle (pypdf copies each page object verbatim, so the
    # vector text and pictures are identical to the combined
    # pack). Never build these from the raster preview PNGs.
    page_names = ["is-it-a-sentence", "start-big-end-with-a-mark",
                  "names-and-dates", "build-a-clear-sentence",
                  "write-your-own-sentences"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR, "sentences-that-work-p%d-%s.pdf"
            % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    for name in ["sentences-that-work.pdf",
                 "sentences-that-work-parent-guide.pdf",
                 "sentences-that-work-review.pdf",
                 "sentences-that-work-p1-is-it-a-sentence.pdf",
                 "sentences-that-work-p2-start-big-end-with-a-mark.pdf",
                 "sentences-that-work-p3-names-and-dates.pdf",
                 "sentences-that-work-p4-build-a-clear-sentence.pdf",
                 "sentences-that-work-p5-write-your-own-sentences.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text.
    for name in ["sentences-that-work.pdf",
                 "sentences-that-work-parent-guide.pdf"]:
        text = "".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
    print("em dash check: clean")


if __name__ == "__main__":
    main()
