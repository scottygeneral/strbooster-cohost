"""Free STR AI playbook page (/playbook): playbook steps, starter kits and signup.

Original STR Booster content. Kits live in assets/kits/*.md. The signup form posts
to netlify/functions/brief-signup.js, which adds the contact to HighLevel with the
str-booster-brief tag. playbook.js handles the form and unlocks the kit downloads.
"""
import html

HIGHLEVEL_AFFILIATE = 'https://www.gohighlevel.com/?fp_ref=str-booster-18'
HOSPITABLE_AFFILIATE = 'https://hospitable.com/partners/refer?utm_source=affiliates&utm_medium=other&utm_campaign=V4SALU6R'

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
        ('Pick one assistant and one home for your prompts',
         'Choose Claude, ChatGPT or Gemini and create one project per property or portfolio. Save the kits there. Ten scattered chats teach you nothing; one project gets sharper every week.',
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


def signup_form(form_id, heading_id):
    return f'''<form class="pb-form" id="{form_id}" action="/.netlify/functions/brief-signup" method="post" aria-labelledby="{heading_id}" novalidate>
<div class="pb-field"><label for="{form_id}-name">First name <span class="pb-optional">(optional)</span></label><input id="{form_id}-name" name="first_name" autocomplete="given-name" maxlength="80"></div>
<div class="pb-field"><label for="{form_id}-email">Email</label><input id="{form_id}-email" name="email" type="email" autocomplete="email" required maxlength="254"></div>
<div class="pb-field"><label for="{form_id}-role">I am a</label><select id="{form_id}-role" name="role"><option value="host">Host or owner</option><option value="manager">Property manager or co-host</option><option value="other">Something else</option></select></div>
<div class="pb-hp" aria-hidden="true"><label for="{form_id}-company">Company</label><input id="{form_id}-company" name="company" tabindex="-1" autocomplete="off"></div>
<label class="pb-consent"><input type="checkbox" name="consent" required> <span>Send me the kits and the weekly STR Booster Brief. I can unsubscribe at any time. See our <a href="/privacy.html">privacy policy</a>.</span></label>
<button class="btn pb-submit" type="submit">Send me the kits</button>
<p class="pb-status" role="status" tabindex="-1"></p>
</form>'''


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
<h1>The STR AI Playbook.<br><em>Twelve steps. Five kits. Free.</em></h1>
<p class="lead">A practical way for hosts and property managers to put AI to work on guest messages, listings, pricing, reviews and owner growth. Use it with the AI assistant you already have. No new app to learn.</p>
<ul class="pb-hero-list"><li>12-step playbook, readable right here</li><li>5 ready-to-use AI kits you can download (.md files)</li><li>One useful email a week, plus a note when a new kit drops</li></ul>
</div>
<div class="pb-signup" id="get-the-kits"><p class="eyebrow">Get the kits</p><h2 id="pb-signup-heading">Where should we send them?</h2>
<p>Enter your email and the downloads unlock right away. We will also send the weekly STR Booster Brief. Unsubscribe in one click.</p>
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
            '<h2>Five kits. Copy, fill in, use today.</h2>'
            '<p>Each kit is a plain text file with instructions, a fill-in template and a tested prompt. Save it as a Skill in Claude, '
            'paste it into a ChatGPT project or a Gemini Gem. Every kit is built to say “ask a person” rather than guess.</p></div>'
            '<div class="pb-kit-grid">' + ''.join(kit_card(*k) for k in KITS) + '</div>'
            '<p class="pb-unlock-note" id="pb-unlock-note">Downloads unlock when you <a href="#get-the-kits">enter your email</a>.</p>'
            '</div></section>')

    tools = f'''<section class="section white" id="tools"><div class="wrap"><div class="intro"><p class="eyebrow">Tools we actually use</p><h2>A short list, on purpose.</h2>
<p>You can run every kit with a free or paid AI assistant and the PMS you already have. When you are ready for more, these are the tools we build on.</p></div>
<div class="grid two"><article class="card"><p class="eyebrow">CRM, follow-up and direct booking</p><h3>HighLevel</h3><p>One place for leads, owner follow-up, texting, email, booking pages and automations. It is what STR Booster builds its systems on. Sign up through our link and you get our STR setup support.</p><a class="btn" href="{HIGHLEVEL_AFFILIATE}" target="_blank" rel="sponsored noopener noreferrer">Try HighLevel ↗</a></article>
<article class="card"><p class="eyebrow">Guest messaging and operations</p><h3>Hospitable</h3><p>Guest messaging, scheduled messages and hosting workflows across Airbnb, Vrbo and direct bookings. A natural home for the “safe 60 percent” from step 5.</p><a class="btn" href="{html.escape(HOSPITABLE_AFFILIATE, quote=True)}" target="_blank" rel="sponsored noopener noreferrer">25% off Hospitable ↗</a></article></div>
<p class="note affiliate-disclosure"><strong>Affiliate disclosure:</strong> STR Booster earns a commission if you subscribe through these links, at no extra cost to you. You never need either tool to use the playbook or the kits. See all <a href="/tools-partners.html">partner tools</a>.</p>
</div></section>'''

    faq = ('<section class="section" id="faq"><div class="wrap"><div class="intro"><p class="eyebrow">Questions</p><h2>Fair questions.</h2></div><div class="faq">'
           + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in [
               ('Is it really free?', 'Yes. The playbook, the kits and the weekly email are free. We earn money from the growth systems we build for property managers and from clearly marked partner links. Most of what we send is just useful.'),
               ('What will you email me?', 'The STR Booster Brief: one short email a week with one idea you can use, plus a note when a new kit drops. No daily blasts. Unsubscribe in one click.'),
               ('Which AI assistant do I need?', 'Any current assistant works: Claude, ChatGPT or Gemini, on a free or paid plan. Paid plans handle longer files and web search better.'),
               ('Do I need to be technical?', 'No. Each kit is a text file. You fill in your details, paste it in and follow the steps. If you can write a guest message, you can use these.'),
               ('Will the AI reply to my guests on its own?', 'Not unless you set it up to. The kits are built for drafting first, with clear rules for when a person must step in. Automate only what you have tested.'),
               ('Can you set this up for me?', 'Yes. Connecting these kits to your PMS, CRM and website, and running them across a portfolio, is what STR Booster does. <a href="/growth-services.html">See how we work</a>.'),
           ]) + '</div></div></section>')

    closing = '''<section class="section white" id="join"><div class="wrap"><div class="pb-closing"><div><p class="eyebrow">Not ready yet?</p><h2 id="pb-closing-heading">Get the kits and the weekly Brief.</h2><p>One email a week. A new kit when it drops. Leave any time.</p></div>''' + signup_form('pb-closing-form', 'pb-closing-heading') + '''</div></div></section>'''

    return hero + playbook + kits + tools + faq + closing + '<script src="/playbook.js" defer></script>'
