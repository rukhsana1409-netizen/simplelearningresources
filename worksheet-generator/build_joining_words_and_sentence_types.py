#!/usr/bin/env python3
"""Grade 1 Reading - Joining Words and Sentence Types.

Resource 23 in the approved and locked Grade 1 Reading and
Language Arts roadmap (audit 2026-11-05), after the one-time
comprehensive curriculum and overlap audit
(~/workspace/research_notes/grade-1-ela-audit-20261120/
report.md). Plan approved 2026-11-20 with the user's
refinements. 5 student pages plus a separate 1-page Parent
Guide.

Placement: Grade 1 / Reading and Language / Grammar and
Sentences. Standards L.1.1(g), L.1.1(h), L.1.1(j) taught;
L.1.6 is a thread (because/so use, new words in P5), not a
separate page. Standards appear on the resource page only,
never on student pages or the Parent Guide.

Boundaries, verified against the built packs 2026-11-20:
R16 owns whole ideas, capitals, end-mark fixing, commas in
dates and lists, word-order unscrambling, and writing two
own simple sentences, so none of those is re-taught here;
the P4 end-mark activity is identification, not fixing.
R14 Page 4 and R20 Page 4 because-blanks are
comprehension fill-ins; R23 Page 2 teaches because/so as
joiners. K Building Simple Sentences Page 2 expands by
adding detail; R23 expands by joining. R22 owns pronouns
as grammar; no pronoun teaching here. R21 owns vocabulary;
no vocabulary teaching here. "because" appears only on
Page 2 and in the guide's Answers Page 2 line. "so"
appears only as a joining word, never as an intensifier.
"Look at the rainbow" appears nowhere; Page 4 uses "What
a beautiful rainbow!" instead. Page 2 items 3 and 4 are
the same dark-room situation both ways; that is the
teaching, not a trick.

Her refinements (binding): Page 3 adds "___ umbrella"
(an) as a fourth a/an item, because it fit after the rest
of the page was laid out. Page 3 Activity 3 makes near
and far, one and many, visually unmistakable: the near
apples are large in the child's hands, the far apples
small on a distant shelf. The two Page 3 near/far
pictures were regenerated 2026-11-20 with larger, more
visible shelf apples and no name tags, after the user
found the shelf apples too small to see. Option A
redesign 2026-11-20: Page 3 Activity 2 grew to three
rows with the hint "a introduces the dog. the means the
same dog again.", teaching first mention (a) and second
mention (the); the teach box, Activity 1, gaps,
near/far panel, and Remember box were compacted to pay
for it, and the near/far pictures stayed at their size.
Page 4
Activity 2 uses "What a beautiful rainbow!"
(unambiguously an exclamation). Page
5 self-check uses exactly the three revised boxes, one
per activity, without implying every sentence needs a
conjunction and a determiner. Illustrations reuse first.

"For adults" website guidance (59 words, for the
resource page catalog adultGuidance; NOT printed in the
Parent Guide, per the R18/R19/R20/R21 precedent -- the
guide carries its own "What your child learns"
paraphrase):
"Joining words help your child say more in one sentence.
Help your child hear what and, but, or, so, and because
mean. Talk about a, the, this, and that in books you read
together. Ask what a sentence does: does it tell, ask, or
tell someone to do something? Then let your child build a
sentence of their own."

Illustrations: seven reused JPEGs from Resources 16 and
21 (p2-rain-dog, p2-sun, p3-ball, p3-dog, p4-cake,
p4-cat, p4-kids-playing) and thirteen new original
watercolor storybook JPEGs in the approved style
(p1-run-jump, p1-ice-cream-cold, p1-two-cups,
p2-thirsty-drink, p2-sun-drink, p2-dark-room, p3-apple,
p3-egg, p3-umbrella, p3-near-far-one, p3-near-far-many,
p4-shoes, p5-kite). Two first-round images were rejected
and regenerated: the first p1-run-jump carried a baked-in
title and caption, and the first p2-dark-room carried a
baked-in caption bar; the first p3-apple, p3-egg,
p3-umbrella, and p1-two-cups carried baked-in word
labels, and were regenerated with no text. The kept
images carry no readable text except a doormat that says
WELCOME in p4-shoes and tiny name labels on a few
children's clothes, which are part of the scene. JPEGs
embed as DCT, so the PDF stays small. The Think and
Choose 3D-render assets (tc-icecream, tc-kite, tc-shoe,
tc-dark) were inspected and rejected: wrong style, and
the wrong subjects (a lone cone, a lone kite, a lone
shoe, a sleepy boy). R16 p2-child-jumping was inspected
and rejected for Page 1 item 1: it shows jumping only,
not running and jumping.

Shared design code (logo, header, footer) is imported
verbatim from build_phonics_az.py. Do not fork it here.
Header title is drawn at 18pt; the subtitle is drawn at
12pt (not 14pt) because the full subtitle, "Grade 1
Reading | Joining Words and Sentence Types", is 359.5pt
at 14pt and would run past the teal rule; at 12pt it is
308.2pt and ends inside the rule.

Word-count note: the approved sentences run 6 to 10
words (the but model, "I like rain, but I do not like
thunder.", is 9 words; "I like to swim, but I do not
like cold water." is 10). Each joined idea is 3 to 6
words. The approved wording is kept verbatim; the
counts are reported, not silently rewritten.

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

TITLE = "Joining Words and Sentence Types"
SUBTITLE = "Grade 1 Reading | Joining Words and Sentence Types"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files",
                       "joining-words-and-sentence-types")
IMG_DIR = OUT_DIR  # watercolor illustration JPEGs live beside the PDFs

ADULT_GUIDANCE = ("Joining words help your child say more "
                  "in one sentence. Help your child hear "
                  "what and, but, or, so, and because mean. "
                  "Talk about a, the, this, and that in "
                  "books you read together. Ask what a "
                  "sentence does: does it tell, ask, or tell "
                  "someone to do something? Then let your "
                  "child build a sentence of their own.")


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


def _adult_line(pdf, text, y=74):
    """Centred adult line at y (74 by default). Splits into
    two lines if the text would run past the page edges."""
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica-Bold", 10.5)
    if stringWidth(text, "Helvetica-Bold", 10.5) <= 560:
        pdf.drawCentredString(PAGE_WIDTH / 2, y, text)
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
    pdf.drawCentredString(PAGE_WIDTH / 2, y + 6,
                          " ".join(words[:i]))
    pdf.drawCentredString(PAGE_WIDTH / 2, y - 10,
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
                subtitle_size=12)


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


def _segments_width(segments, size=13):
    """Total width of a segment list (blanks count by width)."""
    total = 0
    for seg in segments:
        if seg[0] == "__blank__":
            total += seg[1]
        else:
            total += stringWidth(seg[0], seg[1], size)
    return total


def _draw_centred_segments(pdf, y, segments, size=13):
    """Draw a segment list centred on the page at baseline y."""
    total = _segments_width(segments, size)
    _draw_segments(pdf, (PAGE_WIDTH - total) / 2, y, segments,
                   size=size)


def _writing_line(pdf, x1, x2, y):
    """A light ruled writing line for the child to write on."""
    pdf.setStrokeColor(HexColor("#B9CBD6"))
    pdf.setLineWidth(0.6)
    pdf.line(x1, y, x2, y)


def _choice_row(pdf, y, h, image, segments, choices):
    """One choose-the-joiner row: the picture on the left
    (when given), the sentence with a ruled blank, and the
    choice pills below the sentence. The child circles the
    pill that fits. y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    if image:
        _draw_image(pdf, os.path.join(IMG_DIR, image),
                    100, y + h / 2, 104, 64)
        tx = 170
    else:
        tx = 56
    _draw_segments(pdf, tx, y + h - 24, segments, size=13)
    _word_pills(pdf, tx, y + 8, choices, size=13)


def _self_check(pdf, y, h, lines):
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
    for line in lines:
        pdf.setStrokeColor(BOX_STROKE)
        pdf.setLineWidth(1.2)
        pdf.rect(56, ly - 3, 12, 12, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.drawString(76, ly, line)
        ly -= 14


# ---------------------------------------------------------------------------
# Page 1 -- Joining with And, But, Or (L.1.1(g))
# ---------------------------------------------------------------------------
def _teach_box_p1(pdf, y, h):
    """The joining-word teach box: title plus the three
    models, each with its plain meaning. y is the bottom
    of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 16,
                          "A joining word joins two ideas.")
    models = [
        ([("and", "Helvetica-Bold", TEAL),
          ("  I like cats and I like dogs.", "Helvetica", NAVY),
          ("  Both things are true.", "Helvetica-Oblique",
           ADULT_GREY)], 12.5),
        ([("but", "Helvetica-Bold", TEAL),
          ("  I like rain, but I do not like thunder.",
           "Helvetica", NAVY),
          ("  The second idea is different.",
           "Helvetica-Oblique", ADULT_GREY)], 12.5),
        ([("or", "Helvetica-Bold", TEAL),
          ("  Do you want an apple or a banana?",
           "Helvetica", NAVY),
          ("  Pick one.", "Helvetica-Oblique", ADULT_GREY)],
         12.5),
    ]
    ly = y + h - 34
    for segments, size in models:
        _draw_centred_segments(pdf, ly, segments, size=size)
        ly -= 18


P1_ROWS = [
    # (image, sentence segments, choices)
    ("p1-run-jump.jpg",
     [("I like to run ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" I like to jump.", "Helvetica", NAVY)],
     ["and", "but"]),
    ("p1-ice-cream-cold.jpg",
     [("I like ice cream, ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" I do not like the cold.", "Helvetica", NAVY)],
     ["and", "but"]),
    ("p1-two-cups.jpg",
     [("Do you want milk ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" juice?", "Helvetica", NAVY)],
     ["and", "or"]),
    (None,
     [("The sun is out ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" it is warm.", "Helvetica", NAVY)],
     ["and", "but"]),
]


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Joining with And, But, Or",
        "Join two ideas with one word.",
        "Read each sentence. Circle the word that joins it.")
    _teach_box_p1(pdf, 508, 84)
    for i, (image, segments, choices) in enumerate(P1_ROWS):
        _choice_row(pdf, 420 - i * 82, 76, image, segments,
                    choices)
    _remember_box(pdf, 104, 48, [
        "and joins two things together. but shows a "
        "difference. or lets you pick one."])
    _adult_line(pdf, "Say each sentence aloud. Ask: Does it "
                     "join, show a difference, or let you pick?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- So and Because (L.1.1(g); L.1.6 thread)
# ---------------------------------------------------------------------------
def _teach_box_p2(pdf, y, h):
    """The because/so teach box: the rain and wet-dog
    picture on the left, the same pair both ways on the
    right. y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, os.path.join(IMG_DIR, "p2-rain-dog.jpg"),
                118, y + h / 2, 150, 84)
    _draw_segments(pdf, 206, y + h - 26, [
        ("The dog is wet ", "Helvetica", NAVY),
        ("because", "Helvetica-Bold", TEAL),
        (" it rained.", "Helvetica", NAVY)], size=13)
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica-Oblique", 11.5)
    pdf.drawString(206, y + h - 44, "because tells why.")
    _draw_segments(pdf, 206, y + h - 66, [
        ("It rained, ", "Helvetica", NAVY),
        ("so", "Helvetica-Bold", TEAL),
        (" the dog is wet.", "Helvetica", NAVY)], size=13)
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica-Oblique", 11.5)
    pdf.drawString(206, y + h - 84, "so tells what happens next.")


P2_ROWS = [
    # (image, sentence segments, choices)
    ("p2-sun-drink.jpg",
     [("The sun is hot, ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" we drink water.", "Helvetica", NAVY)],
     ["because", "so"]),
    ("p2-thirsty-drink.jpg",
     [("We drink water ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" we are thirsty.", "Helvetica", NAVY)],
     ["so", "because"]),
    ("p2-dark-room.jpg",
     [("It is dark, ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" we turn on the light.", "Helvetica", NAVY)],
     ["so", "because"]),
    ("p2-dark-room.jpg",
     [("We turn on the light ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" it is dark.", "Helvetica", NAVY)],
     ["because", "so"]),
]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "So and Because",
        "Because tells why. So tells what happens next.",
        "Read each sentence. Circle because or so.")
    _teach_box_p2(pdf, 500, 92)
    for i, (image, segments, choices) in enumerate(P2_ROWS):
        _choice_row(pdf, 420 - i * 82, 76, image, segments,
                    choices)
    _remember_box(pdf, 104, 48, [
        "because tells why. so tells what happens next."])
    _adult_line(pdf, "Talk about the picture first. Ask: "
                     "What happened first? What happened next?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Little Words Before Nouns (L.1.1(h))
# ---------------------------------------------------------------------------
def _teach_box_p3(pdf, y, h):
    """The little-word models, three centred lines. The
    page subtitle already says the rule, so this box
    shows only the models with their plain meanings.
    Compact spacing (Option A, 2026-11-20): 17pt leading
    and 16pt from the top edge to the first baseline, so
    the box pays for the bigger Activity 2 below. The
    wording is unchanged. y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    lines = [
        ([("a cat", "Helvetica-Bold", TEAL),
          ("  (one cat, any cat)", "Helvetica", NAVY),
          ("     ", "Helvetica", NAVY),
          ("an apple", "Helvetica-Bold", TEAL),
          ("  (an comes before a, e, i, o, u sounds)",
           "Helvetica", NAVY)], 12.5),
        ([("the sun", "Helvetica-Bold", TEAL),
          ("  (the one we know)", "Helvetica", NAVY),
          ("     ", "Helvetica", NAVY),
          ("this apple", "Helvetica-Bold", TEAL),
          ("  (in my hand)", "Helvetica", NAVY),
          ("     ", "Helvetica", NAVY),
          ("that apple", "Helvetica-Bold", TEAL),
          ("  (on the shelf)", "Helvetica", NAVY)], 12.5),
        ([("these apples", "Helvetica-Bold", TEAL),
          ("  (in my hands)", "Helvetica", NAVY),
          ("     ", "Helvetica", NAVY),
          ("those apples", "Helvetica-Bold", TEAL),
          ("  (on the shelf)", "Helvetica", NAVY)], 12.5),
    ]
    ly = y + h - 16
    for segments, size in lines:
        _draw_centred_segments(pdf, ly, segments, size=size)
        ly -= 17


A_OR_AN = [
    ("p3-apple.jpg", "apple"),
    ("p3-ball.jpg", "ball"),
    ("p3-egg.jpg", "egg"),
    ("p3-umbrella.jpg", "umbrella"),
]


def _a_or_an_panel(pdf, y, h):
    """Activity 1: four small pictures in a row, each with
    a blank and the a/an pills below it. The umbrella is
    the fourth item; it fit, so it is in. Compact
    spacing (Option A, 2026-11-20): the title, pictures,
    word line, and pills sit 2pt tighter, so the panel
    pays for the bigger Activity 2 below. The wording,
    pictures, and pill sizes are unchanged. y is the
    bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 12, "1. a or an")
    for i, (image, word) in enumerate(A_OR_AN):
        cx = 106.5 + i * 133
        _draw_image(pdf, os.path.join(IMG_DIR, image),
                    cx, y + h - 36, 60, 44)
        _draw_segments(
            pdf, cx - _segments_width(
                [("__blank__", 30),
                 (" " + word, "Helvetica", NAVY)], size=13) / 2,
            y + h - 70,
            [("__blank__", 30),
             (" " + word, "Helvetica", NAVY)], size=13)
        total = sum(stringWidth(w, "Helvetica-Bold", 13) + 22
                    for w in ("a", "an")) + 10
        _word_pills(pdf, cx - total / 2, y + 2, ("a", "an"),
                    size=13)


def _a_or_the_panel(pdf, y, h):
    """Activity 2: three text rows, each with a blank and
    the a/the pills on the same line, plus a hint line
    under the title. The sun row is unchanged; the dog
    rows teach first mention (a) and second mention
    (the): "I see a dog in the park." then "The dog is
    big." Option A redesign 2026-11-20: the panel grew
    to hold the third row and the hint, and the teach
    box, Activity 1, gaps, near/far panel, and Remember
    box were compacted to pay for it. No pictures here:
    the page budget goes to the big near/far pictures in
    Activity 3, and the sun and dog pictures already
    appear on Pages 2 and 5. y is the bottom of the
    panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 14, "2. a or the")
    hint = ("a introduces the dog. "
            "the means the same dog again.")
    _fit(hint, "Helvetica", 12.5, 500, "Activity 2 hint")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawString(56, y + h - 30, hint)
    rows = [
        ([("I see ", "Helvetica", NAVY),
          ("__blank__", 36),
          (" sun in the sky.", "Helvetica", NAVY)],
         ["a", "the"]),
        ([("I see ", "Helvetica", NAVY),
          ("__blank__", 36),
          (" dog in the park.", "Helvetica", NAVY)],
         ["a", "the"]),
        ([("__blank__", 36),
          (" dog is big.", "Helvetica", NAVY)],
         ["a", "the"]),
    ]
    for i, (segments, choices) in enumerate(rows):
        cy = y + h - 50 - i * 28
        x = _draw_segments(pdf, 56, cy, segments, size=13)
        _word_pills(pdf, x + 10, cy - 9, choices, size=13)


def _near_far_panel(pdf, y, h):
    """Activity 3: the two near/far pictures side by side,
    each with two blanks below it. The near apples are
    large in the child's hands; the far apples are small
    on a distant shelf. y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 16,
                   "3. this, that, these, those")
    _draw_image(pdf, os.path.join(IMG_DIR,
                                  "p3-near-far-one.jpg"),
                160, y + h - 76, 200, 112)
    _draw_image(pdf, os.path.join(IMG_DIR,
                                  "p3-near-far-many.jpg"),
                420, y + h - 76, 200, 112)
    _draw_segments(pdf, 60, y + h - 146, [
        ("__blank__", 40),
        (" apple is in my hand.", "Helvetica", NAVY)],
        size=12.5)
    _draw_segments(pdf, 60, y + h - 163, [
        ("__blank__", 40),
        (" apple is on the shelf.", "Helvetica", NAVY)],
        size=12.5)
    _draw_segments(pdf, 320, y + h - 146, [
        ("__blank__", 40),
        (" apples are in my hands.", "Helvetica", NAVY)],
        size=12.5)
    _draw_segments(pdf, 320, y + h - 163, [
        ("__blank__", 40),
        (" apples are on the shelf.", "Helvetica", NAVY)],
        size=12.5)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Little Words Before Nouns",
        "A little word comes before a naming word.",
        "Circle the little word that fits.")
    _teach_box_p3(pdf, 540, 56)
    _a_or_an_panel(pdf, 434, 104)
    _a_or_the_panel(pdf, 314, 118)
    _near_far_panel(pdf, 142, 170)
    _remember_box(pdf, 78, 62, [
        "a and an mean one. the means the one we know.",
        "this and these are near. that and those are far."])
    # Option A redesign 2026-11-20: Activity 2 grew from
    # 76pt to 118pt (third row plus hint line). The stack
    # pays for it without touching the near/far pictures
    # (still 200x112): teach box 72 to 56, Activity 1 112
    # to 104, near/far panel 172 to 170 and Remember box
    # 64 to 62 (2pt of bottom padding each), all four
    # inter-panel gaps 4pt to 2pt, teach box top up 4pt
    # to 596, Remember box bottom down 2pt to 78. Font
    # sizes, pill sizes, and row pitch are unchanged.
    # The Remember box sits at y=78 here, so the adult
    # line drops to 68 (the other pages use 74) so its
    # ascenders clear the box border.
    _adult_line(pdf, "Point to the picture. Ask: Is it near "
                     "or far? Is it one or more than one?", 68)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Four Kinds of Sentences (L.1.1(j))
# ---------------------------------------------------------------------------
def _teach_box_p4(pdf, y, h):
    """The four kinds, with the soft cat picture on the
    left and the four models on the right. y is the bottom
    of the panel."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, os.path.join(IMG_DIR, "p4-cat.jpg"),
                110, y + h / 2, 120, 100)
    models = [
        ("Statement", "The cat is soft.", "tells something."),
        ("Question", "Is the cat soft?", "asks something."),
        ("Command", "Pet the cat.",
         "tells someone to do something."),
        ("Exclamation", "What a soft cat!",
         "shows a big feeling."),
    ]
    ly = y + h - 26
    for kind, sentence, meaning in models:
        _draw_segments(pdf, 186, ly, [
            (kind, "Helvetica-Bold", TEAL),
            ("  " + sentence + "  ", "Helvetica", NAVY),
            ("(" + meaning + ")", "Helvetica-Oblique",
             ADULT_GREY)], size=13)
        ly -= 22


KIND_CELLS = [
    # (image, sentence, pill rows; the answer sits in a
    # different spot in each cell)
    ("p2-sun.jpg", "The sun is out.",
     [["statement", "question"], ["command", "exclamation"]]),
    ("p4-kids-playing.jpg", "Can we play?",
     [["exclamation", "command"], ["statement", "question"]]),
    ("p4-shoes.jpg", "Put on your shoes.",
     [["question", "command"], ["exclamation", "statement"]]),
    ("p4-cake.jpg", "What a big cake!",
     [["command", "statement"], ["exclamation", "question"]]),
]


def _kind_cell(pdf, x0, y0, w, h, image, sentence, pill_rows):
    """One What-does-it-do cell: the picture on the left,
    the sentence at the top right, and the four kind
    pills in two rows below it. (x0, y0) is the bottom-left
    corner of the cell."""
    _draw_image(pdf, os.path.join(IMG_DIR, image),
                x0 + 38, y0 + h - 38, 58, 58)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(x0 + 78, y0 + h - 16, sentence)
    for r, row in enumerate(pill_rows):
        end = _word_pills(pdf, x0 + 78, y0 + h - 46 - r * 28,
                          row, size=12)
        # _word_pills returns the x after a trailing 10pt
        # gap, so the last pill really ends 10pt earlier.
        assert end - 10 <= x0 + w - 6, \
            "kind pills overflow the cell: %r" % (row,)


def _kind_panel(pdf, y, h):
    """Activity 1: four cells in two columns and two
    rows. y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 16,
                   "1. What does it do? Circle the kind.")
    for i, (image, sentence, pill_rows) in enumerate(KIND_CELLS):
        col = i % 2
        row = i // 2
        _kind_cell(pdf, 40 + col * 266,
                   y + h - 18 - (row + 1) * 76, 266, 76,
                   image, sentence, pill_rows)


def _mark_panel(pdf, y, h):
    """Activity 2: four sentences, each with a ruled blank
    for the end mark. y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 16,
                   "2. Put the right mark. Write . or ? or !")
    rows = [
        "The dog is big ",
        "Where is my ball ",
        "Put the book away ",
        "What a beautiful rainbow ",
    ]
    for i, text in enumerate(rows):
        _draw_segments(pdf, 56, y + h - 46 - i * 22, [
            (text, "Helvetica", NAVY),
            ("__blank__", 28)], size=13)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Four Kinds of Sentences",
        "Every sentence does a job.",
        "Read each sentence. What does it do?")
    _teach_box_p4(pdf, 472, 120)
    _kind_panel(pdf, 292, 174)
    _mark_panel(pdf, 166, 120)
    _remember_box(pdf, 92, 68, [
        "A statement tells. A question asks.",
        "A command tells someone to do. An exclamation "
        "shows a big feeling."])
    _adult_line(pdf, "Cover the mark. Ask: What does this "
                     "sentence do?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Build and Write Sentences (L.1.1(g), (h), (j);
# L.1.6 thread)
# ---------------------------------------------------------------------------
def _join_item(pdf, y, h, line1, line2, choices):
    """Activity 1 item: the two short ideas and the joiner
    pills on one line, then "Write the joined sentence:"
    and two generous ruled writing lines. y is the bottom
    of the panel."""
    _panel(pdf, 40, y, 532, h)
    x = _draw_segments(pdf, 56, y + h - 22, [
        (line1 + " ", "Helvetica", NAVY),
        (line2, "Helvetica", NAVY)], size=13)
    _word_pills(pdf, x + 12, y + h - 31, choices, size=13)
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica-Oblique", 11.5)
    pdf.drawString(56, y + h - 48, "Write the joined sentence:")
    _writing_line(pdf, 56, 556, y + h - 66)
    _writing_line(pdf, 56, 556, y + h - 88)


def _little_word_panel_p5(pdf, y, h):
    """Activity 2: two picture-supported rows, each with a
    blank and the choice pills on the same line. The
    section label is drawn by the page function, not here.
    y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    rows = [
        ("p2-sun.jpg",
         [("I see ", "Helvetica", NAVY),
          ("__blank__", 36),
          (" sun in the sky.", "Helvetica", NAVY)],
         ["a", "the"]),
        ("p3-apple.jpg",
         [("I want ", "Helvetica", NAVY),
          ("__blank__", 36),
          (" apple for lunch.", "Helvetica", NAVY)],
         ["an", "a"]),
    ]
    for i, (image, segments, choices) in enumerate(rows):
        cy = y + h - 22 - i * 36
        _draw_image(pdf, os.path.join(IMG_DIR, image),
                    82, cy, 36, 28)
        x = _draw_segments(pdf, 120, cy, segments, size=13)
        _word_pills(pdf, x + 10, cy - 9, choices, size=13)


def _write_own_panel(pdf, y, h):
    """Activity 3: the kite picture on the left, the
    question prompt and two writing lines on the right,
    then the optional statement line. y is the bottom of
    the panel."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, os.path.join(IMG_DIR, "p5-kite.jpg"),
                112, y + h / 2, 110, 100)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(182, y + h - 24,
                   "Write a question about this picture.")
    _writing_line(pdf, 182, 556, y + h - 50)
    _writing_line(pdf, 182, 556, y + h - 76)
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica-Oblique", 11.5)
    pdf.drawString(182, y + h - 100,
                   "Now write a statement about it.")
    _writing_line(pdf, 182, 556, y + h - 118)


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Build and Write Sentences",
        "Join ideas. Choose the little word. Write your own.",
        "Build each sentence. Then write your own.")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 578, "1. Join the ideas.")
    _join_item(pdf, 472, 96, "It is cold.", "We wear coats.",
               ["and", "so"])
    _join_item(pdf, 370, 96, "I like to swim.",
               "I do not like cold water.", ["but", "so"])
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 358, "2. Choose the little word.")
    _little_word_panel_p5(pdf, 280, 74)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 272, "3. Write your own.")
    _write_own_panel(pdf, 134, 132)
    _self_check(pdf, 56, 72, [
        "Did I join two ideas with a joining word?",
        "Did I choose the right little word?",
        "Did I write a question about the picture?"])
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
    pdf.setFont("Helvetica-Bold", 18)
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
GUIDE_INTRO = ("This pack teaches your child to join two "
               "ideas with joining words, choose a, an, "
               "the, this, that, these, and those, tell "
               "what four kinds of sentences do, and build "
               "sentences of their own.")
GUIDE_SECTIONS = [
    ("How to help", [
        "Page 1: Talk about what and, but, and or mean "
        "before your child picks one.",
        "Page 2: Talk about what happened first and what "
        "happened next in the picture.",
        "Page 3: Point to the pictures. Ask: Is it near or "
        "far? Is it one or more than one? For a and the, "
        "say: a introduces the dog. the means the same "
        "dog again.",
        "Page 4: Ask: What does this sentence do? Does it "
        "tell, ask, or tell someone to do something?",
        "Page 5: Let your child build the sentence alone. "
        "Read it back together.",
    ]),
    ("What your child learns", [
        "Your child learns to join two ideas, choose a, an, "
        "the, this, that, these, and those, tell what four "
        "kinds of sentences do, and build and write "
        "sentences of their own.",
    ]),
    ("Answers", [
        ("Page 1", "and; but; or; and."),
        ("Page 2", "so; because; so; because."),
        ("Page 3", "an apple; a ball; an egg; an umbrella. "
                   "the sun; a dog; the dog. this apple; that "
                   "apple; these apples; those apples."),
        ("Page 4", "The sun is out, statement; Can we play?, "
                   "question; Put on your shoes., command; "
                   "What a big cake!, exclamation. The dog "
                   "is big. Where is my ball? Put the book "
                   "away. What a beautiful rainbow!"),
        ("Page 5", "It is cold, so we wear coats. I like to "
                   "swim, but I do not like cold water. the "
                   "sun; an apple. Any question and any "
                   "statement about the kite picture."),
    ]),
    ("Help your child with words", [
        "Say the joined sentence aloud first, then write it.",
        "For but, ask: \"What is different?\",",
        "For a and an, say the word aloud and listen for the "
        "first sound.",
        "For this and that, use your hands: near is in my "
        "hands, far is over there.",
    ]),
    ("If your child finds it hard", [
        "Page 2: Act out the two parts, first the rain, "
        "then the wet dog, and ask 'Why is the dog wet?' "
        "then 'What happened next?'",
        "Page 4: Cover the end mark and ask what the "
        "sentence does first.",
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
        "Grade 1 Reading: Joining Words and Sentence Types. "
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
    bundle = os.path.join(
        OUT_DIR, "joining-words-and-sentence-types.pdf")
    guide = os.path.join(
        OUT_DIR,
        "joining-words-and-sentence-types-parent-guide.pdf")
    review = os.path.join(
        OUT_DIR, "joining-words-and-sentence-types-review.pdf")
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
    page_names = ["joining-with-and-but-or",
                  "so-and-because",
                  "little-words-before-nouns",
                  "four-kinds-of-sentences",
                  "build-and-write-sentences"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR,
            "joining-words-and-sentence-types-p%d-%s.pdf"
            % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    _render_previews(bundle, guide)
    for name in ["joining-words-and-sentence-types.pdf",
                 "joining-words-and-sentence-types-parent-guide.pdf",
                 "joining-words-and-sentence-types-review.pdf",
                 "joining-words-and-sentence-types-p1-"
                 "joining-with-and-but-or.pdf",
                 "joining-words-and-sentence-types-p2-"
                 "so-and-because.pdf",
                 "joining-words-and-sentence-types-p3-"
                 "little-words-before-nouns.pdf",
                 "joining-words-and-sentence-types-p4-"
                 "four-kinds-of-sentences.pdf",
                 "joining-words-and-sentence-types-p5-"
                 "build-and-write-sentences.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text, no
    # standards codes on student pages or the Parent Guide,
    # no first/third person language.
    for name in ["joining-words-and-sentence-types.pdf",
                 "joining-words-and-sentence-types-parent-guide.pdf"]:
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
    bundle_pages_text = [
        " ".join((PdfReader(bundle).pages[i].extract_text()
                  or "").split())
        for i in range(5)]
    bundle_norm = " ".join(bundle_pages_text)
    # Resource 21 wording must not have leaked into this pack.
    assert "have legs and can move" not in bundle_norm, \
        "R21 wording leaked into the student pages"
    # The ambiguous rainbow sentence must be gone; the
    # unmistakable exclamation must be there.
    assert "Look at the rainbow" not in bundle_norm, \
        "'Look at the rainbow' on a student page"
    assert "What a beautiful rainbow" in bundle_norm, \
        "'What a beautiful rainbow' missing from Page 4"
    # "because" is taught on Page 2 only.
    for i in (0, 2, 3, 4):
        assert "because" not in bundle_pages_text[i].lower(), \
            "'because' on Page %d" % (i + 1)
    assert "because" in bundle_pages_text[1].lower(), \
        "'because' missing from Page 2"
    # "so" is a joining word only, never an intensifier.
    for bad in ("so big", "so much", "so many", "so soft",
                "so hot", "so cold"):
        assert bad not in bundle_norm.lower(), \
            "intensifier %r on a student page" % bad
    # Words where the a/an sound and letter disagree are
    # never used as a/an items.
    for bad in ("unicorn", "honest", "hour"):
        assert bad not in bundle_norm.lower(), \
            "%r on a student page" % bad
    # Page 5 self-check uses exactly the three revised
    # boxes, not the earlier wording.
    p5 = bundle_pages_text[4]
    for box in ("Did I join two ideas with a joining word?",
                "Did I choose the right little word?",
                "Did I write a question about the picture?"):
        assert box in p5, "self-check box missing: %r" % box
    assert "Did I use a little word?" not in p5, \
        "old self-check wording on Page 5"
    assert "Did I write a full sentence?" not in p5, \
        "old self-check wording on Page 5"
    # The umbrella fit, so it must be on Page 3.
    assert "umbrella" in bundle_pages_text[2].lower(), \
        "'umbrella' missing from Page 3"
    # Page 3 Activity 2 teaches first mention (a) and
    # second mention (the) with the dog pair, Option A.
    p3 = bundle_pages_text[2]
    assert "a introduces the dog. the means the same dog " \
        "again." in p3, "Activity 2 hint missing from Page 3"
    assert "dog is big." in p3, \
        "'The dog is big.' missing from Page 3"
    # The four kind names with their plain meanings on P4.
    p4 = bundle_pages_text[3]
    for kind, meaning in (
            ("Statement", "tells something"),
            ("Question", "asks something"),
            ("Command", "tells someone to do something"),
            ("Exclamation", "shows a big feeling")):
        assert kind in p4, "kind name missing: %s" % kind
        assert meaning in p4, "kind meaning missing: %s" % meaning
    # In the Parent Guide, "because" appears only in the
    # Answers Page 2 line ("so; because; so; because.").
    guide_text = " ".join(
        (p.extract_text() or "")
        for p in PdfReader(guide).pages)
    guide_norm = " ".join(guide_text.split())
    assert guide_norm.lower().count("because") == 2, \
        "'because' appears %d times in the guide, not 2" % (
            guide_norm.lower().count("because"))
    # The guide's Page 3 lines must match the revised
    # Page 3: the dog pair in the answers, and the hint
    # echoed in the How to help line.
    assert "a dog; the dog." in guide_norm, \
        "dog pair missing from the guide's Page 3 answers"
    assert "a introduces the dog. the means the same dog " \
        "again." in guide_norm, \
        "hint missing from the guide's Page 3 help line"
    assert "Look at the rainbow" not in guide_norm, \
        "'Look at the rainbow' in the Parent Guide"
    assert "have legs and can move" not in guide_norm, \
        "R21 wording leaked into the Parent Guide"
    # The "For adults" guidance lives on the website
    # resource page, not in the Parent Guide. Confirm the
    # guide carries its own "What your child learns"
    # paraphrase instead of the guidance text, and that
    # the guidance is exactly 59 words.
    assert "Joining words help your child say more" \
        not in guide_norm, "For adults text leaked into guide"
    assert len(ADULT_GUIDANCE.split()) == 59, \
        "For adults guidance is %d words, not 59" % len(
            ADULT_GUIDANCE.split())
    print("text checks: clean; For adults guidance is 59 words")


if __name__ == "__main__":
    main()
