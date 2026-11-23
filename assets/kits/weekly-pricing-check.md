---
name: str-weekly-pricing-check
description: Runs a 20-minute weekly pricing and pacing review for a short-term rental from the host's own calendar and pricing-tool data, and returns a short action list. Use once a week, or when a period is booking slower or faster than expected.
---

# Weekly Pricing Check

A free starter kit from STR Booster (strbooster.com/playbook).

**What it does:** gives you a calm, repeatable weekly review of the next 90 days. It looks at what is booked, what is not, and how far out you are, then tells you which dates need attention and what kind of action to consider: price, stay rules, or promotion.

**What it does not do:** set your prices. Your dynamic pricing tool (PriceLabs, Wheelhouse, Beyond or your PMS) does the price maths. This kit helps you decide where to look and what to try, and it never invents a market rate.

**Works with:** Claude, ChatGPT or Gemini. Upload a CSV or paste a simple table.

**Time:** 20 minutes a week.

---

## Step 1. Export your next 90 days

From your pricing tool or PMS, export (or type) one row per night:

```
date, booked (yes/no), your price, min stay, [optional: market occupancy %, market price]
```

Also note:

```
CONTEXT
Property: [3-bed cabin, sleeps 8]
Typical booking lead time: [e.g. most bookings 3 to 6 weeks out]
Known events in the next 90 days: [festival on the 14th, school holiday from ...]
Last year same period (if known): [busy / quiet / no data]
Your floor price: [the lowest you will ever accept]
```

## Step 2. The prompt (copy as-is)

```
You are a short-term rental revenue analyst doing a weekly review. Use the data and
CONTEXT provided. Do not invent market data, competitor prices or occupancy figures.
If something is missing, say what would help and continue with what you have.

1. Pace snapshot: for each of the next 13 weeks, show nights booked out of 7 and flag
   each week as Ahead, On track or Behind, given the typical lead time.
   (A week inside the typical lead time with few bookings is Behind. A week far out
   with few bookings is usually fine.)
2. Gaps: list orphan nights (1 to 2 open nights between bookings) and whether the
   minimum stay is blocking them.
3. Watch list: the 3 to 5 date ranges that most need attention this week, with why.
4. For each watch-list item, suggest ONE type of action and why:
   - price: "test a lower or higher price in your pricing tool" (never give a number
     below the floor price; do not give a specific price unless market data is provided)
   - stay rules: shorten or lengthen minimum stay, allow gap nights
   - promotion: who to promote these dates to (past guests, a specific guest type)
   - leave it: if it is too early to act
5. Opportunities: any dates booking unusually fast that may be underpriced.
6. Summary in 3 bullets I can act on in 10 minutes.

Keep it short. Use a table for the pace snapshot.
```

## Step 3. Act and log

Keep a simple log so you learn what works for your property:

| Week of | Dates | What I changed | Result 2 weeks later |
|---|---|---|---|
| | | | |

One change per date range. Give it a week or two before judging it.

## Rules worth keeping

- **Do not drop prices on autopilot.** A slow week often needs a stay-rule change or promotion before a discount.
- **Respect lead time.** Panic-discounting dates that are still months away trains guests to wait.
- **Protect your floor.** Every booking has a cleaning and wear cost.

---

STR Booster's 52Rev app (beta) connects this weekly review to your pricing tool and marketing. Get the next kit when it drops: strbooster.com/playbook
