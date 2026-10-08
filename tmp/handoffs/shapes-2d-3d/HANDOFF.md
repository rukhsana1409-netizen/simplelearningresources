# Handoff — 2D & 3D Shapes (Kindergarten Math)

Final approved bundle for Codex. All three pages user-approved and locked
2026-10-08. Nothing was changed for this handoff — the builder is frozen with
all pages flagged `locked=True`; the PDF below is the finalization build from
that locked source, re-rendered at 110 dpi and confirmed pixel-identical
(MD5 match) to every approved review image.

Concept: distinguish flat (2D) from solid (3D) shapes, connect real-world
objects to 3D shapes, then recognize 3D shapes across sizes/orientations.
Progression: flat-vs-solid classification (P1) → real-world 3D recognition
(P2) → orientation/size-invariant 3D naming (P3). Standard Learning Made
Simple header/footer with the canonical `generate_worksheet.py::draw_logo`
lockup (verbatim copy) on all pages.

## Contents

| File | Description |
|---|---|
| `worksheets/kindergarten/math/shapes-2d-3d/shapes-2d-3d-review.pdf` | **Final 3-page PDF**. The "-review" in the name is historical only. |
| `worksheets/kindergarten/math/shapes-2d-3d/shapes-2d-3d-page-01.pdf` … `-page-03.pdf` | Individual page PDFs, extracted from the final bundle. |
| `worksheet-generator/build_2d_3d_shapes.py` | Builder source (reportlab, pure vector; all pages `locked=True`). |
| `worksheet-generator/assets/shapes-2d-3d/obj-{ball,block,can,partyhat,box}.jpg` | Page 2 object illustrations (JPEG embeds). |
| `tmp/handoffs/shapes-2d-3d/HANDOFF.md` | This file. |
| `tmp/handoffs/shapes-2d-3d/s23d-p1.png` … `s23d-p3.png` | Approved review images (110 dpi renders), one per page. |

## Verification (2026-10-08)

- MD5: `f05f0512dddfb942ef0958c2ca41a91f`
- SHA-256: `e2a6a6375927c7f13157e34a621893f1f107ae76473aa7dbe4265af15f0a3bc0`
- 3 pages, US Letter (612×792pt). No clipping or overlap; all shapes,
  choices, and labels within safe print margins.
- All three pages re-rendered at 110 dpi and confirmed pixel-identical
  (MD5 match) to their approved review images.
- Canonical `generate_worksheet.py::draw_logo` lockup on all pages.
- P1 "Flat or Solid?": FLAT SHAPES (circle, triangle, square — truly flat,
  "Flat like paper.") beside SOLID SHAPES (volumetric shaded sphere, cube,
  strong cylinder, "Solid like blocks."); small name labels under each
  reference shape; Practice "Is the shape flat or solid? Circle the answer."
  — 6 large items (triangle, sphere, square, cylinder, circle, cube) with
  ○ Flat / ○ Solid choices, no name labels on practice items.
- P2 "3D Shapes Around Us": compact reference row of five named geometric
  shapes (sphere, cube, cylinder, cone, rectangular prism); Practice "What
  3D shape is it like? Circle the answer." — 5 illustrated objects on white
  photo cards (ball→sphere, toy block→cube, can→cylinder, party
  hat→cone, cardboard parcel→rectangular prism), each with 2 written
  shape choices.
- P3 "Find the 3D Shapes": three find-and-circle sections with 6 unlabeled
  geometric shapes each — "Find all the cones." (3 cones, varied sizes/
  tilts), "Find all the cylinders." (3 cylinders, incl. clearly tilted),
  "Find all the rectangular prisms." (3 prisms, clearly different
  proportions, incl. rotated); sphere and cube used as distractors.

## Page order

1. **Flat or Solid?** (subtitle "2D & 3D Shapes") — reference groups +
   flat/solid classification.
2. **3D Shapes Around Us** — reference row + real-world object matching.
3. **Find the 3D Shapes** — find the target 3D shape across sizes and
   orientations.
