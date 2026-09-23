#!/usr/bin/env python3
"""Feelings & Me (Prototype) — Preschool Communication & Life Skills.

Page 1 (Find the Feeling): recognition — adult names a feeling, the child
  circles the matching face from 3 big faces. One row per feeling:
  happy, sad, angry, scared, surprised.
Page 2 (Name the Feeling): labeling — one large expressive face per row
  with 2 simple feeling-word choices; the adult reads the choices aloud.

Prototype only: these 2 pages for review. Do not extend without approval.
"""

import os

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

PAGE_WIDTH, PAGE_HEIGHT = 612, 792
TITLE = "Feelings & Me"
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "feelings")

TEAL = HexColor("#0f766e")
TEAL_DARK = HexColor("#115e59")
INK = HexColor("#1f2937")
LIGHT_BG = HexColor("#f0fdfa")
RULE = HexColor("#99d5cf")
white = HexColor("#ffffff")

EMOTIONS = ["happy", "sad", "angry", "scared", "surprised"]


def draw_picture(pdf, stem, cx, cy, size):
    img = ImageReader(os.path.join(ASSETS, stem + ".png"))
    iw, ih = img.getSize()
    scale = size / max(iw, ih)
    w, h = iw * scale, ih * scale
    pdf.drawImage(img, cx - w / 2, cy - h / 2, w, h,
                  preserveAspectRatio=True, mask="auto")


def draw_header(pdf, title, subtitle):
    pdf.setFillColor(TEAL)
    pdf.rect(0, 742, PAGE_WIDTH, 50, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(56, 770, "LEARNING")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(56, 758, "MADE SIMPLE")
    pdf.setStrokeColor(white)
    pdf.setLineWidth(1)
    pdf.line(200, 750, 200, 784)
    pdf.setFont("Helvetica-Bold", 19)
    pdf.drawString(216, 768, title)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(216, 753, subtitle)
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1.5)
    pdf.line(36, 728, 576, 728)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(36, 702, "Name:")
    pdf.setStrokeColor(RULE)
    pdf.setLineWidth(1)
    pdf.line(82, 700, 360, 700)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(420, 702, "Date:")
    pdf.line(462, 700, 576, 700)


def draw_footer(pdf):
    pdf.setFillColor(LIGHT_BG)
    pdf.rect(0, 0, PAGE_WIDTH, 44, fill=1, stroke=0)
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(56, 20, "Learning Made Simple")
    pdf.setFillColor(RULE)
    pdf.rect(200, 12, 2, 20, fill=1, stroke=0)
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(360, 20, "Made with love for little learners.")
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(576, 20, "\u00a9 2026 Learning Made Simple")


def draw_instruction(pdf, text, y=648):
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, y, text)


# Page 1: Find the Feeling — one row per emotion, 3 faces per row.
PAGE1_ROWS = [
    ("happy", ["f-happy", "f-sad", "f-angry"]),
    ("sad", ["f-sad", "f-scared", "f-happy"]),
    ("angry", ["f-angry", "f-surprised", "f-sad"]),
    ("scared", ["f-scared", "f-happy", "f-surprised"]),
    ("surprised", ["f-surprised", "f-angry", "f-scared"]),
]
PAGE1_YS = [563, 459, 355, 251, 147]


def draw_page1(pdf):
    draw_header(pdf, f"{TITLE}: Find the Feeling",
                "Preschool Communication & Life Skills")
    draw_instruction(pdf, "Find the feeling. Circle the face.")
    for (emotion, faces), cy in zip(PAGE1_ROWS, PAGE1_YS):
        x, w, h = 36, 540, 90
        y = cy - h / 2
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(x, y, w, h, 14, fill=1, stroke=1)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(56, cy - 6, f"Find the {emotion} face.")
        for stem, cx in zip(faces, (310, 420, 530)):
            draw_picture(pdf, stem, cx, cy, 78)
    draw_footer(pdf)
    pdf.showPage()


# Page 2: Name the Feeling — one large face + 2 word choices per row.
PAGE2_ROWS = [
    ("f-happy", ["happy", "sad"]),
    ("f-sad", ["sad", "angry"]),
    ("f-angry", ["angry", "happy"]),
    ("f-scared", ["scared", "surprised"]),
    ("f-surprised", ["surprised", "scared"]),
]
PAGE2_YS = [563, 459, 355, 251, 147]


def draw_word_choice(pdf, cx, cy, word):
    w, h = 140, 46
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(2.5)
    pdf.roundRect(cx - w / 2, cy - h / 2, w, h, 12, fill=1, stroke=1)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(cx, cy - 6, word)


def draw_page2(pdf):
    draw_header(pdf, f"{TITLE}: Name the Feeling",
                "Preschool Communication & Life Skills")
    draw_instruction(pdf, "How does the face feel? Circle the word.")
    for (stem, words), cy in zip(PAGE2_ROWS, PAGE2_YS):
        x, w, h = 36, 540, 90
        y = cy - h / 2
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(2.5)
        pdf.roundRect(x, y, w, h, 14, fill=1, stroke=1)
        draw_picture(pdf, stem, 130, cy, 80)
        for word, cx in zip(words, (340, 485)):
            draw_word_choice(pdf, cx, cy, word)
    draw_footer(pdf)
    pdf.showPage()


def main():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "communication", "feelings",
        "feelings-me-prototype.pdf",
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} (Prototype) | Learning Made Simple")
    draw_page1(pdf)
    draw_page2(pdf)
    pdf.save()
    print(f"wrote {out} (2 pages)")


if __name__ == "__main__":
    main()
