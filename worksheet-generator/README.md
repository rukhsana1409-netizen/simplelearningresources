# Learning Made Simple Worksheet Generator

This standalone generator creates clean, printable US Letter PDFs. Single worksheets are written to `output/`; finalized counting packs are written to the Preschool Math counting folder under `worksheets/`.

## Generate the starter worksheet

From this folder, run:

```powershell
py -3 generate_worksheet.py content/number-recognition-1-10.json
```

The finished PDF is saved to `output/number-recognition-1-10.pdf`.

## Reuse the template

Duplicate a JSON file in `content/`, then update the worksheet title, directions, footer text, and activity values. The Python template keeps the US Letter page size, margins, Learning Made Simple header and footer, color palette, type hierarchy, and aligned activity layout consistent.

The current layout accepts:

- `trace.items`: ten numbers, arranged in two rows of five.
- `find.target` and `find.choices`: a target number and twelve choices, arranged in two rows of six.
- `write.items`: ten prompts, each with a handwriting line.

For a different activity type or item count, extend the matching drawing function in `generate_worksheet.py`; the shared page branding and layout helpers can remain unchanged.

## Counting worksheets

Use `template: "counting"` with separate `circle`, `match`, and `write` activity data. Object groups use an object name and count; the shared layout supports counts through 20 without changing page-drawing code.

Use `template: "counting-pack"` with five ordered page definitions to generate a bundled Count and Circle, Count and Match, Count and Write, Count and Draw, and Mixed Practice resource. Counting packs are written to `worksheets/preschool/math/counting/`.

Set `range_max` to the largest permitted quantity. Counts 6 through 10 use balanced two- or three-row object grids, while page item counts can be reduced to preserve the approved object and workspace sizes.
