# STR Booster — Custom AI Growth Systems

STR Booster builds custom AI systems for short-term rental marketing, direct bookings, sales follow-up, guest concierge and property-manager owner acquisition. The offer combines implementation with ongoing support and owner control.

The primary site-wide CTA is **Let’s talk**, linking to the verified provider-hosted page for the existing 30-minute discovery calendar:
https://api.leadconnectorhq.com/widget/booking/OnBzpe1qEasSowPwkxXU

## Design and content

The homepage leads with **More bookings. Less busywork.** It uses the existing navy and green brand colours, Outfit typography, clear outcome sections and original HTML/SVG product illustrations. No lifestyle photography, generated people, fake software screens or invented performance metrics are used on the new homepage.

A labelled illustrative workflow explains guest booking, guest questions and owner enquiries. Visitors can choose a scenario, explore its three steps and try an exception that needs owner approval. It does not submit messages, make bookings or run an AI agent. Existing client results retain their dates and qualifications; they are not presented as measured results from the illustrative AI system.

The requested [Scrollcraft skill](https://github.com/nateherkai/scroll-craft) guides the motion. Its MIT-licensed engine is vendored unchanged. The site adds restrained hero depth, section entrances, an existing-result count and one short pinned workflow on suitable desktop viewports. Phones, short viewports and reduced-motion visitors receive a natural-flow explanation. Content and calendar links remain available without JavaScript.

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

- `templates/home.html`: homepage and shared navigation/footer.
- `templates/services.html`, `templates/approach.html`, `templates/discovery.html`: main-content fragments for the three core inner pages.
- `growth.css`, `growth.js`: new design, responsive layout and progressively enhanced workflow.
- `vendor/scrollcraft/`: unchanged third-party engine, license and source attribution.
- `scripts/render-site.py`: build entry point, source overrides and shared discovery-call CTAs.
- `scripts/render-pages.py`: retained generator for existing service, resource and case-study content.
- `scripts/check-story.py`: content, schema, local targets, analytics and CTA checks.
- `scripts/test-growth.cjs`: browser checks and screenshots for responsive layouts, interactions, reduced motion and no JavaScript.
- `scripts/verify-scroll.mjs`: the Scrollcraft screenshot harness adapted for isolated test traffic and this page’s reduced-motion fallback.
- `scrollcraft/builds/ai-growth/BRIEF.md`: design rationale and motion plan.

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

Existing analytics IDs, the GHL chat integration, case-study content and the separate 52Rev waitlist remain in place. Guest Intel remains available as a resource; it is no longer the primary acquisition CTA.
