/* Local-only browser review. No requests reach production calendars, chat or analytics. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
let chromium;
try { ({ chromium } = require('playwright-core')); }
catch { ({ chromium } = require('playwright')); }

const BASE = new URL(process.env.QA_BASE_URL || 'http://127.0.0.1:8765/');
assert.ok(['127.0.0.1', 'localhost', '[::1]'].includes(BASE.hostname) && BASE.protocol === 'http:',
  'Browser checks may run only against a local HTTP server.');
const BOOKING = 'https://api.leadconnectorhq.com/widget/booking/OnBzpe1qEasSowPwkxXU';
const SECTIONS = ['benefits', 'how-it-works', 'owner-control', 'for-managers', 'lets-talk'];
const FOOTER_LINKS = [
  ['Privacy Policy', '/privacy.html'],
  ['Terms & Conditions', '/terms.html'],
  ['Instagram', 'https://www.instagram.com/strbooster/'],
  ['YouTube', 'https://www.youtube.com/@strbooster']
];
const RUN = new Date().toISOString().replace(/[:.]/g, '-');
const OUTPUT = path.resolve(process.env.QA_OUTPUT_DIR || 'previews/growth-review', RUN);
fs.mkdirSync(OUTPUT, { recursive: true });
const report = { run: RUN, base: BASE.href, bookingHandoffs: 'Intercepted locally; no live booking submission', cases: [] };
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
let browser;

async function waitForServer() {
  for (let attempt = 0; attempt < 20; attempt++) {
    try {
      const response = await fetch(BASE, { signal: AbortSignal.timeout(1500) });
      const html = await response.text();
      assert.ok(response.ok && html.includes('sb-team-hero') && html.includes('data-demo'),
        'The local URL must serve the rebuilt STR Booster AI-team page.');
      return;
    } catch (error) {
      if (error instanceof assert.AssertionError || attempt === 19) throw error;
      await delay(150);
    }
  }
}

async function prepare(options) {
  const context = await browser.newContext({
    viewport: options.viewport,
    deviceScaleFactor: 1,
    isMobile: options.viewport.width <= 700,
    hasTouch: options.viewport.width <= 768,
    javaScriptEnabled: options.javaScriptEnabled !== false,
    reducedMotion: options.reducedMotion || 'no-preference',
    serviceWorkers: 'block'
  });
  context.setDefaultTimeout(7000);
  context.setDefaultNavigationTimeout(20000);
  await context.addInitScript(() => {
    // Scrollcraft's verification contract: all pointer input stays virtual.
    Element.prototype.requestPointerLock = function () {
      return Promise.reject(new Error('Native pointer lock disabled during verification'));
    };
    Element.prototype.setPointerCapture = function () {};
    Element.prototype.releasePointerCapture = function () {};
    Document.prototype.exitPointerLock = function () {};
  });
  const diagnostics = { errors: [], localFailures: [], blockedWrites: [], externalBlocked: new Set(), handoffs: [] };
  await context.route('**/*', async route => {
    const request = route.request();
    const url = new URL(request.url());
    if (!['GET', 'HEAD'].includes(request.method())) {
      diagnostics.blockedWrites.push({ method: request.method(), target: url.origin + url.pathname });
      return route.abort();
    }
    if (url.href === BOOKING && request.isNavigationRequest()) {
      diagnostics.handoffs.push({ method: request.method(), url: url.href });
      return route.fulfill({ status: 200, contentType: 'text/html', body:
        '<!doctype html><title>Local booking-link test</title><h1>Booking handoff captured locally</h1><p>No request was sent to the scheduling service.</p>' });
    }
    if (url.origin === BASE.origin || ['fonts.googleapis.com', 'fonts.gstatic.com'].includes(url.hostname)) {
      return route.continue();
    }
    diagnostics.externalBlocked.add(url.hostname);
    return route.abort();
  });
  const page = await context.newPage();
  page.on('pageerror', error => diagnostics.errors.push(error.message));
  page.on('response', response => {
    if (response.url().startsWith(BASE.origin) && response.status() >= 400) {
      diagnostics.localFailures.push(`${response.status()} ${new URL(response.url()).pathname}`);
    }
  });
  page.on('requestfailed', request => {
    if (request.url().startsWith(BASE.origin)) {
      diagnostics.localFailures.push(`${request.failure()?.errorText} ${new URL(request.url()).pathname}`);
    }
  });
  return { context, page, diagnostics };
}

async function open(page, route = '/', javaScriptEnabled = true) {
  const response = await page.goto(new URL(route, BASE).href, { waitUntil: 'domcontentloaded' });
  assert.equal(response.status(), 200, `Local page should load: ${route}`);
  await page.locator('h1').waitFor({ state: 'visible' });
  if (javaScriptEnabled) await page.waitForFunction(() => document.documentElement.classList.contains('has-js'));
  await page.evaluate(() => Promise.race([document.fonts.ready, new Promise(resolve => setTimeout(resolve, 2500))]));
}

async function noOverflow(page, label) {
  const result = await page.evaluate(() => ({
    viewport: innerWidth,
    document: document.documentElement.scrollWidth,
    body: document.body.scrollWidth
  }));
  assert.ok(Math.max(result.document, result.body) <= result.viewport + 1,
    `${label}: horizontal overflow ${JSON.stringify(result)}`);
  return result;
}

async function readable(page, selector, { viewport = false, fontSize = 0 } = {}) {
  await page.waitForFunction(selector => {
    const element = document.querySelector(selector);
    if (!element || !element.getBoundingClientRect().height) return false;
    let opacity = 1;
    for (let node = element; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (style.display === 'none' || style.visibility !== 'visible') return false;
      opacity *= parseFloat(style.opacity);
    }
    return opacity >= .98;
  }, selector);
  const info = await page.locator(selector).evaluate(element => {
    const rect = element.getBoundingClientRect();
    const range = document.createRange();
    range.selectNodeContents(element);
    return {
      text: element.textContent.trim(), fontSize: parseFloat(getComputedStyle(element).fontSize),
      left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom,
      width: innerWidth, height: innerHeight,
      headerBottom: document.querySelector('.site-header')?.getBoundingClientRect().bottom || 0,
      linesInside: [...range.getClientRects()].filter(r => r.width && r.height)
        .every(r => r.left >= -1 && r.right <= innerWidth + 1)
    };
  });
  assert.ok(info.text && info.fontSize >= fontSize, `${selector}: missing or undersized text`);
  assert.ok(info.linesInside && info.left >= -1 && info.right <= info.width + 1,
    `${selector}: text extends past the viewport`);
  if (viewport) assert.ok(info.top >= info.headerBottom - 1 && info.bottom <= info.height + 1,
    `${selector}: text clipped or covered in its intended viewport ${JSON.stringify(info)}`);
  return info;
}

async function primaryLinks(page, home = false) {
  const links = await page.locator('a').evaluateAll(anchors => anchors
    .filter(a => /^Let[’']s talk\b/i.test(a.textContent.trim()))
    .map(a => ({ text: a.textContent.trim(), href: a.getAttribute('href') })));
  assert.ok(links.length >= (home ? 3 : 1), 'The discovery-call action must be available.');
  links.forEach(link => assert.equal(link.href, BOOKING, 'Every Let’s talk link uses the verified scheduler.'));
  assert.equal(await page.locator('[data-cta="navigation"]').getAttribute('href'), BOOKING);
  assert.equal(await page.locator('form[data-guest-strategy]').count(), 0);
  return links.length;
}

async function contrast(page) {
  // These headings and controls use flat CSS surfaces. This supplements, rather
  // than replaces, visual inspection of the saved frames and other page text.
  const samples = await page.evaluate(() => {
    const rgba = value => {
      const channels = value.match(/[\d.]+/g)?.map(Number) || [0, 0, 0, 0];
      return [channels[0], channels[1], channels[2], channels[3] ?? 1];
    };
    const over = (front, back) => front.slice(0, 3)
      .map((channel, i) => channel * front[3] + back[i] * (1 - front[3]));
    const luminance = rgb => rgb.map(channel => channel / 255)
      .map(channel => channel <= .04045 ? channel / 12.92 : ((channel + .055) / 1.055) ** 2.4)
      .reduce((value, channel, i) => value + channel * [.2126, .7152, .0722][i], 0);
    const elements = [...document.querySelectorAll('h1, h1 span'), ...document.querySelectorAll('a')]
      .filter(element => element.matches('h1, h1 span') || /^Let[’']s talk\b/i.test(element.textContent.trim()))
      .filter(element => element.getBoundingClientRect().width && element.getBoundingClientRect().height);
    return elements.map(element => {
      const chain = [];
      for (let node = element; node; node = node.parentElement) chain.unshift(node);
      let background = [255, 255, 255];
      chain.forEach(node => { background = over(rgba(getComputedStyle(node).backgroundColor), background); });
      const style = getComputedStyle(element);
      const foreground = over(rgba(style.color), background);
      const a = luminance(foreground), b = luminance(background);
      const large = parseFloat(style.fontSize) >= 24 || (parseFloat(style.fontSize) >= 18.66 && parseInt(style.fontWeight, 10) >= 700);
      return { text: element.textContent.trim(), color: style.color,
        ratio: (Math.max(a, b) + .05) / (Math.min(a, b) + .05),
        minimum: large && element.matches('h1, h1 span') ? 3 : 4.5 };
    });
  });
  for (const sample of samples) assert.ok(sample.ratio >= sample.minimum,
    `Text contrast below ${sample.minimum}:1 for “${sample.text}”: ${sample.ratio.toFixed(2)}:1 (${sample.color})`);
  return samples;
}

async function menuEscape(page) {
  const toggle = page.locator('.menu-toggle');
  if (!await toggle.isVisible()) {
    assert.ok(await page.locator('#nav-links').isVisible(), 'Desktop navigation must be available.');
    return 'desktop navigation';
  }
  assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
  await toggle.click();
  assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
  assert.ok(await page.locator('#nav-links').isVisible());
  await page.keyboard.press('Escape');
  assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
  assert.equal(await page.locator('#nav-links').isVisible(), false);
  assert.ok(await toggle.evaluate(element => document.activeElement === element), 'Escape returns focus to the menu.');
  return 'menu opens; Escape closes and restores focus';
}

async function screenshot(page, name, fullPage = false) {
  await page.screenshot({ path: path.join(OUTPUT, `${name}.png`), fullPage });
}

async function contentAndFooter(page, name, home = false) {
  assert.equal(await page.locator('#results').count(), 0, 'Client results have been removed.');
  const storyLinks = await page.locator('a[href]').evaluateAll(anchors => anchors
    .filter(anchor => /client-results|case-study-|#results/.test(anchor.getAttribute('href')))
    .map(anchor => anchor.getAttribute('href')));
  assert.deepEqual(storyLinks, [], 'No navigation or content links lead to client stories.');
  assert.doesNotMatch(await page.locator('main').innerText(), /client success stories|client stories/i);
  if (home) {
    assert.equal(await page.locator('#benefits .sb-outcome').count(), 5, 'Five concrete service examples must be present.');
    assert.deepEqual((await page.locator('#benefits .sb-service-note').allTextContents()).map(text => text.trim()),
      ['Marketing agents', 'Social media', 'Enquiries & sales', 'Guest support', 'Operations automation']);
    for (const row of await page.locator('#benefits .sb-outcome').all()) {
      await row.locator('h3').scrollIntoViewIfNeeded();
      assert.ok(await row.locator('h3').isVisible());
      assert.ok((await row.locator('p').innerText()).trim().length > 30, 'Each service has a useful example.');
    }
  }
  assert.equal(await page.locator('footer.story-footer').count(), 1);
  for (const [label, href] of FOOTER_LINKS) {
    const selector = `footer.story-footer a[href="${href}"]`;
    const link = page.locator(selector);
    assert.equal(await link.count(), 1, `Footer must include ${label}.`);
    assert.ok((await link.innerText()).includes(label));
    await link.scrollIntoViewIfNeeded();
    await readable(page, selector, { viewport: true, fontSize: 10 });
    if (href.startsWith('https:')) {
      assert.equal(await link.getAttribute('target'), '_blank');
      assert.match(await link.getAttribute('rel'), /noopener/);
      assert.match(await link.getAttribute('aria-label'), /opens in a new tab/);
    }
  }
  assert.ok(await page.locator('footer.story-footer .sb-brand').isVisible());
  await noOverflow(page, `${name} footer`);
  await screenshot(page, `${name}-footer`);
  return 'Five service examples, no client story links, and visible legal/social footer destinations verified';
}

async function heroMotion(page, name, pinned) {
  const hero = page.locator('.sb-team-hero');
  assert.equal(await hero.getAttribute('data-sc-act'), pinned ? 'pin' : 'flow');
  assert.equal(await hero.getAttribute('data-sc-span'), '1.75');
  assert.equal(await page.locator('#how-it-works').getAttribute('data-sc-act'), 'flow');
  assert.equal(await page.locator('.sc-act--pinned').count(), pinned ? 1 : 0,
    'The hero is the only pinned section.');
  assert.equal(await page.locator('.sb-system-art').getAttribute('role'), 'img');
  assert.match(await page.locator('.sb-system-art').getAttribute('aria-label'), /marketing.*social media.*guest support.*operations/i);
  if (!pinned) {
    assert.equal(await hero.evaluate(element => element.classList.contains('has-hero-motion')), false);
    const offset = await page.locator('.sb-network-lines').evaluate(element => parseFloat(getComputedStyle(element).strokeDashoffset));
    assert.ok(Math.abs(offset) < .01, 'The static hero shows fully connected services.');
    return 'Natural flow with the complete connected service diagram';
  }
  const frames = [];
  const pixels = [];
  for (const [index, progress] of [0, .43, .9].entries()) {
    await page.evaluate(progress => {
      const section = document.querySelector('.sb-team-hero');
      const top = section.getBoundingClientRect().top + scrollY;
      window.scrollTo({ top: top + (section.offsetHeight - innerHeight) * progress, behavior: 'instant' });
    }, progress);
    await page.waitForFunction(progress => {
      const actual = parseFloat(getComputedStyle(document.querySelector('.sb-team-hero')).getPropertyValue('--sc-p'));
      return Math.abs(actual - progress) < .035;
    }, progress);
    await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    await readable(page, 'h1', { viewport: true, fontSize: 30 });
    await readable(page, '[data-cta="hero"]', { viewport: true, fontSize: 12 });
    await noOverflow(page, `${name} hero progress ${progress}`);
    frames.push(await hero.evaluate(element => ({
      progress: parseFloat(getComputedStyle(element).getPropertyValue('--sc-p')),
      transforms: [...element.querySelectorAll('[data-hero-layer]')].map(layer => getComputedStyle(layer).transform),
      connectorOffset: parseFloat(getComputedStyle(element.querySelector('.sb-network-lines')).strokeDashoffset)
    })));
    await screenshot(page, `${name}-hero-scroll-${index + 1}`);
    pixels.push(await page.locator('.sb-system-art').screenshot({ path: path.join(OUTPUT, `${name}-hero-art-${index + 1}.png`) }));
  }
  for (let i = 1; i < frames.length; i++) {
    const changed = frames[i].transforms.filter((transform, j) => transform !== frames[i - 1].transforms[j]).length;
    assert.ok(changed >= 3, 'Scroll must move independent hero layers.');
    assert.ok(frames[i].connectorOffset < frames[i - 1].connectorOffset, 'Connections visibly draw as the team assembles.');
    assert.equal(pixels[i].equals(pixels[i - 1]), false, 'Hero diagram screenshots must change with real scroll.');
  }
  assert.ok(frames.at(-1).connectorOffset < .02, 'The hero resolves into the connected team.');
  return frames;
}

async function conversations(page, name) {
  const cases = [
    { id: 'booking', question: /family weekend/i, answer: /family-friendly/i, next: /direct booking link/i, exception: /early.*Friday/i },
    { id: 'social', question: /couples.*autumn escape/i, answer: /post and caption/i, next: /publishing plan/i, exception: /last-minute discount/i },
    { id: 'operations', question: /guests arrive tomorrow/i, answer: /arrival information/i, next: /task needs attention/i, exception: /maintenance issue/i }
  ];
  assert.equal(await page.locator('[data-demo]').getAttribute('data-stage'), '2', 'The full example is visible before interaction.');
  assert.equal(await page.locator('[data-message][aria-hidden="false"]').count(), 3);
  let previous = '';
  for (const example of cases) {
    await page.locator(`button[data-scenario="${example.id}"]`).click();
    assert.equal(await page.locator('[data-demo]').getAttribute('data-scenario'), example.id);
    assert.equal(await page.locator(`button[data-scenario="${example.id}"]`).getAttribute('aria-pressed'), 'true');
    assert.equal(await page.locator('[data-demo]').getAttribute('data-stage'), '2');
    const texts = await page.locator('[data-message-text]').allTextContents();
    assert.match(texts[0], example.question);
    assert.match(texts[1], example.answer);
    assert.match(texts[2], example.next);
    assert.notEqual(texts.join(' '), previous, 'Scenario changes must update real messages.');
    previous = texts.join(' ');
    assert.ok(await page.locator('button[data-stage="1"]').isVisible(), 'The second workflow step is available.');
    await page.locator('[data-message="2"]').scrollIntoViewIfNeeded();
    await readable(page, '[data-message="2"] p', { viewport: true, fontSize: 11 });
    await page.locator('#approval-toggle').check();
    assert.equal(await page.locator('[data-demo]').getAttribute('data-approval'), 'true');
    const approvalTexts = await page.locator('[data-message-text]').allTextContents();
    assert.match(approvalTexts[0], example.exception);
    assert.notEqual(approvalTexts[1], texts[1], 'Approval changes the answer, not just its badge.');
    assert.notEqual(approvalTexts[2], texts[2], 'Approval changes the next step.');
    assert.equal((await page.locator('[data-next-label]').textContent()).trim(), 'Your decision');
    assert.ok(await page.locator('[data-message="2"]').isVisible());
    if (example.id === 'operations') await screenshot(page, `${name}-operations-approval`);
    await page.locator('#approval-toggle').uncheck();
    assert.deepEqual(await page.locator('[data-message-text]').allTextContents(), texts,
      'Turning approval off restores the routine example.');
  }
  await page.locator('button[data-scenario="booking"]').click();
  await page.locator('button[data-stage="1"]').click();
  assert.equal(await page.locator('[data-demo]').getAttribute('data-stage'), '1');
  assert.ok(await page.locator('[data-message="1"]').isVisible());
  assert.equal(await page.locator('[data-message="2"]').isVisible(), false);
  await page.locator('button[data-stage="2"]').focus();
  await page.keyboard.press('Enter');
  assert.ok(await page.locator('[data-message="2"]').isVisible());
  assert.ok((await page.locator('[data-demo-announcement]').textContent()).trim(), 'Keyboard interaction announces the updated workflow.');
}

async function faq(page) {
  const detail = page.locator('.sb-questions details').first();
  const summary = detail.locator('summary');
  await summary.click();
  assert.ok(await detail.evaluate(element => element.open));
  assert.ok(await detail.locator('p').isVisible());
  await summary.focus();
  await page.keyboard.press('Enter');
  assert.equal(await detail.evaluate(element => element.open), false, 'Native summary keyboard behavior must work.');
}

async function reachableSections(page) {
  for (const id of SECTIONS) {
    const selector = `#${id} h2`;
    await page.locator(selector).scrollIntoViewIfNeeded();
    await readable(page, selector, { viewport: true, fontSize: 24 });
    await noOverflow(page, id);
  }
  await page.locator('[data-cta="final"]').scrollIntoViewIfNeeded();
  await readable(page, '[data-cta="final"]', { viewport: true, fontSize: 12 });
}

async function handoff(page, diagnostics, javaScriptEnabled = true) {
  const events = [];
  if (javaScriptEnabled) {
    await page.exposeFunction('recordBookingEventForTest', (...args) => events.push(args));
    await page.evaluate(() => {
      window.gtag = (...args) => window.recordBookingEventForTest(...args);
    });
  }
  await page.locator('[data-cta="final"]').click();
  await page.waitForURL(BOOKING);
  assert.deepEqual(diagnostics.handoffs, [{ method: 'GET', url: BOOKING }]);
  assert.equal(await page.title(), 'Local booking-link test');
  if (javaScriptEnabled) {
    assert.equal(events.length, 1, 'The discovery call click records one analytics event.');
    assert.equal(events[0][0], 'event');
    assert.equal(events[0][1], 'booking_click');
    assert.equal(events[0][2].button_location, 'final');
    assert.equal(events[0][2].send_to, 'G-YQ9L9GHV31');
    assert.deepEqual(Object.keys(events[0][2]).sort(), ['button_location', 'page_path', 'send_to', 'transport_type']);
  }
}

async function runCase(name, options, test) {
  const { context, page, diagnostics } = await prepare(options);
  const entry = { name, ...options, status: 'pending' };
  try {
    await open(page, options.route || '/', options.javaScriptEnabled !== false);
    assert.equal(await page.locator('h1').count(), 1);
    entry.heading = await readable(page, 'h1', { viewport: true, fontSize: 30 });
    entry.layout = await noOverflow(page, name);
    entry.contrast = await contrast(page);
    entry.fonts = await page.evaluate(() => [...document.fonts].map(face => ({ family: face.family, status: face.status })));
    await test(page, entry, diagnostics);
    assert.deepEqual(diagnostics.errors, [], 'No uncaught browser errors.');
    assert.deepEqual(diagnostics.localFailures, [], 'No failed local assets.');
    assert.deepEqual(diagnostics.blockedWrites, [], 'The tested flow must not attempt a write.');
    entry.status = 'passed';
    console.log(`PASS ${name}`);
  } catch (error) {
    entry.status = 'failed';
    entry.error = error.stack || String(error);
    await screenshot(page, `${name}-failure`).catch(() => {});
    console.error(`FAIL ${name}: ${error.message}`);
  } finally {
    entry.diagnostics = { ...diagnostics, externalBlocked: [...diagnostics.externalBlocked] };
    report.cases.push(entry);
    fs.writeFileSync(path.join(OUTPUT, 'report.json'), JSON.stringify(report, null, 2));
    await context.close();
  }
}

async function main() {
  await waitForServer();
  browser = await chromium.launch({ headless: true,
    ...(process.env.BROWSER_PATH ? { executablePath: process.env.BROWSER_PATH } : {}),
    args: ['--disable-dev-shm-usage'] });
  for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 },
    { width: 360, height: 640 }, { width: 768, height: 900 }, { width: 1024, height: 768 }]) {
    const name = `home-${viewport.width}x${viewport.height}`;
    await runCase(name, { viewport }, async (page, entry, diagnostics) => {
      entry.primaryLinks = await primaryLinks(page, true);
      await screenshot(page, `${name}-hero`);
      entry.navigation = await menuEscape(page);
      const pinned = viewport.width >= 1024 && viewport.height >= 780;
      entry.heroMotion = await heroMotion(page, name, pinned);
      await conversations(page, name);
      await faq(page);
      await reachableSections(page);
      await screenshot(page, `${name}-closing`);
      if ([390, 1440].includes(viewport.width)) await screenshot(page, `${name}-full-page`, true);
      entry.content = await contentAndFooter(page, name, true);
      entry.workflow = 'Three scenarios, keyboard stage controls and approval routing verified; the workflow remains in normal flow';
      await handoff(page, diagnostics);
    });
  }
  for (const viewport of [{ width: 1440, height: 900 }, { width: 360, height: 640 }]) {
    const name = `reduced-${viewport.width}`;
    await runCase(name, { viewport, reducedMotion: 'reduce' }, async (page, entry) => {
      entry.primaryLinks = await primaryLinks(page, true);
      entry.heroMotion = await heroMotion(page, name, false);
      await screenshot(page, `${name}-hero`);
      assert.equal(await page.locator('[data-demo]').getAttribute('data-stage'), '2');
      assert.ok(await page.locator('[data-message="2"]').isVisible());
      assert.equal(await page.evaluate(() => document.getAnimations().filter(animation => animation.playState === 'running').length), 0);
      await reachableSections(page);
      await screenshot(page, `${name}-closing`);
      entry.content = await contentAndFooter(page, name, true);
      entry.reachability = 'Every section and final call link reachable without pinning or running animations';
    });
  }
  await runCase('no-js-390', { viewport: { width: 390, height: 844 }, javaScriptEnabled: false }, async (page, entry, diagnostics) => {
    entry.primaryLinks = await primaryLinks(page, true);
    assert.ok(await page.locator('#nav-links').isVisible(), 'Navigation remains available without JavaScript.');
    entry.heroMotion = await heroMotion(page, 'no-js-390', false);
    assert.equal(await page.locator('[data-message]').count(), 3);
    assert.ok(await page.locator('[data-message="2"]').isVisible(), 'The full example is in the HTML.');
    await faq(page);
    await reachableSections(page);
    await screenshot(page, 'no-js-390-full-page', true);
    entry.content = await contentAndFooter(page, 'no-js-390', true);
    await handoff(page, diagnostics, false);
    entry.fallback = 'Complete reading flow, native FAQ and direct booking link work without JavaScript';
  });
  for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
    await runCase(`shared-shell-${viewport.width}`, { viewport, route: '/guest-positioning-guide.html' }, async (page, entry) => {
      entry.pages = [];
      for (const route of ['/guest-positioning-guide.html', '/growth-services.html', '/our-approach.html', '/get-expert-help.html']) {
        if (new URL(page.url()).pathname !== route) await open(page, route);
        assert.equal(await page.locator('h1').count(), 1);
        await readable(page, 'h1', { viewport: true, fontSize: 30 });
        await noOverflow(page, route);
        await primaryLinks(page);
        await contrast(page);
        assert.equal(await page.locator('link[href="/growth.css"]').count(), 1);
        assert.equal(await page.locator('script[src="/growth.js"]').count(), 1);
        assert.equal(await page.locator('link[href="/story.css"], script[src="/story.js"], script[src="/guest-strategy.js"]').count(), 0);
        await menuEscape(page);
        await screenshot(page, `shared-${viewport.width}-${path.basename(route, '.html')}`);
        await contentAndFooter(page, `shared-${viewport.width}-${path.basename(route, '.html')}`);
        entry.pages.push(route);
      }
    });
  }
  const failed = report.cases.filter(entry => entry.status === 'failed').length;
  report.status = failed ? 'failed' : 'passed';
  fs.writeFileSync(path.join(OUTPUT, 'report.json'), JSON.stringify(report, null, 2));
  console.log(`GROWTH_REVIEW ${report.cases.length - failed}/${report.cases.length} passed; ${OUTPUT}`);
  if (failed) process.exitCode = 1;
}

main().catch(error => {
  report.status = 'failed';
  report.error = error.stack || String(error);
  fs.writeFileSync(path.join(OUTPUT, 'report.json'), JSON.stringify(report, null, 2));
  console.error(error.message);
  process.exitCode = 1;
}).finally(async () => { if (browser) await browser.close(); });
