#!/usr/bin/env python3
"""My Calendar & Time — Preschool Thinking & Our World: Time & Sequence.

An academic calendar pack (not a visual-support schedule): the calendar
concepts are the visual focus. Children appear only where they genuinely
improve understanding. Reusable/cut-apart elements are an optional bonus —
every page must make sense and provide value when simply printed.

Page 1 (this build): Days of the Week — seven large, cheerful, highly
readable day cards in an obvious sequence (two rows with arrows and a
return arrow), plus an optional cut-out TODAY star. Day names dominate;
no decorative clip art competes with the words.

Per-page builders follow; PAGES controls the lock/merge scaffold (locked
pages are carried forward byte-identical from the prototype).
"""
import math
import os
import subprocess
import tempfile

from reportlab.lib.colors import HexColor, white
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



PAGES = [
    # (title, builder, locked)
    ("Days of the Week", build_days_page, False),
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
