#!/usr/bin/env python3
"""Grade 1 Reading -- Describe and Show It (Learning Made Simple).

Four pages, one activity per page. Speaking, drawing, and writing
balanced on every page.
Internal planning standards: SL.1.4 (describe people, places,
things, and events with relevant details) and SL.1.5 (add drawings
or other visual displays to descriptions to clarify ideas). Supports
SL.1.1 and SL.1.6. Standards codes are planning only and never
appear on the child pages. No printable answer key: this is an
open-ended describing, drawing, and writing pack.

Pages:
  P1: Describe a Thing -- describe a familiar thing aloud, write
      two complete describing sentences with a full frame, then
      draw the thing.
  P2: Describe a Place -- draw a familiar place FIRST, then write
      describing sentences about what is there, with a shorter
      frame.
  P3: Describe a Person -- describe a special person, write
      describing sentences with complete left-aligned starters,
      then draw the person.
  P4: My Show and Tell -- independent. The child chooses their
      own person, place, thing, or event, draws it, writes
      describing sentences on open lines (no frame), and gets a
      Show and Tell reminder to share it with someone.

Every page carries a "Say it!" speaking panel in the same place:
the child describes their topic aloud to someone and uses their
own drawing to help explain their ideas. The display is always
the child's own drawing; no supplied illustration is used for it.
Sentence frames fade across the pack: full frame (P1), shorter
frame (P2), minimal frame (P3), open lines (P4).

Canonical header/footer: build_phonics_az (draw_header/draw_footer,
verbatim draw_logo). Handwriting rows: 36pt spacious guides.
Title uses size 20 (fits the 318pt title area).

Run with the repo venv (shared modules live in the
simplelearningresources tree):
  PYTHONPATH=~/workspace/simplelearningresources/worksheet-generator \
    ~/workspace/simplelearningresources/.venv/bin/python \
    build_describe_and_show_it.py
Build only, for review. No lock, handoff, integration, or publish.
v2 (2026-11-13): per her review of v1, P1/P3 writing guides
respaced so each sentence's guide reads as one unit, P1 "and"
placed after a measured blank, P2 frame changed to "I chose",
P3 uses complete left-aligned starters, P4 Show and Tell box
relaid out with the new wording.
"""
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from build_first_writing import _handwriting_lines  # noqa: E402,F401
from build_phonics_az import (  # noqa: E402
    INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
    draw_footer, draw_header,
)

PACK_TITLE = "Describe and Show It"
GRAY = HexColor("#37474F")
GUIDE = HexColor("#7FA3B5")
CORAL = HexColor("#E86A6A")
GOLD = HexColor("#F4B63E")
TEAL_DARK = HexColor("#14707A")
PANEL = HexColor("#F4F9F9")
PANEL_BORDER = HexColor("#D9E7E7")
FRAME_BORDER = HexColor("#BFD9D9")
TIP_FILL = HexColor("#FFF8E1")
TIP_BORDER = HexColor("#F0D9A0")
SAY_FILL = HexColor("#E6F4F4")
SAY_BORDER = HexColor("#A8D8D8")

ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets",
    "describe-and-show-it")
OUT_DIR = os.path.expanduser("~/workspace/your_files/describe-and-show-it")


def _spacious_lines(pdf, x, y_top, width, rows=1, row_h=36, gap=14):
    """Handwriting guide rows with generous height and spacing.
    Each row: solid top, dashed midline, solid baseline. row_h is
    the top-to-baseline height; gap is the space between one row's
    baseline and the next row's top. Returns the baseline y of the
    last row.
    """
    last_baseline = y_top - row_h
    for i in range(rows):
        top = y_top - i * (row_h + gap)
        pdf.setStrokeColor(GUIDE)
        pdf.setLineWidth(1)
        pdf.setDash()
        pdf.line(x, top, x + width, top)
        pdf.setDash(4, 3)
        pdf.line(x, top - row_h / 2, x + width, top - row_h / 2)
        pdf.setDash()
        pdf.setLineWidth(1.4)
        pdf.line(x, top - row_h, x + width, top - row_h)
        last_baseline = top - row_h
    return last_baseline


def _instruction(pdf, lines):
    """Centred instruction line(s) in NAVY bold 15pt. One line at
    y=642; two lines at y=646 and y=624. Both sit clear of the
    header Name/Date rule at y=664. Accepts a single string or a
    list of lines."""
    if isinstance(lines, str):
        lines = [lines]
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    if len(lines) == 1:
        pdf.drawCentredString(PAGE_WIDTH / 2, 642, lines[0])
    else:
        pdf.drawCentredString(PAGE_WIDTH / 2, 646, lines[0])
        pdf.drawCentredString(PAGE_WIDTH / 2, 624, lines[1])


def _say_it(pdf, text_lines):
    """The speaking panel, same place and style on every page:
    a pale teal rounded panel (y 542-608) with a bold "Say it!"
    label and the speaking prompt in NAVY. text_lines is one or
    two lines."""
    pdf.setFillColor(SAY_FILL)
    pdf.setStrokeColor(SAY_BORDER)
    pdf.setLineWidth(1.2)
    pdf.roundRect(40, 542, 532, 66, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(56, 590, "Say it!")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    if len(text_lines) == 1:
        pdf.drawString(56, 570, text_lines[0])
    else:
        pdf.drawString(56, 570, text_lines[0])
        pdf.drawString(56, 552, text_lines[1])


def _draw_box(pdf, x0, y0, w, h):
    """A generous empty drawing box: white fill, teal-grey frame.
    The picture inside is always the child's own work."""
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(FRAME_BORDER)
    pdf.setLineWidth(1.4)
    pdf.roundRect(x0, y0, w, h, 12, stroke=1, fill=1)


def _section_label(pdf, text, y):
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, text)


def _frame_word(pdf, text, x, y):
    """A fixed frame word printed on a handwriting baseline."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(x, y, text)


# ---------------------------------------------------------------------------
# Page 1 -- Describe a Thing
# ---------------------------------------------------------------------------
def _describe_thing(pdf):
    _instruction(pdf, ["Pick a thing you love. Say what it looks like.",
                       "Then write about it and draw it."])
    _say_it(pdf, ["Tell someone what your thing looks like.",
                  "Use words for color, size, and feel."])
    # Writing: two full-frame rows. One 3-line guide per sentence,
    # spaced wide apart so each guide reads as a single unit (no
    # confusing stack of lines). The "and" in sentence 2 follows a
    # measured blank for the first describing word.
    _section_label(pdf, "Write about your thing:", 528)
    _spacious_lines(pdf, 40, 510, 532, rows=2, row_h=36, gap=30)
    _frame_word(pdf, "This is my ", 40, 474)
    _frame_word(pdf, "It is ", 40, 408)
    and_x = 40 + stringWidth("It is ", "Helvetica-Bold", 13) + 120
    _frame_word(pdf, "and ", and_x, 408)
    # Drawing: a big box for the child's own picture.
    _section_label(pdf, "Draw your thing here.", 382)
    _draw_box(pdf, 40, 76, 532, 288)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Describe a Thing", title_size=20)
    _describe_thing(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Describe a Place (draw first, then write)
# ---------------------------------------------------------------------------
def _describe_place(pdf):
    _instruction(pdf, ["Think of a place you love. Draw it first.",
                       "Then write about it."])
    _say_it(pdf, ["Tell someone about your place.",
                  "What can you see and hear there?"])
    # Drawing first: a big box for the child's own picture.
    _section_label(pdf, "Draw your place here.", 528)
    _draw_box(pdf, 40, 240, 532, 270)
    # Writing: three shorter-frame rows.
    _section_label(pdf, "Write about your place:", 224)
    _spacious_lines(pdf, 40, 206, 532, rows=3, row_h=36, gap=12)
    _frame_word(pdf, "I chose ", 40, 170)
    _frame_word(pdf, "I can see ", 40, 122)
    _frame_word(pdf, "I can hear ", 40, 74)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Describe a Place", title_size=20)
    _describe_place(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Describe a Person
# ---------------------------------------------------------------------------
def _describe_person(pdf):
    _instruction(pdf, ["Think of someone special. Write about them.",
                       "Then draw them."])
    _say_it(pdf, ["Tell someone about this person.",
                  "How do they look? How do they make you feel?"])
    # Writing: two rows with complete, left-aligned starters. The
    # full starter sits at the left of its line; the child writes
    # the describing word or feeling after it. Guides spaced wide
    # apart so each reads as a single unit.
    _section_label(pdf, "Write about this person:", 528)
    _spacious_lines(pdf, 40, 510, 532, rows=2, row_h=36, gap=30)
    _frame_word(pdf, "This person is ", 40, 474)
    _frame_word(pdf, "This person makes me feel ", 40, 408)
    # Drawing: a big box for the child's own picture.
    _section_label(pdf, "Draw this person here.", 382)
    _draw_box(pdf, 40, 76, 532, 288)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Describe a Person", title_size=20)
    _describe_person(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- My Show and Tell (independent, open lines)
# ---------------------------------------------------------------------------
def _show_and_tell(pdf):
    _instruction(pdf, ["Choose your own person, place, thing, or event.",
                       "Draw it. Then write about it."])
    _say_it(pdf, ["Use your drawing to help you tell about it."])
    # Drawing: a big box for the child's own picture.
    _section_label(pdf, "Draw it here.", 528)
    _draw_box(pdf, 40, 290, 532, 220)
    # Writing: three open handwriting rows, no frame, no starters.
    _section_label(pdf, "Write about it:", 274)
    _spacious_lines(pdf, 40, 256, 532, rows=3, row_h=36, gap=12)
    # Show and Tell reminder panel.
    pdf.setFillColor(TIP_FILL)
    pdf.setStrokeColor(TIP_BORDER)
    pdf.setLineWidth(1.2)
    pdf.roundRect(40, 58, 532, 52, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(56, 94, "Show and Tell!")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(
        56, 76, "Show your drawing to someone. "
        "Tell them three things about it.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Show and Tell", title_size=20)
    _show_and_tell(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver (full pack)
# ---------------------------------------------------------------------------
def main():
    pages_dir = os.path.join(OUT_DIR, "pages-v2")
    previews_dir = os.path.join(OUT_DIR, "previews")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(previews_dir, exist_ok=True)
    builders = [
        ("Describe a Thing", build_p1_page),
        ("Describe a Place", build_p2_page),
        ("Describe a Person", build_p3_page),
        ("My Show and Tell", build_p4_page),
    ]
    page_pdfs = []
    for i, (title, builder) in enumerate(builders):
        p = os.path.join(pages_dir,
                         "describe-and-show-it-page-%02d.pdf" % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(OUT_DIR, "describe-and-show-it-v2.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 4
    print("bundle: %s (4 pages)" % bundle)


if __name__ == "__main__":
    main()
