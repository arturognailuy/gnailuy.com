# Agent Instructions

- Read `.aidoc/INDEX.md` before changing the site.
- Preserve every published post URL. `content/posts/*.md` contains explicit `url` values copied from the legacy release.
- Preserve files in `static/images/` whose names include content hashes; published pages may link to those legacy assets.
- Build with Hugo Extended 0.165.0 and run `npm test` before opening a PR.
- Run the desktop and mobile Playwright scenarios after UI changes and inspect their screenshots.
- Do not deploy to `test.gnailuy.com` or `gnailuy.com` from a development branch. Production promotion requires explicit approval.
