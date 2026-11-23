# STR Booster — Growth Systems for STR Property Managers

STR Booster builds and runs growth systems for independent short-term rental property managers with 10 to 100 doors. Two outcomes: more direct revenue (Direct Revenue System) and more owner contracts (Owner Acquisition System), tied together by revenue management in the Growth Partner plan. The free Growth Audit is the main lead magnet; Guest Intel and 52Rev are free tools, not services. Plans, starting prices and guarantees live on `/growth-services.html#pricing` and the homepage `#pricing` section.

The primary site-wide CTA is **Let’s talk**, linking to the verified provider-hosted page for the existing 30-minute discovery calendar:
https://api.leadconnectorhq.com/widget/booking/OnBzpe1qEasSowPwkxXU

## Design and content

The homepage is a single dark, motion-led page: **More direct bookings. More owners.** for managers with 10 to 100 doors. Every primary call to action is **Let’s talk** (the discovery calendar above). The brief and feeling curve are in `scrollcraft/builds/disruptor/BRIEF.md`.

Sections: hero, a scroll-reactive marquee, the premise (OTA fees and owner churn), the growth stack (two systems, each with an animated HTML/CSS interface illustration from `partials/systems-ui.html`, then Growth Partner and the concierge add-on), plans and starting prices, how it works with a fit list, a light guest-focus section, the founder, and a full-screen “Let’s talk.” close. The owner acquisition page is `templates/owner-acquisition.html` (main content swapped into the `owner-acquisition` shell from `render-pages.py`).

There are no client logos or results figures on the page itself. Client reviews come from the GHL Reputation widget, opened from a small floating “Client reviews” badge (`reviews.js`) near the top-right of every page; the widget loads only when a visitor opens it. Interface illustrations are labelled as illustrations, and generated photography is marked as illustrative. Reduced-motion visitors get every section in its final state with no video, marquee or scroll effects; the page is readable without JavaScript.

## Build and preview

Python 3; no third-party Python build dependencies.

```sh
python3 scripts/render-site.py
python3 scripts/check-story.py
python3 -m http.server 8765
```

Open http://127.0.0.1:8765 after building. Netlify runs the renderer and content checks before publishing the repository root. Existing redirects, functions and deployment settings are retained.

`python3 scripts/render-site.py --existing-only` reapplies the shared shell to already generated HTML. Use the full build before deployment.

## Source files

- `templates/home.html`: homepage and shared navigation/footer. `home.css` and `home.js` style and animate the homepage only (scoped to `body.dx-home`).
- `partials/systems-ui.html`, `systems-ui.css`: the four animated system illustrations, inserted by `render-site.py` at `<!--include:systems-ui#key-->` markers.
- `assets/dx-*`: homepage imagery and the hero loop (generated with Higgsfield).
- `templates/services.html`, `templates/approach.html`, `templates/discovery.html`: main-content fragments for the three core inner pages.
- `growth.css`, `growth.js`: new design, responsive layout and progressively enhanced workflow.
- `reviews.js`: floating client-reviews badge and panel (GHL Reputation widget, lazy-loaded). Styles live at the end of `growth.css`.
- `scripts/playbook_content.py`, `playbook.js`, `assets/kits/*.md`: the free STR AI Playbook page (`/playbook`), its five downloadable kits and the email signup. The form posts to `netlify/functions/brief-signup.js`, which upserts the contact in the STR Booster HighLevel sub-account and adds the tags `str-booster-brief`, `free-playbook` and a `role-*` tag. It needs the Netlify environment variable `GHL_PRIVATE_TOKEN` (a HighLevel Private Integration token with `contacts.write`); without it the form shows an error and nothing is stored.
- `scripts/guides_content.py`: long-form guide content adapted from *Booked Solid*.
- `vendor/scrollcraft/`: unchanged third-party engine, license and source attribution.
- `scripts/render-site.py`: build entry point, source overrides and shared discovery-call CTAs.
- `scripts/render-pages.py`: retained generator for existing service, resource and case-study content.
- `scripts/check-story.py`: content, schema, local targets, analytics and CTA checks.
- `scripts/test-growth.cjs`: browser checks and screenshots for responsive layouts, interactions, reduced motion and no JavaScript.
- `scripts/verify-scroll.mjs`: the Scrollcraft screenshot harness adapted for isolated test traffic and this page’s reduced-motion fallback.
- `scrollcraft/builds/ai-team/BRIEF.md`: current design rationale, hero layer contract and motion plan. The original brief remains as history.

Generated root HTML is committed for static hosting; edit the templates and rebuild rather than changing the outputs independently. The former story/form assets remain in repository history and files, but are not loaded by the new core pages.

## Browser review

The **Design Review** workflow builds the complete checkout, checks syntax/content and runs Chromium against a local HTTP server. It captures desktop, tablet, phone, compact-phone, reduced-motion and no-JavaScript evidence. Third-party analytics/chat requests are blocked during automated tests. Booking-link navigation is intercepted with a clearly labelled fixture, so tests cannot create appointments or contacts.

The workflow uploads screenshots and JSON reports for review. These tests establish local layout and interaction behaviour; they do not assert that a third-party calendar, chat service or analytics account is available to every visitor. The existing calendar configuration is separate from this website.

For local browser checks after installing Playwright and Chromium:

```sh
QA_BASE_URL=http://127.0.0.1:8765 node scripts/test-growth.cjs
node scripts/verify-scroll.mjs --url http://127.0.0.1:8765 --width 1440 --height 900 --out qa/scroll-desktop
```

A partial source checkout may use `python3 scripts/check-story.py --content-only` to identify missing legacy media separately. Production CI uses the full check; this flag never skips homepage assets or local code/link targets.

Existing analytics IDs, the GHL chat integration and the separate 52Rev waitlist remain in place. The shared footer includes Privacy Policy, Terms & Conditions, Instagram and YouTube. Retired client-story URLs redirect to the services page and are excluded from the sitemap. Guest Intel remains available as a resource; it is no longer the primary acquisition CTA.
