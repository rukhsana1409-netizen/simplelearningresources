#!/usr/bin/env python3
"""Kindergarten Vocabulary & Oral Language -- One Word, Two
Meanings (Learning Made Simple).

DRAFT pack built under the free draft-review workflow
(worksheet-generator/REVIEW_WORKFLOW.md) on the isolated branch
muse/review/one-word-two-meanings. Nothing here is locked or
approved; pages exist for a consolidated review only.

Michigan L.K.4 / L.K.4a (paraphrased): children determine the
meaning of multiple-meaning words from context, identifying
new meanings for familiar words and applying them accurately
(the standard's own example: duck the bird and the verb to
duck). A repo-wide audit (2026-10-19) found this genuinely
untaught: no existing page treats any word as having two
meanings; Categories (L.K.5a), Opposites (L.K.5b), Animals &
Their World, and Describe It! (attributes) all use one word
with one meaning.

Oral-first design: the child speaks; the adult writes the
child's exact words on the scribe lines. Word set chosen so
BOTH meanings are familiar and each shows in one unambiguous
scene: DUCK (bird / bend down), BAT (animal / baseball bat),
BARK (dog's sound / tree covering), WAVE (saying hello / sea
wave). Progression: P1 teach DUCK with spoken models -> P2
supported practice with BAT and BARK -> P3 WAVE introduced,
plus listening questions where context decides the meaning ->
P4 independent: choose a taught word, draw both meanings, and
say a sentence for each.

Shared design code (logo, header, footer, circular pictures)
is imported verbatim from build_phonics_az.py.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageOps
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from build_phonics_az import (_ASSETS as ASSETS, INK, NAVY, PAGE_HEIGHT,
                              PAGE_WIDTH, TEAL, _img_circle, draw_footer,
                              draw_header)

ADULT = HexColor("#37474F")
RULE = HexColor("#9DB8C4")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_LINE = HexColor("#D9E7E7")

DUCK_BIRD = "animal-library/lib-duck.jpg"
DUCK_DOWN = "one-word-two-meanings/mm-duck-down.jpg"
BAT_ANIMAL = "one-word-two-meanings/mm-bat-animal.jpg"
BAT_BALL = "one-word-two-meanings/mm-bat-baseball.jpg"
BARK_DOG = "one-word-two-meanings/mm-dog-bark.jpg"
BARK_TREE = "one-word-two-meanings/mm-bark-tree.jpg"
WAVE_HAND = "one-word-two-meanings/mm-wave-hand.jpg"
WAVE_SEA = "one-word-two-meanings/mm-wave-ocean.jpg"

_fit_cache = {}


def _framed(pdf, name, x, y, w, h, focus=(0.5, 0.5)):
    """Draw an artwork file center-cropped (PIL fit) into a
    rectangle, with a soft rounded outline."""
    path = name if os.path.isabs(name) else os.path.join(ASSETS, name)
    key = (path, int(w * 3), int(h * 3), focus)
    if key not in _fit_cache:
        img = Image.open(path).convert("RGB")
        _fit_cache[key] = ImageOps.fit(img, (key[1], key[2]),
                                       centering=focus)
    pdf.saveState()
    clip = pdf.beginPath()
    clip.roundRect(x, y, w, h, 12)
    pdf.clipPath(clip, stroke=0, fill=0)
    pdf.drawImage(ImageReader(_fit_cache[key]), x, y, w, h)
    pdf.restoreState()
    pdf.setStrokeColor(PANEL_LINE)
    pdf.setLineWidth(1.2)
    pdf.roundRect(x, y, w, h, 12, stroke=1, fill=0)


def _scribe(pdf, x, y, width, rows=1):
    """Plain ruled lines for the ADULT to write the child's
    spoken words (not child handwriting guides)."""
    for i in range(rows):
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(1.1)
        pdf.line(x, y - i * 36, x + width, y - i * 36)


def _instruction(pdf, text, y=616):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, y, text)


def _adult(pdf, lines, top=92):
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    for i, line in enumerate(lines):
        pdf.drawCentredString(PAGE_WIDTH / 2, top - i * 18, line)


def _caption(pdf, cx, y, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(cx, y, text)


def _say_label(pdf, x, y):
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(x, y, "Say a sentence:")


def _word_banner(pdf, word, y=552):
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_LINE)
    pdf.setLineWidth(1)
    pdf.roundRect(196, y, 220, 42, 12, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 24)
    pdf.drawCentredString(PAGE_WIDTH / 2, y + 12, word)


def _word_chip(pdf, x, y, word, w=92, h=44):
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_LINE)
    pdf.setLineWidth(1)
    pdf.roundRect(x, y, w, h, 12, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 17)
    pdf.drawCentredString(x + w / 2, y + h / 2 - 6, word)


def _num_badge(pdf, cx, cy, n):
    pdf.setFillColor(NAVY)
    pdf.circle(cx, cy, 10, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(cx, cy - 4, str(n))


# ---------------------------------------------------------------------------
# Page 1 -- Duck: Two Meanings (DRAFT)
# The teaching page. One word, DUCK, in two large scenes: the
# bird (the meaning children already know) and a child ducking
# under a low branch (the new verb meaning -- the Michigan
# standard's own example). Model sentences are spoken by the
# adult (in the adult line), never printed for the child to
# read; the child says a sentence for each picture and the
# adult scribes it.
# ---------------------------------------------------------------------------
def _duck_two_meanings(pdf):
    _instruction(pdf, "One word can have two meanings!")
    _word_banner(pdf, "DUCK")
    _framed(pdf, DUCK_BIRD, 40, 318, 252, 218)
    _framed(pdf, DUCK_DOWN, 320, 318, 252, 218)
    _caption(pdf, 166, 294, "DUCK \u2014 the bird")
    _caption(pdf, 446, 294, "DUCK \u2014 bend down")
    _say_label(pdf, 40, 262)
    _say_label(pdf, 320, 262)
    _scribe(pdf, 40, 236, 252)
    _scribe(pdf, 320, 236, 252)
    _adult(pdf, [
        "Adult: Say the model sentences: \u201cThe duck has a "
        "green head.\u201d \u201cDuck down! The branch is low.\u201d",
        "Then let your child say a sentence for each picture. "
        "Write the words they say.",
    ])


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "One Word, Two Meanings", "Duck \u2014 Two Meanings")
    _duck_two_meanings(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Say It Two Ways (DRAFT)
# Supported practice with two new words, BAT and BARK. Each
# word gets its two scenes side by side, numbered 1 and 2;
# the child says a sentence for each picture, and the adult
# scribes them on the matching numbered lines under the pair.
# ---------------------------------------------------------------------------
def _word_block(pdf, chip_y, frame_y, word, art1, cap1, art2, cap2,
                focus2=(0.5, 0.5)):
    _word_chip(pdf, 36, chip_y, word)
    _framed(pdf, art1, 146, frame_y, 150, 140)
    _framed(pdf, art2, 322, frame_y, 150, 140, focus=focus2)
    _num_badge(pdf, 158, frame_y + 128, 1)
    _num_badge(pdf, 334, frame_y + 128, 2)
    _caption(pdf, 221, frame_y - 18, cap1)
    _caption(pdf, 397, frame_y - 18, cap2)
    for i, line_y in enumerate((frame_y - 48, frame_y - 84)):
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(146, line_y - 4, f"{i + 1}.")
        _scribe(pdf, 164, line_y, 308)


def _say_it_two_ways(pdf):
    _instruction(pdf, "Say a sentence for each picture!")
    _word_block(pdf, 458, 452, "BAT", BAT_ANIMAL, "the animal",
                BAT_BALL, "the baseball bat", focus2=(0.5, 0.30))
    _word_block(pdf, 210, 204, "BARK", BARK_DOG, "the dog's sound",
                BARK_TREE, "on the tree")
    _adult(pdf, [
        "Adult: Models \u2014 \u201cA bat flies at night.\u201d "
        "\u201cI hit the ball with the bat.\u201d",
        "\u201cThe dog can bark.\u201d \u201cThe bark on the "
        "tree is rough.\u201d Write your child's sentences.",
    ])


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "One Word, Two Meanings", "Say It Two Ways")
    _say_it_two_ways(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Which Meaning? (DRAFT)
# WAVE is introduced the same supported way (two scenes, say
# a sentence for each). Below, three spacious listening rows:
# the adult reads a sentence aloud (scripts and answers in
# the adult line); the child circles the picture the sentence
# means. Context -- not the picture alone -- decides.
# Answers: Q1 duck down, Q2 the bat animal, Q3 the tree bark.
# ---------------------------------------------------------------------------
def _listen_row(pdf, cy, n, art_left, art_right):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(52, cy - 6, f"{n}.")
    _img_circle(pdf, art_left, 190, cy, 33)
    _img_circle(pdf, art_right, 330, cy, 33)


def _which_meaning(pdf):
    _instruction(pdf, "A new word \u2014 WAVE. Say a sentence for each!")
    _img_circle(pdf, WAVE_HAND, 166, 520, 58, zoom=True)
    _img_circle(pdf, WAVE_SEA, 446, 520, 58, zoom=True)
    _caption(pdf, 166, 442, "WAVE \u2014 say hello")
    _caption(pdf, 446, 442, "WAVE \u2014 in the sea")
    _scribe(pdf, 40, 412, 252)
    _scribe(pdf, 320, 412, 252)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 388,
                          "Listen! Circle the picture the sentence means.")
    _listen_row(pdf, 330, 1, DUCK_BIRD, DUCK_DOWN)
    _listen_row(pdf, 254, 2, BAT_ANIMAL, BAT_BALL)
    _listen_row(pdf, 178, 3, BARK_DOG, BARK_TREE)
    _adult(pdf, [
        "Adult: WAVE models: \u201cI wave to my friend.\u201d "
        "\u201cA big wave splashed!\u201d Then read aloud:",
        "1. \u201cThe girl had to duck under the low branch.\u201d "
        "2. \u201cA bat flew over our house last night.\u201d",
        "3. \u201cThe bark on the big tree is rough.\u201d "
        "Answers: 1 duck down, 2 the animal, 3 the tree.",
    ], top=110)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "One Word, Two Meanings", "Which Meaning?")
    _which_meaning(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- My Two Meanings (DRAFT)
# Independent application. The child chooses one TAUGHT word
# from the reminder chips, draws BOTH of its meanings in the
# two big boxes, and says a sentence for each drawing; the
# adult scribes. Drawing support is explicitly allowed --
# the sentences are the goal.
# ---------------------------------------------------------------------------
def _my_two_meanings(pdf):
    _instruction(pdf, "Pick one word. Draw both meanings. "
                      "Say a sentence for each!")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawString(40, 584, "Circle your word:")
    for i, word in enumerate(("DUCK", "BAT", "BARK", "WAVE")):
        _word_chip(pdf, 40 + i * 138, 538, word, w=118, h=34)
    for x, label in ((40, "One meaning"), (320, "The other meaning")):
        pdf.setStrokeColor(PANEL_LINE)
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, 300, 252, 214, 12, stroke=1, fill=0)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(x + 16, 486, label)
    _say_label(pdf, 40, 268)
    _say_label(pdf, 320, 268)
    _scribe(pdf, 40, 240, 252)
    _scribe(pdf, 320, 240, 252)
    _adult(pdf, [
        "Adult: Write the exact words your child says \u2014 "
        "one sentence for each drawing.",
        "Drawing help is fine: start a shape together, or copy "
        "an earlier picture. Sentences are the goal.",
    ])


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "One Word, Two Meanings", "My Two Meanings")
    _my_two_meanings(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [build_p1_page, build_p2_page, build_p3_page, build_p4_page]
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "worksheets", "kindergarten", "reading",
                       "one-word-two-meanings")
PACK = "one-word-two-meanings"


def build_pack():
    from pypdf import PdfReader, PdfWriter
    os.makedirs(OUT_DIR, exist_ok=True)
    writer = PdfWriter()
    for i, build in enumerate(PAGES, start=1):
        page_path = os.path.join(OUT_DIR, f"{PACK}-page-{i:02d}.pdf")
        build(page_path)
        writer.append(PdfReader(page_path))
    with open(os.path.join(OUT_DIR, f"{PACK}-review.pdf"), "wb") as fh:
        writer.write(fh)
    print(f"pack built in {OUT_DIR}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "build"
    if mode == "preview":
        tmp = tempfile.mkdtemp()
        for i, build in enumerate(PAGES, start=1):
            page_pdf = os.path.join(tmp, f"p{i}.pdf")
            build(page_pdf)
            out = f"/tmp/owtm-p{i}"
            subprocess.run(["pdftoppm", "-png", "-r", "150",
                            "-singlefile", page_pdf, out], check=True)
            print(out + ".png")
    else:
        build_pack()
