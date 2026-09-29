"""Build Conversation & Play (Preschool Communication & Life Skills) — prototype.

Page 1 (Can I Play?): four rich, full-scene play illustrations
(blocks, cars, sandbox, tea party). In each scene two children are
already playing and a third child wants to join. Each scene models
a DIFFERENT short, natural joining phrase (GLP-friendly
whole-language chunks: "Can I play?", "I want to play too!",
"Let's play!", "Come play with me!").
The child looks at the picture and says the words.

Layout follows the approved reference: pastel-tinted rounded rows,
scene filling the left of each row, white speech bubble with a
colored border on the right, instruction in a pill banner, and the
established Learning Made Simple brand header and footer.

An adult reads the words aloud; the activity does not depend on
independent reading.
"""

from __future__ import annotations

import os

from PIL import Image
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
NAVY = HexColor("#1E3A5F")

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


def draw_scene_fill(pdf, stem, x, y, w, h, r):
    """Draw the scene aspect-filled into the left part of the row:
    rounded on the left edge (to match the row), straight on the
    right where it meets the pastel fill."""
    path = os.path.join(ASSETS, stem + ".png")
    with Image.open(path) as im:
        iw, ih = im.size
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    pdf.saveState()
    p = pdf.beginPath()
    p.moveTo(x + r, y)
    p.lineTo(x + w, y)
    p.lineTo(x + w, y + h)
    p.lineTo(x + r, y + h)
    p.arc(x, y + h - 2 * r, x + 2 * r, y + h, startAng=90, extent=90)
    p.lineTo(x, y + r)
    p.arc(x, y, x + 2 * r, y + 2 * r, startAng=180, extent=90)
    p.close()
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.drawImage(path, x - (dw - w) / 2, y - (dh - h) / 2, dw, dh,
                  mask="auto")
    pdf.restoreState()


def draw_speech_bubble(pdf, lines, accent, cx, cy, w=168, h=72):
    """White speech bubble with a colored border and a tail pointing
    left toward the joining child in the scene."""
    x = cx - w / 2
    y = cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(2.5)
    tail = pdf.beginPath()
    tail.moveTo(x + 10, cy - 6)
    tail.lineTo(x - 26, cy + 4)
    tail.lineTo(x + 10, cy + 12)
    pdf.drawPath(tail, fill=1, stroke=0)
    pdf.roundRect(x, y, w, h, 18, fill=1, stroke=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    lh = 19
    top = cy + (len(lines) - 1) * lh / 2
    for i, line in enumerate(lines):
        pdf.drawCentredString(cx, top - i * lh - 5, line)


# Page 1 rows: (scene stem, phrase lines, pastel fill, accent border).
PAGE1_ROWS = [
    ("cp-blocks-room", ["Can I play?"],
     HexColor("#E9F3FD"), HexColor("#4A90D9")),
    ("cp-cars-room", ["I want to", "play too!"],
     HexColor("#FFF6DE"), HexColor("#E0A63B")),
    ("cp-sandbox-yard", ["Let's play!"],
     HexColor("#FCE8F0"), HexColor("#DF5F92")),
    ("cp-tea-room", ["Come play", "with me!"],
     HexColor("#E7F6E9"), HexColor("#4FAE62")),
]
PAGE1_YS = [508, 388, 268, 148]
ROW_X, ROW_W, ROW_H, ROW_R = 24, 564, 112, 14
IMG_W = 350


def draw_page1(pdf):
    draw_header(pdf, TITLE, "Preschool Communication & Life Skills")
    # Instruction pill banner.
    pill_w, pill_h, pill_cy = 400, 36, 600
    pdf.setFillColor(HexColor("#D9EAF7"))
    pdf.roundRect(PAGE_WIDTH / 2 - pill_w / 2, pill_cy - pill_h / 2,
                  pill_w, pill_h, 18, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, pill_cy - 5,
                          "Look at the picture. Say the words.")
    for (scene, lines, fill, accent), cy in zip(PAGE1_ROWS, PAGE1_YS):
        y = cy - ROW_H / 2
        # Pastel row base.
        pdf.setFillColor(fill)
        pdf.setStrokeColor(fill)
        pdf.roundRect(ROW_X, y, ROW_W, ROW_H, ROW_R, fill=1, stroke=0)
        # Scene filling the left of the row.
        draw_scene_fill(pdf, scene, ROW_X, y, IMG_W, ROW_H, ROW_R)
        # Row border on top.
        pdf.setFillColor(fill)
        pdf.setStrokeColor(accent)
        pdf.setLineWidth(2.5)
        pdf.roundRect(ROW_X, y, ROW_W, ROW_H, ROW_R, fill=0, stroke=1)
        # Speech bubble on the right.
        draw_speech_bubble(pdf, lines, accent, 492, cy)
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
