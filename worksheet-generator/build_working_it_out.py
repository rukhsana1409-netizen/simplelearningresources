#!/usr/bin/env python3
"""Working It Out (Kindergarten Social Studies, 4 pages).

Pack 3 of the approved Kindergarten Social Studies roadmap
("Myself and Others"), covering the Civics expectations on
resolving conflicts: listening to different viewpoints,
making fair choices, and finding appropriate solutions to
everyday classroom disagreements.

Framing rules (from the approved brief):
  * Activities require thinking, not just spotting obvious
    good/bad behavior: the same problem feels different to
    each friend (P1), more than one strategy can work and
    the child picks the best fit (P2), more than one speech
    bubble can help (P3), and the story ending is the
    child's own (P4).
  * Feelings identification is APPLIED here, not retaught —
    Feelings & Me (preschool) owns feelings vocabulary.
  * No duplication of Pack 2: no school rules, classroom
    jobs, or responsibilities.
  * Speech phrases are short whole chunks a child can say
    as one piece (gestalt-friendly).

  P1 Two Friends, One Problem — both friends want the one
     red crayon; circle how EACH friend feels (mad / sad).
  P2 Stop, Think, Choose — one swing, two friends; the
     stop-think-choose rhythm, then circle a kind strategy
     (use words, take turns, share, say sorry, ask a teacher).
  P3 What Could They Say? — a tower fell; circle the speech
     bubbles whose words could help (two of four).
  P4 Finish the Story — problem, stop and talk, then the
     child draws and dictates their own kind, fair ending.

No separate parent guide (guide-less draft-review workflow).
Answers and guidance live in the website resource-page text.
"""
import math
import os
import sys

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_phonics_az import (  # noqa: E402
    INK, NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL, draw_footer, draw_header,
)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "working-it-out")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "social-studies",
                       "working-it-out")
PACK_TITLE = "Working It Out"
STEM = "working-it-out"

RULE = HexColor("#9DB8C4")
PANEL_FILL = HexColor("#F2F8F8")
WHITE = HexColor("#FFFFFF")
GOLD = HexColor("#F4B63E")
ORANGE = HexColor("#E8862E")
STOP_RED = HexColor("#C8402A")


def A(name):
    return os.path.join(ASSETS, name + ".jpg")


def _adult(pdf, lines, top=84, step=13):
    pdf.setFillColor(INK)
    for i, line in enumerate(lines):
        pdf.setFont("Helvetica-Bold", 11.5 if i == 0 else 11)
        pdf.drawCentredString(PAGE_WIDTH / 2, top - i * step, line)


def _img_fill(pdf, path, x, y, w, h, focus_x=0.5, focus_y=0.5, r=10):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx = x + (w - dw) * focus_x
    dy = y + (h - dh) * focus_y
    pdf.saveState()
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.drawImage(ImageReader(path), dx, dy, dw, dh,
                  preserveAspectRatio=False, mask="auto")
    pdf.restoreState()
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.4)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.drawPath(p, stroke=1, fill=0)


def _panel(pdf, x, y, w, h, r=12):
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.3)
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.drawPath(p, stroke=1, fill=1)


def _instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 19)
    pdf.drawCentredString(PAGE_WIDTH / 2, 616, text)


def _star(pdf, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.381966
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(fill)
    pdf.drawPath(p, stroke=0, fill=1)


def _face_choice(pdf, x, y, img, word):
    _img_fill(pdf, img, x, y + 18, 66, 58, r=8)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawCentredString(x + 33, y + 4, word)


def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Two Friends, One Problem")
    _instruction(pdf, "Two friends. One problem.")
    _img_fill(pdf, A("wo-problem-crayon"), 51, 356, 510, 216)
    _star(pdf, 118, 540, 13, TEAL)
    _star(pdf, 494, 540, 13, ORANGE)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 334,
                          "Both friends want the red crayon. "
                          "There is only one.")
    for x, star_col, order in (
            (51, TEAL, ("wo-face-sad", "wo-face-mad", "wo-face-happy")),
            (327, ORANGE, ("wo-face-mad", "wo-face-happy", "wo-face-sad"))):
        _panel(pdf, x, 176, 234, 140)
        _star(pdf, x + 22, 292, 10, star_col)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawString(x + 40, 288, "How does she feel?")
        words = {"wo-face-happy": "HAPPY", "wo-face-sad": "SAD",
                 "wo-face-mad": "MAD"}
        for i, stem in enumerate(order):
            _face_choice(pdf, x + 12 + i * 72, 186, A(stem), words[stem])
    _adult(pdf, [
        "Adult: The SAME problem can feel different to each",
        "friend. Talk about why each friend feels that way.",
    ], top=150)
    draw_footer(pdf)
    pdf.save()


def _octagon(pdf, cx, cy, r):
    pts = []
    for i in range(8):
        ang = math.pi / 8 + i * math.pi / 4
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(STOP_RED)
    pdf.drawPath(p, stroke=0, fill=1)


def _step_chip(pdf, x, kind, word):
    _panel(pdf, x, 352, 160, 80)
    if kind == "stop":
        _octagon(pdf, x + 80, 404, 17)
    elif kind == "think":
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.6)
        pdf.circle(x + 68, 400, 13, stroke=1, fill=0)
        pdf.circle(x + 88, 408, 10, stroke=1, fill=0)
        pdf.circle(x + 58, 390, 6, stroke=1, fill=0)
    else:
        _star(pdf, x + 80, 402, 16, GOLD)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(x + 80, 364, word)


def page2(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Stop, Think, Choose")
    _instruction(pdf, "When there is a problem: Stop. Think. Choose.")
    _img_fill(pdf, A("wo-problem-swing"), 51, 452, 300, 128)
    _panel(pdf, 363, 452, 198, 128)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    for i, line in enumerate(("Two friends.", "One swing.",
                              "What can", "they do?")):
        pdf.drawCentredString(462, 548 - i * 21, line)
    _step_chip(pdf, 51, "stop", "STOP")
    _step_chip(pdf, 226, "think", "THINK")
    _step_chip(pdf, 401, "choose", "CHOOSE")
    for ax in (199, 374):
        pdf.setFillColor(NAVY)
        p = pdf.beginPath()
        p.moveTo(ax, 384)
        p.lineTo(ax + 14, 392)
        p.lineTo(ax, 400)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 330,
                          "Circle a kind way to fix the problem.")
    strats = [(A("wo-strat-words"), "USE", "WORDS"),
              (A("wo-strat-turns"), "TAKE", "TURNS"),
              (A("wo-strat-share"), "SHARE", ""),
              (A("wo-strat-sorry"), "SAY", "SORRY"),
              (A("wo-strat-teacher"), "ASK A", "TEACHER")]
    for i, (img, l1, l2) in enumerate(strats):
        x = 51 + i * 102
        _panel(pdf, x, 176, 96, 130)
        _img_fill(pdf, img, x + 5, 228, 86, 72, r=8)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawCentredString(x + 48, 210, l1)
        if l2:
            pdf.drawCentredString(x + 48, 196, l2)
    _adult(pdf, [
        "Adult: More than one choice can work. For one swing,",
        "taking turns fits best. Let your child explain why.",
    ], top=150)
    draw_footer(pdf)
    pdf.save()


def _bubble(pdf, x, y, lines):
    pdf.setFillColor(WHITE)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.5)
    p = pdf.beginPath()
    p.roundRect(x, y, 247, 104, 16)
    pdf.drawPath(p, stroke=1, fill=1)
    p = pdf.beginPath()
    p.moveTo(x + 30, y + 2)
    p.lineTo(x + 44, y - 12)
    p.lineTo(x + 58, y + 2)
    p.close()
    pdf.setFillColor(WHITE)
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.line(x + 30, y + 2, x + 44, y - 12)
    pdf.line(x + 44, y - 12, x + 58, y + 2)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 16)
    if len(lines) == 1:
        pdf.drawCentredString(x + 123.5, y + 46, lines[0])
    else:
        pdf.drawCentredString(x + 123.5, y + 58, lines[0])
        pdf.drawCentredString(x + 123.5, y + 36, lines[1])


def page3(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Could They Say?")
    _instruction(pdf, "Circle the words that could help.")
    _img_fill(pdf, A("wo-tower-fell"), 51, 420, 510, 168)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 398,
                          "The tower fell down. "
                          "What could the friend say?")
    _bubble(pdf, 51, 268, ["I'm sorry.", "I didn't mean to."])
    _bubble(pdf, 314, 268, ["It's your fault!"])
    _bubble(pdf, 51, 148, ["Let's build it", "again together."])
    _bubble(pdf, 314, 148, ["You can't", "play here."])
    _adult(pdf, [
        "Adult: Read each bubble aloud. Which words would help",
        "the friends feel better? More than one bubble can help.",
    ], top=110)
    draw_footer(pdf)
    pdf.save()


def _story_panel(pdf, x, num, img, caption_lines):
    _panel(pdf, x, 380, 162, 200)
    if img is not None:
        _img_fill(pdf, img, x + 6, 442, 150, 128)
    pdf.setFillColor(TEAL)
    pdf.circle(x + 18, 556, 12, stroke=0, fill=1)
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(x + 18, 551, str(num))
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11.5)
    for i, line in enumerate(caption_lines):
        pdf.drawCentredString(x + 81, 420 - i * 15, line)


def page4(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Finish the Story")
    _instruction(pdf, "Finish the story.")
    _story_panel(pdf, 51, 1, A("wo-story-ball"),
                 ["Both friends", "want the ball."])
    _story_panel(pdf, 225, 2, A("wo-story-talk"),
                 ["They stop", "and talk."])
    _story_panel(pdf, 399, 3, None,
                 ["Draw: How does", "the story end?"])
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(51, 348, "Tell about your ending:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.1)
    pdf.line(51, 306, 561, 306)
    pdf.line(51, 258, 561, 258)
    _adult(pdf, [
        "Adult: Your child draws the ending, then tells it.",
        "Write their words on the lines, exactly as they say",
        "them. Many endings work if they are kind and fair.",
    ], top=110)
    draw_footer(pdf)
    pdf.save()


BUILDERS = [page1, page2, page3, page4]


def build_pack():
    os.makedirs(OUT_DIR, exist_ok=True)
    singles = []
    for i, fn in enumerate(BUILDERS, 1):
        p = os.path.join(OUT_DIR, f"{STEM}-page-{i:02d}.pdf")
        fn(p)
        singles.append(p)
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for p in singles:
        for pg in PdfReader(p).pages:
            w.add_page(pg)
    out = os.path.join(OUT_DIR, f"{STEM}-review.pdf")
    with open(out, "wb") as fh:
        w.write(fh)
    print("built", out)


def preview():
    for i, fn in enumerate(BUILDERS, 1):
        fn(f"/tmp/wo-p{i}.pdf")
    print("previews in /tmp/wo-pN.pdf")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        preview()
    else:
        build_pack()
