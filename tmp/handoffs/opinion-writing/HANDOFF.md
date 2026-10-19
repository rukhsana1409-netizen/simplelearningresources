# Handoff — My Opinion: I Like, I Think (Kindergarten)

**Status:** All four pages user-approved & locked 2026-10-19. Finalized
by Muse (PDFs + this handoff); integration is Codex's step. NOT
registered in directory.js, NOT merged, NOT published.

## Pack

Kindergarten Writing, Michigan W.K.1 (opinion writing). A compact
four-page pack created after a page-by-page audit (2026-10-19) found
opinion writing was a genuine gap: no existing page had a child name
a topic or book and state an opinion about it. Every page supports
all three composing modes the standard names — drawing, adult
dictation, and emerging independent writing — with reasons always
optional and no prescribed "correct" opinion. The pack deliberately
avoids My First Writing Adventures (labeling, free draw-and-write,
narrative, revision) and Building Simple Sentences (arranging,
expanding, fixing, completing given sentences).

- P1 My Favorite — "What is your favorite? Tell why you like it!"
  An IDEAS strip (apple, ice cream, dog, teddy bear, ball, book —
  reused library art) offers sparks only, with "or your own!";
  nothing is circled as an answer. The child draws their favorite
  in a big box, then completes "My favorite thing is …" and,
  optionally, "I like it because …" on handwriting-guide lines.
- P2 My Favorite Book — "What is your favorite book?" The child
  names the book on a title line ("The book is called …"), draws a
  scene or character from it in a big box, and states their opinion
  on an "I like this book because …" line (reason optional).
- P3 Which Would You Choose? — a meaningful choice between two
  experiences, each a large original illustration created for this
  pack: "Visit the zoo" (girl at a fence with two giraffes) and
  "Visit the beach" (boy building a sandcastle). The child circles
  one, draws themself enjoying it, and states "I would choose …"
  with an optional "I like it because …" reason.
- P4 My Opinion Page — the independent closer. No sentence starters
  anywhere: a plain "My topic:" line, the pack's biggest drawing
  box, and two open handwriting lines under a "What I think:"
  label. A guide line suggests topic kinds (an activity, an animal,
  a food, a place, or a book).

## Deliverables (repo paths)

- worksheets/kindergarten/reading/opinion-writing/opinion-writing-review.pdf — 4-page bundle
- worksheets/kindergarten/reading/opinion-writing/opinion-writing-page-01.pdf … -04.pdf
- worksheets/kindergarten/reading/opinion-writing/opinion-writing-parent-guide.pdf — one-page parent guide (W.K.1 objective, how the pages build independence, example responses marked as examples only — "There is no one correct opinion" — and support tips for drawing, dictation, and invented spelling); NOT in the bundle
- worksheet-generator/build_opinion_writing.py — source generator (all pages locked; "finalize" mode asserts the locks)
- worksheet-generator/assets/opinion-writing/ — 2 artwork files created for this pack (ow-zoo.jpg, ow-beach.jpg); the P1 idea pictures are reused library art, listed in the push manifest
- tmp/handoffs/opinion-writing/ — this file + ow-p1.png … ow-p4.png (110 dpi previews)

## Verification

- All PDFs US Letter (612×792 pt); bundle 4 pages.
- Every bundle page rendered at 150 dpi is pixel-identical (MD5) to
  the preview the user approved for that page
  (P1 91bb1d09…, P2 ecf50d9c…, P3 159ddb5f…, P4 e24df7fa…).
- Bundle: 2,755,280 bytes
  MD5: 478704374c9f31973065e6366144ed03
  SHA-256: a03aab4b57f2b513ddfa347e798adcfd8511775682bc3a17ea8dbd55a50f34bc

## Design notes

- Canonical Learn My Letters header/logo imported verbatim from
  build_phonics_az.py; handwriting-guide rows use the pack standard
  three-line set (solid top and baseline, dashed midline, 30pt rows)
  shared with My First Writing Adventures.
- Scaffolding fades by design: idea pictures + two sentence starters
  (P1) → book frame + starters (P2) → either/or choice + starters
  (P3) → labels only, open lines (P4).
- The same adult line anchors Pages 1–3 ("Your child can draw, tell
  you their words, or write. Telling why is optional."); Page 4's
  two-line version adds that the child picks their own topic.
