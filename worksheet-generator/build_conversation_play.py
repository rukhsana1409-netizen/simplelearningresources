"""Build Conversation & Play (Preschool Communication & Life Skills) — prototype.

Page 1 (Can I Play?): four large, colorful play scenes. In each
scene two children are already playing and a third child wants to
join. Each scene models a DIFFERENT short, natural joining phrase
(GLP-friendly whole-language chunks: "Can I play?",
"I want to play too!", "Let's play!", "Come play with me!").
The child looks at the picture and says the words.

An adult reads the words aloud; the activity does not depend on
independent reading.
"""

from __future__ import annotations

import os

from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792
TITLE = "Can I Play?"

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
GOLD = HexColor("#F4B63E")
INK = HexColor("#202A33")
BORDER = HexColor("#B9D7D2")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "conversation-play")


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


def draw_phrase_bubble(pdf, phrase, cx, cy, w=200, font_size=13):
    """Speech-bubble badge with a small tail pointing left toward the
    scene, so the phrase reads as words the joining child can say."""
    h = 54
    x = cx - w / 2
    y = cy - h / 2
    pdf.setFillColor(HexColor("#EAF4F3"))
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    tail = pdf.beginPath()
    tail.moveTo(x + 8, cy - 5)
    tail.lineTo(x - 18, cy + 2)
    tail.lineTo(x + 8, cy + 11)
    pdf.drawPath(tail, fill=1, stroke=0)
    pdf.roundRect(x, y, w, h, 14, fill=1, stroke=1)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawCentredString(cx, cy - 4.5, phrase)


# Page 1 (Can I Play?): four large play scenes. Two children are
# already playing; a third child (right side of each scene) wants to
# join. Each scene models a different natural joining phrase.
PAGE1_ROWS = [
    ("cp-blocks-join", "Can I play?"),
    ("cp-cars-join", "I want to play too!"),
    ("cp-sandbox-join", "Let's play!"),
    ("cp-playdough-join", "Come play with me!"),
]
PAGE1_YS = [525, 389, 253, 117]


def draw_page1(pdf):
    draw_header(pdf, TITLE, "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 600,
                          "Look at the picture. Say the words.")
    for (scene, phrase), cy in zip(PAGE1_ROWS, PAGE1_YS):
        x, w, h = 36, 540, 128
        y = cy - h / 2
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
        draw_picture(pdf, scene, 195, cy, 120)
        draw_phrase_bubble(pdf, phrase, 465, cy, w=205)
    draw_footer(pdf)
    pdf.showPage()


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "communication",
        "conversation-play", "conversation-play-prototype.pdf",
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    pdf.save()
    print(f"wrote {out} (1 page)")


if __name__ == "__main__":
    main()
