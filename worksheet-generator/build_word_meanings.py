#!/usr/bin/env python3
"""Grade 1 Reading - Word Meanings.

Resource 21 in the approved and locked Grade 1 Reading and
Language Arts roadmap (audit 2026-11-05). Plan approved
2026-11-20 with the user's refinements, after the one-time
comprehensive curriculum and overlap audit
(~/workspace/research_notes/grade-1-ela-audit-20261120/
report.md), 5 student pages plus a separate 1-page Parent
Guide.

Placement: Grade 1 / Reading and Language / Vocabulary.
Standards L.1.4(a), L.1.4(b), L.1.5(a), L.1.5(b), L.1.5(c),
L.1.5(d) taught. L.1.4(c) is explicitly NOT taught: it is
covered by R11 Word Endings (look/looks/looked/looking
plus five other roots), so it is dropped here. Standards
appear on the resource page only, never on student pages
or the Parent Guide.

Boundaries, verified against the built packs 2026-11-20:
R18 Poetry and Feeling Words only names feelings flat
(P4 circles happy/sad/calm, one label per poem; P5 lists
happy/glad/calm as interchangeable picks), so ranking
words by strength is genuinely new here. R11 teaches
inflectional endings (-s/-ed/-ing) as meaning clues, so
this pack teaches derivational affixes only, with a
one-line contrast and nothing more. R15 Page 3 teaches
word meaning from a glossary, so the context-clue work
here comes from the sentence and picture, never from a
glossary. R20 taught ripe and sweet as two incidental
items with no strategy; those words are NOT reused.
R2 Page 4 sorts by sound, not by meaning. R12 Page 4 is
cloze sentence-fit, not working out an unknown word's
meaning. Resource 22 owns pronouns as grammar; no
pronoun teaching here. Resource 23 owns because as a
taught joiner; no joining-word teaching here, and the
clue sentences avoid "because".

Her refinements (binding): Page 3 uses mad/angry/furious,
NOT happy/glad/joyful, on a visible intensity scale, and
must not imply subjective word distinctions are always
absolute (the Parent Guide says people can disagree
about close words). Page 4 teaches naming categories
and defining attributes, not just Preschool-level
sorting, with a model and guided practice. Page 5 has
generous drawing and writing space and an optional
sentence starter.

Final refinements, approved 2026-11-20 (v2): Page 3
uses glance/look/stare, NOT peek/look/stare, and the
progression is how briefly or closely someone looks,
not absolute word strength. Page 4 replaces the
word-sorting section with Name the Group and Tell Why:
name the group and tell what the words share, keeping
the model and two guided definitions. Page 5's starter
is "I chose ___. It reminds me of ___.". Pages 1 and
2 are unchanged from v1 (pixel-identical).

"For adults" website guidance (57 words, for the
resource page catalog adultGuidance; NOT printed in the
Parent Guide, per the R18/R19/R20 precedent -- the guide
carries its own "What your child learns" paraphrase):
"Words can have shades of meaning. Help your child use
the words around a hard word to work out what it means.
Talk about how un- and -ful change a word. Ask which
word is stronger: big, huge, or gigantic? Help your
child name groups, tell what they share, and use a word
from their own day."

Illustrations: seven new original watercolor storybook
JPEGs in the approved style from Resources 16 to 20
(p1-brave-dog, p1-drowsy-child, p1-sturdy-box,
p2-helpful-child, p3-glance-look-stare, p3-elephants,
p3-faces). The v1 p3-peek-look-stare image was deleted
in the v2 revision (it showed a child peeking behind a
door, which no longer matched "glance"). JPEGs embed as
DCT, so the PDF stays small. Pages 4 and 5 need no new
pictures (Page 4 is word-level work; Page 5 is the
child's own drawing).

Shared design code (logo, header, footer) is imported
verbatim from build_phonics_az.py. Do not fork it here.
Header title is drawn at 18pt and the subtitle at 14pt;
both end inside the teal rule.

PROCESS CATCH from Resource 20 (do not repeat it): the
R20 builder did NOT regenerate preview PNGs, so
preview-6 was stale after a guide-only rebuild. This
builder regenerates all six preview PNGs from the final
bundle and guide with pdftoppm at 300 dpi, and main()
asserts every preview file exists before reporting.
"""
import hashlib
import os
import subprocess

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter as _letter  # noqa: F401
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from build_phonics_az import (NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              draw_footer, draw_header, draw_logo)

TITLE = "Word Meanings"
SUBTITLE = "Grade 1 Reading | Word Meanings"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "word-meanings")
IMG_DIR = OUT_DIR  # watercolor illustration JPEGs live beside the PDFs

ADULT_GUIDANCE = ("Words can have shades of meaning. Help "
                  "your child use the words around a hard "
                  "word to work out what it means. Talk about "
                  "how un- and -ful change a word. Ask which "
                  "word is stronger: big, huge, or gigantic? "
                  "Help your child name groups, tell what "
                  "they share, and use a word from their own "
                  "day.")


def _fit(text, font, size, max_w, what):
    """Fail the build if a line would overflow its panel."""
    w = stringWidth(text, font, size)
    assert w <= max_w, "%s is %.1fpt, over %dpt: %r" % (
        what, w, max_w, text)
    return w


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


def _page_title(pdf, title, subtitle, instruction):
    """Page title at 642, subtitle at 624 (teal bold 12.5),
    instruction line(s) at 606 (and 588). subtitle may be
    None, in which case instruction lines start at 624.
    instruction is a string (one line) or a list of lines.
    Returns 592, the y of the top of the content area."""
    _fit(title, "Helvetica-Bold", 15, 532, "page title")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, title)
    if subtitle:
        _fit(subtitle, "Helvetica-Bold", 12.5, 532,
             "page subtitle")
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawCentredString(PAGE_WIDTH / 2, 624, subtitle)
        iy = 606
    else:
        iy = 624
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 12)
    lines = instruction if isinstance(instruction, list) \
        else [instruction]
    for line in lines:
        _fit(line, "Helvetica", 12, 532, "instruction")
        pdf.drawCentredString(PAGE_WIDTH / 2, iy, line)
        iy -= 18
    return 592


def _panel(pdf, x, y, w, h):
    """A light rounded panel. (x, y) is the bottom-left corner."""
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(x, y, w, h, 14, stroke=1, fill=1)


def _header(pdf):
    draw_header(pdf, TITLE, SUBTITLE, title_size=18,
                subtitle_size=14)


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


def _remember_box(pdf, y, h, lines, width=532):
    """A Remember panel with a teal title and centred lines
    of text. (x, y) is the bottom-left corner, x is always
    40. The title sits 18 below the top edge and the lines
    start 38 below it, so a one-line box needs height 48
    and a two-line box needs height 68."""
    _panel(pdf, 40, y, width, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(40 + width / 2, y + h - 18,
                          "Remember")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    ly = y + h - 38
    for line in lines:
        _fit(line, "Helvetica", 12.5, width - 32,
             "Remember line")
        pdf.drawCentredString(40 + width / 2, ly, line)
        ly -= 17


def _draw_segments(pdf, x, y, segments, size=13):
    """Draw (text, font, color) segments left to right
    from x at baseline y. A segment may be ("__blank__",
    width) to draw a ruled blank of that width instead of
    text. Returns the x after the last segment."""
    for seg in segments:
        if seg[0] == "__blank__":
            pdf.setStrokeColor(NAVY)
            pdf.setLineWidth(1)
            pdf.line(x, y - 3, x + seg[1], y - 3)
            x += seg[1]
            continue
        text, font, color = seg
        pdf.setFillColor(color)
        pdf.setFont(font, size)
        pdf.drawString(x, y, text)
        x += stringWidth(text, font, size)
    return x


# ---------------------------------------------------------------------------
# Page 1 -- Hard Word? Look Around It (L.1.4(a))
# ---------------------------------------------------------------------------
def _strategy_box(pdf, y, h):
    """The context-clue strategy box: three centred lines.
    y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 16,
                          "Hard word? Look at the words around it.")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 33,
                          "Look at the picture.")
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 50,
                          "Ask: What makes sense here?")


def _clue_row(pdf, y, h, image, line1, line2, question,
              choices):
    """One context-clue item: the picture on the left, the
    two-line sentence, the question, and two meaning pills
    below it. The child circles the pill that fits. y is
    the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, image, 100, y + h / 2, 104, 84)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13)
    _fit(line1, "Helvetica", 13, 386, "clue sentence")
    _fit(line2, "Helvetica", 13, 386, "clue sentence")
    pdf.drawString(170, y + h - 20, line1)
    pdf.drawString(170, y + h - 38, line2)
    _fit(question, "Helvetica", 13, 386, "clue question")
    pdf.drawString(170, y + h - 60, question)
    _word_pills(pdf, 170, y + 8, choices, size=13)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Hard Word? Look Around It",
        "Use the words around it.",
        "Read each sentence. Circle what the word means.")
    _strategy_box(pdf, 524, 64)
    _clue_row(
        pdf, 412, 106,
        os.path.join(IMG_DIR, "p1-brave-dog.jpg"),
        "The little dog was brave.",
        "It did not run away from the big storm.",
        "What does brave mean? Circle one.",
        ["not afraid", "very fast"])
    _clue_row(
        pdf, 300, 106,
        os.path.join(IMG_DIR, "p1-drowsy-child.jpg"),
        "Ben was drowsy.",
        "His eyes kept closing.",
        "What does drowsy mean? Circle one.",
        ["sleepy", "hungry"])
    _clue_row(
        pdf, 188, 106,
        os.path.join(IMG_DIR, "p1-sturdy-box.jpg"),
        "The sturdy box held all the heavy books.",
        "It did not break.",
        "What does sturdy mean? Circle one.",
        ["strong", "soft"])
    _remember_box(pdf, 104, 68, [
        "Look at the words around a hard word.",
        "They can tell you what it means."])
    _adult_line(pdf, "Read each sentence aloud. Ask: What "
                     "makes sense here?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Word Parts Change the Meaning (L.1.4(b))
# ---------------------------------------------------------------------------
AFFIX_MEANINGS = [
    ("un-", "means not", "re-", "means again"),
    ("-ful", "means full of", "-less", "means without"),
]

BUILD_ROWS = [
    # (build segments, meaning choices)
    ([("un", "Helvetica-Bold", TEAL),
      (" + happy = ", "Helvetica", NAVY),
      ("unhappy", "Helvetica-Bold", NAVY)],
     ["not happy", "very happy"]),
    ([("re", "Helvetica-Bold", TEAL),
      (" + do = ", "Helvetica", NAVY),
      ("redo", "Helvetica-Bold", NAVY)],
     ["do it again", "do it first"]),
    ([("help", "Helvetica-Bold", NAVY),
      (" + ", "Helvetica", NAVY),
      ("ful", "Helvetica-Bold", TEAL),
      (" = ", "Helvetica", NAVY),
      ("helpful", "Helvetica-Bold", NAVY)],
     ["full of help", "no help at all"]),
    ([("fear", "Helvetica-Bold", NAVY),
      (" + ", "Helvetica", NAVY),
      ("less", "Helvetica-Bold", TEAL),
      (" = ", "Helvetica", NAVY),
      ("fearless", "Helvetica-Bold", NAVY)],
     ["without fear", "full of fear"]),
]


def _teach_panel(pdf, y, h):
    """The four affix meanings, two lines of two, with the
    helpful-child picture on the right. y is the bottom
    of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 20,
                   "What does each part mean?")
    for i, (a1, m1, a2, m2) in enumerate(AFFIX_MEANINGS):
        ly = y + h - 44 - i * 22
        _draw_segments(pdf, 56, ly, [
            (a1, "Helvetica-Bold", TEAL),
            (" " + m1, "Helvetica", NAVY)], size=13)
        _draw_segments(pdf, 260, ly, [
            (a2, "Helvetica-Bold", TEAL),
            (" " + m2, "Helvetica", NAVY)], size=13)
    _draw_image(pdf, os.path.join(IMG_DIR,
                                  "p2-helpful-child.jpg"),
                500, y + h / 2, 90, 90)


def _build_row(pdf, y, h, segments, choices):
    """One word-build row: the build on the left, two
    meaning pills right-aligned on the same line. The
    child circles the meaning the built word has. y is
    the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    _draw_segments(pdf, 56, y + h / 2 - 5, segments, size=14)
    total_w = sum(stringWidth(w, "Helvetica-Bold", 13) + 22
                  for w in choices) + 10 * (len(choices) - 1)
    px = 556 - total_w
    _word_pills(pdf, px, y + h / 2 - 13, choices, size=13)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Word Parts Change the Meaning",
        "A small part can change a word.",
        "Build each word. Circle what it means.")
    _teach_panel(pdf, 488, 100)
    for i, (segments, choices) in enumerate(BUILD_ROWS):
        _build_row(pdf, 406 - i * 82, 76, segments, choices)
    _remember_box(pdf, 96, 48, [
        "-ed tells when it happened. un- and -ful tell what "
        "the word means."])
    _adult_line(pdf, "Build each word. Ask: What does this "
                     "part mean?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Stronger and Stronger (L.1.5(d))
# ---------------------------------------------------------------------------
# Each set is presented in a shuffled order, so the child
# must judge the strength, not read top to bottom as
# 1-2-3. Answers: glance 1, look 2, stare 3; big 1, huge 2,
# gigantic 3; mad 1, angry 2, furious 3. The first set is
# about how briefly or closely someone looks, not absolute
# word strength: a glance is a quick look, a stare is a
# long, close look.
SHADE_SETS = [
    ("p3-glance-look-stare.jpg", ["look", "stare", "glance"]),
    ("p3-elephants.jpg", ["gigantic", "big", "huge"]),
    ("p3-faces.jpg", ["furious", "mad", "angry"]),
]


def _shade_row(pdf, y, h, image, words):
    """One shades row: the picture on the left with a
    visible intensity scale under it (1 = a little,
    3 = a lot), and the three words on the right, each
    with an empty box the child writes 1, 2, or 3 in.
    y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, os.path.join(IMG_DIR, image),
                140, y + h - 44, 190, 80)
    # Intensity scale under the picture: 1 at the left
    # (a little), 3 at the right (a lot). The image box
    # ends 46pt above the panel bottom, so the numbers
    # (top at y+38) clear it by 8pt.
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.2)
    pdf.line(56, y + 22, 224, y + 22)
    for i, tx in enumerate((56, 140, 224)):
        pdf.line(tx, y + 18, tx, y + 26)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawCentredString(tx, y + 28, str(i + 1))
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(56, y + 8, "a little")
    pdf.drawRightString(224, y + 8, "a lot")
    for i, word in enumerate(words):
        cy = y + h - 30 - i * 35
        pdf.setStrokeColor(BOX_STROKE)
        pdf.setLineWidth(1.2)
        pdf.rect(280, cy - 12, 24, 24, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(314, cy - 5, word)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Stronger and Stronger",
        "Put the words in order.",
        "Write 1 for a little, 2 in the middle, 3 for a lot.")
    for i, (image, words) in enumerate(SHADE_SETS):
        _shade_row(pdf, 458 - i * 136, 130, image, words)
    _remember_box(pdf, 96, 68, [
        "Some words tell how much. A glance is a quick look.",
        "A stare is a long, close look. Put the words in "
        "order, from a little to a lot."])
    _adult_line(pdf, "Act out a glance, then a stare. Ask: "
                     "Which look is longer?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Name the Group and Tell Why (L.1.5(a) + L.1.5(b))
# ---------------------------------------------------------------------------
# v2 (approved 2026-11-20): the Preschool-style word
# sorting section is gone. Each set gives three words;
# the child names the group and tells what the words
# share, choosing the shared attribute from the bank.
# Answers: Animals (dog, cat, bird) have legs and can
# move; Fruits (apple, banana, orange) have seeds;
# Clothes (hat, coat, shoes) are things we wear.
GROUP_SETS = [
    "dog, cat, bird",
    "apple, banana, orange",
    "hat, coat, shoes",
]
ATTRIBUTE_BANK = ["have seeds", "are things we wear",
                  "have legs and can move"]


def _attribute_bank(pdf, y):
    """One bank line at the top of the activity: the label
    and the three attribute chips in shuffled order. y is
    the bottom of the pills (26 tall). The pills are 12pt
    (not 13pt) so the longest chip, "have legs and can
    move", still fits on one line inside the right margin:
    from x=164 the three pills end at 560, inside 572."""
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + 9, "Attribute bank:")
    _word_pills(pdf, 164, y, ATTRIBUTE_BANK, size=12)


def _group_set_panel(pdf, y, h, words):
    """One group set: the three words on one line, then
    "Name the group:" with a blank, then "Tell why: They
    all" with a blank wide enough for the longest
    attribute ("have legs and can move", 141pt of text
    in 13pt Helvetica, so a 170pt blank). y is the bottom
    of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 17, words)
    _draw_segments(pdf, 56, y + h - 36, [
        ("Name the group: ", "Helvetica", NAVY),
        ("__blank__", 110)], size=13)
    _draw_segments(pdf, 56, y + 9, [
        ("Tell why: They all ", "Helvetica", NAVY),
        ("__blank__", 170),
        (".", "Helvetica", NAVY)], size=13)


def _model_row(pdf, y, h):
    """The worked definition model. y is the bottom of
    the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + 13, "Model:")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(130, y + 13, "A duck is a bird that swims.")


def _define_row(pdf, y, h, segments, bank):
    """A guided definition: a sentence with ruled blanks
    on the first line and the word bank pills below it.
    The child writes the bank words on the blanks. y is
    the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    _draw_segments(pdf, 56, y + h - 22, segments, size=13)
    _word_pills(pdf, 56, y + 8, bank, size=13)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Name the Group and Tell Why",
        "Name the group. Tell what they share.",
        "Read each group of words. Name the group. Tell "
        "what they share.")
    _attribute_bank(pdf, 560)
    for i, words in enumerate(GROUP_SETS):
        _group_set_panel(pdf, 486 - i * 74, 64, words)
    _model_row(pdf, 296, 34)
    _define_row(pdf, 230, 60, [
        ("An ", "Helvetica", NAVY),
        ("__blank__", 54),
        (" is a ", "Helvetica", NAVY),
        ("__blank__", 48),
        (" that ", "Helvetica", NAVY),
        ("__blank__", 130),
        (".", "Helvetica", NAVY)],
        ["apple", "fruit", "grows on trees"])
    _define_row(pdf, 164, 60, [
        ("A dog is an animal that ", "Helvetica", NAVY),
        ("__blank__", 90),
        (".", "Helvetica", NAVY)],
        ["barks", "swims", "flies"])
    _remember_box(pdf, 90, 68, [
        "A word tells what group it is in,",
        "and one thing that makes it special."])
    _adult_line(pdf, "Name the group. Ask: What do they all "
                     "share?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- My Word in My Life (L.1.5(c))
# ---------------------------------------------------------------------------
WORD_BANK = ["cozy", "brave", "helpful", "joyful", "sturdy",
             "fearless"]


def _self_check(pdf, y, h):
    """The self-check panel: three lines, each with an
    empty checkbox the child ticks. Compact: title 15
    below the top edge, first line 31 below it, 14pt
    leading, so the lowest checkbox sits 6pt above the
    panel's bottom edge at h=68. y is the bottom of the
    panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 15,
                          "Check your work")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    ly = y + h - 31
    for line in ("Did I pick a word from this pack?",
                 "Did I draw it in my life?",
                 "Did I write about it?"):
        pdf.setStrokeColor(BOX_STROKE)
        pdf.setLineWidth(1.2)
        pdf.rect(56, ly - 3, 12, 12, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.drawString(76, ly, line)
        ly -= 14


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "My Word in My Life",
        "Use a word in your own life.",
        "Pick one word. Draw it. Write about it.")
    _panel(pdf, 40, 520, 532, 64)
    total_w = sum(stringWidth(w, "Helvetica-Bold", 13) + 22
                  for w in WORD_BANK) + 10 * (len(WORD_BANK) - 1)
    _word_pills(pdf, (PAGE_WIDTH - total_w) / 2, 539,
                WORD_BANK, size=13)
    _panel(pdf, 40, 128, 532, 384)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 128 + 384 - 22, "My word:")
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1)
    pdf.line(150, 128 + 384 - 25, 330, 128 + 384 - 25)
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica-Oblique", 11.5)
    pdf.drawString(
        56, 128 + 62,
        "You can start like this: I chose ___. It reminds "
        "me of ___.")
    pdf.setStrokeColor(HexColor("#B9CBD6"))
    pdf.setLineWidth(0.6)
    pdf.line(56, 128 + 38, 556, 128 + 38)
    pdf.line(56, 128 + 16, 556, 128 + 16)
    _self_check(pdf, 52, 68)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Parent Guide
# ---------------------------------------------------------------------------
def _guide_header(pdf):
    """The brand header for the Parent Guide, without the
    Name and Date fields (this page is for the adult, not
    the child). Uses the pack title so it fits."""
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
                max_w=500, leading=13):
    """Draw a wrapped paragraph. Returns the y below it."""
    for line in _wrap_lines(text, font, size, max_w):
        pdf.setFont(font, size)
        pdf.drawString(x, y, line)
        y -= leading
    return y


GUIDE_TITLE = "How to Use This Pack"
GUIDE_INTRO = ("This pack teaches your child to work out "
               "what words mean, change words with small "
               "parts, put words in order from a little to a "
               "lot, name groups and tell what they share, "
               "and use a word in their own life.")
GUIDE_SECTIONS = [
    ("How to help", [
        "Page 1: Read each sentence together. Point to the "
        "picture. Ask: What makes sense here?",
        "Page 2: Build each word together. Ask: What does "
        "this part mean?",
        "Page 3: Put the words in order together. Act them "
        "out. Ask: Which look is longer?",
        "Page 4: Name each group together. Ask: What group "
        "is it in? What do they all share?",
        "Page 5: Let your child pick a word and draw or "
        "write alone. Ask your child to tell about their "
        "word.",
    ]),
    ("What your child learns", [
        "Your child learns to work out a hard word from the "
        "words around it, change a word with un-, re-, -ful, "
        "and -less, put words in order from a little to a "
        "lot, name groups and tell what the words in each "
        "group share, and use a word from their own life.",
    ]),
    ("Answers", [
        ("Page 1", "brave, not afraid; drowsy, sleepy; "
                   "sturdy, strong."),
        ("Page 2", "unhappy, not happy; redo, do it again; "
                   "helpful, full of help; fearless, without "
                   "fear."),
        ("Page 3", "glance 1, look 2, stare 3; big 1, huge 2, "
                   "gigantic 3; mad 1, angry 2, furious 3."),
        ("Page 4", "Animals: dog, cat, bird. They all have "
                   "legs and can move. Fruits: apple, banana, "
                   "orange. They all have seeds. Clothes: hat, "
                   "coat, shoes. They all are things we wear. "
                   "An apple is a fruit that grows on trees. "
                   "A dog is an animal that barks."),
        ("Page 5", "Any word from the bank, drawn from the "
                   "child's own life, with a sentence. Check "
                   "all three boxes."),
    ]),
    ("Help your child with words", [
        "When your child meets a hard word, ask: What do the "
        "words around it say?",
        "Play with word parts: What does unhappy mean? What "
        "about redo?",
        "Ask: Which word is stronger, big, huge, or "
        "gigantic?",
        "Ask your child to tell you about a word from their "
        "day.",
    ]),
    ("If your child finds it hard", [
        "Page 1: Read the sentence aloud and ask: What "
        "makes sense here?",
        "Page 3: Act out the words, a quick glance, then a "
        "stare, and ask which look is longer. Close feeling "
        "words can overlap. People can disagree about them.",
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
                    max_w=500, leading=13)
    y = 574
    for heading, items in GUIDE_SECTIONS:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(40, y, heading)
        y -= 16
        pdf.setFillColor(NAVY)
        if heading == "Answers":
            for label, text in items:
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(56, y, label + ":")
                lw = stringWidth(label + ": ", "Helvetica-Bold",
                                 12)
                y = _guide_text(pdf, 56 + lw, y, text, size=12,
                                max_w=500 - lw, leading=13)
                y -= 1
        else:
            for para in items:
                y = _guide_text(pdf, 56, y, para, size=12,
                                max_w=500, leading=13)
                y -= 1
        y -= 4
    assert y >= 70, "Parent Guide overflowed: ended at y=%.1f" % y
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 58,
        "Grade 1 Reading: Word Meanings. "
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


def _render_previews(bundle, guide):
    """Regenerate all six preview PNGs at 300 dpi from the
    FINAL bundle and guide with pdftoppm. This is the
    Resource 20 process catch: previews must come from
    the final files, never from an earlier build."""
    for i in range(1, 6):
        subprocess.run(
            ["pdftoppm", "-png", "-r", "300", "-f", str(i),
             "-l", str(i), "-singlefile", bundle,
             os.path.join(OUT_DIR, "preview-%d" % i)],
            check=True)
    subprocess.run(
        ["pdftoppm", "-png", "-r", "300", "-singlefile", guide,
         os.path.join(OUT_DIR, "preview-6")],
        check=True)
    for i in range(1, 7):
        p = os.path.join(OUT_DIR, "preview-%d.png" % i)
        assert os.path.exists(p) and os.path.getsize(p) > 0, \
            "preview-%d.png missing" % i


def main():
    from pypdf import PdfReader, PdfWriter
    os.makedirs(OUT_DIR, exist_ok=True)
    bundle = os.path.join(OUT_DIR, "word-meanings.pdf")
    guide = os.path.join(
        OUT_DIR, "word-meanings-parent-guide.pdf")
    review = os.path.join(
        OUT_DIR, "word-meanings-review.pdf")
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
    page_names = ["hard-word-look-around-it",
                  "word-parts-change-the-meaning",
                  "stronger-and-stronger",
                  "word-groups",
                  "my-word-in-my-life"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR, "word-meanings-p%d-%s.pdf"
            % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    _render_previews(bundle, guide)
    for name in ["word-meanings.pdf",
                 "word-meanings-parent-guide.pdf",
                 "word-meanings-review.pdf",
                 "word-meanings-p1-hard-word-look-around-it.pdf",
                 "word-meanings-p2-word-parts-change-the-meaning.pdf",
                 "word-meanings-p3-stronger-and-stronger.pdf",
                 "word-meanings-p4-word-groups.pdf",
                 "word-meanings-p5-my-word-in-my-life.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text, no
    # standards codes on student pages or the Parent Guide,
    # no first/third person language, and no wording that
    # implies the shades order is always absolute.
    for name in ["word-meanings.pdf",
                 "word-meanings-parent-guide.pdf"]:
        text = " ".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        norm = " ".join(text.split())
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
        assert "L.1" not in norm, \
            "standards code in %s" % name
        assert "first person" not in norm.lower(), \
            "first person in %s" % name
        assert "third person" not in norm.lower(), \
            "third person in %s" % name
    bundle_text = " ".join(
        (p.extract_text() or "")
        for p in PdfReader(bundle).pages)
    bundle_norm = " ".join(bundle_text.split())
    assert "always" not in bundle_norm.lower(), \
        "absolute wording (always) on a student page"
    assert "only right order" not in bundle_norm.lower(), \
        "absolute wording (only right order) on a student page"
    assert "because" not in bundle_norm.lower(), \
        "'because' on a student page (Resource 23 owns it)"
    assert "peek" not in bundle_norm.lower(), \
        "'peek' still on a student page (v2 uses glance)"
    assert "glance" in bundle_norm.lower(), \
        "'glance' missing from the student pages"
    print("text checks: clean")
    # The "For adults" guidance lives on the website
    # resource page, not in the Parent Guide. Confirm the
    # guide carries its own "What your child learns"
    # paraphrase instead of the guidance text, and that
    # the guidance is exactly 57 words.
    guide_text = " ".join(
        (p.extract_text() or "")
        for p in PdfReader(guide).pages)
    guide_norm = " ".join(guide_text.split())
    assert "Words can have shades of meaning" \
        not in guide_norm, "For adults text leaked into guide"
    assert "peek" not in guide_norm.lower(), \
        "'peek' still in the Parent Guide (v2 uses glance)"
    assert "because" not in guide_norm.lower(), \
        "'because' in the Parent Guide (Resource 23 owns it)"
    assert len(ADULT_GUIDANCE.split()) == 57, \
        "For adults guidance is %d words, not 57" % len(
            ADULT_GUIDANCE.split())
    print("guide check: clean; For adults guidance is 57 words")


if __name__ == "__main__":
    main()
