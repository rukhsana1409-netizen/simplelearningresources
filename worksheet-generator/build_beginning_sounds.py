"""Build the 5-page Beginning Sounds pack (final).

Preschool Reading & Language:
- Pages 1, 3, 5 (What Sound?): 5 large pictures of familiar
  objects/animals; beside each picture are 2 large letter choices.
  The child circles the letter the word begins with.
- Pages 2, 4 (Match the Sound): 4 large target letters and 4 pictures
  in mixed order (no picture names). The child draws a line from each
  picture to its beginning letter.

All pictures are different across the pack, with clear, unambiguous
beginning sounds and familiar preschool vocabulary.
"""

import os
import sys

from reportlab.lib.colors import white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_worksheet import (
    BLUE,
    CORAL,
    GOLD,
    GREEN,
    INK,
    MUTED,
    ORANGE,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    PURPLE,
    TEAL,
    TEAL_DARK,
    draw_footer,
    draw_header,
)

TITLE = "Beginning Sounds"
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "assets", "letters")
_CONVERT_DIR = os.path.join("/tmp", "beginning_sounds_jpg")
_CONVERTED = {}


def asset_path(stem):
    """Build-time conversion: WebP -> print-sized JPEG for embedding."""
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


def draw_picture(pdf, stem, word, cx, cy, box, label_size=12, show_label=True):
    img = ImageReader(asset_path(stem))
    pdf.drawImage(img, cx - box / 2, cy - box / 2, width=box, height=box,
                  preserveAspectRatio=True, anchor="c", mask="auto")
    if show_label:
        pdf.setFillColor(MUTED)
        pdf.setFont("Helvetica-Bold", label_size)
        pdf.drawCentredString(cx, cy - box / 2 - 16, word)


def draw_letter_badge(pdf, cx, cy, letter, bg, r=34, font_size=44):
    pdf.setFillColor(bg)
    pdf.circle(cx, cy, r, fill=1, stroke=0)
    pdf.setFillColor(white)
    pdf.setFillAlpha(0.18)
    pdf.circle(cx - r * 0.28, cy + r * 0.33, r * 0.30, fill=1, stroke=0)
    pdf.setFillAlpha(1)
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", font_size)
    pdf.drawCentredString(cx, cy - font_size * 0.357, letter)


# "What Sound?" pages: (asset stem, word, [left letter, right letter],
# [left color, right color]). Correct side varies within each page.
WHAT_SOUND_PAGES = [
    [  # Page 1 (approved)
        ("d-dog", "dog", ["D", "P"], [CORAL, TEAL]),
        ("s-sun", "sun", ["T", "S"], [BLUE, GOLD]),
        ("c-cat", "cat", ["R", "C"], [PURPLE, GREEN]),
        ("h-hat", "hat", ["H", "K"], [ORANGE, TEAL]),
        ("b-banana", "banana", ["D", "B"], [PURPLE, CORAL]),
    ],
    [  # Page 3
        ("f-fish", "fish", ["F", "J"], [TEAL, CORAL]),
        ("l-lion", "lion", ["N", "L"], [BLUE, GOLD]),
        ("e-egg", "egg", ["I", "E"], [GREEN, PURPLE]),
        ("c-cake", "cake", ["C", "G"], [ORANGE, TEAL]),
        ("k-key", "key", ["T", "K"], [PURPLE, GOLD]),
    ],
    [  # Page 5
        ("r-rabbit", "rabbit", ["B", "R"], [TEAL, CORAL]),
        ("g-guitar", "guitar", ["G", "D"], [GOLD, PURPLE]),
        ("p-penguin", "penguin", ["M", "P"], [BLUE, GREEN]),
        ("o-orange", "orange", ["O", "A"], [ORANGE, TEAL]),
        ("z-zebra", "zebra", ["S", "Z"], [PURPLE, BLUE]),
    ],
]
WHAT_SOUND_YS = [518, 412, 306, 200, 94]
PIC_CX = 135
CHOICE_CXS = [350, 470]

# "Match the Sound" pages: target letters (left) and pictures in mixed
# order (right); no picture names.
MATCH_PAGES = [
    {  # Page 2 (approved)
        "letters": [("B", CORAL), ("P", TEAL), ("T", GOLD), ("M", PURPLE)],
        "pictures": [("m-moon", "moon"), ("b-bear", "bear"),
                     ("p-pizza", "pizza"), ("t-train", "train")],
    },
    {  # Page 4
        "letters": [("D", GREEN), ("F", BLUE), ("S", ORANGE), ("C", TEAL)],
        "pictures": [("f-frog", "frog"), ("s-snake", "snake"),
                     ("c-cloud", "cloud"), ("d-drum", "drum")],
    },
]
MATCH_YS = [498, 388, 278, 168]
LETTER_CX = 170
PICTURE_CX = 445


def draw_what_sound_page(pdf, rows):
    draw_header(pdf, {"title": f"{TITLE}: What Sound?",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "What sound does it start with? Circle the letter.",
    )
    for (stem, word, letters, colors), cy in zip(rows, WHAT_SOUND_YS):
        draw_picture(pdf, stem, word, PIC_CX, cy + 8, 80)
        for cx, letter, color in zip(CHOICE_CXS, letters, colors):
            draw_letter_badge(pdf, cx, cy, letter, color)
    draw_footer(pdf)
    pdf.showPage()


def draw_match_page(pdf, spec):
    draw_header(pdf, {"title": f"{TITLE}: Match the Sound",
                      "subtitle": "Preschool Reading & Language"})
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 596,
        "Draw a line from each picture to its first sound.",
    )
    for (letter, color), cy in zip(spec["letters"], MATCH_YS):
        draw_letter_badge(pdf, LETTER_CX, cy, letter, color, r=40, font_size=52)
    for (stem, word), cy in zip(spec["pictures"], MATCH_YS):
        draw_picture(pdf, stem, word, PICTURE_CX, cy, 84, show_label=False)
    draw_footer(pdf)
    pdf.showPage()


def build():
    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "beginning-sounds.pdf",
    )
    pdf = canvas.Canvas(out, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle(f"{TITLE} | Learning Made Simple")
    pdf.setAuthor("Learning Made Simple")
    draw_what_sound_page(pdf, WHAT_SOUND_PAGES[0])  # page 1
    draw_match_page(pdf, MATCH_PAGES[0])             # page 2
    draw_what_sound_page(pdf, WHAT_SOUND_PAGES[1])  # page 3
    draw_match_page(pdf, MATCH_PAGES[1])             # page 4
    draw_what_sound_page(pdf, WHAT_SOUND_PAGES[2])  # page 5
    pdf.save()
    print(f"wrote {out} (5 pages)")


if __name__ == "__main__":
    build()
