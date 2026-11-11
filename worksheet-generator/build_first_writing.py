"""My First Writing Adventures -- Kindergarten Reading & Language
(Early Writing).

Five pages moving from supported writing to independent expression,
aligned to Michigan K ELA W.K.2 (informative), W.K.3 (narrative),
W.K.5 (add details), and L.K.1-2 (sentence formation and
conventions), and to the Kindergarten writing descriptors in RCS's
public standards-based report-card family guide. Deliberately
distinct from Building Simple Sentences: nothing here arranges,
expands, fixes, or completes given text -- the child GENERATES the
writing, mostly about their own drawing, growing from single labels
to connected multi-sentence text. Phonetic / invented spelling is
accepted and welcomed throughout.

Pages:
  P1: Label My Picture                      (APPROVED + LOCKED 2026-10-14)
  P2: Draw and Tell                         (APPROVED + LOCKED 2026-10-14)
  P3: Tell What Happened                    (APPROVED + LOCKED 2026-10-14)
  P4: Add More Details                      (APPROVED + LOCKED 2026-10-14;
                                             pastel question chips +
                                             transparent house art)
  P5: My Little Story                       (APPROVED + LOCKED 2026-10-14)

Run with the repo venv:
  ../.venv/bin/python build_first_writing.py
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

PACK_TITLE = "My First Writing Adventures"
GRAY = HexColor("#37474F")
GUIDE = HexColor("#7FA3B5")


def _panel(pdf, px0, py0, w, h):
    pdf.setFillColor(HexColor("#F4F9F9"))
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.roundRect(px0, py0, w, h, 14, stroke=1, fill=1)


def _handwriting_lines(pdf, x, y_top, width, rows=1):
    """Kindergarten handwriting guide set(s): solid top and baseline
    with a dashed midline; each writing row is 30pt tall."""
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


def _scene(pdf, rel_path, x0, y0, w, h, ratio):
    """Draw an image inside a rounded-rectangle scene frame, center-
    cropped to the frame's ratio."""
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
# Page 1 -- Label My Picture
# A cheerful park scene with six clearly identifiable items (sun,
# tree, slide, dog, ball, grass). Each item gets a white label chip
# inside the scene -- mini three-line handwriting guide inside -- and
# a thin leader line with a dot on the item. Chip positions are set
# against the exact wide crop (mfwa-park-wide.jpg), so leaders land
# on their items. The Picture Words bank sits BELOW the scene
# (support to consult after trying, per the adult line). An optional
# "Tell more if you want" writing area closes the page -- clearly
# the child's choice, not a requirement.
# (word, chip x, chip y, leader start x, leader start y, dot x, dot y)
# ---------------------------------------------------------------------------
P1_LABELS = [
    ("tree", 52, 566, 160, 562, 173, 549),
    ("sun", 436, 516, 470, 552, 438, 578),
    ("slide", 446, 384, 455, 420, 447, 448),
    ("dog", 52, 352, 170, 382, 243, 392),
    ("grass", 52, 304, 110, 340, 105, 349),
    ("ball", 440, 304, 440, 330, 390, 344),
]
P1_BANK = ["sun", "dog", "ball", "tree", "grass", "slide"]
SCENE = (40, 298, 532, 330)


def _label_chip(pdf, x, y):
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(GUIDE)
    pdf.setLineWidth(1.1)
    pdf.roundRect(x, y, 118, 36, 8, stroke=1, fill=1)
    pdf.setStrokeColor(GUIDE)
    pdf.setLineWidth(0.9)
    pdf.setDash()
    pdf.line(x + 10, y + 27, x + 108, y + 27)
    pdf.setDash(3, 3)
    pdf.line(x + 10, y + 18, x + 108, y + 18)
    pdf.setDash()
    pdf.setLineWidth(1.2)
    pdf.line(x + 10, y + 9, x + 108, y + 9)


def _label_my_picture(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 642,
        "Look at the picture. Label each part.")
    sx, sy, sw, sh = SCENE
    _scene(pdf, "first-writing/mfwa-park-wide.jpg", sx, sy, sw, sh,
           ratio=sw / sh)
    for _w, cx, cy, lx, ly, dx, dy in P1_LABELS:
        pdf.setStrokeColor(GUIDE)
        pdf.setLineWidth(1.1)
        pdf.line(lx, ly, dx, dy)
        pdf.setFillColor(GUIDE)
        pdf.circle(dx, dy, 2.6, stroke=0, fill=1)
        _label_chip(pdf, cx, cy)
    # picture words bank
    pdf.setFillColor(HexColor("#F4F9F9"))
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.roundRect(40, 244, 532, 42, 12, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(58, 261, "PICTURE WORDS")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 15)
    pdf.drawString(172, 259, "  \u00b7  ".join(P1_BANK))
    # optional telling lines
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 218, "Tell more if you want:")
    _handwriting_lines(pdf, 40, 208, 532, rows=2)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 104,
        "Adult: Let your child try their own spelling first. The "
        "Picture Words are there to help.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Label My Picture")
    _label_my_picture(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Draw and Tell
# The child draws something they like to do in a large, genuinely
# blank drawing frame (nothing pre-drawn, nothing decorative inside),
# then writes about their own drawing on three spacious handwriting
# rows. A small support strip offers three optional sentence
# starters. The adult note has the child describe the drawing aloud
# before writing, and welcomes invented spelling.
# ---------------------------------------------------------------------------
def _draw_and_tell(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Draw something you like to do.")
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 316, 532, 308, 12, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 292, "Now write about your drawing:")
    _handwriting_lines(pdf, 40, 282, 532, rows=3)
    # optional starting-words strip
    _panel(pdf, 40, 100, 532, 42)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(58, 117, "STARTING WORDS")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 16)
    pdf.drawString(196, 115,
                   "I like to...   \u00b7   I can...   \u00b7   This is...")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 78,
        "Adult: Ask your child to tell about the drawing first, then "
        "write. Invented spelling is welcome.")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Draw and Tell")
    _draw_and_tell(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Tell What Happened
# A three-step picture sequence of one everyday event -- a block
# tower: (1) the child begins a short stack, (2) a tall tower,
# (3) the tower fallen, the child laughing. The same child, blocks,
# and playroom appear throughout, and the order is obvious from the
# pictures alone. Each panel pairs its picture with a printed time
# word (First / Next / Last) as a visual support and TWO handwriting
# rows; no sentence is provided -- the child generates the words.
# ---------------------------------------------------------------------------
P3_STEPS = [
    ("first-writing/mfwa-tower-1.jpg", "First"),
    ("first-writing/mfwa-tower-2.jpg", "Next"),
    ("first-writing/mfwa-tower-3.jpg", "Last"),
]


def _tell_what_happened(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Look at the pictures. Write what happened.")
    for row, (img, word) in enumerate(P3_STEPS):
        py0 = 626 - row * 174 - 152
        _panel(pdf, 40, py0, 532, 152)
        _scene(pdf, img, 52, py0 + 12, 168, 128, ratio=168 / 128)
        pdf.setFillColor(HexColor("#FFF3D6"))
        pdf.setStrokeColor(HexColor("#E4B93E"))
        pdf.setLineWidth(1)
        wch = stringWidth(word, "Andika-Bold", 17) + 28
        pdf.roundRect(224, py0 + 114, wch, 26, 9, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 17)
        pdf.drawString(224 + 14, py0 + 120, word)
        _handwriting_lines(pdf, 224, py0 + 102, 336, rows=2)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 100,
        "Adult: The time words First, Next, and Last help your child "
        "tell the event in order.")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Tell What Happened")
    _tell_what_happened(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Add More Details (W.K.5)
# A before-and-after revision page. TOP: the plain line-art house
# (mfwa-house-crop.png, transparent background so it blends into
# the panel) with the plain printed sentence "The house is big."
# MIDDLE: three guiding questions on subtle pastel chips -- the
# "feedback" the child responds to. BELOW: a large white drawing
# area containing THE SAME plain house at a bigger size, so the
# child adds their own invented details (color, people, trees,
# flowers...) directly to the scene -- no word bank, nothing to
# choose from -- followed by two handwriting rows for one or two
# improved sentences. Because the starting house is identical in
# both places, the improvement is visible at a glance.
# ---------------------------------------------------------------------------
P4_QUESTIONS = [
    ("What color is the house?", "#FFF3D6", "#E3C878"),
    ("Who is there?", "#E8F3FA", "#A9CCE3"),
    ("What else can you see?", "#FDECEC", "#F0B4B4"),
]


def _contain(pdf, rel_path, x0, y0, w, h):
    """Draw an image fully inside a box, preserving its aspect."""
    path = os.path.join(_ASSETS, rel_path)
    iw, ih = ImageReader(path).getSize()
    s = min(w / iw, h / ih)
    dw, dh = iw * s, ih * s
    pdf.drawImage(ImageReader(path), x0 + (w - dw) / 2,
                  y0 + (h - dh) / 2, dw, dh, mask="auto")


def _add_more_details(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 642,
        "Look at the house. Add more details to make it better.")
    # BEFORE panel (image first, so it can never cover the label)
    _panel(pdf, 40, 480, 532, 146)
    _contain(pdf, "first-writing/mfwa-house-crop.png", 64, 484, 170,
             110)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 606, "THE FIRST DRAWING")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 26)
    pdf.drawString(262, 545, "The house is big.")
    # guiding questions on pastel chips
    widths = [stringWidth(q, "Andika-Bold", 14.5) + 24
              for q, _f, _b in P4_QUESTIONS]
    total = sum(widths) + 9 * (len(widths) - 1)
    qx = (PAGE_WIDTH - total) / 2
    for (q, fill, border), wch in zip(P4_QUESTIONS, widths):
        pdf.setFillColor(HexColor(fill))
        pdf.setStrokeColor(HexColor(border))
        pdf.setLineWidth(1)
        pdf.roundRect(qx, 420, wch, 48, 12, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 14.5)
        pdf.drawCentredString(qx + wch / 2, 438, q)
        qx += wch + 9
    # drawing area with the same plain house
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 398,
                   "Your turn: add your details to the picture:")
    _contain(pdf, "first-writing/mfwa-house-crop.png", 40, 216, 532,
             172)
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 216, 532, 172, 12, stroke=1, fill=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 192, "Now write your better sentences:")
    _handwriting_lines(pdf, 40, 182, 532, rows=2)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 80,
        "Adult: Questions help writers add details. New details make "
        "the writing stronger.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Add More Details")
    _add_more_details(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- My Little Story
# The pack's independent capstone: a child-led story planner with a
# title line and three connected sections -- Beginning / Middle /
# End -- each with a generous blank drawing space (side by side with
# the writing, so the drawing box keeps usable proportions), ONE
# spacious handwriting row, and a small First / Next / Last reminder
# chip carried over from Page 3. No prewritten sentences, no word
# bank, no printed story pictures: the story is entirely the
# child's. One short sentence per part is plenty; labels and phrases
# are full successes for emerging writers (adult line).
# ---------------------------------------------------------------------------
P5_SECTIONS = [("BEGINNING", "First"), ("MIDDLE", "Next"),
               ("END", "Last")]


def _my_little_story(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Plan your story. Draw and write each part.")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 620, "My story is about:")
    _handwriting_lines(pdf, 40, 612, 532, rows=1)
    for row, (section, time_word) in enumerate(P5_SECTIONS):
        py0 = 570 - row * 158 - 150
        _panel(pdf, 40, py0, 532, 150)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(54, py0 + 126, section)
        pdf.setFillColor(HexColor("#FFF3D6"))
        pdf.setStrokeColor(HexColor("#E4B93E"))
        pdf.setLineWidth(1)
        wch = stringWidth(time_word, "Andika-Bold", 13.5) + 24
        pdf.roundRect(556 - wch, py0 + 118, wch, 24, 8, stroke=1,
                      fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 13.5)
        pdf.drawCentredString(556 - wch / 2, py0 + 123.5, time_word)
        # drawing space: white, blank, generous
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(HexColor("#BFD9D9"))
        pdf.setLineWidth(1.3)
        pdf.roundRect(54, py0 + 14, 268, 98, 10, stroke=1, fill=1)
        # one spacious handwriting row beside it
        _handwriting_lines(pdf, 338, py0 + 84, 218, rows=1)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 82,
        "Adult: Your child tells the story. A word, a phrase, or one "
        "sentence for each part is fine.")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Little Story")
    _my_little_story(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Label My Picture", build_p1_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Draw and Tell", build_p2_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Tell What Happened", build_p3_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Add More Details", build_p4_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("My Little Story", build_p5_page, True),  # APPROVED +
    # LOCKED 2026-10-14
]


def main():
    for title, _builder, locked in PAGES:
        assert locked, "Page not locked: %s" % title
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "worksheets", "kindergarten", "reading",
                          "my-first-writing-adventures")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(
            outdir, "my-first-writing-adventures-page-%02d.pdf"
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
                          "my-first-writing-adventures-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)


if __name__ == "__main__":
    main()
