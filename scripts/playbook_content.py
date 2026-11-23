"""Free STR AI playbook page (/playbook): playbook steps, starter kits and signup.

Original STR Booster content. Kits live in assets/kits/*.md. The signup form posts
to netlify/functions/brief-signup.js, which adds the contact to HighLevel with the
str-booster-brief tag. playbook.js handles the form and unlocks the kit downloads.
"""
import html


KITS = [
    ('guest-messaging-agent', 'Guest Messaging Agent', 'Hosts and PMs',
     'Turns your house manual into an assistant that drafts guest replies in your voice, answers only from your facts, and flags refunds, complaints and safety issues for a person.',
     '20 min setup'),
    ('who-will-book-your-home-report', '“Who Will Book Your Home” Owner Report', 'Property managers',
     'A one-page report for a prospective owner: the guests most likely to book their home, when they come, and the three things you would change first. Start owner calls with a plan, not a pitch.',
     '15 min per report'),
    ('listing-audit', 'Listing Audit', 'Hosts and PMs',
     'Scores an Airbnb or Vrbo listing in eight areas for the guest you want most, then gives a prioritized fix list, free fixes first, with rewritten titles and opening lines.',
     '15 min per listing'),
    ('weekly-pricing-check', 'Weekly Pricing Check', 'Hosts and PMs',
     'A calm 20-minute review of the next 90 days: pace by week, orphan nights and a short watch list. It never invents a market rate; your pricing tool still does the maths.',
     '20 min a week'),
    ('review-reply-and-insights', 'Review Reply + Insight Miner', 'Hosts and PMs',
     'Drafts short, human replies to every review, including the hard ones, and turns 20 to 100 reviews into what to put in your listing, what to fix and who to market to.',
     '2 min per reply'),
]
KIT_NAMES = {slug: name for slug, name, *_ in KITS}

PHASES = [
    ('Foundation', 'Get your facts and your guest straight once. Every tool after this gets better.', [
        ('Write the facts down once',
         'Put check-in, parking, Wi-Fi, pets, rules, local tips and your money rules in one document per property. AI is only as good as the facts you give it, and this one file feeds every step below.',
         '45 min per property', 'guest-messaging-agent'),
        ('Set up Claude with one project per property',
         'Create a Claude project for each property or portfolio, add your facts document and save the kits as Skills. Ten scattered chats teach you nothing; one project gets sharper every week.',
         '15 min', None),
        ('Find the guest you win most often',
         'Paste your last 30 to 50 reviews into the Insight Miner. Look for who is happiest, why they came and what they praise. That guest becomes the target for your listing and your marketing.',
         '20 min', 'review-reply-and-insights'),
    ]),
    ('Guests', 'Take the repetitive messages off your plate without handing your reputation to a robot.', [
        ('Draft every guest reply with AI, send it yourself',
         'For two weeks, paste every guest message into your messaging agent and edit the draft before sending. Each time you edit, add the missing fact to your property document.',
         '2 weeks, a few min a day', 'guest-messaging-agent'),
        ('Automate the safe 60 percent',
         'Check-in times, directions, Wi-Fi and checkout reminders are safe to schedule in your PMS or messaging tool. Keep refunds, complaints, damage and safety with a person, always.',
         '1 hour', None),
        ('Reply to every review in two minutes',
         'Future guests read your replies. A short, specific, never-defensive reply to every review, including the bad ones, is one of the cheapest trust signals you can buy.',
         '2 min per review', 'review-reply-and-insights'),
    ]),
    ('Revenue', 'Earn more from the nights and guests you already have.', [
        ('Audit your listing for that guest',
         'Score your title, first photo, opening lines and amenities for the guest you found in step 3. Make the free fixes first: title, photo order, first paragraph, amenity names.',
         '15 min per listing', 'listing-audit'),
        ('Run a 20-minute pricing check every week',
         'Look at pace by week against your usual lead time, close orphan nights with stay rules, and pick a small watch list. One change per date range, logged, so you learn what works.',
         '20 min a week', 'weekly-pricing-check'),
        ('Bring past guests back directly',
         'Your past guests are your cheapest bookings. Collect emails with consent, then send a short seasonal note to the guests who match the dates you need to fill. No platform fee.',
         '1 hour to set up', None),
    ]),
    ('Growth', 'Win more owners and leads, and keep only the tools that pay for themselves.', [
        ('Win owners with a “who will book your home” report',
         'For property managers: send every prospective owner a one-page report on the guests their home will attract and what you would change first. It shows you did the homework.',
         '15 min per owner', 'who-will-book-your-home-report'),
        ('Answer every lead in five minutes',
         'Owner enquiries and direct-booking leads go cold fast. A simple CRM with an instant text or email reply, then a person within the hour, wins deals that a slow inbox loses.',
         '2 hours to set up', None),
        ('Cut a tool for every tool you add',
         'Once a month, list your subscriptions and what each one saved or earned. Keep what pays for itself. Fewer tools, used well, beat a stack of apps nobody logs into.',
         '30 min a month', None),
    ]),
]


def kit_link(slug, label=None, cls='pb-kit-link'):
    label = label or 'Download the kit'
    return (f'<a class="{cls}" href="/assets/kits/{slug}.md" download data-kit="{slug}">'
            f'{html.escape(label)} <span aria-hidden="true">↓</span></a>')


GHL_FORM_ID = 'X2ch8hqmAh3G9qypYlVe'  # HighLevel form "Newsletter Sign Up" (STR Booster sub-account)


def signup_form(form_id, heading_id):
    """HighLevel form embed: signups land in HighLevel directly, no API key needed."""
    return f'''<div class="pb-form pb-ghl" id="{form_id}" aria-labelledby="{heading_id}">
<iframe src="https://api.leadconnectorhq.com/widget/form/{GHL_FORM_ID}" id="inline-{GHL_FORM_ID}" class="pb-ghl-frame" title="Newsletter sign up" loading="lazy" data-layout="{{'id':'INLINE'}}" data-trigger-type="alwaysShow" data-trigger-value="" data-activation-type="alwaysActivated" data-activation-value="" data-deactivation-type="neverDeactivate" data-deactivation-value="" data-form-name="Newsletter Sign Up" data-height="320" data-layout-iframe-id="inline-{GHL_FORM_ID}" data-form-id="{GHL_FORM_ID}"></iframe>
<script src="https://link.msgsndr.com/js/form_embed.js" defer></script>
<p class="pb-consent-note">By subscribing you agree to get the kits and the weekly STR Booster Brief. Unsubscribe any time. See our <a href="/privacy.html">privacy policy</a>.</p>
<p class="pb-status" role="status" tabindex="-1"></p>
<button class="text-link pb-unlock" type="button">I’ve subscribed: open the kits</button>
</div>'''


def kit_card(slug, name, who, desc, time):
    return (f'<article class="pb-kit" id="kit-{slug}"><p class="pb-kit-meta"><span>{html.escape(who)}</span>'
            f'<span>{html.escape(time)}</span></p><h3>{html.escape(name)}</h3><p>{html.escape(desc)}</p>'
            + kit_link(slug) + '</article>')


def step_item(number, title, copy, time, kit):
    extra = kit_link(kit, 'Use the ' + KIT_NAMES[kit], 'pb-step-kit') if kit else ''
    return (f'<li class="pb-step"><span class="pb-step-num" aria-hidden="true">{number:02d}</span><div>'
            f'<h4>{html.escape(title)}</h4><p>{html.escape(copy)}</p>'
            f'<p class="pb-step-time">{html.escape(time)}</p>{extra}</div></li>')


def body():
    hero = '''<section class="pb-hero"><div class="wrap pb-hero-grid"><div>
<div class="breadcrumb"><a href="/">Home</a> / Free playbook</div>
<p class="eyebrow">Free. No catch, no call.</p>
<h1>The STR AI Playbook.<br><em>Twelve steps. Five Claude kits. Free.</em></h1>
<p class="lead">Growth systems for hosts and property managers, built on Claude. Put it to work on guest messages, listings, pricing, reviews and owner growth. No new app to learn.</p>
<ul class="pb-hero-list"><li>12-step playbook, readable right here</li><li>5 ready-to-use Claude kits you can download and save as Skills</li><li>One useful email a week, plus a note when a new kit drops</li></ul>
</div>
<div class="pb-signup" id="get-the-kits"><p class="eyebrow">Get the kits</p><h2 id="pb-signup-heading">Where should we send them?</h2>
<p>Subscribe below, then open the kits. We will also send the weekly STR Booster Brief. Unsubscribe in one click.</p>
''' + signup_form('pb-signup-form', 'pb-signup-heading') + '''</div></div></section>'''

    steps, n = [], 0
    for phase, intro, items in PHASES:
        lis = ''
        for title, copy, time, kit in items:
            n += 1
            lis += step_item(n, title, copy, time, kit)
        steps.append(f'<div class="pb-phase"><div class="pb-phase-head"><h3>{html.escape(phase)}</h3>'
                     f'<p>{html.escape(intro)}</p></div><ol class="pb-steps" start="{n - len(items) + 1}">{lis}</ol></div>')
    playbook = ('<section class="section white" id="playbook"><div class="wrap">'
                '<div class="intro"><p class="eyebrow">The playbook</p><h2>From busy host to running on systems.</h2>'
                '<p>Work through it in order. Each step takes minutes, not weeks, and most use a kit you can download below. '
                'You do not need to be technical, and you do not need to buy anything.</p></div>'
                + ''.join(steps) + '</div></section>')

    kits = ('<section class="section" id="kits"><div class="wrap"><div class="intro"><p class="eyebrow">Starter kits</p>'
            '<h2>Five Claude kits. Fill in, use today.</h2>'
            '<p>Each kit is a Claude Skill: instructions, a fill-in template and a tested prompt in one file. Upload it to Claude as a Skill, '
            'or add it to a Claude project. Every kit is built to say “ask a person” rather than guess.</p></div>'
            '<div class="pb-kit-grid">' + ''.join(kit_card(*k) for k in KITS) + '</div>'
            '<p class="pb-unlock-note" id="pb-unlock-note">Downloads unlock when you <a href="#get-the-kits">enter your email</a>.</p>'
            '</div></section>')

    tools = '''<section class="section white" id="claude"><div class="wrap"><div class="intro"><p class="eyebrow">Why Claude</p><h2>One assistant. Your facts. Your rules.</h2>
<p>Everything STR Booster builds runs on Claude. One assistant, set up once with your property facts, replaces a pile of single-purpose apps.</p></div>
<div class="grid three"><article class="card"><h3>Skills you can reuse</h3><p>Each kit installs as a Claude Skill, so Claude follows the same steps and rules every time you ask, for every property.</p></article>
<article class="card"><h3>Projects per property</h3><p>A Claude project keeps a property’s facts, reviews and listing together, so every answer starts from what is true about that home.</p></article>
<article class="card"><h3>You stay in control</h3><p>The kits draft and check. Refunds, complaints, safety and anything about money always come back to a person.</p></article></div>
</div></section>'''

    faq = ('<section class="section" id="faq"><div class="wrap"><div class="intro"><p class="eyebrow">Questions</p><h2>Fair questions.</h2></div><div class="faq">'
           + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in [
               ('Is it really free?', 'Yes. The playbook, the kits and the weekly email are free, and there is nothing to buy. We build these systems and share them.'),
               ('What will you email me?', 'The STR Booster Brief: one short email a week with one idea you can use, plus a note when a new kit drops. No daily blasts. Unsubscribe in one click.'),
               ('Do I need a paid Claude plan?', 'You can start on the free plan. Projects, Skills and longer files work best on a paid Claude plan, which is what we use.'),
               ('Do I need to be technical?', 'No. Each kit is a text file. You fill in your details, upload it to Claude and follow the steps. If you can write a guest message, you can use these.'),
               ('Will the AI reply to my guests on its own?', 'Not unless you set it up to. The kits are built for drafting first, with clear rules for when a person must step in. Automate only what you have tested.'),
           ]) + '</div></div></section>')

    closing = '''<section class="section white" id="join"><div class="wrap"><div class="pb-closing"><div><p class="eyebrow">Not ready yet?</p><h2 id="pb-closing-heading">Get the kits and the weekly Brief.</h2><p>One email a week. A new kit when it drops. Leave any time.</p></div>''' + '<div class="pb-closing-cta"><a class="btn" href="#get-the-kits" data-cta="playbook-closing">Get the free kits</a></div>' + '''</div></div></section>'''

    return hero + playbook + kits + tools + faq + closing + '<script src="/playbook.js" defer></script>'
