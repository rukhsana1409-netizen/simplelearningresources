#!/usr/bin/env python3
"""Grade 1 Reading - Two Books, One Topic (apples).

Resource 20 in the approved and locked Grade 1 Reading and
Language Arts roadmap (audit 2026-11-05). Plan approved
2026-11-20 with the user's refinements, apples as the
topic, 5 student pages plus a separate 1-page Parent Guide.

Placement: Grade 1 / Reading and Language / Informational
Reading. Standards RI.1.9 (main focus), RI.1.8 and RI.1.4
addressed where appropriate; RI.1.10 is a level condition
only. This pack claims RI.1.9 ONLY, not RL.1.9. RL.1.5 and
RL.1.9 were removed from Resource 19 at her direction and
remain recorded curriculum gaps for the later reading
audit; no new packs are created for them.

Boundaries, verified against the built packs 2026-11-20:
Resource 14 teaches main topic and key details inside one
text, and its Page 4 already teaches within-text
cause-and-effect, so Page 4 here must keep its two-book
source question ("Which book tells you why...?") front
and center. Resource 15 teaches word meaning from a
glossary (Page 3) and picture-vs-words inside one book
(Page 4), so the RI.1.4 work here comes from the sentence
and picture, never from a glossary. Resource 21 owns
shades of meaning; this pack never ranks synonyms.
Resource 22 owns pronouns as grammar; "they" in the
texts is ordinary text, never a taught item. No
story-vs-information sorting, per her Resource 19
refinement. No prediction, no inference beyond the text.

Her refinements (binding): Pages 3, 4, and 5 carry a
readable reference panel with both Book A and Book B
texts, so children answer without relying on memory.
Page 4 connects each point with the reason actually
stated in that book, and asks which book tells each
reason. Page 5 is an independent comparison activity
with three generous drawing and writing spaces and a
self-check. No adult line on Page 5.

Revisions approved 2026-11-20 after her visual
review: Page 5 boxes enlarged to 100pt with ONE
writing line at the bottom and the labels "One fact
only in Book A", "One fact only in Book B", "The same
in both books"; Page 2 "sweet" choices changed to
"tastes sugary" / "tastes sour"; Page 3 uses the full
original wording for the two shortened facts, wrapped
onto two lines each. Approved passages, illustrations,
and overall design preserved; Pages 1 and 4 unchanged.

"For adults" website guidance (60 words, for the
resource page catalog adultGuidance; NOT printed in the
Parent Guide, per the R18/R19 precedent -- the guide
carries its own "What your child learns" paraphrase):
"Two books can tell about one topic. Help your child
read both books about apples. Ask what is the same in
both books, and what is new in each one. Point to the
reason the author gives. Help your child work out a
hard word from the words and picture near it. Then let
your child tell what they learned."

Illustrations: four new original watercolor storybook
JPEGs in the approved style from Resources 16 to 19
(p1-apple-tree, p2-apple-slices-juice, p3-two-books,
p4-farmer-picking). The P2 juice picture is reused on
Page 4 for the juice point. JPEGs embed as DCT, so the
PDF stays small.

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

TITLE = "Two Books, One Topic"
SUBTITLE = "Grade 1 Reading | Two Books, One Topic"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "two-books-one-topic")
IMG_DIR = OUT_DIR  # watercolor illustration JPEGs live beside the PDFs

BOOK_A_TITLE = "How Apples Grow"
BOOK_B_TITLE = "Eating Apples"
# The two book texts, kept verbatim from the approved plan.
# The last sentence of each book is split across two lines
# when drawn, so it fits the panel; the wording is unchanged.
BOOK_A_LINES = ["Apples are a fruit.",
                "Apples grow on trees.",
                "Some apples are red.",
                "A flower grows first.",
                "Farmers pick the apples in fall",
                "because they are ripe."]
BOOK_B_LINES = ["Apples are a fruit.",
                "Apples are good to eat.",
                "Some apples are red.",
                "We can cut an apple into slices.",
                "We drink apple juice because",
                "it tastes sweet."]

ADULT_GUIDANCE = ("Two books can tell about one topic. Help "
                  "your child read both books about apples. "
                  "Ask what is the same in both books, and "
                  "what is new in each one. Point to the "
                  "reason the author gives. Help your child "
                  "work out a hard word from the words and "
                  "picture near it. Then let your child tell "
                  "what they learned.")


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
    assert px >= 56 + stringWidth(question, "Helvetica", 13) \
        + 8, "question and pills overlap: %r" % question
    _word_pills(pdf, px, y + h / 2 - 13, choices, size=13)


def _reference_panel(pdf, y, h):
    """The two-book reference panel used on Pages 3, 4,
    and 5: Book A text in the left column, Book B text in
    the right column, both at 12pt, so the child can answer
    without relying on memory. y is the bottom of the
    panel; the panel is always 532 wide at x=40."""
    _panel(pdf, 40, y, 532, h)
    for label, lines, x in (("Book A", BOOK_A_LINES, 56),
                            ("Book B", BOOK_B_LINES, 316)):
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(x, y + h - 24, label)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 12)
        ly = y + h - 44
        for line in lines:
            _fit(line, "Helvetica", 12, 240, "reference line")
            pdf.drawString(x, ly, line)
            ly -= 16
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.line(306, y + 8, 306, y + h - 8)


# ---------------------------------------------------------------------------
# Pages 1 and 2 -- Meet Book A / Meet Book B
# ---------------------------------------------------------------------------
def _book_panel(pdf, y, h, label, image, lines):
    """One book on Pages 1 and 2: the illustration on the
    left, the labelled book text on the right. y is the
    bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, image, 150, y + h / 2, 200, 133)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(280, y + h - 26, label)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 14)
    ly = y + h - 48
    for line in lines:
        _fit(line, "Helvetica", 14, 292, "book line")
        pdf.drawString(280, ly, line)
        ly -= 22


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Meet Book A", "How Apples Grow",
        "Read Book A. Then answer the questions.")
    _book_panel(
        pdf, 392, 200, "Book A",
        os.path.join(IMG_DIR, "p1-apple-tree.jpg"),
        BOOK_A_LINES)
    _choice_question_row(pdf, 320, 64,
                         "What is this book about? Circle one.",
                         ["apples", "trees"])
    _choice_question_row(pdf, 246, 64,
                         "Where do apples grow? Circle one.",
                         ["trees", "flowers"])
    _choice_question_row(pdf, 172, 64,
                         "What does ripe mean? Circle one.",
                         ["ready to pick", "green and hard"])
    _remember_box(pdf, 96, 68, [
        "Apples grow on trees.",
        "Farmers pick the apples in fall because they are "
        "ripe."])
    _adult_line(pdf, "Point to the apple tree. Ask: Where do "
                     "apples grow?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Meet Book B", "Eating Apples",
        "Read Book B. Then answer the questions.")
    _book_panel(
        pdf, 392, 200, "Book B",
        os.path.join(IMG_DIR, "p2-apple-slices-juice.jpg"),
        BOOK_B_LINES)
    _choice_question_row(pdf, 320, 64,
                         "What is this book about? Circle one.",
                         ["apples", "juice"])
    _choice_question_row(pdf, 246, 64,
                         "What can we drink? Circle one.",
                         ["apple juice", "milk"])
    _choice_question_row(pdf, 172, 64,
                         "What does sweet mean? Circle one.",
                         ["tastes sugary", "tastes sour"])
    _remember_box(pdf, 96, 68, [
        "Apples are good to eat.",
        "We drink apple juice because it tastes sweet."])
    _adult_line(pdf, "Point to the apple slices. Ask: What "
                     "can we drink?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Same and Different
# ---------------------------------------------------------------------------
SORT_FACTS = [
    "Apples are a fruit.",
    "Some apples are red.",
    "Apples grow on trees.",
    # Full original wording, wrapped onto two lines: the
    # full sentence is 304.9pt at 13pt, over the 249.3pt
    # available before the pills, so it cannot fit on one
    # line. The wrap matches how Book A splits the same
    # sentence in the reference panel.
    ["Farmers pick the apples in fall",
     "because they are ripe."],
    "Apples are good to eat.",
    # Full original wording, wrapped onto two lines: the
    # full sentence is 259.4pt, 10.1pt over the 249.3pt
    # available, so it cannot fit on one line either. The
    # wrap matches how Book B splits the same sentence in
    # the reference panel.
    ["We drink apple juice because",
     "it tastes sweet."],
]
SORT_PILLS = ["Both Books", "Only A", "Only B"]


def _sort_rows(pdf, y, h):
    """Six fact rows inside one panel: the fact on the
    left, three choice pills right-aligned. The child
    circles one pill per fact. A fact may be a string
    (one line) or a list of two lines; a two-line fact is
    centred on its row's pills, and the 38pt row pitch
    leaves a clear gap to the rows above and below. y is
    the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    total_w = sum(stringWidth(w, "Helvetica-Bold", 13) + 22
                  for w in SORT_PILLS) + 10 * (len(SORT_PILLS) - 1)
    px = 556 - total_w
    pill_y = y + h - 34
    for fact in SORT_FACTS:
        lines = fact if isinstance(fact, list) else [fact]
        for line in lines:
            _fit(line, "Helvetica", 13, px - 56 - 8,
                 "sort fact")
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 13)
        if len(lines) == 1:
            pdf.drawString(56, pill_y + 8, lines[0])
        else:
            pdf.drawString(56, pill_y + 17, lines[0])
            pdf.drawString(56, pill_y + 1, lines[1])
        _word_pills(pdf, px, pill_y, SORT_PILLS, size=13)
        pill_y -= 38


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Same and Different", "Two books, one topic.",
        "Read both books. For each fact, circle where it "
        "goes.")
    _reference_panel(pdf, 452, 140)
    _sort_rows(pdf, 204, 240)
    _remember_box(pdf, 118, 68, [
        "Two books can tell about one topic.",
        "Some facts are the same. Some facts are new."],
        width=372)
    _draw_image(pdf, os.path.join(IMG_DIR, "p3-two-books.jpg"),
                492, 152, 130, 87)
    _adult_line(pdf, "Ask: Is this fact in both books, or "
                     "only in one?")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Why Does the Author Say So?
# ---------------------------------------------------------------------------
def _match_row(pdf, y, h, image, question, choices):
    """One point-to-reason row: a small picture on the left,
    the point ending in "because" above two reason pills.
    The child circles the reason the book gives. y is the
    bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, image, 100, y + 35, 90, 60)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(160, y + 50, question)
    _word_pills(pdf, 160, y + 10, choices, size=13)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Why Does the Author Say So?",
        "Each book tells why.",
        "Read both books. Match each point to its reason.")
    _reference_panel(pdf, 452, 140)
    _match_row(
        pdf, 374, 70,
        os.path.join(IMG_DIR, "p4-farmer-picking.jpg"),
        "Farmers pick the apples because",
        ["they are ripe", "it tastes sweet"])
    _match_row(
        pdf, 296, 70,
        os.path.join(IMG_DIR, "p2-apple-slices-juice.jpg"),
        "We drink apple juice because",
        ["they are ripe", "it tastes sweet"])
    _choice_question_row(
        pdf, 234, 54,
        "Which book tells why farmers pick the apples?",
        ["Book A", "Book B"])
    _choice_question_row(
        pdf, 172, 54,
        "Which book tells why we drink apple juice?",
        ["Book A", "Book B"])
    _remember_box(pdf, 96, 68, [
        "Farmers pick the apples because they are ripe.",
        "We drink apple juice because it tastes sweet."])
    _adult_line(pdf, "Ask: Why do farmers pick the apples? "
                     "The book says they are ripe.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- My Two-Book Page
# ---------------------------------------------------------------------------
def _fact_space(pdf, y, h, label):
    """One generous drawing and writing space: a teal label
    at the top and ONE ruled writing line at the bottom,
    with open room to draw in between. The single line
    leaves about 57pt of drawing room in a 100pt box
    (label bottom to line), nearly double the 34pt the
    two-line layout left. y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    _fit(label, "Helvetica-Bold", 13, 500, "fact space label")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 22, label)
    pdf.setStrokeColor(HexColor("#B9CBD6"))
    pdf.setLineWidth(0.6)
    pdf.line(56, y + 18, 556, y + 18)


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
    for line in ("I used a fact from Book A.",
                 "I used a fact from Book B.",
                 "I told what is the same."):
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
        pdf, "My Two-Book Page", "Tell what you learned.",
        "Use both books. Draw or write three facts.")
    _reference_panel(pdf, 452, 140)
    # Enlarged boxes, 100pt each (was 95pt): the
    # self-check is compacted to 68pt (was 80pt) and the
    # gaps tightened to 6-8pt, so the three boxes gain
    # 5pt each. The bigger gain is inside each box: one
    # writing line at the bottom leaves about 57pt of
    # drawing room, nearly double the old 34pt.
    _fact_space(pdf, 344, 100, "One fact only in Book A")
    _fact_space(pdf, 238, 100, "One fact only in Book B")
    _fact_space(pdf, 132, 100, "The same in both books")
    _self_check(pdf, 56, 68)
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
GUIDE_INTRO = ("This pack teaches your child to compare two "
               "books about one topic. Your child will read "
               "both books about apples, find what is the same "
               "and what is new, and listen for the reason the "
               "author gives.")
GUIDE_SECTIONS = [
    ("How to help", [
        "Page 1: Read Book A together. Point to the apple "
        "tree. Ask: Where do apples grow?",
        "Page 2: Read Book B together. Point to the apple "
        "slices and the juice. Ask: What can we drink?",
        "Page 3: Read both books again. Ask: Is this fact in "
        "both books, or only in one?",
        "Page 4: Match each point to its reason. Ask: Why do "
        "farmers pick the apples? The book says they are "
        "ripe.",
        "Page 5: Let your child draw or write independently. "
        "Ask your child to tell what they learned.",
    ]),
    ("What your child learns", [
        "Your child learns to read two books about one topic, "
        "find what is the same and what is new, listen for "
        "the reason the author gives, and work out a hard "
        "word from the words and picture near it.",
    ]),
    ("Answers", [
        ("Page 1", "apples; trees; ready to pick."),
        ("Page 2", "apples; apple juice; tastes sugary."),
        ("Page 3", "Both Books: Apples are a fruit; Some "
                   "apples are red. Only Book A: Apples grow "
                   "on trees; Farmers pick the apples in fall "
                   "because they are ripe. Only Book B: Apples "
                   "are good to eat; We drink apple juice "
                   "because it tastes sweet."),
        ("Page 4", "Farmers pick the apples because they are "
                   "ripe (Book A). We drink apple juice "
                   "because it tastes sweet (Book B)."),
        ("Page 5", "One fact only in Book A, one fact only "
                   "in Book B, and the same in both books. "
                   "Check all three boxes."),
    ]),
    ("Help your child compare books", [
        "Read two books about one thing at home. Ask: What "
        "is the same?",
        "Ask: What is new in this book?",
        "Ask: Why does the author say that? Point to the "
        "reason in the book.",
        "Ask your child to tell what they learned, in their "
        "own words.",
    ]),
    ("If your child finds it hard", [
        "Page 3: Cover Book B. Find the fact in Book A. "
        "Then uncover Book B and check if the fact is there "
        "too.",
        "Page 4: Read the reason sentence aloud and ask: "
        "Which words tell why?",
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
        "Grade 1 Reading: Two Books, One Topic. "
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
    bundle = os.path.join(OUT_DIR, "two-books-one-topic.pdf")
    guide = os.path.join(
        OUT_DIR, "two-books-one-topic-parent-guide.pdf")
    review = os.path.join(
        OUT_DIR, "two-books-one-topic-review.pdf")
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
    page_names = ["meet-book-a", "meet-book-b",
                  "same-and-different",
                  "why-does-the-author-say-so",
                  "my-two-book-page"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR, "two-books-one-topic-p%d-%s.pdf"
            % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    for name in ["two-books-one-topic.pdf",
                 "two-books-one-topic-parent-guide.pdf",
                 "two-books-one-topic-review.pdf",
                 "two-books-one-topic-p1-meet-book-a.pdf",
                 "two-books-one-topic-p2-meet-book-b.pdf",
                 "two-books-one-topic-p3-same-and-different.pdf",
                 "two-books-one-topic-p4-why-does-the-author-say-so.pdf",
                 "two-books-one-topic-p5-my-two-book-page.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text, no
    # standards codes on student pages or the Parent Guide,
    # and no first/third person language.
    for name in ["two-books-one-topic.pdf",
                 "two-books-one-topic-parent-guide.pdf"]:
        text = " ".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        norm = " ".join(text.split())
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
        assert "RI.1" not in norm, \
            "standards code in %s" % name
        assert "first person" not in norm.lower(), \
            "first person in %s" % name
        assert "third person" not in norm.lower(), \
            "third person in %s" % name
    print("text checks: clean")
    # The "For adults" guidance lives on the website
    # resource page, not in the Parent Guide. Confirm the
    # guide carries its own "What your child learns"
    # paraphrase instead of the guidance text.
    guide_text = " ".join(
        (p.extract_text() or "")
        for p in PdfReader(guide).pages)
    guide_norm = " ".join(guide_text.split())
    assert "Help your child read both books about apples" \
        not in guide_norm, "For adults text leaked into guide"
    print("guide check: clean")


if __name__ == "__main__":
    main()
