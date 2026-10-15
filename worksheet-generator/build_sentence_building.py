"""Building Simple Sentences -- Kindergarten Reading & Language
(Sentences & Mechanics).

Five pages moving from supported sentence construction to early
independent writing, aligned to Michigan K ELA (L.K.1f, L.K.2a/b,
RF.K.1c, W.K.2/3) and RCS Kindergarten expectations. Every sentence
uses only the 11 taught common words, true CVC words, and words
established in earlier packs. Deliberately distinct from Understanding
Print & Sentences (recognition-level mechanics) and Emergent
Decodable Reading (comprehension): here children PRODUCE sentences --
arrange, rewrite, repair, complete, and finally compose their own on
Kindergarten handwriting lines.

Pages:
  P1: Build a Sentence                      (APPROVED + LOCKED 2026-10-14)
  P2: Make a Sentence Longer                (APPROVED + LOCKED 2026-10-14)
  P3: Fix the Sentence                      (APPROVED + LOCKED 2026-10-14)
  P4: Finish the Sentence                   (APPROVED + LOCKED 2026-10-14)
  P5: Write Your Own Sentence               (APPROVED + LOCKED 2026-10-14)

Run with the repo venv:
  ../.venv/bin/python build_sentence_building.py
"""
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from build_phonics_az import (  # noqa: E402
    _ASSETS, INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
    draw_footer, draw_header, draw_logo, _img_circle,
)

PACK_TITLE = "Building Simple Sentences"
GRAY = HexColor("#37474F")
GUIDE = HexColor("#7FA3B5")


def _panel(pdf, px0, py0, w, h):
    pdf.setFillColor(HexColor("#F4F9F9"))
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.roundRect(px0, py0, w, h, 14, stroke=1, fill=1)


def _scissors(pdf, cx, cy):
    """Small scissors mark (vector, as in build_calendar_time.py)."""
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.8)
    pdf.setLineCap(1)
    pdf.circle(cx - 8, cy + 6, 4.2, stroke=1, fill=0)
    pdf.circle(cx - 8, cy - 6, 4.2, stroke=1, fill=0)
    pdf.line(cx - 4, cy + 4, cx + 10, cy - 8)
    pdf.line(cx - 4, cy - 4, cx + 10, cy + 8)
    pdf.setFillColor(TEAL)
    pdf.circle(cx + 2, cy, 1.6, stroke=0, fill=1)


def _handwriting_lines(pdf, x, y_top, width, rows=1):
    """One Kindergarten handwriting guide set: solid top and baseline
    with a dashed midline; the writing row is 30pt tall. y_top is the
    top line. Returns the baseline y of the last row."""
    y = y_top
    for _ in range(rows):
        pdf.setStrokeColor(GUIDE)
        pdf.setLineWidth(1)
        pdf.setDash()
        pdf.line(x, y, x + width, y)                    # top line
        pdf.setDash(4, 3)
        pdf.line(x, y - 15, x + width, y - 15)          # midline
        pdf.setDash()
        pdf.setLineWidth(1.4)
        pdf.line(x, y - 30, x + width, y - 30)          # baseline
        y -= 44
    return y + 44 - 30


def _scene(pdf, rel_path, x0, y0, w, h, ratio=1.45):
    """Draw an image inside a rounded-rectangle scene frame, center-
    cropped to the frame's ratio (as in build_decodable_reading.py)."""
    p = pdf.beginPath()
    p.roundRect(x0, y0, w, h, 10)
    pdf.saveState()
    pdf.clipPath(p, stroke=0, fill=0)
    path = os.path.join(_ASSETS, rel_path)
    iw, ih = ImageReader(path).getSize()
    scale = max(w / iw, h / (iw / ratio))
    sw = iw * scale
    sh = iw / ratio * scale
    pdf.drawImage(ImageReader(path), x0 + (w - sw) / 2,
                  y0 + (h - sh) / 2, sw, sh, mask="auto")
    pdf.restoreState()
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.2)
    pdf.roundRect(x0, y0, w, h, 10, stroke=1, fill=0)


# ---------------------------------------------------------------------------
# Page 1 -- Build a Sentence (cut and paste)
# Three builds: a picture, a strip of empty word-placement boxes (one
# per word, sized to the tiles), and a separated CUT-OUT AREA at the
# bottom holding each sentence's word tiles, shuffled within their
# set, on dashed cut borders. Each tile set forms exactly one
# sensible sentence. Work area and cut-out area are kept apart, per
# the cut-and-paste standard.
# ---------------------------------------------------------------------------
P1_BUILDS = [
    ("animal-library/lib-cat.jpg",
     ["The", "cat", "can", "sit"],
     ["can", "sit", "The", "cat"]),
    ("decodable-reading/edr-hen-crop.jpg",
     ["I", "can", "see", "a", "hen"],
     ["see", "hen", "I", "can", "a"]),
    ("sentence-building/bss-pup-run.jpg",
     ["The", "pup", "can", "run"],
     ["run", "The", "can", "pup"]),
]


def _build_a_sentence(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 640,
        "Cut the words. Glue them in order to make a sentence.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 306,
        "Adult: Help with cutting if needed. Read each finished "
        "sentence together.")
    # three build panels
    for i, (img, sentence, _tiles) in enumerate(P1_BUILDS):
        top = 626 - i * 110
        py0 = top - 88
        _panel(pdf, 40, py0, 532, 88)
        pdf.setFillColor(TEAL)
        pdf.roundRect(54, py0 + 63, 24, 20, 6, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawCentredString(66, py0 + 69, str(i + 1))
        _img_circle(pdf, img, 82, py0 + 30, 23, zoom=True)
        n = len(sentence)
        bw, gap = (84, 10) if n == 4 else (70, 8)
        x = 118
        for _w in sentence:
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(GUIDE)
            pdf.setLineWidth(1.2)
            pdf.roundRect(x, py0 + 24, bw, 40, 7, stroke=1, fill=1)
            x += bw + gap
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 20)
        pdf.drawString(x - gap + 2, py0 + 36, ".")
    # cut-out area
    py0 = 100
    pdf.setStrokeColor(GUIDE)
    pdf.setLineWidth(1.2)
    pdf.setDash(5, 4)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.roundRect(40, py0, 532, 196, 12, stroke=1, fill=1)
    pdf.setDash()
    _scissors(pdf, 66, py0 + 170)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(88, py0 + 165, "CUT-OUT AREA")
    for i, (_img, sentence, tiles) in enumerate(P1_BUILDS):
        n = len(sentence)
        # tiles are drawn smaller than their placement boxes, so a
        # glued tile sits comfortably inside its box
        bw, gap = (74, 20) if n == 4 else (62, 16)
        total = n * bw + (n - 1) * gap
        x = 118 + ((84 if n == 4 else 70) * n
                   + (10 if n == 4 else 8) * (n - 1) - total) / 2
        ty = py0 + 116 - i * 52
        for word in tiles:
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(GUIDE)
            pdf.setLineWidth(1.1)
            pdf.setDash(4, 3)
            pdf.roundRect(x, ty, bw, 36, 7, stroke=1, fill=1)
            pdf.setDash()
            pdf.setFillColor(NAVY)
            pdf.setFont("Andika-Bold", 19)
            pdf.drawCentredString(x + bw / 2, ty + 11, word)
            x += bw + gap


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Build a Sentence")
    _build_a_sentence(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Make a Sentence Longer
# The progression from Page 1: no cutting, no ordering -- the child
# EXPANDS a short printed sentence by adding a meaningful detail,
# then rewrites the complete new sentence on a spacious three-line
# handwriting guide. Each panel: picture (the detail is visible in
# it), the short sentence, a clearly labeled detail clue chip giving
# the exact words to add, and one writing row. Details: where (on
# the mat), what it looks like (red), how (fast -- the detail words
# are printed in the chip, so the child copies them into the new
# sentence).
# ---------------------------------------------------------------------------
P2_ITEMS = [
    ("sentence-building/bss-cat-nap.jpg", "The cat can nap.",
     "on the mat", "The cat can nap on the mat."),
    ("sentence-building/bss-red-bug.jpg", "I see a bug.",
     "red", "I see a red bug."),
    ("sentence-building/bss-pup-fast.jpg", "The pup can run.",
     "fast", "The pup can run fast."),
]


def _make_it_longer(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 640,
        "Read the sentence. Make it longer. Write the new sentence.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 96,
        "Adult: Help your child add the detail words. Write the "
        "whole new sentence.")
    for i, (img, short, detail, _full) in enumerate(P2_ITEMS):
        top = 628 - i * 174
        py0 = top - 160
        _panel(pdf, 40, py0, 532, 160)
        pdf.setFillColor(TEAL)
        pdf.roundRect(54, py0 + 128, 24, 20, 6, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawCentredString(66, py0 + 134, str(i + 1))
        _scene(pdf, img, 88, py0 + 58, 128, 88)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 20)
        pdf.drawString(238, py0 + 126, short)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawString(238, py0 + 98, "ADD THE DETAIL:")
        chip_w = stringWidth(detail, "Andika-Bold", 17) + 30
        pdf.setFillColor(HexColor("#FFF3D6"))
        pdf.setStrokeColor(HexColor("#E4B93E"))
        pdf.setLineWidth(1.2)
        pdf.roundRect(354, py0 + 84, chip_w, 30, 9, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 17)
        pdf.drawCentredString(354 + chip_w / 2, py0 + 93, detail)
        _handwriting_lines(pdf, 64, py0 + 42, 484)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Make a Sentence Longer")
    _make_it_longer(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Fix the Sentence
# Each sentence is printed with ONE kind of mistake (capital letter,
# word spacing, or end mark). The child rewrites it correctly on a
# spacious handwriting guide. A small hint names the KIND of fix --
# the corrected sentence is never shown anywhere on the page.
# ---------------------------------------------------------------------------
P3_ITEMS = [
    ("phonics-a-z/ph-sun.jpg", "the sun is up",
     "Use a capital letter. Add an end mark.", "The sun is up."),
    ("animal-library/lib-piglet.jpg", "ican see the pig",
     "Fix the capital I. Add a space and an end mark.",
     "I can see the pig."),
    ("decodable-reading/edr-hen-crop.jpg", "The hen is red",
     "Fix: add the end mark.", "The hen is red."),
]


def _fix_the_sentence(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 640,
        "Read the sentence. Fix it. Write it the right way.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 96,
        "Adult: Help your child fix the mistake and write the "
        "sentence the right way.")
    for i, (img, broken, hint, _fixed) in enumerate(P3_ITEMS):
        top = 628 - i * 174
        py0 = top - 160
        _panel(pdf, 40, py0, 532, 160)
        pdf.setFillColor(TEAL)
        pdf.roundRect(54, py0 + 128, 24, 20, 6, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawCentredString(66, py0 + 134, str(i + 1))
        _img_circle(pdf, img, 116, py0 + 92, 30, zoom=True)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 21)
        pdf.drawString(168, py0 + 100, broken)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawString(168, py0 + 74, hint)
        _handwriting_lines(pdf, 64, py0 + 46, 484)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Fix the Sentence")
    _fix_the_sentence(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Finish the Sentence
# Visually distinct from Pages 1-3: a wide scene, the sentence printed
# large with the writing guide built INTO the blank (top line, dashed
# midline, baseline at the sentence's own height), and a small word
# bank of three chips per activity. The picture makes exactly one
# bank word right. The child writes only the missing word.
# ---------------------------------------------------------------------------
P4_ITEMS = [
    ("sentence-building/bss-bug-log.jpg", "A bug is on a ", ".",
     ["rug", "log", "bus"], "log"),
    ("sentence-building/bss-red-van.jpg", "The ", " is red.",
     ["hen", "van", "cup"], "van"),
    ("decodable-reading/edr-ben-hug.jpg", "I can ", " the pup.",
     ["hug", "sip", "run"], "hug"),
]
_BLANK_W = 100


def _blank_guide(pdf, x, baseline):
    pdf.setStrokeColor(GUIDE)
    pdf.setLineWidth(1)
    pdf.setDash()
    pdf.line(x, baseline + 21, x + _BLANK_W, baseline + 21)
    pdf.setDash(4, 3)
    pdf.line(x, baseline + 10.5, x + _BLANK_W, baseline + 10.5)
    pdf.setDash()
    pdf.setLineWidth(1.4)
    pdf.line(x, baseline, x + _BLANK_W, baseline)


def _finish_the_sentence(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 640,
        "Look at the picture. Write the missing word.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 96,
        "Adult: Read the sentence together. The picture and the "
        "word bank help your child choose.")
    for i, (img, pre, post, bank, _ans) in enumerate(P4_ITEMS):
        top = 628 - i * 174
        py0 = top - 160
        _panel(pdf, 40, py0, 532, 160)
        pdf.setFillColor(TEAL)
        pdf.roundRect(54, py0 + 128, 24, 20, 6, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawCentredString(66, py0 + 134, str(i + 1))
        _scene(pdf, img, 88, py0 + 52, 148, 96, ratio=1.54)
        baseline = py0 + 108
        x = 258
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 21)
        pdf.drawString(x, baseline, pre)
        x += stringWidth(pre, "Andika-Bold", 21)
        _blank_guide(pdf, x, baseline)
        x += _BLANK_W
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 21)
        pdf.drawString(x, baseline, post)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(258, py0 + 76, "WORD BANK")
        cx = 258
        for word in bank:
            cw = stringWidth(word, "Andika-Bold", 16) + 28
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(GUIDE)
            pdf.setLineWidth(1.1)
            pdf.setDash(4, 3)
            pdf.roundRect(cx, py0 + 38, cw, 30, 8, stroke=1, fill=1)
            pdf.setDash()
            pdf.setFillColor(NAVY)
            pdf.setFont("Andika-Bold", 16)
            pdf.drawCentredString(cx + cw / 2, py0 + 47, word)
            cx += cw + 10


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Finish the Sentence")
    _finish_the_sentence(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Write Your Own Sentence
# The pack's most independent page: two fresh picture prompts (a
# child playing with a ball outdoors; a garden with a butterfly),
# two spacious handwriting rows each, a small Helping Words bank
# that supports spelling without prescribing any sentence, the
# writer's self-check, and an adult note welcoming invented
# spelling. No sentence is modeled anywhere on the page.
# ---------------------------------------------------------------------------
P5_PROMPTS = [
    "sentence-building/bss-ball-play.jpg",
    "sentence-building/bss-garden.jpg",
]
P5_HELPING = ["I", "see", "can", "like", "the", "is", "on", "a",
              "ball", "play", "sun", "red"]
P5_CHECKS = ["I start with a capital.", "I use spaces.",
             "I end with a mark."]


def _write_your_own(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 640,
        "Look at the picture. Write your own sentence.")
    for i, img in enumerate(P5_PROMPTS):
        top = 628 - i * 214
        py0 = top - 200
        _panel(pdf, 40, py0, 532, 200)
        pdf.setFillColor(TEAL)
        pdf.roundRect(54, py0 + 168, 24, 20, 6, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawCentredString(66, py0 + 174, str(i + 1))
        _scene(pdf, img, 88, py0 + 58, 156, 124, ratio=1.26)
        _handwriting_lines(pdf, 264, py0 + 140, 284, rows=2)
    # helping words bank
    pdf.setFillColor(HexColor("#F4F9F9"))
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.roundRect(40, 158, 532, 46, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(58, 189, "HELPING WORDS")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 15)
    words = "  \u00b7  ".join(P5_HELPING)
    pdf.drawCentredString(PAGE_WIDTH / 2, 169, words)
    # writer's self-check
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(58, 138, "MY WRITER'S CHECK")
    x = 58
    for text in P5_CHECKS:
        pdf.setStrokeColor(GUIDE)
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, 108, 14, 14, 3, stroke=1, fill=0)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 11.5)
        pdf.drawString(x + 20, 111, text)
        x += 20 + stringWidth(text, "Helvetica-Bold", 11.5) + 26
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 88,
        "Adult: Let your child say the sentence, then write it. "
        "Invented spelling is welcome.")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Write Your Own Sentence")
    _write_your_own(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Build a Sentence", build_p1_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Make a Sentence Longer", build_p2_page, True),  # APPROVED +
    # LOCKED 2026-10-14
    ("Fix the Sentence", build_p3_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Finish the Sentence", build_p4_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Write Your Own Sentence", build_p5_page, True),  # APPROVED +
    # LOCKED 2026-10-14
]


def main():
    for title, _builder, locked in PAGES:
        assert locked, "Page not locked: %s" % title
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "worksheets", "kindergarten", "reading",
                          "building-simple-sentences")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(outdir,
                         "building-simple-sentences-page-%02d.pdf"
                         % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(outdir,
                          "building-simple-sentences-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)


if __name__ == "__main__":
    main()
