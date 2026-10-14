# Handoff — Common Words: Read & Learn (Kindergarten Reading, High-Frequency Words)

Finalized 2026-10-14. All 5 pages user-approved and locked.

Eleven common words taught across the pack, mixing fully decodable
words with accurately taught pattern pieces (no "memorize the whole
word" framing; no technical terms in child-facing text):
- Sound-out words: it, in, on, can
- Pattern-part words: the (th team + weak e), a (weak sound alone),
  I (says its name alone), is (s = /z/), see (ee team),
  my (y says its name), like (quiet end e)

Marking scheme used on Pages 1 and 3: a teal dot under a letter = an
individual sound the child can sound out; a teal underline = letters
that work together or need extra practice.

## Pages
1. **Read the Words** — six words introduced (the, a, I, is, it, in), each large with markings above a tiny pictured phrase; child reads the word and finds it in the phrase. Adult note explains the dots/underlines scheme, and that the e in "the" makes a weak sound like the word "a".
2. **Read & Find** — word-level sentence completion: picture + sentence with one missing common word + two word choices to circle (the, a, I, is, It, in). Both choices are readable; only one makes the sentence right.
3. **Meet the New Words** — guided reading: the five remaining words (on, can, see, like, my) shown large with markings, then in large-print phrases with matching pictures; child finds and circles the new word inside the phrase. Adult note explains ee in see, the quiet end e in like, and y in my.
4. **Read & Match the Sentences** — five complete sentences (capital + period) matched by drawn lines to shuffled pictures showing each sentence's exact meaning ("My hat is red." / "I can hop." / "I see the hen." / "The cat is on the log." / "The pig is in the box."). Shuffle yields only two line crossings.
5. **Common Word Search** — 9x9 grid, all 11 words, across or down only (no backwards, no diagonals), with a check-off word list. Answer key below.

## Word-search answer key (start row, start column, direction; 1-based from top-left)
- the: row 2, col 7, down · see: row 7, col 7, across
- on: row 3, col 3, across · can: row 6, col 6, down
- is: row 5, col 8, down · like: row 5, col 4, down
- it: row 7, col 5, down · my: row 5, col 5, down
- in: row 7, col 2, down
- a: row 6, col 3 (single letter) · I: row 9, col 4 (single letter)
Note: every 2+ letter word occurs exactly once in any straight
direction (verified programmatically). The single-letter words
naturally recur as letters: "a" also appears inside "can", and the
letter i appears inside several words; the key gives the intended
standalone spots.

## Verification
- Every Page 2 choice pair audited: exactly one choice completes each sentence grammatically and matches its picture; no a/the or I/it pairings used.
- All 5 pages re-rendered at 150 dpi and confirmed pixel-identical to the approved review images.
- Bundle page count: 5; US Letter portrait; page order verified (Read the Words / Read & Find / Meet the New Words / Read & Match the Sentences / Common Word Search).
- Bundle MD5: `b1121c811e5565b8d441a81c654bf9a5`
- Bundle SHA-256: `7f7d2433fe7cd30ffdbca9ae2620f8f4cdefa33676ac365c8a3434d44abe69e6`
- All builder entries `locked=True`.

## Contents
- `common-words-read-learn-page-01.pdf` … `-05.pdf` — in the pack directory
- `cw-p1.png` … `cw-p5.png` — approved review renders (110 dpi), in this handoff directory
- Builder: `worksheet-generator/build_common_words.py` (imports the shared header/logo/image code from `build_phonics_az.py`, also included)
- Bundle: `worksheets/kindergarten/reading/common-words-read-learn/common-words-read-learn-review.pdf`
- Assets: `worksheet-generator/assets/cvc-words/` (pack pictures incl. the cw-* scenes) plus the referenced `animal-library` and `phonics-a-z` library files, and `assets/fonts/Andika-Bold.ttf`

Not in `directory.js`. Not merged to main. Not published to R2. Awaiting Codex review.
