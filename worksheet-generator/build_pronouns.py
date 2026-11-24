#!/usr/bin/env python3
"""Grade 1 Reading - Pronouns.

Resource 22 in the approved and locked Grade 1 Reading and
Language Arts roadmap (audit 2026-11-05), after the one-time
comprehensive curriculum and overlap audit
(~/workspace/research_notes/grade-1-ela-audit-20261120/
report.md). Plan approved 2026-11-23 with the user's
refinements. Revised 2026-11-23 per her review
corrections: Page 1 captions respaced with vector
we/they bubble labels; Page 2 cat replaced by a toy car;
Page 3 "get the action" replaced by "come after the
action word, or after to"; Page 5 indefinite items
rewritten so each has exactly one defensible answer.
Page 1 matching redesigned again 2026-11-23 at her
request: two side-by-side blocks (four and three rows)
after measuring that seven single-column rows would
force pictures about 26pt tall. Redesigned again
2026-11-24 at her request: she rejected the two-block
split, so Page 1 is now one single-column matching
list (seven pills on the left, seven picture cards on
the right, captions beside the pictures) with a wide
blank centre for drawing lines. Page 4 unchanged. 5 student pages plus a separate
1-page Parent Guide.

Placement: Grade 1 / Reading and Language / Grammar and
Sentences. Standard L.1.1(d) taught; no other standard
claimed. Standards appear on the resource page only, never
on student pages or the Parent Guide.

Boundaries, verified against the audit 2026-11-20 and the
built packs: no positional words or prepositions anywhere
(a Grade 1 Positional Words resource already exists, so
L.1.1(i) is dropped entirely). No pronoun-as-narrator-clue
teaching (Resource 19 owns that use; this pack teaches
pronouns as grammar). No re-teaching possessive nouns
(Resource 17 owns Mia's and the dog's; Page 4 uses them
only as the contrast that makes hers, his, and theirs
new). No joining words, no a/an/the/this/that, no
sentence types (Resource 23 owns those; possessive
determiners my, your, his, her, our, their are different
words from Resource 23's determiners and belong to
L.1.1(d)). No vocabulary teaching (Resource 21 owns it).
No my/I sight-word work (K Common Words owns that).
"because" appears nowhere in this pack. "her" is never
tested as a possessive on Page 4 because Page 3 teaches
"her" as an object pronoun; the Parent Guide explains
the two jobs to the adult. "his" is identical in both
possessive jobs; the Page 4 teach box says so once.

Her refinements (binding, 2026-11-23): Page 1 makes the
we/they distinction visually unmistakable: for we, the
speaking child is visibly inside the group with a speech
bubble; for they, the speaking child is visibly outside
the group looking on. All seven matching activities stay
large and readable. Page 4 uses a spacious two-column,
three-row arrangement for the six ownership activities;
pictures and answer choices are never squeezed. Page 5
teaches someone, anyone, everyone, and everything;
something appears only as an optional extension, with a
brief explanation in the Parent Guide. Page 5 self-check
is exactly "Did I use a pronoun?" (one box, not three).
The indefinite-pronoun questions have exactly one
defensible answer each: Someone is one person at the
door; Anyone follows "not" in "I did not see anyone"
with an empty room; Everyone is stated by "All the
children are singing"; Everything is a bag with all
the things inside it.

"For adults" website guidance (57 words, for the
resource page catalog adultGuidance; NOT printed in the
Parent Guide, per the R18/R19/R20/R21/R23 precedent --
the guide carries its own "What your child learns"
paraphrase):
"Pronouns take the place of a name. Help your child say
the name first, then the short word that takes its
place. Point to the picture and ask who it shows. For
mine, yours, his, hers, ours, and theirs, ask whose
thing it is. Then let your child use a pronoun in a
sentence of their own."

Illustrations: two reused JPEGs from approved packs
(p4-your-ball from Resource 23 p3-ball, a beach ball;
p4-our-dog from Resource 21 p1-brave-dog, a small dog
in a rainy garden) and twenty-seven new original
watercolor storybook JPEGs in the approved style. The
Page 2 Noah-running and Mia-reading pictures reuse the
Page 1 he and she pictures inside this pack (the same
boy is Noah, the same girl is Mia). Reuse candidates
inspected and rejected: Resource 23 p1-run-jump shows a
boy jumping, not running, so it cannot carry "He is
running."; Resource 16 p4-cat-mat shows a cat sitting
awake with wide-open eyes, so it could not carry "The cat
is sleeping."; the cat item is now a toy car, because a
pet can take he or she while a toy car can only be "it".
Resource 23 p5-kite shows a boy holding
the string, so it cannot carry "Ana and Ben's kite".
JPEGs embed as DCT, so the PDF stays small.

Shared design code (logo, header, footer) is imported
verbatim from build_phonics_az.py. Do not fork it here.
Header title is drawn at 18pt; the subtitle is drawn at
12pt. The full subtitle, "Grade 1 Reading | Pronouns",
is 162pt at 12pt and ends inside the teal rule.

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

TITLE = "Pronouns"
SUBTITLE = "Grade 1 Reading | Pronouns"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "pronouns")
IMG_DIR = OUT_DIR  # watercolor illustration JPEGs live beside the PDFs

ADULT_GUIDANCE = ("Pronouns take the place of a name. "
                  "Help your child say the name first, then "
                  "the short word that takes its place. "
                  "Point to the picture and ask who it "
                  "shows. For mine, yours, his, hers, ours, "
                  "and theirs, ask whose thing it is. Then "
                  "let your child use a pronoun in a "
                  "sentence of their own.")


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


def _drawn_rect(path, cx, cy, w, h):
    """The rect _draw_image would draw into: (x0, y0, dw, dh)
    in PDF coordinates, for an image fitted inside a w-by-h
    box centred at (cx, cy) preserving aspect ratio."""
    from PIL import Image as _PILImage
    with _PILImage.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    return cx - dw / 2, cy - dh / 2, dw, dh


def _frac_point(rect, fx, fy):
    """A point inside a drawn image rect, given as fractions
    of the image measured from its top-left corner."""
    x0, y0, dw, dh = rect
    return x0 + fx * dw, y0 + (1 - fy) * dh


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


def _pill_centred(pdf, cx, y, word, size=13):
    """One word-choice pill centred at cx, bottom at y."""
    ww = stringWidth(word, "Helvetica-Bold", size) + 22
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(BOX_STROKE)
    pdf.setLineWidth(1.2)
    pdf.roundRect(cx - ww / 2, y, ww, 26, 8, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(cx, y + 9, word)


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


def _self_check(pdf, y, h, lines):
    """The self-check panel: lines, each with an empty
    checkbox the child ticks. Title 15 below the top
    edge, first line 31 below it, 14pt leading. For one
    line, h=50 leaves the checkbox clear of the panel's
    bottom edge. y is the bottom of the panel."""
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
# Page 1 -- Meet the Pronouns (L.1.1(d))
# ---------------------------------------------------------------------------
def _teach_box_p1(pdf, y, h):
    """The pronoun teach box: title plus two model lines.
    y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 16,
                          "A pronoun is a short word that "
                          "takes the place of a name.")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 34,
                          "Mia is a name. She is a pronoun.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, y + h - 52,
        "I, you, he, she, it, we, and they are pronouns.")


# Page 1 matching, redesigned 2026-11-24 at the user's
# request: she rejected the two-block split layout, so
# the matching is now ONE clean activity: seven pills in
# a single vertical list on the left, seven picture cards
# in a single vertical list on the right, in shuffled
# order, with a wide blank centre for drawing matching
# lines. Nothing is split into groups and nothing floats.
#
# FIT: the matching area runs from the teach box bottom
# (524) to the Remember box top (152), 372pt. Seven rows
# at a 52pt pitch use 364pt, leaving a 7pt margin above
# the first card and below the last card. Each card is
# 276x46, so the picture box inside it is 66x44 and the
# caption sits BESIDE the picture (12pt, left-aligned)
# rather than below it: a caption below would have forced
# the picture to about 32pt tall, while beside it the
# picture stays 44pt tall. All seven cards are identical
# in size and layout, with the same thin teal outline and
# pale fill, so the list reads as one calm column.
#
# (word, image, caption) per row, top to bottom. The
# picture order is shuffled against the pill order so the
# child has to find each match, and no picture sits in
# the same row as its own pill (asserted in _p1_matching).
# The we picture shows the speaking child inside the
# group with a speech bubble; the they picture shows the
# speaking child outside the group looking on: the
# distinction is the teaching.
P1_ROWS = [
    ("I", "p1-she.jpg", "She is reading."),
    ("you", "p1-it.jpg", "It is red."),
    ("he", "p1-they.jpg", "They are playing."),
    ("she", "p1-i.jpg", "I am Sam. I can jump."),
    ("it", "p1-we.jpg", "We are playing."),
    ("we", "p1-he.jpg", "He is running."),
    ("they", "p1-you.jpg", "You can jump too!"),
]
# Image file to the pronoun it pictures, for the
# same-row check in _p1_matching.
P1_IMAGE_WORD = {
    "p1-she.jpg": "she", "p1-it.jpg": "it",
    "p1-they.jpg": "they", "p1-i.jpg": "I",
    "p1-we.jpg": "we", "p1-he.jpg": "he",
    "p1-you.jpg": "you",
}


def _p1_matching(pdf):
    """One clean matching activity: seven pills in a single
    vertical list on the left (centred at x=80), seven
    identical picture cards in a single vertical list on
    the right (x 296-572), and a wide blank centre between
    them (about 190pt of clear space from the widest pill
    to the first card) for drawing matching lines. Rows
    are at a 52pt pitch, centres 494 down to 182, so the
    list is centred in the matching area with a 7pt
    margin above the first card and below the last card.
    Each card is 276x46 with a thin teal outline and pale
    fill; the picture draws in a 66x44 box at the card's
    left (heights consistent at 44pt; landscape pictures
    draw 66 wide, the square I picture 44 wide, the
    portrait you picture 22 wide) and the 12pt caption
    sits beside it, left-aligned and vertically centred.
    Pills are 26 tall, centred on the row."""
    pill_cx = 80
    card_x = 296
    card_w = 276
    card_h = 46
    pic_w, pic_h = 66, 44
    caption_x = card_x + 4 + pic_w + 8
    for (word, image, caption), cy in zip(
            P1_ROWS, [494 - i * 52 for i in range(7)]):
        assert word.lower() != P1_IMAGE_WORD[image].lower(), \
            "picture %s sits in its own pill's row: %s" % (
                image, word)
        _pill_centred(pdf, pill_cx, cy - 13, word, size=13)
        pdf.setFillColor(PANEL_FILL)
        pdf.setStrokeColor(PANEL_STROKE)
        pdf.setLineWidth(1)
        pdf.roundRect(card_x, cy - card_h / 2, card_w, card_h,
                      8, stroke=1, fill=1)
        pic_cx = card_x + 4 + pic_w / 2
        path = os.path.join(IMG_DIR, image)
        _draw_image(pdf, path, pic_cx, cy, pic_w, pic_h)
        _fit(caption, "Helvetica", 12, 180, "P1 caption")
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(caption_x, cy - 4, caption)
        if image == "p1-we.jpg":
            # The picture already has an empty speech bubble
            # above the middle child (the speaker, inside
            # the group): put the word "We" in it.
            rect = _drawn_rect(path, pic_cx, cy, pic_w, pic_h)
            bx, by = _frac_point(rect, 0.604, 0.145)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawCentredString(bx, by - 4, "We")
        elif image == "p1-they.jpg":
            # The watching girl stands apart at the right
            # (the speaker, outside the group): a small
            # white bubble with a teal outline and a tail
            # pointing to her, in the open sky above her.
            # Slightly smaller than the 2026-11-23 bubble
            # (26x13 instead of 28x14) and a touch lower
            # (fy 0.16 instead of 0.13) so it stays inside
            # the smaller picture.
            rect = _drawn_rect(path, pic_cx, cy, pic_w, pic_h)
            bx, by = _frac_point(rect, 0.75, 0.16)
            tx, ty = _frac_point(rect, 0.885, 0.275)
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(1)
            p = pdf.beginPath()
            p.moveTo(bx - 4, by - 6.5)
            p.lineTo(bx + 5, by - 6.5)
            p.lineTo(tx, ty)
            p.close()
            pdf.drawPath(p, stroke=1, fill=1)
            pdf.roundRect(bx - 13, by - 6.5, 26, 13, 6.5,
                          stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawCentredString(bx, by - 3, "They")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Meet the Pronouns",
        "A short word takes the place of a name.",
        "Draw a line from each word to its picture.")
    _teach_box_p1(pdf, 524, 64)
    # One clean matching activity: seven pills in a single
    # list on the left, seven picture cards in a single
    # list on the right, wide blank centre for the lines.
    _p1_matching(pdf)
    _remember_box(pdf, 84, 68, [
        "A pronoun takes the place of a name. "
        "She is one girl.",
        "He is one boy. They are more than one."])
    _adult_line(pdf, "Name each picture together first. Say "
                     "the pronoun with its picture.", 68)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Who Are We Talking About? (L.1.1(d))
# ---------------------------------------------------------------------------
def _teach_box_p2(pdf, y, h):
    """The name-first teach box: title plus the worked
    Mia model, with She in teal. y is the bottom of the
    panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 16,
                          "Say the name first. Then use a "
                          "short word.")
    _draw_centred_segments(pdf, y + h - 34, [
        ("Mia is reading. ", "Helvetica", NAVY),
        ("She", "Helvetica-Bold", TEAL),
        (" likes books.", "Helvetica", NAVY)], size=12.5)


def _choice_row(pdf, y, h, image, segments, choices):
    """One choose-the-pronoun row: the picture on the left,
    the sentence with a ruled blank, and the choice pills
    below the sentence. y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    if image:
        _draw_image(pdf, os.path.join(IMG_DIR, image),
                    100, y + h / 2, 96, 56)
        tx = 170
    else:
        tx = 56
    _draw_segments(pdf, tx, y + h - 24, segments, size=13)
    _word_pills(pdf, tx, y + 6, choices, size=13)


P2_ROWS = [
    # (image, sentence segments, choices)
    # The Page 1 he and she pictures are reused here: the
    # same boy is Noah, the same girl is Mia.
    ("p1-he.jpg",
     [("Noah is running. ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" is running fast.", "Helvetica", NAVY)],
     ["he", "she", "they"]),
    ("p1-she.jpg",
     [("Mia is reading. ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" likes books.", "Helvetica", NAVY)],
     ["she", "he", "it"]),
    ("p2-mia-noah-playing.jpg",
     [("Mia and Noah are playing. ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" are playing ball.", "Helvetica", NAVY)],
     ["they", "we", "he"]),
    ("p2-sam-i-building.jpg",
     [("Sam and I are building. ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" are building a tower.", "Helvetica", NAVY)],
     ["we", "they", "I"]),
    # The cat is gone: a pet can take he or she, so "it"
    # was not the only intended pronoun. A toy car can
    # only be "it".
    ("p2-toy-car.jpg",
     [("The toy car is fast. ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" is fast.", "Helvetica", NAVY)],
     ["it", "he", "she"]),
]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Who Are We Talking About?",
        "Say the name first. Then use a short word.",
        "Read each pair. Circle the pronoun that takes the "
        "name's place.")
    _teach_box_p2(pdf, 528, 60)
    for i, (image, segments, choices) in enumerate(P2_ROWS):
        _choice_row(pdf, 448 - i * 70, 66, image, segments,
                    choices)
    _remember_box(pdf, 104, 48, [
        "The pronoun takes the place of the name."])
    _adult_line(pdf, "Cover the name in the second sentence. "
                     "Ask: Who are we talking about?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Me, Him, Her, Us, Them (L.1.1(d))
# ---------------------------------------------------------------------------
def _teach_box_p3(pdf, y, h):
    """The do/after teach box: the two job lines plus the
    worked I/me and Dad/us models. y is the bottom of the
    panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 16,
                          "I, he, she, we, and they do the "
                          "action.")
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 34,
                          "Me, him, her, us, and them come "
                          "after the action word, or after to.")
    _draw_centred_segments(pdf, y + h - 52, [
        ("I help Mom. ", "Helvetica", NAVY),
        ("Mom helps ", "Helvetica", NAVY),
        ("me", "Helvetica-Bold", TEAL),
        (".", "Helvetica", NAVY)], size=12.5)
    _draw_centred_segments(pdf, y + h - 70, [
        ("Dad reads to ", "Helvetica", NAVY),
        ("us", "Helvetica-Bold", TEAL),
        (".", "Helvetica", NAVY)], size=12.5)


P3_ROWS = [
    # (image, sentence segments, choices: object pronoun
    # first, then its subject partner, so the choice itself
    # teaches the contrast)
    ("p3-mom-helps-me.jpg",
     [("Mom helps ", "Helvetica", NAVY),
      ("__blank__", 36),
      (".", "Helvetica", NAVY)],
     ["me", "I"]),
    ("p3-i-see-him.jpg",
     [("I see ", "Helvetica", NAVY),
      ("__blank__", 36),
      (".", "Helvetica", NAVY)],
     ["him", "he"]),
    ("p3-dad-reads-us.jpg",
     [("Dad reads to ", "Helvetica", NAVY),
      ("__blank__", 36),
      (".", "Helvetica", NAVY)],
     ["us", "we"]),
    ("p3-we-thank-her.jpg",
     [("We thank ", "Helvetica", NAVY),
      ("__blank__", 36),
      (".", "Helvetica", NAVY)],
     ["her", "she"]),
    ("p3-we-call-them.jpg",
     [("We call ", "Helvetica", NAVY),
      ("__blank__", 36),
      (".", "Helvetica", NAVY)],
     ["them", "they"]),
]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Me, Him, Her, Us, Them",
        "Some pronouns come after the action.",
        "Read each sentence. Circle the pronoun that comes "
        "after the action word.")
    # Four-line teach box (the "Dad reads to us" model is
    # its own line now), so the box is taller and the rows
    # start lower, at a 68 pitch with 64-tall panels.
    _teach_box_p3(pdf, 504, 84)
    for i, (image, segments, choices) in enumerate(P3_ROWS):
        _choice_row(pdf, 434 - i * 68, 64, image, segments,
                    choices)
    _remember_box(pdf, 104, 48, [
        "Me, him, her, us, and them come after the action "
        "word, or after to."])
    _adult_line(pdf, "Act it out first. Who does it? Who "
                     "does it happen to?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Mine, Yours, His, Hers, Ours, Theirs (L.1.1(d))
# ---------------------------------------------------------------------------
def _teach_box_p4(pdf, y, h):
    """The whose teach box: the my/mine rule, the his rule,
    and the their/theirs rule. y is the bottom of the
    panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 15,
                          "My goes before a thing. Mine "
                          "stands alone.")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 31,
                          "This is my book. The book is mine.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, y + h - 47,
        "His stays the same. This is his ball. The ball is "
        "his.")
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, y + h - 63,
        "Their kite means the kite belongs to Ana and Ben. "
        "Theirs means the same thing.")


OWN_CELLS = [
    # (image, lead-in line, second-line start, choices)
    ("p4-my-book.jpg", "This is my book.",
     "The book is ", ["mine", "yours"]),
    ("p4-your-ball.jpg", "This is your ball.",
     "The ball is ", ["yours", "mine"]),
    ("p4-mias-book.jpg", "This is Mia's book.",
     "The book is ", ["hers", "his"]),
    ("p4-sams-ball.jpg", "This is Sam's ball.",
     "The ball is ", ["his", "hers"]),
    ("p4-our-dog.jpg", "This is our dog.",
     "The dog is ", ["ours", "theirs"]),
    ("p4-their-kite.jpg", "This is Ana and Ben's kite.",
     "The kite is ", ["theirs", "ours"]),
]


def _own_cell(pdf, x0, y0, w, h, image, lead, start, choices):
    """One ownership cell: the picture at the top, the
    lead-in sentence, then the second sentence with its
    blank and the two standalone-form pills. (x0, y0) is
    the bottom-left corner of the cell."""
    _draw_image(pdf, os.path.join(IMG_DIR, image),
                x0 + w / 2, y0 + 84, 96, 60)
    _fit(lead, "Helvetica", 12.5, w - 12, "own lead-in")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawCentredString(x0 + w / 2, y0 + 40, lead)
    # Second line: text + blank + pills, centred as a group.
    segs = [(start, "Helvetica", NAVY), ("__blank__", 36)]
    text_w = _segments_width(segs, size=13)
    pills_w = sum(stringWidth(c, "Helvetica-Bold", 13) + 22
                  for c in choices) + 10 * (len(choices) - 1)
    total = text_w + 10 + pills_w
    assert total <= w - 12, \
        "own cell line too wide: %.1fpt" % total
    x = x0 + (w - total) / 2
    x = _draw_segments(pdf, x, y0 + 12, segs, size=13)
    _word_pills(pdf, x + 10, y0 + 3, choices, size=13)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Mine, Yours, His, Hers, Ours, Theirs",
        "My goes before a thing. Mine stands alone.",
        "Read each pair. Circle the word that stands alone.")
    _teach_box_p4(pdf, 516, 72)
    # Spacious two-column, three-row arrangement: each cell
    # is 266 wide and 114 tall, with room for the picture,
    # both sentences, and the pills. The picture's bottom
    # edge sits 5pt above the lead-in sentence, so the text
    # never crosses the picture.
    _panel(pdf, 40, 148, 532, 360)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 148 + 360 - 16, "Whose is it?")
    for i, (image, lead, start, choices) in enumerate(OWN_CELLS):
        col = i % 2
        row = i // 2
        _own_cell(pdf, 40 + col * 266,
                  148 + 360 - 18 - (row + 1) * 114,
                  266, 114, image, lead, start, choices)
    _remember_box(pdf, 76, 68, [
        "My, your, his, her, our, and their go before a "
        "thing.",
        "Mine, yours, his, hers, ours, and theirs stand "
        "alone."])
    _adult_line(pdf, "Hold the thing. Ask: Whose is it?", 60)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Someone, Anyone, Everyone, Everything (L.1.1(d))
# ---------------------------------------------------------------------------
def _teach_box_p5(pdf, y, h):
    """The indefinite teach box: the four meanings in two
    lines, plus the anyone-after-not line. y is the bottom
    of the panel."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + h - 16,
                          "Someone, anyone, everyone, "
                          "everything.")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, y + h - 34,
        "Someone means one person, but we do not say who. "
        "Anyone means any one person.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, y + h - 52,
        "Everyone means all the people. Everything means "
        "all the things.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, y + h - 70,
        "We use anyone after not. I did not see anyone.")


P5_ROWS = [
    # (image, sentence segments, choices: all four taught
    # words every time, in a different order, so the child
    # must use the picture to choose)
    ("p5-someone-door.jpg",
     [("__blank__", 36),
      (" is at the door.", "Helvetica", NAVY)],
     ["Someone", "Anyone", "Everyone", "Everything"]),
    ("p5-empty-room.jpg",
     [("I looked in the room. ", "Helvetica", NAVY),
      ("I did not see ", "Helvetica", NAVY),
      ("__blank__", 36),
      (".", "Helvetica", NAVY)],
     ["Anyone", "Someone", "Everyone", "Everything"]),
    ("p5-everyone-singing.jpg",
     [("__blank__", 36),
      (" is singing. ", "Helvetica", NAVY),
      ("All the children are singing.", "Helvetica", NAVY)],
     ["Everyone", "Everything", "Someone", "Anyone"]),
    ("p5-everything-bag-inside.jpg",
     [("I put all my things away. ", "Helvetica", NAVY),
      ("__blank__", 36),
      (" is in the bag.", "Helvetica", NAVY)],
     ["Everything", "Everyone", "Anyone", "Someone"]),
]

P5_BANK_1 = "I, he, she, we, they, me, him, her"
P5_BANK_2 = "mine, yours, someone, anyone, everyone, something"


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Someone, Anyone, Everyone, Everything",
        "Some words do not name one person or thing.",
        "Read each sentence. Circle the word that fits.")
    # The teach box has a fourth line now (anyone after
    # not), so it is taller and the rows start lower, at a
    # 74 pitch.
    _teach_box_p5(pdf, 506, 82)
    for i, (image, segments, choices) in enumerate(P5_ROWS):
        _choice_row(pdf, 432 - i * 74, 70, image, segments,
                    choices)
    # Activity B: the application picture, the prompt, the
    # word bank (something appears here as the optional
    # extension), and one writing line.
    _panel(pdf, 40, 104, 532, 110)
    _draw_image(pdf, os.path.join(
        IMG_DIR, "p5-children-playing-ball.jpg"),
        112, 159, 110, 90)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(182, 192,
                   "Write one sentence about the picture.")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(182, 174,
                   "Use a pronoun from the word bank.")
    _draw_segments(pdf, 182, 156, [
        ("Word bank: ", "Helvetica-Bold", TEAL),
        (P5_BANK_1, "Helvetica", NAVY)], size=12)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(182, 140, P5_BANK_2)
    _writing_line(pdf, 182, 556, 122)
    _self_check(pdf, 48, 50, ["Did I use a pronoun?"])
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
GUIDE_INTRO = ("Read each page with your child. Point to "
               "the pictures and talk about them. Let your "
               "child try first, and give a hint only when "
               "stuck. Praise every good try.")
GUIDE_SECTIONS = [
    ("How to help", [
        "Page 1: Name each picture together first. Say the "
        "pronoun with its picture.",
        "Page 2: Cover the name in the second sentence. "
        "Ask: Who are we talking about?",
        "Page 3: Act out who does the action and who comes "
        "after the action word. Try: 'Dad reads to us.' "
        "Try it together.",
        "Page 4: Hold the thing and ask: Whose is it? Then "
        "say the short word together.",
        "Page 5: Point to the picture. Ask: Is it one "
        "person, any person, all the people, or all the "
        "things?",
    ]),
    ("What your child learns", [
        "Your child learns to use pronouns in place of "
        "names, after action words, to show who owns a "
        "thing, and for people and things we do not name.",
    ]),
    ("Answers", [
        ("Page 1", "I, you, he, she, it, we, and they, "
                   "matched to their pictures."),
        ("Page 2", "he; she; they; we; it."),
        ("Page 3", "me; him; us; her; them."),
        ("Page 4", "mine; yours; hers; his; ours; theirs."),
        ("Page 5", "Someone; Anyone; Everyone; Everything. "
                   "Any sentence about the picture that uses "
                   "a pronoun."),
    ]),
    ("Help your child with words", [
        "Say the name first, then the short word.",
        "For I and me, act it out: \"I jump\" and "
        "\"Mom helps me\".",
        "For mine and hers, hold the thing and ask "
        "\"Whose is it?\"",
        "For someone, anyone, and everyone, play a guessing "
        "game. Ask: \"Someone is at the door. Who could it "
        "be?\"",
        "Something is the thing word that pairs with "
        "someone. Try: \"Something is in the bag.\"",
    ]),
    ("If your child finds it hard", [
        "Page 1: Point to who is talking. For we, the "
        "speaker is in the group. For they, the speaker is "
        "outside the group.",
        "Page 3: Use two toys: \"I give the ball to Sam. "
        "Sam gets the ball. I give it to him.\"",
        "Page 4: Cover the name and ask \"Whose is it?\", "
        "then supply the short word.",
        "Page 5: We often use anyone in questions and after "
        "not. For example, 'Can anyone help?' and 'I did "
        "not see anyone.'",
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
    y = _guide_text(pdf, 56, 616, GUIDE_INTRO, size=12,
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
        "Grade 1 Reading: Pronouns. "
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


def _build_bundle(path, old_p4=None):
    """Assemble the bundle from the four rebuilt pages plus
    the existing Page 4, copied losslessly. old_p4 is the
    path of a one-page PDF holding the approved Page 4
    (extracted from the previous bundle before it is
    overwritten); Page 4 is never rebuilt."""
    tmp = []
    builders = [build_p1_page, build_p2_page, build_p3_page,
                None, build_p5_page]
    sources = []
    for i, builder in enumerate(builders):
        if builder is None:
            assert old_p4 is not None, \
                "Page 4 needs the preserved page"
            sources.append(old_p4)
            continue
        p = os.path.join(OUT_DIR, "_tmp_p%d.pdf" % (i + 1))
        builder(p)
        tmp.append(p)
        sources.append(p)
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in sources:
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
    bundle = os.path.join(OUT_DIR, "pronouns.pdf")
    guide = os.path.join(OUT_DIR, "pronouns-parent-guide.pdf")
    review = os.path.join(OUT_DIR, "pronouns-review.pdf")
    # Preserve the approved Page 4 before the bundle is
    # overwritten: extract it from the existing bundle.
    old_p4 = os.path.join(OUT_DIR, "_old_p4.pdf")
    assert os.path.exists(bundle), \
        "no existing bundle to take Page 4 from"
    _old_reader = PdfReader(bundle)
    assert len(_old_reader.pages) == 5, \
        "old bundle is not 5 pages"
    _w = PdfWriter()
    _w.add_page(_old_reader.pages[3])
    with open(old_p4, "wb") as f:
        _w.write(f)
    _build_bundle(bundle, old_p4=old_p4)
    os.remove(old_p4)
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
    page_names = ["meet-the-pronouns",
                  "who-are-we-talking-about",
                  "me-him-her-us-them",
                  "mine-yours-his-hers-ours-theirs",
                  "someone-anyone-everyone-everything"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        if i == 3:
            # Page 4 stays exactly as approved: do not
            # rewrite its per-page PDF.
            continue
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR, "pronouns-p%d-%s.pdf" % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    # The untouched Page 4 per-page PDF must still match
    # the approved hash.
    assert _sha256(os.path.join(
        OUT_DIR, "pronouns-p4-mine-yours-his-hers-ours-theirs.pdf")
    ) == "039789b93cc6ab919a949769cf5bd04058941d77c6ca2ec4cfc8ff683e2c12fc", \
        "Page 4 per-page PDF changed"
    _render_previews(bundle, guide)
    for name in ["pronouns.pdf",
                 "pronouns-parent-guide.pdf",
                 "pronouns-review.pdf",
                 "pronouns-p1-meet-the-pronouns.pdf",
                 "pronouns-p2-who-are-we-talking-about.pdf",
                 "pronouns-p3-me-him-her-us-them.pdf",
                 "pronouns-p4-mine-yours-his-hers-ours-theirs.pdf",
                 "pronouns-p5-someone-anyone-everyone-everything.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text, no
    # standards codes on student pages or the Parent Guide,
    # no first/third person language, no narrator language.
    for name in ["pronouns.pdf", "pronouns-parent-guide.pdf"]:
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
        assert "narrator" not in norm.lower(), \
            "narrator language in %s" % name
    bundle_pages_text = [
        " ".join((PdfReader(bundle).pages[i].extract_text()
                  or "").split())
        for i in range(5)]
    bundle_norm = " ".join(bundle_pages_text)
    # Resource 21 wording must not have leaked into this pack.
    assert "have legs and can move" not in bundle_norm, \
        "R21 wording leaked into the student pages"
    # "because" is taught nowhere in this pack.
    assert "because" not in bundle_norm.lower(), \
        "'because' on a student page"
    # Positional words are never taught here (L.1.1(i) is
    # dropped); the ordinary in/on/at inside the approved
    # sentences are not positional teaching.
    for bad in (" above ", " below ", " behind ", " beside ",
                " between ", " next to ", " in front of ",
                " under ", " through ", " over "):
        assert bad not in bundle_norm.lower(), \
            "positional word %r on a student page" % bad.strip()
    # Resource 23 teaching must not have leaked in: no
    # joining words, no a/an/the/this/that lessons, no
    # sentence types.
    for bad in ("joining word", "Little Words", "Four Kinds",
                "statement", "exclamation",
                "What a beautiful rainbow", "Look at the rainbow"):
        assert bad not in bundle_norm, \
            "R23 wording %r on a student page" % bad
    # "get the action" is gone as a teaching label (the
    # guide keeps "Sam gets the ball" as an ordinary verb
    # in an example sentence, which is not the label).
    for bad in ("get the action", "gets the action",
                "gets it"):
        assert bad not in bundle_norm.lower(), \
            "old 'get the action' wording on a student page: %r" % bad
    # Page 1: the we/they pair and the I sentence.
    p1 = bundle_pages_text[0]
    assert "We are playing." in p1, \
        "'We are playing.' missing from Page 1"
    assert "They are playing." in p1, \
        "'They are playing.' missing from Page 1"
    assert "I am Sam. I can jump." in p1, \
        "'I am Sam. I can jump.' missing from Page 1"
    assert "You can jump too!" in p1, \
        "'You can jump too!' missing from Page 1"
    # Page 2: all five name-replacement sentences.
    p2 = bundle_pages_text[1]
    for frag in ("is running fast.", "likes books.",
                 "are playing ball.", "are building a tower.",
                 "is fast."):
        assert frag in p2, "Page 2 fragment missing: %r" % frag
    # Page 3: the do/after rule and the two models.
    # (pypdf extracts each drawn segment on its own line,
    # so a period drawn as its own segment reads as " ."
    # after normalization; strip that space before
    # checking the model sentences.)
    p3 = bundle_pages_text[2]
    assert "come after the action word, or after to" in p3, \
        "do/after rule missing from Page 3"
    assert "I help Mom." in p3, \
        "'I help Mom.' missing from Page 3"
    p3_clean = p3.replace(" .", ".")
    assert "Mom helps me." in p3_clean, \
        "'Mom helps me.' missing from Page 3"
    assert "Dad reads to us." in p3_clean, \
        "'Dad reads to us.' missing from Page 3"
    # Page 4: the my/mine rule and all six standalone forms.
    p4 = bundle_pages_text[3]
    assert "Mine stands alone" in p4, \
        "'Mine stands alone' missing from Page 4"
    for form in ("mine", "yours", "hers", "his", "ours",
                 "theirs"):
        assert form in p4.lower(), \
            "possessive form %r missing from Page 4" % form
    # Page 5: the four indefinite meanings, the
    # anyone-after-not line, the three revised sentences,
    # and the single revised self-check box.
    p5 = bundle_pages_text[4]
    for frag in ("Someone means one person",
                 "Anyone means any one person",
                 "Everyone means all the people",
                 "Everything means all the things"):
        assert frag in p5, "Page 5 meaning missing: %r" % frag
    assert "We use anyone after not. I did not see anyone." \
        in p5, "anyone-after-not line missing from Page 5"
    assert "I looked in the room. I did not see" in p5, \
        "revised Page 5 item 2 missing"
    assert "is singing. All the children are singing." in p5, \
        "revised Page 5 item 3 missing"
    assert "I put all my things away." in p5, \
        "revised Page 5 item 4 missing"
    for old in ("help me carry this", "is singing in class."):
        assert old not in p5, \
            "old ambiguous Page 5 wording: %r" % old
    assert "Did I use a pronoun?" in p5, \
        "revised self-check missing from Page 5"
    for old in ("Did I join two ideas",
                "Did I choose the right little word",
                "Did I write a question about the picture?"):
        assert old not in p5, \
            "old self-check wording on Page 5: %r" % old
    # In the Parent Guide, "because" appears nowhere and the
    # something extension note must be there.
    guide_text = " ".join(
        (p.extract_text() or "")
        for p in PdfReader(guide).pages)
    guide_norm = " ".join(guide_text.split())
    assert "because" not in guide_norm.lower(), \
        "'because' in the Parent Guide"
    assert "Something is the thing word" in guide_norm, \
        "something extension note missing from the guide"
    assert "Point to who is talking" in guide_norm, \
        "revised Page 1 hard tip missing from the guide"
    assert "Act out who does the action and who comes after " \
        "the action word" in guide_norm, \
        "revised Page 3 help line missing from the guide"
    assert "We often use anyone in questions and after not" \
        in guide_norm, \
        "Page 5 anyone hard tip missing from the guide"
    assert "Can anyone help?" in guide_norm and \
        "I did not see anyone." in guide_norm, \
        "Page 5 anyone examples missing from the guide"
    for bad in ("get the action", "gets the action",
                "gets it"):
        assert bad not in guide_norm.lower(), \
            "old 'get the action' wording in the guide: %r" % bad
    assert "mine; yours; hers; his; ours; theirs." \
        in guide_norm, \
        "Page 4 answers missing from the guide"
    assert "have legs and can move" not in guide_norm, \
        "R21 wording leaked into the Parent Guide"
    # The "For adults" guidance lives on the website
    # resource page, not in the Parent Guide. Confirm the
    # guide carries its own "What your child learns"
    # paraphrase instead of the guidance text, and that
    # the guidance is exactly 57 words.
    assert "Point to the picture and ask who it shows" \
        not in guide_norm, "For adults text leaked into guide"
    assert "ask whose thing it is" not in guide_norm, \
        "For adults text leaked into guide"
    assert len(ADULT_GUIDANCE.split()) == 57, \
        "For adults guidance is %d words, not 57" % len(
            ADULT_GUIDANCE.split())
    print("text checks: clean; For adults guidance is 57 words")


if __name__ == "__main__":
    main()
