#!/usr/bin/env python3
"""My Calendar & Time — Preschool Thinking & Our World: Time & Sequence.

An academic calendar pack (not a visual-support schedule): the calendar
concepts are the visual focus. Children appear only where they genuinely
improve understanding. Reusable/cut-apart elements are an optional bonus —
every page must make sense and provide value when simply printed.

Page 1 (LOCKED): Days of the Week — seven large horizontal strips stacked
vertically (Sunday first), rainbow-like soft-color progression, very large
bold dark day names, one small original vector icon at the left of each
strip, compact optional TODAY tag near the bottom.

Page 2 (this build): Yesterday, Today & Tomorrow — three large drop-zone
panels ("Yesterday was / Today is / Tomorrow will be") with arrows
emanating outward from the Today anchor panel, plus the seven day pills in
Page 1's exact colors (cut out and place, or point). Calendar meaning, no
event-sequencing story, no characters.

Per-page builders follow; PAGES controls the lock/merge scaffold (locked
pages are carried forward byte-identical from the prototype).
"""
import math
import os
import subprocess
import tempfile

from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792
RESOURCE = "My Calendar & Time"

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
TEAL_ARROW = HexColor("#0E7C7B")
GOLD = HexColor("#F4B63E")
INK = HexColor("#202A33")
NAVY = HexColor("#1E3A5F")
CUT = HexColor("#C9D6D3")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "calendar-time")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "thinking", "time-sequence",
                   "my-calendar-time-prototype.pdf")


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
    size = 30
    pdf.setFont("Helvetica-Bold", size)
    max_w = PAGE_WIDTH - MARGIN - title_x
    while pdf.stringWidth(focus, "Helvetica-Bold", size) > max_w and size > 18:
        size -= 1
        pdf.setFont("Helvetica-Bold", size)
    pdf.drawString(title_x, PAGE_HEIGHT - 98, focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11.5)
    pdf.drawString(title_x, PAGE_HEIGHT - 116, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    rule_y = PAGE_HEIGHT - 131
    pdf.line(MARGIN, rule_y, PAGE_WIDTH - MARGIN, rule_y)
    return rule_y


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


def draw_h_arrow(pdf, x, y, length, color=TEAL_ARROW, width=2.6, head=7):
    """Small horizontal arrow pointing right, centered at (x, y)."""
    pdf.setStrokeColor(color)
    pdf.setFillColor(color)
    pdf.setLineWidth(width)
    pdf.setLineCap(1)
    pdf.line(x - length / 2, y, x + length / 2 - head * 0.6, y)
    p = pdf.beginPath()
    p.moveTo(x + length / 2, y)
    p.lineTo(x + length / 2 - head, y + head * 0.55)
    p.lineTo(x + length / 2 - head, y - head * 0.55)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)


def draw_star(pdf, cx, cy, r_outer, r_inner, fill=GOLD, stroke=None):
    """Five-pointed star centered at (cx, cy)."""
    pts = []
    for k in range(10):
        r = r_outer if k % 2 == 0 else r_inner
        a = math.pi / 2 + k * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    p = pdf.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    pdf.setFillColor(fill)
    if stroke:
        pdf.setStrokeColor(stroke)
        pdf.setLineWidth(1.6)
        pdf.drawPath(p, stroke=1, fill=1)
    else:
        pdf.drawPath(p, stroke=0, fill=1)


# ---------------------------------------------------------------------------
# Page 1: Days of the Week — calendar-time display / reference chart.
#
# Seven large horizontal strips stacked vertically (Sunday first), each in
# its own cheerful soft color (rainbow-like progression). One small original
# vector icon sits at the left of each strip, secondary to the very large,
# bold, dark day name. No arrows between days, no paths, no characters —
# the page works as a plain reference chart. A compact optional TODAY tag
# near the bottom can be cut out and placed beside the current day.
# ---------------------------------------------------------------------------

STRIP_DAYS = [
    # (day, fill, border, icon)
    ("Sunday", "#FFD9D9", "#EFA9A9", "sun"),
    ("Monday", "#FFE4C4", "#F0BE8A", "cloud"),
    ("Tuesday", "#FFF3C0", "#EAD483", "flower"),
    ("Wednesday", "#D9F0D2", "#A9D69B", "star"),
    ("Thursday", "#CFECE8", "#93CFC6", "balloon"),
    ("Friday", "#D8E8FF", "#9FC0F0", "heart"),
    ("Saturday", "#E6DBFF", "#BDA9F0", "kite"),
]

STRIP_X, STRIP_W, STRIP_H, STRIP_GAP = 40, 532, 58, 12


def _icon_sun(pdf, cx, cy):
    pdf.setStrokeColor(HexColor("#F5A623"))
    pdf.setLineWidth(2.4)
    pdf.setLineCap(1)
    for k in range(8):
        a = math.pi / 4 * k
        pdf.line(cx + 13 * math.cos(a), cy + 13 * math.sin(a),
                 cx + 18 * math.cos(a), cy + 18 * math.sin(a))
    pdf.setFillColor(HexColor("#FFC93C"))
    pdf.circle(cx, cy, 10.5, fill=1, stroke=0)


def _icon_cloud(pdf, cx, cy):
    # Light blue (not white) so it reads on the white chip.
    pdf.setFillColor(HexColor("#D9EAFB"))
    pdf.circle(cx - 9, cy + 1, 7.5, fill=1, stroke=0)
    pdf.circle(cx, cy + 6, 10, fill=1, stroke=0)
    pdf.circle(cx + 9, cy + 1, 7, fill=1, stroke=0)
    p = pdf.beginPath()
    p.ellipse(cx - 15, cy - 10, 30, 14)
    pdf.drawPath(p, stroke=0, fill=1)


def _icon_flower(pdf, cx, cy):
    pdf.setFillColor(HexColor("#F78FB3"))
    for k in range(5):
        a = math.pi * 2 * k / 5 - math.pi / 2
        px, py = cx + 9.5 * math.cos(a), cy + 9.5 * math.sin(a)
        pdf.saveState()
        pdf.translate(px, py)
        pdf.rotate(a * 180 / math.pi + 90)
        p = pdf.beginPath()
        p.ellipse(-5, -8, 10, 16)
        pdf.drawPath(p, stroke=0, fill=1)
        pdf.restoreState()
    pdf.setFillColor(HexColor("#FFC93C"))
    pdf.circle(cx, cy, 5.5, fill=1, stroke=0)


def _icon_balloon(pdf, cx, cy):
    pdf.setFillColor(HexColor("#4ECDC4"))
    p = pdf.beginPath()
    p.ellipse(cx - 11, cy - 8, 22, 26)
    pdf.drawPath(p, stroke=0, fill=1)
    p = pdf.beginPath()  # knot
    p.moveTo(cx - 3.5, cy - 12)
    p.lineTo(cx + 3.5, cy - 12)
    p.lineTo(cx, cy - 16)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(HexColor("#3AA89F"))
    pdf.setLineWidth(1.8)
    p = pdf.beginPath()  # string
    p.moveTo(cx, cy - 16)
    p.curveTo(cx - 4, cy - 20, cx + 4, cy - 23, cx - 1, cy - 26)
    pdf.drawPath(p, stroke=1, fill=0)


def _icon_heart(pdf, cx, cy):
    pdf.setFillColor(HexColor("#E8486B"))
    pdf.circle(cx - 6.5, cy + 4, 7, fill=1, stroke=0)
    pdf.circle(cx + 6.5, cy + 4, 7, fill=1, stroke=0)
    p = pdf.beginPath()
    p.moveTo(cx - 13, cy + 2)
    p.lineTo(cx + 13, cy + 2)
    p.lineTo(cx, cy - 12)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)


def _icon_kite(pdf, cx, cy):
    pdf.setFillColor(HexColor("#7B61C9"))
    p = pdf.beginPath()
    p.moveTo(cx, cy + 15)
    p.lineTo(cx + 11, cy + 1)
    p.lineTo(cx, cy - 13)
    p.lineTo(cx - 11, cy + 1)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(white)
    pdf.setLineWidth(1.4)
    pdf.line(cx, cy + 15, cx, cy - 13)
    pdf.line(cx - 11, cy + 1, cx + 11, cy + 1)
    pdf.setStrokeColor(HexColor("#7B61C9"))  # tail
    pdf.setLineWidth(1.8)
    p = pdf.beginPath()
    p.moveTo(cx, cy - 13)
    p.curveTo(cx - 3, cy - 18, cx - 8, cy - 20, cx - 9, cy - 25)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setFillColor(HexColor("#7B61C9"))  # tail bow
    p = pdf.beginPath()
    p.moveTo(cx - 9, cy - 25)
    p.lineTo(cx - 13, cy - 23)
    p.lineTo(cx - 11, cy - 28)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)


ICONS = {
    "sun": _icon_sun,
    "cloud": _icon_cloud,
    "flower": _icon_flower,
    "star": lambda pdf, cx, cy: draw_star(pdf, cx, cy, 14, 6,
                                         fill=HexColor("#FF6B6B")),
    "balloon": _icon_balloon,
    "heart": _icon_heart,
    "kite": _icon_kite,
}


def draw_day_strip(pdf, day, fill_hex, border_hex, icon, y):
    pdf.setFillColor(HexColor(fill_hex))
    pdf.setStrokeColor(HexColor(border_hex))
    pdf.setLineWidth(1.6)
    pdf.roundRect(STRIP_X, y, STRIP_W, STRIP_H, 16, stroke=1, fill=1)
    cy = y + STRIP_H / 2
    # White chip holding the small icon — keeps it secondary and tidy.
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor(border_hex))
    pdf.setLineWidth(1.2)
    pdf.roundRect(STRIP_X + 12, cy - 24, 48, 48, 13, stroke=1, fill=1)
    ICONS[icon](pdf, STRIP_X + 36, cy)
    # The day name dominates: very large, bold, dark, centered.
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 32)
    pdf.drawCentredString(STRIP_X + STRIP_W / 2 + 18, cy - 11, day)


def draw_today_tag(pdf, cx, cy):
    """Compact optional TODAY marker: gold tag with a tiny star."""
    tag_w, tag_h = 132, 40
    x = cx - tag_w / 2
    y = cy - tag_h / 2
    pdf.setFillColor(GOLD)
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, y, tag_w, tag_h, 12, stroke=1, fill=1)
    draw_star(pdf, x + 24, cy, 9.5, 4, fill=white)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(x + 40, cy - 5.5, "TODAY")


def build_days_page(out_path):
    pdf = canvas.Canvas(out_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "My Calendar & Time: Days of the Week",
                "Preschool \u00b7 Time & Sequence")
    draw_footer(pdf)

    # Child-facing instruction.
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 628,
                          "Say each day. Put the TODAY marker beside today!")

    # Seven stacked strips, Sunday first.
    top = 602
    for i, (day, fill, border, icon) in enumerate(STRIP_DAYS):
        draw_day_strip(pdf, day, fill, border, icon,
                       top - i * (STRIP_H + STRIP_GAP) - STRIP_H)

    # Compact TODAY marker with a dashed cut guide — optional; the page is
    # a complete reference chart without cutting anything.
    guide_w, guide_h = 152, 60
    gx = (PAGE_WIDTH - guide_w) / 2
    gy = 52
    pdf.setStrokeColor(CUT)
    pdf.setLineWidth(1.4)
    pdf.setDash(6, 4)
    pdf.roundRect(gx, gy, guide_w, guide_h, 14, stroke=1, fill=0)
    pdf.setDash()
    draw_today_tag(pdf, gx + guide_w / 2, gy + guide_h / 2)

    pdf.showPage()
    pdf.save()



# ---------------------------------------------------------------------------
# Page 2: Yesterday, Today & Tomorrow — calendar meaning, not event
# sequencing. Three large illustrated drop-zone panels ("Yesterday was /
# Today is / Tomorrow will be") with down-flow arrows between them
# (yesterday -> today -> tomorrow). Each panel carries a small original
# vector illustration: a calendar page marked YESTERDAY with a back arrow,
# a smiling sun with a TODAY tag, a calendar page marked TOMORROW with a
# forward arrow. Below: one dashed cut-strip holding the seven day pills in
# Page 1's exact colors AND icons, in week order — cut out and place, or
# simply point. No characters, no story pictures.
# ---------------------------------------------------------------------------

P2_PANELS = [
    # (kind, label, fill, border, border_width)
    ("yesterday", "Yesterday was", "#FFEDE6", "#E8A08A", 1.6),
    ("today", "Today is", "#E4F4FB", "#0E7C7B", 2.6),
    ("tomorrow", "Tomorrow will be", "#ECE9FB", "#9A8FE0", 1.6),
]

P2_PANEL_X, P2_PANEL_W, P2_PANEL_H, P2_PANEL_GAP = 40, 532, 120, 22


def draw_v_arrow(pdf, x, y, length, direction, color=TEAL_ARROW, width=2.6,
                 head=7):
    """Small vertical arrow centered at (x, y); direction 'up'/'down'."""
    pdf.setStrokeColor(color)
    pdf.setFillColor(color)
    pdf.setLineWidth(width)
    pdf.setLineCap(1)
    if direction == "up":
        pdf.line(x, y - length / 2, x, y + length / 2 - head * 0.6)
        p = pdf.beginPath()
        p.moveTo(x, y + length / 2)
        p.lineTo(x - head * 0.55, y + length / 2 - head)
        p.lineTo(x + head * 0.55, y + length / 2 - head)
        p.close()
    else:
        pdf.line(x, y + length / 2, x, y - length / 2 + head * 0.6)
        p = pdf.beginPath()
        p.moveTo(x, y - length / 2)
        p.lineTo(x - head * 0.55, y - length / 2 + head)
        p.lineTo(x + head * 0.55, y - length / 2 + head)
        p.close()
    pdf.drawPath(p, stroke=0, fill=1)


def fit_font(pdf, text, font, max_w, start=14, min_size=8):
    size = start
    pdf.setFont(font, size)
    while pdf.stringWidth(text, font, size) > max_w and size > min_size:
        size -= 1
        pdf.setFont(font, size)
    return size


def _p2_calendar_icon(pdf, cx, cy, accent_hex, dark_hex, word, arrow_dir):
    """Original mini calendar page: binding rings, small word, arrow."""
    accent, dark = HexColor(accent_hex), HexColor(dark_hex)
    w, h = 62, 72
    x, y = cx - w / 2, cy - h / 2
    pdf.setFillColor(white)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.6)
    pdf.roundRect(x, y, w, h, 8, stroke=1, fill=1)
    pdf.setFillColor(accent)  # top binding (rounded top only)
    p = pdf.beginPath()
    p.roundRect(x, y + h - 16, w, 16, 8)
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.rect(x, y + h - 16, w, 8, stroke=0, fill=1)
    pdf.setFillColor(white)  # rings
    pdf.circle(x + 18, y + h - 8, 4, fill=1, stroke=0)
    pdf.circle(x + w - 18, y + h - 8, 4, fill=1, stroke=0)
    pdf.setFillColor(dark)  # word
    pdf.setFont("Helvetica-Bold", 7.5)
    pdf.drawCentredString(cx, y + h - 31, word)
    ay = y + 19  # arrow
    pdf.setStrokeColor(dark)
    pdf.setFillColor(dark)
    pdf.setLineWidth(3)
    pdf.setLineCap(1)
    if arrow_dir == "left":
        pdf.line(cx + 13, ay, cx - 9, ay)
        p = pdf.beginPath()
        p.moveTo(cx - 17, ay)
        p.lineTo(cx - 7, ay + 6)
        p.lineTo(cx - 7, ay - 6)
        p.close()
    else:
        pdf.line(cx - 13, ay, cx + 9, ay)
        p = pdf.beginPath()
        p.moveTo(cx + 17, ay)
        p.lineTo(cx + 7, ay + 6)
        p.lineTo(cx + 7, ay - 6)
        p.close()
    pdf.drawPath(p, stroke=0, fill=1)


def _p2_sun_icon(pdf, cx, cy):
    """Original smiling sun with a TODAY tag underneath."""
    face_y = cy + 14
    pdf.setStrokeColor(HexColor("#F5A623"))
    pdf.setLineWidth(2.6)
    pdf.setLineCap(1)
    for k in range(8):
        a = math.pi / 4 * k + math.pi / 8
        pdf.line(cx + 28 * math.cos(a), face_y + 28 * math.sin(a),
                 cx + 34 * math.cos(a), face_y + 34 * math.sin(a))
    pdf.setFillColor(HexColor("#FFC93C"))
    pdf.circle(cx, face_y, 24, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#8A5A00"))  # eyes
    pdf.circle(cx - 8, face_y + 7, 2.8, fill=1, stroke=0)
    pdf.circle(cx + 8, face_y + 7, 2.8, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#F78FB3"))  # cheeks
    pdf.circle(cx - 14, face_y - 1, 3.2, fill=1, stroke=0)
    pdf.circle(cx + 14, face_y - 1, 3.2, fill=1, stroke=0)
    pdf.setStrokeColor(HexColor("#8A5A00"))  # smile
    pdf.setLineWidth(2.2)
    pdf.setLineCap(1)
    p = pdf.beginPath()
    p.arc(cx - 11, face_y - 9, cx + 11, face_y + 9, 200, 140)
    pdf.drawPath(p, stroke=1, fill=0)
    pdf.setFillColor(TEAL_ARROW)  # TODAY tag
    pdf.roundRect(cx - 33, cy - 34, 66, 20, 10, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(cx, cy - 27, "TODAY")


def draw_p2_panel(pdf, kind, label, fill_hex, border_hex, border_w, y):
    pdf.setFillColor(HexColor(fill_hex))
    pdf.setStrokeColor(HexColor(border_hex))
    pdf.setLineWidth(border_w)
    pdf.roundRect(P2_PANEL_X, y, P2_PANEL_W, P2_PANEL_H, 16,
                  stroke=1, fill=1)
    cy = y + P2_PANEL_H / 2
    ix = P2_PANEL_X + 72  # illustration center
    if kind == "yesterday":
        _p2_calendar_icon(pdf, ix, cy, "#E89B8B", "#D94F4F", "YESTERDAY",
                          "left")
    elif kind == "tomorrow":
        _p2_calendar_icon(pdf, ix, cy, "#9A8FE0", "#6A5FC0", "TOMORROW",
                          "right")
    else:
        _p2_sun_icon(pdf, ix, cy)
    pdf.setFillColor(NAVY)  # big label, centered between art and slot
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawCentredString(310, cy - 10, label)
    slot_w, slot_h = 92, 92  # dashed drop-zone slot for a day pill
    sx = P2_PANEL_X + P2_PANEL_W - 28 - slot_w
    pdf.setStrokeColor(CUT)
    pdf.setLineWidth(1.6)
    pdf.setDash(6, 4)
    pdf.roundRect(sx, cy - slot_h / 2, slot_w, slot_h, 14,
                  stroke=1, fill=0)
    pdf.setDash()


def draw_day_pill(pdf, day, fill_hex, border_hex, icon, x, y, w, h):
    """Day pill in Page 1's colors with its Page 1 icon; dashed border is
    the cut guide."""
    pdf.setFillColor(HexColor(fill_hex))
    pdf.setStrokeColor(HexColor(border_hex))
    pdf.setLineWidth(1.4)
    pdf.setDash(5, 3)
    pdf.roundRect(x, y, w, h, 14, stroke=1, fill=1)
    pdf.setDash()
    fit_font(pdf, day, "Helvetica-Bold", w - 8, start=12)
    pdf.setFillColor(NAVY)
    pdf.drawCentredString(x + w / 2, y + h - 21, day)
    ICONS[icon](pdf, x + w / 2, y + h / 2 - 9)


def draw_scissors(pdf, cx, cy):
    pdf.setStrokeColor(TEAL_ARROW)
    pdf.setLineWidth(1.8)
    pdf.setLineCap(1)
    pdf.circle(cx - 8, cy + 6, 4.2, stroke=1, fill=0)
    pdf.circle(cx - 8, cy - 6, 4.2, stroke=1, fill=0)
    pdf.line(cx - 4, cy + 4, cx + 10, cy - 8)
    pdf.line(cx - 4, cy - 4, cx + 10, cy + 8)
    pdf.setFillColor(TEAL_ARROW)
    pdf.circle(cx + 2, cy, 1.6, stroke=0, fill=1)


def build_yesterday_today_tomorrow_page(out_path):
    pdf = canvas.Canvas(out_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "My Calendar & Time: Yesterday, Today & Tomorrow",
                "Preschool \u00b7 Time & Sequence")
    draw_footer(pdf)

    # Child-facing instruction + activity cue.
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 628,
                          "Yesterday was before today. "
                          "Tomorrow comes after today.")
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 606,
                          "Put the right day in each space!")

    # Three illustrated panels with down-flow arrows between them.
    tops = [590, 590 - (P2_PANEL_H + P2_PANEL_GAP),
            590 - 2 * (P2_PANEL_H + P2_PANEL_GAP)]
    for (kind, label, fill, border, bw), top in zip(P2_PANELS, tops):
        draw_p2_panel(pdf, kind, label, fill, border, bw,
                      top - P2_PANEL_H)
    for top in tops[:2]:
        draw_v_arrow(pdf, 310, top - P2_PANEL_H - P2_PANEL_GAP / 2, 16,
                     "down", width=3.4, head=9)

    # Dashed cut-strip with the seven day pills (Page 1 colors + icons).
    strip_x, strip_w, strip_y, strip_h = 32, 548, 54, 130
    pdf.setStrokeColor(CUT)
    pdf.setLineWidth(1.4)
    pdf.setDash(7, 5)
    pdf.roundRect(strip_x, strip_y, strip_w, strip_h, 18,
                  stroke=1, fill=0)
    pdf.setDash()
    pdf.setFillColor(HexColor("#4A7A76"))
    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(PAGE_WIDTH / 2, strip_y + strip_h - 18,
                          "Cut out the days, or simply point to each one.")
    draw_scissors(pdf, strip_x + 24, strip_y + 58)
    pill_w, pill_h, pill_gap = 66, 84, 6
    px0 = 76
    py = strip_y + 16
    for i, (day, fill, border, icon) in enumerate(STRIP_DAYS):
        draw_day_pill(pdf, day, fill, border, icon,
                      px0 + i * (pill_w + pill_gap), py, pill_w, pill_h)

    pdf.showPage()
    pdf.save()



# ---------------------------------------------------------------------------
# Page 3: Months of the Year — 2 columns x 6 rows, all 12 months in order.
# Each panel: large bold month name (the dominant element, one consistent
# size fitted to "September"), small number badge (1-12), one cute original
# vector icon in a white chip (decorative memory cue only — no seasonal or
# holiday imagery), soft pastel fill from a 12-step spectrum. Below the
# grid: the cut-out "MY BIRTHDAY" star tag (or just point). The grid doubles
# as a displayable reference poster.
# ---------------------------------------------------------------------------

MONTHS = [
    ("January", "#FBD9D9", "drum"),
    ("February", "#FBE3CF", "balloon"),
    ("March", "#FBF0C8", "ball"),
    ("April", "#EAF7C9", "duck"),
    ("May", "#D7F5D3", "rocket"),
    ("June", "#CFF3E8", "fish"),
    ("July", "#CDEBFB", "cupcake"),
    ("August", "#D3DDFC", "star"),
    ("September", "#DFD4FB", "turtle"),
    ("October", "#EDCFF8", "owl"),
    ("November", "#F9CBE8", "teddy"),
    ("December", "#F5C9DA", "crown"),
]

M3_PANEL_W, M3_PANEL_H = 262, 62
M3_GAP_X, M3_GAP_Y = 12, 10


def _darken(hex_color, f=0.72):
    c = HexColor(hex_color)
    return Color(c.red * f, c.green * f, c.blue * f)


def m3_icon_drum(pdf, cx, cy):
    pdf.setFillColor(HexColor("#E86A6A"))
    pdf.setStrokeColor(HexColor("#C0392B"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(cx - 10, cy - 8, 20, 15, 3, stroke=1, fill=1)
    pdf.setFillColor(HexColor("#FFF7EE"))
    pdf.ellipse(cx - 10, cy + 5, cx + 10, cy + 12, stroke=1, fill=1)
    pdf.setStrokeColor(white)
    pdf.setLineWidth(1.6)
    pdf.line(cx - 3, cy - 7, cx - 3, cy + 6)
    pdf.line(cx + 3, cy - 7, cx + 3, cy + 6)


def m3_icon_balloon(pdf, cx, cy):
    pdf.setFillColor(HexColor("#FF8A80"))
    pdf.ellipse(cx - 8, cy - 4, cx + 8, cy + 16, stroke=0, fill=1)
    p = pdf.beginPath()
    p.moveTo(cx - 2.5, cy - 5)
    p.lineTo(cx + 2.5, cy - 5)
    p.lineTo(cx, cy - 8.5)
    p.close()
    pdf.setFillColor(HexColor("#E86A6A"))
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setStrokeColor(HexColor("#C96A5A"))
    pdf.setLineWidth(1.4)
    p = pdf.beginPath()
    p.moveTo(cx, cy - 8)
    p.curveTo(cx - 4, cy - 12, cx + 6, cy - 14, cx + 2, cy - 19)
    pdf.drawPath(p, stroke=1, fill=0)


def m3_icon_ball(pdf, cx, cy):
    pdf.saveState()
    p = pdf.beginPath()
    p.circle(cx, cy, 11)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.setFillColor(HexColor("#5FB4E8"))
    pdf.rect(cx - 11, cy - 11, 22, 22, stroke=0, fill=1)
    pdf.setStrokeColor(white)
    pdf.setLineWidth(5)
    q = pdf.beginPath()
    q.arc(cx - 11, cy - 6, cx + 11, cy + 10, 195, 150)
    pdf.drawPath(q, stroke=1, fill=0)
    pdf.restoreState()
    pdf.setStrokeColor(HexColor("#3A86C8"))
    pdf.setLineWidth(1.6)
    pdf.circle(cx, cy, 11, stroke=1, fill=0)


def m3_icon_duck(pdf, cx, cy):
    pdf.setFillColor(HexColor("#FFD93C"))
    pdf.ellipse(cx - 10, cy - 6, cx + 10, cy + 7, stroke=0, fill=1)
    pdf.circle(cx + 6, cy + 9, 7, stroke=0, fill=1)
    p = pdf.beginPath()
    p.moveTo(cx + 11, cy + 7)
    p.lineTo(cx + 11, cy + 11)
    p.lineTo(cx + 16.5, cy + 9)
    p.close()
    pdf.setFillColor(HexColor("#F58518"))
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#5A3A00"))
    pdf.circle(cx + 7, cy + 11, 1.6, stroke=0, fill=1)


def m3_icon_rocket(pdf, cx, cy):
    p = pdf.beginPath()
    p.moveTo(cx - 4, cy - 15)
    p.lineTo(cx + 4, cy - 15)
    p.lineTo(cx, cy - 8)
    p.close()
    pdf.setFillColor(HexColor("#F58518"))
    pdf.drawPath(p, stroke=0, fill=1)
    p = pdf.beginPath()
    p.moveTo(cx - 6, cy - 8)
    p.lineTo(cx - 11, cy - 14)
    p.lineTo(cx - 6, cy - 13)
    p.close()
    p2 = pdf.beginPath()
    p2.moveTo(cx + 6, cy - 8)
    p2.lineTo(cx + 11, cy - 14)
    p2.lineTo(cx + 6, cy - 13)
    p2.close()
    pdf.setFillColor(HexColor("#C0392B"))
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.drawPath(p2, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#F2F4F6"))
    pdf.setStrokeColor(HexColor("#B0B6BE"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(cx - 6, cy - 8, 12, 22, 5, stroke=1, fill=1)
    p = pdf.beginPath()
    p.moveTo(cx - 6, cy + 14)
    p.lineTo(cx + 6, cy + 14)
    p.lineTo(cx, cy + 20)
    p.close()
    pdf.setFillColor(HexColor("#E86A6A"))
    pdf.setStrokeColor(HexColor("#C0392B"))
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(HexColor("#7FB3E8"))
    pdf.setStrokeColor(HexColor("#5A7A9A"))
    pdf.setLineWidth(1.2)
    pdf.circle(cx, cy + 5, 3.4, stroke=1, fill=1)


def m3_icon_fish(pdf, cx, cy):
    p = pdf.beginPath()
    p.moveTo(cx - 9, cy)
    p.lineTo(cx - 17, cy + 6)
    p.lineTo(cx - 17, cy - 6)
    p.close()
    pdf.setFillColor(HexColor("#FF9E57"))
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#4DB6AC"))
    pdf.ellipse(cx - 9, cy - 6, cx + 10, cy + 6, stroke=0, fill=1)
    p = pdf.beginPath()
    p.moveTo(cx - 2, cy + 6)
    p.lineTo(cx + 3, cy + 6)
    p.lineTo(cx, cy + 10)
    p.close()
    pdf.setFillColor(HexColor("#3A9A90"))
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.circle(cx + 5, cy + 1, 2.6, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#23403D"))
    pdf.circle(cx + 5.5, cy + 1, 1.3, stroke=0, fill=1)


def m3_icon_cupcake(pdf, cx, cy):
    p = pdf.beginPath()
    p.moveTo(cx - 9, cy - 11)
    p.lineTo(cx + 9, cy - 11)
    p.lineTo(cx + 6, cy - 1)
    p.lineTo(cx - 6, cy - 1)
    p.close()
    pdf.setFillColor(HexColor("#C98A5A"))
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#F8A9C4"))
    pdf.circle(cx, cy + 3, 8, stroke=0, fill=1)
    pdf.circle(cx, cy + 9, 4.2, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#E84A5A"))
    pdf.circle(cx, cy + 12.5, 2.6, stroke=0, fill=1)
    pdf.setStrokeColor(HexColor("#7B61C9"))
    pdf.setLineWidth(1.4)
    pdf.setLineCap(1)
    pdf.line(cx - 4, cy + 4, cx - 1, cy + 6)
    pdf.setStrokeColor(HexColor("#4A90D9"))
    pdf.line(cx + 4, cy + 2, cx + 6, cy + 5)


def m3_icon_star(pdf, cx, cy):
    draw_star(pdf, cx, cy, 13, 6, HexColor("#FFC93C"), HexColor("#E8A020"))


def m3_icon_turtle(pdf, cx, cy):
    pdf.setFillColor(HexColor("#5AA85F"))
    pdf.circle(cx - 6, cy - 9, 2.5, stroke=0, fill=1)
    pdf.circle(cx + 5, cy - 9, 2.5, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#7BC47F"))
    p = pdf.beginPath()
    p.arc(cx - 11, cy - 8, cx + 11, cy + 4, 0, 180)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    pdf.circle(cx + 12, cy - 4, 4.5, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#23403D"))
    pdf.circle(cx + 13, cy - 3, 1.4, stroke=0, fill=1)


def m3_icon_owl(pdf, cx, cy):
    pdf.setFillColor(HexColor("#B08968"))
    for ex in (-6, 6):
        p = pdf.beginPath()
        p.moveTo(ex + cx - 3, cy + 9)
        p.lineTo(ex + cx, cy + 15)
        p.lineTo(ex + cx + 3, cy + 9)
        p.close()
        pdf.drawPath(p, stroke=0, fill=1)
    pdf.roundRect(cx - 10, cy - 11, 20, 23, 9, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#EAD9C2"))
    pdf.ellipse(cx - 6, cy - 9, cx + 6, cy + 3, stroke=0, fill=1)
    for ex in (-5, 5):
        pdf.setFillColor(white)
        pdf.circle(cx + ex, cy + 5, 4.2, stroke=0, fill=1)
        pdf.setFillColor(HexColor("#3A2A1A"))
        pdf.circle(cx + ex, cy + 5, 2, stroke=0, fill=1)
    p = pdf.beginPath()
    p.moveTo(cx - 2.2, cy + 1)
    p.lineTo(cx + 2.2, cy + 1)
    p.lineTo(cx, cy - 2)
    p.close()
    pdf.setFillColor(HexColor("#F58518"))
    pdf.drawPath(p, stroke=0, fill=1)


def m3_icon_teddy(pdf, cx, cy):
    pdf.setFillColor(HexColor("#A0714F"))
    pdf.circle(cx - 8, cy + 8, 4.2, stroke=0, fill=1)
    pdf.circle(cx + 8, cy + 8, 4.2, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#B08968"))
    pdf.circle(cx, cy + 1, 9.5, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#EAD9C2"))
    pdf.ellipse(cx - 4.5, cy - 4, cx + 4.5, cy + 2, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#5A3A22"))
    pdf.circle(cx - 3.5, cy + 4, 1.6, stroke=0, fill=1)
    pdf.circle(cx + 3.5, cy + 4, 1.6, stroke=0, fill=1)
    pdf.circle(cx, cy - 2, 1.8, stroke=0, fill=1)


def m3_icon_crown(pdf, cx, cy):
    p = pdf.beginPath()
    p.moveTo(cx - 11, cy - 7)
    p.lineTo(cx - 11, cy + 1)
    p.lineTo(cx - 6, cy - 3)
    p.lineTo(cx, cy + 5)
    p.lineTo(cx + 6, cy - 3)
    p.lineTo(cx + 11, cy + 1)
    p.lineTo(cx + 11, cy - 7)
    p.close()
    pdf.setFillColor(HexColor("#FFC93C"))
    pdf.setStrokeColor(HexColor("#E8A020"))
    pdf.setLineWidth(1.4)
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(HexColor("#E84A5A"))
    pdf.circle(cx, cy - 3, 2, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#4A90D9"))
    pdf.circle(cx - 6, cy - 4, 2, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#4CAF50"))
    pdf.circle(cx + 6, cy - 4, 2, stroke=0, fill=1)


M3_ICONS = {
    "drum": m3_icon_drum, "balloon": m3_icon_balloon, "ball": m3_icon_ball,
    "duck": m3_icon_duck, "rocket": m3_icon_rocket, "fish": m3_icon_fish,
    "cupcake": m3_icon_cupcake, "star": m3_icon_star,
    "turtle": m3_icon_turtle, "owl": m3_icon_owl, "teddy": m3_icon_teddy,
    "crown": m3_icon_crown,
}


def draw_month_panel(pdf, name, num, fill_hex, icon_fn, x, y, font_size):
    border = _darken(fill_hex)
    pdf.setFillColor(HexColor(fill_hex))
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.6)
    pdf.roundRect(x, y, M3_PANEL_W, M3_PANEL_H, 14, stroke=1, fill=1)
    # Small decorative icon chip (secondary to the name).
    pdf.setFillColor(white)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.2)
    pdf.roundRect(x + 12, y + 11, 40, 40, 10, stroke=1, fill=1)
    icon_fn(pdf, x + 32, y + 31)
    # Month name dominates, one consistent size.
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawCentredString(x + 146, y + 31 - font_size * 0.35, name)
    # Number badge (1-12).
    bx, by = x + M3_PANEL_W - 22, y + M3_PANEL_H - 20
    pdf.setFillColor(border)
    pdf.circle(bx, by, 11, stroke=0, fill=1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(bx, by - 3.5, str(num))


def draw_birthday_star(pdf):
    tw, th = 190, 42
    tx, ty = (PAGE_WIDTH - tw) / 2, 100
    pdf.setStrokeColor(CUT)
    pdf.setLineWidth(1.4)
    pdf.setDash(6, 4)
    pdf.roundRect(tx - 10, ty - 10, tw + 20, th + 20, 16,
                  stroke=1, fill=0)
    pdf.setDash()
    pdf.setFillColor(HexColor("#FFC93C"))
    pdf.setStrokeColor(HexColor("#E8A020"))
    pdf.setLineWidth(1.6)
    pdf.roundRect(tx, ty, tw, th, 20, stroke=1, fill=1)
    draw_star(pdf, tx + 30, ty + th / 2, 13, 6, HexColor("#FFF3D6"),
              HexColor("#E8A020"))
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(tx + 108, ty + th / 2 - 5, "MY BIRTHDAY")


def build_months_page(out_path):
    pdf = canvas.Canvas(out_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "My Calendar & Time: Months of the Year",
                "Preschool \u00b7 Time & Sequence")
    draw_footer(pdf)

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 626, "A year has 12 months!")
    pdf.setFont("Helvetica-Bold", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 604,
                          "Find your birthday month. Put the star on it!")

    # Largest consistent name size that safely fits "September".
    font_size = 30
    pdf.setFont("Helvetica-Bold", font_size)
    while (pdf.stringWidth("September", "Helvetica-Bold", font_size) > 168
           and font_size > 10):
        font_size -= 1

    for i, (name, fill, icon_key) in enumerate(MONTHS):
        row, col = divmod(i, 2)
        x = 38 + col * (M3_PANEL_W + M3_GAP_X)
        y = 584 - M3_PANEL_H - row * (M3_PANEL_H + M3_GAP_Y)
        draw_month_panel(pdf, name, i + 1, fill, M3_ICONS[icon_key], x, y,
                         font_size)

    draw_birthday_star(pdf)
    pdf.setFillColor(HexColor("#4A7A76"))
    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(PAGE_WIDTH / 2, 78,
                          "Cut out the star, or just point!")

    pdf.showPage()
    pdf.save()



# ---------------------------------------------------------------------------
# Page 4: Seasons of the Year
# ---------------------------------------------------------------------------
# Four large panels in a 2x2 reading-order grid (Spring, Summer / Fall,
# Winter), each with one large original hero illustration showing that
# season's unmistakable signs.  A circular "round and round" arrow badge
# sits in the centre of the grid (drawn over the gap as a deliberate seal)
# to teach cyclical time without dominating the page.  The activity is
# observation ("Look outside. What season is it? Point to it!") plus a
# cut-out THIS SEASON marker tag that moves four times a year.
# ---------------------------------------------------------------------------

S4_SPRING = "Spring"
S4_SUMMER = "Summer"
S4_FALL = "Fall"
S4_WINTER = "Winter"

S4_PANELS = [
    # (name, fill, border)
    (S4_SPRING, "#DFF5DC", "#8FCB8A"),
    (S4_SUMMER, "#FFF4C8", "#EAD483"),
    (S4_FALL,   "#FFE8D2", "#E8A86A"),
    (S4_WINTER, "#DDEAFB", "#9FBFDF"),
]

S4_PANEL_W = 252
S4_PANEL_H = 200
S4_GAP_X = 28
S4_GAP_Y = 28
S4_XS = [38, 38 + S4_PANEL_W + S4_GAP_X]
S4_TOPS = [588, 588 - S4_PANEL_H - S4_GAP_Y]


def s4_spring_tree(pdf, cx, cy):
    """Blossom tree: brown trunk, pink blossom clusters, grass, 3 flowers."""
    pdf.setLineWidth(1)
    # grass mound
    pdf.setFillColor(HexColor("#7BC47F"))
    pdf.setStrokeColor(HexColor("#7BC47F"))
    pdf.ellipse(cx - 58, cy - 66, cx + 58, cy - 38, stroke=0, fill=1)
    # trunk (tapered polygon)
    pdf.setFillColor(HexColor("#A0714F"))
    pdf.setStrokeColor(HexColor("#A0714F"))
    p = pdf.beginPath()
    p.moveTo(cx - 8, cy - 56)
    p.lineTo(cx + 8, cy - 56)
    p.lineTo(cx + 5, cy - 8)
    p.lineTo(cx - 5, cy - 8)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    # branches
    pdf.setStrokeColor(HexColor("#A0714F"))
    pdf.setLineWidth(4)
    pdf.setLineCap(1)
    pdf.line(cx - 2, cy - 22, cx - 24, cy + 0)
    pdf.line(cx + 2, cy - 16, cx + 25, cy + 8)
    # blossom clusters
    clusters = [
        (cx - 28, cy + 16, 17, "#F8A9C4"),
        (cx + 28, cy + 16, 17, "#F8A9C4"),
        (cx, cy + 30, 19, "#F5BFD4"),
        (cx - 15, cy + 40, 15, "#F9D3E3"),
        (cx + 15, cy + 40, 15, "#F9D3E3"),
        (cx, cy + 12, 15, "#F8A9C4"),
    ]
    pdf.setLineWidth(1)
    for bx, by, r, col in clusters:
        pdf.setFillColor(HexColor(col))
        pdf.setStrokeColor(HexColor("#E58BAE"))
        pdf.circle(bx, by, r, stroke=1, fill=1)
    # 3 little flowers on the grass
    for fx, fcol in [(cx - 40, "#E84A5A"), (cx + 32, "#FFC93C"),
                     (cx + 6, "#B678E8")]:
        pdf.setStrokeColor(HexColor("#4E9A51"))
        pdf.setLineWidth(2.2)
        pdf.line(fx, cy - 52, fx, cy - 38)
        pdf.setFillColor(HexColor(fcol))
        pdf.setStrokeColor(HexColor(fcol))
        pdf.circle(fx, cy - 34, 5, stroke=0, fill=1)


def s4_summer_sun(pdf, cx, cy):
    """Big smiling sun wearing sunglasses."""
    # rays
    pdf.setStrokeColor(HexColor("#F5A623"))
    pdf.setLineWidth(5)
    pdf.setLineCap(1)
    for k in range(12):
        a = math.radians(k * 30)
        pdf.line(cx + 46 * math.cos(a), cy + 46 * math.sin(a),
                 cx + 58 * math.cos(a), cy + 58 * math.sin(a))
    # face
    pdf.setFillColor(HexColor("#FFC93C"))
    pdf.setStrokeColor(HexColor("#E8A020"))
    pdf.setLineWidth(2)
    pdf.circle(cx, cy, 44, stroke=1, fill=1)
    # sunglasses
    pdf.setFillColor(HexColor("#3A3A3A"))
    pdf.setStrokeColor(HexColor("#3A3A3A"))
    pdf.roundRect(cx - 32, cy - 4, 27, 21, 9, stroke=0, fill=1)
    pdf.roundRect(cx + 5, cy - 4, 27, 21, 9, stroke=0, fill=1)
    pdf.setLineWidth(4)
    pdf.line(cx - 5, cy + 5, cx + 5, cy + 5)
    # shine on left lens
    pdf.setStrokeColor(HexColor("#FFFFFF"))
    pdf.setLineWidth(2.5)
    pdf.line(cx - 26, cy + 8, cx - 18, cy - 1)
    # smile below the glasses
    pdf.setStrokeColor(HexColor("#7A4A12"))
    pdf.setLineWidth(3)
    p = pdf.beginPath()
    p.arc(cx - 15, cy - 26, cx + 15, cy - 8, 200, 340)
    pdf.drawPath(p, stroke=1, fill=0)


def s4_fall_tree(pdf, cx, cy):
    """Leaf tree in fall colours, leaves drifting down."""
    pdf.setLineWidth(1)
    # ground mound
    pdf.setFillColor(HexColor("#EBCB90"))
    pdf.setStrokeColor(HexColor("#EBCB90"))
    pdf.ellipse(cx - 58, cy - 66, cx + 58, cy - 40, stroke=0, fill=1)
    # trunk
    pdf.setFillColor(HexColor("#A0714F"))
    pdf.setStrokeColor(HexColor("#A0714F"))
    p = pdf.beginPath()
    p.moveTo(cx - 8, cy - 56)
    p.lineTo(cx + 8, cy - 56)
    p.lineTo(cx + 5, cy - 8)
    p.lineTo(cx - 5, cy - 8)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)
    # branches
    pdf.setLineWidth(4)
    pdf.setLineCap(1)
    pdf.line(cx - 2, cy - 22, cx - 24, cy + 0)
    pdf.line(cx + 2, cy - 16, cx + 25, cy + 8)
    # autumn canopy
    clusters = [
        (cx - 28, cy + 16, 17, "#F58518"),
        (cx + 28, cy + 16, 17, "#E84A5A"),
        (cx, cy + 30, 19, "#FFC93C"),
        (cx - 15, cy + 40, 15, "#E8A020"),
        (cx + 15, cy + 40, 15, "#F58518"),
        (cx, cy + 12, 15, "#E84A5A"),
    ]
    pdf.setLineWidth(1)
    for bx, by, r, col in clusters:
        pdf.setFillColor(HexColor(col))
        pdf.setStrokeColor(HexColor("#C96A2A"))
        pdf.circle(bx, by, r, stroke=1, fill=1)
    # falling leaves (small rotated ellipses with stems)
    for lx, ly, col, rot in [(cx - 42, cy - 22, "#F58518", 35),
                             (cx + 40, cy - 32, "#E84A5A", -30),
                             (cx - 22, cy - 40, "#FFC93C", 60),
                             (cx + 26, cy - 10, "#E8A020", -55)]:
        pdf.saveState()
        pdf.translate(lx, ly)
        pdf.rotate(rot)
        pdf.setFillColor(HexColor(col))
        pdf.setStrokeColor(HexColor(col))
        pdf.ellipse(-6, -3.5, 6, 3.5, stroke=0, fill=1)
        pdf.restoreState()


def s4_winter_snowman(pdf, cx, cy):
    """Cheerful snowman with scarf, stick arms, falling snowflakes."""
    pdf.setLineWidth(1.5)
    # snowy ground
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(HexColor("#BFD9EA"))
    pdf.ellipse(cx - 60, cy - 68, cx + 60, cy - 38, stroke=1, fill=1)
    # body balls (bottom -> top)
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(HexColor("#BFD9EA"))
    pdf.circle(cx, cy - 28, 30, stroke=1, fill=1)
    pdf.circle(cx, cy + 12, 21, stroke=1, fill=1)
    pdf.circle(cx, cy + 42, 14, stroke=1, fill=1)
    # stick arms
    pdf.setStrokeColor(HexColor("#A0714F"))
    pdf.setLineWidth(3)
    pdf.setLineCap(1)
    pdf.line(cx - 19, cy + 14, cx - 36, cy + 26)
    pdf.line(cx + 19, cy + 14, cx + 36, cy + 26)
    # scarf
    pdf.setFillColor(HexColor("#E84A5A"))
    pdf.setStrokeColor(HexColor("#E84A5A"))
    pdf.roundRect(cx - 17, cy + 26, 34, 9, 4, stroke=0, fill=1)
    pdf.roundRect(cx + 6, cy + 10, 8, 18, 4, stroke=0, fill=1)
    # face
    pdf.setFillColor(HexColor("#3A3A3A"))
    pdf.setStrokeColor(HexColor("#3A3A3A"))
    pdf.circle(cx - 5, cy + 46, 2.2, stroke=0, fill=1)
    pdf.circle(cx + 5, cy + 46, 2.2, stroke=0, fill=1)
    pdf.setLineWidth(2.5)
    p = pdf.beginPath()
    p.arc(cx - 7, cy + 34, cx + 7, cy + 44, 200, 340)
    pdf.drawPath(p, stroke=1, fill=0)
    # carrot nose
    pdf.setFillColor(HexColor("#F58518"))
    pdf.setStrokeColor(HexColor("#F58518"))
    q = pdf.beginPath()
    q.moveTo(cx, cy + 42)
    q.lineTo(cx, cy + 38)
    q.lineTo(cx + 11, cy + 40)
    q.close()
    pdf.drawPath(q, stroke=0, fill=1)
    # buttons
    pdf.setFillColor(HexColor("#3A3A3A"))
    pdf.setStrokeColor(HexColor("#3A3A3A"))
    pdf.circle(cx, cy + 16, 2.4, stroke=0, fill=1)
    pdf.circle(cx, cy + 6, 2.4, stroke=0, fill=1)
    # falling snowflakes (3-line asterisks)
    pdf.setStrokeColor(HexColor("#9FC3E0"))
    pdf.setLineWidth(1.8)
    for fx, fy in [(cx - 48, cy + 20), (cx + 50, cy + 28), (cx - 38, cy + 48),
                   (cx + 42, cy - 8), (cx - 8, cy + 62), (cx + 24, cy + 58)]:
        pdf.line(fx - 5, fy, fx + 5, fy)
        pdf.line(fx - 2.5, fy - 4.3, fx + 2.5, fy + 4.3)
        pdf.line(fx + 2.5, fy - 4.3, fx - 2.5, fy + 4.3)


S4_ICONS = {
    S4_SPRING: s4_spring_tree,
    S4_SUMMER: s4_summer_sun,
    S4_FALL: s4_fall_tree,
    S4_WINTER: s4_winter_snowman,
}


def draw_season_panel(pdf, name, fill_hex, border_hex, x, y):
    """One large season panel: big name at top, hero illustration below."""
    w, h = S4_PANEL_W, S4_PANEL_H
    pdf.setFillColor(HexColor(fill_hex))
    pdf.setStrokeColor(HexColor(border_hex))
    pdf.setLineWidth(2.5)
    pdf.roundRect(x, y, w, h, 16, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(x + w / 2, y + h - 40, name)
    S4_ICONS[name](pdf, x + w / 2, y + 80)


def draw_cycle_badge(pdf, cx, cy):
    """White seal with a teal circular arrow: seasons go round and round."""
    pdf.setFillColor(HexColor("#FFFFFF"))
    pdf.setStrokeColor(HexColor("#D8E2E0"))
    pdf.setLineWidth(1.5)
    pdf.circle(cx, cy, 30, stroke=1, fill=1)
    # circular arrow (300-degree sweep, arrowhead at the end)
    r = 19
    start = -60.0
    sweep = 300.0
    pdf.setStrokeColor(HexColor("#0E7C7B"))
    pdf.setLineWidth(4.5)
    pdf.setLineCap(1)
    p = pdf.beginPath()
    p.arc(cx - r, cy - r, cx + r, cy + r, start, sweep)
    pdf.drawPath(p, stroke=1, fill=0)
    end = math.radians(start + sweep)
    ex, ey = cx + r * math.cos(end), cy + r * math.sin(end)
    # tangent in direction of travel (increasing angle)
    tx, ty = -math.sin(end), math.cos(end)
    nx, ny = math.cos(end), math.sin(end)
    tipx, tipy = ex + 9 * tx, ey + 9 * ty
    bx, by = ex - 5 * tx, ey - 5 * ty
    pdf.setFillColor(HexColor("#0E7C7B"))
    pdf.setStrokeColor(HexColor("#0E7C7B"))
    q = pdf.beginPath()
    q.moveTo(tipx, tipy)
    q.lineTo(bx + 6 * nx, by + 6 * ny)
    q.lineTo(bx - 6 * nx, by - 6 * ny)
    q.close()
    pdf.drawPath(q, stroke=0, fill=1)


def draw_this_season_tag(pdf, cx, ty):
    """Gold THIS SEASON cut-out marker tag with a dashed cut guide."""
    tw, th = 196, 42
    tx = cx - tw / 2
    pdf.setStrokeColor(HexColor("#B9C4C2"))
    pdf.setLineWidth(1.2)
    pdf.setDash(4, 3)
    pdf.roundRect(tx - 7, ty - 7, tw + 14, th + 14, 10, stroke=1, fill=0)
    pdf.setDash()
    pdf.setFillColor(HexColor("#FFC93C"))
    pdf.setStrokeColor(HexColor("#E8A020"))
    pdf.setLineWidth(1.6)
    pdf.roundRect(tx, ty, tw, th, 10, stroke=1, fill=1)
    draw_star(pdf, tx + 30, ty + th / 2, 13, 6, HexColor("#FFF3D6"),
              HexColor("#E8A020"))
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(tx + tw / 2 + 12, ty + 15.5, "THIS SEASON")


def build_seasons_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "My Calendar & Time", "Seasons of the Year")
    # instruction lines
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 628,
                          "There are 4 seasons. They go round and round!")
    pdf.setFont("Helvetica", 13.5)
    pdf.drawCentredString(PAGE_WIDTH / 2, 606,
                          "Look outside. What season is it? Point to it!")
    # four season panels, reading order (draw_season_panel takes the bottom y)
    k = 0
    for row in range(2):
        for col in range(2):
            name, fill_hex, border_hex = S4_PANELS[k]
            draw_season_panel(pdf, name, fill_hex, border_hex,
                              S4_XS[col], S4_TOPS[row] - S4_PANEL_H)
            k += 1
    # cycle badge at the centre of the grid
    draw_cycle_badge(pdf, 38 + S4_PANEL_W + S4_GAP_X / 2, S4_TOPS[1] + 14)
    # THIS SEASON marker tag
    draw_this_season_tag(pdf, PAGE_WIDTH / 2, 94)
    pdf.setFillColor(HexColor("#8A9492"))
    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawCentredString(PAGE_WIDTH / 2, 68,
                          "Cut out the marker, or just point!")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    # (title, builder, locked)
    ("Days of the Week", build_days_page, True),
    ("Yesterday, Today & Tomorrow", build_yesterday_today_tomorrow_page,
     True),
    ("Months of the Year", build_months_page, True),
    ("Seasons of the Year", build_seasons_page, False),
]


def main():
    tmpdir = tempfile.mkdtemp(prefix="ct-")
    if not os.path.exists(OUT):
        # First build: render every page fresh.
        ordered = []
        for k, (title, builder, _locked) in enumerate(PAGES):
            p = os.path.join(tmpdir, f"page-{k}.pdf")
            builder(p)
            ordered.append(p)
            print(f"built page: {title} -> {p}")
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        subprocess.run(["pdfunite", *ordered, OUT], check=True)
        print(f"built {len(ordered)} page(s) -> {OUT}")
        return
    # Split the existing prototype so locked pages can be reused as-is.
    splitdir = tempfile.mkdtemp(prefix="ct-split-")
    subprocess.run(["pdfseparate", OUT, os.path.join(splitdir, "p-%d.pdf")],
                   check=True)
    n_existing = len([f for f in os.listdir(splitdir) if f.endswith(".pdf")])
    n_locked = sum(1 for _, _, locked in PAGES if locked)
    n_new = sum(1 for _, _, locked in PAGES if not locked)
    # Locked PAGES entries correspond, in order, to the first n_locked pages
    # of the existing prototype; any remaining prototype pages are old
    # versions of unlocked pages being rebuilt (or new pages appended).
    if not (n_locked <= n_existing <= len(PAGES)):
        raise SystemExit(
            f"page mismatch: prototype has {n_existing} pages, "
            f"{n_locked} locked / {len(PAGES)} total pages configured")
    ordered = []
    li = 0
    for k, (title, builder, locked) in enumerate(PAGES):
        if locked:
            li += 1
            ordered.append(os.path.join(splitdir, f"p-{li}.pdf"))
        else:
            p = os.path.join(tmpdir, f"newpage-{k}.pdf")
            builder(p)
            ordered.append(p)
            print(f"rebuilt page: {title} -> {p}")
    merged = OUT + ".new"
    subprocess.run(["pdfunite", *ordered, merged], check=True)
    os.replace(merged, OUT)
    print(f"merged {len(ordered)} page(s) ({n_locked} locked, {n_new} "
          f"rebuilt) -> {OUT}")


if __name__ == "__main__":
    main()
