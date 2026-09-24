"""Build I Can Tell You (Expressing Needs & Ideas) — Page 1 prototype.

Page 1 (What Do You Need?): four spacious everyday situations. Each row
shows a child with a clear need plus two picture choices; the child
circles what the person needs. Tests understanding and communication,
not inference or reading ability.
"""

from __future__ import annotations

import os

from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = 612, 792
TITLE = "I Can Tell You"

TEAL = HexColor("#007C70")
TEAL_DARK = HexColor("#005F57")
GOLD = HexColor("#F4B63E")
INK = HexColor("#202A33")
BORDER = HexColor("#B9D7D2")
MARGIN = 40

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "i-can-tell-you")


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
    prefix, focus = title.split(": ", 1)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(title_x, PAGE_HEIGHT - 67, prefix + ":")
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(title_x, PAGE_HEIGHT - 98, focus)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11.5)
    pdf.drawString(title_x, PAGE_HEIGHT - 116, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    pdf.line(MARGIN, PAGE_HEIGHT - 131, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 131)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(MARGIN, PAGE_HEIGHT - 160, "Name:")
    pdf.setStrokeColor(BORDER)
    pdf.setLineWidth(0.9)
    pdf.line(MARGIN + 37, PAGE_HEIGHT - 163, 315, PAGE_HEIGHT - 163)
    pdf.setFillColor(INK)
    pdf.drawString(430, PAGE_HEIGHT - 160, "Date:")
    pdf.setStrokeColor(BORDER)
    pdf.line(463, PAGE_HEIGHT - 163, PAGE_WIDTH - MARGIN, PAGE_HEIGHT - 163)


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF4F3"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#0E7C7B"))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(56, 19, "Learning Made Simple")
    pdf.setStrokeColor(HexColor("#9FD3D1"))
    pdf.setLineWidth(1.5)
    pdf.line(200, 10, 200, 34)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(320, 19, "Made with love for little learners.")
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(556, 19, "\u00a9 2026 Learning Made Simple")


def draw_picture(pdf, stem, cx, cy, size):
    path = os.path.join(ASSETS, stem + ".png")
    pdf.drawImage(path, cx - size / 2, cy - size / 2, size, size,
                  preserveAspectRatio=True, mask="auto")


# Page 1 (What Do You Need?): label, situation picture, then the two
# choices (correct answer position varies row to row).
PAGE1_ROWS = [
    ("She is thirsty.", "ity-thirsty-girl", ["ity-water", "ity-sandwich"]),
    ("He is hungry.", "ity-hungry-boy", ["ity-apple", "ity-water"]),
    ("She is cold.", "ity-cold-girl", ["ity-jacket", "ity-sun-hat"]),
    ("He is tired.", "ity-tired-boy", ["ity-bed", "ity-chair"]),
]
PAGE1_YS = [500, 374, 248, 122]


def draw_page1(pdf):
    draw_header(pdf, f"{TITLE}: What Do You Need?",
                "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 588, "Circle what they need.")
    for (label, situation, choices), cy in zip(PAGE1_ROWS, PAGE1_YS):
        x, w, h = 36, 540, 112
        y = cy - h / 2
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawString(52, cy + 5, label)
        draw_picture(pdf, situation, 255, cy, 90)
        draw_picture(pdf, choices[0], 425, cy, 80)
        draw_picture(pdf, choices[1], 525, cy, 80)
    draw_footer(pdf)
    pdf.showPage()


# Page 2 (What Can I Say?): a child with a clear need, followed by two
# short communication choices with supportive pictures. The child circles
# what they could say. An adult reads the words aloud; the activity does
# not depend on independent reading. Correct-answer position varies.
PAGE2_ROWS = [
    ("She is thirsty.", "ity-thirsty-girl",
     [("Water, please.", "ity-water"), ("Ball, please.", "ity-ball")]),
    ("He needs help.", "ity-help-boy",
     [("Bye!", "ity-waving-hand"),
      ("Help me, please.", "ity-helping-hand")]),
    ("She wants a turn.", "ity-turn-girl",
     [("My turn, please.", "ity-toy-car"), ("Good night.", "ity-moon")]),
    ("He needs a break.", "ity-break-boy",
     [("More, please.", "ity-blocks"), ("Break, please.", "ity-chair")]),
]
PAGE2_YS = [500, 374, 248, 122]


def draw_page2(pdf):
    draw_header(pdf, f"{TITLE}: What Can I Say?",
                "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 588, "Circle what they could say.")
    for (label, situation, choices), cy in zip(PAGE2_ROWS, PAGE2_YS):
        x, w, h = 36, 540, 112
        y = cy - h / 2
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawString(52, cy + 5, label)
        draw_picture(pdf, situation, 255, cy, 90)
        for (phrase, stem), cx in zip(choices, (420, 525)):
            draw_picture(pdf, stem, cx, cy + 10, 70)
            pdf.setFillColor(INK)
            pdf.setFont("Helvetica-Bold", 11.5)
            pdf.drawCentredString(cx, cy - 42, phrase)
    draw_footer(pdf)
    pdf.showPage()


# Page 3 (Tell What You Want): the child chooses between two things
# they might want and completes the repeated phrase "I want ___, please."
# Either option is correct — this is about expressing a personal choice,
# not a right/wrong matching activity. The blank space lets the child
# point, say, draw, or have an adult write the choice.
PAGE3_ROWS = [
    ("ity-apple", "ity-banana"),
    ("ity-ball", "ity-blocks"),
    ("ity-book", "ity-crayons"),
    ("ity-teddy-bear", "ity-toy-car"),
]
PAGE3_YS = [500, 374, 248, 122]


def draw_page3(pdf):
    draw_header(pdf, f"{TITLE}: Tell What You Want",
                "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 588, "Point and say what you want.")
    for (stem1, stem2), cy in zip(PAGE3_ROWS, PAGE3_YS):
        x, w, h = 36, 540, 112
        y = cy - h / 2
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 16)
        tx = 52
        pdf.drawString(tx, cy + 6, "I want")
        line_x1 = tx + 64
        line_x2 = line_x1 + 108
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.2)
        pdf.line(line_x1, cy + 2, line_x2, cy + 2)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(line_x2 + 8, cy + 6, "please.")
        draw_picture(pdf, stem1, 400, cy, 88)
        draw_picture(pdf, stem2, 520, cy, 88)
    draw_footer(pdf)
    pdf.showPage()


# Page 4 (I Can Say No): the child communicates that they do not want
# something, using simple functional phrases ("No, thank you.",
# "I don't want it."). The focus is appropriate self-advocacy and
# communicating "no" — not identifying emotions or choosing a
# right/wrong object. Text is minimal: the situation picture tells the
# story and the phrase is the communication.
PAGE4_ROWS = [
    ("ity-no-food", "No, thank you."),
    ("ity-no-toy", "I don't want it."),
    ("ity-no-play", "No, thank you."),
    ("ity-no-more", "I don't want it."),
]
PAGE4_YS = [500, 374, 248, 122]


def draw_page4(pdf):
    draw_header(pdf, f"{TITLE}: I Can Say No",
                "Preschool Communication & Life Skills")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 588,
                          "Practice saying no in a kind way.")
    for (situation, phrase), cy in zip(PAGE4_ROWS, PAGE4_YS):
        x, w, h = 36, 540, 112
        y = cy - h / 2
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(x, y, w, h, 16, fill=1, stroke=1)
        draw_picture(pdf, situation, 200, cy, 95)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawCentredString(445, cy - 7, phrase)
    draw_footer(pdf)
    pdf.showPage()


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "communication",
        "i-can-tell-you", "i-can-tell-you-prototype.pdf",
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    draw_page2(pdf)
    draw_page3(pdf)
    draw_page4(pdf)
    pdf.save()
    print(f"wrote {out} (4 pages)")


if __name__ == "__main__":
    main()
