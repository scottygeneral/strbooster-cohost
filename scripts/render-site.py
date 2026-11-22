"""Build the site with shared growth-system navigation and discovery-call CTAs.

The original renderer preserves resource, case-study and legal content.
templates/home.html is the homepage source (with figures from
partials/systems-ui.html inserted at <!--include:systems-ui#key--> markers);
templates/discovery.html supplies
only the main content for the existing contact page. Guest Intel remains a
resource, while the primary site-wide action is the discovery-call calendar.
"""
from pathlib import Path
import argparse
import html
import json
import re
import runpy

ROOT = Path(__file__).resolve().parent.parent
BOOKING_URL = 'https://api.leadconnectorhq.com/widget/booking/OnBzpe1qEasSowPwkxXU'
DISCOVERY_TITLE = 'Book a Discovery Call: STR Growth Systems'
DISCOVERY_DESCRIPTION = (
    'Book a 30-minute discovery call with STR Booster. Discuss your portfolio, '
    'your direct revenue and owner growth goals, and which growth system fits.'
)
HEADER = r'<header class="site-header(?: story-header)?">.*?</header>'
FOOTER = r'<footer class="site-footer(?: story-footer)?">.*?</footer>'
EXCLUDED_PAGES = {'index.html', 'STR Booster Website.dc.html', '404.html'}


def booking_link(placement: str = 'page-final') -> str:
    return (f'<a class="btn" href="{BOOKING_URL}" '
            f'data-cta="{html.escape(placement, quote=True)}">'
            'Let’s talk <svg class="sb-arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 18 18 6M6 6h12v12"/></svg></a>')


def replace_legacy_ctas(source: str) -> str:
    """Replace global acquisition CTAs without rewriting resource-specific links."""
    source = re.sub(
        r'<section class="dark cta-band">.*?</section>',
        '<section class="dark cta-band"><h2>What would make your rental business easier?</h2>'
        '<p>Let’s talk about more bookings, less repetitive work and the right '
        'AI systems for your business.</p><div class="actions">'
        + booking_link() + '</div><p class="note">Book a 30-minute discovery call.</p></section>',
        source, flags=re.S,
    )

    # Also clean already-generated output when --existing-only is used.
    # This does not touch the separate 52Rev waitlist or other business forms.
    def replace_form(match: re.Match) -> str:
        placement = re.search(r'data-guest-strategy=["\']([^"\']+)', match.group())
        return booking_link(placement.group(1) if placement else 'page-final')

    source = re.sub(
        r'<form\b(?=[^>]*\bdata-guest-strategy=)[^>]*>.*?</form>',
        replace_form, source, flags=re.S,
    )

    def replace_link(match: re.Match) -> str:
        anchor = match.group()
        href = re.search(r'\bhref=["\']([^"\']+)', anchor)
        if not href:
            return anchor
        label = re.sub(r'<[^>]+>', '', anchor)
        label = ' '.join(html.unescape(label).split())
        is_old_anchor = href.group(1) in {'/#guest-strategy', '#guest-strategy'}
        is_old_cta = 'guest-intel.strbooster.com' in href.group(1) and (
            'Get Started for Free' in label or 'Get my free Guest Strategy' in label
        )
        if is_old_anchor or is_old_cta:
            placement = re.search(r'data-cta=["\']([^"\']+)', anchor)
            return booking_link(placement.group(1) if placement else 'page-final')
        return anchor

    return re.sub(r'<a\b[^>]*>.*?</a>', replace_link, source, flags=re.S)


def apply_assets(source: str) -> str:
    """Use one shared stylesheet/script without loading the previous form UI."""
    source = re.sub(
        r'<link\b[^>]*\bhref=["\']/?(?:story|guest-strategy)\.css(?:\?[^"\']*)?["\'][^>]*>\s*',
        '', source, flags=re.I,
    )
    source = re.sub(
        r'<script\b[^>]*\bsrc=["\']/?(?:story|guest-strategy)\.js(?:\?[^"\']*)?["\'][^>]*>.*?</script>\s*',
        '', source, flags=re.I | re.S,
    )
    additions = []
    if not re.search(r'\bhref=["\']/growth\.css(?:\?[^"\']*)?["\']', source):
        additions.append('<link rel="stylesheet" href="/growth.css">')
    for asset in ('app.js', 'growth.js', 'reviews.js'):
        if not re.search(r'\bsrc=["\']/' + re.escape(asset) + r'(?:\?[^"\']*)?["\']', source):
            additions.append(f'<script src="/{asset}" defer></script>')
    if additions:
        source = source.replace('</head>', '\n'.join(additions) + '\n</head>', 1)
    return source


def apply_discovery(source: str, content: str, title: str = DISCOVERY_TITLE,
                    description: str = DISCOVERY_DESCRIPTION) -> str:
    """Keep the contact page's existing integrations and canonical URL."""
    source, count = re.subn(r'<main\b[^>]*>.*?</main>', lambda _: content.strip(),
                           source, count=1, flags=re.S)
    if count != 1:
        raise ValueError('The contact page must contain one main content element.')
    source = re.sub(r'<title>.*?</title>',
                    f'<title>{title} | STR Booster</title>', source, count=1, flags=re.S)
    for attr, key, value in (
        ('name', 'description', description),
        ('property', 'og:title', f'{title} | STR Booster'),
        ('property', 'og:description', description),
        ('property', 'og:image', 'https://strbooster.com/assets/ai-growth-social.png'),
        ('name', 'twitter:title', f'{title} | STR Booster'),
        ('name', 'twitter:description', description),
        ('name', 'twitter:image', 'https://strbooster.com/assets/ai-growth-social.png'),
    ):
        source = re.sub(
            rf'<meta\b[^>]*\b{attr}=["\']{key}["\'][^>]*>',
            f'<meta {attr}="{key}" content="{html.escape(value, quote=True)}">',
            source, count=1,
        )

    def update_schema(match: re.Match) -> str:
        data = json.loads(match.group(1))
        nodes = data.get('@graph', [data])
        for node in nodes:
            if node.get('@type') == 'WebPage':
                node.update(name=title, description=description)
            elif node.get('@type') == 'BreadcrumbList' and node.get('itemListElement'):
                node['itemListElement'][-1]['name'] = title
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'

    return re.sub(r'<script type="application/ld\+json">(.*?)</script>',
                  update_schema, source, flags=re.S)


def include_partials(source: str, root: Path) -> str:
    """Insert one <figure data-system="key"> from partials/systems-ui.html per marker."""
    partial = root / 'partials/systems-ui.html'
    figures = {}
    if partial.is_file():
        for match in re.finditer(r'<figure\b[^>]*\bdata-system="([^"]+)".*?</figure>',
                                 partial.read_text(encoding='utf-8'), flags=re.S):
            figures[match.group(1)] = match.group()

    def insert(match: re.Match) -> str:
        key = match.group(1)
        if key not in figures:
            raise ValueError(f'partials/systems-ui.html has no figure for {key!r}.')
        return figures[key]

    return re.sub(r'<!--include:systems-ui#([a-z-]+)-->', insert, source)


def apply_growth(root: Path) -> int:
    source = apply_assets(replace_legacy_ctas(include_partials(
        (root / 'templates/home.html').read_text(encoding='utf-8'), root
    )))
    header = re.search(HEADER, source, re.S)
    footer = re.search(FOOTER, source, re.S)
    if not header or not footer:
        raise ValueError('The homepage template must contain its shared header and footer.')
    overrides = {
        'get-expert-help.html': ('discovery.html', DISCOVERY_TITLE, DISCOVERY_DESCRIPTION),
        'growth-services.html': ('services.html', 'Short-Term Rental Growth Systems & Pricing',
            'Direct Revenue, Owner Acquisition and Growth Partner plans for STR managers with 10 to 100 doors, with starting prices, guarantees and a free Growth Audit.'),
        'owner-acquisition.html': ('owner-acquisition.html', 'Owner Acquisition for Vacation Rental Managers',
            'Win more owner contracts with an owner landing page, revenue estimates, AI follow-up and nurture for owners and realtors. Built and run for property managers.'),
        'our-approach.html': ('approach.html', 'How We Build Your Growth System',
            'Start with a free Growth Audit. STR Booster builds your direct revenue and owner acquisition systems around your PMS and markets, then runs them with you.'),
    }
    (root / 'index.html').write_text(source, encoding='utf-8')
    updated = 1
    for page in sorted(root.glob('*.html')):
        if page.name in EXCLUDED_PAGES:
            continue
        text = page.read_text(encoding='utf-8')
        if not re.search(HEADER, text, re.S):
            continue
        text = re.sub(HEADER, lambda _: header.group(), text, count=1, flags=re.S)
        text = re.sub(FOOTER, lambda _: footer.group(), text, count=1, flags=re.S)
        if page.name in overrides:
            template, title, description = overrides[page.name]
            text = apply_discovery(text, (root / 'templates' / template).read_text(encoding='utf-8'),
                                   title, description)
        text = apply_assets(replace_legacy_ctas(text))
        page.write_text(text, encoding='utf-8')
        updated += 1
    return updated


SITE = 'https://strbooster.com'
LOGO_URL = SITE + '/assets/logo-512.png'
# Offers published on the pricing pages. check-story.py confirms each price is
# still visible on the page, so the schema cannot drift from the copy.
OFFERS = {
    'growth-audit': ('Growth Audit', 0, None),
    'direct-revenue': ('Direct Revenue System', 3500, 750),
    'owner-system': ('Owner Acquisition System', 2500, 995),
    'growth-partner': ('Growth Partner', None, 2000),
}
SERVICE_PAGES = {
    'growth-services': ('Growth systems for short-term rental property managers',
                        ['growth-audit', 'direct-revenue', 'owner-system', 'growth-partner']),
    'owner-acquisition': ('Owner Acquisition System', ['owner-system']),
}
FAQ_SCHEMA_PAGES = {'growth-services', 'owner-acquisition', 'tools-partners'}
LINK = re.compile(r'(\bhref=")/([A-Za-z0-9_-]+)\.html([#?][^"]*)?"')


def offer_schema(key: str) -> dict:
    name, setup, monthly = OFFERS[key]
    prices = []
    if setup is not None:
        prices.append({'@type': 'UnitPriceSpecification', 'name': 'Setup' if setup else 'Free',
                       'price': setup, 'priceCurrency': 'USD'})
    if monthly is not None:
        spec = {'@type': 'UnitPriceSpecification', 'name': 'Monthly', 'price': monthly,
                'priceCurrency': 'USD', 'unitCode': 'MON',
                'referenceQuantity': {'@type': 'QuantitativeValue', 'value': 1, 'unitCode': 'MON'}}
        if setup is None:
            spec['name'] = 'Monthly, starting price'
        prices.append(spec)
    return {'@type': 'Offer', 'name': name, 'url': SITE + '/growth-services#' + key, 'priceCurrency': 'USD',
            'price': setup if setup is not None else monthly,
            'priceSpecification': prices, 'seller': {'@id': SITE + '/#organization'}}


def page_faqs(source: str) -> list:
    """Question and answer pairs from the visible FAQ block (not the nav dropdowns)."""
    block = re.search(r'<div class="faq">(.*?)</div>\s*</div>\s*</section>', source, re.S)
    if not block:
        return []
    pairs = []
    for summary, answer in re.findall(r'<details>\s*<summary>(.*?)</summary>(.*?)</details>', block.group(1), re.S):
        question = ' '.join(html.unescape(re.sub(r'<[^>]+>', '', summary)).split())
        text = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', answer)).split())
        if question and text:
            pairs.append((question, text))
    return pairs


def apply_search_polish(root: Path) -> None:
    """Final pass: canonical internal links and richer structured data."""
    for page in sorted(root.glob('*.html')):
        if page.name in {'STR Booster Website.dc.html'}:
            continue
        slug = page.stem
        text = page.read_text(encoding='utf-8')

        # Link to the canonical, extensionless URL that the sitemap and canonical tags use.
        def clean(match: re.Match) -> str:
            name, rest = match.group(2), match.group(3) or ''
            if not (root / f'{name}.html').is_file():
                return match.group()
            return f'{match.group(1)}{"/" if name == "index" else "/" + name}{rest}"'
        text = LINK.sub(clean, text)

        def update_schema(match: re.Match) -> str:
            data = json.loads(match.group(1))
            nodes = data.get('@graph', [data])
            canonical = SITE + ('/' if slug == 'index' else '/' + slug)
            for node in nodes:
                if node.get('@id') == SITE + '/#organization':
                    node['logo'] = {'@type': 'ImageObject', 'url': LOGO_URL, 'width': 512, 'height': 512}
                    node['contactPoint'] = {'@type': 'ContactPoint', 'contactType': 'sales',
                                            'email': 'info@strbooster.com', 'url': BOOKING_URL,
                                            'availableLanguage': 'English'}
            if slug in SERVICE_PAGES and not any(n.get('@type') == 'Service' for n in nodes):
                name, keys = SERVICE_PAGES[slug]
                nodes.append({'@type': 'Service', '@id': canonical + '#service', 'name': name, 'url': canonical,
                              'provider': {'@id': SITE + '/#organization'},
                              'audience': {'@type': 'BusinessAudience',
                                           'name': 'Short-term rental property managers with 10 to 100 units'},
                              'offers': [offer_schema(k) for k in keys]})
            if slug in FAQ_SCHEMA_PAGES and not any(n.get('@type') == 'FAQPage' for n in nodes):
                faqs = page_faqs(text)
                if faqs:
                    nodes.append({'@type': 'FAQPage', '@id': canonical + '#faq', 'mainEntity': [
                        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                        for q, a in faqs]})
            if '@graph' not in data:
                data = {'@context': 'https://schema.org', '@graph': nodes}
            return ('<script type="application/ld+json">'
                    + json.dumps(data, ensure_ascii=False).replace('<', '\\u003c') + '</script>')

        text = re.sub(r'<script type="application/ld\+json">(.*?)</script>', update_schema, text, flags=re.S)
        page.write_text(text, encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--existing-only', action='store_true',
                        help='Refresh existing HTML without running the original renderer.')
    args = parser.parse_args()
    if not args.existing_only:
        runpy.run_path(str(ROOT / 'scripts/render-pages.py'), run_name='__main__')
    print(f'Growth-system design and discovery-call CTAs applied to {apply_growth(ROOT)} pages.')
    apply_search_polish(ROOT)
    print('Internal links point at canonical URLs; FAQ, Service and Offer schema applied.')


if __name__ == '__main__':
    main()
