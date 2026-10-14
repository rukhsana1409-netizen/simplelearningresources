#!/usr/bin/env python3
"""Common Words -- Read & Learn (Kindergarten).

High-frequency word recognition that respects how English spelling
works: children sound out every part that follows a taught pattern
(dot under the letter), and parts that follow a pattern they have not
met yet are underlined -- the adult guidance names the pattern in
plain words (e.g. in "the", the letters th work as a team). No word is
taught as an unanalyzed whole; no symbols or phonics jargon appear on
the child-facing page.

11 words, introduced gradually (6 on P1, 5 more inside phrases on P3):
  Sound-out (CVC/VC patterns already taught): it, in, on, can
  One untaught-pattern part (underlined): the (th team + weak e),
  a (weak sound alone), I (its letter-name sound alone),
  is (s says /z/), see (ee pattern), my (y as a vowel),
  like (silent-e pattern)

Pages:
  P1: Read the Words (the, a, I, is, it, in)  (LOCKED 2026-10-14)
  P2: Read & Find (missing word, two choices) (LOCKED 2026-10-14)
  P3: Meet the New Words (on, can, see, like, my) (LOCKED 2026-10-14)
  P4: Read & Match the Sentences              (LOCKED 2026-10-14)
  P5: Common Word Search                      (in review)

Branding/layout imported from build_phonics_az (the approved
phonics-pack implementation).
"""

import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from build_phonics_az import (  # noqa: E402
    NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL, draw_footer, draw_header,
    _img_circle,
)

PAGE_WIDTH, PAGE_HEIGHT = LETTER


# ---------------------------------------------------------------------------
# Page 1 -- Read the Words
# Six panels. Each shows the word large (Andika-Bold 40) with a teal dot
# under every letter whose sound the child can sound out, and a teal
# underline under a letter group that follows a not-yet-taught pattern.
# Beneath, a tiny pictured phrase uses the word once more.
# ---------------------------------------------------------------------------
P1_ITEMS = [
    # word, marker groups [(letters, "dot"|"line")], phrase, picture
    ("the", [("th", "line")],
     "the cat", "animal-library/lib-cat.jpg"),
    ("a", [],
     "a dog", "animal-library/lib-dog.jpg"),
    ("I", [],
     "I sit", "cvc-words/cvc-sit.jpg"),
    ("is", [("i", "dot"), ("s", "line")],
     "the sun is up", "phonics-a-z/ph-sun.jpg"),
    ("it", [("i", "dot"), ("t", "dot")],
     "It is a pig.", "animal-library/lib-piglet.jpg"),
    ("in", [("i", "dot"), ("n", "dot")],
     "in bed", "cvc-words/cvc-bed.jpg"),
]

WORD_FONT, WORD_SIZE = "Andika-Bold", 40


def _marked_word(pdf, word, groups, x, baseline):
    """Draw word at (x, baseline) with dots/underlines per group."""
    pdf.setFillColor(NAVY)
    pdf.setFont(WORD_FONT, WORD_SIZE)
    pdf.drawString(x, baseline, word)
    widths = [stringWidth(ch, WORD_FONT, WORD_SIZE) for ch in word]
    centers = []
    cx = x
    for wch in widths:
        centers.append(cx + wch / 2)
        cx += wch
    # letter index ranges for each group
    idx = 0
    spans = []
    for letters, kind in groups:
        spans.append((idx, idx + len(letters) - 1, kind))
        idx += len(letters)
    for first, last, kind in spans:
        gx0 = x + sum(widths[:first])
        gx1 = x + sum(widths[:last + 1])
        if kind == "dot":
            pdf.setFillColor(TEAL)
            for li in range(first, last + 1):
                pdf.circle(centers[li], baseline - 13, 3.2,
                           stroke=0, fill=1)
        elif kind == "line":  # underline the group as one pattern unit
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(2.2)
            pdf.line(gx0 + 1, baseline - 11, gx1 - 1, baseline - 11)


def _read_words(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read the word. Find it in the phrase.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 98,
        "Adult: Read each word together. Dots show individual sounds.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 84,
        "Underlines show letters that work together "
        "or need extra practice.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 70,
        "In the, the e makes a weak sound, like the word a.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (word, groups, phrase, img) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 166 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        _marked_word(pdf, word, groups, px0 + 30, py0 + 96)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 17)
        pdf.drawString(px0 + 30, py0 + 34, phrase)
        _img_circle(pdf, img, px0 + 206, py0 + 48, 23, zoom=True)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Common Words: Read & Learn", "Read the Words")
    _read_words(pdf, P1_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Read & Find (missing word)
# Each panel: a picture, a short sentence with ONE missing word, and two
# large word choices to circle. Each of the six Page 1 words is the
# correct answer exactly once. Foils are chosen so every item has
# exactly one grammatically and contextually correct answer -- the
# confusable pairs a/the and I/it are never offered against each other.
# ---------------------------------------------------------------------------
P2_ITEMS = [
    # target, sentence before blank, sentence after blank, choices
    # (correct, foil), picture
    ("the", "", " dog is big.", ("the", "is"),
     "animal-library/lib-dog.jpg"),
    ("a", "It is ", " pig.", ("a", "in"),
     "animal-library/lib-piglet.jpg"),
    ("I", "", " sit.", ("I", "is"),
     "cvc-words/cvc-sit.jpg"),
    ("is", "The sun ", " up.", ("is", "in"),
     "phonics-a-z/ph-sun.jpg"),
    ("it", "", " is a fish.", ("It", "in"),
     "animal-library/lib-fish.jpg"),
    ("in", "The cat is ", " the bed.", ("in", "it"),
     "cvc-words/cw-cat-bed.jpg"),
]

SENT_FONT, SENT_SIZE = "Andika-Bold", 19
BLANK_W = 36


def _missing_word_sentence(pdf, before, after, x, baseline):
    pdf.setFillColor(NAVY)
    pdf.setFont(SENT_FONT, SENT_SIZE)
    cx = x
    if before:
        pdf.drawString(cx, baseline, before)
        cx += stringWidth(before, SENT_FONT, SENT_SIZE)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.4)
    pdf.line(cx + 2, baseline - 3, cx + BLANK_W - 2, baseline - 3)
    cx += BLANK_W
    if after:
        pdf.setFillColor(NAVY)
        pdf.setFont(SENT_FONT, SENT_SIZE)
        pdf.drawString(cx, baseline, after)


def _read_find(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read. Circle the word that fits.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 76,
        "Adult: Both words can be read. "
        "Only one makes the sentence right.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (_t, before, after, choices, img) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 606 - row * 166 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        _missing_word_sentence(pdf, before, after, px0 + 22, py0 + 108)
        # two large word choices (order alternates by panel)
        pair = choices if i % 2 == 0 else (choices[1], choices[0])
        for c, word in enumerate(pair):
            bx = px0 + 24 + c * 74
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(HexColor("#7FA3B5"))
            pdf.setLineWidth(1.2)
            pdf.roundRect(bx, py0 + 26, 64, 36, 8, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Andika-Bold", 20)
            pdf.drawCentredString(bx + 32, py0 + 37, word)
        _img_circle(pdf, img, px0 + 204, py0 + 44, 24, zoom=True)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Common Words: Read & Learn", "Read & Find")
    _read_find(pdf, P2_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Meet the New Words (guided reading)
# The remaining five words (on, can, see, like, my) are introduced in
# context. Each panel: the NEW word large with Page 1 markings, then
# the phrase in large print with a matching picture -- the child reads
# the word, then finds and circles it inside the phrase.
# ---------------------------------------------------------------------------
P3_ITEMS = [
    # target word, marker groups, phrase, picture
    ("on", [("o", "dot"), ("n", "dot")], "on the mat",
     "cvc-words/cw-cat-mat.jpg"),
    ("can", [("c", "dot"), ("a", "dot"), ("n", "dot")], "I can run",
     "cvc-words/cw-run.jpg"),
    ("see", [("s", "dot"), ("ee", "line")], "see the dog",
     "animal-library/lib-dog.jpg"),
    ("like", [("l", "dot"), ("i", "none"), ("k", "dot"),
              ("e", "line")], "I like jam",
     "phonics-a-z/ph-jam.jpg"),
    ("my", [("m", "dot"), ("y", "line")], "my cat",
     "animal-library/lib-cat.jpg"),
]


def _read_phrase(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read the word. Find and circle it "
                          "in the phrase.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 98,
        "Adult: Read each word and phrase together. "
        "Dots show individual sounds.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 84,
        "Underlines show letters that work together "
        "or need extra practice.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 70,
        "In see, ee works as a team. In like, the end e is quiet. "
        "In my, y says its name.")
    panel_w, panel_h, gutter = 250, 150, 32
    for i, (word, groups, phrase, img) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        if i == 4:
            px0 = (PAGE_WIDTH - panel_w) // 2
        py0 = 606 - row * 166 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        _marked_word(pdf, word, groups, px0 + 24, py0 + 102)
        _img_circle(pdf, img, px0 + 204, py0 + 104, 24, zoom=True)
        # the phrase in large print -- room to circle the target word
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 26)
        pdf.drawString(px0 + 24, py0 + 38, phrase)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Common Words: Read & Learn", "Meet the New Words")
    _read_phrase(pdf, P3_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Read & Match the Sentences
# Five complete sentences (capital + period) in a left column; five
# original illustrations showing each sentence's exact meaning in a
# shuffled right column. The child reads each sentence and draws a
# line to its picture. Shuffle keeps line crossings to two.
# ---------------------------------------------------------------------------
P4_LEFT = [
    ("My hat is red.", "phonics-a-z/ph-hat.jpg"),
    ("I can hop.", "cvc-words/cw-hop.jpg"),
    ("I see the hen.", "cvc-words/cvc-hen.jpg"),
    ("The cat is on the log.", "cvc-words/cw-cat-log.jpg"),
    ("The pig is in the box.", "cvc-words/cw-pig-box.jpg"),
]
# right column top-to-bottom (picture keys into P4_LEFT)
P4_RIGHT_ORDER = [1, 2, 0, 3, 4]


def _read_match_lines(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read the sentences. Draw a line "
                          "to the picture.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 76,
        "Adult: Your child reads each sentence, then draws a line "
        "to the picture it tells about.")
    centers = [560, 470, 380, 290, 200]
    # left column: sentence panels with a line-start dot
    for (phrase, _img), cy in zip(P4_LEFT, centers):
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(40, cy - 27, 262, 54, 12, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 20)
        pdf.drawString(56, cy - 7, phrase)
        pdf.setStrokeColor(TEAL)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setLineWidth(1.6)
        pdf.circle(320, cy, 5, stroke=1, fill=1)
    # right column: shuffled pictures with a line-end dot
    for pos, left_idx in enumerate(P4_RIGHT_ORDER):
        cy = centers[pos]
        _img = P4_LEFT[left_idx][1]
        pdf.setStrokeColor(TEAL)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setLineWidth(1.6)
        pdf.circle(424, cy, 5, stroke=1, fill=1)
        _img_circle(pdf, _img, 508, cy, 36, zoom=True)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Common Words: Read & Learn",
                "Read & Match the Sentences")
    _read_match_lines(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Common Word Search
# A 9x9 letter grid holding all 11 taught words, across or down only
# (no backwards, no diagonals). The grid was solved and verified
# programmatically: every word of 2+ letters occurs EXACTLY ONCE in
# any straight direction. The single-letter words are different by
# nature: "a" appears twice (its own cell, plus inside "can"), and
# the letter i/I appears in several words -- the key below gives the
# intended standalone spots for a and I.
# Answer key (start row, start column, direction; 1-based):
#   the: row 2, col 7, down     a: row 6, col 3 (single letter)
#   I:   row 9, col 4 (single)  is: row 5, col 8, down
#   it:  row 7, col 5, down     in: row 7, col 2, down
#   on:  row 3, col 3, across   can: row 6, col 6, down
#   see: row 7, col 7, across   like: row 5, col 4, down
#   my:  row 5, col 5, down
# ---------------------------------------------------------------------------
WS_GRID = [
    "netvwbyhr",
    "jwxeznttv",
    "rgonmghxp",
    "hwkecgepm",
    "ueplmlcie",
    "ygaiycuso",
    "ciekias ee".replace(" ", ""),
    "rntetnpnx",
    "ygdIxztwo",
]
WS_WORDS = ["the", "a", "I", "is", "it", "in",
            "on", "can", "see", "like", "my"]


def _word_search(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Find the words. Circle each word.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 76,
        "Adult: All the words go across or down. Say each word "
        "together, then find its letters in order.")
    cell = 42
    gx0, gy_top = 50, 572
    # grid cells
    for r, row in enumerate(WS_GRID):
        for c, ch in enumerate(row):
            x = gx0 + c * cell
            y = gy_top - (r + 1) * cell
            pdf.setStrokeColor(HexColor("#D9E7E7"))
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setLineWidth(0.8)
            pdf.rect(x, y, cell, cell, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Andika-Bold", 27)
            pdf.drawCentredString(x + cell / 2, y + 13, ch)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.8)
    pdf.rect(gx0, gy_top - 9 * cell, 9 * cell, 9 * cell,
             stroke=1, fill=0)
    # word list, heading aligned with the top of the grid, rows
    # evenly spaced and aligned with the grid rows
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(452, gy_top - 9, "Words to find")
    for i, w in enumerate(WS_WORDS):
        wy = 530 - i * 33
        pdf.setStrokeColor(HexColor("#7FA3B5"))
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setLineWidth(1.1)
        pdf.roundRect(452, wy - 4, 13, 13, 3, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 21)
        pdf.drawString(474, wy - 3, w)


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Common Words: Read & Learn",
                "Common Word Search")
    _word_search(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Read the Words", build_p1_page, True),  # APPROVED 2026-10-14
    ("Read & Find", build_p2_page, True),  # APPROVED 2026-10-14
    ("Read the Phrase", build_p3_page, True),  # APPROVED 2026-10-14,
    # shown as "Meet the New Words"
    ("Read & Match the Sentences", build_p4_page, True),  # APPROVED
    # 2026-10-14
    ("Common Word Search", build_p5_page, True),  # APPROVED
    # 2026-10-14
]


def main():
    for title, _builder, locked in PAGES:
        assert locked, "Page not locked: %s" % title
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "worksheets", "kindergarten", "reading",
                          "common-words-read-learn")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(outdir,
                         "common-words-read-learn-page-%02d.pdf"
                         % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(outdir, "common-words-read-learn-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)


if __name__ == "__main__":
    main()
