# Handoff — Place Value: Tens & Ones (Kindergarten Math)

Final approved bundle for Codex. All 6 pages user-approved and locked 2026-10-06.
Nothing was changed for this handoff — files are exact copies of the approved finals.

Concept: numbers 11–19 as 1 group of ten plus additional ones (Page 6 also uses
20 as a tens transition: 2 tens + 0 ones). Pastel palette throughout: light-blue
tens (#A9C9EE), soft-peach ones (#F9B98C), dark outlines. Pure vector ReportLab,
no image assets.

## Contents

| File | Description |
|---|---|
| `worksheets/kindergarten/math/place-value/place-value-review.pdf` | **Final 6-page PDF** (29,573 bytes). The "-review" in the name is historical only. |
| `worksheet-generator/build_place_value.py` | Builder source (reportlab, pure vector). All 6 pages flagged `locked=True`. |
| `tmp/handoffs/place-value-tens-ones/HANDOFF.md` | This file. |

## Verification (2026-10-06)

- MD5: `dfa69bad4a253cb7e7c454ed641942c1`
- SHA-256: `dbd213bd8487db6d74b09bbb4ced404e8ded9260c9e86e47a2cbfbf54c732963`
- All 6 pages re-rendered at 110 dpi and confirmed pixel-identical (SHA-256 match)
  to their approved review images. All 6 pages flagged locked in the builder.
- Math audited on every problem: tens/ones counts, printed numbers, and
  correct/incorrect relationships all verified (see Page order below).

## Page order

1. **Build Numbers with Tens & Ones** — "Count the tens and ones. Write the numbers."
   Completed example (1 ten + 3 ones = 13, values shown in answer boxes), then
   practice: 12 (2 ones), 15 (5 ones), 17 (7 ones), 19 (9 ones).
   Sentence pattern: `1 ten and [ ] ones = [ ]`.
2. **Count Tens & Ones** — "Count the dots. Write the number." 10 problems in
   clean horizontal rows: one full light-blue ten frame + one peach ones frame
   + large answer box. Numbers: 11, 14, 17, 12, 15, 18, 13, 16, 19, 14.
3. **Count the Blocks** — "Count the tens and ones. Write the number."
   6 problems (2×3): one vertical light-blue tens rod + neat peach ones block
   + one large number box. Numbers: 13, 16, 19, 11, 15, 17.
4. **Tens & Ones** — "Write each digit in the Tens and Ones boxes." 6 numbers
   (12, 15, 18, 14, 11, 17) with large labeled Tens | Ones digit boxes (70×70).
5. **Match the Number** — "Count the blocks. Match the number." Cut-and-paste:
   6 problems (2×3) with vertical tens rod + ones + large dashed paste box;
   6 shuffled dashed numeral cards at the bottom (16, 12, 19, 11, 14, 18) with
   scissors label. Models: 12, 18, 14, 11, 19, 16 — card set matches exactly.
6. **Is the Number Correct?** — "Count the blocks. Is the number correct?
   Circle Yes or No." 6 problems (2×3 cards): continuous vertical light-blue
   tens rod(s) (single outer border, 9 thin dividers = 10 units) + peach ones
   on a shared baseline + large printed number + Yes / No.
   (1 ten+5 ones → 15 ✓) · (1 ten+3 ones → 14 ✗, is 13) ·
   (2 tens → 20 ✓) · (1 ten+7 ones → 16 ✗, is 17) ·
   (1 ten+2 ones → 12 ✓) · (1 ten+8 ones → 19 ✗, is 18).
   3 correct / 3 believable near-misses.

## Notes for Codex

- Do NOT alter any locked page. Do not merge to main, publish, or deploy
  without the user's separate explicit authorization.
- Keep this pack conceptually separate from the Addition & Subtraction packs:
  no arithmetic beyond the place-value representations shown here.
