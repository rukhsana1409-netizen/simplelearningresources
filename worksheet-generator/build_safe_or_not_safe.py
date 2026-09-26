"""Build Safe or Not Safe? (Independence & Safety) — prototype.

Page 1 (Safe or Not Safe?): four large everyday preschool
situations where the safe/not-safe behavior is immediately obvious
from the picture. Each panel shows one large full-scene
illustration plus two big choice pills — Safe. / Not safe.
The child circles the right one.

Page 2 (I Can Stay Safe.): four functional safety phrases, each
modeled by a large full-scene illustration with the exact words
in a speech bubble. The child says the words.

An adult reads the words aloud; the activity does not depend on
independent reading.
"""

from __future__ import annotations

import os

from reportlab.lib.colors import HexColor, white
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


def draw_picture(pdf, stem, cx, cy, size):
    path = os.path.join(ASSETS, stem + ".png")
    pdf.drawImage(path, cx - size / 2, cy - size / 2, size, size,
                  preserveAspectRatio=True, mask="auto")


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


def draw_speech_bubble(pdf, text, cx, cy, w=232, h=52):
    """White speech bubble with a tail, carrying the exact phrase."""
    x0, y0 = cx - w / 2, cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    # tail (drawn first so the bubble covers its base)
    tx, ty = cx, y0 + h
    p = pdf.beginPath()
    p.moveTo(tx - 11, ty - 1)
    p.lineTo(tx, ty + 17)
    p.lineTo(tx + 11, ty - 1)
    p.close()
    pdf.drawPath(p, fill=1, stroke=0)
    # bubble
    pdf.roundRect(x0, y0, w, h, 14, fill=1, stroke=1)
    pdf.line(tx - 11, ty - 1, tx, ty + 17)
    pdf.line(tx + 11, ty - 1, tx, ty + 17)
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
        draw_picture(pdf, scene, cx, cy + 28, 170)
        draw_speech_bubble(pdf, phrase, cx, cy - 88)
    draw_footer(pdf)
    pdf.showPage()


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    pdf = canvas.Canvas(OUT, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_page1(pdf)
    draw_page2(pdf)
    pdf.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
