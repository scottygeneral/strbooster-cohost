---
name: the-brain
description: Build the business brain for a short-term rental business. Interview the host for goals, revenue and costs, work out NOI per property and for the portfolio, value each property with its contents (FF&E), work out cap rates, and set calibrated targets in business-brain.md.
---

# The Brain: Objectives And Strategies

Step 1 of the free STR Booster playbook. It turns a host's or property manager's scattered numbers into one file, `business-brain.md`, that every later step reads. That file holds the goals, each property's revenue and costs, NOI, value, cap rate, break-even point and the targets for the next 12 months.

Use it when someone asks to build their business brain, set goals or targets for their rentals, work out NOI or cap rate, see what each property really makes, or "start step 1".

The person is usually busy and has no system yet. Keep it fast, plain and friendly. They should be done in about 45 minutes, even if they only have rough numbers.

## Ground rules

- **One question at a time.** Group small related items into one question, such as "What do you pay a year for property tax, insurance and HOA?". Never send a wall of questions.
- **Plain words.** Say "nightly rate", not "ADR", the first time, and define NOI and cap rate in one line when they first come up.
- **Never invent a number.** If they don't know a number, offer three choices: look it up now, estimate it together, or skip it. Every estimate is labeled "Est." in the data and in the file, with its source.
- **Rough is fine.** A ballpark today beats a perfect number never. Round to the nearest $100.
- **Accept whatever they have.** If they paste or upload a P&L, owner statement, payout CSV, PMS report or tax Schedule E, read the numbers from it and only ask about what is missing. Confirm what you read in a short table before using it.
- **NOI leaves out** mortgage payments, depreciation, income tax and big one-off improvements (a new roof or a full refurnish). If they list those as costs, set them aside and say why in one line. Mortgage payments go in `annual_debt_service` so the file can show cash flow after debt.
- **Privacy.** Don't send addresses or owner names to any outside service except to look up a value estimate the person asked for.

## Step 1: Goals (5 minutes)

Ask what they want the next 12 months to look like, in their own words. Then pin down one or two numbers:

1. "What would make the next 12 months a win?" Prompt with examples: more revenue, a profit number, higher occupancy, more owners or properties, time back each week, a better rating.
2. Turn the answer into a portfolio NOI goal, a cap rate goal, or both. If they give a revenue goal, keep it as a statement and work out NOI once you have their costs. If they give a "take-home" goal, treat it as NOI goal plus their mortgage payments.
3. Ask for any rule they never break, such as "never under $150 a night" or "no parties". Keep these as goal statements.

Save these under `goals.statements`, `goals.portfolio_noi` and `goals.portfolio_cap_rate`.

## Step 2: The properties (2 minutes each)

For each property, ask in one message: name, town, type, bedrooms, sleeps, and whether they manage it themselves or pay a manager. For a property manager with many units, offer to start with their 3 to 5 biggest earners and add the rest later.

## Step 3: Revenue per property (5 minutes each)

Use the last 12 months. If they've owned it less than a year, use what they have and say the numbers are annualized.

Ask for:
- Nights booked and nights available (365 minus owner stays and blocked nights).
- Number of stays, or the average stay length.
- Rent: what guests paid for the nights, before platform fees. If they only know payouts, ask for the platform fee rate and work back to gross.
- Cleaning fees collected.
- Other income: pet fees, early check-in, upsells, damage fees kept.
- If they have it, revenue by month for last year. It shapes the monthly targets.

From this you get occupancy, nightly rate and RevPAR (revenue per available night). Say these back in one line so they can sanity-check.

## Step 4: Costs per property (10 minutes each)

Walk through costs in three groups. Show the list for each group so they can answer in one go, and put 0 for anything that doesn't apply.

**A. Costs that move with revenue (a % of revenue)**
- Management fee (often 15% to 30% of revenue)
- Platform fees (Airbnb, Vrbo, Booking.com: 3% to about 16% depending on the fee setting; check a payout report)
- Payment processing for direct bookings (about 3%)
- Occupancy taxes only if the host pays them out of their own pocket. If the platform collects and remits them, leave them out of both revenue and costs.

**B. Costs per stay**
- Cleaning per turnover, laundry and linens, consumables (coffee, toiletries, paper goods), and any per-stay guest gift.

**C. Fixed costs (per year)**
- Property tax, insurance, HOA
- Electric, water, gas, internet, trash
- Software: PMS, pricing tool, smart locks, noise monitors
- Landscaping, snow removal, pool or hot tub service, pest control
- Repairs and maintenance (not big improvements)
- STR license or permit, and anything else that repeats

Then set a **replacement reserve**, money set aside for furniture, linens and appliances that wear out. Default 3% of revenue. Ask if they want 2% (newer furnishings) or 5% (older or high-wear).

If they manage it themselves, the file also shows NOI as if they paid a manager (default 20%). That's the number a buyer, lender or owner would use, and it shows how much of the profit is really their own labor.

## Step 5: Value and cap rate (5 minutes each)

Cap rate is NOI divided by what the property is worth. It tells them how hard the asset is working.

Ask: "Roughly what is the property worth today, and what are the furniture, fixtures and equipment (FF&E) worth: furniture, decor, linens, kitchen, hot tub, games, outdoor furniture?"

If they don't know, offer to estimate, and label every estimate "Est." with its source:
- **Property value.** Search the web for public estimates: Zillow, Redfin or Realtor.com for the address, the county assessor's market value (assessed value is often a fraction of market value, so check how the county assesses), or 2 or 3 recent sales of similar homes nearby. Use the average of what you find and name the sources. If nothing comes back, use purchase price plus major improvements and say so.
- **FF&E.** Ask for receipts or the original furnishing budget first. Otherwise estimate by bedroom: about $5,000 to $8,000 per bedroom for a basic setup, $10,000 to $15,000 for well-furnished, and $20,000 or more for luxury, plus big items like a hot tub or game room. Then discount for age: about 10% a year, down to no less than 30% of the original cost.

Show the result in one line per property, for example: "$520,000 (Est.) + $45,000 FF&E (Est.) = $565,000, so the cap rate is 3.5%."

Optional: ask for the yearly mortgage payments if they want cash flow after debt.

## Step 6: The market (optional, 3 minutes each)

Targets need a ceiling. Ask if they know their market's average occupancy and nightly rate for similar homes (from AirDNA, PriceLabs, Rabbu, Key Data or their PMS). If not, offer to estimate from a web search or a quick look at 5 to 10 comparable listings, labeled "Est.". Small and rural markets often run 30% to 50% occupancy outside peak weeks, so don't assume 70%. Skip this if they want speed. The targets then use default caps.

## Step 7: Calculate

Write the answers to `brain-data.json` using the schema in `brain-data-template.json`. Percentages are decimals (20% = 0.20). Money is annual dollars.

If you can run code, run the bundled calculator:

```bash
python brain_calc.py brain-data.json --md business-brain.md --json brain-results.json
```

It is standard-library Python and does all the maths, so you never do arithmetic by hand when it is available. If you can't run code, do the same maths step by step, and show your working in a collapsed table at the end:

- **Total revenue** = rent + cleaning fees + other income
- **Occupancy** = booked nights ÷ available nights. **Nightly rate** = rent ÷ booked nights. **RevPAR** = rent ÷ available nights
- **Operating costs** = (sum of % costs + reserve %) × total revenue + per-stay costs × stays + fixed costs
- **NOI** = total revenue − operating costs. **NOI margin** = NOI ÷ total revenue
- **Cap rate** = NOI ÷ (property value + FF&E)
- **Break-even nights** = fixed costs ÷ (revenue per booked night × (1 − % costs) − per-stay costs ÷ average stay)
- **Portfolio** = the sum of each property's revenue, costs, NOI and value. Portfolio cap rate = total NOI ÷ total value. Never average the property cap rates.

## Step 8: Build and calibrate the targets

The calculator builds four levels for every property:

| Level | What it means |
|---|---|
| **Floor** | Break-even occupancy at today's nightly rate. Below this the property loses money. It becomes the price and occupancy guardrail for step 7. |
| **Today** | The last 12 months. |
| **Target (12 months)** | Realistic: up to +5 occupancy points and +5% nightly rate, capped near the market (market occupancy + 5 points, market rate + 5%, never above 85% occupancy). |
| **Stretch** | Up to +10 points, +10% rate and 3% lower fixed and per-stay costs, capped at market + 10 points and market rate + 15%. |

Then it checks the goal both ways:
- **Top-down:** it splits the portfolio NOI goal across properties by their share of the Target NOI, then works out the occupancy each property needs at today's rate, and the nightly rate it needs at target occupancy.
- **Bottom-up:** it compares the goal with the Target and Stretch totals and says whether the goal is within the target, between target and stretch, or beyond stretch.

Calibrate with the person before saving:
1. Show the portfolio table and the goal check.
2. If the goal is beyond stretch, say so plainly and offer three fixes: a longer timeline, a cost project, or a lower goal. Never quietly inflate the targets to fit the goal.
3. If they know something the defaults don't, such as a renovation, a new listing, a market slump or a planned rate rise, change that property's `levers` and re-run.
4. Rewrite section 4, "Strategies", from the calculator's first draft into 3 to 5 concrete moves. Each move names the property, the lever (rate, occupancy, a cost line), the expected NOI impact in dollars, and the playbook step that delivers it: 4 Listings, 5 OTA Distribution, 6 Marketing, 7 Revenue Management, 8 Win More Homes, 9 Guest Experience.

Typical cost ranges the calculator uses to flag lines are rough rules of thumb, not facts about any market. Present them as "worth a look", never as errors.

## Step 9: Save and hand off

1. Add a short **Business** section at the top of `business-brain.md` if the person wants it (2 minutes): who their guests are in one line, their voice in three words, and their non-negotiable rules. Later steps fill in more detail.
2. Show a short summary in chat: portfolio NOI, cap rate, the goal check, and the top 3 strategies. Then give them the file.
3. Tell them: "Create a Claude project called 'Business brain' and add business-brain.md and brain-data.json to it. Every later step starts there. Re-run this each quarter with fresh numbers."

## Files in this kit

- `SKILL.md`: these instructions.
- `brain_calc.py`: the calculator (NOI, cap rate, break-even, targets, goal check, flags, business-brain.md writer).
- `brain-data-template.json`: the blank data schema.
- `sample-brain-data.json`, `sample-business-brain.md`: a full run on a made-up 2-property portfolio.

## What good looks like

- Every number traces back to something the person said, a document they shared, or an estimate labeled "Est." with its source.
- The portfolio cap rate is total NOI ÷ total value, never an average.
- Self-managed properties show NOI with a paid manager as well.
- The targets are reachable, or the file says plainly that the goal isn't, and why.
- The file reads in five minutes and a later step can find any number in it.
