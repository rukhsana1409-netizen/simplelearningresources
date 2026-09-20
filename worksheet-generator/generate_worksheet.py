"""Generate clean, print-ready Learning Made Simple worksheets from JSON content."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from bundle_assets import BundleAssetContract, generate_bundle_assets

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
        "addition-pack", "subtraction-pack", "arithmetic-facts-pack",
        "story-problems-sample", "story-problems-pack"
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


def validate_story_problem_pack(data: dict) -> None:
    """Validate the five-page visual story bundle and its within-five arithmetic."""
    pages = data.get("pages")
    expected_types = ["put-together", "take-away", "look-solve", "choose-operation", "draw-story"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Story-problem pack pages must be {expected_types}.")
    expected_counts = [3, 3, 3, 3, 2]
    for page, expected_count in zip(pages, expected_counts):
        items = page.get("activity", {}).get("items", [])
        if len(items) != expected_count:
            raise ValueError(f'{page.get("type")} must contain exactly {expected_count} stories.')
        for item in items:
            if not isinstance(item.get("story"), str) or not item["story"].strip():
                raise ValueError("Every story problem requires a short sentence.")
            if page["type"] == "put-together":
                left = item.get("left", {}).get("count")
                right = item.get("right", {}).get("count")
                result = item.get("total")
                operation = "addition"
            else:
                operation = item.get("operation", "addition")
                left, right, result = item.get("left"), item.get("right"), item.get("result")
            if not all(isinstance(value, int) for value in (left, right, result)):
                raise ValueError("Story quantities must be integers.")
            valid = left >= 1 and right >= 1 and (
                (operation == "addition" and left + right == result and result <= 5) or
                (operation == "subtraction" and left - right == result and result >= 0 and left <= 5)
            )
            if not valid:
                raise ValueError("Story problems must use valid addition or subtraction within 5.")


def draw_story_card(pdf: canvas.Canvas, y: float, accent, story: str) -> None:
    pdf.setFillColor(white)
    pdf.setStrokeColor(accent)
    pdf.setLineWidth(1.5)
    pdf.roundRect(48, y, PAGE_WIDTH - 96, 118, 12, fill=1, stroke=1)
    pdf.setFillColor(accent)
    pdf.roundRect(48, y, 8, 118, 4, fill=1, stroke=0)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(67, y + 92, story)


def draw_take_away_story_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                              row_gap: float) -> None:
    accents = (CORAL, BLUE, GOLD)
    for index, item in enumerate(items):
        y = y_top - index * row_gap - 118
        accent = accents[index]
        draw_story_card(pdf, y, accent, item["story"])
        group = {"object": item["object"], "count": item["left"]}
        pdf.setFillColor(PALE_TEAL)
        pdf.setStrokeColor(accent)
        pdf.roundRect(67, y + 14, 324, 64, 10, fill=1, stroke=1)
        draw_crossed_object_group(pdf, group, item["right"], 79, y + 22, 300, 48)
        draw_addition_symbol(pdf, "=", 419, y + 46, 24)
        draw_write_box(pdf, 465, y + 46, 66)


def draw_mixed_story_rows(pdf: canvas.Canvas, items: list[dict], y_top: float,
                          row_gap: float, choose_operation: bool = False) -> None:
    accents = (CORAL, BLUE, GOLD)
    for index, item in enumerate(items):
        y = y_top - index * row_gap - 118
        accent = accents[index]
        draw_story_card(pdf, y, accent, item["story"])
        left = {"object": item["object"], "count": item["left"]}
        right = {"object": item["object"], "count": item["right"]}
        draw_addition_panel(pdf, left, 67, y + 14, 142, 64, accent)
        if choose_operation:
            draw_write_box(pdf, 216, y + 46, 46)
        else:
            symbol = "+" if item["operation"] == "addition" else "-"
            draw_addition_symbol(pdf, symbol, 229, y + 46, 24)
        draw_addition_panel(pdf, right, 269, y + 14, 122, 64,
                            (BLUE, GOLD, CORAL)[index])
        draw_addition_symbol(pdf, "=", 419, y + 46, 24)
        draw_write_box(pdf, 465, y + 46, 66)


def draw_story_drawing_rows(pdf: canvas.Canvas, items: list[dict]) -> None:
    accents = (CORAL, BLUE)
    for index, item in enumerate(items):
        y = 326 - index * 215
        accent = accents[index]
        pdf.setFillColor(white)
        pdf.setStrokeColor(accent)
        pdf.setLineWidth(1.5)
        pdf.roundRect(48, y, PAGE_WIDTH - 96, 190, 12, fill=1, stroke=1)
        pdf.setFillColor(accent)
        pdf.roundRect(48, y, 8, 190, 4, fill=1, stroke=0)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(67, y + 164, item["story"])
        pdf.setFillColor(PALE_TEAL)
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.3)
        pdf.roundRect(67, y + 48, PAGE_WIDTH - 134, 102, 10, fill=1, stroke=1)
        symbol = "+" if item["operation"] == "addition" else "-"
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawRightString(455, y + 18, f'{item["left"]} {symbol} {item["right"]} =')
        draw_write_box(pdf, 470, y + 25, 52)


def build_story_problem_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_story_problem_pack(data)
    for section_number, page in enumerate(data["pages"], start=1):
        draw_header(pdf, {**data, "page_instruction": page["subtitle"]})
        activity = page["activity"]
        section_heading(pdf, section_number, activity["title"], activity["prompt"], 585)
        if page["type"] == "put-together":
            draw_put_together_story_rows(pdf, activity["items"], 540, 147)
        elif page["type"] == "take-away":
            draw_take_away_story_rows(pdf, activity["items"], 540, 147)
        elif page["type"] == "look-solve":
            draw_mixed_story_rows(pdf, activity["items"], 540, 147)
        elif page["type"] == "choose-operation":
            draw_mixed_story_rows(pdf, activity["items"], 540, 147, True)
        else:
            draw_story_drawing_rows(pdf, activity["items"])
        draw_footer(pdf)
        pdf.showPage()


SHAPE_COLORS = {"circle": CORAL, "square": BLUE, "triangle": GOLD, "rectangle": GREEN}


def draw_basic_shape(pdf: canvas.Canvas, kind: str, center_x: float, center_y: float,
                     size: float, fill: bool = True, traced: bool = False) -> None:
    """Draw one reusable circle, square, triangle, or rectangle."""
    if kind not in SHAPE_COLORS:
        raise ValueError(f"Unknown 2D shape: {kind}")
    pdf.setStrokeColor(INK if traced else TEAL_DARK)
    pdf.setFillColor(SHAPE_COLORS[kind] if fill else white)
    pdf.setLineWidth(2 if traced else 1.5)
    if traced:
        pdf.setDash(2.2, 3.2)
    if kind == "circle":
        pdf.circle(center_x, center_y, size * .42, fill=int(fill), stroke=1)
    elif kind == "square":
        side = size * .82
        pdf.rect(center_x - side / 2, center_y - side / 2, side, side,
                 fill=int(fill), stroke=1)
    elif kind == "triangle":
        path = pdf.beginPath()
        path.moveTo(center_x, center_y + size * .46)
        path.lineTo(center_x - size * .46, center_y - size * .38)
        path.lineTo(center_x + size * .46, center_y - size * .38)
        path.close()
        pdf.drawPath(path, fill=int(fill), stroke=1)
    else:
        width, height = size * 1.08, size * .7
        pdf.rect(center_x - width / 2, center_y - height / 2, width, height,
                 fill=int(fill), stroke=1)
    if traced:
        pdf.setDash()


def draw_meet_shapes(pdf: canvas.Canvas, shapes: list[str]) -> None:
    for index, shape in enumerate(shapes):
        center_y = 490 - index * 102
        pdf.setFillColor(white)
        pdf.setStrokeColor(SHAPE_COLORS[shape])
        pdf.setLineWidth(1.4)
        pdf.roundRect(52, center_y - 40, PAGE_WIDTH - 104, 80, 11, fill=1, stroke=1)
        draw_basic_shape(pdf, shape, 120, center_y, 60)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawString(174, center_y - 6, shape.title())
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica", 10.5)
        pdf.drawString(174, center_y - 24, "Trace the shape.")
        draw_basic_shape(pdf, shape, 448, center_y, 64, False, True)


def draw_find_shapes(pdf: canvas.Canvas, items: list[dict]) -> None:
    for index, item in enumerate(items):
        center_y = 490 - index * 102
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(52, center_y + 31, f'Find the {item["target"]}.')
        choices = item["choices"]
        for choice_index, shape in enumerate(choices):
            draw_basic_shape(pdf, shape, 102 + choice_index * 102, center_y - 4, 53)
        if index < len(items) - 1:
            pdf.setStrokeColor(BORDER)
            pdf.setLineWidth(.8)
            pdf.line(52, center_y - 47, PAGE_WIDTH - 52, center_y - 47)


def draw_match_shapes(pdf: canvas.Canvas, left: list[str], right: list[str]) -> None:
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(67, 523, "SHAPES")
    pdf.drawRightString(PAGE_WIDTH - 67, 523, "MATCH")
    for index, shape in enumerate(left):
        center_y = 465 - index * 100
        draw_basic_shape(pdf, shape, 112, center_y, 64)
        draw_basic_shape(pdf, right[index], 500, center_y, 64)


def draw_trace_and_draw_shapes(pdf: canvas.Canvas, shapes: list[str]) -> None:
    for index, shape in enumerate(shapes):
        center_y = 485 - index * 104
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(53, center_y + 34, shape.title())
        draw_basic_shape(pdf, shape, 135, center_y - 5, 65, False, True)
        pdf.setFillColor(PALE_TEAL)
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.3)
        pdf.roundRect(230, center_y - 43, 320, 82, 10, fill=1, stroke=1)
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(244, center_y + 23, "Draw it here")


def draw_shape_object(pdf: canvas.Canvas, kind: str, center_x: float, center_y: float,
                      size: float) -> None:
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.5)
    if kind == "sun":
        pdf.setFillColor(GOLD)
        pdf.circle(center_x, center_y, size * .28, fill=1, stroke=1)
        for angle in range(0, 360, 45):
            radians = math.radians(angle)
            pdf.line(center_x + math.cos(radians) * size * .38,
                     center_y + math.sin(radians) * size * .38,
                     center_x + math.cos(radians) * size * .53,
                     center_y + math.sin(radians) * size * .53)
    elif kind == "window":
        pdf.setFillColor(BLUE)
        pdf.rect(center_x - size * .4, center_y - size * .4, size * .8, size * .8, fill=1, stroke=1)
        pdf.setStrokeColor(white)
        pdf.line(center_x, center_y - size * .4, center_x, center_y + size * .4)
        pdf.line(center_x - size * .4, center_y, center_x + size * .4, center_y)
    elif kind == "sign":
        draw_basic_shape(pdf, "triangle", center_x, center_y + 5, size * .9)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(3)
        pdf.line(center_x, center_y - size * .35, center_x, center_y - size * .7)
    elif kind == "door":
        pdf.setFillColor(GREEN)
        pdf.rect(center_x - size * .3, center_y - size * .45, size * .6, size * .9, fill=1, stroke=1)
        pdf.setFillColor(GOLD)
        pdf.circle(center_x + size * .18, center_y, 2.5, fill=1, stroke=0)
    else:
        raise ValueError(f"Unknown familiar shape object: {kind}")


def draw_shapes_around_us(pdf: canvas.Canvas, items: list[dict]) -> None:
    for index, item in enumerate(items):
        center_y = 490 - index * 102
        pdf.setFillColor(white)
        pdf.setStrokeColor(SHAPE_COLORS[item["answer"]])
        pdf.setLineWidth(1.3)
        pdf.roundRect(52, center_y - 41, PAGE_WIDTH - 104, 82, 10, fill=1, stroke=1)
        draw_shape_object(pdf, item["object"], 112, center_y, 62)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(160, center_y + 22, f'{item["label"]}: Circle its shape.')
        for choice_index, shape in enumerate(item["choices"]):
            draw_basic_shape(pdf, shape, 245 + choice_index * 105, center_y - 10, 45, False)


def validate_shapes_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["meet", "find", "match", "trace-draw", "around-us"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"2D Shapes pack pages must be {expected_types}.")
    allowed = set(SHAPE_COLORS)
    for page in pages:
        activity = page.get("activity", {})
        serialized = json.dumps(activity)
        mentioned = {shape for shape in allowed if shape in serialized}
        if not mentioned or not mentioned.issubset(allowed):
            raise ValueError("Every shapes page must use supported 2D shapes.")


def build_shapes_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_shapes_pack(data)
    for section_number, page in enumerate(data["pages"], start=1):
        draw_header(pdf, {**data, "subtitle": page["subtitle"]})
        activity = page["activity"]
        section_heading(pdf, section_number, activity["title"], activity["prompt"], 585)
        if page["type"] == "meet":
            draw_meet_shapes(pdf, activity["shapes"])
        elif page["type"] == "find":
            draw_find_shapes(pdf, activity["items"])
        elif page["type"] == "match":
            draw_match_shapes(pdf, activity["left"], activity["right"])
        elif page["type"] == "trace-draw":
            draw_trace_and_draw_shapes(pdf, activity["shapes"])
        else:
            draw_shapes_around_us(pdf, activity["items"])
        draw_footer(pdf)
        pdf.showPage()


THREE_D_SHAPES = {"sphere", "cube", "cone", "cylinder", "rectangular prism"}
THREE_D_COLORS = {
    "sphere": CORAL,
    "cube": BLUE,
    "cone": ORANGE,
    "cylinder": PURPLE,
    "rectangular prism": GREEN,
}


def draw_3d_shape(pdf: canvas.Canvas, kind: str, center_x: float, center_y: float,
                  size: float, fill: bool = True, traced: bool = False) -> None:
    """Draw one simple, colorful, preschool-friendly 3D shape."""
    if kind not in THREE_D_SHAPES:
        raise ValueError(f"Unknown 3D shape: {kind}")
    color = THREE_D_COLORS[kind]
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setFillColor(color if fill else white)
    pdf.setLineWidth(1.7)
    if kind == "sphere":
        radius = size * .39
        pdf.circle(center_x, center_y, radius, fill=int(fill), stroke=1)
        pdf.setStrokeColor(white if fill else TEAL_DARK)
        pdf.setLineWidth(2.2)
        pdf.arc(center_x - radius * .7, center_y - radius,
                center_x + radius * .7, center_y + radius, 72, 216)
    elif kind in {"cube", "rectangular prism"}:
        width = size * (.86 if kind == "cube" else 1.08)
        height = size * (.72 if kind == "cube" else .58)
        depth = size * .22
        left = center_x - width / 2
        bottom = center_y - height / 2
        front = pdf.beginPath()
        front.moveTo(left, bottom)
        front.lineTo(left + width, bottom)
        front.lineTo(left + width, bottom + height)
        front.lineTo(left, bottom + height)
        front.close()
        pdf.drawPath(front, fill=int(fill), stroke=1)
        pdf.setFillColor(HexColor("#DDEFEA") if fill else white)
        top = pdf.beginPath()
        top.moveTo(left, bottom + height)
        top.lineTo(left + depth, bottom + height + depth)
        top.lineTo(left + width + depth, bottom + height + depth)
        top.lineTo(left + width, bottom + height)
        top.close()
        pdf.drawPath(top, fill=int(fill), stroke=1)
        pdf.setFillColor(HexColor("#C7DED8") if fill else white)
        side = pdf.beginPath()
        side.moveTo(left + width, bottom)
        side.lineTo(left + width + depth, bottom + depth)
        side.lineTo(left + width + depth, bottom + height + depth)
        side.lineTo(left + width, bottom + height)
        side.close()
        pdf.drawPath(side, fill=int(fill), stroke=1)
    elif kind == "cone":
        half_width = size * .38
        top_y = center_y + size * .42
        base_y = center_y - size * .28
        path = pdf.beginPath()
        path.moveTo(center_x, top_y)
        path.lineTo(center_x - half_width, base_y)
        path.lineTo(center_x + half_width, base_y)
        path.close()
        pdf.drawPath(path, fill=int(fill), stroke=1)
        pdf.ellipse(center_x - half_width, base_y - size * .10,
                    center_x + half_width, base_y + size * .10, fill=int(fill), stroke=1)
    else:
        half_width = size * .34
        top_y = center_y + size * .34
        bottom_y = center_y - size * .34
        pdf.rect(center_x - half_width, bottom_y, half_width * 2,
                 top_y - bottom_y, fill=int(fill), stroke=1)
        pdf.ellipse(center_x - half_width, top_y - size * .10,
                    center_x + half_width, top_y + size * .10, fill=int(fill), stroke=1)
        pdf.ellipse(center_x - half_width, bottom_y - size * .10,
                    center_x + half_width, bottom_y + size * .10, fill=int(fill), stroke=1)


def draw_introduce_3d_shapes(pdf: canvas.Canvas, items: list[dict]) -> None:
    centers = (510, 421, 332, 243, 154)
    for index, item in enumerate(items):
        center_y = centers[index]
        shape = item["shape"]
        pdf.setFillColor(HexColor("#F8FCFB"))
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.2)
        pdf.roundRect(52, center_y - 34, PAGE_WIDTH - 104, 68, 11, fill=1, stroke=1)
        shape_y = center_y - 4 if shape == "cube" else center_y
        draw_3d_shape(pdf, shape, 104, shape_y, 58)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(165, center_y + 7, shape.title())
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica", 10.5)
        pdf.drawString(165, center_y - 13, f'A {item["label"].lower()} has this shape.')
        draw_3d_shape_object(pdf, item["object"], 485, center_y, 59)


def draw_identify_3d_shapes(pdf: canvas.Canvas, items: list[dict]) -> None:
    centers = (500, 383, 266, 149)
    for index, item in enumerate(items):
        center_y = centers[index]
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(58, center_y + 39, f'Find the {item["target"]}.')
        pdf.setFillColor(HexColor("#F8FCFB"))
        pdf.setStrokeColor(BORDER)
        pdf.roundRect(52, center_y - 48, PAGE_WIDTH - 104, 78, 11, fill=1, stroke=1)
        for choice_index, object_name in enumerate(item["objects"]):
            draw_3d_shape_object(pdf, object_name, 150 + choice_index * 157,
                                 center_y - 9, 67)


def draw_match_3d_shapes(pdf: canvas.Canvas, left: list[str], right: list[str]) -> None:
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(67, 523, "SHAPES")
    pdf.drawRightString(PAGE_WIDTH - 67, 523, "MATCH")
    centers = (485, 399, 313, 227, 141)
    for index, shape in enumerate(left):
        center_y = centers[index]
        draw_3d_shape(pdf, shape, 112, center_y, 63)
        draw_3d_shape_object(pdf, right[index], 500, center_y, 66)


def draw_choice_pill(pdf: canvas.Canvas, label: str, center_x: float,
                     center_y: float, width: float = 112) -> None:
    pdf.setFillColor(white)
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1.2)
    pdf.roundRect(center_x - width / 2, center_y - 13, width, 26, 13, fill=1, stroke=1)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 8.5 if len(label) > 12 else 10)
    pdf.drawCentredString(center_x, center_y - 3.5, label)


def draw_classify_3d_shapes(pdf: canvas.Canvas, items: list[dict]) -> None:
    centers = (510, 421, 332, 243, 154)
    for index, item in enumerate(items):
        center_y = centers[index]
        pdf.setFillColor(HexColor("#F8FCFB"))
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.2)
        pdf.roundRect(52, center_y - 34, PAGE_WIDTH - 104, 68, 11, fill=1, stroke=1)
        draw_3d_shape_object(pdf, item["object"], 102, center_y, 59)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(165, center_y + 7, item["label"])
        draw_choice_pill(pdf, item["choices"][0], 345, center_y, 128)
        draw_choice_pill(pdf, item["choices"][1], 490, center_y, 128)


def draw_3d_shape_object(pdf: canvas.Canvas, kind: str, center_x: float,
                         center_y: float, size: float) -> None:
    if kind == "ball":
        radius = size * .38
        pdf.setFillColor(CORAL)
        pdf.setStrokeColor(TEAL_DARK)
        pdf.setLineWidth(1.7)
        pdf.circle(center_x, center_y, radius, fill=1, stroke=1)
        pdf.setStrokeColor(white)
        pdf.setLineWidth(2.5)
        pdf.arc(center_x - radius * .75, center_y - radius,
                center_x + radius * .75, center_y + radius, 68, 220)
        pdf.arc(center_x - radius, center_y - radius * .55,
                center_x + radius, center_y + radius * .55, 195, 145)
    elif kind == "block":
        draw_3d_shape(pdf, "cube", center_x, center_y - 4, size)
        pdf.setFillColor(white)
        pdf.setFont("Helvetica-Bold", max(9, size * .22))
        pdf.drawCentredString(center_x, center_y - 4 - size * .10, "A")
    elif kind == "traffic cone":
        draw_3d_shape(pdf, "cone", center_x, center_y + 3, size)
        pdf.setStrokeColor(INK)
        pdf.setFillColor(ORANGE)
        pdf.rect(center_x - size * .42, center_y - size * .34,
                 size * .84, size * .10, fill=1, stroke=1)
        pdf.setStrokeColor(white)
        pdf.setLineWidth(3)
        pdf.line(center_x - size * .22, center_y - size * .08,
                 center_x + size * .22, center_y - size * .08)
    elif kind == "can":
        draw_3d_shape(pdf, "cylinder", center_x, center_y, size)
        pdf.setFillColor(white)
        pdf.setStrokeColor(white)
        pdf.roundRect(center_x - size * .21, center_y - size * .10,
                      size * .42, size * .20, 3, fill=1, stroke=0)
        pdf.setFillColor(PURPLE)
        pdf.setFont("Helvetica-Bold", max(7, size * .14))
        pdf.drawCentredString(center_x, center_y - size * .045, "CAN")
    elif kind == "box":
        draw_3d_shape(pdf, "rectangular prism", center_x, center_y - 3, size)
        pdf.setFillColor(white)
        pdf.setStrokeColor(white)
        pdf.rect(center_x - size * .17, center_y - 3 - size * .12,
                 size * .34, size * .21, fill=1, stroke=0)
    else:
        raise ValueError(f"Unknown familiar 3D shape object: {kind}")


def draw_3d_shapes_around_us(pdf: canvas.Canvas, items: list[dict]) -> None:
    centers = (510, 421, 332, 243, 154)
    for index, item in enumerate(items):
        center_y = centers[index]
        pdf.setFillColor(HexColor("#F8FCFB"))
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.2)
        pdf.roundRect(52, center_y - 38, PAGE_WIDTH - 104, 76, 11, fill=1, stroke=1)
        draw_3d_shape_object(pdf, item["object"], 102, center_y, 66)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(165, center_y + 12, item["label"])
        for choice_index, shape in enumerate(item["choices"]):
            draw_choice_pill(pdf, shape.title(), 260 + choice_index * 112,
                             center_y - 11, 104)


def validate_3d_shapes_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["introduce", "identify", "match", "classify", "around-us"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"3D Shapes pack pages must be {expected_types}.")
    serialized = json.dumps(pages)
    if any(shape not in serialized for shape in THREE_D_SHAPES):
        raise ValueError("3D Shapes pack must use all five supported shapes.")


def build_3d_shapes_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_3d_shapes_pack(data)
    for section_number, page in enumerate(data["pages"], start=1):
        draw_header(pdf, {**data, "subtitle": page["subtitle"]})
        activity = page["activity"]
        section_heading(pdf, section_number, activity["title"], activity["prompt"], 585)
        if page["type"] == "introduce":
            draw_introduce_3d_shapes(pdf, activity["items"])
        elif page["type"] == "identify":
            draw_identify_3d_shapes(pdf, activity["items"])
        elif page["type"] == "match":
            draw_match_3d_shapes(pdf, activity["left"], activity["right"])
        elif page["type"] == "classify":
            draw_classify_3d_shapes(pdf, activity["items"])
        else:
            draw_3d_shapes_around_us(pdf, activity["items"])
        draw_footer(pdf)
        pdf.showPage()


POSITION_WORDS = {"above", "below", "in", "on", "under", "next to", "between"}


def draw_position_object(pdf: canvas.Canvas, kind: str, center_x: float,
                         center_y: float, size: float) -> None:
    """Draw one familiar object used by the positional-words pack."""
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1.5)
    if kind == "ball":
        draw_3d_shape_object(pdf, "ball", center_x, center_y, size)
    elif kind == "block":
        draw_3d_shape_object(pdf, "block", center_x, center_y, size)
    elif kind == "table":
        pdf.setFillColor(ORANGE)
        pdf.roundRect(center_x - size * .48, center_y, size * .96, size * .18,
                      3, fill=1, stroke=1)
        pdf.rect(center_x - size * .38, center_y - size * .48,
                 size * .13, size * .48, fill=1, stroke=1)
        pdf.rect(center_x + size * .25, center_y - size * .48,
                 size * .13, size * .48, fill=1, stroke=1)
    elif kind == "shelf":
        pdf.setFillColor(BLUE)
        pdf.roundRect(center_x - size * .5, center_y - size * .06,
                      size, size * .18, 3, fill=1, stroke=1)
        pdf.rect(center_x - size * .44, center_y - size * .22,
                 size * .09, size * .17, fill=1, stroke=1)
        pdf.rect(center_x + size * .35, center_y - size * .22,
                 size * .09, size * .17, fill=1, stroke=1)
    elif kind == "box":
        pdf.setFillColor(GOLD)
        pdf.rect(center_x - size * .44, center_y - size * .34,
                 size * .88, size * .68, fill=1, stroke=1)
        pdf.setFillColor(HexColor("#F9D983"))
        pdf.rect(center_x - size * .44, center_y + size * .18,
                 size * .88, size * .16, fill=1, stroke=1)
    elif kind == "chair":
        pdf.setFillColor(PURPLE)
        pdf.roundRect(center_x - size * .32, center_y - size * .02,
                      size * .64, size * .18, 3, fill=1, stroke=1)
        pdf.roundRect(center_x - size * .30, center_y + size * .15,
                      size * .60, size * .48, 4, fill=1, stroke=1)
        pdf.rect(center_x - size * .25, center_y - size * .40,
                 size * .10, size * .38, fill=1, stroke=1)
        pdf.rect(center_x + size * .15, center_y - size * .40,
                 size * .10, size * .38, fill=1, stroke=1)
    elif kind == "kite":
        pdf.setFillColor(CORAL)
        path = pdf.beginPath()
        path.moveTo(center_x, center_y + size * .45)
        path.lineTo(center_x + size * .34, center_y)
        path.lineTo(center_x, center_y - size * .45)
        path.lineTo(center_x - size * .34, center_y)
        path.close()
        pdf.drawPath(path, fill=1, stroke=1)
        pdf.setStrokeColor(PURPLE)
        pdf.line(center_x, center_y - size * .45,
                 center_x + size * .16, center_y - size * .72)
    elif kind == "teddy":
        pdf.setFillColor(ORANGE)
        pdf.circle(center_x - size * .22, center_y + size * .27,
                   size * .13, fill=1, stroke=1)
        pdf.circle(center_x + size * .22, center_y + size * .27,
                   size * .13, fill=1, stroke=1)
        pdf.circle(center_x, center_y + size * .14, size * .29, fill=1, stroke=1)
        pdf.circle(center_x, center_y - size * .22, size * .31, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.circle(center_x - size * .10, center_y + size * .20,
                   size * .025, fill=1, stroke=0)
        pdf.circle(center_x + size * .10, center_y + size * .20,
                   size * .025, fill=1, stroke=0)
    elif kind == "tree":
        pdf.setFillColor(ORANGE)
        pdf.rect(center_x - size * .09, center_y - size * .40,
                 size * .18, size * .48, fill=1, stroke=1)
        pdf.setFillColor(GREEN)
        pdf.circle(center_x, center_y + size * .18, size * .35, fill=1, stroke=1)
        pdf.circle(center_x - size * .24, center_y + size * .10,
                   size * .24, fill=1, stroke=1)
        pdf.circle(center_x + size * .24, center_y + size * .10,
                   size * .24, fill=1, stroke=1)
    elif kind == "flower":
        pdf.setStrokeColor(GREEN)
        pdf.setLineWidth(2.3)
        pdf.line(center_x, center_y - size * .38, center_x, center_y + size * .03)
        pdf.setFillColor(CORAL)
        for dx, dy in ((0, .18), (.17, .06), (.10, -.13), (-.10, -.13), (-.17, .06)):
            pdf.circle(center_x + size * dx, center_y + size * (.15 + dy),
                       size * .13, fill=1, stroke=1)
        pdf.setFillColor(GOLD)
        pdf.circle(center_x, center_y + size * .15, size * .11, fill=1, stroke=1)
    elif kind == "bird":
        pdf.setFillColor(BLUE)
        pdf.ellipse(center_x - size * .34, center_y - size * .20,
                    center_x + size * .30, center_y + size * .23, fill=1, stroke=1)
        pdf.setFillColor(GOLD)
        beak = pdf.beginPath()
        beak.moveTo(center_x + size * .30, center_y + size * .05)
        beak.lineTo(center_x + size * .50, center_y + size * .14)
        beak.lineTo(center_x + size * .30, center_y + size * .20)
        beak.close()
        pdf.drawPath(beak, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.circle(center_x + size * .14, center_y + size * .13,
                   size * .025, fill=1, stroke=0)
    elif kind == "apple":
        pdf.setFillColor(CORAL)
        pdf.circle(center_x - size * .10, center_y, size * .27, fill=1, stroke=1)
        pdf.circle(center_x + size * .10, center_y, size * .27, fill=1, stroke=1)
        pdf.setStrokeColor(TEAL_DARK)
        pdf.line(center_x, center_y + size * .23,
                 center_x + size * .04, center_y + size * .42)
    elif kind == "star":
        pdf.setFillColor(GOLD)
        path = pdf.beginPath()
        for point in range(10):
            angle = math.radians(90 + point * 36)
            radius = size * (.42 if point % 2 == 0 else .19)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            (path.moveTo if point == 0 else path.lineTo)(x, y)
        path.close()
        pdf.drawPath(path, fill=1, stroke=1)
    else:
        raise ValueError(f"Unknown positional-words object: {kind}")


def draw_relation_scene(pdf: canvas.Canvas, relation: str, center_x: float,
                        center_y: float, size: float, subject: str = "ball",
                        anchor: str | None = None) -> None:
    """Draw a compact scene with one unmistakable spatial relationship."""
    if relation == "above":
        draw_position_object(pdf, subject, center_x, center_y + size * .25, size * .42)
        draw_position_object(pdf, anchor or "table", center_x, center_y - size * .27, size * .48)
    elif relation == "below":
        draw_position_object(pdf, anchor or "shelf", center_x, center_y + size * .26, size * .62)
        draw_position_object(pdf, subject, center_x, center_y - size * .25, size * .42)
    elif relation == "in":
        draw_position_object(pdf, "box", center_x, center_y - size * .08, size * .65)
        draw_position_object(pdf, subject, center_x, center_y + size * .03, size * .34)
    elif relation == "on":
        draw_position_object(pdf, "table", center_x, center_y - size * .20, size * .65)
        draw_position_object(pdf, subject, center_x, center_y + size * .06, size * .38)
    elif relation == "under":
        draw_position_object(pdf, "table", center_x, center_y + size * .20, size * .68)
        draw_position_object(pdf, subject, center_x, center_y - size * .26, size * .38)
    elif relation == "next to":
        draw_position_object(pdf, "block", center_x - size * .24, center_y, size * .45)
        draw_position_object(pdf, subject, center_x + size * .25, center_y, size * .42)
    elif relation == "between":
        draw_position_object(pdf, "apple", center_x - size * .36, center_y, size * .38)
        draw_position_object(pdf, subject, center_x, center_y, size * .38)
        draw_position_object(pdf, "star", center_x + size * .36, center_y, size * .38)
    else:
        raise ValueError(f"Unknown positional relationship: {relation}")


def draw_introduce_positions(pdf: canvas.Canvas, items: list[str]) -> None:
    centers = (512, 416, 320, 224, 128)
    for index, relation in enumerate(items):
        center_y = centers[index]
        pdf.setFillColor(HexColor("#F8FCFB"))
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.2)
        pdf.roundRect(52, center_y - 41, PAGE_WIDTH - 104, 82, 11, fill=1, stroke=1)
        draw_relation_scene(pdf, relation, 137, center_y + 3, 80)
        pdf.setFillColor(TEAL_DARK)
        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawString(247, center_y - 6, relation.upper())


def draw_above_below_positions(pdf: canvas.Canvas, items: list[dict]) -> None:
    centers = (492, 367, 242, 117)
    for index, item in enumerate(items):
        center_y = centers[index]
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(58, center_y + 52, item["prompt"])
        pdf.setFillColor(HexColor("#F8FCFB"))
        pdf.setStrokeColor(BORDER)
        pdf.roundRect(52, center_y - 45, PAGE_WIDTH - 104, 86, 11, fill=1, stroke=1)
        subject = item.get("subject", "ball")
        anchor = "table" if "table" in item["prompt"].lower() else "shelf"
        draw_relation_scene(pdf, "above", 205, center_y + 5, 84, subject, anchor)
        draw_relation_scene(pdf, "below", 410, center_y + 5, 84, subject, anchor)


def draw_in_on_under_positions(pdf: canvas.Canvas, items: list[dict]) -> None:
    centers = (478, 303, 128)
    choices = ("in", "on", "under")
    for index, item in enumerate(items):
        center_y = centers[index]
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(58, center_y + 69, item["prompt"])
        pdf.setFillColor(HexColor("#F8FCFB"))
        pdf.setStrokeColor(BORDER)
        pdf.roundRect(52, center_y - 64, PAGE_WIDTH - 104, 122, 11, fill=1, stroke=1)
        for choice_index, relation in enumerate(choices):
            draw_relation_scene(pdf, relation, 140 + choice_index * 166,
                                center_y - 4, 104)


def draw_next_to_between_positions(pdf: canvas.Canvas, items: list[dict]) -> None:
    centers = (492, 367, 242, 117)
    for index, item in enumerate(items):
        center_y = centers[index]
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(58, center_y + 52, item["prompt"])
        pdf.setFillColor(HexColor("#F8FCFB"))
        pdf.setStrokeColor(BORDER)
        pdf.roundRect(52, center_y - 45, PAGE_WIDTH - 104, 86, 11, fill=1, stroke=1)
        if item["kind"] == "next to":
            positions = (184, 257, 456)
        else:
            positions = (184, 306, 428)
        for object_name, x in zip(item["objects"], positions):
            draw_position_object(pdf, object_name, x, center_y + 3, 64)


def draw_position_review(pdf: canvas.Canvas, items: list[dict]) -> None:
    centers = (512, 416, 320, 224, 128)
    for index, item in enumerate(items):
        center_y = centers[index]
        pdf.setFillColor(HexColor("#F8FCFB"))
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.2)
        pdf.roundRect(52, center_y - 43, PAGE_WIDTH - 104, 86, 11, fill=1, stroke=1)
        scene_size = 86 if item["relation"] != "between" else 104
        draw_relation_scene(pdf, item["relation"], 137, center_y + 4, scene_size)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 11.5)
        pdf.drawString(220, center_y + 13, item["question"])
        draw_choice_pill(pdf, item["choices"][0], 355, center_y - 11, 112)
        draw_choice_pill(pdf, item["choices"][1], 485, center_y - 11, 112)


def validate_positional_words_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["introduce", "above-below", "in-on-under", "next-to-between", "review"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Positional Words pack pages must be {expected_types}.")
    serialized = json.dumps(pages).lower()
    if any(word not in serialized for word in POSITION_WORDS):
        raise ValueError("Positional Words pack must cover all seven supported relationships.")


def build_positional_words_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_positional_words_pack(data)
    for section_number, page in enumerate(data["pages"], start=1):
        draw_header(pdf, {**data, "subtitle": page["subtitle"]})
        activity = page["activity"]
        section_heading(pdf, section_number, activity["title"], activity["prompt"], 585)
        if page["type"] == "introduce":
            draw_introduce_positions(pdf, activity["items"])
        elif page["type"] == "above-below":
            draw_above_below_positions(pdf, activity["items"])
        elif page["type"] == "in-on-under":
            draw_in_on_under_positions(pdf, activity["items"])
        elif page["type"] == "next-to-between":
            draw_next_to_between_positions(pdf, activity["items"])
        else:
            draw_position_review(pdf, activity["items"])
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


PATTERN_OBJECT_KINDS = frozenset({
    "apple", "star", "balloon", "flower", "fish", "leaf", "car", "butterfly",
})


def _require_object_kind(kind: str, context: str) -> str:
    if kind not in PATTERN_OBJECT_KINDS:
        raise ValueError(f"{context} uses unsupported object kind: {kind!r}.")
    return kind


PATTERN_SHAPE_COLORS = {
    "red": CORAL, "blue": BLUE, "yellow": GOLD, "green": GREEN, "purple": PURPLE,
}
PATTERN_SHAPES = ("circle", "square", "triangle")


def draw_pattern_shape(pdf: canvas.Canvas, spec: dict, center_x: float,
                       center_y: float, size: float) -> None:
    """Draw one simple shape a preschooler can copy: circle, square, triangle."""
    shape = spec.get("shape")
    color = PATTERN_SHAPE_COLORS.get(spec.get("color"))
    scale = spec.get("scale", 1.0)
    if shape not in PATTERN_SHAPES or color is None:
        raise ValueError(f"Bad pattern shape spec: {spec!r}.")
    if not isinstance(scale, (int, float)) or not 0.2 <= scale <= 1.5:
        raise ValueError(f"Bad pattern shape scale: {spec!r}.")
    size = size * scale
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.setFillColor(color)
    if shape == "circle":
        pdf.circle(center_x, center_y, size * .40, fill=1, stroke=1)
    elif shape == "square":
        side = size * .78
        pdf.rect(center_x - side / 2, center_y - side / 2, side, side,
                 fill=1, stroke=1)
    else:
        path = pdf.beginPath()
        path.moveTo(center_x, center_y + size * .44)
        path.lineTo(center_x - size * .44, center_y - size * .36)
        path.lineTo(center_x + size * .44, center_y - size * .36)
        path.close()
        pdf.drawPath(path, fill=1, stroke=1)


def _validate_pattern_spec(value, context: str) -> None:
    if isinstance(value, dict):
        if value.get("shape") not in PATTERN_SHAPES:
            raise ValueError(f"{context} uses unsupported shape: {value!r}.")
        if value.get("color") not in PATTERN_SHAPE_COLORS:
            raise ValueError(f"{context} uses unsupported color: {value!r}.")
        scale = value.get("scale", 1.0)
        if not isinstance(scale, (int, float)) or not 0.2 <= scale <= 1.5:
            raise ValueError(f"{context} uses unsupported scale: {value!r}.")
    else:
        _require_object_kind(value, context)


def draw_pattern_cells(pdf: canvas.Canvas, sequence: list, x: float, y: float,
                       box: float = 48.0, gap: float = 10.0) -> None:
    """Draw a row of pattern cells; None entries render as dashed blanks."""
    for index, kind in enumerate(sequence):
        cell_x = x + index * (box + gap)
        center_x, center_y = cell_x + box / 2, y + box / 2
        if kind is None:
            pdf.setFillColor(white)
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(1.6)
            pdf.setDash(6, 4)
            pdf.roundRect(cell_x, y, box, box, 9, fill=1, stroke=1)
            pdf.setDash()
            pdf.setFillColor(TEAL_DARK)
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawCentredString(center_x, center_y - 7, "?")
        else:
            _require_object_kind(kind, "Pattern")
            pdf.setFillColor(white)
            pdf.setStrokeColor(BORDER)
            pdf.setLineWidth(1.2)
            pdf.roundRect(cell_x, y, box, box, 9, fill=1, stroke=1)
            draw_object(pdf, kind, center_x, center_y, box * 0.68)


def draw_choice_circles(pdf: canvas.Canvas, choices: list, x: float, y: float,
                        radius: float = 24.0, gap: float = 18.0) -> None:
    accents = (TEAL, BLUE, GOLD, CORAL, PURPLE)
    for index, kind in enumerate(choices):
        _require_object_kind(kind, "Pattern choice")
        center_x = x + radius + index * (radius * 2 + gap)
        pdf.setFillColor(white)
        pdf.setStrokeColor(accents[index % len(accents)])
        pdf.setLineWidth(2)
        pdf.circle(center_x, y, radius, fill=1, stroke=1)
        draw_object(pdf, kind, center_x, y, radius * 1.1)


def draw_meet_patterns(pdf: canvas.Canvas, items: list) -> None:
    y = 490
    for item in items:
        pdf.setFillColor(TEAL_DARK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(55, y + 58, item["label"])
        draw_pattern_cells(pdf, item["sequence"], 55, y, box=46.0)
        y -= 118


def draw_pattern_next(pdf: canvas.Canvas, items: list) -> None:
    y = 460
    for item in items:
        draw_pattern_cells(pdf, list(item["sequence"]) + [None], 55, y + 50, box=44.0)
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(55, y + 16, "Choices: circle what comes next.")
        draw_choice_circles(pdf, item["choices"], 55, y - 14, radius=24.0)
        y -= 118


def draw_pattern_finish(pdf: canvas.Canvas, items: list) -> None:
    y = 496
    for item in items:
        blanks = set(item.get("blanks", []))
        sequence = [kind if index not in blanks else None
                    for index, kind in enumerate(item["sequence"])]
        draw_pattern_cells(pdf, sequence, 55, y, box=46.0, gap=9.0)
        y -= 120


def draw_pattern_copy(pdf: canvas.Canvas, items: list) -> None:
    y = 458
    for item in items:
        draw_pattern_cells(pdf, item["sequence"], 55, y + 56, box=44.0)
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica", 10.5)
        pdf.drawString(55, y + 32, "Copy it here:")
        draw_pattern_cells(pdf, [None] * len(item["sequence"]), 55, y - 30, box=44.0)
        y -= 150


def draw_pattern_create(pdf: canvas.Canvas, items: list) -> None:
    y = 488
    for item in items:
        pdf.setFillColor(TEAL_DARK)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(55, y + 58, item["label"])
        draw_pattern_cells(pdf, [None] * item["boxes"], 55, y - 4, box=46.0)
        y -= 140


def validate_patterns_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["meet", "next", "finish", "copy", "create"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Patterns pack pages must be {expected_types}.")
    for page in pages:
        activity = page.get("activity", {})
        for item in activity.get("items", []):
            for kind in item.get("sequence", []):
                _require_object_kind(kind, "Patterns")
            for kind in item.get("choices", []):
                _require_object_kind(kind, "Patterns")


def build_patterns_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_patterns_pack(data)
    for section_number, page in enumerate(data["pages"], start=1):
        draw_header(pdf, {**data, "subtitle": page["subtitle"]})
        activity = page["activity"]
        section_heading(pdf, section_number, activity["title"], activity["prompt"], 585)
        page_type = page["type"]
        if page_type == "meet":
            draw_meet_patterns(pdf, activity["items"])
        elif page_type == "next":
            draw_pattern_next(pdf, activity["items"])
        elif page_type == "finish":
            draw_pattern_finish(pdf, activity["items"])
        elif page_type == "copy":
            draw_pattern_copy(pdf, activity["items"])
        else:
            draw_pattern_create(pdf, activity["items"])
        draw_footer(pdf)
        pdf.showPage()


def draw_ribbon(pdf: canvas.Canvas, x: float, y: float, length: float,
                height: float, color) -> None:
    pdf.setFillColor(color)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.5)
    pdf.roundRect(x, y, length, height, height / 2, fill=1, stroke=1)


def draw_tower(pdf: canvas.Canvas, x: float, y: float, width: float,
               height: float, color) -> None:
    pdf.setFillColor(color)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.5)
    pdf.roundRect(x, y, width, height, 8, fill=1, stroke=1)
    pdf.setFillColor(white)
    rows = max(1, int((height - 18) // 32))
    for row in range(rows):
        window_y = y + 10 + row * 32
        if window_y + 15 > y + height - 8:
            break
        pdf.roundRect(x + width / 2 - 10, window_y, 20, 14, 3, fill=1, stroke=0)


def draw_cup(pdf: canvas.Canvas, center_x: float, y: float, width: float,
             height: float, fill_ratio: float, liquid) -> None:
    half_bottom, half_top = width / 2 - 2, width / 2 - 13
    fill_ratio = max(0.0, min(1.0, fill_ratio))
    fill_height = (height - 10) * fill_ratio
    if fill_height > 1:
        pdf.setFillColor(liquid)
        pdf.setStrokeColor(liquid)
        width_at = lambda depth: half_bottom - (half_bottom - half_top) * (depth / height)
        path = pdf.beginPath()
        path.moveTo(center_x - width_at(4), y + 4)
        path.lineTo(center_x + width_at(4), y + 4)
        path.lineTo(center_x + width_at(4 + fill_height), y + 4 + fill_height)
        path.lineTo(center_x - width_at(4 + fill_height), y + 4 + fill_height)
        path.close()
        pdf.drawPath(path, fill=1, stroke=0)
    outline = pdf.beginPath()
    outline.moveTo(center_x - half_bottom, y + 2)
    outline.lineTo(center_x + half_bottom, y + 2)
    outline.lineTo(center_x + half_top, y + height)
    outline.lineTo(center_x - half_top, y + height)
    outline.close()
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.8)
    pdf.drawPath(outline, fill=0, stroke=1)


def _draw_measured_shape(pdf: canvas.Canvas, item: dict, center_x: float,
                         center_y: float, size: float) -> None:
    """Draw a big simple shape for the measurement pack."""
    _validate_pattern_spec({"shape": item["shape"], "color": item["color"]},
                           "Measurement")
    draw_pattern_shape(pdf, {"shape": item["shape"], "color": item["color"],
                             "scale": 1.0}, center_x, center_y, size)


def draw_long_short(pdf: canvas.Canvas, items: list) -> None:
    """Three big ribbon pairs, centered, with plenty of space between rows."""
    for index, item in enumerate(items[:3]):
        top = 500 - index * 140
        first_long = item["longer"] == "first"
        lengths = (340, 190) if first_long else (190, 340)
        draw_ribbon(pdf, (PAGE_WIDTH - lengths[0]) / 2, top - 44, lengths[0], 44, CORAL)
        draw_ribbon(pdf, (PAGE_WIDTH - lengths[1]) / 2, top - 100, lengths[1], 44, BLUE)


def draw_tall_short(pdf: canvas.Canvas, items: list) -> None:
    """Three big tower pairs; rows well clear of the prompt and the footer."""
    for index, item in enumerate(items[:3]):
        top = 495 - index * 150
        tower_y = top - 140
        first_tall = item["taller"] == "first"
        heights = (130, 75) if first_tall else (75, 130)
        colors = (TEAL, GOLD, PURPLE) if first_tall else (BLUE, CORAL, TEAL)
        draw_tower(pdf, 150, tower_y, 70, heights[0], colors[index % 3])
        draw_tower(pdf, 392, tower_y, 70, heights[1], colors[(index + 1) % 3])
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(PAGE_WIDTH / 2, tower_y + 60, "OR")


def draw_big_small(pdf: canvas.Canvas, items: list) -> None:
    """Three big shape pairs; simple shapes a child could draw."""
    for index, item in enumerate(items[:3]):
        center_y = 440 - index * 150
        first_big = item["bigger"] == "first"
        sizes = (96, 52) if first_big else (52, 96)
        _draw_measured_shape(pdf, item, 170, center_y, sizes[0])
        _draw_measured_shape(pdf, item, 420, center_y, sizes[1])
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(PAGE_WIDTH / 2, center_y - 5, "OR")


def draw_capacity(pdf: canvas.Canvas, items: list) -> None:
    """Three big cup pairs with a clear more/less difference."""
    for index, item in enumerate(items[:3]):
        cup_y = 400 - index * 160
        first_full = item["fuller"] == "first"
        fills = (0.85, 0.25) if first_full else (0.25, 0.85)
        draw_cup(pdf, 170, cup_y, 150, 100, fills[0], BLUE)
        draw_cup(pdf, 420, cup_y, 150, 100, fills[1], BLUE)
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawCentredString(PAGE_WIDTH / 2, cup_y + 44, "OR")


def draw_order_by_size(pdf: canvas.Canvas, items: list) -> None:
    """Three big order rows; short label, then three large shapes."""
    for index, item in enumerate(items[:3]):
        top = 505 - index * 160
        pdf.setFillColor(TEAL_DARK)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(55, top - 14, item["label"])
        for center_x, size in zip((150, 306, 462), item["sizes"]):
            _draw_measured_shape(pdf, item, center_x, top - 80, size)


def validate_measurement_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["long-short", "tall-short", "big-small", "capacity", "order"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Measurement pack pages must be {expected_types}.")
    for page in pages:
        for item in page.get("activity", {}).get("items", []):
            if "shape" in item:
                _validate_pattern_spec({"shape": item["shape"],
                                        "color": item["color"]}, "Measurement")


def build_measurement_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_measurement_pack(data)
    for section_number, page in enumerate(data["pages"], start=1):
        draw_header(pdf, {**data, "subtitle": page["subtitle"]})
        activity = page["activity"]
        section_heading(pdf, section_number, activity["title"], activity["prompt"], 585)
        page_type = page["type"]
        if page_type == "long-short":
            draw_long_short(pdf, activity["items"])
        elif page_type == "tall-short":
            draw_tall_short(pdf, activity["items"])
        elif page_type == "big-small":
            draw_big_small(pdf, activity["items"])
        elif page_type == "capacity":
            draw_capacity(pdf, activity["items"])
        else:
            draw_order_by_size(pdf, activity["items"])
        draw_footer(pdf)
        pdf.showPage()


def draw_sort_row(pdf: canvas.Canvas, kinds: list, sizes: list, x: float, y: float,
                  box: float = 56.0, gap: float = 10.0) -> None:
    for index, kind in enumerate(kinds):
        _require_object_kind(kind, "Sorting")
        cell_x = x + index * (box + gap)
        pdf.setFillColor(white)
        pdf.setStrokeColor(BORDER)
        pdf.setLineWidth(1.2)
        pdf.roundRect(cell_x, y, box, box, 9, fill=1, stroke=1)
        size = sizes[index] if sizes else box * 0.66
        draw_object(pdf, kind, cell_x + box / 2, y + box / 2, size)


def draw_sort_kind(pdf: canvas.Canvas, items: list) -> None:
    y = 486
    for item in items:
        pdf.setFillColor(TEAL_DARK)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(55, y + 66, item["label"])
        draw_sort_row(pdf, item["objects"], item.get("sizes"), 55, y)
        y -= 122


def draw_match_groups(pdf: canvas.Canvas, items: list) -> None:
    y = 500
    for item in items:
        for index, kind in enumerate(item["choices"]):
            _require_object_kind(kind, "Sorting")
            center_x = 108 + index * 80
            pdf.setFillColor(white)
            pdf.setStrokeColor(TEAL)
            pdf.setLineWidth(1.8)
            pdf.circle(center_x, y, 31, fill=1, stroke=1)
            draw_object(pdf, kind, center_x, y, 34)
        for group_index, group_kind in enumerate(item["groups"]):
            _require_object_kind(group_kind, "Sorting")
            box_x = 372 + group_index * 118
            pdf.setFillColor(PALE_TEAL)
            pdf.setStrokeColor((GOLD, PURPLE)[group_index % 2])
            pdf.setLineWidth(1.6)
            pdf.roundRect(box_x, y - 35, 104, 70, 10, fill=1, stroke=1)
            draw_object(pdf, group_kind, box_x + 52, y, 36)
        y -= 115


def draw_picture_graph(pdf: canvas.Canvas, rows: list, questions: list,
                       y_top: float = 500) -> float:
    y = y_top
    for row in rows:
        _require_object_kind(row["object"], "Sorting")
        pdf.setFillColor(TEAL_DARK)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(55, y + 14, row["label"])
        for index in range(row["count"]):
            draw_object(pdf, row["object"], 175 + index * 62, y + 18, 40)
        y -= 78
    for question in questions:
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 11.5)
        pdf.drawString(55, y, question)
        y -= 30
    return y


def draw_sorting_review(pdf: canvas.Canvas, activity: dict) -> None:
    y = 486
    for item in activity["sort_items"]:
        pdf.setFillColor(TEAL_DARK)
        pdf.setFont("Helvetica-Bold", 12.5)
        pdf.drawString(55, y + 66, item["label"])
        draw_sort_row(pdf, item["objects"], item.get("sizes"), 55, y)
        y -= 122
    draw_picture_graph(pdf, activity["graph_rows"], activity["graph_questions"], y_top=y)


def validate_sorting_pack(data: dict) -> None:
    pages = data.get("pages")
    expected_types = ["sort-kind", "sort-size", "match-groups", "picture-graph", "review"]
    if not isinstance(pages, list) or [page.get("type") for page in pages] != expected_types:
        raise ValueError(f"Sorting pack pages must be {expected_types}.")
    for page in pages:
        activity = page.get("activity", {})
        for item in activity.get("items", []):
            for kind in item.get("objects", []) + item.get("choices", []) + item.get("groups", []):
                _require_object_kind(kind, "Sorting")
            if "target" in item:
                _require_object_kind(item["target"], "Sorting")
        for item in activity.get("sort_items", []):
            for kind in item.get("objects", []):
                _require_object_kind(kind, "Sorting")
        for row in activity.get("rows", []) + activity.get("graph_rows", []):
            _require_object_kind(row["object"], "Sorting")


def build_sorting_pack(pdf: canvas.Canvas, data: dict) -> None:
    validate_sorting_pack(data)
    for section_number, page in enumerate(data["pages"], start=1):
        draw_header(pdf, {**data, "subtitle": page["subtitle"]})
        activity = page["activity"]
        section_heading(pdf, section_number, activity["title"], activity["prompt"], 585)
        page_type = page["type"]
        if page_type in {"sort-kind", "sort-size"}:
            draw_sort_kind(pdf, activity["items"])
        elif page_type == "match-groups":
            draw_match_groups(pdf, activity["items"])
        elif page_type == "picture-graph":
            draw_picture_graph(pdf, activity["rows"], activity["questions"])
        else:
            draw_sorting_review(pdf, activity)
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
    if data.get("template") == "story-problems-pack":
        build_story_problem_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "shapes-pack":
        build_shapes_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "3d-shapes-pack":
        build_3d_shapes_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "positional-words-pack":
        build_positional_words_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "patterns-pack":
        build_patterns_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "measurement-pack":
        build_measurement_pack(pdf, data)
        pdf.save()
        return
    if data.get("template") == "sorting-pack":
        build_sorting_pack(pdf, data)
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


def resolve_bundle_output_path(data: dict, generator_dir: Path) -> Path:
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
    elif data.get("template") == "story-problems-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "addition"
    elif data.get("template") in {"shapes-pack", "3d-shapes-pack", "positional-words-pack"}:
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "shapes"
    elif data.get("template") == "patterns-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "patterns"
    elif data.get("template") == "measurement-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "measurement"
    elif data.get("template") == "sorting-pack":
        output_dir = generator_dir.parent / "worksheets" / "preschool" / "math" / "sorting"
    else:
        output_dir = generator_dir / "output"
    return output_dir / data["filename"]


def main() -> None:
    assets_only = len(sys.argv) == 3 and sys.argv[1] == "--assets-only"
    if (not assets_only and len(sys.argv) != 2) or (assets_only and len(sys.argv) != 3):
        raise SystemExit(
            "Usage: py -3 generate_worksheet.py [--assets-only] content/worksheet.json"
        )
    source_path = Path(sys.argv[2] if assets_only else sys.argv[1])
    data = json.loads(source_path.read_text(encoding="utf-8"))
    generator_dir = Path(__file__).parent
    repository_root = generator_dir.parent
    output_path = resolve_bundle_output_path(data, generator_dir)
    if not assets_only:
        build_pdf(data, output_path)

    asset_output = data.get("asset_output")
    if assets_only and asset_output is None:
        raise ValueError(f"{source_path} does not define asset_output.")
    if asset_output is not None:
        contract = BundleAssetContract.from_dict(asset_output)
        generated_assets = generate_bundle_assets(output_path, contract, repository_root)
        for asset in generated_assets:
            print(
                f"page={asset.page_number} pdf={asset.page_pdf_path.relative_to(repository_root)} "
                f"preview={asset.preview_path.relative_to(repository_root)} "
                f"dimensions={asset.preview_dimensions[0]}x{asset.preview_dimensions[1]}"
            )


if __name__ == "__main__":
    main()
