#!/usr/bin/env python3
"""Build the Pre-Writing Lines & Strokes prototype PDF.

Preschool Reading & Language / Early Writing pack. Page 1 only for now
(Straight Lines); pages 2-4 (Zigzags & Steps, Curves & Waves, Mixed Paths
& Loops) are added after the Page 1 review.

Design (redesigned 2026-09-29): five large scene-based tracing activities,
each its own visual row. Illustrations are big, colorful, and drawn without
boxes; each dotted tracing path is integrated into its scene (a train track,
falling rain, a flight trail, a jump trail, a road turning a corner). No
captions on the rows: the scene carries the activity visually. Every path
starts with one small green start dot and no arrowhead.
"""

from __future__ import annotations

import io
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


def draw_illustration(pdf, stem, cx, cy, w, h=None):
    """Large illustration drawn directly on the page (no box), contained
    in a w x h frame centered at (cx, cy)."""
    path = os.path.join(ASSETS, stem + ".png")
    img = Image.open(path).convert("RGB")
    if img.width > MAX_EMBED_WIDTH:
        img = img.resize(
            (MAX_EMBED_WIDTH,
             int(img.height * MAX_EMBED_WIDTH / img.width)), Image.LANCZOS)
    iw, ih = img.size
    if h is None:
        h = w * ih / iw
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    pdf.drawImage(ImageReader(buf), cx - dw / 2, cy - dh / 2, dw, dh,
                  preserveAspectRatio=True, mask="auto")


def draw_trace_path(pdf, points):
    """One large dotted tracing path through `points`, with a single small
    green start dot and no arrowhead."""
    p = pdf.beginPath()
    p.moveTo(*points[0])
    for pt in points[1:]:
        p.lineTo(*pt)
    pdf.saveState()
    pdf.setStrokeColor(TEAL_DOT)
    pdf.setLineWidth(6.5)
    pdf.setLineCap(1)
    pdf.setLineJoin(1)
    pdf.setDash(0.5, 12)
    pdf.drawPath(p, fill=0, stroke=1)
    pdf.restoreState()
    pdf.setFillColor(GREEN)
    pdf.circle(points[0][0], points[0][1], 5.5, fill=1, stroke=0)


# ---------------------------------------------------------------- Page 1
# Five scene-based rows, evenly spaced (103pt bands inside 568 -> 53):
# B1 568-465 (cy 517): horizontal  -- train -> tunnel (the track)
# B2 465-362 (cy 414): vertical    -- cloud -> flower (falling rain)
# B3 362-259 (cy 311): diagonal down -- bird -> nest (flight trail)
# B4 259-156 (cy 208): diagonal up   -- frog -> lily pad (jump trail)
# B5 156-53  (cy 105): corner combo  -- bus -> school (road turns corner)

P1_TITLE = "Straight Lines"
P1_INSTRUCTION = "Trace the line."


def page_straight_lines(pdf):
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(MARGIN, 602, P1_TITLE)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(MARGIN, 580, P1_INSTRUCTION)

    # --- illustrations (drawn first, no boxes) ---
    # B1: train -> tunnel
    draw_illustration(pdf, "pw-train", 135, 519, 140, 95)
    draw_illustration(pdf, "pw-tunnel", 490, 519, 115, 95)
    # B2: cloud -> flower (rain)
    draw_illustration(pdf, "pw-cloud", 165, 438, 155, 64)
    draw_illustration(pdf, "pw-flower", 440, 392, 78, 78)
    # B3: bird -> nest
    draw_illustration(pdf, "pw-bird", 150, 328, 105, 84)
    draw_illustration(pdf, "pw-nest", 465, 292, 95, 75)
    # B4: frog -> lily pad
    draw_illustration(pdf, "pw-frog", 150, 190, 90, 78)
    draw_illustration(pdf, "pw-lilypad", 465, 230, 100, 70)
    # B5: bus -> school
    draw_illustration(pdf, "pw-bus", 120, 118, 135, 88)
    draw_illustration(pdf, "pw-school", 478, 98, 108, 88)

    # --- tracing paths (integrated into each scene) ---
    # B1: the train track (horizontal)
    draw_trace_path(pdf, [(215, 477), (490, 477)])
    # B2: rain falling from the cloud (vertical)
    draw_trace_path(pdf, [(325, 452), (325, 368)])
    # B3: the bird's flight trail (diagonal down)
    draw_trace_path(pdf, [(205, 340), (412, 280)])
    # B4: the frog's jump trail (diagonal up)
    draw_trace_path(pdf, [(205, 178), (412, 238)])
    # B5: the road turning the corner (horizontal, then down)
    draw_trace_path(pdf, [(200, 122), (380, 122), (380, 80)])


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
