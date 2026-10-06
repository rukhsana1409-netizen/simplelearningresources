# Build the Compare Weight pack (Kindergarten Math).
# Qualitative weight comparison only: heavier/lighter, balance scales,
# reasoning (bigger != always heavier; full vs empty). No units, no numbers-as-weight.
# Pure vector reportlab output.
# Pages carry a (title, builder, locked) flag. Approved pages are NEVER
# rebuilt differently: builders for locked pages are frozen.
#
# P1 only for now (review). P2-P5 to be added after P1 approval.
#
# Usage: ../.venv/bin/python build_compare_weight.py

import math
import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

PAGE_WIDTH = 612
PAGE_HEIGHT = 792

TEAL = HexColor("#0E7C7B")
TEAL_DARK = HexColor("#0B6362")
INK = HexColor("#1F2A37")
NAVY = HexColor("#1F3A5F")

# cheerful light object palette
APPLE_R = HexColor("#E86A5E")
LEAF = HexColor("#7BC96F")
TRUNK = HexColor("#A9764F")
BOOK_C = HexColor("#6FB3E8")
BOOK_D = HexColor("#4E8FC2")
CUP_C = HexColor("#DCEBFA")
WATER = HexColor("#6FB3E8")
ROCK = HexColor("#B9C3CE")
ROCK_D = HexColor("#8A94A0")
BASKET = HexColor("#D9A05B")
BASKET_D = HexColor("#B07F3F")
PUMPKIN = HexColor("#F2994A")
PUMPKIN_D = HexColor("#D97F33")
STEM = HexColor("#5DA85F")
GLASS = HexColor("#BFE3FF")
# P1 reference-style palette: color-coded key words + tinted rows
HEAVIER_RED = HexColor("#D94F4F")
LIGHTER_ORANGE = HexColor("#E8912D")
ELEPHANT = HexColor("#9AA5B1")
EAR = HexColor("#C3CEDA")
RABBIT = HexColor("#C49A6C")
ROSE = HexColor("#F2A4B8")
BIKE = HexColor("#3E7CB1")
PACK = HexColor("#6FB3E8")
PACK_D = HexColor("#4E8FC2")
BERRY = HexColor("#E8545E")
SEED = HexColor("#FFE08A")
MELON = HexColor("#58B368")
MELON_D = HexColor("#2F7D44")
PILLOW = HexColor("#FFF6E8")
SEAM = HexColor("#E3D3B8")
WOOD = HexColor("#B07A4F")
MATTRESS = HexColor("#DCEBFA")
BLANKET = HexColor("#6FB3E8")
WHEEL_CTR = HexColor("#D9E6F2")
CAR_B = HexColor("#6FB3E8")
ER_PINK = HexColor("#F6A9C0")
GRAY = HexColor("#9AA5B1")
PENCIL_Y = HexColor("#FFD54A")
PENCIL_D = HexColor("#E0A93B")
HL_YELLOW = HexColor("#FFE08A")
HL_GRAY = HexColor("#B9C3CE")
HL_EAR = HexColor("#D9E2EC")
ELEPHANT_D = HexColor("#8A94A0")
HL_RABBIT = HexColor("#D9B48F")
CAR_RED = HexColor("#E86A5E")
HL_CAR = HexColor("#F2A4A8")
HL_PACK = HexColor("#8FC3EE")
BOTTLE = HexColor("#7FC8F8")
HL_MELON = HexColor("#A8DDB0")
STEM_D = HexColor("#6B8F3E")
HL_BERRY = HexColor("#F7A8B0")
WOOD_D = HexColor("#8F5F3A")
BLANKET_D = HexColor("#4E8FC2")
CREAM = HexColor("#FFF9F0")
PAGE_L = HexColor("#D8DEE6")
HL_BOOK = HexColor("#8FC3EE")
SLEEVE_B = HexColor("#3E7CB1")
HL_ERASER = HexColor("#F9C6DA")
SHADOW = HexColor("#E3E8EE")
BOWL = HexColor("#3A4A5E")
BOWL_HL = HexColor("#5A6E86")
BOWL_HOLE = HexColor("#1F2A37")
TENNIS = HexColor("#D7E94C")
CASE = HexColor("#C98F4E")
CASE_D = HexColor("#A96F35")
GRAY_L = HexColor("#D5DEE8")
FEATHER = HexColor("#BFE3FF")
PACK = HexColor("#4E9BE0")
PACK_L = HexColor("#8FC3EE")
PACK_D = HexColor("#3573AB")
SHOE = HexColor("#E86A5E")
SHOE_D = HexColor("#C24E42")
SOLE = HexColor("#F2F4F7")
CLIP = HexColor("#9AA5B1")
HL_PUMPKIN = HexColor("#F7B96E")
LEAFG = HexColor("#58B368")
LEAF_D = HexColor("#2F7D44")
BAG = HexColor("#D9A05B")
BAG_D = HexColor("#B07F3F")
BAGUETTE = HexColor("#E8B96E")
BAGUETTE_D = HexColor("#C99A52")
GREENS = HexColor("#58B368")


def draw_logo(pdf, x, y):
    pdf.setFillColor(TEAL)
    pdf.circle(x, y, 9, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#F2C14E"))
    pdf.circle(x + 7, y + 11, 5, fill=1, stroke=0)
    pdf.setStrokeColor(TEAL_DARK)
    pdf.setLineWidth(1.6)
    pdf.line(x, y - 9, x - 8, y - 20)
    pdf.line(x, y - 9, x + 8, y - 20)
    pdf.line(x, y - 9, x, y - 21)


def draw_header(pdf, page_title, subtitle):
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, fill=1, stroke=0)
    draw_logo(pdf, 78, 720)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(96, 728, "LEARNING")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(96, 714, "MADE SIMPLE")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1)
    pdf.line(196, 700, 196, 742)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(212, 726, page_title)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(212, 706, subtitle)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.4)
    pdf.line(40, 688, PAGE_WIDTH - 40, 688)
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(40, 668, "Name:")
    pdf.line(82, 666, 300, 666)
    pdf.drawString(330, 668, "Date:")
    pdf.line(368, 666, 540, 666)


def draw_instruction(pdf, text):
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(PAGE_WIDTH / 2, 630, text)


def draw_footer(pdf):
    pdf.setFillColor(HexColor("#EAF2F1"))
    pdf.rect(0, 0, PAGE_WIDTH, 44, fill=1, stroke=0)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, 18, "Learning Made Simple")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(0.8)
    pdf.line(190, 8, 190, 30)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(PAGE_WIDTH / 2, 18, "Made with love for little learners.")
    pdf.drawRightString(PAGE_WIDTH - 40, 18, "\u00a9 2026 Learning Made Simple")


def draw_panel(pdf, x, top, w, h):
    pdf.setFillColor(HexColor("#F7FAFC"))
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - h, w, h, 12, stroke=1, fill=1)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Page 1 -- Heavy or Light?  (AI-illustrated: storybook watercolor objects
# on white cards, tinted rows, color-coded key words, compact instruction)
# ---------------------------------------------------------------------------
CW_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "assets", "compare-weight")

# pastel row tints with matching borders
TINTS = [
    (HexColor("#FDE9EE"), HexColor("#F3C6D3")),  # pink
    (HexColor("#FDF4DC"), HexColor("#EDD9A8")),  # yellow
    (HexColor("#E4F1FB"), HexColor("#B9D6EC")),  # blue
    (HexColor("#E5F5EA"), HexColor("#BDE3C9")),  # green
    (HexColor("#F0E9F8"), HexColor("#D3C2EA")),  # purple
]

# (left_img, right_img, key_word) -- correct sides L,R,R,L,R
P1_ROWS = [
    ("cw-watermelon.jpg", "cw-strawberry.jpg", "heavier"),
    ("cw-backpack.jpg", "cw-pencil.jpg", "lighter"),
    ("cw-paper.jpg", "cw-book.jpg", "heavier"),
    ("cw-leaf.jpg", "cw-pumpkin.jpg", "lighter"),
    ("cw-brick.jpg", "cw-balloon.jpg", "heavier"),
]

CARD_W, CARD_H = 174, 84


def _place_illustration(pdf, img_name, card_x, card_y,
                        card_w=CARD_W, card_h=CARD_H):
    from PIL import Image as PILImage
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#D5DEE8"))
    pdf.setLineWidth(1.2)
    pdf.roundRect(card_x, card_y, card_w, card_h, 10, stroke=1, fill=1)
    path = os.path.join(CW_ASSETS, img_name)
    iw, ih = PILImage.open(path).size
    pad = 6
    scale = min((card_w - 2 * pad) / iw, (card_h - 2 * pad) / ih)
    dw, dh = iw * scale, ih * scale
    pdf.drawImage(path, card_x + (card_w - dw) / 2,
                  card_y + (card_h - dh) / 2, dw, dh)


def _number_box(pdf, x, y, w=40, h=22):
    pdf.setFillColor(white)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.roundRect(x, y, w, h, 6, stroke=1, fill=1)


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Heavy or Light?", "Compare Weight")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640,
                          "Look at each pair. Circle the heavier or lighter object.")

    tops = (606, 502, 398, 294, 190)
    for k, (limg, rimg, word) in enumerate(P1_ROWS):
        top = tops[k]
        tint, border = TINTS[k]
        pdf.setFillColor(tint)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 96, 532, 96, 12, stroke=1, fill=1)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.2)
        pdf.line(162, top - 88, 162, top - 8)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(56, top - 34, "Circle the")
        pdf.setFont("Helvetica-Bold", 19)
        pdf.setFillColor(HEAVIER_RED if word == "heavier" else LIGHTER_ORANGE)
        pdf.drawString(56, top - 57, word)
        pdf.setFillColor(INK)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(56, top - 78, "one.")
        _place_illustration(pdf, limg, 184, top - 90)
        _place_illustration(pdf, rimg, 384, top - 90)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Order by Weight. Four trios with unmistakable real-world weight
# progressions; positions randomized (never lightest -> heaviest).
# Verified answers (1=lightest, 2=middle, 3=heaviest):
#   row1: bicycle(3) feather(1) apple(2)
#   row2: paperclip(1) suitcase(3) book(2)
#   row3: shoe(2) leaf(1) chair(3)
#   row4: watermelon(3) orange(2) pencil(1)
# ---------------------------------------------------------------------------
P2_ROWS = [
    ("cw2-bicycle.jpg", "cw2-feather.jpg", "cw2-apple.jpg"),
    ("cw3-paperclip.jpg", "cw3-suitcase.jpg", "cw-book.jpg"),
    ("cw2-shoe.jpg", "cw-leaf.jpg", "cw3-chair.jpg"),
    ("cw-watermelon.jpg", "cw2-orange.jpg", "cw-pencil.jpg"),
]

P2_TINTS = TINTS[:4]
P2_CARD_XS = (58, 227, 396)
P2_CARD_W, P2_CARD_H = 158, 84


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Order by Weight", "Compare Weight")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 640,
        "Number the objects: 1 = lightest, 2 = middle, 3 = heaviest.")

    tops = (598, 462, 326, 190)
    for k, row in enumerate(P2_ROWS):
        top = tops[k]
        tint, border = P2_TINTS[k]
        pdf.setFillColor(tint)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(40, top - 126, 532, 126, 12, stroke=1, fill=1)
        for j, img in enumerate(row):
            cx = P2_CARD_XS[j]
            _place_illustration(pdf, img, cx, top - 98,
                                P2_CARD_W, P2_CARD_H)
            _number_box(pdf, cx + (P2_CARD_W - 40) / 2, top - 124)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()

# ---------------------------------------------------------------------------
# Page 3 -- Balance Scale Detective. The scale position is the evidence:
# lower side = heavier, higher side = lighter. Object pairs are deliberately
# ambiguous so children must read the scale, not prior knowledge.
# Verified (lower side / answer side):
#   p1: apple down-L / orange up-R, "heavier" -> apple (L)
#   p2: ball up-L / teddy down-R, "lighter" -> ball (L)
#   p3: block up-L / book down-R, "heavier" -> book (R)
#   p4: mitten down-L / hat up-R, "lighter" -> hat (R)
# ---------------------------------------------------------------------------
SCALE_WOOD = HexColor("#B07A4F")
SCALE_DARK = HexColor("#8F5F3A")
PAN_C = HexColor("#DCEBFA")
PAN_D = HexColor("#B9D2EA")


def _draw_pan(pdf, px, py, rx):
    pdf.setFillColor(PAN_C)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    p = pdf.beginPath()
    p.moveTo(px - rx, py)
    p.curveTo(px - rx, py - 20, px + rx, py - 20, px + rx, py)
    p.close()
    pdf.drawPath(p, stroke=1, fill=1)
    pdf.setFillColor(PAN_D)
    pdf.ellipse(px - rx, py - 5, px + rx, py + 5, stroke=1, fill=1)


def draw_balance_scale(pdf, cx, pivot_y, half_beam=80, tilt_deg=16,
                       left_down=True, hang=36, pan_rx=44, base_y=None):
    drop = half_beam * math.sin(math.radians(tilt_deg))
    run = half_beam * math.cos(math.radians(tilt_deg))
    # NOTE: in PDF coordinates larger y = higher on the page,
    # so the LOWER side gets the SMALLER y.
    if left_down:
        ly, ry = pivot_y - drop, pivot_y + drop
    else:
        ly, ry = pivot_y + drop, pivot_y - drop
    lx, rx = cx - run, cx + run
    if base_y is None:
        base_y = pivot_y - 120
    pdf.setFillColor(SCALE_DARK)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.6)
    pdf.roundRect(cx - 26, base_y, 52, 12, 4, stroke=1, fill=1)
    pdf.setFillColor(SCALE_WOOD)
    pdf.rect(cx - 5, base_y + 12, 10, pivot_y - base_y - 12, stroke=1, fill=1)
    pdf.setStrokeColor(SCALE_DARK)
    pdf.setLineWidth(9)
    pdf.setLineCap(1)
    pdf.line(lx, ly, rx, ry)
    pdf.setFillColor(SCALE_DARK)
    pdf.setStrokeColor(INK)
    pdf.setLineWidth(1.4)
    pdf.circle(lx, ly, 5, stroke=1, fill=1)
    pdf.circle(rx, ry, 5, stroke=1, fill=1)
    pdf.setFillColor(INK)
    pdf.circle(cx, pivot_y, 5.5, stroke=0, fill=1)
    pans = []
    for px, py in ((lx, ly), (rx, ry)):
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.8)
        pdf.line(px, py - 4, px, py - hang)
        _draw_pan(pdf, px, py - hang, pan_rx)
        pans.append((px, py - hang))
    return pans


def _object_on_pan(pdf, img_name, px, py, card_w=80, card_h=54):
    _place_illustration(pdf, img_name, px - card_w / 2, py + 3, card_w, card_h)


def _labeled_line(pdf, x, y, before, word, color):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    pdf.setFont("Helvetica-Bold", 13)
    pdf.setFillColor(NAVY)
    pdf.drawString(x, y, before)
    pdf.setFillColor(color)
    pdf.drawString(x + stringWidth(before, "Helvetica-Bold", 13), y, word)


def _question(pdf, cx, y, word):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    pdf.setFont("Helvetica-Bold", 13)
    before = "Which is "
    bw = stringWidth(before, "Helvetica-Bold", 13)
    qw = stringWidth(word + "?", "Helvetica-Bold", 13)
    x0 = cx - (bw + qw) / 2
    pdf.setFillColor(NAVY)
    pdf.drawString(x0, y, before)
    pdf.setFillColor(HEAVIER_RED if word in ("heavier", "heaviest") else LIGHTER_ORANGE)
    pdf.drawString(x0 + bw, y, word + "?")


def _answer_pills(pdf, cx, y, labels):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    pdf.setFont("Helvetica-Bold", 11)
    widths = [stringWidth(t, "Helvetica-Bold", 11) + 22 for t in labels]
    total = sum(widths) + 12
    x = cx - total / 2
    for t, w in zip(labels, widths):
        pdf.setFillColor(white)
        pdf.setStrokeColor(INK)
        pdf.setLineWidth(1.3)
        pdf.roundRect(x, y, w, 20, 10, stroke=1, fill=1)
        pdf.setFillColor(INK)
        pdf.drawCentredString(x + w / 2, y + 6.5, t)
        x += w + 12


P3_PROBLEMS = [
    ("cw2-apple.jpg", "cw2-orange.jpg", True, "heavier", ("apple", "orange")),
    ("cw3-ball.jpg", "cw3-teddy.jpg", False, "lighter", ("ball", "teddy bear")),
    ("cw3-block.jpg", "cw-book.jpg", False, "heavier", ("block", "book")),
    ("cw3-mitten.jpg", "cw3-hat.jpg", True, "lighter", ("mitten", "hat")),
]
P3_TINTS = [TINTS[0], TINTS[2], TINTS[3], TINTS[4]]


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Balance Scale Detective", "Compare Weight")

    # teaching example
    pdf.setFillColor(HexColor("#FFF8E7"))
    pdf.setStrokeColor(HexColor("#EDD9A8"))
    pdf.setLineWidth(1.4)
    pdf.roundRect(40, 548, 532, 92, 12, stroke=1, fill=1)
    pans = draw_balance_scale(pdf, 150, 598, half_beam=64, left_down=True,
                              hang=30, pan_rx=36, base_y=552)
    _object_on_pan(pdf, "cw2-apple.jpg", pans[0][0], pans[0][1], 56, 40)
    _object_on_pan(pdf, "cw2-feather.jpg", pans[1][0], pans[1][1], 56, 40)
    _labeled_line(pdf, 300, 604, "Lower side = ", "heavier.", HEAVIER_RED)
    _labeled_line(pdf, 300, 580, "Higher side = ", "lighter.", LIGHTER_ORANGE)

    # 4 large problems in a 2x2 grid
    for k, (limg, rimg, left_down, word, pills) in enumerate(P3_PROBLEMS):
        col, row = k % 2, k // 2
        x = 40 + col * 276
        top = 532 - row * 240
        tint, border = P3_TINTS[k]
        pdf.setFillColor(tint)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - 232, 256, 232, 12, stroke=1, fill=1)
        _question(pdf, x + 128, top - 22, word)
        pans = draw_balance_scale(pdf, x + 128, top - 72, left_down=left_down,
                                  hang=36, pan_rx=44, base_y=top - 192)
        _object_on_pan(pdf, limg, pans[0][0], pans[0][1])
        _object_on_pan(pdf, rimg, pans[1][0], pans[1][1])
        _answer_pills(pdf, x + 128, top - 218, pills)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()

# ---------------------------------------------------------------------------
# Page 4 -- Think About Weight. Two balance-scale clues order three objects;
# the child combines BOTH clues (transitive reasoning). Pictures only, no
# letters or symbols. Verified:
#   p1: apple>orange, orange>strawberry; "heaviest" -> apple (choice pos 3)
#   p2: book>block, block>ball; "lightest" -> ball (choice pos 1)
#   p3: teddy>hat, hat>mitten; "heaviest" -> teddy (choice pos 2)
#   p4: shoe>pencil, pencil>paperclip; "lightest" -> paperclip (choice pos 1)
# ---------------------------------------------------------------------------
P4_PROBLEMS = [
    ("cw2-apple.jpg", "cw2-orange.jpg", "cw-strawberry.jpg",
     "heaviest", True, False, (2, 1, 0)),
    ("cw-book.jpg", "cw3-block.jpg", "cw3-ball.jpg",
     "lightest", True, False, (2, 0, 1)),
    ("cw3-teddy.jpg", "cw3-hat.jpg", "cw3-mitten.jpg",
     "heaviest", False, True, (2, 0, 1)),
    ("cw2-shoe.jpg", "cw-pencil.jpg", "cw3-paperclip.jpg",
     "lightest", True, False, (2, 0, 1)),
]
P4_TINTS = [TINTS[1], TINTS[0], TINTS[2], TINTS[3]]


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Think About Weight", "Compare Weight")
    pdf.setFillColor(INK)
    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640, "Use both scales. Circle the answer.")
    for k, (aimg, bimg, cimg, qword, s1ld, s2ld, order) in enumerate(P4_PROBLEMS):
        col, row = k % 2, k // 2
        x = 40 + col * 272
        top = 612 - row * 276
        tint, border = P4_TINTS[k]
        pdf.setFillColor(tint)
        pdf.setStrokeColor(border)
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, top - 264, 260, 264, 12, stroke=1, fill=1)
        # two clue scales: clue 1 shows A heavier than B, clue 2 B heavier than C
        clues = ((s1ld, aimg, bimg), (s2ld, bimg, cimg))
        for j, (ld, heavy_img, light_img) in enumerate(clues):
            cx = x + 62 + j * 136
            limg = heavy_img if ld else light_img
            rimg = light_img if ld else heavy_img
            pans = draw_balance_scale(pdf, cx, top - 80, half_beam=40,
                                      tilt_deg=20, left_down=ld, hang=28,
                                      pan_rx=24, base_y=top - 148)
            _object_on_pan(pdf, limg, pans[0][0], pans[0][1], 48, 34)
            _object_on_pan(pdf, rimg, pans[1][0], pans[1][1], 48, 34)
        _question(pdf, x + 130, top - 168, qword)
        imgs = (aimg, bimg, cimg)
        for m, idx in enumerate(order):
            _place_illustration(pdf, imgs[idx], x + 3 + m * 88, top - 234, 78, 56)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()

# ---------------------------------------------------------------------------
# Page 5 -- Weight Challenge (final review page). Four sections:
#   1. Order by Weight: feather(1) < soccer ball(2) < chair(3); display order
#      chair, feather, soccer ball -> answers 3, 1, 2.
#   2. Balance Scale: book down-L / balloon up-R; "heavier" -> book (L).
#   3. Draw something heavier than a pencil (many answers: book, shoe...).
#   4. Draw something lighter than a backpack (many answers: feather...).
# ---------------------------------------------------------------------------
P5_ORDER = [
    ("cw3-chair.jpg", 3),
    ("cw2-feather.jpg", 1),
    ("cw5-soccer.jpg", 2),
]
P5_TINTS = [TINTS[1], TINTS[0], TINTS[3], TINTS[2]]


def _draw_prompt(pdf, x, y, keyword, rest, color):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    pdf.setFont("Helvetica-Bold", 12.5)
    pdf.setFillColor(NAVY)
    pdf.drawString(x, y, "Draw something")
    pdf.setFillColor(color)
    pdf.drawString(x, y - 20, keyword)
    kw = stringWidth(keyword, "Helvetica-Bold", 12.5)
    pdf.setFillColor(NAVY)
    pdf.drawString(x + kw, y - 20, rest)


def _drawing_box(pdf, x, y, w, h):
    pdf.setFillColor(white)
    pdf.setStrokeColor(HexColor("#B9C6D6"))
    pdf.setLineWidth(1.4)
    pdf.setDash(6, 4)
    pdf.roundRect(x, y, w, h, 8, stroke=1, fill=1)
    pdf.setDash()


def _section_title(pdf, cx, y, text):
    pdf.setFont("Helvetica-Bold", 13)
    pdf.setFillColor(NAVY)
    pdf.drawCentredString(cx, y, text)


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    draw_header(pdf, "Weight Challenge", "Compare Weight")

    # ---- Section 1: Order by Weight (upper left)
    x, top = 40, 640
    tint, border = P5_TINTS[0]
    pdf.setFillColor(tint)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - 250, 260, 250, 12, stroke=1, fill=1)
    _section_title(pdf, x + 130, top - 24, "Order by Weight")
    pdf.setFont("Helvetica", 11.5)
    pdf.setFillColor(NAVY)
    pdf.drawCentredString(x + 130, top - 46, "Number them:")
    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(x + 130, top - 64, "1 = lightest, 2 = middle, 3 = heaviest.")
    for i, (img, _ans) in enumerate(P5_ORDER):
        cx = x + 8 + i * 84 + 38
        _place_illustration(pdf, img, x + 8 + i * 84, top - 142, 76, 58)
        _number_box(pdf, cx - 19, top - 184, 38, 34)

    # ---- Section 2: Balance Scale (upper right)
    x, top = 312, 640
    tint, border = P5_TINTS[1]
    pdf.setFillColor(tint)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - 250, 260, 250, 12, stroke=1, fill=1)
    _section_title(pdf, x + 130, top - 24, "Balance Scale")
    _question(pdf, x + 130, top - 48, "heavier")
    pans = draw_balance_scale(pdf, x + 130, top - 104, half_beam=72,
                              tilt_deg=16, left_down=True, hang=34,
                              pan_rx=38, base_y=top - 192)
    _object_on_pan(pdf, "cw-book.jpg", pans[0][0], pans[0][1], 72, 50)
    _object_on_pan(pdf, "cw-balloon.jpg", pans[1][0], pans[1][1], 72, 50)
    _answer_pills(pdf, x + 130, top - 226, ("book", "balloon"))

    # ---- Section 3: Draw heavier than a pencil (lower left)
    x, top = 40, 374
    tint, border = P5_TINTS[2]
    pdf.setFillColor(tint)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - 290, 260, 290, 12, stroke=1, fill=1)
    _draw_prompt(pdf, x + 14, top - 32, "heavier ", "than a pencil.", HEAVIER_RED)
    _place_illustration(pdf, "cw-pencil.jpg", x + 184, top - 78, 64, 46)
    _drawing_box(pdf, x + 12, top - 278, 236, 164)

    # ---- Section 4: Draw lighter than a backpack (lower right)
    x, top = 312, 374
    tint, border = P5_TINTS[3]
    pdf.setFillColor(tint)
    pdf.setStrokeColor(border)
    pdf.setLineWidth(1.4)
    pdf.roundRect(x, top - 290, 260, 290, 12, stroke=1, fill=1)
    _draw_prompt(pdf, x + 14, top - 32, "lighter ", "than a backpack.", LIGHTER_ORANGE)
    _place_illustration(pdf, "cw-backpack.jpg", x + 184, top - 78, 64, 46)
    _drawing_box(pdf, x + 12, top - 278, 236, 164)

    draw_footer(pdf)
    pdf.showPage()
    pdf.save()

# ---------------------------------------------------------------------------
# Driver (P1 only for now)
# ---------------------------------------------------------------------------
PAGES = [
    # (title, builder, locked)
    ("Heavy or Light?", build_p1_page, True),  # APPROVED 2026-10-06
    ("Order by Weight", build_p2_page, True),  # APPROVED 2026-10-06
    ("Balance Scale Detective", build_p3_page, True),  # APPROVED 2026-10-06
    ("Think About Weight", build_p4_page, True),  # APPROVED 2026-10-06
    ("Weight Challenge", build_p5_page, True),  # APPROVED 2026-10-06
]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "worksheets", "kindergarten", "math",
                           "compare-weight")
    os.makedirs(out_dir, exist_ok=True)
    pages = []
    for i, (title, builder, locked) in enumerate(PAGES):
        tmp = os.path.join("/tmp", "cw_tmp_%d.pdf" % i)
        builder(tmp)
        pages.append(tmp)
        print("built page: %s" % title)
    from pypdf import PdfWriter
    writer = PdfWriter()
    for p in pages:
        writer.append(p)
    final = os.path.join(out_dir, "compare-weight-review.pdf")
    with open(final, "wb") as f:
        writer.write(f)
    print("merged %d page(s) -> %s" % (len(pages), final))


if __name__ == "__main__":
    main()
