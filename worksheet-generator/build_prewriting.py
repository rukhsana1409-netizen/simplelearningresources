#!/usr/bin/env python3
"""Build the Pre-Writing Lines & Strokes prototype PDF.

Preschool Reading & Language / Early Writing pack. Page 1 only for now
(Straight Lines); pages 2-4 (Zigzags & Steps, Curves & Waves, Mixed Paths
& Loops) are added after the Page 1 review.

Design (redesigned 2026-09-29, revised alignment): five large scene-based
tracing activities, each one connected illustrated row. Illustrations are
big, colorful, and drawn without boxes; each dotted tracing path begins
immediately beside its starting picture and finishes immediately beside
its destination -- the two pictures are positioned around the path, not
independently from it. Vertical activity: start picture directly above
the line, destination directly below, centered on the same axis.
Horizontal activities: both pictures share the row's axis with the line.
Diagonal activities: pictures aligned precisely with the path endpoints.
No captions on the rows. Every path starts with one small green start dot
and no arrowhead. All Page 1 paths are straight.
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


def draw_illustration(pdf, stem, cx, cy, w, h=None, flip=False):
    """Large illustration drawn directly on the page (no box), contained
    in a w x h frame centered at (cx, cy). flip mirrors it horizontally."""
    path = os.path.join(ASSETS, stem + ".png")
    img = Image.open(path).convert("RGB")
    if flip:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
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
# Five connected illustrated rows. Each dotted path begins immediately
# beside its starting picture and finishes immediately beside its
# destination; the pictures are positioned around the path.
# B1 568-484 (84):  horizontal     -- train -> station (the track)
# B2 484-328 (156): vertical       -- cloud -> flower (rain), stacked on x=306
# B3 328-236 (92):  diagonal down  -- bird -> nest (flight trail)
# B4 236-144 (92):  diagonal up    -- frog -> lily pad (jump trail)
# B5 144-53  (91):  horizontal     -- bus -> school (straight road)

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
    # B1: train -> station
    draw_illustration(pdf, "pw-train", 128, 528, 128, 82)
    draw_illustration(pdf, "pw-station", 488, 528, 108, 82)
    # B2: cloud -> flower (rain), stacked on the path axis
    draw_illustration(pdf, "pw-cloud", 306, 460, 118, 50)
    draw_illustration(pdf, "pw-flower", 306, 358, 58, 58)
    # B3: bird -> nest
    draw_illustration(pdf, "pw-bird", 135, 322, 90, 72)
    draw_illustration(pdf, "pw-nest", 418, 258, 78, 58)
    # B4: frog -> lily pad (diagonal up)
    draw_illustration(pdf, "pw-frog", 210, 168, 82, 68)
    draw_illustration(pdf, "pw-lilypad", 507, 222, 84, 56)
    # B5: bus -> school
    draw_illustration(pdf, "pw-bus", 124, 94, 128, 82)
    draw_illustration(pdf, "pw-school", 484, 92, 102, 78)

    # --- tracing paths (each connects its two pictures) ---
    # B1: the train track (horizontal)
    draw_trace_path(pdf, [(196, 494), (432, 494)])
    # B2: rain falling from the cloud to the flower (vertical)
    draw_trace_path(pdf, [(306, 429), (306, 389)])
    # B3: the bird's flight trail (diagonal down)
    draw_trace_path(pdf, [(186, 314), (375, 262)])
    # B4: the frog's jump trail (diagonal up)
    draw_trace_path(pdf, [(256, 176), (461, 226)])
    # B5: the road to school (straight horizontal)
    draw_trace_path(pdf, [(192, 62), (430, 62)])


# ---------------------------------------------------------------- Page 2
# Five connected zigzag/step rows, easy -> harder (even 103pt bands):
# R1 568-465 (cy 517): bunny -> carrot   (small zigzag, 2 peaks)
# R2 465-362 (cy 414): mouse -> cheese   (ascending steps, 2 steps)
# R3 362-259 (cy 311): fish -> treasure  (medium zigzag, 3 peaks)
# R4 259-156 (cy 208): penguin -> igloo    (descending steps, 3 steps)
# R5 156-53  (cy 105): rocket -> planet  (big zigzag, 4 peaks)

P2_TITLE = "Zigzags & Steps"
P2_INSTRUCTION = "Trace the line."


def page_zigzags_steps(pdf):
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(MARGIN, 602, P2_TITLE)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 13)
    pdf.drawString(MARGIN, 580, P2_INSTRUCTION)

    # --- illustrations (drawn first, no boxes) ---
    draw_illustration(pdf, "pw-bunny", 120, 516, 88, 82)
    draw_illustration(pdf, "pw-carrot", 490, 516, 72, 76)
    draw_illustration(pdf, "pw-mouse", 122, 390, 82, 76)
    draw_illustration(pdf, "pw-cheese", 490, 438, 70, 70)
    draw_illustration(pdf, "pw-fish", 120, 310, 88, 80)
    draw_illustration(pdf, "pw-treasure", 492, 310, 85, 80)
    draw_illustration(pdf, "pw-penguin", 122, 230, 80, 76)
    draw_illustration(pdf, "pw-igloo", 492, 174, 84, 68)
    draw_illustration(pdf, "pw-rocket", 120, 104, 85, 85)
    draw_illustration(pdf, "pw-planet", 490, 100, 76, 76)

    # --- tracing paths (each connects its two pictures) ---
    # R1: bunny's angular zigzag hop (2 sharp peaks)
    draw_trace_path(pdf, [(172, 516), (241, 548), (309, 484),
                          (378, 548), (446, 516)])
    # R2: mouse climbs the steps (ascending, 2 steps)
    draw_trace_path(pdf, [(175, 390), (265, 390), (265, 415),
                          (355, 415), (355, 440), (445, 440)])
    # R3: fish's zigzag swim (3 peaks)
    draw_trace_path(pdf, [(172, 310), (218, 334), (263, 286), (309, 334),
                          (354, 286), (400, 334), (444, 310)])
    # R4: penguin slides down the steps (descending, 3 steps)
    draw_trace_path(pdf, [(172, 235), (240, 235), (240, 215), (308, 215),
                          (308, 195), (376, 195), (376, 175), (445, 175)])
    # R5: rocket's big zigzag flight (4 peaks)
    draw_trace_path(pdf, [(172, 104), (206, 136), (241, 72), (275, 136),
                          (309, 72), (343, 136), (378, 72), (412, 136),
                          (446, 104)])


PAGES = [page_straight_lines, page_zigzags_steps]


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
