#!/usr/bin/env python3
"""Kindergarten Reading - Blending & Segmenting (Learning Made Simple).

Phonological Awareness pack. ORAL-ONLY: no printed letter decoding or
spelling tasks. Each activity panel carries a small adult "Say:" script
(phonemes, General American) for the parent/teacher to read aloud.

Shared design code (logo, header, footer, circular-masked pictures) is
imported verbatim from build_phonics_az.py - do not fork it here.

Page plan (approved 2026-10-13):
  P1: Blend the Parts (onset-rime blending)      (LOCKED 2026-10-13)
  P2: Blend the Sounds (phoneme blending)        (LOCKED 2026-10-13)
  P3: Count the Sounds (segmenting)              (LOCKED 2026-10-13)
  P4: Find the Last Sound (final-phoneme match)  (LOCKED 2026-10-13)
  P5: Change the Sound (initial substitution)    (LOCKED 2026-10-13)
"""
import os
import random

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter as _letter  # noqa: F401
from reportlab.pdfgen import canvas

from build_phonics_az import (NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              _img_circle, draw_footer, draw_header)

# ---------------------------------------------------------------------------
# Page 1 -- Blend the Parts (onset + rime)
# Adult says the onset, pauses, then the rime; child blends and circles.
# Scripts audited for General American phonemic accuracy.
# ---------------------------------------------------------------------------
P1_ITEMS = [
    # word, onset, rime, key picture, distractors (name, path)
    ("cat", "/k/", "/\u00e6t/", "animal-library/lib-cat.jpg",
     [("pig", "animal-library/lib-piglet.jpg"),
      ("sun", "phonics-a-z/ph-sun.jpg")]),
    ("sun", "/s/", "/\u028cn/", "phonics-a-z/ph-sun.jpg",
     [("dog", "animal-library/lib-dog.jpg"),
      ("fish", "animal-library/lib-fish.jpg")]),
    ("pig", "/p/", "/\u026a\u0261/", "animal-library/lib-piglet.jpg",
     [("cat", "animal-library/lib-cat.jpg"),
      ("bus", "blending-segmenting/bs-bus.jpg")]),
    ("bus", "/b/", "/\u028cs/", "blending-segmenting/bs-bus.jpg",
     [("hat", "phonics-a-z/ph-hat.jpg"),
      ("dog", "animal-library/lib-dog.jpg")]),
    ("hat", "/h/", "/\u00e6t/", "phonics-a-z/ph-hat.jpg",
     [("pig", "animal-library/lib-piglet.jpg"),
      ("sun", "phonics-a-z/ph-sun.jpg")]),
    ("fish", "/f/", "/\u026a\u0283/", "animal-library/lib-fish.jpg",
     [("cat", "animal-library/lib-cat.jpg"),
      ("moon", "phonics-a-z/ph-moon.jpg")]),
]


def _blend_parts(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Listen to the two sound parts. Put them together.")
    pdf.drawCentredString(PAGE_WIDTH / 2, 624, "Circle the picture.")
    # adult guidance (bottom of page, clear of panels and footer)
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Say each sound part aloud with a short pause. "
        "Do not say the whole word or letter names.")
    panel_w, panel_h, gutter = 248, 158, 36
    for i, (_word, onset, rime, img, distractors) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 172 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        # adult script: onset and rime clearly separated
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(px0 + 16, py0 + panel_h - 28, "Say:")
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 16)
        pdf.drawString(px0 + 52, py0 + panel_h - 29,
                       "%s   \u2026   %s" % (onset, rime))
        # 3 picture choices (key + 2 distractors, shuffled)
        choices = [img] + [d[1] for d in distractors]
        order = [0, 1, 2]
        rnd = random.Random(3000 + i)
        rnd.shuffle(order)
        for k, oi in enumerate(order):
            cx = px0 + 16 + k * 72 + 36
            cy = py0 + 56
            _img_circle(pdf, choices[oi], cx, cy, 35, zoom=True)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Blending & Segmenting", "Blend the Parts")
    _blend_parts(pdf, P1_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Blend the Sounds (phoneme by phoneme)
# Adult says each phoneme separately; child blends and circles.
# Scripts are each word's ACTUAL phonemes (General American).
# ---------------------------------------------------------------------------
P2_ITEMS = [
    # word, phonemes, key picture, distractors (name, path)
    ("egg", ["/\u025b/", "/\u0261/"], "blending-segmenting/bs-egg.jpg",
     [("fish", "animal-library/lib-fish.jpg"),
      ("sun", "phonics-a-z/ph-sun.jpg")]),
    ("bee", ["/b/", "/i/"], "blending-segmenting/bs-bee.jpg",
     [("dog", "animal-library/lib-dog.jpg"),
      ("cat", "animal-library/lib-cat.jpg")]),
    ("dog", ["/d/", "/\u0251/", "/\u0261/"], "animal-library/lib-dog.jpg",
     [("pig", "animal-library/lib-piglet.jpg"),
      ("sun", "phonics-a-z/ph-sun.jpg")]),
    ("cup", ["/k/", "/\u028c/", "/p/"], "blending-segmenting/bs-cup.jpg",
     [("hat", "phonics-a-z/ph-hat.jpg"),
      ("fish", "animal-library/lib-fish.jpg")]),
    ("web", ["/w/", "/\u025b/", "/b/"], "blending-segmenting/bs-web.jpg",
     [("moon", "phonics-a-z/ph-moon.jpg"),
      ("cat", "animal-library/lib-cat.jpg")]),
    ("moon", ["/m/", "/u/", "/n/"], "phonics-a-z/ph-moon.jpg",
     [("sun", "phonics-a-z/ph-sun.jpg"),
      ("dog", "animal-library/lib-dog.jpg")]),
]


def _blend_sounds(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Listen to each sound. Put them together.")
    pdf.drawCentredString(PAGE_WIDTH / 2, 624, "Circle the picture.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Say each sound aloud with a short pause. "
        "Do not say the whole word or letter names.")
    panel_w, panel_h, gutter = 248, 158, 36
    for i, (_word, phonemes, img, distractors) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 172 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(px0 + 16, py0 + panel_h - 28, "Say:")
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 16)
        pdf.drawString(px0 + 52, py0 + panel_h - 29,
                       "  \u2022  ".join(phonemes))
        choices = [img] + [d[1] for d in distractors]
        order = [0, 1, 2]
        rnd = random.Random(4000 + i)
        rnd.shuffle(order)
        for k, oi in enumerate(order):
            cx = px0 + 16 + k * 72 + 36
            cy = py0 + 56
            _img_circle(pdf, choices[oi], cx, cy, 35, zoom=True)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Blending & Segmenting", "Blend the Sounds")
    _blend_sounds(pdf, P2_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Count the Sounds (segmenting)
# Adult says the word aloud; child says it slowly and colors one box for
# every SOUND heard (phonemes, NOT letters). Sound counts verified:
#   egg 2 (/ɛ/ /ɡ/), cat 3, pig 3, bus 3,
#   nest 4 (/n/ /ɛ/ /s/ /t/), fox 4 (/f/ /ɑ/ /k/ /s/ -- x = /k/ + /s/).
# ---------------------------------------------------------------------------
P3_ITEMS = [
    # word, phoneme count, picture
    ("egg", 2, "blending-segmenting/bs-egg.jpg"),
    ("cat", 3, "animal-library/lib-cat.jpg"),
    ("pig", 3, "animal-library/lib-piglet.jpg"),
    ("bus", 3, "blending-segmenting/bs-bus.jpg"),
    ("nest", 4, "animal-library/lib-nest.jpg"),
    ("fox", 4, "phonics-a-z/ph-fox.jpg"),
]


def _count_sounds(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Say the word. Say each sound. "
                          "Color one box for each sound.")
    # adult note: count SOUNDS, not letters
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Say each word aloud slowly, stretching the sounds. "
        "Count sounds, not letters.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (_word, count, img) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 166 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        _img_circle(pdf, img, px0 + 52, py0 + 75, 38, zoom=True)
        # exactly `count` empty boxes (one per phoneme), row centered
        pdf.setStrokeColor(HexColor("#7FA3B5"))
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setLineWidth(1.2)
        row_w = (count - 1) * 35 + 28
        start_x = px0 + 104 + (133 - row_w) // 2
        for b in range(count):
            bx = start_x + b * 35
            pdf.roundRect(bx, py0 + 61, 28, 28, 4, stroke=1, fill=1)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Blending & Segmenting", "Count the Sounds")
    _count_sounds(pdf, P3_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Find the Last Sound (final-phoneme matching)
# Adult says the target word aloud; child circles the choice that ENDS
# with the same sound. Exactly one correct answer per item (verified:
# distractors end in different sounds).
#   cat /t/ -> hat | dog /g/ -> pig | sun /n/ -> moon
#   cup /p/ -> top | web /b/ -> tub | fish /sh/ -> brush
# ---------------------------------------------------------------------------
P4_ITEMS = [
    # target word, ending phoneme, target picture,
    # answer (name, path), distractors (name, path)
    ("cat", "/t/", "animal-library/lib-cat.jpg",
     ("hat", "phonics-a-z/ph-hat.jpg"),
     [("sun", "phonics-a-z/ph-sun.jpg"),
      ("pig", "animal-library/lib-piglet.jpg")]),
    ("dog", "/\u0261/", "animal-library/lib-dog.jpg",
     ("pig", "animal-library/lib-piglet.jpg"),
     [("cat", "animal-library/lib-cat.jpg"),
      ("bus", "blending-segmenting/bs-bus.jpg")]),
    ("sun", "/n/", "phonics-a-z/ph-sun.jpg",
     ("moon", "phonics-a-z/ph-moon.jpg"),
     [("fish", "animal-library/lib-fish.jpg"),
      ("cup", "blending-segmenting/bs-cup.jpg")]),
    ("cup", "/p/", "blending-segmenting/bs-cup.jpg",
     ("top", "blending-segmenting/bs-top.jpg"),
     [("dog", "animal-library/lib-dog.jpg"),
      ("web", "blending-segmenting/bs-web.jpg")]),
    ("web", "/b/", "blending-segmenting/bs-web.jpg",
     ("tub", "blending-segmenting/bs-tub.jpg"),
     [("sun", "phonics-a-z/ph-sun.jpg"),
      ("hat", "phonics-a-z/ph-hat.jpg")]),
    ("fish", "/\u0283/", "animal-library/lib-fish.jpg",
     ("brush", "blending-segmenting/bs-brush.jpg"),
     [("cat", "animal-library/lib-cat.jpg"),
      ("moon", "phonics-a-z/ph-moon.jpg")]),
]


def _last_sound(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Circle the picture that ends with the same sound.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Say the big-picture word aloud. Children circle the "
        "picture with the same ending sound.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (_word, ending, target, answer, distractors) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 166 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        # target picture (top left) with a "Listen" label beside it
        _img_circle(pdf, target, px0 + 54, py0 + 100, 32, zoom=True)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(px0 + 100, py0 + 96, "Listen")
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawCentredString(px0 + 125, py0 + 70, "Circle one")
        # 3 choices along the bottom (answer + 2 distractors, shuffled)
        choices = [answer[1]] + [d[1] for d in distractors]
        order = [0, 1, 2]
        rnd = random.Random(5000 + i)
        rnd.shuffle(order)
        for k, oi in enumerate(order):
            cx = px0 + 47 + k * 78
            _img_circle(pdf, choices[oi], cx, py0 + 33, 30, zoom=True)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Blending & Segmenting", "Find the Last Sound")
    _last_sound(pdf, P4_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Change the Sound (initial-phoneme substitution)
# Adult says the starting word, then the change ("Say: /k/ to /b/");
# child circles the NEW word. Choices = new word + starting word + one
# word with a different first sound (exactly one correct answer).
#   cat /k/->/b/ bat | pig /p/->/w/ wig | mop /m/->/t/ top
#   sun /s/->/b/ bun | dog /d/->/l/ log | van /v/->/f/ fan
# ---------------------------------------------------------------------------
P5_ITEMS = [
    # start word, from-sound, to-sound, start picture,
    # answer (name, path), other choices (name, path)
    ("cat", "/k/", "/b/", "animal-library/lib-cat.jpg",
     ("bat", "blending-segmenting/bs-bat.jpg"),
     [("cat", "animal-library/lib-cat.jpg"),
      ("hat", "phonics-a-z/ph-hat.jpg")]),
    ("pig", "/p/", "/w/", "animal-library/lib-piglet.jpg",
     ("wig", "blending-segmenting/bs-wig.jpg"),
     [("pig", "animal-library/lib-piglet.jpg"),
      ("dog", "animal-library/lib-dog.jpg")]),
    ("mop", "/m/", "/t/", "blending-segmenting/bs-mop.jpg",
     ("top", "blending-segmenting/bs-top.jpg"),
     [("mop", "blending-segmenting/bs-mop.jpg"),
      ("cup", "blending-segmenting/bs-cup.jpg")]),
    ("sun", "/s/", "/b/", "phonics-a-z/ph-sun.jpg",
     ("bun", "blending-segmenting/bs-bun.jpg"),
     [("sun", "phonics-a-z/ph-sun.jpg"),
      ("moon", "phonics-a-z/ph-moon.jpg")]),
    ("dog", "/d/", "/l/", "animal-library/lib-dog.jpg",
     ("log", "blending-segmenting/bs-log.jpg"),
     [("dog", "animal-library/lib-dog.jpg"),
      ("pig", "animal-library/lib-piglet.jpg")]),
    ("van", "/v/", "/f/", "blending-segmenting/bs-van.jpg",
     ("fan", "blending-segmenting/bs-fan.jpg"),
     [("van", "blending-segmenting/bs-van.jpg"),
      ("bus", "blending-segmenting/bs-bus.jpg")]),
]


def _change_sound(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Change the first sound. Circle the new word.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Say the starting word aloud, then the sound change. "
        "Children circle the new word.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (_w, s_from, s_to, start, answer, others) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 166 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        # starting picture + Listen label + the adult's change script
        _img_circle(pdf, start, px0 + 54, py0 + 100, 32, zoom=True)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(px0 + 100, py0 + 110, "Listen")
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 15)
        pdf.drawString(px0 + 100, py0 + 88,
                       "Say: %s to %s" % (s_from, s_to))
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawCentredString(px0 + 125, py0 + 70, "Circle one")
        choices = [answer[1]] + [d[1] for d in others]
        order = [0, 1, 2]
        rnd = random.Random(6000 + i)
        rnd.shuffle(order)
        for k, oi in enumerate(order):
            cx = px0 + 47 + k * 78
            _img_circle(pdf, choices[oi], cx, py0 + 33, 30, zoom=True)


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Blending & Segmenting", "Change the Sound")
    _change_sound(pdf, P5_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Blend the Parts", build_p1_page, True),  # APPROVED 2026-10-13
    ("Blend the Sounds", build_p2_page, True),  # APPROVED 2026-10-13
    ("Count the Sounds", build_p3_page, True),  # APPROVED 2026-10-13
    ("Find the Last Sound", build_p4_page, True),  # APPROVED 2026-10-13
    ("Change the Sound", build_p5_page, True),  # APPROVED 2026-10-13
]


def main():
    for title, _builder, locked in PAGES:
        assert locked, "Page not locked: %s" % title
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                          "worksheets", "kindergarten", "reading",
                          "blending-segmenting")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(outdir, "blending-segmenting-page-%02d.pdf"
                         % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(outdir, "blending-segmenting-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)


if __name__ == "__main__":
    main()
