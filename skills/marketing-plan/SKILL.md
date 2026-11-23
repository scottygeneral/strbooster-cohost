---
name: marketing-plan
description: Build a monthly marketing plan for a short-term rental. Four weeks of one past-guest email and two social posts a week, each built only from the host's real reviews, photos and local events, aimed at the nights the calendar needs to sell. Includes a guest circle (consent-based email list) with a welcome sequence, a five-minute enquiry reply, and an offer check that compares what each booking route keeps before any discount. Method from the book Booked Solid.
---

# Monthly Marketing Plan

Step 6 of the free STR Booster playbook (Marketing and sales). It gives one property (or a group of similar ones) a plan for next month that takes about an hour to run:

1. **Which nights need help?** Marketing starts from the calendar, not from a content calendar.
2. **What story sells them?** The guest is the hero and the property is the setting. Two or three guest stories carry the month.
3. **What goes out, and when?** One past-guest email and two social posts a week for four weeks, written out in full, each saying which review, photo or event it was built from.
4. **How does interest become a relationship?** A guest circle with one real privilege, a short welcome sequence, and a holding reply for every direct enquiry inside five minutes.
5. **Is an offer worth it?** Work out what each booking route keeps from the same stay before discounting anything. Usually a privilege beats a discount.

The output is a styled HTML/PDF plan in the property's colors, plus the posts and emails as plain text, ready to paste.

Use it when someone asks for a marketing plan, a content calendar, social posts or emails for their rental, how to get more direct bookings, what to send past guests, how to build an email list, how to fill a slow month, or "start the marketing step".

The person is usually a busy host or property manager with thin margins, too many apps and no time for content. Use what they already have: their phone camera, their reviews, the free scheduler in Meta Business Suite (or whatever they post with now), the email tool they already pay for, and Claude. Don't recommend new software.

## The method (from Booked Solid)

This skill follows the marketing chapters of *Booked Solid* by David Anthony Scott. Hold to these ideas:

- **The guest is the hero, the property is the setting.** A dining room is a feature. Three generations around one table is a story. Every post starts from a moment the guest wants, not a room tour.
- **A story has a person, a desire, a little tension and a moment of possibility.** "Beautiful accommodation" is not an angle. "The family organizer gets to enjoy the weekend too" is.
- **Real imagery only.** AI can help with scripts, captions and plans. A generated view or amenity the guest would believe is part of the property is not allowed.
- **Content is an investment, not an obligation to post.** Film one session, sort clips by guest moment ("slow morning", "arrival"), and reuse each clip across a reel, a still, a web section and an email.
- **Measure meaningful interest:** saves, thoughtful questions, profile visits, signups, enquiries and bookings. Not views.
- **A promotion is a particular invitation, not a substitute for positioning.** Decide who it's for, why now, what you can deliver and how someone responds. There is no universal promotion calendar.
- **Calculate before you discount.** A direct label doesn't make a booking more profitable. Compare what each route keeps after fees, acquisition and stay costs.
- **A privilege changes the experience or the access; a discount only lowers the price.** First access to dates, a returning-guest touch, a local introduction.
- **Capture is not consent.** Only people who chose to hear from you go on the list. Booking messages and marketing stay separate. Booking channels' off-platform rules apply.
- **The relationship sets the pace.** About one email a month, written like a host, with a person reading replies.

## The inputs come from earlier steps

Look for these files first and don't re-ask what they answer:

| Input | Where it comes from | What you take |
|---|---|---|
| Goals and guardrails | `business-brain.md` from **The Brain** skill (step 1) | The 12-month goal, the floor (lowest nightly rate after fees), rules never broken, and any strategy pointed at marketing. |
| Brand | `brand.md`, the brand core in the **Guest Experience Storyboard** JSON, or a Hospitality Brand Blueprint | Promise, voice, banned words (anti-vocabulary), palette and display font. |
| Ideal guest | The **Guest Intelligence Report** (JSON, HTML or PDF) | Who they are, what they want from the trip, pain points, booking triggers, where they research (Instagram, Facebook groups, search), occasion types and lead time. |
| Guest experience | The **Guest Experience Storyboard** | The signature moment, the after-stay and advocacy beats, scripts already in use. Marketing must promise only what the stay delivers. |
| Calendar plan | The plan JSON from the **OTA Distribution** skill (step 5) | Night classes (Peak, High, Shoulder, Soft, Gap), high-demand dates, the floor, and any "past guests first" release rule. |

If a file is missing, ask only the short version, one question at a time:
- **No brain:** "What's the one number you want to move this year, and what's the lowest nightly rate you'll take?"
- **No brand:** "In six words or fewer, why does a guest pick your place? And which words should never appear in your posts?"
- **No guest report:** "Who books most often, what are they hoping the trip feels like, and where do they look for places to stay?" Or offer to run the Guest Intelligence Report skill first.
- **No calendar plan:** "Which nights next month are still open, and which dates always sell out?"

Then ask for this month's material, in one message. **The plan is built only from this:**
- **Reviews:** paste the newest ones (or all of them if there are few). Quote them exactly. Don't use guest names.
- **Photos and clips:** a list or the files, with what each shows. If there are none, the plan includes a shot list for one filming session.
- **Local events and seasons:** what's happening next month near the property. You'll check dates (Step 2).
- **The list today:** how many past guests or subscribers have opted in to marketing, and which email tool they use. "None yet" is a normal answer: the plan then starts the guest circle.
- **Where they post now:** Instagram, Facebook, TikTok, none.
- **Offers:** whether they want any discount this month. Default is no.

## Step 1: Pick the month's job

From the calendar plan or the open nights, write one line: which nights this month must sell and the one relationship goal (for example "grow the circle before the 2027 football schedule drops"). List the dates in `nights`, each with its night class, status and the invitation that fits it. Peak nights are never discounted and often aren't marketed at all: they're the circle's privilege.

## Step 2: Check the facts

Never rely on memory for an event date, a platform rule or a fee. Before writing:
- Confirm every event date on the organizer's own page. If it isn't published yet, say "confirm" and how.
- Check the current off-platform and messaging rules of each booking channel the property uses.
- Reuse the fees from the OTA Distribution plan if they're less than three months old; otherwise check them.

**If you have the Agent tool**, send two researchers in parallel: an **event checker** ("List next month's events, holidays and seasonal moments within 30 minutes of [town] that fit [guest], with dates and source URLs") and a **rules checker** ("For [channels], find the current rules on contacting guests off-platform and using guest contact details, with source URLs"). **If not**, run both yourself with web search. Mark anything you can't confirm as "Unverified". Keep the sources for the last section of the plan.

## Step 3: Write two or three guest stories

For each `angle`, write: `name`, `guest` (the ideal guest in a specific situation), `desire`, `tension`, `moment` (one sentence the reader can see), `proof` (3 to 4 real facts that make the moment true) and `useFor`. Build them from the guest report's desires and pain points, the brand promise and the nights to sell. Every `proof` item must be a real fact from the listing, a review or the host. If a moment needs something the property doesn't have, change the moment.

## Step 4: Write the four weeks

Each week: one past-guest email and two social posts (the playbook's promise). For each item fill `type`, `channel`, `day`, `angle`, `builtFrom`, `hook`, `copy`, `cta`, and `shots` for posts or `subject` for emails.

Rules for the copy:
- `builtFrom` names the exact review, photo, clip or event used. If an item isn't built from supplied material, cut it.
- Quote reviews word for word, credited as "(guest review)". Never invent or improve a review.
- Write in the brand voice. None of the banned words. Specifics over adjectives: minutes, acres, bird names, the real view.
- Emails: under 150 words, from a person, with a reason to arrive (a season, a local find, a date release, a planning tip). Not every email asks for a booking. Use `{first name}`.
- Posts: the first line is the moment, not the property. Under 70 words of caption. One clear next step.
- No fake urgency, no countdowns, no "only 1 left", no exclamation marks, no hashtag walls.
- No discount unless the person asked for one. A seasonal note, a first look or a useful plan usually does more.
- Each week has a `theme` that matches a story and the nights it is selling.

## Step 5: Set up the guest circle

If there's no list yet, the circle is the most valuable thing this month builds. Fill `circle`:
- `name` and `invitation`: say why the guest would care, not "join our mailing list". Include the frequency.
- `privilege`: one benefit, explained in one sentence, that the host can deliver every time. First access to peak dates is the default when the calendar plan has a "past guests first" rule. Say its limits (first access is not a held date).
- `capture`: where people join (direct booking page, a printed card in the property, direct enquiries) and the consent rule for each. Marketing consent is a separate, unticked choice. Guests from Airbnb, Vrbo and other channels can only join by choosing to, never from contact details the channel provided.
- `welcome`: three short emails: right away (welcome, what to expect, a person reads replies), day 3 (something useful about the trip), day 7 (how the privilege works).

## Step 6: Write the enquiry replies

Fill `enquiry`: a `holding` reply the host can send inside five minutes (it says when the real answer comes and that dates aren't held yet), one `followUp` for a quiet enquirer, and the `rule` in one line. Answer the question before mentioning the circle.

## Step 7: Run the offer check

Before any offer, compare what the same stay leaves after costs (`offer.math`). Use the property's real price, cleaning fee, turnover and supply costs and channel fees; mark estimates "Est.". Include at least: the main OTA, direct to the circle at full price, direct with the discount being considered, and direct from a paid ad. Then:
- `decision` and `why`: usually "no discount, use the privilege", unless a discount on soft nights still beats the OTA booking and stays above the floor.
- `privilegeCost`: what the privilege or perk costs to deliver.
- `ceiling`: the most a direct booking can cost to win and still beat the OTA booking (direct contribution before acquisition, minus the OTA contribution).

## Step 8: Add discovery, scenes and the hour

- `discovery`: 2 to 4 routes beyond social: one genuinely helpful search page for the direct site, the Google Vacation Rentals connection (from step 5), community groups where self-promotion is allowed, and one local partner (a feature swap, no money and no referral deals).
- `sceneLibrary`: 4 to 5 guest moments with the shots to capture and where each is used.
- `routine`: the hour a month (gather, run, edit, schedule, read the numbers).
- `never`: 5 to 6 rules. `measures`: 4 to 5 numbers about meaningful interest and booked nights by source.
- `sources`: every review, photo set, event and fee used, with where it came from.

## Step 9: Fill the plan JSON

Keys are fixed and the template reads them.

```json
{
 "propertyName": "", "location": "City, ST", "preparedFor": "", "date": "Month Year", "month": "The month planned",
 "brand": {"promise": "", "voice": "", "antiVocabulary": [""], "palette": {"ink": "#", "ground": "#", "accent": "#", "support": "#"}, "displayFont": "Georgia"},
 "inputs": {"goal": "", "goalSource": "", "guest": "name, age, one line", "guestWhere": "where they look and how far ahead they book",
  "monthJob": "", "monthWhy": "", "floor": "Floor $X a night, after fees", "rules": [""]},
 "planLine": "The month in two or three sentences.",
 "nights": [{"when": "", "class": "Peak | High | Shoulder | Soft | Gap", "status": "", "ask": "", "confirm": "optional"}],
 "angles": [{"name": "", "guest": "", "desire": "", "tension": "", "moment": "", "proof": [""], "useFor": ""}],
 "weeks": [{"week": "Week 1 · dates", "theme": "",
  "items": [{"type": "Past-guest email | Social post", "channel": "", "day": "", "angle": "", "builtFrom": "",
   "hook": "", "subject": "emails only", "copy": "", "cta": "", "shots": ["posts only"]}]}],
 "circle": {"name": "", "invitation": "", "privilege": "", "frequency": "",
  "capture": [{"route": "", "how": "", "consent": ""}], "welcome": [{"when": "", "subject": "", "body": ""}]},
 "enquiry": {"rule": "", "holding": "", "followUp": ""},
 "offer": {"note": "", "math": {"basis": "", "rows": [{"route": "", "math": "", "keep": ""}]},
  "decision": "", "why": "", "privilegeCost": "", "ceiling": ""},
 "discovery": [{"route": "", "action": "", "note": ""}],
 "sceneLibrary": [{"scene": "", "shots": [""], "use": ""}],
 "routine": [{"when": "", "task": "", "minutes": ""}],
 "never": [""], "measures": [""],
 "sources": [{"item": "", "source": ""}],
 "footer": "Say what is estimated and which dates still need confirming."
}
```

Use `\n` for line breaks inside `copy` and `body`. Sort `offer.math.rows` by contribution, highest first.

## Step 10: Render

1. Save the template below as `marketing-plan.html`.
2. Replace the `{}` inside `<script type="application/json" id="plan-data">` with your JSON. Change nothing else. If any string contains `</`, write it as `<\/`.
3. Make the PDF if you can run code: open the HTML in headless Chromium (Playwright `page.pdf({format:'Letter', printBackground:true})`, or `chrome --headless --print-to-pdf`). Otherwise deliver the HTML and tell the person to open it and use Print, then Save as PDF.
4. Look at the result before you deliver it. Check for empty sections, raw HTML and banned words.
5. Name files `marketing-plan-{property-slug}-{month}.html/.pdf`.

## Step 11: Hand it over

Deliver the PDF (or HTML) with a 3-line summary: the month's job, the two stories, and the offer decision. Then give every email and post as plain text, in order, ready to paste into the scheduler and email tool. Offer:
- The circle invitation and welcome emails as plain text for their email tool.
- A shot list for one filming session, if they're short on photos.
- To save the plan JSON next to `business-brain.md`, so next month's run can see what was sent and what worked.

Tell them to run it again at the start of each month with new reviews, photos and events, and to bring the numbers from the last month.

## Rules

- Build only from the reviews, photos and events the person gives you. Name the source of every piece.
- Never invent a review, an amenity, a view, a guest or a result. Real imagery only.
- No discounts unless asked. Never discount peak nights or go below the floor.
- Only email people who opted in to marketing. Keep booking messages and marketing separate. Respect each booking channel's off-platform rules.
- No fake urgency or scarcity. No banned brand words. Never offer anything for a review.
- Check every event date and rule, with a source. Anything unconfirmed says "confirm" or "Unverified".
- No affiliate or referral links, and no paid tools the person didn't ask for. Use what they have plus Claude.
- The guest is a composite. Don't use real guest names, faces or words without permission.
- Keep sentences short and concrete.

## Files in this kit

- `SKILL.md`: these instructions, with the template below.
- `template.html`: the same template as a file.
- `sample-songbird-acres.json`, `.html`, `.pdf`: a sample January plan for Songbird Acres, a studio on 11 acres near Athens, GA. Its goal, review lines, photos and costs are demo values.

## Template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Monthly Marketing Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--ink:#1a1a1a;--ground:#f6f2ea;--accent:#f07c33;--support:#3d5a48;--paper:#fff;--line:#e4ddd0;--mute:#6f6a60;--display:Georgia,'Times New Roman',serif}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font:13px/1.5 Inter,system-ui,sans-serif}
.page{max-width:900px;margin:0 auto;padding:32px 24px}
h1,h2,h3,.disp{font-family:var(--display);font-weight:400;margin:0}
h2{font-size:24px;margin:34px 0 4px;break-after:avoid}
.kicker{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700}
.mute{color:var(--mute)}
.lbl{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);font-weight:600;margin-bottom:3px}
.head{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;border-bottom:2px solid var(--ink);padding-bottom:10px}
.head .disp{font-size:30px;line-height:1.1}
.head .meta{text-align:right;font-size:12px}
.banner{background:var(--accent);color:#fff;font-weight:800;font-size:32px;letter-spacing:.02em;text-transform:uppercase;text-align:center;padding:14px 10px;margin:18px -24px 0;line-height:1.1}
.banner small{display:block;font-size:13px;letter-spacing:.14em;font-weight:700;opacity:.9;margin-top:4px}
.promise{background:var(--ink);color:#fff;text-align:center;padding:14px 20px;margin:0 -24px}
.promise .disp{font-size:22px;font-style:italic}
.promise .sub{font-size:12px;opacity:.75;margin-top:4px}
.inputs{display:grid;grid-template-columns:repeat(4,1fr);border:2px solid var(--ink);margin-top:20px}
.inputs>div{padding:10px 12px;border-right:2px solid var(--ink)}
.inputs>div:last-child{border-right:0}
.inputs b{display:block;font-size:13.5px;line-height:1.35}
.inputs span{display:block;color:var(--mute);font-size:11.5px;margin-top:2px}
.oneline{font-family:var(--display);font-size:19px;line-height:1.4;margin:22px 0 0;padding-left:14px;border-left:4px solid var(--accent)}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{text-align:left;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);font-weight:600;padding:6px;border-bottom:2px solid var(--ink)}
td{padding:7px 6px;border-bottom:1px solid var(--line);vertical-align:top}
.why{color:var(--mute);font-size:11.5px}
.pill{display:inline-block;border-radius:999px;padding:2px 9px;font-size:11px;font-weight:700;white-space:nowrap;background:var(--ground);border:1px solid var(--accent)}
.pill.email{background:var(--support);border-color:var(--support);color:#fff}
.pill.post{background:var(--ground)}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:12px}
.card{background:var(--paper);border:2px solid var(--ink);break-inside:avoid;display:flex;flex-direction:column}
.card .top{background:var(--ground);border-bottom:2px solid var(--ink);padding:10px 14px}
.card .top h3{font-family:Inter,sans-serif;font-weight:800;font-size:16px}
.card .body{padding:10px 14px 12px;display:grid;gap:7px}
.card ul{margin:0;padding-left:16px}
.moment{font-family:var(--display);font-style:italic;font-size:14.5px;border-left:3px solid var(--accent);padding-left:8px}
.week{border:2px solid var(--ink);margin-top:16px;break-inside:avoid}
.week .wk{display:flex;justify-content:space-between;gap:12px;align-items:baseline;background:var(--ink);color:#fff;padding:8px 14px}
.week .wk b{font-size:15px}
.week .wk span{font-size:12px;opacity:.85}
.item{display:grid;grid-template-columns:150px 1fr;gap:14px;padding:12px 14px;border-top:1px solid var(--line);break-inside:avoid}
.item:first-of-type{border-top:0}
.item .side{font-size:11.5px;color:var(--mute);display:grid;gap:6px;align-content:start}
.item .hook{font-weight:700;font-size:13.5px}
.copy{white-space:pre-line;background:var(--ground);border-left:3px solid var(--accent);padding:8px 10px;margin:6px 0;font-size:12.5px}
.subj{font-size:12px;margin-top:2px}
.row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.box{border:1px solid var(--line);border-radius:10px;padding:14px;break-inside:avoid}
ul.plain{margin:4px 0 0;padding-left:18px}
ul.plain li{margin:0 0 4px}
.seq{display:grid;gap:10px;margin-top:10px}
.seq .copy{margin:4px 0 0}
.econ td:last-child{font-weight:700}
.decision{background:var(--support);color:#fff;padding:12px 14px;margin-top:10px;font-size:13.5px}
.decision b{display:block;font-size:15px;margin-bottom:2px}
.foot{margin-top:30px;border-top:2px solid var(--ink);padding-top:10px;font-size:11px;color:var(--mute)}
@media (max-width:700px){.inputs,.cards,.row,.item{grid-template-columns:1fr}.inputs>div{border-right:0;border-bottom:2px solid var(--ink)}.banner{font-size:22px}.scroll{overflow-x:auto}}
@media print{.page{padding:18px 20px}.banner,.promise{margin-left:-20px;margin-right:-20px}h2{margin-top:24px}}
</style>
</head>
<body>
<div class="page" id="app"></div>
<script type="application/json" id="plan-data">{}</script>
<script>
const D = JSON.parse(document.getElementById('plan-data').textContent);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const B = D.brand || {};
const P = B.palette || {};
for (const k of ['ink','ground','accent','support']) if (P[k]) document.documentElement.style.setProperty('--' + k, P[k]);
if (B.displayFont) document.documentElement.style.setProperty('--display', B.displayFont + ", Georgia, serif");
const list = a => (a || []).map(x => '<li>' + esc(x) + '</li>').join('');
const I = D.inputs || {};
let h = '';
let n = 0;
const sec = (title, note) => { n++; return `<h2>${n}. ${esc(title)}</h2>` + (note ? `<p class="mute">${esc(note)}</p>` : ''); };

h += `<div class="head"><div><div class="kicker">STR Booster playbook · Step 6</div><div class="disp">${esc(D.propertyName)}</div><div class="mute">${esc(D.location)}</div></div>
<div class="meta">Prepared for <b>${esc(D.preparedFor)}</b><br>${esc(D.date)}</div></div>`;
h += `<div class="banner">Marketing Plan<small>${esc(D.month)}</small></div>`;
if (B.promise) h += `<div class="promise"><div class="disp">“${esc(B.promise)}”</div><div class="sub">The guest is the hero. The property is the setting. Every post and email below keeps this promise.</div></div>`;
h += `<div class="inputs">
<div><div class="lbl">Goal</div><b>${esc(I.goal)}</b><span>${esc(I.goalSource)}</span></div>
<div><div class="lbl">Ideal guest</div><b>${esc(I.guest)}</b><span>${esc(I.guestWhere)}</span></div>
<div><div class="lbl">This month's job</div><b>${esc(I.monthJob)}</b><span>${esc(I.monthWhy)}</span></div>
<div><div class="lbl">Guardrails</div><b>${esc(I.floor)}</b><span>${esc((I.rules || []).join(' · '))}</span></div></div>`;
if (D.planLine) h += `<p class="oneline">${esc(D.planLine)}</p>`;

const nights = D.nights || [];
if (nights.length) {
  h += sec('The nights this month has to sell', 'Marketing starts from the calendar, not from a content calendar. These are the dates that need help, and the invitation that fits each one.');
  h += `<div class="scroll"><table><thead><tr><th>When</th><th>Class</th><th>Status</th><th>The invitation</th></tr></thead><tbody>`;
  for (const x of nights) h += `<tr><td><b>${esc(x.when)}</b>${x.confirm ? `<div class="why">${esc(x.confirm)}</div>` : ''}</td><td>${esc(x.class)}</td><td>${esc(x.status)}</td><td>${esc(x.ask)}</td></tr>`;
  h += `</tbody></table></div>`;
}

const angles = D.angles || [];
if (angles.length) {
  h += sec('The guest stories', 'Each angle has a person, a desire, a little tension and a moment of possibility. The property only appears as the setting that makes the moment real.');
  h += `<div class="cards">`;
  for (const a of angles) h += `<div class="card"><div class="top"><h3>${esc(a.name)}</h3><div class="why">${esc(a.guest)}</div></div><div class="body">
<div><div class="lbl">Wants</div>${esc(a.desire)}</div>
<div><div class="lbl">Tension</div>${esc(a.tension)}</div>
<div class="moment">${esc(a.moment)}</div>
<div><div class="lbl">True because</div><ul>${list(a.proof)}</ul></div>
${a.useFor ? `<div><div class="lbl">Use it for</div>${esc(a.useFor)}</div>` : ''}
</div></div>`;
  h += `</div>`;
}

const weeks = D.weeks || [];
if (weeks.length) {
  h += sec('The four weeks', 'One past-guest email and two social posts a week. Every piece is built only from the reviews, photos and local events supplied, and says which one.');
  for (const w of weeks) {
    h += `<div class="week"><div class="wk"><b>${esc(w.week)}</b><span>${esc(w.theme)}</span></div>`;
    for (const it of (w.items || [])) {
      const isEmail = /email/i.test(it.type || '');
      h += `<div class="item"><div class="side"><span><span class="pill ${isEmail ? 'email' : 'post'}">${esc(it.type)}</span></span>
<span><b>${esc(it.channel)}</b>${it.day ? ' · ' + esc(it.day) : ''}</span>
<span><span class="lbl">Angle</span><br>${esc(it.angle)}</span>
<span><span class="lbl">Built from</span><br>${esc(it.builtFrom)}</span></div>
<div><div class="hook">${esc(it.hook)}</div>${it.subject ? `<div class="subj"><span class="lbl">Subject</span> ${esc(it.subject)}</div>` : ''}
<div class="copy">${esc(it.copy)}</div>
<div class="why"><b>Next step:</b> ${esc(it.cta)}</div>
${it.shots && it.shots.length ? `<div class="why"><b>Shots:</b> ${it.shots.map(esc).join(' · ')}</div>` : ''}</div></div>`;
    }
    h += `</div>`;
  }
}

const C = D.circle;
if (C) {
  h += sec('The guest circle', 'Interest that ends at a booking button disappears. The circle keeps the relationship going, with permission, until the next trip is possible.');
  h += `<div class="row"><div class="box"><div class="lbl">Name</div><b>${esc(C.name)}</b>
<div class="lbl" style="margin-top:10px">The invitation</div><div class="copy">${esc(C.invitation)}</div>
<div class="lbl" style="margin-top:10px">The one privilege</div>${esc(C.privilege)}
<div class="lbl" style="margin-top:10px">How often</div>${esc(C.frequency)}</div>
<div class="box"><div class="lbl">Where people join</div><table><tbody>`;
  for (const r of (C.capture || [])) h += `<tr><td><b>${esc(r.route)}</b><div class="why">${esc(r.how)}</div><div class="why"><b>Consent:</b> ${esc(r.consent)}</div></td></tr>`;
  h += `</tbody></table></div></div>`;
  if ((C.welcome || []).length) {
    h += `<div class="seq"><div class="lbl" style="margin-top:12px">Welcome sequence</div>`;
    for (const m of C.welcome) h += `<div class="box"><b>${esc(m.when)}</b> · <span class="mute">Subject:</span> ${esc(m.subject)}<div class="copy">${esc(m.body)}</div></div>`;
    h += `</div>`;
  }
}

const E = D.enquiry;
if (E) {
  h += sec('Every direct enquiry, inside five minutes', E.rule);
  h += `<div class="row"><div class="box"><div class="lbl">Holding reply (send within 5 minutes)</div><div class="copy">${esc(E.holding)}</div></div>
<div class="box"><div class="lbl">One follow-up, if they go quiet</div><div class="copy">${esc(E.followUp)}</div></div></div>`;
}

const O = D.offer;
if (O) {
  h += sec('The offer check', O.note);
  if (O.math && O.math.rows) {
    h += `<div class="scroll"><table class="econ"><thead><tr><th>Route</th><th>How it is worked out (${esc(O.math.basis)})</th><th>Contribution</th></tr></thead><tbody>`;
    for (const r of O.math.rows) h += `<tr><td><b>${esc(r.route)}</b></td><td class="mute">${esc(r.math)}</td><td>${esc(r.keep)}</td></tr>`;
    h += `</tbody></table></div>`;
  }
  h += `<div class="decision"><b>${esc(O.decision)}</b>${esc(O.why)}</div>`;
  if (O.ceiling || O.privilegeCost) h += `<div class="row" style="margin-top:12px">${O.privilegeCost ? `<div class="box"><div class="lbl">What the privilege costs</div>${esc(O.privilegeCost)}</div>` : ''}${O.ceiling ? `<div class="box"><div class="lbl">Most you'd pay to win one booking</div>${esc(O.ceiling)}</div>` : ''}</div>`;
}

const disc = D.discovery || [];
if (disc.length) {
  h += sec('Other ways to be found', 'Social creates desire before dates are chosen. These routes reach people who are already planning.');
  h += `<table><thead><tr><th>Route</th><th>This month</th></tr></thead><tbody>`;
  for (const r of disc) h += `<tr><td><b>${esc(r.route)}</b></td><td>${esc(r.action)}${r.note ? `<div class="why">${esc(r.note)}</div>` : ''}</td></tr>`;
  h += `</tbody></table>`;
}

const scenes = D.sceneLibrary || [];
if (scenes.length) {
  h += sec('The scene library', 'One filming session, sorted by guest moment rather than by room, so each clip can serve a reel, a still, a website section and an email.');
  h += `<table><thead><tr><th>Moment</th><th>Shots to capture</th><th>Use</th></tr></thead><tbody>`;
  for (const s of scenes) h += `<tr><td><b>${esc(s.scene)}</b></td><td>${esc((s.shots || []).join(' · '))}</td><td>${esc(s.use)}</td></tr>`;
  h += `</tbody></table>`;
}

h += sec('The hour, the rules and the numbers');
h += `<div class="row"><div class="box"><div class="lbl">One hour a month</div><table><tbody>`;
for (const r of (D.routine || [])) h += `<tr><td style="white-space:nowrap"><b>${esc(r.when)}</b></td><td>${esc(r.task)}</td><td style="white-space:nowrap" class="why">${esc(r.minutes)}</td></tr>`;
h += `</tbody></table></div><div class="box"><div class="lbl">Never</div><ul class="plain">${list(D.never)}</ul><div class="lbl" style="margin-top:12px">Measure it monthly</div><ul class="plain">${list(D.measures)}</ul></div></div>`;

if ((D.sources || []).length) {
  h += sec('Where every piece came from');
  h += `<table><thead><tr><th>Material</th><th>Source</th></tr></thead><tbody>`;
  for (const s of D.sources) h += `<tr><td><b>${esc(s.item)}</b></td><td>${esc(s.source)}</td></tr>`;
  h += `</tbody></table>`;
}
h += `<div class="foot">${esc(D.footer)}<br>Made with the free Marketing Plan skill from STR Booster · strbooster.com/skills · Method from Booked Solid by David Anthony Scott</div>`;
document.getElementById('app').innerHTML = h;
</script>
</body>
</html>
```
