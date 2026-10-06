# Handoff — Compare Weight (Kindergarten Math)

Final approved bundle for Codex. All 5 pages user-approved and locked 2026-10-06.
Nothing was changed for this handoff — the builder is frozen with all pages
flagged `locked=True`; the PDF below is the finalization build from that
locked source.

Concept: qualitative weight comparison only — heavier/lighter, ordering, and
reading balance scales. No pounds, ounces, kilograms, numerical weight
measurement, or weight arithmetic anywhere. Progression: Heavy or Light?
(P1, circle heavier/lighter) → Order by Weight (P2, number 1-2-3) → Balance
Scale Detective (P3, read a tilted scale) → Think About Weight (P4, combine
two scale clues transitively) → Weight Challenge (P5, mixed review + drawing).
Illustrations: storybook-realistic educational watercolor (style reference
`worksheet-generator/assets/animal-library/lib-calf.png`), white cards on
tinted panels, standard Learning Made Simple header/footer. Balance scales are
vector-drawn, mechanically consistent: vertical hangers, 16° tilt (20° on the
small P4 clue scales), lower side = heavier.

## Contents

| File | Description |
|---|---|
| `worksheets/kindergarten/math/compare-weight/compare-weight-review.pdf` | **Final 5-page PDF** (12,362,907 bytes). The "-review" in the name is historical only. |
| `worksheet-generator/build_compare_weight.py` | Builder source (reportlab + approved JPG assets in `worksheet-generator/assets/compare-weight/`). All 5 pages flagged `locked=True`. |
| `tmp/handoffs/compare-weight/HANDOFF.md` | This file. |
| `tmp/handoffs/compare-weight/cw-p1.png` … `cw-p5.png` | Approved review images (110 dpi renders), one per page. |

## Verification (2026-10-06)

- MD5: `086948dd3231f707becf608edf664172`
- SHA-256: `52e57c5666cc9944a91e921bec16b7827678da27b88eba064008d089257ce4b1`
- 5 pages, US Letter (612×792pt). No clipping or overlap on any page;
  all instructions, number boxes, answer pills, and drawing boxes verified.
- Pages 2–5 re-rendered at 110 dpi and confirmed pixel-identical (MD5 match)
  to their approved review images. Page 1 is visually identical to its
  approved review image; a sub-visible anti-aliasing-level difference in the
  illustration regions (mean abs diff ~1.2/255, invisible side-by-side) dates
  from before this session's work — the approved `cw-p1.png` is preserved
  above as the record and was not overwritten.
- All weight/order answers re-verified (see key below); every balance-scale
  tilt direction matches its intended answer (lower = heavier); P4's two-clue
  chains are consistent (A>B, B>C); P5 ordering feather=1, soccer ball=2,
  chair=3; P5 book lower/heavier than balloon.

## Page order and answer key

1. **Heavy or Light?** (subtitle "Compare Weight") — "Look at each pair.
   Circle the heavier or lighter object." 5 tinted rows; prompt word colored
   (heavier = red, lighter = orange). Correct: watermelon heavier (L) ·
   pencil lighter (R) · book heavier (R) · leaf lighter (L) · brick
   heavier (L).
2. **Order by Weight** (subtitle "Compare Weight") — "Number the objects:
   1 = lightest, 2 = middle, 3 = heaviest." 4 tinted rows × 3 objects,
   number box under each. Correct: bicycle/feather/apple → 3,1,2 ·
   paper clip/suitcase/book → 1,3,2 · shoe/leaf/chair → 2,1,3 ·
   watermelon/orange/pencil → 3,2,1.
3. **Balance Scale Detective** (subtitle "Compare Weight") — teaching panel:
   "Lower side = heavier. Higher side = lighter." (apple lower, feather
   higher). 4 large scales (2×2). Correct: apple heavier (L) · ball
   lighter (L) · book heavier (R) · hat lighter (R). Object pairs are
   deliberately ambiguous so the scale is the only evidence.
4. **Think About Weight** (subtitle "Compare Weight") — "Use both scales.
   Circle the answer." 4 problems (2×2); each shows two small clue scales
   ordering three objects; 3 picture answer cards below. Correct:
   apple>orange>strawberry, heaviest → apple (3rd) · book>block>ball,
   lightest → ball (1st) · teddy>hat>mitten, heaviest → teddy (2nd) ·
   shoe>pencil>paperclip, lightest → paperclip (1st).
5. **Weight Challenge** (subtitle "Compare Weight") — final review. Order by
   Weight: chair/feather/soccer ball → 3,1,2 (feather=1, soccer ball=2,
   chair=3). Balance Scale: book lower/heavier than balloon, "Which is
   heavier?" → book (pills: book/balloon). Draw: "Draw something heavier
   than a pencil." (pencil reference + large drawing box) · "Draw something
   lighter than a backpack." (backpack reference + large drawing box).

## Notes for Codex

- Do NOT alter any locked page. Do not merge to main, publish, or deploy
  without the user's separate explicit authorization.
- Do not integrate into `directory.js` or the website without the user's
  separate explicit authorization.
- Pack slug suggestion: `compare-weight` under `worksheets/kindergarten/math/`
  (already the PDF's location).
