"""Dependency-free publication checks. Run after render-site.py."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import json

ROOT = Path(__file__).resolve().parent.parent
BOOKING_URL = 'https://api.leadconnectorhq.com/widget/booking/OnBzpe1qEasSowPwkxXU'
REQUIRED_SECTIONS = ('main', 'benefits', 'how-it-works', 'owner-control',
                     'for-managers', 'lets-talk')
LEGACY_ASSETS = {'/story.css', '/story.js', '/guest-strategy.css', '/guest-strategy.js'}
MEDIA_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif',
                    '.svg', '.ico', '.mp4', '.webm', '.woff', '.woff2'}


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.ids = []
        self.json_blocks = []
        self.json_errors = []
        self._json = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self._json = ''

    def handle_data(self, data):
        if self._json is not None:
            self._json += data

    def handle_endtag(self, tag):
        if tag == 'script' and self._json is not None:
            try:
                self.json_blocks.append(json.loads(self._json))
            except json.JSONDecodeError as error:
                self.json_errors.append(str(error))
            self._json = None


def check(root, content_only=False):
    root = Path(root)
    texts = {p.name: p.read_text(encoding='utf-8') for p in sorted(root.glob('*.html'))}
    docs = {name: Document(text) for name, text in texts.items()}
    text, doc = texts['index.html'], docs['index.html']
    errors = []
    skipped_media = set()

    def require(test, message):
        if not test:
            errors.append(message)

    require(sum(tag == 'h1' for tag, _ in doc.tags) == 1, 'Homepage must have one H1.')
    for ident in REQUIRED_SECTIONS:
        require(ident in doc.ids, f'Homepage is missing section: {ident}')
    require(not any(tag in {'picture', 'video'} for tag, _ in doc.tags),
            'Homepage must use product visuals without lifestyle imagery or video.')
    for tag, attrs in doc.tags:
        if tag in {'img', 'image'}:
            src = attrs.get('src', attrs.get('href', ''))
            require(urlsplit(src).path.lower().endswith('.svg'),
                    'Homepage image elements may contain vector icons only.')
    require('data-hero-video' not in text, 'Previous hero film must not be loaded.')
    require('Get Started for Free' not in text and 'Get my free Guest Strategy' not in text,
            'Homepage must lead to a discovery call rather than the previous free entry.')
    require(not any(tag == 'form' for tag, _ in doc.tags),
            'Homepage discovery-call CTA must be a direct, accessible link.')
    require('client-results' not in text and 'case-study-' not in text and 'sb-proof' not in text,
            'Homepage must not contain client stories or results promotions.')
    home_canonicals = [a for tag, a in doc.tags if tag == 'link' and a.get('rel') == 'canonical']
    require(len(home_canonicals) == 1 and home_canonicals[0].get('href') == 'https://strbooster.com/',
            'Homepage canonical must uniquely identify the live home URL.')
    require(len(doc.json_blocks) == 1 and not doc.json_errors,
            'Homepage needs one valid structured-data block.')
    if len(doc.json_blocks) == 1:
        schema = doc.json_blocks[0]
        nodes = schema.get('@graph', [schema]) if isinstance(schema, dict) else []
        types = {node.get('@type') for node in nodes if isinstance(node, dict) and isinstance(node.get('@type'), str)}
        require({'Organization', 'WebSite', 'WebPage'} <= types,
                'Homepage structured data must describe the organisation, site and page.')

    managed = {name: page for name, page in docs.items()
               if name != 'STR Booster Website.dc.html'
               and any(tag == 'header' and 'site-header' in attrs.get('class', '').split()
                       for tag, attrs in page.tags)}
    require('index.html' in managed, 'Homepage shared navigation is missing.')
    require('get-expert-help.html' in managed, 'Discovery-call contact page is missing.')
    for name, page in managed.items():
        page_text = texts[name]
        require(not [key for key, n in Counter(page.ids).items() if n > 1],
                f'{name}: duplicate HTML IDs.')
        require(not page.json_errors, f'{name}: invalid structured data.')
        require('GTM-55FK2NZ' in page_text and 'G-YQ9L9GHV31' in page_text,
                f'{name}: existing analytics identifiers missing.')
        navigation = [a for tag, a in page.tags if tag == 'a' and a.get('data-cta') == 'navigation']
        require(len(navigation) == 1 and navigation[0].get('href') == BOOKING_URL,
                f'{name}: navigation CTA must open the verified discovery-call calendar.')
        scripts = [urlsplit(a.get('src', '')).path for tag, a in page.tags if tag == 'script']
        styles = [urlsplit(a.get('href', '')).path for tag, a in page.tags
                  if tag == 'link' and a.get('rel') == 'stylesheet']
        require(scripts.count('/app.js') == 1 and scripts.count('/growth.js') == 1,
                f'{name}: load the shared integration and motion scripts once each.')
        require(styles.count('/growth.css') == 1, f'{name}: shared growth stylesheet missing or duplicated.')
        require(not LEGACY_ASSETS.intersection(scripts + styles),
                f'{name}: old story or Guest Strategy assets are still loaded.')
        require(not any(tag == 'form' and 'data-guest-strategy' in a for tag, a in page.tags),
                f'{name}: obsolete free-report form remains.')
        footer = page_text.split('<footer', 1)[-1].split('</footer>', 1)[0]
        for destination in ('/privacy.html', '/terms.html', 'https://www.instagram.com/strbooster/',
                            'https://www.youtube.com/@strbooster'):
            require(destination in footer, f'{name}: footer is missing {destination}')
        for tag, attrs in page.tags:
            if tag == 'a' and attrs.get('data-cta') in {'navigation', 'hero', 'final', 'page-final'}:
                require(attrs.get('href') == BOOKING_URL,
                        f'{name}: primary CTA must use the discovery-call destination.')
            for attr in ('href', 'src', 'data-src', 'action', 'poster'):
                value = attrs.get(attr, '')
                if not value:
                    continue
                url = urlsplit(value)
                if url.scheme or url.netloc:
                    continue
                require(value != '#', f'{name}: placeholder link has no destination.')
                relative = unquote(url.path).lstrip('/')
                target = root / (relative or name)
                if url.path == '/':
                    target = root / 'index.html'
                elif url.path.startswith('/.netlify/functions/'):
                    # Netlify maps this public route to the checked-in handler.
                    target = root / 'netlify/functions' / (url.path.rsplit('/', 1)[-1] + '.js')
                if not target.is_file():
                    if content_only and name != 'index.html' and target.suffix.lower() in MEDIA_EXTENSIONS:
                        skipped_media.add(relative)
                    else:
                        require(False, f'{name}: missing local target {value}')
                if url.fragment and target.suffix == '.html' and target.is_file():
                    target_doc = docs.get(target.name)
                    if target_doc is None:
                        target_doc = Document(target.read_text(encoding='utf-8'))
                    require(unquote(url.fragment) in target_doc.ids,
                            f'{name}: missing anchor {value}')

    discovery = texts.get('get-expert-help.html', '')
    require(BOOKING_URL in discovery and 'mailto:david@strbooster.com' in discovery,
            'Discovery page requires the verified calendar and an email alternative.')
    require('30-minute' in discovery, 'Discovery page must explain the call duration.')
    if errors:
        raise AssertionError('\n'.join(errors))
    print(f'PASS: {len(managed)} pages; discovery CTAs, shared assets, schema, anchors and analytics.')
    if skipped_media:
        print(f'Legacy media not checked in this snapshot: {len(skipped_media)} asset(s). '
              'Homepage and all local code/link targets were checked.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--content-only', action='store_true',
                        help='Skip missing legacy media only; still verify homepage assets, code and links.')
    check(ROOT, parser.parse_args().content_only)
