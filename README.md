# STR Booster — Brand + Booking Funnel

STR Booster builds vacation rental brands and booking funnels to attract more direct bookings and bring guests back. Marketing is the specialty; this is not a property-management or PMS replacement.

## Design

A hospitality-led, editorial homepage inspired by the storytelling direction discussed using Journey as a reference. All copy and layout are original to this rebuild; no Journey imagery, logos or footage are included. Retains STR Booster navy (#0d1f2d), green (#1a7f64), cream (#f5f3ee), Fraunces and Outfit, and existing repository imagery.

Homepage story: the opportunity → understand the guest → build the brand → build the booking funnel → documented client work → founder → scope/FAQ → free Guest Intel report.

The primary CTA is **Get Started for Free** and links to https://guest-intel.strbooster.com/. The illustrative guest-profile card is explicitly labelled as an example, not an actual report or client result. Case-study metrics retain their existing periods and qualifications. HighLevel is described as the supporting software, with affiliate disclosure in the FAQ.

## Build and preview

Python 3; no third-party Python dependencies.

```sh
python3 scripts/render-site.py
python3 scripts/check-story.py
python3 -m http.server 8000
```

Open http://localhost:8000 after running the build. The existing Netlify root-directory deployment now runs the renderer and regression checks before publishing. Existing redirects and the disabled branch/PR-preview settings are preserved. This pull request does not deploy or merge itself.

## Editing

- `templates/home.html`: canonical homepage, including the shared header/footer.
- `index.html`: committed homepage output; regenerate it rather than editing it separately.
- `story.css`: homepage design and namespaced shared navigation/footer styling.
- `story.js`: progressively enhanced, keyboard-accessible booking-journey tabs; optional hero-film controls; lazy review widget.
- `scripts/render-site.py`: build entry point. Runs the existing page generator, renders the new homepage, and applies the shared navigation/footer and free-report CTA to generated inner pages.
- `scripts/render-pages.py`: the previous production generator, retained verbatim for existing service/resource/case-study content.
- `scripts/seo.py`, `scripts/case_studies.py`, `styles.css`, `app.js`: existing inner-page metadata/content, styles, analytics and chat integration retained.

`python3 scripts/render-site.py --existing-only` refreshes the new design around already generated files without running the original generator. Always use the full build before deployment so all inner-page navigation is current.

## Hero film

No film asset is included. The existing property image is the real default, not a broken video request. Add an approved, licensed, optimized landscape loop at `assets/strbooster-hero-film.mp4` and rebuild to enable the video. The renderer only inserts a video if that file exists. Playback is muted, inline and pausable; reduced-motion/data-saving preferences and page visibility are respected. Failed playback leaves the image visible. No new film was generated or licensed as part of this code update.

## Validation and remaining review

- Python syntax and homepage content/CTA/schema checks passed locally.
- Offline Chromium layout tests passed at 320, 375, 390, 768, 1024 and 1440px with no horizontal overflow.
- Mobile menu/Escape, funnel clicks and arrow/Home/End keyboard control, FAQ disclosure, no-JavaScript content fallback and reduced-motion behavior passed with no page JavaScript errors.
- Renderer fixture tests passed for shared-shell replacement, preserving page content/metadata, idempotence and video-present/video-absent output.
- Local browser tests used neutral image fixtures and blocked external services because original image bytes, remote fonts and integrations were unavailable in that environment. They do NOT constitute final imagery/font review or end-to-end testing of Guest Intel, analytics, chat or reviews.
- The original full renderer and Netlify deployment have not been executed in the local test environment. Review a complete-checkout build and actual asset rendering before merging. Inner-page body content is preserved, not fully redesigned.

No new testimonials, client counts, time-savings or performance guarantees have been added.
