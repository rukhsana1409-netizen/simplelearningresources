# Handoff — Number Words 1–10 (Kindergarten Math, supplemental)

Final approved bundle for Codex. Both pages user-approved and locked
2026-10-08. Nothing was changed for this handoff — the builder is frozen with
all pages flagged `locked=True`; the PDF below is the finalization build from
that locked source, re-rendered at 150 dpi and confirmed pixel-identical
(MD5 match) to every approved review image.

Scope note: this is a small SUPPLEMENTAL resource, deliberately stopped at
1–10. Number words are not a direct RCS/CCSS Kindergarten requirement
(K.CC.A.3 covers numerals; number words enter formally in Grade 2). No
11–20/teen pages were built, per the user's explicit direction.

Concept: connect numerals 1–10 with their written number words — read, then
trace, then write (P1); then pure recognition (P2). Standard Learning Made
Simple header/footer with the canonical `generate_worksheet.py::draw_logo`
lockup (verbatim copy) on both pages.

## Contents

| File | Description |
|---|---|
| `worksheets/kindergarten/math/number-words-1-20/number-words-1-20-review.pdf` | **Final 2-page PDF**. The "-review" in the name is historical only. (Directory name retained for continuity.) |
| `worksheets/kindergarten/math/number-words-1-20/number-words-1-20-page-01.pdf`, `-page-02.pdf` | Individual page PDFs, extracted from the final bundle. |
| `worksheet-generator/build_number_words.py` | Builder source (reportlab; both pages `locked=True`). Tracing letters are hand-built single-stroke dashed vector paths — no tracing font required at build time. |
| `worksheet-generator/assets/fonts/Andika-Regular.ttf`, `Andika-Bold.ttf` | Printed-word font (SIL Open Font License). |
| `tmp/handoffs/number-words/HANDOFF.md` | This file. |
| `tmp/handoffs/number-words/nw-p1.png`, `nw-p2.png` | Approved review images (150 dpi renders), one per page. |

## Verification (2026-10-08)

- MD5: `e25f2446d83beade4f5e16aa8cb0f076`
- SHA-256: `c1af99d7df9175d98251ff59a8ca85e9108fea8c0d58dbfc627768228f057ef1`
- 2 pages, US Letter (612×792pt). No clipping or overlap; all words,
  choices, and guide lines within safe print margins.
- Both pages re-rendered at 150 dpi and confirmed pixel-identical (MD5
  match) to their approved review images, in correct page order.
- Canonical `generate_worksheet.py::draw_logo` lockup on both pages.
- P1 "Number Words" (Numbers 1–10): "Read the number word. Trace it. Write
  it." — one column, 10 rows: large numeral | large printed word
  (Andika-Bold, capitalized) | dashed single-stroke tracing word on light
  full-width handwriting guide strips with blank write-it space after.
  Corrected manuscript lowercase 'e' used in every occurrence.
- P2 "Which Number Word?": "Circle the correct number word." — 6 spacious
  rows (numerals 1, 3, 4, 6, 8, 10), 3 large word choices each, correct
  positions varied (middle, first, middle, last, last, middle). No tracing,
  no handwriting lines, no pictures.

## Page order

1. **Number Words** (subtitle "Numbers 1–10") — read, trace & write.
2. **Which Number Word?** — circle the correct number word (recognition).
