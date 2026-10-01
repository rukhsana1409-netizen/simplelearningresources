"""All About Me — Preschool Thinking & Our World / Myself & Family.

A 4-page pack about the child themselves:
  P1 My Body        — match 12 body-part words to a professionally
                      illustrated full-body child (v3: same character in
                      overall shorts; neck/arms/knees clearly visible)
  P2 My Five Senses — match each sense to the picture (redesigned 2026-10-01
                      v2: illustrated sense visuals + shuffled pictures;
                      Tongue -- Taste)
  P3 My Family       — warm multi-generational scene; find grandma and baby
                      (LOCKED - approved)
  P4 All About Me    — draw yourself; circle age and favorite color
                      (LOCKED - approved)

Minimal reading, one obvious task per page, original artwork.
"""

import math
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
    pdf.setFont("Helvetica-Bold", 14)
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
# Page 1: My Body -- match 12 body-part words to a professionally illustrated
# full-body child (v3: same character, overall shorts so knees/legs/neck are
# clearly visible). Six labels per side, vertically shuffled so children
# actually match, with generous blank drawing space between each word and
# the child.
# ---------------------------------------------------------------------------
P1_CHILD = "aam-child-v3-crop.jpg"
P1_CHILD_CX, P1_CHILD_TOP, P1_CHILD_H = 306, 570, 380
P1_CHILD_W = P1_CHILD_H * 772 / 1836
P1_LABELS_LEFT = [("Knee", 575), ("Mouth", 505), ("Head", 435),
                  ("Leg", 365), ("Hand", 295), ("Fingers", 225)]
P1_LABELS_RIGHT = [("Ears", 555), ("Neck", 485), ("Arm", 415),
                   ("Eyes", 345), ("Foot", 275), ("Nose", 205)]


def build_p1_body_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "All About Me", "My Body")
    draw_instruction(pdf, "Draw a line to match each body part.")
    pdf.drawImage(os.path.join(ASSETS, P1_CHILD),
                  P1_CHILD_CX - P1_CHILD_W / 2, P1_CHILD_TOP - P1_CHILD_H,
                  width=P1_CHILD_W, height=P1_CHILD_H,
                  preserveAspectRatio=True, anchor="c")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 20)
    for word, y in P1_LABELS_LEFT:
        pdf.drawCentredString(112, y, word)
    for word, y in P1_LABELS_RIGHT:
        pdf.drawCentredString(500, y, word)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()



# ---------------------------------------------------------------------------
# Page 2: My Five Senses -- draw a line to match each sense to the picture.
# Left column: five professionally illustrated sense visuals in one
# consistent 2D children's-book style, each labeled (Tongue -- Taste, not
# Mouth). Right column: five real-world pictures in shuffled order (bell,
# teddy, rainbow, orange, flower) so the answers land 3rd/1st/5th/4th/2nd
# for eyes/ears/nose/tongue/hand -- no straight-across matches.
# (Tongue illustration pending -- dashed placeholder until approved art.)
# ---------------------------------------------------------------------------
P2_SENSES = [
    ("aam3-eyes.jpg", "Eyes \u2014 See"),
    ("aam3-ears.jpg", "Ears \u2014 Hear"),
    ("aam3-nose.jpg", "Nose \u2014 Smell"),
    ("aam3-tongue.jpg", "Tongue \u2014 Taste"),
    ("aam3-hand.jpg", "Hand \u2014 Touch"),
]
P2_PICS = ["aam3-bell.jpg", "aam3-teddy.jpg", "aam3-rainbow.jpg",
           "aam3-orange.jpg", "aam3-flower.jpg"]
P2_ROW_TOPS = [606, 499, 392, 285, 178]
P2_IMG = 80
P2_LEFT_CX, P2_RIGHT_CX = 160, 452


def build_p2_senses_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "All About Me", "My Five Senses")
    draw_instruction(pdf, "Draw a line to match each sense to the picture.")
    # Subtle vertical divider between the two columns.
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(1.5)
    pdf.line(306, 80, 306, 600)
    for k, top in enumerate(P2_ROW_TOPS):
        y = top - P2_IMG
        pdf.drawImage(os.path.join(ASSETS, P2_SENSES[k][0]),
                      P2_LEFT_CX - P2_IMG / 2, y,
                      width=P2_IMG, height=P2_IMG,
                      preserveAspectRatio=True, anchor="c")
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(P2_LEFT_CX, y - 16, P2_SENSES[k][1])
        pdf.drawImage(os.path.join(ASSETS, P2_PICS[k]),
                      P2_RIGHT_CX - P2_IMG / 2, y,
                      width=P2_IMG, height=P2_IMG,
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
# Page 4: About Me — poster-style card set (redesigned 2026-10-01 v2 from a
# user-supplied reference: layout/concept inspiration only; all artwork is
# original to this pack). Six pastel cards: Draw yourself! / My name is /
# I am _ years old / My favorite color is / When I grow up... / My favorite
# animal is. Small vector decorations (sun, heart, star, paw) plus three
# original illustrations in the pack's 2D style.
# ---------------------------------------------------------------------------
P4_COLORS = [HexColor("#E74C3C"), HexColor("#3498DB"), HexColor("#F1C40F"),
             HexColor("#2ECC71"), HexColor("#9B59B6")]


def _p4_card(pdf, x, top, w, h, fill, border):
    y = top - h
    pdf.setFillColor(fill)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.5)
    pdf.roundRect(x, y, w, h, 14, stroke=1, fill=1)
    return y


def _p4_title(pdf, cx, y, text, size=14):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(cx, y, text)


def _p4_frame(pdf, x, top, w, h):
    y = top - h
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(1.5)
    pdf.roundRect(x, y, w, h, 10, stroke=1, fill=1)
    return y


def _p4_sun(pdf, cx, cy, r):
    pdf.setStrokeColor(HexColor("#F0A92E"))
    pdf.setLineWidth(2)
    for a in range(0, 360, 45):
        rad = math.radians(a)
        pdf.line(cx + math.cos(rad) * (r + 4), cy + math.sin(rad) * (r + 4),
                 cx + math.cos(rad) * (r + 12), cy + math.sin(rad) * (r + 12))
    pdf.setFillColor(HexColor("#FFC93C"))
    pdf.circle(cx, cy, r, stroke=1, fill=1)


def _p4_heart(pdf, cx, cy, s):
    pdf.setFillColor(HexColor("#E86A7A"))
    p = pdf.beginPath()
    p.moveTo(cx, cy - 0.9 * s)
    p.curveTo(cx - 1.5 * s, cy, cx - 0.75 * s, cy + 0.95 * s, cx, cy + 0.4 * s)
    p.curveTo(cx + 0.75 * s, cy + 0.95 * s, cx + 1.5 * s, cy, cx, cy - 0.9 * s)
    pdf.drawPath(p, stroke=0, fill=1)


def _p4_star(pdf, cx, cy, r):
    pdf.setFillColor(HexColor("#FFC93C"))
    pdf.setStrokeColor(HexColor("#F0A92E"))
    pdf.setLineWidth(1.2)
    p = pdf.beginPath()
    for k in range(10):
        ang = math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        px, py = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
        if k == 0:
            p.moveTo(px, py)
        else:
            p.lineTo(px, py)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)


def _p4_paw(pdf, cx, cy, s, color):
    pdf.setFillColor(color)
    pdf.ellipse(cx - 0.9 * s, cy - 0.7 * s, cx + 0.9 * s, cy + 0.7 * s,
                stroke=0, fill=1)
    for dx, dy in [(-0.75, 0.8), (-0.25, 1.05), (0.25, 1.05), (0.75, 0.8)]:
        pdf.circle(cx + dx * s, cy + dy * s, 0.32 * s, stroke=0, fill=1)


def build_p4_about_me_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "All About Me", "About Me")
    draw_instruction(pdf, "Show who you are!")

    # Card 1 (blue): Draw yourself!
    _p4_card(pdf, 60, 590, 238, 200, HexColor("#E9F4FE"), HexColor("#BFDDF5"))
    _p4_title(pdf, 179, 562, "Draw yourself!")
    _p4_frame(pdf, 72, 548, 214, 146)
    _p4_sun(pdf, 272, 570, 8)

    # Card 2 (pink): My favorite color is
    _p4_card(pdf, 60, 380, 238, 108, HexColor("#FDEDF3"), HexColor("#F3C9D8"))
    _p4_title(pdf, 179, 354, "My favorite color is", 13)
    dx = 103
    for col in P4_COLORS:
        pdf.setFillColor(col)
        pdf.setStrokeColor(HexColor("#D7E0EA"))
        pdf.setLineWidth(2)
        pdf.circle(dx, 314, 15, stroke=1, fill=1)
        dx += 38

    # Card 3 (orange): When I grow up, I want to be...
    _p4_card(pdf, 60, 262, 238, 182, HexColor("#FDF1E2"), HexColor("#F0D9B8"))
    _p4_title(pdf, 179, 238, "When I grow up,", 13)
    _p4_title(pdf, 179, 220, "I want to be...", 13)
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(1.5)
    pdf.roundRect(150, 144, 124, 64, 30, stroke=1, fill=1)
    for bx, by, br in [(140, 150, 7), (128, 138, 5), (118, 128, 3.5)]:
        pdf.circle(bx, by, br, stroke=1, fill=1)
    pdf.drawImage(os.path.join(ASSETS, "aam4-dream-girl.png"), 50, 82,
                  width=92, height=116, preserveAspectRatio=True, anchor="c",
                  mask="auto")

    # Card 4 (yellow): My name is
    _p4_card(pdf, 314, 590, 238, 140, HexColor("#FDF6DF"), HexColor("#EDDFAE"))
    _p4_title(pdf, 433, 562, "My name is")
    _p4_frame(pdf, 326, 546, 214, 84)
    _p4_heart(pdf, 524, 566, 9)
    _p4_star(pdf, 338, 474, 11)

    # Card 5 (green): I am _ years old.
    _p4_card(pdf, 314, 442, 238, 158, HexColor("#EAF6EA"), HexColor("#BFE3BF"))
    _p4_title(pdf, 433, 416, "I am")
    ax = 349
    for n in ("2", "3", "4", "5", "6"):
        pdf.setStrokeColor(HexColor("#9CCB9C"))
        pdf.setLineWidth(2)
        pdf.setFillColor(white)
        pdf.circle(ax, 372, 18, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawCentredString(ax, 366, n)
        ax += 42
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(433, 336, "years old.")

    # Card 6 (purple): My favorite animal is
    _p4_card(pdf, 314, 274, 238, 194, HexColor("#F0EBFA"), HexColor("#D3C6EE"))
    _p4_title(pdf, 433, 250, "My favorite animal is", 13)
    _p4_frame(pdf, 326, 234, 214, 110)
    _p4_paw(pdf, 346, 146, 10, HexColor("#B9A3D9"))
    pdf.drawImage(os.path.join(ASSETS, "aam4-puppy.png"), 516, 76,
                  width=62, height=71, preserveAspectRatio=True, anchor="c",
                  mask="auto")

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
