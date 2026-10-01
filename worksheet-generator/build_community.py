"""Our Community — Preschool Thinking & Our World / Community.

A 5-page pack with a real progression:
  P1 People in Our Community  — meet 8 community people (vocabulary intro)
  P2 What Do They Use?        — worker -> tool (true matching activity)
  P3 Places in Our Community  — picture -> community place (true matching)
  P4 Who Can Help?            — everyday situation -> helper (apply)
  P5 What Belongs With the Job? — odd one out (reasoning/application)

Revised 2026-10-01: new art direction (warm, simple, flat children's
educational illustration — not glossy 3D), 8 workers instead of 4,
matching-line activities on P2/P3, all-new original assets.

Revised round 2 (2026-10-01): P1 instruction "Meet the people in our
community!"; clearer books, stamped envelopes, grocery-filled cart,
bold "LIBRARY CARD"; new school-bus asset; P3 matches bus / older
librarian / cart / fire truck with a column divider; four unmistakable
P4 situations; dividers on both matching pages.

FINALIZED 2026-10-01: all 5 pages user-approved and locked. The combined
PDF is merged from these locked pages only — do not regenerate them.

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
                      "assets", "community")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "worksheets", "preschool", "thinking",
                   "community",
                   "our-community-prototype.pdf")


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
# Page 1: People in Our Community — vocabulary introduction, not a quiz.
# 8 large labeled portraits in a spacious 2 x 4 grid.
# ---------------------------------------------------------------------------
P1_WORKERS = [
    ("com-w-police.jpg", "Police Officer"),
    ("com-w-fire.jpg", "Firefighter"),
    ("com-w-nurse.jpg", "Nurse"),
    ("com-w-teacher.jpg", "Teacher"),
    ("com-w-librarian.jpg", "Librarian"),
    ("com-w-mail.jpg", "Mail Carrier"),
    ("com-w-vet.jpg", "Veterinarian"),
    ("com-w-build.jpg", "Construction Worker"),
]
P1_COL_CX = [196, 416]
P1_ROW_TOPS = [600, 464, 328, 192]
P1_IMG = 100


def build_p1_people_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Our Community", "People in Our Community")
    draw_instruction(pdf, "Meet the people in our community!")
    for r, top in enumerate(P1_ROW_TOPS):
        for c, cx in enumerate(P1_COL_CX):
            img, label = P1_WORKERS[r * 2 + c]
            pdf.drawImage(os.path.join(ASSETS, img),
                          cx - P1_IMG / 2, top - P1_IMG,
                          width=P1_IMG, height=P1_IMG,
                          preserveAspectRatio=True, anchor="c")
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawCentredString(cx, top - P1_IMG - 22, label)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Shared matching layout for P2/P3: left column + right column with wide
# open space between them for children to draw matching lines.
# ---------------------------------------------------------------------------
MATCH_ROW_TOPS = [600, 468, 336, 204]
MATCH_LEFT_CX, MATCH_RIGHT_CX = 97, 515


def build_match_page(path, subtitle, instruction, left_items, right_items,
                     img_size, label_size=0):
    """left_items / right_items: lists of (filename, label or None)."""
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Our Community", subtitle)
    draw_instruction(pdf, instruction)
    # Clear vertical divider between the two columns.
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(1.5)
    pdf.line(306, 80, 306, 596)
    for top, (l_img, l_label), (r_img, _r_label) in zip(
            MATCH_ROW_TOPS, left_items, right_items):
        pdf.drawImage(os.path.join(ASSETS, l_img),
                      MATCH_LEFT_CX - img_size / 2, top - img_size,
                      width=img_size, height=img_size,
                      preserveAspectRatio=True, anchor="c")
        if l_label and label_size:
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", label_size)
            pdf.drawCentredString(MATCH_LEFT_CX, top - img_size - 20,
                                  l_label)
        pdf.drawImage(os.path.join(ASSETS, r_img),
                      MATCH_RIGHT_CX - img_size / 2, top - img_size,
                      width=img_size, height=img_size,
                      preserveAspectRatio=True, anchor="c")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2: What Do They Use? — draw a line from each worker to their tool.
# Right column shuffled: no straight-across answers.
# ---------------------------------------------------------------------------
P2_LEFT = [
    ("com-w-fire.jpg", None),
    ("com-w-librarian.jpg", None),
    ("com-w-mail.jpg", None),
    ("com-w-build.jpg", None),
]
P2_RIGHT = [
    ("com-o-letters.jpg", None),   # -> mail carrier (row 3)
    ("com-o-hammer.jpg", None),    # -> construction worker (row 4)
    ("com-o-books.jpg", None),     # -> librarian (row 2)
    ("com-o-hose.jpg", None),      # -> firefighter (row 1)
]


def build_p2_tools_page(path):
    build_match_page(path, "What Do They Use?",
                     "Draw a line to match each person to what they use.",
                     P2_LEFT, P2_RIGHT, 105)


# ---------------------------------------------------------------------------
# Page 3: Places in Our Community — draw a line from each picture to
# the place. Buildings carry labels; the child matches by recognizing
# what each community place looks like.
# ---------------------------------------------------------------------------
P3_LEFT = [
    ("com-b-school.jpg", "School"),
    ("com-b-library.jpg", "Library"),
    ("com-b-grocery.jpg", "Grocery Store"),
    ("com-b-firestation.jpg", "Fire Station"),
]
P3_RIGHT = [
    ("com-o-cart.jpg", None),    # -> grocery store (row 3)
    ("com-o-bus.jpg", None),     # -> school (row 1)
    ("com-o-truck.jpg", None),   # -> fire station (row 4)
    ("com-w-librarian.jpg", None),  # -> library (row 2)
]


def build_p3_places_page(path):
    build_match_page(path, "Places in Our Community",
                     "Draw a line to match each picture to the place.",
                     P3_LEFT, P3_RIGHT, 105, label_size=14)


# ---------------------------------------------------------------------------
# Shared quiz-row layout for P4/P5: one rounded panel per row, anchor
# image on the left, divider, three choices on the right.
# ---------------------------------------------------------------------------
ROW_PANEL_X, ROW_PANEL_W, ROW_PANEL_H = 26, 560, 120
ROW_TOPS = [608, 469, 330, 191]
DIVIDER_X = 26 + 150


def draw_quiz_row(pdf, left_img, left_size, choices, choice_size, top):
    y = top - ROW_PANEL_H
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(2)
    pdf.roundRect(ROW_PANEL_X, y, ROW_PANEL_W, ROW_PANEL_H, 16,
                  stroke=1, fill=1)
    cy = y + ROW_PANEL_H / 2
    pdf.drawImage(os.path.join(ASSETS, left_img),
                  26 + 75 - left_size / 2, cy - left_size / 2,
                  width=left_size, height=left_size,
                  preserveAspectRatio=True, anchor="c")
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(1.5)
    pdf.line(DIVIDER_X, y + 14, DIVIDER_X, y + ROW_PANEL_H - 14)
    slot = (ROW_PANEL_X + ROW_PANEL_W - DIVIDER_X - 8) / 3
    for i, fn in enumerate(choices):
        cx = DIVIDER_X + 8 + slot * (i + 0.5)
        pdf.drawImage(os.path.join(ASSETS, fn),
                      cx - choice_size / 2, cy - choice_size / 2,
                      width=choice_size, height=choice_size,
                      preserveAspectRatio=True, anchor="c")


# ---------------------------------------------------------------------------
# Page 4: Who Can Help? — gentle everyday situation -> the right helper.
# Correct positions: 2, 1, 3, 2 (varied, no adjacent repeats).
# ---------------------------------------------------------------------------
P4_PROBLEMS = [
    ("com-s-sick.jpg",
     ["com-w-fire.jpg", "com-w-nurse.jpg",
      "com-w-teacher.jpg"]),          # nurse: 2nd
    ("com-s-lost.jpg",
     ["com-w-police.jpg", "com-w-nurse.jpg",
      "com-w-mail.jpg"]),             # police officer: 1st
    ("com-s-book.jpg",
     ["com-w-build.jpg", "com-w-librarian.jpg",
      "com-w-fire.jpg"]),             # librarian: 2nd
    ("com-s-pet.jpg",
     ["com-w-librarian.jpg", "com-w-build.jpg",
      "com-w-vet.jpg"]),              # veterinarian: 3rd
]


def build_p4_who_can_help_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Our Community", "Who Can Help?")
    draw_instruction(pdf, "Look at the picture. Who can help? Circle them!")
    for idx, (situation, choices) in enumerate(P4_PROBLEMS):
        draw_quiz_row(pdf, situation, 115, choices, 88, ROW_TOPS[idx])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5: What Belongs With the Job? — odd one out (reasoning).
# Wrong positions: 2, 3, 1, 2 (varied, no adjacent repeats).
# ---------------------------------------------------------------------------
P5_PROBLEMS = [
    ("com-w-fire.jpg",
     ["com-o-truck.jpg", "com-o-spoon.jpg",
      "com-o-hose.jpg"]),             # spoon does not belong: 2nd
    ("com-w-build.jpg",
     ["com-o-hammer.jpg", "com-o-hardhat.jpg",
      "com-o-banana.jpg"]),           # banana does not belong: 3rd
    ("com-w-mail.jpg",
     ["com-o-icecream.jpg", "com-o-letters.jpg",
      "com-o-mailbox.jpg"]),          # ice cream does not belong: 1st
    ("com-w-librarian.jpg",
     ["com-o-books.jpg", "com-o-soccer.jpg",
      "com-o-libcard.jpg"]),          # soccer ball does not belong: 2nd
]


def build_p5_odd_one_out_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Our Community", "What Belongs With the Job?")
    draw_instruction(pdf, "Which one does NOT belong? Circle it!")
    for idx, (worker, choices) in enumerate(P5_PROBLEMS):
        draw_quiz_row(pdf, worker, 100, choices, 82, ROW_TOPS[idx])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page registry + build/merge driver (locked pages are reused from the
# existing prototype so approved pages are never re-rendered).
# ---------------------------------------------------------------------------
PAGES = [
    ("People in Our Community", build_p1_people_page, True),
    ("What Do They Use?", build_p2_tools_page, True),
    ("Places in Our Community", build_p3_places_page, True),
    ("Who Can Help?", build_p4_who_can_help_page, True),
    ("What Belongs With the Job?", build_p5_odd_one_out_page, True),
]


def main():
    tmpdir = tempfile.mkdtemp(prefix="com-")
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
    splitdir = tempfile.mkdtemp(prefix="com-split-")
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
