# Handoff — Compare Length & Height (Kindergarten Math)

Final approved bundle for Codex. All 7 pages user-approved and locked 2026-10-06.
Nothing was changed for this handoff — files are exact copies of the approved finals.

Concept: non-standard measurement progression — compare length/height visually
(P1–P2) → measure height with equal blocks (P3) → compare measured heights (P4)
→ measure length with blocks, compare, and draw (P5) → order by length (P6) →
order by height (P7). All artwork is original vector ReportLab; no image assets.
Equal counting blocks are 16×16pt with 2pt gaps throughout; every measured
object is sized to an exact whole number of blocks
(object size = n × 18 − 2pt, top of object = top of final block), verified by
build-time assertions. No rulers, inches, or centimeters anywhere.

## Contents

| File | Description |
|---|---|
| `worksheets/kindergarten/math/compare-length-height/compare-length-height-review.pdf` | **Final 7-page PDF** (34,479 bytes). The "-review" in the name is historical only. |
| `worksheet-generator/build_compare_length.py` | Builder source (reportlab, pure vector). All 7 pages flagged `locked=True`. |
| `tmp/handoffs/compare-length-height/HANDOFF.md` | This file. |
| `tmp/handoffs/compare-length-height/clh-p1.png` … `clh-p7.png` | Approved review images (110 dpi renders), one per page. |

## Verification (2026-10-06)

- MD5: `18e7f19108966031b6957047d63253d6`
- SHA-256: `350be8682ac785781d5bcbac986c835bfebefeb824ddd34f87d5f0590778e44d`
- All 7 pages re-rendered at 110 dpi and confirmed pixel-identical (SHA-256 match)
  to their approved review images. All 7 pages flagged locked in the builder.
- All 7 pages US Letter (612×792pt), standard Learning Made Simple header/footer,
  pure vector, standard PDF fonts (print-safe).
- Measurement invariants re-verified from the builder data: P3 6/6, P4 12/12,
  P5 measure/compare problems all hold (object size = n × 18 − 2).

## Page order and answer key

1. **Longer or Shorter?** — "Look at each pair. Circle the longer or shorter
   object." 6 rows; same object twice per pair, length the only difference,
   shared baseline. Correct: longer worm (L) · shorter pencil→crayon (R) ·
   longer scarf (R) · shorter toothbrush (L) · longer train (R) ·
   shorter ruler (L).
2. **Taller or Shorter?** (subtitle "Compare Height") — "Look at each pair.
   Circle the taller or shorter one." 6 rows; same object twice per pair,
   shared baseline. Correct: taller tree (L) · shorter building (R) ·
   taller candle (R) · shorter bottle (L) · taller flower (R) ·
   shorter ladder (L).
3. **Measure the Height** (subtitle "Measure with Blocks") — "Count the blocks.
   Write the height." 6 problems (2×3): upright object + equal-block column on
   a shared ground line, column top = object top, large answer box + "blocks".
   Answers: flower 2 · glue bottle 3 · crayon 4 · pencil 5 · water bottle 6 ·
   toy rocket 7.
4. **Compare the Heights** (subtitle "Measure with Blocks") — "Count the blocks.
   Circle the taller object." 6 problems (2×3): two objects, each with its own
   block column, one shared baseline per problem; no counts printed. Correct:
   marker 4 (R) · rocket 7 (L) · water bottle 6 (R) · pencil 7 (L) ·
   pencil 6 (R) · water bottle 8 (L).
   Problems: flower 2/marker 4 · rocket 7/spoon 3 · book 4/bottle 6 ·
   pencil 7/mug 3 · toothbrush 3/pencil 6 · bottle 8/ice cream 5.
5. **Measure the Length** (subtitle "Measure with Blocks") — "Measure length
   with blocks." Mixed: 3× "How many blocks long?" (crayon 3 · toothbrush 5 ·
   pencil 7, answer box + "blocks"); 2× "Circle the longer object."
   (paintbrush 6 over spoon 3 → top; toothbrush 4 over pencil 7 → bottom);
   1× "Draw something 5 blocks long." (5-block reference row + dashed drawing
   area, open-ended).
6. **Order by Length** (subtitle "Shortest to Longest") — "Number the objects:
   1 = shortest, 2 = middle, 3 = longest." 5 panels × 3 same-design objects in
   mixed order, common baseline, large number boxes. Answers: pencils 2,1,3 ·
   crayons 3,1,2 · ribbons 1,3,2 · buses 2,3,1 · paintbrushes 3,2,1.
7. **Order by Height** (subtitle "Shortest to Tallest") — "Number the objects:
   1 = shortest, 2 = middle, 3 = tallest." 4 large panels × 3 same-design
   objects in mixed order, one clearly visible common baseline, large number
   boxes. Only height varies within a set. Answers: trees 2,3,1 ·
   flowers 1,3,2 · rockets 3,1,2 · pencils 2,1,3.

## Notes for Codex

- Do NOT alter any locked page. Do not merge to main, publish, or deploy
  without the user's separate explicit authorization.
- Do not integrate into `directory.js` or the website without the user's
  separate explicit authorization.
- Pack slug suggestion: `compare-length-height` under
  `worksheets/kindergarten/math/` (already the PDF's location).
