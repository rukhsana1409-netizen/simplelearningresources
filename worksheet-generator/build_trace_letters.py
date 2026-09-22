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
                     top: float) -> None:
    pdf.setStrokeColor(LINE_BLUE)
    pdf.setLineWidth(1.4)
    pdf.line(x1, top, x2, top)
    pdf.line(x1, y_base, x2, y_base)
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
    "B": [[(0.15, 0.0), (0.15, 1.0)],
          _arc_points(0.15, 0.76, 0.44, 0.24, 90, -90),
          _arc_points(0.15, 0.26, 0.48, 0.26, 90, -90)],
    "b": [[(0.22, 0.0), (0.22, 1.0)],
          _arc_points(0.52, 0.25, 0.30, 0.23, 0, 360)],
    "C": [_arc_points(0.52, 0.50, 0.40, 0.48, 55, 305)],
    "c": [_arc_points(0.46, 0.25, 0.32, 0.24, 55, 305)],
}


def draw_dotted_letters(pdf: canvas.Canvas, letters: list, x_start: float,
                        x_end: float, baseline: float, cap_height: float) -> None:
    """Draw single-line dotted tracing letters, one centered per equal slot."""
    pdf.saveState()
    pdf.setStrokeColor(TRACE_STROKE)
    pdf.setLineWidth(7.5)
    pdf.setLineCap(1)   # round caps -> clean dots
    pdf.setLineJoin(1)  # round joins
    pdf.setDash(0.5, 8.5)
    n = len(letters)
    slot = (x_end - x_start) / n
    box_w = slot * 0.66
    for i, letter in enumerate(letters):
        strokes = DOTTED_LETTERS[letter]
        xs = [p[0] for s in strokes for p in s]
        minx, maxx = min(xs), max(xs)
        span = maxx - minx if maxx > minx else 1.0
        cx = x_start + slot * (i + 0.5)
        ox = cx - box_w / 2 - minx * (box_w / span)
        k = box_w / span
        for stroke in strokes:
            p = pdf.beginPath()
            for j, (ux, uy) in enumerate(stroke):
                x = ox + ux * k
                y = baseline + uy * cap_height
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
    draw_guide_lines(pdf, baseline, x1, x2, baseline + cap)
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
    draw_guide_lines(pdf, 55, MARGIN, PAGE_WIDTH - MARGIN, 55 + 46)

    draw_footer(pdf)
    pdf.showPage()


TRACE_LETTERS = [
    {"upper": "A", "lower": "a", "word": "Airplane", "asset": "a-airplane"},
    {"upper": "B", "lower": "b", "word": "Bear", "asset": "b-bear"},
    {"upper": "C", "lower": "c", "word": "Cow", "asset": "c-cow"},
]


def build(out_path: str) -> None:
    pdf = canvas.Canvas(out_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle("Trace My Letters A-Z (A-C) | Learning Made Simple")
    for spec in TRACE_LETTERS:
        draw_trace_page(pdf, spec)
    pdf.save()
    print(f"wrote {out_path} ({len(TRACE_LETTERS)} pages)")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "trace-my-letters-abc-prototype.pdf",
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build(out)
