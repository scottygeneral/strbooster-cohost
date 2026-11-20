"""Long-form guide content, adapted from Booked Solid (2nd edition) by David Anthony Scott.

Each guide keeps five numbered H2 steps: seo.py reads them for HowTo structured data
(the first paragraph after each numbered H2 is the step summary). Unnumbered H2s
are supporting sections and are not treated as steps.

Worked examples use the book's illustrative woodland cottage, not client results.
"""

BOOK_URL = 'https://www.amazon.com/dp/B0FF3BR42Q'


def book_panel(chapters: str) -> str:
    return ('<div class="community-panel guide-book"><div><p class="eyebrow">Go deeper</p>'
            '<h2>From the book <em>Booked Solid</em></h2>'
            f'<p>This guide is adapted from {chapters} of <em>Booked Solid: Scaling Direct Bookings and Guest '
            'Loyalty Through Brand Story and Experience</em> by David Anthony Scott. The book includes worked '
            'examples, AI prompts and a practical workbook.</p></div><div class="actions">'
            f'<a class="btn" href="{BOOK_URL}" target="_blank" rel="noopener noreferrer">Get Booked Solid on Amazon ↗</a>'
            '</div></div>')


GUIDES = {
'guest-positioning-guide': '''
<p>One property can mean very different things to different guests. For the person organising a family celebration, it is the place that finally gets everyone under one roof. For someone planning a small retreat, the same shared rooms offer space to think without everyday interruptions. Your positioning explains why your stay is a sensible choice for a particular person on a particular occasion.</p>
<p>The aim of this guide is a one-page ideal guest profile that changes real decisions: which photo leads, what the opening paragraph says, what you explain before arrival and which quiet dates you test. If a profile changes nothing, it is only a description.</p>

<h2>1. Start with the travel need</h2>
<p>Describe why someone travels, who travels with them, and what a successful stay looks like. A purpose such as a quiet anniversary break is more useful than an age group alone.</p>
<p>"Couples", "families" and "business travellers" are starting points, not answers. Two couples booking the same town for the same weekend can want completely different things. One is celebrating an anniversary and plans to spend most of the weekend at the property; they care about privacy and a comfortable place to linger. The other is attending a wedding and needs mirrors, parking, an accurate travel time to the venue and a good night's sleep. Same party size, different reasons to choose.</p>
<p>Ask four questions about the trip:</p>
<ul><li>What is bringing someone to your area?</li><li>What are they trying to make happen?</li><li>What could make the stay difficult?</li><li>What must be true for your property to work for them?</li></ul>
<p>A useful profile connects the practical task to the emotional outcome. A family may want enough real beds and an easy meal routine because they want a holiday that feels less exhausting. The emotional benefit becomes believable when the property supports it in practical terms.</p>

<h2>2. Check the evidence</h2>
<p>Look for repeated experiences in guest reviews and recurring questions in enquiries. Separate consistent strengths from occasional perks, and record where the property is a poor fit.</p>
<p>Begin with what you already hold: booking records, reviews, enquiries and guest conversations, ideally across a full seasonal cycle. Booking records show when guests stayed, for how long, through which channel and at what price. Reviews show what guests noticed and the words they used. Enquiries expose the information people needed before deciding.</p>
<p>Keep observations separate from interpretations. "The guest asked whether the garden was enclosed" is an observation. "Dog owners are our strongest market" is an interpretation that needs more support. Read for repetition, but also for disagreement: several guests praising the beds identifies a dependable strength, while one guest delighted by a surprise anniversary gift does not create a standard inclusion to advertise.</p>
<p>A valuable guest is someone whose needs fit what you provide and whose booking supports the business you want to run. Spending is part of that, not all of it. A high nightly rate can bring high acquisition costs or a short gap that is hard to resell; a longer stay at a lower rate can perform well in a quiet period.</p>

<h2>3. Choose the strongest promise</h2>
<p>Connect a guest priority to something your property can reliably deliver. Make the promise specific and support it with accurate photos, amenities and location detail.</p>
<p>Guests rarely choose a property in isolation. They compare it with other rentals, hotels, a different destination or postponing the trip. Pick three to five realistic alternatives for your priority trip and compare the same dates and party size: total price shown, sleeping arrangements, location advantages, limitations and cancellation terms. You do not need to claim nobody else has a deck. You need the combination of your offer to be clear enough that the right guest recognises it.</p>
<p>Write three short chains of <strong>property fact → guest use → supporting proof</strong>. The cottage has a kitchen; for two adults on a restful break, that means cooking and staying in for the evening; the proof is an equipment list and accurate photos. If a chain breaks, you need better information, an operational improvement or a more modest claim.</p>
<p>Your promise must stay true on an ordinary Tuesday, in poor weather, when you are not personally present. Positioning should also help you decline investments: an amenity earns its place when it improves guest fit and has a commercial case, not because every listing nearby has one.</p>

<h2>4. Apply it across the listing</h2>
<p>Use the title and first photos to establish the experience. Expand the reasons to choose the stay in your description and answer practical concerns before they interrupt a booking.</p>
<p>Give every photo a job. The opening image should show a distinctive, usable part of the stay. The next images should establish the living space, the bedrooms and beds, the kitchen, the bathroom and access. Put important limitations, such as outdoor steps, where guests will see them during a normal scroll, not after a dozen decorative close-ups. Use captions where they remove doubt: "Private deck for cottage guests", "Access to the entrance includes outdoor steps".</p>
<p>Write the facts before the flourish. Compare these two openings for the same property:</p>
<blockquote class="quote">Weak: "Welcome to our stunning luxury escape, perfect for everyone, with every amenity you could need."</blockquote>
<blockquote class="quote">Stronger: "Settle into a two-bedroom woodland cottage with a private deck, a kitchen for evenings in, and parking at the property. It sleeps up to four. Access includes outdoor steps, and the garden is not enclosed."</blockquote>
<p>The second version gives a place, capacity, useful features, a possible experience and the limitations that matter. Clear limitations make the positive claims more credible.</p>

<h2>5. Review by season</h2>
<p>Different weeks can attract different travel needs. Revisit the guest profile when the reason to travel changes, while keeping the property facts consistent.</p>
<p>A property can keep one identity while serving different trips through the year: families during school holidays, couples' short breaks in quieter weeks. Start with the dates that actually need support. "More couples" is too broad if summer weekends already sell; "test demand for two-adult breaks on selected autumn weekdays" gives the work a commercial purpose.</p>
<p>Then test without pretending to prove too much. Write down the audience, dates, message and change, and record a baseline. Avoid changing photos, rates, minimum stays and the message all at once if you want to learn which change helped. Suitable bookings support the direction; a handful do not establish a rule.</p>

<h2>Worked example: a woodland cottage</h2>
<p><em>This cottage and its figures are illustrative.</em> A two-bedroom cottage sleeps four, has a private deck, a usable kitchen and parking. Access includes outdoor steps and the garden is not enclosed. The owner reviews 30 completed stays: 12 couples' weekend breaks, 10 family holidays, 4 wedding stays and 4 with no recorded purpose. Seven couples mention quiet or privacy and five mention the deck. Families appreciate the kitchen but ask about the stairs and the garden boundary.</p>
<p>The resulting profile: two adults on a short driving break, mainly to rest at the property. Evidence is strongest for weekends; midweek demand is unproven. The owner shows the deck and kitchen clearly while disclosing the steps, improves first-evening arrival information, and tests a quiet-break message for selected autumn weekdays before changing anything bigger.</p>

<h2>Common mistakes to avoid</h2>
<ul><li>Building the profile from demographics instead of the trip.</li><li>Treating one enthusiastic review as a market.</li><li>Promising outcomes ("you will reconnect") instead of describing conditions the property provides.</li><li>Hiding limitations on a policy page that guests never read.</li><li>Redesigning the whole property around an imagined guest before testing demand.</li></ul>
<p>Want a head start? <a href="/guest-intel.html">Guest Intel</a> creates a free first-draft guest persona. Treat it as a starting point and check it against your own reviews and enquiries.</p>
''',

'weekly-revenue-guide': '''
<p>An empty night is an outcome. It does not tell you why the night stayed empty. Perhaps too few suitable people saw the property, the offer did not fit their trip, they wanted dates you had blocked, or a minimum stay made the gap impossible to book. These look identical on a calendar and need very different responses. A discount will not repair a restriction problem, and more advertising will not make an unavailable Friday available.</p>
<p>This guide gives you a weekly routine, one focused sitting, that keeps demand, price, stay rules and promotion working from the same plan.</p>

<h2>Before you start: the numbers you will use</h2>
<ul><li><strong>Sellable nights:</strong> calendar nights minus owner use and planned maintenance. Record those separately so blocking unsold nights never flatters your occupancy.</li><li><strong>Occupancy:</strong> sold nights divided by sellable nights. Eighteen sold out of 24 sellable nights is 75%.</li><li><strong>ADR (average daily rate):</strong> lodging revenue divided by sold nights, keeping cleaning fees separate.</li><li><strong>Revenue per available night:</strong> lodging revenue divided by sellable nights. It combines rate and occupancy.</li><li><strong>Booking contribution:</strong> what a reservation leaves after its own costs: channel or payment fees, acquisition cost, turnover and variable stay costs. It is not final profit, but it is the right number for comparing opportunities.</li></ul>

<h2>1. Review the booking position</h2>
<p>Compare booked nights, lead time and pace for the weeks ahead. Separate owner-blocked nights from nights you genuinely intend to sell.</p>
<p>A booking-pace view looks at what is already on the books for future dates at the same point before arrival. Comparing next month's booked nights with last year's final total is premature; compare with what you had at the equivalent lead time, then allow for cancellations and changed conditions.</p>
<p>Inspect the calendar as a guest would. Search the trip lengths, arrival days and party sizes you hope to sell. A three-night minimum can leave an unsellable two-night gap; a restricted arrival day can block an otherwise open stay; an incorrect capacity setting can exclude a party you can host. These may be deliberate choices, but know their cost.</p>

<h2>2. Identify the reason to travel</h2>
<p>Consider the relevant guest, seasonal activities, events and booking window for each period. Verify event dates before building a campaign around them.</p>
<p>Every soft week should have a named guest and a reason they would come. An autumn weekday might suit two adults on a quiet break; a school-holiday week might suit a family organiser. Check feasibility: is there enough to do at that time of year, can guests reach the property easily, and does your minimum stay fit the trip? A persuasive message cannot fix an offer that is impractical for the dates being promoted.</p>
<p>Not every gap needs a new audience. Some are better handled through pricing, restrictions, maintenance scheduling, or accepting that opening those dates has a cost.</p>

<h2>3. Choose the commercial response</h2>
<p>Decide whether the gap calls for a pricing adjustment, a stay-rule change, clearer positioning or more relevant promotion. Account for the cost of acquiring the booking.</p>
<p>Match the response to the obstacle. Low impressions point to availability, eligibility or listing completeness. Plenty of views but few clicks point to the lead photo, title, displayed total price or the alternatives beside you. Visitors who check dates but cannot find a stay point to inventory and restrictions.</p>
<p>Then check the economics. Take an illustrative three-night stay worth $690 (lodging plus retained cleaning fee) with $130 of turnover and stay costs. Through a channel charging 15%, it contributes about $456. Booked direct from your own email list with a $30 discount, 3% payment fees and $10 of campaign cost, it contributes about $500. Booked direct through a paid ad costing $100 per booking, it contributes about $410, less than the channel booking. "Direct" is not automatically better; compare what each route leaves you.</p>
<p>A higher ADR on fewer nights is not automatically a better outcome, and neither is a full calendar at a low rate. Judge against contribution and the time the booking demands from you.</p>

<h2>4. Coordinate the message</h2>
<p>Match the offer and marketing theme to the target guest. Check that the message, availability and booking rules agree across channels.</p>
<p>The most common failure is inconsistency: a campaign promotes a two-night autumn break while the booking engine still requires three nights, or an old social post advertises dates that are no longer open. The guest sees a broken promise, whichever system caused it.</p>
<p>Before you send anything, confirm the promoted dates are open, the minimum stay matches the offer, the total price is clear, and the conditions are stated. Then lead with the trip, not the discount: "a quiet two-night break with the deck to yourselves" gives a reason to book that a percentage off does not.</p>

<h2>5. Measure what happened</h2>
<p>Review booking pickup and revenue alongside campaign activity. Treat observed changes as signals to investigate, rather than proof that one action caused the result.</p>
<p>Keep a small scorecard for one reporting period with one inventory definition: sellable and sold nights, lodging revenue, ADR, reservations, average stay length, cancellations and the channel behind each booking. For your website, add availability searches, checkout starts and completed reservations where you can track them reliably. Label every rate so someone else could reproduce it, and never compare an OTA conversion rate with a website rate as if they counted the same people.</p>
<p>Write a one-line note of what you changed each week. With small booking volumes, that change log is often more useful than a formal test, and it gives next month's comparison its context.</p>

<h2>Your weekly routine on one page</h2>
<ul><li>Pull pace for the next 4–12 weeks and compare it with the same lead time last year.</li><li>Search your own calendar for the stays you want to sell; fix any restriction that blocks them.</li><li>Name the guest and reason to travel for each soft week.</li><li>Choose one response per week: price, stay rule, positioning or promotion, and check its contribution.</li><li>Confirm the message, dates and rules match on every channel.</li><li>Record what you changed and review pickup next week.</li></ul>
<p>A useful AI prompt for the review: "Explain these booking figures in plain English. Separate what the data shows from possible explanations. Identify the three decisions I should consider, and tell me what information is missing." Always check the arithmetic against your dashboard.</p>
''',

'automation-guide': '''
<p>A solo host can now do much of the research, follow-up and analysis that once needed several specialists. AI helps you think and draft. Automation handles repeatable work. Neither can clean a room or open a jammed door, but together they can stop the repeated digital tasks that pull you away from higher-value decisions.</p>
<p>The right first automation is not the most impressive one. It is a repetitive workflow with a clear trigger and an outcome you can observe. This guide helps you choose it, build it safely and decide whether it is worth keeping.</p>

<h2>1. Map the current task</h2>
<p>Write down what starts the task, the information it needs, the steps involved and who is responsible. Identify exceptions before choosing a tool.</p>
<p>Start by finding where your time actually goes. For two ordinary weeks, log time spent on guest communication, turnovers, maintenance coordination, marketing, administration and travel, including interruptions. You are looking for patterns, not a perfect time study. The best candidates usually show up quickly: the same arrival question answered five times, every email written from scratch, the calendar checked by hand.</p>
<p>A written procedure, an SOP, is simply your way of doing a recurring task. A useful one fits on a phone screen and says what to check and what to do if something fails. If you cannot write the task down clearly, it is not ready to automate.</p>

<h2>2. Use what you already have</h2>
<p>Check your PMS, CRM and existing integrations for relevant features. Avoid adding a subscription that duplicates something your current system can do.</p>
<p>Many hosts already pay for scheduled messaging, saved replies and calendar sync they never switched on. Before buying anything, list the tools you use and what each can trigger: a confirmed booking, a changed date, a cancellation, a form submission. A CRM is simply the system that remembers your guest relationships; if yours can tag guests and send timed messages, your first workflow may need nothing new.</p>
<p>When you do need a connected sales and marketing system, choose one that covers several needs at once rather than stacking single-purpose apps.</p>

<h2>3. Define the boundaries</h2>
<p>Agree what the automation can change, when it must pause, and how it should escalate an exception. Keep human review where a mistake would materially affect a guest or booking.</p>
<p>Automation can bring a problem to your attention; it should not make promises you have not approved. An automated reply can acknowledge an urgent message and alert you, but it must not promise a refund or a repair time. If a guest replies to a sequence, pause any message that would ignore what they said.</p>
<p>Send each message for a reason the guest will recognise. Sending something at every stage because the software allows it overwhelms people. Combine related information, put access details in a controlled channel at the right time, and set response expectations you can actually meet.</p>

<h2>4. Test a complete journey</h2>
<p>Use test records to check triggers, timing, duplicate messages and failure handling. Confirm that the right person can see when a workflow fails.</p>
<p>For anything tied to a reservation, test three paths before you rely on it: a confirmed stay schedules the message; a changed arrival date moves it; a cancellation stops it. Most automation failures in rentals come from the second and third paths, where a guest receives check-in instructions for a stay that moved or no longer exists.</p>
<p>Also test what happens when something goes wrong: a missing phone number, a booking made at the last minute, a message that fails to send. Someone should be notified, not left to discover the problem from a guest.</p>

<h2>5. Review the result</h2>
<p>Compare the manual effort removed with the effort required to monitor and maintain the workflow. Keep the automation only if it improves the overall process.</p>
<p>Give your time a planning value, even though it is not a payroll expense. If a change produces $80 more contribution but takes four extra hours, that work returns $20 an hour before other considerations. Apply the same arithmetic to automation: hours saved each month, minus hours spent fixing and checking it, against what the tool costs.</p>
<p>Review after a month of real use. Look at guest questions, incidents and replies. If people still ask the question your message was meant to answer, rewrite the message or simplify the underlying process.</p>

<h2>Worked example: the pre-arrival message</h2>
<p><em>Illustrative.</em> A cottage owner answers the same questions before every stay: where to park, how the steps affect luggage, how entry works and what the kitchen provides. The owner writes one concise arrival message with what guests need while travelling, keeps a fuller guide for later reading, and schedules the message from the confirmed reservation. Entry details go through the booking channel at the intended time. The three paths (confirm, change, cancel) are tested with test bookings, and a short post-arrival note offers help without demanding a reply: "If anything in the cottage needs attention, contact us through your usual booking channel. There is no need to reply if everything is fine."</p>
<p>The result is not a robot host. It is a consistent first evening and an inbox with fewer repeat questions, so the owner's attention goes to the exceptions that need a person.</p>

<h2>Good first automations for rental owners</h2>
<ul><li>Booking confirmation with next steps.</li><li>Pre-arrival message with parking, access and first-evening information.</li><li>Post-arrival check-in that does not require a reply.</li><li>Departure reminder that is short and consistent with your terms.</li><li>Enquiry follow-up for people who asked but did not book, with their permission.</li><li>An alert to you when an urgent guest message arrives.</li></ul>
''',
}

CHAPTERS = {
    'guest-positioning-guide': 'chapters 3 to 5',
    'weekly-revenue-guide': 'chapters 1 to 3 and 8',
    'automation-guide': 'chapters 1, 6, 7 and 11',
}
