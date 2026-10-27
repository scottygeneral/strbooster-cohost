"""Create a portable, analytics-free HTML review of the actual homepage.
--embed-images makes an offline image review; Google Fonts retains its fallback.
"""
from pathlib import Path
import argparse
import base64
import mimetypes
import re

ROOT = Path(__file__).resolve().parent.parent
RAW = 'https://raw.githubusercontent.com/scottygeneral/strbooster-cohost/main/'


def build(root=ROOT, embed=False):
    source = (root / 'index.html').read_text(encoding='utf-8')
    source = re.sub(r'<noscript>.*?</noscript>', '', source, flags=re.S)
    source = re.sub(r'<script\b(?![^>]*type="application/ld\+json")[^>]*>.*?</script>', '', source, flags=re.S)
    source = re.sub(r'<link rel="canonical"[^>]*>', '', source)
    source = source.replace('<head>', '<head>\n<meta name="robots" content="noindex,nofollow">')
    source = source.replace('<title>', '<title>DESIGN REVIEW — ')
    for name in ('story.css', 'guest-strategy.css'):
        source = source.replace(f'<link rel="stylesheet" href="/{name}">',
                                '<style>\n' + (root / name).read_text() + '\n</style>')
    def media(match):
        attr, path = match.groups()
        file = root / path.lstrip('/')
        if embed and file.is_file():
            mime = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
            data = base64.b64encode(file.read_bytes()).decode('ascii')
            return f'{attr}="data:{mime};base64,{data}"'
        return f'{attr}="{RAW}{path.lstrip(chr(47))}"'
    source = re.sub(r'(src|href)="(/(?:assets/[^\"]+|favicon.svg))"', media, source)
    source = source.replace('href="/#', 'href="#')
    source = re.sub(r'href="/(?!/)([^\"]*)"', r'href="https://strbooster.com/\1"', source)
    source = re.sub(r'<details class="v-review-disclosure".*?</details>',
                    '<p><a class="v-text-link" href="https://strbooster.com/client-results.html">Read client stories ↗</a></p>', source, flags=re.S)
    scripts = '\n'.join('<script>\n' + (root / name).read_text() + '\n</script>'
                        for name in ('story.js', 'guest-strategy.js'))
    source = source.replace('</body>', scripts + '\n</body>')
    destination = root / 'previews/index.html'
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(source, encoding='utf-8')
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--embed-images', action='store_true')
    print(build(embed=parser.parse_args().embed_images))
