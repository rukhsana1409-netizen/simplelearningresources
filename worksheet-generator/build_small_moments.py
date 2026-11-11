#!/usr/bin/env python3
"""Grade 1 Writing -- Small Moments: My Narrative (Learning Made Simple).

Five pages moving from planning to independent writing to revision.
Internal planning standards: W.1.3 (narrate a single event or several
loosely linked events, in order, with details) and W.1.5 (add details
and revise). Standards codes are planning only and never appear on
the child pages. No printable answer key: this is an open-ended
writing pack.

Pages:
  P1: Plan Your Small Moment -- draw beginning, middle, end
  P2: Tell It in Order -- First / Next / Last sentence frames
  P3: Add a Detail -- who, where, how it felt; feeling-words bank
  P4: Write Your Story -- independent writing, open ruled lines
  P5: Make It Better -- checklist, add a detail, revise your story

Canonical header/footer: build_phonics_az (draw_header/draw_footer,
verbatim draw_logo). Handwriting lines: build_first_writing.
Title uses size 20 (measured) so it stays inside the teal rule.

Run with the repo venv:
  ../.venv/bin/python build_small_moments.py
Build only, for review. No lock, handoff, integration, or publish.
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

PACK_TITLE = "Small Moments: My Narrative"
GRAY = HexColor("#37474F")
GUIDE = HexColor("#7FA3B5")
CORAL = HexColor("#E86A6A")
GOLD = HexColor("#F4B63E")
TEAL_DARK = HexColor("#14707A")
PANEL = HexColor("#F4F9F9")
PANEL_BORDER = HexColor("#D9E7E7")
FRAME_BORDER = HexColor("#BFD9D9")
FACE_FILL = HexColor("#FFF6D6")
TONGUE = HexColor("#F28B8B")

ASSETS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "small-moments")
OUT_DIR = os.path.expanduser("~/workspace/your_files/small-moments")


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


def _face(pdf, cx, cy, r, mood):
    """Small vector face for the feeling-words bank."""
    pdf.setFillColor(FACE_FILL)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.1)
    pdf.circle(cx, cy, r, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    if mood in ("proud", "calm"):
        # closed happy eyes: small upward arcs
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.2)
        pdf.arc(cx - 6.5, cy + 2, cx - 1.5, cy + 7, 0, 180)
        pdf.arc(cx + 1.5, cy + 2, cx + 6.5, cy + 7, 0, 180)
    else:
        pdf.circle(cx - 5, cy + 4, 1.6, stroke=0, fill=1)
        pdf.circle(cx + 5, cy + 4, 1.6, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.3)
    if mood == "surprised":
        pdf.circle(cx, cy - 4, 2.6, stroke=1, fill=0)
    elif mood == "silly":
        pdf.arc(cx - 5, cy - 8, cx + 5, cy + 2, 180, 180)
        pdf.setFillColor(TONGUE)
        pdf.roundRect(cx - 2, cy - 11, 4, 5, 2, stroke=0, fill=1)
    elif mood == "excited":
        pdf.arc(cx - 6, cy - 9, cx + 6, cy + 3, 180, 180)
        pdf.setFillColor(GOLD)
        pdf.circle(cx - 8, cy - 1, 1.4, stroke=0, fill=1)
        pdf.circle(cx + 8, cy - 1, 1.4, stroke=0, fill=1)
    elif mood == "calm":
        pdf.arc(cx - 4, cy - 7, cx + 4, cy + 1, 180, 180)
    else:  # happy, proud
        pdf.arc(cx - 5, cy - 8, cx + 5, cy + 2, 180, 180)


def _instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, text)


# ---------------------------------------------------------------------------
# Page 1 -- Plan Your Small Moment
# ---------------------------------------------------------------------------
def _plan_moment(pdf):
    _instruction(pdf, "Think of one small moment. Draw it in order.")
    _image_frame(pdf, os.path.join(ASSETS_DIR, "sm-moment-spark.jpg"),
                 40, 502, 170, 113)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(226, 600, "My small moment is:")
    _handwriting_lines(pdf, 226, 588, 346, rows=2)
    boxes = [
        ("Beginning", "What happened first?", TEAL),
        ("Middle", "What happened next?", NAVY),
        ("End", "How did it end?", CORAL),
    ]
    y_top = 486
    for label, hint, color in boxes:
        y0 = y_top - 118
        pdf.setStrokeColor(FRAME_BORDER)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, y0, 532, 118, 12, stroke=1, fill=0)
        pdf.setFillColor(color)
        pdf.roundRect(52, y0 + 84, 118, 26, 8, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawCentredString(52 + 59, y0 + 92, label)
        pdf.setFillColor(GRAY)
        pdf.setFont("Helvetica", 11)
        pdf.drawString(182, y0 + 92, hint)
        y_top = y0 - 10


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Plan Your Small Moment", title_size=20)
    _plan_moment(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Tell It in Order
# ---------------------------------------------------------------------------
def _tell_in_order(pdf):
    _instruction(pdf,
                 "Write what happened, in order. Use the time words.")
    words = [
        ("First", TEAL, HexColor("#FFFFFF")),
        ("Next", GOLD, NAVY),
        ("Last", NAVY, HexColor("#FFFFFF")),
    ]
    y_top = 620
    for word, color, text_color in words:
        y0 = y_top - 148
        pdf.setFillColor(PANEL)
        pdf.setStrokeColor(PANEL_BORDER)
        pdf.setLineWidth(1)
        pdf.roundRect(40, y0, 532, 148, 12, stroke=1, fill=1)
        pdf.setFillColor(color)
        pdf.roundRect(56, y0 + 57, 92, 34, 10, stroke=0, fill=1)
        pdf.setFillColor(text_color)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(56 + 46, y0 + 68, word)
        _handwriting_lines(pdf, 168, y0 + 132, 388, rows=3)
        y_top = y0 - 12
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 138,
        "Read your three sentences. Do they tell your moment in order?")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Tell It in Order", title_size=20)
    _tell_in_order(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Add a Detail
# ---------------------------------------------------------------------------
FEELINGS = ["happy", "excited", "proud", "surprised", "calm", "silly"]


def _add_detail(pdf):
    _instruction(pdf, "Add details to your moment.")
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(PANEL_BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 492, 532, 124, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(58, 596, "FEELING WORDS")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 10.5)
    pdf.drawString(180, 596, "Circle how you felt.")
    for i, word in enumerate(FEELINGS):
        col, row = i % 3, i // 3
        cx0 = 50 + col * 172
        cy0 = 548 - row * 48
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(PANEL_BORDER)
        pdf.setLineWidth(1)
        pdf.roundRect(cx0, cy0, 162, 42, 10, stroke=1, fill=1)
        _face(pdf, cx0 + 26, cy0 + 21, 13, word)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 15)
        pdf.drawString(cx0 + 46, cy0 + 15, word)
    prompts = [
        ("Who was with you?", 470),
        ("Where were you?", 350),
        ("How did you feel?", 230),
    ]
    for label, ly in prompts:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, ly, label)
        _handwriting_lines(pdf, 40, ly - 12, 532, rows=2)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Add a Detail", title_size=20)
    _add_detail(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Write Your Story (independent writing, no frames)
# ---------------------------------------------------------------------------
def _write_story(pdf):
    _instruction(pdf, "Write your whole small moment.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(PAGE_WIDTH / 2, 622,
                          "Use your plan, your time words, and your details.")
    pdf.setStrokeColor(FRAME_BORDER)
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 400, 532, 200, 12, stroke=1, fill=0)
    pdf.setFillColor(GUIDE)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(54, 578, "Draw your moment here.")
    _handwriting_lines(pdf, 40, 384, 532, rows=6)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Write Your Story", title_size=20)
    _write_story(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Make It Better
# ---------------------------------------------------------------------------
def _make_better(pdf):
    _instruction(pdf, "Read your story again. Make it better.")
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(PANEL_BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 500, 532, 116, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(58, 596, "CHECKLIST")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 10.5)
    pdf.drawString(150, 596, "Tick each box when it is true.")
    checks = [
        "Did I tell what happened first, next, and last?",
        "Did I add a detail?",
        "Did I end my story?",
    ]
    for i, text in enumerate(checks):
        y = 566 - i * 30
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.4)
        pdf.roundRect(58, y, 18, 18, 3, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 13)
        pdf.drawString(88, y + 4, text)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 468, "Add one more detail:")
    _handwriting_lines(pdf, 40, 458, 532, rows=3)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 306, "Revise your story:")
    pdf.setFillColor(PANEL)
    pdf.setStrokeColor(PANEL_BORDER)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 176, 532, 112, 12, stroke=1, fill=1)
    steps = [
        "Reread your story on Page 4.",
        "Choose one place to add a detail. Draw a star on Page 4.",
        "Write your detail into your story on Page 4.",
    ]
    for i, text in enumerate(steps):
        cy = 268 - i * 32
        pdf.setFillColor(TEAL)
        pdf.circle(68, cy, 10, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawCentredString(68, cy - 4, str(i + 1))
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 13)
        pdf.drawString(88, cy - 4, text)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 140,
                          "You wrote a real story. Great work!")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Make It Better", title_size=20)
    _make_better(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    ("Plan Your Small Moment", build_p1_page),
    ("Tell It in Order", build_p2_page),
    ("Add a Detail", build_p3_page),
    ("Write Your Story", build_p4_page),
    ("Make It Better", build_p5_page),
]


def main():
    pages_dir = os.path.join(OUT_DIR, "pages-v2")
    previews_dir = os.path.join(OUT_DIR, "previews")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(previews_dir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder) in enumerate(PAGES):
        p = os.path.join(pages_dir,
                         "small-moments-page-%02d.pdf" % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(OUT_DIR, "small-moments-my-narrative-v2.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)


if __name__ == "__main__":
    main()
