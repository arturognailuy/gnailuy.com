# Agent Instructions

- Read `.aidoc/INDEX.md` before changing the site.
- Preserve every published post URL. `content/posts/*.md` contains explicit `url` values copied from the legacy release.
- Keep only author-provided source images under `assets/images/_fullsize/`; generated image files MUST NOT be committed.
- Authors reference images by their source filename with Markdown such as `![Alt text](/images/photo.jpg)`; Hugo owns generated responsive variants and filenames.
- Build with Hugo Extended 0.165.0 and run `npm test` before opening a PR.
- Run the desktop and mobile Playwright scenarios after UI changes and inspect their screenshots.
- Never deploy uncommitted or unverified work. An immutable artifact from an open PR may be deployed to `test.gnailuy.com` only after the full local gates pass and Yuliang explicitly requests the preview. Production promotion requires a merged default-branch commit and separate explicit approval.
