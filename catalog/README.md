# Resource catalog

This directory is the modular source model introduced by Phase 1, Migration Step 1. Each resource has one JSON definition beneath `resources/<grade>/<subject>/<topic>/`. Shared grade, subject, topic, and skill definitions live under `taxonomy/`; deployment-wide URL settings live in `site.json`.

Step 1 is deliberately disconnected from the production site. `directory.js`, sitemap generation, navigation, search, resource routes, and the R2 publisher continue to use their existing inputs. The catalog becomes a production input only in a later, separately reviewed migration step.

Run the dependency-free checks from the repository root:

```text
python site-tools/validate_catalog.py
python site-tools/check_catalog_parity.py
```

The validator checks schema rules, taxonomy references, unique IDs and ordering, asset/page counts, preview conventions, source contracts, and required files. The parity check separately requires the 41 published definitions to match the current live registry and all 42 definitions (including the retired `story-comprehension` resource) to match the existing publisher asset contracts.

Migration Step 2 adds a shadow-only generator. It writes deterministic artifacts beneath `tmp/catalog-shadow` and never updates a production input or site file:

```text
python site-tools/generate_shadow_outputs.py
python site-tools/check_shadow_parity.py
```

The compatibility section in `site.json` records current query URL, topic-route override, singleton-topic, and sitemap ordering behavior. These rules preserve existing behavior during shadow parity and can be retired only in a later URL migration.

Migration Step 3 keeps the public synchronous JavaScript API while replacing the hand-maintained resource block in `directory.js` with catalog-generated compatibility data:

```text
python site-tools/generate_production_runtime.py
```

The generated block retains the current registry ordering, resource SEO fields, query URLs, asset paths, page labels, and object shape. Directory rendering, search, canonical handling, navigation, and routing remain hand-written and unchanged during this step.

Migration Step 4 also emits `worksheetDirectoryTaxonomy` into the same synchronous compatibility block. Grade, subject, planned-topic, skill, directory-file, and special-route data now comes from the authoritative taxonomy and site compatibility configuration. The rendering code still owns presentation copy and markup.

Discoverability Phase 1 prepares each definition for future static resource pages without changing production output. The existing `description` is the concise human-authored resource summary, and `seo.title` and `seo.description` remain explicit authored metadata. Published resources also require an immutable `routing.slug`, optional aliases, publication dates, and at least one concise `learningFocus` statement. `adultGuidance`, `language`, `resourceType`, `seo.socialImage`, per-page `previewAlt`, and curated `relatedResources` are overrides and should be omitted unless a resource needs them.

Technical values stay derived: page count comes from `pages`, language defaults to `en`, resource type follows the page count, the first preview is the default social image, and preview alt text combines the page label with the resource title. Related resources are selected deterministically from published catalog order unless a curated override exists. These derivations live in `site-tools/resource_discoverability.py`; they are not connected to production pages until the separately reviewed static-page phase.

Discoverability Phase 2 generates semantic resource pages for review under `tmp/resource-pages-shadow`. It does not change production routes, canonicals, sitemaps, navigation, search, or publisher inputs:

```text
python site-tools/generate_static_resource_pages.py
python site-tools/validate_static_resource_pages.py
python -m unittest site-tools.tests.test_static_resource_pages
```

The proposed clean URL is `/resources/{slug}/`, represented on disk as `resources/{slug}/index.html`. The shadow manifest maps every published catalog resource to its clean path and content hash. Retired resources are excluded. Technical metadata, preview alt text, asset URLs, page counts, structured data, and related resources are derived from the catalog rather than maintained separately.

The coordinated production migration uses the validated shadow output as its exact source. It writes one page per published resource, copies the shared resource-page stylesheet and navigation behavior, and generates clean resource sitemap entries:

```text
python site-tools/generate_production_resource_pages.py
python site-tools/generate_production_runtime.py
python site-tools/validate_production_resource_pages.py
```

Generated runtime records use `resources/{slug}/` for current links and retain `resource-preview.html?resource={id}` as `legacyPreviewHref`. The legacy preview remains functional and derives its canonical from the current clean `previewHref`.
