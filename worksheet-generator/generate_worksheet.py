"""Generate clean, print-ready Learning Made Simple worksheets from JSON content."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 40
TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
INK = HexColor("#202A33")
MUTED = HexColor("#55606C")
BORDER = HexColor("#B9D7D2")
PALE_TEAL = HexColor("#F2FAF8")
FOOTER = HexColor("#EEF8F6")
GOLD = HexColor("#F4B63E")


def draw_logo(pdf: canvas.Canvas, x: float, y: float) -> None:
    """Draw a compact, vector-only Learning Made Simple mark and wordmark."""
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


def draw_header(pdf: canvas.Canvas, data: dict) -> None:
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, fill=1, stroke=0)
    draw_logo(pdf, MARGIN, PAGE_HEIGHT - 86)
    divider_x = 210
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1)
    pdf.line(divider_x, PAGE_HEIGHT - 46, divider_x, PAGE_HEIGHT - 106)
    title_x = divider_x + 19
    prefix, focus = data["title"].split(": ", 1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(title_x, PAGE_HEIGHT - 67, prefix + ":")
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(title_x, PAGE_HEIGHT - 98, focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11.5)
    pdf.drawString(title_x, PAGE_HEIGHT - 116, data["subtitle"])
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    pdf.line(MARGIN, PAGE_HEIGHT - 131, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 131)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(MARGIN, PAGE_HEIGHT - 160, "Name:")
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(.9)
    pdf.line(MARGIN + 37, PAGE_HEIGHT - 163, 315, PAGE_HEIGHT - 163)
    pdf.setFillColor(INK)
    pdf.drawString(430, PAGE_HEIGHT - 160, "Date:")
    pdf.setStrokeColor(BORDER)
    pdf.line(463, PAGE_HEIGHT - 163, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 163)


def section_heading(pdf: canvas.Canvas, number: int, title: str, prompt: str, y: float) -> None:
    pdf.setFillColor(TEAL)
    pdf.circle(MARGIN + 15, y, 15, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(MARGIN + 15, y - 4.5, str(number))
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(MARGIN + 37, y - 4, title)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 10.5)
    pdf.drawString(MARGIN + 37, y - 21, prompt)


def draw_number_cards(pdf: canvas.Canvas, values: list[int], y_top: float, columns: int, height: float, font_size: int, target: int) -> None:
    gap = 10
    width = (PAGE_WIDTH - (2 * MARGIN) - gap * (columns - 1)) / columns
    for index, value in enumerate(values):
        row, col = divmod(index, columns)
        x = MARGIN + col * (width + gap)
        y = y_top - row * (height + gap) - height
        pdf.setFillColor(PALE_TEAL if value == target else white)
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.1)
        pdf.roundRect(x, y, width, height, 10, fill=1, stroke=1)
        pdf.setFillColor(TEAL if value == target else INK)
        pdf.setFont("Helvetica-Bold", font_size)
        pdf.drawCentredString(x + width / 2, y + (height - font_size) / 2 + 2, str(value))


def draw_handwriting_bands(pdf: canvas.Canvas, target: int) -> None:
    left, right = MARGIN + 10, PAGE_WIDTH - MARGIN - 10
    for index, top in enumerate([173, 111]):
        bottom, middle = top - 48, top - 24
        pdf.setStrokeColor(TEAL)
        pdf.setLineWidth(1.1)
        pdf.line(left, top, right, top)
        pdf.line(left, bottom, right, bottom)
        pdf.setStrokeColor(BORDER)
        pdf.setDash(4, 4)
        pdf.line(left, middle, right, middle)
        pdf.setDash()
        slot_width = (right - left) / 6
        for position in range(6):
            center_x = left + slot_width * (position + .5)
            baseline = bottom + 4
            if position == 0:
                pdf.setFillColor(INK)
                pdf.setFont("Helvetica", 41)
                pdf.drawCentredString(center_x, baseline, str(target))
                continue
            pdf.setStrokeColor(INK)
            pdf.setLineWidth(.8)
            pdf.setLineCap(1)
            pdf.setDash(1.3, 2.2)
            traced = pdf.beginText()
            traced.setTextOrigin(center_x - stringWidth(str(target), "Helvetica", 41) / 2, baseline)
            traced.setFont("Helvetica", 41)
            traced.setTextRenderMode(1)
            traced.textOut(str(target))
            traced.setTextRenderMode(0)
            pdf.drawText(traced)
            pdf.setDash()


def draw_footer(pdf: canvas.Canvas) -> None:
    pdf.setFillColor(FOOTER)
    pdf.rect(0, 0, PAGE_WIDTH, 37, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.circle(MARGIN + 10, 18.5, 9, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(MARGIN + 10, 15, "L")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(MARGIN + 26, 15, "Learning Made Simple")
    pdf.setStrokeColor(BORDER)
    pdf.line(201, 10, 201, 27)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(224, 14, "♥")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(243, 15, "Made with love for little learners.")
    pdf.drawRightString(PAGE_WIDTH - MARGIN, 15, "© Learning Made Simple")


def build_pdf(data: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output_path), pagesize=letter, pageCompression=1)
    pdf.setTitle(data["title"] + " | Learning Made Simple")
    pdf.setAuthor("Learning Made Simple")
    draw_header(pdf, data)
    trace = data["activities"]["trace"]
    section_heading(pdf, 1, trace["title"], trace["prompt"], 586)
    target = int(data["activities"]["find"]["target"])
    draw_number_cards(pdf, trace["items"], 549, 5, 58, 26, target)
    find = data["activities"]["find"]
    section_heading(pdf, 2, find["title"], find["prompt"], 395)
    draw_number_cards(pdf, find["choices"], 358, 6, 42, 22, target)
    write = data["activities"]["write"]
    section_heading(pdf, 3, write["title"], write["prompt"], 216)
    draw_handwriting_bands(pdf, int(write["items"][0]))
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: py -3 generate_worksheet.py content/worksheet.json")
    source_path = Path(sys.argv[1])
    data = json.loads(source_path.read_text(encoding="utf-8"))
    build_pdf(data, Path(__file__).parent / "output" / data["filename"])


if __name__ == "__main__":
    main()
