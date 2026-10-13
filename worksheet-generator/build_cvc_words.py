#!/usr/bin/env python3
"""Kindergarten Reading - CVC Words: Read & Spell (Learning Made Simple).

Phonics & Word Recognition pack. Strictly true CVC words only (3 letters
= 3 phonemes, short vowels): no digraphs, no blends, no x-words, no
silent e. Progression: guided blending -> reading -> guided spelling ->
missing vowel -> independent spelling.

Shared design code (logo, header, footer, circular-masked pictures) is
imported verbatim from build_phonics_az.py - do not fork it here.

Page plan (approved 2026-10-13):
  P1: Blend It (sound dots, guided blending)     (LOCKED 2026-10-13)
  P2: Read & Match (all five vowels)             (LOCKED 2026-10-13)
  P3: Build the Word (letter bank + 3 boxes)     (LOCKED 2026-10-13)
  P4: Missing Vowel                              (LOCKED 2026-10-13)
  P5: Spell It Myself (independent)              (LOCKED 2026-10-13)
"""
import os
import random

from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from build_phonics_az import (NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              _img_circle, draw_footer, draw_header)

# ---------------------------------------------------------------------------
# Page 1 -- Blend It
# Word printed large with a dot under each letter; the child says each
# sound, blends the word, and circles the matching picture. Short a and
# short i only. Exactly one correct picture per item.
# ---------------------------------------------------------------------------
P1_ITEMS = [
    # word, key picture, distractors (name, path)
    ("cat", "animal-library/lib-cat.jpg",
     [("hat", "phonics-a-z/ph-hat.jpg"),
      ("pig", "animal-library/lib-piglet.jpg")]),
    ("pig", "animal-library/lib-piglet.jpg",
     [("pin", "cvc-words/cvc-pin.jpg"),
      ("cat", "animal-library/lib-cat.jpg")]),
    ("map", "cvc-words/cvc-map.jpg",
     [("mop", "blending-segmenting/bs-mop.jpg"),
      ("sun", "phonics-a-z/ph-sun.jpg")]),
    ("sit", "cvc-words/cvc-sit.jpg",
     [("pig", "animal-library/lib-piglet.jpg"),
      ("bat", "blending-segmenting/bs-bat.jpg")]),
    ("bat", "blending-segmenting/bs-bat.jpg",
     [("cat", "animal-library/lib-cat.jpg"),
      ("bus", "blending-segmenting/bs-bus.jpg")]),
    ("pin", "cvc-words/cvc-pin.jpg",
     [("pig", "animal-library/lib-piglet.jpg"),
      ("hat", "phonics-a-z/ph-hat.jpg")]),
]


def _draw_dotted_word(pdf, word, x0, baseline):
    """Lowercase word, Andika-Bold 34, with a teal dot under each letter."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 34)
    centers = []
    x = x0
    for ch in word:
        w = stringWidth(ch, "Andika-Bold", 34)
        pdf.drawString(x, baseline, ch)
        centers.append(x + w / 2)
        x += w + 14
    pdf.setFillColor(TEAL)
    for cx in centers:
        pdf.circle(cx, baseline - 16, 3.2, stroke=0, fill=1)
    return centers


def _blend_it(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Say each sound. Blend the word. "
                          "Circle the picture.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Point to each dot. The child says each sound, "
        "then blends the whole word.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (word, img, distractors) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 166 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        _draw_dotted_word(pdf, word, px0 + 22, py0 + 106)
        choices = [img] + [d[1] for d in distractors]
        order = [0, 1, 2]
        rnd = random.Random(7000 + i)
        rnd.shuffle(order)
        for k, oi in enumerate(order):
            cx = px0 + 47 + k * 78
            _img_circle(pdf, choices[oi], cx, py0 + 33, 30, zoom=True)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "CVC Words: Read & Spell", "Blend It")
    _blend_it(pdf, P1_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Read & Match
# Word printed large WITHOUT sound dots (support removed); the child
# reads the word and circles the picture it names. Exactly one correct
# picture per item.
# ---------------------------------------------------------------------------
P2_ITEMS = [
    # word, key picture, distractors (name, path)
    ("sun", "phonics-a-z/ph-sun.jpg",
     [("moon", "phonics-a-z/ph-moon.jpg"),
      ("bus", "blending-segmenting/bs-bus.jpg")]),
    ("bed", "cvc-words/cvc-bed.jpg",
     [("web", "blending-segmenting/bs-web.jpg"),
      ("sun", "phonics-a-z/ph-sun.jpg")]),
    ("dog", "animal-library/lib-dog.jpg",
     [("pig", "animal-library/lib-piglet.jpg"),
      ("cat", "animal-library/lib-cat.jpg")]),
    ("cup", "blending-segmenting/bs-cup.jpg",
     [("hat", "phonics-a-z/ph-hat.jpg"),
      ("fish", "animal-library/lib-fish.jpg")]),
    ("web", "blending-segmenting/bs-web.jpg",
     [("bee", "blending-segmenting/bs-bee.jpg"),
      ("bed", "cvc-words/cvc-bed.jpg")]),
    ("jam", "phonics-a-z/ph-jam.jpg",
     [("hat", "phonics-a-z/ph-hat.jpg"),
      ("bun", "blending-segmenting/bs-bun.jpg")]),
]


def _read_match(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read the word. Circle the picture.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: The child reads each word aloud, "
        "then circles the picture it names.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (word, img, distractors) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 166 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 34)
        pdf.drawString(px0 + 22, py0 + 100, word)
        choices = [img] + [d[1] for d in distractors]
        order = [0, 1, 2]
        rnd = random.Random(8000 + i)
        rnd.shuffle(order)
        for k, oi in enumerate(order):
            cx = px0 + 47 + k * 78
            _img_circle(pdf, choices[oi], cx, py0 + 33, 30, zoom=True)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "CVC Words: Read & Spell", "Read & Match")
    _read_match(pdf, P2_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Build the Word
# Picture + three large writing boxes; the word's three letters are shown
# SCRAMBLED in a separate dashed letter bank beneath. The child hears the
# sounds in order and writes each letter in its box. All words are true
# CVC (3 letters = 3 phonemes); bank order is never the word order.
# ---------------------------------------------------------------------------
P3_ITEMS = [
    # word, picture, scrambled bank letters
    ("cat", "animal-library/lib-cat.jpg", ["t", "c", "a"]),
    ("pig", "animal-library/lib-piglet.jpg", ["g", "p", "i"]),
    ("bus", "blending-segmenting/bs-bus.jpg", ["s", "u", "b"]),
    ("sun", "phonics-a-z/ph-sun.jpg", ["n", "s", "u"]),
    ("dog", "animal-library/lib-dog.jpg", ["g", "d", "o"]),
    ("cup", "blending-segmenting/bs-cup.jpg", ["p", "c", "u"]),
]


def _build_word(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Look at the picture. Use the letters "
                          "to write the word.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: The child says the word slowly, hears each sound, "
        "and writes the letters in order.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (_word, img, bank) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 166 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        _img_circle(pdf, img, px0 + 48, py0 + 103, 32, zoom=True)
        # three large writing boxes (equal spacing, centers aligned
        # with the picture center at py0 + 103)
        for b in range(3):
            bx = px0 + 96 + b * 42
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(HexColor("#7FA3B5"))
            pdf.setLineWidth(1.2)
            pdf.roundRect(bx, py0 + 83, 36, 40, 4, stroke=1, fill=1)
            pdf.setStrokeColor(HexColor("#D9E7E7"))
            pdf.setLineWidth(0.8)
            pdf.line(bx + 4, py0 + 93, bx + 32, py0 + 93)
        # separate scrambled-letter bank, centered beneath the boxes
        pdf.setStrokeColor(HexColor("#9FB6C9"))
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setLineWidth(1)
        pdf.setDash(4, 3)
        pdf.roundRect(px0 + 89, py0 + 16, 134, 42, 8, stroke=1, fill=0)
        pdf.setDash()
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 20)
        for t, ch in enumerate(bank):
            tx = px0 + 101 + t * 40
            pdf.setStrokeColor(HexColor("#D9E7E7"))
            pdf.roundRect(tx, py0 + 22, 30, 30, 5, stroke=1, fill=0)
            pdf.drawCentredString(tx + 15, py0 + 29, ch)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "CVC Words: Read & Spell", "Build the Word")
    _build_word(pdf, P3_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Missing Vowel
# Picture + the word shown as three boxes with the first and last letters
# given; the middle box is empty (stronger outline) for the child to
# write the missing vowel. All five short vowels; short a appears twice.
# ---------------------------------------------------------------------------
P4_ITEMS = [
    # word, picture, missing vowel
    ("cat", "animal-library/lib-cat.jpg", "a"),
    ("bed", "cvc-words/cvc-bed.jpg", "e"),
    ("pig", "animal-library/lib-piglet.jpg", "i"),
    ("dog", "animal-library/lib-dog.jpg", "o"),
    ("sun", "phonics-a-z/ph-sun.jpg", "u"),
    ("hat", "phonics-a-z/ph-hat.jpg", "a"),
]


def _missing_vowel(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Look at the picture. Write the missing vowel.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: The child says the word slowly "
        "and listens for the middle sound.")
    panel_w, panel_h, gutter = 250, 118, 32
    for i, (word, img, _vowel) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 182 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        _img_circle(pdf, img, px0 + 48, py0 + 59, 32, zoom=True)
        # three boxes aligned with the picture center (py0 + 59),
        # same box geometry as Page 3: first/last letters given,
        # middle box empty (teal outline) for the missing vowel
        for b in range(3):
            bx = px0 + 96 + b * 42
            pdf.setFillColor(HexColor("#FFFFFF"))
            if b == 1:
                pdf.setStrokeColor(TEAL)
                pdf.setLineWidth(1.8)
            else:
                pdf.setStrokeColor(HexColor("#7FA3B5"))
                pdf.setLineWidth(1.2)
            pdf.roundRect(bx, py0 + 39, 36, 40, 4, stroke=1, fill=1)
            pdf.setStrokeColor(HexColor("#D9E7E7"))
            pdf.setLineWidth(0.8)
            pdf.line(bx + 4, py0 + 49, bx + 32, py0 + 49)
            if b != 1:
                pdf.setFillColor(NAVY)
                pdf.setFont("Andika-Bold", 24)
                pdf.drawCentredString(bx + 18, py0 + 48, word[b])


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "CVC Words: Read & Spell", "Missing Vowel")
    _missing_vowel(pdf, P4_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Spell It Myself (independent spelling)
# Picture + three large EMPTY writing boxes only. No letter bank, no
# word hints, no sound dots. Same compact panel layout as Page 4.
# ---------------------------------------------------------------------------
P5_ITEMS = [
    # word, picture
    ("jam", "phonics-a-z/ph-jam.jpg"),
    ("hen", "cvc-words/cvc-hen.jpg"),
    ("mop", "blending-segmenting/bs-mop.jpg"),
    ("van", "blending-segmenting/bs-van.jpg"),
    ("bed", "cvc-words/cvc-bed.jpg"),
    ("rug", "cvc-words/cvc-rug.jpg"),
]


def _spell_myself(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Look at the picture. Say the word. "
                          "Write the letters.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Stretch the word together. The child listens for "
        "each sound and writes the letters.")
    panel_w, panel_h, gutter = 250, 118, 32
    for i, (_word, img) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 182 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        _img_circle(pdf, img, px0 + 48, py0 + 59, 32, zoom=True)
        for b in range(3):
            bx = px0 + 96 + b * 42
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(HexColor("#7FA3B5"))
            pdf.setLineWidth(1.2)
            pdf.roundRect(bx, py0 + 39, 36, 40, 4, stroke=1, fill=1)
            pdf.setStrokeColor(HexColor("#D9E7E7"))
            pdf.setLineWidth(0.8)
            pdf.line(bx + 4, py0 + 49, bx + 32, py0 + 49)


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "CVC Words: Read & Spell", "Spell It Myself")
    _spell_myself(pdf, P5_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Blend It", build_p1_page, True),  # APPROVED 2026-10-13
    ("Read & Match", build_p2_page, True),  # APPROVED 2026-10-13
    ("Build the Word", build_p3_page, True),  # APPROVED 2026-10-13
    ("Missing Vowel", build_p4_page, True),  # APPROVED 2026-10-13
    ("Spell It Myself", build_p5_page, True),  # APPROVED 2026-10-13
]


def main():
    for title, _builder, locked in PAGES:
        assert locked, "Page not locked: %s" % title
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                          "worksheets", "kindergarten", "reading",
                          "cvc-words-read-spell")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(outdir, "cvc-words-read-spell-page-%02d.pdf"
                         % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(outdir, "cvc-words-read-spell-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)


if __name__ == "__main__":
    main()
