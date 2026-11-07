# STR Booster — Custom AI Growth Systems

STR Booster builds AI agents and automation for short-term rental marketing, social media, booking enquiries, guest support and operations. A separate owner-acquisition pathway serves property managers and co-hosts. The offer combines implementation with ongoing support and owner control.

The primary site-wide CTA is **Let’s talk**, linking to the verified provider-hosted page for the existing 30-minute discovery calendar:
https://api.leadconnectorhq.com/widget/booking/OnBzpe1qEasSowPwkxXU

## Design and content

The homepage is a single dark, motion-led page: **AI growth systems for short-term rentals.** "Custom AI for your marketing, bookings and guest service. Built for your business, with support that keeps you in control." Every call to action is **Let’s talk** (the discovery calendar above). The brief and feeling curve are in `scrollcraft/builds/disruptor/BRIEF.md`.

Sections: hero (Higgsfield-generated rental render with a muted, script-started loop video and floating service chips), a scroll-reactive service marquee, the premise (manifesto that lights up word by word over a tangle-to-signal render), the growth stack (four systems, each with an animated HTML/CSS interface illustration from `partials/systems-ui.html`), how it works, a light guest-focus section with illustrative lifestyle photography, the founder, and a full-screen “Let’s talk.” close.

There are no client logos, testimonials or results figures. Interface illustrations are labelled as illustrations, and generated photography is marked as illustrative. Reduced-motion visitors get every section in its final state with no video, marquee or scroll effects; the page is readable without JavaScript.

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
