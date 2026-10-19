# Worksheet draft review workflow

This workflow adds a human review gate before a Muse draft reaches a permanent
`muse/*-handoff` branch. It uses Git, Python, and PyMuPDF already used by the
project. It does not call paid APIs, upload assets, publish resources, merge
branches, or deploy the website.

## 1. Prepare the complete draft on a review branch

Create a branch that cannot be confused with the permanent handoff branch:

```bat
git switch -c muse/review/example-pack
```

Place the complete draft on that branch: one combined PDF, matching individual
page PDFs, one preview per page, and the complete parent guide. Then run:

```bat
python worksheet-generator\review_pack.py prepare ^
  --resource-id example-pack ^
  --bundle worksheets\kindergarten\reading\example\example-review.pdf ^
  --individual-glob "worksheets/kindergarten/reading/example/example-page-*.pdf" ^
  --preview-glob "tmp/reviews/example-pack/source-previews/*.png" ^
  --parent-guide worksheets\kindergarten\reading\example\example-parent-guide.pdf ^
  --expected-pages 4 ^
  --review-dir tmp\reviews\example-pack
```

The command fails unless the branch begins with `muse/review/`. It checks:

- exact page and preview counts;
- readable, non-empty PDFs and images;
- US Letter dimensions for every worksheet and guide page;
- successful 144-DPI rendering;
- pixel equivalence between each individual PDF and its bundle page;
- SHA-256 hashes and byte sizes for every review file.

It writes `review-manifest.json` and consistent 1224×1584 review renders beneath
the review directory. Commit all draft files, renders, and the manifest to the
review branch. Because `tmp/` is ignored, add review artifacts explicitly:

```bat
git add -f tmp\reviews\example-pack
```

## 2. Share one consolidated review set

Upload the files listed in the manifest's `chatgptReviewSet` to ChatGPT. This
includes the complete combined PDF, complete parent guide, all canonical page
renders, and the manifest. Ask for one consolidated visual and educational
review covering page order, instructions, age appropriateness, accuracy,
clipping, overlap, artwork, and parent guidance.

Muse revises every flagged page on the same review branch, reruns `prepare`, and
commits the new manifest and renders. Rerunning `prepare` removes any earlier
approval record because changed files require a complete new review.

## 3. Record explicit approval

Only after the complete revised PDF and parent guide are explicitly approved,
record that decision with the reviewer name and a durable conversation or issue
reference:

```bat
python worksheet-generator\review_pack.py approve ^
  --review-dir tmp\reviews\example-pack ^
  --approved-by "Rukhsana" ^
  --approval-reference "ChatGPT review YYYY-MM-DD"
```

Commit `approval.json`. It locks the manifest, bundle, and parent-guide hashes.
This command records an approval already given by a human; it does not grant or
infer approval itself.

Verify the lock at any time:

```bat
python worksheet-generator\review_pack.py verify ^
  --review-dir tmp\reviews\example-pack ^
  --require-approval
```

Any changed reviewed file or manifest fails verification and requires the full
pack and parent guide to be reviewed and approved again.

## 4. Promote manually to the permanent handoff branch

After approval, Muse manually copies or cherry-picks only the approved files,
manifest, and approval record into the appropriate permanent
`muse/*-handoff` branch. No script performs this irreversible step.

On the permanent handoff branch, run:

```bat
python worksheet-generator\review_pack.py check-promotion ^
  --review-dir tmp\reviews\example-pack
```

Promotion is allowed only when the current branch is a permanent
`muse/*-handoff` branch, all hashes still match, and the approval locks the
current manifest. Codex can then use the existing Muse → Git → Codex integration
and publishing workflow without any change.
