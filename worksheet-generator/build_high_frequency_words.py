#!/usr/bin/env python3
"""Grade 1 Reading - High-Frequency Words: Read, Spell & Use.

Resource 12 in the approved Grade 1 Reading roadmap (Tier 2 core).
RF.1.3(g) and L.1.2(d) addressed (not mastered, not fully covered):
the child reads and spells 12 grade-appropriate irregularly
spelled words by their irregular part, not by whole-word
memorization. The regular parts are sounded out; only the
tricky part is learned by heart. Builds on Kindergarten
Common Words (11 words) and on Resources 1-3, 10, 11, which
taught the phonics patterns the regular parts rely on.

Plan approved 2026-11-17 with her refinements: title kept,
5 student pages plus a separate one-page Parent Guide,
"old" replaced by "would" (it pairs with "could": same ou
pattern and silent l), Page 3 simplified to six spacious
spelling activities (Set 1 only), Page 4 sentence completion
uses Set 2 (meaningful spelling practice for the other six),
every Page 4 sentence has one unambiguous answer, standards
described as addressed.

Title note: the approved title uses an em dash between the
two parts. The worksheet header uses a colon instead, per
the standing no-em-dash rule for all worksheets.

Marking (from Kindergarten Common Words, user-set): teal DOT
under each letter that says its taught sound; teal UNDERLINE
only under the tricky part (the heart part) the adult
guidance introduces. No heart symbols and no phonics
terminology on child-facing pages.

Sound-to-spelling (General American, phonemes not letters),
CORRECTED and verified 2026-11-17. Corrections from the
first draft: could and would have a SILENT l (missed before)
and their ou says short oo /u/ like in book, not long oo;
who has TWO tricky parts, wh says /h/ not /w/ (the taught
wh says /w/) and o says long oo; once has TWO tricky parts,
o makes a /w/ sound and ce says /s/ (soft c, not yet taught);
any ends in y saying /ee/, NOT like the K word my (where y
says long i); was, some, once use the up sound /u/ for the
vowel, and the s in was says /z/ like in is.
  was:  w dot, a line (/u/, not short a), s line (says /z/,
         not the regular /s/; same pattern as in is)
  said: s dot, ai line (/e/, not long a), d dot
  could: c dot, oul line (one unit: ou says /u/ and the l
         is silent, so the l makes no separate sound), d dot
  some: s dot, o line (/u/), m dot, e none (silent)
  give: g dot, i line (stays short), v dot, e none (silent)
  once: o line (makes /w/), n dot, ce line (says /s/)
  were: w dot, ere line (says /ur/)
  who:  wh line (says /h/), o line (says long oo)
  been: b dot, ee line (says short i), n dot
  know: k line (silent), n dot, ow dot (long o, taught)
  would: w dot, oul line (one unit, same as could), d dot
  any:  a line (/e/, not short a), n dot, y dot (says /ee/)

v2 (2026-11-17, her review corrections): the s in was is
now a LINE, not a dot, because s saying /z/ is not the
regular sound of s (her rule: every dot is a regular
sound-spelling correspondence). Page 1 once phrase changed
to "I went there once." Page 5 story rewritten as a natural
story about Sam, Max the dog, a red ball, and Ben at the
lake, using seven target words where they fit (once, was,
said, could, would, some, give); the other five are not
forced in. New Page 5 picture (Sam, Ben, Max, red ball).
Parent Guide corrected: was (a and s both tricky), once
(o makes a w sound though there is no w), who (w is silent),
been (some people say it like bean; spelling the same),
would (same as could), and the Page 5 answer (story uses
seven words, not all 12). Pages 2, 3, 4 are UNCHANGED
(approved v1) and are NOT rebuilt here.

v3 (2026-11-17, her final corrections): could and would
are now marked with ONE underline under "oul" (not two
separate underlines for ou and l), so the silent l is
included in the single tricky unit and does not imply a
separate sound. The guide's "once" explanation is her
exact wording. Page 5 story: "Ben got the ball" changed
to "Ben helped get the ball." Pages 3 and 4 are UNCHANGED
(approved v1) and are NOT rebuilt here; Page 2 is rebuilt
only for the would marking, which is the same ou + silent
l pattern as could.

Pages:
  P1: Meet the Words, Set 1 (was, said, could, some, give,
      once). Six panels, marked word plus picture plus phrase.
  P2: Meet the Words, Set 2 (were, who, been, know, would,
      any). Same layout as P1.
  P3: Spell the Words, Set 1. Six spacious activities: fill
      in the tricky part, then write the whole word. The
      missing parts are a, ai, oul, o, i, o.
  P4: Use the Words in Sentences, Set 2. Six sentences, word
      bank of the six Set 2 words, one unambiguous answer
      each. Answers: 1. were, 2. who, 3. been, 4. know,
      5. would, 6. any.
  P5: Read and Write on Your Own. A short story using all 12
      words, then two sentences of the child's own from a
      12-word bank.

Decoding audit (General American): every non-target word on
the pages is a Kindergarten Common Word, a passage word
already used in Resources 4, 9, 11, 13, 14 (has, and, to,
at, she, he, with, then, do, you, have, they, me), or
decodable from taught patterns (short vowels, blends,
digraphs, final-e, vowel teams ai, ay, ee, ea, oa, ow as
long o, two-syllable splitting). Familiar words kept from
the approved plan: puppy, hello, book, went, down, lake,
gate, home, way, red, pen, cups, mat, dogs, Sam, Ben.

Shared design code (logo, header, footer, circular-masked
pictures) is imported verbatim from build_phonics_az.py.
The marked-word drawing is imported verbatim from
build_common_words.py. Do not fork either here. Header
title is drawn at 18pt and the subtitle at 14pt, as in
Word Endings, so both end inside the teal rule.
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
from build_common_words import _marked_word

TITLE = "High-Frequency Words: Read, Spell & Use"
SUBTITLE = "Grade 1 Reading | High-Frequency Words"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "high-frequency-words")
ASSETS = "high-frequency-words/"


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


def _header(pdf):
    draw_header(pdf, TITLE, SUBTITLE, title_size=18,
                subtitle_size=14)


# ---------------------------------------------------------------------------
# Pages 1-2 -- Meet the Words
# Six panels (2 cols x 3 rows). Each shows the marked word
# large (Andika-Bold 40, dots and underlines per the marking
# table), a picture, and a short phrase using the word.
# ---------------------------------------------------------------------------
P1_ITEMS = [
    # word, marker groups, phrase, picture
    ("was", [("w", "dot"), ("a", "line"), ("s", "line")],
     "He was a puppy.", ASSETS + "hf-puppy.jpg"),
    ("said", [("s", "dot"), ("ai", "line"), ("d", "dot")],
     "She said, 'Hello!'", ASSETS + "hf-girl-speaking.jpg"),
    ("could", [("c", "dot"), ("oul", "line"), ("d", "dot")],
     "I could lift it.", ASSETS + "hf-child-lifting.jpg"),
    ("some", [("s", "dot"), ("o", "line"), ("m", "dot"),
              ("e", "none")],
     "I have some apples.", ASSETS + "hf-some-apples.jpg"),
    ("give", [("g", "dot"), ("i", "line"), ("v", "dot"),
              ("e", "none")],
     "Give me the ball.", ASSETS + "hf-child-giving-ball.jpg"),
    ("once", [("o", "line"), ("n", "dot"), ("ce", "line")],
     "I went there once.", ASSETS + "hf-child-slide.jpg"),
]

P2_ITEMS = [
    ("were", [("w", "dot"), ("ere", "line")],
     "They were at the lake.",
     ASSETS + "hf-two-children-lake.jpg"),
    ("who", [("wh", "line"), ("o", "line")],
     "Who is at the gate?", ASSETS + "hf-person-gate.jpg"),
    ("been", [("b", "dot"), ("ee", "line"), ("n", "dot")],
     "I have been to the lake.", ASSETS + "hf-child-lake.jpg"),
    ("know", [("k", "line"), ("n", "dot"), ("ow", "dot")],
     "I know the way.", ASSETS + "hf-child-path.jpg"),
    ("would", [("w", "dot"), ("oul", "line"), ("d", "dot")],
     "I would like a pen.", ASSETS + "hf-child-pen.jpg"),
    ("any", [("a", "line"), ("n", "dot"), ("y", "dot")],
     "Do you have any pens?", ASSETS + "hf-child-pens.jpg"),
]


def _meet_words(pdf, items, top):
    """Six word panels, starting at the given content top.
    Word at top-left, picture top-right, phrase below.
    Panel 250x150."""
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (word, groups, phrase, img) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = top - row * 166 - panel_h
        _panel(pdf, px0, py0, panel_w, panel_h)
        _marked_word(pdf, word, groups, px0 + 20, py0 + 96)
        _img_circle(pdf, img, px0 + 212, py0 + 112, 24,
                    zoom=True)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 14)
        pdf.drawString(px0 + 20, py0 + 45, phrase)


def _meet_p1(pdf):
    top = _page_title(
        pdf, "Meet the Words",
        "Read each word. Dots show sounds to sound out.\n"
        "The line shows the tricky part to remember.")
    _meet_words(pdf, P1_ITEMS, top)
    _adult_line(pdf, "Adult: Read each word together. Dots show "
                     "sounds to sound out. The line shows the "
                     "tricky part.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _meet_p1(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def _meet_p2(pdf):
    top = _page_title(
        pdf, "Meet More Words",
        "Read each word. Dots show sounds to sound out.\n"
        "The line shows the tricky part to remember.")
    _meet_words(pdf, P2_ITEMS, top)
    _adult_line(pdf, "Adult: Read each word together. Ask your "
                     "child to point to the tricky part.")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _meet_p2(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Spell the Words (Set 1)
# Six spacious activities. Each panel shows a picture, the
# word with its tricky part blanked out (a teal line), and a
# ruled line to write the whole word. The missing parts are
# a, ai, oul, o, i, o. Set 2 gets its spelling practice on
# Pages 4 (writing the word in a sentence) and 5 (writing
# sentences of the child's own).
# ---------------------------------------------------------------------------
P3_ITEMS = [
    # word, blank start index, blank length, picture, answer
    ("was", 1, 1, ASSETS + "hf-puppy.jpg", "a"),
    ("said", 1, 2, ASSETS + "hf-girl-speaking.jpg", "ai"),
    ("could", 1, 3, ASSETS + "hf-child-lifting.jpg", "oul"),
    ("some", 1, 1, ASSETS + "hf-some-apples.jpg", "o"),
    ("give", 1, 1, ASSETS + "hf-child-giving-ball.jpg", "i"),
    ("once", 0, 1, ASSETS + "hf-child-slide.jpg", "o"),
]

GAP_FONT, GAP_SIZE = "Andika-Bold", 28


def _gapped_word(pdf, word, blank_start, blank_len, x, baseline):
    """Draw the word with a teal blank line replacing the
    letters [blank_start:blank_start+blank_len]. The child
    writes the missing letters on the blank line."""
    pdf.setFont(GAP_FONT, GAP_SIZE)
    before = word[:blank_start]
    missing = word[blank_start:blank_start + blank_len]
    after = word[blank_start + blank_len:]
    pdf.setFillColor(NAVY)
    cx = x
    if before:
        pdf.drawString(cx, baseline, before)
        cx += stringWidth(before, GAP_FONT, GAP_SIZE)
    bw = stringWidth(missing, GAP_FONT, GAP_SIZE)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(cx + 2, baseline, cx + bw - 2, baseline)
    cx += bw
    if after:
        pdf.drawString(cx, baseline, after)
        cx += stringWidth(after, GAP_FONT, GAP_SIZE)
    return cx


def _spell_words(pdf):
    top = _page_title(
        pdf, "Spell the Words",
        "Fill in the tricky part. Then write the whole word.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (word, bstart, blen, img, _ans) in enumerate(P3_ITEMS):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 166 - panel_h
        _panel(pdf, px0, py0, panel_w, panel_h)
        _img_circle(pdf, img, px0 + 30, py0 + 118, 20,
                    zoom=True)
        _gapped_word(pdf, word, bstart, blen, px0 + 62,
                     py0 + 110)
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawString(px0 + 20, py0 + 58, "Write the word:")
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1)
        pdf.line(px0 + 20, py0 + 35, px0 + 230, py0 + 35)
    _adult_line(pdf, "Adult: Say the word. Ask which part is "
                     "tricky. Help your child write it, then "
                     "write the whole word.")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _spell_words(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Use the Words in Sentences (Set 2)
# Six sentences, each missing one Set 2 word. The word bank
# holds the six Set 2 words, shuffled. Every sentence has
# exactly one word that fits, checked against all six bank
# words: "were" is the only past plural verb for the dogs;
# "who" is the only question word; "been" is the only word
# that follows "have"; "know" is the only verb that fits
# "I ___ the way home"; "would" is the only word that fits
# "I ___ like"; "any" is the only word that fits
# "Do you have ___ cups?".
# ---------------------------------------------------------------------------
P4_ITEMS = [
    ("The dogs ", " on the mat.",
     ASSETS + "hf-dogs-mat.jpg", "were"),
    ("", " is at the gate?",
     ASSETS + "hf-person-gate.jpg", "who"),
    ("I have ", " to the lake.",
     ASSETS + "hf-child-lake.jpg", "been"),
    ("I ", " the way home.",
     ASSETS + "hf-child-home.jpg", "know"),
    ("I ", " like a red pen.",
     ASSETS + "hf-child-pen.jpg", "would"),
    ("Do you have ", " cups?",
     ASSETS + "hf-cups.jpg", "any"),
]
# Word bank, shuffled against the sentence order above:
# know, any, were, would, who, been.
P4_BANK = ["know", "any", "were", "would", "who", "been"]

BLANK_W = 80


def _use_words(pdf):
    top = _page_title(
        pdf, "Use the Words in Sentences",
        "Read each sentence. Pick the word that fits.\n"
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
                     "which word fits. Only one word fits each "
                     "sentence.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _use_words(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Read and Write on Your Own
# A short, natural story using seven target words where they
# fit (once, was, said, could, would, some, give). The other
# five (were, who, been, know, any) are not forced into the
# story; the child meets them on Pages 1-4 and can use them
# in the two sentences of their own. v2 story replaces the
# v1 dialogue, which forced all 12 words into an awkward
# conversation. Writing section unchanged (spacious, two
# sentences, 12-word bank).
# Story (57 words): Once, Sam was at the lake with his dog
# Max. A red ball was in the lake. Sam said, "Max, get the
# ball!" Max could not get it. Sam said, "I would like some
# help." Ben was at the lake. Ben said, "I will give you the
# ball." Ben got the ball, and Sam was so glad.
# ---------------------------------------------------------------------------
P5_STORY = [
    "Once, Sam was at the lake with his dog Max.",
    "A red ball was in the lake. Sam said, 'Max, get",
    "the ball!' Max could not get it. Sam said, 'I",
    "would like some help.' Ben was at the lake. Ben",
    "said, 'I will give you the ball.' Ben helped get",
    "the ball, and Sam was so glad.",
]
P5_BANK = ["was", "said", "could", "some", "give", "once",
           "were", "who", "been", "know", "would", "any"]


def _read_write(pdf):
    top = _page_title(
        pdf, "Read and Write on Your Own",
        "Read the story. Then write two sentences of your own.")
    # Story panel.
    _panel(pdf, 40, top - 150, 532, 150)
    _img_circle(pdf, ASSETS + "hf-sam-ben-max-lake.jpg", 500,
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
                            "Use words from the box.")
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
    ("Meet the Words", build_p1_page),
    ("Meet More Words", build_p2_page),
    ("Spell the Words", build_p3_page),
    ("Use the Words in Sentences", build_p4_page),
    ("Read and Write on Your Own", build_p5_page),
]


# ---------------------------------------------------------------------------
# Parent guide (separate one-page PDF, NOT in the student
# bundle). Plain language for parents, no standards codes.
# ---------------------------------------------------------------------------
GUIDE_TITLE = "How to Use This Pack"
GUIDE_INTRO = [
    "Some words do not follow the usual spelling patterns.",
    "Your child learns 12 of these words by sounding out",
    "the regular parts and remembering only the tricky part.",
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
        "Say the word together. Sound out the dotted letters.",
        "Point to the underlined part and say it together.",
        "Then read the whole word.",
        "On Page 3, fill in the tricky part, then write the word.",
        "On Page 4, read the sentence and ask which word fits.",
        "On Page 5, listen as your child reads, then help them",
        "write two sentences of their own.",
    ]),
    ("The tricky part in each word", [
        "was: the a says the up sound, not short a, and the s says z, like in is.",
        "said: the ai says short e, not long a.",
        "could: the ou says short oo, like in book. The l is silent.",
        "some: the o says the up sound. The e at the end is silent.",
        "give: the i stays short even with an e at the end. The e is silent.",
        "once sounds like 'wuns.' Its spelling is unusual, so help your child remember the tricky parts.",
        "were: the ere says ur.",
        "who: the wh says h, not w. The w is silent. The o says long oo.",
        "been: the ee says short i, not long e. Some people say it like bean. The spelling is the same.",
        "know: the k is silent. The ow says long o, like in snow.",
        "would: the ou says short oo, like in book. The l is silent. (The same as could.)",
        "any: the a says short e, not short a. The y at the end says ee.",
    ]),
    ("Answers", [
        "Page 3: was, said, could, some, give, once.",
        "Page 4: 1. were, 2. who, 3. been, 4. know, 5. would, 6. any.",
        "Page 5: the story uses once, was, said, could, would,",
        "some, and give. The two sentences are your child's own.",
    ]),
    ("If your child finds it hard", [
        "Sound out the dotted parts first. Focus on just the",
        "underlined part. Practice one word at a time.",
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
        "Grade 1 Reading: High-Frequency Words. "
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
    # v3 rebuilds Pages 1, 2, 5, and the Parent Guide only.
    # Pages 3 and 4 (v1) are unchanged and are NOT rebuilt
    # here; the v3 bundle reuses their v1 PDFs. Page 2 is
    # rebuilt only for the would marking (same ou + silent
    # l pattern as could).
    v3 = [
        ("Meet the Words", build_p1_page,
         "high-frequency-words-page-01-v3.pdf"),
        ("Meet More Words", build_p2_page,
         "high-frequency-words-page-02-v3.pdf"),
        ("Read and Write on Your Own", build_p5_page,
         "high-frequency-words-page-05-v3.pdf"),
    ]
    for title, builder, name in v3:
        path = os.path.join(OUT_DIR, name)
        builder(path)
        print("built %s: %s" % (name, title))
    guide = "high-frequency-words-parent-guide-v3.pdf"
    build_parent_guide(os.path.join(OUT_DIR, guide))
    print("built %s: Parent Guide" % guide)
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    bundle_parts = [
        "high-frequency-words-page-01-v3.pdf",
        "high-frequency-words-page-02-v3.pdf",
        "high-frequency-words-page-03-v1.pdf",
        "high-frequency-words-page-04-v1.pdf",
        "high-frequency-words-page-05-v3.pdf"]
    for name in bundle_parts:
        path = os.path.join(OUT_DIR, name)
        for page in PdfReader(path).pages:
            writer.add_page(page)
    bundle = os.path.join(OUT_DIR, "high-frequency-words-v3.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)
    for name in [n for _t, _b, n in v3] + [guide,
                                           "high-frequency-words-v3.pdf"]:
        path = os.path.join(OUT_DIR, name)
        size = os.path.getsize(path)
        print("%s %d bytes sha256 %s" % (name, size,
                                         _sha256(path)))
    # No em dash or en dash anywhere in the rebuilt pages' text.
    for name in [n for _t, _b, n in v3] + [guide]:
        text = "".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
    print("em dash check: clean")


if __name__ == "__main__":
    main()
