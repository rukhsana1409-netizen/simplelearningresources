"""Our Community — Preschool Thinking & Our World / Community.

A 4-page pack about community helpers, with a real progression:
  P1 Who Helps Us?    — meet the helpers; point to each one (identify)
  P2 What Do They Use? — helper -> tool; circle the tool (associate)
  P3 Where Do They Work? — helper -> workplace; circle it (associate)
  P4 Who Can Help?    — everyday situation -> helper; circle (apply)

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
# Page 1: Who Helps Us? — meet the four helpers; adult names each one.
# ---------------------------------------------------------------------------
P1_HELPERS = ["com-firefighter.jpg", "com-doctor.jpg",
              "com-teacher.jpg", "com-mailcarrier.jpg"]
P1_PANEL_XS = [26, 316]
P1_PANEL_W, P1_PANEL_H = 270, 230
P1_ROW_TOPS = [608, 348]


def build_p1_helpers_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Our Community", "Who Helps Us?")
    draw_instruction(pdf, "Point to the helper!")
    for r, top in enumerate(P1_ROW_TOPS):
        y = top - P1_PANEL_H
        for c, x in enumerate(P1_PANEL_XS):
            helper = P1_HELPERS[r * 2 + c]
            pdf.setFillColor(white)
            pdf.setStrokeColor(HexColor("#D7E0EA"))
            pdf.setLineWidth(2)
            pdf.roundRect(x, y, P1_PANEL_W, P1_PANEL_H, 16,
                          stroke=1, fill=1)
            pdf.drawImage(os.path.join(ASSETS, helper),
                          x + 15, y + 12,
                          width=P1_PANEL_W - 30, height=P1_PANEL_H - 24,
                          preserveAspectRatio=True, anchor="c")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Shared row layout for P2/P3/P4: left anchor image + divider + 3 choices.
# ---------------------------------------------------------------------------
ROW_PANEL_X, ROW_PANEL_W, ROW_PANEL_H = 26, 560, 120
ROW_TOPS = [608, 469, 330, 191]
LEFT_IMG = 104
DIVIDER_X = 26 + 138


def draw_choice_row(pdf, left_img, choices, top):
    y = top - ROW_PANEL_H
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(2)
    pdf.roundRect(ROW_PANEL_X, y, ROW_PANEL_W, ROW_PANEL_H, 16,
                  stroke=1, fill=1)
    cy = y + ROW_PANEL_H / 2
    pdf.drawImage(os.path.join(ASSETS, left_img),
                  26 + 69 - LEFT_IMG / 2, cy - LEFT_IMG / 2,
                  width=LEFT_IMG, height=LEFT_IMG,
                  preserveAspectRatio=True, anchor="c")
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(1.5)
    pdf.line(DIVIDER_X, y + 14, DIVIDER_X, y + ROW_PANEL_H - 14)
    slot = (ROW_PANEL_X + ROW_PANEL_W - DIVIDER_X - 8) / 3
    for i, fn in enumerate(choices):
        cx = DIVIDER_X + 8 + slot * (i + 0.5)
        pdf.drawImage(os.path.join(ASSETS, fn),
                      cx - 44, cy - 44, width=88, height=88,
                      preserveAspectRatio=True, anchor="c")


# ---------------------------------------------------------------------------
# Page 2: What Do They Use? — helper -> tool.
# ---------------------------------------------------------------------------
P2_PROBLEMS = [
    ("com-firefighter.jpg",
     ["com-tool-stethoscope.jpg", "com-tool-hose.jpg",
      "com-tool-book.jpg"], 1),
    ("com-doctor.jpg",
     ["com-tool-stethoscope.jpg", "com-tool-mailbag.jpg",
      "com-tool-hose.jpg"], 0),
    ("com-teacher.jpg",
     ["com-tool-mailbag.jpg", "com-tool-hose.jpg",
      "com-tool-book.jpg"], 2),
    ("com-mailcarrier.jpg",
     ["com-tool-book.jpg", "com-tool-mailbag.jpg",
      "com-tool-stethoscope.jpg"], 1),
]


def build_p2_tools_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Our Community", "What Do They Use?")
    draw_instruction(pdf, "What does the helper use? Circle it!")
    for idx, (helper, choices, _correct) in enumerate(P2_PROBLEMS):
        draw_choice_row(pdf, helper, choices, ROW_TOPS[idx])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3: Where Do They Work? — helper -> workplace.
# ---------------------------------------------------------------------------
P3_PROBLEMS = [
    ("com-firefighter.jpg",
     ["com-place-school.jpg", "com-place-firestation.jpg",
      "com-place-hospital.jpg"], 1),
    ("com-doctor.jpg",
     ["com-place-hospital.jpg", "com-place-postoffice.jpg",
      "com-place-school.jpg"], 0),
    ("com-teacher.jpg",
     ["com-place-firestation.jpg", "com-place-hospital.jpg",
      "com-place-school.jpg"], 2),
    ("com-mailcarrier.jpg",
     ["com-place-school.jpg", "com-place-postoffice.jpg",
      "com-place-firestation.jpg"], 1),
]


def build_p3_places_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Our Community", "Where Do They Work?")
    draw_instruction(pdf, "Where does the helper work? Circle it!")
    for idx, (helper, choices, _correct) in enumerate(P3_PROBLEMS):
        draw_choice_row(pdf, helper, choices, ROW_TOPS[idx])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4: Who Can Help? — everyday situation -> helper.
# ---------------------------------------------------------------------------
P4_PROBLEMS = [
    ("com-sit-sick.jpg",
     ["com-firefighter.jpg", "com-doctor.jpg",
      "com-teacher.jpg"], 1),
    ("com-sit-kitten.jpg",
     ["com-firefighter.jpg", "com-mailcarrier.jpg",
      "com-doctor.jpg"], 0),
    ("com-sit-letter.jpg",
     ["com-teacher.jpg", "com-firefighter.jpg",
      "com-mailcarrier.jpg"], 2),
    ("com-sit-reading.jpg",
     ["com-doctor.jpg", "com-teacher.jpg",
      "com-mailcarrier.jpg"], 1),
]


def build_p4_who_can_help_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Our Community", "Who Can Help?")
    draw_instruction(pdf, "Who can help? Circle the helper!")
    for idx, (situation, choices, _correct) in enumerate(P4_PROBLEMS):
        draw_choice_row(pdf, situation, choices, ROW_TOPS[idx])
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page registry + build/merge driver (locked pages are reused from the
# existing prototype so approved pages are never re-rendered).
# ---------------------------------------------------------------------------
PAGES = [
    ("Who Helps Us?", build_p1_helpers_page, True),
    ("What Do They Use?", build_p2_tools_page, True),
    ("Where Do They Work?", build_p3_places_page, True),
    ("Who Can Help?", build_p4_who_can_help_page, True),
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
