#!/usr/bin/env python3
"""Kindergarten Vocabulary & Oral Language -- Describe It!
Words That Tell More (Learning Made Simple).

DRAFT pack built under the free draft-review workflow
(worksheet-generator/REVIEW_WORKFLOW.md) on the isolated branch
muse/review/describe-it. Nothing here is locked or approved;
pages exist for a consolidated review only.

Michigan SL.K.4 / SL.K.5 / SL.K.6 + L.K.5 / L.K.6 (paraphrased):
children describe familiar things and, with support, add detail;
a drawing can add detail to a description; children speak
clearly and use words they have learned. A page-by-page audit
(2026-10-19) found this genuinely untaught: existing resources
teach sorting (Categories, Sort Count & Compare), opposites
recognition (Opposites), and attribute-word recognition
(Exploring Materials) -- but no page has a child DESCRIBE an
object in spoken sentences with precise attributes.

Oral-first design: the child speaks; the adult writes the
child's exact words on the scribe lines. No picture matching,
no attribute circling, no written sentence completion.
Progression: P1 one sentence per describing lens for a teddy
bear -> P2 fuller multi-attribute descriptions of three varied
objects -> P3 describing with a communicative purpose (a
guessing game that needs precise words) -> P4 independent:
choose, draw, and describe your own thing.

Shared design code (logo, header, footer, circular pictures) is
imported verbatim from build_phonics_az.py.
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
GOLD = HexColor("#F4B63E")
RED = HexColor("#D64545")
BLUE = HexColor("#3E7CB1")

_fit_cache = {}


def _framed(pdf, name, x, y, w, h):
    """Draw an artwork file center-cropped (PIL fit) into a
    rectangle, with a soft rounded outline."""
    path = name if os.path.isabs(name) else os.path.join(ASSETS, name)
    key = (path, int(w * 3), int(h * 3))
    if key not in _fit_cache:
        img = Image.open(path).convert("RGB")
        _fit_cache[key] = ImageOps.fit(img, (key[1], key[2]))
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


def _lens_icon(pdf, kind, cx, cy):
    """Tiny geometric icons for the four describing lenses."""
    pdf.saveState()
    if kind == "COLOR":
        for dx, col in ((-8, RED), (0, GOLD), (8, BLUE)):
            pdf.setFillColor(col)
            pdf.circle(cx + dx, cy, 5, stroke=0, fill=1)
    elif kind == "SIZE":
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.6)
        pdf.rect(cx - 11, cy - 4, 8, 8, stroke=1, fill=0)
        pdf.rect(cx - 1, cy - 8, 13, 16, stroke=1, fill=0)
    elif kind == "FEEL":
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.6)
        p = pdf.beginPath()
        for i in range(25):
            import math
            px = cx - 12 + i
            py = cy + 4.5 * math.sin(i / 24 * 2 * math.pi)
            (p.moveTo if i == 0 else p.lineTo)(px, py)
        pdf.drawPath(p, stroke=1, fill=0)
    elif kind == "PART":
        pdf.setFillColor(GOLD)
        pdf.circle(cx, cy, 8, stroke=0, fill=1)
        pdf.setFillColor(PANEL_FILL)
        pdf.circle(cx + 7, cy + 7, 5.5, stroke=0, fill=1)
    pdf.restoreState()


def _lens_chip(pdf, x, y, kind, word, w=118):
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_LINE)
    pdf.setLineWidth(1)
    pdf.roundRect(x, y, w, 30, 10, stroke=1, fill=1)
    _lens_icon(pdf, kind, x + 20, y + 15)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 12.5)
    pdf.drawString(x + 36, y + 10, word)


LENSES = [("COLOR", "COLOR"), ("SIZE", "SIZE"), ("FEEL", "FEEL"),
          ("PART", "A PART")]


# ---------------------------------------------------------------------------
# Page 1 -- Words That Tell (DRAFT)
# The teaching page. A big teddy bear and four describing lenses,
# every one meaningful for THIS bear: COLOR (brown), SIZE (big),
# FEEL (soft), and A PART -- where shape is told through a part
# ("Its ears are round"). One spoken sentence per lens; the adult
# writes the child's exact words on the line beside each lens.
# ---------------------------------------------------------------------------
def _words_that_tell(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 616,
                          "Look at the teddy bear. Tell about it!")
    _framed(pdf, "living-nonliving/ln-teddy.jpg", 40, 330, 236, 264)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(158, 306, "Words that tell more:")
    rows = [("COLOR", 534), ("SIZE", 452), ("FEEL", 370),
            ("PART", 288)]
    for kind, top in rows:
        word = dict(LENSES)[kind] if kind != "PART" else "A PART"
        _lens_chip(pdf, 300, top, kind, word)
        _scribe(pdf, 300, top - 22, 272, rows=1)
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 92,
        "Adult: Ask about each telling word. Write the words "
        "your child says.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "For a part, your child might say: \u201cIts ears are "
        "round.\u201d")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Describe It!", "Words That Tell")
    _words_that_tell(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Tell Me More (DRAFT)
# Three varied objects chosen for DIFFERENT descriptive
# vocabulary: a banana (yellow, long, curved, smooth), a striped
# ball (round, red-and-white stripes, bouncy), a mug (blue, white
# dots, hard, a handle). The child combines two or more
# attributes per object in their own spoken sentences; the adult
# scribes on two lines per object. No lens chips -- only a small
# reminder that more telling is the goal.
# ---------------------------------------------------------------------------
def _object_row(pdf, cy, art, name, zoom=False):
    _img_circle(pdf, art, 96, cy, 42, zoom=zoom)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(96, cy - 56, name)
    _scribe(pdf, 168, cy + 8, 404, rows=2)


def _tell_me_more(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 616,
                          "Tell two things about each one!")
    _object_row(pdf, 520, "sort-count-compare/scc-banana.jpg",
                "BANANA")
    _object_row(pdf, 366, "living-nonliving/ln-ball.jpg", "BALL")
    _object_row(pdf, 212, "living-nonliving/ln-cup.jpg", "CUP")
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 92,
        "Adult: Write the words your child says. Help them put "
        "two telling")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "words into one sentence: \u201cIt is yellow and "
        "long.\u201d")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Describe It!", "Tell Me More")
    _tell_me_more(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Describe and Guess (DRAFT)
# Describing with a real purpose. Three balls that differ in
# SIZE, PATTERN, and COLOR (a big purple ball with white dots, a
# medium red-and-white striped ball, a small plain green ball),
# drawn at genuinely different sizes on one shelf line. The child
# secretly picks one and describes it; the listener must be able
# to point to the right ball from the words alone -- color alone
# is never the only difference. The adult records the child's
# describing words, then roles swap.
# ---------------------------------------------------------------------------
def _describe_and_guess(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 616,
                          "Pick one ball. Do not tell which one!")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 590,
                          "Describe it. Can your listener guess it?")
    _img_circle(pdf, "describe-it/di-ball-dots.jpg", 138, 486, 62)
    _img_circle(pdf, "living-nonliving/ln-ball.jpg", 306, 472, 48)
    _img_circle(pdf, "describe-it/di-ball-plain.jpg", 458, 458, 34,
                zoom=True)
    pdf.setStrokeColor(PANEL_LINE)
    pdf.setLineWidth(1.4)
    pdf.line(56, 422, 556, 422)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 386, "My describing words:")
    _scribe(pdf, 40, 356, 532, rows=3)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 218,
                          "Then switch! Your listener describes "
                          "one, and you guess.")
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 92,
        "Adult: Point to the ball your child describes. If you "
        "cannot tell,")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "ask for one more describing word.")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Describe It!", "Describe and Guess")
    _describe_and_guess(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- My Describing Page (DRAFT)
# Independent: the child chooses any thing, the adult records its
# name, the child draws it (the drawing itself adds detail to
# the description), and describes it in their own spoken
# sentences. The only support left is a small reminder strip of
# the four lenses.
# ---------------------------------------------------------------------------
def _my_describing_page(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 616,
                          "Choose your own thing. Draw it. "
                          "Tell about it!")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 592,
                          "Use any words that help you "
                          "describe it.")
    label = "My thing:"
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 16)
    pdf.drawString(40, 560, label)
    sx = 40 + stringWidth(label, "Andika-Bold", 16) + 10
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(sx, 558, 572, 558)
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 300, 532, 230, 12, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 500, "Draw it here.")
    # minimal reminder strip: the four lenses, small and OPTIONAL
    total = 4 * 118 + 3 * 10
    x = (PAGE_WIDTH - total) / 2
    for kind, word in LENSES:
        _lens_chip(pdf, x, 252, kind, word)
        x += 128
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 218, "My words:")
    _scribe(pdf, 40, 188, 532, rows=3)
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 92,
        "Adult: Write the exact words your child says. Their "
        "drawing tells even more.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "The word chips are only reminders. Any describing "
        "words count.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Describe It!", "My Describing Page")
    _my_describing_page(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [build_p1_page, build_p2_page, build_p3_page, build_p4_page]
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "worksheets", "kindergarten", "reading",
                       "describe-it")
PACK = "describe-it"
PREVIEW_DIR = os.path.expanduser("~/workspace/your_files/describe-it")


def build_pack():
    os.makedirs(OUT_DIR, exist_ok=True)
    page_paths = []
    for i, builder in enumerate(PAGES, start=1):
        p = os.path.join(OUT_DIR, f"{PACK}-page-{i:02d}.pdf")
        builder(p)
        page_paths.append(p)
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_paths:
        for pg in PdfReader(p).pages:
            writer.add_page(pg)
    bundle = os.path.join(OUT_DIR, f"{PACK}-review.pdf")
    with open(bundle, "wb") as fh:
        writer.write(fh)
    print("pack built in", os.path.normpath(OUT_DIR))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build_pack()
    else:
        os.makedirs(PREVIEW_DIR, exist_ok=True)
        for i, builder in enumerate(PAGES, start=1):
            builder(f"/tmp/di-p{i}.pdf")
        print("previews built in /tmp")
