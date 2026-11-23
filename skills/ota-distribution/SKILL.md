---
name: ota-distribution
description: Build an OTA distribution plan for a short-term rental. Match the property, brand and ideal guest to the best booking channels (Airbnb, Vrbo, Booking.com, direct and niche ones such as Whimstay or Hipcamp), say how to position the listing for each channel's users, and decide which high-demand nights open on which channel. Sends research subagents to check channels, fees and demand dates.
---

# OTA Distribution Plan

Step 5 of the free STR Booster playbook. It answers three questions for one property (or a group of similar ones):

1. **Where should it list?** Every channel scored against the ideal guest, the brand, the strategy, the money kept and the effort, with a verdict: Core, Test or Skip.
2. **How should it be positioned on each one?** Each channel's users arrive with a different question. Same facts everywhere, a different first line.
3. **Which nights open where?** Nights are sorted by demand. Peak nights go to the channels that net the most and reach the guest who books early. Soft nights and gaps can go to discount or niche channels. Nothing sells below the floor.

The output is a styled HTML/PDF plan in the property's colors, plus a short summary in chat.

Use it when someone asks where to list their rental, which OTAs or booking sites to use, whether to join Vrbo, Booking.com, Whimstay, Hipcamp or another channel, how to fill last-minute gaps, how to handle event weekends across channels, or "start the OTA distribution step".

The person is usually a busy host or property manager with thin margins and too many apps already. Every channel adds work. Recommend the fewest channels that do the job, and give every test channel an exit rule.

## The inputs come from earlier steps

This step reads what the earlier playbook steps produced. Look for these files first and don't re-ask what they answer:

| Input | Where it comes from | What you take |
|---|---|---|
| Goals and guardrails | `business-brain.md` from **The Brain** skill (step 1) | The 12-month goal (occupancy, nightly rate or NOI), the floor (break-even nightly rate or the person's "never under" rule), the rules they never break, and the strategies that point at step 5. |
| Brand promise | `brand.md` or the brand core from the **Guest Experience Storyboard** skill, or a Hospitality Brand Blueprint | The promise (6 words or fewer), voice, banned words and palette. |
| Ideal guest | The **Guest Intelligence Report** (its JSON, HTML or PDF) | Who books, how far ahead, which channels they use, what triggers a booking, the market's peak seasons and events. |
| The listing | The Airbnb or other listing URL | Facts, photos, house rules, current channels. |

If a file is missing, ask only the short version, one question at a time:
- **No brain:** "What's the one number you want to move this year: more booked nights, a higher nightly rate, or more profit? And what's the lowest nightly rate you'll ever take?"
- **No brand:** "In six words or fewer, why does a guest pick your place over the cheaper one down the road?"
- **No guest report:** "Who books most often, how far ahead do they book, and where do they search?" Or offer to run the Guest Intelligence Report skill first.

Then ask two things the earlier steps don't cover, in one message:
- Which channels it's on today, and how they connect: a channel manager or PMS (which one), or iCal links.
- Whether they lean toward any strategy already. Offer these: **premium early** (sell peaks far ahead at full price), **last-minute fill** (lots of short-notice gaps to sell), **mid-term** (30+ night stays), **event peaks plus soft-night fill**, or **not sure**.

## Step 1: Set the strategy lean

Pick one lean and write it in one line with the reason. It drives which niche channels make the cut:

| Lean | When it fits | Channels it pulls in |
|---|---|---|
| Premium early | Strong peak demand, guests who book months ahead | Airbnb, Vrbo, direct, Booking.com late release on peaks |
| Last-minute fill | Many unsold nights inside 30 days, drive-to market | Whimstay, Booking.com, Airbnb last-minute pricing |
| Event peaks plus soft-night fill | A few event weekends make the year, quiet weekdays | Core channels for peaks, a niche channel for soft nights |
| Mid-term | Hospital, university or corporate demand, slow winters | Furnished Finder, Airbnb and Vrbo monthly settings |
| Unique or land stay | Acreage, cabins, glamping, farm | Hipcamp, Glamping Hub |
| Premium or design home | High-end, professionally managed | Marriott Homes & Villas, Plum Guide (both vet hard) |

If the portfolio leans to last-minute bookings, Whimstay is the first niche channel to test. If the brain's goal is a higher nightly rate rather than more nights, be careful with any channel that requires a discount.

## Step 2: Research (send subagents)

Fees, programs and channels change every few months. Never rely on memory for a fee, a rule or an event date. Research first.

**If you have the Agent tool** (Claude Code, Cowork or another agent setup), send these four researchers in parallel, in one message, each with the property's town, type, size, the guest summary and the strategy lean. Ask each to return a short list of findings, each with a source URL and the date it was checked, and to mark anything it couldn't confirm as "Unverified".

**If you don't have the Agent tool** (Claude.ai chat), run the four briefs yourself, one after another, with web search. Tell the person you're doing it, because it takes a few minutes.

1. **Channel scout.** "Find the booking channels that list rentals like this near [town]: the big OTAs, and niche ones that fit a [property type] for [guest]: last-minute (such as Whimstay), land and glamping (Hipcamp, Glamping Hub), mid-term (Furnished Finder), family, pet-friendly, LGBTQ+ (such as Misterb&b), premium or design homes, and channels that matter for travelers from abroad (Booking.com, Agoda, Trip.com). For each, say who its users are, whether it lists properties in this area, and whether it accepts independent hosts or only property managers."
2. **Fee checker.** "For each of these channels: [shortlist], find the current host commission or fee, any guest service fee, required discounts, payment processing, rate or availability terms, whether it connects to [their channel manager or PMS] or only by iCal, and any changes announced in the last 12 months. Use the platform's own help pages first, then PMS and channel-manager guides."
3. **Demand mapper.** "List the nights that sell out or spike in price every year near [town] for the next 12 months: events, university dates, sports schedules, festivals, holidays and seasons. Give each one dates (or 'dates not published yet') and a source."
4. **Comp checker.** "Find 5 to 10 listings like this near [town] (same size and type) and note which channels each appears on, their nightly rates on peak and normal nights, and how they describe themselves on each channel."

When they report back, merge the findings. Where two sources disagree, use the platform's own page and note the other. Keep a research log for section 7 of the plan.

## Step 3: Score every channel

Score each channel from the scout's list 1 to 5 on five things, and add them up (out of 25):

- **Guest**: how many of its users look like the ideal guest. This matters most.
- **Brand**: whether the channel's style and audience fit the promise (a quiet farm stay on a party-weekend deal app is a poor fit).
- **Strategy**: whether it serves the lean from Step 1.
- **Money kept**: what you keep from a typical night after its fees and any required discount. Work it out in section 3.
- **Easy**: setup and ongoing effort. Score lower if it only syncs by iCal, needs separate pricing or vets hard.

Then give a verdict:
- **Core** (usually 2 to 3 channels): carries the calendar. Usually the channel where the ideal guest starts, a second big one, and a direct booking page for repeat guests.
- **Test** (at most 2 at a time): a 60-day trial with a written keep rule, such as "3 bookings at or above the floor in 60 days". A test channel never gets peak nights unless a release rule says so.
- **Skip**: one line on why, and when to look again.

Include the direct booking page every time. It is the only channel with no commission, and repeat guests should land there. Say plainly when it needs work the person may not have time for.

## Step 4: Position the listing for each channel

For every Core and Test channel, write:
- `userBase`: who is on it, in one or two plain sentences.
- `angle`: how to position the property for those users, in one line, true to the brand promise.
- `title`: a title written for that channel's users. Respect each channel's title limit (check it in research; Airbnb's is 50 characters).
- `emphasize`: 3 to 4 things to lead with. `avoid`: 2 to 3 things to leave out.
- `fee`, `feeChecked` (month and year), `sync`, `setup` steps, and for Test channels an `exitRule`.

Rules for positioning:
- Facts never change between channels: beds, stairs, rules, amenities, photos of what's there. Only the order and the first lines change.
- No banned brand words. No fake urgency.
- Never promise anything a channel doesn't allow, and never suggest moving a guest off a platform mid-booking.

## Step 5: Decide which nights open where

**Sort the next 12 months into night classes.** Use the demand mapper's dates and the guest report's seasons. The usual five:

| Class | What it is |
|---|---|
| Peak | Nights that sell out every year: big events, graduation, holidays in hot markets |
| High | Strong but not sold-out nights: smaller events, prime-season weekends |
| Shoulder | Normal weekends |
| Soft | Weekdays outside events, the slow season |
| Gap | 1 or 2 empty nights between stays, inside 14 days |

**For each class and each Core or Test channel, choose one state:**
- **Open**: available from the start.
- **Late**: opens only if still unsold at a set number of days out (say "if unsold 21 days out").
- **Closed**: never available on that channel.

**The rules for high-demand nights:**
1. Open peak nights first on the channels where the ideal guest books early and where you keep the most. Set the dates the moment the event dates are known.
2. Give past guests first pick (a day or two early on the direct page) when the person has a past-guest list.
3. Never put a peak or high night on a channel that requires a discount. Whimstay, for example, requires at least 15% off for bookings inside 30 days, so peak nights stay closed there.
4. Use late release for channels with weaker guest fit but strong reach on event dates (often Booking.com for hotel shoppers and travelers from abroad).
5. Peak nights only go on channels connected through the channel manager or PMS, never iCal only. iCal sync can lag by hours and double-book the best night of the year.
6. Set minimum stays and cancellation terms per class. Firmer on peaks, looser on soft nights and gaps.
7. Check every channel's net against the floor. If a required discount plus fees would take a night below the floor, that channel only gets nights priced high enough. Work out the lowest rate it can take: floor ÷ (1 − discount), and say it in plain words (for example "only nights priced $152 or more, so 15% off stays above $129").
8. Before setting different prices on different channels, read each channel's rate terms. Some contracts require rate parity. Mention commissions as facts. Don't advise breaking a channel's rules.

**List the high-demand nights** with their dates (or "confirm when published"), why they sell, their class and the release plan per channel.

## Step 6: Fill the plan JSON

Keys are fixed and the template reads them.

```json
{
 "propertyName": "", "location": "City, ST", "preparedFor": "", "date": "Month Year",
 "brand": {"promise": "", "palette": {"ink": "#", "ground": "#", "accent": "#", "support": "#"}, "displayFont": "Georgia"},
 "inputs": {"goal": "", "goalSource": "From the brain, or what the person said",
  "guest": "name, age, one line", "guestBooks": "how far ahead and where",
  "strategyLean": "", "strategyWhy": "", "floor": "Floor $X a night, after fees", "rules": [""]},
 "planLine": "The whole plan in two or three sentences.",
 "channels": [
  {"name": "", "verdict": "Core | Test | Skip", "role": "Main engine | Repeat guests | Soft nights | ...",
   "why": "one line", "scores": {"guest": 1, "brand": 1, "strategy": 1, "economics": 1, "effort": 1},
   "userBase": "", "positioning": {"angle": "", "title": "", "emphasize": [""], "avoid": [""]},
   "fee": "", "feeChecked": "Mon YYYY", "sync": "", "setup": [""], "exitRule": "Test channels only"}
 ],
 "economics": {"basis": "$200 night", "note": "", "rows": [{"channel": "", "math": "", "keep": ""}]},
 "nightClasses": [
  {"name": "Peak", "definition": "", "minStay": "",
   "release": {"<channel name exactly as above>": {"state": "open | late | closed", "note": "short"}}}
 ],
 "highDemandNights": [{"when": "", "confirm": "how to confirm the date", "event": "", "class": "", "plan": ""}],
 "rollout": [{"when": "Week 1", "task": "", "owner": ""}],
 "never": ["5-6"], "measures": ["4-5"],
 "research": [{"agent": "Channel scout | Fee checker | Demand mapper | Comp checker", "question": "", "finding": "", "sources": [""]}],
 "footer": "Say what is estimated, when fees were checked, and which dates still need confirming."
}
```

Skip channels need only `name`, `verdict`, `why` and `scores`. Every channel in `release` must use the exact `name` from `channels`. Use the real channel names, and keep the economics rows sorted by what you keep, highest first.

## Step 7: Render

1. Save the template below as `ota-distribution-plan.html`.
2. Replace the `{}` inside `<script type="application/json" id="plan-data">` with your JSON. Change nothing else. If any string contains `</`, write it as `<\/`.
3. Make the PDF if you can run code: open the HTML in headless Chromium (Playwright `page.pdf({format:'Letter', printBackground:true})`, or `chrome --headless --print-to-pdf`). Otherwise deliver the HTML and tell the person to open it and use Print, then Save as PDF.
4. Look at the result before you deliver it. Check for empty cells, raw HTML and wrapped tables.
5. Name files `ota-distribution-plan-{property-slug}.html/.pdf`.

## Step 8: Hand it over

Deliver the PDF (or HTML) with a 3-line summary: the core channels, the one test to start this month, and the peak-night rule. Then offer:
- The channel titles and opening lines as plain text, ready to paste.
- The release rules as a short checklist for the pricing tool or channel manager.
- To save the plan JSON next to `business-brain.md`, so step 7 (revenue management) can use the night classes and the floor.

Tell them to re-run it every quarter, and whenever a channel announces a fee change.

## Rules

- Research before you recommend. Every fee, program and event date has a source and the month it was checked. Anything not confirmed says "Unverified" or "Est.".
- Mention commissions as facts only. Never call a channel cheap or expensive without the numbers.
- Fewest channels that do the job. At most two tests at a time, each with a keep rule.
- Never discount peak nights. Never let any channel sell below the floor after fees and discounts.
- Peak nights only on channels connected by API through a channel manager or PMS.
- Same facts on every channel. No banned brand words, no fake urgency.
- Respect each channel's terms (rate parity, review rules, off-platform rules). Never tie anything to a review.
- No affiliate or referral links, and no paid tools the person didn't ask for. Use what they have plus Claude.
- The guest is a composite. Don't use real guest names.
- Keep sentences short and concrete.

## Files in this kit

- `SKILL.md`: these instructions, with the template below.
- `template.html`: the same template as a file.
- `sample-songbird-acres.json`, `.html`, `.pdf`: a sample plan for Songbird Acres, a studio on 11 acres near Athens, GA.

## Template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OTA Distribution Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--ink:#1a1a1a;--ground:#f6f2ea;--accent:#f07c33;--support:#3d5a48;--paper:#fff;--line:#e4ddd0;--mute:#6f6a60;--open:#2f7d4f;--late:#c98a1b;--closed:#a94438;--display:Georgia,'Times New Roman',serif}
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
.promise{background:var(--ink);color:#fff;text-align:center;padding:14px 20px;margin:0 -24px}
.promise .disp{font-size:22px;font-style:italic}
.promise .sub{font-size:12px;opacity:.75;margin-top:4px}
.inputs{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border:2px solid var(--ink);margin-top:20px}
.inputs>div{padding:10px 12px;border-right:2px solid var(--ink)}
.inputs>div:last-child{border-right:0}
.inputs b{display:block;font-size:13.5px;line-height:1.35}
.inputs span{display:block;color:var(--mute);font-size:11.5px;margin-top:2px}
.oneline{font-family:var(--display);font-size:19px;line-height:1.4;margin:22px 0 0;padding-left:14px;border-left:4px solid var(--accent)}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{text-align:left;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);font-weight:600;padding:6px 6px;border-bottom:2px solid var(--ink)}
td{padding:7px 6px;border-bottom:1px solid var(--line);vertical-align:top}
td.n{text-align:center;white-space:nowrap}
.dots{letter-spacing:1px;color:var(--accent);white-space:nowrap}
.dots i{color:var(--line);font-style:normal}
.tot{font-weight:800;font-size:14px}
.vd{display:inline-block;border-radius:999px;padding:2px 9px;font-size:11px;font-weight:700;white-space:nowrap}
.vd.core{background:var(--support);color:#fff}
.vd.test{background:var(--ground);border:1px solid var(--accent);color:var(--ink)}
.vd.skip{background:#eee;color:var(--mute)}
.why{color:var(--mute);font-size:11.5px}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px}
.card{background:var(--paper);border:2px solid var(--ink);break-inside:avoid;display:flex;flex-direction:column}
.card .top{background:var(--ground);border-bottom:2px solid var(--ink);padding:10px 14px;display:flex;justify-content:space-between;align-items:center;gap:8px}
.card .top h3{font-family:Inter,sans-serif;font-weight:800;font-size:17px}
.card .body{padding:10px 14px 12px;display:grid;gap:8px}
.card .title{font-family:var(--display);font-size:15.5px;font-style:italic;border-left:3px solid var(--accent);padding-left:8px}
.card ul{margin:0;padding-left:16px}
.card li{margin:0 0 2px}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:8px;border-top:1px solid var(--line);padding-top:8px;font-size:11.5px}
.matrix td,.matrix th{text-align:center}
.matrix td:first-child,.matrix th:first-child{text-align:left}
.cell{border-radius:6px;padding:5px 4px;font-size:10.5px;line-height:1.3;color:#fff;font-weight:600}
.cell small{display:block;font-weight:400;opacity:.92;margin-top:1px}
.cell.open{background:var(--open)}.cell.late{background:var(--late)}.cell.closed{background:var(--closed)}
.legend{display:flex;gap:14px;font-size:11.5px;margin:6px 0 0}
.legend span::before{content:"";display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px;background:var(--c)}
.cls b{display:block}
.cls span{color:var(--mute);font-size:11px;display:block;line-height:1.35}
.row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.box{border:1px solid var(--line);border-radius:10px;padding:14px;break-inside:avoid}
ul.plain{margin:4px 0 0;padding-left:18px}
ul.plain li{margin:0 0 4px}
.econ td:last-child{font-weight:700}
.foot{margin-top:30px;border-top:2px solid var(--ink);padding-top:10px;font-size:11px;color:var(--mute)}
@media (max-width:700px){.inputs,.cards,.row,.facts{grid-template-columns:1fr}.inputs>div{border-right:0;border-bottom:2px solid var(--ink)}.banner{font-size:22px}.scroll{overflow-x:auto}}
@media print{.page{padding:18px 20px}.banner,.promise{margin-left:-20px;margin-right:-20px}h2{margin-top:24px}}
</style>
</head>
<body>
<div class="page" id="app"></div>
<script type="application/json" id="plan-data">{}</script>
<script>
const D = JSON.parse(document.getElementById('plan-data').textContent);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const P = (D.brand && D.brand.palette) || {};
for (const k of ['ink','ground','accent','support']) if (P[k]) document.documentElement.style.setProperty('--' + k, P[k]);
if (D.brand && D.brand.displayFont) document.documentElement.style.setProperty('--display', D.brand.displayFont + ", Georgia, serif");
const dots = n => { n = Math.max(0, Math.min(5, Number(n) || 0)); return '<span class="dots">' + '●'.repeat(n) + '<i>' + '●'.repeat(5 - n) + '</i></span>'; };
const list = a => (a || []).map(x => '<li>' + esc(x) + '</li>').join('');
const vclass = v => ({Core:'core', Test:'test', Skip:'skip'})[v] || 'skip';
const chans = D.channels || [];
const live = chans.filter(c => c.verdict !== 'Skip');
const I = D.inputs || {};
let h = '';
h += `<div class="head"><div><div class="kicker">STR Booster playbook · Step 5</div><div class="disp">${esc(D.propertyName)}</div><div class="mute">${esc(D.location)}</div></div>
<div class="meta">Prepared for <b>${esc(D.preparedFor)}</b><br>${esc(D.date)}</div></div>`;
h += `<div class="banner">OTA Distribution Plan</div>`;
if (D.brand && D.brand.promise) h += `<div class="promise"><div class="disp">“${esc(D.brand.promise)}”</div><div class="sub">Every channel, title and night below is tested against this promise.</div></div>`;
h += `<div class="inputs">
<div><div class="lbl">Goal</div><b>${esc(I.goal)}</b><span>${esc(I.goalSource)}</span></div>
<div><div class="lbl">Ideal guest</div><b>${esc(I.guest)}</b><span>${esc(I.guestBooks)}</span></div>
<div><div class="lbl">Strategy lean</div><b>${esc(I.strategyLean)}</b><span>${esc(I.strategyWhy)}</span></div>
<div><div class="lbl">Guardrails</div><b>${esc(I.floor)}</b><span>${esc((I.rules || []).join(' · '))}</span></div></div>`;
if (D.planLine) h += `<p class="oneline">${esc(D.planLine)}</p>`;

h += `<h2>1. Where to list</h2><p class="mute">Each channel scored 1 to 5 on how well its users match the ideal guest, the brand, the strategy, the money you keep, and the effort. Core channels carry the calendar. Test channels get a 60-day trial with a clear exit rule.</p>
<div class="scroll"><table><thead><tr><th>Channel</th><th>Verdict</th><th class="n">Guest</th><th class="n">Brand</th><th class="n">Strategy</th><th class="n">Money kept</th><th class="n">Easy</th><th class="n">Total</th></tr></thead><tbody>`;
for (const c of chans) {
  const s = c.scores || {};
  const tot = ['guest','brand','strategy','economics','effort'].reduce((a, k) => a + (Number(s[k]) || 0), 0);
  h += `<tr><td><b>${esc(c.name)}</b><div class="why">${esc(c.why)}</div></td><td><span class="vd ${vclass(c.verdict)}">${esc(c.verdict)}</span></td>
<td class="n">${dots(s.guest)}</td><td class="n">${dots(s.brand)}</td><td class="n">${dots(s.strategy)}</td><td class="n">${dots(s.economics)}</td><td class="n">${dots(s.effort)}</td><td class="n tot">${tot}/25</td></tr>`;
}
h += `</tbody></table></div>`;

h += `<h2>2. How to position on each channel</h2><p class="mute">Same facts everywhere. Different first line, because each channel's users arrive with a different question.</p><div class="cards">`;
for (const c of live) {
  const p = c.positioning || {};
  h += `<div class="card"><div class="top"><h3>${esc(c.name)}</h3><span class="vd ${vclass(c.verdict)}">${esc(c.verdict)} · ${esc(c.role)}</span></div><div class="body">
<div><div class="lbl">Who is on it</div>${esc(c.userBase)}</div>
<div><div class="lbl">Position it as</div>${esc(p.angle)}</div>
<div class="title">${esc(p.title)}</div>
<div class="row"><div><div class="lbl">Lead with</div><ul>${list(p.emphasize)}</ul></div><div><div class="lbl">Leave out</div><ul>${list(p.avoid)}</ul></div></div>
<div class="facts"><div><div class="lbl">Fee (checked ${esc(c.feeChecked)})</div>${esc(c.fee)}</div><div><div class="lbl">Connection</div>${esc(c.sync)}</div></div>
${c.setup && c.setup.length ? `<div><div class="lbl">Set up</div><ul>${list(c.setup)}</ul></div>` : ''}
${c.exitRule ? `<div><div class="lbl">Keep it if</div>${esc(c.exitRule)}</div>` : ''}
</div></div>`;
}
h += `</div>`;

if (D.economics && D.economics.rows) {
  h += `<h2>3. What you keep on a ${esc(D.economics.basis)}</h2><p class="mute">${esc(D.economics.note)}</p><table class="econ"><thead><tr><th>Channel</th><th>How it is worked out</th><th>You keep</th></tr></thead><tbody>`;
  for (const r of D.economics.rows) h += `<tr><td><b>${esc(r.channel)}</b></td><td class="mute">${esc(r.math)}</td><td>${esc(r.keep)}</td></tr>`;
  h += `</tbody></table>`;
}

const classes = D.nightClasses || [];
h += `<h2>4. Which nights open where</h2><p class="mute">Nights are sorted into classes by demand. Each class opens on some channels, opens late on others, and stays closed on the rest.</p>
<div class="legend"><span style="--c:var(--open)">Open</span><span style="--c:var(--late)">Opens late, if still unsold</span><span style="--c:var(--closed)">Closed</span></div>
<div class="scroll"><table class="matrix"><thead><tr><th>Night class</th>${live.map(c => `<th>${esc(c.name)}</th>`).join('')}</tr></thead><tbody>`;
for (const k of classes) {
  h += `<tr><td class="cls"><b>${esc(k.name)}</b><span>${esc(k.definition)}</span><span>Min stay: ${esc(k.minStay)}</span></td>`;
  for (const c of live) {
    const r = (k.release || {})[c.name] || {state:'closed', note:''};
    const label = ({open:'Open', late:'Late', closed:'Closed'})[r.state] || r.state;
    h += `<td><div class="cell ${esc(r.state)}">${esc(label)}${r.note ? `<small>${esc(r.note)}</small>` : ''}</div></td>`;
  }
  h += `</tr>`;
}
h += `</tbody></table></div>`;

h += `<h2>5. High-demand nights</h2><p class="mute">The dates that make the year. Set these first, before anything else on the calendar.</p>
<table><thead><tr><th>When</th><th>Why</th><th>Class</th><th>Release plan</th></tr></thead><tbody>`;
for (const n of (D.highDemandNights || [])) h += `<tr><td><b>${esc(n.when)}</b>${n.confirm ? `<div class="why">${esc(n.confirm)}</div>` : ''}</td><td>${esc(n.event)}</td><td>${esc(n.class)}</td><td>${esc(n.plan)}</td></tr>`;
h += `</tbody></table>`;

h += `<h2>6. Rollout and rules</h2><div class="row"><div class="box"><div class="lbl">Next 90 days</div><table><tbody>`;
for (const r of (D.rollout || [])) h += `<tr><td style="white-space:nowrap"><b>${esc(r.when)}</b></td><td>${esc(r.task)}<div class="why">${esc(r.owner)}</div></td></tr>`;
h += `</tbody></table></div><div class="box"><div class="lbl">Never</div><ul class="plain">${list(D.never)}</ul><div class="lbl" style="margin-top:12px">Measure it monthly</div><ul class="plain">${list(D.measures)}</ul></div></div>`;

if ((D.research || []).length) {
  h += `<h2>7. What the research found</h2><table><thead><tr><th>Researcher</th><th>Question</th><th>Finding</th></tr></thead><tbody>`;
  for (const r of D.research) h += `<tr><td><b>${esc(r.agent)}</b></td><td>${esc(r.question)}</td><td>${esc(r.finding)}${r.sources && r.sources.length ? `<div class="why">${r.sources.map(esc).join(' · ')}</div>` : ''}</td></tr>`;
  h += `</tbody></table>`;
}
h += `<div class="foot">${esc(D.footer)}<br>Made with the free OTA Distribution skill from STR Booster · strbooster.com/skills</div>`;
document.getElementById('app').innerHTML = h;
</script>
</body>
</html>
```
