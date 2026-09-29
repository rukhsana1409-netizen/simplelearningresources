#!/usr/bin/env python3
"""My Daily Routines — Preschool Visual Supports & Routines.

Practical printable visual-support pack (not a worksheet). Each page shows
one routine as a clear visual sequence of large step cards in a spacious
grid with numbers and arrows. Every card is self-contained (number badge +
illustration + short label) so it also works as an individual visual card
if cut apart; card borders double as subtle cut guides.

Page 1 (this build): Brush, Wash & Get Ready (8 steps, 4x2 grid).
"""
import os

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
TEAL_ARROW = HexColor("#0E7C7B")
GOLD = HexColor("#F4B63E")
INK = HexColor("#202A33")
NAVY = HexColor("#1E3A5F")
CUT = HexColor("#C9D6D3")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "daily-routines")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "communication",
                   "visual-supports-routines", "my-daily-routines-prototype.pdf")


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


def draw_header(pdf, title, subtitle, compact=False):
    """Established brand header (Learn My Letters style): teal top strip,
    vector logo + wordmark, divider, two-line teal title, teal rule.
    The compact variant is slightly shorter to give 8-step pages room."""
    strip = 12 if compact else 14
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - strip, PAGE_WIDTH, strip, fill=1, stroke=0)
    draw_logo(pdf, MARGIN, PAGE_HEIGHT - (78 if compact else 86))
    divider_x = 210
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1)
    if compact:
        pdf.line(divider_x, PAGE_HEIGHT - 42, divider_x, PAGE_HEIGHT - 96)
    else:
        pdf.line(divider_x, PAGE_HEIGHT - 46, divider_x, PAGE_HEIGHT - 106)
    title_x = divider_x + 19
    if ": " in title:
        prefix, focus = title.split(": ", 1)
    else:
        prefix, focus = "", title
    if prefix:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 20 if compact else 22)
        pdf.drawString(title_x, PAGE_HEIGHT - (60 if compact else 67),
                       prefix + ":")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 28 if compact else 30)
    pdf.drawString(title_x, PAGE_HEIGHT - (88 if compact else 98), focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11 if compact else 11.5)
    pdf.drawString(title_x, PAGE_HEIGHT - (104 if compact else 116),
                   subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    rule_y = PAGE_HEIGHT - (116 if compact else 131)
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


def draw_step_image(pdf, stem, x, y, w, h, r=12, fx=0.5):
    """One step illustration, aspect-filled into a rounded rect. fx biases
    the horizontal crop focus (0.5 = centered)."""
    path = os.path.join(ASSETS, stem + ".png")
    # Downscale photographic embeds via PIL before embedding: keeps the
    # prototype PDF under GitHub's ~35MB blob limit while staying crisp
    # in print (1100px across a ~3in card image ≈ 340 DPI). Locked pages
    # are never rebuilt, so this cannot alter them.
    import io as _io
    with Image.open(path) as _im:
        _im = _im.convert("RGB")
        if _im.width > 1100:
            _im = _im.resize((1100, int(_im.height * 1100 / _im.width)),
                             Image.LANCZOS)
        _buf = _io.BytesIO()
        _im.save(_buf, "JPEG", quality=88)
        _buf.seek(0)
        iw, ih = _im.size
    img = ImageReader(_buf)
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx = x + (w - dw) * fx
    dy = y + (h - dh) / 2
    pdf.saveState()
    p = pdf.beginPath()
    p.roundRect(x, y, w, h, r)
    pdf.clipPath(p, stroke=0, fill=0)
    pdf.drawImage(img, dx, dy, dw, dh, preserveAspectRatio=False,
                  mask="auto")
    pdf.restoreState()


# Layouts keyed by step count. 8-step pages use a 4x2 grid; 5/6-step
# pages use the 2-column layout (5-step centers its final card).
LAYOUTS = {
    8: dict(cols=4, card_w=126, card_h=272, col_gap=16, row_gap=28,
            grid_top=664, margin=30, label_pt=14, label_dy=15,
            img_pad_top=30, img_h=196, badge_r=14, badge_pt=17,
            arrow_s=0.7, compact_header=True),
    7: dict(cols=4, card_w=126, card_h=272, col_gap=16, row_gap=28,
            grid_top=664, margin=30, label_pt=14, label_dy=15,
            img_pad_top=30, img_h=196, badge_r=14, badge_pt=17,
            arrow_s=0.7, compact_header=True),
    6: dict(cols=2, card_w=252, card_h=172, col_gap=28, row_gap=22,
            grid_top=636, margin=40, label_pt=15, label_dy=15,
            img_pad_top=26, img_h=106, badge_r=15, badge_pt=19,
            arrow_s=1.0, compact_header=False),
    5: dict(cols=2, card_w=252, card_h=172, col_gap=28, row_gap=22,
            grid_top=636, margin=40, label_pt=15, label_dy=15,
            img_pad_top=26, img_h=106, badge_r=15, badge_pt=19,
            arrow_s=1.0, compact_header=False),
}


def card_pos(i, n, L):
    """Top-left (x, top_y) of step card i (0-based). The final card of a
    5-step page is centered for balance, as is the 3-card second row of a
    7-step page; card size never changes."""
    cols = L["cols"]
    if n == 5 and cols == 2 and i == 4:
        x = (PAGE_WIDTH - L["card_w"]) / 2
    elif n == 7 and cols == 4 and i >= 4:
        row_w = 3 * L["card_w"] + 2 * L["col_gap"]
        x = (PAGE_WIDTH - row_w) / 2 + (i - 4) * (L["card_w"] + L["col_gap"])
    else:
        x = L["margin"] + (i % cols) * (L["card_w"] + L["col_gap"])
    top = L["grid_top"] - (i // cols) * (L["card_h"] + L["row_gap"])
    return x, top


def draw_card(pdf, i, label, stem, n, L, fx=0.5, badge=True):
    x, top = card_pos(i, n, L)
    cw, ch = L["card_w"], L["card_h"]
    y = top - ch
    # card body; dashed border doubles as a subtle cut guide
    pdf.setFillColor(white)
    pdf.setStrokeColor(CUT)
    pdf.setLineWidth(1.2)
    pdf.setDash(6, 4)
    p = pdf.beginPath()
    p.roundRect(x, y, cw, ch, 12)
    pdf.drawPath(p, fill=1, stroke=1)
    pdf.setDash()
    # illustration
    ix, iw = x + 10, cw - 20
    itop, ih = top - L["img_pad_top"], L["img_h"]
    draw_step_image(pdf, stem, ix, itop - ih, iw, ih, fx=fx)
    # number badge overlapping the illustration's top-left corner
    if badge:
        br = L["badge_r"]
        bx, by = x + 10 + br + 2, itop
        pdf.setFillColor(TEAL)
        pdf.circle(bx, by, br, fill=1, stroke=0)
        pdf.setFillColor(white)
        pdf.setFont("Helvetica-Bold", L["badge_pt"])
        pdf.drawCentredString(bx, by - L["badge_pt"] * 0.34, str(i + 1))
    # short label
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", L["label_pt"])
    pdf.drawCentredString(x + cw / 2, y + L["label_dy"], label)


def draw_h_arrow(pdf, x, y, s=1.0):
    a = 9 * s
    pdf.setStrokeColor(TEAL_ARROW)
    pdf.setLineCap(1)
    pdf.setLineWidth(3)
    pdf.line(x - a, y, x + a * 0.55, y)
    p = pdf.beginPath()
    p.moveTo(x + a * 1.2, y)
    p.lineTo(x + a * 0.35, y - a * 0.55)
    p.lineTo(x + a * 0.35, y + a * 0.55)
    p.close()
    pdf.setFillColor(TEAL_ARROW)
    pdf.drawPath(p, fill=1, stroke=0)


def draw_v_arrow(pdf, x, y):
    pdf.setStrokeColor(TEAL_ARROW)
    pdf.setLineCap(1)
    pdf.setLineWidth(3)
    pdf.line(x, y + 7, x, y - 3)
    p = pdf.beginPath()
    p.moveTo(x, y - 9)
    p.lineTo(x - 5, y - 1)
    p.lineTo(x + 5, y - 1)
    p.close()
    pdf.setFillColor(TEAL_ARROW)
    pdf.drawPath(p, fill=1, stroke=0)


def draw_arrows(pdf, n, L):
    cols = L["cols"]
    rows = (n + cols - 1) // cols
    margin, cw, cg, ch, rg, gtop = (L["margin"], L["card_w"], L["col_gap"],
                                    L["card_h"], L["row_gap"],
                                    L["grid_top"])
    # horizontal arrows between cards in the same row
    for r in range(rows):
        top = gtop - r * (ch + rg)
        for c in range(cols - 1):
            i = r * cols + c
            if i + 1 < n and (i + 1) // cols == r:
                gx = margin + (c + 1) * (cw + cg) - cg / 2
                draw_h_arrow(pdf, gx, top - ch / 2, L["arrow_s"])
    # vertical arrows between rows (never after the final step).
    # Rows always read left-to-right; the arrow drops down the right
    # side (carriage return), matching the approved Page 1 pattern.
    for r in range(rows - 1):
        if (r + 1) >= rows:
            continue
        if n == 5 and r == 1:
            ax = PAGE_WIDTH / 2  # to the centered final card
        else:
            ax = PAGE_WIDTH - margin - 20  # down the right side
        gy = gtop - (r + 1) * ch - r * rg - rg / 2
        draw_v_arrow(pdf, ax, gy)


MORNING_STEPS = [
    ("Get toothbrush", "dr-teeth-1", 0.5),
    ("Add toothpaste", "dr-teeth-2", 0.5),
    ("Brush teeth", "dr-teeth-3", 0.5),
    ("Spit it out", "dr-teeth-4", 0.62),
    ("Rinse mouth", "dr-teeth-5", 0.5),
    ("Wash face", "dr-teeth-7", 0.5),
    ("Dry face", "dr-teeth-8", 0.5),
    ("All done!", "dr-teeth-6", 0.5),
]


HANDS_STEPS = [
    ("Turn on water", "dr-hands-1", 0.5),
    ("Wet hands", "dr-hands-2", 0.5),
    ("Add soap", "dr-hands-3", 0.5),
    ("Scrub hands", "dr-hands-4", 0.5),
    ("Rinse hands", "dr-hands-5", 0.5),
    ("Dry hands", "dr-hands-6", 0.5),
]


BEDTIME_STEPS = [
    ("Clean up", "dr-bed-1", 0.5),
    ("Take a bath", "dr-bed-2", 0.5),
    ("Put on pajamas", "dr-bed-3", 0.5),
    ("Go potty", "dr-bed-4", 0.5),
    ("Brush teeth", "dr-bed-5", 0.5),
    ("Read a story", "dr-bed-6", 0.5),
    ("Sleep", "dr-bed-7", 0.5),
]


# Illustrations cropped from the user-supplied "My Toilet Routine" reference
# image (2026-09-29); wording follows the reference.
TOILET_STEPS = [
    ("Go to the toilet", "dr-potty-1", 0.5),
    ("Sit on the toilet", "dr-potty-2", 0.5),
    ("Go potty", "dr-potty-3", 0.5),
    ("Wipe", "dr-potty-4", 0.5),
    ("Pull up pants", "dr-potty-5", 0.5),
    ("Flush", "dr-potty-6", 0.5),
    ("Wash hands", "dr-potty-7", 0.5),
    ("Dry hands", "dr-potty-8", 0.5),
]


# Pages whose cards carry no number badges: the arrows alone communicate
# the sequence, so the cards feel like visual supports, not worksheet steps.
NO_BADGES = {"My Bedtime Routine", "My Toilet Routine"}


def draw_routine_page(pdf, focus, steps):
    n = len(steps)
    L = LAYOUTS[n]
    draw_header(pdf, "My Daily Routines: " + focus,
                "Preschool Visual Supports & Routines",
                compact=L["compact_header"])
    for i, (label, stem, fx) in enumerate(steps):
        draw_card(pdf, i, label, stem, n, L, fx=fx,
                  badge=(focus not in NO_BADGES))
    draw_arrows(pdf, n, L)
    draw_footer(pdf)


def build_single_page(focus, steps, out_path):
    pdf = canvas.Canvas(out_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_routine_page(pdf, focus, steps)
    pdf.save()


# All pages in order. Pages marked locked are carried over byte-identical
# from the existing prototype (split with pdfseparate); only unlocked pages
# are rebuilt. To revise a page, mark it unlocked and keep earlier pages
# locked; to add a page, append it unlocked.
PAGES = [
    ("Brush, Wash & Get Ready", MORNING_STEPS, True),   # LOCKED 2026-09-29
    ("Wash My Hands", HANDS_STEPS, True),               # LOCKED 2026-09-29
    ("My Toilet Routine", TOILET_STEPS, True),               # LOCKED 2026-09-29
    ("My Bedtime Routine", BEDTIME_STEPS, True),             # LOCKED 2026-09-29
]


def main():
    import subprocess
    import tempfile
    tmpdir = tempfile.mkdtemp(prefix="dr-")
    if not os.path.exists(OUT):
        raise SystemExit(f"prototype not found: {OUT}")
    # Split the existing prototype so locked pages can be reused as-is.
    splitdir = tempfile.mkdtemp(prefix="dr-split-")
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
    for k, (focus, steps, locked) in enumerate(PAGES):
        if locked:
            li += 1
            ordered.append(os.path.join(splitdir, f"p-{li}.pdf"))
        else:
            p = os.path.join(tmpdir, f"newpage-{k}.pdf")
            build_single_page(focus, steps, p)
            ordered.append(p)
            print(f"rebuilt page: {focus} -> {p}")
    merged = OUT + ".new"
    subprocess.run(["pdfunite", *ordered, merged], check=True)
    os.replace(merged, OUT)
    print(f"merged {len(ordered)} page(s) ({n_locked} locked, {n_new} rebuilt) -> {OUT}")


if __name__ == "__main__":
    main()
