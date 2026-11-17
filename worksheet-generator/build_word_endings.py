#!/usr/bin/env python3
"""Grade 1 Reading - Word Endings: -s, -es, -ed, -ing (RF.1.3(f), L.1.4(c)).

Resource 11 in the approved Grade 1 Reading roadmap (Tier 2 core).
The child reads words with inflectional endings and sees how an
ending changes what a word means: -s and -es for more than one
or he, she, it does it; -ing for happening right now; -ed for
already happened. Roots are printed in dark navy and endings
in teal, so the child can see where the root ends and the
ending begins.

Plan approved 2026-11-16. 4 student pages plus a separate
one-page Parent Guide. No standards codes on child pages or
the guide. No em dash anywhere.

Page 1, One or More (-s and -es): plural -s/-es kept apart
from verb -s/-es by section. Picture pairs show one thing
against many. Words: cats, dogs, hens, boxes, dishes, buses
(more than one); runs, jumps, looks, sings, watches
(he, she, it does it). The -es words end in s, ch, sh, or x:
buses, boxes, dishes, watches. v2: adult line now covers
both uses ("Ask, is it one or more than one? Who does it?").
v3: explanation box and adult line use her exact final
wording (box: "-s or -es can mean more than one, or tell
what he, she, or it does" with cat/cats, run/runs,
box/boxes, dish/dishes; adult line asks "How many?" for the
top section and "What does he, she, or it do?" for the
bottom section). Illustrations, layout, and activities
unchanged.
Page 2, Happening Now (-ing): match each -ing word to its
action picture. Words: jumping, looking, playing, singing,
walking, helping. The ending adds on directly; no doubling
or drop-e rules in this pack. v2: words in a 3x2 grid on the
left, large pictures (radius 48) in a 3x2 grid on the right,
open middle for drawing lines, no matching dots. v3: back to
two vertical columns, one word and one picture per row,
pictures radius 35, open middle for lines, no dots, because
the grid confused young children.
Page 3, Already Happened (-ed): match each root to its past
form. Words: jumped, looked, played, walked, helped, washed.
v2: roots with a large supporting picture (radius 40) in a
3x2 grid on the left, past forms in a 3x2 grid on the right,
open middle for drawing lines, no matching dots. v3: back to
two vertical columns, one root with its picture on the left
and one past form on the right per row, pictures radius 33,
open middle for lines, no dots, because the grid confused
young children.
Page 4, Pick the Ending: mixed-ending sentences with exactly
one correct ending per item. Each sentence has a picture and
a clue word (now, yesterday, two, every day, he, she).
  1. Two dog___ play in the yard. (-s; dogs)
  2. He is jump___ now. (-ing; jumping)
  3. She wash___ the cups yesterday. (-ed; washed)
  4. Two bus___ stop at the school. (-es; buses)
  5. She look___ at the red bird every day. (-s; looks)
  6. He watch___ the show every day. (-es; watches)
Every other ending is ungrammatical in its sentence: "every
day" blocks -ed in items 5 and 6 ("She looked every day" is
wrong), "yesterday" blocks -s in item 3, "is" blocks -s/-ed
in item 2, and "Two" blocks -ed/-ing in items 1 and 4.

Decoding audit (General American, phonemes not letters),
verified against Resources 1-3 (short vowels; blends;
digraphs sh, ch, th, wh, ph; final-e; vowel teams ai, ay,
ee, ea, oa, ow as long o) plus familiar high-frequency words:
  P1: cat, dog, hen, box, dish (sh), watch (ch), bus, run,
      jump, look (oo), sing, all short vowels and taught
      digraphs. "sing" uses ng, a familiar word kept from
      the approved plan.
  P2: jump, look, play (ay), sing, walk, help. "walk" is a
      familiar high-frequency word kept from the approved
      plan; the rest are fully decodable.
  P3: jump, look, play, walk, help, wash (sh), all as P2.
  P4: "Two dogs play in the yard." (two, yard familiar),
      "He is jumping now.", "She washed the cups
      yesterday." (yesterday, cups familiar/decodable),
      "Two buses stop at the school.", "She looks at the
      red bird every day." (day, ay), "He watches the show
      every day." (show, ow as long o). All decodable.

Shared design code (logo, header, footer, circular-masked
pictures) is imported verbatim from build_phonics_az.py - do
not fork it here. Header title is drawn at 18pt (the full
title is 324pt at 22pt, wider than the 318pt space inside
the teal rule) and the subtitle at 14pt (327pt at 15pt,
also past the rule). Both now end inside the rule.

Pictures: 15 new in assets/word-endings/ (we-cats-pair,
we-dogs-pair, we-hens-pair, we-boxes-pair, we-dishes-pair,
we-buses-pair, we-boy-running, we-girl-jumping,
we-boy-looking, we-bird-singing, we-boy-watching,
we-kids-playing, we-girl-walking, we-boy-helping,
we-girl-washing), watercolor picture-book style, all JPEG.
The generator added invented names and labels to the first
versions; the pair images were cropped and three were
regenerated so no picture carries text. No approved animal
library picture fits the plural pairs, so all 15 are new.
v2 (2026-11-17): four action pictures remade clearer for
Pages 2-3 (we-boy-looking-v2, we-girl-walking-v2,
we-kids-helping-v2, we-kid-playing-v2). Looking has no bird,
walking has no basket, helping shows two children carrying
a box together, playing is one child tossing a ball. Page 1
keeps the original looking picture; only Pages 2-3 use v2.
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

TITLE = "Word Endings: -s, -es, -ed, -ing"
SUBTITLE = "Grade 1 Reading | Phonics and Word Reading"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "word-endings")


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


def _teach_box(pdf, top, heading, lines, height):
    """Teaching box: teal bold heading, navy body lines."""
    _panel(pdf, 40, top - height, 532, height)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, top - 20, heading)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    y = top - 40
    for line in lines:
        pdf.drawString(56, y, line)
        y -= 16
    return top - height


def _split_word(pdf, root, ending, x, y, font_size=18):
    """A word drawn with the root in navy and the ending in
    teal, starting at x. Returns the x just past the word."""
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.setFillColor(NAVY)
    pdf.drawString(x, y, root)
    x += stringWidth(root, "Helvetica-Bold", font_size)
    pdf.setFillColor(TEAL)
    pdf.drawString(x, y, ending)
    return x + stringWidth(ending, "Helvetica-Bold", font_size)


def _split_word_centred(pdf, root, ending, cx, y, font_size=18):
    """A word drawn with the root in navy and the ending in
    teal, centred on cx."""
    pdf.setFont("Helvetica-Bold", font_size)
    w = stringWidth(root + ending, "Helvetica-Bold", font_size)
    return _split_word(pdf, root, ending, cx - w / 2, y, font_size)


def _header(pdf):
    draw_header(pdf, TITLE, SUBTITLE, title_size=18,
                subtitle_size=14)


# ---------------------------------------------------------------------------
# Page 1 -- One or More (-s and -es)
# Two sections keep plural -s/-es apart from verb -s/-es.
# The child reads each word, circles the root, and underlines
# the ending. Picture pairs show one thing against many.
# ---------------------------------------------------------------------------
P1_PLURALS = [
    ("cat", "s", "word-endings/we-cats-pair.jpg"),
    ("dog", "s", "word-endings/we-dogs-pair.jpg"),
    ("hen", "s", "word-endings/we-hens-pair.jpg"),
    ("box", "es", "word-endings/we-boxes-pair.jpg"),
    ("dish", "es", "word-endings/we-dishes-pair.jpg"),
    ("bus", "es", "word-endings/we-buses-pair.jpg"),
]
P1_VERBS = [
    ("run", "s", "word-endings/we-boy-running.jpg"),
    ("jump", "s", "word-endings/we-girl-jumping.jpg"),
    ("look", "s", "word-endings/we-boy-looking.jpg"),
    ("sing", "s", "word-endings/we-bird-singing.jpg"),
    ("watch", "es", "word-endings/we-boy-watching.jpg"),
]


def _one_or_more(pdf):
    top = _page_title(
        pdf, "One or More",
        "Read each word. Circle the root. Underline the ending.")
    box_bottom = _teach_box(
        pdf, top,
        "Adding -s or -es can mean more than one, or tell what "
        "he, she, or it does.",
        ["cat becomes cats. run becomes runs.",
         "Some words need -es: box becomes boxes, "
         "dish becomes dishes."],
        80)
    # Section A: more than one, 2 cols x 3 rows, cells 256x58.
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, box_bottom - 14, "More than one")
    xs = [40, 316]
    tops_a = [box_bottom - 30 - i * 64 for i in range(3)]
    for i, (root, ending, img) in enumerate(P1_PLURALS):
        x0 = xs[i % 2]
        ptop = tops_a[i // 2]
        _panel(pdf, x0, ptop - 58, 256, 58)
        cy = ptop - 29
        _img_circle(pdf, img, x0 + 32, cy, 24, zoom=True)
        _split_word(pdf, root, ending, x0 + 66, cy - 6,
                    font_size=18)
    # Section B: he, she, it does it, 2 cols x 3 rows.
    bottom_a = tops_a[2] - 58
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, bottom_a - 14, "He, she, it does it")
    tops_b = [bottom_a - 30 - i * 64 for i in range(3)]
    for i, (root, ending, img) in enumerate(P1_VERBS):
        x0 = xs[i % 2]
        ptop = tops_b[i // 2]
        _panel(pdf, x0, ptop - 58, 256, 58)
        cy = ptop - 29
        _img_circle(pdf, img, x0 + 32, cy, 24, zoom=True)
        _split_word(pdf, root, ending, x0 + 66, cy - 6,
                    font_size=18)
    _adult_line(pdf, "Adult: For the top section, ask 'How many?' "
                     "For the bottom section, ask 'What does he, "
                     "she, or it do?'")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _one_or_more(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Happening Now (-ing)
# The child reads each -ing word and draws a line to its
# action picture. Pictures are scrambled so no word matches
# straight across.
# ---------------------------------------------------------------------------
P2_WORDS = [
    ("jump", "ing", "word-endings/we-girl-jumping.jpg"),
    ("look", "ing", "word-endings/we-boy-looking-v2.jpg"),
    ("play", "ing", "word-endings/we-kid-playing-v2.jpg"),
    ("sing", "ing", "word-endings/we-bird-singing.jpg"),
    ("walk", "ing", "word-endings/we-girl-walking-v2.jpg"),
    ("help", "ing", "word-endings/we-kids-helping-v2.jpg"),
]
# Picture order, shuffled against the word order above:
# playing, walking, singing, helping, jumping, looking.
# The v2 pictures (looking, walking, helping, playing) are
# clearer single-action images: looking has no bird, walking
# has no basket, helping shows two children carrying a box
# together, playing is one child tossing a ball.
P2_PICTURES = [
    "word-endings/we-kid-playing-v2.jpg",
    "word-endings/we-girl-walking-v2.jpg",
    "word-endings/we-bird-singing.jpg",
    "word-endings/we-kids-helping-v2.jpg",
    "word-endings/we-girl-jumping.jpg",
    "word-endings/we-boy-looking-v2.jpg",
]


def _happening_now(pdf):
    top = _page_title(
        pdf, "Happening Now",
        "Read each word. Draw a line to the matching picture.")
    box_bottom = _teach_box(
        pdf, top,
        "Adding -ing means the action is happening right now.",
        ["jump becomes jumping. The ending goes right on the",
         "end of the word."],
        66)
    # Two vertical columns, one word and one picture per row,
    # no dots. Words on the left, large pictures on the right,
    # open middle for drawing lines. Pictures are radius 35
    # circles (70pt across, up from 60pt) with the clearer
    # v2 images. Pictures shuffled so no word matches
    # straight across.
    tops = [box_bottom - 8 - i * 75 for i in range(6)]
    for i, ((root, ending, _img), pic) in enumerate(
            zip(P2_WORDS, P2_PICTURES)):
        cy = tops[i] - 35
        _split_word(pdf, root, ending, 60, cy - 7, font_size=20)
        _img_circle(pdf, pic, 470, cy, 35, zoom=True)
    _adult_line(pdf, "Adult: Act out each word with your child. "
                     "Then your child matches it.")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _happening_now(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Already Happened (-ed)
# The child reads each root and draws a line to the past form
# that means it already happened. Past forms are scrambled so
# no root matches straight across. The pictures show the same
# actions as Page 2, so the child links the action to its
# past form.
# ---------------------------------------------------------------------------
P3_ROOTS = [
    ("jump", "word-endings/we-girl-jumping.jpg"),
    ("look", "word-endings/we-boy-looking-v2.jpg"),
    ("play", "word-endings/we-kid-playing-v2.jpg"),
    ("walk", "word-endings/we-girl-walking-v2.jpg"),
    ("help", "word-endings/we-kids-helping-v2.jpg"),
    ("wash", "word-endings/we-girl-washing.jpg"),
]
# Past forms, scrambled against the root order above:
# walked, played, washed, helped, looked, jumped.
P3_PAST = [
    ("walk", "ed"),
    ("play", "ed"),
    ("wash", "ed"),
    ("help", "ed"),
    ("look", "ed"),
    ("jump", "ed"),
]


def _already_happened(pdf):
    top = _page_title(
        pdf, "Already Happened",
        "Read each word. Draw a line from the root\n"
        "to the word that means it already happened.")
    box_bottom = _teach_box(
        pdf, top,
        "Adding -ed means it already happened.",
        ["jump becomes jumped. walk becomes walked.",
         "The word tells about yesterday."],
        66)
    # Two vertical columns, one root and one past form per
    # row, no dots. Roots on the left with a large supporting
    # picture beside each, past forms on the right, open
    # middle for drawing lines. Pictures are radius 33
    # circles (66pt across, up from 56pt) with the clearer
    # v2 images. Past forms shuffled so no root matches
    # straight across.
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(60, box_bottom - 14, "Root word")
    pdf.drawString(372, box_bottom - 14, "Already happened")
    tops = [box_bottom - 26 - i * 72 for i in range(6)]
    for i, ((root, img), (proot, ending)) in enumerate(
            zip(P3_ROOTS, P3_PAST)):
        cy = tops[i] - 33
        _img_circle(pdf, img, 86, cy, 33, zoom=True)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(130, cy - 7, root)
        _split_word(pdf, proot, ending, 372, cy - 7, font_size=20)
    _adult_line(pdf, "Adult: Say each pair aloud. "
                     "Yesterday, she jumped.")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _already_happened(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Pick the Ending
# Six sentences, each with a picture and a clue word (two,
# now, yesterday, every day, he, she). The child circles the
# one ending that makes the sentence right. See the module
# docstring for the uniqueness check on every item.
# ---------------------------------------------------------------------------
P4_ITEMS = [
    ("Two dog", " play in the yard.",
     "word-endings/we-dogs-pair.jpg", "s"),
    ("He is jump", " now.",
     "word-endings/we-girl-jumping.jpg", "ing"),
    ("She wash", " the cups yesterday.",
     "word-endings/we-girl-washing.jpg", "ed"),
    ("Two bus", " stop at the school.",
     "word-endings/we-buses-pair.jpg", "es"),
    ("She look", " at the red bird every day.",
     "word-endings/we-boy-looking.jpg", "s"),
    ("He watch", " the show every day.",
     "word-endings/we-boy-watching.jpg", "es"),
]
P4_ENDINGS = ["-s", "-es", "-ed", "-ing"]


def _pick_ending(pdf):
    top = _page_title(
        pdf, "Pick the Ending",
        "Read each sentence. Circle the ending\n"
        "that makes the sentence right.")
    tops = [top - i * 80 for i in range(6)]
    for i, (before, after, img, _answer) in enumerate(P4_ITEMS):
        ptop = tops[i]
        cy = ptop - 38
        pdf.setFont("Helvetica-Bold", 16)
        pdf.setFillColor(NAVY)
        pdf.drawString(40, ptop - 26, before + "___")
        pdf.drawString(
            40 + stringWidth(before + "___", "Helvetica-Bold", 16),
            ptop - 26, after)
        _img_circle(pdf, img, 512, cy, 27, zoom=True)
        # Four ending pills to circle, on the line below.
        px = 40
        for ending in P4_ENDINGS:
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(1.5)
            pdf.roundRect(px, ptop - 68, 52, 26, 13, stroke=1,
                          fill=1)
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawCentredString(px + 26, ptop - 59, ending)
            px += 64
    _adult_line(pdf, "Adult: Read the clue word together. "
                     "Then your child picks the ending.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _pick_ending(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("One or More", build_p1_page),
    ("Happening Now", build_p2_page),
    ("Already Happened", build_p3_page),
    ("Pick the Ending", build_p4_page),
]


# ---------------------------------------------------------------------------
# Parent guide (separate one-page PDF, NOT in the student
# bundle). Plain language for parents, no standards codes.
# ---------------------------------------------------------------------------
GUIDE_TITLE = "How to Use This Pack"
GUIDE_INTRO = [
    "Word endings change what a word means. A small ending",
    "can make one thing into many things, or tell when",
    "something happens.",
]
GUIDE_SECTIONS = [
    ("The endings in this pack", [
        "-s and -es mean more than one, or he, she, it does it.",
        "-ing means the action is happening right now.",
        "-ed means it already happened.",
    ]),
    ("A note about how -ed sounds", [
        "The -ed ending does not always sound the same.",
        "In jumped and walked it sounds like t. In played",
        "it sounds like d. Say the whole word first, then",
        "look at the letters together.",
    ]),
    ("Answers: Page 1, One or More", [
        "cats, dogs, hens, boxes, dishes, buses",
        "runs, jumps, looks, sings, watches",
    ]),
    ("Answers: Page 2, Happening Now", [
        "jumping, looking, playing, singing, walking, helping",
    ]),
    ("Answers: Page 3, Already Happened", [
        "jump jumped, look looked, play played,",
        "walk walked, help helped, wash washed",
    ]),
    ("Answers: Page 4, Pick the Ending", [
        "dogs, jumping, washed, buses, looks, watches",
    ]),
    ("If your child finds it hard", [
        "Cover the ending. Read the root first. Then add",
        "the ending and read the whole word.",
        "Act out the word together. Then read it again.",
        "Go back to Page 1 and sort the words into one",
        "and more than one.",
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
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(234, PAGE_HEIGHT - 68, TITLE)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
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
        "Grade 1 Reading: Word Endings. "
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
    # v4 rebuilds Page 1 only. Pages 2-3 (v3), Page 4 (v1),
    # and the Parent Guide (v1) are unchanged and are NOT
    # rebuilt here.
    v4 = [
        ("One or More", build_p1_page,
         "word-endings-page-01-v3.pdf"),
    ]
    for title, builder, name in v4:
        path = os.path.join(OUT_DIR, name)
        builder(path)
        print("built %s: %s" % (name, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    bundle_parts = [name for _t, _b, name in v4] + [
        "word-endings-page-02-v3.pdf",
        "word-endings-page-03-v3.pdf",
        "word-endings-page-04-v1.pdf"]
    for name in bundle_parts:
        path = os.path.join(OUT_DIR, name)
        for page in PdfReader(path).pages:
            writer.add_page(page)
    bundle = os.path.join(OUT_DIR, "word-endings-v4.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 4
    print("bundle: %s (4 pages)" % bundle)
    for name in [n for _t, _b, n in v4] + ["word-endings-v4.pdf"]:
        path = os.path.join(OUT_DIR, name)
        size = os.path.getsize(path)
        print("%s %d bytes sha256 %s" % (name, size,
                                         _sha256(path)))
    # No em dash anywhere in the rebuilt pages' text.
    for _t, _b, name in v4:
        text = "".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
    print("em dash check: clean")


if __name__ == "__main__":
    main()
