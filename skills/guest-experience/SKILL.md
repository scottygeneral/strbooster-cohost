---
name: guest-experience-storyboard
description: Turn a property's brand promise and its ideal guest into a Guest Experience Storyboard. Six panels (Booking to Advocacy), a Pre Stay / Stay / After Stay checklist, and 12 beats with the exact words, costs and risks, all tested against the brand promise.
---

# Guest Experience Storyboard

The guest experience step of the free STR Booster playbook. It takes two things that must already exist, **the brand** and **the ideal guest**, and storyboards every touchpoint of the stay so each one keeps the brand promise. The output is a styled HTML/PDF storyboard in the property's own colors, plus copy-ready message scripts.

Use it when someone asks for a guest experience storyboard, a guest journey, touchpoints, a welcome or check-in plan, "what should my guest messages say", or "start the guest experience step".

The person is usually a busy host or property manager with thin margins and too many apps already. Keep it fast and plain. Recommend things they can do with what they already have: their channel's or PMS's scheduled messages, a printer, a phone, and Claude.

## The order is fixed: brand, then guest, then storyboard

The experience has to prove the brand promise. So never write a storyboard without a brand promise. If there is no brand yet, build the brand core first (Step 1). Then the guest (Step 2). Only then the storyboard.

## What the storyboard contains (always in this order)

1. **Header**: guest initials, Property, Guest Category, the title banner, and the brand promise under it.
2. **Six panels**, in this order, each with two beats:
   | Panel | Beat 1 | Beat 2 |
   |---|---|---|
   | Booking | Confirmation | Personalization |
   | Arrival | Smooth check-in | Welcome token |
   | Stay | Communicate | Quality |
   | Check Out | Make it simple | Offer support |
   | Post Stay | Say thanks | Request review |
   | Advocacy | Network | Incentivize |
3. **The checklist**: three columns, Pre Stay, Stay and After Stay, each with 7 fixed items (listed in Step 4), and for each item how this property does it.
4. **Brand first, then the guest**: brand values, personality, voice and banned words next to the guest's snapshot, fears and what wins them. Then the experience in one line.
5. **Emotion curve**: how the guest feels (1 to 5) at each of the 12 beats, with four marked moments: first impression, peak, recovery and last impression.
6. **The 12 beats**: for each, the scene, before and after feelings, how it keeps the promise, the exact words, what breaks the promise, touchpoints, who does it and what it costs.
7. **Build list** (cheapest first), **Never** list, **Measure it** list, and a footer.

## Step 1: The brand (must come first)

Look for an existing brand before asking anything:
- A brand document from the Hospitality Brand Blueprint skill (a .docx or its text), a `brand.md`, or brand notes in `business-brain.md`.
- If the person has the Hospitality Brand Blueprint skill and no brand yet, offer to run it first. It takes longer but gives the full brand.

If there's nothing, build a **brand core** in about 10 minutes. Ask one question at a time:
1. "In a few words, what is this place, and where is it?" (Read the listing if they give a URL.)
2. "What's the one feeling you want guests to leave with?" (Prompt: rest, adventure, togetherness, quiet, discovery, celebration.)
3. "If this property were a person, how would they act with guests?"
4. "Who do you lose bookings to, and why do people pick you instead?"
5. "Do you have a logo or brand colors?" If they upload a logo, sample its real colors. Never invent a palette when a logo exists. Without one, pick 4 calm colors that fit the place and say they are a starting point.

Then write the brand core and confirm it with them before moving on:
- **Promise**: 6 words or fewer. It must be true of this property and false of a cheaper alternative. Test it: could the motel down the road say this? If yes, sharpen it. Good patterns: what the place removes (noise, rush, planning), or the land itself doing the work.
- **Promise meaning**: one plain sentence that turns the promise into a rule for decisions.
- **Values**: 4 single words.
- **Personality**: one sentence ("a calm neighbor who...").
- **Voice**: one or two sentences on how messages sound.
- **Banned words**: 5 to 6 words this brand never uses (always include clichés like stunning, nestled, cozy, oasis, amazing, and exclamation marks unless they truly fit).
- **Palette**: ink (darkest), ground (light background), accent, support, as hex.

Save it as `brand.md` so later steps can reuse it.

## Step 2: The ideal guest

Look for the Guest Intelligence Report first (its JSON, HTML or PDF). If they have it, take the avatar from it: name, age, home city, job, household, why they travel, pain points, what triggers a booking, and the 7-stage journey notes. Don't re-ask anything it already answers.

If there's no report, offer to run the Guest Intelligence Report skill on their listing URL, or ask four quick questions: Who books most often (and who would you love more of)? Why do they come? What worries them before booking? What makes them rave in reviews? Then write one composite guest with a believable name. Never use a real person's name or details.

One guest only. If they have two very different guests (say, families and wedding parties), make one storyboard per guest.

## Step 3: The property facts

You need facts so the scripts are true. Read the listing if you have the URL, then ask only for what's missing, in one message:
- How guests get in (keypad, lockbox, in person), parking, stairs or access issues, house rules.
- Whether the host lives on site or nearby.
- How they message guests today (Airbnb, Vrbo, a PMS, text) and whether they can schedule messages.
- What they already give guests (welcome gift, guidebook) and a rough budget per stay for the welcome token.
- Anything that often goes wrong (Wi-Fi, hot tub, parking, noise complaints).

Never invent listing facts, local businesses, distances or rules. If you don't know a real local name, write a placeholder in brackets such as `[your favorite breakfast spot]`, or describe it generically.

## Step 4: Write the storyboard

Before writing, note to yourself the promise, the guest's top 3 fears and top 3 wins. Every beat must answer one fear or deliver one win, in a way that keeps the promise.

**Rules for each beat:**
- `headline`: the short line that shows under the beat on the panel, 4 to 10 words.
- `when`: a real moment ("Within 1 hour of booking", "7 days before arrival", "Arrival day, 10 am").
- `scene`: 2 to 3 present-tense sentences from the guest's point of view, using their first name and real details of the property. Write it like a storyboard frame: what they see, hear or read.
- `feelsBefore` and `feelsAfter`: a few words each. `emotion` is the after feeling, 1 to 5.
- `promiseProof`: one or two sentences on how this beat keeps the brand promise. If you can't write it, change the beat.
- `script`: the actual words in the brand voice: the message, card or house-book text, ready to paste. Short. No banned words. Use placeholders for codes and Wi-Fi.
- `risk`: what would break the promise at this beat. This is where negative reviews come from.
- `touchpoints`, `owner` (Host, Cleaner, Scheduled message, "Claude drafts, host sends") and `cost` (`$0`, `Under $5 a stay`, `One-time, under $50`). Prefer $0 ideas. Thin margins are the norm.
- Mark exactly four beats with `moment`: `first` (usually Smooth check-in), `peak` (usually Welcome token or a stay moment), `recovery` (the beat where a likely problem gets fixed fast, usually Communicate), and `end` (usually Make it simple). Guests remember these most, so give them the most care.

**Beat guidance:**
- *Confirmation*: reply fast, use their name, and answer the biggest worry before they ask (stairs, privacy, drive time).
- *Personalization*: one question, then a short guide built from the answer, with insider tips and what to expect.
- *Smooth check-in*: entry in three steps or fewer, sent on arrival day. No calls needed.
- *Welcome token*: small, specific to the place and the guest, and cheap. Something from the land or the town beats branded swag.
- *Communicate*: one check-in at most, then a fast, plain fix for the problem most likely to happen.
- *Quality*: clean, working, labeled. The house book is one page.
- *Make it simple*: 3 checkout tasks at most. Late checkout when the calendar allows.
- *Offer support*: one helpful message after they leave (lost items, route home). No asks.
- *Say thanks*: names one thing from their stay. No review ask in the same message.
- *Request review*: once, with the honest reason. Never ask for 5 stars and never offer anything for a review (it breaks Airbnb and Vrbo rules).
- *Network*: opt-in only. A small past-guest list, two or three messages a year, and a link they can share.
- *Incentivize*: reward returning guests with access (first pick of dates, early booking) before discounts. It protects margin.

**The checklist (fixed items, write the `how` for this property):**
- Pre Stay: Confirm, reassure guests · Build excitement · Personalize stay · Clear check-in instructions · Offer local partner deals · Local insider tips · What to expect
- Stay: Smooth check-in & out · Warm welcome with gift · Tour / welcome book · Labels and instructions · Support · Clean · Functioning amenities
- After Stay: Thanks for stay · Keep in touch request · Join the network · Review request · Ask guest to promote · Offer a reward / incentive · Maintain contact

For "Offer local partner deals", recommend local places the host genuinely likes. Never suggest paid referral or affiliate deals. If an item goes against the brand (for example, a tour when the promise is privacy), say so in the `how` and give the on-brand version.

**Also write:**
- `experienceLine`: the whole stay in one sentence, from the guest's side.
- `buildList`: every item the beats need, cheapest and fastest first, with beat numbers, owner and cost. Message scripts, guides and house books are Claude's job.
- `never`: 5 to 6 things that break the promise at any point.
- `measures`: 4 to 5 simple things to track (reply time, review rate, reviews that use the promise's words, repeat bookings).

Fill this JSON. Keys are fixed and the template reads them.

```json
{
 "propertyName": "", "location": "City, ST", "guestCategory": "short label for the guest segment",
 "preparedFor": "", "date": "Month Year",
 "brand": {"promise": "6 words or fewer", "promiseMeaning": "", "values": ["4"], "personality": "", "voice": "",
  "antiVocabulary": ["5-6"], "palette": {"ink": "#", "ground": "#", "accent": "#", "support": "#"}, "displayFont": "Georgia"},
 "persona": {"name": "First Last", "snapshot": "age, job, home city, household", "why": "", "fears": ["4"], "wins": ["4"]},
 "experienceLine": "",
 "panels": [
  {"stage": "Booking", "beats": [
   {"title": "Confirmation", "headline": "", "when": "", "emotion": 4, "moment": "",
    "scene": "", "feelsBefore": "", "feelsAfter": "", "promiseProof": "",
    "scriptLabel": "Confirmation message", "script": "use \n for line breaks", "risk": "",
    "touchpoints": [""], "owner": "", "cost": ""},
   {"title": "Personalization", "...": "same fields"}]},
  {"stage": "Arrival", "beats": [{"title": "Smooth check-in"}, {"title": "Welcome token"}]},
  {"stage": "Stay", "beats": [{"title": "Communicate"}, {"title": "Quality"}]},
  {"stage": "Check Out", "beats": [{"title": "Make it simple"}, {"title": "Offer support"}]},
  {"stage": "Post Stay", "beats": [{"title": "Say thanks"}, {"title": "Request review"}]},
  {"stage": "Advocacy", "beats": [{"title": "Network"}, {"title": "Incentivize"}]}
 ],
 "checklist": {"preStay": [{"item": "Confirm, reassure guests", "how": ""}], "stay": [], "afterStay": []},
 "buildList": [{"item": "", "beat": "1, 3", "owner": "", "cost": ""}],
 "never": ["5-6"], "measures": ["4-5"],
 "footer": "Note what is sample or estimated, that the guest is a composite, and that costs are rough."
}
```

Leave `moment` empty (or omit it) on the 8 unmarked beats. Keep the 6 stages and 12 beat titles exactly as named. Panel icons follow the stage order.

## Step 5: Render

1. Save the template below as `guest-experience-storyboard.html`.
2. Replace the `{}` inside `<script type="application/json" id="storyboard-data">` with your JSON. Change nothing else. If any string contains `</`, write it as `<\/`.
3. Make the PDF if you can run code: open the HTML in headless Chromium (Playwright `page.pdf({format:'Letter', printBackground:true})`, or `chrome --headless --print-to-pdf`). Otherwise deliver the HTML and tell the person to open it and use Print, then Save as PDF.
4. Look at the result before you deliver it. Check for empty panels, raw HTML, and overlapping labels.
5. Name files `guest-experience-storyboard-{property-slug}.html/.pdf`.

## Step 6: Hand it over

Deliver the PDF (or HTML) with a 3-line summary: the promise, the peak moment, and the one fix to make first. Then offer the scripts as plain text, one per beat, ready to paste into their scheduled messages. Offer to save `brand.md` and the storyboard JSON so the next steps (listings, marketing, reviews) use the same promise and voice.

## Rules

- Brand first. No promise, no storyboard.
- Every beat names how it keeps the promise. Cut or change any beat that doesn't.
- Never invent listing facts, local businesses, reviews or rules. Use bracketed placeholders.
- No new apps or subscriptions. Use what they have plus Claude. Never recommend affiliate or paid referral deals.
- Costs are rough and cheapest first. Prefer $0 ideas.
- Never ask for 5-star reviews or tie a reward to a review.
- No banned words and no exclamation marks in scripts unless the brand voice truly calls for them.
- The guest is a fictional composite. Don't use real guest names or photos.
- Keep sentences short and concrete.

## Template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guest Experience Storyboard</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--ink:#1a1a1a;--ground:#f6f2ea;--accent:#f07c33;--support:#3d5a48;--paper:#fff;--line:#e4ddd0;--mute:#6f6a60;--display:Georgia,'Times New Roman',serif}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font:13px/1.5 Inter,system-ui,sans-serif}
.page{max-width:880px;margin:0 auto;padding:32px 24px}
h1,h2,h3,.disp{font-family:var(--display);font-weight:400;margin:0}
.kicker{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700}
.mute{color:var(--mute)}
.lbl{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);font-weight:600;margin-bottom:3px}
/* header, after concept 2 */
.head{display:grid;grid-template-columns:auto 1fr 1fr;gap:20px;align-items:center}
.av{width:62px;height:62px;border-radius:50%;background:var(--support);color:#fff;display:grid;place-items:center;font-weight:700;font-size:22px}
.fill{border-bottom:2px solid var(--ink);padding:4px 0;font-size:13px}
.fill b{font-weight:600}
.banner{background:var(--accent);color:#fff;font-weight:800;font-size:34px;letter-spacing:.02em;text-transform:uppercase;text-align:center;padding:14px 10px;margin:18px -24px 0;line-height:1.1}
.promise{background:var(--ink);color:#fff;text-align:center;padding:16px 20px;margin:0 -24px}
.promise .disp{font-size:24px;font-style:italic}
.promise .sub{font-size:12px;opacity:.75;margin-top:4px}
/* six panels, after concept 1 */
.six{display:grid;grid-template-columns:repeat(3,1fr);gap:26px 30px;margin-top:26px}
.pnl .box{border:4px solid var(--ink);aspect-ratio:1/0.82;display:grid;place-items:center;background:var(--paper)}
.pnl .box svg{width:46%;height:auto}
.pnl .st{color:var(--accent);font-weight:800;font-size:19px;text-align:center;padding:4px 0;border-bottom:2px solid var(--ink)}
.pnl .bt{text-align:center;padding:5px 2px;border-bottom:2px solid var(--ink);font-size:14px}
.pnl .bt small{display:block;color:var(--mute);font-size:11.5px;line-height:1.35;margin-top:1px}
/* three columns, after concept 2 */
.three{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;margin-top:10px}
.col h3{font-family:Inter,sans-serif;font-weight:600;font-size:19px;text-align:center;border-bottom:2px solid var(--ink);padding-bottom:4px}
.col ul{margin:12px 0 0;padding-left:16px}
.col li{margin:0 0 8px}
.col li b{font-weight:600;display:block}
.col li span{color:var(--mute);font-size:12px}
h2{font-size:24px;margin:34px 0 4px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:18px;margin:14px 0;break-inside:avoid}
.row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{background:var(--ground);border:1px solid var(--line);border-radius:999px;padding:3px 10px;font-size:11.5px}
.chip.a{background:var(--accent);border-color:var(--accent);color:#fff}
ul.plain{margin:4px 0 0;padding-left:18px}
.curve svg{width:100%;height:auto;display:block}
/* detailed frames */
.stage{margin:28px 0 10px;display:flex;align-items:center;gap:12px;border-bottom:3px solid var(--ink);padding-bottom:6px;break-after:avoid}
.stage .ic{width:38px;height:38px;border:3px solid var(--ink);display:grid;place-items:center;flex:none}
.stage .ic svg{width:26px}
.stage h3{font-family:Inter,sans-serif;font-weight:800;font-size:20px;color:var(--accent)}
.frames{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.frame{border:2px solid var(--ink);background:var(--paper);break-inside:avoid;display:flex;flex-direction:column}
.shot{background:var(--ground);border-bottom:2px solid var(--ink);padding:12px 14px;position:relative}
.shot .no{font-weight:800;color:var(--accent);font-size:12px;letter-spacing:.08em}
.shot .ttl{font-weight:700;font-size:15px}
.shot .when{font-size:10.5px;color:var(--mute);text-transform:uppercase;letter-spacing:.08em}
.shot .scene{font-family:var(--display);font-style:italic;font-size:13.5px;margin-top:7px;line-height:1.45}
.shot .emo{position:absolute;top:12px;right:14px;font-size:10px;text-align:right;color:var(--mute)}
.dots{letter-spacing:2px;color:var(--accent);font-size:11px}
.moment{display:inline-block;background:var(--accent);color:#fff;font-size:9.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;border-radius:3px;padding:1px 6px;margin-top:7px}
.notes{padding:11px 14px 13px;display:grid;gap:9px}
.feel{font-size:12px}
.feel b{font-weight:600}
.proof{border-left:3px solid var(--accent);padding:2px 0 2px 10px;font-size:12.5px}
.script{background:var(--ground);border-radius:6px;padding:9px 11px;font-size:12.5px;white-space:pre-line}
.risk{font-size:11.5px;color:#9a3b2a}
.meta{display:flex;flex-wrap:wrap;gap:6px;font-size:11px;color:var(--mute)}
.tag{border:1px solid var(--line);border-radius:4px;padding:1px 7px}
.tag.cost{border-color:var(--support);color:var(--support);font-weight:600}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{text-align:left;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);border-bottom:2px solid var(--ink);padding:6px 8px}
td{border-bottom:1px solid var(--line);padding:7px 8px;vertical-align:top}
.never li::marker{content:"✕  ";color:#9a3b2a}
.foot{font-size:11px;color:var(--mute);margin-top:26px;border-top:1px solid var(--line);padding-top:10px}
.brk{break-before:page}
@media (max-width:680px){.six,.three{grid-template-columns:1fr 1fr}.frames,.row,.head{grid-template-columns:1fr}.banner{font-size:24px}}
@media (max-width:440px){.six,.three{grid-template-columns:1fr}}
@media print{.page{padding:0 8px;max-width:none}.banner,.promise{margin-left:-8px;margin-right:-8px}}
</style>
</head>
<body>
<div class="page" id="app"></div>
<script type="application/json" id="storyboard-data">{}</script>
<script>
const D = JSON.parse(document.getElementById('storyboard-data').textContent || '{}');
const e = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const B = D.brand || {}, P = D.persona || {}, PN = D.panels || [], CL = D.checklist || {};
const pal = B.palette || {};
['ink','ground','accent','support'].forEach(k => { if (pal[k]) document.documentElement.style.setProperty('--' + k, pal[k]); });
if (B.displayFont) document.documentElement.style.setProperty('--display', B.displayFont + ', Georgia, serif');
const chips = (a, cls='') => `<div class="chips">${(a||[]).map(x => `<span class="chip ${cls}">${e(x)}</span>`).join('')}</div>`;
const list = a => `<ul class="plain">${(a||[]).map(x => `<li>${e(x)}</li>`).join('')}</ul>`;
const initials = (P.name||'?').split(' ').map(w => w[0]).slice(0,2).join('');
const first = (P.name||'the guest').split(' ')[0];
const dots = n => '●'.repeat(n||0) + '○'.repeat(5-(n||0));
const momentLabel = {first:'First impression', peak:'Peak moment', recovery:'Recovery moment', end:'Last impression'};

// Simple line icons, one per stage (fixed order: Booking, Arrival, Stay, Check Out, Post Stay, Advocacy)
const S = 'fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"';
const ICONS = [
 `<svg viewBox="0 0 100 100" ${S}><rect x="14" y="20" width="72" height="66" rx="6"/><path d="M14 38h72M32 12v16M68 12v16M35 62l11 11 21-22"/></svg>`,
 `<svg viewBox="0 0 100 100" ${S}><rect x="22" y="34" width="40" height="52" rx="5"/><path d="M34 34v-10h16v10M34 46v28M50 46v28"/><circle cx="76" cy="40" r="10"/><path d="M76 50v32M76 64h8M76 74h6"/></svg>`,
 `<svg viewBox="0 0 100 100" ${S}><path d="M10 74V30M10 58h80v16M90 58V46a8 8 0 0 0-8-8H46v20"/><circle cx="28" cy="46" r="8"/><path d="M62 14h12l-12 12h12M78 4h8l-8 8h8"/></svg>`,
 `<svg viewBox="0 0 100 100" ${S}><path d="M20 12h40v76H20zM60 30l14 0M60 88V12"/><path d="M48 50h40M78 40l10 10-10 10"/><circle cx="50" cy="52" r="2.5" fill="currentColor"/></svg>`,
 `<svg viewBox="0 0 100 100" ${S}><rect x="10" y="24" width="80" height="56" rx="6"/><path d="M10 30l40 28 40-28"/><path d="M50 18c-4-8-16-6-14 3 2 6 14 13 14 13s12-7 14-13c2-9-10-11-14-3z" fill="currentColor" stroke-width="2"/></svg>`,
 `<svg viewBox="0 0 100 100" ${S}><circle cx="50" cy="48" r="9"/><path d="M34 88c0-14 7-22 16-22s16 8 16 22"/><circle cx="24" cy="58" r="7"/><path d="M10 88c0-10 6-16 14-16"/><circle cx="76" cy="58" r="7"/><path d="M90 88c0-10-6-16-14-16"/><path d="M58 8h30v18H72l-8 7v-7h-6z"/></svg>`
];

function curve(frames){
  if (!frames.length) return '';
  const W = 820, H = 180, px = 34, py = 26;
  const x = i => px + i * (W - 2*px) / Math.max(1, frames.length - 1);
  const y = v => H - py - ((v||3) - 1) * (H - 2*py) / 4;
  const pts = frames.map((f,i) => `${x(i).toFixed(1)},${y(f.emotion).toFixed(1)}`).join(' ');
  const grid = [1,2,3,4,5].map(v => `<line x1="${px}" x2="${W-px}" y1="${y(v)}" y2="${y(v)}" stroke="var(--line)"/>`).join('');
  const marks = frames.map((f,i) => {
    const below = f.moment === 'recovery' || (i > 0 && (frames[i-1].emotion||3) > (f.emotion||3));
    const lab = f.moment ? `<text x="${x(i)}" y="${below ? y(f.emotion)+20 : y(f.emotion)-12}" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent)">${e((momentLabel[f.moment]||f.moment).toUpperCase())}</text>` : '';
    return `<circle cx="${x(i)}" cy="${y(f.emotion)}" r="${f.moment?7:4.5}" fill="${f.moment?'var(--accent)':'var(--ink)'}" stroke="#fff" stroke-width="2"/>${lab}<text x="${x(i)}" y="${H-6}" text-anchor="middle" font-size="10" fill="var(--mute)">${i+1}</text>`;
  }).join('');
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="How the guest feels at each beat, 1 to 5">${grid}
   <text x="2" y="${y(5)+4}" font-size="9" fill="var(--mute)">great</text><text x="2" y="${y(1)+4}" font-size="9" fill="var(--mute)">low</text>
   <polyline points="${pts}" fill="none" stroke="var(--support)" stroke-width="2.5" stroke-linejoin="round"/>${marks}</svg>`;
}

let n = 0;
const allBeats = PN.flatMap(p => p.beats || []);
const frame = b => `<div class="frame">
  <div class="shot"><div class="emo">feels<br><span class="dots">${dots(b.emotion)}</span></div>
   <div class="no">BEAT ${String(++n).padStart(2,'0')}</div><div class="ttl">${e(b.title)}</div><div class="when">${e(b.when)}</div>
   <div class="scene">${e(b.scene)}</div>${b.moment ? `<span class="moment">${e(momentLabel[b.moment]||b.moment)}</span>` : ''}</div>
  <div class="notes">
   <div class="feel"><b>Before:</b> ${e(b.feelsBefore)} <b>After:</b> ${e(b.feelsAfter)}</div>
   <div class="proof"><div class="lbl">How this keeps the promise</div>${e(b.promiseProof)}</div>
   ${b.script ? `<div><div class="lbl">${e(b.scriptLabel || 'The words')}</div><div class="script">${e(b.script)}</div></div>` : ''}
   ${b.risk ? `<div class="risk"><b>Breaks the promise if:</b> ${e(b.risk)}</div>` : ''}
   <div class="meta">${(b.touchpoints||[]).map(t => `<span class="tag">${e(t)}</span>`).join('')}${b.owner ? `<span class="tag">Who: ${e(b.owner)}</span>` : ''}${b.cost ? `<span class="tag cost">${e(b.cost)}</span>` : ''}</div>
  </div></div>`;

const col = (title, items) => `<div class="col"><h3>${title}</h3><ul>${(items||[]).map(i => `<li><b>${e(i.item)}</b><span>${e(i.how)}</span></li>`).join('')}</ul></div>`;

document.getElementById('app').innerHTML = `
<div class="head">
  <div class="av">${e(initials)}</div>
  <div class="mute" style="font-size:12.5px">Every touchpoint in ${e(first)}'s stay, built to keep one promise. Read the six panels for the story, the three columns for the checklist, and the beats for the exact words.</div>
  <div><div class="fill"><b>Property:</b> ${e(D.propertyName)}${D.location ? ', ' + e(D.location) : ''}</div><div class="fill" style="margin-top:8px"><b>Guest Category:</b> ${e(D.guestCategory)}</div></div>
</div>
<div class="banner">Guest Experience Storyboard</div>
<div class="promise"><div class="disp">“${e(B.promise)}”</div><div class="sub">The brand promise. ${e(B.promiseMeaning)}</div></div>

<div class="six">${PN.map((p,i) => `<div class="pnl"><div class="box" style="color:var(--ink)">${ICONS[i]||''}</div><div class="st">${e(p.stage)}</div>${(p.beats||[]).map(b => `<div class="bt">${e(b.title)}<small>${e(b.headline)}</small></div>`).join('')}</div>`).join('')}</div>

<h2>The checklist</h2>
<div class="mute">The standard touchpoints, written for this property and this guest.</div>
<div class="three">${col('Pre Stay', CL.preStay)}${col('Stay', CL.stay)}${col('After Stay', CL.afterStay)}</div>

<div class="brk"></div>
<h2>Brand first, then the guest</h2>
<div class="row">
  <div class="card"><div class="kicker">The brand</div>
    <div class="lbl" style="margin-top:10px">Values</div>${chips(B.values,'a')}
    <div class="lbl" style="margin-top:10px">Personality</div><div>${e(B.personality)}</div>
    <div class="lbl" style="margin-top:10px">Voice</div><div>${e(B.voice)}</div>
    ${B.antiVocabulary ? `<div class="lbl" style="margin-top:10px">Words we never use</div>${chips(B.antiVocabulary)}` : ''}</div>
  <div class="card"><div class="kicker">The guest</div>
    <div style="font-weight:700;font-size:15px;margin-top:10px">${e(P.name)}</div><div class="mute">${e(P.snapshot)}</div>
    <div class="lbl" style="margin-top:10px">Why they travel</div><div>${e(P.why)}</div>
    <div class="lbl" style="margin-top:10px">What they fear</div>${list(P.fears)}
    <div class="lbl" style="margin-top:10px">What wins them</div>${chips(P.wins)}</div>
</div>
<div class="card"><div class="kicker">The experience in one line</div><div class="disp" style="font-size:19px;margin-top:6px">${e(D.experienceLine)}</div></div>

<h2>How ${e(first)} feels, beat by beat</h2>
<div class="mute">Guests remember the first impression, the high point, how you handled the one thing that went wrong, and the ending. Those beats are marked.</div>
<div class="card curve">${curve(allBeats)}</div>

<h2>The storyboard, beat by beat</h2>
${PN.map((p,i) => `<div class="stage"><div class="ic">${ICONS[i]||''}</div><h3>${e(p.stage)}</h3></div><div class="frames">${(p.beats||[]).map(frame).join('')}</div>`).join('')}

<h2>Build list</h2>
<div class="mute">Everything the storyboard needs, cheapest and fastest first.</div>
<div class="card"><table><thead><tr><th>What</th><th>Beat</th><th>Who</th><th>Cost</th></tr></thead><tbody>
${(D.buildList||[]).map(b => `<tr><td>${e(b.item)}</td><td>${e(b.beat)}</td><td>${e(b.owner)}</td><td>${e(b.cost)}</td></tr>`).join('')}
</tbody></table></div>
<div class="row">
  <div class="card"><div class="kicker">Never, at any beat</div><ul class="plain never">${(D.never||[]).map(x => `<li>${e(x)}</li>`).join('')}</ul></div>
  <div class="card"><div class="kicker">Measure it</div>${list(D.measures)}</div>
</div>
<div class="foot">${e(D.footer)}</div>`;
</script>
</body>
</html>

```
