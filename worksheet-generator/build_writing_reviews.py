#!/usr/bin/env python3
"""Grade 1 Writing -- Writing Reviews: My Opinion (Learning Made Simple).

Resource 7, five pages moving from stating an opinion to writing and
revising a short review. This REPLACES the planned four-page Resource 7
version; it is not a duplicate opinion-writing pack.
Internal planning standard: W.1.1 (write an opinion piece: state an
opinion, supply a reason, provide closure). The standards code is
planning only and never appears on the child pages. No printable
answer key: this is an open-ended writing pack.

Pages:
  P1: My Opinion -- pick a review topic, state an opinion, draw it
  P2: Give a Reason -- specific reasons with "because", reason bank
  P3: My Opinion and My Reason -- combine opinion and reason
  P4: Write My Review -- independent review, open lines, reminder chips
  P5: Make It Better -- checklist, improve the Page 4 review

Page 2 models SPECIFIC reasons only (never "because it is good").
Page 4 has a small visual reminder (Opinion / Reason / Closing chips)
and open lines only, no sentence frames.

v2 revision: Pages 1-3 rebuilt with roomy 40pt handwriting rows
(ROOMY_ROW_H) after the user found the 30pt rows too cramped for
Grade 1. Page 1 cards shrank slightly and Page 2's reason bank was
compacted to make room; Page 3's "Try another one" dropped from 3
rows to 2. Pages 4 and 5 are approved and untouched.

v3 revision (typography only): printed words raised for Grade 1
readability. Sentence starters 16pt -> 17pt; instructions stay 15pt;
section labels, reason banks, chips, checklist items, and notes raised
to 13-14pt. Header title 20pt -> 22pt and subtitle 15pt -> 17pt so
headings stay clearly larger than body text. Handwriting spacing,
row positions, writing/drawing areas, illustrations, wording, and
layouts are unchanged from v2.

Canonical header/footer: build_phonics_az (draw_header/draw_footer,
verbatim draw_logo). Handwriting lines: build_first_writing.
Title uses size 22 (measured 303.2pt, fits inside the teal rule);
subtitle uses size 17 (longest subtitle 222.0pt, fits).

Run with the repo venv:
  ../.venv/bin/python build_writing_reviews.py
Build only, for review. No lock, handoff, integration, or publish.

Note for a future handoff: the four topic JPGs live in
~/workspace/your_files/writing-reviews/assets/ and must be copied into
the repo's worksheet-generator/assets/writing-reviews/ so the builder's
asset path resolves from the repo.
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

PACK_TITLE = "Writing Reviews: My Opinion"
GRAY = HexColor("#37474F")
GUIDE = HexColor("#7FA3B5")
CORAL = HexColor("#E86A6A")
GOLD = HexColor("#F4B63E")
TEAL_DARK = HexColor("#14707A")
PANEL = HexColor("#F4F9F9")
PANEL_BORDER = HexColor("#D9E7E7")
FRAME_BORDER = HexColor("#BFD9D9")

# v2: roomy primary handwriting guidelines for Pages 1-3 (the 30pt rows
# from build_first_writing were too cramped for Grade 1). Each roomy
# row is 40pt tall with the dashed midline halfway, and rows are spaced
# on the same 14pt gap as the 30pt rows (54pt pitch). Pages 4 and 5
# keep the original 30pt rows and are unchanged.
ROOMY_ROW_H = 40
ROOMY_PITCH = 54


def _roomy_handwriting_lines(pdf, x, y_top, width, rows=1):
    """Roomy primary handwriting guide set(s): solid top and baseline
    with a dashed midline; each writing row is 40pt tall."""
    y = y_top
    for _ in range(rows):
        pdf.setStrokeColor(GUIDE)
        pdf.setLineWidth(1)
        pdf.setDash()
        pdf.line(x, y, x + width, y)
        pdf.setDash(4, 3)
        pdf.line(x, y - ROOMY_ROW_H // 2, x + width,
                 y - ROOMY_ROW_H // 2)
        pdf.setDash()
        pdf.setLineWidth(1.4)
        pdf.line(x, y - ROOMY_ROW_H, x + width, y - ROOMY_ROW_H)
        y -= ROOMY_PITCH
    return y + ROOMY_PITCH - ROOMY_ROW_H

ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "writing-reviews")
OUT_DIR = os.path.expanduser("~/workspace/your_files/writing-reviews")


def _fit_image_frame(pdf, path, x0, y0, w, h):
    """Draw an image fitted (not cropped) inside a rounded frame.

    The whole picture stays visible, so mixed portrait/landscape
    subjects are never cut off.
    """
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(FRAME_BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(x0, y0, w, h, 10, stroke=1, fill=1)
    iw, ih = ImageReader(path).getSize()
    scale = min((w - 8) / iw, (h - 8) / ih)
    sw, sh = iw * scale, ih * scale
    pdf.drawImage(ImageReader(path), x0 + (w - sw) / 2,
                  y0 + (h - sh) / 2, sw, sh, mask="auto")


def _instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, text)


# ---------------------------------------------------------------------------
# Page 1 -- My Opinion
# ---------------------------------------------------------------------------
TOPICS = [
    ("wr-topic-book.jpg", "Book"),
    ("wr-topic-game.jpg", "Game"),
    ("wr-topic-food.jpg", "Food"),
    ("wr-topic-activity.jpg", "Activity"),
]


def _my_opinion(pdf):
    _instruction(pdf, "Pick something you like. Say what you think.")
    for i, (img, label) in enumerate(TOPICS):
        col, row = i % 2, i // 2
        x0 = 40 + col * 274
        y0 = 470 - row * 162
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(PANEL_BORDER)
        pdf.setLineWidth(1.2)
        pdf.roundRect(x0, y0, 258, 150, 12, stroke=1, fill=1)
        _fit_image_frame(pdf, os.path.join(ASSETS_DIR, img),
                         x0 + 64, y0 + 32, 130, 106)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(x0 + 129, y0 + 13, label)
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.4)
        pdf.circle(x0 + 238, y0 + 130, 9, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, 284, "My opinion:")
    _roomy_handwriting_lines(pdf, 40, 272, 532, rows=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(40, 232, "I think")
    pdf.drawString(400, 232, "is the best.")
    pdf.setStrokeColor(FRAME_BORDER)
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 64, 532, 140, 12, stroke=1, fill=0)
    pdf.setFillColor(GUIDE)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(54, 188, "Draw it here.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Opinion", title_size=22,
                subtitle_size=17)
    _my_opinion(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Give a Reason
# ---------------------------------------------------------------------------
REASONS_P2 = [
    ("it has funny pictures", TEAL),
    ("it tastes sweet and crunchy", GOLD),
    ("it is fun to play with friends", NAVY),
    ("it has a good story", CORAL),
]


def _give_reason(pdf):
    _instruction(pdf, "Give a real reason. Tell why.")
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(PANEL_BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 480, 532, 140, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(58, 598, "REASON BANK")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(180, 598, "Pick a reason, or think of your own.")
    for i, (reason, color) in enumerate(REASONS_P2):
        col, row = i % 2, i // 2
        x0 = 58 + col * 264
        y0 = 552 - row * 48
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(PANEL_BORDER)
        pdf.setLineWidth(1)
        pdf.roundRect(x0, y0, 250, 38, 10, stroke=1, fill=1)
        pdf.setFillColor(color)
        pdf.circle(x0 + 16, y0 + 19, 6, stroke=0, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 14)
        pdf.drawString(x0 + 34, y0 + 13, reason)
    chip_colors = [TEAL, GOLD, NAVY]
    for i in range(3):
        y0 = 356 - i * 128
        pdf.setFillColor(PANEL)
        pdf.setStrokeColor(PANEL_BORDER)
        pdf.setLineWidth(1)
        pdf.roundRect(40, y0, 532, 116, 12, stroke=1, fill=1)
        pdf.setFillColor(chip_colors[i])
        pdf.circle(72, y0 + 58, 13, stroke=0, fill=1)
        pdf.setFillColor(NAVY if chip_colors[i] == GOLD
                         else HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(72, y0 + 54, str(i + 1))
        _roomy_handwriting_lines(pdf, 120, y0 + 108, 432, rows=2)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawString(120, y0 + 68, "I like")
        pdf.setFillColor(TEAL)
        pdf.drawString(120, y0 + 14, "because")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 86,
                          "Read your reasons. Do they tell why?")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Give a Reason", title_size=22,
                subtitle_size=17)
    _give_reason(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- My Opinion and My Reason
# ---------------------------------------------------------------------------
REASONS_P3 = [
    ("it makes me laugh", TEAL),
    ("it is fun with friends", GOLD),
    ("the pictures are colorful", NAVY),
]


def _opinion_and_reason(pdf):
    _instruction(pdf, "Say what you think, and tell why.")
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(PANEL_BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 536, 532, 84, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(58, 596, "NEED AN IDEA?")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(180, 596, "Try one of these.")
    for i, (reason, color) in enumerate(REASONS_P3):
        x0 = 58 + i * 174
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(PANEL_BORDER)
        pdf.setLineWidth(1)
        pdf.roundRect(x0, 548, 166, 36, 10, stroke=1, fill=1)
        pdf.setFillColor(color)
        pdf.circle(x0 + 14, 566, 5, stroke=0, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 13)
        pdf.drawString(x0 + 26, 561, reason)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, 508, "My opinion:")
    _roomy_handwriting_lines(pdf, 40, 496, 532, rows=2)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(40, 456, "I think")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, 372, "My reason:")
    _roomy_handwriting_lines(pdf, 40, 360, 532, rows=2)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(40, 320, "I think so because")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, 236, "Try another one:")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(180, 236, "Write an opinion and a reason.")
    _roomy_handwriting_lines(pdf, 40, 224, 532, rows=2)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 100,
                          "Read your sentences. Did you tell why?")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Opinion and My Reason",
                title_size=22, subtitle_size=17)
    _opinion_and_reason(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Write My Review (independent writing, open lines only)
# ---------------------------------------------------------------------------
def _write_review(pdf):
    _instruction(pdf, "Write your own review.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 622,
                          "Pick a book, a game, a food, or an activity.")
    chips = [
        ("1  Opinion", TEAL, HexColor("#FFFFFF")),
        ("2  Reason", GOLD, NAVY),
        ("3  Closing", NAVY, HexColor("#FFFFFF")),
    ]
    for i, (label, color, text_color) in enumerate(chips):
        x0 = 40 + i * 181
        pdf.setFillColor(color)
        pdf.roundRect(x0, 566, 170, 36, 10, stroke=0, fill=1)
        pdf.setFillColor(text_color)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(x0 + 85, 578, label)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, 546, "My review is about:")
    _handwriting_lines(pdf, 40, 538, 532, rows=1)
    pdf.setStrokeColor(FRAME_BORDER)
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 330, 532, 168, 12, stroke=1, fill=0)
    pdf.setFillColor(GUIDE)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(54, 478, "Draw what you reviewed.")
    _handwriting_lines(pdf, 40, 314, 532, rows=5)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Write My Review", title_size=22,
                subtitle_size=17)
    _write_review(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Make It Better (revise the Page 4 review)
# ---------------------------------------------------------------------------
def _make_better(pdf):
    _instruction(pdf, "Read your review again. Make it better.")
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(PANEL_BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 500, 532, 116, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(58, 596, "CHECKLIST")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(150, 596, "Tick each box when it is true.")
    checks = [
        "Did I say what I think?",
        "Did I give a reason with 'because'?",
        "Did I end my piece?",
    ]
    for i, text in enumerate(checks):
        y = 566 - i * 30
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.4)
        pdf.roundRect(58, y, 18, 18, 3, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 14)
        pdf.drawString(88, y + 4, text)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, 468, "Add or improve one part:")
    _handwriting_lines(pdf, 40, 458, 532, rows=3)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, 306, "Make it better:")
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(PANEL_BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 176, 532, 112, 12, stroke=1, fill=1)
    steps = [
        "Reread your review on Page 4.",
        "Choose one part to make better.",
        "Write it into your review on Page 4.",
    ]
    for i, text in enumerate(steps):
        cy = 268 - i * 32
        pdf.setFillColor(TEAL)
        pdf.circle(68, cy, 10, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawCentredString(68, cy - 4, str(i + 1))
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 14)
        pdf.drawString(88, cy - 4, text)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(PAGE_WIDTH / 2, 140,
                          "You wrote a real review. Great work!")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Make It Better", title_size=22,
                subtitle_size=17)
    _make_better(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    ("My Opinion", build_p1_page),
    ("Give a Reason", build_p2_page),
    ("My Opinion and My Reason", build_p3_page),
    ("Write My Review", build_p4_page),
    ("Make It Better", build_p5_page),
]


def main():
    pages_dir = os.path.join(OUT_DIR, "pages")
    previews_dir = os.path.join(OUT_DIR, "previews")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(previews_dir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder) in enumerate(PAGES):
        p = os.path.join(pages_dir,
                         "writing-reviews-page-%02d.pdf" % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(OUT_DIR, "writing-reviews-my-opinion-v3.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)


if __name__ == "__main__":
    main()
