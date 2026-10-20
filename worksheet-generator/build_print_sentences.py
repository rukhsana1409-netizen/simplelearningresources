"""Understanding Print & Sentences -- Kindergarten Reading & Language
(Alphabet & Print Concepts).

Five pages teaching how print works: letters vs words vs sentences,
spaces between words, capital letters and end marks, reading
direction, and a final combined passage. Everything is recognition
and identification -- no letter tracing or letter naming (preschool
packs cover those), and no sentence writing (a later pack).

All sentences use the 11 common words from Common Words -- Read &
Learn plus familiar decodable CVC words, so children can read every
word on the page.

Pages:
  P1: Let's Learn About Letters, Words & Sentences (LOCKED 2026-10-14)
  P2: Spaces Between Words                  (LOCKED 2026-10-14)
  P3: Beginning & Ending a Sentence         (LOCKED 2026-10-14)
  P4: Follow the Words                      (LOCKED 2026-10-14)
  P5: Put It Together                       (LOCKED 2026-10-14)

Run with the repo venv:
  ../.venv/bin/python build_print_sentences.py
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

PACK_TITLE = "Understanding Print & Sentences"


def _panel(pdf, px0, py0, w, h):
    pdf.setFillColor(HexColor("#F4F9F9"))
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.roundRect(px0, py0, w, h, 14, stroke=1, fill=1)


# ---------------------------------------------------------------------------
# Page 1 -- Let's Learn About Letters, Words & Sentences (teaching page)
# Three spacious sections, one per idea, each with its own soft tint:
# LETTER (one big symbol + example letter tiles), WORD (letter tiles
# build into the word), SENTENCE (the full sentence with a picture).
# A recap strip at the bottom repeats the whole progression.
# No questions on this page -- it teaches.
# ---------------------------------------------------------------------------
P1_TINTS = [
    (HexColor("#F4F9F9"), HexColor("#D9E7E7")),
    (HexColor("#FDF8EE"), HexColor("#EBDCBE")),
    (HexColor("#F5F3FA"), HexColor("#DCD6EA")),
]


def _section(pdf, py0, h, idx, label):
    fill, border = P1_TINTS[idx]
    pdf.setFillColor(fill)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1)
    pdf.roundRect(40, py0, 532, h, 14, stroke=1, fill=1)
    pdf.setFillColor(TEAL)
    pdf.roundRect(56, py0 + h - 36, 108, 24, 8, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(110, py0 + h - 28, "%d  %s" % (idx + 1, label))


def _down_arrow(pdf, cx, cy):
    pdf.setFillColor(TEAL)
    p = pdf.beginPath()
    p.moveTo(cx - 7, cy + 5)
    p.lineTo(cx + 7, cy + 5)
    p.lineTo(cx, cy - 6)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)


def _right_arrow(pdf, x, cy):
    pdf.setStrokeColor(TEAL)
    pdf.setFillColor(TEAL)
    pdf.setLineWidth(2.4)
    pdf.line(x, cy, x + 20, cy)
    p = pdf.beginPath()
    p.moveTo(x + 20, cy - 5)
    p.lineTo(x + 30, cy)
    p.lineTo(x + 20, cy + 5)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)


def _tile(pdf, x, y, w, h, text, size):
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(HexColor("#7FA3B5"))
    pdf.setLineWidth(1.2)
    pdf.roundRect(x, y, w, h, 8, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", size)
    pdf.drawCentredString(x + w / 2, y + h / 2 - size * 0.36, text)


def _explain(pdf, py0, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 20)
    pdf.drawString(64, py0 + 26, text)


def _letters_words_sentences(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 648,
                          "Letters make words. Words make sentences.")
    tops = [622, 464, 306]
    h = 144
    # 1 -- LETTER
    py0 = tops[0] - h
    _section(pdf, py0, h, 0, "LETTER")
    for j, ch in enumerate(["c", "a", "t"]):
        _tile(pdf, 120 + j * 96, py0 + 48, 58, 60, ch, 36)
    _explain(pdf, py0, "A letter is one symbol.")
    _down_arrow(pdf, PAGE_WIDTH / 2, tops[1] + 7)
    # 2 -- WORD
    py0 = tops[1] - h
    _section(pdf, py0, h, 1, "WORD")
    for j, ch in enumerate(["c", "a", "t"]):
        _tile(pdf, 84 + j * 66, py0 + 48, 48, 50, ch, 30)
        if j < 2:
            pdf.setFillColor(NAVY)
            pdf.setFont("Andika-Bold", 24)
            pdf.drawCentredString(84 + j * 66 + 57, py0 + 64, "+")
    _right_arrow(pdf, 292, py0 + 73)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 44)
    pdf.drawString(340, py0 + 56, "cat")
    _explain(pdf, py0, "Letters together make a word.")
    _down_arrow(pdf, PAGE_WIDTH / 2, tops[2] + 7)
    # 3 -- SENTENCE
    py0 = tops[2] - h
    _section(pdf, py0, h, 2, "SENTENCE")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 31)
    pdf.drawString(64, py0 + 70, "The cat is big.")
    # subtle underline connects "cat" back to the WORD section
    ux0 = 64 + stringWidth("The ", "Andika-Bold", 31)
    ux1 = ux0 + stringWidth("cat", "Andika-Bold", 31)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(ux0 + 1, py0 + 62, ux1 - 1, py0 + 62)
    _img_circle(pdf, "animal-library/lib-cat.jpg", 500, py0 + 70, 26,
                zoom=True)
    _explain(pdf, py0, "Words together tell a complete idea.")
    # recap strip: c + a + t -> cat -> The cat is big.
    pdf.setFont("Andika-Bold", 20)
    segs = [("c", "t"), ("+", "p"), ("a", "t"), ("+", "p"),
            ("t", "t"), ("", "a"), ("cat", "t"), ("", "a"),
            ("The cat is big.", "t")]
    total = 0
    for text, kind in segs:
        if kind == "t":
            total += stringWidth(text, "Andika-Bold", 20)
        elif kind == "p":
            total += stringWidth("+", "Andika-Bold", 20) + 10
        else:
            total += 44
    x = (PAGE_WIDTH - total) / 2
    for text, kind in segs:
        if kind == "t":
            pdf.setFillColor(NAVY)
            pdf.setFont("Andika-Bold", 20)
            pdf.drawString(x, 118, text)
            x += stringWidth(text, "Andika-Bold", 20)
        elif kind == "p":
            pdf.setFillColor(NAVY)
            pdf.setFont("Andika-Bold", 20)
            pdf.drawString(x + 5, 118, "+")
            x += stringWidth("+", "Andika-Bold", 20) + 10
        else:
            _right_arrow(pdf, x + 8, 124)
            x += 44
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 78,
        "Adult: Read the page together. Point to each part "
        "as you name it.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE,
                "Let's Learn About Letters, Words & Sentences",
                title_size=19.5)
    _letters_words_sentences(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Spaces Between Words
# Teaching example: the words of "I see the sun." in separate boxes
# with numbers under them. Then four counting rows (sentence + picture
# + answer box) and one fix-it panel where the spaces are missing and
# the child draws a line for each space. All counts verified.
# ---------------------------------------------------------------------------
P2_COUNT = [
    ("I see the cat.", 4, "animal-library/lib-cat.jpg"),
    ("The hen can run.", 4, "cvc-words/cw-hen-run.jpg"),
    ("It is a big sun.", 5, "phonics-a-z/ph-sun.jpg"),
    ("The pig is in the box.", 6, "cvc-words/cw-pig-box.jpg"),
]
P2_TEACH_WORDS = ["I", "see", "the", "sun."]


def _spaces_between_words(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Count the words. Write the number.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 68,
        "Adult: Words have spaces between them. Touch each word "
        "as you count.")
    # teaching example
    _panel(pdf, 40, 522, 532, 104)
    x = 66
    for i, w in enumerate(P2_TEACH_WORDS):
        tw = stringWidth(w, "Andika-Bold", 24)
        bw = tw + 20
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(TEAL)
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, 552, bw, 44, 8, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 24)
        pdf.drawCentredString(x + bw / 2, 566, w)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(x + bw / 2, 536, str(i + 1))
        x += bw + 14
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 17)
    pdf.drawString(408, 584, "This sentence")
    pdf.drawString(408, 562, "has 4 words.")
    # counting rows
    for i, (sentence, _n, img) in enumerate(P2_COUNT):
        top = 506 - i * 84
        _panel(pdf, 40, top - 66, 532, 66)
        cy = top - 33
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 22)
        pdf.drawString(62, cy - 8, sentence)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(HexColor("#7FA3B5"))
        pdf.setLineWidth(1.4)
        pdf.roundRect(408, cy - 19, 38, 38, 8, stroke=1, fill=1)
        pdf.setFillColor(HexColor("#37474F"))
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(452, cy - 4, "words")
        _img_circle(pdf, img, 524, cy, 21, zoom=True)
    # fix-it panel: a worked example with the divider lines drawn,
    # then "Ilikejam." for the child to separate on their own
    _panel(pdf, 40, 84, 532, 96)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(62, 160,
                   "Oops! The spaces are missing. Draw a line "
                   "to show each space.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(62, 130, "Example:")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 20)
    pdf.drawString(140, 124, "Iseeit.")
    for part in ("I", "Isee"):
        dx = 140 + stringWidth(part, "Andika-Bold", 20)
        pdf.setStrokeColor(TEAL)
        pdf.setLineWidth(1.8)
        pdf.line(dx, 116, dx, 138)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 24)
    pdf.drawString(90, 96, "Ilikejam.")
    _img_circle(pdf, "phonics-a-z/ph-jam.jpg", 524, 112, 18, zoom=True)


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Spaces Between Words", title_size=19.5)
    _spaces_between_words(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Beginning & Ending a Sentence
# Teaching panel first: capitals (t -> T, with the capital in a model
# sentence underlined) and the three end marks, each with a model
# sentence and its job (tells / asks / big feeling). Practice:
# (1) circle the correctly capitalized sentence (2 rows);
# (2) circle the right end mark (3 rows) -- pairs are chosen so the
# answer is decided by sentence form alone: statements and questions
# are only ever paired with each other, never against "!", and the
# exclamation item uses the "What a ...!" form paired against "?".
# ---------------------------------------------------------------------------
P3_CAPITAL_ROWS = [
    ("the dog can run.", "The dog can run."),
    ("I see the hen.", "i see the hen."),
]
P3_MARK_ROWS = [
    ("Can the pig run", [".", "?"], "?"),
    ("The pig can run", [".", "?"], "."),
    ("What a big pig", ["?", "!"], "!"),
]


def _beginning_ending(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "A sentence starts with a capital letter "
                          "and ends with a mark.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 88,
        "Adult: Every sentence starts with a capital letter.")
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 74,
        "The end mark tells how to read it: telling, asking, "
        "or a big feeling.")
    # teaching panel
    _panel(pdf, 40, 500, 532, 126)
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.line(340, 512, 340, 614)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(56, 604, "STARTS WITH A CAPITAL LETTER")
    _tile(pdf, 56, 542, 42, 44, "t", 26)
    _right_arrow(pdf, 106, 564)
    _tile(pdf, 142, 542, 42, 44, "T", 26)
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 16)
    pdf.drawString(204, 558, "The cat is big.")
    ux0 = 204
    ux1 = ux0 + stringWidth("T", "Andika-Bold", 16)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.8)
    pdf.line(ux0, 552, ux1, 552)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(356, 604, "ENDS WITH A MARK")
    models = [
        (".", "The cat is big.", "tells"),
        ("?", "Can the cat run?", "asks"),
        ("!", "The cat is big!", "big feeling"),
    ]
    for i, (mark, sent, job) in enumerate(models):
        by = 578 - i * 27
        pdf.setFillColor(TEAL)
        pdf.setFont("Andika-Bold", 20)
        pdf.drawString(352, by, mark)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 14.5)
        pdf.drawString(374, by, sent)
        pdf.setFillColor(HexColor("#37474F"))
        pdf.setFont("Helvetica", 11)
        pdf.drawRightString(560, by, job)
    # part 1: capitalization
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawString(40, 478,
                   "Circle the sentence that is written "
                   "the right way.")
    for i, (opt_a, opt_b) in enumerate(P3_CAPITAL_ROWS):
        top = 468 - i * 68
        _panel(pdf, 40, top - 56, 532, 56)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 19)
        pdf.drawString(62, top - 36, opt_a)
        pdf.drawString(322, top - 36, opt_b)
    # part 2: end marks
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawString(40, 322, "Read the sentence. Circle the right "
                            "end mark.")
    for i, (sentence, marks, _ans) in enumerate(P3_MARK_ROWS):
        top = 312 - i * 60
        _panel(pdf, 40, top - 52, 532, 52)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 20)
        pdf.drawString(62, top - 33, sentence)
        for c, mark in enumerate(marks):
            bx = 448 + c * 54
            pdf.setFillColor(HexColor("#FFFFFF"))
            pdf.setStrokeColor(HexColor("#7FA3B5"))
            pdf.setLineWidth(1.2)
            pdf.roundRect(bx, top - 46, 42, 42, 8, stroke=1, fill=1)
            pdf.setFillColor(NAVY)
            pdf.setFont("Andika-Bold", 24)
            pdf.drawCentredString(bx + 21, top - 36, mark)


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Beginning & Ending a Sentence", title_size=19.5)
    _beginning_ending(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Follow the Words
# Three DISTINCT sections teaching different parts of print direction:
# 1) Read with me (guided): a two-line sentence with a numbered dot
#    under every word (1-6) so the reading path -- left to right, then
#    down and back to the start of the next line -- cannot be
#    misread; one pale hook arrow marks the turn.
# 2) Your turn to read (independent): a two-line sentence with no
#    path shown; the child finds the first word (dot under it) and
#    the last word (circle it).
# 3) Choose the next words: line 1 is given; the child reads it,
#    moves down, and circles the line 2 that truly continues it
#    (picture + meaning decide).
# ---------------------------------------------------------------------------
P4_S1 = ("The cat is on", "the mat.", "cvc-words/cw-cat-mat.jpg")
P4_S2 = ("I can see", "the big dog.", "animal-library/lib-dog.jpg")
P4_S3 = ("The pig is in", ["the box.", "the sun."], "the box.",
         "cvc-words/cw-pig-box.jpg")
ARROW_PALE = HexColor("#9FC4C4")


def _p4_tag(pdf, py0, h, num, title):
    pdf.setFillColor(TEAL)
    pdf.roundRect(56, py0 + h - 34, 26, 22, 7, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(69, py0 + h - 27, str(num))
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawString(92, py0 + h - 27, title)


def _numbered_line(pdf, words, x0, baseline, first_num):
    """Draw one line of words with a numbered teal dot under each."""
    pdf.setFont("Andika-Bold", 22)
    space = stringWidth(" ", "Andika-Bold", 22)
    cx = x0
    for i, w in enumerate(words):
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 22)
        pdf.drawString(cx, baseline, w)
        w_w = stringWidth(w, "Andika-Bold", 22)
        pdf.setFillColor(TEAL)
        pdf.circle(cx + w_w / 2, baseline - 17, 8, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawCentredString(cx + w_w / 2, baseline - 20.5,
                              str(first_num + i))
        cx += w_w + space
    return cx - space  # end x of the line's text


def _follow_the_words(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "We read from left to right, then down "
                          "to the next line.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 76,
        "Adult: We read from left to right. At the end of a line, "
        "we go down to the next line.")
    h = 152
    # -- section 1: guided example with numbered words
    py0 = 630 - h
    _panel(pdf, 40, py0, 532, h)
    _p4_tag(pdf, py0, h, 1, "Read with me. Follow the numbers.")
    line1, line2, img = P4_S1
    x0 = 88
    y1, y2 = py0 + 84, py0 + 38
    _numbered_line(pdf, line1.split(), x0, y1, 1)
    _numbered_line(pdf, line2.split(), x0, y2, 5)
    # small pale start arrows before each line: direction of travel,
    # nothing crosses the words or the numbered dots
    pdf.setStrokeColor(ARROW_PALE)
    pdf.setFillColor(ARROW_PALE)
    pdf.setLineWidth(1.6)
    for yy in (y1, y2):
        pdf.line(x0 - 30, yy + 7, x0 - 13, yy + 7)
        head = pdf.beginPath()
        head.moveTo(x0 - 6, yy + 7)
        head.lineTo(x0 - 15, yy + 2.5)
        head.lineTo(x0 - 15, yy + 11.5)
        head.close()
        pdf.drawPath(head, stroke=0, fill=1)
    _img_circle(pdf, img, 500, py0 + 68, 26, zoom=True)
    # -- section 2: independent first/last word
    py0 = 448 - h
    _panel(pdf, 40, py0, 532, h)
    _p4_tag(pdf, py0, h, 2, "Your turn to read.")
    line1, line2, img = P4_S2
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 22)
    pdf.drawString(x0, py0 + 90, line1)
    pdf.drawString(x0, py0 + 52, line2)
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(62, py0 + 16,
                   "Put a dot under the first word. "
                   "Circle the last word.")
    _img_circle(pdf, img, 500, py0 + 74, 26, zoom=True)
    # -- section 3: choose the continuation
    py0 = 266 - h
    _panel(pdf, 40, py0, 532, h)
    _p4_tag(pdf, py0, h, 3, "Choose the words that come next.")
    line1, options, _answer, img = P4_S3
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 22)
    pdf.drawString(x0, py0 + 94, line1)
    for c, opt in enumerate(options):
        bx = 88 + c * 168
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(HexColor("#7FA3B5"))
        pdf.setLineWidth(1.2)
        pdf.roundRect(bx, py0 + 24, 152, 38, 9, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 19)
        pdf.drawCentredString(bx + 76, py0 + 36, opt)
    _img_circle(pdf, img, 500, py0 + 74, 26, zoom=True)


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Follow the Words", title_size=19.5)
    _follow_the_words(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Put It Together (independent practice, no worked examples)
# A short story panel with one scene illustration covering the whole
# passage, then four activity panels in a 2x2 grid, one per earlier
# page's skill: count the sentences (3), circle the first word and
# underline the last word of the story (on a reprint, so the story
# stays clean for reading), add the missing spaces in "Ilikejam.",
# and choose the correctly written sentence.
# ---------------------------------------------------------------------------
P5_STORY = ["The cat is on the mat.", "The sun is up. I like my cat."]
P5_STORY_LINES3 = ["The cat is on the mat.", "The sun is up.",
                   "I like my cat."]


def _p5_tag(pdf, px0, py0, h, num):
    pdf.setFillColor(TEAL)
    pdf.roundRect(px0 + 16, py0 + h - 34, 26, 22, 7, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(px0 + 29, py0 + h - 27, str(num))


def _p5_task(pdf, px0, py0, lines):
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 11.5)
    for i, line in enumerate(lines):
        pdf.drawString(px0 + 16, py0 + 98 - i * 15, line)


def _put_it_together(pdf):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Read the story. Do the activities.")
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 76,
        "Adult: Let your child try each job on their own first. "
        "Help only if they are stuck.")
    # story panel
    py0 = 492
    _panel(pdf, 40, py0, 532, 136)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(56, py0 + 110, "THE STORY")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 20)
    pdf.drawString(56, py0 + 74, P5_STORY[0])
    pdf.drawString(56, py0 + 42, P5_STORY[1])
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "assets", "cvc-words", "ups-story-wide.jpg")
    pdf.saveState()
    clip = pdf.beginPath()
    clip.roundRect(392, py0 + 14, 164, 108, 10)
    pdf.clipPath(clip, stroke=0, fill=0)
    pdf.drawImage(img_path, 392, py0 + 14, 164, 108)
    pdf.restoreState()
    pdf.setStrokeColor(HexColor("#D9E7E7"))
    pdf.setLineWidth(1)
    pdf.roundRect(392, py0 + 14, 164, 108, 10, stroke=1, fill=0)
    # four activity panels, 2x2
    pw, ph = 250, 148
    positions = [(40, 476 - ph), (322, 476 - ph),
                 (40, 312 - ph), (322, 312 - ph)]
    # 1 -- count the sentences
    px0, py0 = positions[0]
    _panel(pdf, px0, py0, pw, ph)
    _p5_tag(pdf, px0, py0, ph, 1)
    _p5_task(pdf, px0, py0, ["How many sentences are",
                             "in the story?"])
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(HexColor("#7FA3B5"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(px0 + 66, py0 + 24, 46, 46, 8, stroke=1, fill=1)
    pdf.setFillColor(HexColor("#37474F"))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(px0 + 122, py0 + 42, "sentences")
    # 2 -- first and last word (mark the reprint)
    px0, py0 = positions[1]
    _panel(pdf, px0, py0, pw, ph)
    _p5_tag(pdf, px0, py0, ph, 2)
    _p5_task(pdf, px0, py0, ["Circle the first word.", "Underline the "
                             "last word."])
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 16)
    for i, line in enumerate(P5_STORY_LINES3):
        pdf.drawString(px0 + 16, py0 + 59 - i * 21, line)
    # 3 -- missing spaces
    px0, py0 = positions[2]
    _panel(pdf, px0, py0, pw, ph)
    _p5_tag(pdf, px0, py0, ph, 3)
    _p5_task(pdf, px0, py0, ["Add the missing spaces."])
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 24)
    pdf.drawCentredString(px0 + pw / 2, py0 + 42, "Ilikejam.")
    # 4 -- choose the correctly written sentence
    px0, py0 = positions[3]
    _panel(pdf, px0, py0, pw, ph)
    _p5_tag(pdf, px0, py0, ph, 4)
    _p5_task(pdf, px0, py0, ["Circle the sentence that is",
                             "written the right way."])
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 16)
    pdf.drawString(px0 + 24, py0 + 60, "the sun is up")
    pdf.drawString(px0 + 24, py0 + 24, "The sun is up.")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Put It Together", title_size=19.5)
    _put_it_together(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Let's Learn About Letters, Words & Sentences", build_p1_page,
     True),  # APPROVED + LOCKED 2026-10-14
    ("Spaces Between Words", build_p2_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Beginning & Ending a Sentence", build_p3_page, True),  # APPROVED
    # + LOCKED 2026-10-14
    ("Follow the Words", build_p4_page, True),  # APPROVED + LOCKED
    # 2026-10-14
    ("Put It Together", build_p5_page, True),  # APPROVED + LOCKED
    # 2026-10-14
]


def main():
    for title, _builder, locked in PAGES:
        assert locked, "Page not locked: %s" % title
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "worksheets", "kindergarten", "reading",
                          "understanding-print-sentences")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(outdir,
                         "understanding-print-sentences-page-%02d.pdf"
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
                          "understanding-print-sentences-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 5
    print("bundle: %s (5 pages)" % bundle)


if __name__ == "__main__":
    main()
