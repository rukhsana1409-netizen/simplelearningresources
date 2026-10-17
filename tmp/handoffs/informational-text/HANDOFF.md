# Handoff — Informational Text: Main Topic & Key Details (Kindergarten)

**Status:** All five pages user-approved & locked 2026-10-16. Finalized by Muse
(PDFs + this handoff); integration is Codex's step. NOT registered in
directory.js, NOT merged, NOT published.

## Pack

Kindergarten Reading & Language → Comprehension (Informational Text),
Michigan RI.K.1–3 + RI.K.7. Five pages that teach a child to find the
main topic of a short nonfiction text, pick out its key details, and
see how a picture can show what the words say. Every passage is a
short adult read-aloud in a boxed FACTS panel (neutral label, so the
panel never gives away the topic); every child response is
picture-based.

- P1 What Is This Text About? (main topic, RI.K.2) — Bees. Passage:
  "Bees are insects. They live in a hive. / Bees fly from flower to
  flower. / Bees make honey." Choices: bee / flowers / honey — the
  two wrong choices are details IN the text, so the child must grasp
  the whole-text topic (the user's plan revision; no unrelated
  giveaway picture).
- P2 Find the Key Details (RI.K.1/2) — Penguins. Passage: "Penguins
  are birds. Penguins cannot fly. / Penguins swim in the cold sea
  and catch fish. / Many penguins live where it is cold and snowy."
  Circle three: swimming (TL), fish in beak (TR), penguins standing
  in snow (BR). The flying penguin (BL) contradicts the text. The
  passage deliberately avoids any "all penguins live on ice" claim.
  The snow choice shows penguins STANDING in their habitat (user
  revision; an earlier sliding-penguin version was replaced).
- P3 What Does the Picture Show? (RI.K.7) — Rain. Passage: "Rain
  falls from clouds in the sky. / Rain makes puddles on the ground.
  / Rain helps plants and flowers grow." One big illustration shows
  all three details; two focused questions (NOT a visual search):
  What does rain fall from? → the cloud (sun/moon distractors).
  What does rain help grow? → the flowers (snowman/sandcastle).
- P4 From Wheat to Bread (RI.K.1/2/3) — Process passage: wheat
  grows → grains are ground into flour → bakers use the flour to
  make bread. Three question rows: main topic (loaf; shoe/boat
  wrong); What are the grains ground into? → flour (middle; wheat
  = step before, loaf = step after); What happens after wheat
  grains are ground into flour? → the baker making dough (middle;
  shoe/kite wrong) — Q3 wording and choices set by the user's
  revision, replacing an earlier "What do bakers make" question.
- P5 Taking Care of My Teeth (capstone, RI.K.2/7) — Passage:
  "Brushing keeps your teeth clean and strong. / Brush your teeth
  in the morning and at night. / A dentist checks your teeth."
  Topic: the tooth being brushed (hairbrush/book wrong). Details —
  circle TWO stated details as action scenes (user revision): a boy
  brushing his teeth, a dentist examining teeth; wrong: a girl
  combing her hair (never in the text; no ambiguous food
  distractors). Draw: "DRAW ONE WAY YOU TAKE CARE OF YOUR TEETH."
  in a full-width box, explained aloud (user-set wording).

## Deliverables (repo paths)

- worksheets/kindergarten/reading/informational-text/informational-text-review.pdf — 5-page bundle
- worksheets/kindergarten/reading/informational-text/informational-text-page-01.pdf … -05.pdf
- worksheets/kindergarten/reading/informational-text/informational-text-answer-key.pdf — one-page parent key (objective + every answer, incl. drawing guidance); NOT in the bundle
- worksheet-generator/build_informational_text.py — source generator (all pages locked; main() asserts the lock)
- worksheet-generator/assets/informational-text/ — 34 artwork files (incl. superseded it-obj-brushpaste.jpg, it-hands.jpg, it-obj-scarf.jpg, kept with the pack's assets)
- tmp/handoffs/informational-text/ — this file + it-p1.png … it-p5.png (110 dpi previews)

## Verification

- All PDFs US Letter (612×792 pt); bundle 5 pages.
- Every bundle page rendered at 150 dpi is pixel-identical (MD5) to
  the preview the user approved for that page.
- Bundle: 18,252,198 bytes
  MD5: 59b93a5f59a38360e8d1070ab64e45eb
  SHA-256: b2eefdc677a832e9cfac25bdbf51be644bf70d92231e26000091301e2bb61c50

## Design notes

- Canonical Learn My Letters header/logo imported verbatim from
  build_phonics_az.py; watercolor picture-book art throughout.
- The FACTS label is intentionally neutral: titling the panel with
  the topic would answer Page 1's question for the child.
- Factual-accuracy rules the user set for this pack: every circled
  detail is stated in the passage in so many words; no blanket
  animal generalizations; process questions must require the text,
  not picture recognition.
