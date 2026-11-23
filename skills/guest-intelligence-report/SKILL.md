---
name: guest-intelligence-report
description: Turn an Airbnb listing URL into a Guest Intelligence Report (ideal guest avatar, travel patterns, 7-stage journey map, upsells, amenity additions, strategy, market intel) as a styled HTML/PDF.
---

# Guest Intelligence Report

Give it an Airbnb listing URL. It reads the listing, researches the local market, builds the one guest most likely to book and love this place, and produces a 6-7 page report in a fixed design: white cards, orange accent bar, peach chips, Inter font.

Use it when someone pastes an Airbnb link and asks for a guest avatar, guest persona, ideal guest, guest intelligence report, "who books this place", or "reproduce this report".

## What the report contains (always in this order)

1. **Header**: "Guest Intelligence Report" and "AI-powered analysis for: {url}".
2. **Ideal Guest Avatar card**: initials circle, name, "Your Ideal Guest Avatar", age, gender, relationship.
   - Demographic Profile: 6 tiles (Location, Occupation, Income, Education, Household, Home).
   - Core Values (4 chips). Lifestyle Priorities and Technology Adoption boxes.
   - Travel Behavior: Frequency, Duration, Lead Time, Budget, Channels, Price Sensitivity. Travel Party and Trip Purpose boxes.
   - Interests & Preferences (5-6 chips), Preferred Amenities (6-8 chips), Common Pain Points (4 bullets), Booking Behavior box.
3. **Travel Patterns**: Seasonality plus why, Primary Reason, Stay Length, Occasion Types, Research Sources, Non-Negotiables, What Triggers Booking.
4. **Guest Journey Map**: 7 stages in this order. Dreaming (Inspiration), Researching (Consideration), Booking (Decision), Pre-Arrival (Anticipation), Arrival & Stay (Experience), Departure (Transition), Post-Stay (Advocacy). Fields per stage are listed in the schema below.
5. **High-ROI Upsells**: 3 items (category, demand level, title, how to run it, est. monthly revenue).
6. **Amenity Additions**: 4 items, same format.
7. **Strategic Recommendations**: 3 columns. Marketing Message, Experience Optimization (with a Signature Moment), Channel Strategy.
8. **Market Intelligence: {City, State, Country}**: ADR, Occupancy, RevPAR stat tiles, Peak Seasons, Occupancy Drivers & Attractions (with distances), Upcoming Events (with demand impact), Competitive Landscape.
9. **Footer**: sources and the note that the avatar is a composite.

## Step 1: Read the listing

Fetch the URL with WebFetch, or with a browser tool if you have one. Strip tracking parameters (`?source_impression_id=...`) from the URL you show in the report. Capture:

- Title, property type, city, state, county, neighborhood
- Guests, bedrooms, beds (and bed types), baths, square footage
- Badges (New, Superhost, Guest favorite), rating, review count, review snippets
- Host name, time hosting, response rate and time, on-site or remote host
- The full description and the visible amenities (Airbnb only shows about 5 without JavaScript, so mine the description for the rest)
- House rules, anything restricted (no fires, stairs, shared grounds, no pets)
- Photo captions

If the page is blocked or empty, ask the user to paste the listing text (title, description, amenities, location). Do not invent a listing.

## Step 2: Research the market

Run a few web searches for the listing's town and nearest demand center:

- STR stats for the town or county: ADR, occupancy, listing count (AirDNA, Mashvisor, AirROI pages, or comparable listings)
- Top demand drivers within about 30 miles: universities, stadiums, wineries, racetracks, lakes, parks, hospitals, outlet malls. Note approximate distances.
- Recurring events with months: football seasons, graduations, races, festivals
- Seasonality: when demand peaks and why

Prefer real numbers with a source. When you estimate, write "Est." in the value and keep ranges realistic. Small rural markets often run 20-40% occupancy outside event weekends; do not default to 65-75%.

## Step 3: Pick the one ideal guest

Choose the single guest segment that best fits the listing's evidence: location plus demand drivers, layout (sleeps 2 vs 8, workspace, washer/dryer), price tier, setting, rules and constraints. Write down to yourself 3-4 pieces of listing evidence that point to this guest before writing anything. Then give that guest a believable full name, age, home city (a real feeder market within a typical drive or flight), job, income, and household.

Every claim in the avatar should trace back to something in the listing or the market. Examples: stairs → older guest objection; "no fires" → don't upsell s'mores, suggest a propane fire table; hosts on site → privacy question in Researching; 2 reviews → "lack of reviews" objection.

## Step 4: Write the report data as JSON

Fill this structure exactly. Keys are fixed; the template reads them. Keep each text value to 1-2 sentences. Use the listing's real name in the Core Message and Signature Moment.

```json
{
 "listingUrl": "clean listing URL",
 "listingTitle": "listing title",
 "avatar": {
  "name": "First Last", "photoUrl": "", "age": 34, "gender": "Female", "relationship": "Partnered",
  "demographics": {"location":"City, State","occupation":"","income":"$000,000","education":"","household":"","home":""},
  "coreValues": ["4 short values"],
  "lifestylePriorities": "", "technologyAdoption": "",
  "interests": ["5-6"], "preferredAmenities": ["6-8, tied to this listing"], "painPoints": ["4"],
  "bookingBehavior": ""
 },
 "travelBehavior": {"frequency":"","duration":"","leadTime":"","budget":"$X - $Y","channels":"","priceSensitivity":"","travelParty":"","tripPurpose":""},
 "travelPatterns": {"seasonality":"","seasonalityWhy":"","primaryReason":"","stayLength":"","occasionTypes":["3-5"],"researchSources":["2-4"],"nonNegotiables":["4"],"bookingTriggers":["4"]},
 "journey": [
  {"stage":"Dreaming","phase":"Inspiration Phase","fields":[
   {"label":"Emotional Trigger","value":"sentence"},
   {"label":"Inspiration Sources","type":"chips","value":["2"]},
   {"label":"Key Touchpoints","type":"greychips","value":["3"]}]},
  {"stage":"Researching","phase":"Consideration Phase","fields":[
   {"label":"","type":"small","value":"Research Timeline: ..."},
   {"label":"Key Questions","type":"list","value":["3"]},
   {"label":"Decision Factors","type":"chips","value":["4-5"]},
   {"label":"Common Objections","type":"list","value":["1-2"]}]},
  {"stage":"Booking","phase":"Decision Phase","fields":[
   {"label":"Final Trigger","value":""},{"label":"Preferred Method","value":""},
   {"label":"Last-Minute Doubts","type":"list","value":["1"]},
   {"label":"Expected Communication","type":"small","value":""}]},
  {"stage":"Pre-Arrival","phase":"Anticipation Phase","fields":[
   {"label":"Communication Preference","value":""},
   {"label":"Information Needed","type":"list","value":["2-3"]},
   {"label":"Anticipation Enhancers","type":"chips","value":["2"]}]},
  {"stage":"Arrival & Stay","phase":"Experience Phase","fields":[
   {"label":"First Impression Priorities","type":"chips","value":["3"]},
   {"label":"Daily Routine","type":"small","value":""},
   {"label":"Unexpected Delights","type":"list","value":["3"]},
   {"label":"Negative Review Triggers","type":"list","value":["3"]}]},
  {"stage":"Departure","phase":"Transition Phase","fields":[
   {"label":"Checkout Preferences","value":""},{"label":"Post-Stay Feelings","value":""}]},
  {"stage":"Post-Stay","phase":"Advocacy Phase","fields":[
   {"label":"Review Likelihood","value":""},{"label":"Social Media Sharing","value":""},
   {"label":"Rebook Triggers","type":"chips","value":["2-3"]},
   {"label":"Referral Triggers","type":"greychips","value":["1"]}]}
 ],
 "upsells": [{"category":"Add-on | Experience","demand":"High | Medium | Low","title":"Name: one-line pitch","detail":"how to run it and the guest price","monthlyRevenue":"$000"}],
 "amenityAdditions": [{"category":"Technology | Comfort | Outdoor | Entertainment | Nature","demand":"High | Medium | Low","title":"","detail":"why it matters for this guest","monthlyRevenue":"$000"}],
 "strategy": {
  "marketing": {"coreMessage":"","headline":"without quotes","features":["4"],"visualStyle":""},
  "experience": {"amenityAdditions":["3"],"frictionPoints":["2-3"],"signatureMoment":"a specific arrival moment, using the avatar's name"},
  "channels": {"best":["3, each 'Channel: why/how'"],"contentTypes":["3"],"partnerships":["2"]}
 },
 "market": {
  "location":"City, State, Country","adr":"","occupancy":"","revpar":"",
  "peakSeasons":["2-3"],
  "attractions":[{"name":"","distance":"Approx. X miles"}],
  "events":[{"name":"","when":"","impact":"Very high demand, premium rates"}],
  "competitiveLandscape":"3-4 sentences: who the competition is, price range, and this listing's edge and gaps"
 },
 "footer": "Market figures are estimates from public sources ({sources}, {Month Year}) and comparable listings. The guest avatar is a composite, not a real person."
}
```

`monthlyRevenue` is the estimated extra revenue per month for the host. Base it on a stated assumption in `detail` (price × likely takers per month), never a bare guess.

Journey field `type` values: omitted = normal text, `small` = smaller text, `list` = bullet list, `chips` = orange chips, `greychips` = grey chips.

## Step 5: Render

1. Save the template below as `guest-intelligence-report.html`.
2. Replace the `{}` inside `<script type="application/json" id="report-data">` with your JSON. Change nothing else. If any string contains `</`, write it as `<\/`.
3. Make the PDF if you can run code: open the HTML in headless Chromium (Playwright `page.pdf({format:'A4', printBackground:true})`, or `chrome --headless --print-to-pdf`). Otherwise deliver the HTML and tell the user to open it and use Print, then Save as PDF.
4. Look at the result (a screenshot or a PDF page) before you deliver it. Check for empty sections or raw HTML showing.
5. Name files `guest-intelligence-report-{listing-slug}.html/.pdf`.

## Rules

- Never invent listing facts, reviews, ratings or host details. If a fact is unknown, leave it out or say "not listed".
- Respect house rules in every recommendation (no fires means no fire-pit upsells).
- Label every estimated market number "Est.".
- The avatar is a fictional composite; do not use a real person's name or photo. Leave `photoUrl` empty to show initials.
- Keep sentences short and concrete. No filler like "nestled" or "unparalleled".
- Deliver the PDF (or HTML) plus a 3-line summary: who the guest is, the single biggest opportunity, and the top fix.

## Template

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guest Intelligence Report</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--accent:#f26b1d;--accent2:#f59e0b;--peach:#fde3d6;--peach-t:#e2611c;--grey:#f6f6f6;--chip:#ececec;--line:#ececec;--ink:#111;--mute:#6b6b6b;--green-bg:#d9f5e3;--green:#22a456;--amber-bg:#fde7c2;--amber:#d98a00}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);font:13px/1.45 Inter,system-ui,sans-serif}
.page{max-width:820px;margin:0 auto;padding:40px 24px}
h1{font-size:26px;font-weight:800;margin:0;letter-spacing:-.02em}
.sub{color:var(--mute);font-size:11px;margin-top:2px;word-break:break-all}
.card{border:1px solid var(--line);border-radius:10px;padding:22px 20px;margin-top:22px;break-inside:avoid-page}
.card.top{border-top:0;position:relative;margin-top:14px}
.card.top:before{content:"";position:absolute;left:-1px;right:-1px;top:-1px;height:4px;border-radius:10px 10px 0 0;background:linear-gradient(90deg,var(--accent),var(--accent2))}
.h2{display:flex;align-items:center;gap:8px;font-size:17px;font-weight:700;margin:0 0 14px}
.h3{font-size:13.5px;font-weight:700;margin:20px 0 9px}
.ico{width:16px;height:16px;stroke:var(--accent);fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
.bubble{width:28px;height:28px;border-radius:50%;background:#fff0e9;display:grid;place-items:center;flex:none}
.avatar{display:flex;gap:16px;align-items:center}
.av{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;display:grid;place-items:center;font-weight:700;font-size:24px;overflow:hidden;flex:none}
.av img{width:100%;height:100%;object-fit:cover}
.name{font-size:18px;font-weight:700}
.small{font-size:11px;color:var(--mute)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.tile{background:var(--grey);border-radius:8px;padding:10px 12px;display:flex;gap:10px}
.tile .lbl{font-size:10.5px;color:var(--mute)}
.box{border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.box .t{display:flex;gap:8px;align-items:center;font-weight:500;margin-bottom:6px}
.box p{margin:0;color:var(--mute);font-size:12px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{background:var(--chip);border-radius:999px;padding:4px 10px;font-size:11.5px}
.chip.o{background:var(--peach);color:#333}
.chip.ot{background:#fff0e9;color:var(--peach-t)}
.chip.sq{border-radius:4px}
.kv{display:flex;flex-wrap:wrap;gap:6px 22px;font-size:12px}
.kv span.k{color:var(--mute)}
ul.dots{list-style:none;padding:0;margin:0}
ul.dots li{position:relative;padding-left:12px;margin:4px 0;color:#333;font-size:12px}
ul.dots li:before{content:"";position:absolute;left:0;top:6px;width:5px;height:5px;border-radius:50%;background:var(--accent)}
ul.plain{margin:2px 0;padding-left:0;list-style:none;font-size:11.5px}
ul.plain li:before{content:"• "}
.phase{display:flex;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}
.phase:last-child{border-bottom:0}
.phase .pn{font-size:14px;font-weight:500}
.f{margin-top:8px}
.f .l{font-size:10.5px;color:var(--mute);margin-bottom:2px}
.f .v{font-size:12.5px}
.item{border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin-top:10px;display:flex;gap:14px;align-items:center}
.item .body{flex:1}
.cat{font-size:10px;letter-spacing:.06em;color:#555;text-transform:uppercase;display:flex;gap:8px;align-items:center}
.dem{font-size:10px;letter-spacing:0;text-transform:none;border-radius:999px;padding:2px 8px}
.dem.High{background:var(--green-bg);color:var(--green)}
.dem.Medium{background:var(--amber-bg);color:var(--amber)}
.dem.Low{background:var(--chip);color:#555}
.item .ti{font-weight:700;margin:4px 0 2px}
.item .de{color:var(--mute);font-size:12px}
.price{background:#fff0e9;border-radius:8px;padding:8px 12px;color:var(--peach-t);font-weight:700;white-space:nowrap}
.price small{font-weight:400;color:var(--mute);font-size:10px}
.col{border:1px solid var(--line);border-radius:10px;padding:14px}
.col .t{display:flex;gap:8px;align-items:center;font-weight:700;margin-bottom:8px}
.big{font-size:14px}
.sig{background:#fff7f2;border:1px solid var(--peach);border-radius:8px;padding:12px;margin-top:10px}
.stat{border:1px solid var(--line);border-radius:10px;padding:18px 12px;text-align:center}
.stat .v{font-size:19px;font-weight:700;line-height:1.25;margin-top:6px}
.att{border:1px solid var(--line);border-radius:8px;padding:10px 12px;display:flex;justify-content:space-between;align-items:center}
.dist{background:var(--chip);border-radius:4px;font-size:10px;padding:2px 6px;color:#555}
.ev{border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin-top:8px;display:flex;justify-content:space-between;align-items:center;gap:12px}
.ev .imp{background:var(--green-bg);color:var(--green);border-radius:999px;padding:4px 10px;font-size:11px;white-space:nowrap}
.foot{margin-top:28px;color:var(--mute);font-size:10.5px;text-align:center}
@media (max-width:640px){.grid2,.grid3{grid-template-columns:1fr}.item{flex-direction:column;align-items:flex-start}}
@media print{.page{padding:0}.card{break-inside:auto}.phase,.item,.box,.col,.stat,.ev,.tile{break-inside:avoid}@page{size:A4;margin:14mm}}
</style>
</head>
<body>
<div class="page" id="app"></div>

<!-- ===== REPORT DATA: Claude replaces this JSON object, nothing else ===== -->
<script type="application/json" id="report-data">
{}
</script>

<script>
const D = JSON.parse(document.getElementById('report-data').textContent);
const I = {
 pin:'<path d="M12 22s7-7.6 7-13a7 7 0 1 0-14 0c0 5.4 7 13 7 13z"/><circle cx="12" cy="9" r="2.5"/>',
 brief:'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
 dollar:'<path d="M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
 cap:'<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/>',
 users:'<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-6 7-6s7 2.5 7 6"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M22 20c0-3-2-5-5-5.7"/>',
 home:'<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>',
 heart:'<path d="M12 21s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 6-8 11-8 11z"/>',
 phone:'<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
 plane:'<path d="M2 16l20-8-6 14-3-6z"/><path d="M13 16l-3 3"/>',
 clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 cal:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 card:'<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
 sun:'<path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="3"/>',
 spark:'<path d="M12 3l2 6 6 2-6 2-2 6-2-6-6-2 6-2z"/>',
 search:'<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',
 door:'<path d="M14 4h5v16h-5"/><path d="M10 8l4 4-4 4M14 12H3"/>',
 star:'<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
 trend:'<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
 bulb:'<path d="M9 18h6M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V16h8v-1.3A7 7 0 0 0 12 2z"/>',
 mega:'<path d="M3 11v2a1 1 0 0 0 1 1h3l7 5V5L7 10H4a1 1 0 0 0-1 1z"/><path d="M18 9a4 4 0 0 1 0 6"/>',
 share:'<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/>'
};
const ic = (k,b) => { const s=`<svg class="ico" viewBox="0 0 24 24">${I[k]||I.spark}</svg>`; return b?`<span class="bubble">${s}</span>`:s; };
const e = s => String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const chips = (a,cls='') => `<div class="chips">${(a||[]).map(x=>`<span class="chip ${cls}">${e(x)}</span>`).join('')}</div>`;
const dots = a => `<ul class="dots">${(a||[]).map(x=>`<li>${e(x)}</li>`).join('')}</ul>`;
const plain = a => `<ul class="plain">${(a||[]).map(x=>`<li>${e(x)}</li>`).join('')}</ul>`;
const raw = (l,html) => `<div class="f"><div class="l">${e(l)}</div><div class="v">${html}</div></div>`;
const fld = (l,v,big=true) => v==null||v===''||(Array.isArray(v)&&!v.length)?'':`<div class="f"><div class="l">${e(l)}</div><div class="v">${Array.isArray(v)?v:(big?e(v):`<span class="small" style="color:#333">${e(v)}</span>`)}</div></div>`;
const A = D.avatar||{}, dm = A.demographics||{}, tb = D.travelBehavior||{}, tp = D.travelPatterns||{}, sr = D.strategy||{}, mk = D.market||{};
const initials = (A.name||'?').split(' ').map(w=>w[0]).slice(0,2).join('');
const phaseIco = ['spark','search','card','plane','home','door','star'];
const tile = (k,l,v) => `<div class="tile">${ic(k)}<div><div class="lbl">${l}</div><div>${e(v)}</div></div></div>`;
const box = (k,t,p) => `<div class="box"><div class="t">${ic(k)}${e(t)}</div><p>${e(p)}</p></div>`;
const items = a => (a||[]).map(u=>`<div class="item"><div class="body"><div class="cat">${e(u.category)}<span class="dem ${e(u.demand)}">${e(u.demand)} Demand</span></div><div class="ti">${e(u.title)}</div><div class="de">${e(u.detail)}</div></div><div class="price">$ ${e(u.monthlyRevenue)} <small>est. /month</small></div></div>`).join('');

let h = `
<h1>Guest Intelligence Report</h1>
<div class="sub">AI-powered analysis for: ${e(D.listingUrl)}</div>

<div class="card top">
 <div class="avatar"><div class="av">${A.photoUrl?`<img src="${e(A.photoUrl)}" alt="">`:e(initials)}</div>
  <div><div class="name">${e(A.name)}</div><div class="small">Your Ideal Guest Avatar</div><div style="font-size:12px;margin-top:4px">${e(A.age)} years old • ${e(A.gender)} • ${e(A.relationship)}</div></div></div>
 <div class="h3">Demographic Profile</div>
 <div class="grid2">${tile('pin','Location',dm.location)}${tile('brief','Occupation',dm.occupation)}${tile('dollar','Income',dm.income)}${tile('cap','Education',dm.education)}${tile('users','Household',dm.household)}${tile('home','Home',dm.home)}</div>
 <div class="h3">Core Values</div>${chips(A.coreValues,'o')}
 <div class="grid2" style="margin-top:12px">${box('heart','Lifestyle Priorities',A.lifestylePriorities)}${box('phone','Technology Adoption',A.technologyAdoption)}</div>
 <div class="h3">Travel Behavior</div>
 <div class="kv">
  <div>${ic('plane')} <span class="k">Frequency:</span> ${e(tb.frequency)}</div>
  <div>${ic('clock')} <span class="k">Duration:</span> ${e(tb.duration)}</div>
  <div>${ic('cal')} <span class="k">Lead Time:</span> ${e(tb.leadTime)}</div>
  <div>${ic('dollar')} <span class="k">Budget:</span> ${e(tb.budget)}</div>
  <div>${ic('card')} <span class="k">Channels:</span> ${e(tb.channels)}</div>
  <div>${ic('dollar')} <span class="k">Price Sensitivity:</span> ${e(tb.priceSensitivity)}</div>
 </div>
 <div class="grid2" style="margin-top:12px">${box('users','Travel Party',tb.travelParty)}${box('heart','Trip Purpose',tb.tripPurpose)}</div>
 <div class="h3">Interests &amp; Preferences</div>${chips(A.interests,'ot')}
 <div class="h3">Preferred Amenities</div>${chips(A.preferredAmenities)}
 <div class="h3">Common Pain Points</div>${dots(A.painPoints)}
 <div class="box" style="margin-top:14px"><div class="t" style="font-weight:700">Booking Behavior</div><p>${e(A.bookingBehavior)}</p></div>
</div>

<div class="card">
 <div class="h2">${ic('cal')}Travel Patterns</div>
 <div class="box"><div class="t">${ic('sun')}Seasonality</div><div>${e(tp.seasonality)}</div><p class="small" style="margin-top:4px">${e(tp.seasonalityWhy)}</p></div>
 <div class="grid2" style="margin-top:10px">${box('heart','Primary Reason',tp.primaryReason)}${box('clock','Stay Length',tp.stayLength)}</div>
 <div class="h3">Occasion Types</div>${chips(tp.occasionTypes,'ot sq')}
 <div class="h3">Research Sources</div>${chips(tp.researchSources,'sq')}
 <div class="h3">Non-Negotiables</div>${dots(tp.nonNegotiables)}
 <div class="h3">What Triggers Booking</div>${dots(tp.bookingTriggers)}
</div>

<div class="card">
 <div class="h2">${ic('plane')}Guest Journey Map</div>
 ${(D.journey||[]).map((p,i)=>`<div class="phase">${ic(phaseIco[i]||'spark',1)}<div style="flex:1"><div class="pn">${e(p.stage)}</div><div class="small">${e(p.phase)}</div>${(p.fields||[]).map(f=>{
   if(f.type==='chips') return raw(f.label,chips(f.value,'ot sq'));
   if(f.type==='greychips') return raw(f.label,chips(f.value,'sq'));
   if(f.type==='list') return raw(f.label,plain(f.value));
   if(f.type==='small') return fld(f.label,f.value,false);
   return fld(f.label,f.value);
 }).join('')}</div></div>`).join('')}
</div>

<div class="card"><div class="h2">${ic('trend')}High-ROI Upsells</div>${items(D.upsells)}</div>
<div class="card"><div class="h2">${ic('home')}Amenity Additions</div>${items(D.amenityAdditions)}</div>

<div class="card">
 <div class="h2">${ic('bulb')}Strategic Recommendations</div>
 <div class="grid3">
  <div class="col"><div class="t">${ic('mega',1)}Marketing Message</div>
   ${fld('Core Message',(sr.marketing||{}).coreMessage)}
   ${raw('Headline Angle',`<i>"${e((sr.marketing||{}).headline)}"</i>`)}
   <div class="f"><div class="l">Features to Emphasize</div>${dots((sr.marketing||{}).features)}</div>
   ${fld('Visual Style',(sr.marketing||{}).visualStyle,false)}</div>
  <div class="col"><div class="t">${ic('spark',1)}Experience Optimization</div>
   <div class="f"><div class="l">Amenity Additions</div>${dots((sr.experience||{}).amenityAdditions)}</div>
   <div class="f"><div class="l">Friction Points to Eliminate</div>${dots((sr.experience||{}).frictionPoints)}</div>
   <div class="sig"><div class="small">Signature Moment</div><div style="margin-top:4px">${e((sr.experience||{}).signatureMoment)}</div></div></div>
  <div class="col"><div class="t">${ic('share',1)}Channel Strategy</div>
   <div class="f"><div class="l">Best Marketing Channels</div><div class="chips" style="flex-direction:column">${((sr.channels||{}).best||[]).map((x,i)=>`<span class="chip ot" style="border-radius:12px">${i+1}. ${e(x)}</span>`).join('')}</div></div>
   <div class="f"><div class="l">Content Types</div><div class="chips" style="flex-direction:column">${((sr.channels||{}).contentTypes||[]).map(x=>`<span class="chip" style="border-radius:12px">${e(x)}</span>`).join('')}</div></div>
   <div class="f"><div class="l">Partnership Opportunities</div>${dots((sr.channels||{}).partnerships)}</div></div>
 </div>
</div>

<div class="card">
 <div class="h2">${ic('pin')}Market Intelligence: ${e(mk.location)}</div>
 <div class="grid3"><div class="stat"><div class="small">Avg. Daily Rate</div><div class="v">${e(mk.adr)}</div></div><div class="stat"><div class="small">Occupancy Rate</div><div class="v">${e(mk.occupancy)}</div></div><div class="stat"><div class="small">RevPAR</div><div class="v">${e(mk.revpar)}</div></div></div>
 <div class="h3" style="display:flex;gap:8px">${ic('cal')}Peak Seasons</div>${chips(mk.peakSeasons,'ot')}
 <div class="h3" style="display:flex;gap:8px">${ic('plane')}Occupancy Drivers &amp; Attractions</div>
 <div class="grid2">${(mk.attractions||[]).map(a=>`<div class="att"><span>${e(a.name)}</span><span class="dist">${e(a.distance)}</span></div>`).join('')}</div>
 <div class="h3" style="display:flex;gap:8px">${ic('cal')}Upcoming Events</div>
 ${(mk.events||[]).map(v=>`<div class="ev"><div><div style="font-weight:500">${e(v.name)}</div><div class="small">${e(v.when)}</div></div><span class="imp">${e(v.impact)}</span></div>`).join('')}
 <div class="box" style="margin-top:14px"><div class="t" style="font-weight:700">Competitive Landscape</div><p>${e(mk.competitiveLandscape)}</p></div>
</div>
<div class="foot">${e(D.footer||'')}</div>`;
document.getElementById('app').innerHTML = h;
document.title = 'Guest Intelligence Report' + (D.listingTitle?' · '+D.listingTitle:'');
</script>
</body>
</html>
```
