# Handoff — Say It & Split It: Rhymes and Word Parts (Kindergarten)

**Status:** All four pages user-approved & locked 2026-10-19. Finalized
by Muse (PDFs + this handoff); integration is Codex's step. NOT
registered in directory.js, NOT merged, NOT published.

## Pack

Kindergarten Phonological Awareness, Michigan RF.K.2a–c. A compact
four-page ORAL-ONLY pack built to fill the gaps a page-by-page audit
of the existing resources found (rhyme production, syllable blending,
syllable segmentation/pronunciation, onset–rime segmentation) without
duplicating Preschool Rhyming Pictures, Clap the Syllables, Blending &
Segmenting, or CVC Words. No fifth page. Nothing on any child page is
meant to be read or written by the child; the spoken material lives in
the parent answer key.

- P1 Say a Rhyme (rhyme production, RF.K.2a) — four picture prompts
  (cap, pig, boat, moon), each with a "My rhyme:" speech bubble where
  the adult records the word the child says, plus an optional
  "Draw it if you wish" box. Any real or nonsense word with the same
  ending sound counts. (The original "map" target was replaced by a
  large blue baseball cap at the user's direction.)
- P2 Blend the Word Parts (syllable blending, RF.K.2b) — six panels,
  three picture choices each. The child page carries NO printed
  scripts (user revision): each panel says only "Listen!". The adult
  says the syllables with a short pause, without first saying the
  whole word: cup…cake, rain…bow, snow…man, ba…na…na, but…ter…fly,
  el…e…phant. Answers (in reading order): middle, right, middle,
  middle, right, left. There is NO separate parent guide PDF (user
  correction 2026-10-19) — the prompts are in the answer key.
- P3 Say the Word Parts (syllable segmentation, RF.K.2b) — six large
  picture prompts (pancake, toothbrush, popcorn, rabbit, potato,
  umbrella). Purely oral (user revision): the child says the whole
  word, then each syllable slowly, one at a time. No strips, no
  line-drawing, no counting, no component-picture matching.
  Divisions: pan-cake, tooth-brush, pop-corn, rab-bit, po-ta-to,
  um-brel-la.
- P4 Split the Word (onset–rime segmentation, RF.K.2c) — six large
  picture prompts (cake, leaf, boat, rain, kite, mouse), none of
  them in Blending & Segmenting's onset–rime blending set. The child
  says the whole word, then the first sound, then the rest of the
  word as one chunk. Splits (sounds, not letters): k…ake, l…eaf,
  b…oat, r…ain, k…ite, m…ouse.

## Deliverables (repo paths)

- worksheets/kindergarten/reading/say-it-split-it/say-it-split-it-review.pdf — 4-page bundle
- worksheets/kindergarten/reading/say-it-split-it/say-it-split-it-page-01.pdf … -04.pdf
- worksheets/kindergarten/reading/say-it-split-it/say-it-split-it-answer-key.pdf — one-page parent key (learning objective, practical tips, rhyme examples, P2 spoken prompts with answers/positions, P3 syllable divisions, P4 sound splits); NOT in the bundle
- worksheet-generator/build_say_it_split_it.py — source generator (all pages locked; "finalize" mode asserts the lock)
- worksheet-generator/assets/say-it-split-it/ — 5 artwork files created for this pack (ss-cap.jpg, ss-pancake.jpg, ss-popcorn.jpg, ss-potato.jpg, ss-rain.jpg); other pictures are reused library art, listed in the push manifest
- tmp/handoffs/say-it-split-it/ — this file + ss-p1.png … ss-p4.png (110 dpi previews)

## Verification

- All PDFs US Letter (612×792 pt); bundle 4 pages.
- Every bundle page rendered at 150 dpi is pixel-identical (MD5) to
  the preview the user approved for that page
  (P1 da3c29b5…, P2 9925352d…, P3 1be84fc1…, P4 b2d62e32…).
- Bundle: 3,979,373 bytes
  MD5: d3336b401029791ccc042a8303c7b8fa
  SHA-256: e0939228c0edb0fa171243296807f103b24b3f68c83589e7ec7a94dc2db91d7c

## Design notes

- Canonical Learn My Letters header/logo and circular picture code
  imported verbatim from build_phonics_az.py.
- Oral-language pages carry nothing for the child to read: P2 panels
  say only "Listen!", and P3/P4 panels hold a single large picture.
- Syllable boundaries and onset–rime splits were verified against
  natural General American pronunciation (butterfly and elephant are
  three syllables each: but-ter-fly, el-e-phant).
