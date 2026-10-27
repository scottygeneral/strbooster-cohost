"""Build the legacy resource pages, then apply the brand-and-funnel design.

The original renderer is preserved verbatim in render-pages.py. The canonical
homepage is templates/home.html. No third-party Python packages are required.
"""
from pathlib import Path
import argparse
import re
import runpy

ROOT = Path(__file__).resolve().parent.parent
FILM = Path('assets/strbooster-hero-film.mp4')


def apply_story(root: Path) -> int:
    """Render the homepage and synchronize the shared navigation and footer."""
    source = (root / 'templates/home.html').read_text(encoding='utf-8')
    if (root / FILM).is_file():
        source = source.replace('<!-- HERO_FILM -->',
            '<video data-hero-video data-src="/assets/strbooster-hero-film.mp4" '
            'muted loop playsinline preload="none" aria-hidden="true"></video>')
        source = source.replace('<!-- HERO_CONTROL -->',
            '<button type="button" class="s-video-toggle" data-video-toggle hidden '
            'aria-label="Play background film">Play background film</button>')
    header = re.search(r'<header class="site-header story-header">.*?</header>', source, re.S)
    footer = re.search(r'<footer class="site-footer story-footer">.*?</footer>', source, re.S)
    if not header or not footer:
        raise ValueError('The homepage template must contain its shared header and footer.')
    (root / 'index.html').write_text(source, encoding='utf-8')
    updated = 1
    for page in sorted(root.glob('*.html')):
        if page.name in {'index.html', 'STR Booster Website.dc.html', '404.html'}:
            continue
        text = page.read_text(encoding='utf-8')
        # Leave standalone/legal documents without the shared shell untouched.
        if not re.search(r'<header class="site-header(?: story-header)?">', text):
            continue
        text = re.sub(r'<header class="site-header(?: story-header)?">.*?</header>',
                      lambda _: header.group(), text, count=1, flags=re.S)
        text = re.sub(r'<footer class="site-footer(?: story-footer)?">.*?</footer>',
                      lambda _: footer.group(), text, count=1, flags=re.S)
        if 'href="/story.css"' not in text:
            text = text.replace('</head>', '<link rel="stylesheet" href="/story.css">\n</head>', 1)
        if 'src="/story.js"' not in text:
            text = text.replace('</head>', '<script src="/story.js" defer></script>\n</head>', 1)
        # Consistent site-wide free entry point; keep community pages and their links.
        text = re.sub(r'<section class="dark cta-band">.*?</section>',
            '<section class="dark cta-band"><h2>Start with the guest. Build from there.</h2>'
            '<p>Get your free Guest Intel snapshot, then turn the insight into a clearer '
            'brand and a more connected booking journey.</p><div class="actions">'
            '<a class="btn" href="https://guest-intel.strbooster.com/" data-cta="page-final">'
            'Get Started for Free</a><a class="btn secondary" href="/get-expert-help.html">'
            'Discuss your project</a></div></section>', text, flags=re.S)
        page.write_text(text, encoding='utf-8')
        updated += 1
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--existing-only', action='store_true',
                        help='Refresh already generated HTML without running the original renderer.')
    args = parser.parse_args()
    if not args.existing_only:
        runpy.run_path(str(ROOT / 'scripts/render-pages.py'), run_name='__main__')
    count = apply_story(ROOT)
    print(f'Brand + funnel story applied to {count} pages.')


if __name__ == '__main__':
    main()
