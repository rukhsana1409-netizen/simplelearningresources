#!/usr/bin/env python3
"""Grade 1 Reading - Nouns and Verbs in Action.

Resource 17 in the approved and locked Grade 1 Reading and
Language Arts roadmap (audit 2026-11-05). Plan approved
2026-11-19 with six adjustments (a person, place, thing
visual reminder on Page 1; "The children hop" on Page 2;
a Yesterday, Today, Tomorrow visual strip on Page 3;
separate describing-word and whose-word sections on
Page 4; Page 5 asks for a describing word in at least one
sentence and is independent application of nouns, verbs,
and adjectives, not an assessment of all four standards).
Placement: Grade 1 / Reading & Language / Grammar and
Sentences. Standards L.1.1(b), L.1.1(c), L.1.1(e),
L.1.1(f):
L.1.1(b) covers common, proper, and possessive nouns.
L.1.1(c) covers singular and plural nouns with matching
verbs in basic sentences (He hops; We hop). L.1.1(e)
covers verbs to convey past, present, and future.
L.1.1(f) covers frequently occurring adjectives.

Progression: spot the naming word (Page 1), match the
action word to one or many (Page 2), pick the verb form
that tells when it happens (Page 3), add a describing
word and a whose word (Page 4), and write two sentences
of their own about a picture (Page 5). Every naming word,
action word, and describing word appears inside a real
sentence, never as a labeling drill.

Boundaries: Resource 16 owns sentence mechanics (whole
idea, capitals, end marks, commas). Resource 22 owns
pronouns (including possessive pronouns such as my, his,
hers) and prepositions. Resource 23 owns conjunctions,
determiners, sentence types, and expansion. This pack
teaches possessive NOUNS (Mia's, the dog's) with
apostrophe-s, not possessive pronouns. Word Endings
(Resource 11) teaches the endings -s, -es, -ed, -ing as
word forms; this pack uses those endings as grammar
(the verb changes to match the subject and the time).

No printable answer key. The Parent Guide is the only
extra download and carries the answers. No em dash
anywhere in the student pages or the guide.

Illustrations: the approved watercolor storybook style
from Resource 16. Reused approved Resource 16 JPEGs
(p1-dog-running, p1-girl-reading, p3-school-v2,
p1-boy-kicking, p1-two-birds, p2-red-ball, p2-sun,
p2-child-bike) sit beside the seven new original
watercolor JPEGs (p1-reminder-strip, p2-boy-hopping,
p2-children-hopping, p2-one-bird, p3-mia-ball,
p4-dog-bone, p5-beach-scene), all embedded with
_draw_image. JPEGs embed as DCT, so the PDF stays small.
The beach scene is shown whole (3:2) rather than cropped.

Shared design code (logo, header, footer) is imported
verbatim from build_phonics_az.py. Do not fork it here.
Header title is drawn at 18pt and the subtitle at 14pt;
both end inside the teal rule.
"""
import hashlib
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter as _letter  # noqa: F401
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from build_phonics_az import (NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              draw_footer, draw_header, draw_logo)

TITLE = "Nouns and Verbs in Action"
SUBTITLE = "Grade 1 Reading | Nouns and Verbs in Action"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")
PAST_FILL = HexColor("#DCE9F5")
FUTURE_FILL = HexColor("#FFF3D6")
FUTURE_TEXT = HexColor("#8A6D00")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "nouns-and-verbs-in-action")
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


def _draw_sentence_blank(pdf, x, y, prefix, answer, suffix,
                         size=14):
    """Draw a sentence with a ruled blank where the child
    writes the answer word. The blank is wide enough for
    the answer. Returns the x after the sentence."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", size)
    if prefix:
        pdf.drawString(x, y, prefix)
        x += stringWidth(prefix, "Helvetica", size)
    bw = stringWidth(answer, "Helvetica", size) + 26
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.line(x, y, x + bw, y)
    x += bw
    if suffix:
        pdf.drawString(x, y, suffix)
        x += stringWidth(suffix, "Helvetica", size)
    return x


def _word_pills(pdf, x, y, words, size=13):
    """Two word-choice pills side by side. Each pill is a
    rounded rectangle with the word in bold. The child
    circles the pill that fits. y is the bottom of the
    pills. Returns the x after the last pill."""
    for w in words:
        ww = stringWidth(w, "Helvetica-Bold", size) + 22
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(BOX_STROKE)
        pdf.setLineWidth(1.2)
        pdf.roundRect(x, y, ww, 26, 8, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", size)
        pdf.drawCentredString(x + ww / 2, y + 9, w)
        x += ww + 10
    return x


def _choice_row(pdf, y, h, image, prefix, answer, suffix,
                choices):
    """One row: picture at left, sentence with a blank, and
    two word-choice pills below the sentence."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, image, 100, y + h / 2 + 2, 96, h - 8)
    _draw_sentence_blank(pdf, 160, y + h - 32, prefix, answer,
                         suffix, size=14)
    _word_pills(pdf, 160, y + 12, choices, size=13)


def _remember_box(pdf, y, h, lines):
    """A Remember panel with a teal title and centred lines
    of text. (x, y) is the bottom-left corner. The title
    sits 18 below the top edge and the lines start 38 below
    it, so a one-line box needs height 48 and a two-line
    box needs height 68."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 18, "Remember")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    ly = y + h - 38
    for line in lines:
        pdf.drawCentredString(PAGE_WIDTH / 2, ly, line)
        ly -= 17


# ---------------------------------------------------------------------------
# Page 1 -- Naming Words
# ---------------------------------------------------------------------------
P1_ROWS = [
    (os.path.join(IMG_DIR, "p1-dog-running.jpg"),
     "The ", "dog", " runs fast.", ["dog", "jump"]),
    (os.path.join(IMG_DIR, "p1-girl-reading.jpg"),
     "", "Mia", " reads a book.", ["Mia", "reads"]),
    (os.path.join(IMG_DIR, "p3-school-v2.jpg"),
     "We learn at ", "school", ".", ["school", "learn"]),
    (os.path.join(IMG_DIR, "p1-boy-kicking.jpg"),
     "", "Ben", " kicks the ball.", ["Ben", "kicks"]),
]


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Naming Words",
        "A naming word names a person, a place, or a thing.\n"
        "Circle the naming word that fits. Write it in the sentence.")
    # Person, place, thing visual reminder: the three
    # vignettes in the strip sit at about 17 percent, 50
    # percent, and 81 percent of the image width, so the
    # labels go under those spots.
    _panel(pdf, 40, 464, 532, 128)
    _draw_image(pdf, os.path.join(IMG_DIR, "p1-reminder-strip.jpg"),
                PAGE_WIDTH / 2, 536, 300, 100)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 11)
    for frac, label in ((0.17, "Person"), (0.50, "Place"),
                        (0.81, "Thing")):
        pdf.drawCentredString(156 + frac * 300, 470, label)
    rh, gap = 84, 8
    y = 454 - rh
    for image, prefix, answer, suffix, choices in P1_ROWS:
        _choice_row(pdf, y, rh, image, prefix, answer, suffix,
                    choices)
        y -= rh + gap
    _adult_line(pdf, "A name starts with a big letter. Ask: is "
                     "it a person, a place, or a thing?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- One or Many?
# ---------------------------------------------------------------------------
P2_ROWS = [
    (os.path.join(IMG_DIR, "p2-boy-hopping.jpg"),
     "Sam ", "hops", ".", ["hops", "hop"]),
    (os.path.join(IMG_DIR, "p2-children-hopping.jpg"),
     "The children ", "hop", ".", ["hop", "hops"]),
    (os.path.join(IMG_DIR, "p2-one-bird.jpg"),
     "The bird ", "sings", ".", ["sings", "sing"]),
    (os.path.join(IMG_DIR, "p1-two-birds.jpg"),
     "The birds ", "sing", ".", ["sing", "sings"]),
]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "One or Many?",
        "One does it one way. Many do it another way.\n"
        "Circle the action word that fits. Write it in the sentence.")
    rh, gap = 96, 10
    y = top - rh
    for image, prefix, answer, suffix, choices in P2_ROWS:
        _choice_row(pdf, y, rh, image, prefix, answer, suffix,
                    choices)
        y -= rh + gap
    _remember_box(pdf, 100, 68, [
        "One hops. Many hop.",
        "The action word changes when one or many do it."])
    _adult_line(pdf, "Point to the picture and count. One child "
                     "means hops. Many children means hop.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- When Did It Happen?
# ---------------------------------------------------------------------------
def _time_strip(pdf, y, h):
    """Yesterday, Today, Tomorrow strip with arrows and
    small labels (past, now, yet to come)."""
    _panel(pdf, 40, y, 532, h)
    boxes = [("Yesterday", "past", PAST_FILL, NAVY),
             ("Today", "now", LIGHT_TEAL, TEAL),
             ("Tomorrow", "yet to come", FUTURE_FILL,
              FUTURE_TEXT)]
    bw, bh = 140, 30
    total = 3 * bw + 2 * 30
    x = PAGE_WIDTH / 2 - total / 2
    cy = y + h / 2 + 8
    for i, (label, sub, fill, tcol) in enumerate(boxes):
        pdf.setFillColor(fill)
        pdf.setStrokeColor(BOX_STROKE)
        pdf.setLineWidth(1)
        pdf.roundRect(x, cy - bh / 2, bw, bh, 8, stroke=1,
                      fill=1)
        pdf.setFillColor(tcol)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawCentredString(x + bw / 2, cy - 4, label)
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica", 10.5)
        pdf.drawCentredString(x + bw / 2, y + 14, sub)
        if i < 2:
            ax = x + bw
            pdf.setStrokeColor(NAVY)
            pdf.setFillColor(NAVY)
            pdf.setLineWidth(2)
            pdf.line(ax + 4, cy, ax + 20, cy)
            p = pdf.beginPath()
            p.moveTo(ax + 20, cy - 5)
            p.lineTo(ax + 27, cy)
            p.lineTo(ax + 20, cy + 5)
            p.close()
            pdf.drawPath(p, stroke=0, fill=1)
        x += bw + 30


def _time_row(pdf, y, h, image, time_word, time_color,
              prefix, answer, suffix, choices):
    """One row: picture at left, the time word in color,
    the sentence with a blank, and two word-choice pills."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, image, 100, y + h / 2 + 2, 96, h - 8)
    pdf.setFillColor(time_color)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(160, y + h - 22, time_word)
    _draw_sentence_blank(pdf, 160, y + h - 48, prefix, answer,
                         suffix, size=14)
    _word_pills(pdf, 160, y + 8, choices, size=13)


P3_ROWS = [
    (os.path.join(IMG_DIR, "p1-boy-kicking.jpg"),
     "Yesterday", NAVY, "Ben ", "kicked", " the ball.",
     ["kicked", "kicks"]),
    (os.path.join(IMG_DIR, "p3-mia-ball.jpg"),
     "Today", TEAL, "Mia ", "plays", " with a ball.",
     ["plays", "played"]),
    (os.path.join(IMG_DIR, "p2-child-bike.jpg"),
     "Tomorrow", FUTURE_TEXT, "Sam ", "will play",
     " at the park.", ["will play", "played"]),
    (os.path.join(IMG_DIR, "p1-dog-running.jpg"),
     "Yesterday", NAVY, "The dog ", "played", " in the park.",
     ["played", "plays"]),
]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "When Did It Happen?",
        "Circle the action word that fits the time. "
        "Write it in the sentence.")
    _time_strip(pdf, 530, 76)
    rh, gap = 88, 8
    y = 520 - rh
    for (image, time_word, time_color, prefix, answer, suffix,
         choices) in P3_ROWS:
        _time_row(pdf, y, rh, image, time_word, time_color,
                  prefix, answer, suffix, choices)
        y -= rh + gap
    _remember_box(pdf, 90, 48, [
        "Yesterday: played. Today: plays. Tomorrow: will play."])
    _adult_line(pdf, "Say the time word first. Yesterday means "
                     "it is done. Tomorrow is yet to come.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Tell Me More
# ---------------------------------------------------------------------------
def _section_label(pdf, y, text, color):
    """A section label in its own color, with a thin rule
    under it, so the two skills on this page read as two
    separate sections."""
    pdf.setFillColor(color)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, y, text)
    pdf.setStrokeColor(color)
    pdf.setLineWidth(1.2)
    pdf.line(40, y - 6, 572, y - 6)


P4_ADJ_ROWS = [
    (os.path.join(IMG_DIR, "p4-big-ball.jpg"),
     "The ", "big", " ball rolls.", ["big", "run"]),
    (os.path.join(IMG_DIR, "p2-sun.jpg"),
     "The ", "yellow", " sun is up.", ["yellow", "up"]),
]

P4_POSS_ROWS = [
    (os.path.join(IMG_DIR, "p1-girl-reading.jpg"),
     "This is ", "Mia's", " book.", ["Mia's", "Mia"]),
    (os.path.join(IMG_DIR, "p4-dog-bone.jpg"),
     "That is the ", "dog's", " bone.", ["dog's", "dog"]),
]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Tell Me More",
        "A describing word tells what it is like. A whose word "
        "tells who it belongs to.\n"
        "Circle the word that fits. Write it in the sentence.")
    rh, gap = 88, 8
    _section_label(pdf, 572, "Describing words", TEAL)
    y = 564 - rh
    for image, prefix, answer, suffix, choices in P4_ADJ_ROWS:
        _choice_row(pdf, y, rh, image, prefix, answer, suffix,
                    choices)
        y -= rh + gap
    _section_label(pdf, 360, "Whose words", CORAL)
    y = 352 - rh
    for image, prefix, answer, suffix, choices in P4_POSS_ROWS:
        _choice_row(pdf, y, rh, image, prefix, answer, suffix,
                    choices)
        y -= rh + gap
    _remember_box(pdf, 94, 68, [
        "Describing words tell what it is like: big, red, happy.",
        "Whose words tell who it belongs to: Mia's, the dog's."])
    _adult_line(pdf, "Ask: what is it like? Then ask: whose is it?")
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
        "Look at the picture. Write two sentences about it.\n"
        "Use a naming word and an action word. Put a describing "
        "word in at least one.")
    # The beach is a full 3:2 watercolor scene, so it is
    # shown whole (360 by 240) rather than cropped.
    _draw_image(pdf, os.path.join(IMG_DIR, "p5-beach-scene.jpg"),
                PAGE_WIDTH / 2, top - 120, 360, 240)
    _writing_area(pdf, 254, 92, "Sentence 1")
    _writing_area(pdf, 156, 92, "Sentence 2")
    _panel(pdf, 40, 54, 532, 96)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 132,
                          "Check your sentences:")
    checks = ["Did I use a naming word?",
              "Did I use an action word?",
              "Did I use a describing word?"]
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
    pdf.drawString(234, PAGE_HEIGHT - 68, "Nouns and Verbs in Action")
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
GUIDE_INTRO = ("This pack teaches your child the words inside "
               "a sentence: the naming word, the action word, "
               "and the describing word.")
GUIDE_SECTIONS = [
    ("How to help", [
        "Page 1: ask, is it a person, a place, or a thing?",
        "Page 2: point to the picture and count. One hops, "
        "many hop.",
        "Page 3: say the time word first. Yesterday means it "
        "is done. Tomorrow means it has not happened yet.",
        "Page 4: ask, what is it like? Then ask, whose is it?",
        "Page 5: let your child choose what to write.",
    ]),
    ("What your child learns", [
        "Naming words name a person, a place, or a thing. "
        "Names start with a big letter. Action words tell "
        "what happens and change when one or many do it, and "
        "when the time changes. Describing words tell what "
        "something is like. Whose words tell who it belongs "
        "to. On Page 5 your child writes two sentences of "
        "their own, using a naming word and an action word "
        "in each, with a describing word in at least one.",
    ]),
    ("Answers", [
        ("Page 1", "dog / Mia / school / Ben."),
        ("Page 2", "hops / hop / sings / sing."),
        ("Page 3", "kicked / plays / will play / played."),
        ("Page 4", "big / yellow / Mia's / dog's."),
        ("Page 5", "Two sentences of their own. Check for a "
                   "naming word, an action word, and a "
                   "describing word in at least one."),
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
        "Page 2: point to the picture and count. One child "
        "means hops. Many children means hop.",
        "Page 3: say the time word first. Yesterday means the "
        "action is done. Tomorrow means it has not happened "
        "yet.",
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
        "Grade 1 Reading: Nouns and Verbs in Action. "
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
    bundle = os.path.join(OUT_DIR, "nouns-and-verbs-in-action.pdf")
    guide = os.path.join(
        OUT_DIR, "nouns-and-verbs-in-action-parent-guide.pdf")
    review = os.path.join(
        OUT_DIR, "nouns-and-verbs-in-action-review.pdf")
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
    page_names = ["naming-words", "one-or-many",
                  "when-did-it-happen", "tell-me-more",
                  "write-your-own-sentences"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR, "nouns-and-verbs-in-action-p%d-%s.pdf"
            % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    for name in ["nouns-and-verbs-in-action.pdf",
                 "nouns-and-verbs-in-action-parent-guide.pdf",
                 "nouns-and-verbs-in-action-review.pdf",
                 "nouns-and-verbs-in-action-p1-naming-words.pdf",
                 "nouns-and-verbs-in-action-p2-one-or-many.pdf",
                 "nouns-and-verbs-in-action-p3-when-did-it-happen.pdf",
                 "nouns-and-verbs-in-action-p4-tell-me-more.pdf",
                 "nouns-and-verbs-in-action-p5-write-your-own-sentences.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text.
    for name in ["nouns-and-verbs-in-action.pdf",
                 "nouns-and-verbs-in-action-parent-guide.pdf"]:
        text = "".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
    print("em dash check: clean")


if __name__ == "__main__":
    main()
