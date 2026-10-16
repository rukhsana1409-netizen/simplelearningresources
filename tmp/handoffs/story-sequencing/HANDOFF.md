# Story Sequencing — First, Next & Last — Handoff

Kindergarten Reading & Language (Literature / retelling). Five
worksheet pages, all user-approved and locked 2026-10-15/16, plus a
separate one-page parent answer key. Aligned with the Michigan
kindergarten reading standard RL.K.2 (with prompting and support,
retell familiar stories, including key details) — sequencing events
is taught here as the foundation of retelling.

## Files

- `worksheets/kindergarten/reading/story-sequencing/story-sequencing-review.pdf`
  — the 5-page bundle (14,034,184 bytes)
  - MD5: `cc6b4b4b090a14360258642abc4c7419`
  - SHA-256: `4e1d385684724f604e1a9d6c1d3eb8c5b8c5b5d9e012a4f52859ec530d7b3903`
- `story-sequencing-page-01.pdf` … `story-sequencing-page-05.pdf`
  — the individual pages
- `story-sequencing-answer-key.pdf` — parent answer key with the
  learning objective (NOT part of the child bundle)
- `worksheet-generator/build_story_sequencing.py` — the builder
  (imports the canonical header/footer from `build_phonics_az.py`,
  also included, with the Andika-Bold font)
- Artwork under `worksheet-generator/assets/story-sequencing/`
- Previews: `tmp/handoffs/story-sequencing/sq-p1.png` … `sq-p5.png`
  (110 dpi renders of the final bundle pages)

## The pages

1. **First, Next, Last** — building a snowman (one snowball → two
   stacked → finished snowman). Pictures are in order; children
   write 1, 2, 3 under FIRST / NEXT / LAST labels.
2. **Put the Story in Order** — a muddy puppy gets a bath, shown
   mixed up. Correct numbers left to right: 3, 1, 2.
3. **What Happens Next?** — bubble story: wand dipped (1), small
   bubble forming (2), then circle the correct ending from three
   choices. Answer: the middle picture (the big bubble). The other
   choices (scooter, reading) keep the same character so only the
   bubble picture can complete the story.
4. **Sequence a Short Story** — adult reads the Leo kite story
   aloud (boxed story panel); three events mixed up. Correct
   numbers left to right: 2, 3, 1. Each story sentence matches
   exactly one picture.
5. **My Story Sequence** — four-step cookie-baking story in a 2×2
   grid (bright flat artwork, plain backgrounds — redesigned at the
   user's direction after a muted watercolor version was rejected
   as too small/crowded). Children cut the number tiles 1–4 from
   the labeled strip and paste them under the pictures. Correct
   pastes: top-left 3 (baked tray), top-right 1 (mixing), bottom-
   left 4 (eating), bottom-right 2 (shaping dough balls). Tiles are
   cut at 48 pt, slightly smaller than the 56 pt paste boxes, so
   each pasted number sits inside its box with a margin.

## Notes for integration

- Every bundle page was verified pixel-identical (150 dpi renders)
  to the preview the user approved for that page.
- All pages are US Letter (612×792).
- Page 5 has no adult instruction line (the 2×2 grid plus cut-out
  strip fills the page); the guidance is in the answer key.
- The scissors mark on Page 5's cut-out strip is drawn vector art
  (the ZapfDingbats scissors glyph does not render in this build
  environment).
- Not registered in directory.js; not published. Website
  integration is Codex's step, as usual.
