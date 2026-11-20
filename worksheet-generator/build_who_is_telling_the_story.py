#!/usr/bin/env python3
"""Grade 1 Reading - Who Is Telling the Story?

Resource 19 in the approved and locked Grade 1 Reading and
Language Arts roadmap (audit 2026-11-05). Plan approved
2026-11-19 with the user's refinements, and approved for
building 2026-11-19 with one final teaching refinement:

The reliable clue is the narrator's own words. Words
like I, my, we, and our can help identify a character
telling the story. He and she may appear in either kind
of narration (Page 3's own story says "She is small and
wet" about the kitten, yet Lily tells it), so they do
not decide who tells it. The child is encouraged to ask:
"Who is telling us what happened?" On Pages 4 and 5 the
child uses the narrator's words as evidence and
underlines them. The pack never teaches a missing I or
my as proof of an outside narrator, and never uses the
terms for the two kinds of narration as taught language.

Placement: Grade 1 / Reading & Language / Reading
Comprehension. Standard RL.1.6 (identify who is telling
the story at various points in a text); RL.1.10 is a
level condition only. RL.1.5 and RL.1.9 are NOT claimed
here; they are recorded as separate curriculum gaps for
the later reading audit.

Boundaries: Resource 13 Meet the Characters asks who
is in the story and what they are like; this pack asks
who tells the story, a different question, and uses two
new characters (Lily and Noah), not Maya and Theo.
Resource 4 Read and Think asks for key details, causes,
sequences, and retellings; this pack does none of those.
Kindergarten Story Elements teaches characters, setting,
and events by listening; this pack teaches narrator
voice in print. Resource 22 owns pronouns as grammar;
this pack uses I, my, we, and our only as reading clues
for who tells the story.

Characters: Lily (girl with dark hair in a ponytail,
teal dress) and Noah (boy with short dark hair, yellow
shirt, blue shorts), plus Zoe (girl with dark curly
hair, red coat) and Spot (a brown dog) on Page 5.

Illustrations: nine new original watercolor storybook
JPEGs in the approved style from Resources 16, 17, and
18 (p1-lily-ball, p1-noah-kite, p2-kite-tree,
p2-dog-run, p3-kitten, p4-kite-a, p4-kite-b,
p5-lily-spot, p5-zoe-snowman), all embedded with
_draw_image. JPEGs embed as DCT, so the PDF stays
small. Page 4 shows the same kite-in-a-tree scene in
both pictures, so only the telling changes. Page 5 uses
two distinct story situations, so the child must read
the words rather than match the pictures.

Shared design code (logo, header, footer) is imported
verbatim from build_phonics_az.py. Do not fork it here.
Header title is drawn at 18pt and the subtitle at 14pt;
both end inside the teal rule (measured: title 216pt,
subtitle 291pt, against 318pt available).
"""
import hashlib
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter as _letter  # noqa: F401
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from build_phonics_az import (NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              draw_footer, draw_header, draw_logo)

TITLE = "Who Is Telling the Story?"
SUBTITLE = "Grade 1 Reading | Who Is Telling the Story?"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "who-is-telling-the-story")
IMG_DIR = OUT_DIR  # watercolor illustration JPEGs live beside the PDFs


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
        _fit(line, "Helvetica", 12.5, 500, "Remember line")
        pdf.drawCentredString(PAGE_WIDTH / 2, ly, line)
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


# ---------------------------------------------------------------------------
# Page 1 -- Who Is Speaking?
# ---------------------------------------------------------------------------
def _example_section(pdf, y, h, label, image, sentence, pills):
    """One example on Page 1: picture on the left, a
    labelled sentence, the question, and two choice pills
    on the right. y is the bottom of the panel."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, image, 150, y + h / 2, 210, 140)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(280, y + h - 30, label)
    _fit(sentence, "Helvetica", 14, 260, "example sentence")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 14)
    pdf.drawString(302, y + h - 30, sentence)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(280, y + h - 72, "Who tells it? Circle one.")
    _word_pills(pdf, 280, y + h - 122, pills, size=13)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Who Is Speaking?", None,
        ["Every story has someone who tells it.",
         "Look at each picture. Who tells the story?"])
    _example_section(
        pdf, 412, 180, "A",
        os.path.join(IMG_DIR, "p1-lily-ball.jpg"),
        "I see a red ball in the park.",
        ["Lily", "someone outside the story"])
    _example_section(
        pdf, 222, 180, "B",
        os.path.join(IMG_DIR, "p1-noah-kite.jpg"),
        "Noah sees a red kite in the park.",
        ["Noah", "someone outside the story"])
    _remember_box(pdf, 118, 68, [
        "Words like I, my, we, and our can tell you a "
        "character tells the story.",
        "He and she can be in any story. Ask: Who is "
        "telling us what happened?"])
    _adult_line(pdf, "Point to the word I in A. In B, the "
                     "story says Noah, so someone outside "
                     "tells it.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- I or Someone Else?
# ---------------------------------------------------------------------------
def _clue_pair(pdf, y, h, image, rows):
    """One pair of clue rows on Page 2: one picture on the
    left, two sentence rows on the right. Each row has a
    sentence and two choice pills. y is the bottom of
    the panel. rows is a list of (sentence, choices)."""
    _panel(pdf, 40, y, 532, h)
    _draw_image(pdf, image, 150, y + h / 2, 200, 133)
    ry = y + h - 40
    for sentence, choices in rows:
        _fit(sentence, "Helvetica", 13, 292, "clue sentence")
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 13)
        pdf.drawString(280, ry, sentence)
        _word_pills(pdf, 280, ry - 42, choices, size=13)
        ry -= 78


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "I or Someone Else?",
        "Look for the words that tell you.",
        "Read each sentence. Circle I or my if you see it. "
        "Then circle who tells the story.")
    _clue_pair(
        pdf, 392, 200,
        os.path.join(IMG_DIR, "p2-kite-tree.jpg"),
        [("I see a red kite in the tree.",
          ["a character", "someone outside"]),
         ("She sees a red kite in the tree.",
          ["a character", "someone outside"])])
    _clue_pair(
        pdf, 182, 200,
        os.path.join(IMG_DIR, "p2-dog-run.jpg"),
        [("My dog runs fast in the park.",
          ["a character", "someone outside"]),
         ("He runs fast in the park.",
          ["a character", "someone outside"])])
    _remember_box(pdf, 104, 68, [
        "Words like I, my, we, and our can tell you a "
        "character tells the story.",
        "He and she can be in any story."])
    _adult_line(pdf, "Ask: Who is telling us what happened? "
                     "Look for the words I, my, we, and our.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- The Character Tells It
# ---------------------------------------------------------------------------
def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "The Character Tells It",
        "A character tells this story.",
        "Read the story. Who tells it? Circle the word "
        "that tells you.")
    # Story panel: the kitten picture on the left, the
    # five-line story on the right.
    _panel(pdf, 40, 392, 532, 200)
    _draw_image(pdf, os.path.join(IMG_DIR, "p3-kitten.jpg"),
                150, 492, 200, 133)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(280, 566, "My Kitten")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 14)
    for text, y in (("I see a kitten in the rain.", 544),
                    ("She is small and wet.", 522),
                    ("I pick her up.", 500),
                    ("I take her home.", 478),
                    ("She naps in my lap.", 456)):
        _fit(text, "Helvetica", 14, 292, "story line")
        pdf.drawString(280, y, text)
    _choice_question_row(pdf, 318, 64,
                         "Who tells this story? Circle one.",
                         ["Lily", "someone outside the story"])
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 296,
                          "Circle the word that tells you.")
    _choice_question_row(pdf, 214, 64,
                         "What did Lily find? Circle one.",
                         ["a kitten", "a ball"])
    _remember_box(pdf, 118, 68, [
        "Words like I, my, we, and our can tell you a "
        "character tells the story.",
        "Ask: Who is telling us what happened?"])
    _adult_line(pdf, "Ask: Who is telling us what happened? "
                     "Lily says I.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Same Event, Different Voice
# ---------------------------------------------------------------------------
def _version_section(pdf, y, h, title, lines, image, img_w,
                     img_h, question, pills):
    """One version on Page 4: title and four story lines on
    the left, illustration on the right, and the question
    with two choice pills below the story. y is the
    bottom of the section."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + h - 24, title)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 14)
    ly = y + h - 46
    for line in lines:
        _fit(line, "Helvetica", 14, 300, "version line")
        pdf.drawString(56, ly, line)
        ly -= 19
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + 48, question)
    _word_pills(pdf, 56, y + 14, pills, size=13)
    _draw_image(pdf, image, 470, y + h / 2, img_w, img_h)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Same Event, Different Voice",
        "The same event, told two ways.",
        ["Read both stories. They tell the same thing. Who "
         "tells each one?",
         "Underline the words that tell you who tells it."])
    _version_section(
        pdf, 394, 180, "Version A",
        ["I see my kite in a tree.",
         "I run to get my dad.",
         "Dad gets the kite down.",
         "I hold it fast."],
        os.path.join(IMG_DIR, "p4-kite-a.jpg"), 140, 160,
        "Who tells Version A? Circle one.",
        ["Noah", "someone outside the story"])
    _version_section(
        pdf, 204, 180, "Version B",
        ["Noah sees his kite in a tree.",
         "He runs to get his dad.",
         "Dad gets the kite down.",
         "Noah holds it fast."],
        os.path.join(IMG_DIR, "p4-kite-b.jpg"), 200, 133,
        "Who tells Version B? Circle one.",
        ["Noah", "someone outside the story"])
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(56, 180, "Do they tell the same thing? "
                             "Circle one.")
    total_w = sum(stringWidth(w, "Helvetica-Bold", 13) + 22
                  for w in ["yes", "no"]) + 10
    _word_pills(pdf, 556 - total_w, 168, ["yes", "no"],
                size=13)
    _remember_box(pdf, 88, 68, [
        "The same thing can be told in two ways. Use the "
        "words as clues.",
        "Ask: Who is telling us what happened?"])
    _adult_line(pdf, "Underline I and my in A, and Noah, he, "
                     "and his in B.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Who Tells This Story?
# ---------------------------------------------------------------------------
def _passage_section(pdf, y, h, label, lines, image, pills):
    """One passage on Page 5: a teal bold label (A or B) and
    four story lines on the left, illustration on the
    right, the question with two choice pills below, and
    the underline direction at the bottom. The label sits
    on the first line's baseline, in the same style as
    the A and B labels on Page 1, and the first line
    starts 22pt to its right. y is the bottom of the
    section."""
    _panel(pdf, 40, y, 532, h)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(56, y + h - 26, label)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 14)
    ly = y + h - 26
    for i, line in enumerate(lines):
        _fit(line, "Helvetica", 14, 278 if i == 0 else 300,
             "passage line")
        pdf.drawString(78 if i == 0 else 56, ly, line)
        ly -= 22
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, y + 70, "Who tells this story? "
                                "Circle one.")
    _word_pills(pdf, 56, y + 28, pills, size=13)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawString(56, y + 12, "Underline the words that "
                                "tell you.")
    _draw_image(pdf, image, 470, y + h / 2, 200, 133)


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _page_title(
        pdf, "Who Tells This Story?",
        "Read and find who tells it.",
        "Read each story. Who tells it? Underline the words "
        "that tell you.")
    _passage_section(
        pdf, 392, 200, "A",
        ["I have a dog named Spot.",
         "Spot runs fast in the park.",
         "I throw a red ball.",
         "Spot brings it back to me."],
        os.path.join(IMG_DIR, "p5-lily-spot.jpg"),
        ["Lily", "someone outside the story"])
    _passage_section(
        pdf, 182, 200, "B",
        ["Zoe rolls a big snowball.",
         "She puts a red hat on top.",
         "She gives it a red nose.",
         "The snowman smiles in the sun."],
        os.path.join(IMG_DIR, "p5-zoe-snowman.jpg"),
        ["Zoe", "someone outside the story"])
    _remember_box(pdf, 104, 68, [
        "Words like I, my, we, and our can tell you a "
        "character tells it.",
        "Use the words as clues. Ask: Who is telling us "
        "what happened?"])
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
GUIDE_INTRO = ("This pack teaches your child to find who tells "
               "a story. Your child will look for the words I, "
               "my, we, and our, and ask: Who is telling us "
               "what happened?")
GUIDE_SECTIONS = [
    ("How to help", [
        "Page 1: Read both examples. Point to I in A. In B, "
        "point out the story says Noah.",
        "Page 2: Ask: Who is telling us what happened? In "
        "these sentences, I and my are clues that a "
        "character tells the story.",
        "Page 3: Read the kitten story. Ask who says I. "
        "Note: She is the kitten, not the one who tells it.",
        "Page 4: Read both kite stories. Underline I and my "
        "in A, and Noah, he, and his in B.",
        "Page 5: Let your child read both stories alone. Ask "
        "who tells each one and which words tell them.",
    ]),
    ("What your child learns", [
        "Your child learns to find who tells a story. Words "
        "like I, my, we, and our can help show that a "
        "character in the story tells it. He and she can be "
        "in any story. Encourage your child to ask: Who is "
        "telling us what happened? Then look at the words "
        "for clues.",
    ]),
    ("Answers", [
        ("Page 1", "A: Lily (clue: I). B: someone outside the "
                   "story (clue: the story says Noah)."),
        ("Page 2", "Row 1: I, a character. Row 2: no I or my "
                   "in this sentence, someone outside. Row 3: "
                   "My, a character. Row 4: no I or my in this "
                   "sentence, someone outside."),
        ("Page 3", "Lily tells it. Clue word: I. Lily found a "
                   "kitten. (She is the kitten.)"),
        ("Page 4", "Version A: Noah. Version B: someone "
                   "outside the story. Underline: A: I, my. "
                   "B: Noah, he, his. Same thing: yes."),
        ("Page 5", "Passage A: Lily tells it. Underline: I "
                   "(and me, if spotted). Passage B: someone "
                   "outside tells it. Underline: Zoe, She."),
    ]),
    ("Help your child tell a story", [
        "Ask your child to tell you about their day, "
        "starting with I.",
        "Tell the same small event twice: once starting with "
        "I, once starting with your child's name. Ask which "
        "one is your child telling.",
        "When you read a story together, pause and ask: does "
        "it say I or my? Who tells it?",
    ]),
    ("If your child finds it hard", [
        "Page 2: If your child circles he or she as the "
        "clue, remind them: he and she can be in any story. "
        "Ask: Who is telling us what happened? In these "
        "sentences, I and my are the clues.",
        "Page 4: If your child is unsure, read Version A "
        "aloud. Ask: who says I? That is Noah telling it.",
        "Page 5: If your child matches the pictures instead "
        "of reading, cover the pictures and read the words "
        "first. The two stories are about different things.",
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
        "Grade 1 Reading: Who Is Telling the Story? "
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
    bundle = os.path.join(OUT_DIR, "who-is-telling-the-story.pdf")
    guide = os.path.join(
        OUT_DIR, "who-is-telling-the-story-parent-guide.pdf")
    review = os.path.join(
        OUT_DIR, "who-is-telling-the-story-review.pdf")
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
    page_names = ["who-is-speaking", "i-or-someone-else",
                  "the-character-tells-it",
                  "same-event-different-voice",
                  "who-tells-this-story"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR, "who-is-telling-the-story-p%d-%s.pdf"
            % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    for name in ["who-is-telling-the-story.pdf",
                 "who-is-telling-the-story-parent-guide.pdf",
                 "who-is-telling-the-story-review.pdf",
                 "who-is-telling-the-story-p1-who-is-speaking.pdf",
                 "who-is-telling-the-story-p2-i-or-someone-else.pdf",
                 "who-is-telling-the-story-p3-the-character-tells-it.pdf",
                 "who-is-telling-the-story-p4-same-event-different-voice.pdf",
                 "who-is-telling-the-story-p5-who-tells-this-story.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text.
    for name in ["who-is-telling-the-story.pdf",
                 "who-is-telling-the-story-parent-guide.pdf"]:
        text = "".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
    print("em dash check: clean")
    # The final teaching refinement: the pack must never
    # teach a missing I or my as proof of an outside
    # narrator, and must never use the terms for the two
    # kinds of narration as taught language.
    forbidden = "if there is no i or my, someone outside tells it"
    for name in ["who-is-telling-the-story.pdf",
                 "who-is-telling-the-story-parent-guide.pdf"]:
        text = " ".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        norm = " ".join(text.lower().split())
        assert forbidden not in norm, \
            "forbidden rule in %s" % name
        assert "first person" not in norm, \
            "first person in %s" % name
        assert "third person" not in norm, \
            "third person in %s" % name
    print("teaching refinement check: clean")


if __name__ == "__main__":
    main()
