# Learning Made Simple Worksheet Generator

This standalone generator creates clean, printable US Letter PDFs. It does not use or modify the existing website pages or `worksheets/` directory.

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
