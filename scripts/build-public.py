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
import zipfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '_site'

# Top-level file types that make up the site. Design-tool exports
# (*.dc.html) are excluded explicitly below.
PUBLIC_SUFFIXES = {'.html', '.css', '.js'}
PUBLIC_FILES = {'robots.txt', 'sitemap.xml', 'llms.txt', 'favicon.svg'}
EXCLUDED_FILES = {'STR Booster Website.dc.html'}
# Folders whose whole contents are served.
PUBLIC_DIRS = ['assets', 'skills']
PLACEHOLDER_MARK = 'STATUS: placeholder'

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


def skill_name(skill_md, fallback):
    """The name in a SKILL.md's front matter; Claude expects the zip folder to match it."""
    m = re.search(r'^name:\s*(.+)$', skill_md, re.M)
    return m.group(1).strip().strip('"') if m else fallback


def write_zip(dest, entries):
    """entries: (path inside the zip, bytes). Fixed timestamps keep rebuilds identical."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zf:
        for arcname, data in entries:
            info = zipfile.ZipInfo(arcname, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)


def build_skill_zips():
    """Package every Claude skill as /skills/<slug>.zip, ready to upload to Claude.

    Multi-file skills: skills/<slug>/ (SKILL.md plus scripts, templates, samples).
    Single-file kits: assets/kits/<slug>.md becomes <name>/SKILL.md in the zip.
    Placeholders are skipped.
    """
    made = []
    for folder in sorted(p for p in (ROOT / 'skills').iterdir() if p.is_dir()):
        skill_md = folder / 'SKILL.md'
        if not skill_md.is_file():
            continue
        text = skill_md.read_text(encoding='utf-8')
        if PLACEHOLDER_MARK in text:
            continue
        name = skill_name(text, folder.name)
        entries = [(f'{name}/{p.relative_to(folder).as_posix()}', p.read_bytes())
                   for p in sorted(folder.rglob('*')) if p.is_file()]
        write_zip(OUT / 'skills' / f'{folder.name}.zip', entries)
        made.append(folder.name)
    for kit in sorted((ROOT / 'assets' / 'kits').glob('*.md')):
        text = kit.read_text(encoding='utf-8')
        if PLACEHOLDER_MARK in text:
            continue
        write_zip(OUT / 'skills' / f'{kit.stem}.zip', [(f'{skill_name(text, kit.stem)}/SKILL.md', text.encode('utf-8'))])
        made.append(kit.stem)
    return made


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
    zips = build_skill_zips()

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
    print(f'Packaged {len(zips)} Claude skills as /skills/*.zip: {", ".join(zips)}')
    if missing:
        print('FAIL: published pages reference files that are not in _site/:')
        for item in sorted(missing):
            print(f'  {item}')
        sys.exit(1)
    print('PASS: every local link and asset in the published pages resolves.')


if __name__ == '__main__':
    main()
