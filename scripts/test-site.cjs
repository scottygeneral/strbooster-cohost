/* Pull-request browser check for every page in scripts/pages.json.
 * Runs only against a local server. External requests (calendar, chat,
 * analytics, reviews) are blocked, so nothing reaches live services.
 * Saves desktop and phone screenshots of each page for visual review. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const BASE = new URL(process.env.QA_BASE_URL || 'http://127.0.0.1:8765/');
assert.ok(['127.0.0.1', 'localhost'].includes(BASE.hostname) && BASE.protocol === 'http:',
  'Browser checks may run only against a local HTTP server.');
const BOOKING = 'https://api.leadconnectorhq.com/widget/booking/OnBzpe1qEasSowPwkxXU';
const PAGES = JSON.parse(fs.readFileSync(path.join(__dirname, 'pages.json'), 'utf8'));
const OUTPUT = path.resolve(process.env.QA_OUTPUT_DIR || 'previews/site-check');
const VIEWPORTS = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'phone', width: 390, height: 844 }
];
const ALLOWED_HOSTS = new Set(['fonts.googleapis.com', 'fonts.gstatic.com']);

async function checkPage(browser, file, viewport) {
  const route = file === 'index.html' ? '/' : '/' + file;
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    deviceScaleFactor: 1,
    isMobile: viewport.width <= 700,
    hasTouch: viewport.width <= 768,
    serviceWorkers: 'block'
  });
  const problems = [];
  await context.route('**/*', async r => {
    const url = new URL(r.request().url());
    if (url.origin === BASE.origin || ALLOWED_HOSTS.has(url.hostname)) return r.continue();
    return r.abort();
  });
  const page = await context.newPage();
  page.on('pageerror', e => problems.push(`JavaScript error: ${e.message}`));
  page.on('response', res => {
    if (res.url().startsWith(BASE.origin) && res.status() >= 400) {
      problems.push(`Missing file: ${res.status()} ${new URL(res.url()).pathname}`);
    }
  });
  try {
    const res = await page.goto(new URL(route, BASE).href, { waitUntil: 'load', timeout: 20000 });
    if (!res || res.status() !== 200) problems.push(`Page did not load (status ${res && res.status()})`);
    await page.waitForTimeout(400);

    const facts = await page.evaluate(() => {
      const h1 = document.querySelector('h1');
      const box = h1 && h1.getBoundingClientRect();
      return {
        title: document.title.trim(),
        h1: h1 ? h1.textContent.trim() : '',
        h1Shown: !!box && box.width > 0 && box.height > 0,
        overflow: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - innerWidth,
        talkLinks: [...document.querySelectorAll('a')]
          .filter(a => /^Let[’']s talk\b/i.test(a.textContent.trim()))
          .map(a => a.getAttribute('href'))
      };
    });
    if (!facts.title) problems.push('Page has no <title>');
    if (!facts.h1 || !facts.h1Shown) problems.push('Main heading (h1) is missing or hidden');
    if (facts.overflow > 1) problems.push(`Page scrolls sideways by ${facts.overflow}px`);
    if (!facts.talkLinks.length) problems.push('No "Let\'s talk" booking link');
    facts.talkLinks.filter(h => h !== BOOKING)
      .forEach(h => problems.push(`"Let's talk" link points somewhere else: ${h}`));

    const shot = path.join(OUTPUT, viewport.name, file.replace(/\.html$/, '') + '.png');
    fs.mkdirSync(path.dirname(shot), { recursive: true });
    await page.screenshot({ path: shot, fullPage: true });
  } catch (error) {
    problems.push(`Check crashed: ${error.message.split('\n')[0]}`);
  } finally {
    await context.close();
  }
  return problems;
}

(async () => {
  fs.mkdirSync(OUTPUT, { recursive: true });
  const browser = await chromium.launch();
  const report = [];
  let failures = 0;
  for (const file of PAGES) {
    for (const viewport of VIEWPORTS) {
      const problems = await checkPage(browser, file, viewport);
      report.push({ page: file, viewport: viewport.name, problems });
      failures += problems.length;
      console.log(`${problems.length ? 'FAIL' : 'PASS'} ${file} (${viewport.name})`);
      problems.forEach(p => console.log(`     - ${p}`));
    }
  }
  await browser.close();
  fs.writeFileSync(path.join(OUTPUT, 'report.json'), JSON.stringify(report, null, 2));
  console.log(failures ? `\n${failures} problem(s) found.` : `\nAll ${report.length} page checks passed.`);
  process.exit(failures ? 1 : 0);
})();
