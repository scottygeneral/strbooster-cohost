# STR Booster — Revenue Growth System

Static website based on the existing green/navy STR Booster brand.

## Structure
Home, Our Approach, four service pillars with expandable modules, free community, resource guides, app overview pages, tools and partner offers, and a secondary 30-day sprint.

## Editing
Edit scripts/render-site.py, then run `python scripts/render-site.py`. Generated HTML is committed for the existing root-directory Netlify deployment. Styles and interactions live in styles.css and app.js. Existing assets, analytics identifier and legal pages are retained.

## Validation
The private build passed checks across 20 pages and 657 local links/assets. JavaScript syntax passed. Browser visual QA has not been completed.

## Before public release
- Confirm Guest Intel’s website URL. Its current CTA opens an email enquiry.
- Confirm the direct Host Growth Hub registration URL; the established hostgrowthhub.com domain is used.
- Confirm 52Rev beta integration availability. The page does not promise all integrations are live.
- Supply current partner offer details and approved case studies if desired. No discounts or performance results were invented.

This revision is for review. Public Netlify branch/PR previews are disabled in this branch; main has not been changed. The separate private Sites preview strips analytics and adds noindex.
