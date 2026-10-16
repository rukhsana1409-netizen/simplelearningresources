"""Story Sequencing -- First, Next & Last -- Kindergarten Reading
Comprehension.

Five pages on putting story events in order (the kindergarten form
of retelling: Michigan RL.K.2 / RL.K.3 with prompting and support).
The pack progresses from pictures already in order, to mixed-up
pictures, to choosing what happens next, to sequencing a read-aloud
story, to a four-step cut-and-paste sequence. Order is always
evident from the pictures themselves -- no outside knowledge is
needed. A parent answer key with a parent-friendly learning
objective is generated at finalization (not part of the bundle).

Pages:
  P1: First, Next, Last        (pictures in order)   (APPROVED + LOCKED
                                                      2026-10-15)
  P2: Put the Story in Order   (mixed-up pictures)   (APPROVED + LOCKED
                                                      2026-10-15)
  P3: What Happens Next?       (choose the ending)   (APPROVED + LOCKED
                                                      2026-10-16)
  P4: Sequence a Short Story   (read-aloud story)    (APPROVED + LOCKED
                                                      2026-10-16)
  P5: My Story Sequence        (cut-and-paste 1-4)   (APPROVED + LOCKED
                                                      2026-10-16)

Run with the repo venv:
  ../.venv/bin/python build_story_sequencing.py
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

PACK_TITLE = "Story Sequencing"
GRAY = HexColor("#37474F")
GOLD_FILL = HexColor("#FFF3D6")
GOLD_LINE = HexColor("#E4B93E")
GUIDE = HexColor("#7FA3B5")


def _panel(pdf, px0, py0, w, h):
    pdf.setFillColor(HexColor("#F4F9F9"))
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.roundRect(px0, py0, w, h, 14, stroke=1, fill=1)


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


def _number_box(pdf, cx, y0, w=48, h=52):
    """An empty box for the child to write a sequence number."""
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(GUIDE)
    pdf.setLineWidth(1.4)
    pdf.roundRect(cx - w / 2, y0, w, h, 8, stroke=1, fill=1)


# ---------------------------------------------------------------------------
# Page 1 -- First, Next, Last (teaching page: pictures IN ORDER)
# Building a snowman in three steps whose order is evident from the
# snowman's completeness alone: one big snowball -> two stacked
# snowballs, undecorated -> the finished snowman (carrot nose, coal
# smile, stick arms, scarf). A vocabulary strip ties FIRST/NEXT/LAST
# to 1/2/3; each picture is labeled and has an empty number box.
# ---------------------------------------------------------------------------
P1_STEPS = [  # (asset, word, number)
    ("story-sequencing/sq-snowman-1.jpg", "FIRST", "1"),
    ("story-sequencing/sq-snowman-2.jpg", "NEXT", "2"),
    ("story-sequencing/sq-snowman-3.jpg", "LAST", "3"),
]


def _first_next_last(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 636,
        "Look at the pictures. Tell what happens first, next, "
        "and last.")
    pdf.drawCentredString(PAGE_WIDTH / 2, 614, "Then write 1, 2, 3.")
    # vocabulary strip: FIRST 1 -> NEXT 2 -> LAST 3
    _panel(pdf, 40, 546, 532, 42)
    for i, (_rel, word, num) in enumerate(P1_STEPS):
        cx = 126 + i * 180
        pdf.setFillColor(HexColor("#EAF4F4"))
        pdf.setStrokeColor(TEAL)
        pdf.setLineWidth(0.9)
        pdf.roundRect(cx - 66, 552, 132, 30, 9, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawCentredString(cx, 562, "%s  %s" % (word, num))
        if i < 2:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawCentredString(cx + 90, 561, "\u2192")
    # three step panels
    for i, (rel, word, _num) in enumerate(P1_STEPS):
        px0 = 40 + i * 184
        cx = px0 + 82
        _panel(pdf, px0, 172, 164, 344)
        _scene(pdf, rel, px0 + 10, 342, 144, 162, ratio=144 / 162)
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 18)
        pdf.drawCentredString(cx, 314, word)
        _number_box(pdf, cx, 208)
        if i < 2:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawCentredString(px0 + 174, 416, "\u2192")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 128,
        "Adult: Talk about what happens first, next, and last. On "
        "this page, the pictures are in order.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "First, Next, Last")
    _first_next_last(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Put the Story in Order (pictures MIXED UP, no labels)
# A muddy puppy gets a bath in the backyard: mud-covered puppy by an
# empty tub -> puppy in the tub under soap bubbles -> clean, fluffy
# puppy wrapped in a towel. The state of the puppy (mud / suds /
# clean and dry) makes the order readable from the pictures alone.
# Displayed scrambled as [3, 1, 2]: the correct numbers across the
# page are 3, 1, 2, so the first box is NOT 1 -- no position hints,
# no FIRST/NEXT/LAST labels, no arrows.
# ---------------------------------------------------------------------------
P2_DISPLAY = [  # (asset, correct number) in display order
    ("story-sequencing/sq-pup-3.jpg", 3),
    ("story-sequencing/sq-pup-1.jpg", 1),
    ("story-sequencing/sq-pup-2.jpg", 2),
]


def _put_story_in_order(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 636,
                          "The pictures are mixed up.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 614,
        "Write 1, 2, 3 to put the story in order.")
    for i, (rel, _num) in enumerate(P2_DISPLAY):
        px0 = 40 + i * 184
        cx = px0 + 82
        _panel(pdf, px0, 190, 164, 330)
        _scene(pdf, rel, px0 + 10, 330, 144, 170, ratio=144 / 170)
        _number_box(pdf, cx, 222)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 140,
        "Adult: Ask your child to tell the story. Which picture "
        "happened first?")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Put the Story in Order")
    _put_story_in_order(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- What Happens Next? (two given events + choose the third)
# A bubble story told as a visible ladder, so the correct ending is
# the natural completion rather than a guess: the girl dips her wand
# in the bubble jar -> she blows and a small bubble forms -> one big
# bubble floats up. Distractors keep the same girl and garden but
# switch activities (riding a scooter, reading under a tree), so
# only one picture can complete THIS story. The story row carries
# printed 1 / 2 badges (given, not answers) and a dashed "?" panel
# for the missing step; the child circles one of three choices.
# ---------------------------------------------------------------------------
P3_STORY = [
    "story-sequencing/sq-bub-1.jpg",
    "story-sequencing/sq-bub-2.jpg",
]
P3_CHOICES = [  # (asset, is_correct) in display order
    ("story-sequencing/sq-bub-x1.jpg", False),
    ("story-sequencing/sq-bub-3.jpg", True),
    ("story-sequencing/sq-bub-x2.jpg", False),
]


def _badge(pdf, cx, cy, text):
    pdf.setFillColor(TEAL)
    pdf.setStrokeColor(TEAL)
    pdf.circle(cx, cy, 13, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setFont("Andika-Bold", 15)
    pdf.drawCentredString(cx, cy - 5.5, text)


def _what_happens_next(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 636,
                          "Look at the story. Circle what happens "
                          "next.")
    for i in range(3):
        px0 = 40 + i * 184
        if i < 2:
            _panel(pdf, px0, 396, 164, 210)
            _scene(pdf, P3_STORY[i], px0 + 10, 452, 144, 144,
                   ratio=1.0)
            _badge(pdf, px0 + 27, 579, str(i + 1))
        else:
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(GUIDE)
            pdf.setLineWidth(1.6)
            pdf.setDash(6, 4)
            pdf.roundRect(px0, 396, 164, 210, 14, stroke=1, fill=1)
            pdf.setDash()
            pdf.setFillColor(TEAL)
            pdf.setFont("Andika-Bold", 72)
            pdf.drawCentredString(px0 + 82, 478, "?")
        if i < 2:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawCentredString(px0 + 174, 494, "\u2192")
    for i, (rel, _ok) in enumerate(P3_CHOICES):
        px0 = 40 + i * 184
        _panel(pdf, px0, 176, 164, 168)
        _scene(pdf, rel, px0 + 10, 202, 144, 132, ratio=144 / 132)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 132,
        "Adult: Look at the two story pictures together. Ask: What "
        "happens next?")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Happens Next?")
    _what_happens_next(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Sequence a Short Story (read-aloud story, mixed-up events)
# Leo flies his red kite. The kite's height is the sequence cue:
# held in both hands at the ground -> lifting behind him as he runs
# -> soaring high while he holds the string. Story text sits in its
# own boxed panel, visually separate from the activity (standing
# preference). Events displayed [2, 3, 1], so the correct numbers
# across the page are 2, 3, 1 -- a different scramble from Page 2.
# ---------------------------------------------------------------------------
P4_STORY = [
    "Leo took his red kite to the park.",
    "Leo ran fast with his kite.",
    "The kite flew high in the sky. Leo smiled!",
]
P4_DISPLAY = [  # (asset, correct number) in display order
    ("story-sequencing/sq-kite-2.jpg", 2),
    ("story-sequencing/sq-kite-3.jpg", 3),
    ("story-sequencing/sq-kite-1.jpg", 1),
]


def _sequence_short_story(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 638,
        "Listen to the story. Write 1, 2, 3 to show the order.")
    _panel(pdf, 40, 500, 532, 122)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(218, 607, "THE STORY")
    _scene(pdf, "story-sequencing/sq-kite-story.jpg", 54, 510, 150,
           102, ratio=150 / 102)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 15)
    y = 580
    for line in P4_STORY:
        pdf.drawString(218, y, line)
        y -= 25
    for i, (rel, _num) in enumerate(P4_DISPLAY):
        px0 = 40 + i * 184
        cx = px0 + 82
        _panel(pdf, px0, 190, 164, 268)
        _scene(pdf, rel, px0 + 10, 316, 144, 132, ratio=144 / 132)
        _number_box(pdf, cx, 224)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 140,
        "Adult: Read the story aloud. Then ask your child to put "
        "the pictures in order.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Sequence a Short Story")
    _sequence_short_story(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- My Story Sequence (four steps, cut-and-paste numbers 1-4)
# Baking cookies: mixing dough -> shaping dough balls on a tray ->
# holding a tray of golden baked cookies -> eating a cookie. The
# dough's state makes the order evident. REDESIGNED 2026-10-16 at
# the user's direction: a spacious 2x2 grid with much larger
# pictures and bright flat artwork on plain backgrounds (the first
# version's muted watercolor kitchen scenes were too small,
# crowded, and detailed for kindergarten). Displayed [3, 1, 4, 2].
# Cut-and-paste contract: WORK AREA and CUT-OUT AREA clearly
# separated (warm-tinted strip with a scissors mark); number tiles
# are simple dashed squares cut at 48x48, slightly smaller than
# the 56x56 paste boxes, so each pasted number sits inside its
# box with a small margin all around. The compact strip leaves no
# room for an adult line on this page; adult guidance lives in the
# answer key.
# ---------------------------------------------------------------------------
P5_DISPLAY = [  # (asset, correct number) in display order
    ("story-sequencing/sq-cookie2-3.jpg", 3),
    ("story-sequencing/sq-cookie2-1.jpg", 1),
    ("story-sequencing/sq-cookie2-4.jpg", 4),
    ("story-sequencing/sq-cookie2-2.jpg", 2),
]


def _paste_box(pdf, cx, y0, size=56):
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(GUIDE)
    pdf.setLineWidth(1.4)
    pdf.roundRect(cx - size / 2, y0, size, size, 8, stroke=1, fill=1)


def _scissors(pdf, x, y):
    """A small scissors mark drawn with lines (the ZapfDingbats
    scissors glyph does not render in this environment). (x, y) is
    the center of the mark."""
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.6)
    pdf.circle(x - 5, y - 6, 3.1, stroke=1, fill=0)
    pdf.circle(x - 5, y + 6, 3.1, stroke=1, fill=0)
    pdf.line(x - 2.5, y - 4.5, x + 9, y + 7)
    pdf.line(x - 2.5, y + 4.5, x + 9, y - 7)


def _my_story_sequence(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 644,
        "Look at the pictures. Cut and paste the numbers in order.")
    positions = [(40, 452), (314, 452), (40, 228), (314, 228)]
    for (rel, _num), (px0, py0) in zip(P5_DISPLAY, positions):
        cx = px0 + 129
        _panel(pdf, px0, py0, 258, 166)
        _scene(pdf, rel, px0 + 8, py0 + 8, 242, 150, ratio=242 / 150)
        _paste_box(pdf, cx, py0 - 56)
    # --- CUT-OUT AREA (separate warm strip) ---
    pdf.setFillColor(HexColor("#FFF9EA"))
    pdf.setStrokeColor(GOLD_LINE)
    pdf.setLineWidth(1.1)
    pdf.roundRect(40, 72, 532, 84, 14, stroke=1, fill=1)
    _scissors(pdf, 64, 136)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(82, 132, "CUT OUT THE NUMBERS")
    for i in range(4):
        tx0 = 226 + i * 88 + 4
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(GUIDE)
        pdf.setLineWidth(1.4)
        pdf.setDash(5, 3)
        pdf.roundRect(tx0, 86, 48, 48, 6, stroke=1, fill=1)
        pdf.setDash()
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 25)
        pdf.drawCentredString(tx0 + 24, 102, str(i + 1))


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Story Sequence")
    _my_story_sequence(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("First, Next, Last", build_p1_page, True),  # APPROVED +
    # LOCKED 2026-10-15
    ("Put the Story in Order", build_p2_page, True),  # APPROVED +
    # LOCKED 2026-10-15
    ("What Happens Next?", build_p3_page, True),  # APPROVED +
    # LOCKED 2026-10-16
    ("Sequence a Short Story", build_p4_page, True),  # APPROVED +
    # LOCKED 2026-10-16
    ("My Story Sequence", build_p5_page, True),  # APPROVED +
    # LOCKED 2026-10-16
]


# ---------------------------------------------------------------------------
# Answer key (parent/teacher page, NOT part of the 5-page bundle)
# States the pack's learning objective in parent-friendly language
# and gives the answer for every page, with positions.
# ---------------------------------------------------------------------------
OBJECTIVE_LINES = [
    "This pack teaches your child to put story events in order \u2014",
    "what happens first, next, and last. Ordering events is the",
    "first step toward retelling a story, an important early",
    "reading skill. The pages grow step by step: naming first,",
    "next, and last; putting mixed-up pictures in order; choosing",
    "what happens next; sequencing a story read aloud; and",
    "ordering a four-step story with cut-and-paste numbers.",
]
ANSWER_BLOCKS = [
    ("Page 1 \u2014 First, Next, Last",
     ["The pictures are already in order. Write 1 under the big",
      "snowball (left), 2 under the two stacked snowballs (middle),",
      "and 3 under the finished snowman (right)."]),
    ("Page 2 \u2014 Put the Story in Order",
     ["Left to right, the numbers are 3, 1, 2. First (1) the muddy",
      "puppy by the empty tub (middle), next (2) the puppy in the",
      "soapy bath (right), last (3) the clean puppy in the towel (left)."]),
    ("Page 3 \u2014 What Happens Next?",
     ["Circle the middle picture: the big bubble floating in the",
      "air. The scooter and the book do not finish the bubble story."]),
    ("Page 4 \u2014 Sequence a Short Story",
     ["Left to right, the numbers are 2, 3, 1. First (1) Leo holds",
      "his kite (right), next (2) Leo runs and the kite lifts",
      "(left), last (3) the kite flies high (middle)."]),
    ("Page 5 \u2014 My Story Sequence",
     ["Paste 3 under the tray of baked cookies (top left), 1 under",
      "mixing the dough (top right), 4 under eating a cookie",
      "(bottom left), and 2 under shaping dough balls (bottom right)."]),
]


def build_answer_key(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Answer Key for Grown-Ups")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, 636, "WHAT YOUR CHILD IS LEARNING")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12)
    y = 612
    for line in OBJECTIVE_LINES:
        pdf.drawString(40, y, line)
        y -= 17
    y -= 10
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, y, "ANSWERS")
    y -= 24
    for title, lines in ANSWER_BLOCKS:
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, y, title)
        y -= 17
        pdf.setFont("Helvetica", 12)
        for line in lines:
            pdf.drawString(40, y, line)
            y -= 17
        y -= 8
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(
        40, y - 4,
        "Tip: After each page, ask your child to tell the story "
        "back: \u201cFirst\u2026 next\u2026 last\u2026\u201d")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def main():
    for title, _builder, locked in PAGES:
        assert locked, "Page not locked: %s" % title
    for line in OBJECTIVE_LINES:
        assert stringWidth(line, "Helvetica", 12) <= 532, line
    for _t, lines in ANSWER_BLOCKS:
        for line in lines:
            assert stringWidth(line, "Helvetica", 12) <= 532, line
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "worksheets", "kindergarten", "reading",
                          "story-sequencing")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(outdir, "story-sequencing-page-%02d.pdf"
                         % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(outdir, "story-sequencing-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)
    key = os.path.join(outdir, "story-sequencing-answer-key.pdf")
    build_answer_key(key)
    print("answer key: %s" % key)


if __name__ == "__main__":
    main()


def main():
    for title, builder, _locked in PAGES:
        tmp = "/tmp/sq_p.pdf"
        builder(tmp)
        print("built page: %s" % title)


if __name__ == "__main__":
    main()
