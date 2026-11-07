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
const BOOKING = 'https://links.strbooster.com/widget/booking/OnBzpe1qEasSowPwkxXU';
const SECTIONS = ['benefits', 'how-it-works', 'owner-control', 'results', 'for-managers', 'lets-talk'];
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
      assert.ok(response.ok && /Custom AI Growth Systems/.test(html) && html.includes('data-demo'),
        'Port 8765 must serve the rebuilt STR Booster page, not a different or stale site.');
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

async function scrollStage(page, progress, stage) {
  await page.evaluate(progress => {
    const section = document.querySelector('#how-it-works');
    const top = section.getBoundingClientRect().top + scrollY;
    window.scrollTo({ top: top + (section.offsetHeight - innerHeight) * progress, behavior: 'instant' });
  }, progress);
  await page.waitForFunction(({ progress, stage }) => {
    const section = document.querySelector('#how-it-works');
    const actual = parseFloat(getComputedStyle(section).getPropertyValue('--sc-p'));
    return Math.abs(actual - progress) < .035 && document.querySelector('[data-demo]').dataset.stage === String(stage);
  }, { progress, stage });
  const visible = await page.locator('[data-message]').evaluateAll(messages => messages
    .filter(message => getComputedStyle(message).display !== 'none' && message.getAttribute('aria-hidden') !== 'true').length);
  assert.equal(visible, stage + 1, 'Scrolling must reveal actual conversation messages.');
  await readable(page, `[data-message="${stage}"] p`, { viewport: true, fontSize: 11 });
}

async function conversations(page, name, pinned) {
  const cases = [
    { id: 'booking', question: /family weekend/i, answer: /family-friendly/i, next: /booking engine/i, exception: /early.*Friday/i },
    { id: 'concierge', question: /park.*arrive/i, answer: /parking and arrival/i, next: /instructions/i, exception: /extra guest/i },
    { id: 'owner', question: /manage.*holiday home/i, answer: /property.*location.*goals/i, next: /discovery call/i, exception: /guarantee/i }
  ];
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
    if (!pinned) await page.locator('[data-message="2"]').scrollIntoViewIfNeeded();
    await readable(page, '[data-message="2"] p', { viewport: true, fontSize: 11 });
    await page.locator('#approval-toggle').check();
    assert.equal(await page.locator('[data-demo]').getAttribute('data-approval'), 'true');
    const approvalTexts = await page.locator('[data-message-text]').allTextContents();
    assert.match(approvalTexts[0], example.exception);
    assert.notEqual(approvalTexts[1], texts[1], 'Approval changes the answer, not just its badge.');
    assert.notEqual(approvalTexts[2], texts[2], 'Approval changes the next step.');
    assert.equal((await page.locator('[data-next-label]').textContent()).trim(), 'Your decision');
    assert.ok(await page.locator('[data-message="2"]').isVisible());
    if (example.id === 'owner') await screenshot(page, `${name}-owner-approval`);
    await page.locator('#approval-toggle').uncheck();
    assert.deepEqual(await page.locator('[data-message-text]').allTextContents(), texts,
      'Turning approval off restores the routine example.');
  }
  await page.locator('button[data-scenario="booking"]').click();
  await page.locator('button[data-stage="1"]').click();
  assert.equal(await page.locator('[data-demo]').getAttribute('data-stage'), '1');
  assert.ok(await page.locator('[data-message="1"]').isVisible());
  assert.equal(await page.locator('[data-message="2"]').isVisible(), false);
  await page.locator('button[data-stage="2"]').click();
  assert.ok(await page.locator('[data-message="2"]').isVisible());
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

async function handoff(page, diagnostics) {
  await page.locator('[data-cta="final"]').click();
  await page.waitForURL(BOOKING);
  assert.deepEqual(diagnostics.handoffs, [{ method: 'GET', url: BOOKING }]);
  assert.equal(await page.title(), 'Local booking-link test');
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
      const pinned = viewport.width >= 1024 && viewport.height >= 760;
      assert.equal(await page.locator('#how-it-works').getAttribute('data-sc-act'), pinned ? 'pin' : 'flow');
      if (pinned) {
        for (const [progress, stage] of [[.08, 0], [.43, 1], [.78, 2]]) {
          await scrollStage(page, progress, stage);
          await screenshot(page, `${name}-scroll-step-${stage + 1}`);
          await noOverflow(page, `${name} scroll step ${stage + 1}`);
        }
      }
      await conversations(page, name, pinned);
      await faq(page);
      await reachableSections(page);
      await screenshot(page, `${name}-closing`);
      if ([390, 1440].includes(viewport.width)) await screenshot(page, `${name}-full-page`, true);
      entry.workflow = pinned
        ? 'Three scroll stages, three scenarios and approval routing verified'
        : 'Three scenarios and approval routing verified; the workflow remains in normal flow';
      await handoff(page, diagnostics);
    });
  }
  for (const viewport of [{ width: 1440, height: 900 }, { width: 360, height: 640 }]) {
    const name = `reduced-${viewport.width}`;
    await runCase(name, { viewport, reducedMotion: 'reduce' }, async (page, entry) => {
      entry.primaryLinks = await primaryLinks(page, true);
      assert.equal(await page.locator('.sc-act--pinned').count(), 0);
      assert.equal(await page.locator('#how-it-works').getAttribute('data-sc-act'), 'flow');
      assert.equal(await page.locator('[data-demo]').getAttribute('data-stage'), '2');
      assert.ok(await page.locator('[data-message="2"]').isVisible());
      assert.equal(await page.evaluate(() => document.getAnimations().filter(animation => animation.playState === 'running').length), 0);
      await reachableSections(page);
      await screenshot(page, `${name}-closing`);
      entry.reachability = 'Every section and final call link reachable without pinning or running animations';
    });
  }
  await runCase('no-js-390', { viewport: { width: 390, height: 844 }, javaScriptEnabled: false }, async (page, entry, diagnostics) => {
    entry.primaryLinks = await primaryLinks(page, true);
    assert.ok(await page.locator('#nav-links').isVisible(), 'Navigation remains available without JavaScript.');
    assert.equal(await page.locator('.sc-act--pinned').count(), 0);
    assert.equal(await page.locator('[data-message]').count(), 3);
    assert.ok(await page.locator('[data-message="2"]').isVisible(), 'The full example is in the HTML.');
    await faq(page);
    await reachableSections(page);
    await screenshot(page, 'no-js-390-full-page', true);
    await handoff(page, diagnostics);
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
        await page.locator('.story-footer').scrollIntoViewIfNeeded();
        assert.ok(await page.locator('.story-footer .sb-brand').isVisible());
        await noOverflow(page, `${route} footer`);
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
