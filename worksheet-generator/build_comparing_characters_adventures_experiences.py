#!/usr/bin/env python3
"""Grade 1 Reading - Comparing Characters' Adventures and
Experiences (RL.1.9).

A supplementary pack in the approved and locked Grade 1
Reading and Language Arts roadmap (audit 2026-11-05), after
the one-time comprehensive curriculum and overlap audit
(~/workspace/research_notes/grade-1-ela-audit-20261120/
report.md). RL.1.9 was Missing and ownerless after it was
removed from Resource 19 at her direction 2026-11-19, and
the 2026-11-20 audit proposed a combined RL.1.5 + RL.1.9
pack. Plan approved 2026-11-24 with her decisions: this
five-page pack REPLACES the planned two-page RL.1.9
portion of that combined pack (no duplicate RL.1.9
worksheets); RL.1.5 stays a separately planned future
resource titled "Story Book or Information Book?" and is
not built now; Resource 24 is reserved for "Ask and Speak
Up at School" (Communication and Life Skills), so this
pack is identified by title and RL.1.9 standard only and
is not numbered. Two original stories starring Maya and
Theo, with their established Resource 13 appearances
(Maya: dark hair in a ponytail, teal dress; Theo: short
black hair, yellow shirt, blue shorts). 5 student pages
plus a separate 1-page Parent Guide.

Placement: Grade 1 / Reading and Language / Literature.
Standard RL.1.9 taught; no other standard claimed.
Standards appear on the resource page only, never on
student pages or the Parent Guide.

Final stories (approved wording, verbatim):
Story A, "Maya and the Big Slide": "Maya goes to the
park. She sees the big slide. Maya feels scared. Ana
goes down first and says, 'Come on!' Maya goes down the
slide. She feels happy. 'Again!' she says."
Story B, "Theo and the Shallow Pool": "Theo goes to the
pool. He sees the shallow pool. Theo feels scared. Dad
stands beside him and says, 'Come on! You can do it!'
Theo steps into the water. Theo feels happy. 'Again!'
he says."
Revised at her direction: shallow pool, Dad beside him
reassuring, Theo steps in. No deep pool, no jumping in.
Similarities preserved: both feel scared, receive
encouragement, try something new, feel happy.
Differences preserved: playground vs. pool, slide vs.
water, Ana vs. Dad, sliding down vs. stepping into
the water.

Boundaries, verified against the audit 2026-11-20 and
the built packs: RL.1.9 only. No retelling, no
sequencing, no generic comprehension questions. No
Resource 20 three-column "Both Books / Only A / Only B"
fact sort. No RL.1.5 story-vs-information sorting.
No narrator work (Resource 19 owns it). No possessive
nouns (Resource 17). No joining words, determiners, or
sentence types (Resource 23). No pronouns as grammar
(Resource 22). No shades of meaning or context-clue
strategy (Resource 21). No "first person" or "third
person" language. No prediction. Every answer is visible
in the picture or the sentence. "because" appears
nowhere in this pack. "deep" and "jump" appear nowhere
in this pack.

"For adults" website guidance (55 words, for the
resource page catalog adultGuidance; NOT printed in the
Parent Guide, per the R18/R19/R20/R21/R22/R23 precedent --
the guide carries its own "What your child learns"
paraphrase):
"Comparing two characters helps your child see how
stories can be alike and different. Read both stories
with your child and talk about the pictures. Ask how
Maya and Theo felt, what helped them, and what was
different. Then let your child tell you one way they
are alike and one way they are different."

Illustrations: eleven new original watercolor storybook
JPEGs in the approved style, made for this pack. Pictures
are reused across pages wherever possible instead of
generating new ones. JPEGs embed as DCT, so the PDF
stays small.

Shared design code (logo, header, footer) is imported
verbatim from build_phonics_az.py. Do not fork it here.
Header title is drawn at 18pt; the subtitle is drawn at
12pt. The header title "Comparing Characters" and the
subtitle "Grade 1 Reading | Comparing Characters" both
start at x=234 and must end inside the right margin
(552); the builder asserts both widths.

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

TITLE = "Comparing Characters"
SUBTITLE = "Grade 1 Reading | Comparing Characters"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files",
                       "comparing-characters-adventures-experiences")
IMG_DIR = OUT_DIR  # watercolor illustration JPEGs live beside the PDFs

ADULT_GUIDANCE = ("Comparing two characters helps your child "
                  "see how stories can be alike and different. "
                  "Read both stories with your child and talk "
                  "about the pictures. Ask how Maya and Theo "
                  "felt, what helped them, and what was "
                  "different. Then let your child tell you one "
                  "way they are alike and one way they are "
                  "different.")
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




def _teach_box(pdf, y, h, lines):
    """A light panel with centred lines and no title. y is
    the bottom, h the height. Lines at 12.5pt, first
    baseline h-24 below the top edge, 17pt leading."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    ly = y + h - 24
    for line in lines:
        _fit(line, "Helvetica", 12.5, 500, "teach line")
        pdf.drawCentredString(PAGE_WIDTH / 2, ly, line)
        ly -= 17


def _story_panel(pdf, x, y, w, h, image, story_title, lines):
    """One story panel: a large picture, the story title,
    and the story lines left-aligned. (x, y) is the
    bottom-left corner."""
    _panel(pdf, x, y, w, h)
    _draw_image(pdf, image, x + w / 2, y + h - 70, 240, 125)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    _fit(story_title, "Helvetica-Bold", 13, w - 28,
         "story title")
    pdf.drawCentredString(x + w / 2, y + h - 151, story_title)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    ly = y + h - 169
    for line in lines:
        _fit(line, "Helvetica", 12, w - 28, "story line")
        pdf.drawString(x + 14, ly, line)
        ly -= 13.5


# ---------------------------------------------------------------------------
# Page 1 -- Two Adventures (RL.1.9)
# ---------------------------------------------------------------------------

def _p1_match_cell(pdf, x, image):
    """One matching picture with Maya and Theo pills below
    it. The child circles the right name. x is the left
    edge of the 133pt cell."""
    _draw_image(pdf, image, x + 66, 280, 120, 80)
    total = (stringWidth("Maya", "Helvetica-Bold", 12) + 22
             + 10
             + stringWidth("Theo", "Helvetica-Bold", 12) + 22)
    _word_pills(pdf, x + (133 - total) / 2, 208,
                ["Maya", "Theo"], size=12)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(pdf, "Two Adventures", "Maya and Theo",
                "Read both stories. Circle the right name "
                "under each picture.")
    _story_panel(pdf, 40, 332, 260, 260,
                 os.path.join(IMG_DIR, "cca-maya-slide.jpg"),
                 "Maya and the Big Slide",
                 ["Maya goes to the park.",
                  "She sees the big slide.",
                  "Maya feels scared.",
                  "Ana goes down first and says, 'Come on!'",
                  "Maya goes down the slide.",
                  "She feels happy. 'Again!' she says."])
    _story_panel(pdf, 312, 332, 260, 260,
                 os.path.join(IMG_DIR, "cca-theo-pool.jpg"),
                 "Theo and the Shallow Pool",
                 ["Theo goes to the pool.",
                  "He sees the shallow pool.",
                  "Theo feels scared.",
                  "Dad stands beside him and says,",
                  "'Come on! You can do it!'",
                  "Theo steps into the water.",
                  "Theo feels happy. 'Again!' he says."])
    # Four experience pictures, shuffled so the two Maya
    # pictures and the two Theo pictures interleave. Each
    # picture is distinguishable by setting and action
    # (slide vs. water, park vs. pool), not just by who
    # is in it.
    _p1_match_cell(pdf, 40,
                   os.path.join(IMG_DIR, "cca-maya-scared.jpg"))
    _p1_match_cell(pdf, 173,
                   os.path.join(IMG_DIR, "cca-theo-happy.jpg"))
    _p1_match_cell(pdf, 306,
                   os.path.join(IMG_DIR, "cca-maya-happy.jpg"))
    _p1_match_cell(pdf, 439,
                   os.path.join(IMG_DIR, "cca-theo-scared.jpg"))
    _remember_box(pdf, 132, 68,
                  ["Each story is about one child.",
                   "Look at the picture to tell whose story "
                   "it is."])
    _adult_line(pdf, "Read each story aloud first. Point to "
                     "the picture and ask: Who is this?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- How Are They Alike? (RL.1.9)
# ---------------------------------------------------------------------------

def _p2_cell(pdf, x0, y0, w, h, images, sentence):
    """One choice cell: picture(s) above, one sentence
    below. The child circles the picture only if the
    sentence happened to both children."""
    _panel(pdf, x0, y0, w, h)
    if len(images) == 2:
        _draw_image(pdf, images[0], x0 + w / 2 - 48,
                    y0 + h - 46, 85, 68)
        _draw_image(pdf, images[1], x0 + w / 2 + 48,
                    y0 + h - 46, 85, 68)
    else:
        _draw_image(pdf, images[0], x0 + w / 2, y0 + h - 46,
                    110, 80)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12.5)
    _fit(sentence, "Helvetica-Bold", 12.5, w - 20,
         "choice sentence")
    pdf.drawCentredString(x0 + w / 2, y0 + 20, sentence)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(pdf, "How Are They Alike?", "Maya and Theo",
                "Circle only what happened to both children.")
    _teach_box(pdf, 524, 68,
               ["Maya and Theo did some things the same.",
                "Some things happened to only one child."])
    img = lambda name: os.path.join(IMG_DIR, name)
    # Six choices, interleaved so the four shared
    # experiences and the two differences are not grouped.
    # Row 1: scared (both) | slide (Maya only).
    # Row 2: tried (both) | water (Theo only).
    # Row 3: help (both) | happy (both).
    _p2_cell(pdf, 40, 384, 260, 128,
             [img("cca-maya-scared.jpg"),
              img("cca-theo-scared.jpg")],
             "Both felt scared.")
    _p2_cell(pdf, 312, 384, 260, 128,
             [img("cca-maya-happy.jpg")],
             "Went down a slide.")
    _p2_cell(pdf, 40, 248, 260, 128,
             [img("cca-maya-happy.jpg"),
              img("cca-theo-happy.jpg")],
             "Both tried something new.")
    _p2_cell(pdf, 312, 248, 260, 128,
             [img("cca-theo-happy.jpg")],
             "Stepped into the water.")
    _p2_cell(pdf, 40, 112, 260, 128,
             [img("cca-ana-help.jpg"),
              img("cca-dad-help.jpg")],
             "Both got help.")
    _p2_cell(pdf, 312, 112, 260, 128,
             [img("cca-maya-again.jpg"),
              img("cca-theo-again.jpg")],
             "Both felt happy.")
    _adult_line(pdf, "Say each one aloud. Ask: Did this "
                     "happen to both?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- How Are They Different? (RL.1.9)
# ---------------------------------------------------------------------------

def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(pdf, "How Are They Different?", "Maya and Theo",
                "Look at what happened in each story. Draw a "
                "line to Maya or Theo.")
    _teach_box(pdf, 536, 56,
               ["Maya and Theo did some things that were not "
                "the same.",
                "Look at what happened in each picture. Draw "
                "a line to the child it happened to."])
    img = lambda name: os.path.join(IMG_DIR, name)
    # Six pictures in a 3-by-2 grid, shuffled so Maya and
    # Theo pictures interleave. Each picture carries a
    # short experience label: the task is to match what
    # happened, not to name the child in the picture.
    # Row 1: the big slide (Maya) | Dad helped (Theo) |
    # went down the slide (Maya).
    # Row 2: the shallow pool (Theo) | Ana helped (Maya) |
    # stepped into the water (Theo).
    for cx, cy, name, label in [
            (125, 484, "cca-maya-slide.jpg", "the big slide"),
            (305, 484, "cca-dad-help.jpg", "Dad helped"),
            (485, 484, "cca-maya-happy.jpg",
             "went down the slide"),
            (125, 368, "cca-theo-pool.jpg", "the shallow pool"),
            (305, 368, "cca-ana-help.jpg", "Ana helped"),
            (485, 368, "cca-theo-happy.jpg",
             "stepped into the water")]:
        _draw_image(pdf, img(name), cx, cy, 150, 90)
        _fit(label, "Helvetica-Bold", 12, 170, "Page 3 label")
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(cx, cy - 58, label)
    # Two large target panels, each headed by the
    # character's picture and name. The child draws a line
    # from each picture to the right panel.
    for x0, name, image in [
            (40, "Maya", "cca-maya-scared.jpg"),
            (312, "Theo", "cca-theo-scared.jpg")]:
        _panel(pdf, x0, 95, 260, 175)
        _draw_image(pdf, img(image), x0 + 130, 230, 90, 70)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(x0 + 130, 172, name)
    _adult_line(pdf, "Name what happened in each picture "
                     "first. Then ask: Which character did "
                     "this happen to?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Alike and Different (RL.1.9)
# ---------------------------------------------------------------------------

def _p4_bank_chip(pdf, cx, image, word):
    """One picture-word chip: a small picture with the
    word below it."""
    _draw_image(pdf, image, cx, 535, 70, 55)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(cx, 495, word)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(pdf, "Alike and Different", "Maya and Theo",
                "Use the picture words to finish each "
                "sentence.")
    img = lambda name: os.path.join(IMG_DIR, name)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, 572, "Picture words:")
    # The bank is shuffled so its left-to-right order does
    # not give the sentence answers away.
    for cx, name, word in [
            (90, "cca-theo-pool.jpg", "water"),
            (190, "cca-ana-help.jpg", "Ana"),
            (290, "cca-both-scared.jpg", "scared"),
            (390, "cca-dad-help.jpg", "Dad"),
            (490, "cca-maya-slide.jpg", "slide")]:
        _p4_bank_chip(pdf, cx, img(name), word)
    # Three sentence pairs. Blanks are ruled lines the
    # child writes the picture word on.
    sentences = [
        (440, [("Maya and Theo both felt ", "Helvetica-Bold",
                NAVY), ("__blank__", 70),
               (".", "Helvetica-Bold", NAVY)]),
        (370, [("Maya went down the ", "Helvetica-Bold",
                NAVY), ("__blank__", 70),
               (". Theo stepped into the ", "Helvetica-Bold",
                NAVY), ("__blank__", 70),
               (".", "Helvetica-Bold", NAVY)]),
        (300, [("__blank__", 60),
               (" helped Maya. ", "Helvetica-Bold", NAVY),
               ("__blank__", 60),
               (" helped Theo.", "Helvetica-Bold", NAVY)]),
    ]
    for y, segs in sentences:
        assert _segments_width(segs, 14) <= 532, \
            "Page 4 sentence too wide: %r" % (segs,)
        _draw_centred_segments(pdf, y, segs, size=14)
    _remember_box(pdf, 180, 68,
                  ["Alike means the same.",
                   "Different means not the same."])
    _adult_line(pdf, "Point to the picture words first. "
                     "Then read each sentence together.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Tell About Both (RL.1.9)
# ---------------------------------------------------------------------------

def _p5_writing_area(pdf, y, h, label):
    """One large writing area: a light panel with a label
    and four ruled lines. y is the bottom, h the height."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 20, label)
    ly = y + h - 48
    for _ in range(4):
        _writing_line(pdf, 56, 556, ly)
        ly -= 25


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(pdf, "Tell About Both", "Maya and Theo",
                "Write one way they are alike and one way "
                "they are different.")
    _draw_image(pdf,
                os.path.join(IMG_DIR, "cca-together.jpg"),
                PAGE_WIDTH / 2, 520, 200, 120)
    _p5_writing_area(pdf, 300, 140,
                     "One way they are alike:")
    _p5_writing_area(pdf, 140, 140,
                     "One way they are different:")
    _self_check(pdf, 64, 50,
                ["Did I tell one way they are alike and one "
                 "way they are different?"])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Parent Guide (separate one-page guide, NOT in the student bundle)
# ---------------------------------------------------------------------------

GUIDE_TITLE = "How to Use This Pack"
GUIDE_INTRO = ("Read each page with your child. Point to "
               "the pictures and talk about them. Let your "
               "child try first, and give a hint only when "
               "stuck. Praise every good try.")
GUIDE_SECTIONS = [
    ("How to help", [
        "Page 1: Read both stories aloud. Point to each "
        "picture and name what happens.",
        "Page 2: Say each one aloud. Ask: Did this happen "
        "to both children?",
        "Page 3: Name what happened in each picture. Ask: "
        "Which character did this happen to?",
        "Page 4: Point to the picture words first. Then let "
        "your child choose the word.",
        "Page 5: Let your child say the sentence aloud "
        "first. Then help them write it.",
    ]),
    ("What your child learns", [
        "Your child learns to compare what two characters "
        "do and feel in two stories, to tell what is the "
        "same and what is different, and to say it in a "
        "sentence of their own.",
    ]),
    ("Answers", [
        ("Page 1", "Scared Maya at the slide, Maya. Happy "
                   "Theo in the pool, Theo. Happy Maya on "
                   "the slide, Maya. Scared Theo at the "
                   "pool, Theo."),
        ("Page 2", "Circle: both felt scared; both got "
                   "help; both tried something new; both "
                   "felt happy. Do not circle: went down a "
                   "slide; stepped into the water."),
        ("Page 3", "Maya: the big slide, Ana helped, went "
                   "down the slide. Theo: the shallow pool, "
                   "Dad helped, stepped into the water."),
        ("Page 4", "1. scared. 2. slide; water. 3. Ana; "
                   "Dad."),
        ("Page 5", "Any sentence that tells one way they "
                   "are alike and one way they are "
                   "different. For example: 'Both felt "
                   "scared.' and 'Maya went down the slide. "
                   "Theo stepped into the water.'"),
    ]),
    ("Four tips", [
        "Read both stories aloud first, before any page.",
        "For 'alike', ask: Did this happen to both "
        "children?",
        "For 'different', ask: Which character did this "
        "happen to?",
        "Let your child point to the picture before "
        "choosing the word.",
    ]),
    ("If your child finds it hard", [
        "Page 2: Cover one story. Ask what happened in the "
        "other story. Then ask: Did it happen in both?",
        "Page 5: Let your child say the sentence aloud "
        "first, then write it. Your child may point, "
        "speak, or dictate while you write it down.",
    ]),
    ("Try this next", [
        "Read two story books together. Ask your child to "
        "tell you one way the characters are alike and one "
        "way they are different.",
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
        "Grade 1 Reading: Comparing Characters' Adventures "
        "and Experiences. For parents, not for the child.")
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
    """Assemble the bundle from the five freshly built
    pages, copied losslessly."""
    from pypdf import PdfReader, PdfWriter
    tmp = []
    builders = [build_p1_page, build_p2_page, build_p3_page,
                build_p4_page, build_p5_page]
    sources = []
    for i, builder in enumerate(builders):
        p = os.path.join(OUT_DIR, "_tmp_p%d.pdf" % (i + 1))
        builder(p)
        tmp.append(p)
        sources.append(p)
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
    # The header title and subtitle start at x=234 and must
    # end inside the right margin (552).
    _fit(TITLE, "Helvetica-Bold", 18, 318, "header title")
    _fit(SUBTITLE, "Helvetica-Bold", 12, 318,
         "header subtitle")
    bundle = os.path.join(
        OUT_DIR,
        "comparing-characters-adventures-experiences.pdf")
    guide = os.path.join(
        OUT_DIR,
        "comparing-characters-adventures-experiences-"
        "parent-guide.pdf")
    review = os.path.join(
        OUT_DIR,
        "comparing-characters-adventures-experiences-"
        "review.pdf")
    _build_bundle(bundle)
    build_parent_guide(guide)
    writer = PdfWriter()
    for src in (bundle, guide):
        for page in PdfReader(src).pages:
            writer.add_page(page)
    with open(review, "wb") as f:
        writer.write(f)
    # Individual per-page PDFs, split losslessly from the
    # final bundle (pypdf copies each page object
    # verbatim, so the vector text and pictures are
    # identical to the combined pack). Never build these
    # from the raster preview PNGs.
    page_names = ["two-adventures",
                  "how-are-they-alike",
                  "how-are-they-different",
                  "alike-and-different",
                  "tell-about-both"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR,
            "comparing-characters-adventures-experiences-"
            "p%d-%s.pdf" % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    _render_previews(bundle, guide)
    for name in ["comparing-characters-adventures-"
                 "experiences.pdf",
                 "comparing-characters-adventures-"
                 "experiences-parent-guide.pdf",
                 "comparing-characters-adventures-"
                 "experiences-review.pdf",
                 "comparing-characters-adventures-"
                 "experiences-p1-two-adventures.pdf",
                 "comparing-characters-adventures-"
                 "experiences-p2-how-are-they-alike.pdf",
                 "comparing-characters-adventures-"
                 "experiences-p3-how-are-they-different.pdf",
                 "comparing-characters-adventures-"
                 "experiences-p4-alike-and-different.pdf",
                 "comparing-characters-adventures-"
                 "experiences-p5-tell-about-both.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text, no
    # standards codes on student pages or the Parent Guide,
    # no first/third person language, no narrator language.
    for name in ["comparing-characters-adventures-"
                 "experiences.pdf",
                 "comparing-characters-adventures-"
                 "experiences-parent-guide.pdf"]:
        text = " ".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        norm = " ".join(text.split())
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
        assert "L.1" not in norm, \
            "standards code in %s" % name
        assert "RL.1" not in norm, \
            "standards code in %s" % name
        assert "first person" not in norm.lower(), \
            "first person in %s" % name
        assert "third person" not in norm.lower(), \
            "third person in %s" % name
        assert "narrator" not in norm.lower(), \
            "narrator language in %s" % name
        assert "because" not in norm.lower(), \
            "'because' in %s" % name
    bundle_pages_text = [
        " ".join((PdfReader(bundle).pages[i].extract_text()
                  or "").split())
        for i in range(5)]
    bundle_norm = " ".join(bundle_pages_text)
    # The revised Theo story: shallow pool, Dad beside him,
    # stepping in. No deep pool, no jumping in.
    assert "deep" not in bundle_norm.lower(), \
        "'deep' on a student page"
    assert "jump" not in bundle_norm.lower(), \
        "'jump' on a student page"
    # No RL.1.5 story-vs-information sorting.
    for bad in ("story book", "information book",
                "true facts", "made-up"):
        assert bad not in bundle_norm.lower(), \
            "RL.1.5 wording %r on a student page" % bad
    # No Resource 20 three-column fact sort.
    for bad in ("Both Books", "Only Book A", "Only Book B"):
        assert bad not in bundle_norm, \
            "R20 wording %r on a student page" % bad
    # No retelling or sequencing.
    for bad in ("retell", "beginning, middle",
                "first, next, last"):
        assert bad not in bundle_norm.lower(), \
            "retelling/sequencing wording %r on a student " \
            "page" % bad
    # Page 1: both stories verbatim.
    p1 = bundle_pages_text[0]
    for frag in ("Maya goes to the park.",
                 "She sees the big slide.",
                 "Maya feels scared.",
                 "Ana goes down first and says, 'Come on!'",
                 "Maya goes down the slide.",
                 "She feels happy. 'Again!' she says.",
                 "Theo goes to the pool.",
                 "He sees the shallow pool.",
                 "Theo feels scared.",
                 "Dad stands beside him and says,",
                 "'Come on! You can do it!'",
                 "Theo steps into the water.",
                 "Theo feels happy. 'Again!' he says."):
        assert frag in p1, "Page 1 fragment missing: %r" % frag
    # Page 2: all six choices.
    p2 = bundle_pages_text[1]
    for frag in ("Both felt scared.", "Went down a slide.",
                 "Both tried something new.",
                 "Stepped into the water.", "Both got help.",
                 "Both felt happy."):
        assert frag in p2, "Page 2 choice missing: %r" % frag
    # Page 3: the two column names, the experience
    # directions, and the six experience labels.
    p3 = bundle_pages_text[2]
    assert "Maya" in p3 and "Theo" in p3, \
        "Page 3 column names missing"
    assert "Look at what happened in each story. Draw a " \
        "line to Maya or Theo." in p3, \
        "Page 3 directions missing"
    for label in ("the big slide", "Ana helped",
                  "went down the slide", "the shallow pool",
                  "Dad helped", "stepped into the water"):
        assert label in p3, \
            "Page 3 label missing: %r" % label
    # Page 4: the three sentence frames and the
    # alike/different rule.
    p4 = bundle_pages_text[3]
    for frag in ("Maya and Theo both felt",
                 "Maya went down the",
                 "Theo stepped into the",
                 "helped Maya", "helped Theo",
                 "Alike means the same.",
                 "Different means not the same."):
        assert frag in p4, "Page 4 fragment missing: %r" % frag
    # The five picture-word choices are unchanged; the
    # scared picture now shows both children.
    for word in ("scared", "slide", "water", "Ana", "Dad"):
        assert word in p4, \
            "Page 4 picture word missing: %r" % word
    # Page 5: the two writing labels and the self-check.
    p5 = bundle_pages_text[4]
    for frag in ("One way they are alike:",
                 "One way they are different:",
                 "Did I tell one way they are alike and one "
                 "way they are different?"):
        assert frag in p5, "Page 5 fragment missing: %r" % frag
    # In the Parent Guide: the modality support, the
    # extension, and the exact answers.
    guide_text = " ".join(
        (p.extract_text() or "")
        for p in PdfReader(guide).pages)
    guide_norm = " ".join(guide_text.split())
    assert "point, speak, or dictate" in guide_norm, \
        "modality support missing from the guide"
    assert "Read two story books together" in guide_norm, \
        "extension missing from the guide"
    # Page 1 answers are listed in picture order, left to
    # right: Maya, Theo, Maya, Theo.
    assert "Scared Maya at the slide, Maya. Happy Theo in " \
        "the pool, Theo. Happy Maya on the slide, Maya. " \
        "Scared Theo at the pool, Theo." in guide_norm, \
        "Page 1 answers missing from the guide"
    assert "Maya: the big slide, Ana helped, went down the " \
        "slide. Theo: the shallow pool, Dad helped, stepped " \
        "into the water." in guide_norm, \
        "Page 3 answers missing from the guide"
    assert "Which character did this happen to?" \
        in guide_norm, \
        "Page 3 guidance question missing from the guide"
    assert "1. scared. 2. slide; water. 3. Ana; Dad." \
        in guide_norm, "Page 4 answers missing from the guide"
    # The "For adults" guidance lives on the website
    # resource page, not in the Parent Guide. Confirm the
    # guide carries its own "What your child learns"
    # paraphrase instead of the guidance text, and that
    # the guidance is exactly 55 words.
    assert "Comparing two characters helps your child see " \
        "how stories can be alike" not in guide_norm, \
        "For adults text leaked into guide"
    assert len(ADULT_GUIDANCE.split()) == 55, \
        "For adults guidance is %d words, not 55" % len(
            ADULT_GUIDANCE.split())
    print("text checks: clean; For adults guidance is 55 words")


if __name__ == "__main__":
    main()
