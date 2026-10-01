#!/usr/bin/env python3
"""REVIEW BUILD ONLY — My Body & Five Senses (Preschool -> Science & Discovery).

Reuses the user-approved My Body and My Five Senses pages from the
FINALIZED "All About Me" pack WITHOUT modifying that pack in any way.
The ONLY adaptation per page is the header pack title:
    "All About Me" -> "My Body & Five Senses"

Everything else — artwork, layout, wording, spacing, instructions —
is byte-for-byte the approved content.

Do NOT lock, finalize, merge, or publish until the user reviews.
"""

import os
import subprocess
import sys
import tempfile

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_all_about_me as aam

PACK_TITLE = "My Body & Five Senses"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "preschool", "science", "human-body")
OUT = os.path.join(OUT_DIR, "my-body-five-senses.pdf")


def build_p1_body(path):
    """Adapted from build_all_about_me.build_p1_body_page: title only."""
    pdf = canvas.Canvas(path, pagesize=(aam.PAGE_WIDTH, aam.PAGE_HEIGHT))
    aam.draw_header(pdf, PACK_TITLE, "My Body")
    aam.draw_instruction(pdf, "Draw a line to match each body part.")
    pdf.drawImage(os.path.join(aam.ASSETS, aam.P1_CHILD),
                  aam.P1_CHILD_CX - aam.P1_CHILD_W / 2,
                  aam.P1_CHILD_TOP - aam.P1_CHILD_H,
                  width=aam.P1_CHILD_W, height=aam.P1_CHILD_H,
                  preserveAspectRatio=True, anchor="c")
    pdf.setFillColor(aam.INK)
    pdf.setFont("Helvetica-Bold", 20)
    for word, y in aam.P1_LABELS_LEFT:
        pdf.drawCentredString(112, y, word)
    for word, y in aam.P1_LABELS_RIGHT:
        pdf.drawCentredString(500, y, word)
    aam.draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def build_p2_senses(path):
    """Adapted from build_all_about_me.build_p2_senses_page: title only."""
    pdf = canvas.Canvas(path, pagesize=(aam.PAGE_WIDTH, aam.PAGE_HEIGHT))
    aam.draw_header(pdf, PACK_TITLE, "My Five Senses")
    aam.draw_instruction(pdf, "Draw a line to match each sense to the picture.")
    # Subtle vertical divider between the two columns.
    pdf.setStrokeColor(HexColor("#D7E0EA"))
    pdf.setLineWidth(1.5)
    pdf.line(306, 80, 306, 600)
    for k, top in enumerate(aam.P2_ROW_TOPS):
        y = top - aam.P2_IMG
        pdf.drawImage(os.path.join(aam.ASSETS, aam.P2_SENSES[k][0]),
                      aam.P2_LEFT_CX - aam.P2_IMG / 2, y,
                      width=aam.P2_IMG, height=aam.P2_IMG,
                      preserveAspectRatio=True, anchor="c")
        pdf.setFillColor(aam.INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(aam.P2_LEFT_CX, y - 16, aam.P2_SENSES[k][1])
        pdf.drawImage(os.path.join(aam.ASSETS, aam.P2_PICS[k]),
                      aam.P2_RIGHT_CX - aam.P2_IMG / 2, y,
                      width=aam.P2_IMG, height=aam.P2_IMG,
                      preserveAspectRatio=True, anchor="c")
    aam.draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    # (title, builder, locked) — BOTH PAGES APPROVED by user 2026-10-01.
    ("My Body", build_p1_body, True),
    ("My Five Senses", build_p2_senses, True),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="body-senses-")
    splitdir = tempfile.mkdtemp(prefix="body-senses-split-")
    # Split the existing prototype so locked pages are preserved byte-exact.
    if os.path.exists(OUT):
        subprocess.run(["pdfseparate", OUT,
                        os.path.join(splitdir, "p-%d.pdf")], check=True)
        n_existing = len([f for f in os.listdir(splitdir)
                          if f.endswith(".pdf")])
    else:
        n_existing = 0
    ordered = []
    for k, (title, builder, locked) in enumerate(PAGES):
        if locked and 1 <= k + 1 <= n_existing:
            ordered.append(os.path.join(splitdir, f"p-{k + 1}.pdf"))
        else:
            p = os.path.join(tmpdir, f"newpage-{k}.pdf")
            builder(p)
            ordered.append(p)
            print(f"built page: {title} -> {p}")
    merged = OUT + ".new"
    subprocess.run(["pdfunite", *ordered, merged], check=True)
    os.replace(merged, OUT)
    print(f"merged {len(ordered)} page(s) "
          f"({sum(1 for _t, _b, l in PAGES if l)} locked) -> {OUT}")


if __name__ == "__main__":
    main()
