"""Free STR AI journey page (/playbook): nine open steps, each with .md resources.

Original STR Booster content. Nothing on the page is gated. Resources live in
assets/kits/*.md. A resource file that still contains the line
"STATUS: placeholder" is shown as "Coming soon" with no download link; remove
that line once the file is written and the page links it on the next build.

Claude Skills with more than one file (a SKILL.md plus scripts, templates and
samples) live in skills/<slug>/ at the repository root, so they can be read on
GitHub. scripts/build-public.py zips each one to /skills/<slug>.zip, ready to
upload to Claude. A step resource written as "skill:<slug>" links that zip, and
shows "Coming soon" until skills/<slug>/SKILL.md exists.

The full playbook is a separate document sent by email to newsletter signups.
The optional signup is the embedded HighLevel form "Newsletter Sign Up".
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT_DIR = ROOT / 'assets' / 'kits'
SKILL_DIR = ROOT / 'skills'
GITHUB_SKILLS = 'https://github.com/scottygeneral/strbooster-cohost/tree/main/skills'
PLACEHOLDER_MARK = 'STATUS: placeholder'

PAINS = [
    ('“Not another app.”', 'You already juggle a PMS, a channel manager, a pricing tool and three inboxes. This journey adds no new app. It runs in Claude, one assistant you set up once.'),
    ('“The margins are too thin to experiment.”', 'Everything here is free. Each step is small, takes minutes, and pays you back in time before you move on.'),
    ('“I tried ChatGPT once and it was generic.”', 'Generic in, generic out. Step 1 gives Claude your facts, goals and voice, so every answer after that is about your business.'),
    ('“I don’t want a robot talking to my guests.”', 'You stay in charge. Everything here drafts and checks. Refunds, complaints, safety and money always come back to a person.'),
    ('“I don’t know where to start.”', 'Start at step 1 and go in order. Each step builds on the one before, and you can stop at any point and keep what works.'),
    ('“I’m not technical.”', 'If you can write a guest message, you can do this. Every step is plain language, a prompt to copy and a file to download.'),
]

# David's journey order (Nov 23 2026).
# (anchor, title, the problem, what to do, copy-paste prompt, time, [(resource slug, resource name)])
JOURNEY = [
    ('brain', 'The brain: objectives and strategies',
     'AI with no goals and no facts gives random answers. Most hosts skip this step, then decide AI does not work.',
     ['Write down your goals for the next 12 months: revenue, occupancy, owners, time back.',
      'List your properties, who books them, the numbers you watch and the rules you never break.',
      'Create one Claude project called “Business brain” and add that document. Every later step starts here.'],
     'Interview me one question at a time to build the “business brain” for my short-term rental business: my goals for the next 12 months, my properties, my guests, the numbers I track, my voice and my rules. When we are done, write it as one clear document I can add to a Claude project. Do not invent anything I have not told you.',
     '45 minutes, once',
     [('skill:the-brain', 'The Brain skill')]),
    ('brand', 'Brand building',
     'If your listing sounds like every other listing, you compete on price. A clear brand is why a guest books you, and books direct next time.',
     ['Write your promise in one sentence: who you are for and why they will love staying with you.',
      'Pick three voice words, with what each one sounds like and what it never sounds like.',
      'Save it as a one-page brand guide in your business brain.'],
     'Using my business brain, draft a one-page brand guide for my rentals: the promise in one sentence, who it is for and who it is not for, three voice words with a do and a don’t example for each, and five phrases we use and five we avoid. Ask me before you invent any detail.',
     '30 minutes',
     [('brand-guide', 'One-Page Brand Guide kit')]),
    ('guest', 'Know your guest',
     'You cannot market to everyone. Your reviews already tell you who loves your place most, and why.',
     ['Paste your last 30 to 50 reviews into Claude with the Review Insight kit.',
      'Find your happiest guest: why they came, who they came with, what they praised.',
      'Add that guest profile to your business brain. It drives every step after this.'],
     'Here are my latest reviews. Find the guests who were happiest: their trip purpose, group type and season. List the top five things they praise, with exact short quotes, and anything that comes up more than once as a problem. Do not invent quotes or counts.',
     '20 minutes',
     [('skill:guest-intelligence-report', 'Guest Intelligence Report skill'), ('review-reply-and-insights', 'Review Reply + Insight Miner')]),
    ('listings', 'Optimize your listings',
     'Most listings are written for the host, not the guest. The title, first photo and first two lines decide the click.',
     ['Run the Listing Audit for the guest you found in step 3.',
      'Make the free fixes first: title, photo order, opening lines, amenity names.',
      'Note your views and bookings now, then run the audit again in 30 days.'],
     'Audit this listing for my target guest. Score the title, first photo and photo order, opening lines, fit signals, amenities, objection handling, proof and house rules from 1 to 5 with evidence. Then give me the top five fixes, free ones first, and three rewritten titles.',
     '15 minutes per listing',
     [('listing-audit', 'Listing Audit')]),
    ('distribution', 'OTA distribution',
     'One channel is one algorithm change away from an empty calendar. But every channel has its own guests, fees and rules, and the wrong one discounts your best nights.',
     ['Match the channels to your guest, your brand and your strategy: Airbnb, Vrbo, Booking.com, your own site, and niche ones like Whimstay for last-minute gaps.',
      'Write each channel its own first line for its own users, and keep every fact identical everywhere.',
      'Decide which nights open where: peak nights on the channels where you keep the most, soft nights and gaps on the rest, nothing below your floor.'],
     'Using my business brain, brand promise and guest profile, research which booking channels fit this property, including niche ones. Score each on guest fit, brand fit, strategy fit, money kept after fees and effort. Recommend two or three core channels and at most two tests, say how to position the listing on each, and tell me which high-demand nights to open on which channel. Check current fees and event dates with sources. Never let a channel sell below my floor.',
     '1 hour, then quarterly',
     [('skill:ota-distribution', 'OTA Distribution skill')]),
    ('marketing', 'Marketing and sales',
     'No time for content, and past guests forgotten the day they check out. Your cheapest next booking is someone who already stayed.',
     ['Collect past-guest emails with consent, and send a short note each season.',
      'Turn real reviews and local events into posts. No stock phrases, no fake urgency.',
      'Answer every direct enquiry within five minutes, even with a holding reply.'],
     'Using my brand guide and guest profile, write a four-week plan: one past-guest email and two social posts a week, each built only from the reviews, photos and local events I give you. Keep my voice. No discounts unless I ask for one.',
     '1 hour a month',
     [('skill:marketing-plan', 'Monthly Marketing Plan skill')]),
    ('revenue', 'Revenue management',
     'Prices left on autopilot, or panic-discounted. A calm weekly check beats both.',
     ['Export the next 90 days from your pricing tool or PMS.',
      'Run the Weekly Pricing Check: pace by week, orphan nights, a short watch list.',
      'Make one change per date range and log it, so you learn what works for your home.'],
     'Here are my next 90 nights: date, booked, price and minimum stay, plus my typical lead time and floor price. Show pace by week as ahead, on track or behind, list orphan nights, and give me a watch list of three to five date ranges with one suggested action each. Never invent market data.',
     '20 minutes a week',
     [('weekly-pricing-check', 'Weekly Pricing Check')]),
    ('owners', 'Owner acquisition',
     'For property managers and co-hosts: owner pitches all sound the same. Show the owner their home and their guests, not your logo.',
     ['Before the first call, build a “who will book your home” report for that owner.',
      'Send it as a one-page PDF with one line of context.',
      'Use the call to walk through it together, with real numbers from your pricing tool.'],
     'Prepare a one-page report titled “Who will book [owner]’s home” for this property: the main guest it can win and why, the three most likely guest types with when they come and what wins them, best and slowest seasons, and three low-cost changes you would make first. Do not invent revenue figures or results.',
     '15 minutes per owner',
     [('who-will-book-your-home-report', '“Who Will Book Your Home” Owner Report')]),
    ('experience', 'Guest experience',
     'The same twenty questions, every day, at every hour. Fast, warm, accurate replies are what five-star reviews are made of.',
     ['Set up the Guest Messaging Agent with your property facts.',
      'Draft every reply with it for two weeks, edit, and send yourself.',
      'Then automate only the safe questions: check-in, Wi-Fi, parking, directions. Keep money, complaints and safety with a person.'],
     'You are my guest messaging assistant. Using only the property facts I gave you, draft a reply to the guest message below in my voice, under 90 words. If it involves a refund, a complaint, damage, safety or anything not in my facts, start with “HOST NEEDED” and give me a holding reply instead.',
     '30 minutes to set up',
     [('skill:guest-experience', 'Guest Experience Storyboard skill'), ('guest-messaging-agent', 'Guest Messaging Agent')]),
]

GHL_FORM_ID = 'X2ch8hqmAh3G9qypYlVe'  # HighLevel form "Newsletter Sign Up" (STR Booster sub-account)


def resource_ready(slug):
    if slug.startswith('skill:'):
        path = SKILL_DIR / slug[6:] / 'SKILL.md'
    else:
        path = KIT_DIR / f'{slug}.md'
    return path.is_file() and PLACEHOLDER_MARK not in path.read_text(encoding='utf-8')


def frontmatter(text):
    """name and description from a SKILL.md or kit's YAML front matter."""
    meta = {}
    m = re.match(r'---\n(.*?)\n---', text, re.S)
    for line in (m.group(1).splitlines() if m else []):
        key, _, value = line.partition(':')
        meta[key.strip()] = value.strip().strip('"')
    return meta


def skill_files(slug):
    return sorted(p.relative_to(SKILL_DIR / slug).as_posix()
                  for p in (SKILL_DIR / slug).rglob('*') if p.is_file())


def resource_link(slug, name):
    if resource_ready(slug):
        return (f'<a class="pb-res" href="/assets/kits/{slug}.md" download data-kit="{slug}">'
                f'<span class="pb-res-type">.md</span><span class="pb-res-name">{html.escape(name)}</span>'
                f'<span class="pb-res-action">Download <span aria-hidden="true">↓</span></span></a>')
    return (f'<div class="pb-res pb-res-soon"><span class="pb-res-type">.md</span>'
            f'<span class="pb-res-name">{html.escape(name)}</span><span class="pb-res-action">Coming soon</span></div>')


def signup_form(form_id, heading_id):
    """HighLevel form embed: signups land in HighLevel directly, no API key needed."""
    return f'''<div class="pb-form pb-ghl" id="{form_id}" aria-labelledby="{heading_id}">
<iframe src="https://api.leadconnectorhq.com/widget/form/{GHL_FORM_ID}" id="inline-{GHL_FORM_ID}" class="pb-ghl-frame bx-form" title="Newsletter sign up" loading="lazy" data-layout="{{'id':'INLINE'}}" data-trigger-type="alwaysShow" data-trigger-value="" data-activation-type="alwaysActivated" data-activation-value="" data-deactivation-type="neverDeactivate" data-deactivation-value="" data-form-name="Newsletter Sign Up" data-height="320" data-layout-iframe-id="inline-{GHL_FORM_ID}" data-form-id="{GHL_FORM_ID}"></iframe>
<script src="https://link.msgsndr.com/js/form_embed.js" defer></script>
<p class="pb-consent-note">By subscribing you agree to get the playbook and the weekly STR Booster Brief by email. Unsubscribe any time. See our <a href="/privacy.html">privacy policy</a>.</p>
</div>'''


TITLE_CASE = {
    'brain': 'The Brain: Objectives And Strategies', 'brand': 'Brand Building', 'guest': 'Know Your Guest',
    'listings': 'Optimize Your Listings', 'distribution': 'OTA Distribution', 'marketing': 'Marketing And Sales',
    'revenue': 'Revenue Management', 'owners': 'Scale Up: Win More Homes', 'experience': 'Guest Experience',
}
STAGES = [('Stage 1', 'Foundation.', 0, 3), ('Stage 2', 'Get Booked.', 3, 6), ('Stage 3', 'Grow.', 6, 9)]


def file_chip(slug, name):
    if slug.startswith('skill:'):
        skill = slug[6:]
        if resource_ready(slug):
            return (f'<a class="bx-file bx-file-skill" href="/skills/{skill}.zip" download data-kit="{skill}">'
                    f'{skill} · Claude skill .zip<span class="sr-only"> ({html.escape(name)})</span> <span aria-hidden="true">↓</span></a>')
        return f'<span class="bx-file bx-file-soon">{skill} skill · coming soon</span>'
    if resource_ready(slug):
        return (f'<a class="bx-file" href="/assets/kits/{slug}.md" download data-kit="{slug}">{slug}.md'
                f'<span class="sr-only"> ({html.escape(name)})</span> <span aria-hidden="true">↓</span></a>')
    return f'<span class="bx-file bx-file-soon">{slug}.md · coming soon</span>'


def tab(label, glyph='■', ident=''):
    idattr = f' id="{ident}"' if ident else ''
    return f'<p class="bx-tab"{idattr}><span aria-hidden="true">{glyph}</span>{html.escape(label)}</p>'


def journey_step(n, anchor, title, problem, todo, prompt, time, resources):
    items = ''.join(f'<li>{html.escape(t)}</li>' for t in todo)
    files = ''.join(file_chip(slug, name) for slug, name in resources)
    return (f'<li class="bx-step" id="step-{n}"><span class="bx-num" aria-hidden="true">{n}</span><div>'
            f'<h3 id="{anchor}">{html.escape(TITLE_CASE[anchor])}.</h3>'
            f'<p class="bx-meta">Step {n} of {len(JOURNEY)} · {html.escape(time)}</p>'
            f'<p>{html.escape(problem)}</p>'
            f'<ul class="bx-do">{items}</ul>'
            f'<details class="bx-prompt"><summary>The prompt</summary>'
            f'<p id="prompt-{n}">{html.escape(prompt)}</p>'
            f'<button type="button" class="pb-copy" data-copy="prompt-{n}">Copy prompt</button></details>'
            f'<div class="bx-files">{files}</div></div></li>')


def body():
    hero = ('<section class="bx-hero bx-hero-sub"><div class="bx-wrap">'
            '<div class="breadcrumb"><a href="/">Home</a> / The Journey</div>'
            '<h1>The Journey.</h1>'
            '<p class="bx-lede">Nine steps. Read the step, copy the prompt, take the file.</p>'
            '<p class="bx-actions"><a class="bx-btn" href="#step-1" data-cta="journey-start">Start Step 1</a>'
            '<a class="bx-btn bx-btn-ghost" href="/skills.html" data-cta="journey-skills">All Skills</a>'
            '<a class="bx-btn bx-btn-ghost" href="#get-the-kits" data-cta="playbook-email">Get The Playbook</a></p>'
            '</div></section>')

    problem = ('<section class="bx-section" id="why"><div class="bx-wrap">' + tab('Before You Start', '▲')
               + '<div class="bx-card bx-panel"><h2>Here’s Why Most Hosts Haven’t.</h2><ul class="bx-list bx-list-wide">'
               + ''.join(f'<li><span class="bx-ico" aria-hidden="true">{g}</span><div><strong>{t}</strong><span>{html.escape(a)}</span></div></li>'
                         for g, t, (q, a) in zip(['▣', '$', '?'],
                             ['Not Another App.', 'The Margins Are Too Thin To Experiment.', 'I Tried ChatGPT Once. It Was Generic.'], PAINS[:3]))
               + '</ul><p class="bx-turn">So start small. Step 1 takes one evening, and everything after it gets easier.</p></div></div></section>')

    stages = ''
    for idx, (label, name, lo, hi) in enumerate(STAGES, 1):
        steps = ''.join(journey_step(i + 1, *JOURNEY[i]) for i in range(lo, hi))
        stages += ('<section class="bx-section"><div class="bx-wrap">' + tab(f'{label} · Steps {lo + 1} to {hi}', '▮', f'stage-{idx}')
                   + f'<div class="bx-card bx-panel"><h2>{name}</h2><ol class="bx-steps">{steps}</ol></div></div></section>')
    journey = ('<div id="kits"><div id="journey"></div>' + stages + '</div>')

    how = ('<section class="bx-section" id="how-files"><div class="bx-wrap">' + tab('How A File Works', '◆')
           + '<div class="bx-card bx-panel"><h2>Three Steps. One Evening.</h2><ul class="bx-list bx-list-wide">'
           '<li><span class="bx-ico" aria-hidden="true">1</span><div><strong>Open Claude.</strong><span>A free account is fine to start. Create one project for your business.</span></div></li>'
           '<li><span class="bx-ico" aria-hidden="true">2</span><div><strong>Add The File.</strong><span>A .zip is a Claude skill: upload it in Claude under Settings, Skills. A .md file goes into your project.</span></div></li>'
           '<li><span class="bx-ico" aria-hidden="true">3</span><div><strong>Fill In The Brackets.</strong><span>Answer its questions once with your real facts. Then use it every week.</span></div></li>'
           '</ul><p class="bx-small">Files marked “coming soon” are on the way. Use the prompt for that step until then.</p></div></div></section>')

    faq = ('<section class="bx-section" id="faq"><div class="bx-wrap">' + tab('Questions', '?')
           + '<div class="bx-card bx-panel"><h2>Fair Questions.</h2><div class="faq">'
           + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in [
               ('Is it really free?', 'Yes. The journey, the prompts, the files and the emailed playbook are free, and there is nothing to buy. You do not need to sign up to use anything on this page.'),
               ('Why Claude?', 'One assistant, set up once with your facts, replaces a pile of single-purpose apps. Projects keep each property’s facts together, and Skills let Claude follow the same steps every time.'),
               ('Do I need a paid Claude plan?', 'You can start on the free plan. Projects, Skills and longer files work best on a paid Claude plan, which is what we use.'),
               ('Do I need to be technical?', 'No. Each step is plain language and a prompt to copy. Each file is a text file you upload. If you can write a guest message, you can use these.'),
               ('Will the AI reply to my guests on its own?', 'Not unless you set it up to. Everything here drafts first, with clear rules for when a person must step in. Automate only what you have tested.'),
           ]) + '</div></div></div></section>')

    email = ('<section class="bx-section bx-last" id="get-the-kits"><div class="bx-wrap">' + tab('Email', '✉')
             + '<div class="bx-card bx-panel"><h2 id="pb-signup-heading">Get The Playbook.</h2>'
             '<p class="bx-sub">The whole journey in one document. One email when a new file drops. No spam. Nothing to buy.</p>'
             + signup_form('pb-signup-form', 'pb-signup-heading') + '</div></div></section>')

    return '<div class="bx">' + hero + problem + journey + how + faq + email + '</div><script src="/playbook.js" defer></script><script src="/motion.js" defer></script>'


def step_for(slug):
    for n, row in enumerate(JOURNEY, 1):
        if any(s == slug for s, _ in row[6]):
            return n, TITLE_CASE[row[0]]
    return None, ''


def catalog():
    """Every skill in journey order: (slug, title, description, zip slug, step, kind, ready).

    Multi-file skills come from skills/<slug>/; single-file kits from
    assets/kits/<slug>.md. build-public.py zips both kinds to /skills/<slug>.zip.
    """
    rows = []
    for n, row in enumerate(JOURNEY, 1):
        for slug, name in row[6]:
            ready = resource_ready(slug)
            if slug.startswith('skill:'):
                key = slug[6:]
                path = SKILL_DIR / key / 'SKILL.md'
                kind = 'skill'
            else:
                key = slug
                path = KIT_DIR / f'{slug}.md'
                kind = 'kit'
            meta = frontmatter(path.read_text(encoding='utf-8')) if ready else {}
            rows.append((key, name, meta.get('description', ''), n, TITLE_CASE[row[0]], kind, ready))
    return rows


def short(text, limit=230):
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(' ', 1)[0].rstrip(',;:') + '…'


def skill_card(key, name, desc, n, step_title, kind, ready):
    head = (f'<p class="bx-meta">Step {n} · {html.escape(step_title)}</p>'
            f'<h3>{html.escape(name)}</h3>')
    if not ready:
        return (f'<li class="bx-skill bx-skill-soon">{head}<p>On the way. Use the prompt for step {n} until then.</p>'
                f'<div class="bx-files"><span class="bx-file bx-file-soon">{key} · coming soon</span></div></li>')
    if kind == 'skill':
        files = skill_files(key)
        extra = (f'<p class="bx-small">{len(files)} files: ' + ', '.join(html.escape(f) for f in files) + '</p>')
        links = (f'<a class="bx-file bx-file-skill" href="/skills/{key}.zip" download data-kit="{key}">Download .zip <span aria-hidden="true">↓</span></a>'
                 f'<a class="bx-file" href="/skills/{key}/SKILL.md" target="_blank" rel="noopener">Read SKILL.md</a>'
                 f'<a class="bx-file" href="{GITHUB_SKILLS}/{key}" target="_blank" rel="noopener noreferrer">GitHub <span aria-hidden="true">↗</span></a>')
    else:
        extra = ''
        links = (f'<a class="bx-file bx-file-skill" href="/skills/{key}.zip" download data-kit="{key}">Download .zip <span aria-hidden="true">↓</span></a>'
                 f'<a class="bx-file" href="/assets/kits/{key}.md" download data-kit="{key}">.md file <span aria-hidden="true">↓</span></a>'
                 f'<a class="bx-file" href="https://github.com/scottygeneral/strbooster-cohost/blob/main/assets/kits/{key}.md" target="_blank" rel="noopener noreferrer">GitHub <span aria-hidden="true">↗</span></a>')
    return (f'<li class="bx-skill" id="skill-{key}">{head}<p>{html.escape(short(desc))}</p>{extra}'
            f'<div class="bx-files">{links}</div></li>')


def skills_body():
    rows = catalog()
    ready = sum(1 for r in rows if r[6])
    hero = ('<section class="bx-hero bx-hero-sub"><div class="bx-wrap">'
            '<div class="breadcrumb"><a href="/">Home</a> / Skills</div>'
            '<h1>Skills.</h1>'
            f'<p class="bx-lede">{ready} free Claude skills for short-term rentals. Download one, upload it to Claude, and it does the job the same way every time.</p>'
            '<p class="bx-actions"><a class="bx-btn" href="#all-skills" data-cta="skills-browse">Browse The Skills</a>'
            f'<a class="bx-btn bx-btn-ghost" href="{GITHUB_SKILLS}" target="_blank" rel="noopener noreferrer" data-cta="skills-github">All Skills On GitHub ↗</a></p>'
            '</div></section>')

    install = ('<section class="bx-section" id="install"><div class="bx-wrap">' + tab('Install A Skill', '◆')
               + '<div class="bx-card bx-panel"><h2>Three Steps. Two Minutes.</h2><ul class="bx-list bx-list-wide">'
               '<li><span class="bx-ico" aria-hidden="true">1</span><div><strong>Download The .zip.</strong><span>Each skill is one .zip file. Don’t unzip it.</span></div></li>'
               '<li><span class="bx-ico" aria-hidden="true">2</span><div><strong>Upload It To Claude.</strong><span>In Claude, open Settings, find Skills, and upload the .zip. Turn on code execution if Claude asks, since some skills run a small script.</span></div></li>'
               '<li><span class="bx-ico" aria-hidden="true">3</span><div><strong>Just Ask.</strong><span>Say what you want, like “build my business brain” or “make a guest intelligence report for this listing.” Claude picks the skill up on its own.</span></div></li>'
               '</ul><p class="bx-small">Prefer to read first? Every skill is plain text. Open SKILL.md here or browse the folder on GitHub. The .md files also work dropped into a Claude project.</p></div></div></section>')

    cards = ''.join(skill_card(*r) for r in rows)
    grid = ('<section class="bx-section" id="all-skills"><div class="bx-wrap">' + tab('In Journey Order', '▮')
            + '<div class="bx-card bx-panel"><h2>Every Skill, Step By Step.</h2>'
            '<p class="bx-sub">They follow the nine steps of <a href="/playbook.html">the journey</a>. Start with step 1: the others read the file it makes.</p>'
            f'<ol class="bx-skills">{cards}</ol></div></div></section>')

    email = ('<section class="bx-section bx-last" id="get-the-kits"><div class="bx-wrap">' + tab('Email', '✉')
             + '<div class="bx-card bx-panel"><h2 id="sk-signup-heading">Get New Skills By Email.</h2>'
             '<p class="bx-sub">One email when a new skill drops, plus the whole journey in one document. No spam. Nothing to buy.</p>'
             + signup_form('sk-signup-form', 'sk-signup-heading') + '</div></div></section>')

    return '<div class="bx">' + hero + grid + install + email + '</div><script src="/playbook.js" defer></script><script src="/motion.js" defer></script>'
