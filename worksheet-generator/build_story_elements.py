"""Story Elements -- Characters, Setting & Events -- Kindergarten
Reading & Language (Literature).

Five pages aligned to Michigan RL.K.3: with prompting and support,
identify characters, settings, and major events in a story. The pack
progresses from identifying characters and settings, to recognizing
major events, to completing a simple story map. Stories are short
and read aloud by an adult ("with prompting and support"); responses
are picture-based with minimal reading demand, per the standard and
the Learning Made Simple design system.

Pages:
  P1: Who Is in the Story?   (characters)        (APPROVED + LOCKED
                                                  2026-10-15)
  P2: Where Does It Happen?  (setting)           (APPROVED + LOCKED
                                                  2026-10-15)
  P3: What Happened?         (major event)       (APPROVED + LOCKED
                                                  2026-10-15)
  P4: Story Detective        (who/where/what)    (APPROVED + LOCKED
                                                  2026-10-15)
  P5: My Story Map           (story map)         (APPROVED + LOCKED
                                                  2026-10-15)
  P3-P5: events + story map                      (not built)

Run with the repo venv:
  ../.venv/bin/python build_story_elements.py
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

PACK_TITLE = "Story Elements"
GRAY = HexColor("#37474F")


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
# Page 1 -- Who Is in the Story? (characters)
# Benny the bunny and Pip the bird: a four-sentence read-aloud story
# with its scene, a one-line kid-friendly definition of "characters",
# and a picture response -- circle the two characters among four
# animal pictures. The distractors (cat, fish) appear nowhere in the
# story or the scene. Story and activity are visually separate
# sections.
# ---------------------------------------------------------------------------
P1_STORY = [
    "Benny the bunny lived in a garden.",
    "One day, Benny found a big carrot.",
    "Benny called his friend Pip the bird.",
    "They ate the carrot together.",
]
P1_CHOICES = [  # (asset, is_character)
    ("story-elements/se-bunny.jpg", True),  # brown, matches Benny
    ("animal-library/lib-cat.jpg", False),
    ("animal-library/lib-bird.jpg", True),
    ("animal-library/lib-fish.jpg", False),
]


def _who_is_in_the_story(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, "Listen to the story.")
    # story section
    _panel(pdf, 40, 462, 532, 164)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(246, 611, "THE STORY")
    _scene(pdf, "story-elements/se-garden-story.jpg", 54, 474, 176,
           140, ratio=176 / 140)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 16.5)
    y = 581
    for line in P1_STORY:
        pdf.drawString(246, y, line)
        y -= 27
    # teaching strip: what a character is
    _panel(pdf, 40, 404, 532, 46)
    pdf.setFillColor(TEAL)
    pdf.setFont("Andika-Bold", 17)
    w1 = stringWidth("Characters", "Andika-Bold", 17)
    pdf.setFillColor(NAVY)
    w2 = stringWidth(" are who the story is about.", "Andika-Bold", 17)
    x0 = (PAGE_WIDTH - w1 - w2) / 2
    pdf.setFillColor(TEAL)
    pdf.drawString(x0, 421, "Characters")
    pdf.setFillColor(NAVY)
    pdf.drawString(x0 + w1, 421, " are who the story is about.")
    # activity
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, 372, "Circle the characters from the story.")
    for i, (rel, _ok) in enumerate(P1_CHOICES):
        _img_circle(pdf, os.path.join(_ASSETS, rel), 103 + i * 134,
                    268, 46)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 150,
        "Adult: Read the story aloud. A character is a person or "
        "animal in the story.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Who Is in the Story?")
    _who_is_in_the_story(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Where Does It Happen? (setting)
# Benny and Pip return in a new four-sentence story whose setting --
# a pond -- is unmistakable in the scene and named in the text. The
# teaching strip defines "setting" in parallel with Page 1. The
# response is three large setting pictures (forest / pond / desert
# from the habitat library); only the pond is correct. The pond
# choice is a different picture from the story scene, so the child
# must recognize the PLACE, not match the image.
# ---------------------------------------------------------------------------
P2_STORY = [
    "Benny the bunny hopped to the pond.",
    "Pip the bird flew to the pond too.",
    "They splashed in the water.",
    "What a fun day at the pond!",
]
P2_CHOICES = [  # (asset, is_setting)
    ("animal-library/lib-habitat-forest.jpg", False),
    ("animal-library/lib-habitat-pond.jpg", True),
    ("animal-library/lib-habitat-desert.jpg", False),
]


def _where_does_it_happen(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, "Listen to the story.")
    _panel(pdf, 40, 462, 532, 164)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(246, 611, "THE STORY")
    _scene(pdf, "story-elements/se-pond-story.jpg", 54, 474, 176, 140,
           ratio=176 / 140)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 16.5)
    y = 581
    for line in P2_STORY:
        pdf.drawString(246, y, line)
        y -= 27
    _panel(pdf, 40, 404, 532, 46)
    pdf.setFont("Andika-Bold", 17)
    w1 = stringWidth("Setting", "Andika-Bold", 17)
    w2 = stringWidth(" is where the story happens.", "Andika-Bold",
                     17)
    x0 = (PAGE_WIDTH - w1 - w2) / 2
    pdf.setFillColor(TEAL)
    pdf.drawString(x0, 421, "Setting")
    pdf.setFillColor(NAVY)
    pdf.drawString(x0 + w1, 421, " is where the story happens.")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, 372, "Circle the setting from the story.")
    for i, (rel, _ok) in enumerate(P2_CHOICES):
        px0 = 40 + i * 184
        _panel(pdf, px0, 186, 164, 156)
        _scene(pdf, rel, px0 + 10, 196, 144, 136, ratio=144 / 136)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 130,
        "Adult: Read the story aloud. The setting is the place where "
        "the story happens.")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Where Does It Happen?")
    _where_does_it_happen(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- What Happened? (major event)
# New characters for variety: Kit the kitten. The story has ONE clear
# major event -- a butterfly lands on Kit's nose -- and the three
# event pictures show that event (a different, closer picture, so
# the child recalls the event rather than matching the scene), Kit
# drinking milk, and Kit asleep. Neither distractor event is
# mentioned anywhere in the story, so the answer is unambiguous.
# ---------------------------------------------------------------------------
P3_STORY = [
    "Kit the kitten sat in the sun.",
    "A butterfly came by.",
    "It landed right on Kit's nose!",
    "Kit laughed and laughed.",
]
P3_CHOICES = [  # (asset, is_event)
    ("story-elements/se-event-milk.jpg", False),
    ("story-elements/se-event-butterfly.jpg", True),
    ("story-elements/se-event-sleep.jpg", False),
]


def _what_happened(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, "Listen to the story.")
    _panel(pdf, 40, 462, 532, 164)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(246, 611, "THE STORY")
    _scene(pdf, "story-elements/se-kitten-story.jpg", 54, 474, 176,
           140, ratio=176 / 140)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 16.5)
    y = 581
    for line in P3_STORY:
        pdf.drawString(246, y, line)
        y -= 27
    _panel(pdf, 40, 404, 532, 46)
    pdf.setFont("Andika-Bold", 17)
    w1 = stringWidth("Events", "Andika-Bold", 17)
    w2 = stringWidth(" are things that happen in a story.",
                     "Andika-Bold", 17)
    x0 = (PAGE_WIDTH - w1 - w2) / 2
    pdf.setFillColor(TEAL)
    pdf.drawString(x0, 421, "Events")
    pdf.setFillColor(NAVY)
    pdf.drawString(x0 + w1, 421,
                   " are things that happen in a story.")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, 372, "Circle what happened in the story.")
    for i, (rel, _ok) in enumerate(P3_CHOICES):
        px0 = 40 + i * 184
        _panel(pdf, px0, 186, 164, 156)
        _scene(pdf, rel, px0 + 10, 196, 144, 136, ratio=144 / 136)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 130,
        "Adult: Read the story aloud. Ask: What was the big thing "
        "that happened?")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Happened?")
    _what_happened(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Story Detective (who / where / what, combined)
# A new story and new character: Max the puppy at the beach, who digs
# up a big shell. The story panel is slightly shorter so three
# question rows fit comfortably on one page; each row has a question
# label (key word in teal) and three large picture choices with
# exactly one correct answer. Correct-answer positions vary by row
# (2nd / 3rd / 1st). Distractor content is absent from the story.
# ---------------------------------------------------------------------------
P4_STORY = [
    "Max the puppy ran on the beach.",
    "Max dug in the sand.",
    "Max found a big shell!",
    "Max was so happy!",
]
P4_QUESTIONS = [
    ("WHO", " is in the story?", [
        ("animal-library/lib-frog.jpg", False),
        ("sentence-building/bss-pup-run.jpg", True),
        ("animal-library/lib-duck.jpg", False),
    ]),
    ("WHERE", " does the story happen?", [
        ("animal-library/lib-habitat-forest.jpg", False),
        ("animal-library/lib-habitat-desert.jpg", False),
        ("story-elements/se-beach-setting.jpg", True),
    ]),
    ("WHAT", " happened in the story?", [
        ("story-elements/se-event-shell.jpg", True),
        ("story-elements/se-event-splash.jpg", False),
        ("story-elements/se-event-nap.jpg", False),
    ]),
]


def _question_row(pdf, label_y, panel_y, key, rest, choices):
    pdf.setFont("Helvetica-Bold", 14)
    w1 = stringWidth(key, "Helvetica-Bold", 14)
    pdf.setFillColor(TEAL)
    pdf.drawString(40, label_y, key)
    pdf.setFillColor(NAVY)
    pdf.drawString(40 + w1, label_y, rest)
    for i, (rel, _ok) in enumerate(choices):
        px0 = 40 + i * 184
        _panel(pdf, px0, panel_y, 164, 106)
        _scene(pdf, rel, px0 + 8, panel_y + 5, 148, 96,
               ratio=148 / 96)


def _story_detective(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Listen to the story. Answer the questions.")
    _panel(pdf, 40, 500, 532, 126)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(218, 611, "THE STORY")
    _scene(pdf, "story-elements/se-beach-story.jpg", 54, 510, 150,
           106, ratio=150 / 106)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 15.5)
    y = 584
    for line in P4_STORY:
        pdf.drawString(218, y, line)
        y -= 24
    rows = [(482, 372), (350, 240), (218, 108)]
    for (key, rest, choices), (ly, py) in zip(P4_QUESTIONS, rows):
        _question_row(pdf, ly, py, key, rest, choices)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 84,
        "Adult: Read the story aloud. Then read each question and "
        "let your child choose.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Story Detective")
    _story_detective(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- My Story Map (capstone)
# Slightly more challenging than Page 4 in two deliberate ways:
# (1) WHO offers FOUR choices and includes the story's minor
# character -- the sleeping cat, who is IN the story but is not the
# main character (Molly is the subject of every sentence; the adult
# line defines "main character"); (2) the three sections are
# presented as a labeled story map under a gold MY STORY MAP banner.
# New characters and setting: Molly the mouse, a barn, and a big
# cheese. The WHAT distractors show Molly sleeping and Molly
# swimming -- neither happens to Molly in the story (only the cat
# sleeps, which is exactly the careful reading this page rewards).
# ---------------------------------------------------------------------------
P5_STORY = [
    "Molly the mouse lived in a barn.",
    "One day, Molly found a big cheese.",
    "Molly tiptoed past the sleeping cat.",
    "Molly ate the cheese. Yum!",
]
P5_SECTIONS = [
    ("WHO", " \u2014 the main character", 124, [
        ("animal-library/lib-frog.jpg", False),
        ("animal-library/lib-cat.jpg", False),  # in story, minor
        ("story-elements/se-mouse.jpg", True),
        ("animal-library/lib-duck.jpg", False),
    ]),
    ("WHERE", " \u2014 the setting", 164, [
        ("story-elements/se-barn-setting.jpg", True),
        ("animal-library/lib-habitat-pond.jpg", False),
        ("story-elements/se-beach-setting.jpg", False),
    ]),
    ("WHAT", " \u2014 the big event", 164, [
        ("story-elements/se-event-mouse-swim.jpg", False),
        ("story-elements/se-event-mouse-sleep.jpg", False),
        ("story-elements/se-event-cheese.jpg", True),
    ]),
]


def _map_row(pdf, label_y, panel_y, key, rest, panel_w, choices):
    pdf.setFont("Helvetica-Bold", 14)
    w1 = stringWidth(key, "Helvetica-Bold", 14)
    pdf.setFillColor(TEAL)
    pdf.drawString(40, label_y, key)
    pdf.setFillColor(NAVY)
    pdf.drawString(40 + w1, label_y, rest)
    n = len(choices)
    gap = (532 - n * panel_w) / (n - 1) if n > 1 else 0
    for i, (rel, _ok) in enumerate(choices):
        px0 = 40 + i * (panel_w + gap)
        _panel(pdf, px0, panel_y, panel_w, 96)
        _scene(pdf, rel, px0 + 8, panel_y + 5, panel_w - 16, 86,
               ratio=(panel_w - 16) / 86)


def _my_story_map(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Listen to the story. Circle the answers "
                          "in the story map.")
    _panel(pdf, 40, 508, 532, 118)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(218, 611, "THE STORY")
    _scene(pdf, "story-elements/se-mouse-story.jpg", 54, 516, 150,
           102, ratio=150 / 102)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 15)
    y = 586
    for line in P5_STORY:
        pdf.drawString(218, y, line)
        y -= 23
    pdf.setFillColor(HexColor("#FFF3D6"))
    pdf.setStrokeColor(HexColor("#E4B93E"))
    pdf.setLineWidth(1.1)
    pdf.roundRect(40, 466, 532, 30, 10, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 476, "MY STORY MAP")
    rows = [(448, 344), (326, 222), (204, 100)]
    for (key, rest, pw, choices), (ly, py) in zip(P5_SECTIONS, rows):
        _map_row(pdf, ly, py, key, rest, pw, choices)
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 78,
        "Adult: Read the story aloud. The main character is who the "
        "story is mostly about.")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Story Map")
    _my_story_map(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Who Is in the Story?", build_p1_page, True),  # APPROVED +
    # LOCKED 2026-10-15
    ("Where Does It Happen?", build_p2_page, True),  # APPROVED +
    # LOCKED 2026-10-15
    ("What Happened?", build_p3_page, True),  # APPROVED +
    # LOCKED 2026-10-15
    ("Story Detective", build_p4_page, True),  # APPROVED +
    # LOCKED 2026-10-15
    ("My Story Map", build_p5_page, True),  # APPROVED +
    # LOCKED 2026-10-15
]


# ---------------------------------------------------------------------------
# Answer key (parent/teacher page, NOT part of the 5-page bundle)
# States the pack's learning objective in parent-friendly language
# and gives the answer for every page, with positions.
# ---------------------------------------------------------------------------
OBJECTIVE_LINES = [
    "This pack builds early reading comprehension. Your child listens",
    "to short stories and shows what they understood by finding three",
    "things: the characters (who the story is about), the setting",
    "(where it happens), and the important events (what happened).",
    "The pages grow step by step \u2014 one idea at a time, then all",
    "three together in a story map. Aligned with the Michigan",
    "kindergarten reading standard RL.K.3: with prompting and",
    "support, identify characters, settings, and major events.",
]
ANSWER_BLOCKS = [
    ("Page 1 \u2014 Who Is in the Story?",
     ["Circle TWO pictures: the bunny (1st) and the bird (3rd).",
      "Benny and Pip are the characters. The cat and the fish are not",
      "in the story."]),
    ("Page 2 \u2014 Where Does It Happen?",
     ["Circle the pond (middle picture). The story happens at the",
      "pond \u2014 not in the forest or the desert."]),
    ("Page 3 \u2014 What Happened?",
     ["Circle the butterfly on Kit's nose (middle picture). Kit did",
      "not drink milk or go to sleep in this story."]),
    ("Page 4 \u2014 Story Detective",
     ["WHO: the puppy (middle).  WHERE: the beach (right).",
      "WHAT: Max finding the big shell (left)."]),
    ("Page 5 \u2014 My Story Map",
     ["WHO: Molly the mouse (3rd of 4). The cat is in the story, but",
      "the story is mostly about Molly.  WHERE: the barn (left).",
      "WHAT: Molly eating the big cheese (right)."]),
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
    y -= 14
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, y, "ANSWERS")
    y -= 26
    for title, lines in ANSWER_BLOCKS:
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, y, title)
        y -= 17
        pdf.setFont("Helvetica", 12)
        for line in lines:
            pdf.drawString(40, y, line)
            y -= 17
        y -= 12
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(
        40, y - 4,
        "Tip: Read each story aloud first, then let your child find "
        "the answers in the pictures.")
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
                          "story-elements")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(outdir, "story-elements-page-%02d.pdf"
                         % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(outdir, "story-elements-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)
    key = os.path.join(outdir, "story-elements-answer-key.pdf")
    build_answer_key(key)
    print("answer key: %s" % key)


if __name__ == "__main__":
    main()
