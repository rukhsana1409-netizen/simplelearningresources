"""Emergent Decodable Reading -- Kindergarten Reading & Language
(Fluency).

Five pages of guided reading fluency and early comprehension. Every
word a child must read is either one of the 11 common words taught in
Common Words -- Read & Learn (the, a, I, is, it, in, on, can, see, my,
like) or a true short-vowel CVC word from the taught phonics. No
digraphs, blends, long vowels, or untaught sight words in any passage
(the only patterns beyond CVC are the taught see ee-team and, where
used, like's silent e). "Box" is read as established in Understanding
Print & Sentences. Support fades page by page: adult-modeled repeated
reading, then choice comprehension, writing from a word bank, drawing
from a description, and sequencing a story's events.

Pages:
  P1: Let's Read Together                   (LOCKED 2026-10-14)
  P2: Read & Choose                         (LOCKED 2026-10-14)
  P3: Read & Complete                       (LOCKED 2026-10-14)
  P4: Read & Draw                           (LOCKED 2026-10-14)
  P5: Read & Sequence                       (LOCKED 2026-10-14)

Run with the repo venv:
  ../.venv/bin/python build_decodable_reading.py
"""
import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from build_phonics_az import (  # noqa: E402
    INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
    draw_footer, draw_header, draw_logo, _img_circle,
)

PACK_TITLE = "Emergent Decodable Reading"
GRAY = HexColor("#37474F")


def _panel(pdf, px0, py0, w, h):
    pdf.setFillColor(HexColor("#F4F9F9"))
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.roundRect(px0, py0, w, h, 14, stroke=1, fill=1)


def _scene(pdf, rel_path, x, y, w, h):
    """Draw an illustration inside a rounded-corner frame."""
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "assets", rel_path)
    pdf.saveState()
    clip = pdf.beginPath()
    clip.roundRect(x, y, w, h, 10)
    pdf.clipPath(clip, stroke=0, fill=0)
    pdf.drawImage(img_path, x, y, w, h)
    pdf.restoreState()
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.roundRect(x, y, w, h, 10, stroke=1, fill=0)


# ---------------------------------------------------------------------------
# Page 1 -- Let's Read Together (fluency)
# A short decodable passage in a story panel with a scene illustration,
# then the three reading steps in a row (Listen -> Read Together ->
# Read Again), each with an empty circle the child colors on finishing
# that read. One small adult guidance line sits above the footer.
# No timers, no speed pressure.
# ---------------------------------------------------------------------------
P1_STORY = ["Sam is on a mat.",
            "A cat is on the mat.",
            "The cat can nap.",
            "Sam can pat the cat.",
            "The cat can sit on Sam.",
            "Sam can nap on the mat."]
P1_STEPS = [
    ("Listen", ["An adult reads the",
                "story. Follow the",
                "words with a finger."]),
    ("Read Together", ["Read the story",
                       "together. Say each",
                       "word nice and smooth."]),
    ("Read Again", ["Read the story on",
                    "your own.",
                    "You can do it!"]),
]



def _lets_read_together(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read the story three times.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 88,
        "Adult: Model the reading, read together, then let your "
        "child try independently.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Encourage accuracy and smooth reading without rushing.")
    # story panel
    py0 = 414
    _panel(pdf, 40, py0, 532, 216)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(56, py0 + 186, "THE STORY")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 20)
    for i, line in enumerate(P1_STORY):
        pdf.drawString(56, py0 + 152 - i * 26, line)
    _scene(pdf, "decodable-reading/edr-sam-cat.jpg",
           388, py0 + 52, 168, 112)
    # three steps in a row
    sw, sh = 168, 200
    for i, (title, lines) in enumerate(P1_STEPS):
        px0 = 40 + i * 182
        py0 = 162
        _panel(pdf, px0, py0, sw, sh)
        pdf.setFillColor(TEAL)
        pdf.roundRect(px0 + 14, py0 + sh - 38, 26, 22, 7, stroke=0,
                      fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(px0 + 27, py0 + sh - 31, str(i + 1))
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(px0 + 48, py0 + sh - 31, title)
        pdf.setFillColor(GRAY)
        pdf.setFont("Helvetica", 11)
        for j, line in enumerate(lines):
            pdf.drawString(px0 + 14, py0 + sh - 70 - j * 18, line)
        pdf.setStrokeColor(HexColor("#7FA3B5"))
        pdf.setLineWidth(1.4)
        pdf.circle(px0 + sw / 2, py0 + 32, 13, stroke=1, fill=0)
        pdf.setFillColor(GRAY)
        pdf.setFont("Helvetica", 8.5)
        pdf.drawCentredString(px0 + sw / 2, py0 + 52,
                              "Color when done")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Let's Read Together")
    _lets_read_together(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Read & Choose (comprehension)
# A new story, then three question panels. Each question has exactly
# one correct answer; choices are large word chips only (no choice
# pictures, so answers cannot be matched from the illustrations).
# Correct answers sit in different chip positions (2nd, 1st, 3rd).
# Story illustration shows Ben hugging the pup (no box), so Q1's
# answer cannot be read off the picture. Per the user's revision the
# story uses "The pup is glad." (not "not sad"); Q2's choices remain
# sad / mad / bad (glad carries the gl blend; bad is decodable).
# ---------------------------------------------------------------------------
P2_STORY = ["A pup is in a box.",
            "The pup is sad.",
            "Ben can hug the pup.",
            "The pup is glad.",
            "The pup can nap in the box."]
P2_QUESTIONS = [
    ("Where is the pup?", ["bed", "box", "rug"], "box"),
    ("How is the pup at first?", ["sad", "mad", "bad"], "sad"),
    ("What can Ben do?", ["pat", "sip", "hug"], "hug"),
]


def _read_and_choose(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read the story. Circle the right answer.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 88,
        "Adult: Read the story together first. Then let your child "
        "find each answer in the story.")
    # story panel
    py0 = 452
    _panel(pdf, 40, py0, 532, 178)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(56, py0 + 150, "THE STORY")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 20)
    for i, line in enumerate(P2_STORY):
        pdf.drawString(56, py0 + 122 - i * 27, line)
    _scene(pdf, "decodable-reading/edr-ben-hug.jpg",
           388, py0 + 33, 168, 112)
    # three question panels
    for i, (question, choices, _ans) in enumerate(P2_QUESTIONS):
        top = 436 - i * 108
        py0 = top - 92
        _panel(pdf, 40, py0, 532, 92)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawString(56, py0 + 62, "%d.  %s" % (i + 1, question))
        for c, word in enumerate(choices):
            bx = 56 + c * 172
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(HexColor("#7FA3B5"))
            pdf.setLineWidth(1.2)
            pdf.roundRect(bx, py0 + 12, 156, 40, 9, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Andika-Bold", 20)
            pdf.drawCentredString(bx + 78, py0 + 25, word)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Read & Choose")
    _read_and_choose(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Read & Complete (comprehension)
# A new story, a clearly separated word bank (pen / red / log -- each
# used exactly once), and three fill-in sentences with long writing
# lines. The story illustration is the pack's own hen picture: a plain
# hen with no pen and no log in frame, so two of the three answers
# live only in the text.
# ---------------------------------------------------------------------------
P3_STORY = ["A hen is in a pen.",
            "The hen is red.",
            "The hen can run.",
            "The hen can hop on a log.",
            "I see the hen."]
P3_BANK = ["pen", "red", "log"]
P3_ITEMS = [
    ("The hen is in a", "pen"),
    ("The hen is", "red"),
    ("The hen can hop on a", "log"),
]


def _blank_sentence(pdf, x0, baseline, prefix):
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 20)
    pdf.drawString(x0, baseline, prefix)
    bx = x0 + stringWidth(prefix + " ", "Andika-Bold", 20)
    pdf.setStrokeColor(HexColor("#7FA3B5"))
    pdf.setLineWidth(1.6)
    pdf.line(bx, baseline - 2, bx + 110, baseline - 2)
    pdf.setFillColor(NAVY)
    pdf.drawString(bx + 114, baseline, ".")


def _read_and_complete(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read the story. Write the missing words.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 88,
        "Adult: Read the story together first. The word bank has "
        "the words your child needs.")
    # story panel
    py0 = 470
    _panel(pdf, 40, py0, 532, 160)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(56, py0 + 132, "THE STORY")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 20)
    for i, line in enumerate(P3_STORY):
        pdf.drawString(56, py0 + 108 - i * 23, line)
    _img_circle(pdf, "decodable-reading/edr-hen-crop.jpg", 512,
                py0 + 80, 38, zoom=True)
    # word bank
    py0 = 398
    pdf.setStrokeColor(HexColor("#7FA3B5"))
    pdf.setLineWidth(1.2)
    pdf.setDash(5, 4)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.roundRect(40, py0, 532, 58, 12, stroke=1, fill=1)
    pdf.setDash()
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(58, py0 + 23, "Word Bank")
    for c, word in enumerate(P3_BANK):
        bx = 196 + c * 122
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(bx, py0 + 12, 106, 34, 8, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 19)
        pdf.drawCentredString(bx + 53, py0 + 22, word)
    # three fill-in panels
    for i, (prefix, _ans) in enumerate(P3_ITEMS):
        top = 382 - i * 88
        py0 = top - 76
        _panel(pdf, 40, py0, 532, 76)
        pdf.setFillColor(TEAL)
        pdf.roundRect(56, py0 + 27, 26, 22, 7, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(69, py0 + 34, str(i + 1))
        _blank_sentence(pdf, 104, py0 + 32, prefix)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Read & Complete")
    _read_and_complete(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Read & Draw (visualization)
# A short descriptive passage and one large blank drawing area. NO
# illustration anywhere: the child draws the picture the words make
# (a pond with a red fish, the sun up, a bug on a rock). The words
# fish / pond / rock are beyond the taught phonics (sh digraph, nd
# blend, ck digraph), so they are flagged as adult-supported: a soft
# dotted underline in the story and a naming line for the adult.
# ---------------------------------------------------------------------------
P4_LINES = ["A red fish is in a pond. The sun is up.",
            "A bug is on a rock."]
P4_NEW_WORDS = ["fish", "pond", "rock"]


def _dotted_under(pdf, x, y, word, size=20):
    w = stringWidth(word, "Andika-Bold", size)
    pdf.setStrokeColor(HexColor("#9DB8C4"))
    pdf.setLineWidth(1.4)
    pdf.setDash(0.5, 2.2)
    pdf.line(x, y, x + w, y)
    pdf.setDash()


def _read_and_draw(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read the story. Draw what you read.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 88,
        "Adult: The words fish, pond, and rock are new. Read them "
        "with your child.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Let your child sound out the rest, then draw what the "
        "words say.")
    # story panel
    py0 = 512
    _panel(pdf, 40, py0, 532, 118)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(56, py0 + 90, "THE STORY")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 20)
    for i, line in enumerate(P4_LINES):
        pdf.drawString(56, py0 + 56 - i * 32, line)
    # dotted flags under the adult-supported words
    y1 = py0 + 56 - 4
    x = 56 + stringWidth("A red ", "Andika-Bold", 20)
    _dotted_under(pdf, x, y1, "fish")
    x = 56 + stringWidth("A red fish is in a ", "Andika-Bold", 20)
    _dotted_under(pdf, x, y1, "pond")
    y2 = py0 + 24 - 4
    x = 56 + stringWidth("A bug is on a ", "Andika-Bold", 20)
    _dotted_under(pdf, x, y2, "rock")
    # one large blank drawing area
    dy0, dh = 116, 380
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.roundRect(40, dy0, 532, dh, 14, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, dy0 + dh - 26, "DRAW WHAT YOU READ")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Read & Draw")
    _read_and_draw(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Read & Sequence (comprehension)
# A kite story in four beats: flying the kite, the wind blows it
# into the tree, a man frees it with a long pole (named in the text
# and shown in the picture; no child climbs), and the children have
# it back, glad. The passage is as decodable as a natural story
# allows; the untaught words (and, fly, wind, blows, into, tree,
# has, back) are dotted in the text and named for the adult, the
# pack's Page 4 convention.
# "Kite" and "pole" follow the taught silent-e pattern of "like";
# "by" follows "my"; "glad" was read on Page 2. Four event pictures
# each with a large empty answer box beneath for the numbers 1-4.
# ---------------------------------------------------------------------------
P5_LINES = [
    "Sam, Pam, and Tom fly a big kite.",
    "The wind blows the kite into the tree.",
    "A man has a pole. The man can get the kite.",
    "The kite is back.",
    "Sam is glad. Pam is glad. Tom is glad.",
]
P5_FLAGS = [
    (0, "Sam, Pam, ", "and"),
    (0, "Sam, Pam, and Tom ", "fly"),
    (1, "The ", "wind"),
    (1, "The wind ", "blows"),
    (1, "The wind blows the kite ", "into"),
    (1, "The wind blows the kite into the ", "tree"),
    (2, "A man ", "has"),
    (3, "The kite is ", "back"),
]
P5_FLAG_WORDS = ["and", "fly", "wind", "blows", "into", "tree",
                 "has", "back"]
# display order: (image, story number)
P5_CELLS = [("edr-kite-3-pole-wide.jpg", 3),
            ("edr-kite-1-fly-wide.jpg", 1),
            ("edr-kite-4-back-wide.jpg", 4),
            ("edr-kite-2-stuck-wide.jpg", 2)]


def _read_and_sequence(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read the story. Number the pictures in "
                          "order.")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 88,
        "Adult: Read the story together first. Help your child "
        "with the dotted words:")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "and, fly, wind, blows, into, tree, has, back. Then let "
        "your child number the pictures.")
    # story panel
    py0 = 478
    _panel(pdf, 40, py0, 532, 152)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(56, py0 + 126, "THE STORY")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 19)
    line_y = []
    for i, line in enumerate(P5_LINES):
        y = py0 + 102 - i * 22
        line_y.append(y)
        pdf.drawString(56, y, line)
    for line_idx, prefix, word in P5_FLAGS:
        x = 56 + stringWidth(prefix, "Andika-Bold", 19)
        _dotted_under(pdf, x, line_y[line_idx] - 4, word, size=19)
    # 2 x 2 picture grid, shuffled
    for idx, (img, _num) in enumerate(P5_CELLS):
        px0 = 40 + (idx % 2) * 274
        py0 = 291 if idx < 2 else 108
        _panel(pdf, px0, py0, 258, 171)
        _scene(pdf, "decodable-reading/" + img, px0 + 8, py0 + 47,
               242, 124)
        bx = px0 + 258 / 2 - 23
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(HexColor("#7FA3B5"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(bx, py0 + 7, 46, 32, 7, stroke=1, fill=1)


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Read & Sequence")
    _read_and_sequence(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Let's Read Together", build_p1_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Read & Choose", build_p2_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Read & Complete", build_p3_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Read & Draw", build_p4_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Read & Sequence", build_p5_page, True),  # APPROVED + LOCKED
    # 2026-10-14
]


def main():
    for title, _builder, locked in PAGES:
        assert locked, "Page not locked: %s" % title
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "worksheets", "kindergarten", "reading",
                          "emergent-decodable-reading")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(outdir,
                         "emergent-decodable-reading-page-%02d.pdf"
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
                          "emergent-decodable-reading-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)


if __name__ == "__main__":
    main()
