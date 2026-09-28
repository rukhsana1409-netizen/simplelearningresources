"""Build Safe or Not Safe? (Independence & Safety) — prototype.

Page 1 (Safe or Not Safe?): four large everyday preschool
situations where the safe/not-safe behavior is immediately obvious
from the picture. Each panel shows one large full-scene
illustration plus two big choice pills — Safe. / Not safe.
The child circles the right one.

Page 2 (I Can Stay Safe.): four functional safety phrases, each
modeled by a large full-scene illustration with the exact words
in a speech bubble. The child says the words.

Page 4 (Match the Safety Rule.): a left-to-right matching
activity — four large full-scene illustrations on the left, four
shuffled safety rules with small vector cue icons on the right.
The child draws a line to match each picture to its rule.

An adult reads the words aloud; the activity does not depend on
independent reading.
"""

from __future__ import annotations

import io
import os

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792
TITLE = "Safe or Not Safe?"

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
GOLD = HexColor("#F4B63E")
INK = HexColor("#202A33")
BORDER = HexColor("#B9D7D2")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "safe-or-not-safe")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "communication",
                   "safe-or-not-safe", "safe-or-not-safe-prototype.pdf")


def draw_logo(pdf, x, y):
    """Vector-only Learning Made Simple mark and wordmark (established
    brand header, as in Learn My Letters)."""
    pdf.setFillColor(TEAL)
    pdf.circle(x + 18, y + 26, 7, fill=1, stroke=0)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(x + 18, y + 18, x + 18, y + 4)
    pdf.line(x + 18, y + 14, x + 6, y + 5)
    pdf.line(x + 18, y + 14, x + 30, y + 5)
    pdf.setLineWidth(1.3)
    pdf.line(x + 2, y + 4, x + 18, y)
    pdf.line(x + 18, y, x + 34, y + 4)
    pdf.setFillColor(GOLD)
    pdf.circle(x + 18, y + 39, 3.5, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(x + 43, y + 24, "LEARNING")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(x + 43, y + 10, "MADE SIMPLE")


def draw_header(pdf, title, subtitle):
    """Established brand header (Learn My Letters style): teal top strip,
    vector logo + wordmark, divider, two-line teal title, teal rule."""
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, fill=1, stroke=0)
    draw_logo(pdf, MARGIN, PAGE_HEIGHT - 86)
    divider_x = 210
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1)
    pdf.line(divider_x, PAGE_HEIGHT - 46, divider_x, PAGE_HEIGHT - 106)
    title_x = divider_x + 19
    if ": " in title:
        prefix, focus = title.split(": ", 1)
    else:
        prefix, focus = "", title
    if prefix:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(title_x, PAGE_HEIGHT - 67, prefix + ":")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(title_x, PAGE_HEIGHT - 98, focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11.5)
    pdf.drawString(title_x, PAGE_HEIGHT - 116, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    pdf.line(MARGIN, PAGE_HEIGHT - 131, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 131)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(MARGIN, PAGE_HEIGHT - 160, "Name:")
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.9)
    pdf.line(MARGIN + 37, PAGE_HEIGHT - 163, 315, PAGE_HEIGHT - 163)
    pdf.setFillColor(INK)
    pdf.drawString(430, PAGE_HEIGHT - 160, "Date:")
    pdf.setStrokeColor(BORDER)
    pdf.line(463, PAGE_HEIGHT - 163, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 163)


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF4F3"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#0E7C7B"))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(56, 19, "Learning Made Simple")
    pdf.setStrokeColor(HexColor("#9FD3D1"))
    pdf.setLineWidth(1.5)
    pdf.line(200, 10, 200, 34)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(320, 19, "Made with love for little learners.")
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(556, 19, "\u00a9 2026 Learning Made Simple")


# New-page images are embedded downscaled to 1100px wide: still ~400
# DPI at the largest print size on Page 4, and it keeps the PDF small
# enough for the GitHub blob API. Full-resolution masters stay in
# assets/. Pages 1-2 keep full-resolution embeds so their approved
# renders stay byte-identical.
MAX_EMBED_WIDTH = 1100


def draw_picture(pdf, stem, cx, cy, size, max_w=None):
    path = os.path.join(ASSETS, stem + ".png")
    img = Image.open(path)
    if max_w and img.width > max_w:
        img = img.resize(
            (max_w, int(img.height * max_w / img.width)), Image.LANCZOS)
    if max_w:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        src = ImageReader(buf)
    else:
        src = path
    pdf.drawImage(src, cx - size / 2, cy - size / 2,
                  size, size, preserveAspectRatio=True, mask="auto")


def draw_choice_pill(pdf, text, cx, cy, w=112, h=42, safe=True):
    """Big rounded choice pill under each scene, green for Safe and
    red for Not safe (the text carries the meaning; color decorates)."""
    bg = HexColor("#E3F3E4") if safe else HexColor("#FBE3E6")
    fg = HexColor("#1E7A34") if safe else HexColor("#C02434")
    pdf.setFillColor(bg)
    pdf.setStrokeColor(fg)
    pdf.setLineWidth(2)
    pdf.roundRect(cx - w / 2, cy - h / 2, w, h, h / 2, fill=1, stroke=1)
    pdf.setFillColor(fg)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(cx, cy - 4.5, text)


# Page 1 (Safe or Not Safe?): 2x2 grid of large scenes. The
# safe/not-safe behavior is immediately obvious from each picture.
# The child circles one of the two choice pills under each scene.
# Order: hand-hold (Safe), bike no helmet (Not safe),
# car seat (Safe), chair reach (Not safe).


def draw_page1(pdf):
    draw_header(pdf, TITLE, "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 588,
                          "Look at the picture. Circle: Safe or not safe.")
    pw, ph = 262, 250
    xs = [36 + pw / 2, 36 + pw + 16 + pw / 2]
    ys = [446, 184]
    scenes = ["sonss-hand-hold", "sonss-bike-no-helmet",
              "sonss-car-seat", "sonss-chair-reach"]
    for (cx, cy), scene in zip([(x, y) for y in ys for x in xs], scenes):
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(cx - pw / 2, cy - ph / 2, pw, ph, 16, fill=1, stroke=1)
        draw_picture(pdf, scene, cx, cy + 22, 186)
        draw_choice_pill(pdf, "Safe.", cx - 61, cy - 97, safe=True)
        draw_choice_pill(pdf, "Not safe.", cx + 61, cy - 97, safe=False)
    draw_footer(pdf)
    pdf.showPage()


def draw_speech_bubble(pdf, text, cx, cy, w=232, h=50, tail=22):
    """White speech bubble with a tail, carrying the exact phrase."""
    x0, y0 = cx - w / 2, cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    # tail (drawn first so the bubble covers its base)
    tx, ty = cx, y0 + h
    p = pdf.beginPath()
    p.moveTo(tx - 11, ty - 1)
    p.lineTo(tx, ty + tail)
    p.lineTo(tx + 11, ty - 1)
    p.close()
    pdf.drawPath(p, fill=1, stroke=0)
    # bubble
    pdf.roundRect(x0, y0, w, h, 14, fill=1, stroke=1)
    pdf.line(tx - 11, ty - 1, tx, ty + tail)
    pdf.line(tx + 11, ty - 1, tx, ty + tail)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(cx, cy - 4.5, text)


# Page 2 (I Can Stay Safe.): four functional safety phrases, each
# modeled by a large full-scene illustration with the exact words
# in a speech bubble. The child says the words.
PAGE2_TITLE = "I Can Stay Safe."
PAGE2_ROWS = [
    ("sonss-p2-hand", "Hold my hand, please."),
    ("sonss-p2-walking-feet", "I use walking feet."),
    ("sonss-p2-sit-seat", "I sit in my seat."),
    ("sonss-p2-curb", "I stop at the curb."),
]


def draw_page2(pdf):
    draw_header(pdf, PAGE2_TITLE, "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 588, "Say the words.")
    pw, ph = 262, 250
    xs = [36 + pw / 2, 36 + pw + 16 + pw / 2]
    ys = [446, 184]
    for (cx, cy), (scene, phrase) in zip(
            [(x, y) for y in ys for x in xs], PAGE2_ROWS):
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(cx - pw / 2, cy - ph / 2, pw, ph, 16, fill=1, stroke=1)
        draw_picture(pdf, scene, cx, cy + 34, 258)
        draw_speech_bubble(pdf, phrase, cx, cy - 90)
    draw_footer(pdf)
    pdf.showPage()


def draw_cue(pdf, kind, cx, cy, s=17):
    """Small vector cue icon beside a rule card."""
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.5)
    if kind == "helmet":
        pdf.setFillColor(HexColor("#D64545"))
        p = pdf.beginPath()
        p.moveTo(cx - s, cy)
        p.arc(cx - s, cy - s, cx + s, cy + s, startAng=0, extent=180)
        p.close()
        pdf.drawPath(p, fill=1, stroke=1)
        pdf.line(cx - s * 0.4, cy, cx - s * 0.4, cy - s * 0.9)
        pdf.line(cx + s * 0.4, cy, cx + s * 0.4, cy - s * 0.9)
    elif kind == "buckle":
        pdf.setFillColor(HexColor("#8A8F98"))
        pdf.roundRect(cx - s * 0.9, cy - s * 0.7, s * 1.15, s * 1.4, 4,
                      fill=1, stroke=1)
        pdf.setFillColor(HexColor("#D64545"))
        pdf.roundRect(cx - s * 0.62, cy - s * 0.35, s * 0.6, s * 0.7, 3,
                      fill=1, stroke=1)
        pdf.setFillColor(HexColor("#C9CED6"))
        pdf.roundRect(cx + s * 0.25, cy - s * 0.35, s * 0.85, s * 0.7, 3,
                      fill=1, stroke=1)
    elif kind == "grownup":
        pdf.setFillColor(TEAL)
        pdf.circle(cx - s * 0.55, cy + s * 0.4, s * 0.42, fill=1, stroke=1)
        pdf.roundRect(cx - s * 0.95, cy - s * 1.0, s * 0.8, s * 1.05, 6,
                      fill=1, stroke=1)
        pdf.setFillColor(HexColor("#F2A0C0"))
        pdf.circle(cx + s * 0.55, cy + s * 0.12, s * 0.32, fill=1, stroke=1)
        pdf.roundRect(cx + s * 0.24, cy - s * 1.0, s * 0.62, s * 0.82, 6,
                      fill=1, stroke=1)
        pdf.line(cx - s * 0.15, cy - s * 0.35, cx + s * 0.24, cy - s * 0.35)
    elif kind == "bottle":
        pdf.setFillColor(HexColor("#E8A33D"))
        pdf.roundRect(cx - s * 0.55, cy - s * 0.95, s * 1.1, s * 1.55, 5,
                      fill=1, stroke=1)
        pdf.setFillColor(HexColor("#8A8F98"))
        pdf.roundRect(cx - s * 0.35, cy + s * 0.6, s * 0.7, s * 0.45, 3,
                      fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(cx, cy - s * 0.42, "?")


# Page 4 (Match the Safety Rule.): four large full-scene
# illustrations on the left; the four shuffled safety rules with a
# small visual cue on the right. The child draws a line to match
# each picture to its rule.
PAGE4_TITLE = "Match: the Safety Rule."
PAGE4_ROWS = [
    ("sonss-p4-helmet", "helmet", "I wear my helmet."),
    ("sonss-p4-buckle", "buckle", "I buckle up."),
    ("sonss-p4-grownup", "grownup", "I stay with my grown-up."),
    ("sonss-p4-medicine", "bottle", "I ask before I touch."),
]
# shuffled order of the rules on the right-hand side
PAGE4_RULE_ORDER = [3, 0, 2, 1]


def draw_page4(pdf):
    draw_header(pdf, PAGE4_TITLE, "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 588,
                          "Draw a line to match each picture to the safety rule.")
    row_h, gap = 120, 8
    top = 556
    pic_cx, rule_cx = 36 + 117, 576 - 117
    for i, (asset, cue, rule) in enumerate(PAGE4_ROWS):
        cy = top - i * (row_h + gap) - row_h / 2
        # picture card (left)
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(36, cy - row_h / 2, 234, row_h, 12, fill=1, stroke=1)
        draw_picture(pdf, asset, pic_cx, cy, 196, max_w=MAX_EMBED_WIDTH)
        # anchor dot where the matching line starts
        pdf.setFillColor(TEAL)
        pdf.circle(270, cy, 5, fill=1, stroke=0)
        # rule card (right), shuffled — same height and vertical center
        # as the picture card, so each pair forms one clean row
        r_asset, r_cue, r_rule = PAGE4_ROWS[PAGE4_RULE_ORDER[i]]
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(342, cy - row_h / 2, 234, row_h, 12, fill=1, stroke=1)
        pdf.setFillColor(TEAL)
        pdf.circle(342, cy, 5, fill=1, stroke=0)
        draw_cue(pdf, r_cue, rule_cx - 82, cy)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawCentredString(rule_cx + 16, cy - 4.5, r_rule)
    draw_footer(pdf)
    pdf.showPage()


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pdf = canvas.Canvas(OUT, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_page1(pdf)
    draw_page2(pdf)
    draw_page4(pdf)
    pdf.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
