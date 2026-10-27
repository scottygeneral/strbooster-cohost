# STR Booster — Design direction 02

This replaces the rejected serif-led draft on the existing review branch. It is an original composition using hospitality/editorial principles discussed with the owner, not a copy of Journey's proprietary layout, text, assets or code.

## What changed

- Full-bleed property photography, transparent navigation and oversized contemporary sans typography.
- Green brand ribbon and a typographic statement with an inset photographic crop.
- Distinct brand and booking-funnel spreads, with an illustrative website/email composition rather than a grid of service cards.
- A keyboard-accessible four-step guest journey and a tangible, clearly illustrative Guest Intel report.
- Four primary Get Started for Free CTAs lead to Guest Intel.
- Navy, green and cream remain the palette. No property-management replacement claims.
- Existing case metrics retain their comparison periods and qualifications; illustrative owner imagery is not presented as client proof.

## Review

The `Design review (no deployment)` Actions workflow builds the complete checkout, checks local links and assets, and renders the actual repository images at five viewport widths. It blocks analytics/chat/reviews while capturing screenshots. Results, desktop/mobile JPGs and an embedded-image HTML are uploaded as the `strbooster-design-review` artifact.

For a light preview, download `previews/open-draft.html` from this branch and open it in a browser with internet access. It reads the current public review-branch sources and strips analytics, chat and reviews. Its links deliberately open the current public site or Guest Intel, not imaginary demo screens. It is not a production deployment.

`python3 scripts/make-review.py --embed-images` creates `previews/index.html` from a full checkout. The file embeds repository images, CSS and JS; Google Fonts still requires a connection, with a system fallback. No production analytics or chat scripts are retained in the review.

## Media and scope

This version uses the existing repository images. No new film or new licensed stock collection is included. The optional hero film is enabled only when `assets/strbooster-hero-film.mp4` exists; reduced-motion, save-data and pause handling remain implemented.

Main and production are untouched. Existing Netlify branch/deploy-preview exclusions are preserved. Browser checks verify rendering and interactions, not marketing effectiveness or visual similarity. Final editorial approval of images and the future film is still needed.
