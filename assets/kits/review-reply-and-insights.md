---
name: str-review-reply-and-insights
description: Drafts public replies to guest reviews in the host's voice and turns a batch of reviews into a list of listing, marketing and operations improvements. Use after new reviews arrive, or monthly for a portfolio review.
---

# Review Reply + Insight Miner

A free Claude kit from STR Booster (strbooster.com/playbook).

**What it does:** two jobs in one kit.

1. **Reply:** drafts a short, human public reply to each review, including the difficult ones.
2. **Mine:** reads 20 to 100 reviews at once and tells you what guests love (use it in your listing), what keeps coming up (fix it), and who your happiest guests are (market to more of them).

**Built for Claude:** upload this file as a Claude Skill or add it to a Claude project. Paste reviews, or upload an export from your PMS.

**Time:** 2 minutes per reply; 15 minutes for a monthly insight review.

---

## Part 1. Reply to reviews

### Your voice settings

```
Host name to sign with: [David]
Tone: [warm, brief, specific; never defensive]
Things I never say: [no "we're sorry you feel that way", no promises of refunds in public]
Property name: [Lakeview Cabin]
```

### The prompt (copy as-is)

```
Write a public reply to the guest review below, for future guests to read as much as
for this guest.

- 40 to 80 words. Sign with the host name.
- Thank the guest by first name and mention one specific detail from their review.
- If the review contains a complaint: acknowledge it in one sentence without arguing,
  state briefly what has been done or will be done (only if I told you; otherwise
  write "[what we fixed]" for me to fill in), and invite them back only if it fits.
- Never reveal private details about the guest, the booking, money or refunds.
- Never sound defensive or blame the guest, even if the review is unfair. If the review
  breaks platform rules (e.g. mentions something that did not happen, or threats),
  add a note to me: "Consider reporting to the platform: [reason]".
- Include one natural mention of what future guests will enjoy, without sounding
  like an advert.

Review:
[paste review]
```

## Part 2. Mine your reviews for insight

### The prompt (copy as-is)

```
Below are [number] guest reviews for [property or portfolio]. Analyse them and return:

1. Top 5 things guests love, with how many reviews mention each and one short quote
   each (quote exactly; do not paraphrase as a quote).
2. Recurring issues: anything mentioned 2+ times, ranked by frequency, with a suggested
   fix and whether it is a listing fix (set expectations), an operations fix
   (cleaning, maintenance, check-in) or an investment.
3. Who your happiest guests are: patterns in trip purpose, group type and season among
   the 5-star reviews, if the reviews reveal them.
4. Listing gaps: things guests praise that the listing does not mention (if I paste the
   listing below), and expectations the listing creates that reviews contradict.
5. Three lines of marketing copy built only from what guests actually said.

Do not invent quotes, counts or guest details. If a pattern is weak, say so.

Reviews:
[paste reviews]

Listing (optional):
[paste listing description]
```

### Put the insight to work

- Move the #1 thing guests love into your title or first photo.
- Fix the #1 recurring issue this month, or set expectations for it in the listing.
- Use the "happiest guests" pattern to decide who to target in your next promotion.

## For property managers

Run Part 2 across each owner's reviews every quarter and include the top three findings in your owner update. Owners rarely see their reviews analysed. It shows you are paying attention.

---

Get the next kit when it drops: strbooster.com/playbook
