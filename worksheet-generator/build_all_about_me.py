"""All About Me — Preschool Thinking & Our World / Myself & Family.

A 4-page pack about the child themselves:
  P1 My Body        — draw lines from body-part close-ups to a big child
  P2 My Five Senses — circle the body part used in each situation
  P3 My Family       — warm multi-generational scene; find grandma and baby
  P4 All About Me    — draw yourself; circle age and favorite color

Minimal reading, one obvious task per page, original artwork.
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
                      "assets", "all-about-me")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "thinking",
                   "myself-family",
                   "all-about-me-prototype.pdf")


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


def draw_instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630, text)


# ---------------------------------------------------------------------------
# Page 1: My Body — draw a line from each close-up to the body part
# ---------------------------------------------------------------------------
P1_CHIPS = ["aam-eyes.jpg", "aam-nose.jpg", "aam-mouth.jpg", "aam-hand.jpg"]
P1_CHIP_TOPS = [608, 474, 340, 206]
P1_CHIP_SIZE = 120
P1_IMG = 100
P1_CHILD_PANEL_X = 200
P1_CHILD_PANEL_W = 386


def build_p1_body_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "All About Me", "My Body")
    draw_instruction(pdf, "Draw a line to the body part!")
    for top, chip in zip(P1_CHIP_TOPS, P1_CHIPS):
        y = top - P1_CHIP_SIZE
        pdf.setFillColor(white)
        pdf.setStrokeColor(HexColor("#D7E0EA"))
        pdf.setLineWidth(2)
        pdf.roundRect(26, y, P1_CHIP_SIZE, P1_CHIP_SIZE, 16,
                      stroke=1, fill=1)
        pdf.drawImage(os.path.join(ASSETS, chip),
                      26 + (P1_CHIP_SIZE - P1_IMG) / 2,
                      y + (P1_CHIP_SIZE - P1_IMG) / 2,
                      width=P1_IMG, height=P1_IMG,
                      preserveAspectRatio=True)
    # Big child panel on the right.
    y0, y1 = 86, 608
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(2)
    pdf.roundRect(P1_CHILD_PANEL_X, y0, P1_CHILD_PANEL_W, y1 - y0, 16,
                  stroke=1, fill=1)
    pdf.drawImage(os.path.join(ASSETS, "aam-child.jpg"),
                  P1_CHILD_PANEL_X + 18, y0 + 14,
                  width=P1_CHILD_PANEL_W - 36, height=y1 - y0 - 28,
                  preserveAspectRatio=True, anchor="c")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2: My Five Senses — circle the body part used in each situation
# ---------------------------------------------------------------------------
# Five rows.  Each row shows a situation vignette on the left and three
# body-part close-ups (reused from Page 1 for consistency) on the right.
# Correct positions: 2nd / 3rd / 1st / 2nd / 3rd.
P2_PROBLEMS = [
    ("aam-see-rainbow.jpg", ["aam-hand.jpg", "aam-eyes.jpg", "aam-nose.jpg"]),
    ("aam-hear-bird.jpg", ["aam-mouth.jpg", "aam-hand.jpg", "aam-ears.jpg"]),
    ("aam-smell-flower.jpg", ["aam-nose.jpg", "aam-eyes.jpg", "aam-mouth.jpg"]),
    ("aam-taste-juice.jpg", ["aam-ears.jpg", "aam-mouth.jpg", "aam-hand.jpg"]),
    ("aam-touch-teddy.jpg", ["aam-nose.jpg", "aam-mouth.jpg", "aam-hand.jpg"]),
]
P2_ROW_TOPS = [608, 500, 392, 284, 176]
P2_ROW_H = 100
P2_SIT_X, P2_SIT_W = 26, 190
P2_CHIP_SIZE, P2_CHIP_IMG = 96, 84
P2_CHIP_XS = [246, 358, 470]


def build_p2_senses_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "All About Me", "My Five Senses")
    draw_instruction(pdf, "Circle the body part you use!")
    for top, (sit, choices) in zip(P2_ROW_TOPS, P2_PROBLEMS):
        y = top - P2_ROW_H
        pdf.setFillColor(white)
        pdf.setStrokeColor(HexColor("#D7E0EA"))
        pdf.setLineWidth(2)
        pdf.roundRect(P2_SIT_X, y, P2_SIT_W, P2_ROW_H, 14,
                      stroke=1, fill=1)
        pdf.drawImage(os.path.join(ASSETS, sit),
                      P2_SIT_X + 6, y + 6,
                      width=P2_SIT_W - 12, height=P2_ROW_H - 12,
                      preserveAspectRatio=True, anchor="c")
        for cx, chip in zip(P2_CHIP_XS, choices):
            pdf.setFillColor(white)
            pdf.setStrokeColor(HexColor("#D7E0EA"))
            pdf.setLineWidth(2)
            pdf.roundRect(cx, y, P2_CHIP_SIZE, P2_CHIP_SIZE, 14,
                          stroke=1, fill=1)
            pdf.drawImage(os.path.join(ASSETS, chip),
                          cx + (P2_CHIP_SIZE - P2_CHIP_IMG) / 2,
                          y + (P2_CHIP_SIZE - P2_CHIP_IMG) / 2,
                          width=P2_CHIP_IMG, height=P2_CHIP_IMG,
                          preserveAspectRatio=True, anchor="c")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3: My Family — warm multi-generational family scene; observe + name.
# Inclusive by design: "this family", never "your family"; no fixed structure
# is implied. The adult names family words; the child finds them in the scene.
# ---------------------------------------------------------------------------
P3_SCENE = "aam-family-scene.jpg"
P3_PANEL_X, P3_PANEL_W = 26, 560
P3_PANEL_TOP, P3_PANEL_H = 600, 462


def build_p3_family_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "All About Me", "My Family")
    draw_instruction(pdf, "Look at this family! Can you find the grandma and the baby?")
    y = P3_PANEL_TOP - P3_PANEL_H
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(2)
    pdf.roundRect(P3_PANEL_X, y, P3_PANEL_W, P3_PANEL_H, 16,
                  stroke=1, fill=1)
    pdf.drawImage(os.path.join(ASSETS, P3_SCENE),
                  P3_PANEL_X + 14, y + 12,
                  width=P3_PANEL_W - 28, height=P3_PANEL_H - 24,
                  preserveAspectRatio=True, anchor="c")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4: All About Me — draw yourself; circle age and favorite color
# ---------------------------------------------------------------------------
# All vector: big draw frame, age numerals to circle, color dots to circle.
P4_COLORS = [HexColor("#E74C3C"), HexColor("#3498DB"), HexColor("#F1C40F"),
             HexColor("#2ECC71"), HexColor("#9B59B6")]


def build_p4_about_me_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "All About Me", "")
    draw_instruction(pdf, "Show who you are!")
    # Draw-yourself frame.
    fx, fw, ftop, fh = 26, 560, 608, 290
    fy = ftop - fh
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(2)
    pdf.roundRect(fx, fy, fw, fh, 16, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, ftop - 30, "Draw yourself!")
    pdf.setStrokeColor(HexColor("#B9C9D8"))
    pdf.setLineWidth(1.2)
    pdf.setDash(6, 4)
    pdf.roundRect(fx + 18, fy + 18, fw - 36, fh - 62, 10, stroke=1, fill=0)
    pdf.setDash()
    # Age row.
    ay = 248
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(60, ay, "I am")
    pdf.setFont("Helvetica", 16)
    ax = 140
    for n in ("3", "4", "5"):
        pdf.setStrokeColor(HexColor("#D7E0EA"))
        pdf.setLineWidth(2)
        pdf.setFillColor(white)
        pdf.circle(ax + 22, ay + 6, 22, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(ax + 22, ay - 1, n)
        ax += 76
    pdf.setFont("Helvetica", 16)
    pdf.drawString(ax + 6, ay, "years old.")
    # Favorite color row.
    cy = 150
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(60, cy, "My favorite color is")
    dx = 300
    for col in P4_COLORS:
        pdf.setFillColor(col)
        pdf.setStrokeColor(HexColor("#D7E0EA"))
        pdf.setLineWidth(2)
        pdf.circle(dx, cy + 6, 20, stroke=1, fill=1)
        dx += 56
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("My Body", build_p1_body_page, True),
    ("My Five Senses", build_p2_senses_page, True),
    ("My Family", build_p3_family_page, True),
    ("All About Me", build_p4_about_me_page, True),
]


def main():
    tmpdir = tempfile.mkdtemp(prefix="aam-")
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
    splitdir = tempfile.mkdtemp(prefix="aam-split-")
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
    for k, (title, builder, locked) in enumerate(PAGES):
        if locked:
            # Locked page k reuses existing page k+1 (page numbers, not the
            # locked-page counter — an unlocked page earlier in the pack must
            # not shift which split file a later locked page reuses).
            ordered.append(os.path.join(splitdir, f"p-{k + 1}.pdf"))
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
