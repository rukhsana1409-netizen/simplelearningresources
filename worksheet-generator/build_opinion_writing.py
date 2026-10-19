#!/usr/bin/env python3
"""Kindergarten Writing -- My Opinion: I Like, I Think
(Learning Made Simple).

Opinion Writing pack (Michigan W.K.1), approved 2026-10-19 after a
page-by-page audit found opinion writing to be a genuine gap: no
existing page has a child name a topic and state an opinion about
it. Four pages; every page supports drawing, adult dictation, or
emerging independent writing, and none of them reduces composing
to circling or filling a given blank.

Approved plan (user revisions, 2026-10-19):
  P1: My Favorite -- name a topic and express a preference, with
      picture choices but freedom to choose another answer.
      APPROVED + LOCKED 2026-10-19 (v2).
  P2: My Favorite Book -- name a book and express an opinion;
      reasons encouraged but optional, open-ended responses.
      APPROVED + LOCKED 2026-10-19.
  P3: Which Would You Choose? -- choose between two meaningful
      activities/experiences and express a preference, optionally
      explaining why (NOT a repeat of P1's favorite-item format).
      APPROVED + LOCKED 2026-10-19.
  P4: My Opinion Page -- independently choose a topic, draw, and
      state an opinion. APPROVED + LOCKED 2026-10-19.
      Finalized 2026-10-19: bundle + page PDFs + separate parent
      guide (opinion-writing-parent-guide.pdf, NOT in the bundle).

Deliberately distinct from My First Writing Adventures (labeling,
free draw-and-write, narrative, revision) and Building Simple
Sentences (arranging/expanding/fixing/completing given sentences).

Shared design code (logo, header, footer, circular pictures) is
imported verbatim from build_phonics_az.py.
"""
import hashlib
import os
import subprocess
import sys
import tempfile

from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from build_phonics_az import (INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              _ASSETS, _img_circle, draw_footer, draw_header)

ADULT = HexColor("#37474F")
GUIDE = HexColor("#7FA3B5")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_LINE = HexColor("#D9E7E7")


def _handwriting_lines(pdf, x, y_top, width, rows=1):
    """Kindergarten handwriting guide set(s): solid top and baseline
    with a dashed midline; each writing row is 30pt tall.
    (Same guide standard as My First Writing Adventures.)"""
    y = y_top
    for _ in range(rows):
        pdf.setStrokeColor(GUIDE)
        pdf.setLineWidth(1)
        pdf.setDash()
        pdf.line(x, y, x + width, y)
        pdf.setDash(4, 3)
        pdf.line(x, y - 15, x + width, y - 15)
        pdf.setDash()
        pdf.setLineWidth(1.4)
        pdf.line(x, y - 30, x + width, y - 30)
        y -= 44
    return y + 44 - 30


def _panel(pdf, px0, py0, w, h):
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_LINE)
    pdf.setLineWidth(1)
    pdf.roundRect(px0, py0, w, h, 14, stroke=1, fill=1)


def _scene(pdf, rel_path, x0, y0, w, h):
    """Draw an image inside a rounded-rectangle frame, center-
    cropped to the frame's ratio (same approach as the story
    packs' scene helper)."""
    p = pdf.beginPath()
    p.roundRect(x0, y0, w, h, 12)
    pdf.saveState()
    pdf.clipPath(p, stroke=0, fill=0)
    path = os.path.join(_ASSETS, rel_path)
    iw, ih = ImageReader(path).getSize()
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    pdf.drawImage(ImageReader(path), x0 - (dw - w) / 2,
                  y0 - (dh - h) / 2, dw, dh, mask="auto")
    pdf.restoreState()
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x0, y0, w, h, 12, stroke=1, fill=0)


# ---------------------------------------------------------------------------
# Page 1 -- My Favorite (IN REVIEW)
# The child names a favorite thing (the topic) and states their
# preference. A strip of small pictures offers IDEAS only -- the
# child may pick one of them or any favorite of their own; nothing
# is circled as an answer. The composing happens in the big
# drawing box and on the writing lines: the child draws, dictates
# their words to an adult, or writes with their own spelling.
# ---------------------------------------------------------------------------
P1_IDEAS = [
    "phonics-a-z/ph-apple.jpg",        # apple
    "think-choose/tc-icecream.jpg",    # ice cream
    "animal-library/lib-dog.jpg",      # dog
    "living-nonliving/ln-teddy.jpg",   # teddy bear
    "living-nonliving/ln-ball.jpg",    # ball
    "informational-text/it-obj-book.jpg",  # book
]


def _my_favorite(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "What is your favorite? Tell why you like it!")
    # idea strip: suggestions only, never an answer to circle
    _panel(pdf, 40, 552, 532, 54)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(58, 573, "IDEAS:")
    for i, img in enumerate(P1_IDEAS):
        _img_circle(pdf, img, 126 + i * 56, 579, 19, zoom=True)
    pdf.setFillColor(TEAL)
    pdf.setFont("Andika-Bold", 12.5)
    pdf.drawString(466, 572, "or your own!")
    # big drawing box
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 254, 532, 286, 12, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 512, "Draw your favorite thing here.")
    # composing lines: the child names their favorite, then gives
    # their reason. Both are the child's own words -- drawn from
    # their drawing, dictated to an adult, or written with their
    # own spelling. The reason line is optional.
    starter = "My favorite thing is"
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 17)
    pdf.drawString(40, 196, starter)
    sx = 40 + stringWidth(starter, "Andika-Bold", 17) + 10
    _handwriting_lines(pdf, sx, 226, 572 - sx, rows=1)
    reason = "I like it because"
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 17)
    pdf.drawString(40, 130, reason)
    rx = 40 + stringWidth(reason, "Andika-Bold", 17) + 10
    _handwriting_lines(pdf, rx, 160, 572 - rx, rows=1)
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Your child can draw, tell you their words, or write. "
        "Telling why is optional.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "My Opinion", "My Favorite")
    _my_favorite(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- My Favorite Book (IN REVIEW)
# Responding to a BOOK, not a generic favorite thing: the child
# names their favorite book (title dictated or written on a
# handwriting line), draws a scene or character from it in a big
# box, and states their opinion -- "I like this book because ..."
# -- in their own words. The reason is encouraged but optional;
# the same lines serve drawing talk, adult dictation, and
# emerging independent writing.
# ---------------------------------------------------------------------------
def _my_favorite_book(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "What is your favorite book?")
    # name the book
    starter = "The book is called"
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 17)
    pdf.drawString(40, 574, starter)
    sx = 40 + stringWidth(starter, "Andika-Bold", 17) + 10
    _handwriting_lines(pdf, sx, 604, 572 - sx, rows=1)
    # big drawing box: a scene or character from the book
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 262, 532, 286, 12, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 522, "Draw a scene or character from the book.")
    # state the opinion, with an optional reason
    reason = "I like this book because"
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 17)
    pdf.drawString(40, 176, reason)
    rx = 40 + stringWidth(reason, "Andika-Bold", 17) + 10
    _handwriting_lines(pdf, rx, 206, 572 - rx, rows=1)
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Your child can draw, tell you their words, or write. "
        "Telling why is optional.")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "My Opinion", "My Favorite Book")
    _my_favorite_book(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Which Would You Choose? (IN REVIEW)
# A meaningful choice between two EXPERIENCES, not another
# favorite item: visit the zoo or visit the beach, each shown in
# a large original illustration with a short caption. The child
# circles the one they choose, draws THEMSELVES enjoying it, and
# states their preference in their own words -- "I would choose
# ..." -- with an optional reason on a second line. The lines
# serve dictation and emerging writing alike.
# ---------------------------------------------------------------------------
P3_CHOICES = [
    ("opinion-writing/ow-zoo.jpg", "Visit the zoo"),
    ("opinion-writing/ow-beach.jpg", "Visit the beach"),
]


def _which_would_you_choose(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Which would you choose? Circle one.")
    for i, (img, caption) in enumerate(P3_CHOICES):
        px = 40 + i * 276
        _scene(pdf, img, px, 446, 256, 168)
        # caption chip overlaid at the panel's bottom centre
        wch = stringWidth(caption, "Andika-Bold", 14.5) + 26
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(PANEL_LINE)
        pdf.setLineWidth(1)
        pdf.roundRect(px + (256 - wch) / 2, 456, wch, 26, 9,
                      stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 14.5)
        pdf.drawCentredString(px + 128, 464, caption)
    # draw yourself enjoying your choice
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 250, 532, 182, 12, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 406, "Draw yourself enjoying it.")
    # state the preference, then an optional reason
    starter = "I would choose"
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 17)
    pdf.drawString(40, 194, starter)
    sx = 40 + stringWidth(starter, "Andika-Bold", 17) + 10
    _handwriting_lines(pdf, sx, 224, 572 - sx, rows=1)
    reason = "I like it because"
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 17)
    pdf.drawString(40, 128, reason)
    rx = 40 + stringWidth(reason, "Andika-Bold", 17) + 10
    _handwriting_lines(pdf, rx, 158, 572 - rx, rows=1)
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Your child can draw, tell you their words, or write. "
        "Telling why is optional.")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "My Opinion", "Which Would You Choose?")
    _which_would_you_choose(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- My Opinion Page (IN REVIEW)
# The independent closer: the scaffolding of Pages 1-3 (idea
# pictures, book frame, either/or choices, sentence starters) is
# gone. The child picks ANY topic -- an activity, an animal, a
# food, a place, or a book -- names it on a plain topic line,
# draws it in a big box, and writes or dictates what they think
# about it on two open lines under a simple "What I think:"
# label. A reason is welcome but optional.
# ---------------------------------------------------------------------------
def _my_opinion_page(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Choose your own topic. Tell what you think "
                          "about it!")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 618,
                          "It could be an activity, an animal, a food, "
                          "a place, or a book.")
    # topic line: a label only, no sentence frame
    label = "My topic:"
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 16)
    pdf.drawString(40, 566, label)
    sx = 40 + stringWidth(label, "Andika-Bold", 16) + 10
    _handwriting_lines(pdf, sx, 596, 572 - sx, rows=1)
    # big drawing box
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 262, 532, 288, 12, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 524, "Draw your topic here.")
    # open opinion-writing area: two starter-free lines
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(40, 238, "What I think:")
    _handwriting_lines(pdf, 40, 226, 532, rows=2)
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 92,
        "Adult: Your child picks their own topic and tells what "
        "they think about it.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "They can draw, tell you their words, or write. Telling "
        "why is optional.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "My Opinion", "My Opinion Page")
    _my_opinion_page(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    # (approved preview file, locked render md5, builder, subtitle)
    ("ow-p1-v2.png", "91bb1d0934f8f3ee1419160003cef4f8",
     build_p1_page, "My Favorite"),
    ("ow-p2.png", "ecf50d9cb862e4b9341cf90b26dad6aa",
     build_p2_page, "My Favorite Book"),
    ("ow-p3.png", "159ddb5f5e651f4a0a8ad1d7928cd81a",
     build_p3_page, "Which Would You Choose?"),
    ("ow-p4.png", "e24df7fa4eb7f925ef249668ff728163",
     build_p4_page, "My Opinion Page"),
]

PREVIEW_DIR = os.path.expanduser("~/workspace/your_files/opinion-writing")


def _render_md5(pdf_path):
    with tempfile.TemporaryDirectory() as td:
        stem = os.path.join(td, "page")
        subprocess.run(["pdftoppm", "-png", "-r", "150", "-singlefile",
                        pdf_path, stem], check=True)
        with open(stem + ".png", "rb") as fh:
            return hashlib.md5(fh.read()).hexdigest()


def _check_locks():
    """Rebuild every locked page and verify it still renders
    pixel-identical to the preview the user approved."""
    for preview, md5, builder, subtitle in PAGES:
        if md5 is None:
            continue
        with tempfile.TemporaryDirectory() as td:
            probe = os.path.join(td, "probe.pdf")
            builder(probe)
            got = _render_md5(probe)
        assert got == md5, (
            f"LOCKED PAGE CHANGED: {subtitle} renders {got}, "
            f"approved {md5} ({preview})")
        print(f"lock check OK: {subtitle} == {preview}")


# ---------------------------------------------------------------------------
# Parent guide (separate PDF, NOT part of the child bundle).
# Explains W.K.1, the learning objective, how the four pages grow
# in independence, example responses (explicitly examples only --
# there is no one correct opinion), and how to support drawing,
# dictation, and emerging writing.
# ---------------------------------------------------------------------------
def _guide_heading(pdf, y, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(56, y, text)
    return y - 20


def _guide_wrap(pdf, y, text, bold_prefix=None, size=10.5,
                width=500):
    """Draw a paragraph (optionally starting with a bold prefix),
    word-wrapped; returns the y below the paragraph. Only the
    prefix itself is bold; the rest of the first line is regular."""
    pw = (pdf.stringWidth(bold_prefix, "Helvetica-Bold", size)
          if bold_prefix else 0)
    words = text.split()
    lines, cur = [], ""
    avail = width - pw
    for w in words:
        trial = (cur + " " + w) if cur else w
        if pdf.stringWidth(trial, "Helvetica", size) > avail and cur:
            lines.append(cur)
            cur = w
            avail = width
        else:
            cur = trial
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines):
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", size)
        if i == 0 and bold_prefix:
            pdf.setFont("Helvetica-Bold", size)
            pdf.drawString(56, y, bold_prefix)
            pdf.setFont("Helvetica", size)
            pdf.drawString(56 + pw, y, ln)
        else:
            pdf.drawString(56, y, ln)
        y -= 15
    return y - 5


def build_parent_guide(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "My Opinion", "Parent Guide")
    y = 646
    y = _guide_heading(pdf, y, "What your child is learning")
    y = _guide_wrap(
        pdf, y,
        "These pages teach opinion writing (Michigan Kindergarten "
        "standard W.K.1). Your child names a topic or a book, says "
        "what they think about it, and may add a reason. In "
        "kindergarten, composing can be drawing, dictating words "
        "to an adult, or writing \u2014 all three count.")
    y -= 6
    y = _guide_heading(pdf, y, "How the pages build independence")
    y = _guide_wrap(
        pdf, y,
        "draws a favorite thing and completes \u201cMy favorite "
        "thing is \u2026\u201d and, if they wish, \u201cI like it "
        "because \u2026\u201d The small pictures are ideas only "
        "\u2014 any favorite counts.",
        bold_prefix="Page 1 \u2014 My Favorite: ")
    y = _guide_wrap(
        pdf, y,
        "names a favorite book, draws a scene or character from "
        "it, and tells why they like it.",
        bold_prefix="Page 2 \u2014 My Favorite Book: ")
    y = _guide_wrap(
        pdf, y,
        "chooses a zoo visit or a beach visit, draws themself "
        "enjoying it, and says \u201cI would choose \u2026\u201d "
        "with an optional reason.",
        bold_prefix="Page 3 \u2014 Which Would You Choose?: ")
    y = _guide_wrap(
        pdf, y,
        "picks any topic, draws it, and writes what they think "
        "\u2014 no sentence starters, fully their own.",
        bold_prefix="Page 4 \u2014 My Opinion Page: ")
    y -= 6
    y = _guide_heading(pdf, y, "Example responses (examples only)")
    for ex in (
        "Page 1: \u201cMy favorite thing is my bike. I like it "
        "because it goes fast.\u201d",
        "Page 2: \u201cThe book is called Brown Bear, Brown Bear. "
        "I like this book because it is funny.\u201d",
        "Page 3: \u201cI would choose the beach. I like it because "
        "I can dig in the sand.\u201d",
        "Page 4: Topic: \u201cCats.\u201d \u2014 \u201cCats are "
        "soft. I like cats because they sit with me.\u201d",
    ):
        y = _guide_wrap(pdf, y, ex)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(56, y, "There is no one correct opinion. Whatever "
                         "your child thinks is the right")
    pdf.drawString(56, y - 15, "answer for them.")
    y -= 42
    y = _guide_heading(pdf, y, "How to support your child")
    for tip in (
        "\u2022  Ask your child to say their opinion aloud before "
        "they draw or write.",
        "\u2022  Drawing counts. Young children compose with "
        "pictures first.",
        "\u2022  Dictation counts. If your child is not writing "
        "yet, write their exact words for them and read them back "
        "together.",
        "\u2022  Welcome invented spelling. Sounding words out "
        "matters more than spelling them correctly right now.",
        "\u2022  Reasons are always optional. A simple \u201cI "
        "like it\u201d is a complete opinion.",
    ):
        y = _guide_wrap(pdf, y, tip)
    assert y > 70, f"parent guide overflowed the page (y={y})"
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "worksheets", "kindergarten", "reading",
                       "opinion-writing")
PACK = "opinion-writing"


def finalize():
    for preview, md5, _b, subtitle in PAGES:
        assert md5 is not None, f"{subtitle} is not locked"
    _check_locks()
    os.makedirs(OUT_DIR, exist_ok=True)
    page_paths = []
    for i, (_p, _m, builder, _s) in enumerate(PAGES, start=1):
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
    guide = os.path.join(OUT_DIR, f"{PACK}-parent-guide.pdf")
    build_parent_guide(guide)
    # -- quality checks -------------------------------------------------
    for p in page_paths + [bundle, guide]:
        r = PdfReader(p)
        for pg in r.pages:
            assert float(pg.mediabox.width) == 612.0, p
            assert float(pg.mediabox.height) == 792.0, p
    assert len(PdfReader(bundle).pages) == len(PAGES)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-png", "-r", "150", bundle,
                        os.path.join(td, "b")], check=True)
        renders = sorted(f for f in os.listdir(td)
                         if f.startswith("b-") and f.endswith(".png"))
        assert len(renders) == len(PAGES), renders
        for i, (_p, md5, _b, subtitle) in enumerate(PAGES, start=1):
            with open(os.path.join(td, renders[i - 1]), "rb") as fh:
                got = hashlib.md5(fh.read()).hexdigest()
            assert got == md5, f"bundle page {i} ({subtitle}) != locked"
            print(f"bundle page {i} pixel-identical: {subtitle}")
    for p in page_paths + [bundle, guide]:
        data = open(p, "rb").read()
        print(f"{os.path.basename(p)}: {len(data)} bytes, "
              f"md5 {hashlib.md5(data).hexdigest()}, "
              f"sha256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "finalize":
        finalize()
    else:
        _check_locks()
        os.makedirs(PREVIEW_DIR, exist_ok=True)
        build_p4_page("/tmp/ow-p4.pdf")
        print("built /tmp/ow-p4.pdf")