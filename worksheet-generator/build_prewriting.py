#!/usr/bin/env python3
"""Build the Pre-Writing Lines & Strokes prototype PDF.

Preschool Reading & Language / Early Writing pack. Page 1 only for now
(Straight Lines); pages 2-4 (Zigzags & Steps, Curves & Waves, Mixed Paths
& Loops) are added after the Page 1 review.

Design: six large tracing rows. Each row pairs two colorful illustrations
with one large dotted tracing path between them. No captions on the rows:
the illustrations and path carry the activity visually. Every path starts
with a green start dot plus one subtle direction arrowhead.
"""

from __future__ import annotations

import io
import math
import os

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792

PACK_TITLE = "Pre-Writing Lines & Strokes"
SUBTITLE = "Preschool Reading & Language"

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
TEAL_DOT = HexColor("#2A9D90")
GREEN = HexColor("#2E9E44")
GOLD = HexColor("#F4B63E")
INK = HexColor("#202A33")
BORDER = HexColor("#B9D7D2")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "pre-writing")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "preschool", "reading",
                       "pre-writing-lines-strokes")
OUT = os.path.join(OUT_DIR, "pre-writing-lines-strokes-prototype.pdf")

MAX_EMBED_WIDTH = 600


def draw_logo(pdf, x, y):
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


def draw_header(pdf):
    """Established brand header (Learn My Letters style)."""
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, fill=1, stroke=0)
    draw_logo(pdf, MARGIN, PAGE_HEIGHT - 86)
    divider_x = 210
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1)
    pdf.line(divider_x, PAGE_HEIGHT - 46, divider_x, PAGE_HEIGHT - 106)
    title_x = divider_x + 19
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(title_x, PAGE_HEIGHT - 67, "Pre-Writing")
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(title_x, PAGE_HEIGHT - 98, "Lines & Strokes")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11.5)
    pdf.drawString(title_x, PAGE_HEIGHT - 116, SUBTITLE)
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


def draw_picture_card(pdf, stem, cx, cy, size, r=14):
    """Illustration shown whole inside a soft rounded card."""
    path = os.path.join(ASSETS, stem + ".png")
    img = Image.open(path).convert("RGB")
    if img.width > MAX_EMBED_WIDTH:
        img = img.resize(
            (MAX_EMBED_WIDTH,
             int(img.height * MAX_EMBED_WIDTH / img.width)), Image.LANCZOS)
    pdf.setFillColor(white)
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(2)
    pdf.roundRect(cx - size / 2, cy - size / 2, size, size, r,
                  fill=1, stroke=1)
    pad = 7
    iw, ih = img.size
    scale = min((size - 2 * pad) / iw, (size - 2 * pad) / ih)
    dw, dh = iw * scale, ih * scale
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    pdf.drawImage(ImageReader(buf), cx - dw / 2, cy - dh / 2, dw, dh,
                  preserveAspectRatio=True, mask="auto")


def draw_trace_path(pdf, x1, y1, x2, y2):
    """One large dotted tracing path with a green start dot and a single
    subtle direction arrowhead just past the start."""
    pdf.saveState()
    pdf.setStrokeColor(TEAL_DOT)
    pdf.setLineWidth(5)
    pdf.setLineCap(1)
    pdf.setDash(0.5, 11)
    pdf.line(x1, y1, x2, y2)
    pdf.restoreState()
    # green start dot
    pdf.setFillColor(GREEN)
    pdf.circle(x1, y1, 7.5, fill=1, stroke=0)
    # single subtle direction arrowhead
    ang = math.atan2(y2 - y1, x2 - x1)
    d = 26            # distance from start dot center to arrow tip
    back = 11         # arrow length
    half_w = 5        # arrow half width
    tx = x1 + d * math.cos(ang)
    ty = y1 + d * math.sin(ang)
    bx = x1 + (d - back) * math.cos(ang)
    by = y1 + (d - back) * math.sin(ang)
    px, py = -math.sin(ang), math.cos(ang)
    pdf.setFillColor(TEAL_DARK)
    p = pdf.beginPath()
    p.moveTo(tx, ty)
    p.lineTo(bx + half_w * px, by + half_w * py)
    p.lineTo(bx - half_w * px, by - half_w * py)
    p.close()
    pdf.drawPath(p, fill=1, stroke=0)


# ---------------------------------------------------------------- Page 1
# Six large rows with engineered vertical rhythm: no two cards in the
# same column ever come closer than 8pt. Row bands (top -> bottom):
# R1 84, R2 60, R3 104, R4 84, R5 104, R6 60, inside 568 -> 68.

P1_TITLE = "Straight Lines"
P1_INSTRUCTION = "Trace the line."

LEFT_X, RIGHT_X = 110, 502
MID_X = 306


def page_straight_lines(pdf):
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(MARGIN, 602, P1_TITLE)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(MARGIN, 580, P1_INSTRUCTION)

    # R1 (cy 526): vertical line down -- bee (top-left) to flower (bottom-right)
    draw_picture_card(pdf, "pw-bee", LEFT_X, 542, 44)
    draw_picture_card(pdf, "pw-flower", RIGHT_X, 510, 44)
    draw_trace_path(pdf, MID_X, 556, MID_X, 496)

    # R2 (cy 454): horizontal line -- car to garage
    draw_picture_card(pdf, "pw-car", LEFT_X, 454, 48)
    draw_picture_card(pdf, "pw-garage", RIGHT_X, 454, 48)
    draw_trace_path(pdf, 150, 454, 462, 454)

    # R3 (cy 372): diagonal line down-right -- bird to nest
    draw_picture_card(pdf, "pw-bird", LEFT_X, 394, 48)
    draw_picture_card(pdf, "pw-nest", RIGHT_X, 350, 48)
    draw_trace_path(pdf, 168, 414, 444, 330)

    # R4 (cy 278): vertical line up -- balloon (bottom-left) to cloud (top-right)
    draw_picture_card(pdf, "pw-balloon", LEFT_X, 262, 44)
    draw_picture_card(pdf, "pw-cloud", RIGHT_X, 294, 44)
    draw_trace_path(pdf, MID_X, 248, MID_X, 308)

    # R5 (cy 184): diagonal line up-right -- frog to lily pad
    draw_picture_card(pdf, "pw-frog", LEFT_X, 162, 48)
    draw_picture_card(pdf, "pw-lilypad", RIGHT_X, 206, 48)
    draw_trace_path(pdf, 168, 140, 444, 228)

    # R6 (cy 102): long horizontal line -- bus to school
    draw_picture_card(pdf, "pw-bus", LEFT_X, 102, 48)
    draw_picture_card(pdf, "pw-school", RIGHT_X, 102, 48)
    draw_trace_path(pdf, 150, 102, 462, 102)


PAGES = [page_straight_lines]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    pdf = canvas.Canvas(OUT, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    for page in PAGES:
        draw_header(pdf)
        draw_footer(pdf)
        page(pdf)
        pdf.showPage()
    pdf.save()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
