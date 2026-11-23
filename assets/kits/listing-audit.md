---
name: str-listing-audit
description: Audits an Airbnb or Vrbo listing against the guest it should win and returns a scored, prioritized fix list. Use when a listing is under-booking, before a relaunch, or when onboarding a new property.
---

# Listing Audit

A free Claude kit from STR Booster (strbooster.com/playbook).

**What it does:** scores your listing in eight areas and gives you a short, prioritized list of fixes, starting with the ones that cost nothing. It judges the listing through the eyes of the guest you most want, not a generic checklist.

**Built for Claude:** upload this file as a Claude Skill or add it to a Claude project. Paste your listing text and attach screenshots of the first five photos; Claude can read images.

**Time:** 15 minutes per listing.

---

## Step 1. Gather the inputs

Copy these from your listing (or the listing you are auditing):

```
LISTING
Platform: [Airbnb / Vrbo / direct site]
Title: [...]
Description (full text): [...]
Amenities list: [...]
House rules: [...]
First five photos, in order: [describe each, or attach screenshots]
Review average and count: [4.86 from 112 reviews]
Three recent reviews (paste): [...]
Current nightly price range: [optional]

TARGET GUEST
Who you most want to book: [e.g. two families travelling together for a lake week]
If unsure, write "unsure" and the audit will suggest one.
```

## Step 2. The prompt (copy as-is)

```
You are an experienced short-term rental listing reviewer. Audit the LISTING for the
TARGET GUEST. If the target guest is "unsure", first propose the most likely best guest
from the property facts and reviews, then audit for that guest.

Score each area from 1 to 5 with one sentence of evidence quoted or described from the
listing:
1. Title: would the target guest click it in search results?
2. First photo and photo order: does the first photo show the reason to book?
   Do the first five tell the story in order?
3. Opening lines of the description: do the first 2 lines answer "why here, why this home"?
4. Fit signals: does the listing say clearly who it is perfect for (and who it is not for)?
5. Amenities: are the amenities the target guest filters for listed and named clearly?
6. Objection handling: are likely worries (parking, stairs, noise, beds, Wi-Fi speed,
   kid or pet details) answered before the guest has to ask?
7. Proof: do the reviews support the promise? What do guests praise most that the
   listing does not mention?
8. Rules and tone: are the house rules clear without sounding hostile?

Then give:
- Total score out of 40.
- Top 5 fixes in priority order. For each: what to change, an example rewrite where
  relevant, cost (free / low / investment) and which score it improves.
- A rewritten title (3 options, within the platform's character limit) and a rewritten
  first paragraph.

Rules
- Base every point on what is actually in the listing. Do not assume missing facts.
- Do not recommend buying amenities unless the target guest clearly expects them;
  flag them as "investment" and keep them out of the top 3.
- Do not invent review quotes. Only quote what was pasted.
```

## Step 3. Act on it

1. Make the free fixes today: title, photo order, first paragraph, amenity names.
2. Note your current views, booking rate and nightly revenue for the next 30 days.
3. Re-run the audit after 30 days. Change one big thing at a time so you can tell what worked.

## Tip for property managers

Run this on every new owner's listing during onboarding and share the score with the owner. It sets a baseline and makes your first month of work visible.

---

Get the next kit when it drops: strbooster.com/playbook
