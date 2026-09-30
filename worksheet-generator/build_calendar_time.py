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
# Page 1: Days of the Week
# ---------------------------------------------------------------------------

DAYS = [
    ("Sunday", "#FFE1E1", "#F0B9B9"),
    ("Monday", "#FFE9CF", "#F2C795"),
    ("Tuesday", "#FFF4C7", "#EBD68F"),
    ("Wednesday", "#DFF3DA", "#AED8A8"),
    ("Thursday", "#D8EFEB", "#9FD0C9"),
    ("Friday", "#DDEAFF", "#A9C6F2"),
    ("Saturday", "#E9DFFF", "#C3B2EE"),
]

CARD_W, CARD_H = 124, 104
ROW_GAP_X = 18


def fit_font(pdf, text, font, max_w, start=30, min_size=14):
    size = start
    pdf.setFont(font, size)
    while pdf.stringWidth(text, font, size) > max_w and size > min_size:
        size -= 1
        pdf.setFont(font, size)
    return size


def draw_day_card(pdf, day, fill_hex, border_hex, x, y):
    pdf.setFillColor(HexColor(fill_hex))
    pdf.setStrokeColor(HexColor(border_hex))
    pdf.setLineWidth(2)
    pdf.roundRect(x, y, CARD_W, CARD_H, 16, stroke=1, fill=1)
    fit_font(pdf, day, "Helvetica-Bold", CARD_W - 16, start=30)
    pdf.setFillColor(NAVY)
    pdf.drawCentredString(x + CARD_W / 2, y + CARD_H / 2 - 11, day)


def build_days_page(out_path):
    pdf = canvas.Canvas(out_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "My Calendar & Time: Days of the Week",
                "Preschool \u00b7 Time & Sequence")
    draw_footer(pdf)

    # Child-facing instruction.
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawCentredString(PAGE_WIDTH / 2, 624,
                          "Say each day. Put the star on today!")

    # Row 1: Sunday..Wednesday. Row 2: Thursday..Saturday.
    row1_top, row2_top = 585, 415
    row1 = DAYS[:4]
    row2 = DAYS[4:]
    xs1 = [(PAGE_WIDTH - (4 * CARD_W + 3 * ROW_GAP_X)) / 2
           + i * (CARD_W + ROW_GAP_X) for i in range(4)]
    xs2 = [(PAGE_WIDTH - (3 * CARD_W + 2 * ROW_GAP_X)) / 2
           + i * (CARD_W + ROW_GAP_X) for i in range(3)]

    for (day, fill, border), x in zip(row1, xs1):
        draw_day_card(pdf, day, fill, border, x, row1_top - CARD_H)
    for (day, fill, border), x in zip(row2, xs2):
        draw_day_card(pdf, day, fill, border, x, row2_top - CARD_H)

    # Arrows between cards within each row.
    mid1 = row1_top - CARD_H / 2
    mid2 = row2_top - CARD_H / 2
    for i in range(3):
        draw_h_arrow(pdf, xs1[i] + CARD_W + ROW_GAP_X / 2, mid1, 12)
    for i in range(2):
        draw_h_arrow(pdf, xs2[i] + CARD_W + ROW_GAP_X / 2, mid2, 12)

    # Return arrow: the week continues on the next row. Elbow in the right
    # margin from Wednesday's right edge down to row-2 height, arrowhead
    # pointing left toward the second row.
    ex = xs1[3] + CARD_W  # Wednesday right edge
    ax = PAGE_WIDTH - 20  # elbow x in the right margin
    pdf.setStrokeColor(TEAL_ARROW)
    pdf.setLineWidth(2.6)
    pdf.setLineCap(1)
    pdf.line(ex, mid1, ax, mid1)
    pdf.line(ax, mid1, ax, mid2)
    pdf.setFillColor(TEAL_ARROW)
    p = pdf.beginPath()
    p.moveTo(ax - 13, mid2)
    p.lineTo(ax - 4, mid2 + 5.5)
    p.lineTo(ax - 4, mid2 - 5.5)
    p.close()
    pdf.drawPath(p, stroke=0, fill=1)

    # TODAY star: optional cut-out. Dashed panel doubles as the cut guide;
    # the page works fine printed as-is without cutting.
    panel_w, panel_h = 150, 128
    px = (PAGE_WIDTH - panel_w) / 2
    py = 122
    pdf.setStrokeColor(CUT)
    pdf.setLineWidth(1.4)
    pdf.setDash(6, 4)
    pdf.roundRect(px, py, panel_w, panel_h, 14, stroke=1, fill=0)
    pdf.setDash()
    # Chunky star so the TODAY label sits comfortably inside it.
    star_cy = py + panel_h / 2
    draw_star(pdf, px + panel_w / 2, star_cy, 46, 26, stroke=TEAL_ARROW)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(px + panel_w / 2, star_cy - 5, "TODAY")

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
