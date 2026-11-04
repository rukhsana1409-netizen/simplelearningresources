# Unknown Numbers and True or False Equations Within 20 — review notes

Grade 1 Math | Unknown Numbers and True or False. Builder:
`worksheet-generator/build_unknown_numbers_true_false.py`.

Status: APPROVED 2026-11-04, LOCKED. Approved in the user's own
words for all 5 revised pages, exactly as reviewed. No further
content, layout, or visual changes after this approval. Not
merged to main, not published; Codex handles integration
separately. No printable answer key built.

## Scope

Bare equations only, no word stories. No strategy teaching: no
count on, count back, count up, make 10, or doubles. No fact
family triangles, no ten frames, no number lines, no base ten
rods. Visuals are original vector balance scales and dot
groups only. All numbers, sums, and differences within 20.
Standards alignment is internal only and never appears on a
child page.

## Answers (internal check only)

- Page 1 Equal Means the Same Amount: worked 5 and 5, Same.
  Practice 1: 5 and 5, Same. Practice 2: 4 and 6, Not Same.
  The third scale tips down on the heavier right side.
- Page 2 True or False?: worked 9 + 3 = 12, True (12 and 12).
  8 + 5 = 12, False (13, not 12). 7 = 8 - 1, True (7 and 7).
  10 - 4 = 5 + 2, False (6, not 7). 6 + 7 = 5 + 8, True
  (13 and 13). 15 - 8 = 6, False (7, not 6). Three true,
  three false counting the worked example.
- Page 3 Find the Missing Number in Addition: worked
  ? + 6 = 14, missing 8, check 8 + 6 = 14. 9 + ? = 17,
  missing 8. 8 + 7 = ?, missing 15. ? + 5 = 12,
  missing 7. 6 + ? = 18, missing 12. Start, change,
  result, start, and change positions.
- Page 4 Find the Missing Number in Subtraction: worked
  ? - 5 = 11, missing 16, check 16 dots with 5 crossed out
  and 11 left. Practice in two columns, 8 equations:
  16 - ? = 9, missing 7; 18 - 6 = ?, missing 12;
  ? - 8 = 9, missing 17; 19 - ? = 13, missing 6;
  ? - 4 = 10, missing 14; 15 - ? = 6, missing 9;
  17 - 9 = ?, missing 8; ? - 7 = 11, missing 18.
  Positions: change, result, start, change, start,
  change, result, start. All 8 practice answers are
  distinct and none matches the worked answer 16.
- Page 5 Mixed Check: 9 + 4 = 5 + 8, True (13 and 13).
  ? + 7 = 15, missing 8. 17 - ? = 10, missing 7.
  12 = 9 + 4, False (13, not 12). ? - 6 = 12,
  missing 18.
  Fix the False One: 8 + 3 = 12 is false (8 + 3 = 11).
  Accept any fix that changes exactly one number to a true
  equation: 8 + 3 = 11, 8 + 4 = 12, or 9 + 3 = 12.

## Checks done before delivery

- Builder asserts passed for every equation and answer above.
- All 5 previews read at print size. Balance scales: level
  when totals match, tipped down on the heavier side when
  they differ, trays hanging from the beam ends by diagonal
  strings as on a real scale. Page 4 worked example: first
  5 dots crossed, 11 uncrossed, matching 16 - 5 = 11.
- No overlap: Page 4 worked box was moved down after the
  first render, when it overlapped the Watch label, and the
  page was re-rendered clear. No text reaches the footer on
  any page. Child PDF text checked clean of em-dash, borrow,
  and regroup.

## Revision 2026-11-04 (header fix plus added practice)

- Header overflow found and fixed locally in this pack's
  builder only, shared header untouched: at 15pt the
  subtitle ran to x=607.5, 55.5pt past the teal rule at
  x=552, and the Page 4 and Page 5 titles also ran past
  the rule. Subtitle is now 12pt (ends x=532.8) and the
  Page 3, 4, and 5 titles are reduced to 17pt, 16pt, and
  16pt, so every title and subtitle ends inside the rule.
  Page 1 content is otherwise unchanged.
- Pages 2 to 4 gained 2 practice equations each, Page 5
  gained 1 true or false item and 1 missing-number item.

## Revision 2, 2026-11-04 (Pages 2, 4, and 5 only)

- Pages 2 and 5: True and False pills moved from x=370
  to x=310, closer to the equations in a consistent
  column, and raised so their centres match the equation
  centres (pill starts at equation baseline minus 12, for
  a 40pt pill). Equations on Pages 2 and 5 are unchanged.
  Pages 1 and 3 were verified pixel-identical to the
  previous revision, so they are not reshown.
- Page 4: worked example unchanged at the top. Practice
  is now 8 equations in two columns, 4 rows, left column
  x=60 and right column x=320, boxes still 50 by 44pt,
  rows 75pt apart, widest right-column equation ending
  near x=516, inside the 552 margin. All three unknown
  positions are included, answers listed above.
  All existing worked examples and practice items are
  kept, in the same order, with new items added after
  them (Page 5 Fix the False One stays last). All new
  answers were validated by builder asserts and re-read
  on the revised previews.
