/* Browser checks intercept the Guest Intel destination; no reports are requested. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const BASE = process.env.REVIEW_URL || 'http://127.0.0.1:8765';
const sample = 'https://www.airbnb.com/rooms/123456789?source=review&check_in=2027-01-10';
let browser;
const deadline = setTimeout(() => { console.error('Widget checks exceeded 3 minutes'); process.exit(1); }, 180000);
(async () => {
  browser = await chromium.launch();
  fs.mkdirSync('previews', {recursive:true});
  const report = [];
  async function prepare(options = {}) {
    const context = await browser.newContext(options);
    const page = await context.newPage();
    page.setDefaultTimeout(12000);
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    await page.route('**/*', route => {
      const url = route.request().url();
      if (/googletagmanager|google-analytics|leadconnectorhq|reputationhub/.test(url)) return route.abort();
      return route.continue();
    });
    await page.goto(BASE, {waitUntil:'networkidle', timeout:30000});
    return {context, page, errors};
  }
  for (const width of [320,390,640,768,1024,1280,1440,1920]) {
    const {context, page, errors} = await prepare({viewport:{width,height:1000},reducedMotion:'reduce'});
    const forms = page.locator('form[data-guest-strategy]');
    assert.equal(await forms.count(),3);
    for (let i=0; i<3; i++) {
      const form = forms.nth(i);
      await form.scrollIntoViewIfNeeded();
      const input = form.locator('input[name="listing"]');
      const submit = form.locator('button[type="submit"]');
      for (const control of [form,input,submit]) {
        const box = await control.boundingBox();
        assert.ok(box && box.x>=0 && box.x+box.width<=width+1, `Overflow at ${width}px`);
      }
      const ib = await input.boundingBox(), bb = await submit.boundingBox();
      assert.ok(ib.height>=50 && bb.height>=50,'Touch targets');
      if (width<=680) assert.ok(bb.y>=ib.y+ib.height-1,'Mobile controls must stack');
      assert.equal(await form.getAttribute('method'),'GET');
      assert.equal(await form.getAttribute('action'),'https://guest-intel.strbooster.com/');
      assert.equal(await input.evaluate(el=>getComputedStyle(el).fontSize),'16px');
      for (const invalid of ['', 'not a link', 'ftp://example.com/listing', 'javascript:alert(1)']) {
        await input.fill(invalid);
        assert.equal(await input.evaluate(el=>el.checkValidity()),false);
      }
      await input.fill(sample);
      assert.equal(await input.evaluate(el=>el.checkValidity()),true);
      await input.fill('');
    }
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
    const nav = page.locator('[data-cta="navigation"]');
    assert.equal(await nav.getAttribute('href'),'/#guest-strategy');
    await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));
    if (width<=900) await page.locator('.menu-toggle').click();
    await nav.click();
    await page.waitForFunction(()=>document.activeElement?.id==='guest-strategy-listing');
    if (width===390 || width===1440) {
      await page.locator('#guest-strategy-listing').evaluate(el=>el.blur());
      await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));
      await page.screenshot({path:`previews/widget-hero-${width}.jpg`,type:'jpeg',quality:88});
      await page.locator('#guest-strategy').screenshot({path:`previews/widget-${width}.png`});
    }
    assert.deepEqual(errors,[]);
    report.push({width,overflow:false,forms:3,validation:true,navigationFocus:true,errors});
    await context.close();
  }
  for (const javaScriptEnabled of [true,false]) {
    for (const location of ['hero','guest-insight','final']) {
      const {context,page} = await prepare({viewport:{width:390,height:1000},javaScriptEnabled,reducedMotion:'reduce'});
      const form = page.locator(`[data-guest-strategy="${location}"]`);
      const input = form.locator('input[name="listing"]');
      let captured = null;
      await page.route('https://guest-intel.strbooster.com/**', async route => {
        captured = {url:route.request().url(), method:route.request().method()};
        await route.fulfill({status:200,contentType:'text/html',body:'<!doctype html><title>Intercepted handoff</title><p>Test only. No report requested.</p>'});
      });
      await input.fill(sample);
      await input.press('Enter');
      await page.waitForURL('https://guest-intel.strbooster.com/**');
      assert.ok(captured);
      assert.equal(captured.method,'GET');
      const url=new URL(captured.url);
      assert.equal(url.searchParams.get('listing'),sample,'Preserve the entire listing URL');
      assert.deepEqual([...url.searchParams.keys()],['listing']);
      report.push({location,javaScriptEnabled,nativeGET:true,encodedListingPreserved:true,externalRequestIntercepted:true});
      await context.close();
    }
  }
  const {context,page} = await prepare({reducedMotion:'reduce'});
  await page.evaluate(() => {
    window.__widgetEvents=[];
    window.strBoosterTrack=(name,details)=>window.__widgetEvents.push({name,details});
    document.querySelector('#guest-strategy').addEventListener('submit',e=>e.preventDefault());
  });
  await page.locator('#guest-strategy-listing').fill(sample);
  await page.locator('#guest-strategy button').click();
  const events = await page.evaluate(()=>window.__widgetEvents);
  assert.deepEqual(events,[{name:'guest_strategy_submit',details:{form_location:'hero',app_name:'guest_intel'}}]);
  assert.ok(!JSON.stringify(events).includes(sample));
  await context.close();
  fs.writeFileSync('previews/widget-report.json',JSON.stringify(report,null,2));
  console.log('GUEST_STRATEGY_REVIEW',JSON.stringify(report));
})().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{
  if(browser) await browser.close();
  clearTimeout(deadline);
});
