#!/usr/bin/env python3
"""Story Retelling -- Beginning, Middle & End.

Kindergarten Reading & Language (Literature / retelling). Five
pages that teach children to understand a story as three parts --
beginning, middle, end -- and to retell it. Companion to (and
distinct from) Story Sequencing, which taught ORDER with numbers
1-4; this pack teaches story PARTS and telling the story back.

  P1: Beginning, Middle & End  (three-part story intro)  (APPROVED +
                                                          LOCKED
                                                          2026-10-16)
  P2: Tell the Story           (picture prompts)        (APPROVED +
                                                          LOCKED
                                                          2026-10-16)
  P3: What Happened in the Middle? (choose the missing  (APPROVED +
      middle event)                                       LOCKED
                                                          2026-10-16)
  P4: Retell a Short Story     (read-aloud story)       (APPROVED +
                                                          LOCKED
                                                          2026-10-16)
  P5: My Story Retelling       (draw-and-retell)        (APPROVED +
                                                          LOCKED
                                                          2026-10-16)

Header/logo/helpers are imported verbatim from build_phonics_az.py
(the canonical Learn My Letters header). Local helpers (_panel,
_scene) follow the same pattern as build_story_sequencing.py.

Run from this directory with the repo venv python:
    ../.venv/bin/python build_story_retelling.py
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

PACK_TITLE = "Story Retelling"
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


# ---------------------------------------------------------------------------
# Page 1 -- Beginning, Middle & End (introduce the three story parts)
# Mia's rainy day told in three labeled panels: dark clouds gather
# (beginning) -> rain pours and she splashes in a puddle (middle) ->
# the sun comes out with a rainbow (end). The weather makes each
# part visually unmistakable. Each panel carries the part's name and
# two short read-aloud sentences; the child only listens and looks.
# ---------------------------------------------------------------------------
P1_PARTS = [  # (label, asset, sentence lines)
    ("BEGINNING", "story-retelling/rt-rain-1.jpg",
     ["Dark clouds come.", "Mia gets her umbrella."]),
    ("MIDDLE", "story-retelling/rt-rain-2.jpg",
     ["Rain falls down.", "Mia splashes. Splash!"]),
    ("END", "story-retelling/rt-rain-3.jpg",
     ["The sun comes out.", "Mia sees a rainbow!"]),
]


def _three_parts(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 636, "Listen to the story.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 614,
        "A story has a beginning, a middle, and an end.")
    _panel(pdf, 40, 532, 532, 44)
    flow = [("BEGINNING", NAVY), ("\u2192", TEAL), ("MIDDLE", NAVY),
            ("\u2192", TEAL), ("END", NAVY)]
    widths = [stringWidth(t, "Helvetica-Bold", 13.5) for t, _c in flow]
    x = PAGE_WIDTH / 2 - (sum(widths) + 12 * (len(flow) - 1)) / 2
    pdf.setFont("Helvetica-Bold", 13.5)
    for (text, color), w in zip(flow, widths):
        pdf.setFillColor(color)
        pdf.drawString(x, 549.5, text)
        x += w + 12
    for i, (label, rel, lines) in enumerate(P1_PARTS):
        px0 = 40 + i * 184
        cx = px0 + 82
        _panel(pdf, px0, 208, 164, 288)
        _scene(pdf, rel, px0 + 10, 344, 144, 142, ratio=144 / 142)
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 16)
        pdf.drawCentredString(cx, 318, label)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 12)
        y = 290
        for line in lines:
            pdf.drawCentredString(cx, y, line)
            y -= 20
        if i < 2:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawCentredString(px0 + 174, 418, "\u2192")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 140,
        "Adult: Read the story aloud. Point to each part: the "
        "beginning, the middle, and the end.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Beginning, Middle & End")
    _three_parts(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Tell the Story (retell from picture prompts)
# A new story: a boy and his red cap. He puts the cap on
# (beginning) -> the wind blows it away and he chases it (middle)
# -> he puts it back on, laughing (end). Unlike Page 1 there are NO
# sentences on the panels: each part carries only its name and the
# prompt "What happens here?", so the child retells each part in
# their own words instead of reading ours.
# ---------------------------------------------------------------------------
P2_PARTS = [  # (label, asset)
    ("BEGINNING", "story-retelling/rt-hat-1.jpg"),
    ("MIDDLE", "story-retelling/rt-hat-2.jpg"),
    ("END", "story-retelling/rt-hat-3.jpg"),
]


def _tell_the_story(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 636,
        "Look at the pictures. Tell the story in your own words.")
    for i, (label, rel) in enumerate(P2_PARTS):
        px0 = 40 + i * 184
        cx = px0 + 82
        _panel(pdf, px0, 216, 164, 314)
        _scene(pdf, rel, px0 + 10, 356, 144, 164, ratio=144 / 164)
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 16)
        pdf.drawCentredString(cx, 328, label)
        pdf.setFillColor(HexColor("#5E7A8A"))
        pdf.setFont("Andika-Bold", 11.5)
        pdf.drawCentredString(cx, 300, "What happens here?")
        if i < 2:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawCentredString(px0 + 174, 430, "\u2192")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 148,
        "Adult: Let your child tell each part in their own words. "
        "Ask: What happens here?")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Tell the Story")
    _tell_the_story(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- What Happened in the Middle? (choose the missing event)
# A third story, told by its two ends: a girl holds an EMPTY cone at
# the ice-cream cart and points at the pink flavor (beginning); the
# same girl sits on a bench happily eating a tall pink cone (end).
# The middle frame is empty ("?"). Of the three choices, only the
# vendor scooping pink ice cream onto her cone (middle choice)
# connects the two ends; the bicycle and the swing keep the same
# girl but belong to no ice-cream story. The vendor (older woman,
# glasses, blue apron) and the cart are the same in the beginning
# and the correct middle.
# ---------------------------------------------------------------------------
P3_GIVEN = [  # (label, asset or None for the missing middle)
    ("BEGINNING", "story-retelling/rt-ice-b.jpg"),
    ("MIDDLE", None),
    ("END", "story-retelling/rt-ice-e.jpg"),
]
P3_CHOICES = [  # the correct middle is the MIDDLE choice
    "story-retelling/rt-ice-x2.jpg",  # swinging (wrong)
    "story-retelling/rt-ice-m.jpg",   # vendor scoops her cone
    "story-retelling/rt-ice-x1.jpg",  # riding a bicycle (wrong)
]


def _missing_middle(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 636,
        "Look at the beginning and the end.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 614, "Circle what happens in the middle.")
    for i, (label, rel) in enumerate(P3_GIVEN):
        px0 = 40 + i * 184
        cx = px0 + 82
        _panel(pdf, px0, 396, 164, 210)
        if rel is not None:
            _scene(pdf, rel, px0 + 10, 452, 144, 130,
                   ratio=144 / 130)
        else:
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(GUIDE)
            pdf.setLineWidth(1.4)
            pdf.setDash(5, 3)
            pdf.roundRect(px0 + 10, 452, 144, 130, 10, stroke=1,
                          fill=1)
            pdf.setDash()
            pdf.setFillColor(TEAL)
            pdf.setFont("Andika-Bold", 64)
            pdf.drawCentredString(cx, 488, "?")
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 13.5)
        pdf.drawCentredString(cx, 424, label)
        if i < 2:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawCentredString(px0 + 174, 494, "\u2192")
    for i, rel in enumerate(P3_CHOICES):
        px0 = 40 + i * 184
        _panel(pdf, px0, 168, 164, 176)
        _scene(pdf, rel, px0 + 10, 194, 144, 132, ratio=144 / 132)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 124,
        "Adult: Talk about the beginning and the end. Ask: What "
        "must happen in the middle?")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Happened in the Middle?")
    _missing_middle(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Retell a Short Story (read-aloud, then retell by parts)
# A fourth story: Lily and her teddy bear. The boxed story panel is
# read aloud by an adult (three lines, one per part); below, the
# three events appear IN ORDER with their part labels and the
# familiar "What happens here?" prompt, so the child retells the
# beginning, middle, and end in their own words. There are NO
# numbers and nothing to order -- the pictures are already in story
# order; the work is the telling.
#   Beginning: Lily plays with Teddy on a blanket in the garden.
#   Middle:    Teddy is lost; Lily searches under a bush, worried.
#   End:       Lily finds Teddy behind the flower pots and hugs
#              him tight.
# ---------------------------------------------------------------------------
P4_STORY_LINES = [
    "Lily played with Teddy in the garden.",
    "Oh no! Teddy was lost. Lily looked and looked.",
    "Lily found Teddy! She hugged him tight.",
]
P4_EVENTS = [  # (label, asset) in story order
    ("BEGINNING", "story-retelling/rt-ted-1.jpg"),
    ("MIDDLE", "story-retelling/rt-ted-2.jpg"),
    ("END", "story-retelling/rt-ted-3.jpg"),
]


def _retell_short_story(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 638,
        "Listen to the story. Then tell it in your own words.")
    _panel(pdf, 40, 500, 532, 122)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(218, 607, "THE STORY")
    _scene(pdf, "story-retelling/rt-ted-story.jpg", 54, 510, 150,
           102, ratio=150 / 102)
    pdf.setFillColor(INK)
    pdf.setFont("Andika-Bold", 15)
    y = 578
    for line in P4_STORY_LINES:
        pdf.drawString(218, y, line)
        y -= 25
    for i, (label, rel) in enumerate(P4_EVENTS):
        px0 = 40 + i * 184
        cx = px0 + 82
        _panel(pdf, px0, 190, 164, 268)
        _scene(pdf, rel, px0 + 10, 316, 144, 132, ratio=144 / 132)
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 14)
        pdf.drawCentredString(cx, 288, label)
        pdf.setFillColor(HexColor("#5E7A8A"))
        pdf.setFont("Andika-Bold", 11.5)
        pdf.drawCentredString(cx, 262, "What happens here?")
        if i < 2:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawCentredString(px0 + 174, 388, "\u2192")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 140,
        "Adult: Read the story aloud. Then let your child retell "
        "the beginning, middle, and end.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Retell a Short Story")
    _retell_short_story(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- My Story Retelling (draw and retell)
# A fifth story in bright flat art (plain backgrounds, bold simple
# shapes): a boy spots a big orange butterfly on a flower
# (beginning) -> follows it through the garden (middle) -> it lands
# on his fingertip (end). Under each picture prompt is a large
# empty drawing box where the child draws the part in their own
# way -- their own butterfly, their own garden -- and then tells
# each part OUT LOUD. There are no writing lines: the retelling is
# oral, as the adult line states.
# ---------------------------------------------------------------------------
P5_EVENTS = [  # (label, asset) in story order
    ("BEGINNING", "story-retelling/rt-fly-1.jpg"),
    ("MIDDLE", "story-retelling/rt-fly-2.jpg"),
    ("END", "story-retelling/rt-fly-3.jpg"),
]


def _my_story_retelling(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 638,
        "Look at the pictures. Draw what happened at the")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 615,
        "beginning, middle, and end. Then tell the story out loud.")
    for i, (label, rel) in enumerate(P5_EVENTS):
        px0 = 40 + i * 184
        cx = px0 + 82
        _panel(pdf, px0, 156, 164, 434)
        _scene(pdf, rel, px0 + 10, 452, 144, 128, ratio=144 / 128)
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 14)
        pdf.drawCentredString(cx, 426, label)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(GUIDE)
        pdf.setLineWidth(1.4)
        pdf.roundRect(px0 + 10, 176, 144, 214, 10, stroke=1, fill=1)
        if i < 2:
            pdf.setFillColor(TEAL)
            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawCentredString(px0 + 174, 516, "\u2192")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 112,
        "Adult: Help your child retell the picture story. "
        "Encourage them to draw each part and explain it aloud.")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Story Retelling")
    _my_story_retelling(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Beginning, Middle & End", build_p1_page, True),  # APPROVED +
    # LOCKED 2026-10-16
    ("Tell the Story", build_p2_page, True),  # APPROVED +
    # LOCKED 2026-10-16
    ("What Happened in the Middle?", build_p3_page, True),  # APPROVED
    # + LOCKED 2026-10-16
    ("Retell a Short Story", build_p4_page, True),  # APPROVED +
    # LOCKED 2026-10-16
    ("My Story Retelling", build_p5_page, True),  # APPROVED +
    # LOCKED 2026-10-16
]


# ---------------------------------------------------------------------------
# Answer key (parent/teacher page, NOT part of the 5-page bundle)
# States the pack's learning objective in parent-friendly language.
# Page 3 has one correct answer; the retelling pages are open-ended,
# so the key gives a SAMPLE retelling for each one -- any telling
# that matches the pictures is right.
# ---------------------------------------------------------------------------
OBJECTIVE_LINES = [
    "This pack teaches your child to retell a story in three",
    "parts: the beginning, the middle, and the end. Retelling",
    "shows that your child understood the story. The pages grow",
    "step by step: learning the three parts, telling a story",
    "from pictures, finding a missing middle, retelling a story",
    "that is read aloud, and drawing and telling a story of",
    "their own. (Kindergarten standard RL.K.2: retelling.)",
]
ANSWER_BLOCKS = [
    ("Page 1 \u2014 Beginning, Middle & End",
     ["BEGINNING: dark clouds come; Mia gets her umbrella.",
      "MIDDLE: rain falls down; Mia splashes in a puddle.",
      "END: the sun comes out; Mia sees a rainbow."]),
    ("Page 2 \u2014 Tell the Story",
     ["Sample retelling: \u201cThe boy puts on his red cap. The wind",
      "blows it away, and he runs after it. He gets his cap back",
      "and laughs.\u201d Any telling that matches the pictures is right."]),
    ("Page 3 \u2014 What Happened in the Middle?",
     ["Circle the middle picture: the vendor scooping pink ice",
      "cream onto her cone. (Beginning: empty cone. End: eating it.)"]),
    ("Page 4 \u2014 Retell a Short Story",
     ["Sample retelling: \u201cLily played with Teddy in the garden.",
      "Teddy was lost, and Lily looked and looked. Lily found",
      "Teddy and hugged him tight!\u201d"]),
    ("Page 5 \u2014 My Story Retelling",
     ["There is no single right answer. Your child draws each",
      "part of the butterfly story and tells it aloud: the boy sees",
      "the butterfly, follows it, and it lands on his finger."]),
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
    pdf.drawString(40, y, "ANSWERS AND SAMPLE RETELLINGS")
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
        "Tip: Praise every telling. If a part is missing, point to "
        "its picture and ask: What happens here?")
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
                          "story-retelling")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(outdir, "story-retelling-page-%02d.pdf"
                         % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(outdir, "story-retelling-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)
    key = os.path.join(outdir, "story-retelling-answer-key.pdf")
    build_answer_key(key)
    print("answer key: %s" % key)


if __name__ == "__main__":
    main()
