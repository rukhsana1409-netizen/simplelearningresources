# Handoff — All About… My Fact Pages (Kindergarten)

**Status:** All three pages user-approved & locked 2026-10-19; the
final pack was approved for handoff by the user the same day.
Finalized by Muse (PDFs + this handoff); integration is Codex's
step. NOT registered in directory.js, NOT merged, NOT published.

## Pack

Kindergarten Writing, Michigan W.K.2 (informative/explanatory
writing). A compact three-page pack created after a page-by-page
audit (2026-10-19) found informative composing was a genuine gap:
no existing page had a child name a topic and supply information
about it. (My First Writing Adventures is labeling, free
draw-and-write, narrative, and revision; the Informational Text
pack teaches READING main topic and key details, not composing.)
Every page supports drawing, adult dictation, and emerging
independent writing; facts must be true — the parent guide draws
the fact/opinion line explicitly. Companion pack: My Opinion:
I Like, I Think (W.K.1), handed off earlier on this branch.

- P1 One True Fact — the topic (dogs) is given and printed as the
  page heading, "All About Dogs." The child draws a dog in a big
  box and completes ONE fact with a child-friendly starter:
  "Dogs can …" (run, swim, dig, bark). Adult line: "A fact is
  something true."
- P2 Two True Facts — same supported format, new topic (fish,
  chosen because its basic facts are unconditionally true). Two
  numbered fact rows with two DIFFERENT starters so the facts
  come out different: ① "Fish can …" (something fish do — swim)
  and ② "Fish have …" (something fish have — fins, tails,
  scales). Label: "Tell two DIFFERENT true facts about fish:"
- P3 My Information Page — the independent closer. No printed
  topic and no sentence starters: the child chooses any topic
  (guide line: an animal, a food, a place, or a thing), names it
  on a plain "My topic:" line, draws it in a spacious box, and
  writes or dictates two different true facts in two numbered,
  starter-free fact areas with full primary handwriting lines.

## Deliverables (repo paths)

- worksheets/kindergarten/reading/all-about-fact-pages/all-about-fact-pages-review.pdf — 3-page bundle
- worksheets/kindergarten/reading/all-about-fact-pages/all-about-fact-pages-page-01.pdf … -03.pdf
- worksheets/kindergarten/reading/all-about-fact-pages/all-about-fact-pages-parent-guide.pdf — one-page parent guide (W.K.2 objective; a facts-vs-opinions section with examples and a gentle redirect question; accurate example facts for every page — dogs run/swim/dig, fish swim/fins/tails, and apples for the open page; support tips for drawing, dictation, and invented spelling); NOT in the bundle
- worksheet-generator/build_informational_writing.py — source generator (all pages locked; "finalize" mode asserts the locks). No artwork files: all three pages are text-and-drawing-space only by design
- tmp/handoffs/all-about-fact-pages/ — this file + fp-p1.png … fp-p3.png (110 dpi previews)

## Verification

- All PDFs US Letter (612×792 pt); bundle 3 pages.
- Every bundle page rendered at 150 dpi is pixel-identical (MD5) to
  the preview the user approved for that page
  (P1 74a0c0c6…, P2 92ef4a2c…, P3 6e3b222c…).
- Bundle: 68,658 bytes
  MD5: 408283108d8d3b3fc99bb095617463af
  SHA-256: f9ef1e18586ef4808c099af2889d488bd7f313d5606f49121b6a4d8926aa5c26

## Design notes

- Canonical Learn My Letters header/logo imported verbatim from
  build_phonics_az.py; handwriting-guide rows use the pack standard
  three-line set (solid top and baseline, dashed midline, 30pt rows)
  shared with My First Writing Adventures.
- Scaffolding fades by design: printed topic + one starter (P1) →
  printed topic + two different starters (P2) → child's own topic,
  labels only, open lines (P3).
- Fact accuracy was a design constraint: starters were chosen so
  every natural completion is true ("Dogs can…", "Fish can…",
  "Fish have…"), avoiding overgeneralizations such as "birds can
  fly."
