"""Search metadata and crawl files for the static STR Booster site."""
import html
import json
import re

BASE = 'https://strbooster.com'
OG_IMAGE = BASE + '/assets/dx-og.jpg'
GUIDE_PUBLISHED = '2026-09-14'
GUIDE_UPDATED = '2026-11-20'
GUIDE_UPDATED_LABEL = 'November 2026'
SAME_AS = ['https://www.instagram.com/strbooster/', 'https://www.youtube.com/@strbooster',
           'https://www.linkedin.com/company/strbooster']
FOUNDER = {'@type': 'Person', '@id': BASE + '/#founder', 'name': 'David Anthony Scott',
           'jobTitle': 'Founder, STR Booster', 'url': BASE + '/#founder',
           'image': BASE + '/assets/founder-david.png',
           'sameAs': ['https://www.linkedin.com/in/david-anthony-scott/'],
           'knowsAbout': ['Short-term rental revenue management', 'Vacation rental marketing',
                          'Hospitality automation', 'Boutique hotel operations']}
GUIDES = {'guest-positioning-guide', 'weekly-revenue-guide', 'automation-guide'}
RETIRED_STORY_PAGES = frozenset({
    'client-results.html',
    'case-study-brigantine.html',
    'case-study-north-carolina.html',
    'case-study-tuscany.html',
    'case-study-phoenix.html',
    'growth-sprint.html',  # 30-day sprint offer retired
    # Nov 2026: services and pricing removed; STR Booster now shares free Claude growth systems.
    'growth-services.html',
    'owner-acquisition.html',
    'listing-optimization.html',
    'revenue-management.html',
    'technology-automation.html',
    'websites-funnels.html',
    'tools-partners.html',
    'get-expert-help.html',
    'our-approach.html',
})
META = {
 'index': ('Vacation Rental Growth & Automation', 'Grow your vacation rental with guest insights, revenue management, listing optimization and automation. Explore expert services and a free host community.'),
 'our-approach': ('Vacation Rental Growth Strategy', 'Connect guest positioning, pricing, marketing and automation in one vacation rental growth strategy. Build a more valuable stay and a stronger business.'),
 'growth-services': ('Short-Term Rental Growth Systems & Pricing', 'Direct Revenue, Owner Acquisition and Growth Partner plans for STR managers with 10 to 100 doors, with starting prices, guarantees and a free Growth Audit.'),
 'owner-acquisition': ('Owner Acquisition for Vacation Rental Managers', 'Win more owner contracts with an owner landing page, revenue estimates, AI follow-up and nurture for owners and realtors. Built and run for property managers.'),
 'listing-optimization': ('Airbnb & Vacation Rental Listing Optimization', 'Improve your vacation rental listing with ideal guest positioning, copy, photo strategy and amenity priorities. Get focused help from STR Booster.'),
 'revenue-management': ('Vacation Rental Revenue Management Services', 'Connect vacation rental pricing, minimum stays, seasonal marketing and channel distribution. Get revenue management support built around your property.'),
 'technology-automation': ('Short-Term Rental Automation & PMS Optimization', 'Improve your PMS, CRM and guest workflows with short-term rental automation. Connect marketing, social media and defined AI tasks around your operation.'),
 'websites-funnels': ('Vacation Rental Websites & Direct Booking Funnels', 'Build a vacation rental website with booking pathways, lead capture, CRM, chatbots and automated follow-up. Turn guest interest into booking opportunities.'),
 'our-apps': ('Free Vacation Rental Tools: Guest Intel & 52Rev', 'Free tools from STR Booster: Guest Intel shows who your rental is best placed to win, and the 52Rev beta plans weekly revenue marketing.'),
 'guest-intel': ('Guest Intel: Find Your Ideal Rental Guest', 'Identify your ideal vacation rental guest with Guest Intel. Apply guest insights to positioning, listing content and marketing, with STR Booster support.'),
 '52rev': ('52Rev: Vacation Rental Revenue Marketing Beta', 'Join the 52Rev beta waitlist. Connect weekly guest targeting, revenue planning and marketing playbooks for your vacation rental.'),
 'tools-partners': ('Vacation Rental Software Picks (Affiliate)', 'Vacation rental software we use and recommend for pricing, PMS, guest marketing and operations. Affiliate links, plainly disclosed.'),
 'get-expert-help': ('Vacation Rental Consulting: Talk to STR Booster', 'Discuss your vacation rental with STR Booster. Get help choosing a focused project or ongoing support for revenue, positioning, marketing and automation.'),
 'guest-positioning-guide': ('How to Identify Your Ideal Vacation Rental Guest', 'Use guest reviews, travel needs and seasonal demand to identify your ideal vacation rental guest and improve your listing positioning.'),
 'weekly-revenue-guide': ('Vacation Rental Pricing & Marketing Weekly Plan', 'Follow a weekly routine to review booking pace, target relevant guests and coordinate vacation rental pricing, stay rules and marketing.'),
 'playbook': ('Free STR AI Playbook & Starter Kits', 'A free 12-step AI playbook for short-term rental hosts and property managers, with five downloadable kits: guest messaging, listing audit, pricing check, reviews and owner reports.'),
 'resources': ('Guides & Tools for Short-Term Rental Managers', 'Free guides, video tutorials and tools for short-term rental managers: direct bookings, pricing, guest positioning and automation.'),
 'automation-guide': ('Short-Term Rental Automation: Where to Start', 'Choose your first short-term rental automation: map the task, check your existing tools, test the workflow and measure the effort saved.'),
}
HEADINGS = {
 'listing-optimization': 'Vacation rental listing optimization.<br><em>Give guests a reason to book.</em>',
 'revenue-management': 'Vacation rental revenue management.<br><em>Pricing and channels, aligned.</em>',
 'technology-automation': 'Short-term rental automation.<br><em>Make your tools do more.</em>',
 'websites-funnels': 'Vacation rental websites.<br><em>Built for direct bookings.</em>',
 'tools-partners': 'Vacation rental software.<br><em>Affiliate links, plainly disclosed.</em>',
}
RELATED = {
 'guest-positioning-guide': [('guest-intel','Explore Guest Intel'),('playbook','Run the free listing audit kit')],
 'weekly-revenue-guide': [('playbook','Get the free weekly pricing check kit'),('52rev','Discover 52Rev revenue marketing')],
 'automation-guide': [('playbook','Start with the free guest messaging kit'),('resources','Browse more resources')],
 'resources': [('playbook','Get the free STR AI Playbook'),('guest-intel','Explore Guest Intel')],
}

# Visible FAQ sections (rendered on the page) with matching FAQPage schema.
# Only for pages whose main content is not replaced by a template override.
FAQS = {
 'listing-optimization': [
  ('What does vacation rental listing optimization include?', 'It aligns your title, description, photo order, captions and amenity priorities around the guest your property serves best, so the listing answers that guest\'s questions and gives them a clear reason to book.'),
  ('Does this work for Airbnb and Vrbo?', 'Yes. We keep one consistent guest promise across Airbnb, Vrbo, your direct booking website and other relevant channels, and adapt the content to each platform\'s format.'),
  ('How do you identify the ideal guest?', 'We look at guest reviews, recurring enquiries, travel purpose and seasonal demand. Guest Intel, our guest insight app, can speed up this step.'),
  ('Do I have to buy new amenities?', 'No. We prioritise improvements by likely guest value, cost and operational effort, and recommend only those that support your guest promise.'),
 ],
 'revenue-management': [
  ('What is vacation rental revenue management?', 'Vacation rental revenue management is the practice of setting nightly rates, minimum stays, gap-night rules, booking windows and channel mix from real demand, so each night earns as much as it reasonably can after the cost of winning the booking.'),
  ('Do I need to change my pricing tool?', 'No. We work with the tools you already use, including dynamic pricing tools such as PriceLabs. Any change or new subscription is agreed with you before implementation.'),
  ('How are pricing and marketing connected?', 'Each week of the calendar is reviewed for booking pace and the guest most likely to travel. Pricing, stay rules and promotion then respond to the same plan instead of working separately.'),
  ('How much does revenue management support cost?', 'Revenue management is part of the Growth Partner plan, from $2,000 a month, alongside the Direct Revenue and Owner Acquisition systems. See the pricing page for details.'),
 ],
 'technology-automation': [
  ('What can be automated in a short-term rental business?', 'Common starting points are guest messaging, enquiry follow-up, review requests, CRM updates, social media scheduling and repetitive PMS tasks. The best first automation has a clear trigger and a result you can check.'),
  ('Will AI reply to guests without my approval?', 'Only within limits you set. Each workflow has agreed permissions, checks and an escalation route to a person when a decision could affect a guest or a booking.'),
  ('Do I need new software?', 'Usually not. We start with your existing PMS, CRM and integrations, and only recommend a new tool when it fills a clear gap.'),
 ],
 'websites-funnels': [
  ('Do I need a website if I already list on Airbnb?', 'A direct booking website gives you a channel you control: your own guest data, repeat-stay marketing and bookings without platform fees. It works alongside your OTA listings rather than replacing them.'),
  ('Does the website connect to my booking engine?', 'Yes. The site is built around your existing booking engine or PMS so visitors can check availability and book, and booking-engine handoffs can be tracked.'),
  ('What happens to visitors who do not book straight away?', 'Opted-in visitors can be captured into your CRM and followed up with relevant, consent-based messages until they are ready to book.'),
 ],
 'guest-positioning-guide': [
  ('What is an ideal guest for a vacation rental?', 'An ideal guest is the type of traveller your property serves best, defined by why they travel, who they travel with and what a successful stay looks like for them, rather than by age group alone.'),
  ('Where do I find evidence of my best guest?', 'Start with your guest reviews and the questions people ask in enquiries. Repeated praise points to real strengths; repeated concerns show where the property is a poor fit.'),
  ('How often should I review my guest positioning?', 'Review it whenever the main reason to travel changes, typically each season, while keeping the property facts consistent.'),
 ],
 'weekly-revenue-guide': [
  ('How often should I review vacation rental pricing?', 'A weekly review works well for most rentals: check booking pace and lead time for the weeks ahead, then decide whether price, stay rules or promotion need to change.'),
  ('Should I lower my price when a week is not booking?', 'Not automatically. A slow week may need a stay-rule change, clearer positioning or more relevant promotion instead. Account for the cost of acquiring the booking before discounting.'),
  ('How do I know if a pricing or marketing change worked?', 'Compare booking pickup and revenue with what you changed. Treat the result as a signal to investigate rather than proof that one action caused it.'),
 ],
 'automation-guide': [
  ('What should I automate first in my rental business?', 'Choose a repetitive task with a clear trigger and an outcome you can observe, such as a pre-arrival message or enquiry follow-up.'),
  ('How do I avoid automation mistakes with guests?', 'Define what the automation may change, when it must pause and who it escalates to. Test the full journey with test records before switching it on.'),
  ('Do I need to buy an automation tool?', 'Check your PMS, CRM and existing integrations first. Many have the features you need, so a new subscription may duplicate what you already pay for.'),
 ],
}

HOWTO_TIME = {'guest-positioning-guide': 'PT1H', 'weekly-revenue-guide': 'PT30M', 'automation-guide': 'PT1H'}


def faq_section(items):
    rows = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in items)
    return ('<section class="section" id="faq"><div class="wrap"><div class="intro"><p class="eyebrow">Questions</p>'
            '<h2>Frequently asked questions</h2></div><div class="faq">' + rows + '</div></div></section>')


def guide_steps(markup):
    """Return (name, text) for each numbered H2 step in a guide's prose."""
    article = re.search(r'<article class="prose">(.*?)</article>', markup, re.S)
    if not article:
        return []
    return [(re.sub(r'^\d+\.\s*', '', html.unescape(n)), html.unescape(t))
            for n, t in re.findall(r'<h2>(\d+\..*?)</h2>\s*<p>(.*?)</p>', article.group(1), re.S)]


def enhance_page(markup, slug, title, desc):
    canonical = BASE + ('/' if slug == 'index' else '/' + slug)
    if slug in HEADINGS:
        markup = re.sub(r'<h1>.*?</h1>', '<h1>'+HEADINGS[slug]+'</h1>', markup, count=1, flags=re.S)
    if slug in RELATED:
        links=''.join('<li><a href="/'+target+'.html">'+label+'</a></li>' for target,label in RELATED[slug])
        section='<section class="section white"><div class="wrap"><h2>Put the next step into practice</h2><ul>'+links+'</ul></div></section>'
        markup=markup.replace('</main>',section+'</main>')
    if slug in GUIDES:
        byline=('<p class="note guide-byline">By <a href="/#founder">David Anthony Scott</a>, founder of STR Booster · '
                f'Updated <time datetime="{GUIDE_UPDATED}">{GUIDE_UPDATED_LABEL}</time></p>')
        markup=re.sub(r'(<section class="page-hero">.*?</h1>)', lambda m: m.group(1)+byline, markup, count=1, flags=re.S)
    if slug in FAQS:
        block=faq_section(FAQS[slug])
        if '<section class="dark cta-band">' in markup:
            markup=markup.replace('<section class="dark cta-band">', block+'<section class="dark cta-band">', 1)
        else:
            markup=markup.replace('</main>', block+'</main>', 1)
    graph=[{'@type':'Organization','@id':BASE+'/#organization','name':'STR Booster','url':BASE+'/', 'email':'info@strbooster.com','logo':BASE+'/favicon.svg','parentOrganization':{'@type':'Organization','name':'Green Door Hotel Inc.'},'founder':{'@id':BASE+'/#founder'},'sameAs':SAME_AS},
           FOUNDER,
           {'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'STR Booster','publisher':{'@id':BASE+'/#organization'}},
           {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':desc,'isPartOf':{'@id':BASE+'/#website'}}]
    if slug!='index':
        graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},{'@type':'ListItem','position':2,'name':title,'item':canonical}]})
    if slug in ['listing-optimization','revenue-management','technology-automation','websites-funnels']:
        graph.append({'@type':'Service','name':title,'description':desc,'url':canonical,'provider':{'@id':BASE+'/#organization'}})
    if slug in GUIDES:
        graph.append({'@type':'Article','@id':canonical+'#article','headline':title,'description':desc,'url':canonical,
                      'mainEntityOfPage':{'@id':canonical+'#webpage'},'author':{'@id':BASE+'/#founder'},
                      'publisher':{'@id':BASE+'/#organization'},'datePublished':GUIDE_PUBLISHED,'dateModified':GUIDE_UPDATED,'image':OG_IMAGE,'inLanguage':'en','isBasedOn':{'@type':'Book','name':'Booked Solid: Scaling Direct Bookings and Guest Loyalty Through Brand Story and Experience','bookEdition':'Second edition','author':{'@id':BASE+'/#founder'},'url':'https://www.amazon.com/dp/B0FF3BR42Q'}})
        steps=guide_steps(markup)
        if steps:
            graph.append({'@type':'HowTo','name':title,'description':desc,'totalTime':HOWTO_TIME.get(slug,'PT1H'),
                          'step':[{'@type':'HowToStep','position':i+1,'name':n,'text':t,'url':canonical} for i,(n,t) in enumerate(steps)]})
    if slug in FAQS:
        graph.append({'@type':'FAQPage','@id':canonical+'#faq','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in FAQS[slug]]})
    metadata=f'<link rel="canonical" href="{canonical}"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="STR Booster"><meta property="og:image" content="{OG_IMAGE}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title,quote=True)} | STR Booster"><meta name="twitter:description" content="{html.escape(desc,quote=True)}"><meta name="twitter:image" content="{OG_IMAGE}">'
    metadata+='<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph}).replace('<','\\u003c')+'</script>'
    metadata+='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    return markup.replace('</head>',metadata+'</head>')

def write_crawl_files(root, pages):
    import datetime, subprocess
    today=datetime.date.today().isoformat()
    def lastmod(page):
        # The date the page last changed in git, so lastmod only moves when content does.
        try:
            out=subprocess.run(['git','log','-1','--format=%cs','--',page],cwd=root,capture_output=True,text=True,timeout=10).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            out=''
        return out or today
    urls=[(BASE+('/' if p=='index.html' else '/'+p[:-5]),lastmod(p)) for p in pages
          if p!='community.html' and p not in RETIRED_STORY_PAGES]
    (root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+html.escape(url)+'</loc><lastmod>'+mod+'</lastmod></url>\n' for url,mod in urls)+'</urlset>\n')
    (root/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
    (root/'404.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Page Not Found | STR Booster</title><link rel="stylesheet" href="/styles.css"><link rel="icon" href="/favicon.svg" type="image/svg+xml"></head><body><main class="wrap"><section class="page-hero"><p class="eyebrow">STR Booster · 404</p><h1>We could not find that page.</h1><p>The link may have changed. Get the free playbook or return to the homepage.</p><div class="actions"><a class="btn" href="/">Return Home</a><a class="btn secondary" href="/playbook">Get the Free Playbook</a></div></section></main></body></html>''')
