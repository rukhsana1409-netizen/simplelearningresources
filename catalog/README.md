# Resource catalog

This directory is the modular source model introduced by Phase 1, Migration Step 1. Each resource has one JSON definition beneath `resources/<grade>/<subject>/<topic>/`. Shared grade, subject, topic, and skill definitions live under `taxonomy/`; deployment-wide URL settings live in `site.json`.

Step 1 is deliberately disconnected from the production site. `directory.js`, sitemap generation, navigation, search, resource routes, and the R2 publisher continue to use their existing inputs. The catalog becomes a production input only in a later, separately reviewed migration step.

Run the dependency-free checks from the repository root:

```text
python site-tools/validate_catalog.py
python site-tools/check_catalog_parity.py
```

The validator checks schema rules, taxonomy references, unique IDs and ordering, asset/page counts, preview conventions, source contracts, and required files. The parity check separately requires the 41 published definitions to match the current live registry and all 42 definitions (including the retired `story-comprehension` resource) to match the existing publisher asset contracts.

`site-tools/migrate_catalog_step1.py` documents the one-time bootstrap used for this migration. It refuses to overwrite any existing resource definition.

Migration Step 2 adds a shadow-only generator. It writes deterministic artifacts beneath `tmp/catalog-shadow` and never updates a production input or site file:

```text
python site-tools/generate_shadow_outputs.py
python site-tools/check_shadow_parity.py
```

The compatibility section in `site.json` records current query URL, topic-route override, singleton-topic, and sitemap ordering behavior. These rules preserve existing behavior during shadow parity and can be retired only in a later URL migration.
