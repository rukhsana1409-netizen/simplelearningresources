#!/usr/bin/env python3
"""Grade 1 Reading - Poetry and Feeling Words.

Resource 18 in the approved and locked Grade 1 Reading and
Language Arts roadmap (audit 2026-11-05). Plan approved
2026-11-19 with the user's final content refinements:
Page 1 keeps the activity but clarifies that poems can
contain sentences, so the distinction is the arrangement
into lines and stanzas, not that poems are the opposite
of sentences. Page 2 approved unchanged. Page 3 uses the
user's garden poem and four sensory questions (see, hear,
feel, smell), each with two word choices. Page 4 uses the
user's Play Day and My Lost Ball poems, keeps the
happy, sad, calm choices, asks the child to underline one
or two supporting clues, and shows the sad child without
the missing ball visible. Page 5 approved unchanged.

Placement: Grade 1 / Reading & Language / Reading
Comprehension. Standards RL.1.4 (identify words and
phrases in stories or poems that suggest feelings or
appeal to the senses) and RL.1.10 (read grade-level
poems with prompting and support, a level condition, not
a taught skill).

Boundaries: Preschool Rhyming Pictures matches rhymes by
picture only and Kindergarten Say It and Split It asks
the child to say a rhyming word aloud; this pack is the
Grade 1 step of finding rhyming words inside a printed
poem. The Feelings and Me pack is social-emotional life
skills; this pack finds feeling words inside poems
(RL.1.4), not self-management. Resource 17 teaches
adjectives as grammar; this pack finds sensory words in
poems and does not re-teach adjective grammar. Resource
13 describes characters in stories; this pack names a
poem's mood from its words and pictures. Resource 21
owns shades of meaning; this pack does not rank synonyms.
Resource 16 owns sentence mechanics; Page 1 builds on it
and shows that a poem is written in lines and stanzas.

No printable answer key. The Parent Guide is the only
extra download and carries the answers. No em dash
anywhere in the student pages or the guide.

Illustrations: six new original watercolor storybook
JPEGs in the approved style from Resources 16 and 17
(p1-cat, p2-rain, p3-garden, p4-happy, p4-sad,
p5-garden), all embedded with _draw_image. JPEGs embed
as DCT, so the PDF stays small. The sad child is shown
without the missing ball visible, so the child must use
the poem's words, not the picture alone. The beach scene
is not reused here; the Page 5 picture prompt is a
garden, distinct from Resource 17's beach.

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

TITLE = "Poetry and Feeling Words"
SUBTITLE = "Grade 1 Reading | Poetry and Feeling Words"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "poetry-and-feeling-words")
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


def _word_pills(pdf, x, y, words, size=13):
    """Word-choice pills in a row. Each pill is a rounded
    rectangle with the word in bold. The child circles the
    pill that fits. y is the bottom of the pills. Returns
    the x after the last pill."""
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


def _count_blank(pdf, x, y, label, blank_w=50):
    """A label followed by a ruled blank for a number.
    Returns the x after the blank."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(x, y, label)
    x += stringWidth(label, "Helvetica", 13) + 8
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.line(x, y, x + blank_w, y)
    return x + blank_w


def _choice_question_row(pdf, y, h, question, choices):
    """A panel with a question on the left and two
    word-choice pills right-aligned. The child circles the
    pill that fits. y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(56, y + h / 2 - 5, question)
    total_w = sum(stringWidth(w, "Helvetica-Bold", 13) + 22
                  for w in choices) + 10 * (len(choices) - 1)
    px = 556 - total_w
    _word_pills(pdf, px, y + h / 2 - 13, choices, size=13)


# ---------------------------------------------------------------------------
# Page 1 -- Meet a Poem
# ---------------------------------------------------------------------------
def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Meet a Poem",
        "A poem is written in lines. Read the poem.\n"
        "Count the lines and the stanzas.")
    # Poem panel: the gray cat on the left, the poem on the
    # right, in two stanzas with a blank line between them.
    _panel(pdf, 40, 430, 532, 162)
    _draw_image(pdf, os.path.join(IMG_DIR, "p1-cat.jpg"),
                150, 511, 200, 133)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(280, 566, "My Cat")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 14)
    for text, y in (("My cat is soft and gray,", 544),
                    ("She naps and plays all day.", 524),
                    ("She chases a red ball,", 494),
                    ("Then naps, and that is all.", 474)):
        pdf.drawString(280, y, text)
    # Counting blanks, centred as a pair.
    x = _count_blank(pdf, 130, 398, "How many lines?")
    _count_blank(pdf, x + 44, 398, "How many stanzas?")
    # Which one is written like a poem? The same words
    # arranged two ways: in lines (a poem) and in one long
    # line (a sentence). The child circles the poem.
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 370,
                          "Which one is written like a poem? "
                          "Circle it.")
    _panel(pdf, 40, 288, 532, 72)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 334, "A")
    pdf.setFont("Helvetica", 13)
    pdf.drawString(80, 342, "My cat is soft and gray,")
    pdf.drawString(80, 322, "She naps and plays all day.")
    _panel(pdf, 40, 206, 532, 72)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 238, "B")
    pdf.setFont("Helvetica", 13)
    pdf.drawString(80, 238,
                   "My cat is soft and gray and she naps all day.")
    _remember_box(pdf, 118, 68, [
        "Poems often arrange words in lines.",
        "A group of lines is called a stanza."])
    _adult_line(pdf, "Point to each line of the poem. Poems "
                     "arrange words in lines, often in groups "
                     "called stanzas.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Listen for Rhymes
# ---------------------------------------------------------------------------
def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Listen for Rhymes",
        "Read the poem. Circle the words that rhyme.")
    # Poem panel: the poem on the left, the rain picture on
    # the right. The picture fits inside the right half of
    # the panel (200 by 133, centred at x=470).
    _panel(pdf, 40, 406, 532, 200)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 566, "Rain")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 14)
    for text, y in (("Rain, rain, on my hat,", 544),
                    ("I jump and splash, just like that.", 522),
                    ("The sun shines for play,", 500),
                    ("I run and jump all day.", 478)):
        pdf.drawString(56, y, text)
    _draw_image(pdf, os.path.join(IMG_DIR, "p2-rain.jpg"),
                470, 506, 200, 133)
    _choice_question_row(pdf, 318, 78,
                         "Which word rhymes with sun?",
                         ["run", "rain"])
    _choice_question_row(pdf, 230, 78,
                         "Which word rhymes with cake?",
                         ["lake", "cat"])
    _remember_box(pdf, 140, 56, [
        "Words that rhyme sound the same at the end."])
    _adult_line(pdf, "Say the two words aloud. Do they sound "
                     "the same at the end?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Words We Can Feel
# ---------------------------------------------------------------------------
def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "Words We Can Feel",
        "Read the poem. Then answer the questions.")
    # Poem panel: the user's garden poem on the left, the
    # garden picture on the right.
    _panel(pdf, 40, 430, 532, 176)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 566, "In the Garden")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 14)
    for text, y in (
            ("A red rose grows beside a tree,", 544),
            ("A little bee hums next to me.", 522),
            ("Soft green grass is at my feet,", 500),
            ("The rose smells fresh and sweet.", 478)):
        pdf.drawString(56, y, text)
    _draw_image(pdf, os.path.join(IMG_DIR, "p3-garden.jpg"),
                470, 518, 200, 133)
    # Four sensory questions, each with two word choices.
    # Every word comes from the poem, and each pair has one
    # clear answer.
    _choice_question_row(pdf, 376, 46,
                         "Which word tells what I see?",
                         ["rose", "hums"])
    _choice_question_row(pdf, 322, 46,
                         "Which word tells what I hear?",
                         ["hums", "sweet"])
    _choice_question_row(pdf, 268, 46,
                         "Which word tells what I feel?",
                         ["soft", "red"])
    _choice_question_row(pdf, 214, 46,
                         "Which word tells what I smell?",
                         ["sweet", "green"])
    _remember_box(pdf, 136, 48, [
        "Words can tell what we see, hear, feel, smell, "
        "and taste."])
    _adult_line(pdf, "Point to the picture. What do you see? "
                     "What do you hear?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- How Does the Poem Feel?
# ---------------------------------------------------------------------------
def _poem_feeling_section(pdf, y, h, title, poem_lines, image,
                          img_w, img_h):
    """One poem on Page 4: title and four poem lines on the
    left, illustration on the right, and happy, sad, calm
    pills below the poem. The child circles the feeling
    and underlines one or two words that tell it. y is the
    bottom of the section."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 24, title)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13.5)
    ly = y + h - 48
    for line in poem_lines:
        pdf.drawString(56, ly, line)
        ly -= 19
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(56, y + 56, "How does it feel? Circle one.")
    _word_pills(pdf, 56, y + 16, ["happy", "sad", "calm"],
                size=13)
    _draw_image(pdf, image, 470, y + h / 2, img_w, img_h)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "How Does the Poem Feel?",
        "Read each poem. Circle how it feels.\n"
        "Underline one or two words that tell you.")
    _poem_feeling_section(
        pdf, 392, 200, "Play Day",
        ["The sun is bright, I run and play,",
         "I jump and smile throughout the day.",
         "My dog runs fast beside my feet,",
         "We race along the sunny street."],
        os.path.join(IMG_DIR, "p4-happy.jpg"), 180, 150)
    _poem_feeling_section(
        pdf, 182, 200, "My Lost Ball",
        ["My little ball is gone today,",
         "I looked for it along the way.",
         "I sit alone and give a sigh,",
         "I miss my ball and want to cry."],
        os.path.join(IMG_DIR, "p4-sad.jpg"), 150, 180)
    _remember_box(pdf, 114, 48, [
        "The words in a poem tell how it feels."])
    _adult_line(pdf, "Look at the picture first. Then find the "
                     "words that tell the feeling.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- My Little Poem
# ---------------------------------------------------------------------------
def _writing_row(pdf, y, starter):
    """One poem line: the starter words in bold, then a
    ruled line the child writes on, to the right edge."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(56, y, starter)
    x = 56 + stringWidth(starter, "Helvetica-Bold", 14) + 10
    _ruled_line(pdf, x, 556, y)


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    top = _page_title(
        pdf, "My Little Poem",
        "Look at the picture. Write a short poem about it.\n"
        "Use words from the word bank, or use your own words.")
    # The garden picture prompt, shown whole (360 by 240).
    _draw_image(pdf, os.path.join(IMG_DIR, "p5-garden.jpg"),
                PAGE_WIDTH / 2, top - 120, 360, 240)
    # Word bank: three groups, each a bold label and words.
    _panel(pdf, 40, 258, 532, 84)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 324, "Word Bank")
    bank = [
        ("Words that rhyme: ", "sun, run, day, play"),
        ("Words that tell what it is like: ",
         "soft, sweet, red, warm"),
        ("Words that tell how I feel: ", "happy, glad, calm"),
    ]
    by = 302
    for label, words in bank:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(56, by, label)
        x = 56 + stringWidth(label, "Helvetica-Bold", 12)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(x, by, words)
        by -= 18
    # Four writing lines, the list poem frame.
    _writing_row(pdf, 240, "I see")
    _writing_row(pdf, 206, "I hear")
    _writing_row(pdf, 172, "I feel")
    _writing_row(pdf, 138, "I am")
    # Self-check. The panel is tall enough for all three
    # checkboxes to sit inside it, above the footer.
    _panel(pdf, 40, 48, 532, 82)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 108,
                          "Check your poem:")
    checks = ["Did I write my poem in lines?",
              "Did I use a word that tells what I see, hear, "
              "or feel?",
              "Did I use a feeling word?"]
    cy = 90
    for text in checks:
        pdf.setStrokeColor(BOX_STROKE)
        pdf.setLineWidth(1.4)
        pdf.rect(96, cy - 4, 13, 13, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(118, cy, text)
        cy -= 16
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
    pdf.drawString(234, PAGE_HEIGHT - 68, "Poetry and Feeling Words")
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
GUIDE_INTRO = ("This pack teaches your child to read poems and "
               "find the words that tell how a poem feels and "
               "what it shows us. Your child will count lines "
               "and stanzas, find rhyming words, find words "
               "that tell what we see, hear, feel, and smell, "
               "and write a short poem of their own.")
GUIDE_SECTIONS = [
    ("How to help", [
        "Page 1: read the poem aloud. Count the lines "
        "together. Poems often arrange words in lines, and "
        "a group of lines is called a stanza. A poem can "
        "contain sentences too. A sentence is not defined by "
        "being on one printed line.",
        "Page 2: read the poem aloud. Listen for the words "
        "that sound the same at the end.",
        "Page 3: read the poem aloud. Ask, what does the "
        "child see, hear, feel, and smell?",
        "Page 4: read each poem aloud. Ask, how does it "
        "feel? Point to the words that tell you.",
        "Page 5: let your child choose words from the word "
        "bank, or use their own words.",
    ]),
    ("What your child learns", [
        "Poems often arrange words in lines. A group of "
        "lines is called a stanza. Words that rhyme sound "
        "the same at the end. Words can tell what we see, "
        "hear, feel, "
        "smell, and taste. The words in a poem tell how it "
        "feels. On Page 5 your child writes a short poem "
        "of their own, using a word that tells what they "
        "see, hear, or feel, and a word that tells how "
        "they feel.",
    ]),
    ("Answers", [
        ("Page 1", "4 lines, 2 stanzas. The poem is the text "
                   "in lines (A)."),
        ("Page 2", "hat / that, play / day. run, lake."),
        ("Page 3", "See: rose. Hear: hums. Feel: soft. "
                   "Smell: sweet."),
        ("Page 4", "Play Day: happy. My Lost Ball: sad. Clue "
                   "words: Play Day: run, play, jump, smile, "
                   "race, sunny. My Lost Ball: gone, looked, "
                   "alone, sigh, miss, cry."),
        ("Page 5", "A poem of their own. Check for lines, a "
                   "word that tells what they see, hear, or "
                   "feel, and a feeling word."),
    ]),
    ("Help a beginning writer", [
        "Let your child say each line aloud before writing it.",
        "Sound out words slowly. Spelling a word the way it "
        "sounds is fine.",
        "Praise the words your child chose first, then fix "
        "spelling together.",
        "Keep it short and cheerful. If the hand gets tired, "
        "take a break.",
    ]),
    ("If your child finds it hard", [
        "Page 2: say the two words aloud. Do they sound the "
        "same at the end?",
        "Page 3: point to the picture. Ask, what do you see? "
        "What do you hear?",
        "Page 4: look at the picture first. Does the child "
        "look happy or sad? Then find the words that tell you.",
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
                    max_w=500, leading=14)
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
                                max_w=500 - lw, leading=14)
                y -= 2
        else:
            for para in items:
                y = _guide_text(pdf, 56, y, para, size=12,
                                max_w=500, leading=14)
                y -= 1
        y -= 6
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 58,
        "Grade 1 Reading: Poetry and Feeling Words. "
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
    bundle = os.path.join(OUT_DIR, "poetry-and-feeling-words.pdf")
    guide = os.path.join(
        OUT_DIR, "poetry-and-feeling-words-parent-guide.pdf")
    review = os.path.join(
        OUT_DIR, "poetry-and-feeling-words-review.pdf")
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
    page_names = ["meet-a-poem", "listen-for-rhymes",
                  "words-we-can-feel", "how-does-the-poem-feel",
                  "my-little-poem"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR, "poetry-and-feeling-words-p%d-%s.pdf"
            % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    for name in ["poetry-and-feeling-words.pdf",
                 "poetry-and-feeling-words-parent-guide.pdf",
                 "poetry-and-feeling-words-review.pdf",
                 "poetry-and-feeling-words-p1-meet-a-poem.pdf",
                 "poetry-and-feeling-words-p2-listen-for-rhymes.pdf",
                 "poetry-and-feeling-words-p3-words-we-can-feel.pdf",
                 "poetry-and-feeling-words-p4-how-does-the-poem-feel.pdf",
                 "poetry-and-feeling-words-p5-my-little-poem.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text.
    for name in ["poetry-and-feeling-words.pdf",
                 "poetry-and-feeling-words-parent-guide.pdf"]:
        text = "".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
    print("em dash check: clean")


if __name__ == "__main__":
    main()
