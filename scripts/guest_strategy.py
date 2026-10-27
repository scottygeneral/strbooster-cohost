"""Render the user-supplied Guest Intel GET widget before HTML is published.

This is a build-time enhancement, not a JavaScript-only CTA replacement.
The native form works without JavaScript. Submission navigates to Guest Intel;
it does not embed the report or promise an on-site result.
"""
import re

DESTINATION = 'https://guest-intel.strbooster.com/'
PLACEMENTS = {'hero', 'guest-insight', 'final', 'page-final'}


def form(location: str) -> str:
    if location not in PLACEMENTS:
        raise ValueError(f'Unknown Guest Strategy placement: {location}')
    ident = 'guest-strategy' if location == 'hero' else f'guest-strategy-{location}'
    theme = 'light' if location == 'guest-insight' else 'dark'
    return f'''<form id="{ident}" class="gs-form gs-form--{theme}" action="{DESTINATION}" method="GET" data-guest-strategy="{location}" aria-label="Get your free Guest Strategy">
  <label class="gs-label" for="{ident}-listing">Your Airbnb listing link</label>
  <div class="gs-fields">
    <input class="gs-input" id="{ident}-listing" type="url" name="listing" placeholder="Paste your Airbnb listing link…" required inputmode="url" autocomplete="url" autocapitalize="off" spellcheck="false" pattern="https?://.+" title="Enter a complete listing link beginning with https:// or http://." aria-describedby="{ident}-help {ident}-error">
    <button class="gs-submit" type="submit"><span>Get my free Guest Strategy</span><span class="gs-arrow" aria-hidden="true">↗</span></button>
  </div>
  <p class="gs-help" id="{ident}-help">Free to start. Continue in Guest Intel with your listing link.</p>
  <p class="gs-error" id="{ident}-error" aria-live="polite" hidden></p>
</form>'''


def enhance(source: str) -> str:
    """Replace only free-entry CTAs, preserving other links and integrations.

    Called for the homepage before shared-shell extraction and for each inner
    page after its existing CTA band is generated. Safe to run more than once.
    """
    def replace(match: re.Match) -> str:
        anchor = match.group(0)
        found = re.search(r'\bdata-cta="([^"]+)"', anchor)
        if not found:
            return anchor
        location = found.group(1)
        if location == 'navigation':
            return re.sub(r'\bhref="[^"]*"', 'href="/#guest-strategy"', anchor, count=1)
        return form(location) if location in PLACEMENTS else anchor

    source = re.sub(r'<a\b[^>]*>.*?</a>', replace, source, flags=re.S)
    if 'data-guest-strategy=' in source or 'href="/#guest-strategy"' in source:
        if 'href="/guest-strategy.css"' not in source:
            source = source.replace('</head>', '<link rel="stylesheet" href="/guest-strategy.css">\n</head>', 1)
        if 'src="/guest-strategy.js"' not in source:
            source = source.replace('</head>', '<script src="/guest-strategy.js" defer></script>\n</head>', 1)
    source = source.replace('<p class="v-micro">Start with your free Guest Intel report.</p>', '')
    return source
