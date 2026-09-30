"""Think & Choose — Preschool Thinking & Our World / Logic & Problem Solving.

Page 1 (this build): Which One Is Different? — three rows of four large
pictures; in each row three are identical and one differs by a single
visual feature (color -> size -> direction). The child points to the
different one.

Later pages will slot into the PAGES lock/merge scaffold below.
"""

import os
import subprocess
import tempfile

from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
INK = HexColor("#202A33")
NAVY = HexColor("#1E3A5F")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "think-choose")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "thinking",
                   "logic-problem-solving",
                   "think-choose-prototype.pdf")


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
    pdf.line(x + 10, y + 8, x + 26, y + 8)
    pdf.setFillColor(HexColor("#F4B63E"))
    pdf.circle(x + 18, y + 38, 4, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(x + 38, y + 30, "LEARNING")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(x + 38, y + 16, "MADE SIMPLE")


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
    pdf.drawString(MARGIN, 26, "Learning Made Simple")
    pdf.setStrokeColor(HexColor("#9CCBC6"))
    pdf.setLineWidth(1)
    pdf.line(190, 18, 190, 34)
    pdf.setFillColor(HexColor("#0E7C7B"))
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_WIDTH / 2 + 20, 26,
                          "Made with love for little learners.")
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(PAGE_WIDTH - MARGIN, 26,
                        "\u00a9 2026 Learning Made Simple")


# ---------------------------------------------------------------------------
# Page 1: Which One Is Different?
# ---------------------------------------------------------------------------
# Three rows of four large pictures.  In each row three pictures are
# identical and one differs by exactly one visual feature:
#   row 1: color     (3 red balls + 1 blue ball)
#   row 2: size      (3 big stars + 1 small star)
#   row 3: direction (3 ducks facing left + 1 duck facing right)
#   row 4: detail    (3 five-petal flowers + 1 four-petal flower)
# The odd picture sits in a different position each row.
# ---------------------------------------------------------------------------

P1_ROWS = [
    ["tc-ball-red.webp", "tc-ball-red.webp", "tc-ball-blue.webp",
     "tc-ball-red.webp"],
    ["tc-star.webp", "tc-star.webp", "tc-star.webp", "tc-star.webp"],
    ["tc-duck-left.webp", "tc-duck-left.webp", "tc-duck-left.webp",
     "tc-duck-right.webp"],
    ["tc-flower-5.webp", "tc-flower-4.webp", "tc-flower-5.webp",
     "tc-flower-5.webp"],
]
# Per-row, per-slot draw size (None = P1_IMG).  Row 2's odd star is small.
P1_SIZES = [
    [None, None, None, None],
    [58, None, None, None],
    [None, None, None, None],
    [None, None, None, None],
]

# ---------------------------------------------------------------------------
# Page 2: Which One Doesn't Belong?
# ---------------------------------------------------------------------------
# Four rows of four large pictures.  In each row three pictures belong to
# one familiar category and one does not.  All sixteen illustrations share
# the same style, size and detail level, so the odd one can only be found
# by meaning — never by color, size, direction or art style.
#   row 1: Fruits         (strawberry, banana, watermelon + sock)
#   row 2: Animals        (elephant, rabbit, butterfly + cup)
#   row 3: Things you wear (shirt, pants, cap + apple)
#   row 4: Vehicles       (car, bicycle, bus + book)
# ---------------------------------------------------------------------------

P2_ROWS = [
    ["tc-strawberry.webp", "tc-banana.webp", "tc-sock.webp",
     "tc-watermelon.webp"],
    ["tc-cup.webp", "tc-elephant.webp", "tc-rabbit.webp",
     "tc-butterfly.webp"],
    ["tc-shirt.webp", "tc-pants.webp", "tc-cap.webp", "tc-apple.webp"],
    ["tc-car.webp", "tc-book.webp", "tc-bicycle.webp", "tc-bus.webp"],
]
P2_SIZES = [[None] * 4 for _ in range(4)]

P1_PANEL_X = 26
P1_PANEL_W = 560
P1_PANEL_H = 120
P1_ROW_TOPS = [608, 469, 330, 191]
P1_IMG = 96


def draw_row(pdf, files, sizes, top):
    y = top - P1_PANEL_H
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(2)
    pdf.roundRect(P1_PANEL_X, y, P1_PANEL_W, P1_PANEL_H, 16,
                  stroke=1, fill=1)
    for i, fn in enumerate(files):
        size = sizes[i] or P1_IMG
        cx = P1_PANEL_X + 70 + i * 140
        cy = y + P1_PANEL_H / 2
        pdf.drawImage(os.path.join(ASSETS, fn),
                      cx - size / 2, cy - size / 2,
                      width=size, height=size, preserveAspectRatio=True)


def build_p1_different_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Think & Choose", "Which One Is Different?")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630,
                          "Which one is different? Point to it!")
    for files, sizes, top in zip(P1_ROWS, P1_SIZES, P1_ROW_TOPS):
        draw_row(pdf, files, sizes, top)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def build_p2_belong_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Think & Choose", "Which One Doesn\u2019t Belong?")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630,
                          "Which one doesn\u2019t belong? Point to it!")
    for files, sizes, top in zip(P2_ROWS, P2_SIZES, P1_ROW_TOPS):
        draw_row(pdf, files, sizes, top)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3: Find the Silly Mistake
# ---------------------------------------------------------------------------
# Four large storybook scenes in a 2x2 grid.  Each scene is an everyday
# situation containing exactly one obvious, unmistakably silly mistake:
#   scene 1: a child unlocking a front door with a banana (not a key)
#   scene 2: a fish swimming in the sky among the birds
#   scene 3: a car with square wheels instead of round ones
#   scene 4: a snowman melting on a sunny beach
# ---------------------------------------------------------------------------

P3_SCENES = [
    "tc-door-banana.webp",
    "tc-fish-sky.webp",
    "tc-car-square.webp",
    "tc-snowman-beach.webp",
]
P3_COL_X = [26, 313]
P3_PANEL_W = 273
P3_PANEL_H = 245
P3_ROW_TOPS = [600, 335]
P3_IMG_W = 253  # scenes are 3:2 landscape; fill the panel width
P3_IMG_H = 169


def draw_p3_panel(pdf, fn, x, top):
    y = top - P3_PANEL_H
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(2)
    pdf.roundRect(x, y, P3_PANEL_W, P3_PANEL_H, 16, stroke=1, fill=1)
    pdf.drawImage(os.path.join(ASSETS, fn),
                  x + (P3_PANEL_W - P3_IMG_W) / 2,
                  y + (P3_PANEL_H - P3_IMG_H) / 2,
                  width=P3_IMG_W, height=P3_IMG_H,
                  preserveAspectRatio=True)


def build_p3_silly_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Think & Choose", "Find the Silly Mistake")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630,
                          "Something is silly! Find the mistake.")
    for idx, fn in enumerate(P3_SCENES):
        row, col = divmod(idx, 2)
        draw_p3_panel(pdf, fn, P3_COL_X[col], P3_ROW_TOPS[row])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Which One Is Different?", build_p1_different_page, True),
    ("Which One Doesn\u2019t Belong?", build_p2_belong_page, True),
    ("Find the Silly Mistake", build_p3_silly_page, False),
]


def main():
    tmpdir = tempfile.mkdtemp(prefix="tc-")
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
    splitdir = tempfile.mkdtemp(prefix="tc-split-")
    subprocess.run(["pdfseparate", OUT, os.path.join(splitdir, "p-%d.pdf")],
                   check=True)
    n_existing = len([f for f in os.listdir(splitdir) if f.endswith(".pdf")])
    n_locked = sum(1 for _, _, locked in PAGES if locked)
    n_new = sum(1 for _, _, locked in PAGES if not locked)
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
