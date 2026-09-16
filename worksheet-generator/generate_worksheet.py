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
CORAL = HexColor("#E98779")
CROSSOUT_RED = HexColor("#D94B45")
GREEN = HexColor("#72AE72")
BLUE = HexColor("#82B7D8")
PURPLE = HexColor("#AA91C4")
ORANGE = HexColor("#E9A25D")


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
    compact = data.get("template") in {"counting", "counting-pack"}
    addition = data.get("template") in {
        "addition-pack", "subtraction-pack", "arithmetic-facts-pack", "story-problems-sample"
    }
    logo_y = PAGE_HEIGHT - (76 if compact else 86)
    divider_top = PAGE_HEIGHT - (38 if compact else 46)
    divider_bottom = PAGE_HEIGHT - (102 if compact else 106)
    title_y = PAGE_HEIGHT - (63 if compact else 67)
    focus_y = PAGE_HEIGHT - (90 if compact else 98)
    subtitle_y = PAGE_HEIGHT - (92 if compact else 116)
    rule_y = PAGE_HEIGHT - (109 if compact else 131)
    fields_y = PAGE_HEIGHT - (136 if compact else 160)
    fields_rule_y = PAGE_HEIGHT - (139 if compact else 163)
    if addition:
        subtitle_y = PAGE_HEIGHT - 92
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, fill=1, stroke=0)
    draw_logo(pdf, MARGIN, logo_y)
    divider_x = 210
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1)
    pdf.line(divider_x, divider_top, divider_x, divider_bottom)
    title_x = divider_x + 19
    title_parts = data["title"].split(": ", 1)
    prefix, focus = title_parts if len(title_parts) == 2 else (data["title"], "")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 25 if addition else (23 if compact else 22))
    pdf.drawString(title_x, title_y, prefix + (":" if focus else ""))
    if focus:
        pdf.setFont("Helvetica-Bold", 30)
        pdf.drawString(title_x, focus_y, focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold" if compact or addition else "Helvetica", 11.5)
    pdf.drawString(title_x, subtitle_y, data["subtitle"])
    if addition:
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica", 10.5)
        pdf.drawString(title_x, subtitle_y - 19, data["page_instruction"])
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    pdf.line(MARGIN, rule_y, PAGE_WIDTH - MARGIN, rule_y)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(MARGIN, fields_y, "Name:")
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(.9)
    pdf.line(MARGIN + 37, fields_rule_y, 315, fields_rule_y)
    pdf.setFillColor(INK)
    pdf.drawString(430, fields_y, "Date:")
    pdf.setStrokeColor(BORDER)
    pdf.line(463, fields_rule_y, PAGE_WIDTH - MARGIN, fields_rule_y)


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


def draw_spot_it_cards(pdf: canvas.Canvas, values: list[int], y_top: float) -> None:
    """Draw large, neutral numeral cards without revealing the answers."""
    columns, gap, height = 4, 14, 58
    width = (PAGE_WIDTH - 2 * MARGIN - gap * (columns - 1)) / columns
    for index, value in enumerate(values):
        row, col = divmod(index, columns)
        x = MARGIN + col * (width + gap)
        y = y_top - row * (height + 12) - height
        pdf.setFillColor(white)
        pdf.setStrokeColor((TEAL, GOLD, CORAL, BLUE)[index % 4])
        pdf.setLineWidth(1.5)
        pdf.roundRect(x, y, width, height, 10, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 30)
        pdf.drawCentredString(x + width / 2, y + 17, str(value))


def draw_quantity_choices(pdf: canvas.Canvas, groups: list[dict], y: float) -> None:
    """Draw three spacious object-group choices for quantity recognition."""
    gap, width, height = 16, (PAGE_WIDTH - 2 * MARGIN - 32) / 3, 108
    for index, group in enumerate(groups):
        x = MARGIN + index * (width + gap)
        pdf.setFillColor(PALE_TEAL if index % 2 == 0 else white)
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.3)
        pdf.roundRect(x, y, width, height, 12, fill=1, stroke=1)
        draw_object_group(pdf, group, x + 10, y + 10, width - 20, height - 20)


def draw_trace_boxes(pdf: canvas.Canvas, target: int, y: float) -> None:
    """Provide five large boxes containing clear dotted tracing numerals."""
    count, gap, height = 5, 10, 102
    width = (PAGE_WIDTH - 2 * MARGIN - gap * (count - 1)) / count
    for index in range(count):
        x = MARGIN + index * (width + gap)
        pdf.setFillColor(PALE_TEAL if index % 2 == 0 else white)
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, y, width, height, 10, fill=1, stroke=1)
        font_size = 56 if target < 10 else 49
        baseline = y + (height - font_size) / 2 + 4
        pdf.setStrokeColor(TEAL_DARK)
        pdf.setLineWidth(1.15)
        pdf.setDash(2.2, 2.6)
        traced = pdf.beginText()
        traced.setTextOrigin(x + (width - stringWidth(str(target), "Helvetica-Bold", font_size)) / 2, baseline)
        traced.setFont("Helvetica-Bold", font_size)
        traced.setTextRenderMode(1)
        traced.textOut(str(target))
        traced.setTextRenderMode(0)
        pdf.drawText(traced)
        pdf.setDash()


def validate_number_recognition_pack(data: dict) -> None:
    pages = data.get("pages")
    if not isinstance(pages, list) or len(pages) != 5:
        raise ValueError("A number recognition pack must contain exactly five pages.")
    expected = list(range(data["range_start"], data["range_end"] + 1))
    targets = [page.get("target") for page in pages]
    if len(expected) != 5 or targets != expected:
        raise ValueError(f"Number recognition targets must be in order: {expected}.")
    for page in pages:
        target = page["target"]
        spot_values = page.get("spot_values", [])
        groups = page.get("quantity_groups", [])
        if len(spot_values) != 8 or spot_values.count(target) < 2:
            raise ValueError(f"Number {target} requires eight Spot It values with repeated targets.")
        if len(groups) != 3 or sum(group["count"] == target for group in groups) != 1:
            raise ValueError(f"Number {target} requires three quantity groups and one correct answer.")
        if any(group["count"] < 1 or group["count"] > 20 for group in groups):
            raise ValueError("Number recognition quantity groups must use counts from 1 through 20.")


def build_number_recognition_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_number_recognition_pack(data)
    for page in data["pages"]:
        target = page["target"]
        object_word = "object" if target == 1 else "objects"
        draw_header(pdf, {
            **data,
            "title": f"Number Recognition: {target}",
            "subtitle": f"Find, count, trace, and practice the number {target}.",
        })
        section_heading(pdf, 1, "Spot It", f"Circle every {target}.", 610)
        draw_spot_it_cards(pdf, page["spot_values"], 570)
        section_heading(pdf, 2, "Find It", f"Circle the group with {target} {object_word}.", 408)
        draw_quantity_choices(pdf, page["quantity_groups"], 266)
        section_heading(pdf, 3, "Trace the Number", f"Trace the number {target} in each box.", 225)
        draw_trace_boxes(pdf, target, 72)
        draw_footer(pdf)
        pdf.showPage()


def draw_footer(pdf: canvas.Canvas) -> None:
    pdf.setFillColor(FOOTER)
    pdf.rect(0, 0, PAGE_WIDTH, 37, fill=1, stroke=0)
    pdf.setFillColor(TEAL_DARK)
    pdf.circle(MARGIN + 10, 18.5, 9, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(MARGIN + 10, 15, "L")
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(MARGIN + 26, 15, "Learning Made Simple")
    pdf.setStrokeColor(BORDER)
    pdf.line(201, 10, 201, 27)
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(224, 14, "*")
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(243, 15, "Made with love for little learners.")
    pdf.drawRightString(PAGE_WIDTH - MARGIN, 15, "\u00a9 2026 Learning Made Simple")


def draw_object(pdf: canvas.Canvas, kind: str, x: float, y: float, size: float) -> None:
    """Draw one simple, original counting object centered at x/y."""
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    if kind == "apple":
        pdf.setFillColor(CORAL)
        pdf.circle(x, y, size * .38, fill=1, stroke=1)
        pdf.line(x, y + size * .36, x + size * .07, y + size * .56)
        pdf.setFillColor(GREEN)
        pdf.ellipse(x + size * .02, y + size * .39, x + size * .3, y + size * .56, fill=1, stroke=1)
    elif kind == "star":
        import math
        pdf.setFillColor(GOLD)
        path = pdf.beginPath()
        for index in range(10):
            angle = math.radians(90 + index * 36)
            radius = size * (.48 if index % 2 == 0 else .22)
            px, py = x + radius * math.cos(angle), y + radius * math.sin(angle)
            (path.moveTo if index == 0 else path.lineTo)(px, py)
        path.close()
        pdf.drawPath(path, fill=1, stroke=1)
    elif kind == "balloon":
        pdf.setFillColor(BLUE)
        pdf.ellipse(x - size * .31, y - size * .18, x + size * .31, y + size * .43, fill=1, stroke=1)
        pdf.line(x, y - size * .18, x - size * .05, y - size * .42)
    elif kind == "flower":
        pdf.setFillColor(PURPLE)
        for dx, dy in ((0, .28), (.27, 0), (0, -.28), (-.27, 0)):
            pdf.circle(x + dx * size, y + dy * size, size * .19, fill=1, stroke=1)
        pdf.setFillColor(GOLD)
        pdf.circle(x, y, size * .16, fill=1, stroke=1)
    elif kind == "fish":
        pdf.setFillColor(BLUE)
        pdf.ellipse(x - size * .34, y - size * .2, x + size * .28, y + size * .2, fill=1, stroke=1)
        path = pdf.beginPath()
        path.moveTo(x + size * .28, y)
        path.lineTo(x + size * .52, y + size * .24)
        path.lineTo(x + size * .52, y - size * .24)
        path.close()
        pdf.drawPath(path, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.circle(x - size * .18, y + size * .05, 1.3, fill=1, stroke=0)
    elif kind == "leaf":
        pdf.setFillColor(GREEN)
        path = pdf.beginPath()
        path.moveTo(x - size * .42, y - size * .12)
        path.curveTo(x - size * .2, y + size * .5, x + size * .3, y + size * .45, x + size * .43, y)
        path.curveTo(x + size * .2, y - size * .4, x - size * .2, y - size * .4, x - size * .42, y - size * .12)
        path.close()
        pdf.drawPath(path, fill=1, stroke=1)
        pdf.line(x - size * .27, y - size * .08, x + size * .28, y + size * .12)
    elif kind == "car":
        pdf.setFillColor(CORAL)
        pdf.roundRect(x - size * .48, y - size * .18, size * .96, size * .38, size * .08, fill=1, stroke=1)
        pdf.setFillColor(ORANGE)
        pdf.roundRect(x - size * .22, y + size * .12, size * .47, size * .25, size * .06, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.circle(x - size * .28, y - size * .2, size * .12, fill=1, stroke=1)
        pdf.circle(x + size * .28, y - size * .2, size * .12, fill=1, stroke=1)
        pdf.setFillColor(white)
        pdf.circle(x - size * .28, y - size * .2, size * .045, fill=1, stroke=0)
        pdf.circle(x + size * .28, y - size * .2, size * .045, fill=1, stroke=0)
    elif kind == "butterfly":
        pdf.setFillColor(PURPLE)
        pdf.ellipse(x - size * .43, y, x - size * .02, y + size * .38, fill=1, stroke=1)
        pdf.ellipse(x + size * .02, y, x + size * .43, y + size * .38, fill=1, stroke=1)
        pdf.setFillColor(CORAL)
        pdf.ellipse(x - size * .35, y - size * .3, x - size * .02, y + size * .04, fill=1, stroke=1)
        pdf.ellipse(x + size * .02, y - size * .3, x + size * .35, y + size * .04, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.roundRect(x - size * .045, y - size * .28, size * .09, size * .55, size * .04, fill=1, stroke=0)
        pdf.line(x, y + size * .25, x - size * .14, y + size * .43)
        pdf.line(x, y + size * .25, x + size * .14, y + size * .43)
    else:
        raise ValueError(f"Unknown object kind: {kind}")


def draw_object_group(pdf: canvas.Canvas, group: dict, x: float, y: float, width: float, height: float) -> None:
    """Lay out 1-20 objects in a clear grid inside a reusable region."""
    count = int(group["count"])
    default_columns = 10 if count >= 11 else {6: 3, 7: 4, 8: 4, 9: 3, 10: 5}.get(count, min(count, 5))
    columns = int(group.get("columns", default_columns))
    if columns < 1 or columns > count:
        raise ValueError(f"Object group columns must be between 1 and {count}.")
    rows = (count + columns - 1) // columns
    size = min(28, width / (columns + .5), height / (rows + .35))
    x_gap, y_gap = width / columns, height / rows
    for index in range(count):
        row, col = divmod(index, columns)
        row_count = min(columns, count - row * columns)
        center_offset = (columns - row_count) * x_gap / 2
        draw_object(pdf, group["object"], x + center_offset + (col + .5) * x_gap,
                    y + height - (row + .5) * y_gap, size)


def draw_answer_choices(pdf: canvas.Canvas, values: list[int], x: float, y: float) -> None:
    for index, value in enumerate(values):
        cx = x + index * 76
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawCentredString(cx, y - 8, str(value))


def draw_write_box(pdf: canvas.Canvas, x: float, y: float, size: float = 47) -> None:
    pdf.setFillColor(white)
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(1.6)
    pdf.roundRect(x, y - size / 2, size, size, 7, fill=1, stroke=1)


def build_counting_pdf(pdf: canvas.Canvas, data: dict) -> None:
    activities = data["activities"]
    section_heading(pdf, 1, activities["circle"]["title"], activities["circle"]["prompt"], 610)
    for index, item in enumerate(activities["circle"]["items"]):
        y = 550 - index * 62
        draw_object_group(pdf, item, 48, y - 25, 205, 52)
        draw_answer_choices(pdf, item["choices"], 335, y)
        if index < len(activities["circle"]["items"]) - 1:
            pdf.setStrokeColor(PALE_TEAL)
            pdf.line(48, y - 32, PAGE_WIDTH - 48, y - 32)

    section_heading(pdf, 2, activities["match"]["title"], activities["match"]["prompt"], 366)
    match = activities["match"]
    for index, group in enumerate(match["groups"]):
        y = 298 - index * 59
        draw_object_group(pdf, group, 52, y - 21, 190, 44)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawCentredString(475, y - 8, str(match["numbers"][index]))

    section_heading(pdf, 3, activities["write"]["title"], activities["write"]["prompt"], 140)
    for index, group in enumerate(activities["write"]["groups"]):
        x = 235 + index * 270
        draw_object_group(pdf, group, x - 175, 59, 145, 46)
        draw_write_box(pdf, x, 82, 50)


def build_extended_mixed_pdf(pdf: canvas.Canvas, activities: dict) -> None:
    circle = activities["circle"]
    section_heading(pdf, 1, circle["title"], circle["prompt"], 610)
    for index, item in enumerate(circle["items"]):
        y = 550 - index * 50
        draw_object_group(pdf, item, 48, y - 22, 220, 44)
        draw_answer_choices(pdf, item["choices"], 335, y)
        if index < len(circle["items"]) - 1:
            pdf.setStrokeColor(PALE_TEAL)
            pdf.line(48, y - 25, PAGE_WIDTH - 48, y - 25)

    match = activities["match"]
    section_heading(pdf, 2, match["title"], match["prompt"], 392)
    for index, group in enumerate(match["groups"]):
        y = 330 - index * 55
        draw_object_group(pdf, group, 52, y - 21, 185, 42)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawCentredString(475, y - 8, str(match["numbers"][index]))

    write = activities["write"]
    section_heading(pdf, 3, write["title"], write["prompt"], 170)
    for index, group in enumerate(write["groups"]):
        group_x = 45 + index * 275
        box_x = 225 + index * 275
        draw_object_group(pdf, group, group_x, 45, 150, 94)
        draw_write_box(pdf, box_x, 92, 70)


def build_upper_range_mixed_pdf(pdf: canvas.Canvas, activities: dict) -> None:
    """Draw a reduced-density mixed review for quantities above ten."""
    circle = activities["circle"]
    section_heading(pdf, 1, circle["title"], circle["prompt"], 610)
    for index, item in enumerate(circle["items"]):
        y = 535 - index * 82
        draw_object_group(pdf, item, 48, y - 35, 245, 70)
        draw_answer_choices(pdf, item["choices"], 360, y)
        if index < len(circle["items"]) - 1:
            pdf.setStrokeColor(PALE_TEAL)
            pdf.line(48, y - 42, PAGE_WIDTH - 48, y - 42)

    match = activities["match"]
    section_heading(pdf, 2, match["title"], match["prompt"], 390)
    for index, group in enumerate(match["groups"]):
        y = 315 - index * 92
        draw_object_group(pdf, group, 52, y - 37, 245, 74)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 25)
        pdf.drawCentredString(475, y - 9, str(match["numbers"][index]))

    write = activities["write"]
    section_heading(pdf, 3, write["title"], write["prompt"], 145)
    draw_object_group(pdf, write["groups"][0], 55, 48, 330, 68)
    draw_write_box(pdf, 445, 82, 70)


def draw_count_and_circle_page(pdf: canvas.Canvas, activity: dict) -> None:
    section_heading(pdf, 1, activity["title"], activity["prompt"], 610)
    row_gap = 83 if len(activity["items"]) >= 6 else 102
    for index, item in enumerate(activity["items"]):
        y = 535 - index * row_gap
        draw_object_group(pdf, item, 52, y - 34, 230, 68)
        draw_answer_choices(pdf, item["choices"], 350, y)
        if index < len(activity["items"]) - 1:
            pdf.setStrokeColor(PALE_TEAL)
            pdf.line(48, y - row_gap / 2, PAGE_WIDTH - 48, y - row_gap / 2)


def draw_count_and_match_page(pdf: canvas.Canvas, activity: dict) -> None:
    section_heading(pdf, 2, activity["title"], activity["prompt"], 610)
    for index, group in enumerate(activity["groups"]):
        y = 525 - index * 110
        draw_object_group(pdf, group, 55, y - 48, 220, 96)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 26)
        pdf.drawCentredString(475, y - 9, str(activity["numbers"][index]))


def draw_count_and_write_page(pdf: canvas.Canvas, activity: dict) -> None:
    section_heading(pdf, 3, activity["title"], activity["prompt"], 610)
    for index, group in enumerate(activity["groups"]):
        y = 525 - index * 95
        draw_object_group(pdf, group, 65, y - 36, 275, 74)
        draw_write_box(pdf, 445, y, 72)
        if index < len(activity["groups"]) - 1:
            pdf.setStrokeColor(PALE_TEAL)
            pdf.line(55, y - 55, PAGE_WIDTH - 55, y - 55)


def draw_count_and_draw_page(pdf: canvas.Canvas, activity: dict) -> None:
    section_heading(pdf, 4, activity["title"], activity["prompt"], 610)
    box_height = 100 if len(activity["numbers"]) <= 4 else 78
    row_gap = 115 if len(activity["numbers"]) <= 4 else 96
    for index, value in enumerate(activity["numbers"]):
        top = 555 - index * row_gap
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 27)
        pdf.drawCentredString(70, top - box_height / 2 - 9, str(value))
        pdf.setFillColor(white)
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.4)
        pdf.roundRect(110, top - box_height, 440, box_height, 10, fill=1, stroke=1)


def validate_counting_pack(data: dict) -> None:
    pages = data.get("pages")
    if not isinstance(pages, list) or len(pages) != 5:
        raise ValueError("A counting pack must contain exactly five pages.")
    expected_types = ["circle", "match", "write", "draw", "mixed"]
    if [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Counting pack page types must be {expected_types}.")
    values = []
    for page in pages:
        activity = page.get("activity", page.get("activities", {}))
        for item in activity.get("items", []):
            values.append(item["count"])
            values.extend(item.get("choices", []))
        for group in activity.get("groups", []):
            values.append(group["count"])
        values.extend(activity.get("numbers", []))
        if page["type"] == "mixed":
            for mixed_activity in activity.values():
                for item in mixed_activity.get("items", []):
                    values.append(item["count"])
                    values.extend(item.get("choices", []))
                for group in mixed_activity.get("groups", []):
                    values.append(group["count"])
                values.extend(mixed_activity.get("numbers", []))
    range_min = data.get("range_min", 1)
    range_max = data.get("range_max")
    if not isinstance(range_min, int) or range_min < 1 or range_min > 20:
        raise ValueError("Counting packs require an integer range_min from 1 through 20.")
    if not isinstance(range_max, int) or range_max < 1 or range_max > 20:
        raise ValueError("Counting packs require an integer range_max from 1 through 20.")
    if range_min > range_max:
        raise ValueError("Counting pack range_min cannot exceed range_max.")
    if not values or any(not isinstance(value, int) or value < range_min or value > range_max for value in values):
        raise ValueError(f"Counting pack content must use integers from {range_min} through {range_max} only.")


def build_counting_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_counting_pack(data)
    renderers = {
        "circle": draw_count_and_circle_page,
        "match": draw_count_and_match_page,
        "write": draw_count_and_write_page,
        "draw": draw_count_and_draw_page,
    }
    for page in data["pages"]:
        draw_header(pdf, {**data, "subtitle": page["subtitle"]})
        if page["type"] == "mixed":
            if page.get("layout") == "upper-range":
                build_upper_range_mixed_pdf(pdf, page["activities"])
            elif page.get("layout") == "extended":
                build_extended_mixed_pdf(pdf, page["activities"])
            else:
                build_counting_pdf(pdf, {"activities": page["activities"]})
        else:
            renderers[page["type"]](pdf, page["activity"])
        draw_footer(pdf)
        pdf.showPage()


def draw_order_box(pdf: canvas.Canvas, x: float, y: float, width: float, height: float,
                   value: int | None = None, accent=TEAL) -> None:
    """Draw one reusable number or answer box for ordering activities."""
    pdf.setFillColor(PALE_TEAL if value is not None else white)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.5)
    pdf.roundRect(x, y, width, height, 9, fill=1, stroke=1)
    if value is not None:
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 25)
        pdf.drawCentredString(x + width / 2, y + height / 2 - 9, str(value))


def draw_order_arrow(pdf: canvas.Canvas, x: float, y: float, length: float = 24) -> None:
    """Draw a simple right-pointing vector arrow."""
    pdf.setStrokeColor(TEAL)
    pdf.setFillColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(x, y, x + length, y)
    path = pdf.beginPath()
    path.moveTo(x + length, y)
    path.lineTo(x + length - 7, y + 5)
    path.lineTo(x + length - 7, y - 5)
    path.close()
    pdf.drawPath(path, fill=1, stroke=0)


def draw_before_after_rows(pdf: canvas.Canvas, items: list[int], y_top: float, row_gap: float) -> None:
    box_width, box_height, gap = 104, 62, 32
    total_width = box_width * 3 + gap * 2
    start_x = (PAGE_WIDTH - total_width) / 2
    accents = (BLUE, TEAL, CORAL)
    for index, value in enumerate(items):
        y = y_top - index * row_gap - box_height
        draw_order_box(pdf, start_x, y, box_width, box_height, accent=accents[0])
        draw_order_box(pdf, start_x + box_width + gap, y, box_width, box_height, value, accents[1])
        draw_order_box(pdf, start_x + 2 * (box_width + gap), y, box_width, box_height, accent=accents[2])
        draw_order_arrow(pdf, start_x + box_width + 4, y + box_height / 2, gap - 8)
        draw_order_arrow(pdf, start_x + 2 * box_width + gap + 4, y + box_height / 2, gap - 8)


def draw_missing_rows(pdf: canvas.Canvas, rows: list[list[int | None]], y_top: float, row_gap: float) -> None:
    box_width, box_height, gap = 82, 58, 15
    total_width = box_width * 5 + gap * 4
    start_x = (PAGE_WIDTH - total_width) / 2
    accents = (TEAL, GOLD, CORAL, BLUE, PURPLE)
    for row_index, row in enumerate(rows):
        y = y_top - row_index * row_gap - box_height
        for index, value in enumerate(row):
            x = start_x + index * (box_width + gap)
            draw_order_box(pdf, x, y, box_width, box_height, value, accents[index])


def draw_sort_rows(pdf: canvas.Canvas, rows: list[list[int]], y_top: float, row_gap: float) -> None:
    card_width, card_height, gap = 48, 54, 8
    for row_index, row in enumerate(rows):
        y = y_top - row_index * row_gap - card_height
        for index, value in enumerate(row):
            draw_order_box(pdf, 48 + index * (card_width + gap), y, card_width, card_height, value,
                           (GOLD, CORAL, BLUE, PURPLE)[index])
        draw_order_arrow(pdf, 282, y + card_height / 2, 28)
        for index in range(len(row)):
            draw_order_box(pdf, 328 + index * (card_width + gap), y, card_width, card_height)


def validate_number_order_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["before-after", "missing", "order", "mixed"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Number Order pages must be {expected_types}.")
    values: list[int] = []
    for page in pages:
        activity = page.get("activity", page.get("activities", {}))
        sections = activity.values() if page["type"] == "mixed" else [activity]
        for section in sections:
            values.extend(section.get("items", []))
            for row in section.get("rows", []):
                values.extend(value for value in row if value is not None)
    range_min = data.get("range_min", 1)
    range_max = data.get("range_max", 10)
    if not isinstance(range_min, int) or not isinstance(range_max, int) or not 1 <= range_min <= range_max <= 20:
        raise ValueError("Number Order requires a valid range from 1 through 20.")
    if not values or any(not isinstance(value, int) or value < range_min or value > range_max for value in values):
        raise ValueError(f"Number Order content must use integers from {range_min} through {range_max} only.")


def build_number_order_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_number_order_pack(data)
    for page in data["pages"]:
        draw_header(pdf, {**data, "subtitle": page["subtitle"]})
        if page["type"] == "before-after":
            activity = page["activity"]
            section_heading(pdf, 1, activity["title"], activity["prompt"], 610)
            draw_before_after_rows(pdf, activity["items"], 555, 87)
        elif page["type"] == "missing":
            activity = page["activity"]
            section_heading(pdf, 2, activity["title"], activity["prompt"], 610)
            draw_missing_rows(pdf, activity["rows"], 555, 86)
        elif page["type"] == "order":
            activity = page["activity"]
            section_heading(pdf, 3, activity["title"], activity["prompt"], 610)
            draw_sort_rows(pdf, activity["rows"], 550, 103)
        else:
            activities = page["activities"]
            before = activities["before_after"]
            section_heading(pdf, 1, before["title"], before["prompt"], 610)
            draw_before_after_rows(pdf, before["items"], 560, 78)
            missing = activities["missing"]
            section_heading(pdf, 2, missing["title"], missing["prompt"], 390)
            draw_missing_rows(pdf, missing["rows"], 345, 76)
            order = activities["order"]
            section_heading(pdf, 3, order["title"], order["prompt"], 175)
            draw_sort_rows(pdf, order["rows"], 130, 70)
        draw_footer(pdf)
        pdf.showPage()


def draw_comparison_panel(pdf: canvas.Canvas, group: dict, x: float, y: float,
                          width: float, height: float, accent) -> None:
    """Draw one large, circle-ready object group panel."""
    pdf.setFillColor(PALE_TEAL)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.5)
    pdf.roundRect(x, y, width, height, 11, fill=1, stroke=1)
    draw_object_group(pdf, group, x + 12, y + 8, width - 24, height - 16)


def draw_comparison_pairs(pdf: canvas.Canvas, items: list[dict], y_top: float, row_gap: float,
                          panel_height: float = 70) -> None:
    panel_width, left_x, right_x = 210, 55, 347
    for index, item in enumerate(items):
        y = y_top - index * row_gap - panel_height
        draw_comparison_panel(pdf, item["left"], left_x, y, panel_width, panel_height,
                              (TEAL, BLUE, GOLD, CORAL, PURPLE)[index % 5])
        draw_comparison_panel(pdf, item["right"], right_x, y, panel_width, panel_height,
                              (CORAL, GOLD, PURPLE, BLUE, TEAL)[index % 5])
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawCentredString(PAGE_WIDTH / 2, y + panel_height / 2 - 3, "OR")


def draw_same_rows(pdf: canvas.Canvas, items: list[dict], y_top: float, row_gap: float,
                   panel_height: float = 72) -> None:
    panel_width = 145
    for index, item in enumerate(items):
        y = y_top - index * row_gap - panel_height
        draw_comparison_panel(pdf, item["target"], 48, y, panel_width, panel_height, TEAL)
        draw_order_arrow(pdf, 204, y + panel_height / 2, 24)
        draw_comparison_panel(pdf, item["choices"][0], 242, y, panel_width, panel_height,
                              (GOLD, BLUE, CORAL, PURPLE)[index % 4])
        draw_comparison_panel(pdf, item["choices"][1], 419, y, panel_width, panel_height,
                              (PURPLE, CORAL, GOLD, BLUE)[index % 4])


def validate_comparison_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["more", "fewer", "same", "mixed"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Comparison pack pages must be {expected_types}.")
    counts: list[int] = []
    for page in pages:
        activity = page.get("activity", page.get("activities", {}))
        sections = activity.values() if page["type"] == "mixed" else [activity]
        for section in sections:
            for item in section.get("items", []):
                if "left" in item:
                    pair = [item["left"], item["right"]]
                    if pair[0]["count"] == pair[1]["count"]:
                        raise ValueError("More and fewer comparisons require different quantities.")
                    counts.extend(group["count"] for group in pair)
                else:
                    choices = item["choices"]
                    if len(choices) != 2 or sum(choice["count"] == item["target"]["count"] for choice in choices) != 1:
                        raise ValueError("Same comparisons require two choices with exactly one match.")
                    counts.append(item["target"]["count"])
                    counts.extend(choice["count"] for choice in choices)
    if not counts or any(not isinstance(count, int) or count < 1 or count > 10 for count in counts):
        raise ValueError("Comparison packs must use quantities from 1 through 10 only.")


def build_comparison_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_comparison_pack(data)
    for page in data["pages"]:
        draw_header(pdf, {**data, "subtitle": page["subtitle"]})
        if page["type"] in {"more", "fewer"}:
            activity = page["activity"]
            section_heading(pdf, 1 if page["type"] == "more" else 2,
                            activity["title"], activity["prompt"], 610)
            draw_comparison_pairs(pdf, activity["items"], 555, 88)
        elif page["type"] == "same":
            activity = page["activity"]
            section_heading(pdf, 3, activity["title"], activity["prompt"], 610)
            draw_same_rows(pdf, activity["items"], 555, 101)
        else:
            activities = page["activities"]
            more = activities["more"]
            section_heading(pdf, 1, more["title"], more["prompt"], 610)
            draw_comparison_pairs(pdf, more["items"], 555, 78, 66)
            fewer = activities["fewer"]
            section_heading(pdf, 2, fewer["title"], fewer["prompt"], 365)
            draw_comparison_pairs(pdf, fewer["items"], 310, 78, 66)
            same = activities["same"]
            section_heading(pdf, 3, same["title"], same["prompt"], 145)
            draw_same_rows(pdf, same["items"], 112, 70, 60)
        draw_footer(pdf)
        pdf.showPage()


def draw_addition_panel(pdf: canvas.Canvas, group: dict, x: float, y: float,
                        width: float, height: float, accent, label: int | None = None) -> None:
    """Draw one reusable, colorful addend panel."""
    pdf.setFillColor(PALE_TEAL)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, y, width, height, 10, fill=1, stroke=1)
    label_space = 20 if label is not None else 0
    draw_object_group(pdf, group, x + 10, y + 7 + label_space, width - 20, height - 14 - label_space)
    if label is not None:
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawCentredString(x + width / 2, y + 8, str(label))


def draw_addition_symbol(pdf: canvas.Canvas, symbol: str, x: float, y: float,
                         size: float = 24) -> None:
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(x, y - size * .32, symbol)


def draw_addition_picture_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                               row_gap: float, panel_height: float, show_addends: bool = False) -> None:
    accents = (CORAL, BLUE, GOLD, PURPLE, TEAL)
    for index, item in enumerate(items):
        y = y_top - index * row_gap - panel_height
        draw_addition_panel(pdf, item["left"], 48, y, 174, panel_height, accents[index % 5],
                            item["left"]["count"] if show_addends else None)
        draw_addition_symbol(pdf, "+", 244, y + panel_height / 2)
        draw_addition_panel(pdf, item["right"], 266, y, 174, panel_height, accents[(index + 2) % 5],
                            item["right"]["count"] if show_addends else None)
        draw_addition_symbol(pdf, "=", 462, y + panel_height / 2)
        draw_write_box(pdf, 500, y + panel_height / 2, 58)


def draw_picture_addition_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                               row_gap: float) -> None:
    accents = (BLUE, CORAL, PURPLE, GOLD)
    for index, item in enumerate(items):
        y = y_top - index * row_gap - 76
        pdf.setFillColor(PALE_TEAL)
        pdf.setStrokeColor(accents[index % 4])
        pdf.setLineWidth(1.4)
        pdf.roundRect(50, y, 390, 76, 11, fill=1, stroke=1)
        draw_object_group(pdf, item["left"], 65, y + 9, 155, 58)
        pdf.setFillColor(white)
        pdf.rect(224, y + 5, 42, 66, fill=1, stroke=0)
        draw_addition_symbol(pdf, "+", 245, y + 38)
        draw_object_group(pdf, item["right"], 270, y + 9, 155, 58)
        draw_addition_symbol(pdf, "=", 462, y + 38)
        draw_write_box(pdf, 500, y + 38, 58)


def draw_complete_addition_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                                row_gap: float) -> None:
    accents = (TEAL, GOLD, CORAL, BLUE, PURPLE)
    for index, item in enumerate(items):
        center_y = y_top - index * row_gap
        left_group = {"object": item["object"], "count": item["left"]}
        right_group = {"object": item["object"], "count": item["right"]}
        draw_addition_panel(pdf, left_group, 55, center_y - 34, 105, 68, accents[index % 5])
        draw_addition_symbol(pdf, "+", 180, center_y, 21)
        draw_addition_panel(pdf, right_group, 200, center_y - 34, 105, 68,
                            accents[(index + 2) % 5])
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 25)
        pdf.drawString(350, center_y - 9, f'{item["left"]}  +  {item["right"]}  =')
        draw_write_box(pdf, 505, center_y, 62)
        if index < len(items) - 1:
            pdf.setStrokeColor(PALE_TEAL)
            pdf.line(52, center_y - row_gap / 2, PAGE_WIDTH - 52, center_y - row_gap / 2)


def draw_draw_and_add_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                           row_gap: float) -> None:
    accents = (CORAL, BLUE, GOLD)
    for index, item in enumerate(items):
        y = y_top - index * row_gap - 96
        for box_index, value in enumerate((item["left"], item["right"])):
            x = 50 + box_index * 215
            pdf.setFillColor(white)
            pdf.setStrokeColor(accents[(index + box_index) % 3])
            pdf.setLineWidth(1.5)
            pdf.roundRect(x, y, 180, 96, 10, fill=1, stroke=1)
            pdf.setFillColor(MUTED)
            pdf.setFont("Helvetica-Bold", 11)
            noun = "object" if value == 1 else "objects"
            pdf.drawString(x + 11, y + 76, f"Draw {value} {noun}")
        draw_addition_symbol(pdf, "+", 245, y + 48, 23)
        draw_addition_symbol(pdf, "=", 462, y + 48, 23)
        draw_write_box(pdf, 500, y + 48, 58)


def validate_addition_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["put-together", "count-add", "picture-addition", "complete", "draw-add"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Addition pack pages must be {expected_types}.")
    equations: list[tuple[int, int, int]] = []
    for page in pages:
        for item in page["activity"]["items"]:
            if page["type"] in {"put-together", "count-add", "picture-addition"}:
                left, right, total = item["left"]["count"], item["right"]["count"], item["total"]
            else:
                left, right, total = item["left"], item["right"], item["total"]
            equations.append((left, right, total))
    if not equations or any(not all(isinstance(value, int) for value in equation) for equation in equations):
        raise ValueError("Addition pack equations must use integers.")
    if any(left < 1 or right < 1 or left + right != total or total > 5
           for left, right, total in equations):
        raise ValueError("Addition pack equations must use positive addends with sums up to 5.")


def build_addition_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_addition_pack(data)
    for page in data["pages"]:
        draw_header(pdf, {**data, "page_instruction": page["subtitle"]})
        activity = page["activity"]
        section_heading(pdf, page["section_number"], activity["title"], activity["prompt"], 585)
        if page["type"] == "put-together":
            draw_addition_picture_rows(pdf, activity["items"], 555, 115, 76)
        elif page["type"] == "count-add":
            draw_addition_picture_rows(pdf, activity["items"], 555, 91, 62, True)
        elif page["type"] == "picture-addition":
            draw_picture_addition_rows(pdf, activity["items"], 555, 114)
        elif page["type"] == "complete":
            draw_complete_addition_rows(pdf, activity["items"], 515, 91)
        else:
            draw_draw_and_add_rows(pdf, activity["items"], 550, 165)
        draw_footer(pdf)
        pdf.showPage()


def validate_story_problem_sample(data: dict) -> None:
    """Validate the single Put Together page used for story-bundle review."""
    page = data.get("page")
    if not isinstance(page, dict) or page.get("type") != "put-together":
        raise ValueError("The story-problems sample must contain one Put Together page.")
    items = page.get("activity", {}).get("items", [])
    if len(items) != 3:
        raise ValueError("The Put Together sample must contain exactly three stories.")
    for item in items:
        left = item.get("left", {}).get("count")
        right = item.get("right", {}).get("count")
        total = item.get("total")
        if not all(isinstance(value, int) for value in (left, right, total)):
            raise ValueError("Story quantities must be integers.")
        if left < 1 or right < 1 or left + right != total or total > 5:
            raise ValueError("Put Together stories must use positive groups with totals up to 5.")
        if not isinstance(item.get("story"), str) or not item["story"].strip():
            raise ValueError("Every story problem requires a short sentence.")


def draw_put_together_story_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                                 row_gap: float) -> None:
    """Draw three roomy, picture-led story problems with large answer boxes."""
    accents = (CORAL, BLUE, GOLD)
    for index, item in enumerate(items):
        y = y_top - index * row_gap - 118
        accent = accents[index % len(accents)]
        pdf.setFillColor(white)
        pdf.setStrokeColor(accent)
        pdf.setLineWidth(1.5)
        pdf.roundRect(48, y, PAGE_WIDTH - 96, 118, 12, fill=1, stroke=1)
        pdf.setFillColor(accent)
        pdf.roundRect(48, y, 8, 118, 4, fill=1, stroke=0)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(67, y + 92, item["story"])
        draw_addition_panel(pdf, item["left"], 67, y + 14, 142, 64, accent)
        draw_addition_symbol(pdf, "+", 229, y + 46, 24)
        draw_addition_panel(pdf, item["right"], 249, y + 14, 142, 64,
                            (BLUE, GOLD, CORAL)[index % 3])
        draw_addition_symbol(pdf, "=", 419, y + 46, 24)
        draw_write_box(pdf, 465, y + 46, 66)


def build_story_problem_sample(pdf: canvas.Canvas, data: dict) -> None:
    validate_story_problem_sample(data)
    page = data["page"]
    draw_header(pdf, {**data, "page_instruction": page["subtitle"]})
    activity = page["activity"]
    section_heading(pdf, 1, activity["title"], activity["prompt"], 585)
    draw_put_together_story_rows(pdf, activity["items"], 540, 147)
    draw_footer(pdf)
    pdf.showPage()


def draw_crossed_object_group(pdf: canvas.Canvas, group: dict, remove_count: int,
                              x: float, y: float, width: float, height: float) -> None:
    """Draw a countable group with the final objects visibly crossed out."""
    count = int(group["count"])
    columns = int(group.get("columns", min(count, 5)))
    rows = (count + columns - 1) // columns
    size = min(28, width / (columns + .5), height / (rows + .35))
    x_gap, y_gap = width / columns, height / rows
    for index in range(count):
        row, col = divmod(index, columns)
        row_count = min(columns, count - row * columns)
        center_offset = (columns - row_count) * x_gap / 2
        center_x = x + center_offset + (col + .5) * x_gap
        center_y = y + height - (row + .5) * y_gap
        draw_object(pdf, group["object"], center_x, center_y, size)
        if index >= count - remove_count:
            cross_size = size * .48
            pdf.setStrokeColor(CROSSOUT_RED)
            pdf.setLineWidth(2.8)
            pdf.line(center_x - cross_size, center_y - cross_size,
                     center_x + cross_size, center_y + cross_size)
            pdf.line(center_x - cross_size, center_y + cross_size,
                     center_x + cross_size, center_y - cross_size)


def draw_take_away_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                        row_gap: float, crossed: bool) -> None:
    accents = (CORAL, BLUE, GOLD, PURPLE, TEAL)
    for index, item in enumerate(items):
        center_y = y_top - index * row_gap
        pdf.setFillColor(PALE_TEAL)
        pdf.setStrokeColor(accents[index % 5])
        pdf.setLineWidth(1.5)
        pdf.roundRect(55, center_y - 36, 350, 72, 10, fill=1, stroke=1)
        group = {"object": item["object"], "count": item["start"]}
        if crossed:
            draw_crossed_object_group(pdf, group, item["take_away"], 68, center_y - 28, 324, 56)
        else:
            draw_object_group(pdf, group, 68, center_y - 28, 324, 56)
            pdf.setFillColor(CORAL)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(420, center_y + 13, f'Cross out {item["take_away"]}')
        draw_addition_symbol(pdf, "=", 452, center_y - (10 if not crossed else 0), 23)
        draw_write_box(pdf, 500, center_y - (10 if not crossed else 0), 58)


def draw_picture_subtraction_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                                  row_gap: float, panel_height: float = 76) -> None:
    accents = (CORAL, BLUE, GOLD, PURPLE)
    for index, item in enumerate(items):
        y = y_top - index * row_gap - panel_height
        start = {"object": item["object"], "count": item["start"]}
        removed = {"object": item["object"], "count": item["take_away"]}
        draw_addition_panel(pdf, start, 48, y, 174, panel_height, accents[index % 4])
        draw_addition_symbol(pdf, "-", 244, y + panel_height / 2)
        pdf.setFillColor(PALE_TEAL)
        pdf.setStrokeColor(accents[(index + 2) % 4])
        pdf.setLineWidth(1.4)
        pdf.roundRect(266, y, 174, panel_height, 10, fill=1, stroke=1)
        draw_crossed_object_group(pdf, removed, item["take_away"], 276, y + 8, 154, panel_height - 16)
        draw_addition_symbol(pdf, "=", 462, y + panel_height / 2)
        draw_write_box(pdf, 500, y + panel_height / 2, 58)


def draw_complete_subtraction_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                                   row_gap: float) -> None:
    accents = (TEAL, GOLD, CORAL, BLUE, PURPLE)
    for index, item in enumerate(items):
        center_y = y_top - index * row_gap
        start = {"object": item["object"], "count": item["start"]}
        removed = {"object": item["object"], "count": item["take_away"]}
        draw_addition_panel(pdf, start, 48, center_y - 34, 128, 68, accents[index % 5])
        draw_addition_symbol(pdf, "-", 194, center_y, 21)
        pdf.setFillColor(PALE_TEAL)
        pdf.setStrokeColor(accents[(index + 2) % 5])
        pdf.setLineWidth(1.4)
        pdf.roundRect(212, center_y - 34, 108, 68, 10, fill=1, stroke=1)
        draw_object_group(pdf, removed, 222, center_y - 27, 88, 54)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 25)
        pdf.drawString(352, center_y - 9, f'{item["start"]}  -  {item["take_away"]}  =')
        draw_write_box(pdf, 505, center_y, 62)
        if index < len(items) - 1:
            pdf.setStrokeColor(PALE_TEAL)
            pdf.line(52, center_y - row_gap / 2, PAGE_WIDTH - 52, center_y - row_gap / 2)


def draw_and_take_away_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                            row_gap: float) -> None:
    accents = (CORAL, BLUE, GOLD)
    for index, item in enumerate(items):
        y = y_top - index * row_gap - 104
        pdf.setFillColor(white)
        pdf.setStrokeColor(accents[index % 3])
        pdf.setLineWidth(1.5)
        pdf.roundRect(55, y, 380, 104, 10, fill=1, stroke=1)
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(68, y + 83,
                       f'Draw {item["start"]} objects. Cross out {item["take_away"]}.')
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawRightString(490, y + 45, f'{item["start"]} - {item["take_away"]} =')
        draw_write_box(pdf, 500, y + 52, 58)


def validate_subtraction_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["take-away", "cross-out", "picture-subtraction", "complete", "draw-take-away"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Subtraction pack pages must be {expected_types}.")
    problems = [item for page in pages for item in page["activity"]["items"]]
    if not problems or any(not all(isinstance(item[key], int) for key in ("start", "take_away", "result"))
                           for item in problems):
        raise ValueError("Subtraction pack problems must use integers.")
    if any(item["start"] > 5 or item["start"] < 1 or item["take_away"] < 1
           or item["start"] - item["take_away"] != item["result"]
           or item["result"] < 0 or item["result"] > 5 for item in problems):
        raise ValueError("Subtraction pack values and results must stay within 0 through 5.")


def build_subtraction_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_subtraction_pack(data)
    for page in data["pages"]:
        draw_header(pdf, {**data, "page_instruction": page["subtitle"]})
        activity = page["activity"]
        section_heading(pdf, page["section_number"], activity["title"], activity["prompt"], 585)
        if page["type"] == "take-away":
            draw_take_away_rows(pdf, activity["items"], 515, 112, True)
        elif page["type"] == "cross-out":
            draw_take_away_rows(pdf, activity["items"], 520, 91, False)
        elif page["type"] == "picture-subtraction":
            draw_picture_subtraction_rows(pdf, activity["items"], 555, 114)
        elif page["type"] == "complete":
            draw_complete_subtraction_rows(pdf, activity["items"], 515, 91)
        else:
            draw_and_take_away_rows(pdf, activity["items"], 545, 165)
        draw_footer(pdf)
        pdf.showPage()


def draw_fact_card(pdf: canvas.Canvas, x: float, y: float, width: float, height: float,
                   accent) -> None:
    """Draw a reusable, child-friendly equation card without picture clues."""
    pdf.setFillColor(PALE_TEAL)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.5)
    pdf.roundRect(x, y, width, height, 11, fill=1, stroke=1)


def draw_horizontal_fact_rows(pdf: canvas.Canvas, facts: list[dict], symbol: str,
                              y_top: float, row_gap: float) -> None:
    accents = (CORAL, BLUE, GOLD, PURPLE, TEAL)
    for index, fact in enumerate(facts):
        center_y = y_top - index * row_gap
        draw_fact_card(pdf, 70, center_y - 35, 472, 70, accents[index % 5])
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 27)
        for value, x in ((fact["left"], 285), (symbol, 330), (fact["right"], 375), ("=", 420)):
            pdf.drawCentredString(x, center_y - 9, str(value))
        draw_write_box(pdf, 455, center_y, 58)


def draw_vertical_fact_card(pdf: canvas.Canvas, fact: dict, symbol: str,
                            x: float, y: float, accent) -> None:
    draw_fact_card(pdf, x, y, 215, 132, accent)
    center_x = x + 107
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 25)
    equation_right = center_x + 18
    pdf.drawRightString(equation_right, y + 96, str(fact["left"]))
    pdf.drawRightString(equation_right, y + 66, f"{symbol} {fact['right']}")
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.7)
    pdf.line(center_x - 21, y + 56, center_x + 21, y + 56)
    pdf.line(center_x - 21, y + 20, center_x + 21, y + 20)


def draw_vertical_fact_grid(pdf: canvas.Canvas, facts: list[dict], symbol: str,
                            y_top: float) -> None:
    accents = (CORAL, BLUE, GOLD, PURPLE, TEAL)
    for index, fact in enumerate(facts):
        row, col = divmod(index, 2)
        draw_vertical_fact_card(pdf, fact, symbol, 70 + col * 265,
                                y_top - row * 150 - 132, accents[index % 5])


def draw_varied_fact_grid(pdf: canvas.Canvas, facts: list[dict], symbol: str,
                          y_top: float) -> None:
    accents = (GOLD, CORAL, BLUE, PURPLE, TEAL)
    for index, fact in enumerate(facts):
        row, col = divmod(index, 2)
        x, y = 58 + col * 273, y_top - row * 145 - 104
        draw_fact_card(pdf, x, y, 223, 104, accents[index % 5])
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 22)
        for value, offset in ((fact["left"], 35), (symbol, 65), (fact["right"], 95), ("=", 125)):
            pdf.drawCentredString(x + offset, y + 46, str(value))
        draw_write_box(pdf, x + 151, y + 55, 48)


def draw_mixed_fact_page(pdf: canvas.Canvas, activity: dict, symbol: str) -> None:
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(70, 535, "Across")
    draw_horizontal_fact_rows(pdf, activity["horizontal"], symbol, 490, 82)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(70, 265, "Up and Down")
    accents = (PURPLE, GOLD)
    for index, fact in enumerate(activity["vertical"]):
        draw_vertical_fact_card(pdf, fact, symbol, 70 + index * 265, 90, accents[index])


def validate_arithmetic_facts_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["horizontal", "vertical", "fill-in", "varied", "mixed"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Arithmetic facts pages must be {expected_types}.")
    operation = data.get("operation")
    if operation not in {"addition", "subtraction"}:
        raise ValueError("Arithmetic facts operation must be addition or subtraction.")
    facts: list[dict] = []
    for page in pages:
        activity = page["activity"]
        if page["type"] == "mixed":
            facts.extend(activity["horizontal"])
            facts.extend(activity["vertical"])
        else:
            facts.extend(activity["facts"])
    for fact in facts:
        values = (fact.get("left"), fact.get("right"), fact.get("result"))
        if not all(isinstance(value, int) and 0 <= value <= 5 for value in values):
            raise ValueError("Arithmetic facts must use integers from 0 through 5.")
        expected = fact["left"] + fact["right"] if operation == "addition" else fact["left"] - fact["right"]
        if fact["result"] != expected:
            raise ValueError("Arithmetic fact result does not match its equation.")


def build_arithmetic_facts_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_arithmetic_facts_pack(data)
    symbol = "+" if data["operation"] == "addition" else "-"
    for page in data["pages"]:
        draw_header(pdf, {**data, "page_instruction": page["subtitle"]})
        activity = page["activity"]
        section_heading(pdf, page["section_number"], activity["title"], activity["prompt"], 585)
        if page["type"] in {"horizontal", "fill-in"}:
            draw_horizontal_fact_rows(pdf, activity["facts"], symbol, 520, 82)
        elif page["type"] == "vertical":
            draw_vertical_fact_grid(pdf, activity["facts"], symbol, 545)
        elif page["type"] == "varied":
            draw_varied_fact_grid(pdf, activity["facts"], symbol, 545)
        else:
            draw_mixed_fact_page(pdf, activity, symbol)
        draw_footer(pdf)
        pdf.showPage()


def build_pdf(data: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output_path), pagesize=letter, pageCompression=1)
    pdf.setTitle(data["title"] + " | Learning Made Simple")
    pdf.setAuthor("Learning Made Simple")
    if data.get("template") == "number-recognition-pack":
        build_number_recognition_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "counting-pack":
        build_counting_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "number-order-pack":
        build_number_order_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "comparison-pack":
        build_comparison_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "addition-pack":
        build_addition_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "subtraction-pack":
        build_subtraction_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "arithmetic-facts-pack":
        build_arithmetic_facts_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "story-problems-sample":
        build_story_problem_sample(pdf, data)
        pdf.save()
        return
    draw_header(pdf, data)
    if data.get("template") == "counting":
        build_counting_pdf(pdf, data)
        draw_footer(pdf)
        pdf.showPage()
        pdf.save()
        return
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
    generator_dir = Path(__file__).parent
    if data.get("template") == "counting-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "counting"
    elif data.get("template") == "number-recognition-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "number-recognition"
    elif data.get("template") == "number-order-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "number-order"
    elif data.get("template") == "comparison-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "more-fewer-same"
    elif data.get("template") == "addition-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "addition"
    elif data.get("template") == "subtraction-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "subtraction"
    elif data.get("template") == "arithmetic-facts-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / ("addition" if data["operation"] == "addition" else "subtraction")
    else:
        output_dir = generator_dir / "output"
    build_pdf(data, output_dir / data["filename"])


if __name__ == "__main__":
    main()
