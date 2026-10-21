#!/usr/bin/env python3
"""Our Flag & Our School Rules (Kindergarten Social Studies,
5 pages).

Pack 2 of the approved Kindergarten Social Studies roadmap
("Myself and Others"), covering the Civics expectations: the
U.S. flag as a national symbol, school rules and why they
matter, choosing appropriate actions at school, and individual
responsibility through classroom jobs.

Accuracy rules (from the approved brief):
  * The flag is drawn as exact vector art — 13 stripes and
    50 stars in the official 9-row arrangement, official
    proportions (canton = 7 stripes high, 2/5 of the fly).
    Children are never asked to count all 50 stars.
  * Pages never claim all classrooms have identical rules or
    jobs: adult lines direct talk about the rules and jobs in
    the child's OWN classroom.
  * Page 5's personal responsibilities (backpack, lunchbox,
    chair) are personal-care actions, distinct from the
    self-care routines packs (washing, dressing, toileting).

  P1 Our Flag — the flag as a symbol of the United States;
     picture observation: count the 13 stripes, circle one
     star in a magnified star field, color the 3 flag colors.
  P2 Draw Our Flag — guided coloring/completion of an outlined
     accurate flag (50 star outlines printed) from a full-color
     reference flag.
  P3 Rules Help Us — match three school rules (walk inside,
     listen, take turns) to why each helps (no one gets hurt,
     we can hear and learn, everyone gets a turn).
  P4 What Should We Do? — circle the better action in the
     hallway, the cafeteria, and on the playground.
  P5 My Jobs at School — four classroom jobs to circle, draw
     yourself doing the job, plus three everyday personal
     responsibilities with check boxes.

No separate parent guide (guide-less draft-review workflow).
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
                      "assets", "flag-rules")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "kindergarten", "social-studies",
                       "flag-rules")
PACK_TITLE = "Our Flag & Our School Rules"
STEM = "flag-rules"

RULE = HexColor("#9DB8C4")
PANEL_FILL = HexColor("#F2F8F8")
WHITE = HexColor("#FFFFFF")
FLAG_RED = HexColor("#B22234")
FLAG_BLUE = HexColor("#3C3B6E")
CUE_RED = HexColor("#EFC3C9")


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


def _star(pdf, cx, cy, r, fill=None, stroke=None):
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
    if fill is not None:
        pdf.setFillColor(fill)
    if stroke is not None:
        pdf.setStrokeColor(stroke)
        pdf.setLineWidth(0.8)
    pdf.drawPath(p, stroke=1 if stroke is not None else 0,
                 fill=1 if fill is not None else 0)


def _star_field(pdf, x, y_top, cw, ch, flag_h, outlines=False):
    """The official arrangement: 9 rows alternating 6 and 5
    stars (50 total), on the standard 12-by-10 grid."""
    row_step = ch / 10.0
    col_step = cw / 12.0
    r = 0.0308 * flag_h
    for row in range(9):
        cy = y_top - row_step * (row + 1)
        count = 6 if row % 2 == 0 else 5
        for j in range(count):
            cx = x + col_step * (2 * j + 1 if count == 6 else 2 * j + 2)
            if outlines:
                _star(pdf, cx, cy, r, fill=WHITE, stroke=RULE)
            else:
                _star(pdf, cx, cy, r, fill=WHITE)


def draw_flag(pdf, x, y, w, mode="full"):
    """An accurate U.S. flag: 13 stripes (red at top and
    bottom), blue canton 7 stripes high and 2/5 of the fly,
    50 stars. (x, y) is the flag's bottom-left corner."""
    h = w / 1.9
    sh = h / 13.0
    cw = w * 0.4
    ch = sh * 7
    top = y + h
    for i in range(13):
        from_top = 12 - i
        red = from_top % 2 == 0
        pdf.setFillColor(FLAG_RED if (red and mode == "full") else WHITE)
        pdf.rect(x, y + i * sh, w, sh + 0.4, stroke=0, fill=1)
    if mode == "outline":
        pdf.setStrokeColor(RULE)
        pdf.setLineWidth(0.9)
        for i in range(1, 13):
            pdf.line(x, y + i * sh, x + w, y + i * sh)
    if mode == "full":
        pdf.setFillColor(FLAG_BLUE)
        pdf.rect(x, top - ch, cw, ch, stroke=0, fill=1)
        _star_field(pdf, x, top, cw, ch, h)
    else:
        pdf.setFillColor(WHITE)
        pdf.rect(x, top - ch, cw, ch, stroke=0, fill=1)
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.2)
        pdf.rect(x, top - ch, cw, ch, stroke=1, fill=0)
        _star_field(pdf, x, top, cw, ch, h, outlines=True)
        pdf.setFillColor(CUE_RED)
        for s in range(7):
            cy = top - (2 * s + 0.5) * sh
            cx = x + cw + 9 if s < 4 else x + 9
            pdf.circle(cx, cy, 3.4, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.6)
    pdf.rect(x, y, w, h, stroke=1, fill=0)
    return h


def _obs_card(pdf, x, title):
    _panel(pdf, x, 150, 160, 196)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(x + 80, 322, title)


def page1(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Our Flag")
    _instruction(pdf, "Our flag is a symbol of our country.")
    draw_flag(pdf, 136, 412, 340, mode="full")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 388,
                          "It is the flag of the United States of America.")
    # Card A: count the stripes (stripes-only stack, 13 bands)
    _obs_card(pdf, 51, "STRIPES")
    sx, sy, sw = 83, 228, 96
    band = 72 / 13.0
    for i in range(13):
        from_top = 12 - i
        pdf.setFillColor(FLAG_RED if from_top % 2 == 0 else WHITE)
        pdf.rect(sx, sy + i * band, sw, band + 0.3, stroke=0, fill=1)
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.rect(sx, sy, sw, 72, stroke=1, fill=0)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(131, 212, "Count the stripes.")
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.6)
    pdf.rect(105, 156, 52, 46, stroke=1, fill=0)
    # Card B: circle one star (magnified star field)
    _obs_card(pdf, 226, "STARS")
    pdf.setFillColor(FLAG_BLUE)
    p = pdf.beginPath()
    p.roundRect(258, 218, 96, 72, 8)
    pdf.drawPath(p, stroke=0, fill=1)
    for r_i in range(3):
        for c_i in range(3):
            _star(pdf, 274 + c_i * 32, 234 + r_i * 21, 9, fill=WHITE)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(306, 196, "Circle one star.")
    pdf.drawCentredString(306, 172,
                          "Our flag has 50 stars.")
    # Card C: color the three flag colors
    _obs_card(pdf, 401, "COLORS")
    for i, (word, col) in enumerate((("RED", FLAG_RED),
                                     ("WHITE", WHITE),
                                     ("BLUE", FLAG_BLUE))):
        cx = 434 + i * 43
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.3)
        pdf.circle(cx, 250, 16, stroke=1, fill=0)
        pdf.setFillColor(col)
        pdf.circle(cx, 282, 4.5, stroke=0, fill=1)
        if word == "WHITE":
            pdf.setStrokeColor(NAVY)
            pdf.setLineWidth(0.8)
            pdf.circle(cx, 282, 4.5, stroke=1, fill=0)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 10.5)
        pdf.drawCentredString(cx, 224, word)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.drawCentredString(481, 196, "Color each circle")
    pdf.drawCentredString(481, 172, "the right color.")
    _adult(pdf, [
        "Adult: Our flag stands for the United States of America.",
        "Point to the stripes, the stars, and each color as you",
        "talk. The flag has 13 stripes and 50 stars in all.",
    ], top=110)
    draw_footer(pdf)
    pdf.save()


def page2(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Draw Our Flag")
    _instruction(pdf, "Look at our flag. Now color this flag.")
    draw_flag(pdf, 221, 478, 170, mode="full")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 462, "OUR FLAG")
    draw_flag(pdf, 76, 186, 460, mode="outline")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(PAGE_WIDTH / 2, 152,
                          "Color the dotted stripes red. Color the "
                          "corner blue.")
    _adult(pdf, [
        "Adult: There are 13 stripes. The top and bottom stripes",
        "are red; a light dot marks each red stripe. Color the",
        "corner blue and leave the 50 little stars white.",
    ], top=110)
    draw_footer(pdf)
    pdf.save()


def _match_panel(pdf, x, y, img, label, label_size=13.5):
    _panel(pdf, x, y, 190, 120)
    _img_fill(pdf, img, x + 8, y + 30, 174, 82)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", label_size)
    pdf.drawCentredString(x + 95, y + 11, label)
    pdf.setFillColor(NAVY)
    pdf.circle(x + (196 if x < 300 else -6), y + 60, 4.5,
               stroke=0, fill=1)


def page3(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "Rules Help Us")
    _instruction(pdf, "Draw a line from each rule to why it helps.")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(146, 592, "OUR RULES")
    pdf.drawCentredString(466, 592, "WHY IT HELPS")
    rows = [466, 326, 186]
    rules = [(A("fr-rule-walk"), "Walk inside."),
             (A("fr-rule-listen"), "Listen."),
             (A("fr-rule-turns"), "Take turns.")]
    reasons = [(A("fr-reason-turn"), "Everyone gets a turn.", 12),
               (A("fr-reason-safe"), "No one gets hurt.", 13.5),
               (A("fr-reason-learn"), "We can hear and learn.", 12)]
    for (img, label), y in zip(rules, rows):
        _match_panel(pdf, 51, y, img, label)
    for (img, label, size), y in zip(reasons, rows):
        _match_panel(pdf, 371, y, img, label, label_size=size)
    _adult(pdf, [
        "Adult: Read the rules and the reasons aloud. Rules help",
        "keep us safe, help us learn, and give everyone a turn.",
        "Talk about the rules in your child's own classroom.",
    ], top=110)
    draw_footer(pdf)
    pdf.save()


def _scenario(pdf, top, chip, left_img, right_img):
    pdf.setFillColor(TEAL)
    p = pdf.beginPath()
    p.roundRect(51, top - 20, 150, 20, 7)
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 11.5)
    pdf.drawCentredString(126, top - 14, chip)
    for x, img in ((51, left_img), (314, right_img)):
        _panel(pdf, x, top - 140, 247, 112)
        _img_fill(pdf, img, x + 8, top - 132, 231, 96)


def page4(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "What Should We Do?")
    _instruction(pdf, "Circle the better choice.")
    _scenario(pdf, 600, "IN THE HALLWAY",
              A("fr-hall-walk"), A("fr-hall-run"))
    _scenario(pdf, 446, "IN THE CAFETERIA",
              A("fr-cafe-leave"), A("fr-cafe-return"))
    _scenario(pdf, 292, "ON THE PLAYGROUND",
              A("fr-play-help"), A("fr-play-pass"))
    _adult(pdf, [
        "Adult: For each place, talk about what each child is",
        "doing. Which choice is safer or kinder? Circle it.",
        "Answers are on the website page.",
    ], top=110)
    draw_footer(pdf)
    pdf.save()


def page5(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, PACK_TITLE, "My Jobs at School")
    _instruction(pdf, "Jobs help our classroom. Circle a job for you.")
    jobs = [(A("fr-job-line"), "LINE LEADER"),
            (A("fr-job-papers"), "PAPER HELPER"),
            (A("fr-job-plant"), "PLANT HELPER"),
            (A("fr-job-tidy"), "BOOK HELPER")]
    for i, (img, label) in enumerate(jobs):
        x = 51 + i * 126
        _panel(pdf, x, 428, 118, 142)
        _img_fill(pdf, img, x + 6, 470, 106, 94)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 11.5)
        pdf.drawCentredString(x + 59, 444, label)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 410,
                          "Draw yourself doing the job you circled.")
    _panel(pdf, 51, 238, 510, 158)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(51, 216, "My own jobs every day:")
    resp = [(A("fr-resp-backpack"), "Hang up my", "backpack"),
            (A("fr-resp-lunchbox"), "Put my", "lunchbox away"),
            (A("fr-resp-chair"), "Push in", "my chair")]
    for i, (img, l1, l2) in enumerate(resp):
        x = 51 + i * 174
        _panel(pdf, x, 122, 162, 84)
        _img_fill(pdf, img, x + 6, 130, 62, 68, r=8)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 11.5)
        pdf.drawString(x + 76, 172, l1)
        pdf.drawString(x + 76, 158, l2)
        pdf.setStrokeColor(NAVY)
        pdf.setLineWidth(1.3)
        pdf.rect(x + 132, 130, 15, 15, stroke=1, fill=0)
    _adult(pdf, [
        "Adult: Jobs are different in every classroom. Talk",
        "about the jobs in your child's classroom, circle one,",
        "then draw it. The bottom jobs are every child's own.",
    ], top=100)
    draw_footer(pdf)
    pdf.save()


BUILDERS = [page1, page2, page3, page4, page5]


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
        fn(f"/tmp/fr-p{i}.pdf")
    print("previews in /tmp/fr-pN.pdf")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        preview()
    else:
        build_pack()
