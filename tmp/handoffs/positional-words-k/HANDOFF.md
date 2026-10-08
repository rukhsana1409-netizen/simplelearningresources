# Handoff — Positional Words (Kindergarten Math, K.G.A.1)

Final approved bundle for Codex. All four pages user-approved and locked
2026-10-08. Nothing was changed for this handoff — the builder is frozen with
all pages flagged `locked=True`; the PDF below is the finalization build from
that locked source, re-rendered at 150 dpi and confirmed pixel-identical
(MD5 match) to every approved review image.

K.G.A.1: describe objects in the environment using names of shapes and
positional/relative-position words. This pack is a genuine Kindergarten
progression from the Preschool Positional Words pack (which used everyday
objects and recognition-only tasks): shapes are the subjects, tasks require
completing positional statements and following spatial directions, and it
introduces the new terms beside, in front of, and behind.

Concept: shape vocabulary fused with positional language — example, then
complete-the-statement, then follow-the-direction drawing tasks.
Pure-vector builder; canonical `generate_worksheet.py::draw_logo` lockup
(verbatim copy) on every page.

## Contents

| File | Description |
|---|---|
| `worksheets/kindergarten/math/positional-words-k/positional-words-k-review.pdf` | **Final 4-page PDF**. The "-review" in the name is historical only. |
| `worksheets/kindergarten/math/positional-words-k/positional-words-k-page-01.pdf` … `-page-04.pdf` | Individual page PDFs, extracted from the final bundle. |
| `worksheet-generator/build_positional_words_k.py` | Builder source (reportlab; all pages `locked=True`). |
| `tmp/handoffs/positional-words-k/HANDOFF.md` | This file. |
| `tmp/handoffs/positional-words-k/pwk-p1.png` … `pwk-p4.png` | Approved review images (150 dpi renders), one per page. |

## Verification (2026-10-08)

- MD5: `b0f63d8db845f59183f0a77b14f25e45`
- SHA-256: `11bf7771c104f853373ccdf6ed6044e8b5ccb3e6b68e9dca1274d87f5b7ce778`
- 4 pages, US Letter (612×792pt). No clipping or overlap; all shapes,
  sentences, choices, and drawing areas within safe print margins.
- All 4 pages re-rendered at 150 dpi and confirmed pixel-identical (MD5
  match) to their approved review images, in correct page order.
- Canonical `generate_worksheet.py::draw_logo` lockup on every page.
- Answer logic verified against every illustration:
  - P1: circle above square → "above"; hexagon below triangle → "below";
    draw triangle below circle / square above circle.
  - P2: triangle beside rectangle → "beside" (distractor "above"); circle
    beside hexagon → "beside" (distractor "below"); draw circle beside
    square / triangle next to circle.
  - P3: circle behind square → "behind"; hexagon in front of triangle →
    "in front of"; draw circle behind square / triangle in front of
    rectangle. Approved overlap relationships preserved (front shape
    clearly covers a portion of the back shape; both shapes recognizable).
  - P4: true sentences — circle above square; hexagon beside circle;
    triangle behind rectangle; 3-step draw (circle above square, triangle
    beside circle, hexagon below square).

## Page order

1. **Above & Below** — example + complete the sentence + follow the direction.
2. **Beside / Next To** — "Beside means next to." bridge; same structure.
3. **In Front Of & Behind** — overlap-based depth; same structure.
4. **Where Is It?** — mixed review: circle the true sentence (3 items) +
   3-step follow-the-directions drawing task.
