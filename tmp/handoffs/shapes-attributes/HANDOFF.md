# Handoff — Shapes & Their Attributes (Kindergarten Math)

Final approved bundle for Codex. All 4 pages user-approved and locked 2026-10-07.
Nothing was changed for this handoff — the builder is frozen with all pages
flagged `locked=True`; the PDF below is the finalization build from that
locked source, re-rendered at 110 dpi and confirmed pixel-identical (MD5 match)
to every approved review image.

Concept: defining attributes of shapes. Progression: triangle attributes +
identification (P1) → squares/rectangles identification (P2) → color/size/
direction don't change shape type (P3) → draw shapes from attributes (P4).
All shapes are vector-drawn (reportlab) for mathematical accuracy — no image
assets. Standard Learning Made Simple header/footer with the canonical
`generate_worksheet.py::draw_logo` lockup (verbatim copy) on all 4 pages.

## Contents

| File | Description |
|---|---|
| `worksheets/kindergarten/math/shapes-attributes/shapes-attributes-review.pdf` | **Final 4-page PDF** (14,140 bytes). The "-review" in the name is historical only. |
| `worksheets/kindergarten/math/shapes-attributes/shapes-attributes-page-01.pdf` … `-page-04.pdf` | Individual page PDFs, extracted from the final bundle. |
| `worksheet-generator/build_shapes_attributes.py` | Builder source (reportlab, pure vector; all 4 pages `locked=True`). No image assets required. |
| `tmp/handoffs/shapes-attributes/HANDOFF.md` | This file. |
| `tmp/handoffs/shapes-attributes/sa-p1.png` … `sa-p4.png` | Approved review images (110 dpi renders), one per page. |

## Verification (2026-10-07)

- MD5: `7860570ee4b63985f98d001d5ac6cf1b`
- SHA-256: `32d04b1e349492798f6615ebc44e2b00b8449a193d59abd04ae4e2e4f8407b7e`
- 4 pages, US Letter (612×792pt). No clipping or overlap; all panels, shapes,
  prompts, answer areas, and drawing boxes within safe print margins.
- All 4 pages re-rendered at 110 dpi and confirmed pixel-identical (MD5 match)
  to their approved review images.
- Canonical `generate_worksheet.py::draw_logo` lockup verified on all 4 pages
  (pixel-compared against the approved Addition Within 5 header).
- P1: Learn (3 triangles: upright/rotated/small; shared attribute strip: 3
  straight sides, 3 corners, closed shape) + Find the Triangles (8 shapes:
  4 true triangles varied; distractors = trapezoid, open 3-sided shape,
  curved-side shape, pentagon).
- P2: Find the Squares (3 true squares incl. rotated; distractors = rectangle,
  non-square rhombus, irregular quad) + Find the Rectangles (3 elongated
  rectangles incl. vertical and tilted; distractors = trapezoid,
  parallelogram, pentagon).
- P3: Color Can Change (3 triangles, 3 colors) · Size Can Change (3 teal
  squares: small/medium/large) · Direction Can Change (horizontal/vertical/
  rotated rectangles, all with 4 right angles). All prompts answer Yes.
  Takeaway box preserved.
- P4: Build & Draw Shapes — triangle (3 sides, 3 corners, closed), rectangle
  (4 sides, 4 corners, 4 square corners, closed), shape challenge (4 straight
  sides, 4 corners, all sides the same length → square). Large blank drawing
  boxes; nothing pre-drawn.

## Page order

1. **What Makes a Triangle?** (subtitle "Shapes & Their Attributes") — Learn +
   "Circle all the triangles."
2. **Which Shapes Belong?** — "Circle all the squares." + "Circle all the
   rectangles."
3. **What Can Change?** — "Are they all triangles/squares/rectangles?"
   Yes/No bubbles + takeaway box.
4. **Build & Draw Shapes** — draw from defining-attribute clues.
