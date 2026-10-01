#!/usr/bin/env python3
"""REVIEW BUILD ONLY — Weather & Seasons (Preschool -> Science & Discovery).

Reuses the user-approved Seasons and Weather pages from the LOCKED
"My Calendar & Time" pack WITHOUT modifying that pack in any way.
The ONLY adaptation per page is the header pack title:
    "My Calendar & Time" -> "Weather & Seasons"

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
import build_calendar_time as ct

PACK_TITLE = "Weather & Seasons"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "worksheets", "preschool", "science", "weather-seasons")
OUT = os.path.join(OUT_DIR, "weather-seasons.pdf")


def build_p1_seasons(path):
    """Adapted from build_calendar_time.build_seasons_page: title only."""
    pdf = canvas.Canvas(path, pagesize=(ct.PAGE_WIDTH, ct.PAGE_HEIGHT))
    ct.draw_header(pdf, PACK_TITLE, "Seasons of the Year")
    # instruction lines
    pdf.setFillColor(ct.NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(ct.PAGE_WIDTH / 2, 628,
                          "There are 4 seasons. They go round and round!")
    pdf.setFont("Helvetica", 13.5)
    pdf.drawCentredString(ct.PAGE_WIDTH / 2, 606,
                          "Look outside. What season is it? Point to it!")
    # four season panels, reading order (draw_season_panel takes the bottom y)
    k = 0
    for row in range(2):
        for col in range(2):
            name, fill_hex, border_hex = ct.S4_PANELS[k]
            ct.draw_season_panel(pdf, name, fill_hex, border_hex,
                                 ct.S4_XS[col],
                                 ct.S4_TOPS[row] - ct.S4_PANEL_H)
            k += 1
    # cycle badge at the centre of the grid
    ct.draw_cycle_badge(pdf,
                        38 + ct.S4_PANEL_W + ct.S4_GAP_X / 2,
                        ct.S4_TOPS[1] + 14)
    # THIS SEASON marker tag
    ct.draw_this_season_tag(pdf, ct.PAGE_WIDTH / 2, 94)
    pdf.setFillColor(HexColor("#8A9492"))
    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawCentredString(ct.PAGE_WIDTH / 2, 68,
                          "Cut out the marker, or just point!")
    ct.draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def build_p2_weather(path):
    """Adapted from build_calendar_time.build_weather_page: title only."""
    pdf = canvas.Canvas(path, pagesize=(ct.PAGE_WIDTH, ct.PAGE_HEIGHT))
    ct.draw_header(pdf, PACK_TITLE, "What\u2019s the Weather?")
    pdf.setFillColor(ct.NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(ct.PAGE_WIDTH / 2, 628,
                          "What\u2019s the weather today?")
    pdf.setFont("Helvetica", 13.5)
    pdf.drawCentredString(ct.PAGE_WIDTH / 2, 606,
                          "Look outside. Point and say: Today is _____!")
    for (name, fill, border, _fn), x in zip(ct.W5_CARDS[:3], ct.W5_ROW1_XS):
        ct.draw_weather_card(pdf, name, fill, border, x,
                             ct.W5_TOP1 - ct.W5_CARD_H)
    for (name, fill, border, _fn), x in zip(ct.W5_CARDS[3:], ct.W5_ROW2_XS):
        ct.draw_weather_card(pdf, name, fill, border, x,
                             ct.W5_TOP2 - ct.W5_CARD_H)
    ct.draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    # (title, builder, locked) — BOTH PAGES APPROVED by user 2026-10-01.
    ("Seasons of the Year", build_p1_seasons, True),
    ("What\u2019s the Weather?", build_p2_weather, True),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="weather-seasons-")
    splitdir = tempfile.mkdtemp(prefix="weather-seasons-split-")
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
