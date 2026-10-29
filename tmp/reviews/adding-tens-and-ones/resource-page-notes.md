# Adding Tens and Ones Within 100 — review notes (7-page revision, DRAFT)

Grade 1 Math | Adding Tens and Ones. Builder:
`worksheet-generator/build_adding_tens_ones_v2.py`. Models are
the Tens and Ones to 100 pack's base-ten cubes (turquoise rods,
gold ones), reused exactly. Every sum stays within 100.
No carried-digit algorithm anywhere. No printable key built.

## Answers (internal check only)

- Page 1 Add Tens: 34 + 20 = 54 (worked); 52 + 30 = 82;
  26 + 40 = 66. Only the tens change.
- Page 2 Add Ones: 45 + 3 = 48 (worked); 52 + 5 = 57;
  37 + 2 = 39. Only the ones change. Closing question,
  asked once: Did the tens change? No.
- Page 3 Add Tens and Ones Together (no regrouping):
  34 + 25 = 59 (worked, combined model drawn); 42 + 21 = 63;
  35 + 24 = 59. Children draw the combined model in the
  dashed frame, then record tens, ones, sum.
- Page 4 Make a Group of 10 (visual only, no addition
  equations): worked example is an explicit before-and-after
  sequence. Before: 13 ones with 10 circled, 3 left outside
  the circle. After (separate display): exactly 1 ten rod and
  3 ones, labeled "1 ten and 3 ones", so the original 10 are
  never counted again. Practice: 16 ones = 1 ten and 6 ones;
  12 ones = 1 ten and 2 ones; 18 ones = 1 ten and 8 ones.
- Page 5 Add Ones and Make a New Ten (2-digit + 1-digit):
  worked 47 + 5 = 52 in four separated steps (combine 12
  ones; circle 10; trade for 1 ten rod, 2 left; count
  5 tens, 2 ones). Supported: 36 + 7 = 43 (13 ones);
  58 + 6 = 64 (14 ones).
- Page 6 Add Two-Digit Numbers with a New Ten: worked
  36 + 28 = 64 (start models; combine 14 ones; circle 10;
  trade for 1 ten rod, 4 left; count 3 tens, 2 tens, and
  1 new ten make 6 tens). Supported: 47 + 35 = 82
  (12 ones; 4 tens, 3 tens, and 1 new ten make 8 tens).
- Page 7 Let's Practice Adding: instruction "Add. Draw tens
  and ones if you need help." 64 + 30 = 94; 52 + 6 = 58;
  29 + 8 = 37; word problem 45 + 27 = 72 (Sam's apples),
  with a full-width dashed "Make a new ten" area where the
  child shows the exchange ("Draw all 12 ones here. Circle
  10. Draw 1 new ten rod.", so the 5 and 7 ones are combined
  before exchanging). Large equations and answer boxes unchanged.

## Design notes

- Every problem page puts a large equation (18-20pt bold)
  before the visuals. Page 4 is the exception by design:
  it has no addition equations at all.
- Regrouping steps are visually separated. The circled ones
  and the new ten rod never share a counting display, so
  the 10 ones are never counted twice.
- Page 2 keeps worked + 2 practice problems plus the
  single closing tens-change question, so the enlarged
  models fit. Page 3 reads "2 spacious problems" as
  2 practice problems plus the worked example.
- Page 6 has 1 supported problem (not 2), because the
  five-row worked example fills the page.
