# Handoff — Blending & Segmenting (Kindergarten Reading, Phonological Awareness)

Finalized 2026-10-13. All 5 pages user-approved and locked.

Oral-only phonological awareness: no printed letter decoding or spelling
tasks for children. Adult "Say:" scripts and guidance lines are printed
for the parent/teacher; all phonemes are General American.

## Pages
1. **Blend the Parts** — onset–rime blending; adult says onset, pauses, says rime (Say: /k/ … /æt/); child circles the picture (cat, sun, pig, bus, hat, fish)
2. **Blend the Sounds** — phoneme-by-phoneme blending; each script is the word's actual phonemes (egg /ɛ/•/ɡ/, bee /b/•/i/, dog, cup, web, moon)
3. **Count the Sounds** — segmenting; child says each sound and colors exactly the number of boxes shown (egg 2, cat 3, pig 3, bus 3, nest 4, fox 4 — phonemes, not letters; fox = /f/ /ɑ/ /k/ /s/)
4. **Find the Last Sound** — final-phoneme matching; target picture labeled "Listen," choices under "Circle one" (cat→hat, dog→pig, sun→moon, cup→top, web→tub, fish→brush); purely oral, no printed sound symbols
5. **Change the Sound** — initial-phoneme substitution; adult script "Say: /k/ to /b/" (cat→bat, pig→wig, mop→top, sun→bun, dog→log, van→fan)

## Verification
- Phoneme audit passed for every page: onset–rime scripts recombine to the target words; Page 2 scripts are the words' actual phonemes; Page 3 counts are phoneme counts; Pages 4–5 have exactly one correct answer per item (distractor ending/initial sounds checked).
- All 5 pages re-rendered at 150 dpi and confirmed pixel-identical to the approved review images.
- Bundle page count: 5; US Letter portrait.
- Bundle MD5: `ccf97ca0baeeadbd5b7909792b6473d5`
- Bundle SHA-256: `ac45685a0cde24a57a987bcf4c8a2667f01411d708c0f738d40d06cbd8f99ee6`
- All builder entries `locked=True`.

## Contents
- `blending-segmenting-page-01.pdf` … `-05.pdf` — in the pack directory
- `bs-p1.png` … `bs-p5.png` — approved review renders (110 dpi), in this handoff directory
- Builder: `worksheet-generator/build_blending_segmenting.py` (imports the shared header/logo/image code from `build_phonics_az.py`, also included)
- Bundle: `worksheets/kindergarten/reading/blending-segmenting/blending-segmenting-review.pdf`
- Assets: `worksheet-generator/assets/blending-segmenting/` (15 pack pictures) plus the referenced `animal-library` and `phonics-a-z` library files, and `assets/fonts/Andika-Bold.ttf`

Not in `directory.js`. Not merged to main. Not published to R2. Awaiting Codex review.
