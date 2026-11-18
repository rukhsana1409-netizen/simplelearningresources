#!/usr/bin/env python3
"""Grade 1 Math - Coins and Money: Identify, Count and Add.

A new resource for the locked Grade 1 Math roadmap, added
at her direction 2026-11-18 because Ayan's Grade 1
classroom is teaching coins now. Money was deliberately
NOT proposed in the locked roadmap (2026-11-04), so this
pack is a roadmap addition, approved as a plan
2026-11-18 (6 student pages + 1-page Parent Guide).

Placement: Grade 1 / Math, new topic "Money" (Grade 2
already has a Money topic). Slug: coins-and-money.
Codex assigns the catalog number at integration.
Do NOT integrate, merge, or publish until she approves
the completed pack.

Alignment, stated honestly (no Grade 1 money standard
claimed anywhere): there is NO Grade 1 Common Core /
Michigan money standard. Money is formally Grade 2:
2.MD.C.8 (solve word problems with dollar bills,
quarters, dimes, nickels, and pennies, using $ and
cent symbols). This pack is introductory Grade 1
enrichment that prepares children for 2.MD.C.8. It
builds on real Grade 1 standards: 1.OA.A.1, 1.OA.A.2
(word problems within 20), 1.OA.C.6 (add within 20),
1.NBT.A.1 (count to 120, which covers counting coin
values up to 100 cents). Standards codes stay on the
website resource page only, never on printable pages.
Michigan note: the pre-2010 Grade 1 GLCEs did include
coin identification (M.UN.01.04-01.06), and Michigan
districts still teach it in Grade 1 (e.g. Midland 2026-27
handbook lists "identify coins and bills and state their
values" under Grade 1 Measurement and Data). RCS Atlas
Grade 1 math units have no money-titled unit; the
classroom teaching is the live evidence.

Revision v2 (2026-11-18, her review): print sharpness and
page space. The v1 coins printed soft because the shared
_img_circle helper downsamples every picture to 280x280
px, so the largest coins printed at only ~210 PPI. This
builder now draws 900x900 px circled masters built by
build_coin_masters.py from the same 2000x2000 originals
(same disc detection and 1.14x square crop, transparent
padding instead of a background-color fill, so there is
no dark ring around the penny). The largest coin now
prints at over 600 PPI. Text, lines, and borders were
already vector and print sharp; the soft text she saw
was the 110-dpi preview render, so final previews are
rendered at 200 dpi. Layout changes in v2: P1 coins
bigger (panels base 52, size row base 40); P2 coins
base 27 with wider row spacing; P3 coins base 32 with
wider rows; P4 coins base 28 plus a "Steps:" write-in
line under each row for counting steps; P5 rows spread
vertically across the page with base 20 coins; P6 panels
taller (230) with bigger coins, answer lines, and Yes/No
pills; Parent Guide body 12.5pt with wider spacing.
All activities, totals, and coin combinations are
unchanged from the approved plan.

Coin pictures: real U.S. Mint obverse images.
  penny   Wikimedia Commons "US One Cent Obv.png"
          (2000x2000, public domain)
  nickel  U.S. Mint image library, 2025 Jefferson nickel,
          Uncirculated Obverse, Philadelphia
          (usmint.gov, offered for use in publications)
  dime    U.S. Mint image library, 2025 Roosevelt dime,
          Uncirculated Obverse, Philadelphia
  quarter U.S. Mint image library, 2025 American Women
          Quarters obverse (standard Washington portrait),
          Uncirculated Obverse, Philadelphia
The nickel, dime, and quarter come from the Mint
directly because Wikimedia Commons rate-limited
downloads (HTTP 429) on 2026-11-18 and the Mint's
content server blocks command-line fetches (Cloudflare
challenge), so the three Mint images were downloaded
through the live browser. All four are the classic
designs children see in circulation: Lincoln penny,
Jefferson nickel, Roosevelt dime, Washington quarter.
The builder draws 900x900 px circled masters
(assets/coins-and-money/hi/, built by
build_coin_masters.py), NOT the shared _img_circle
helper, which downsamples to 280x280 px.
Real diameters (U.S. Mint): quarter 24.26 mm, nickel
21.21 mm, penny 19.05 mm, dime 17.91 mm. Every coin on
every page is drawn at a radius proportional to its real
diameter, so the relative sizes are true: the dime is
visibly the smallest coin and the quarter the biggest.
The pack teaches that directly: the dime is smaller
than the nickel but worth more.

Scope: the four coins only. No bills, no half dollars,
no dollar coins. No making change. Every total stays
within 100 cents, and totals grow gradually.

Pages (all math verified in the data tables below):
  P1: Meet the Coins. Name and value each coin (write
      the value). Then the coins in size order, smallest
      to biggest, with the dime-smaller-but-worth-more
      teaching line.
  P2: Match the Coins. Two matchings: coins to names,
      then coins to values. Shuffled so no correct pair
      sits straight across.
  P3: Count the Coins. Groups of identical coins, count
      by 1s, 5s, 10s, 25s. Totals 3, 20, 30, 50, 100.
  P4: Add Mixed Coins. Worked example (quarter + dime
      = 35 cents), then 5 groups progressing 2 coins,
      2 coins, 3 coins, 3 coins, 4 coins. Totals 30, 11,
      36, 16, 41. Generous working space.
  P5: Make the Amount. Circle coins to make each
      amount. Every amount is achievable with the coins
      shown; two amounts ask for two distinct ways.
      10c one way (dime); 15c two ways (dime + nickel,
      or nickel + nickel + 5 pennies); 30c one way
      (quarter + nickel); 25c two ways (quarter, or
      dime + 3 nickels).
  P6: Money Word Problems. Four short illustrated
      problems, answers in cents, plus one buying
      question with no change: Sam has exactly 40c for
      a 40c ball. Answers 23c, 30c, 15c, Yes.

Parent Guide (separate one-page PDF, NOT in the student
bundle): coin value table with the size note, how to
help, the full answer key, and what to do if it is hard.
No standards codes in the guide.

Shared design code (logo, header, footer, circular-masked
pictures) is imported verbatim from build_phonics_az.py.
Do not fork it here. Header title is drawn at 15pt (not
the usual 18pt) because the full approved title is 363pt
wide at 18pt and would run 45pt past the teal rule; the
subtitle stays at 14pt.
"""
import hashlib
import os
import textwrap

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter as _letter  # noqa: F401
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

from build_phonics_az import (NAVY, PAGE_HEIGHT, PAGE_WIDTH, TEAL,
                              _ASSETS, draw_footer, draw_header,
                              draw_logo)

TITLE = "Coins and Money: Identify, Count and Add"
SUBTITLE = "Grade 1 Math | Coins and Money"

ADULT_GREY = HexColor("#37474F")
PANEL_FILL = HexColor("#F4F9F9")
PANEL_STROKE = HexColor("#D9E7E7")
BOX_STROKE = HexColor("#7FA3B5")
LIGHT_TEAL = HexColor("#E3F2F2")
GOLD = HexColor("#F4B63E")
CORAL = HexColor("#E86A6A")

OUT_DIR = os.path.join(os.path.expanduser("~"), "workspace",
                       "your_files", "coins-and-money")
ASSETS = "coins-and-money/"

CENT = "\u00a2"

# Real U.S. Mint diameters in mm. Display radius is always
# proportional to these, so relative sizes stay true.
# Images are the 900x900 px circled masters in hi/ (see
# build_coin_masters.py); the v1 build used the shared
# _img_circle helper, which downsamples to 280x280 px and
# printed the largest coins at only ~210 PPI.
COINS = {
    "penny":   {"name": "penny",   "value": 1,  "dia": 19.05,
                "img": ASSETS + "hi/coin-penny-900.png"},
    "nickel":  {"name": "nickel",  "value": 5,  "dia": 21.21,
                "img": ASSETS + "hi/coin-nickel-900.png"},
    "dime":    {"name": "dime",    "value": 10, "dia": 17.91,
                "img": ASSETS + "hi/coin-dime-900.png"},
    "quarter": {"name": "quarter", "value": 25, "dia": 24.26,
                "img": ASSETS + "hi/coin-quarter-900.png"},
}
QUARTER_DIA = 24.26


def _coin_r(base_r, key):
    """Display radius for a coin, true to its real size."""
    return base_r * COINS[key]["dia"] / QUARTER_DIA


def _coin(pdf, key, cx, cy, base_r):
    """Draw a coin from its 900x900 master, at true relative
    size, with the same light border ring _img_circle draws.
    The master is already circular-masked with transparent
    corners, so drawImage with mask="auto" keeps the
    circle; the ring is vector and prints sharp."""
    r = _coin_r(base_r, key)
    pdf.drawImage(os.path.join(_ASSETS, COINS[key]["img"]),
                  cx - r, cy - r, width=2 * r, height=2 * r,
                  mask="auto")
    pdf.setStrokeColor(HexColor("#9DB6C9"))
    pdf.setLineWidth(1.3)
    pdf.circle(cx, cy, r, stroke=1, fill=0)


def _adult_line(pdf, text):
    """Centred adult line at y=74. Splits into two lines if
    the text would run past the page edges."""
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica-Bold", 10.5)
    if stringWidth(text, "Helvetica-Bold", 10.5) <= 560:
        pdf.drawCentredString(PAGE_WIDTH / 2, 74, text)
        return
    words = text.split(" ")
    half = len(words) // 2
    best = None
    for i in range(2, len(words) - 1):
        w1 = stringWidth(" ".join(words[:i]), "Helvetica-Bold",
                         10.5)
        w2 = stringWidth(" ".join(words[i:]), "Helvetica-Bold",
                         10.5)
        if best is None or max(w1, w2) < best[0]:
            best = (max(w1, w2), i)
    i = best[1]
    pdf.drawCentredString(PAGE_WIDTH / 2, 80,
                          " ".join(words[:i]))
    pdf.drawCentredString(PAGE_WIDTH / 2, 64,
                          " ".join(words[i:]))


def _page_title(pdf, title, instruction):
    """Page title at 642 and instruction line(s) below it.
    Returns the y of the top of the content area: 606 for a
    one-line instruction, 592 for a two-line instruction."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 642, title)
    if "\n" in instruction:
        line1, line2 = instruction.split("\n", 1)
        pdf.drawCentredString(PAGE_WIDTH / 2, 624, line1)
        pdf.drawCentredString(PAGE_WIDTH / 2, 606, line2)
        return 592
    pdf.drawCentredString(PAGE_WIDTH / 2, 624, instruction)
    return 606


def _panel(pdf, x, y, w, h):
    """A light rounded panel. (x, y) is the bottom-left corner."""
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(x, y, w, h, 14, stroke=1, fill=1)


def _header(pdf):
    # Title at 15pt (not the usual 18pt): the full approved
    # title is 363pt wide at 18pt and would run 45pt past
    # the teal rule, which ends at x=552.
    draw_header(pdf, TITLE, SUBTITLE, title_size=15,
                subtitle_size=14)


def _value_line(pdf, x, y, w):
    """A write-in line for a cent amount, with the cent sign
    after it. Returns nothing."""
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(1.2)
    pdf.line(x, y, x + w, y)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(x + w + 4, y, CENT)


def _total_box(pdf, x, y, w=64):
    """A boxed write-in for a total: a line plus cent sign."""
    _value_line(pdf, x, y, w)


# ---------------------------------------------------------------------------
# Page 1 -- Meet the Coins
# Four panels in value order (penny, nickel, dime,
# quarter): big coin, name printed, write the value.
# Then the same four coins in size order (dime, penny,
# nickel, quarter) with smallest/biggest labels and the
# key teaching line: the dime is the smallest coin but
# is worth more than the nickel.
# ---------------------------------------------------------------------------
P1_ORDER = ["penny", "nickel", "dime", "quarter"]
P1_SIZE_ORDER = ["dime", "penny", "nickel", "quarter"]


def _meet_coins(pdf):
    top = _page_title(
        pdf, "Meet the Coins",
        "Say the name of each coin. Write how much it is worth.")
    # Row 1: four panels in value order.
    panel_w, panel_h, gutter = 125, 190, 10.67
    for i, key in enumerate(P1_ORDER):
        px0 = 40 + i * (panel_w + gutter)
        py0 = top - panel_h
        _panel(pdf, px0, py0, panel_w, panel_h)
        cx = px0 + panel_w / 2
        _coin(pdf, key, cx, py0 + 124, 52)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 17)
        pdf.drawCentredString(cx, py0 + 48, COINS[key]["name"])
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawCentredString(cx, py0 + 28, "Worth:")
        _value_line(pdf, cx - 8, py0 + 10, 30)
    # Row 2: size order.
    sy = top - panel_h - 58
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(PAGE_WIDTH / 2, sy + 34,
                          "Coins in order of size, smallest to biggest:")
    xs = [150, 256, 362, 468]
    for key, cx in zip(P1_SIZE_ORDER, xs):
        _coin(pdf, key, cx, sy - 14, 40)
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica", 11)
        pdf.drawCentredString(cx, sy - 66, COINS[key]["name"])
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(150, sy - 86, "smallest")
    pdf.drawCentredString(468, sy - 86, "biggest")
    pdf.setFillColor(NAVY)
    pdf.setFont("Andika-Bold", 15)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, sy - 118,
        "The dime is the smallest coin, but it is worth more than the nickel!")
    _adult_line(pdf, "Adult: Say each coin's name and value together. "
                     "The dime is small but worth more than the nickel.")


def build_p1_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _meet_coins(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 2 -- Match the Coins
# Two matchings. A: coins (left, shuffled) to names
# (right, shuffled). B: coins (left, shuffled) to values
# (right, shuffled). No correct pair sits straight
# across in either matching.
#   A coins: dime, quarter, penny, nickel
#   A names: quarter, penny, nickel, dime
#   B coins: nickel, dime, quarter, penny
#   B values: 25c, 1c, 10c, 5c
# ---------------------------------------------------------------------------
P2_A_COINS = ["dime", "quarter", "penny", "nickel"]
P2_A_NAMES = ["quarter", "penny", "nickel", "dime"]
P2_B_COINS = ["nickel", "dime", "quarter", "penny"]
P2_B_VALUES = [25, 1, 10, 5]


def _match_rows(pdf, top, label, left_coins, right_labels):
    """One matching activity: 4 rows. left_coins are coin
    keys, right_labels are strings. Coins are base 27 with
    55pt row spacing, so neighbouring coins have a clear
    gap. Returns the y just below the last row."""
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, top, label)
    y = top - 46
    for i, (key, lab) in enumerate(zip(left_coins, right_labels)):
        cy = y - i * 55
        _coin(pdf, key, 110, cy, 27)
        pdf.setFillColor(NAVY)
        pdf.setFont("Andika-Bold", 18)
        pdf.drawString(420, cy - 6, lab)
    return y - 3 * 55 - 31


def _match_coins(pdf):
    top = _page_title(
        pdf, "Match the Coins",
        "Draw a line from each coin to its name. Then draw a line to its value.")
    y = _match_rows(pdf, top - 8, "Match the name:",
                    P2_A_COINS, P2_A_NAMES)
    _match_rows(pdf, y - 18, "Match the value:",
                P2_B_COINS,
                ["%d%s" % (v, CENT) for v in P2_B_VALUES])
    _adult_line(pdf, "Adult: Say the coin's name together before your "
                     "child draws the line. Then say its value.")


def build_p2_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _match_coins(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 3 -- Count the Coins
# Five rows of identical coins. Totals grow gradually:
# 3 pennies = 3c, 4 nickels = 20c, 3 dimes = 30c,
# 2 quarters = 50c, 4 quarters = 100c. Each row names
# its counting step.
# ---------------------------------------------------------------------------
P3_ROWS = [
    # coin key, count, counting step, total cents
    ("penny", 3, "Count by 1s", 3),
    ("nickel", 4, "Count by 5s", 20),
    ("dime", 3, "Count by 10s", 30),
    ("quarter", 2, "Count by 25s", 50),
    ("quarter", 4, "Count by 25s", 100),
]


def _count_coins(pdf):
    top = _page_title(
        pdf, "Count the Coins",
        "Count coins that are the same. Write the total.")
    y = top
    for key, count, step, _total in P3_ROWS:
        cy = y - 42
        x = 40
        for _ in range(count):
            _coin(pdf, key, x + _coin_r(32, key) + 4, cy, 32)
            x += 2 * _coin_r(32, key) + 8
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(360, cy - 4, step)
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(452, cy - 6, "=")
        _total_box(pdf, 470, cy - 6, 64)
        y -= 100
    _adult_line(pdf, "Adult: Count aloud together. Count nickels by 5s, "
                     "dimes by 10s, and quarters by 25s.")


def build_p3_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _count_coins(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 4 -- Add Mixed Coins
# Worked example at the top (quarter + dime = 35c), then
# five groups progressing 2, 2, 3, 3, 4 coins. Totals
# 30, 11, 36, 16, 41. Generous working space: each group
# has its own row with room to count.
# ---------------------------------------------------------------------------
P4_EXAMPLE = (["quarter", "dime"], 35)
P4_ROWS = [
    (["quarter", "nickel"], 30),
    (["dime", "penny"], 11),
    (["quarter", "dime", "penny"], 36),
    (["dime", "nickel", "penny"], 16),
    (["quarter", "dime", "nickel", "penny"], 41),
]


def _mixed_row(pdf, keys, cy, total_shown=None, base_r=28,
               steps=False):
    """Draw one mixed-coin row: the coins, then = and a
    write-in total. total_shown prints the answer (example
    only); otherwise the child writes it. steps=True adds a
    "Steps:" write-in line under the row, where the child
    writes the count-on steps (for example 25, 35, 36)."""
    x = 40
    for key in keys:
        r = _coin_r(base_r, key)
        _coin(pdf, key, x + r + 4, cy, base_r)
        x += 2 * r + 12
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(430, cy - 6, "=")
    if total_shown is None:
        _total_box(pdf, 452, cy - 6, 64)
    else:
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(452, cy - 6, "%d%s" % (total_shown, CENT))
    if steps:
        pdf.setFillColor(ADULT_GREY)
        pdf.setFont("Helvetica", 9.5)
        pdf.drawString(40, cy - 40, "Steps:")
        pdf.setStrokeColor(ADULT_GREY)
        pdf.setLineWidth(0.8)
        pdf.line(84, cy - 40, 380, cy - 40)


def _add_mixed(pdf):
    top = _page_title(
        pdf, "Add Mixed Coins",
        "Count the coins from the biggest value to the smallest.\n"
        "Write the total.")
    # Worked example strip.
    _panel(pdf, 40, top - 84, 532, 84)
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(56, top - 22, "Example:")
    _mixed_row(pdf, P4_EXAMPLE[0], top - 50, P4_EXAMPLE[1],
               base_r=22)
    y = top - 84
    for keys, _total in P4_ROWS:
        cy = y - 38
        _mixed_row(pdf, keys, cy, steps=True)
        y -= 84
    _adult_line(pdf, "Adult: Start with the biggest coin. Count on from "
                     "there: 25, then 35.")


def build_p4_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _add_mixed(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 5 -- Make the Amount
# Circle coins to make each amount. Every amount is
# achievable with the coins in its row; two amounts ask
# for two distinct ways, each with its own copy of the
# bank row. All solutions verified:
#   10c, one way:  dime (nickel + 3 pennies cannot reach it)
#   15c, two ways: dime + nickel; nickel + nickel + 5 pennies
#   30c, one way:  quarter + nickel
#   25c, two ways: quarter; dime + nickel + nickel + nickel
# ---------------------------------------------------------------------------
P5_ITEMS = [
    # target cents, ways, bank coins
    (10, 1, ["dime", "nickel", "penny", "penny", "penny"]),
    (15, 2, ["dime", "nickel", "nickel", "penny", "penny",
             "penny", "penny", "penny"]),
    (30, 1, ["quarter", "dime", "nickel", "penny", "penny"]),
    (25, 2, ["quarter", "dime", "nickel", "nickel", "nickel",
             "penny", "penny", "penny", "penny", "penny"]),
]


def _make_amount(pdf):
    top = _page_title(
        pdf, "Make the Amount",
        "Circle the coins to make each amount. Way 1 and Way 2 must be different.")
    # Six bank rows spread across the page: labels 82pt apart,
    # coins base 20, so each row has generous circling room
    # and the page has no unused band at the top or bottom.
    y = top - 41
    for target, ways, bank in P5_ITEMS:
        for w in range(ways):
            label = ("Make %d%s" % (target, CENT)
                     if ways == 1 else
                     "Make %d%s, way %d" % (target, CENT, w + 1))
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(40, y, label)
            x = 40
            for key in bank:
                r = _coin_r(20, key)
                _coin(pdf, key, x + r + 2, y - 28, 20)
                x += 2 * r + 6
            y -= 82
    _adult_line(pdf, "Adult: Way 1 and Way 2 must use different coins. "
                     "If the coins add up to the amount, it is right.")


def build_p5_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _make_amount(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


# ---------------------------------------------------------------------------
# Page 6 -- Money Word Problems
# Four panels (2 x 2). Each has a short story, the coins
# to count, and a write-in answer. The fourth is the
# buying question: Sam has exactly 40c for a 40c ball,
# so the answer is Yes, with no change to make.
#   1. Mia: 2 dimes + 3 pennies = 23c
#   2. Ben: 1 quarter + 1 nickel = 30c
#   3. Lily: 3 nickels = 15c
#   4. Sam: quarter + dime + nickel = 40c, ball costs 40c
# ---------------------------------------------------------------------------
P6_ITEMS = [
    ("Mia has 2 dimes and 3 pennies.\nHow many cents does she have?",
     ["dime", "dime", "penny", "penny", "penny"], "cents"),
    ("Ben has 1 quarter and 1 nickel.\nHow many cents does he have?",
     ["quarter", "nickel"], "cents"),
    ("Lily has 3 nickels.\nHow many cents does she have?",
     ["nickel", "nickel", "nickel"], "cents"),
    ("A ball costs 40 cents.\nSam has these coins.\nCan Sam buy the ball?",
     ["quarter", "dime", "nickel"], "yesno"),
]


def _word_problems(pdf):
    top = _page_title(
        pdf, "Money Word Problems",
        "Read each story. Count the coins. Write how many cents.")
    panel_w, panel_h, gutter = 250, 230, 32
    for i, (story, keys, kind) in enumerate(P6_ITEMS):
        col, row = i % 2, i // 2
        px0 = 40 + col * (panel_w + gutter)
        py0 = top - row * 246 - panel_h
        _panel(pdf, px0, py0, panel_w, panel_h)
        pdf.setFillColor(NAVY)
        # Story at 14pt: 14.5pt would run past the panel
        # (the longest line is 219pt wide at 14.5pt, the
        # panel's inner width is 218pt).
        pdf.setFont("Andika-Bold", 14)
        sy = py0 + 198
        for line in story.split("\n"):
            pdf.drawString(px0 + 16, sy, line)
            sy -= 18
        x = px0 + 16
        if kind == "cents":
            cy = py0 + 104
            for key in keys:
                r = _coin_r(24, key)
                _coin(pdf, key, x + r + 2, cy, 24)
                x += 2 * r + 6
            _value_line(pdf, px0 + 16, py0 + 36, 60)
        else:
            cy = py0 + 118
            for key in keys:
                r = _coin_r(24, key)
                _coin(pdf, key, x + r + 2, cy, 24)
                x += 2 * r + 6
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(px0 + 16, py0 + 68, "Sam has")
            _value_line(pdf, px0 + 80, py0 + 68, 48)
            pdf.setFillColor(NAVY)
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawString(px0 + 16, py0 + 32, "Circle one:")
            for j, word in enumerate(["Yes", "No"]):
                bx = px0 + 112 + j * 74
                pdf.setStrokeColor(TEAL)
                pdf.setLineWidth(1.5)
                pdf.roundRect(bx, py0 + 16, 64, 32, 16, stroke=1, fill=0)
                pdf.setFillColor(TEAL)
                pdf.setFont("Helvetica-Bold", 15)
                pdf.drawCentredString(bx + 32, py0 + 27, word)
    _adult_line(pdf, "Adult: Read the story together. Count the coins from "
                     "the biggest value down.")


def build_p6_page(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _header(pdf)
    _word_problems(pdf)
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


PAGES = [
    ("Meet the Coins", build_p1_page),
    ("Match the Coins", build_p2_page),
    ("Count the Coins", build_p3_page),
    ("Add Mixed Coins", build_p4_page),
    ("Make the Amount", build_p5_page),
    ("Money Word Problems", build_p6_page),
]


# ---------------------------------------------------------------------------
# Parent guide (separate one-page PDF, NOT in the student
# bundle). Plain language for parents, no standards codes.
# ---------------------------------------------------------------------------
GUIDE_TITLE = "How to Use This Pack"
GUIDE_INTRO = [
    "Your child learns the four coins, what each one is",
    "worth, and how to count and add them. Coin work is",
    "formally taught in Grade 2, so this pack introduces",
    "it early in a Grade 1 way.",
]


def _guide_header(pdf):
    """Brand header for the parent guide, WITHOUT the Name/Date
    fields: the guide is for adults, not a student page. This
    replicates draw_header minus the Name/Date block; the shared
    draw_header (and build_phonics_az.py) is untouched, and
    student pages keep their Name/Date fields."""
    pdf.setFillColor(TEAL)
    pdf.rect(0, PAGE_HEIGHT - 14, PAGE_WIDTH, 14, stroke=0, fill=1)
    draw_logo(pdf, 60, PAGE_HEIGHT - 86)
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1)
    pdf.line(218, PAGE_HEIGHT - 88, 218, PAGE_HEIGHT - 48)
    pdf.setFillColor(TEAL)
    # Title at 15pt, matching the student header: at 18pt
    # the full title would run past the teal rule.
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(234, PAGE_HEIGHT - 68, TITLE)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(234, PAGE_HEIGHT - 90, "Parent Guide")
    pdf.setStrokeColor(TEAL)
    pdf.setLineWidth(1.6)
    pdf.line(60, PAGE_HEIGHT - 104, PAGE_WIDTH - 60,
             PAGE_HEIGHT - 104)


GUIDE_SECTIONS = [
    ("The four coins", [
        "Penny: 1 cent. Nickel: 5 cents. Dime: 10 cents. "
        "Quarter: 25 cents. The dime is the smallest coin, "
        "but it is worth more than the nickel. The quarter "
        "is the biggest coin.",
    ]),
    ("How to help", [
        "Say the coin's name and value together.",
        "Count from the biggest value down: quarters, then "
        "dimes, then nickels, then pennies.",
        "Count aloud by 5s, 10s, and 25s. Let your child "
        "handle real coins from a jar.",
        "On Page 5, Way 1 and Way 2 must use different coins. "
        "If the coins add up to the amount, it is right.",
    ]),
    ("Answers", [
        "Page 1: penny 1 cent, nickel 5 cents, dime 10 cents, "
        "quarter 25 cents.",
        "Page 2: dime to dime, quarter to quarter, penny to "
        "penny, nickel to nickel; nickel to 5 cents, dime to "
        "10 cents, quarter to 25 cents, penny to 1 cent.",
        "Page 3: 3 cents, 20 cents, 30 cents, 50 cents, "
        "100 cents.",
        "Page 4: 30 cents, 11 cents, 36 cents, 16 cents, "
        "41 cents.",
        "Page 5: 10 cents: one dime. 15 cents: dime and nickel, "
        "or two nickels and five pennies. 30 cents: quarter and "
        "nickel. 25 cents: one quarter, or dime and three nickels.",
        "Page 6: 23 cents, 30 cents, 15 cents, Yes.",
    ]),
    ("If your child finds it hard", [
        "Start with pennies and nickels only. Count real coins.",
        "Practice one page at a time. The dime is the tricky "
        "one, because it is small but worth 10 cents.",
    ]),
]
# Guide body is 12.5pt Helvetica; each item is wrapped at
# 74 characters, which fits the 516pt text width.
GUIDE_WRAP = 74


def build_parent_guide(path):
    pdf = canvas.Canvas(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    _guide_header(pdf)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(PAGE_WIDTH / 2, 640, GUIDE_TITLE)
    pdf.setFillColor(PANEL_FILL)
    pdf.setStrokeColor(PANEL_STROKE)
    pdf.setLineWidth(1)
    pdf.roundRect(40, 542, 532, 84, 14, stroke=1, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica", 12.5)
    y = 606
    for line in GUIDE_INTRO:
        pdf.drawString(56, y, line)
        y -= 16
    y = 526
    for heading, items in GUIDE_SECTIONS:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 13.5)
        pdf.drawString(40, y, heading)
        y -= 17
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica", 12.5)
        for item in items:
            for line in textwrap.wrap(item, GUIDE_WRAP):
                pdf.drawString(56, y, line)
                y -= 15
        y -= 9
    pdf.setFillColor(ADULT_GREY)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        PAGE_WIDTH / 2, 58,
        "Grade 1 Math: Coins and Money. "
        "For parents, not for the child.")
    draw_footer(pdf)
    pdf.showPage()
    pdf.save()


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _build_bundle(bundle_path):
    """The 6 student pages in one PDF."""
    pdf = canvas.Canvas(bundle_path,
                        pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    for title, builder in PAGES:
        _header(pdf)
        # Reuse each page builder's content function by
        # rebuilding on this canvas: builders are split so
        # the content step is callable separately.
        _draw_page_content(pdf, title)
        draw_footer(pdf)
        pdf.showPage()
    pdf.save()


def _draw_page_content(pdf, title):
    if title == "Meet the Coins":
        _meet_coins(pdf)
    elif title == "Match the Coins":
        _match_coins(pdf)
    elif title == "Count the Coins":
        _count_coins(pdf)
    elif title == "Add Mixed Coins":
        _add_mixed(pdf)
    elif title == "Make the Amount":
        _make_amount(pdf)
    elif title == "Money Word Problems":
        _word_problems(pdf)
    else:
        raise ValueError("unknown page %r" % title)


def main():
    from pypdf import PdfReader, PdfWriter
    os.makedirs(OUT_DIR, exist_ok=True)
    bundle = os.path.join(OUT_DIR, "coins-and-money.pdf")
    guide = os.path.join(OUT_DIR,
                         "coins-and-money-parent-guide.pdf")
    review = os.path.join(OUT_DIR, "coins-and-money-review.pdf")
    _build_bundle(bundle)
    build_parent_guide(guide)
    writer = PdfWriter()
    for src in (bundle, guide):
        for page in PdfReader(src).pages:
            writer.add_page(page)
    with open(review, "wb") as f:
        writer.write(f)
    # Individual per-page PDFs, split losslessly from the final
    # bundle (pypdf copies each page object verbatim, so the
    # vector text and the high-resolution coin images are
    # identical to the combined pack). Never build these from
    # the raster preview PNGs.
    page_names = ["meet-the-coins", "match-the-coins",
                  "count-the-coins", "add-mixed-coins",
                  "make-the-amount", "money-word-problems"]
    bundle_pages = PdfReader(bundle).pages
    for i, slug in enumerate(page_names):
        single = PdfWriter()
        single.add_page(bundle_pages[i])
        single_path = os.path.join(
            OUT_DIR, "coins-and-money-p%d-%s.pdf" % (i + 1, slug))
        with open(single_path, "wb") as f:
            single.write(f)
    for name in ["coins-and-money.pdf",
                 "coins-and-money-parent-guide.pdf",
                 "coins-and-money-review.pdf",
                 "coins-and-money-p1-meet-the-coins.pdf",
                 "coins-and-money-p2-match-the-coins.pdf",
                 "coins-and-money-p3-count-the-coins.pdf",
                 "coins-and-money-p4-add-mixed-coins.pdf",
                 "coins-and-money-p5-make-the-amount.pdf",
                 "coins-and-money-p6-money-word-problems.pdf"]:
        path = os.path.join(OUT_DIR, name)
        print("%s %d bytes sha256 %s"
              % (name, os.path.getsize(path), _sha256(path)))
    # No em dash or en dash anywhere in the pack's text.
    for name in ["coins-and-money.pdf",
                 "coins-and-money-parent-guide.pdf"]:
        text = "".join(
            (p.extract_text() or "")
            for p in PdfReader(os.path.join(OUT_DIR, name)).pages)
        assert "\u2014" not in text, "em dash in %s" % name
        assert "\u2013" not in text, "en dash in %s" % name
    print("em dash check: clean")


if __name__ == "__main__":
    main()
