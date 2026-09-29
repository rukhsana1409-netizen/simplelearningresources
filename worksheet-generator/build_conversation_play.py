"""Build Conversation & Play: Phrases I Can Use (Preschool Communication
& Life Skills) — prototype.

A practical phrase resource for preschool children, including gestalt
language processors: natural, reusable whole-language chunks they can
actually use during play, school, and interactions with friends.

Each page: one large contextual scene (~25-30% of the page) to
establish the environment, then 8 colorful phrase cards in a spacious
2-column x 4-row grid as the visual focus. Large readable text,
generous spacing, soft varied colors, and a small meaningful icon
only where it genuinely helps comprehension. No tiny decorative
clipart.

Page 1 — At the Playground (phrases locked 2026-09-29):
  "Can I play?" / "Come play with me!" / "Can I have a turn, please?" /
  "I'm waiting for my turn." / "Watch out! I'm coming!" /
  "Can you push me, please?" / "That was fun!" / "Let's do it again!"

Instruction: "Say the words. Try them when you play!"

An adult reads the words aloud; the activity does not depend on
independent reading.
"""

from __future__ import annotations

import math
import os

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

PAGE_WIDTH, PAGE_HEIGHT = 612, 792
PREFIX = "Phrases I Can Use"
FOCUS = "At the Playground"

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


def draw_scene(pdf, stem, x, y, w, h, r):
    """Large contextual scene, aspect-filled into a rounded rect."""
    path = os.path.join(ASSETS, stem + ".png")
    with Image.open(path) as im:
        iw, ih = im.size
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    pdf.saveState()
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.drawImage(path, x - (dw - w) / 2, y - (dh - h) / 2, dw, dh,
                  mask="auto")
    pdf.restoreState()


def _arrowhead(pdf, ex, ey, theta, size=7):
    """Two barbs forming an arrowhead pointing along theta."""
    for sgn in (1, -1):
        a = theta + sgn * math.radians(150)
        pdf.line(ex, ey, ex + size * math.cos(a), ey + size * math.sin(a))


def _arc_arrow(pdf, x1, y1, x2, y2, start, extent):
    """Arc with an arrowhead at its end, pointing along travel."""
    p = pdf.beginPath()
    p.arc(x1, y1, x2, y2, startAng=start, extent=extent)
    pdf.drawPath(p, fill=0, stroke=1)
    end = math.radians(start + extent)
    rx, ry = (x2 - x1) / 2, (y2 - y1) / 2
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    ex, ey = cx + rx * math.cos(end), cy + ry * math.sin(end)
    theta = math.atan2(ry * math.cos(end), -rx * math.sin(end))
    _arrowhead(pdf, ex, ey, theta)


def draw_icon(pdf, kind, cx, cy):
    """Small, simple vector cue — consistent size/style, secondary to
    the phrase text. Each one helps a preschooler understand or
    remember the phrase."""
    if kind == "star":
        pdf.setFillColor(HexColor("#F4B63E"))
        pdf.setStrokeColor(HexColor("#D99420"))
        pdf.setLineWidth(1)
        pts = []
        for i in range(10):
            ang = math.pi / 2 + i * math.pi / 5
            rad = 14 if i % 2 == 0 else 6
            pts += [cx + rad * math.cos(ang), cy + rad * math.sin(ang)]
        p = pdf.beginPath()
        p.moveTo(pts[0], pts[1])
        for j in range(2, len(pts), 2):
            p.lineTo(pts[j], pts[j + 1])
        p.close()
        pdf.drawPath(p, fill=1, stroke=1)
    elif kind == "swing":
        pdf.setStrokeColor(HexColor("#2E86C1"))
        pdf.setLineCap(1)
        pdf.setLineWidth(2.5)
        pdf.line(cx - 11, cy + 13, cx + 11, cy + 13)
        pdf.line(cx - 7, cy + 13, cx - 7, cy - 8)
        pdf.line(cx + 7, cy + 13, cx + 7, cy - 8)
        pdf.setLineWidth(4.5)
        pdf.line(cx - 9, cy - 8, cx + 9, cy - 8)
    elif kind == "slide":
        pdf.setStrokeColor(HexColor("#D94F4F"))
        pdf.setLineCap(1)
        pdf.setLineWidth(2.5)
        pdf.line(cx - 11, cy - 12, cx - 11, cy + 12)
        pdf.setLineWidth(2)
        for ry in (-6, 0, 6):
            pdf.line(cx - 11, cy + ry, cx - 4, cy + ry)
        pdf.setStrokeColor(HexColor("#2E86C1"))
        pdf.setLineWidth(4.5)
        pdf.line(cx - 4, cy + 12, cx + 12, cy - 12)
        # small child sliding down the chute
        pdf.setFillColor(HexColor("#2E86C1"))
        pdf.circle(cx + 4, cy + 4, 3.6, fill=1, stroke=0)
    elif kind == "repeat":
        pdf.setStrokeColor(HexColor("#3D9E4D"))
        pdf.setLineCap(1)
        pdf.setLineWidth(3)
        _arc_arrow(pdf, cx - 10, cy - 10, cx + 10, cy + 10,
                   start=40, extent=280)
    elif kind == "swap":
        # two turn-taking arrows chasing each other
        pdf.setStrokeColor(HexColor("#8E44AD"))
        pdf.setLineCap(1)
        pdf.setLineWidth(2.8)
        _arc_arrow(pdf, cx - 11, cy - 3, cx + 11, cy + 11,
                   start=200, extent=140)
        _arc_arrow(pdf, cx - 11, cy - 11, cx + 11, cy + 3,
                   start=20, extent=140)
    elif kind == "clock":
        pdf.setStrokeColor(HexColor("#1E3A5F"))
        pdf.setLineCap(1)
        pdf.setLineWidth(2.5)
        pdf.circle(cx, cy, 11, fill=0, stroke=1)
        pdf.setLineWidth(2.2)
        pdf.line(cx, cy, cx, cy + 7)
        pdf.line(cx, cy, cx + 5, cy - 1)
    elif kind == "figures":
        # two children playing together
        pdf.setFillColor(HexColor("#2E86C1"))
        pdf.circle(cx - 8, cy + 6, 5, fill=1, stroke=0)
        pdf.circle(cx + 8, cy + 6, 5, fill=1, stroke=0)
        pdf.roundRect(cx - 13, cy - 12, 10, 13, 4, fill=1, stroke=0)
        pdf.roundRect(cx + 3, cy - 12, 10, 13, 4, fill=1, stroke=0)
    elif kind == "hand":
        # inviting wave: open hand with motion arcs
        pdf.setStrokeColor(HexColor("#2E86C1"))
        pdf.setLineCap(1)
        pdf.setLineWidth(2.5)
        pdf.roundRect(cx - 8, cy - 10, 13, 14, 5, fill=0, stroke=1)
        for fx in (-5, -1.5, 2):
            pdf.line(cx + fx, cy + 4, cx + fx, cy + 11)
        pdf.line(cx - 8, cy - 3, cx - 13, cy + 1)
        pdf.setLineWidth(2)
        p = pdf.beginPath()
        p.arc(cx + 7, cy - 8, cx + 17, cy + 8, startAng=-55, extent=110)
        pdf.drawPath(p, fill=0, stroke=1)


# Page 1 phrase cards: (lines, card fill, icon kind or None).
# Every phrase stays on ONE line (gestalt chunks are never split);
# the font auto-fits to the card width instead.
PAGE1_CARDS = [
    (["Can I play?"], HexColor("#E2F0FD"), "figures"),
    (["Come play with me!"], HexColor("#FFF4D6"), "hand"),
    (["Can I have a turn, please?"], HexColor("#FCE4EC"), "swap"),
    (["I'm waiting for my turn."], HexColor("#E2F4E2"), "clock"),
    (["Watch out! I'm coming!"], HexColor("#ECE4FA"), "slide"),
    (["Can you push me, please?"], HexColor("#FFE4D1"), "swing"),
    (["That was fun!"], HexColor("#D9F0F0"), "star"),
    (["Let's do it again!"], HexColor("#E6EAFB"), "repeat"),
]

CARD_X = (40, 313)
CARD_W, CARD_H, CARD_R, CARD_GAP = 259, 58, 16, 10
CARD_TOP = 326  # top edge of the first card row


def fit_font(lines, max_w, start=16, minimum=12.5):
    fs = start
    while fs > minimum:
        if max(stringWidth(l, "Helvetica-Bold", fs) for l in lines) <= max_w:
            return fs
        fs -= 0.5
    return minimum


def draw_card(pdf, lines, fill, icon, cx, cy):
    x = cx - CARD_W / 2
    y = cy - CARD_H / 2
    pdf.setFillColor(fill)
    pdf.roundRect(x, y, CARD_W, CARD_H, CARD_R, fill=1, stroke=0)
    text_cx = cx + 12 if icon else cx
    max_w = CARD_W - (86 if icon else 40)
    fs = fit_font(lines, max_w)
    if icon:
        draw_icon(pdf, icon, x + 30, cy)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", fs)
    lh = fs * 1.28
    if len(lines) == 1:
        pdf.drawCentredString(text_cx, cy - fs * 0.35, lines[0])
    else:
        top = cy + lh / 2
        for i, line in enumerate(lines):
            pdf.drawCentredString(text_cx, top - i * lh - fs * 0.35, line)


def draw_page1(pdf):
    draw_header(pdf, f"{PREFIX}: {FOCUS}",
                "Preschool Communication & Life Skills")
    # Large contextual scene (~26% of the page).
    draw_scene(pdf, "cp-playground-scene", 40, 390, 532, 210, 18)
    # Instruction pill.
    pill_w, pill_h, pill_cy = 400, 36, 358
    pdf.setFillColor(HexColor("#D9EAF7"))
    pdf.roundRect(PAGE_WIDTH / 2 - pill_w / 2, pill_cy - pill_h / 2,
                  pill_w, pill_h, 18, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, pill_cy - 5,
                          "Say the words. Try them when you play!")
    # 8 phrase cards, 2 columns x 4 rows.
    for i, (lines, fill, icon) in enumerate(PAGE1_CARDS):
        row, col = divmod(i, 2)
        cx = CARD_X[col] + CARD_W / 2
        cy = CARD_TOP - CARD_H / 2 - row * (CARD_H + CARD_GAP)
        draw_card(pdf, lines, fill, icon, cx, cy)
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
    pdf.setTitle(f"{PREFIX}: {FOCUS} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    pdf.save()
    print(f"wrote {out} (1 page)")


if __name__ == "__main__":
    main()
