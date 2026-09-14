"""Search metadata and crawl files for the static STR Booster site."""
import html
import json
import re

BASE = 'https://strbooster.com'
META = {
 'index': ('Vacation Rental Growth & Automation', 'Grow your vacation rental with guest insights, revenue management, listing optimization and automation. Explore expert services and a free host community.'),
 'our-approach': ('Vacation Rental Growth Strategy', 'Connect guest positioning, pricing, marketing and automation in one vacation rental growth strategy. Build a more valuable stay and a stronger business.'),
 'growth-services': ('Vacation Rental Consulting & Growth Services', 'Explore vacation rental consulting for listing optimization, revenue management, automation and direct booking websites. Choose focused or ongoing support.'),
 'listing-optimization': ('Airbnb & Vacation Rental Listing Optimization', 'Improve your vacation rental listing with ideal guest positioning, copy, photo strategy and amenity priorities. Get focused help from STR Booster.'),
 'revenue-management': ('Vacation Rental Revenue Management Services', 'Connect vacation rental pricing, minimum stays, seasonal marketing and channel distribution. Get revenue management support built around your property.'),
 'technology-automation': ('Short-Term Rental Automation & PMS Optimization', 'Improve your PMS, CRM and guest workflows with short-term rental automation. Connect marketing, social media and defined AI tasks around your operation.'),
 'websites-funnels': ('Vacation Rental Websites & Direct Booking Funnels', 'Build a vacation rental website with booking pathways, lead capture, CRM, chatbots and automated follow-up. Turn guest interest into booking opportunities.'),
 'our-apps': ('Vacation Rental Apps: Guest Intel & 52Rev', 'Explore Guest Intel for ideal guest insights and 52Rev for weekly revenue marketing. Specialist apps developed by STR Booster to complement your growth plan.'),
 'guest-intel': ('Guest Intel: Find Your Ideal Vacation Rental Guest', 'Identify your ideal vacation rental guest with Guest Intel. Apply guest insights to positioning, listing content and marketing, with STR Booster support.'),
 '52rev': ('52Rev: Vacation Rental Revenue Marketing Beta', 'Join the 52Rev beta waitlist. Connect weekly guest targeting, revenue planning and marketing playbooks for your vacation rental.'),
 'tools-partners': ('Vacation Rental Software & Partner Offers', 'Explore vacation rental software for pricing, PMS, guest marketing and operations, with partner offers from Hospitable, HighLevel, PriceLabs and more.'),
 'growth-sprint': ('30-Day Vacation Rental Revenue Growth Sprint', 'Implement a focused vacation rental growth plan in 30 days. Connect guest positioning, pricing and automation for one primary property. US$2,750.'),
 'get-expert-help': ('Vacation Rental Consulting: Talk to STR Booster', 'Discuss your vacation rental with STR Booster. Get help choosing a focused project or ongoing support for revenue, positioning, marketing and automation.'),
 'guest-positioning-guide': ('How to Identify Your Ideal Vacation Rental Guest', 'Use guest reviews, travel needs and seasonal demand to identify your ideal vacation rental guest and improve your listing positioning.'),
 'weekly-revenue-guide': ('Vacation Rental Pricing & Marketing: A Weekly Plan', 'Follow a weekly routine to review booking pace, target relevant guests and coordinate vacation rental pricing, stay rules and marketing.'),
 'automation-guide': ('Short-Term Rental Automation: Where to Start', 'Choose your first short-term rental automation: map the task, check your existing tools, test the workflow and measure the effort saved.'),
}
HEADINGS = {
 'listing-optimization': 'Vacation rental listing optimization.<br><em>Give guests a reason to book.</em>',
 'revenue-management': 'Vacation rental revenue management.<br><em>Pricing and channels, aligned.</em>',
 'technology-automation': 'Short-term rental automation.<br><em>Make your tools do more.</em>',
 'websites-funnels': 'Vacation rental websites.<br><em>Built for direct bookings.</em>',
 'tools-partners': 'Vacation rental software.<br><em>Tools and partner offers.</em>',
}
RELATED = {
 'guest-positioning-guide': [('guest-intel','Explore Guest Intel'),('listing-optimization','Get listing optimization support')],
 'weekly-revenue-guide': [('revenue-management','Explore revenue management services'),('52rev','Discover 52Rev revenue marketing')],
 'automation-guide': [('technology-automation','Explore rental automation services'),('tools-partners','Compare tools and partner offers')],
 'listing-optimization': [('guest-positioning-guide','How to identify your ideal guest'),('websites-funnels','Carry your positioning into your website')],
 'revenue-management': [('weekly-revenue-guide','Build a weekly pricing and marketing routine'),('tools-partners','Explore pricing and distribution tools')],
 'technology-automation': [('automation-guide','Choose your first automation'),('tools-partners','Explore software and partner offers')],
 'websites-funnels': [('guest-positioning-guide','Define the guest your website should attract'),('technology-automation','Connect your CRM and marketing workflows')],
}

RELATED['listing-optimization'] += [('case-study-brigantine','Brigantine: guest positioning and listing performance'),('case-study-tuscany','Tuscany: a closer look at listing conversion')]
RELATED['revenue-management'] += [('case-study-phoenix','Phoenix: reviewing an existing PriceLabs setup'),('case-study-north-carolina','North Carolina: revenue and distribution results')]
RELATED['technology-automation'] += [('case-study-north-carolina','North Carolina: getting more from Hostaway')]
RELATED['websites-funnels'] += [('case-study-north-carolina','North Carolina: a connected direct booking website')]
RELATED['resources'] = [('client-results','Explore client case studies')]

def enhance_page(markup, slug, title, desc):
    canonical = BASE + ('/' if slug == 'index' else '/' + slug + '.html')
    if slug in HEADINGS:
        markup = re.sub(r'<h1>.*?</h1>', '<h1>'+HEADINGS[slug]+'</h1>', markup, count=1, flags=re.S)
    if slug in RELATED:
        links=''.join('<li><a href="/'+target+'.html">'+label+'</a></li>' for target,label in RELATED[slug])
        section='<section class="section white"><div class="wrap"><h2>Put the next step into practice</h2><ul>'+links+'</ul></div></section>'
        markup=markup.replace('</main>',section+'</main>')
    graph=[{'@type':'Organization','@id':BASE+'/#organization','name':'STR Booster','url':BASE+'/', 'email':'david@strbooster.com'},
           {'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'STR Booster','publisher':{'@id':BASE+'/#organization'}},
           {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':desc,'isPartOf':{'@id':BASE+'/#website'}}]
    if slug!='index':
        graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},{'@type':'ListItem','position':2,'name':title,'item':canonical}]})
    if slug in ['listing-optimization','revenue-management','technology-automation','websites-funnels','growth-sprint']:
        graph.append({'@type':'Service','name':title,'description':desc,'url':canonical,'provider':{'@id':BASE+'/#organization'}})
    metadata=f'<link rel="canonical" href="{canonical}"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="STR Booster"><meta name="twitter:card" content="summary">'
    metadata+='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph}).replace('<','\\u003c')+'</script>'
    metadata+='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    return markup.replace('</head>',metadata+'</head>')

def write_crawl_files(root, pages):
    urls=[BASE+('/' if p=='index.html' else '/'+p) for p in pages if p!='community.html']
    (root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+html.escape(url)+'</loc></url>\n' for url in urls)+'</urlset>\n')
    (root/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
    (root/'404.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Page Not Found | STR Booster</title><link rel="stylesheet" href="/styles.css"><link rel="icon" href="/favicon.svg" type="image/svg+xml"></head><body><main class="wrap"><section class="page-hero"><p class="eyebrow">STR Booster · 404</p><h1>We could not find that page.</h1><p>The link may have changed. Explore our services or return to the homepage.</p><div class="actions"><a class="btn" href="/">Return Home</a><a class="btn secondary" href="/growth-services.html">Explore Growth Services</a></div></section></main></body></html>''')
