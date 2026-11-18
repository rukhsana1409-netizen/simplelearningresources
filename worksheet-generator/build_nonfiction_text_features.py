#!/usr/bin/env python3
"""Grade 1 Reading - Nonfiction Text Features.

Resource 15 in the approved and locked Grade 1 Reading and
Language Arts roadmap (audit 2026-11-05). Plan approved
2026-11-18. Placement: Grade 1 / Reading & Language /
Informational Reading. Standards RI.1.5 and RI.1.7:
RI.1.5 covers the text features (contents, headings,
glossary, icons) on Pages 1 to 3, and RI.1.7 covers the
Picture or Words activity on Page 4, where the child uses
the illustrations and the details in the text to describe
the key ideas. (RI.1.6 was listed in the first build and
corrected to RI.1.7 on 2026-11-18.)

One coherent mini nonfiction book, "All About the Seasons",
runs through all four pages, so the contents, headings,
glossary, and icons are consistent everywhere, as a real
book would be.

The book:
  Contents: Spring page 2, Summer page 3, Fall page 4,
  Winter page 5.
  Headings and facts:
    Spring: "In spring, flowers bloom."
    Summer: "In summer, the days are long and hot."
    Fall: "In fall, leaves turn red, yellow, and orange."
    Winter: "In winter, snow falls."
  Glossary:
    bloom: "A flower opens up."
    harvest: "Farmers pick food when it is ready."
    frost: "A thin coat of ice on cold grass and leaves."
  Icons:
    magnifying glass: "Look closely."
    star: "A big fact to remember."
    arrow: "See that page."

Pages:
  P1: Meet the Text Features. A sample page from the book
      shows all four features. The child draws a line from
      each feature name to the feature on the page.
  P2: Find It Fast. Use the Contents and the headings to
      find the page for each fact. Answers: snow page 5,
      flowers page 2, leaves turning red page 4, long hot
      days page 3.
  P3: Words to Know. Match each bold glossary word in a
      sentence to its meaning, then match each icon to its
      job. Glossary order is bloom, harvest, frost; the
      sentences are shuffled (harvest, frost, bloom) so
      position gives nothing away. Icon jobs are shuffled
      the same way.
  P4: Picture or Words? Six facts, each with a picture and
      a sentence. The child circles Picture, Words, or Both.
      Two picture-only, two words-only, two both, mixed in
      order so no pattern gives the answer away. Every
      picture is vector-drawn so its content is exact: the
      fall tree shows red leaves only (red is consistent
      with the sentence, but yellow and orange are only in
      the words, so the words-only answer stays
      unambiguous); the pumpkin picture has no farmer in
      it; the flower picture shows a closed bud beside open
      flowers so blooming is visible in the picture; and
      the snow picture shows flakes falling with motion
      dashes, so the two Both answers are unambiguous.
      Answers: 1. Picture, 2. Words, 3. Both, 4. Picture,
      5. Words, 6. Both.

No printable answer key. The Parent Guide is the only
extra download and carries the answers. No em dash
anywhere in the student pages or the guide.

Shared design code (logo, header, footer) is imported
verbatim from build_phonics_az.py. Do not fork it here.
Header title is drawn at 18pt and the subtitle at 14pt;
both end inside the teal rule (title 211pt, subtitle
287pt, limit 318pt).
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

TITLE = "Nonfiction Text Features"
SUBTITLE = "Grade 1 Reading | Nonfiction Text Features"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")
SKY = HexColor("#D6EAF8")
GRASS = HexColor("#A8D5A2")
SUN = HexColor("#F7C948")
LEAF = HexColor("#4CAF50")
LEAF_DARK = HexColor("#388E3C")
FALL_RED = HexColor("#D32F2F")
FALL_RED_DARK = HexColor("#9C1F1F")
TRUNK = HexColor("#8D6E63")
SNOW = HexColor("#F4F8FB")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "nonfiction-text-features")

CHAPTERS = [
    ("Spring", 2, "In spring, flowers bloom."),
    ("Summer", 3, "In summer, the days are long and hot."),
    ("Fall", 4, "In fall, leaves turn red, yellow, and orange."),
    ("Winter", 5, "In winter, snow falls."),
]

GLOSSARY = [
    ("bloom", "A flower opens up."),
    ("harvest", "Farmers pick food when it is ready."),
    ("frost", "A thin coat of ice on cold grass and leaves."),
]

ICON_JOBS = [
    ("glass", "Look closely."),
    ("star", "A big fact to remember."),
    ("arrow", "See that page."),
]

# Page 3 sentences, shuffled against the glossary order
# (glossary: bloom, harvest, frost; sentences: harvest,
# frost, bloom) so position gives nothing away.
P3_SENTENCES = [
    ("Farmers", "harvest", "pumpkins in fall."),
    ("There is", "frost", "on the grass in winter."),
    ("The flowers", "bloom", "in spring."),
]

# Page 3 icon jobs, shuffled against the icon order
# (icons: glass, star, arrow; jobs: arrow, glass, star).
P3_JOB_ORDER = ["See that page.", "Look closely.",
                "A big fact to remember."]

# Page 2 questions: (question, page number).
P2_QUESTIONS = [
    ("Which page tells about snow?", 5),
    ("Which page tells about flowers?", 2),
    ("Which page tells about leaves turning red?", 4),
    ("Which page tells about long, hot days?", 3),
]

# Page 4 rows: (scene, sentence, question, answer).
# Two picture-only, two words-only, two both, mixed.
P4_ROWS = [
    ("snowman",
     "In winter, children build snowmen.",
     "What color is the snowman's scarf?",
     "Picture"),
    ("tree",
     "In fall, leaves turn red, yellow, and orange.",
     "What colors do the leaves turn?",
     "Words"),
    ("flowers_bloom",
     "In spring, flowers bloom.",
     "What do flowers do in spring?",
     "Both"),
    ("beach",
     "In summer, the days are long and hot.",
     "What is on the sand?",
     "Picture"),
    ("pumpkin",
     "In fall, farmers harvest pumpkins.",
     "Who harvests the pumpkins?",
     "Words"),
    ("snow",
     "In winter, snow falls.",
     "What falls in winter?",
     "Both"),
]


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


def _write_line(pdf, cx, y, w=52):
    """A write-in line centred on cx."""
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.line(cx - w / 2, y, cx + w / 2, y)


# ---------------------------------------------------------------------------
# Icons (vector). Each draws centred on (cx, cy) at about the
# given radius r.
# ---------------------------------------------------------------------------
def _icon_glass(pdf, cx, cy, r=13, color=NAVY):
    pdf.setStrokeColor(color)
    pdf.setLineWidth(2.2)
    pdf.circle(cx - 2, cy + 2, r - 4, stroke=1, fill=0)
    pdf.line(cx + 6, cy - 6, cx + r + 2, cy - r - 2)


def _icon_star(pdf, cx, cy, r=14, color=GOLD):
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang),
                    cy + rr * math.sin(ang)))
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(color)
    pdf.setStrokeColor(HexColor("#D99A1F"))
    pdf.setLineWidth(1)
    pdf.drawPath(p, stroke=1, fill=1)


def _icon_arrow(pdf, cx, cy, w=26, color=TEAL):
    pdf.setStrokeColor(color)
    pdf.setFillColor(color)
    pdf.setLineWidth(2.4)
    pdf.line(cx - w / 2, cy, cx + w / 2 - 8, cy)
    p = pdf.beginPath()
    p.moveTo(cx + w / 2 + 4, cy)
    p.lineTo(cx + w / 2 - 8, cy + 7)
    p.lineTo(cx + w / 2 - 8, cy - 7)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)


def _draw_icon(pdf, kind, cx, cy, r=13):
    if kind == "glass":
        _icon_glass(pdf, cx, cy, r)
    elif kind == "star":
        _icon_star(pdf, cx, cy, r)
    else:
        _icon_arrow(pdf, cx, cy, w=2 * r)


# ---------------------------------------------------------------------------
# Page 4 picture scenes (vector). Each draws inside a box
# centred on (cx, cy), about 110 wide and 62 tall. The
# content is exact: the tree is red leaves only, the pumpkin
# picture has no person, the beach ball sits on the sand
# with the sun in the sky, and the snowman's scarf is red.
# ---------------------------------------------------------------------------
def _scene_snowman(pdf, cx, cy):
    # Snow ground.
    pdf.setFillColor(SNOW)
    pdf.setStrokeColor(HexColor("#D9E7F0"))
    pdf.setLineWidth(1)
    pdf.roundRect(cx - 52, cy - 30, 104, 12, 6, stroke=1, fill=1)
    # Body: three white circles.
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(HexColor("#B9CBD8"))
    pdf.setLineWidth(1.2)
    pdf.circle(cx, cy - 12, 15, stroke=1, fill=1)
    pdf.circle(cx, cy + 6, 11, stroke=1, fill=1)
    pdf.circle(cx, cy + 20, 8, stroke=1, fill=1)
    # Stick arms.
    pdf.setStrokeColor(TRUNK)
    pdf.setLineWidth(1.6)
    pdf.line(cx - 11, cy + 6, cx - 24, cy + 14)
    pdf.line(cx + 11, cy + 6, cx + 24, cy + 14)
    # Black top hat.
    pdf.setFillColor(HexColor("#2B2B2B"))
    pdf.setStrokeColor(HexColor("#2B2B2B"))
    pdf.rect(cx - 6, cy + 26, 12, 10, stroke=0, fill=1)
    pdf.rect(cx - 10, cy + 25, 20, 2.5, stroke=0, fill=1)
    # Eyes and carrot nose.
    pdf.setFillColor(HexColor("#2B2B2B"))
    pdf.circle(cx - 3, cy + 22, 1.4, stroke=0, fill=1)
    pdf.circle(cx + 3, cy + 22, 1.4, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#F07F13"))
    p = pdf.beginPath()
    p.moveTo(cx + 1, cy + 19)
    p.lineTo(cx + 12, cy + 17)
    p.lineTo(cx + 1, cy + 16)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    # Red scarf: band plus a tail.
    pdf.setFillColor(HexColor("#D32F2F"))
    pdf.setStrokeColor(HexColor("#D32F2F"))
    pdf.rect(cx - 11, cy + 11, 22, 5, stroke=0, fill=1)
    pdf.rect(cx + 6, cy - 2, 5, 13, stroke=0, fill=1)
    # Buttons.
    pdf.setFillColor(HexColor("#2B2B2B"))
    pdf.circle(cx, cy + 8, 1.4, stroke=0, fill=1)
    pdf.circle(cx, cy - 2, 1.4, stroke=0, fill=1)
    pdf.circle(cx, cy - 12, 1.4, stroke=0, fill=1)


def _scene_tree(pdf, cx, cy):
    # Grass.
    pdf.setFillColor(GRASS)
    pdf.setStrokeColor(HexColor("#8FBE8B"))
    pdf.setLineWidth(1)
    pdf.roundRect(cx - 52, cy - 30, 104, 12, 6, stroke=1, fill=1)
    # Trunk.
    pdf.setFillColor(TRUNK)
    pdf.setStrokeColor(TRUNK)
    pdf.rect(cx - 4, cy - 18, 8, 22, stroke=0, fill=1)
    # Canopy: red leaves only. The sentence says the leaves
    # turn red, yellow, and orange, so a green canopy would
    # contradict it. Red alone is consistent with the
    # sentence but does not give away yellow and orange, so
    # the full list of colors is still only in the words.
    pdf.setFillColor(FALL_RED)
    pdf.setStrokeColor(FALL_RED_DARK)
    pdf.setLineWidth(1)
    pdf.circle(cx - 13, cy + 8, 13, stroke=1, fill=1)
    pdf.circle(cx + 13, cy + 8, 13, stroke=1, fill=1)
    pdf.circle(cx, cy + 20, 14, stroke=1, fill=1)
    pdf.setFillColor(FALL_RED_DARK)
    pdf.circle(cx - 6, cy + 12, 2, stroke=0, fill=1)
    pdf.circle(cx + 8, cy + 16, 2, stroke=0, fill=1)
    pdf.circle(cx, cy + 24, 2, stroke=0, fill=1)


def _scene_flowers(pdf, cx, cy, bud_first=False):
    # Grass.
    pdf.setFillColor(GRASS)
    pdf.setStrokeColor(HexColor("#8FBE8B"))
    pdf.setLineWidth(1)
    pdf.roundRect(cx - 52, cy - 30, 104, 12, 6, stroke=1, fill=1)
    colors = [HexColor("#F48FB1"), HexColor("#FFD54F"),
              HexColor("#BA68C8")]
    for i, col in enumerate(colors):
        fx = cx - 28 + i * 28
        # Stem and leaves.
        pdf.setStrokeColor(LEAF_DARK)
        pdf.setLineWidth(2)
        pdf.line(fx, cy - 18, fx, cy + 8)
        pdf.setFillColor(LEAF)
        pdf.setStrokeColor(LEAF_DARK)
        pdf.setLineWidth(1)
        pdf.ellipse(fx - 8, cy - 10, fx - 1, cy - 4,
                    stroke=1, fill=1)
        if bud_first and i == 0:
            # A closed bud on the first stem: the picture
            # shows a bud opening into a flower, so the
            # action "bloom" is visible in the picture, not
            # only in the words. This makes the Both answer
            # unambiguous on Page 4.
            pdf.setFillColor(col)
            pdf.setStrokeColor(HexColor("#C2185B"))
            pdf.setLineWidth(1)
            p = pdf.beginPath()
            p.moveTo(fx, cy + 20)
            p.curveTo(fx - 6, cy + 14, fx - 5, cy + 6,
                      fx, cy + 5)
            p.curveTo(fx + 5, cy + 6, fx + 6, cy + 14,
                      fx, cy + 20)
            p.close()
            pdf.drawPath(p, stroke=1, fill=1)
            continue
        # Five petals around a gold centre.
        pdf.setFillColor(col)
        pdf.setStrokeColor(col)
        for a in range(5):
            ang = a * 2 * math.pi / 5 + math.pi / 2
            px = fx + 7 * math.cos(ang)
            py = cy + 14 + 7 * math.sin(ang)
            pdf.circle(px, py, 5, stroke=0, fill=1)
        pdf.setFillColor(SUN)
        pdf.circle(fx, cy + 14, 4, stroke=0, fill=1)


def _scene_flowers_bloom(pdf, cx, cy):
    """Flowers with a closed bud on the first stem, used only
    for the Page 4 Both question so the picture itself shows
    blooming. Page 1 keeps the plain three-open-flowers
    picture."""
    _scene_flowers(pdf, cx, cy, bud_first=True)


def _scene_beach(pdf, cx, cy):
    # Sky and sun.
    pdf.setFillColor(SKY)
    pdf.setStrokeColor(HexColor("#BFDDF0"))
    pdf.setLineWidth(1)
    pdf.roundRect(cx - 52, cy - 30, 104, 62, 8, stroke=1, fill=1)
    pdf.setFillColor(SUN)
    pdf.setStrokeColor(HexColor("#E8A90C"))
    pdf.setLineWidth(1.4)
    pdf.circle(cx + 34, cy + 18, 9, stroke=1, fill=1)
    for a in range(8):
        ang = a * math.pi / 4
        pdf.line(cx + 34 + 11 * math.cos(ang),
                 cy + 18 + 11 * math.sin(ang),
                 cx + 34 + 15 * math.cos(ang),
                 cy + 18 + 15 * math.sin(ang))
    # Sand.
    pdf.setFillColor(HexColor("#F5D98B"))
    pdf.setStrokeColor(HexColor("#E3C078"))
    pdf.roundRect(cx - 52, cy - 30, 104, 16, 6, stroke=1, fill=1)
    # Beach ball on the sand: striped circle via clip.
    bx, by, br = cx - 8, cy - 6, 13
    pdf.saveState()
    p = pdf.beginPath()
    p.circle(bx, by, br)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.setFillColor(HexColor("#EF5350"))
    pdf.rect(bx - br, by - br, 2 * br / 3, 2 * br,
             stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFEB3B"))
    pdf.rect(bx - br / 3, by - br, 2 * br / 3, 2 * br,
             stroke=0, fill=1)
    pdf.setFillColor(HexColor("#42A5F5"))
    pdf.rect(bx + br / 3, by - br, 2 * br / 3, 2 * br,
             stroke=0, fill=1)
    pdf.restoreState()
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.circle(bx, by, br, stroke=1, fill=0)


def _scene_pumpkin(pdf, cx, cy):
    # Porch step.
    pdf.setFillColor(HexColor("#BCAAA4"))
    pdf.setStrokeColor(HexColor("#A1887F"))
    pdf.setLineWidth(1)
    pdf.roundRect(cx - 52, cy - 30, 104, 12, 6, stroke=1, fill=1)
    # Pumpkin body: orange ellipse with ridge lines.
    pdf.setFillColor(HexColor("#FB8C00"))
    pdf.setStrokeColor(HexColor("#E65100"))
    pdf.setLineWidth(1.2)
    pdf.ellipse(cx - 24, cy - 18, cx + 24, cy + 18,
                stroke=1, fill=1)
    pdf.setStrokeColor(HexColor("#E65100"))
    pdf.setLineWidth(1)
    pdf.ellipse(cx - 12, cy - 18, cx + 12, cy + 18,
                stroke=1, fill=0)
    # Stem.
    pdf.setFillColor(HexColor("#558B2F"))
    pdf.setStrokeColor(HexColor("#558B2F"))
    pdf.rect(cx - 3, cy + 16, 6, 8, stroke=0, fill=1)


def _scene_snow(pdf, cx, cy):
    # Sky.
    pdf.setFillColor(SKY)
    pdf.setStrokeColor(HexColor("#BFDDF0"))
    pdf.setLineWidth(1)
    pdf.roundRect(cx - 52, cy - 30, 104, 62, 8, stroke=1, fill=1)
    # Snow ground.
    pdf.setFillColor(SNOW)
    pdf.setStrokeColor(HexColor("#D9E7F0"))
    pdf.roundRect(cx - 52, cy - 30, 104, 12, 6, stroke=1, fill=1)
    # House: red walls, dark roof with snow on top.
    pdf.setFillColor(HexColor("#C62828"))
    pdf.setStrokeColor(HexColor("#8E0000"))
    pdf.setLineWidth(1)
    pdf.rect(cx - 20, cy - 18, 40, 26, stroke=1, fill=1)
    p = pdf.beginPath()
    p.moveTo(cx - 24, cy + 8)
    p.lineTo(cx, cy + 24)
    p.lineTo(cx + 24, cy + 8)
    p.close()
    pdf.setFillColor(HexColor("#4E342E"))
    pdf.drawPath(p, stroke=1, fill=1)
    # Snow on the roof edge.
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(HexColor("#FFFFFF"))
    pdf.roundRect(cx - 24, cy + 6, 48, 4, 2, stroke=0, fill=1)
    # Door.
    pdf.setFillColor(HexColor("#6D4C41"))
    pdf.rect(cx - 5, cy - 18, 10, 16, stroke=0, fill=1)
    # Falling snowflakes, larger and with short downward
    # dashes under three of them, so the picture clearly
    # shows snow FALLING, not only snow sitting on the roof.
    # This makes the Both answer unambiguous on Page 4.
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(HexColor("#90CAF9"))
    pdf.setLineWidth(0.8)
    flakes = [(cx - 38, cy + 22), (cx - 28, cy + 8),
              (cx + 30, cy + 20), (cx + 38, cy + 2),
              (cx - 40, cy - 8), (cx + 14, cy + 26)]
    for fx, fy in flakes:
        pdf.circle(fx, fy, 3, stroke=1, fill=1)
    pdf.setStrokeColor(HexColor("#64B5F6"))
    pdf.setLineWidth(1.2)
    for fx, fy in [(cx - 38, cy + 22), (cx + 30, cy + 20),
                   (cx + 14, cy + 26)]:
        pdf.line(fx, fy - 5, fx, fy - 10)


def _draw_scene(pdf, kind, cx, cy):
    if kind == "snowman":
        _scene_snowman(pdf, cx, cy)
    elif kind == "tree":
        _scene_tree(pdf, cx, cy)
    elif kind == "flowers":
        _scene_flowers(pdf, cx, cy)
    elif kind == "flowers_bloom":
        _scene_flowers_bloom(pdf, cx, cy)
    elif kind == "beach":
        _scene_beach(pdf, cx, cy)
    elif kind == "pumpkin":
        _scene_pumpkin(pdf, cx, cy)
    else:
        _scene_snow(pdf, cx, cy)

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


# ---------------------------------------------------------------------------
# Page 1 -- Meet the Text Features
# ---------------------------------------------------------------------------
def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Meet the Text Features",
        "This is a page from All About the Seasons.\n"
        "Find each part. Draw a line to its name.")
    # Sample book page panel.
    px, py, pw, ph = 40, 315, 532, 268
    _panel(pdf, px, py, pw, ph)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(PAGE_WIDTH / 2, py + ph - 24,
                          "All About the Seasons")
    # Contents box, top left of the sample page.
    cx0, cy0, cw, ch = 60, 430, 200, 118
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.2)
    pdf.roundRect(cx0, cy0, cw, ch, 10, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(cx0 + cw / 2, cy0 + ch - 22, "Contents")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    yy = cy0 + ch - 44
    for name, pg, _fact in CHAPTERS:
        pdf.drawString(cx0 + 14, yy, name)
        pdf.drawRightString(cx0 + cw - 14, yy, str(pg))
        yy -= 20
    # Page number at the bottom left, as a real book has.
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(cx0 + cw / 2, py + 16, "Page 2")
    # Heading, sentence, and icon on the right of the sample page.
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(416, 512, "Spring")
    _draw_mixed_centred(
        pdf, [("In spring, the flowers ", False),
              ("bloom", True), (".", False)],
        416, 478, size=13)
    _icon_glass(pdf, 520, 478, r=13)
    # A small flower picture, as a real book page has.
    _scene_flowers(pdf, 416, 400)
    # A small glossary entry at the bottom of the sample page,
    # so the child can see where the bold word "bloom" is
    # explained. There is NO line from the bold word to the
    # entry: the child draws their own matching line from
    # the Glossary Word card to the bold word, as the
    # activity asks. (A thin connecting line was added in
    # the first revision and removed 2026-11-18 at her
    # direction, so the child does the matching.) The box
    # sits in the free strip below the flowers, so the page
    # is not crowded.
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.2)
    pdf.roundRect(340, 322, 220, 40, 8, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(352, 350, "Glossary")
    _draw_mixed_left(pdf, [("bloom", True),
                           (": A flower opens up.", False)],
                     352, 335, size=11)
    # Feature name cards, in the same left-to-right order as
    # the features appear on the sample page, so the lines
    # the child draws do not tangle.
    cards = [
        ("Table of Contents", "Tells you what is in the book."),
        ("Heading", "Tells you what a part is about."),
        ("Glossary Word", "A bold word. Find it in the glossary."),
        ("Icon", "A small picture that tells you what to do."),
    ]
    cw2, ch2, gut = 125, 118, 10.67
    for i, (name, what) in enumerate(cards):
        x0 = 40 + i * (cw2 + gut)
        y0 = 175
        _panel(pdf, x0, y0, cw2, ch2)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12)
        # Wrap the name on two lines if needed.
        if stringWidth(name, "Helvetica-Bold", 12) <= cw2 - 12:
            pdf.drawCentredString(x0 + cw2 / 2, y0 + ch2 - 22, name)
            wy = y0 + ch2 - 44
        else:
            w1, w2 = name.split(" ", 1)
            pdf.drawCentredString(x0 + cw2 / 2, y0 + ch2 - 22, w1)
            pdf.drawCentredString(x0 + cw2 / 2, y0 + ch2 - 38, w2)
            wy = y0 + ch2 - 58
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica", 10.5)
        words = what.split(" ")
        lines = []
        cur = ""
        for wd in words:
            if stringWidth(cur + " " + wd, "Helvetica", 10.5) <= cw2 - 14:
                cur = (cur + " " + wd).strip()
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        for ln in lines:
            pdf.drawCentredString(x0 + cw2 / 2, wy, ln)
            wy -= 14
        # A teal dot at the bottom of the card marks where the
        # child starts the line to the feature on the page.
        pdf.setFillColor(TEAL)
        pdf.circle(x0 + cw2 / 2, y0 + 16, 4, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(PAGE_WIDTH / 2, 148,
                          "You found all four parts of a nonfiction book.")
    _adult_line(pdf, "Point to each part as you name it.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Find It Fast
# ---------------------------------------------------------------------------
def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Find It Fast",
        "Use the Contents to find the page.\n"
        "Write the page number on the line.")
    # Contents box at the top.
    cx0, cy0, cw, ch = 156, 496, 300, 84
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.2)
    pdf.roundRect(cx0, cy0, cw, ch, 10, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(cx0 + cw / 2, cy0 + ch - 20, "Contents")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    # Two columns of two chapters.
    for i, (name, pg, _fact) in enumerate(CHAPTERS):
        col = i % 2
        row = i // 2
        x = cx0 + 24 + col * 150
        y = cy0 + ch - 42 - row * 20
        pdf.drawString(x, y, name)
        pdf.drawRightString(x + 96, y, str(pg))
    # Four heading panels, 2 by 2.
    pw2, ph2 = 258, 82
    for i, (name, pg, fact) in enumerate(CHAPTERS):
        col = i % 2
        row = i // 2
        x0 = 40 + col * (pw2 + 16)
        y0 = 392 - row * (ph2 + 12)
        _panel(pdf, x0, y0, pw2, ph2)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(x0 + pw2 / 2, y0 + ph2 - 26, name)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 11.5)
        pdf.drawCentredString(x0 + pw2 / 2, y0 + 22, fact)
    # Four questions, each with a write-in line.
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    y = 284
    for q, _pg in P2_QUESTIONS:
        pdf.drawString(60, y, q)
        _write_line(pdf, 500, y, w=44)
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(528, y, "page")
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 12.5)
        y -= 42
    _adult_line(pdf, "Let your child use the Contents, not memory.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Words to Know
# ---------------------------------------------------------------------------
def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Words to Know",
        "Read the bold word. Draw a line to what it means.\n"
        "Then match each picture to what it tells you to do.")
    # Glossary box on the left.
    gx, gy, gw, gh = 40, 372, 252, 208
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.2)
    pdf.roundRect(gx, gy, gw, gh, 10, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(gx + gw / 2, gy + gh - 24, "Glossary")
    # Three glossary entries, each word plus its meaning.
    ey = gy + gh - 52
    for word, meaning in GLOSSARY:
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(gx + 14, ey, word)
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica", 11)
        # Wrap the meaning to two lines.
        words = meaning.split(" ")
        lines = []
        cur = ""
        for wd in words:
            if stringWidth(cur + " " + wd, "Helvetica", 11) <= gw - 28:
                cur = (cur + " " + wd).strip()
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        yy = ey - 16
        for ln in lines:
            pdf.drawString(gx + 14, yy, ln)
            yy -= 14
        ey -= 62
    # Sentences on the right, shuffled against the glossary.
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(316, gy + gh - 24, "Read each sentence.")
    sy = gy + gh - 56
    for before, word, after in P3_SENTENCES:
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(316, sy, before)
        x = 316 + stringWidth(before + " ", "Helvetica", 12)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, sy, word)
        x += stringWidth(word + " ", "Helvetica-Bold", 12)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, sy, after)
        sy -= 62
    # Icons section.
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(PAGE_WIDTH / 2, 330, "Icons")
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 11.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 312,
        "Each picture tells you what to do. Draw a line to its job.")
    # Three icons on the left, three jobs on the right, shuffled.
    iy = 280
    for kind, _job in ICON_JOBS:
        _draw_icon(pdf, kind, 110, iy, r=13)
        iy -= 68
    jy = 280
    for job in P3_JOB_ORDER:
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 12.5)
        pdf.drawString(360, jy - 4, job)
        jy -= 68
    _adult_line(pdf, "Say the word and its meaning together.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Picture or Words?
# ---------------------------------------------------------------------------
def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Picture or Words?",
        "Look at the picture and read the words.\n"
        "Where did you learn the answer? Circle one.")
    cell_w, cell_h = 258, 150
    for i, (scene, sentence, question, _ans) in enumerate(P4_ROWS):
        col = i % 2
        row = i // 2
        x0 = 40 + col * (cell_w + 16)
        y0 = 435 - row * (cell_h + 10)
        _panel(pdf, x0, y0, cell_w, cell_h)
        cx = x0 + cell_w / 2
        # Picture at the top of the cell.
        _draw_scene(pdf, scene, cx, y0 + cell_h - 38)
        # Sentence, then the question in bold.
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 11)
        pdf.drawCentredString(cx, y0 + 62, sentence)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(cx, y0 + 44, question)
        # Three choice pills: Picture, Words, Both.
        pills = ["Picture", "Words", "Both"]
        pw = 76
        start_x = cx - (3 * pw + 2 * 6) / 2
        for j, label in enumerate(pills):
            px0 = start_x + j * (pw + 6)
            py0 = y0 + 10
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(BOX_STROKE)
            pdf.setLineWidth(1.2)
            pdf.roundRect(px0, py0, pw, 24, 12, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 11.5)
            pdf.drawCentredString(px0 + pw / 2, py0 + 8, label)
    _adult_line(pdf, "Ask: did the picture show it, or did the words say it?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()

# ---------------------------------------------------------------------------
# Parent Guide (separate one-page guide, NOT in the student bundle)
# ---------------------------------------------------------------------------
def _guide_header(pdf):
    """Brand header for the parent guide, WITHOUT the Name/Date
    fields: the guide is for adults, not a student page. This
    replicates draw_header minus the Name/Date block; the shared
    draw_header (and build_phonics_az.py) is untouched, and
    student pages keep their Name/Date fields."""
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, stroke=0, fill=1)
    draw_logo(pdf, 60, PAGE_HEIGHT - 86)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1)
    pdf.line(218, PAGE_HEIGHT - 88, 218, PAGE_HEIGHT - 48)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(234, PAGE_HEIGHT - 68, TITLE)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(234, PAGE_HEIGHT - 90, "Parent Guide")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.6)
    pdf.line(60, PAGE_HEIGHT - 104, PAGE_WIDTH - 60,
             PAGE_HEIGHT - 104)


GUIDE_TITLE = "How to Use This Pack"
GUIDE_INTRO = [
    "This pack teaches your child to use the parts of a",
    "nonfiction book to find facts fast, and to tell whether",
    "a fact came from a picture or from the words.",
]

GUIDE_SECTIONS = [
    ("How to help", [
        "On Page 1, name each part together, then let your",
        "child draw the lines.",
        "On Page 2, let your child use the Contents, not memory.",
        "On Page 3, say each word and its meaning together.",
        "On Page 4, ask: did the picture show it, or did the",
        "words say it? Let your child circle one answer.",
    ]),
    ("The book in this pack", [
        "All About the Seasons. Contents: Spring page 2,",
        "Summer page 3, Fall page 4, Winter page 5.",
        "Glossary: bloom means a flower opens up; harvest",
        "means farmers pick food when it is ready; frost",
        "means a thin coat of ice on cold grass and leaves.",
        "Icons: a magnifying glass means look closely; a star",
        "means a big fact to remember; an arrow means see that page.",
    ]),
    ("Answers", [
        "Page 1: Table of Contents to the Contents box;",
        "Heading to Spring; Glossary Word to bloom; Icon to",
        "the magnifying glass.",
        "Page 2: snow page 5, flowers page 2, leaves turning",
        "red page 4, long hot days page 3.",
        "Page 3: bloom means a flower opens up; harvest means",
        "farmers pick food when it is ready; frost means a thin",
        "coat of ice on cold grass and leaves. Magnifying",
        "glass means look closely; star means a big fact to",
        "remember; arrow means see that page.",
        "Page 4: 1. Picture, 2. Words, 3. Both, 4. Picture,",
        "5. Words, 6. Both.",
    ]),
    ("If your child finds it hard", [
        "On Page 4, cover the words and ask what the picture",
        "shows. Then cover the picture and read the words.",
        "That makes it clear which one gave the answer.",
    ]),
]


def build_parent_guide(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _guide_header(pdf)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640, GUIDE_TITLE)
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 566, 532, 60, 14, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    y = 606
    for line in GUIDE_INTRO:
        pdf.drawString(56, y, line)
        y -= 15
    y = 550
    for heading, lines in GUIDE_SECTIONS:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(40, y, heading)
        y -= 16
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 11.5)
        for line in lines:
            pdf.drawString(56, y, line)
            y -= 14
        y -= 8
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 58,
        "Grade 1 Reading: Nonfiction Text Features. "
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
                build_p4_page]
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
    bundle = os.path.join(OUT_DIR, "nonfiction-text-features.pdf")
    guide = os.path.join(
        OUT_DIR, "nonfiction-text-features-parent-guide.pdf")
    review = os.path.join(
        OUT_DIR, "nonfiction-text-features-review.pdf")
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
    page_names = ["meet-the-text-features", "find-it-fast",
                  "words-to-know", "picture-or-words"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR, "nonfiction-text-features-p%d-%s.pdf"
            % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    for name in ["nonfiction-text-features.pdf",
                 "nonfiction-text-features-parent-guide.pdf",
                 "nonfiction-text-features-review.pdf",
                 "nonfiction-text-features-p1-meet-the-text-features.pdf",
                 "nonfiction-text-features-p2-find-it-fast.pdf",
                 "nonfiction-text-features-p3-words-to-know.pdf",
                 "nonfiction-text-features-p4-picture-or-words.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text.
    for name in ["nonfiction-text-features.pdf",
                 "nonfiction-text-features-parent-guide.pdf"]:
        text = "".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
    print("em dash check: clean")


if __name__ == "__main__":
    main()
