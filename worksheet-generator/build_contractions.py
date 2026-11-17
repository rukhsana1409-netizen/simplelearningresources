#!/usr/bin/env python3
"""Grade 1 Reading - Contractions: Read, Match & Write.

The next new Grade 1 Reading pack (not the original
roadmap's Resource 13, which is Meet the Characters, already
live). Codex assigns the catalog number at integration.
Placement: Grade 1 / Reading & Language / Grammar &
Sentences (not Phonics & Word Reading).

Twelve common contractions in two sets of six. The teaching
idea on every page: two words join to make one short word,
and the apostrophe takes the place of the missing letters.
The apostrophe is drawn in teal on Pages 1-2 so the child
sees it. No whole-word memorization, no phonics terminology
on child-facing pages.

Plan approved 2026-11-17 with her corrections: keep the 12
contractions and the five-page structure plus a separate
Parent Guide; fix Page 4 so each completed sentence is
grammatically correct and exactly one word-bank answer fits,
with no word repeated from inside the contraction; replace
the Page 5 ball story with a fresh picnic story; keep the
Parent Guide explanations, answer key, and the clear note
that won't is irregular; position under Grammar & Sentences;
do not reuse the original roadmap's Resource 13 identifier;
standards framed as RF.1.3(g) and L.1.2(d) supporting Grade
1 skills where applicable, and L.2.2(c) as an introduced
Grade 2 skill, not Grade 1 mastery.

Title note: the approved title uses an em dash between the
two parts. The worksheet header uses a colon instead, per
the standing no-em-dash rule for all worksheets.

The 12 contractions (two words, missing letters):
  Set 1: don't (do + not, o missing), can't (can + not,
         o missing), isn't (is + not, o missing),
         didn't (did + not, o missing),
         won't (will + not, IRREGULAR: will changes to
         wo, and the o in not is missing),
         it's (it + is, i missing)
  Set 2: I'm (I + am, a missing), that's (that + is,
         i missing), we're (we + are, a missing),
         you're (you + are, a missing),
         I'll (I + will, wi missing),
         I've (I + have, ha missing)

Pages:
  P1: Meet the Contractions, Set 1. Six panels, each with
      the contraction (apostrophe in teal), the two words
      it comes from, a picture, and a short phrase.
  P2: Meet More Contractions, Set 2. Same layout as P1.
  P3: Build the Contraction, Set 1. Six spacious
      activities: two words are given, the child writes
      the contraction on a ruled line.
  P4: Use the Contractions in Sentences, Set 2. Six
      sentences, word bank of the six Set 2 words,
      shuffled. Every sentence has exactly one word that
      fits, checked against all six bank words, and no
      sentence repeats a word already inside its answer.
      Answers: 1. I'm, 2. that's, 3. we're, 4. you're,
      5. I'll, 6. I've.
  P5: Read and Write on Your Own. A short, natural picnic
      story (47 words, 7 sentences) using seven
      contractions where they fit (I'm, it's, I'll, I've,
      we're, that's, you're). The other five (don't,
      can't, isn't, didn't, won't) are not forced in; the
      child meets them on Pages 1-4 and can use them in
      the two sentences of their own.

Decoding audit (General American): every non-target word on
the pages is a Kindergarten Common Word, a passage word
already used in Resources 4, 9, 11, 12, 13, 14, or
decodable from taught patterns (short vowels, blends,
digraphs, final-e, vowel teams ai, ay, ee, ea, oa, ow as
long o, two-syllable splitting). Familiar words kept from
the approved plan: sunny, reach, mine, see, fit, ball,
happy, dog, friends, best, help, got, lake, read, picnic,
ready, glad, pack, apples, cups, park, plan, helper.

Shared design code (logo, header, footer, circular-masked
pictures) is imported verbatim from build_phonics_az.py.
Do not fork it here. Header title is drawn at 18pt and the
subtitle at 14pt, as in Word Endings and High-Frequency
Words, so both end inside the teal rule.
"""
import hashlib
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter as _letter  # noqa: F401
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from build_phonics_az import (NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              _img_circle, draw_footer, draw_header,
                              draw_logo)

TITLE = "Contractions: Read, Match & Write"
SUBTITLE = "Grade 1 Reading | Contractions"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "contractions")
ASSETS = "contractions/"


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


def _header(pdf):
    draw_header(pdf, TITLE, SUBTITLE, title_size=18,
                subtitle_size=14)


def _contraction_word(pdf, word, x, baseline, size=36):
    """Draw the contraction with the apostrophe in teal and
    the letters in navy. Returns the x just past the word."""
    font = "Andika-Bold"
    pdf.setFont(font, size)
    before, sep, after = word.partition("'")
    cx = x
    if before:
        pdf.setFillColor(NAVY)
        pdf.drawString(cx, baseline, before)
        cx += stringWidth(before, font, size)
    if sep:
        pdf.setFillColor(TEAL)
        pdf.drawString(cx, baseline, sep)
        cx += stringWidth(sep, font, size)
    if after:
        pdf.setFillColor(NAVY)
        pdf.drawString(cx, baseline, after)
        cx += stringWidth(after, font, size)
    return cx


# ---------------------------------------------------------------------------
# Pages 1-2 -- Meet the Contractions
# Six panels (2 cols x 3 rows). Each shows the contraction
# large (apostrophe in teal), the two words it comes from,
# a picture, and a short phrase using the contraction.
# ---------------------------------------------------------------------------
P1_ITEMS = [
    # contraction, two words, phrase, picture
    ("don't", "do + not", "I don't know.",
     ASSETS + "ct-child-shrugging.jpg"),
    ("can't", "can + not", "I can't reach it.",
     ASSETS + "ct-child-reaching.jpg"),
    ("isn't", "is + not", "It isn't mine.",
     ASSETS + "ct-child-pointing-toy.jpg"),
    ("didn't", "did + not", "I didn't see it.",
     ASSETS + "ct-child-looking.jpg"),
    ("won't", "will + not", "It won't fit.",
     ASSETS + "ct-ball-box.jpg"),
    ("it's", "it + is", "It's sunny.",
     ASSETS + "ct-sunny-child.jpg"),
]

P2_ITEMS = [
    ("I'm", "I + am", "I'm happy.",
     ASSETS + "ct-happy-child.jpg"),
    ("that's", "that + is", "That's my dog.",
     ASSETS + "ct-child-dog.jpg"),
    ("we're", "we + are", "We're friends.",
     ASSETS + "ct-two-friends.jpg"),
    ("you're", "you + are", "You're my friend.",
     ASSETS + "ct-child-friend.jpg"),
    ("I'll", "I + will", "I'll help you.",
     ASSETS + "ct-child-helping.jpg"),
    ("I've", "I + have", "I've got a red ball.",
     ASSETS + "ct-child-red-ball.jpg"),
]


def _meet_contractions(pdf, items, top):
    """Six contraction panels, starting at the given content
    top. Contraction top-left (apostrophe in teal), two words
    below it, picture top-right, phrase below.
    Panel 250x150."""
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (word, two_words, phrase, img) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = top - row * 166 - panel_h
        _panel(pdf, px0, py0, panel_w, panel_h)
        _contraction_word(pdf, word, px0 + 20, py0 + 112, size=36)
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(px0 + 20, py0 + 90, two_words)
        _img_circle(pdf, img, px0 + 212, py0 + 112, 24,
                    zoom=True)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 14)
        pdf.drawString(px0 + 20, py0 + 45, phrase)


def _meet_p1(pdf):
    top = _page_title(
        pdf, "Meet the Contractions",
        "Read each short word. Two words join to make one.\n"
        "The apostrophe takes the place of the missing letters.")
    _meet_contractions(pdf, P1_ITEMS, top)
    _adult_line(pdf, "Adult: Read each short word together. "
                     "Say the two words, then the short word. "
                     "Point to the apostrophe.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _meet_p1(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def _meet_p2(pdf):
    top = _page_title(
        pdf, "Meet More Contractions",
        "Read each short word. Two words join to make one.\n"
        "The apostrophe takes the place of the missing letters.")
    _meet_contractions(pdf, P2_ITEMS, top)
    _adult_line(pdf, "Adult: Read each short word together. Ask "
                     "your child to say the two words it comes "
                     "from.")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _meet_p2(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Build the Contraction (Set 1)
# Six spacious activities. Each panel shows the two words
# with a plus sign, a picture, and a ruled line where the
# child writes the contraction (including the apostrophe).
# Set 2 gets its building practice on Page 4 (writing the
# word in a sentence) and Page 5 (writing sentences of the
# child's own).
# ---------------------------------------------------------------------------
P3_ITEMS = [
    # word1, word2, picture, answer
    ("do", "not", ASSETS + "ct-child-shrugging.jpg", "don't"),
    ("can", "not", ASSETS + "ct-child-reaching.jpg", "can't"),
    ("is", "not", ASSETS + "ct-child-pointing-toy.jpg", "isn't"),
    ("did", "not", ASSETS + "ct-child-looking.jpg", "didn't"),
    ("will", "not", ASSETS + "ct-ball-box.jpg", "won't"),
    ("it", "is", ASSETS + "ct-sunny-child.jpg", "it's"),
]


def _build_contractions(pdf):
    top = _page_title(
        pdf, "Build the Contraction",
        "Two words join to make one short word. Write it.\n"
        "Do not forget the apostrophe.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (w1, w2, img, _ans) in enumerate(P3_ITEMS):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = top - row * 166 - panel_h
        _panel(pdf, px0, py0, panel_w, panel_h)
        _img_circle(pdf, img, px0 + 30, py0 + 118, 20,
                    zoom=True)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 28)
        pdf.drawString(px0 + 62, py0 + 110, "%s + %s" % (w1, w2))
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(px0 + panel_w / 2, py0 + 78, "makes")
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawString(px0 + 20, py0 + 58, "Write the short word:")
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1)
        pdf.line(px0 + 20, py0 + 35, px0 + 230, py0 + 35)
    _adult_line(pdf, "Adult: Say the two words. Ask which letters "
                     "go away. Help your child write the short "
                     "word with the apostrophe.")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _build_contractions(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Use the Contractions in Sentences (Set 2)
# Six sentences, each missing one Set 2 contraction. The word
# bank holds the six Set 2 words, shuffled. Every sentence
# has exactly one word that fits, checked against all six
# bank words, and no sentence repeats a word already inside
# its answer contraction. Context is added where the
# contraction alone would be ambiguous:
#   1. "___ all by myself." -- I'm. "myself" is first-person
#      singular, so only "I am" can take it. "we're",
#      "you're", "that's", "I'll", "I've" are all wrong
#      before "myself".
#   2. "___ not my dog." -- that's. "not" blocks "I've":
#      "I have not my dog" is not standard English (the
#      form is "I don't have my dog"). "I'm", "we're",
#      "you're", "I'll" cannot take "not my dog".
#   3. "___ going to the park together." -- we're. The
#      picture shows the two children speaking about
#      themselves as they go together, so "we are" fits.
#      "I'm" cannot go "together" alone, "that's" cannot
#      go anywhere, "I'll" and "I've" cannot take "going".
#      "you're" is already used in sentence 4.
#   4. "___ my best friend." -- you're. The picture shows
#      the child talking face to face to a friend, so the
#      direct address fits. "that's" would point at a
#      third person, which the picture does not show, and
#      "that's" is already used in sentence 2. "I'm",
#      "we're", "I'll", "I've" cannot take "my best
#      friend".
#   5. "___ help you." -- I'll. Only "I will" takes the
#      base verb "help"; every other bank word is wrong
#      before "help".
#   6. "___ been to the lake." -- I've. Only "I have"
#      takes the past participle "been"; every other bank
#      word is wrong before "been".
# ---------------------------------------------------------------------------
P4_ITEMS = [
    ("", " all by myself.",
     ASSETS + "ct-child-reading.jpg", "I'm"),
    ("", " not my dog.",
     ASSETS + "ct-child-dog.jpg", "that's"),
    ("", " going to the park together.",
     ASSETS + "ct-two-friends.jpg", "we're"),
    ("", " my best friend.",
     ASSETS + "ct-child-friend.jpg", "you're"),
    ("", " help you.",
     ASSETS + "ct-child-helping.jpg", "I'll"),
    ("", " been to the lake.",
     ASSETS + "ct-child-lake.jpg", "I've"),
]
# Word bank, shuffled against the sentence order above:
# you're, I've, I'll, that's, we're, I'm.
P4_BANK = ["you're", "I've", "I'll", "that's", "we're", "I'm"]

BLANK_W = 80


def _use_contractions(pdf):
    top = _page_title(
        pdf, "Use the Contractions in Sentences",
        "Read each sentence. Pick the short word that fits.\n"
        "Write it on the line.")
    # Word bank pills, shuffled.
    bx = 40
    for word in P4_BANK:
        w = stringWidth(word, "Helvetica-Bold", 15) + 28
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(TEAL)
        pdf.setLineWidth(1.5)
        pdf.roundRect(bx, top - 34, w, 30, 15, stroke=1, fill=1)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(bx + w / 2, top - 25, word)
        bx += w + 10
    tops = [top - 48 - i * 76 for i in range(6)]
    for i, (before, after, img, _ans) in enumerate(P4_ITEMS):
        ptop = tops[i]
        cy = ptop - 34
        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor(NAVY)
        x = 40
        if before:
            pdf.drawString(x, ptop - 26, before)
            x += stringWidth(before, "Helvetica-Bold", 16)
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.2)
        pdf.line(x + 2, ptop - 26, x + BLANK_W - 2, ptop - 26)
        x += BLANK_W
        pdf.drawString(x, ptop - 26, after)
        _img_circle(pdf, img, 512, cy, 22, zoom=True)
    _adult_line(pdf, "Adult: Read the sentence together. Ask "
                     "which short word fits. Only one word fits "
                     "each sentence.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _use_contractions(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Read and Write on Your Own
# A short, natural picnic story (53 words, 7 sentences) about
# Ben and Mia getting ready for a picnic. It uses seven
# contractions where they fit naturally (I'm, it's, I'll,
# I've, we're, that's, you're). The other five (don't,
# can't, isn't, didn't, won't) are not forced in; the child
# meets them on Pages 1-4 and can use them in the two
# sentences of their own. Dialogue is carried by action
# beats (Mia smiled, Ben took, Mia held up, Ben took,
# Mia was glad, Ben smiled) with only one "said", so it
# reads naturally without repeating "said Mia" and "said
# Ben". The child must use a contraction in each of the
# two sentences of their own.
# Story: Ben and Mia are getting ready for a picnic. "I'm so
# glad it's sunny!" Mia smiled. "I'll pack the apples,"
# said Ben. "I've got the cups!" Mia held up the cups.
# "We're going to the park." Ben took the basket.
# "That's a good plan!" Mia was glad. "You're the best
# helper!" Ben smiled.
# ---------------------------------------------------------------------------
P5_STORY = [
    "Ben and Mia are getting ready for a picnic.",
    "'I'm so glad it's sunny!' Mia smiled. 'I'll pack",
    "the apples,' said Ben. 'I've got the cups!' Mia",
    "held up the cups. 'We're going to the park.' Ben",
    "took the basket. 'That's a good plan!' Mia was",
    "glad. 'You're the best helper!' Ben smiled.",
]
P5_BANK = ["don't", "can't", "isn't", "didn't", "won't", "it's",
           "I'm", "that's", "we're", "you're", "I'll", "I've"]


def _read_write(pdf):
    top = _page_title(
        pdf, "Read and Write on Your Own",
        "Read the story. Then write two sentences of your own,\n"
        "each with a contraction.")
    # Story panel.
    _panel(pdf, 40, top - 150, 532, 150)
    _img_circle(pdf, ASSETS + "ct-picnic-prep.jpg", 500,
                top - 75, 32, zoom=True)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13.5)
    y = top - 30
    for line in P5_STORY:
        pdf.drawString(56, y, line)
        y -= 20
    # Write your own sentences.
    wy = top - 176
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, wy, "Write two sentences of your own. "
                            "Use a contraction in each one.")
    # Word bank, two rows of six.
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    for r in range(2):
        row = P5_BANK[r * 6:(r + 1) * 6]
        text = "   ".join(row)
        pdf.drawCentredString(PAGE_WIDTH / 2, wy - 22 - r * 20,
                              text)
    # Two writing areas, two ruled lines each.
    for n, ly in enumerate([wy - 92, wy - 172]):
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(40, ly + 8, "%d." % (n + 1))
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1)
        pdf.line(62, ly, 572, ly)
        pdf.line(62, ly - 28, 572, ly - 28)
    _adult_line(pdf, "Adult: Listen as your child reads the "
                     "story. Then help them write two sentences "
                     "using words from the box.")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _read_write(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Meet the Contractions", build_p1_page),
    ("Meet More Contractions", build_p2_page),
    ("Build the Contraction", build_p3_page),
    ("Use the Contractions in Sentences", build_p4_page),
    ("Read and Write on Your Own", build_p5_page),
]


# ---------------------------------------------------------------------------
# Parent guide (separate one-page PDF, NOT in the student
# bundle). Plain language for parents, no standards codes.
# ---------------------------------------------------------------------------
GUIDE_TITLE = "How to Use This Pack"
GUIDE_INTRO = [
    "Two words can join to make one short word. The",
    "apostrophe takes the place of the missing letters.",
    "Your child learns 12 contractions this way.",
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
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(234, PAGE_HEIGHT - 68, TITLE)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(234, PAGE_HEIGHT - 90, "Parent Guide")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.6)
    pdf.line(60, PAGE_HEIGHT - 104, PAGE_WIDTH - 60,
             PAGE_HEIGHT - 104)


GUIDE_SECTIONS = [
    ("How to help", [
        "Say the two words together. Then say the short word.",
        "Point to the apostrophe. It takes the place of the",
        "missing letters.",
        "On Page 3, say the two words, then write the short word.",
        "On Page 4, read the sentence and ask which short word fits.",
        "On Page 5, listen as your child reads, then help them",
        "write two sentences of their own.",
    ]),
    ("The two words in each contraction", [
        "don't: do + not. The o in not is missing.",
        "can't: can + not. The o in not is missing.",
        "isn't: is + not. The o in not is missing.",
        "didn't: did + not. The o in not is missing.",
        "won't: will + not. This one is tricky. Will changes to",
        "wo, and the o in not is missing. It does not follow",
        "the usual rule, so help your child remember it as a whole word.",
        "it's: it + is. The i in is is missing.",
        "I'm: I + am. The a in am is missing.",
        "that's: that + is. The i in is is missing.",
        "we're: we + are. The a in are is missing.",
        "you're: you + are. The a in are is missing.",
        "I'll: I + will. The wi in will is missing.",
        "I've: I + have. The ha in have is missing.",
    ]),
    ("Answers", [
        "Page 3: don't, can't, isn't, didn't, won't, it's.",
        "Page 4: 1. I'm, 2. that's, 3. we're, 4. you're, 5. I'll, 6. I've.",
        "Page 5: the story uses I'm, it's, I'll, I've, we're,",
        "that's, and you're. The two sentences are your child's own.",
    ]),
    ("If your child finds it hard", [
        "Say the two words first. Point to the apostrophe.",
        "Practice one contraction at a time. Won't is the",
        "tricky one, so give it extra time.",
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
        "Grade 1 Reading: Contractions. "
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


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    # v3 rebuilds Page 4 only (her correction 2026-11-17:
    # sentence 3 changed from "together, Ben and I" to
    # "going to the park together"). Pages 1 and 2 (v1),
    # Page 3 (v2), and Page 5 (v2) are approved and
    # unchanged and are NOT rebuilt here. The Parent Guide
    # (v1) is unchanged; its Page 4 answers (1. I'm,
    # 2. that's, 3. we're, 4. you're, 5. I'll, 6. I've)
    # still match.
    v3 = [
        ("Use the Contractions in Sentences", build_p4_page,
         "contractions-page-04-v3.pdf"),
    ]
    for title, builder, name in v3:
        path = os.path.join(OUT_DIR, name)
        builder(path)
        print("built %s: %s" % (name, title))
    for name in [n for _t, _b, n in v3]:
        path = os.path.join(OUT_DIR, name)
        size = os.path.getsize(path)
        print("%s %d bytes sha256 %s" % (name, size,
                                         _sha256(path)))
    # No em dash or en dash anywhere in the rebuilt page's text.
    from pypdf import PdfReader
    for name in [n for _t, _b, n in v3]:
        text = "".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
    print("em dash check: clean")


if __name__ == "__main__":
    main()
