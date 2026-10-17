#!/usr/bin/env python3
"""Informational Text -- Main Topic & Key Details.

Kindergarten Reading & Language (Informational Text). Five pages
that teach children to find the main topic of a short nonfiction
text and pick out its key details. Aligned with Michigan RI.K.1-3
and RI.K.7. All passages are short adult read-alouds in a boxed
fact panel, visually separate from the activity; every child
response is picture-based.

Plan as REVISED AND APPROVED by the user 2026-10-16:
  P1: What Is This Text About? (main topic intro, RI.K.2) --
      Bees. Topic choices are Bees / Flowers / Honey, so the child
      must separate the whole-text topic from two details that ARE
      in the text. (APPROVED + LOCKED 2026-10-16)
  P2: Find the Key Details (RI.K.1/2) -- Penguins. Every correct
      detail is explicitly stated in the passage; no blanket
      "all penguins live on ice" claim. (APPROVED + LOCKED
      2026-10-16)
  P3: Rain (RI.K.7) -- two focused text-to-illustration
      comprehension questions (NOT a visual search). (APPROVED +
      LOCKED 2026-10-16)
  P4: From Wheat to Bread (RI.K.1/2/3) -- the process is kept,
      but questions require understanding the text, not just
      recognizing pictures. (APPROVED + LOCKED 2026-10-16, after
      the user's Q3 next-step revision)
  P5: Taking Care of My Teeth (RI.K.2/7) -- short passage, a main
      topic question and two stated-detail questions, then a
      draw-and-tell response. No ambiguous distractors (no candy).
      (APPROVED + LOCKED 2026-10-16, after the user's detail-row
      and drawing-instruction revision)

Header/logo/helpers are imported verbatim from build_phonics_az.py
(the canonical Learn My Letters header). Local helpers (_panel,
_scene) follow the same pattern as build_story_retelling.py.

Run from this directory with the repo venv python:
    ../.venv/bin/python build_informational_text.py
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

PACK_TITLE = "Informational Text"
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


def _fact_panel(pdf, scene_rel, lines):
    """Boxed read-aloud fact panel: scene left, passage right, with
    a neutral FACTS label (the label never names the topic, so the
    main-topic question stays a real question)."""
    _panel(pdf, 40, 500, 532, 122)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(218, 607, "FACTS")
    _scene(pdf, scene_rel, 54, 510, 150, 102, ratio=150 / 102)
    pdf.setFillColor(INK)
    pdf.setFont("Andika-Bold", 15)
    y = 578
    for line in lines:
        pdf.drawString(218, y, line)
        y -= 25


def _teaching_strip(pdf, segments, y0=452):
    """One-line teaching strip; segments are (text, color) pairs,
    centered as a single flow line."""
    _panel(pdf, 40, y0, 532, 36)
    widths = [stringWidth(t, "Helvetica-Bold", 12.5)
              for t, _c in segments]
    x = PAGE_WIDTH / 2 - sum(widths) / 2
    pdf.setFont("Helvetica-Bold", 12.5)
    for (text, color), w in zip(segments, widths):
        pdf.setFillColor(color)
        pdf.drawString(x, y0 + 13, text)
        x += w


# ---------------------------------------------------------------------------
# Page 1 -- What Is This Text About? (identify the main topic)
# The passage is about BEES: every sentence is about bees, while
# flowers and honey each appear as details. The three choices are
# all IN the text (a bee, flowers, a honey pot), so circling the
# bee requires understanding what the WHOLE text is about -- an
# unrelated-picture giveaway is deliberately avoided. The flowers
# and honey pictures contain no bee.
# ---------------------------------------------------------------------------
P1_FACTS = [
    "Bees are insects. They live in a hive.",
    "Bees fly from flower to flower.",
    "Bees make honey.",
]
P1_CHOICES = [  # the bee (the main topic) is FIRST
    "informational-text/it-choice-bee.jpg",
    "informational-text/it-choice-flowers.jpg",
    "informational-text/it-choice-honey.jpg",
]


def _main_topic(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 636,
        "Listen to the facts. Circle what the text is all about.")
    _fact_panel(pdf, "informational-text/it-bee-scene.jpg", P1_FACTS)
    _teaching_strip(pdf, [
        ("The whole text is about one ", NAVY),
        ("main topic", TEAL),
        (".", NAVY),
    ])
    for i, rel in enumerate(P1_CHOICES):
        px0 = 40 + i * 184
        _panel(pdf, px0, 196, 164, 210)
        _scene(pdf, rel, px0 + 10, 222, 144, 160, ratio=144 / 160)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 140,
        "Adult: Read the facts aloud. Ask: What is this text all "
        "about \u2014 bees, flowers, or honey?")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Is This Text About?")
    _main_topic(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Find the Key Details (Penguins)
# Every correct picture restates a clause of the passage in picture
# form: swimming ("Penguins swim in the cold sea"), a fish in the
# beak ("and catch fish"), penguins in snow ("Many penguins live
# where it is cold and snowy" -- carefully NOT a claim about all
# penguins or about ice). The single wrong picture, a penguin
# flying, contradicts the passage outright ("Penguins cannot
# fly"). The child circles the three that match the facts.
# ---------------------------------------------------------------------------
P2_FACTS = [
    "Penguins are birds. Penguins cannot fly.",
    "Penguins swim in the cold sea and catch fish.",
    "Many penguins live where it is cold and snowy.",
]
P2_CHOICES = [  # 2x2 grid: TL, TR, BL (wrong), BR
    "informational-text/it-peng-swim.jpg",
    "informational-text/it-peng-fish.jpg",
    "informational-text/it-peng-fly.jpg",
    "informational-text/it-peng-snow.jpg",
]


def _key_details(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 636,
        "Listen to the facts. Circle the pictures that match the "
        "facts.")
    _fact_panel(pdf, "informational-text/it-peng-scene.jpg",
                P2_FACTS)
    _teaching_strip(pdf, [
        ("The facts a text tells are its ", NAVY),
        ("key details", TEAL),
        (".", NAVY),
    ])
    positions = [(40, 296), (313, 296), (40, 146), (313, 146)]
    for rel, (px0, py0) in zip(P2_CHOICES, positions):
        _panel(pdf, px0, py0, 259, 136)
        _scene(pdf, rel, px0 + 10, py0 + 10, 239, 116,
               ratio=239 / 116)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 112,
        "Adult: Read the facts aloud. Ask: Which pictures match "
        "the facts?")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Find the Key Details")
    _key_details(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- What Does the Picture Show? (Rain; RI.K.7)
# One clear illustration sits in the fact panel with the passage:
# grey clouds pouring rain over a flower garden with puddles --
# every detail of the text is visible in it. Below are TWO focused
# comprehension questions (not an object hunt in the scene). Each
# asks the child to connect a detail of the text to what a picture
# shows, and each has exactly one answer the text states and the
# big illustration shows:
#   Q1 What does rain fall from?   cloud (sun and moon never are)
#   Q2 What does rain help grow?   flowers (a snowman and a
#                                  sandcastle do not grow)
# ---------------------------------------------------------------------------
P3_FACTS = [
    "Rain falls from clouds in the sky.",
    "Rain makes puddles on the ground.",
    "Rain helps plants and flowers grow.",
]
P3_Q1 = [  # cloud is correct (FIRST)
    "informational-text/it-q-cloud.jpg",
    "informational-text/it-q-sun.jpg",
    "informational-text/it-q-moon.jpg",
]
P3_Q2 = [  # flowers are correct (FIRST)
    "informational-text/it-q-flowers.jpg",
    "informational-text/it-q-snowman.jpg",
    "informational-text/it-q-sandcastle.jpg",
]


def _question_row(pdf, header, choices, header_y, panel_y):
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, header_y, header)
    for i, rel in enumerate(choices):
        px0 = 40 + i * 184
        _panel(pdf, px0, panel_y, 164, 112)
        _scene(pdf, rel, px0 + 10, panel_y + 10, 144, 92,
               ratio=144 / 92)


def _picture_show(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 636,
        "Listen to the facts. Look at the picture. Answer the "
        "questions.")
    _fact_panel(pdf, "informational-text/it-rain-scene.jpg",
                P3_FACTS)
    _teaching_strip(pdf, [
        ("A picture can ", NAVY),
        ("show", TEAL),
        (" what the words say.", NAVY),
    ])
    _question_row(pdf, "WHAT DOES RAIN FALL FROM?", P3_Q1, 424, 300)
    _question_row(pdf, "WHAT DOES RAIN HELP GROW?", P3_Q2, 284, 156)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 112,
        "Adult: Read the facts and each question aloud. Let your "
        "child look at the big picture, then circle.")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Does the Picture Show?")
    _picture_show(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- From Wheat to Bread (RI.K.1/2/3)
# A short process passage: wheat grows, its grains are ground into
# flour, bakers use the flour to make bread. Three question rows
# in the Story Detective geometry, each testing understanding of
# the text rather than picture naming:
#   Q1 main topic -- a loaf of bread, against a shoe and a toy
#      boat (things this text is not about).
#   Q2 the CONNECTION between steps -- the grains are ground into
#      FLOUR: the wheat bundle is the step before, the loaf is the
#      step after, so only the flour shows what grinding makes.
#   Q3 the NEXT STEP (added by user revision 2026-10-16) -- after
#      the grains are ground into flour, a BAKER USES THE FLOUR TO
#      MAKE DOUGH; a shoe and a kite are not steps in the process.
# The same loaf picture is reused across rows.
# ---------------------------------------------------------------------------
P4_FACTS = [
    "Wheat grows tall in the fields.",
    "The wheat grains are ground into soft flour.",
    "Bakers use the flour to make bread.",
]
_LOAF = "informational-text/it-obj-loaf.jpg"
P4_Q1 = [_LOAF,
         "informational-text/it-obj-shoe.jpg",
         "informational-text/it-obj-boat.jpg"]
P4_Q2 = ["informational-text/it-obj-wheat.jpg",
         "informational-text/it-obj-flour.jpg",
         _LOAF]
P4_Q3 = ["informational-text/it-obj-shoe.jpg",
         "informational-text/it-obj-baker.jpg",
         "informational-text/it-obj-kite.jpg"]


def _object_row(pdf, header, choices, header_y, panel_y):
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, header_y, header)
    for i, rel in enumerate(choices):
        px0 = 40 + i * 184
        _panel(pdf, px0, panel_y, 164, 88)
        _scene(pdf, rel, px0 + 27, panel_y + 6, 110, 76,
               ratio=110 / 76)


def _wheat_bread(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 638,
        "Listen to the facts. Answer the questions.")
    _fact_panel(pdf, "informational-text/it-bread-scene.jpg",
                P4_FACTS)
    _object_row(pdf, "WHAT IS THIS TEXT ABOUT?", P4_Q1, 484, 380)
    _object_row(pdf, "WHAT ARE THE GRAINS GROUND INTO?", P4_Q2,
                360, 256)
    _object_row(pdf,
                "WHAT HAPPENS AFTER WHEAT GRAINS ARE GROUND INTO "
                "FLOUR?", P4_Q3, 236, 132)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 96,
        "Adult: Read the facts and each question aloud. Talk about "
        "how the steps go together.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "From Wheat to Bread")
    _wheat_bread(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Taking Care of My Teeth (capstone; RI.K.2/7)
# A short dental-care passage, then the pack's three skills on one
# page: (1) name the main topic -- a tooth being brushed, against
# a hairbrush and a book; (2) circle the TWO details the text
# states -- a child brushing their teeth and a dentist examining
# teeth (action scenes, per the user's revision) -- against a
# child combing their hair, which this text never mentions (no
# ambiguous food distractors, per the user's plan revision);
# (3) draw one way you take care of your teeth in a big box and
# tell about it out loud. There is no single right drawing; the
# adult line invites the oral telling.
# ---------------------------------------------------------------------------
P5_FACTS = [
    "Brushing keeps your teeth clean and strong.",
    "Brush your teeth in the morning and at night.",
    "A dentist checks your teeth.",
]
P5_Q1 = ["informational-text/it-obj-tooth.jpg",
         "informational-text/it-obj-hairbrush.jpg",
         "informational-text/it-obj-book.jpg"]
P5_Q2 = ["informational-text/it-q2-brushing.jpg",
         "informational-text/it-dentist.jpg",
         "informational-text/it-q2-combing.jpg"]


def _teeth(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 638,
        "Listen to the facts. Answer the questions. Then draw.")
    _fact_panel(pdf, "informational-text/it-teeth-scene.jpg",
                P5_FACTS)
    _object_row(pdf, "WHAT IS THIS TEXT ABOUT?", P5_Q1, 484, 380)
    _object_row(pdf, "WHICH TWO DETAILS ARE IN THE TEXT?", P5_Q2,
                360, 256)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, 232, "DRAW ONE WAY YOU TAKE CARE OF YOUR "
                            "TEETH.")
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(HexColor("#BFD9D9"))
    pdf.setLineWidth(1.2)
    pdf.roundRect(40, 104, 532, 112, 12, stroke=1, fill=1)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 80,
        "Adult: Read the facts aloud. Ask your child to tell you "
        "about their drawing.")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Taking Care of My Teeth")
    _teeth(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("What Is This Text About?", build_p1_page, True),  # APPROVED +
    # LOCKED 2026-10-16
    ("Find the Key Details", build_p2_page, True),  # APPROVED +
    # LOCKED 2026-10-16
    ("What Does the Picture Show?", build_p3_page, True),  # APPROVED
    # + LOCKED 2026-10-16
    ("From Wheat to Bread", build_p4_page, True),  # APPROVED +
    # LOCKED 2026-10-16 (after the Q3 next-step revision)
    ("Taking Care of My Teeth", build_p5_page, True),  # APPROVED +
    # LOCKED 2026-10-16
]


# ---------------------------------------------------------------------------
# Finalization (runs only when all five pages are locked):
#   worksheets/kindergarten/reading/informational-text/
#     informational-text-review.pdf       (bundle, 5 pages)
#     informational-text-page-01..05.pdf  (individual pages)
#     informational-text-answer-key.pdf   (one-page parent key --
#                                          NOT part of the bundle)
# ---------------------------------------------------------------------------
import io  # noqa: E402

from pypdf import PdfReader, PdfWriter  # noqa: E402

_WORKSHEET_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(
    __file__)))
PACK_DIR = os.path.join(_WORKSHEET_ROOT, "worksheets", "kindergarten",
                        "reading", "informational-text")
BUNDLE_NAME = "informational-text-review.pdf"
ANSWER_KEY_NAME = "informational-text-answer-key.pdf"

_AK_TITLE = ("Informational Text \u2014 Main Topic & Key Details: "
             "Answer Key")
_AK_OBJECTIVE = [
    "This pack teaches your child to understand nonfiction \u2014 "
    "texts that tell",
    "true facts. Your child learns to find the main topic (what a "
    "whole text",
    "is about), pick out key details (the facts it tells), and see "
    "how a",
    "picture can show what the words say \u2014 building from naming "
    "the topic",
    "to finding details, matching pictures to words, and answering "
    "questions.",
]
_AK_SECTIONS = [
    ("Page 1 \u2014 What Is This Text About? (Bees)", [
        "Circle the bee (first picture). Every sentence in the text "
        "tells about",
        "bees, so bees are the main topic. Flowers and honey are in "
        "the text too,",
        "but they are only details \u2014 small facts, not the whole "
        "topic.",
    ]),
    ("Page 2 \u2014 Find the Key Details (Penguins)", [
        "Circle three pictures: the penguin swimming (top left), the "
        "penguin with",
        "a fish (top right), and the penguins standing in the snow "
        "(bottom right).",
        "Do NOT circle the flying penguin (bottom left) \u2014 the "
        "text says",
        "penguins cannot fly.",
    ]),
    ("Page 3 \u2014 What Does the Picture Show? (Rain)", [
        "Question 1: circle the cloud (first picture) \u2014 the text "
        "says rain falls",
        "from clouds. Question 2: circle the flowers (first picture) "
        "\u2014 the text",
        "says rain helps plants and flowers grow.",
    ]),
    ("Page 4 \u2014 From Wheat to Bread", [
        "Question 1 (main topic): the loaf of bread (first picture).",
        "Question 2: the flour (middle picture) \u2014 wheat grains are "
        "ground into",
        "flour. The wheat is the step before, and the loaf comes "
        "after.",
        "Question 3: the baker making dough (middle picture) \u2014 "
        "bakers use the",
        "flour to make bread.",
    ]),
    ("Page 5 \u2014 Taking Care of My Teeth", [
        "Main topic: the tooth being brushed (first picture).",
        "Key details: circle TWO \u2014 the boy brushing his teeth "
        "(first picture)",
        "and the dentist checking teeth (middle picture). The girl "
        "combing her",
        "hair is not in the text.",
        "Drawing: there is no single right answer. Any way we take "
        "care of our",
        "teeth is a good drawing \u2014 ask your child to tell you "
        "about it.",
    ]),
]


def build_answer_key(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Answer Key",
                "Main Topic & Key Details \u2014 for parents")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640, _AK_TITLE)
    _panel(pdf, 40, 534, 532, 94)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 614, "WHAT THIS PACK TEACHES")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 10.5)
    y = 597
    for line in _AK_OBJECTIVE:
        pdf.drawString(56, y, line)
        y -= 13.5
    y = 516
    for title, lines in _AK_SECTIONS:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, y, title)
        y -= 15
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 11)
        for line in lines:
            pdf.drawString(56, y, line)
            y -= 14
        y -= 12
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 96,
        "Kindergarten Reading: Informational Text (Michigan "
        "RI.K.1\u20133, RI.K.7).")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def _single_page_pdf(build_fn):
    buf = io.BytesIO()
    build_fn(buf)
    buf.seek(0)
    return PdfReader(buf).pages[0]


def build_all():
    assert all(locked for _t, _b, locked in PAGES), (
        "All five pages must be approved and locked first.")
    os.makedirs(PACK_DIR, exist_ok=True)
    writer = PdfWriter()
    for i, (_title, build_fn, _locked) in enumerate(PAGES, start=1):
        page = _single_page_pdf(build_fn)
        writer.add_page(page)
        single = PdfWriter()
        single.add_page(page)
        with open(os.path.join(
                PACK_DIR, "informational-text-page-%02d.pdf" % i),
                "wb") as fh:
            single.write(fh)
    with open(os.path.join(PACK_DIR, BUNDLE_NAME), "wb") as fh:
        writer.write(fh)
    build_answer_key(os.path.join(PACK_DIR, ANSWER_KEY_NAME))
    print("wrote bundle, 5 single pages, and answer key to",
          PACK_DIR)


if __name__ == "__main__":
    build_all()
