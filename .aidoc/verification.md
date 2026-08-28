---
domain: Workflows
status: Active
entry_points:
  - .github/workflows/verify.yml
  - scripts/check-site.py
  - tests/site.spec.js
dependencies:
  - .aidoc/site-architecture.md
---

# Verification

Verification treats the generated site as a user-visible artifact rather than trusting template compilation alone. CI checks deterministic construction, expected URLs, internal links, HTML structure, and responsive browser behavior before a release can be reviewed.

## Related Docs

| Document | Relationship |
|---|---|
| [Site Architecture](site-architecture.md) | Defines the invariants the checks protect |
| [INDEX](INDEX.md) | Documentation discovery and reading chains |

## Why Verification Is Layered

A successful Hugo command does not prove that migrated URLs exist, images resolve, markup is usable, or mobile navigation works. The layered gates keep failures attributable: Hugo owns generation, the Python checker owns artifact integrity, html-validate owns markup quality, and Playwright owns black-box rendering.

External links are not a blocking gate because many historical posts intentionally reference old third-party resources. Internal links are blocking because this repository controls their targets.

## What CI Verifies

`hugo --minify --gc` builds the artifact with the pinned Extended release. `scripts/check-site.py` verifies all explicit post URLs, required pages, and local `href` and `src` targets.

`html-validate` checks every generated HTML file. The configuration relaxes presentational rules that conflict with historical article HTML while retaining document, nesting, attribute, and accessibility-oriented checks.

`tests/site.spec.js` loads the built artifact at desktop and mobile viewports, checks primary navigation, verifies representative articles and generated error pages, proves the legacy 404-to-archive redirect, and rejects horizontal page overflow. Playwright saves screenshots for inspection.

The representative article check also asserts that the configured Google Analytics, responsive AdSense, and Disqus integration points are present without depending on successful third-party network responses.

## How to Run the Gates

Run `hugo --minify --gc`, then `npm test`. For browser-only iteration, run `npm run test:browser`; Playwright starts a local server from `public/`.

CI uploads browser screenshots even when a scenario fails. A release reviewer should inspect both desktop and mobile captures before staging the artifact.
