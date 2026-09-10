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
    logo_y = PAGE_HEIGHT - (76 if compact else 86)
    divider_top = PAGE_HEIGHT - (38 if compact else 46)
    divider_bottom = PAGE_HEIGHT - (102 if compact else 106)
    title_y = PAGE_HEIGHT - (63 if compact else 67)
    focus_y = PAGE_HEIGHT - (90 if compact else 98)
    subtitle_y = PAGE_HEIGHT - (92 if compact else 116)
    rule_y = PAGE_HEIGHT - (109 if compact else 131)
    fields_y = PAGE_HEIGHT - (136 if compact else 160)
    fields_rule_y = PAGE_HEIGHT - (139 if compact else 163)
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
    pdf.setFont("Helvetica-Bold", 23 if compact else 22)
    pdf.drawString(title_x, title_y, prefix + (":" if focus else ""))
    if focus:
        pdf.setFont("Helvetica-Bold", 30)
        pdf.drawString(title_x, focus_y, focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold" if compact else "Helvetica", 11.5)
    pdf.drawString(title_x, subtitle_y, data["subtitle"])
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
    pdf.drawString(224, 14, "*")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(243, 15, "Made with love for little learners.")
    pdf.drawRightString(PAGE_WIDTH - MARGIN, 15, "© 2026 Learning Made Simple")


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
    columns = {6: 3, 7: 4, 8: 4, 9: 3, 10: 5}.get(count, min(count, 5))
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
    range_max = data.get("range_max")
    if not isinstance(range_max, int) or range_max < 1 or range_max > 20:
        raise ValueError("Counting packs require an integer range_max from 1 through 20.")
    if not values or any(not isinstance(value, int) or value < 1 or value > range_max for value in values):
        raise ValueError(f"Counting pack content must use integers from 1 through {range_max} only.")


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
            if page.get("layout") == "extended":
                build_extended_mixed_pdf(pdf, page["activities"])
            else:
                build_counting_pdf(pdf, {"activities": page["activities"]})
        else:
            renderers[page["type"]](pdf, page["activity"])
        draw_footer(pdf)
        pdf.showPage()


def build_pdf(data: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output_path), pagesize=letter, pageCompression=1)
    pdf.setTitle(data["title"] + " | Learning Made Simple")
    pdf.setAuthor("Learning Made Simple")
    if data.get("template") == "counting-pack":
        build_counting_pack(pdf, data)
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
    output_dir = (generator_dir.parent / "worksheets" / "preschool" / "math" / "counting"
                  if data.get("template") == "counting-pack" else generator_dir / "output")
    build_pdf(data, output_dir / data["filename"])


if __name__ == "__main__":
    main()
