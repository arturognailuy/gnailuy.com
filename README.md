# gnailuy.com

Yuliang Jin's personal engineering blog, built as a responsive static site with Hugo.

## Build and verify

Requirements: Hugo Extended 0.165.0, Node.js 24, Python 3.

```sh
npm ci
hugo --minify --gc
npx playwright install chromium
npm test
```

The generated `public/` directory is the immutable deployment artifact. Read `AGENT.md` and `.aidoc/INDEX.md` before changing URLs, assets, templates, CI, or deployment behavior.
