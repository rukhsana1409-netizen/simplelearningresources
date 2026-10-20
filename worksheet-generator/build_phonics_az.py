#!/usr/bin/env python3
"""Kindergarten Reading - Phonics: Letter Sounds A-Z (Learning Made Simple).

US Letter portrait. Each activity panel combines teaching + practice:
large lowercase letter -> /sound/ -> 3 large circled picture choices
(letter-to-sound direction). No separate teaching strip.

Canonical logo: verbatim generate_worksheet.py::draw_logo (Addition Within 5
master, via build_shapes_attributes.py). Do not redraw.

Letter allocation (all 26 exactly once; revised 2026-10-13, m moved P3 -> P2):
  P1: s, a, t, p, i, n   (LOCKED 2026-10-09)
  P2: c, k, e, h, r, m  (LOCKED 2026-10-13)
  P3: d, g, o, l        (LOCKED 2026-10-13; spacious 2x2 layout)
  P4: f, b, u, j, v     (LOCKED 2026-10-13; 5 panels: 2+2+1 centered)
  P5: w, x, y, z, qu    (LOCKED 2026-10-13; x = ending /ks/, qu -> /kw/)
  P6: Sound Detective independent review, 12 items (LOCKED 2026-10-13)
"""
import os

from PIL import Image as PILImage
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = letter  # 612 x 792

pdfmetrics.registerFont(TTFont("Andika-Bold",
                               os.path.join(os.path.dirname(
                                   os.path.abspath(__file__)),
                                   "assets", "fonts", "Andika-Bold.ttf")))

TEAL = HexColor("#1F8A8A")
TEAL_DARK = HexColor("#14707A")
NAVY = HexColor("#1F3A5F")
INK = HexColor("#2B3A4A")

_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# ---------------------------------------------------------------------------
# Canonical logo lockup — VERBATIM copy of generate_worksheet.py::draw_logo,
# the approved Addition Within 5 master (via build_shapes_attributes.py).
# Do not redraw, rescale internals, or reinterpret.
# ---------------------------------------------------------------------------
_LOGO_TEAL = HexColor("#007C70")
_LOGO_INK = HexColor("#202A33")
_LOGO_GOLD = HexColor("#F4B63E")


def draw_logo(pdf, x, y):
    """Draw a compact, vector-only Learning Made Simple mark and wordmark."""
    pdf.setFillColor(_LOGO_TEAL)
    pdf.circle(x + 18, y + 26, 7, fill=1, stroke=0)
    pdf.setStrokeColor(_LOGO_TEAL)
    pdf.setLineWidth(2)
    pdf.line(x + 18, y + 18, x + 18, y + 4)
    pdf.line(x + 18, y + 14, x + 6, y + 5)
    pdf.line(x + 18, y + 14, x + 30, y + 5)
    pdf.setLineWidth(1.3)
    pdf.line(x + 2, y + 4, x + 18, y)
    pdf.line(x + 18, y, x + 34, y + 4)
    pdf.setFillColor(_LOGO_GOLD)
    pdf.circle(x + 18, y + 39, 3.5, fill=1, stroke=0)
    pdf.setFillColor(_LOGO_TEAL)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(x + 43, y + 24, "LEARNING")
    pdf.setFillColor(_LOGO_INK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(x + 43, y + 10, "MADE SIMPLE")


def draw_header(pdf, title, subtitle):
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, stroke=0, fill=1)
    draw_logo(pdf, 60, PAGE_HEIGHT - 86)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1)
    pdf.line(218, PAGE_HEIGHT - 88, 218, PAGE_HEIGHT - 48)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(234, PAGE_HEIGHT - 68, title)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(234, PAGE_HEIGHT - 90, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.6)
    pdf.line(60, PAGE_HEIGHT - 104, PAGE_WIDTH - 60, PAGE_HEIGHT - 104)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(60, PAGE_HEIGHT - 126, "Name:")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.2)
    pdf.line(104, PAGE_HEIGHT - 128, 372, PAGE_HEIGHT - 128)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(400, PAGE_HEIGHT - 126, "Date:")
    pdf.line(440, PAGE_HEIGHT - 128, PAGE_WIDTH - 60, PAGE_HEIGHT - 128)


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF2F2"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, stroke=0, fill=1)
    pdf.setFillColor(TEAL_DARK)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(60, 26, "Learning Made Simple")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1)
    pdf.line(218, 14, 218, 34)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_WIDTH / 2 + 20, 25,
                          "Made with love for little learners.")
    pdf.setFont("Helvetica", 8.5)
    pdf.drawRightString(PAGE_WIDTH - 60, 25, "\u00a9 2026 Learning Made Simple")


# ---------------------------------------------------------------------------
# Image helper: circular-masked PNGs with transparent backgrounds, so the
# illustrations sit cleanly inside the choice circles (no white rectangles).
# Masks are cached in /tmp per build run.
# ---------------------------------------------------------------------------
from PIL import ImageDraw as _ImageDraw

_CIRCLE_CACHE = {}


def _img_circle(pdf, path, cx, cy, r, zoom=False):
    full = os.path.join(_ASSETS, path)
    key = (full, zoom)
    if key not in _CIRCLE_CACHE:
        im = PILImage.open(full).convert("RGBA")
        if zoom:
            # Trim near-background margins so the subject fills ~85-90%
            # of the circle, fully inside it with a small margin.
            # Bbox detection runs on the FULL image (140px copy, pure
            # PIL) BEFORE any square crop, so wide subjects are never
            # pre-clipped; the square is padded with the background
            # color where it extends past the image edges.
            small = im.convert("RGB").resize((140, 140), PILImage.BILINEAR)
            px = small.load()
            corners = [px[2, 2], px[137, 2], px[2, 137], px[137, 137]]
            bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
            minx, miny, maxx, maxy = 140, 140, -1, -1
            for yy in range(140):
                for xx in range(140):
                    r0, g0, b0 = px[xx, yy]
                    if max(abs(r0 - bg[0]), abs(g0 - bg[1]),
                           abs(b0 - bg[2])) > 24:
                        minx, maxx = min(minx, xx), max(maxx, xx)
                        miny, maxy = min(miny, yy), max(maxy, yy)
            if maxx >= 0:
                W, H = im.size
                x0, x1 = minx * W / 140.0, (maxx + 1) * W / 140.0
                y0, y1 = miny * H / 140.0, (maxy + 1) * H / 140.0
                side = int(max(x1 - x0, y1 - y0) * 1.14)
                ccx, ccy = (x0 + x1) / 2, (y0 + y1) / 2
                sx0, sy0 = int(ccx - side / 2), int(ccy - side / 2)
                canvas = PILImage.new("RGBA", (side, side),
                                      bg + (255,))
                ix0, iy0 = max(0, sx0), max(0, sy0)
                ix1, iy1 = min(W, sx0 + side), min(H, sy0 + side)
                canvas.paste(im.crop((ix0, iy0, ix1, iy1)),
                             (ix0 - sx0, iy0 - sy0))
                im = canvas
        else:
            s = min(im.size)
            im = im.crop(((im.size[0] - s) // 2, (im.size[1] - s) // 2,
                         (im.size[0] + s) // 2, (im.size[1] + s) // 2))
        im = im.resize((280, 280), PILImage.LANCZOS)
        im = im.resize((280, 280), PILImage.LANCZOS)
        mask = PILImage.new("L", (280, 280), 0)
        _ImageDraw.Draw(mask).ellipse((0, 0, 280, 280), fill=255)
        im.putalpha(mask)
        tmp = "/tmp/phx_circ_%08x.png" % (abs(hash(key)) % 0xFFFFFFFF)
        im.save(tmp)
        _CIRCLE_CACHE[key] = tmp
    pdf.drawImage(_CIRCLE_CACHE[key], cx - r, cy - r, width=2 * r,
                  height=2 * r, mask="auto")
    pdf.setStrokeColor(HexColor("#9DB6C9"))
    pdf.setLineWidth(1.3)
    pdf.circle(cx, cy, r, stroke=1, fill=0)


# ---------------------------------------------------------------------------
# Page 1 -- Meet the Sounds: s, a, t, p, i, n
# ---------------------------------------------------------------------------
# (letter, sound label, key word, key image, [(distractor word, image)] x2)
P1_ITEMS = [
    ("s", "/s/", "sun", "phonics-a-z/ph-sun.jpg",
     [("dog", "animal-library/lib-dog.jpg"),
      ("fish", "animal-library/lib-fish.jpg")]),
    ("a", "/\u0103/", "apple", "phonics-a-z/ph-apple.jpg",
     [("whale", "animal-library/lib-whale.png"),
      ("kangaroo", "animal-library/lib-kangaroo.png")]),
    ("t", "/t/", "tiger", "phonics-a-z/ph-tiger.jpg",
     [("owl", "animal-library/lib-owl.png"),
      ("lamb", "animal-library/lib-lamb.png")]),
    ("p", "/p/", "pig", "animal-library/lib-piglet.jpg",
     [("bird", "animal-library/lib-bird.jpg"),
      ("gorilla", "animal-library/lib-gorilla.png")]),
    ("i", "/\u012d/", "igloo", "pre-writing/pw-igloo.png",
     [("duck", "animal-library/lib-duck.jpg"),
      ("hive", "animal-library/lib-hive.png")]),
    ("n", "/n/", "nest", "animal-library/lib-nest.jpg",
     [("kangaroo", "animal-library/lib-kangaroo.png"),
      ("foal", "animal-library/lib-foal.png")]),
]


def _practice(pdf, items, zoom=False, layout="grid6", instruction=None,
              notes=None):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    _instr = instruction or \
        "Say the sound. Circle the picture that starts with it."
    if "\n" in _instr:
        _l1, _l2 = _instr.split("\n", 1)
        pdf.drawCentredString(PAGE_WIDTH / 2, 648, _l1)
        pdf.drawCentredString(PAGE_WIDTH / 2, 630, _l2)
    else:
        pdf.drawCentredString(PAGE_WIDTH / 2, 640, _instr)
    from reportlab.pdfbase.pdfmetrics import stringWidth
    if layout == "grid4":
        # Spacious 2x2: taller panels, larger circles, even distribution
        panel_w, panel_h, gutter = 250, 240, 32
        row_tops = [622, 338]  # gap between rows 44 (was 80)
        circ_r, circ_cy, circ_x0, circ_pitch = 38, 104, 47, 78
    elif layout == "grid5":
        # 5 panels: 2 + 2 + 1 centered; snug rows, no empty sixth cell
        panel_w, panel_h, gutter = 250, 170, 32
        row_tops = [622, 427, 232]
        circ_r, circ_cy, circ_x0, circ_pitch = 38, 60, 47, 78
    else:
        # Approved grid6 (Pages 1-2, locked): do not alter these numbers
        panel_w, panel_h, gutter = 248, 158, 36
        row_tops = None
        circ_r, circ_cy, circ_x0, circ_pitch = 35, 52, 52, 72
    for i, (letter, sound, _word, img, distractors) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        if layout == "grid5" and i == 4:
            px0 = 40 + (532 - panel_w) // 2  # last panel centered
        if layout in ("grid4", "grid5"):
            py0 = row_tops[row] - panel_h
        else:
            py0 = 606 - row * 172 - panel_h
        # subtle panel
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        # letter -> sound (arrow nudged right only for wide letters like m;
        # narrow letters keep the approved Page 1 positions exactly)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 38)
        pdf.drawString(px0 + 16, py0 + panel_h - 46, letter)
        lw = stringWidth(letter, "Helvetica-Bold", 38)
        ax = max(px0 + 54, px0 + 16 + lw + 10)
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(ax, py0 + panel_h - 40, "\u2192")
        pdf.setFont("Andika-Bold", 22)
        pdf.drawString(ax + 24, py0 + panel_h - 42, sound)
        # 3 picture choices (key + 2 distractors, shuffled)
        choices = [img] + [d[1] for d in distractors]
        order = [0, 1, 2]
        import random
        rnd = random.Random(1000 + i)
        rnd.shuffle(order)
        for k, oi in enumerate(order):
            cx = px0 + circ_x0 + k * circ_pitch
            cy = py0 + circ_cy
            _img_circle(pdf, choices[oi], cx, cy, circ_r, zoom=zoom)
        # optional per-panel instruction note (Page 5: x is an ending
        # sound, so each panel states its own direction)
        if notes and notes[i]:
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawCentredString(px0 + panel_w / 2, py0 + 9, notes[i])


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Letter Sounds A-Z", "Meet the Sounds: s, a, t, p, i, n")
    _practice(pdf, P1_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Meet the Sounds: c, k, e, h, r
# ---------------------------------------------------------------------------
P2_ITEMS = [
    ("c", "/k/", "cat", "animal-library/lib-cat.jpg",
     [("dog", "animal-library/lib-dog.jpg"),
      ("fish", "animal-library/lib-fish.jpg")]),
    ("k", "/k/", "kite", "phonics-a-z/ph-kite.jpg",
     [("whale", "animal-library/lib-whale.png"),
      ("tiger", "phonics-a-z/ph-tiger.jpg")]),
    ("e", "/\u025b/", "elephant", "animal-library/lib-elephant.jpg",
     [("sun", "phonics-a-z/ph-sun.jpg"),
      ("pig", "animal-library/lib-piglet.jpg")]),
    ("h", "/h/", "hat", "phonics-a-z/ph-hat.jpg",
     [("bird", "animal-library/lib-bird.jpg"),
      ("gorilla", "animal-library/lib-gorilla.png")]),
    ("r", "/r/", "rabbit", "phonics-a-z/ph-rabbit.jpg",
     [("fish", "animal-library/lib-fish.jpg"),
      ("sun", "phonics-a-z/ph-sun.jpg")]),
    ("m", "/m/", "moon", "phonics-a-z/ph-moon.jpg",
     [("sun", "phonics-a-z/ph-sun.jpg"),
      ("dog", "animal-library/lib-dog.jpg")]),
]


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Letter Sounds A-Z", "Meet the Sounds: c, k, e, h, r, m")
    _practice(pdf, P2_ITEMS, zoom=True)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Meet the Sounds: d, g, o, l
# ---------------------------------------------------------------------------
P3_ITEMS = [
    ("d", "/d/", "dog", "animal-library/lib-dog.jpg",
     [("cat", "animal-library/lib-cat.jpg"),
      ("sun", "phonics-a-z/ph-sun.jpg")]),
    ("g", "/g/", "gorilla", "animal-library/lib-gorilla.png",
     [("pig", "animal-library/lib-piglet.jpg"),
      ("fish", "animal-library/lib-fish.jpg")]),
    ("o", "/\u0251/", "octopus", "phonics-a-z/ph-octopus.jpg",
     [("tiger", "phonics-a-z/ph-tiger.jpg"),
      ("moon", "phonics-a-z/ph-moon.jpg")]),
    ("l", "/l/", "lion", "phonics-a-z/ph-lion.jpg",
     [("nest", "animal-library/lib-nest.jpg"),
      ("whale", "animal-library/lib-whale.png")]),
]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Letter Sounds A-Z", "Meet the Sounds: d, g, o, l")
    _practice(pdf, P3_ITEMS, zoom=True, layout="grid4")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Meet the Sounds: f, b, u, j, v
# ---------------------------------------------------------------------------
P4_ITEMS = [
    ("f", "/f/", "fish", "animal-library/lib-fish.jpg",
     [("sun", "phonics-a-z/ph-sun.jpg"),
      ("cat", "animal-library/lib-cat.jpg")]),
    ("b", "/b/", "bird", "animal-library/lib-bird.jpg",
     [("dog", "animal-library/lib-dog.jpg"),
      ("pig", "animal-library/lib-piglet.jpg")]),
    ("u", "/\u028c/", "umbrella", "phonics-a-z/ph-umbrella.jpg",
     [("apple", "phonics-a-z/ph-apple.jpg"),
      ("moon", "phonics-a-z/ph-moon.jpg")]),
    ("j", "/d\u0292/", "jam", "phonics-a-z/ph-jam.jpg",
     [("kite", "phonics-a-z/ph-kite.jpg"),
      ("nest", "animal-library/lib-nest.jpg")]),
    ("v", "/v/", "violin", "phonics-a-z/ph-violin.jpg",
     [("whale", "animal-library/lib-whale.png"),
      ("tiger", "phonics-a-z/ph-tiger.jpg")]),
]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Letter Sounds A-Z", "Meet the Sounds: f, b, u, j, v")
    _practice(pdf, P4_ITEMS, zoom=True, layout="grid5")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Meet the Sounds: w, x, y, z, qu
# x is an ENDING sound (fox ends with /ks/); qu is taught as a unit.
# One top instruction covers both directions; only the x panel keeps a
# short note ("Find /ks/ at the end.").
# ---------------------------------------------------------------------------
P5_ITEMS = [
    ("w", "/w/", "watermelon", "phonics-a-z/ph-watermelon.jpg",
     [("sun", "phonics-a-z/ph-sun.jpg"),
      ("dog", "animal-library/lib-dog.jpg")]),
    ("x", "/ks/", "fox", "phonics-a-z/ph-fox.jpg",
     [("cat", "animal-library/lib-cat.jpg"),
      ("pig", "animal-library/lib-piglet.jpg")]),
    ("y", "/j/", "yarn", "phonics-a-z/ph-yarn.jpg",
     [("kite", "phonics-a-z/ph-kite.jpg"),
      ("apple", "phonics-a-z/ph-apple.jpg")]),
    ("z", "/z/", "zebra", "phonics-a-z/ph-zebra.jpg",
     [("nest", "animal-library/lib-nest.jpg"),
      ("tiger", "phonics-a-z/ph-tiger.jpg")]),
    ("qu", "/kw/", "queen", "phonics-a-z/ph-queen.jpg",
     [("moon", "phonics-a-z/ph-moon.jpg"),
      ("fish", "animal-library/lib-fish.jpg")]),
]

P5_NOTES = [
    None,
    "Find /ks/ at the end.",
    None,
    None,
    None,
]


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Letter Sounds A-Z", "Meet the Sounds: w, x, y, z, qu")
    _practice(pdf, P5_ITEMS, zoom=True, layout="grid5",
              instruction="Say the sound. Circle the picture that starts "
                          "with it.\nFor x, find the ending sound.",
              notes=P5_NOTES)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 6 -- Sound Detective (independent cumulative review)
# 12 mixed items sampled from Pages 1-5, all five short vowels included.
# No /sound/ is printed: the child recalls the sound from the letter.
# Compact horizontal rows: letter at left, 3 picture circles to the right.
# ---------------------------------------------------------------------------
P6_ITEMS = [
    ("s", None, "sun", "phonics-a-z/ph-sun.jpg",
     [("cat", "animal-library/lib-cat.jpg"),
      ("pig", "animal-library/lib-piglet.jpg")]),
    ("a", None, "apple", "phonics-a-z/ph-apple.jpg",
     [("moon", "phonics-a-z/ph-moon.jpg"),
      ("fish", "animal-library/lib-fish.jpg")]),
    ("i", None, "igloo", "pre-writing/pw-igloo.png",
     [("dog", "animal-library/lib-dog.jpg"),
      ("nest", "animal-library/lib-nest.jpg")]),
    ("k", None, "kite", "phonics-a-z/ph-kite.jpg",
     [("whale", "animal-library/lib-whale.png"),
      ("tiger", "phonics-a-z/ph-tiger.jpg")]),
    ("e", None, "elephant", "animal-library/lib-elephant.jpg",
     [("hat", "phonics-a-z/ph-hat.jpg"),
      ("pig", "animal-library/lib-piglet.jpg")]),
    ("m", None, "moon", "phonics-a-z/ph-moon.jpg",
     [("sun", "phonics-a-z/ph-sun.jpg"),
      ("dog", "animal-library/lib-dog.jpg")]),
    ("d", None, "dog", "animal-library/lib-dog.jpg",
     [("cat", "animal-library/lib-cat.jpg"),
      ("sun", "phonics-a-z/ph-sun.jpg")]),
    ("o", None, "octopus", "phonics-a-z/ph-octopus.jpg",
     [("tiger", "phonics-a-z/ph-tiger.jpg"),
      ("moon", "phonics-a-z/ph-moon.jpg")]),
    ("f", None, "fish", "animal-library/lib-fish.jpg",
     [("sun", "phonics-a-z/ph-sun.jpg"),
      ("cat", "animal-library/lib-cat.jpg")]),
    ("u", None, "umbrella", "phonics-a-z/ph-umbrella.jpg",
     [("moon", "phonics-a-z/ph-moon.jpg"),
      ("kite", "phonics-a-z/ph-kite.jpg")]),
    ("w", None, "watermelon", "phonics-a-z/ph-watermelon.jpg",
     [("dog", "animal-library/lib-dog.jpg"),
      ("sun", "phonics-a-z/ph-sun.jpg")]),
    ("x", None, "fox", "phonics-a-z/ph-fox.jpg",
     [("cat", "animal-library/lib-cat.jpg"),
      ("pig", "animal-library/lib-piglet.jpg")]),
]


def _review(pdf, items):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 644,
                          "Say the sound. Circle the picture that starts "
                          "with it.")
    pdf.drawCentredString(PAGE_WIDTH / 2, 626,
                          "For x, find the ending sound.")
    panel_w, panel_h, gutter = 250, 86, 32
    for i, (letter, _s, _word, img, distractors) in enumerate(items):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = 618 - row * 95 - panel_h
        pdf.setFillColor(HexColor("#F4F9F9"))
        pdf.setStrokeColor(HexColor("#D9E7E7"))
        pdf.setLineWidth(1)
        pdf.roundRect(px0, py0, panel_w, panel_h, 14, stroke=1, fill=1)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 36)
        pdf.drawString(px0 + 14, py0 + 34, letter)
        choices = [img] + [d[1] for d in distractors]
        order = [0, 1, 2]
        import random
        rnd = random.Random(2000 + i)
        rnd.shuffle(order)
        for k, oi in enumerate(order):
            cx = px0 + 80 + k * 64
            cy = py0 + 43
            _img_circle(pdf, choices[oi], cx, cy, 30, zoom=True)
        if letter == "x":
            # bottom band of the panel, clear of the circles and border
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 9.5)
            pdf.drawRightString(px0 + panel_w - 12, py0 + 4,
                                "Find /ks/ at the end.")


def build_p6_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Letter Sounds A-Z", "Sound Detective")
    _review(pdf, P6_ITEMS)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
PAGES = [
    ("Meet the Sounds: s, a, t, p, i, n", build_p1_page, True),  # APPROVED 2026-10-09
    ("Meet the Sounds: c, k, e, h, r, m", build_p2_page, True),  # APPROVED 2026-10-13
    ("Meet the Sounds: d, g, o, l", build_p3_page, True),  # APPROVED 2026-10-13
    ("Meet the Sounds: f, b, u, j, v", build_p4_page, True),  # APPROVED 2026-10-13
    ("Meet the Sounds: w, x, y, z, qu", build_p5_page, True),  # APPROVED 2026-10-13
    ("Sound Detective", build_p6_page, True),  # APPROVED 2026-10-13
]


def main():
    for title, _builder, locked in PAGES:
        assert locked, "Page not locked: %s" % title
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                          "worksheets", "kindergarten", "reading",
                          "phonics-letter-sounds")
    os.makedirs(outdir, exist_ok=True)
    page_pdfs = []
    for i, (title, builder, _locked) in enumerate(PAGES):
        p = os.path.join(outdir, "phonics-letter-sounds-page-%02d.pdf"
                         % (i + 1))
        builder(p)
        page_pdfs.append(p)
        print("built page %d: %s" % (i + 1, title))
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter()
    for p in page_pdfs:
        for page in PdfReader(p).pages:
            writer.add_page(page)
    bundle = os.path.join(outdir, "phonics-letter-sounds-review.pdf")
    with open(bundle, "wb") as f:
        writer.write(f)
    assert len(PdfReader(bundle).pages) == 6
    print("bundle: %s (6 pages)" % bundle)


if __name__ == "__main__":
    main()
