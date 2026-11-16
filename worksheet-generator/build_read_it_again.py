#!/usr/bin/env python3
"""Grade 1 Reading - Read It Again! Reading Fluency (RF.1.4).

Decodable fluency pack (RF.1.4(a)-(c), RF.1.3(b)). Five short
passages, each read and reread, with one fluency activity per page.
No timed reading, no words-per-minute targets, no speed pressure.

Plan approved 2026-11-09, build approved 2026-11-16. All five
pages and the separate one-page parent fluency guide built together
for one comprehensive review. No lock, handoff, integration, or
publish until the user approves the finished pack.

v2 (2026-11-16, user corrections): P2 line 3 "The ship is on the
sand." -> "The ship is by the sand." (her exact wording; "by" is
already in the passage, so no new word is introduced and the
45-word count is unchanged); one brief comprehension check after
the fluency activity on every student page (P5 keeps its lunch
question); P2 model scoop arcs measured with stringWidth and
verified exactly under "The ship" and "is big."; P3 snake
illustration regenerated larger and clearly visible; parent guide
header without Name/Date fields (guide only, student pages keep
them). Reading font sizes, line spacing, and layout preserved.

Decoding audit (General American, phonemes not letters), verified
against Resources 1-3 (blends; digraphs sh, ch, th, wh, ph;
final-e; vowel teams ai, ay, ee, ea, oa, ow as long o only) plus
high-frequency words and inflectional -s (RF.1.3(f)):
  P1: 31 words, all decodable. CVC, blends, high-frequency words,
      -s endings only. No changes.
  P2: 45 words, all decodable. Adds digraphs sh, th. No changes.
      (Plan said 41 words; the passage as written is 45.)
      v2: line 3 "The ship is on the sand." -> "The ship is by
      the sand." (user's exact wording). "by" already occurs in
      the passage ("A fish swims by the ship."), so no new word
      is introduced and decodability and the 45-word count are
      unchanged.
  P3: 38 words. One change: "long" (ng not taught) -> "big".
      "The snake is long." -> "The snake is big."
  P4: 41 words. Five changes, all for vowel teams not taught in
      Resource 3 (oo, ou, oy, and ow as the sound in cow):
      roof -> grass, sound -> tap ("The rain taps on the glass."),
      toys -> blocks, tower -> stack, out -> back.
      "The rain falls on the roof." -> "The rain falls on the
      grass." "The rain makes a soft sound." -> "The rain taps on
      the glass." "We play with toys." -> "We play with blocks."
      "We make a tall tower." -> "We make a tall stack."
      "We go out and play." -> "We go back and play."
      (Plan said 40 words; the passage as written is 41, and the
      revised passage is also 41.)
  P5: 36 words. One change: "good" (oo as in book, not taught)
      -> "nice" (final-e). "It is a good lunch." -> "It is a
      nice lunch." (Plan said 37 words; the passage as written
      is 36.)
  "pick" (ck) is decodable: ck appears in Resource 1 ("rock").
  "lunch" (ch) was a Resource 2 example word. "long" was the
  only ng word; it is gone. Double consonants (ll, ss) spell
  one sound and do not change the sound.

Shared design code (logo, header, footer, circular-masked
pictures) is imported verbatim from build_phonics_az.py - do not
fork it here. The passage box follows build_read_and_think.py.

Pictures: 5 new in assets/read-it-again/ (ria-dog-pond,
ria-ship-fish, ria-bike-snake, ria-rain-blocks,
ria-garden-beans), watercolor picture-book style, all JPEG.
"""
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter as _letter  # noqa: F401
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from build_phonics_az import (NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              _img_circle, draw_footer, draw_header,
                              draw_logo)

TITLE = "Read It Again!"
SUBTITLE = "Grade 1 Reading | Reading Fluency"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "read-it-again")


def _passage_box(pdf, lines, img, top=606, height=270,
                 font_size=17, leading=28):
    """Large, clear reading box: passage text on the left, one
    colorful circular picture on the right. Each sentence on its
    own line so the child can track it while reading."""
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(40, top - height, 532, height, 14, stroke=1, fill=1)
    cy = top - height / 2
    _img_circle(pdf, img, 495, cy, 65, zoom=True)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", font_size)
    y = top - 32
    for line in lines:
        pdf.drawString(58, y, line)
        y -= leading


def _adult_line(pdf, text):
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 74, text)


def _pill(pdf, text, x, y, h=36, font_size=16, pad=12):
    """Centred-text pill sized to its text. Returns its width."""
    w = stringWidth(text, "Helvetica-Bold", font_size) + 2 * pad
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.2)
    pdf.roundRect(x, y, w, h, 10, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawCentredString(x + w / 2, y + h / 2 - 6, text)
    return w


def _write_line(pdf, x1, x2, y):
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1)
    pdf.setDash(4, 3)
    pdf.line(x1, y, x2, y)
    pdf.setDash()


def _page_title(pdf, title, instruction):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, title)
    pdf.drawCentredString(PAGE_WIDTH / 2, 624, instruction)


def _check_square(pdf, x, y, size=26):
    """Empty square for the child to tick. Restores the navy
    fill so following text does not inherit the square's white
    fill and vanish against the page."""
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.5)
    pdf.roundRect(x, y, size, size, 4, stroke=1, fill=1)
    pdf.setFillColor(NAVY)


def _scoop(pdf, x1, x2, y, depth=10):
    """A shallow curved scoop (arc) under a phrase, from x1 to x2
    with its lowest point depth points below y."""
    p = pdf.beginPath()
    p.moveTo(x1, y)
    p.curveTo(x1 + (x2 - x1) * 0.25, y - depth,
              x1 + (x2 - x1) * 0.75, y - depth, x2, y)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.drawPath(p, stroke=1, fill=0)


def _comp_check(pdf, question, choices, q_y, pills_y, font_size=16):
    """One brief comprehension check, placed AFTER the fluency
    activity: a centred question and a centred row of clearly
    separated answer pills for the child to circle. Fluency
    stays the primary objective; this is a single quick check."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawCentredString(PAGE_WIDTH / 2, q_y, question)
    total = sum(stringWidth(t, "Helvetica-Bold", font_size) + 24
                for t in choices) + (len(choices) - 1) * 12
    x = (PAGE_WIDTH - total) / 2
    for word in choices:
        x += _pill(pdf, word, x, pills_y, h=36,
                   font_size=font_size) + 12


# ---------------------------------------------------------------------------
# Page 1 -- Read It Smoothly (RF.1.4, supported)
# Fluency focus: reading accurately and smoothly. Pattern focus:
# short vowels and blends only. 31 words, 8 sentences.
# ---------------------------------------------------------------------------
P1_STORY = [
    "Sam has a big dog.",
    "The dog is tan.",
    "Sam and the dog run to the pond.",
    "The dog jumps in.",
    "Plop!",
    "Sam grins.",
    "The dog is wet.",
    "Sam is glad.",
]


def _read_smoothly(pdf):
    _page_title(pdf, "Read It Smoothly",
                "Read the story. Read it again, nice and smooth.")
    _passage_box(pdf, P1_STORY, "read-it-again/ria-dog-pond.jpg")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 312, "My Reading")
    _check_square(pdf, 170, 266)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(210, 274, "I read every word.")
    _check_square(pdf, 170, 216)
    pdf.drawString(210, 224, "I read it smoothly.")
    pdf.drawString(170, 176, "I read it")
    _write_line(pdf, 268, 328, 172)
    pdf.drawString(338, 176, "times.")
    _comp_check(pdf, "Where did the dog jump?", ["pond", "bed", "box"],
                q_y=148, pills_y=98)
    _adult_line(pdf, "Adult: Read the story aloud first. "
                     "Then your child reads it, and reads it again.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, TITLE, SUBTITLE)
    _read_smoothly(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Scoop the Phrases (RF.1.4, guided)
# Fluency focus: reading in meaningful phrases. Pattern focus:
# adds digraphs (sh, th). 45 words, 8 sentences. The child draws
# a scoop under each group of words that go together, right on
# the passage. A printed model scoop sits beneath the passage.
# ---------------------------------------------------------------------------
P2_STORY = [
    "The ship is big.",
    "The ship has a red flag.",
    "The ship is by the sand.",
    "A fish swims by the ship.",
    "The fish is fast.",
    "The fish swims with a crab.",
    "The crab is red.",
    "The ship is big and the fish is fast.",
]


def _scoop_phrases(pdf):
    _page_title(pdf, "Scoop the Phrases",
                "Read the story. Scoop the words that go together.")
    _passage_box(pdf, P2_STORY, "read-it-again/ria-ship-fish.jpg",
                 top=606, height=280, leading=30)
    # Model scoop panel beneath the passage.
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 226, 532, 84, 14, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 292, "Try it like this:")
    model = "The ship is big."
    w_total = stringWidth(model, "Helvetica-Bold", 17)
    w_first = stringWidth("The ship", "Helvetica-Bold", 17)
    w_space = stringWidth(" ", "Helvetica-Bold", 17)
    x0 = (PAGE_WIDTH - w_total) / 2
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(x0, 262, model)
    _scoop(pdf, x0, x0 + w_first, 254)
    _scoop(pdf, x0 + w_first + w_space, x0 + w_total, 254)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 200,
        "Now draw a scoop under the words that go together.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 178,
        "Then read it again, pausing at each scoop.")
    _comp_check(pdf, "What swims by the ship?", ["fish", "bird", "cat"],
                q_y=148, pills_y=98)
    _adult_line(pdf, "Adult: Show the first scoop. "
                     "The child scoops the rest, then reads it again.")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, TITLE, SUBTITLE)
    _scoop_phrases(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Read It with Feeling (RF.1.4, guided)
# Fluency focus: using punctuation and expression. Pattern focus:
# adds final-e. 38 words, 8 sentences, one exclamation and one
# question in dialogue. The ! is on "The bike is fast!" and the
# ? is on "'Is it safe?'". The voice match uses those exact
# sentences.
# ---------------------------------------------------------------------------
P3_STORY = [
    "Jake has a red bike.",
    "Jake rides the bike on the path.",
    "The bike is fast!",
    "Jake spots a snake in the grass.",
    "'Is it safe?' Jake asks.",
    "The snake is big.",
    "Jake rides home.",
    "Jake is safe.",
]


def _read_feeling(pdf):
    _page_title(pdf, "Read It with Feeling",
                "Read the story. Circle ! and ? "
                "Then read with feeling.")
    _passage_box(pdf, P3_STORY, "read-it-again/ria-bike-snake.jpg")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(58, 314,
                   "Read in an excited voice: \"The bike is fast!\"")
    pdf.drawString(58, 290,
                   "Read in a wondering voice: \"Is it safe?\"")
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 258,
                          "Match each mark to its voice. Draw a line.")
    # Voice match: marks on the left, voices on the right in
    # scrambled order so the child has to match, not just draw
    # straight across. ! -> excited voice, ? -> question voice,
    # . -> calm voice. Rows sit 42 apart so the comprehension
    # check below has room without crowding.
    marks = ["!", "?", "."]
    voices = ["question voice", "calm voice", "excited voice"]
    rows_y = [220, 178, 136]
    for mark, voice, cy in zip(marks, voices, rows_y):
        pdf.setFillColor(TEAL)
        pdf.circle(120, cy + 12, 18, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(120, cy + 5, mark)
        pdf.setFillColor(TEAL)
        pdf.circle(140, cy + 12, 5, stroke=0, fill=1)
        w = stringWidth(voice, "Helvetica-Bold", 15) + 24
        x = 492 - w
        _pill(pdf, voice, x, cy - 6, h=36, font_size=15)
        pdf.setFillColor(TEAL)
        pdf.circle(x - 14, cy + 12, 5, stroke=0, fill=1)
    # Comprehension check: oral response only, no writing box.
    # The question plus a teal "Tell an adult." tag on one line,
    # so it fits after the voice match with clear space above
    # and below.
    q = "Why did Jake ask, 'Is it safe?'"
    tag = "Tell an adult."
    q_w = stringWidth(q, "Helvetica-Bold", 16)
    tag_w = stringWidth(tag, "Helvetica-Bold", 13) + 20
    x = (PAGE_WIDTH - (q_w + 12 + tag_w)) / 2
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(x, 100, q)
    _pill(pdf, tag, x + q_w + 12, 92, h=28, font_size=13, pad=10)
    _adult_line(pdf, "Adult: Listen for the excited voice on ! "
                     "and the wondering voice on ?")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, TITLE, SUBTITLE)
    _read_feeling(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Read It Again (RF.1.4, guided to independent)
# Fluency focus: rereading to improve fluency. Pattern focus:
# adds vowel teams (ai, ay, ee, ea, oa, ow as long o). 41 words,
# 8 sentences. The child reads three times, coloring one circle
# for each read, then circles what got better.
# ---------------------------------------------------------------------------
P4_STORY = [
    "It is a rainy day.",
    "The rain falls on the grass.",
    "The rain taps on the glass.",
    "We stay inside and play a game.",
    "We play with blocks.",
    "We make a tall stack.",
    "The rain stops.",
    "We go back and play.",
]


def _read_again(pdf):
    _page_title(pdf, "Read It Again",
                "Read the story three times. "
                "Color one circle each time.")
    _passage_box(pdf, P4_STORY, "read-it-again/ria-rain-blocks.jpg")
    labels = ["Read 1", "Read 2", "Read 3"]
    for i, label in enumerate(labels):
        cx = 192 + i * 114
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(cx, 318, label)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(TEAL)
        pdf.setLineWidth(1.5)
        pdf.circle(cx, 278, 30, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 218,
                          "What got better? Circle it.")
    # All three options on one row (471pt at 14pt, in 532pt) so
    # the comprehension check below has room without shrinking
    # the passage, the circles, or the line spacing.
    row = ["I read it smoother.", "I read the hard words.",
           "I used my voice."]
    total = sum(stringWidth(t, "Helvetica-Bold", 14) + 24
                for t in row) + 2 * 12
    x = (PAGE_WIDTH - total) / 2
    for text in row:
        x += _pill(pdf, text, x, 172, h=36, font_size=14) + 12
    _comp_check(pdf, "What did the children play with inside?",
                ["blocks", "balls", "cars"], q_y=140, pills_y=92)
    _adult_line(pdf, "Adult: Read with your child the first time. "
                     "Then let your child read alone.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, TITLE, SUBTITLE)
    _read_again(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Read It on Your Own (RF.1.4, independent)
# Fluency focus: independent fluent reading, plus understanding
# what was read. Pattern focus: all patterns mixed. 36 words,
# 8 sentences. One quick understanding check, not a
# comprehension set: "What did we eat for lunch?" Answer: beans.
# ---------------------------------------------------------------------------
P5_STORY = [
    "We plant seeds in a pot.",
    "The seeds need sun.",
    "The sun is hot.",
    "The plants grow tall.",
    "We see green leaves.",
    "We pick red beans.",
    "We eat them at lunch.",
    "It is a nice lunch.",
]


def _read_on_own(pdf):
    _page_title(pdf, "Read It on Your Own",
                "Read the story on your own. Then read it again.")
    _passage_box(pdf, P5_STORY, "read-it-again/ria-garden-beans.jpg")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(170, 300, "I read it")
    _write_line(pdf, 268, 328, 296)
    pdf.drawString(338, 300, "times.")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 252,
                          "What did we eat for lunch?")
    choices = ["beans", "cake", "fish"]
    total = sum(stringWidth(t, "Helvetica-Bold", 16) + 24
                for t in choices) + 2 * 12
    x = (PAGE_WIDTH - total) / 2
    for word in choices:
        x += _pill(pdf, word, x, 204) + 12
    _adult_line(pdf, "Adult: Let your child read alone. "
                     "Ask the lunch question after the second read.")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, TITLE, SUBTITLE)
    _read_on_own(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Read It Smoothly", build_p1_page),
    ("Scoop the Phrases", build_p2_page),
    ("Read It with Feeling", build_p3_page),
    ("Read It Again", build_p4_page),
    ("Read It on Your Own", build_p5_page),
]


# ---------------------------------------------------------------------------
# Parent fluency guide (separate one-page PDF, NOT in the student
# bundle). Plain language for parents, no timers, no racing, no
# words-per-minute scoring. Includes support strategies for a
# child who struggles with a passage.
# ---------------------------------------------------------------------------
GUIDE_TITLE = "How to Use This Pack"
GUIDE_INTRO = [
    "Fluency means reading accurately, smoothly, and with",
    "expression, and understanding what you read. It is not",
    "speed. Your child reads the same short story more than once.",
]
GUIDE_SECTIONS = [
    ("A simple routine for each page", [
        "1. You read the story aloud first.",
        "2. Your child reads it.",
        "3. Your child reads it again.",
        "4. Do the page activity together.",
        "5. Talk briefly about what happened.",
    ]),
    ("When your child gets stuck on a word", [
        "Wait. Let your child try. Give the first sound.",
        "Tell the word and move on.",
    ]),
    ("If a story feels hard", [
        "Read the tricky line together.",
        "Break the story into two parts. Read the first half,",
        "then the second.",
        "Let your child point to each word as they read.",
        "Reread a favorite line first, then try the whole story.",
        "Stop while it is still fun. Come back to it tomorrow.",
    ]),
    ("What not to do", [
        "No timer. No counting words in a minute. No racing.",
        "No correcting every small slip. Let your child fix",
        "their own mistakes.",
    ]),
    ("What to praise", [
        "Praise smooth reading, expression, and reading again,",
        "not speed.",
    ]),
    ("The five pages at a glance", [
        "Page 1, Read It Smoothly: read every word, read it smoothly.",
        "Page 2, Scoop the Phrases: read in groups of words",
        "that go together.",
        "Page 3, Read It with Feeling: use ! and ? to read",
        "with expression.",
        "Page 4, Read It Again: read three times and notice",
        "what got better.",
        "Page 5, Read It on Your Own: read alone, then read again.",
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
    pdf.drawString(234, PAGE_HEIGHT - 90, "Parent Fluency Guide")
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
            y -= 14
        y -= 5
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 58,
        "Grade 1 Reading: Read It Again! For parents, not for the child.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    page_pdfs = []
    for i, (title, builder) in enumerate(PAGES):
        p = os.path.join(OUT_DIR,
                         "read-it-again-page-%02d-v2.pdf" % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(OUT_DIR, "read-it-again-v2.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)
    guide = os.path.join(OUT_DIR, "read-it-again-parent-guide-v2.pdf")
    build_parent_guide(guide)
    assert len(PdfReader(guide).pages) == 1
    print("parent guide: %s (1 page)" % guide)


if __name__ == "__main__":
    main()
