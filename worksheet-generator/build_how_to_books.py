#!/usr/bin/env python3
"""Grade 1 Writing -- How-To Books: Writing the Steps (Learning Made Simple).

Four pages, one consistent how-to topic across the whole pack.
Internal planning standards: W.1.2 (informative writing: name a
topic, supply facts, close the piece) and W.1.8 (recall information
from experience to answer a question). Standards codes are planning
only and never appear on the child pages. No printable answer key:
this is an open-ended writing pack.

Pages:
  P1: Pick Your How-To -- choose a topic, name the book, list
      what you need, draw the finished result.
  P2: Draw the Steps -- four numbered frames (First, Next, Then,
      Last) matching the Page 3 writing sections.
  P3: Write the Steps -- four numbered writing sections matching
      the Page 2 drawing sequence, generous handwriting space,
      light sentence support.
  P4: Close It and Check It -- closing sentence, a small
      "My Helpful Tip" activity, simple self-check checklist.

Canonical header/footer: build_phonics_az (draw_header/draw_footer,
verbatim draw_logo). Handwriting lines: build_first_writing.
Title uses size 20 (measured: 316.7pt, fits the 318pt title area).

Run with the repo venv:
  ../.venv/bin/python build_how_to_books.py
Build only, for review. No lock, handoff, integration, or publish.
Page 1 approved as v3 (2026-11-13) and preserved exactly; Pages 2-4
built together for one comprehensive review. v2 (2026-11-13):
bottom writing section respaced for Grade 1 comfort, taller 36pt
handwriting rows, wider gaps, choice cards unchanged. v3
(2026-11-13): final handwriting layout, simple single lines for
the idea and the title ("How to" at the start, no extra guides
above it), three evenly spaced full-guide rows for materials,
new instruction wording.
"""
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from build_first_writing import _handwriting_lines  # noqa: E402
from build_phonics_az import (  # noqa: E402
    INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
    draw_footer, draw_header,
)

PACK_TITLE = "How-To Books: Writing the Steps"
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

# Step colours shared by Pages 2 and 3 so the drawing frames and
# the writing sections match: (word, fill, number-text colour).
STEP_COLORS = [
    ("First", TEAL, HexColor("#FFFFFF")),
    ("Next", GOLD, NAVY),
    ("Then", NAVY, HexColor("#FFFFFF")),
    ("Last", CORAL, HexColor("#FFFFFF")),
]

ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "how-to-books")
OUT_DIR = os.path.expanduser("~/workspace/your_files/how-to-books")


def _image_frame(pdf, path, x0, y0, w, h):
    """Draw an image inside a rounded-rectangle frame, center-cropped."""
    p = pdf.beginPath()
    p.roundRect(x0, y0, w, h, 10)
    pdf.saveState()
    pdf.clipPath(p, stroke=0, fill=0)
    iw, ih = ImageReader(path).getSize()
    scale = max(w / iw, h / ih)
    sw = iw * scale
    sh = ih * scale
    pdf.drawImage(ImageReader(path), x0 + (w - sw) / 2,
                  y0 + (h - sh) / 2, sw, sh, mask="auto")
    pdf.restoreState()
    pdf.setStrokeColor(FRAME_BORDER)
    pdf.setLineWidth(1.2)
    pdf.roundRect(x0, y0, w, h, 10, stroke=1, fill=0)


def _single_line(pdf, x, y, width):
    """One simple, spacious writing line: a single solid baseline
    with no top or midline guide. Used for short phrases (a topic
    name, a book title) where a full handwriting guide would add
    clutter. Returns y.
    """
    pdf.setStrokeColor(GUIDE)
    pdf.setLineWidth(1.4)
    pdf.line(x, y, x + width, y)
    return y


def _spacious_lines(pdf, x, y_top, width, rows=1, row_h=36, gap=14):
    """Handwriting guide rows with generous height and spacing.
    Each row: solid top, dashed midline, solid baseline. row_h is
    the top-to-baseline height; gap is the space between one row's
    baseline and the next row's top. Returns the baseline y of the
    last row. Taller than the shared 30pt guide so first-grade
    letter formation has comfortable room.
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


def _instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, text)


# ---------------------------------------------------------------------------
# Page 1 -- Pick Your How-To
# ---------------------------------------------------------------------------
CHOICES = [
    ("howto-wash-hands.jpg", "Wash", "Hands"),
    ("howto-make-sandwich.jpg", "Make a", "Sandwich"),
    ("howto-plant-seed.jpg", "Plant a", "Seed"),
    ("howto-brush-teeth.jpg", "Brush", "Teeth"),
]


def _pick_how_to(pdf):
    _instruction(pdf, "Circle a picture OR write your own how-to idea.")
    # 2x2 choice cards, each 258 x 122.
    for i, (img, line1, line2) in enumerate(CHOICES):
        col, row = i % 2, i // 2
        x0 = 40 + col * 274
        y0 = 506 - row * 134
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(FRAME_BORDER)
        pdf.setLineWidth(1.4)
        pdf.roundRect(x0, y0, 258, 122, 12, stroke=1, fill=1)
        _image_frame(pdf, os.path.join(ASSETS_DIR, img),
                     x0 + 10, y0 + 11, 108, 100)
        # Empty circle to colour in for the chosen how-to.
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.5)
        pdf.circle(x0 + 230, y0 + 96, 12, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(x0 + 126, y0 + 68, line1)
        pdf.drawString(x0 + 126, y0 + 46, line2)
    # My own idea: one simple, spacious writing line for a short
    # topic name.
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 352, "My own idea:")
    _single_line(pdf, 140, 324, 432)
    # My book title: "How to" at the start of a single clear
    # handwriting line, writing space continuing to its right.
    # No extra guides above it.
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 296, "My book title:")
    _single_line(pdf, 40, 268, 532)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, 268, "How to")
    # Bottom band: what I need (left) and draw the finished result (right).
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 236, "What do I need?")
    _spacious_lines(pdf, 40, 224, 240, rows=3, gap=20)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(300, 236, "Draw what it looks like")
    pdf.drawString(300, 220, "when you are done.")
    pdf.setStrokeColor(FRAME_BORDER)
    pdf.setLineWidth(1.4)
    pdf.roundRect(300, 76, 272, 132, 12, stroke=1, fill=0)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Pick Your How-To", title_size=20)
    _pick_how_to(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Order the Steps
# ---------------------------------------------------------------------------
def _order_steps(pdf):
    _instruction(pdf, "Draw your four steps in order.")
    # 2x2 drawing frames, each 258 x 276, generous drawing space.
    for i, (word, color, text_color) in enumerate(STEP_COLORS):
        col, row = i % 2, i // 2
        x0 = 40 + col * 274
        y0 = 352 - row * 288
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(FRAME_BORDER)
        pdf.setLineWidth(1.4)
        pdf.roundRect(x0, y0, 258, 276, 12, stroke=1, fill=1)
        # Number circle and temporal word at the top of the frame.
        pdf.setFillColor(color)
        pdf.circle(x0 + 30, y0 + 246, 17, stroke=0, fill=1)
        pdf.setFillColor(text_color)
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(x0 + 30, y0 + 240, str(i + 1))
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawString(x0 + 54, y0 + 240, word)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Order the Steps", title_size=20)
    _order_steps(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Write the Steps
# ---------------------------------------------------------------------------
def _write_steps(pdf):
    _instruction(pdf, "Write each step. Use the time words.")
    # Four full-width panels, each 532 x 126, one consistent,
    # spacious handwriting area per step. Steps 1-2 carry a light
    # sentence starter aligned naturally on the row baseline;
    # Steps 3-4 are open lines.
    for i, (word, color, text_color) in enumerate(STEP_COLORS):
        y0 = 502 - i * 144
        pdf.setFillColor(PANEL)
        pdf.setStrokeColor(PANEL_BORDER)
        pdf.setLineWidth(1)
        pdf.roundRect(40, y0, 532, 126, 12, stroke=1, fill=1)
        pdf.setFillColor(color)
        pdf.circle(72, y0 + 98, 15, stroke=0, fill=1)
        pdf.setFillColor(text_color)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(72, y0 + 93, str(i + 1))
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(96, y0 + 92, word)
        _spacious_lines(pdf, 56, y0 + 60, 500, rows=1, row_h=36)
        if i < 2:
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(56, y0 + 24, word + ", ")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Write the Steps", title_size=20)
    _write_steps(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Close It and Check It
# ---------------------------------------------------------------------------
def _lightbulb(pdf, cx, cy, r):
    """Small vector lightbulb for the Helpful Tip panel."""
    pdf.setFillColor(GOLD)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.circle(cx, cy + 4, r, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.roundRect(cx - 6, cy - r - 2, 12, 7, 2, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.line(cx - 4, cy - r - 5, cx + 4, cy - r - 5)


CHECKS = [
    "Did I name my how-to?",
    "Are my steps in order?",
    "Did I include a true fact or helpful tip?",
    "Did I close my book?",
]


def _close_check(pdf):
    _instruction(pdf, "Finish your book. Then check it.")
    # Closing line: "Now you can" starter on a single clear line.
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 614, "My closing line:")
    _single_line(pdf, 40, 586, 532)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, 586, "Now you can")
    # My Helpful Tip panel.
    pdf.setFillColor(TIP_FILL)
    pdf.setStrokeColor(TIP_BORDER)
    pdf.setLineWidth(1.2)
    pdf.roundRect(40, 380, 532, 180, 12, stroke=1, fill=1)
    _lightbulb(pdf, 66, 528, 13)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(88, 532, "My Helpful Tip")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(88, 514, "Write one tip that helps someone do your how-to.")
    _spacious_lines(pdf, 56, 492, 500, rows=2, row_h=36, gap=20)
    # Checklist panel.
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(PANEL_BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 140, 532, 220, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(58, 340, "CHECKLIST")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 10.5)
    pdf.drawString(150, 340, "Tick each box when it is true.")
    for i, text in enumerate(CHECKS):
        y = 316 - i * 48
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.4)
        pdf.roundRect(58, y, 18, 18, 3, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 13)
        pdf.drawString(88, y + 4, text)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 104,
        "You wrote a real how-to book. Great work!")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Close It and Check It", title_size=20)
    _close_check(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver (full pack)
# ---------------------------------------------------------------------------
def main():
    pages_dir = os.path.join(OUT_DIR, "pages-v3")
    previews_dir = os.path.join(OUT_DIR, "previews")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(previews_dir, exist_ok=True)
    builders = [
        ("Pick Your How-To", build_p1_page),
        ("Order the Steps", build_p2_page),
        ("Write the Steps", build_p3_page),
        ("Close It and Check It", build_p4_page),
    ]
    page_pdfs = []
    for i, (title, builder) in enumerate(builders):
        p = os.path.join(pages_dir,
                         "how-to-books-page-%02d.pdf" % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(OUT_DIR, "how-to-books-writing-the-steps-v1.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 4
    print("bundle: %s (4 pages)" % bundle)


if __name__ == "__main__":
    main()
