#!/usr/bin/env python3
"""Kindergarten Writing -- All About... My Fact Pages
(Learning Made Simple).

Informational Writing pack (Michigan W.K.2), started 2026-10-19
after the same page-by-page audit that produced the Opinion pack
found informative composing to be a genuine gap: no existing page
has a child name a topic and supply information about it. (My
First Writing Adventures is labeling, free draw-and-write,
narrative, and revision; the Informational Text pack teaches
READING main topic and key details, not composing.)

Three pages, progressing in independence (user plan, 2026-10-19):
  P1: One True Fact -- a heavily supported first fact page: a
      given topic (dogs), its name printed as the page heading,
      a big drawing space, and ONE true fact composed by the
      child. APPROVED + LOCKED 2026-10-19 (v2).
  P2: Two True Facts -- the child supplies TWO different facts
      about a topic. APPROVED + LOCKED 2026-10-19.
  P3: My Information Page -- a fully independent informational
      page: child-chosen topic, drawing, and facts, no sentence
      frames. APPROVED + LOCKED 2026-10-19. Locally finalized
      2026-10-19 (bundle + page PDFs + separate parent guide);
      promotion to the handoff branch is HELD for the user's
      explicit final-pack approval.

Every page supports drawing, adult dictation, or emerging
independent writing. Facts must be true; the support on each page
(a model topic word, a fact starter, the child's own drawing, and
the adult line) is there to keep them accurate.

Shared design code (logo, header, footer, circular pictures) is
imported verbatim from build_phonics_az.py.
"""
import hashlib
import os
import subprocess
import sys
import tempfile

from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from build_phonics_az import (INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              _img_circle, draw_footer, draw_header)

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


# ---------------------------------------------------------------------------
# Page 1 -- One True Fact (IN REVIEW, v2)
# The topic is GIVEN and printed as the page's heading -- "All
# About Dogs" -- so the whole task is the W.K.2 move: draw the
# topic, then supply one piece of true information about it. The
# fact line opens with a child-friendly starter, "Dogs can ...",
# which the child completes with a true ability (run, swim, dig,
# bark...) by writing or dictating. The big drawing box puts the
# topic in front of the child; the adult line defines a fact in
# plain words and names all three composing modes. (v2 replaced
# the v1 title-writing line and model chip with the printed
# heading, at the user's direction.)
# ---------------------------------------------------------------------------
def _one_true_fact(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Let's write about dogs!")
    # printed topic heading (the topic is named for the child on
    # this supported first page)
    pdf.setFillColor(TEAL)
    pdf.setFont("Andika-Bold", 24)
    pdf.drawCentredString(PAGE_WIDTH / 2, 584, "All About Dogs")
    # big drawing box
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 256, 532, 304, 12, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 532, "Draw a dog here.")
    # one true fact, with a child-friendly starter
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(40, 226, "Tell one true fact about dogs:")
    fact = "Dogs can"
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 17)
    pdf.drawString(40, 176, fact)
    fx = 40 + stringWidth(fact, "Andika-Bold", 17) + 10
    _handwriting_lines(pdf, fx, 206, 572 - fx, rows=1)
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: A fact is something true. Your child can draw, "
        "tell you their words, or write.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "All About\u2026", "One True Fact")
    _one_true_fact(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Two True Facts (IN REVIEW)
# Same supported format as Page 1 (printed topic heading, big
# drawing box), but the child now supplies TWO facts -- and the
# page is built so the two facts come out DIFFERENT: the first
# line opens "Fish can ..." (something the topic can do) and the
# second opens "Fish have ..." (something the topic has). Both
# frames guarantee true completions for fish: can swim; have
# fins / tails / scales. Number chips mark the two facts.
# Topic is fish: simple to draw, and its basic facts are
# unconditionally true (unlike e.g. "birds can fly").
# ---------------------------------------------------------------------------
def _fact_row(pdf, num, starter, baseline):
    pdf.setFillColor(TEAL)
    pdf.circle(52, baseline + 5, 10, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setFont("Andika-Bold", 12)
    pdf.drawCentredString(52, baseline + 1, str(num))
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 17)
    pdf.drawString(76, baseline, starter)
    sx = 76 + stringWidth(starter, "Andika-Bold", 17) + 10
    _handwriting_lines(pdf, sx, baseline + 30, 572 - sx, rows=1)


def _two_true_facts(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Let's write about fish!")
    pdf.setFillColor(TEAL)
    pdf.setFont("Andika-Bold", 24)
    pdf.drawCentredString(PAGE_WIDTH / 2, 584, "All About Fish")
    # big drawing box
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 262, 532, 288, 12, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 524, "Draw a fish here.")
    # two different true facts
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(40, 234, "Tell two DIFFERENT true facts about fish:")
    _fact_row(pdf, 1, "Fish can", 192)
    _fact_row(pdf, 2, "Fish have", 126)
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: A fact is something true. Your child can draw, "
        "tell you their words, or write.")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "All About\u2026", "Two True Facts")
    _two_true_facts(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- My Information Page (IN REVIEW)
# The independent closer: the supports of Pages 1-2 (printed
# topic, topic-specific starters) are gone. The child chooses
# ANY topic, names it on a plain "My topic:" line (a label, not
# a sentence frame), draws it in a spacious box, and writes or
# dictates TWO different true facts in two numbered, starter-
# free fact areas with full primary handwriting lines.
# ---------------------------------------------------------------------------
def _fact_line(pdf, num, baseline):
    pdf.setFillColor(TEAL)
    pdf.circle(52, baseline + 5, 10, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setFont("Andika-Bold", 12)
    pdf.drawCentredString(52, baseline + 1, str(num))
    _handwriting_lines(pdf, 76, baseline + 30, 572 - 76, rows=1)


def _my_information_page(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Choose your own topic. Tell two true "
                          "facts about it!")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 618,
                          "It could be an animal, a food, a place, "
                          "or a thing.")
    # topic line: a label only, no sentence frame
    label = "My topic:"
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 16)
    pdf.drawString(40, 566, label)
    sx = 40 + stringWidth(label, "Andika-Bold", 16) + 10
    _handwriting_lines(pdf, sx, 596, 572 - sx, rows=1)
    # spacious drawing box
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 306, 532, 240, 12, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 520, "Draw your topic here.")
    # two numbered, starter-free fact areas
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(40, 282, "Tell two DIFFERENT true facts:")
    _fact_line(pdf, 1, 222)
    _fact_line(pdf, 2, 156)
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 92,
        "Adult: Your child picks their own topic and tells two "
        "true facts about it.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "They can draw, tell you their words, or write.")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "All About\u2026", "My Information Page")
    _my_information_page(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    # (approved preview file, locked render md5, builder, subtitle)
    ("fp-p1-v2.png", "74a0c0c68a3e13f880bec473376381d4",
     build_p1_page, "One True Fact"),
    ("fp-p2.png", "92ef4a2c33fb863b347146b17921b404",
     build_p2_page, "Two True Facts"),
    ("fp-p3.png", "6e3b222c3aaa1096021b1d2852423b73",
     build_p3_page, "My Information Page"),
]

PREVIEW_DIR = os.path.expanduser("~/workspace/your_files/fact-pages")


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
# Covers the W.K.2 objective, facts versus opinions, accurate
# example facts for each page, and how to support drawing,
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
    draw_header(pdf, "All About\u2026", "Parent Guide")
    y = 646
    y = _guide_heading(pdf, y, "What your child is learning")
    y = _guide_wrap(
        pdf, y,
        "These pages teach informational writing (Michigan "
        "Kindergarten standard W.K.2). Your child names what they "
        "are writing about and supplies information about the "
        "topic. In kindergarten, composing can be drawing, "
        "dictating words to an adult, or writing \u2014 all three "
        "count.")
    y -= 6
    y = _guide_heading(pdf, y, "Facts are not opinions")
    y = _guide_wrap(
        pdf, y,
        "A FACT is something true that can be checked: \u201cFish "
        "live in water.\u201d An OPINION is what someone thinks or "
        "likes: \u201cFish are the best pets.\u201d This pack "
        "practices facts. (Opinions have their own pack: My "
        "Opinion \u2014 I Like, I Think.) If your child offers an "
        "opinion, gently ask for a fact instead: \u201cWhat is "
        "true about fish?\u201d")
    y -= 6
    y = _guide_heading(pdf, y, "How the pages build independence")
    y = _guide_wrap(
        pdf, y,
        "the topic (dogs) is printed as the heading. Your child "
        "draws a dog and completes one fact: \u201cDogs can "
        "\u2026\u201d",
        bold_prefix="Page 1 \u2014 One True Fact: ")
    y = _guide_wrap(
        pdf, y,
        "two DIFFERENT facts about fish, helped by two different "
        "starters: \u201cFish can \u2026\u201d (something fish "
        "do) and \u201cFish have \u2026\u201d (something fish "
        "have).",
        bold_prefix="Page 2 \u2014 Two True Facts: ")
    y = _guide_wrap(
        pdf, y,
        "your child chooses any topic, names it, draws it, and "
        "writes two true facts with no starters at all.",
        bold_prefix="Page 3 \u2014 My Information Page: ")
    y -= 6
    y = _guide_heading(pdf, y, "Accurate example facts")
    for ex in (
        "Page 1 (dogs): \u201cDogs can run.\u201d \u201cDogs can "
        "swim.\u201d \u201cDogs can dig.\u201d",
        "Page 2 (fish): \u201cFish can swim.\u201d \u201cFish have "
        "fins.\u201d \u201cFish have tails.\u201d",
        "Page 3 (example topic \u2014 apples): \u201cApples grow "
        "on trees.\u201d \u201cApples can be red, green, or "
        "yellow.\u201d",
    ):
        y = _guide_wrap(pdf, y, ex)
    y -= 6
    y = _guide_heading(pdf, y, "How to support your child")
    for tip in (
        "\u2022  Ask your child to say each fact aloud before "
        "they draw or write.",
        "\u2022  Drawing counts. Young children compose with "
        "pictures first.",
        "\u2022  Dictation counts. If your child is not writing "
        "yet, write their exact words for them and read them back "
        "together.",
        "\u2022  Welcome invented spelling. Sounding words out "
        "matters more than spelling them correctly right now.",
        "\u2022  Keep facts true and simple. One or two real "
        "things your child knows about the topic is exactly "
        "enough.",
    ):
        y = _guide_wrap(pdf, y, tip)
    assert y > 70, f"parent guide overflowed the page (y={y})"
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "worksheets", "kindergarten", "reading",
                       "all-about-fact-pages")
PACK = "all-about-fact-pages"


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
        build_p3_page("/tmp/fp-p3.pdf")
        print("built /tmp/fp-p3.pdf")
