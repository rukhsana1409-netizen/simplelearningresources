#!/usr/bin/env python3
"""Kindergarten Reading - Say It & Split It (Learning Made Simple).

Phonological Awareness pack. ORAL-ONLY: no printed words for the
child to decode, no letter chunks, and no pictured answer choices
for the production page.

Approved concept and user revisions (2026-10-16):
  P1: Say a Rhyme (rhyme production, RF.K.2a) -- LOCKED 2026-10-16
      Four clear picture prompts with speech bubbles. The child
      says a rhyme aloud; the adult records it. Drawing is
      optional, not required. Targets: cap, pig, boat, moon
      (map replaced by cap in the approved revision).
  P2: Blend the Word Parts (syllable blending, RF.K.2b)
      -- APPROVED + LOCKED 2026-10-19
      Six oral blending tasks with picture choices; natural spoken
      syllable boundaries and unambiguous answers verified.
      Revised 2026-10-16: NO printed syllable scripts on the child
      page -- each panel simply says "Listen!". The exact spoken
      prompts and answers go into the pack's one-page parent
      answer key at finalization; there is no separate guide.
  P3: Say the Word Parts (syllable segmentation, RF.K.2b)
      -- APPROVED + LOCKED 2026-10-19
      The child says the whole word and then its syllables aloud.
      Familiar compounds plus at least one noncompound
      multisyllabic word; pictures support the oral task rather
      than reducing it to matching component pictures.
      Revised 2026-10-19: words are pancake, toothbrush, popcorn,
      rabbit, potato, umbrella; purely oral -- the split strips
      and line-drawing were removed (no counting, no writing).
  P4: Split the Word (onset-rime segmentation, RF.K.2c)
      -- APPROVED + LOCKED 2026-10-19
      Six picture prompts with simple adult-led oral splitting
      into first sound + remaining spoken chunk.

Shared design code (logo, header, footer, circular-masked
pictures) is imported verbatim from build_phonics_az.py.
"""
import os
import random
import sys

from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

from build_phonics_az import (INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              _img_circle, draw_footer, draw_header)

PANEL_FILL = HexColor("#F4F9F9")
PANEL_LINE = HexColor("#D9E7E7")
GUIDE = HexColor("#7FA3B5")
ADULT = HexColor("#37474F")
OPTIONAL = HexColor("#5F7A86")

# Target word, picture. The target word itself is NOT printed on
# the child page: the adult names the picture aloud, and any real
# or nonsense word with the same ending sound is a correct rhyme.
P1_ITEMS = [
    ("cap", "say-it-split-it/ss-cap.jpg"),
    ("pig", "animal-library/lib-piglet.jpg"),
    ("boat", "informational-text/it-obj-boat.jpg"),
    ("moon", "phonics-a-z/ph-moon.jpg"),
]


def _speech_bubble(pdf, x, y, w, h):
    """White speech bubble with two lines for the adult's record."""
    # small tail circles pointing back toward the picture prompt
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.2)
    pdf.circle(x - 5, y + 16, 5, stroke=1, fill=1)
    pdf.circle(x - 14, y + 7, 3, stroke=1, fill=1)
    # bubble body
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, y, w, h, 16, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(x + 11, y + h - 18, "My rhyme:")
    pdf.setStrokeColor(GUIDE)
    pdf.setLineWidth(1)
    pdf.line(x + 11, y + 36, x + w - 11, y + 36)
    pdf.line(x + 11, y + 16, x + w - 11, y + 16)


def _say_a_rhyme(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Name the picture. Say a word that rhymes.")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 621,
                          "Rhyming words end with the same sound.")
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 104,
        "Adult: Name each picture. Ask for a rhyming word. "
        "Write the word your child says.")
    panel_w, panel_h, gutter = 250, 218, 32
    for i, (_word, img) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 592 - row * (panel_h + 20) - panel_h
        pdf.setFillColor(PANEL_FILL)
        pdf.setStrokeColor(PANEL_LINE)
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        # large picture prompt, upper left of the panel
        _img_circle(pdf, img, px0 + 60, py0 + 158, 47, zoom=True)
        # speech bubble, upper right: the adult records the rhyme
        _speech_bubble(pdf, px0 + 126, py0 + 120, 108, 76)
        # optional drawing space along the bottom (not required)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(PANEL_LINE)
        pdf.roundRect(px0 + 16, py0 + 16, panel_w - 32, 84, 10,
                      stroke=1, fill=1)
        pdf.setFillColor(OPTIONAL)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(px0 + 26, py0 + 84, "Draw it if you wish")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Say It & Split It", "Say a Rhyme")
    _say_a_rhyme(pdf, P1_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Blend the Word Parts (syllable blending)
# Adult says a multisyllabic word one syllable at a time; the child
# blends the parts and circles the picture. The units are whole
# SYLLABLES -- not onset-rime parts and not single phonemes.
# The child page prints NO scripts: each panel says only "Listen!",
# so the task stays oral listening, not reading. The exact spoken
# prompts (the script field in P2_ITEMS) and the correct answers
# go into the pack's one-page parent answer key at finalization.
# Syllable boundaries verified against natural spoken syllables
# (General American): cupcake cup-cake, rainbow rain-bow,
# snowman snow-man, banana ba-na-na, butterfly but-ter-fly
# (3 syllables), elephant el-e-phant (3 syllables).
# Distractors share no syllable with the target and look nothing
# like it, so each panel has exactly one possible answer.
# ---------------------------------------------------------------------------
P2_ITEMS = [
    # word, adult script, key picture, distractors
    ("cupcake", "cup \u2026 cake", "compare-weight/cw2-cupcake.jpg",
     ["phonics-a-z/ph-sun.jpg", "animal-library/lib-fish.jpg"]),
    ("rainbow", "rain \u2026 bow", "all-about-me/aam3-rainbow.jpg",
     ["animal-library/lib-dog.jpg", "blending-segmenting/bs-egg.jpg"]),
    ("snowman", "snow \u2026 man", "informational-text/it-q-snowman.jpg",
     ["animal-library/lib-cat.jpg", "blending-segmenting/bs-bus.jpg"]),
    ("banana", "ba \u2026 na \u2026 na", "sort-count-compare/scc-banana.jpg",
     ["blending-segmenting/bs-bee.jpg", "phonics-a-z/ph-moon.jpg"]),
    ("butterfly", "but \u2026 ter \u2026 fly",
     "living-nonliving/ln-butterfly.jpg",
     ["phonics-a-z/ph-apple.jpg", "blending-segmenting/bs-web.jpg"]),
    ("elephant", "el \u2026 e \u2026 phant", "animal-library/lib-elephant.jpg",
     ["animal-library/lib-piglet.jpg", "phonics-a-z/ph-hat.jpg"]),
]


def _blend_word_parts(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Listen to the word parts. Put them together.")
    pdf.drawCentredString(PAGE_WIDTH / 2, 624, "Circle the picture.")
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Say each word part aloud with a short pause. "
        "Do not say the whole word.")
    panel_w, panel_h, gutter = 248, 158, 36
    for i, (_word, script, img, distractors) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 172 - panel_h
        pdf.setFillColor(PANEL_FILL)
        pdf.setStrokeColor(PANEL_LINE)
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 16)
        pdf.drawString(px0 + 16, py0 + panel_h - 29, "Listen!")
        choices = [img] + list(distractors)
        order = [0, 1, 2]
        rnd = random.Random(7000 + i)
        rnd.shuffle(order)
        for k, oi in enumerate(order):
            cx = px0 + 16 + k * 72 + 36
            cy = py0 + 56
            _img_circle(pdf, choices[oi], cx, cy, 35, zoom=True)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Say It & Split It", "Blend the Word Parts")
    _blend_word_parts(pdf, P2_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Say the Word Parts (syllable segmentation)
# REVISED 2026-10-19 (user): purely oral. The child names the
# picture, says the WHOLE word, then pronounces its syllables
# separately aloud, slowly, one at a time. There is NOTHING to
# write, draw, count, or match: no split strips, no component
# pictures, no numerals -- so this stays distinct from the
# Preschool Clap the Syllables counting activity. Each panel
# holds one large picture only; it names the word and nothing
# more. Words (natural spoken syllable breaks verified):
#   pancake pan-cake, toothbrush tooth-brush, popcorn pop-corn
#   (two-syllable compounds); rabbit rab-bit, potato po-ta-to,
#   umbrella um-brel-la (noncompound). The parts lists are the
#   answer-key data for finalization.
# ---------------------------------------------------------------------------
P3_ITEMS = [
    # word, spoken syllable parts, picture
    ("pancake", ["pan", "cake"], "say-it-split-it/ss-pancake.jpg"),
    ("toothbrush", ["tooth", "brush"], "think-choose/tc-toothbrush.jpg"),
    ("popcorn", ["pop", "corn"], "say-it-split-it/ss-popcorn.jpg"),
    ("rabbit", ["rab", "bit"], "animal-library/lib-rabbit.jpg"),
    ("potato", ["po", "ta", "to"], "say-it-split-it/ss-potato.jpg"),
    ("umbrella", ["um", "brel", "la"], "phonics-a-z/ph-umbrella.jpg"),
]


def _say_the_word_parts(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Say the picture word.")
    pdf.drawCentredString(PAGE_WIDTH / 2, 624,
                          "Now say each syllable slowly, one at a time.")
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Listen as your child says each syllable separately.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 58,
        "Help them pronounce the word parts clearly.")
    panel_w, panel_h, gutter = 248, 158, 36
    for i, (_word, _parts, img) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 172 - panel_h
        pdf.setFillColor(PANEL_FILL)
        pdf.setStrokeColor(PANEL_LINE)
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        # one large picture per panel -- it names the word for the
        # oral task; there is nothing else to do on the panel
        _img_circle(pdf, img, px0 + panel_w / 2, py0 + panel_h / 2,
                    56, zoom=True)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Say It & Split It", "Say the Word Parts")
    _say_the_word_parts(pdf, P3_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Split the Word (onset-rime segmentation)
# The REVERSE of Blending & Segmenting Page 1: there the child
# blended onset + rime into a word; here the child starts from
# the whole word and splits OFF the first sound (onset), saying
# the rest of the word as one chunk (rime). Purely oral: no
# printed letter chunks, no diagrams, no spelling. Each panel
# holds one large picture only. All six words are one syllable
# with a single-consonant onset, and NONE of them appeared in
# Blending & Segmenting's onset-rime blending set (cat, sun, pig,
# bus, hat, fish). The onset/rime fields below are the spoken
# splits for the pack's parent answer key (sounds, not letters):
#   cake /k/ + /ayk/, leaf /l/ + /eef/, boat /b/ + /oht/,
#   rain /r/ + /ayn/, kite /k/ + /iyt/, mouse /m/ + /ows/.
# ---------------------------------------------------------------------------
P4_ITEMS = [
    # word, onset (first sound), rime (remaining chunk), picture
    ("cake", "k", "ake", "compare-weight/cw2-cake.jpg"),
    ("leaf", "l", "eaf", "compare-weight/cw-leaf.jpg"),
    ("boat", "b", "oat", "informational-text/it-obj-boat.jpg"),
    ("rain", "r", "ain", "say-it-split-it/ss-rain.jpg"),
    ("kite", "k", "ite", "phonics-a-z/ph-kite.jpg"),
    ("mouse", "m", "ouse", "story-elements/se-mouse.jpg"),
]


def _split_the_word(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642,
                          "Say the picture word.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 624,
        "Now say the first sound, then the rest of the word.")
    pdf.setFillColor(ADULT)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "Adult: Your child says the whole word first, "
        "then splits off the first sound.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 58,
        "The rest of the word stays together as one chunk. "
        "Sounds only, no letters.")
    panel_w, panel_h, gutter = 248, 158, 36
    for i, (_word, _onset, _rime, img) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 172 - panel_h
        pdf.setFillColor(PANEL_FILL)
        pdf.setStrokeColor(PANEL_LINE)
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        _img_circle(pdf, img, px0 + panel_w / 2, py0 + panel_h / 2,
                    56, zoom=True)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Say It & Split It", "Split the Word")
    _split_the_word(pdf, P4_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Answer-key data for Page 2. The exact spoken prompts (P2_ITEMS
# script field) and the correct answers belong in the pack's
# one-page parent answer key at finalization -- there is NO
# separate parent guide for this pack. Answer positions are
# computed from the same shuffle seeds as the child page, so the
# key can never drift out of sync with the printed panels.
# ---------------------------------------------------------------------------
_POSITIONS = ["left", "middle", "right"]


def _p2_answer_position(i):
    order = [0, 1, 2]
    random.Random(7000 + i).shuffle(order)
    return _POSITIONS[order.index(0)]


if __name__ == "__main__":
    build_p1_page("/tmp/ss-p1.pdf")
    build_p2_page("/tmp/ss-p2.pdf")
    build_p3_page("/tmp/ss-p3.pdf")
    build_p4_page("/tmp/ss-p4.pdf")
    print("built /tmp/ss-p1.pdf .. /tmp/ss-p4.pdf")


# ---------------------------------------------------------------------------
# Parent answer key (one page; NOT part of the child bundle).
# Objective + practical guidance + the spoken material for every
# page: acceptable rhyme examples (P1), the exact spoken syllable
# prompts with answers and picture positions (P2), the natural
# syllable divisions (P3), and the onset-rime sound splits (P4).
# ---------------------------------------------------------------------------
P1_RHYME_EXAMPLES = [
    ("cap", "map, tap, nap"),
    ("pig", "wig, big, fig"),
    ("boat", "coat, goat, float"),
    ("moon", "spoon, noon, tune"),
]


def _key_heading(pdf, y, text):
    pdf.setFillColor(TEAL)
    pdf.setFont("Andika-Bold", 13)
    pdf.drawString(56, y, text)


def _key_line(pdf, y, text, bold_prefix=None):
    pdf.setFillColor(INK)
    if bold_prefix:
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawString(56, y, bold_prefix)
        x = 56 + pdf.stringWidth(bold_prefix, "Helvetica-Bold", 10.5)
        pdf.setFont("Helvetica", 10.5)
        pdf.drawString(x, y, text)
    else:
        pdf.setFont("Helvetica", 10.5)
        pdf.drawString(56, y, text)


def build_answer_key(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Say It & Split It", "Parent Answer Key")
    # -- learning objective --------------------------------------------
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(56, 646, "What your child is learning")
    _key_line(pdf, 628,
              "These pages build phonological awareness \u2014 hearing and "
              "playing with the sounds")
    _key_line(pdf, 612,
              "in spoken words (Michigan RF.K.2). Everything is oral: your "
              "child listens and")
    _key_line(pdf, 596,
              "speaks. There are no letters to read and nothing to write.")
    # -- Page 1 ---------------------------------------------------------
    _key_heading(pdf, 562, "Page 1 \u2014 Say a Rhyme")
    _key_line(pdf, 544,
              "Any word with the same ending sound counts \u2014 a real word "
              "or a made-up one.")
    for j, (target, examples) in enumerate(P1_RHYME_EXAMPLES):
        x = 56 if j % 2 == 0 else 316
        y = 522 - (j // 2) * 18
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawString(x, y, target)
        pdf.setFont("Helvetica", 10.5)
        pdf.drawString(x + pdf.stringWidth(target, "Helvetica-Bold", 10.5),
                       y, "  \u2192  " + examples)
    # -- Page 2 ---------------------------------------------------------
    _key_heading(pdf, 468, "Page 2 \u2014 Blend the Word Parts")
    _key_line(pdf, 450,
              "Say each part with a short pause. Do not say the whole "
              "word first.")
    for i, (word, script, _img, _dist) in enumerate(P2_ITEMS):
        x = 56 if i % 2 == 0 else 316
        y = 428 - (i // 2) * 18
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 10.5)
        pdf.drawString(x, y, "%d. %s  \u2192  %s (%s picture)" % (
            i + 1, script, word, _p2_answer_position(i)))
    # -- Page 3 ---------------------------------------------------------
    _key_heading(pdf, 374, "Page 3 \u2014 Say the Word Parts")
    _key_line(pdf, 356,
              "Your child says the whole word, then each syllable "
              "separately. The parts are:")
    for j in range(2):
        row = P3_ITEMS[j * 3:(j + 1) * 3]
        text = "      ".join("%s: %s" % (w, "-".join(parts))
                             for w, parts, _i in row)
        _key_line(pdf, 334 - j * 18, text)
    # -- Page 4 ---------------------------------------------------------
    _key_heading(pdf, 280, "Page 4 \u2014 Split the Word")
    _key_line(pdf, 262,
              "First sound, then the rest of the word as one chunk "
              "(sounds, not letter names):")
    for j in range(2):
        row = P4_ITEMS[j * 3:(j + 1) * 3]
        text = "      ".join("%s: %s \u2026 %s" % (w, onset, rime)
                             for w, onset, rime, _i in row)
        _key_line(pdf, 240 - j * 18, text)
    # -- practical guidance ---------------------------------------------
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(56, 186, "Tips for parents")
    _key_line(pdf, 168,
              "\u2022  Keep it playful and short \u2014 a few minutes at a "
              "time is plenty.")
    _key_line(pdf, 150,
              "\u2022  If a part is hard to hear, say the whole word slowly "
              "together, then try again.")
    _key_line(pdf, 132,
              "\u2022  Praise every try. Hearing the sounds in words grows "
              "with practice.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Finalization (all four pages approved & locked 2026-10-19):
# bundle + individual page PDFs + separate parent answer key.
# ---------------------------------------------------------------------------
LOCKED = {1: True, 2: True, 3: True, 4: True}
PACK_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "worksheets", "kindergarten", "reading", "say-it-split-it")


def main():
    assert all(LOCKED.values()), "all four pages must be locked"
    os.makedirs(PACK_DIR, exist_ok=True)
    from pypdf import PdfWriter
    builders = [build_p1_page, build_p2_page, build_p3_page,
                build_p4_page]
    writer = PdfWriter()
    for n, build in enumerate(builders, start=1):
        page_path = os.path.join(
            PACK_DIR, "say-it-split-it-page-%02d.pdf" % n)
        build(page_path)
        writer.append(page_path)
    bundle = os.path.join(PACK_DIR, "say-it-split-it-review.pdf")
    with open(bundle, "wb") as fh:
        writer.write(fh)
    build_answer_key(os.path.join(
        PACK_DIR, "say-it-split-it-answer-key.pdf"))
    print("finalized into", PACK_DIR)


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "finalize":
    main()
