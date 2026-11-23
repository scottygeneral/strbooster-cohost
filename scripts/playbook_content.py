"""Free STR AI journey page (/playbook): nine open steps, each with .md resources.

Original STR Booster content. Nothing on the page is gated. Resources live in
assets/kits/*.md. A resource file that still contains the line
"STATUS: placeholder" is shown as "Coming soon" with no download link; remove
that line once the file is written and the page links it on the next build.

The full playbook is a separate document sent by email to newsletter signups.
The optional signup is the embedded HighLevel form "Newsletter Sign Up".
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT_DIR = ROOT / 'assets' / 'kits'
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
     [('business-brain', 'Business Brain template')]),
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
     [('review-reply-and-insights', 'Review Reply + Insight Miner')]),
    ('listings', 'Optimize your listings',
     'Most listings are written for the host, not the guest. The title, first photo and first two lines decide the click.',
     ['Run the Listing Audit for the guest you found in step 3.',
      'Make the free fixes first: title, photo order, opening lines, amenity names.',
      'Note your views and bookings now, then run the audit again in 30 days.'],
     'Audit this listing for my target guest. Score the title, first photo and photo order, opening lines, fit signals, amenities, objection handling, proof and house rules from 1 to 5 with evidence. Then give me the top five fixes, free ones first, and three rewritten titles.',
     '15 minutes per listing',
     [('listing-audit', 'Listing Audit')]),
    ('distribution', 'OTA distribution',
     'One channel is one algorithm change away from an empty calendar. Each channel has its own guests, limits and style.',
     ['Decide which channels matter for your guest: Airbnb, Vrbo, Booking.com, your own site.',
      'Keep the facts identical everywhere, and adapt titles and descriptions to each channel.',
      'Check once a quarter that photos, rules and amenities still match across channels.'],
     'Here is my Airbnb listing and my guest profile. Adapt the title and description for Vrbo, Booking.com and my direct booking site. Respect each channel’s style and title limits, keep every fact identical, and list anything a channel asks for that I have not given you.',
     '1 hour, then quarterly',
     [('ota-distribution', 'Channel Distribution kit')]),
    ('marketing', 'Marketing and sales',
     'No time for content, and past guests forgotten the day they check out. Your cheapest next booking is someone who already stayed.',
     ['Collect past-guest emails with consent, and send a short note each season.',
      'Turn real reviews and local events into posts. No stock phrases, no fake urgency.',
      'Answer every direct enquiry within five minutes, even with a holding reply.'],
     'Using my brand guide and guest profile, write a four-week plan: one past-guest email and two social posts a week, each built only from the reviews, photos and local events I give you. Keep my voice. No discounts unless I ask for one.',
     '1 hour a month',
     [('marketing-plan', 'Monthly Marketing Plan kit')]),
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
     [('guest-messaging-agent', 'Guest Messaging Agent')]),
]

GHL_FORM_ID = 'X2ch8hqmAh3G9qypYlVe'  # HighLevel form "Newsletter Sign Up" (STR Booster sub-account)


def resource_ready(slug):
    path = KIT_DIR / f'{slug}.md'
    return path.is_file() and PLACEHOLDER_MARK not in path.read_text(encoding='utf-8')


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
<iframe src="https://api.leadconnectorhq.com/widget/form/{GHL_FORM_ID}" id="inline-{GHL_FORM_ID}" class="pb-ghl-frame" title="Newsletter sign up" loading="lazy" data-layout="{{'id':'INLINE'}}" data-trigger-type="alwaysShow" data-trigger-value="" data-activation-type="alwaysActivated" data-activation-value="" data-deactivation-type="neverDeactivate" data-deactivation-value="" data-form-name="Newsletter Sign Up" data-height="320" data-layout-iframe-id="inline-{GHL_FORM_ID}" data-form-id="{GHL_FORM_ID}"></iframe>
<script src="https://link.msgsndr.com/js/form_embed.js" defer></script>
<p class="pb-consent-note">By subscribing you agree to get the playbook and the weekly STR Booster Brief by email. Unsubscribe any time. See our <a href="/privacy.html">privacy policy</a>.</p>
</div>'''


def journey_step(n, anchor, title, problem, todo, prompt, time, resources):
    items = ''.join(f'<li>{html.escape(t)}</li>' for t in todo)
    res = ''.join(resource_link(slug, name) for slug, name in resources)
    return (f'<li class="pb-jstep" id="step-{n}"><div class="pb-jnum" aria-hidden="true">{n}</div><div class="pb-jbody">'
            f'<p class="pb-jmeta">Step {n} of {len(JOURNEY)} · {html.escape(time)}</p>'
            f'<h3 id="{anchor}">{html.escape(title)}</h3>'
            f'<p class="pb-jproblem">{html.escape(problem)}</p>'
            f'<h4>Do this</h4><ol class="pb-jtodo">{items}</ol>'
            f'<div class="pb-prompt"><div class="pb-prompt-head"><span>Paste into Claude</span>'
            f'<button type="button" class="pb-copy" data-copy="prompt-{n}">Copy prompt</button></div>'
            f'<p id="prompt-{n}">{html.escape(prompt)}</p></div>'
            f'<h4>Resources</h4><div class="pb-res-list">{res}</div></div></li>')


def body():
    nav = ''.join(f'<li><a href="#step-{i}"><span>{i}</span>{html.escape(step[1].split(":")[0])}</a></li>'
                  for i, step in enumerate(JOURNEY, 1))
    hero = f'''<section class="pb-hero"><div class="wrap">
<div class="breadcrumb"><a href="/">Home</a> / The journey</div>
<p class="eyebrow">Free. Open. No sign-up needed.</p>
<h1>Your AI journey for short-term rentals, <em>one step at a time.</em></h1>
<p class="lead">Nine steps, in order, from a clear plan to happy guests. Each step has a prompt you can paste into Claude today and resources you can download. Nothing to buy, nothing to unlock.</p>
<p class="pb-hero-actions"><a class="btn" href="#step-1" data-cta="journey-start">Start at step 1</a><a class="text-link" href="#why">Why most hosts haven’t started</a></p>
<ol class="pb-jnav" aria-label="The nine steps">{nav}</ol>
</div></section>'''

    pains = ('<section class="section white" id="why"><div class="wrap"><div class="intro"><p class="eyebrow">Be honest</p>'
             '<h2>Why you haven’t started yet.</h2><p>You are not behind because you are not smart enough. You are tired of tools that promise a lot and add work. Fair. Here is how this is different.</p></div>'
             '<div class="pb-pains">' + ''.join(f'<article><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></article>' for q, a in PAINS)
             + '</div></div></section>')

    steps = ''.join(journey_step(i, *step) for i, step in enumerate(JOURNEY, 1))
    journey = ('<section class="section" id="journey"><div class="wrap"><div class="intro"><p class="eyebrow">The journey</p>'
               '<h2>Nine steps. Each one builds on the last.</h2>'
               '<p>Go in order. Open Claude (a free account is fine to start), create a project for your business, and paste each prompt in as you go.</p></div>'
               '<ol class="pb-journey">' + steps + '</ol></div></section>')

    signup = ('<section class="section white" id="get-the-kits"><div class="wrap"><div class="pb-closing"><div><p class="eyebrow">Optional</p>'
              '<h2 id="pb-signup-heading">Get the full playbook by email.</h2>'
              '<p>The complete STR AI Playbook goes to your inbox, followed by one short email a week with one idea you can use, and a note when a new resource drops. Free. Leave any time.</p></div>'
              + signup_form('pb-signup-form', 'pb-signup-heading') + '</div></div></section>')

    rows = ''.join(f'<li><span class="pb-idx-step">Step {i}</span><span class="pb-idx-title">{html.escape(step[1].split(":")[0])}</span>'
                   + ''.join(resource_link(slug, name) for slug, name in step[6]) + '</li>'
                   for i, step in enumerate(JOURNEY, 1))
    kits = ('<section class="section" id="kits"><div class="wrap"><div class="intro"><p class="eyebrow">All resources</p>'
            '<h2>Every resource, in one place.</h2>'
            '<p>Each file is plain Markdown. Upload it to Claude as a Skill, or add it to a Claude project. New ones are added as they are ready.</p></div>'
            '<ul class="pb-idx">' + rows + '</ul></div></section>')

    faq = ('<section class="section white" id="faq"><div class="wrap"><div class="intro"><p class="eyebrow">Questions</p><h2>Fair questions.</h2></div><div class="faq">'
           + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in [
               ('Is it really free?', 'Yes. The journey, the prompts, the resources and the emailed playbook are free, and there is nothing to buy. You do not need to sign up to use anything on this page.'),
               ('Why Claude?', 'One assistant, set up once with your facts, replaces a pile of single-purpose apps. Projects keep each property’s facts together, and Skills let Claude follow the same steps every time.'),
               ('Do I need a paid Claude plan?', 'You can start on the free plan. Projects, Skills and longer files work best on a paid Claude plan, which is what we use.'),
               ('Do I need to be technical?', 'No. Each step is plain language and a prompt to copy. Each resource is a text file you upload. If you can write a guest message, you can use these.'),
               ('Will the AI reply to my guests on its own?', 'Not unless you set it up to. Everything here drafts first, with clear rules for when a person must step in. Automate only what you have tested.'),
           ]) + '</div></div></section>')

    return hero + pains + journey + signup + kits + faq + '<script src="/playbook.js" defer></script>'
