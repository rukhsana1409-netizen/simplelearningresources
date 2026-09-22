"""Build Learn My Letters A-Z (26 pages, one per letter).

Reuses the Learning Made Simple branding (header, footer, palette) from
generate_worksheet.py. Embeds original illustrations from assets/letters/.
Each page: huge uppercase+lowercase pair, three labeled beginning-sound
pictures, and a themed "find the letter" hunt practicing BOTH cases.
No tracing (separate resource).
"""

from __future__ import annotations

import math
import os
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_worksheet import (  # noqa: E402
    INK,
    MARGIN,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    PALE_TEAL,
    TEAL,
    TEAL_DARK,
    draw_footer,
    draw_header,
)

LIGHT_GOLD = HexColor("#FDF3DC")
LIGHT_CORAL = HexColor("#FCEDEA")
LIGHT_BLUE = HexColor("#E9F3FA")
LIGHT_PURPLE = HexColor("#F0EAF7")
LIGHT_PINK = HexColor("#F9DDE3")
LEAF = HexColor("#A9D6A5")
RIND = HexColor("#7FBF7F")
MELON = HexColor("#F19494")
SEED = HexColor("#5B4A3F")
TAN = HexColor("#D9A066")
DOME_GOLD = HexColor("#E8B04B")
ORANGE_FILL = HexColor("#F6B26B")
ICE = HexColor("#EAF6FD")

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "letters")

CIRCLE_FILLS = [PALE_TEAL, LIGHT_GOLD, LIGHT_BLUE, LIGHT_CORAL, LIGHT_PURPLE, white]

# Build-time conversion: source illustrations are large WebP files; embedding
# them directly balloons the PDF (reportlab rasterizes them). Convert once per
# build to print-sized JPEGs (600px max side is plenty for ~1.5in print art).
_CONVERT_DIR = os.path.join("/tmp", "letters_assets_jpg")
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


def _hunt_letter(pdf: canvas.Canvas, cx: float, cy: float, letter: str,
                 size: float = 32, dy: float = -11) -> None:
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawCentredString(cx, cy + dy, letter)


def _poly(pdf: canvas.Canvas, points: list, fill, stroke=None, width: float = 2) -> None:
    path = pdf.beginPath()
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    path.close()
    if stroke:
        pdf.setStrokeColor(stroke)
        pdf.setLineWidth(width)
    pdf.setFillColor(fill)
    pdf.drawPath(path, fill=1, stroke=1 if stroke else 0)


# ---- Hunt themes: each draws one container centered at (cx, cy) with the letter.

def hunt_circle(pdf, cx, cy, letter, i):
    pdf.setFillColor(CIRCLE_FILLS[i % len(CIRCLE_FILLS)])
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.circle(cx, cy, 38, fill=1, stroke=1)
    _hunt_letter(pdf, cx, cy, letter)


def hunt_bubble(pdf, cx, cy, letter, i):
    pdf.setFillColor([LIGHT_BLUE, white, PALE_TEAL][i % 3])
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.circle(cx, cy, 36, fill=1, stroke=1)
    pdf.setFillColor(white)
    pdf.circle(cx - 13, cy + 13, 8, fill=1, stroke=0)
    _hunt_letter(pdf, cx, cy, letter)


def hunt_block(pdf, cx, cy, letter, i):
    pdf.setFillColor([LIGHT_GOLD, LIGHT_CORAL, LIGHT_BLUE][i % 3])
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.roundRect(cx - 36, cy - 36, 72, 72, 12, fill=1, stroke=1)
    _hunt_letter(pdf, cx, cy, letter, size=34)


def hunt_flower(pdf, cx, cy, letter, i):
    petal_fill = [LIGHT_PINK, LIGHT_CORAL, LIGHT_PURPLE][i % 3]
    pdf.setFillColor(petal_fill)
    for k in range(6):
        angle = math.radians(90 + k * 60)
        pdf.circle(cx + 27 * math.cos(angle), cy + 27 * math.sin(angle),
                   16, fill=1, stroke=0)
    pdf.setFillColor(LIGHT_GOLD)
    pdf.circle(cx, cy, 21, fill=1, stroke=0)
    _hunt_letter(pdf, cx, cy, letter, size=28)


def hunt_cloud(pdf, cx, cy, letter, i):
    pdf.setFillColor([LIGHT_BLUE, PALE_TEAL, LIGHT_PURPLE][i % 3])
    pdf.ellipse(cx - 42, cy - 22, cx + 42, cy + 22, fill=1, stroke=0)
    pdf.circle(cx - 24, cy + 8, 18, fill=1, stroke=0)
    pdf.circle(cx + 24, cy + 8, 18, fill=1, stroke=0)
    pdf.circle(cx, cy + 16, 24, fill=1, stroke=0)
    _hunt_letter(pdf, cx, cy, letter, size=30, dy=-9)


def hunt_honeycomb(pdf, cx, cy, letter, i):
    points = [(cx + 40 * math.cos(math.radians(90 + k * 60)),
               cy + 40 * math.sin(math.radians(90 + k * 60))) for k in range(6)]
    _poly(pdf, points, LIGHT_GOLD, TEAL, 2)
    _hunt_letter(pdf, cx, cy, letter, size=32)


def hunt_icecube(pdf, cx, cy, letter, i):
    pdf.setFillColor(ICE)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.roundRect(cx - 34, cy - 34, 68, 68, 10, fill=1, stroke=1)
    pdf.setStrokeColor(white)
    pdf.setLineWidth(5)
    pdf.line(cx - 20, cy + 16, cx - 2, cy - 14)
    _hunt_letter(pdf, cx, cy, letter, size=32)


def hunt_jellybean(pdf, cx, cy, letter, i):
    pdf.setFillColor([LIGHT_PINK, LIGHT_PURPLE, LIGHT_CORAL][i % 3])
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.ellipse(cx - 36, cy - 27, cx + 36, cy + 27, fill=1, stroke=1)
    _hunt_letter(pdf, cx, cy, letter, size=32)


def hunt_kite(pdf, cx, cy, letter, i):
    points = [(cx, cy + 34), (cx + 30, cy), (cx, cy - 34), (cx - 30, cy)]
    _poly(pdf, points, [LIGHT_BLUE, LIGHT_CORAL, LIGHT_GOLD][i % 3], TEAL, 2)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(cx, cy - 34, cx, cy - 46)
    _hunt_letter(pdf, cx, cy, letter, size=30, dy=-10)


def hunt_lilypad(pdf, cx, cy, letter, i):
    pdf.setFillColor(LEAF)
    pdf.circle(cx, cy, 36, fill=1, stroke=0)
    pdf.setFillColor(white)
    notch = pdf.beginPath()
    notch.moveTo(cx, cy)
    notch.lineTo(cx + 38, cy - 10)
    notch.lineTo(cx + 38, cy + 10)
    notch.close()
    pdf.drawPath(notch, fill=1, stroke=0)
    _hunt_letter(pdf, cx - 4, cy, letter, size=32)


def hunt_muffin(pdf, cx, cy, letter, i):
    base = [(cx - 26, cy - 34), (cx + 26, cy - 34), (cx + 18, cy - 6), (cx - 18, cy - 6)]
    _poly(pdf, base, TAN)
    dome = pdf.beginPath()
    dome.moveTo(cx + 26, cy - 6)
    dome.arc(cx - 26, cy - 32, cx + 26, cy + 20, 0, 180)
    dome.close()
    pdf.setFillColor(DOME_GOLD)
    pdf.drawPath(dome, fill=1, stroke=0)
    _hunt_letter(pdf, cx, cy + 2, letter, size=28, dy=-10)


def hunt_star(pdf, cx, cy, letter, i):
    points = []
    for k in range(10):
        radius = 38 if k % 2 == 0 else 16
        angle = math.radians(90 + k * 36)
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    _poly(pdf, points, LIGHT_GOLD, TEAL, 1.8)
    _hunt_letter(pdf, cx, cy, letter, size=30, dy=-10)


def hunt_orange(pdf, cx, cy, letter, i):
    pdf.setFillColor(ORANGE_FILL)
    pdf.circle(cx, cy - 2, 34, fill=1, stroke=0)
    pdf.setFillColor(LEAF)
    pdf.ellipse(cx + 4, cy + 28, cx + 24, cy + 38, fill=1, stroke=0)
    _hunt_letter(pdf, cx, cy - 2, letter, size=32)


def hunt_planet(pdf, cx, cy, letter, i):
    pdf.setFillColor([LIGHT_PURPLE, LIGHT_BLUE, LIGHT_CORAL][i % 3])
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.circle(cx, cy, 30, fill=1, stroke=1)
    pdf.saveState()
    pdf.translate(cx, cy)
    pdf.rotate(18)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2.5)
    pdf.ellipse(-46, -14, 46, 14, fill=0, stroke=1)
    pdf.restoreState()
    _hunt_letter(pdf, cx, cy, letter, size=30)


def hunt_quilt(pdf, cx, cy, letter, i):
    pdf.setFillColor([LIGHT_CORAL, LIGHT_GOLD, LIGHT_PURPLE][i % 3])
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.roundRect(cx - 36, cy - 36, 72, 72, 10, fill=1, stroke=1)
    pdf.setDash(4, 3)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.5)
    pdf.roundRect(cx - 28, cy - 28, 56, 56, 8, fill=0, stroke=1)
    pdf.setDash()
    _hunt_letter(pdf, cx, cy, letter, size=32)


def hunt_raindrop(pdf, cx, cy, letter, i):
    pdf.setFillColor(LIGHT_BLUE)
    tri = [(cx, cy + 38), (cx - 24, cy - 6), (cx + 24, cy - 6)]
    _poly(pdf, tri, LIGHT_BLUE)
    pdf.circle(cx, cy - 8, 24, fill=1, stroke=0)
    _hunt_letter(pdf, cx, cy - 4, letter, size=30, dy=-10)


def hunt_shell(pdf, cx, cy, letter, i):
    pdf.setFillColor([LIGHT_CORAL, LIGHT_PINK, LIGHT_GOLD][i % 3])
    pdf.circle(cx, cy, 34, fill=1, stroke=0)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    for deg in (25, 62, 90, 118, 155):
        angle = math.radians(deg)
        pdf.line(cx, cy - 28,
                 cx + 32 * math.cos(angle), cy + 32 * math.sin(angle))
    _hunt_letter(pdf, cx, cy + 4, letter, size=30, dy=-10)


def hunt_tent(pdf, cx, cy, letter, i):
    tri = [(cx - 36, cy - 34), (cx + 36, cy - 34), (cx, cy + 38)]
    _poly(pdf, tri, [LIGHT_CORAL, LIGHT_BLUE, LIGHT_GOLD][i % 3], TEAL, 2)
    door = [(cx - 10, cy - 34), (cx + 10, cy - 34), (cx, cy - 12)]
    _poly(pdf, door, TEAL_DARK)
    _hunt_letter(pdf, cx, cy + 10, letter, size=28, dy=-10)


def hunt_umbrella(pdf, cx, cy, letter, i):
    dome = pdf.beginPath()
    dome.moveTo(cx + 34, cy)
    dome.arc(cx - 34, cy - 34, cx + 34, cy + 34, 0, 180)
    dome.close()
    pdf.setFillColor([LIGHT_PURPLE, LIGHT_BLUE, LIGHT_PINK][i % 3])
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.drawPath(dome, fill=1, stroke=1)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2.5)
    pdf.line(cx, cy, cx, cy - 26)
    pdf.setFillColor(TEAL)
    pdf.circle(cx, cy - 26, 3, fill=1, stroke=0)
    _hunt_letter(pdf, cx, cy + 8, letter, size=28, dy=-10)


def hunt_heart(pdf, cx, cy, letter, i):
    pdf.setFillColor([LIGHT_PINK, LIGHT_CORAL][i % 2])
    pdf.circle(cx - 14, cy + 8, 14, fill=1, stroke=0)
    pdf.circle(cx + 14, cy + 8, 14, fill=1, stroke=0)
    _poly(pdf, [(cx - 26, cy + 4), (cx + 26, cy + 4), (cx, cy - 32)],
          [LIGHT_PINK, LIGHT_CORAL][i % 2])
    _hunt_letter(pdf, cx, cy + 2, letter, size=28, dy=-10)


def hunt_watermelon(pdf, cx, cy, letter, i):
    outer = pdf.beginPath()
    outer.moveTo(cx + 36, cy - 4)
    outer.arc(cx - 36, cy - 40, cx + 36, cy + 32, 0, 180)
    outer.close()
    pdf.setFillColor(RIND)
    pdf.drawPath(outer, fill=1, stroke=0)
    inner = pdf.beginPath()
    inner.moveTo(cx + 28, cy - 4)
    inner.arc(cx - 28, cy - 32, cx + 28, cy + 24, 0, 180)
    inner.close()
    pdf.setFillColor(MELON)
    pdf.drawPath(inner, fill=1, stroke=0)
    pdf.setFillColor(SEED)
    for sx, sy in ((-14, 2), (14, 2), (-7, 14), (7, 14)):
        pdf.ellipse(cx + sx - 2.5, cy + sy - 3.5, cx + sx + 2.5, cy + sy + 3.5,
                    fill=1, stroke=0)
    _hunt_letter(pdf, cx, cy + 6, letter, size=26, dy=-9)


def hunt_xylophone(pdf, cx, cy, letter, i):
    pdf.setFillColor([LIGHT_CORAL, LIGHT_GOLD, LIGHT_BLUE, LIGHT_PURPLE][i % 4])
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.roundRect(cx - 38, cy - 16, 76, 32, 10, fill=1, stroke=1)
    _hunt_letter(pdf, cx, cy, letter, size=30)


def hunt_yoyo(pdf, cx, cy, letter, i):
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(2)
    pdf.line(cx, cy + 32, cx, cy + 44)
    pdf.setFillColor([LIGHT_BLUE, LIGHT_CORAL, LIGHT_GOLD][i % 3])
    pdf.setStrokeColor(TEAL)
    pdf.circle(cx, cy, 32, fill=1, stroke=1)
    pdf.setFillColor(white)
    pdf.circle(cx, cy, 8, fill=1, stroke=0)
    _hunt_letter(pdf, cx, cy, letter, size=30)


def hunt_lightning(pdf, cx, cy, letter, i):
    points = [(cx + 8, cy + 38), (cx - 14, cy + 6), (cx - 4, cy + 6),
              (cx - 8, cy - 38), (cx + 14, cy - 6), (cx + 4, cy - 6)]
    _poly(pdf, points, LIGHT_GOLD, TEAL, 1.8)
    _hunt_letter(pdf, cx, cy, letter, size=30, dy=-10)


HUNT_THEMES = {
    "circle": hunt_circle,
    "bubble": hunt_bubble,
    "block": hunt_block,
    "flower": hunt_flower,
    "cloud": hunt_cloud,
    "honeycomb": hunt_honeycomb,
    "icecube": hunt_icecube,
    "jellybean": hunt_jellybean,
    "kite": hunt_kite,
    "lilypad": hunt_lilypad,
    "muffin": hunt_muffin,
    "star": hunt_star,
    "orange": hunt_orange,
    "planet": hunt_planet,
    "quilt": hunt_quilt,
    "raindrop": hunt_raindrop,
    "shell": hunt_shell,
    "tent": hunt_tent,
    "umbrella": hunt_umbrella,
    "heart": hunt_heart,
    "watermelon": hunt_watermelon,
    "xylophone": hunt_xylophone,
    "yoyo": hunt_yoyo,
    "lightning": hunt_lightning,
}


LETTERS = [
    {"upper": "A", "lower": "a",
     "words": [("ant", "Ant"), ("alligator", "Alligator"), ("astronaut", "Astronaut")],
     "theme": "circle", "hunt": ["A", "b", "C", "a", "B", "A", "c", "a"],
     "verb": "Put a cross on each one."},
    {"upper": "B", "lower": "b",
     "words": [("banana", "Banana"), ("bear", "Bear"), ("book", "Book")],
     "theme": "circle", "hunt": ["B", "a", "C", "b", "A", "B", "c", "b"],
     "verb": "Circle each one."},
    {"upper": "C", "lower": "c",
     "words": [("cat", "Cat"), ("cake", "Cake"), ("cloud", "Cloud")],
     "theme": "circle", "hunt": ["C", "a", "B", "c", "A", "c", "C", "b"],
     "verb": "Draw a box around each one."},
    {"upper": "D", "lower": "d",
     "words": [("dog", "Dog"), ("duck", "Duck"), ("drum", "Drum")],
     "theme": "bubble", "hunt": ["D", "e", "F", "d", "E", "D", "f", "d"],
     "verb": "Put a cross on each one."},
    {"upper": "E", "lower": "e",
     "words": [("elephant", "Elephant"), ("egg", "Egg"), ("elf", "Elf")],
     "theme": "block", "hunt": ["E", "d", "G", "e", "F", "E", "g", "e"],
     "verb": "Circle each one."},
    {"upper": "F", "lower": "f",
     "words": [("fish", "Fish"), ("frog", "Frog"), ("flower", "Flower")],
     "theme": "flower", "hunt": ["F", "e", "H", "f", "G", "F", "h", "f"],
     "verb": "Draw a box around each one."},
    {"upper": "G", "lower": "g",
     "words": [("goat", "Goat"), ("grapes", "Grapes"), ("guitar", "Guitar")],
     "theme": "cloud", "hunt": ["G", "f", "H", "g", "h", "J", "G", "g"],
     "verb": "Color each one."},
    {"upper": "H", "lower": "h",
     "words": [("horse", "Horse"), ("hat", "Hat"), ("house", "House")],
     "theme": "honeycomb", "hunt": ["H", "g", "J", "h", "G", "H", "j", "h"],
     "verb": "Put a cross on each one."},
    {"upper": "I", "lower": "i",
     "words": [("ice-cream", "Ice Cream"), ("iguana", "Iguana"), ("insect", "Insect")],
     "theme": "icecube", "hunt": ["I", "h", "K", "i", "J", "I", "k", "i"],
     "verb": "Circle each one."},
    {"upper": "J", "lower": "j",
     "words": [("jellyfish", "Jellyfish"), ("jar", "Jar"), ("jacket", "Jacket")],
     "theme": "jellybean", "hunt": ["J", "i", "L", "j", "K", "J", "l", "j"],
     "verb": "Draw a box around each one."},
    {"upper": "K", "lower": "k",
     "words": [("kangaroo", "Kangaroo"), ("key", "Key"), ("kite", "Kite")],
     "theme": "kite", "hunt": ["K", "j", "M", "k", "L", "K", "m", "k"],
     "verb": "Color each one."},
    {"upper": "L", "lower": "l",
     "words": [("lion", "Lion"), ("lemon", "Lemon"), ("lamp", "Lamp")],
     "theme": "lilypad", "hunt": ["L", "k", "N", "l", "M", "L", "n", "l"],
     "verb": "Put a cross on each one."},
    {"upper": "M", "lower": "m",
     "words": [("monkey", "Monkey"), ("moon", "Moon"), ("muffin", "Muffin")],
     "theme": "muffin", "hunt": ["M", "l", "N", "m", "n", "P", "M", "m"],
     "verb": "Circle each one."},
    {"upper": "N", "lower": "n",
     "words": [("net", "Net"), ("nose", "Nose"), ("necklace", "Necklace")],
     "theme": "star", "hunt": ["N", "m", "P", "n", "M", "N", "p", "n"],
     "verb": "Draw a box around each one."},
    {"upper": "O", "lower": "o",
     "words": [("octopus", "Octopus"), ("orange", "Orange"), ("owl", "Owl")],
     "theme": "orange", "hunt": ["O", "n", "Q", "o", "P", "O", "q", "o"],
     "verb": "Color each one."},
    {"upper": "P", "lower": "p",
     "words": [("penguin", "Penguin"), ("pizza", "Pizza"), ("piano", "Piano")],
     "theme": "planet", "hunt": ["P", "o", "R", "p", "Q", "P", "r", "p"],
     "verb": "Put a cross on each one."},
    {"upper": "Q", "lower": "q",
     "words": [("queen", "Queen"), ("quilt", "Quilt"), ("quarter", "Quarter")],
     "theme": "quilt", "hunt": ["Q", "p", "R", "q", "r", "S", "Q", "q"],
     "verb": "Circle each one."},
    {"upper": "R", "lower": "r",
     "words": [("rabbit", "Rabbit"), ("rainbow", "Rainbow"), ("robot", "Robot")],
     "theme": "raindrop", "hunt": ["R", "q", "S", "r", "Q", "R", "s", "r"],
     "verb": "Draw a box around each one."},
    {"upper": "S", "lower": "s",
     "words": [("sun", "Sun"), ("snake", "Snake"), ("sandwich", "Sandwich")],
     "theme": "circle", "hunt": ["S", "r", "T", "s", "R", "S", "t", "s"],
     "verb": "Color each one."},
    {"upper": "T", "lower": "t",
     "words": [("tiger", "Tiger"), ("tree", "Tree"), ("train", "Train")],
     "theme": "jellybean", "hunt": ["T", "s", "V", "t", "S", "T", "v", "t"],
     "verb": "Put a cross on each one."},
    {"upper": "U", "lower": "u",
     "words": [("umbrella", "Umbrella"), ("unicorn", "Unicorn"), ("ukulele", "Ukulele")],
     "theme": "bubble", "hunt": ["U", "t", "V", "u", "T", "U", "v", "u"],
     "verb": "Circle each one."},
    {"upper": "V", "lower": "v",
     "words": [("violin", "Violin"), ("volcano", "Volcano"), ("vest", "Vest")],
     "theme": "circle", "hunt": ["V", "u", "W", "v", "U", "V", "w", "v"],
     "verb": "Draw a box around each one."},
    {"upper": "W", "lower": "w",
     "words": [("whale", "Whale"), ("watermelon", "Watermelon"), ("watch", "Watch")],
     "theme": "jellybean", "hunt": ["W", "v", "X", "w", "V", "W", "x", "w"],
     "verb": "Color each one."},
    {"upper": "X", "lower": "x",
     "words": [("xylophone", "Xylophone"), ("x-ray", "X-ray"), ("fox", "Fox")],
     "theme": "xylophone", "hunt": ["X", "w", "Y", "x", "W", "X", "y", "x"],
     "verb": "Put a cross on each one."},
    {"upper": "Y", "lower": "y",
     "words": [("yak", "Yak"), ("yo-yo", "Yo-Yo"), ("yarn", "Yarn")],
     "theme": "yoyo", "hunt": ["Y", "x", "Z", "y", "X", "Y", "z", "y"],
     "verb": "Circle each one."},
    {"upper": "Z", "lower": "z",
     "words": [("zebra", "Zebra"), ("zoo", "Zoo"), ("zipper", "Zipper")],
     "theme": "bubble", "hunt": ["Z", "y", "A", "z", "Y", "Z", "a", "z"],
     "verb": "Draw a box around each one."},
]


def draw_big_letters(pdf: canvas.Canvas, upper: str, lower: str) -> None:
    size = 96
    pdf.setFont("Helvetica-Bold", size)
    upper_text = upper + " "
    w_upper = stringWidth(upper_text, "Helvetica-Bold", size)
    w_lower = stringWidth(lower, "Helvetica-Bold", size)
    start_x = PAGE_WIDTH / 2 - (w_upper + w_lower) / 2
    baseline = 532
    pdf.setFillColor(TEAL_DARK)
    pdf.drawString(start_x, baseline, upper_text)
    pdf.setFillColor(TEAL)
    pdf.drawString(start_x + w_upper, baseline, lower)


def draw_word_row(pdf: canvas.Canvas, spec: dict) -> None:
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(MARGIN, 486, f"Words that begin with {spec['upper']}")
    box = 155.0
    xs = [MARGIN, MARGIN + 188.5, MARGIN + 377.0]
    img_y = 318.0
    for (stem, label), x in zip(spec["words"], xs):
        img = ImageReader(asset_path(f"{spec['lower']}-{stem}"))
        pdf.drawImage(img, x, img_y, width=box, height=box,
                      preserveAspectRatio=True, anchor="c", mask="auto")
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawCentredString(x + box / 2, 298, label)


def draw_find_activity(pdf: canvas.Canvas, spec: dict) -> None:
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(MARGIN, 252,
                   f"Find all the {spec['upper']}'s and {spec['lower']}'s.")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 12.5)
    pdf.drawString(MARGIN, 232, spec["verb"])
    theme_fn = HUNT_THEMES[spec["theme"]]
    centers_x = [MARGIN + 66.5 + i * 133 for i in range(4)]
    for row in range(2):
        cy = 184 - row * 94
        for col in range(4):
            index = row * 4 + col
            theme_fn(pdf, centers_x[col], cy, spec["hunt"][index], index)


def build(out_path: str) -> None:
    data = {
        "title": "Learn My Letters: A-Z",
        "subtitle": "Preschool Reading & Language",
        "template": "letters-pack",
    }
    pdf = canvas.Canvas(out_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle("Learn My Letters A-Z | Learning Made Simple")
    for spec in LETTERS:
        draw_header(pdf, data)
        draw_big_letters(pdf, spec["upper"], spec["lower"])
        draw_word_row(pdf, spec)
        draw_find_activity(pdf, spec)
        draw_footer(pdf)
        pdf.showPage()
    pdf.save()
    print(f"wrote {out_path} ({len(LETTERS)} pages)")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..", "worksheets", "preschool", "reading", "letters",
        "learn-my-letters-prototype.pdf",
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build(out)
