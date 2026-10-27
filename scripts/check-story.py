"""Dependency-free regression checks for the story-led homepage.
Run after render-site.py. --content-only omits the complete-checkout link check.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import json

ROOT = Path(__file__).resolve().parent.parent


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.ids = []
        self.json_blocks = []
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
            self.json_blocks.append(json.loads(self._json))
            self._json = None


def check(root, content_only=False):
    text = (root / 'index.html').read_text(encoding='utf-8')
    doc = Document(text)
    errors = []
    def require(test, message):
        if not test:
            errors.append(message)
    require(sum(tag == 'h1' for tag, _ in doc.tags) == 1, 'Homepage must have one H1.')
    require(not [key for key, n in Counter(doc.ids).items() if n > 1], 'Duplicate HTML IDs.')
    for ident in ('main', 'the-story', 'know-your-guest', 'build-the-brand', 'build-the-funnel', 'client-results'):
        require(ident in doc.ids, f'Missing section: {ident}')
    links = [attrs for tag, attrs in doc.tags if tag == 'a']
    free_links = [a for a in links if a.get('data-cta') in ('navigation', 'hero', 'guest-insight', 'final')]
    require(len(free_links) == 4, 'Expected four primary free-report CTAs.')
    require(all(a.get('href') == 'https://guest-intel.strbooster.com/' for a in free_links), 'Free-report destination changed.')
    require('AI-powered property manager' not in text, 'Obsolete property-manager positioning.')
    require('Own the rental.' not in text, 'Obsolete homepage headline.')
    require('Illustrative example' in text, 'Guest-profile example must be labelled.')
    require('GTM-55FK2NZ' in text and 'G-YQ9L9GHV31' in text, 'Existing analytics identifiers missing.')
    require(sum(tag == 'link' and a.get('rel') == 'canonical' for tag, a in doc.tags) == 1, 'Canonical must be unique.')
    require(len(doc.json_blocks) == 1, 'Expected one valid structured-data block.')
    steps = [a for tag, a in doc.tags if tag == 'button' and 'data-step' in a]
    require(len(steps) == 4, 'Four funnel steps required.')
    for step in steps:
        require('panel-' + step['data-step'] in doc.ids, f'Missing panel for {step["data-step"]}')
    for tag, attrs in doc.tags:
        if tag == 'img':
            require('alt' in attrs and 'width' in attrs and 'height' in attrs, 'Images require alt and dimensions.')
        for attr in ('href', 'src', 'data-src'):
            value = attrs.get(attr, '')
            if not value:
                continue
            url = urlsplit(value)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            target = root / (path.lstrip('/') or 'index.html')
            if not content_only:
                require(target.is_file(), f'Missing local target: {value}')
            if url.fragment and target.name == 'index.html':
                require(url.fragment in doc.ids, f'Missing homepage anchor: {value}')
    if not (root / 'assets/strbooster-hero-film.mp4').exists():
        require('data-hero-video' not in text, 'Missing film must not be requested.')
    if errors:
        raise AssertionError('\n'.join(errors))
    print(f'PASS: story structure, 4 CTAs, 4 funnel steps, schema, accessibility markup'
          + (' (content-only; assets/other pages not checked).' if content_only else ', local links and assets.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--content-only', action='store_true')
    check(ROOT, parser.parse_args().content_only)
