#!/usr/bin/env python3
"""Grade 1 Reading - Two-Syllable Words (RF.1.3(e), RF.1.3(d)).

Resource 10 in the approved Grade 1 Reading roadmap (Tier 2 core).
The child splits printed two-syllable words into syllables and
reads them, and counts syllables in printed words by listening
for vowel sounds. Every syllable uses a pattern taught in
Resources 1-3, so the child decodes one part at a time.

Plan approved 2026-11-16, with two refinements from the user:
  1. Page 2 teaches that every syllable has a vowel SOUND.
     It does NOT suggest counting vowel letters: "Rain" has two
     vowel letters but one sound, so one syllable; "Cake" has a
     silent e, so one syllable. The child listens for vowel
     sounds, never circles vowel letters to count them.
  2. Page 3 divisions are linguistically correct and helpful
     for decoding, with one modeled example before independent
     practice. Model: rab | bit. Divisions: pen | cil,
     bas | ket, lem | on, mit | ten, chick | en, pump | kin.
     All are VC/CV divisions between two consonants, except
     lemon (lem | on, closed first syllable, short e), which is
     the correct and helpful division.

v2 (2026-11-16), the user's two corrections to the approved v1:
  1. Page 3 model now shows the division INSIDE the complete
     printed word (rab|bit, divider inside "rabbit"), so the
     child sees exactly where to draw their line. The arrow
     and the separate whole word are gone.
  2. Page 4 instruction is now the user's exact wording:
     "Read each sentence. Split the green word into two
     syllables. Then draw a line to the matching picture."
     The 18pt sentences give enough room to mark the split,
     so no layout change was needed. Pages 1, 2, and the
     parent guide are unchanged in v2.

Decoding audit (General American, phonemes not letters), verified
against Resources 1-3 (short vowels; blends; digraphs sh, ch,
th, wh, ph; final-e; vowel teams ai, ay, ee, ea, oa, ow as long
o only) plus familiar high-frequency words and inflectional -s:
  P1: sunshine (sun, short u; shine, sh + final-e long i),
      cupcake (cup, short u; cake, final-e long a),
      rainbow (rain, ai; bow, ow as long o),
      snowman (snow, ow as long o; man, short a). All decodable.
  P2: rain (ai), cake (final-e), ship (sh + short i),
      frog (fr blend + short o), rabbit (short a + short i),
      pencil (short e + short i), basket (short a + short e),
      lemon (short e + short o). All decodable.
  P3: pencil, basket, lemon, mitten (short i + short e),
      chicken (ch + short i, ck + short e; ck in Resource 1),
      pumpkin (short u + mp blend, short i). All decodable.
  P4: "The rabbit hops in the sun." (hops is hop + -s),
      "Mom has a red pencil." (red, short e),
      "I see a big basket." (see is a high-frequency word),
      "The kitten is in the box." (kitten, short i + short e;
      box, short o). All decodable.

Syllable-division audit: P1 sun-shine, cup-cake, rain-bow,
snow-man (compound words, split at the word boundary). P2 counts
rain 1, cake 1, ship 1, frog 1, rabbit 2, pencil 2, basket 2,
lemon 2. P3 rab-bit, pen-cil, bas-ket, lem-on, mit-ten,
chick-en, pump-kin. P4 target words rabbit, pencil, basket,
kitten. Every division matches the approved list.

Shared design code (logo, header, footer, circular-masked
pictures) is imported verbatim from build_phonics_az.py - do not
fork it here.

Pictures: 15 new in assets/two-syllable-words/ (tsw-sunshine,
tsw-cupcake, tsw-rainbow, tsw-snowman, tsw-rain, tsw-cake,
tsw-ship, tsw-pencil, tsw-basket, tsw-lemon, tsw-mitten,
tsw-chicken, tsw-pumpkin, tsw-rabbit-sun, tsw-kitten-box),
watercolor picture-book style, all JPEG. Two approved animal
library pictures are reused: animal-library/lib-rabbit.jpg and
animal-library/lib-frog.jpg.
"""
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter as _letter  # noqa: F401
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from build_phonics_az import (NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              _img_circle, draw_footer, draw_header,
                              draw_logo)

TITLE = "Two-Syllable Words"
SUBTITLE = "Grade 1 Reading | Phonics and Word Reading"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "two-syllable-words")


def _adult_line(pdf, text):
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 74, text)


def _page_title(pdf, title, instruction):
    """Page title at 642 and instruction line(s) below it.
    Returns the y of the top of the content area: 606 for a
    one-line instruction, 592 for a two-line instruction."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, title)
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


def _split_parts(pdf, part1, part2, cx, y, font_size=20):
    """Two syllables on one line with a clear vertical divider
    between them. Returns nothing; draws in navy bold."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", font_size)
    w1 = stringWidth(part1, "Helvetica-Bold", font_size)
    pdf.drawString(cx - 12 - w1, y, part1)
    pdf.drawString(cx + 12, y, part2)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(cx, y - 3, cx, y + font_size * 0.75)


def _whole_word_split(pdf, part1, part2, cx, y, font_size=20):
    """A complete printed word with a vertical divider drawn
    INSIDE it at the syllable split, so the child sees exactly
    where to draw their own line. The two parts are drawn
    touching, so the word reads whole; the teal line marks the
    split. Returns nothing; draws in navy bold."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", font_size)
    w1 = stringWidth(part1, "Helvetica-Bold", font_size)
    w2 = stringWidth(part2, "Helvetica-Bold", font_size)
    x = cx - (w1 + w2) / 2
    pdf.drawString(x, y, part1)
    pdf.drawString(x + w1, y, part2)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(x + w1, y - 3, x + w1, y + font_size * 0.75)


def _resp_square(pdf, cx, cy, size=34):
    """Empty square for the child to write 1 or 2, with a small
    "syllables" label beneath it."""
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.5)
    pdf.roundRect(cx - size / 2, cy - size / 2, size, size, 4,
                  stroke=1, fill=1)
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(cx, cy - size / 2 - 12, "syllables")


def _arrow(pdf, x1, x2, y):
    """A short right-pointing arrow: a line plus a filled
    triangle at the end."""
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(x1, y, x2, y)
    p = pdf.beginPath()
    p.moveTo(x2 + 12, y)
    p.lineTo(x2, y - 6)
    p.lineTo(x2, y + 6)
    p.close()
    pdf.setFillColor(TEAL)
    pdf.drawPath(p, stroke=0, fill=1)


def _sentence(pdf, parts, x, y, font_size=17):
    """A sentence drawn word by word. parts is a list of
    (text, is_target); the target word is drawn in teal, the
    rest in navy. Text includes any trailing punctuation."""
    pdf.setFont("Helvetica-Bold", font_size)
    cx = x
    for text, is_target in parts:
        pdf.setFillColor(TEAL if is_target else NAVY)
        pdf.drawString(cx, y, text)
        cx += stringWidth(text, "Helvetica-Bold", font_size)
        cx += stringWidth(" ", "Helvetica-Bold", font_size)


# ---------------------------------------------------------------------------
# Page 1 -- Split It and Read It (RF.1.3(e), guided)
# Compound words, shown split with a clear break. The child reads
# each part, then reads the whole word. The adult models the
# first one. 2x2 grid of large pictures.
# ---------------------------------------------------------------------------
P1_ITEMS = [
    (("sun", "shine"), "sunshine", "two-syllable-words/tsw-sunshine.jpg"),
    (("cup", "cake"), "cupcake", "two-syllable-words/tsw-cupcake.jpg"),
    (("rain", "bow"), "rainbow", "two-syllable-words/tsw-rainbow.jpg"),
    (("snow", "man"), "snowman", "two-syllable-words/tsw-snowman.jpg"),
]


def _split_and_read(pdf):
    top = _page_title(
        pdf, "Split It and Read It",
        "Read each part. Then read the whole word.")
    # 2x2 grid: panels 256 wide x 235 tall.
    panel_w, panel_h = 256, 235
    xs = [40, 316]
    tops = [top, top - 255]
    for i, ((part1, part2), whole, img) in enumerate(P1_ITEMS):
        x0 = xs[i % 2]
        ptop = tops[i // 2]
        _panel(pdf, x0, ptop - panel_h, panel_w, panel_h)
        cx = x0 + panel_w / 2
        _img_circle(pdf, img, cx, ptop - 72, 55, zoom=True)
        _split_parts(pdf, part1, part2, cx, ptop - 168, font_size=20)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(cx, ptop - 198, whole)
    _adult_line(pdf, "Adult: Read the first word with your child. "
                     "Then your child reads the rest.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, TITLE, SUBTITLE)
    _split_and_read(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- How Many Syllables? (RF.1.3(d), guided)
# Refinement 1: every syllable has a vowel SOUND. The teaching
# box says so plainly and shows why counting vowel letters
# would be wrong ("Rain" has two vowel letters but one sound;
# "Cake" has a silent e). The child says each word slowly,
# listens for the vowel sounds, and writes 1 or 2. No circling
# of vowel letters anywhere on this page.
# ---------------------------------------------------------------------------
P2_TEACH = [
    "Every syllable has a vowel sound.",
    "Say the word slowly and listen for the vowel sounds.",
    "'Rain' has two vowel letters, but they make one sound,",
    "so it has one syllable. 'Cake' has a silent e at the",
    "end, so it has one syllable.",
]
# (word, image, syllable count) - rows alternate 1 and 2 so the
# child cannot guess a pattern from the layout.
P2_ITEMS = [
    ("rain", "two-syllable-words/tsw-rain.jpg", 1),
    ("rabbit", "animal-library/lib-rabbit.jpg", 2),
    ("cake", "two-syllable-words/tsw-cake.jpg", 1),
    ("pencil", "two-syllable-words/tsw-pencil.jpg", 2),
    ("ship", "two-syllable-words/tsw-ship.jpg", 1),
    ("basket", "two-syllable-words/tsw-basket.jpg", 2),
    ("frog", "animal-library/lib-frog.jpg", 1),
    ("lemon", "two-syllable-words/tsw-lemon.jpg", 2),
]


def _how_many(pdf):
    top = _page_title(
        pdf, "How Many Syllables?",
        "Say each word slowly. Listen for the vowel sounds.\n"
        "Write 1 or 2 in each box.")
    # Teaching box: 5 lines, heading bold teal, body navy.
    box_top, box_h = top, 100
    _panel(pdf, 40, box_top - box_h, 532, box_h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, box_top - 20, P2_TEACH[0])
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    y = box_top - 40
    for line in P2_TEACH[1:]:
        pdf.drawString(56, y, line)
        y -= 16
    # 2 columns x 4 rows of word cells, 256 wide x 84 tall.
    panel_w, panel_h = 256, 84
    xs = [40, 316]
    tops = [box_top - box_h - 16 - i * 94 for i in range(4)]
    for i, (word, img, _count) in enumerate(P2_ITEMS):
        x0 = xs[i % 2]
        ptop = tops[i // 2]
        _panel(pdf, x0, ptop - panel_h, panel_w, panel_h)
        cy = ptop - panel_h / 2
        _img_circle(pdf, img, x0 + 42, cy, 30, zoom=True)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(x0 + 84, cy - 6, word)
        _resp_square(pdf, x0 + 222, cy + 6)
    _adult_line(pdf, "Adult: Say each word slowly with your child. "
                     "Listen for the vowel sounds together.")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, TITLE, SUBTITLE)
    _how_many(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Split the Word (RF.1.3(e), guided to independent)
# Refinement 2: one modeled example before independent
# practice. v2: the division is shown INSIDE the complete
# printed word (rab|bit, divider inside "rabbit"), so the child
# sees exactly where to draw their own line. No arrow, no
# separate whole word. Six non-compound words; the child draws
# the split line, reads each part, then reads the whole word.
# The picture beside each word lets the child check the word as
# they read. All divisions are linguistically correct and
# helpful for decoding: VC/CV between two consonants, except
# lemon (lem | on, closed first syllable, short e).
# ---------------------------------------------------------------------------
P3_ITEMS = [
    ("pencil", "two-syllable-words/tsw-pencil.jpg"),
    ("basket", "two-syllable-words/tsw-basket.jpg"),
    ("lemon", "two-syllable-words/tsw-lemon.jpg"),
    ("mitten", "two-syllable-words/tsw-mitten.jpg"),
    ("chicken", "two-syllable-words/tsw-chicken.jpg"),
    ("pumpkin", "two-syllable-words/tsw-pumpkin.jpg"),
]


def _split_word(pdf):
    top = _page_title(
        pdf, "Split the Word",
        "Draw a line to split each word. "
        "Read each part, then read the whole word.")
    # Model panel: the complete word with the split line drawn
    # inside it, so the child sees exactly where to draw their
    # own line. No arrow, no separate whole word.
    box_top, box_h = top, 106
    _panel(pdf, 40, box_top - box_h, 532, box_h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, box_top - 20, "Try it like this:")
    # Model row, centred: "rabbit" printed whole, with the teal
    # divider between "rab" and "bit" inside the word.
    my = box_top - 58
    _whole_word_split(pdf, "rab", "bit", PAGE_WIDTH / 2, my,
                      font_size=20)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(PAGE_WIDTH / 2, box_top - 84,
                          "Read each part, then read the whole word.")
    # 2 columns x 3 rows of word cells, 256 wide x 116 tall.
    panel_w, panel_h = 256, 116
    xs = [40, 316]
    tops = [box_top - box_h - 16 - i * 126 for i in range(3)]
    for i, (word, img) in enumerate(P3_ITEMS):
        x0 = xs[i % 2]
        ptop = tops[i // 2]
        _panel(pdf, x0, ptop - panel_h, panel_w, panel_h)
        cy = ptop - panel_h / 2
        _img_circle(pdf, img, x0 + 48, cy, 34, zoom=True)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(x0 + 100, cy - 8, word)
    _adult_line(pdf, "Adult: Show the split in the example first. "
                     "Then your child splits the rest.")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, TITLE, SUBTITLE)
    _split_word(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Read It in a Sentence (RF.1.3(e), independent)
# Four short decodable sentences, each with one two-syllable
# word (drawn in teal). v2 instruction, the user's exact
# wording: "Read each sentence. Split the green word into two
# syllables. Then draw a line to the matching picture." The
# child draws a short vertical line inside the green word to
# mark the split, then draws a line to the picture that
# matches. Pictures are scrambled so no sentence matches
# straight across. The 18pt sentences give enough room to mark
# the split, so no layout change was needed beyond the
# instruction text.
# ---------------------------------------------------------------------------
P4_SENTENCES = [
    [("The", False), ("rabbit", True), ("hops", False),
     ("in", False), ("the", False), ("sun.", False)],
    [("Mom", False), ("has", False), ("a", False),
     ("red", False), ("pencil.", True)],
    [("I", False), ("see", False), ("a", False),
     ("big", False), ("basket.", True)],
    [("The", False), ("kitten", True), ("is", False),
     ("in", False), ("the", False), ("box.", False)],
]
# Picture order, scrambled against the sentence order above:
# basket, kitten, rabbit hopping in the sun, red pencil.
P4_PICTURES = [
    "two-syllable-words/tsw-basket.jpg",
    "two-syllable-words/tsw-kitten-box.jpg",
    "two-syllable-words/tsw-rabbit-sun.jpg",
    "two-syllable-words/tsw-pencil.jpg",
]


def _read_sentence(pdf):
    _page_title(
        pdf, "Read It in a Sentence",
        "Read each sentence. Split the green word into two syllables.\n"
        "Then draw a line to the matching picture.")
    rows_y = [552, 424, 296, 168]
    for i, (parts, img) in enumerate(zip(P4_SENTENCES, P4_PICTURES)):
        cy = rows_y[i]
        _sentence(pdf, parts, 60, cy - 6, font_size=18)
        # Match dots: one at the end of the sentence side, one
        # at the picture side, so the child can draw the line.
        pdf.setFillColor(TEAL)
        pdf.circle(352, cy + 2, 4, stroke=0, fill=1)
        pdf.circle(442, cy + 2, 4, stroke=0, fill=1)
        _img_circle(pdf, img, 500, cy, 50, zoom=True)
    _adult_line(pdf, "Adult: Let your child read alone. "
                     "Help with the two-syllable words if needed.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, TITLE, SUBTITLE)
    _read_sentence(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Split It and Read It", build_p1_page),
    ("How Many Syllables?", build_p2_page),
    ("Split the Word", build_p3_page),
    ("Read It in a Sentence", build_p4_page),
]


# ---------------------------------------------------------------------------
# Parent guide and answer key (separate one-page PDF, NOT in the
# student bundle). Plain language for parents, no standards
# codes. The syllable divisions are listed so a parent can
# check them: parents may not know the correct divisions.
# ---------------------------------------------------------------------------
GUIDE_TITLE = "How to Use This Pack"
GUIDE_INTRO = [
    "Two-syllable words are easier when your child reads one",
    "part at a time. Say the word slowly, listen for the vowel",
    "sounds, and split the word between its syllables.",
]
GUIDE_SECTIONS = [
    ("How to help", [
        "Say the word slowly. Listen for the vowel sounds.",
        "Every syllable has a vowel sound.",
        "Split the word between the syllables.",
        "Read each part, then read the whole word.",
    ]),
    ("A note about counting syllables", [
        "Count vowel sounds, not vowel letters.",
        "'Rain' has two vowel letters, but they make one sound,",
        "so it has one syllable.",
        "'Cake' has a silent e at the end, so it has one syllable.",
    ]),
    ("Answers: Page 1, Split It and Read It", [
        "sun-shine, cup-cake, rain-bow, snow-man",
    ]),
    ("Answers: Page 2, How Many Syllables?", [
        "rain 1, cake 1, ship 1, frog 1",
        "rabbit 2, pencil 2, basket 2, lemon 2",
    ]),
    ("Answers: Page 3, Split the Word", [
        "rab-bit, pen-cil, bas-ket, lem-on,",
        "mit-ten, chick-en, pump-kin",
    ]),
    ("Answers: Page 4, Read It in a Sentence", [
        "rabbit, pencil, basket, kitten",
    ]),
    ("If your child finds it hard", [
        "Cover one part of the word. Read the part you can see.",
        "Say the word slowly together, then let your child",
        "try it alone.",
        "Go back to Page 1 and read the compound words again.",
    ]),
]


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
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(234, PAGE_HEIGHT - 68, TITLE)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(234, PAGE_HEIGHT - 90, "Parent Guide")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.6)
    pdf.line(60, PAGE_HEIGHT - 104, PAGE_WIDTH - 60, PAGE_HEIGHT - 104)


def build_parent_guide(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _guide_header(pdf)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640, GUIDE_TITLE)
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 570, 532, 56, 14, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    y = 610
    for line in GUIDE_INTRO:
        pdf.drawString(56, y, line)
        y -= 15
    y = 554
    for heading, lines in GUIDE_SECTIONS:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(40, y, heading)
        y -= 16
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 11.5)
        for line in lines:
            pdf.drawString(56, y, line)
            y -= 15
        y -= 8
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 58,
        "Grade 1 Reading: Two-Syllable Words. "
        "For parents, not for the child.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def main():
    """Build v2 (2026-11-16). Pages 1 and 2 are unchanged from
    v1 and are read in as built; only Pages 3 and 4 are rebuilt
    (Page 3 model now shows the split inside the complete word;
    Page 4 has the new two-line instruction). The parent guide
    is unchanged and is NOT rebuilt here."""
    os.makedirs(OUT_DIR, exist_ok=True)
    p3 = os.path.join(OUT_DIR, "two-syllable-words-page-03-v2.pdf")
    build_p3_page(p3)
    print("built page 3 (v2): Split the Word")
    p4 = os.path.join(OUT_DIR, "two-syllable-words-page-04-v2.pdf")
    build_p4_page(p4)
    print("built page 4 (v2): Read It in a Sentence")
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for name in ("two-syllable-words-page-01-v1.pdf",
                 "two-syllable-words-page-02-v1.pdf",
                 "two-syllable-words-page-03-v2.pdf",
                 "two-syllable-words-page-04-v2.pdf"):
        path = os.path.join(OUT_DIR, name)
        for page in PdfReader(path).pages:
            writer.add_page(page)
    bundle = os.path.join(OUT_DIR, "two-syllable-words-v2.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 4
    print("bundle: %s (4 pages)" % bundle)


if __name__ == "__main__":
    main()
