#!/usr/bin/env python3
"""Copy only the public website files into _site/ for Netlify to publish.

Netlify used to publish the repository root, which exposed the README, build
scripts, templates, design briefs, uploads and review screenshots. This script
uses an allowlist: anything not listed here stays private. After copying, it
checks that every local file the published HTML, CSS and JS point to exists in
_site/, so a missing asset fails the build instead of breaking the live site.
"""
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '_site'

# Top-level file types that make up the site. Design-tool exports
# (*.dc.html) are excluded explicitly below.
PUBLIC_SUFFIXES = {'.html', '.css', '.js'}
PUBLIC_FILES = {'robots.txt', 'sitemap.xml', 'llms.txt', 'favicon.svg'}
EXCLUDED_FILES = {'STR Booster Website.dc.html'}
# Folders whose whole contents are served.
PUBLIC_DIRS = ['assets']

REF_PATTERN = re.compile(
    r'''(?:src|href|content)=["'](/[^"'#?]*)|url\(["']?(/[^)"'#?]+)'''
)
SITE_URL = re.compile(r'https://(?:www\.)?strbooster\.com(/[^"\'\s#?<)]*)')


def collect():
    files = []
    for path in sorted(ROOT.iterdir()):
        if not path.is_file() or path.name in EXCLUDED_FILES:
            continue
        if path.name.endswith('.dc.html'):
            continue
        if path.suffix in PUBLIC_SUFFIXES or path.name in PUBLIC_FILES:
            files.append(path)
    for folder in PUBLIC_DIRS:
        files.extend(p for p in sorted((ROOT / folder).rglob('*')) if p.is_file())
    return files


def resolves(url_path):
    """True when a site path like /assets/x.png or /52rev exists in _site."""
    rel = url_path.lstrip('/')
    if rel == '':
        return (OUT / 'index.html').exists()
    target = OUT / rel
    if target.is_file():
        return True
    if target.is_dir() and (target / 'index.html').exists():
        return True
    # Netlify pretty URLs: /52rev serves 52rev.html.
    return (OUT / f'{rel}.html').exists()


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    files = collect()
    for src in files:
        dest = OUT / src.relative_to(ROOT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    # Paths handled by netlify.toml redirects rather than files.
    redirected = {'/community', '/community.html'}
    missing = set()
    for page in OUT.glob('*.html'):
        text = page.read_text(encoding='utf-8')
        refs = {a or b for a, b in REF_PATTERN.findall(text)}
        refs |= set(SITE_URL.findall(text))
        for ref in refs:
            if ref.startswith('//') or ref in redirected:
                continue
            if not resolves(ref):
                missing.add(f'{page.name} -> {ref}')

    pages = len(list(OUT.glob('*.html')))
    print(f'Published {len(files)} files ({pages} HTML pages) to _site/.')
    if missing:
        print('FAIL: published pages reference files that are not in _site/:')
        for item in sorted(missing):
            print(f'  {item}')
        sys.exit(1)
    print('PASS: every local link and asset in the published pages resolves.')


if __name__ == '__main__':
    main()
