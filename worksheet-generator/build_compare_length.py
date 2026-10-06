# Build the Compare Length & Height pack (Kindergarten Math).
# Non-standard measurement: longer/shorter, taller/shorter, longest/shortest,
# measuring length/height with equal-sized cubes. Pure vector reportlab output.
# Pages carry a (title, builder, locked) flag. Approved pages are NEVER
# rebuilt differently: builders for locked pages are frozen.
#
# P1 only for now (review). P2-P6 to be added after P1 approval.
#
# Usage: ../.venv/bin/python build_compare_length.py

import os
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

PAGE_WIDTH = 612
PAGE_HEIGHT = 792

TEAL = HexColor("#0E7C7B")
TEAL_DARK = HexColor("#0B6362")
INK = HexColor("#1F2A37")
NAVY = HexColor("#1F3A5F")

# cheerful light object palette
SNAKE = HexColor("#7BC96F")
WORM = HexColor("#F2A4B8")
PENCIL_Y = HexColor("#FFD54A")
WOOD = HexColor("#E8B06E")
ER_PINK = HexColor("#F6A9C0")
GRAY = HexColor("#9AA5B1")
CRAYON_B = HexColor("#6FB3E8")
SCARF_R = HexColor("#E86A5E")
SCARF_D = HexColor("#C24E43")
SOCK_B = HexColor("#8FC1F0")
SOCK_LT = HexColor("#BFE0FA")
BROOM_W = HexColor("#B07A4F")
BRISTLE = HexColor("#E3B96B")
BRUSH_T = HexColor("#7FD1C8")
TRAIN_R = HexColor("#E86A5E")
TRAIN_D = HexColor("#B74A41")
CAR_B = HexColor("#6FB3E8")
GLASS = HexColor("#BFE3FF")
RULER_C = HexColor("#F5D76E")
TONGUE = HexColor("#E4574D")
WHEEL_CTR = HexColor("#D9E6F2")
# P2 height-comparison palette
LEAF = HexColor("#7BC96F")
TRUNK = HexColor("#A9764F")
BLD = HexColor("#F6C453")
BLD_D = HexColor("#D9A53B")
CANDLE_C = HexColor("#F6A9C0")
FLAME = HexColor("#FFD54A")
FLAME_D = HexColor("#E8A33D")
BOTTLE_C = HexColor("#7FD1C8")
CAP_C = HexColor("#E86A5E")
PETAL = HexColor("#C39BD3")
PETAL_D = HexColor("#9B72B0")
FLOWER_CTR = HexColor("#F2C14E")
STEM = HexColor("#5DA85F")
BLOCK_A = HexColor("#F6C453")
BLOCK_B = HexColor("#8FC1F0")
# P4 replacement-object palette
MARKER_C = HexColor("#9B72B0")
SPOON_C = HexColor("#C9D4DC")
BOOK_C = HexColor("#6FBF73")
BOOK_D = HexColor("#4E9A52")
MUG_C = HexColor("#F2994A")
MUG_D = HexColor("#D97F33")
CONE_C = HexColor("#E8B06E")
SCOOP_C = HexColor("#F2A4B8")
PANEL_BG = HexColor("#F7FAFC")
# P6 palette
RIBBON_C = HexColor("#E86A8E")
RIBBON_D = HexColor("#C24E73")
BUS_C = HexColor("#F2B134")


def draw_logo(pdf, x, y):
    pdf.setFillColor(TEAL)
    pdf.circle(x, y, 9, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#F2C14E"))
    pdf.circle(x + 7, y + 11, 5, fill=1, stroke=0)
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1.6)
    pdf.line(x, y - 9, x - 8, y - 20)
    pdf.line(x, y - 9, x + 8, y - 20)
    pdf.line(x, y - 9, x, y - 21)


def draw_header(pdf, page_title, subtitle):
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, fill=1, stroke=0)
    draw_logo(pdf, 78, 720)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(96, 728, "LEARNING")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(96, 714, "MADE SIMPLE")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1)
    pdf.line(196, 700, 196, 742)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(212, 726, page_title)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(212, 706, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    pdf.line(40, 688, PAGE_WIDTH - 40, 688)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(40, 668, "Name:")
    pdf.line(82, 666, 300, 666)
    pdf.drawString(330, 668, "Date:")
    pdf.line(368, 666, 540, 666)


def draw_instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630, text)


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF2F1"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, 18, "Learning Made Simple")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(0.8)
    pdf.line(190, 8, 190, 30)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_WIDTH / 2, 18, "Made with love for little learners.")
    pdf.drawRightString(PAGE_WIDTH - 40, 18, "\u00a9 2026 Learning Made Simple")


def draw_panel(pdf, x, top, w, h):
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - h, w, h, 12, stroke=1, fill=1)


def wavy_stroke(pdf, x, y, length, amp, waves, color, thick):
    """Wavy horizontal stroke centered on y. Used for snake, worm, scarf."""
    pdf.setStrokeColor(color)
    pdf.setLineWidth(thick)
    pdf.setLineCap(1)
    p = pdf.beginPath()
    p.moveTo(x, y)
    n = max(2, int(waves * 2))
    dx = length / n
    for i in range(n):
        x0 = x + i * dx
        s = 1 if i % 2 == 0 else -1
        p.curveTo(x0 + dx * 0.3, y + s * amp,
                  x0 + dx * 0.7, y + s * amp, x0 + dx, y)
    pdf.drawPath(p, stroke=1, fill=0)


# ---------------------------------------------------------------------------
# Familiar objects (original vector artwork). Each draws from left x with its
# baseline at y (everything sits on or above y). Widths noted for layout.
# ---------------------------------------------------------------------------
def draw_snake(pdf, x, y):  # ~150 wide
    wavy_stroke(pdf, x, y + 16, 122, 9, 2.5, SNAKE, 17)
    hx, hy = x + 124, y + 16
    pdf.setFillColor(SNAKE)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.circle(hx, hy, 13, stroke=1, fill=1)
    pdf.setFillColor(white)
    pdf.circle(hx + 4, hy + 5, 4.5, stroke=1, fill=1)
    pdf.setFillColor(INK)
    pdf.circle(hx + 5, hy + 5, 2, stroke=0, fill=1)
    pdf.setStrokeColor(TONGUE)
    pdf.setLineWidth(2)
    pdf.line(hx + 12, hy - 2, hx + 20, hy - 2)
    pdf.line(hx + 20, hy - 2, hx + 24, hy - 5)
    pdf.line(hx + 20, hy - 2, hx + 24, hy + 1)


def draw_worm(pdf, x, y, body=52):  # total width = body + 12
    wavy_stroke(pdf, x, y + 10, body, 6, body / 36.0, WORM, 12)
    hx = x + body + 2
    pdf.setFillColor(WORM)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.4)
    pdf.circle(hx, y + 10, 8, stroke=1, fill=1)
    pdf.setFillColor(white)
    pdf.circle(hx + 3, y + 13, 3, stroke=0, fill=1)
    pdf.setFillColor(INK)
    pdf.circle(hx + 4, y + 13, 1.5, stroke=0, fill=1)


def draw_pencil(pdf, x, y, body=92):  # total width = body + 41
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.4)
    pdf.setFillColor(ER_PINK)
    pdf.rect(x, y, 14, 14, stroke=1, fill=1)
    pdf.setFillColor(GRAY)
    pdf.rect(x + 14, y, 7, 14, stroke=1, fill=1)
    pdf.setFillColor(PENCIL_Y)
    pdf.rect(x + 21, y, body, 14, stroke=1, fill=1)
    bx = x + 21 + body
    pdf.setFillColor(WOOD)
    p = pdf.beginPath()
    p.moveTo(bx, y)
    p.lineTo(bx, y + 14)
    p.lineTo(bx + 20, y + 7)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(INK)
    p = pdf.beginPath()
    p.moveTo(bx + 11, y + 4)
    p.lineTo(bx + 11, y + 10)
    p.lineTo(bx + 20, y + 7)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)


def draw_crayon(pdf, x, y):  # ~72 wide
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.4)
    pdf.setFillColor(CRAYON_B)
    pdf.rect(x, y, 46, 18, stroke=1, fill=1)
    p = pdf.beginPath()
    p.moveTo(x + 46, y)
    p.lineTo(x + 46, y + 18)
    p.lineTo(x + 62, y + 9)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(SOCK_LT)
    pdf.rect(x + 8, y, 12, 18, stroke=1, fill=1)


def draw_scarf(pdf, x, y, length=132):  # total width = length + 18
    wavy_stroke(pdf, x + 6, y + 14, length, 7, length / 66.0, SCARF_R, 24)
    pdf.setStrokeColor(white)
    pdf.setLineWidth(4)
    for f in (0.25, 0.5, 0.75):
        sx = x + 6 + length * f
        pdf.line(sx, y + 4, sx, y + 24)
    pdf.setStrokeColor(SCARF_D)
    pdf.setLineWidth(2)
    for i in range(3):
        pdf.line(x + 4, y + 8 + i * 6, x - 6, y + 6 + i * 7)
        pdf.line(x + 8 + length, y + 8 + i * 6, x + 18 + length, y + 6 + i * 7)


def draw_sock(pdf, x, y):  # ~56 wide, ~50 tall
    pdf.setFillColor(SOCK_B)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    p = pdf.beginPath()
    p.moveTo(x, y)
    p.lineTo(x + 56, y)
    p.lineTo(x + 56, y + 20)
    p.lineTo(x + 26, y + 20)
    p.lineTo(x + 26, y + 48)
    p.lineTo(x, y + 48)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(white)
    pdf.rect(x, y + 38, 26, 10, stroke=1, fill=1)
    pdf.setFillColor(SCARF_R)
    pdf.rect(x, y + 30, 26, 6, stroke=1, fill=1)


def draw_broom(pdf, x, y):  # ~150 wide
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.4)
    pdf.setFillColor(BROOM_W)
    pdf.rect(x, y + 10, 104, 10, stroke=1, fill=1)
    pdf.setFillColor(BRISTLE)
    p = pdf.beginPath()
    p.moveTo(x + 104, y + 2)
    p.lineTo(x + 146, y + 2)
    p.lineTo(x + 138, y + 30)
    p.lineTo(x + 112, y + 30)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(SCARF_R)
    pdf.rect(x + 108, y + 22, 30, 7, stroke=1, fill=1)
    pdf.setStrokeColor(HexColor("#9A6B3F"))
    pdf.setLineWidth(1.2)
    for bx in (x + 116, x + 124, x + 132, x + 140):
        pdf.line(bx, y + 4, bx - 3, y + 22)


def draw_toothbrush(pdf, x, y, handle=52):  # total width = handle + 20
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.4)
    pdf.setFillColor(BRUSH_T)
    pdf.roundRect(x, y + 4, handle, 10, 5, stroke=1, fill=1)
    pdf.setFillColor(white)
    pdf.rect(x + handle, y + 4, 16, 14, stroke=1, fill=1)
    pdf.setStrokeColor(CRAYON_B)
    pdf.setLineWidth(2)
    for bx in (x + handle + 3, x + handle + 7, x + handle + 11):
        pdf.line(bx, y + 18, bx, y + 24)


def draw_train(pdf, x, y, body=124, wheels=3):  # total width = body + 32
    pdf.setFillColor(INK)
    wx0 = x + 28
    wspan = body - 36
    wxs = [wx0 + i * wspan / (wheels - 1) for i in range(wheels)] if wheels > 1 else [wx0]
    for wx in wxs:
        pdf.circle(wx, y + 10, 10, stroke=0, fill=1)
    pdf.setFillColor(WHEEL_CTR)
    for wx in wxs:
        pdf.circle(wx, y + 10, 4, stroke=0, fill=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(TRAIN_R)
    pdf.rect(x + 8, y + 16, body, 24, stroke=1, fill=1)
    pdf.setFillColor(TRAIN_D)
    pdf.rect(x + 8, y + 40, 34, 24, stroke=1, fill=1)
    pdf.setFillColor(GLASS)
    pdf.rect(x + 14, y + 46, 20, 12, stroke=1, fill=1)
    pdf.setFillColor(INK)
    pdf.rect(x + 8 + body - 32, y + 40, 12, 14, stroke=1, fill=1)
    pdf.setFillColor(TRAIN_D)
    p = pdf.beginPath()
    p.moveTo(x + 8 + body, y + 16)
    p.lineTo(x + 8 + body + 14, y + 16)
    p.lineTo(x + 8 + body, y + 2)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)


def draw_car(pdf, x, y):  # ~92 wide
    pdf.setFillColor(INK)
    pdf.circle(x + 22, y + 9, 9, stroke=0, fill=1)
    pdf.circle(x + 70, y + 9, 9, stroke=0, fill=1)
    pdf.setFillColor(WHEEL_CTR)
    pdf.circle(x + 22, y + 9, 3.5, stroke=0, fill=1)
    pdf.circle(x + 70, y + 9, 3.5, stroke=0, fill=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(CAR_B)
    pdf.roundRect(x, y + 12, 92, 18, 7, stroke=1, fill=1)
    pdf.setFillColor(GLASS)
    pdf.roundRect(x + 24, y + 26, 44, 16, 6, stroke=1, fill=1)


def draw_ruler(pdf, x, y, length=150):
    pdf.setFillColor(RULER_C)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.4)
    pdf.rect(x, y, length, 16, stroke=1, fill=1)
    pdf.setLineWidth(1)
    for i in range(1, int(length / 10)):
        tx = x + i * 10
        ln = 8 if i % 5 == 0 else 5
        pdf.line(tx, y + 16, tx, y + 16 - ln)


def draw_eraser(pdf, x, y):  # ~52 wide
    pdf.setFillColor(ER_PINK)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.roundRect(x, y, 52, 24, 5, stroke=1, fill=1)
    pdf.setFillColor(HexColor("#FBD3E2"))
    pdf.rect(x + 30, y, 22, 24, stroke=0, fill=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.roundRect(x, y, 52, 24, 5, stroke=1, fill=0)


# ---------------------------------------------------------------------------
# Page 1 -- Longer or Shorter?  (same-object pairs; only length differs)
# ---------------------------------------------------------------------------
from functools import partial

# (left_fn, left_w, right_fn, right_w, prompt)
P1_ROWS = [
    (partial(draw_worm, body=96), 110,
     partial(draw_worm, body=52), 66, "Circle the longer one."),
    (partial(draw_pencil, body=92), 135,
     partial(draw_pencil, body=48), 91, "Circle the shorter one."),
    (partial(draw_scarf, length=76), 96,
     partial(draw_scarf, length=132), 152, "Circle the longer one."),
    (partial(draw_toothbrush, handle=20), 42,
     partial(draw_toothbrush, handle=52), 74, "Circle the shorter one."),
    (partial(draw_train, body=68, wheels=2), 102,
     partial(draw_train, body=124, wheels=3), 158, "Circle the longer one."),
    (partial(draw_ruler, length=84), 84,
     partial(draw_ruler, length=150), 150, "Circle the shorter one."),
]


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Longer or Shorter?", "Compare Length & Height")
    draw_instruction(pdf, "Look at each pair. Circle the longer or shorter object.")

    tops = (600, 512, 424, 336, 248, 160)
    for k, (lfn, lw, rfn, rw, prompt) in enumerate(P1_ROWS):
        top = tops[k]
        draw_panel(pdf, 40, top, 532, 84)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(58, top - 48, prompt)
        base = top - 70
        # two object slots with a shared baseline for fair comparison
        ax = 236 + (156 - lw) / 2
        bx = 392 + (156 - rw) / 2
        lfn(pdf, ax, base)
        rfn(pdf, bx, base)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Taller or Shorter?  (same-object pairs; only height differs)
# Objects share one baseline per row so height is visually accurate.
# ---------------------------------------------------------------------------
def draw_tree(pdf, x, y, H=58):  # H = total height; width ~0.52*H
    h = H / 0.83
    w = h * 0.62
    cx = x + w / 2
    trunk_h = h * 0.30
    pdf.setFillColor(TRUNK)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.rect(cx - 6, y, 12, trunk_h, stroke=1, fill=1)
    r = h * 0.20
    cy = y + trunk_h + r * 0.85
    pdf.setFillColor(LEAF)
    for dx, dy in ((-r * 0.72, 0), (r * 0.72, 0), (0, r * 0.8)):
        pdf.circle(cx + dx, cy + dy, r, stroke=0, fill=1)


def draw_building(pdf, x, y, h=58, w=52, win_rows=2, door_h=15):
    pdf.setFillColor(BLD)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.rect(x, y, w, h, stroke=1, fill=1)
    pdf.setFillColor(BLD_D)
    pdf.rect(x, y + h - 7, w, 7, stroke=1, fill=1)
    pdf.setFillColor(TRUNK)
    pdf.rect(x + w / 2 - 8, y, 16, door_h, stroke=1, fill=1)
    pdf.setFillColor(GLASS)
    pdf.setLineWidth(1.2)
    for r in range(win_rows):
        wy = y + h - 19 - r * 17
        pdf.rect(x + 8, wy, 13, 10, stroke=1, fill=1)
        pdf.rect(x + w - 21, wy, 13, 10, stroke=1, fill=1)


def draw_candle(pdf, x, y, body=41):  # total height = body + 17; width 26
    w = 26
    pdf.setFillColor(CANDLE_C)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.rect(x, y, w, body, stroke=1, fill=1)
    pdf.circle(x + 8, y + body, 3, stroke=1, fill=1)
    pdf.circle(x + 18, y + body, 3, stroke=1, fill=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2)
    pdf.line(x + w / 2, y + body + 1, x + w / 2, y + body + 5)
    pdf.setFillColor(FLAME)
    pdf.setStrokeColor(FLAME_D)
    pdf.setLineWidth(1.2)
    p = pdf.beginPath()
    p.moveTo(x + w / 2 - 5, y + body + 5)
    p.curveTo(x + w / 2 - 5, y + body + 12, x + w / 2, y + body + 17,
              x + w / 2, y + body + 17)
    p.curveTo(x + w / 2, y + body + 17, x + w / 2 + 5, y + body + 12,
              x + w / 2 + 5, y + body + 5)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)


def draw_bottle(pdf, x, y, h=58):  # width 32; cap/neck/shoulders fixed, body varies
    w = 32
    cap_h, neck_h, sh_h = 6, 8, 9
    body_h = h - cap_h - neck_h - sh_h
    pdf.setFillColor(BOTTLE_C)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.rect(x, y, w, body_h, stroke=1, fill=1)
    p = pdf.beginPath()
    p.moveTo(x, y + body_h)
    p.lineTo(x + w, y + body_h)
    p.lineTo(x + w - 7, y + body_h + sh_h)
    p.lineTo(x + 7, y + body_h + sh_h)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.rect(x + 10, y + body_h + sh_h, 12, neck_h, stroke=1, fill=1)
    pdf.setFillColor(CAP_C)
    pdf.rect(x + 8, y + body_h + sh_h + neck_h, 16, cap_h, stroke=1, fill=1)
    if body_h >= 16:
        pdf.setFillColor(white)
        pdf.setLineWidth(1.2)
        pdf.rect(x + 6, y + body_h * 0.28, w - 12, body_h * 0.36,
                 stroke=1, fill=1)


def draw_flower(pdf, x, y, h=58, leaves=2):  # width 52; head fixed, stem varies
    cx = x + 26
    stem_top = y + h - 17
    pdf.setStrokeColor(STEM)
    pdf.setLineWidth(5)
    pdf.setLineCap(1)
    pdf.line(cx, y, cx, stem_top)
    pdf.setFillColor(LEAF)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.2)
    pdf.ellipse(cx - 18, y + 8, cx - 4, y + 17, stroke=1, fill=1)
    if leaves > 1:
        pdf.ellipse(cx + 4, y + 16, cx + 18, y + 25, stroke=1, fill=1)
    pdf.setFillColor(PETAL)
    pdf.setStrokeColor(PETAL_D)
    pdf.setLineWidth(1.2)
    for a in range(5):
        ang = math.radians(a * 72 - 90)
        pdf.circle(cx + 10 * math.cos(ang), stem_top + 10 * math.sin(ang),
                   7, stroke=1, fill=1)
    pdf.setFillColor(FLOWER_CTR)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.4)
    pdf.circle(cx, stem_top, 6.5, stroke=1, fill=1)


def draw_tower(pdf, x, y, n=3, bs=19):  # width 24; snap-cube style stack
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    for i in range(n):
        pdf.setFillColor(BLOCK_A if i % 2 == 0 else BLOCK_B)
        pdf.rect(x, y + i * bs, 24, bs, stroke=1, fill=1)


def draw_ladder(pdf, x, y, h=58, w=34, rungs=4):  # width 34
    rail_w = 7
    pdf.setFillColor(BROOM_W)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.rect(x, y, rail_w, h, stroke=1, fill=1)
    pdf.rect(x + w - rail_w, y, rail_w, h, stroke=1, fill=1)
    pdf.setFillColor(BRISTLE)
    pdf.setLineWidth(1.2)
    for i in range(rungs):
        ry = y + 5 + i * (h - 16) / (rungs - 1) if rungs > 1 else y + 5
        pdf.rect(x + rail_w, ry, w - 2 * rail_w, 6, stroke=1, fill=1)


# (left_fn, left_w, right_fn, right_w, prompt)
P2_ROWS = [
    (partial(draw_tree, H=58), 34,
     partial(draw_tree, H=34), 20, "Circle the taller one."),
    (partial(draw_building, h=58, win_rows=2), 52,
     partial(draw_building, h=36, win_rows=1), 52, "Circle the shorter one."),
    (partial(draw_candle, body=21), 26,
     partial(draw_candle, body=41), 26, "Circle the taller one."),
    (partial(draw_bottle, h=36), 32,
     partial(draw_bottle, h=58), 32, "Circle the shorter one."),
    (partial(draw_flower, h=43, leaves=1), 52,
     partial(draw_flower, h=58, leaves=2), 52, "Circle the taller one."),
    (partial(draw_ladder, h=38, rungs=3), 34,
     partial(draw_ladder, h=58, rungs=4), 34, "Circle the shorter one."),
]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Taller or Shorter?", "Compare Height")
    draw_instruction(pdf, "Look at each pair. Circle the taller or shorter one.")

    tops = (600, 512, 424, 336, 248, 160)
    for k, (lfn, lw, rfn, rw, prompt) in enumerate(P2_ROWS):
        top = tops[k]
        draw_panel(pdf, 40, top, 532, 84)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(58, top - 48, prompt)
        base = top - 66
        ax = 236 + (156 - lw) / 2
        bx = 392 + (156 - rw) / 2
        lfn(pdf, ax, base)
        rfn(pdf, bx, base)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Measure the Height
# Object + equal-block column share one bottom baseline; the object's height
# is adjusted so its top aligns exactly with the top of the final block
# (object_H = n * BLOCK_PITCH - BLOCK_GAP). Blocks are never resized.
# ---------------------------------------------------------------------------
BLOCK_SIZE = 16
BLOCK_GAP = 2
BLOCK_PITCH = BLOCK_SIZE + BLOCK_GAP  # 18


def draw_block_column(pdf, x, y, n, color):
    pdf.setLineWidth(1.6)
    pdf.setStrokeColor(INK)
    for i in range(n):
        pdf.setFillColor(color)
        pdf.rect(x, y + i * BLOCK_PITCH, BLOCK_SIZE, BLOCK_SIZE,
                 stroke=1, fill=1)


def draw_pencil_v(pdf, x, y, H=90, w=22):  # upright pencil, eraser at bottom
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(ER_PINK)
    pdf.rect(x, y, w, 10, stroke=1, fill=1)
    pdf.setFillColor(GRAY)
    pdf.rect(x, y + 10, w, 6, stroke=1, fill=1)
    tip_h = 16
    body_h = H - 10 - 6 - tip_h
    pdf.setFillColor(PENCIL_Y)
    pdf.rect(x, y + 16, w, body_h, stroke=1, fill=1)
    pdf.setFillColor(WOOD)
    p = pdf.beginPath()
    p.moveTo(x, y + 16 + body_h)
    p.lineTo(x + w, y + 16 + body_h)
    p.lineTo(x + w / 2, y + H)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(INK)
    p = pdf.beginPath()
    p.moveTo(x + w / 2 - 3.5, y + H - 7)
    p.lineTo(x + w / 2 + 3.5, y + H - 7)
    p.lineTo(x + w / 2, y + H)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)


def draw_glue(pdf, x, y, H=54, w=30):  # school glue bottle, nozzle cap on top
    cap_h = 14
    body_h = H - cap_h
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(white)
    pdf.roundRect(x, y, w, body_h, 5, stroke=1, fill=1)
    pdf.setFillColor(HexColor("#D6E9FF"))
    pdf.rect(x + 4, y + 4, w - 8, body_h - 12, stroke=0, fill=1)
    pdf.setFillColor(CAP_C)
    pdf.setLineWidth(1.2)
    pdf.rect(x, y + body_h * 0.35, w, 10, stroke=1, fill=1)
    pdf.setFillColor(HexColor("#F2994A"))
    pdf.setLineWidth(1.6)
    p = pdf.beginPath()
    p.moveTo(x + 4, y + body_h)
    p.lineTo(x + w - 4, y + body_h)
    p.lineTo(x + w / 2 + 4, y + H)
    p.lineTo(x + w / 2 - 4, y + H)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)


def draw_crayon_v(pdf, x, y, H=72, w=20):  # upright crayon, tip at top
    tip_h = 14
    body_h = H - tip_h
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(CRAYON_B)
    pdf.rect(x, y, w, body_h, stroke=1, fill=1)
    p = pdf.beginPath()
    p.moveTo(x, y + body_h)
    p.lineTo(x + w, y + body_h)
    p.lineTo(x + w / 2, y + H)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(SOCK_LT)
    pdf.setLineWidth(1.2)
    pdf.rect(x, y + 8, w, 12, stroke=1, fill=1)


def draw_rocket(pdf, x, y, H=126, w=40, nose_h=None):  # toy rocket; total width = w + 28
    nose_h = 30 if nose_h is None else nose_h
    cx = x + 14 + w / 2
    bx = x + 14
    body_h = H - nose_h
    pdf.setFillColor(CAP_C)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    for sgn in (-1, 1):
        fx = bx if sgn < 0 else bx + w
        p = pdf.beginPath()
        p.moveTo(fx, y)
        p.lineTo(fx + sgn * 14, y)
        p.lineTo(fx, y + 26)
        p.close()
        pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(BOTTLE_C)
    pdf.roundRect(bx, y, w, body_h, 10, stroke=1, fill=1)
    pdf.setFillColor(CAP_C)
    p = pdf.beginPath()
    p.moveTo(bx, y + body_h)
    p.lineTo(bx + w, y + body_h)
    p.lineTo(cx, y + H)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(GLASS)
    pdf.circle(cx, y + max(14, body_h - 22), 9, stroke=0, fill=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.4)
    pdf.circle(cx, y + max(14, body_h - 22), 9, stroke=1, fill=0)


# (object_fn, object_w, object_H, block_count, block_color) -- heights 2..7
# MEASUREMENT INVARIANT: object_H == block_count * BLOCK_PITCH - BLOCK_GAP,
# i.e. the object's top aligns exactly with the top of the final block.
# Blocks are never resized; only the object height is adjusted.
P3_PROBLEMS = [
    (partial(draw_flower, h=34, leaves=1), 52, 34, 2, HexColor("#F2A4B8")),
    (partial(draw_glue, H=52), 30, 52, 3, HexColor("#F6C453")),
    (partial(draw_crayon_v, H=70), 20, 70, 4, HexColor("#8FC1F0")),
    (partial(draw_pencil_v, H=88), 22, 88, 5, HexColor("#7FD1C8")),
    (partial(draw_bottle, h=106), 32, 106, 6, HexColor("#C39BD3")),
    (partial(draw_rocket, H=124), 68, 124, 7, HexColor("#F2994A")),
]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Measure the Height", "Measure with Blocks")
    draw_instruction(pdf, "Count the blocks. Write the height.")

    xs = (40, 316)
    tops = (606, 430, 254)
    for k, (ofn, ow, oH, n, color) in enumerate(P3_PROBLEMS):
        # mathematical check: object top == top of final block
        assert oH == n * BLOCK_PITCH - BLOCK_GAP, (oH, n)
        col, row = k % 2, k // 2
        px, top = xs[col], tops[row]
        draw_panel(pdf, px, top, 256, 168)
        baseline = top - 132
        # shared ground line
        pdf.setStrokeColor(HexColor("#C9D8D2"))
        pdf.setLineWidth(2)
        pdf.line(px + 16, baseline, px + 234, baseline)
        # object, centered in its zone
        ofn(pdf, px + 20 + (80 - ow) / 2, baseline)
        # block column
        draw_block_column(pdf, px + 118, baseline, n, color)
        # answer box + "blocks"
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2)
        pdf.roundRect(px + 156, baseline, 62, 42, 8, stroke=1, fill=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 14)
        pdf.drawCentredString(px + 187, baseline - 18, "blocks")

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Extra familiar objects for P4 (each reaches exactly its H parameter).
# ---------------------------------------------------------------------------
def draw_marker_v(pdf, x, y, H=70, w=20):  # chubby marker standing on its cap
    cap_h = 14
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(HexColor("#5B6B7A"))
    pdf.roundRect(x, y, w, cap_h, 4, stroke=1, fill=1)
    pdf.setFillColor(MARKER_C)
    pdf.rect(x, y + cap_h, w, H - cap_h, stroke=1, fill=1)
    pdf.setFillColor(white)
    pdf.setLineWidth(1.2)
    pdf.rect(x, y + H - 12, w, 8, stroke=1, fill=1)


def draw_spoon_v(pdf, x, y, H=52, w=24):  # upright spoon, bowl at top
    bowl_h = 22
    cx = x + w / 2
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(SPOON_C)
    pdf.roundRect(cx - 4, y, 8, H - bowl_h + 6, 4, stroke=1, fill=1)
    pdf.ellipse(x, y + H - bowl_h, x + w, y + H, stroke=1, fill=1)


def draw_book_v(pdf, x, y, H=70, w=34):  # standing book
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(BOOK_C)
    pdf.roundRect(x, y, w, H, 3, stroke=1, fill=1)
    pdf.setFillColor(BOOK_D)
    pdf.rect(x, y, 9, H, stroke=1, fill=1)
    pdf.setFillColor(white)
    pdf.setLineWidth(1.2)
    pdf.rect(x + 13, y + H * 0.55, w - 17, H * 0.18, stroke=1, fill=1)


def draw_mug(pdf, x, y, H=52, w=30):  # total width = w + 12 (handle)
    body_h = H - 6
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(MUG_C)
    pdf.roundRect(x, y, w, body_h, 4, stroke=1, fill=1)
    pdf.setFillColor(MUG_D)
    pdf.rect(x, y + body_h - 8, w, 8, stroke=1, fill=1)
    pdf.setFillColor(MUG_C)
    pdf.roundRect(x + w - 4, y + 10, 16, body_h - 20, 8, stroke=1, fill=1)
    pdf.setFillColor(PANEL_BG)
    pdf.roundRect(x + w, y + 14, 8, body_h - 28, 5, stroke=0, fill=1)


def draw_toothbrush_v(pdf, x, y, H=52, w=18):  # upright toothbrush, head at top
    head_h = 12
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(BRUSH_T)
    pdf.roundRect(x, y, w, H - head_h, 8, stroke=1, fill=1)
    pdf.setFillColor(white)
    pdf.rect(x, y + H - head_h, w, head_h - 4, stroke=1, fill=1)
    pdf.setStrokeColor(CRAYON_B)
    pdf.setLineWidth(2)
    for bxx in (x + 4, x + 9, x + 14):
        pdf.line(bxx, y + H - 4, bxx, y + H)


def draw_icecream(pdf, x, y, H=88, w=30):  # cone + scoop
    r = w / 2
    cone_h = H - r
    cx = x + w / 2
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(CONE_C)
    p = pdf.beginPath()
    p.moveTo(x, y + cone_h)
    p.lineTo(x + w, y + cone_h)
    p.lineTo(cx, y)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(SCOOP_C)
    pdf.circle(cx, y + cone_h, r, stroke=1, fill=1)
    pdf.setFillColor(CAP_C)
    pdf.circle(cx, y + cone_h + r - 5, 4, stroke=1, fill=1)


# ---------------------------------------------------------------------------
# Page 4 -- Compare the Heights
# Two objects per problem, each with its own equal-block column. All four
# share one baseline; each object's height is adjusted to an exact whole
# number of blocks (object_H = n * BLOCK_PITCH - BLOCK_GAP). Blocks are
# never resized. No answers or counts are printed.
# ---------------------------------------------------------------------------
# (objA_fn, objA_w, objA_H, nA, objB_fn, objB_w, objB_H, nB, column_color)
P4_PROBLEMS = [
    (partial(draw_flower, h=34, leaves=1), 52, 34, 2,
     partial(draw_marker_v, H=70), 20, 70, 4, HexColor("#F2A4B8")),
    (partial(draw_rocket, H=124), 68, 124, 7,
     partial(draw_spoon_v, H=52), 24, 52, 3, HexColor("#8FC1F0")),
    (partial(draw_book_v, H=70), 34, 70, 4,
     partial(draw_bottle, h=106), 32, 106, 6, HexColor("#F6C453")),
    (partial(draw_pencil_v, H=124), 22, 124, 7,
     partial(draw_mug, H=52), 42, 52, 3, HexColor("#7FD1C8")),
    (partial(draw_toothbrush_v, H=52), 18, 52, 3,
     partial(draw_pencil_v, H=106), 22, 106, 6, HexColor("#C39BD3")),
    (partial(draw_bottle, h=142), 32, 142, 8,
     partial(draw_icecream, H=88), 30, 88, 5, HexColor("#F2994A")),
]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Compare the Heights", "Measure with Blocks")
    draw_instruction(pdf, "Count the blocks. Circle the taller object.")

    xs = (40, 316)
    tops = (606, 430, 254)
    for k, (afn, aw, aH, nA, bfn, bw, bH, nB, color) in enumerate(P4_PROBLEMS):
        # mathematical check: each object top == top of its final block
        assert aH == nA * BLOCK_PITCH - BLOCK_GAP, (aH, nA)
        assert bH == nB * BLOCK_PITCH - BLOCK_GAP, (bH, nB)
        col, row = k % 2, k // 2
        px, top = xs[col], tops[row]
        draw_panel(pdf, px, top, 256, 168)
        baseline = top - 148
        # each object sits right beside its own column (one visual pair);
        # the two pairs are separated by a wide gap
        gap_oc, gap_pairs = 12, 40
        total = aw + gap_oc + 16 + gap_pairs + bw + gap_oc + 16
        x0 = px + (256 - total) / 2
        ax = x0
        acx = ax + aw + gap_oc
        bx = acx + 16 + gap_pairs
        bcx = bx + bw + gap_oc
        # shared ground line for both pairs
        pdf.setStrokeColor(HexColor("#C9D8D2"))
        pdf.setLineWidth(2)
        pdf.line(x0 - 6, baseline, bcx + 22, baseline)
        afn(pdf, ax, baseline)
        draw_block_column(pdf, acx, baseline, nA, color)
        bfn(pdf, bx, baseline)
        draw_block_column(pdf, bcx, baseline, nB, color)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Horizontal objects for length measurement (each reaches exactly its L).
# ---------------------------------------------------------------------------
def draw_pencil_h(pdf, x, y, L=124, h=20):  # pointing right, eraser at left
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(ER_PINK)
    pdf.rect(x, y, 12, h, stroke=1, fill=1)
    pdf.setFillColor(GRAY)
    pdf.rect(x + 12, y, 6, h, stroke=1, fill=1)
    pdf.setFillColor(PENCIL_Y)
    pdf.rect(x + 18, y, L - 36, h, stroke=1, fill=1)
    pdf.setFillColor(WOOD)
    p = pdf.beginPath()
    p.moveTo(x + L - 18, y)
    p.lineTo(x + L - 18, y + h)
    p.lineTo(x + L, y + h / 2)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(INK)
    p = pdf.beginPath()
    p.moveTo(x + L - 9, y + h / 2 - 3.5)
    p.lineTo(x + L - 9, y + h / 2 + 3.5)
    p.lineTo(x + L, y + h / 2)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)


def draw_crayon_h(pdf, x, y, L=52, h=22):  # tip pointing right
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(CRAYON_B)
    pdf.rect(x, y, L - 16, h, stroke=1, fill=1)
    p = pdf.beginPath()
    p.moveTo(x + L - 16, y)
    p.lineTo(x + L - 16, y + h)
    p.lineTo(x + L, y + h / 2)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(SOCK_LT)
    pdf.setLineWidth(1.2)
    pdf.rect(x + 6, y, 10, h, stroke=1, fill=1)


def draw_toothbrush_h(pdf, x, y, L=88):  # handle left, head right, bristles up
    hw = L - 18
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(BRUSH_T)
    pdf.roundRect(x, y, hw, 12, 6, stroke=1, fill=1)
    pdf.setFillColor(white)
    pdf.rect(x + hw, y - 2, 18, 16, stroke=1, fill=1)
    pdf.setStrokeColor(CRAYON_B)
    pdf.setLineWidth(2)
    for bxx in (x + hw + 4, x + hw + 9, x + hw + 14):
        pdf.line(bxx, y + 14, bxx, y + 20)


def draw_spoon_h(pdf, x, y, L=70):  # handle left, bowl right
    bowl_w = 26
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(SPOON_C)
    pdf.roundRect(x, y + 4, L - bowl_w + 6, 10, 5, stroke=1, fill=1)
    pdf.ellipse(x + L - bowl_w, y, x + L, y + 20, stroke=1, fill=1)


def draw_car_h(pdf, x, y, L=142):  # toy car side view
    pdf.setFillColor(INK)
    for wxx in (x + 24, x + L / 2, x + L - 24):
        pdf.circle(wxx, y + 9, 9, stroke=0, fill=1)
    pdf.setFillColor(WHEEL_CTR)
    for wxx in (x + 24, x + L / 2, x + L - 24):
        pdf.circle(wxx, y + 9, 3.5, stroke=0, fill=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(CAR_B)
    pdf.roundRect(x, y + 12, L, 20, 8, stroke=1, fill=1)
    pdf.setFillColor(GLASS)
    pdf.roundRect(x + L * 0.28, y + 28, L * 0.32, 16, 6, stroke=1, fill=1)


def draw_paintbrush_h(pdf, x, y, L=106):  # handle left, bristles right
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(BROOM_W)
    pdf.roundRect(x, y + 5, L - 34, 11, 5, stroke=1, fill=1)
    pdf.setFillColor(GRAY)
    pdf.rect(x + L - 34, y + 3, 12, 15, stroke=1, fill=1)
    pdf.setFillColor(BRISTLE)
    p = pdf.beginPath()
    p.moveTo(x + L - 22, y + 4)
    p.lineTo(x + L - 22, y + 17)
    p.lineTo(x + L, y + 10.5)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)


# Page 5 -- Measure the Length (revised: measure + compare + draw)
# Three activity types in one 2x3 grid:
#   A x3: count the blocks, write the length (answer box + "blocks")
#   B x2: two measured objects, circle the longer one
#   C x1: 5-block reference row + spacious drawing area
# Measurement invariant: object length = n * BLOCK_PITCH - BLOCK_GAP.
# ---------------------------------------------------------------------------
# Type A: (object_fn, length, blocks, color)
P5A = [
    (partial(draw_crayon_h, L=52), 52, 3, HexColor("#8FC1F0")),
    (partial(draw_toothbrush_h, L=88), 88, 5, HexColor("#7FD1C8")),
    (partial(draw_pencil_h, L=124), 124, 7, HexColor("#C39BD3")),
]
# Type B: (top_fn, top_len, top_n, bottom_fn, bottom_len, bottom_n, color)
P5B = [
    (partial(draw_paintbrush_h, L=106), 106, 6,
     partial(draw_spoon_h, L=52), 52, 3, HexColor("#F6C453")),
    (partial(draw_toothbrush_h, L=70), 70, 4,
     partial(draw_pencil_h, L=124), 124, 7, HexColor("#F2994A")),
]


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Measure the Length", "Measure with Blocks")
    draw_instruction(pdf, "Measure length with blocks.")

    xs = (40, 316)
    tops = (606, 430, 254)

    def panel_prompt(px, top, text):
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(px + 16, top - 22, text)

    def block_row(bx, by, n, color):
        pdf.setLineWidth(1.6)
        pdf.setStrokeColor(INK)
        for i in range(n):
            pdf.setFillColor(color)
            pdf.rect(bx + i * BLOCK_PITCH, by, BLOCK_SIZE, BLOCK_SIZE,
                     stroke=1, fill=1)

    # --- Type A: count and write ---
    for (col, row), (ofn, oL, n, color) in zip([(0, 0), (1, 0), (0, 1)], P5A):
        assert oL == n * BLOCK_PITCH - BLOCK_GAP, (oL, n)
        px, top = xs[col], tops[row]
        draw_panel(pdf, px, top, 256, 168)
        panel_prompt(px, top, "How many blocks long?")
        by = top - 118
        ox = px + 24
        ofn(pdf, ox, by + 28)
        block_row(ox, by, n, color)
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2)
        pdf.roundRect(px + 178, by, 62, 42, 8, stroke=1, fill=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 14)
        pdf.drawCentredString(px + 209, by - 18, "blocks")

    # --- Type B: circle the longer object ---
    for (col, row), (tfn, tL, tn, bfn, bL, bn, color) in zip([(1, 1), (0, 2)], P5B):
        assert tL == tn * BLOCK_PITCH - BLOCK_GAP, (tL, tn)
        assert bL == bn * BLOCK_PITCH - BLOCK_GAP, (bL, bn)
        px, top = xs[col], tops[row]
        draw_panel(pdf, px, top, 256, 168)
        panel_prompt(px, top, "Circle the longer object.")
        ox = px + 24
        by1, by2 = top - 82, top - 140
        tfn(pdf, ox, by1 + 24)
        block_row(ox, by1, tn, color)
        bfn(pdf, ox, by2 + 24)
        block_row(ox, by2, bn, color)

    # --- Type C: draw something 5 blocks long ---
    px, top = xs[1], tops[2]
    draw_panel(pdf, px, top, 256, 168)
    panel_prompt(px, top, "Draw something 5 blocks long.")
    block_row(px + 24, top - 64, 5, HexColor("#8FC1F0"))
    pdf.setStrokeColor(HexColor("#B9CBD4"))
    pdf.setLineWidth(1.6)
    pdf.setDash(5, 4)
    pdf.roundRect(px + 24, top - 158, 208, 70, 10, stroke=1, fill=0)
    pdf.setDash()

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 6 -- Order by Length (shortest to longest)
# Five panels; each shows three same-design objects in mixed length order.
# Objects share a common baseline, left-aligned per zone; a number box sits
# below each zone for writing 1/2/3. No blocks, no answers printed.
# ---------------------------------------------------------------------------
def draw_ribbon(pdf, x, y, L=96, h=16):  # straight ribbon, fishtail cut
    pdf.setFillColor(RIBBON_C)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    p = pdf.beginPath()
    p.moveTo(x, y)
    p.lineTo(x + L - 12, y)
    p.lineTo(x + L, y + h / 2)
    p.lineTo(x + L - 12, y + h)
    p.lineTo(x, y + h)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setStrokeColor(RIBBON_D)
    pdf.setLineWidth(1.2)
    for fx in (0.3, 0.6):
        pdf.line(x + L * fx, y + 2, x + L * fx + 6, y + h - 2)


def draw_bus(pdf, x, y, L=112):  # school bus side view, 38 tall
    pdf.setFillColor(INK)
    for wxx in (x + 20, x + L - 20):
        pdf.circle(wxx, y + 8, 8, stroke=0, fill=1)
    pdf.setFillColor(WHEEL_CTR)
    for wxx in (x + 20, x + L - 20):
        pdf.circle(wxx, y + 8, 3, stroke=0, fill=1)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(BUS_C)
    pdf.roundRect(x, y + 12, L, 26, 8, stroke=1, fill=1)
    pdf.setFillColor(GLASS)
    pdf.setLineWidth(1.2)
    nwin = max(2, int(L / 28))
    for i in range(nwin):
        wx = x + 10 + i * ((L - 20) / nwin)
        pdf.roundRect(wx, y + 20, (L - 20) / nwin - 8, 12, 3, stroke=1, fill=1)


# each panel: three (draw_fn, length) in mixed display order (never sorted)
P6_SETS = [
    [(partial(draw_pencil_h, L=104), 104),
     (partial(draw_pencil_h, L=72), 72),
     (partial(draw_pencil_h, L=136), 136)],
    [(partial(draw_crayon_h, L=128), 128),
     (partial(draw_crayon_h, L=64), 64),
     (partial(draw_crayon_h, L=96), 96)],
    [(partial(draw_ribbon, L=72), 72),
     (partial(draw_ribbon, L=136), 136),
     (partial(draw_ribbon, L=104), 104)],
    [(partial(draw_bus, L=112), 112),
     (partial(draw_bus, L=144), 144),
     (partial(draw_bus, L=80), 80)],
    [(partial(draw_paintbrush_h, L=136), 136),
     (partial(draw_paintbrush_h, L=104), 104),
     (partial(draw_paintbrush_h, L=72), 72)],
]


def build_p6_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Order by Length", "Shortest to Longest")
    draw_instruction(pdf, "Number the objects: 1 = shortest, 2 = middle, 3 = longest.")

    tops = (606, 500, 394, 288, 182)
    for s, triples in enumerate(P6_SETS):
        top = tops[s]
        draw_panel(pdf, 40, top, 532, 100)
        base = top - 56  # common baseline for all three objects
        for z, (fn, L) in enumerate(triples):
            zx = 48 + z * 173  # zone left; object left-aligned (common start)
            fn(pdf, zx, base)
            # number box centered below the zone
            pdf.setFillColor(white)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(2)
            pdf.roundRect(zx + 85 - 19, top - 94, 38, 30, 8, stroke=1, fill=1)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Page 7 -- Order by Height (shortest to tallest) -- redesigned
# Four large panels; each shows three same-design objects in mixed height
# order on one clearly visible common baseline. Only HEIGHT varies within a
# set -- widths stay fixed. Large number box below each object for 1/2/3.
# ---------------------------------------------------------------------------
def draw_tree_h(pdf, x, y, H=70, w=54):  # fixed-width tree; only height varies
    cx = x + w / 2
    r = 15
    canopy_cy = y + H - r - 2
    pdf.setFillColor(TRUNK)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.8)
    pdf.rect(cx - 7, y, 14, canopy_cy - r * 0.5 - y, stroke=1, fill=1)
    pdf.setFillColor(LEAF)
    for dx, dy in ((-r * 0.72, 0), (r * 0.72, 0), (0, r * 0.75)):
        pdf.circle(cx + dx, canopy_cy + dy, r, stroke=0, fill=1)


# each panel: three (draw_fn, width) in mixed display order (never sorted)
# heights: short 40 / medium 58 / tall 76 -- very obvious, not extreme
P7_SETS = [
    [(partial(draw_tree_h, H=58, w=54), 54),
     (partial(draw_tree_h, H=76, w=54), 54),
     (partial(draw_tree_h, H=40, w=54), 54)],
    [(partial(draw_flower, h=40, leaves=1), 52),
     (partial(draw_flower, h=76, leaves=2), 52),
     (partial(draw_flower, h=58, leaves=1), 52)],
    [(partial(draw_rocket, H=76, nose_h=24), 68),
     (partial(draw_rocket, H=40, nose_h=13), 68),
     (partial(draw_rocket, H=58, nose_h=19), 68)],
    [(partial(draw_pencil_v, H=58), 22),
     (partial(draw_pencil_v, H=40), 22),
     (partial(draw_pencil_v, H=76), 22)],
]


def build_p7_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Order by Height", "Shortest to Tallest")
    draw_instruction(pdf, "Number the objects: 1 = shortest, 2 = middle, 3 = tallest.")

    tops = (608, 474, 340, 206)
    for s, triples in enumerate(P7_SETS):
        top = tops[s]
        draw_panel(pdf, 40, top, 532, 126)
        base = top - 82  # one clearly visible common baseline
        pdf.setStrokeColor(HexColor("#C9D8D2"))
        pdf.setLineWidth(2)
        pdf.line(56, base, 556, base)
        for z, (fn, w) in enumerate(triples):
            zc = 48 + z * 173 + 86  # zone center
            fn(pdf, zc - w / 2, base)  # object centered in its zone
            # large number box directly below the object
            pdf.setFillColor(white)
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(2)
            pdf.roundRect(zc - 21, top - 120, 42, 34, 8, stroke=1, fill=1)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    # (title, builder, locked)
    ("Longer or Shorter?", build_p1_page, True),   # approved & locked 2026-10-06
    ("Taller or Shorter?", build_p2_page, True),   # approved & locked 2026-10-06
    ("Measure the Height", build_p3_page, True),  # approved & locked 2026-10-06
    ("Compare the Heights", build_p4_page, True),  # approved & locked 2026-10-06
    ("Measure the Length", build_p5_page, True),  # approved & locked 2026-10-06
    ("Order by Length", build_p6_page, True),  # approved & locked 2026-10-06
    ("Order by Height", build_p7_page, True),  # approved & locked 2026-10-06
]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "worksheets", "kindergarten", "math",
                           "compare-length-height")
    os.makedirs(out_dir, exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "clh_tmp_%d.pdf" % i)
        builder(tmp)
        pages.append(tmp)
        print("built page: %s" % title)
    from pypdf import PdfWriter
    writer = PdfWriter()
    for p in pages:
        writer.append(p)
    final = os.path.join(out_dir, "compare-length-height-review.pdf")
    with open(final, "wb") as f:
        writer.write(f)
    print("merged %d page(s) -> %s" % (len(pages), final))


if __name__ == "__main__":
    main()
