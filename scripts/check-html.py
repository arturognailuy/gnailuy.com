#!/usr/bin/env python3
"""Run html-validate against canonical pages, excluding Hugo alias redirects."""
from pathlib import Path
import subprocess
pages=[]
for page in Path('public').rglob('*.html'):
    head=page.read_text(errors='replace')[:600].lower()
    if 'http-equiv=refresh' not in head:
        pages.append(str(page))
raise SystemExit(subprocess.call(['npx','html-validate',*pages]))
