# Handoff — CVC Words: Read & Spell (Kindergarten Reading, Phonics & Word Recognition)

Finalized 2026-10-13. All 5 pages user-approved and locked.

Strictly true CVC words only (3 letters = 3 phonemes, short vowels):
no digraphs, no blends, no x-words, no silent e. Support is removed one
layer at a time across the pack.

## Pages
1. **Blend It** — guided decoding; word printed large with a dot under each letter; child says each sound, blends, circles the picture (cat, pig, map, sit, bat, pin — short a/i; pig vs pin one-letter contrast included deliberately)
2. **Read & Match** — unsupported reading; word only, circle the picture it names (sun, bed, dog, cup, web, jam)
3. **Build the Word** — guided spelling; picture + 3 large writing boxes + the word's letters scrambled in a separate dashed letter bank (cat, pig, bus, sun, dog, cup)
4. **Missing Vowel** — vowel encoding; picture + first/last letters given, middle box (teal outline) for the missing vowel (cat a, bed e, pig i, dog o, sun u, hat a — all five vowels, a repeated); compact panels distributed evenly
5. **Spell It Myself** — independent spelling; picture + 3 empty boxes, no bank, hints, or dots (jam, hen, mop, van, bed, rug)

## Verification
- CVC audit passed: every word is consonant–short vowel–consonant (3 letters = 3 phonemes); every key picture matches its word; no distractor picture matches its item's word; Page 3 banks contain exactly the word's letters in scrambled (non-word) order; Page 4's missing letter is the word's short vowel in all six items.
- All 5 pages re-rendered at 150 dpi and confirmed pixel-identical to the approved review images.
- Bundle page count: 5; US Letter portrait.
- Bundle MD5: `aa5c1c6924f6456ec6df8c9b461f5e8d`
- Bundle SHA-256: `58b5cd6fef22a622e6cdbec12c7774081d351408443746e9e78081d75cd01505`
- All builder entries `locked=True`.

## Contents
- `cvc-words-read-spell-page-01.pdf` … `-05.pdf` — in the pack directory
- `cvc-p1.png` … `cvc-p5.png` — approved review renders (110 dpi), in this handoff directory
- Builder: `worksheet-generator/build_cvc_words.py` (imports the shared header/logo/image code from `build_phonics_az.py`, also included)
- Bundle: `worksheets/kindergarten/reading/cvc-words-read-spell/cvc-words-read-spell-review.pdf`
- Assets: `worksheet-generator/assets/cvc-words/` (6 pack pictures) plus the referenced `animal-library`, `phonics-a-z`, and `blending-segmenting` library files, and `assets/fonts/Andika-Bold.ttf`

Not in `directory.js`. Not merged to main. Not published to R2. Awaiting Codex review.
