# Handoff — Understanding Print & Sentences (Kindergarten)

**Pack:** Understanding Print & Sentences — 5 pages
**Category:** Kindergarten → Reading & Language → Alphabet & Print Concepts
**Status:** All 5 pages user-approved and locked (2026-10-14). NOT yet in
directory.js, NOT merged, NOT published — for Codex review/integration.

## Files

- `worksheets/kindergarten/reading/understanding-print-sentences/understanding-print-sentences-review.pdf` — combined 5-page bundle
- `worksheets/kindergarten/reading/understanding-print-sentences/understanding-print-sentences-page-01..05.pdf` — individual pages
- `worksheet-generator/build_print_sentences.py` — builder (imports the
  canonical header/footer/logo and image helper from
  `build_phonics_az.py` — do not fork)
- New illustration assets in `worksheet-generator/assets/cvc-words/`:
  `ups-story.jpg` (source scene) and `ups-story-wide.jpg` (cropped
  version used on Page 5). All other pictures are reused library assets.
- Previews (110 dpi): `tmp/handoffs/understanding-print-sentences/ups-p1..p5.png`

## Verification

- Bundle MD5: `03c84359c3b1b38ea6362d64b2b5a683`
- Bundle SHA-256: `b848118d8d89d2febcf6526e133b7c9379dedf408af412ab7cd065dc657b60eb`
- Bundle size: 1,863,036 bytes; 5 pages; every page 612 × 792 pt (US Letter)
- Every page PDF renders pixel-identical (150 dpi) to the user-approved
  preview.
- Answer audit passed programmatically:
  - P2 word counts: "I see the cat." 4 · "The hen can run." 4 ·
    "It is a big sun." 5 · "The pig is in the box." 6
  - P3: each capitalization pair has exactly one correct option; end-mark
    pairs never pit "." against "!" (answers decided by sentence form)
  - P4: guided numbering 1–6 across the line break; first word *I*, last
    word *dog.*; correct continuation *the box.*
  - P5: story has exactly 3 sentences; first word *The*, last word
    *cat.*; correct choice *The sun is up.*

## Page map

1. Let's Learn About Letters, Words & Sentences — teaching page:
   letter → word → sentence with the c-a-t / cat example threaded
   through all three sections ("cat" underlined in the sentence)
2. Spaces Between Words — boxed-words teaching example (numbered 1–4),
   four word-counting rows, missing-spaces fix-it with a worked
   example (I | see | it.) plus independent practice (Ilikejam.)
3. Beginning & Ending a Sentence — teaching panel (capitals t → T;
   end marks . tells / ? asks / ! big feeling), circle the correctly
   capitalized sentence, circle the right end mark
4. Follow the Words — three distinct sections: numbered guided
   reading (1–6), independent first/last-word marking,
   choose-the-continuation
5. Put It Together — independent practice on a 3-sentence story
   ("The cat is on the mat. The sun is up. I like my cat.") with four
   numbered activities (count sentences, first/last word, missing
   spaces, choose the correctly written sentence)

## Notes for integration

- All text uses only the 11 common words from Common Words — Read &
  Learn plus familiar decodable CVC words.
- One open design note: the pack title at 22 pt in the canonical
  header runs slightly past the right end of the teal rule on every
  page. This was flagged to the user during review and left
  unchanged (the header is the verbatim master); revisit only with
  her approval.
