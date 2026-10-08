# Handoff — Building with 3D Shapes (Kindergarten Math)

Final approved bundle for Codex. Both pages user-approved and locked
2026-10-07/08. Nothing was changed for this handoff — the builder is frozen
with all pages flagged `locked=True`; the PDF below is the finalization build
from that locked source, re-rendered at 110 dpi and confirmed pixel-identical
(MD5 match) to every approved review image.

Concept: composing/decomposing simple 3D structures. Progression: identify
the 3D shapes used to build a structure (P1) → determine the missing 3D
shape in a structure (P2). Shapes used: cube, rectangular prism, cone only
(cylinder deliberately excluded from this pack; flat-vs-solid, sphere, and
broader 3D identification are reserved for a separate dedicated resource).
All shapes are vector-drawn (reportlab) front/top/side faces — no image
assets. Standard Learning Made Simple header/footer with the canonical
`generate_worksheet.py::draw_logo` lockup (verbatim copy) on both pages.

## Contents

| File | Description |
|---|---|
| `worksheets/kindergarten/math/building-3d-shapes/building-3d-shapes-review.pdf` | **Final 2-page PDF**. The "-review" in the name is historical only. |
| `worksheets/kindergarten/math/building-3d-shapes/building-3d-shapes-page-01.pdf`, `-page-02.pdf` | Individual page PDFs, extracted from the final bundle. |
| `worksheet-generator/build_3d_shapes.py` | Builder source (reportlab, pure vector; both pages `locked=True`). No image assets required. |
| `tmp/handoffs/building-3d-shapes/HANDOFF.md` | This file. |
| `tmp/handoffs/building-3d-shapes/b3d-p1.png`, `b3d-p2.png` | Approved review images (110 dpi renders), one per page. |

## Verification (2026-10-08)

- MD5: `45a0f0cd73ea81fbc6a4f21dd1341759`
- SHA-256: `5ac52c7b85142d276866ba72a1eba0a03eb78f55973f9d222f5409115d7259a2`
- 2 pages, US Letter (612×792pt). No clipping or overlap; all structures,
  choices, and labels within safe print margins.
- Both pages re-rendered at 110 dpi and confirmed pixel-identical (MD5 match)
  to their approved review images.
- Canonical `generate_worksheet.py::draw_logo` lockup on both pages
  (same verbatim implementation as the pack's Page 1 approval).
- P1: reference strip (cube, rectangular prism, cone — enlarged, 12.5pt
  labels); Example: stairs from 1 rectangular prism + 2 cubes beside
  "These shapes can build the structure."; Practice "Look at each structure.
  Circle the shapes used to build it." — house→prism & cone, table→cube &
  prism, tower→cone & cube.
- P2: "Look at the structure. What shape is missing? Circle it." —
  complete/incomplete structure pairs with simplified dashed missing-piece
  guides; A/B/C individual choice cards; answers B (cube), A (cone),
  C (cube).

## Page order

1. **What Shapes Built It?** (subtitle "Building with 3D Shapes") — reference
   strip + Example + "Circle the shapes used to build it."
2. **What Shape Is Missing?** — "What shape is missing? Circle it."
