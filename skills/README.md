# STR Booster Claude Skills

Free Claude skills for short-term rental hosts and property managers, one folder per skill.
Download them ready to upload at **https://strbooster.com/skills**.

| Journey step | Skill | What it does |
|---|---|---|
| 1. The brain | [the-brain](the-brain/) | Interviews you for goals, revenue and costs, then works out NOI, value, cap rate and targets in `business-brain.md`. |
| 2. Brand building | [brand-guide](brand-guide/) | Finds the one promise only your place can make, who it is for and not for, the positioning, the voice (with banned words) and the visual direction, then writes a styled guide plus a `brand.md` the later skills read. Works for one rental, a few, or a management company. |
| 3. Know your guest | [guest-intelligence-report](guest-intelligence-report/) | Turns an Airbnb listing URL into a Guest Intelligence Report (ideal guest, journey map, upsells, market intel). |
| 5. OTA distribution | [ota-distribution](ota-distribution/) | Matches the property, brand and ideal guest to the best booking channels (including niche ones like Whimstay and Hipcamp), positions the listing for each, and decides which high-demand nights open on which channel. Sends research subagents to check fees and event dates. |
| 6. Marketing and sales | [marketing-plan](marketing-plan/) | Builds next month's marketing plan from your real reviews, photos and local events: four weeks of one past-guest email and two social posts a week, a guest circle with a welcome sequence, a five-minute enquiry reply, and an offer check before any discount. Method from *Booked Solid*. |
| 9. Guest experience | [guest-experience](guest-experience/) | Turns the brand promise and the ideal guest into a Guest Experience Storyboard: six panels, a Pre Stay / Stay / After Stay checklist, and 12 beats with the exact messages. |

Single-file kits for the other steps live in [`assets/kits/`](../assets/kits/). The site packages
those as skills too.

## Install

1. Download the skill's `.zip` from strbooster.com/skills (don't unzip it).
2. In Claude, open Settings, find Skills, and upload the `.zip`.
3. Ask for what you want. Claude picks the skill up on its own.

## Adding a skill

Add a folder here with a `SKILL.md` (front matter `name` and `description`) and any scripts or
templates it uses, then point a journey step at it in `scripts/playbook_content.py` as
`skill:<folder>`. `scripts/build-public.py` zips it to `/skills/<folder>.zip` on every deploy.
