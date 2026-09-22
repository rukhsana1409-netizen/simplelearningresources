"""Build Trace My Letters A-Z prototype pages (one letter per page).

Learning Made Simple branding (header, footer, palette) reused from
generate_worksheet.py. Each page: large uppercase+lowercase target pair,
one large beginning-sound picture with word label, a "Trace the letters"
section with a few LARGE dashed-outline tracing repetitions on handwriting
guide lines (generous space, not rows of tiny letters), and a small final
"Write it yourself" area with blank handwriting lines.
"""

from __future__ import annotations

import math
import os
import sys

from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_worksheet import (  # noqa: E402
    INK,
    MARGIN,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    TEAL,
    TEAL_DARK,
    draw_footer,
    draw_header,
)

TRACE_STROKE = HexColor("#6FA8A0")
LINE_BLUE = HexColor("#9DC3D8")
LINE_RED = HexColor("#E8A49B")

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "letters")

# Build-time conversion: source illustrations are large WebP files; embedding
# them directly balloons the PDF. Convert once per build to print-sized JPEGs.
_CONVERT_DIR = os.path.join("/tmp", "trace_assets_jpg")
_CONVERTED: dict = {}


def asset_path(stem: str) -> str:
    if stem in _CONVERTED:
        return _CONVERTED[stem]
    path = os.path.join(ASSETS, f"{stem}.webp")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No illustration asset for {stem!r}")
    from PIL import Image
    os.makedirs(_CONVERT_DIR, exist_ok=True)
    dst = os.path.join(_CONVERT_DIR, f"{stem}.jpg")
    im = Image.open(path).convert("RGB")
    im.thumbnail((600, 600), Image.LANCZOS)
    im.save(dst, "JPEG", quality=82)
    _CONVERTED[stem] = dst
    return dst


def draw_big_letters(pdf: canvas.Canvas, upper: str, lower: str,
                     cx: float, baseline: float, size: float = 96) -> None:
    text = upper + "  " + lower
    w = stringWidth(text, "Helvetica-Bold", size)
    x = cx - w / 2
    pdf.setFont("Helvetica-Bold", size)
    pdf.setFillColor(TEAL_DARK)
    pdf.drawString(x, baseline, upper + "  ")
    w_upper = stringWidth(upper + "  ", "Helvetica-Bold", size)
    pdf.setFillColor(TEAL)
    pdf.drawString(x + w_upper, baseline, lower)


def draw_picture(pdf: canvas.Canvas, stem: str, word: str,
                 cx: float, img_y: float, box: float = 190) -> None:
    img = ImageReader(asset_path(stem))
    pdf.drawImage(img, cx - box / 2, img_y, width=box, height=box,
                  preserveAspectRatio=True, anchor="c", mask="auto")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(cx, img_y - 22, word)


def draw_guide_lines(pdf: canvas.Canvas, y_base: float, x1: float, x2: float,
                     top: float, descender: float | None = None) -> None:
    pdf.setStrokeColor(LINE_BLUE)
    pdf.setLineWidth(1.4)
    pdf.line(x1, top, x2, top)
    pdf.line(x1, y_base, x2, y_base)
    if descender is not None:
        pdf.line(x1, descender, x2, descender)
    pdf.setStrokeColor(LINE_RED)
    pdf.setLineWidth(1.1)
    pdf.setDash(7, 5)
    pdf.line(x1, y_base + (top - y_base) / 2, x2, y_base + (top - y_base) / 2)
    pdf.setDash()


def _arc_points(cx, cy, rx, ry, start_deg, end_deg, n=40):
    pts = []
    for i in range(n + 1):
        a = math.radians(start_deg + (end_deg - start_deg) * i / n)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return pts


# Each letter = list of single centerline strokes, in a 0..1 box
# (x: 0..1 across, y: 0 = baseline, 1 = cap-height line). Lowercase bodies
# sit between baseline (0) and the midline (0.5); ascenders reach 1.0.
DOTTED_LETTERS = {
    "A": [[(0.08, 0.0), (0.50, 1.0)],
          [(0.92, 0.0), (0.50, 1.0)],
          [(0.30, 0.38), (0.70, 0.38)]],
    "a": [_arc_points(0.42, 0.25, 0.28, 0.24, 0, 360),
          [(0.70, 0.0), (0.70, 0.50)]],
    "B": [[(0.12, 0.0), (0.12, 1.0)],
          _arc_points(0.12, 0.75, 0.55, 0.25, 90, -90),
          _arc_points(0.12, 0.25, 0.60, 0.25, 90, -90)],
    "b": [[(0.22, 0.0), (0.22, 1.0)],
          _arc_points(0.52, 0.25, 0.30, 0.23, 0, 360)],
    "C": [_arc_points(0.52, 0.50, 0.40, 0.48, 55, 305)],
    "c": [_arc_points(0.46, 0.25, 0.32, 0.24, 55, 305)],
}

# D-Z single-stroke centerline paths (added 2026-09-22), same 0..1 box.
# Descenders (g, j, p, q, y) reach uy < 0 and get a descender guide line.
DOTTED_LETTERS.update({
    "D": [[(0.12, 0.0), (0.12, 1.0)],
          _arc_points(0.12, 0.50, 0.58, 0.50, 90, -90)],
    "d": [_arc_points(0.40, 0.25, 0.28, 0.24, 0, 360),
          [(0.68, 0.0), (0.68, 1.0)]],
    "E": [[(0.15, 0.0), (0.15, 1.0)],
          [(0.15, 1.0), (0.72, 1.0)],
          [(0.15, 0.52), (0.62, 0.52)],
          [(0.15, 0.0), (0.72, 0.0)]],
    "e": [_arc_points(0.43, 0.25, 0.27, 0.23, 60, 300),
          [(0.20, 0.28), (0.66, 0.28)]],
    "F": [[(0.15, 0.0), (0.15, 1.0)],
          [(0.15, 1.0), (0.72, 1.0)],
          [(0.15, 0.55), (0.60, 0.55)]],
    "f": [[(0.45, 0.0), (0.45, 0.82)],
          _arc_points(0.58, 0.82, 0.13, 0.18, 180, 90),
          [(0.28, 0.55), (0.62, 0.55)]],
    "G": [_arc_points(0.52, 0.50, 0.40, 0.48, 55, 305),
          [(0.55, 0.40), (0.82, 0.40)]],
    "g": [_arc_points(0.42, 0.25, 0.28, 0.24, 0, 360),
          [(0.70, 0.42), (0.70, -0.15)],
          _arc_points(0.55, -0.15, 0.15, 0.18, 0, -90)],
    "H": [[(0.15, 0.0), (0.15, 1.0)],
          [(0.75, 0.0), (0.75, 1.0)],
          [(0.15, 0.50), (0.75, 0.50)]],
    "h": [[(0.20, 0.0), (0.20, 1.0)],
          _arc_points(0.48, 0.25, 0.28, 0.25, 180, 0),
          [(0.76, 0.25), (0.76, 0.0)]],
    "I": [[(0.25, 1.0), (0.65, 1.0)],
          [(0.45, 0.0), (0.45, 1.0)],
          [(0.25, 0.0), (0.65, 0.0)]],
    "i": [[(0.40, 0.0), (0.40, 0.50)],
          _arc_points(0.40, 0.68, 0.035, 0.035, 0, 360)],
    "J": [[(0.30, 1.0), (0.70, 1.0)],
          [(0.55, 1.0), (0.55, 0.25)],
          _arc_points(0.40, 0.25, 0.15, 0.25, 0, -90)],
    "j": [[(0.45, 0.50), (0.45, -0.20)],
          _arc_points(0.32, -0.20, 0.13, 0.20, 0, -90),
          _arc_points(0.45, 0.68, 0.035, 0.035, 0, 360)],
    "K": [[(0.15, 0.0), (0.15, 1.0)],
          [(0.70, 1.0), (0.15, 0.45)],
          [(0.15, 0.45), (0.70, 0.0)]],
    "k": [[(0.20, 0.0), (0.20, 0.75)],
          [(0.62, 0.75), (0.20, 0.32)],
          [(0.20, 0.32), (0.62, 0.0)]],
    "L": [[(0.15, 0.0), (0.15, 1.0)],
          [(0.15, 0.0), (0.68, 0.0)]],
    "l": [[(0.40, 0.0), (0.40, 1.0)]],
    "M": [[(0.10, 0.0), (0.10, 1.0), (0.50, 0.45), (0.90, 1.0), (0.90, 0.0)]],
    "m": [[(0.15, 0.0), (0.15, 0.50)],
          _arc_points(0.35, 0.25, 0.20, 0.25, 180, 0),
          [(0.55, 0.25), (0.55, 0.0)],
          _arc_points(0.75, 0.25, 0.20, 0.25, 180, 0),
          [(0.95, 0.25), (0.95, 0.0)]],
    "N": [[(0.12, 0.0), (0.12, 1.0), (0.78, 0.0), (0.78, 1.0)]],
    "n": [[(0.18, 0.0), (0.18, 0.50)],
          _arc_points(0.46, 0.25, 0.28, 0.25, 180, 0),
          [(0.74, 0.25), (0.74, 0.0)]],
    "O": [_arc_points(0.50, 0.50, 0.34, 0.48, 0, 360)],
    "o": [_arc_points(0.45, 0.25, 0.28, 0.24, 0, 360)],
    "P": [[(0.15, 0.0), (0.15, 1.0)],
          _arc_points(0.15, 0.74, 0.55, 0.26, 90, -90)],
    "p": [[(0.25, 0.50), (0.25, -0.50)],
          _arc_points(0.53, 0.25, 0.28, 0.24, 0, 360)],
    "Q": [_arc_points(0.48, 0.52, 0.34, 0.46, 0, 360),
          [(0.62, 0.28), (0.80, 0.05)]],
    "q": [_arc_points(0.37, 0.25, 0.28, 0.24, 0, 360),
          [(0.65, 0.50), (0.65, -0.50)]],
    "R": [[(0.15, 0.0), (0.15, 1.0)],
          _arc_points(0.15, 0.74, 0.55, 0.26, 90, -90),
          [(0.45, 0.50), (0.72, 0.0)]],
    "r": [[(0.22, 0.0), (0.22, 0.50)],
          _arc_points(0.42, 0.30, 0.20, 0.20, 180, 20)],
    "S": [_arc_points(0.50, 0.75, 0.30, 0.25, 45, 270),
          _arc_points(0.50, 0.25, 0.30, 0.25, 90, -135)],
    "s": [_arc_points(0.50, 0.375, 0.30, 0.125, 45, 270),
          _arc_points(0.50, 0.125, 0.30, 0.125, 90, -135)],
    "T": [[(0.20, 1.0), (0.80, 1.0)],
          [(0.50, 1.0), (0.50, 0.0)]],
    "t": [[(0.45, 0.80), (0.45, 0.10)],
          _arc_points(0.55, 0.10, 0.10, 0.10, 180, 360),
          [(0.25, 0.58), (0.65, 0.58)]],
    "U": [[(0.15, 1.0), (0.15, 0.35)],
          _arc_points(0.45, 0.35, 0.30, 0.35, 180, 360),
          [(0.75, 0.35), (0.75, 1.0)]],
    "u": [[(0.20, 0.50), (0.20, 0.18)],
          _arc_points(0.45, 0.18, 0.25, 0.18, 180, 360),
          [(0.70, 0.18), (0.70, 0.50)]],
    "V": [[(0.10, 1.0), (0.50, 0.0), (0.90, 1.0)]],
    "v": [[(0.15, 0.50), (0.45, 0.0), (0.75, 0.50)]],
    "W": [[(0.05, 1.0), (0.28, 0.0), (0.50, 0.62), (0.72, 0.0), (0.95, 1.0)]],
    "w": [[(0.05, 0.50), (0.27, 0.0), (0.50, 0.32), (0.73, 0.0), (0.95, 0.50)]],
    "X": [[(0.15, 0.0), (0.85, 1.0)],
          [(0.15, 1.0), (0.85, 0.0)]],
    "x": [[(0.20, 0.0), (0.70, 0.50)],
          [(0.20, 0.50), (0.70, 0.0)]],
    "Y": [[(0.12, 1.0), (0.50, 0.55)],
          [(0.88, 1.0), (0.50, 0.55)],
          [(0.50, 0.55), (0.50, 0.0)]],
    "y": [[(0.15, 0.50), (0.45, 0.02)],
          [(0.75, 0.50), (0.45, 0.02), (0.38, -0.30), (0.30, -0.38)]],
    "Z": [[(0.15, 1.0), (0.85, 1.0), (0.15, 0.0), (0.85, 0.0)]],
    "z": [[(0.18, 0.50), (0.72, 0.50), (0.18, 0.0), (0.72, 0.0)]],
})


def draw_dotted_letters(pdf: canvas.Canvas, letters: list, x_start: float,
                        x_end: float, baseline: float, cap_height: float) -> None:
    """Draw single-stroke dotted tracing letters, one centered per equal slot.

    Uniform scale (1 unit = cap height) so every letter keeps its natural
    proportions -- no stretched outlines.
    """
    pdf.saveState()
    pdf.setStrokeColor(TRACE_STROKE)
    pdf.setLineWidth(7)
    pdf.setLineCap(1)   # round caps -> clean dots
    pdf.setLineJoin(1)  # round joins
    pdf.setDash(0.5, 8)
    n = len(letters)
    slot = (x_end - x_start) / n
    k = cap_height  # uniform scale for x and y
    for i, letter in enumerate(letters):
        strokes = DOTTED_LETTERS[letter]
        xs = [p[0] for s in strokes for p in s]
        minx, maxx = min(xs), max(xs)
        w = (maxx - minx) * k
        cx = x_start + slot * (i + 0.5)
        ox = cx - w / 2 - minx * k
        for stroke in strokes:
            p = pdf.beginPath()
            for j, (ux, uy) in enumerate(stroke):
                x = ox + ux * k
                y = baseline + uy * k
                if j == 0:
                    p.moveTo(x, y)
                else:
                    p.lineTo(x, y)
            pdf.drawPath(p, fill=0, stroke=1)
    pdf.restoreState()


def draw_trace_row(pdf: canvas.Canvas, letters: list, baseline: float,
                   size: float = 84) -> None:
    x1, x2 = MARGIN, PAGE_WIDTH - MARGIN
    cap = size * 0.72
    desc = any(uy < 0 for L in letters for s in DOTTED_LETTERS[L]
               for _, uy in s)
    draw_guide_lines(pdf, baseline, x1, x2, baseline + cap,
                     descender=(baseline - cap * 0.5) if desc else None)
    draw_dotted_letters(pdf, letters, x1, x2, baseline, cap)


def draw_trace_page(pdf: canvas.Canvas, spec: dict) -> None:
    data = {
        "title": "Trace My Letters: A-Z",
        "subtitle": "Preschool Reading & Language",
        "template": "trace-letters-pack",
    }
    draw_header(pdf, data)

    # Large target pair (left) + big picture with label (right).
    draw_big_letters(pdf, spec["upper"], spec["lower"], cx=165, baseline=540)
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(425, 598, f"{spec['upper']} is for {spec['word']}")
    draw_picture(pdf, spec["asset"], spec["word"], cx=425, img_y=388, box=188)

    # Trace section: a few large dashed repetitions with generous space.
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(MARGIN, 342, "Trace the letters.")
    draw_trace_row(pdf, [spec["upper"]] * 4, baseline=258)
    draw_trace_row(pdf, [spec["lower"]] * 4, baseline=163)

    # Small final "write it yourself" area with blank handwriting lines.
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(MARGIN, 126, "Write it yourself.")
    lower_desc = any(uy < 0 for s in DOTTED_LETTERS[spec["lower"]]
                     for _, uy in s)
    draw_guide_lines(pdf, 55, MARGIN, PAGE_WIDTH - MARGIN, 55 + 46,
                     descender=32 if lower_desc else None)

    draw_footer(pdf)
    pdf.showPage()


TRACE_LETTERS = [
    {"upper": "A", "lower": "a", "word": "Airplane", "asset": "a-airplane"},
    {"upper": "B", "lower": "b", "word": "Bear", "asset": "b-bear"},
    {"upper": "C", "lower": "c", "word": "Cow", "asset": "c-cow"},
    {"upper": "D", "lower": "d", "word": "Dog", "asset": "d-dog"},
    {"upper": "E", "lower": "e", "word": "Elephant", "asset": "e-elephant"},
    {"upper": "F", "lower": "f", "word": "Fish", "asset": "f-fish"},
    {"upper": "G", "lower": "g", "word": "Grapes", "asset": "g-grapes"},
    {"upper": "H", "lower": "h", "word": "Hat", "asset": "h-hat"},
    {"upper": "I", "lower": "i", "word": "Ice cream", "asset": "i-ice-cream"},
    {"upper": "J", "lower": "j", "word": "Jellyfish", "asset": "j-jellyfish"},
    {"upper": "K", "lower": "k", "word": "Kite", "asset": "k-kite"},
    {"upper": "L", "lower": "l", "word": "Lion", "asset": "l-lion"},
    {"upper": "M", "lower": "m", "word": "Monkey", "asset": "m-monkey"},
    {"upper": "N", "lower": "n", "word": "Nest", "asset": "n-nest"},
    {"upper": "O", "lower": "o", "word": "Orange", "asset": "o-orange"},
    {"upper": "P", "lower": "p", "word": "Pig", "asset": "p-pig"},
    {"upper": "Q", "lower": "q", "word": "Queen", "asset": "q-queen"},
    {"upper": "R", "lower": "r", "word": "Rabbit", "asset": "r-rabbit"},
    {"upper": "S", "lower": "s", "word": "Sun", "asset": "s-sun"},
    {"upper": "T", "lower": "t", "word": "Tiger", "asset": "t-tiger"},
    {"upper": "U", "lower": "u", "word": "Umbrella", "asset": "u-umbrella"},
    {"upper": "V", "lower": "v", "word": "Van", "asset": "v-van"},
    {"upper": "W", "lower": "w", "word": "Whale", "asset": "w-whale"},
    {"upper": "X", "lower": "x", "word": "X-ray Fish", "asset": "x-xray-fish"},
    {"upper": "Y", "lower": "y", "word": "Yo-yo", "asset": "y-yo-yo"},
    {"upper": "Z", "lower": "z", "word": "Zebra", "asset": "z-zebra"},
]


def build(out_path: str) -> None:
    pdf = canvas.Canvas(out_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle("Trace My Letters A-Z | Learning Made Simple")
    for spec in TRACE_LETTERS:
        draw_trace_page(pdf, spec)
    pdf.save()
    print(f"wrote {out_path} ({len(TRACE_LETTERS)} pages)")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "trace-my-letters-prototype.pdf",
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build(out)
