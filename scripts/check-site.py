#!/usr/bin/env python3
"""Validate generated URL coverage and internal references."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []
        self.srcsets: list[str] = []
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        key = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if key and values.get(key): self.values.append(values[key] or "")
        if tag == "img" and values.get("srcset"):
            self.srcsets.extend(item.strip().rsplit(" ", 1)[0] for item in (values["srcset"] or "").split(","))

def output_path(url: str) -> Path:
    clean = url.split("?", 1)[0].split("#", 1)[0]
    if clean == "/": return PUBLIC / "index.html"
    if clean.endswith("/"): return PUBLIC / clean.lstrip("/") / "index.html"
    return PUBLIC / clean.lstrip("/")

def main() -> int:
    failures: list[str] = []
    required = ["/", "/archive/", "/about/", "/404.html", "/50x.html", "/index.xml", "/sitemap.xml"]
    for post in (ROOT / "content/posts").glob("*.md"):
        _, frontmatter, _ = post.read_text().split("---", 2)
        required.append(yaml.safe_load(frontmatter)["url"])
    for url in required:
        if not output_path(url).is_file(): failures.append(f"missing expected URL: {url}")
    for page in PUBLIC.rglob("*.html"):
        parser = References(); parser.feed(page.read_text(errors="replace"))
        for value in parser.values + parser.srcsets:
            if not value.startswith("/") or value.startswith("//"): continue
            target = output_path(value)
            if not target.exists(): failures.append(f"{page.relative_to(PUBLIC)} -> {value}")
    source_dir = ROOT / "assets/images/_fullsize"
    static_image_dir = ROOT / "static/images"
    if static_image_dir.exists() and any(static_image_dir.iterdir()):
        failures.append("generated or duplicate images are tracked under static/images")
    referenced_sources: set[str] = set()
    pattern = re.compile(r"!\[[^]]*]\(/images/([^ )]+)(?:\s+[^)]*)?\)")
    for post in (ROOT / "content/posts").glob("*.md"):
        referenced_sources.update(pattern.findall(post.read_text()))
    tracked_sources = {path.name for path in source_dir.iterdir() if path.is_file()}
    for name in sorted(referenced_sources | tracked_sources):
        source = source_dir / name
        published_source = PUBLIC / "images" / name
        if not source.is_file(): failures.append(f"missing author image: {source.relative_to(ROOT)}")
        if not published_source.is_file(): failures.append(f"missing published source image: {published_source.relative_to(PUBLIC)}")
    unused = tracked_sources - referenced_sources
    if unused: failures.append(f"unreferenced author images: {', '.join(sorted(unused))}")
    if failures:
        print("\n".join(sorted(set(failures))), file=sys.stderr); return 1
    print(f"validated {len(required)} expected URLs and {len(list(PUBLIC.rglob('*.html')))} HTML files")
    return 0
if __name__ == "__main__": raise SystemExit(main())
