/* STR Booster: progressive enhancement; the full story works without JavaScript. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const header = document.querySelector('.story-header');
  const hero = document.querySelector('.v-hero');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.v-nav-links');

  // app.js owns production navigation. A standalone, analytics-free review has
  // no app.js, so supply the same behavior only when that integration is absent.
  if (typeof window.strBoosterTrack !== 'function' && toggle && nav) {
    const close = () => { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); };
    toggle.addEventListener('click', () => {
      const open = !nav.classList.contains('open');
      nav.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
    document.addEventListener('click', event => { if (!event.target.closest('.story-header')) close(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && nav.classList.contains('open')) { close(); toggle.focus(); }
    });
  }
  if (header && hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      header.classList.toggle('is-past-hero', !entries[0].isIntersecting);
    }, { rootMargin: '-90px 0px 0px 0px' }).observe(hero);
  }
  if (header && toggle) {
    const syncMenu = () => header.classList.toggle('is-menu-open', toggle.getAttribute('aria-expanded') === 'true');
    new MutationObserver(syncMenu).observe(toggle, { attributes: true, attributeFilter: ['aria-expanded'] });
    syncMenu();
  }

  const funnel = document.querySelector('[data-funnel]');
  if (funnel) {
    const buttons = [...funnel.querySelectorAll('[data-step]')];
    const panels = [...funnel.querySelectorAll('[data-panel]')];
    const list = funnel.querySelector('.v-tabs');
    if (list && buttons.length && buttons.length === panels.length) {
      list.setAttribute('role', 'tablist');
      list.setAttribute('aria-label', 'The guest booking journey');
      list.setAttribute('aria-orientation', 'horizontal');
      const activate = (index, focus = false, track = false) => {
        buttons.forEach((button, i) => {
          const selected = i === index;
          button.setAttribute('aria-selected', String(selected));
          button.tabIndex = selected ? 0 : -1;
          panels[i].hidden = !selected;
          panels[i].classList.toggle('is-entering', selected && !reduced.matches);
        });
        if (focus) buttons[index].focus();
        if (track && typeof window.strBoosterTrack === 'function') {
          window.strBoosterTrack('funnel_step_view', { step: buttons[index].dataset.step });
        }
      };
      buttons.forEach((button, index) => {
        const panel = panels.find(item => item.dataset.panel === button.dataset.step);
        if (!panel) return;
        button.setAttribute('role', 'tab');
        button.setAttribute('aria-controls', panel.id);
        panel.setAttribute('role', 'tabpanel');
        panel.tabIndex = 0;
        button.addEventListener('click', () => activate(index, false, true));
        button.addEventListener('keydown', event => {
          let next;
          if (event.key === 'ArrowRight') next = (index + 1) % buttons.length;
          if (event.key === 'ArrowLeft') next = (index - 1 + buttons.length) % buttons.length;
          if (event.key === 'Home') next = 0;
          if (event.key === 'End') next = buttons.length - 1;
          if (next !== undefined) { event.preventDefault(); activate(next, true, true); }
        });
      });
      activate(0);
    }
  }

  // The renderer emits these elements only when the local film exists.
  const video = document.querySelector('[data-hero-video]');
  const control = document.querySelector('[data-video-toggle]');
  if (video && control) {
    const saveData = Boolean(navigator.connection && navigator.connection.saveData);
    let pausedByUser = false;
    let visible = true;
    let failed = false;
    const label = () => {
      control.textContent = video.paused ? 'Play background film' : 'Pause background film';
      control.setAttribute('aria-label', control.textContent);
    };
    const sync = () => {
      if (failed) return;
      if (reduced.matches || saveData || window.strBoosterMotionEnabled === false || pausedByUser || !visible || document.hidden) {
        video.pause();
        if (reduced.matches || saveData) video.classList.remove('is-playing');
        label();
        return;
      }
      if (!video.getAttribute('src') && video.dataset.src) { video.src = video.dataset.src; video.load(); }
      video.muted = true;
      const playback = video.play();
      if (playback) playback.catch(label);
    };
    control.hidden = reduced.matches || saveData;
    control.addEventListener('click', () => { pausedByUser = !video.paused; sync(); });
    video.addEventListener('playing', () => { video.classList.add('is-playing'); label(); });
    video.addEventListener('pause', label);
    video.addEventListener('error', () => { failed = true; video.classList.remove('is-playing'); control.hidden = true; });
    reduced.addEventListener('change', () => { control.hidden = failed || reduced.matches || saveData; sync(); });
    document.addEventListener('visibilitychange', sync);
    document.addEventListener('strbooster:motion', sync);
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => { visible = entries[0].isIntersecting; sync(); }).observe(video);
    sync();
  }

  const reviews = document.querySelector('[data-reviews]');
  if (reviews) reviews.addEventListener('toggle', () => {
    if (!reviews.open || reviews.dataset.loaded) return;
    reviews.dataset.loaded = 'true';
    const frame = reviews.querySelector('iframe');
    if (frame && frame.dataset.src) frame.src = frame.dataset.src;
    const script = document.createElement('script');
    script.src = 'https://reputationhub.site/reputation/assets/review-widget.js';
    script.async = true;
    document.body.appendChild(script);
  });
})();

/* Motion layer for approved Direction 02.
   Kept self-contained so the existing portable-review exporter includes it.
   No dependencies, scroll hijacking, hidden-until-JS copy or autoplay tab changes.
   Scoped styles are installed only on the homepage; inner-page shell is untouched. */
(() => {
  'use strict';
  const home = document.querySelector('.journey-home');
  if (!home || document.getElementById('sb-motion-style')) return;
  const root = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const connection = navigator.connection;
  const preferenceKey = 'strbooster-motion-paused';
  let userPaused = false;
  try { userPaused = localStorage.getItem(preferenceKey) === 'true'; } catch (_) { /* Storage is optional. */ }
  const blocked = () => reduce.matches || Boolean(connection && connection.saveData);
  const enabled = () => !blocked() && !userPaused;
  const animations = new Set();
  const zones = new Map();
  let frame = 0;
  let elapsed = 0;
  let lastFrame = 0;
  let flowVisible = false;
  let flowFinished = false;
  let selectedStep = -1;
  const duration = 12000;

  const style = document.createElement('style');
  style.id = 'sb-motion-style';
  style.textContent = `
/* Restrained, pausable motion. Geometry and text stay readable at rest. */
.journey-home .sb-motion-control{position:fixed;left:16px;bottom:16px;z-index:45;display:inline-flex;gap:9px;align-items:center;min-height:42px;padding:10px 15px;border:1px solid #b9c8be;border-radius:30px;background:#f5f3eef5;color:#0d1f2d;box-shadow:0 2px 16px #0d1f2d12;font:500 11px/1.3 var(--font);letter-spacing:.02em;cursor:pointer}
.journey-home .sb-motion-control svg{width:12px;height:12px;flex:none;fill:currentColor}
.journey-home .sb-motion-control:disabled{cursor:default}
.sb-motion-zone .sb-continuous,.sb-motion-zone .v-orbit::after{animation-play-state:paused!important}
html[data-sb-motion=running] .sb-motion-zone.sb-inview .sb-continuous,html[data-sb-motion=running] .sb-motion-zone.sb-inview .v-orbit::after{animation-play-state:running!important}
.v-hero-media img.sb-continuous{animation:sb-camera 24s ease-in-out infinite alternate;transform-origin:60% 45%}
.v-orbit{position:relative}
.v-orbit::after{content:'';position:absolute;inset:-6px;border:1px dashed #bde2cdb3;border-radius:50%;animation:sb-orbit 28s linear infinite;pointer-events:none}
.v-browser.sb-continuous{animation:sb-float-browser 9s ease-in-out infinite alternate}
.v-email.sb-continuous{animation:sb-float-email 8s ease-in-out infinite alternate}
@keyframes sb-camera{from{transform:scale(1)}to{transform:scale(1.045) translate(-.3%,.2%)}}
@keyframes sb-orbit{to{transform:rotate(360deg)}}
@keyframes sb-float-browser{from{translate:0 0}to{translate:0 -8px}}
@keyframes sb-float-email{from{translate:0 0}to{translate:0 9px}}
.journey-home .sb-connection{position:relative;margin:0 0 34px;padding:26px 28px 20px;background:var(--navy);color:var(--cream);overflow:hidden;border-radius:2px}
.sb-connection-top{display:flex;justify-content:space-between;gap:20px;align-items:center}
.sb-connection-kicker{font:500 10px/1.6 var(--font);letter-spacing:.15em;text-transform:uppercase;color:var(--mint)}
.sb-replay{display:inline-flex;gap:9px;align-items:center;min-height:40px;padding:7px 0 7px 12px;border:0;border-bottom:1px solid #ffffff55;background:transparent;color:var(--cream);font:400 11px/1.4 var(--font)!important;white-space:nowrap}
.sb-replay:disabled{opacity:.6;cursor:default}
.sb-replay>span{font-size:19px}
.sb-route{position:relative;height:190px;margin-top:4px}
.sb-route>svg{position:absolute;inset:0;width:100%;height:180px;overflow:visible}
.sb-route-base{stroke:#78998e;stroke-width:1;fill:none;opacity:.45}
.sb-route-drawn{stroke:#bde2cd;stroke-width:1.6;fill:none;stroke-dasharray:1;stroke-dashoffset:1}
.sb-route-return{stroke:#bde2cd;stroke-width:1.4;fill:none;stroke-dasharray:1;stroke-dashoffset:1;opacity:.75}
.sb-traveler{fill:#f5f3ee;stroke:#1a7f64;stroke-width:4}
.sb-traveler-halo{fill:#bde2cd;opacity:.15}
.sb-stations{position:absolute;top:40px;inset-inline:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));list-style:none;padding:0;margin:0!important}
.sb-stations>li{display:flex;flex-direction:column;align-items:center;text-align:center;min-width:0;margin:0!important}
.sb-station-icon{display:grid;place-items:center;width:48px;height:48px;border:1px solid #89aa9e;background:var(--navy);border-radius:50%;color:var(--mint);transition:background .45s,color .45s,border-color .45s,box-shadow .45s}
.sb-station-icon>svg{width:21px;height:21px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.sb-stations .is-active .sb-station-icon{background:var(--mint);color:var(--navy);border-color:var(--mint);box-shadow:0 0 0 7px #bde2cd14}
.sb-stations .is-complete .sb-station-icon{border-color:#bde2cd;background:#1a7f6455}
.sb-stations strong{font:400 15px/1.5 var(--font);margin-top:12px;letter-spacing:-.01em}
.sb-stations small{font:400 10px/1.5 var(--font);color:#c1d3ca;margin-top:2px}
.sb-connection-caption{display:flex;justify-content:space-between;gap:20px;align-items:center;border-top:1px solid #ffffff25;padding-top:16px;font:400 11px/1.5 var(--font);color:#d4e2d8}
.sb-connection-caption>span:last-child{color:#bde2cd}
html[data-sb-motion=paused] .journey-home .sb-continuous{animation-play-state:paused!important}
html[data-sb-motion=paused] .journey-home .v-panel,html[data-sb-motion=paused] .journey-home .v-panel.is-entering{animation:none!important}
html[data-sb-motion=paused]{scroll-behavior:auto}
html[data-sb-motion=paused] .journey-home *{transition:none!important}
html[data-sb-motion=paused] .journey-home .v-button:hover,html[data-sb-motion=paused] .journey-home .v-text-link:hover span{transform:none}
@media(max-width:640px){.journey-home .sb-connection{padding:19px 12px 17px;margin-bottom:24px}.sb-connection-top{gap:10px;padding-inline:4px}.sb-connection-kicker{font-size:8px;letter-spacing:.1em;max-width:140px}.sb-replay{font-size:10px!important;gap:6px}.sb-route{height:177px;margin-top:1px}.sb-station-icon{width:38px;height:38px}.sb-station-icon>svg{width:18px;height:18px}.sb-stations{top:45px}.sb-stations strong{font-size:12px;margin-top:10px}.sb-stations small{font-size:8px;max-width:60px}.sb-connection-caption{font-size:9px;gap:12px;align-items:flex-start}.sb-connection-caption>span:first-child{max-width:170px}.sb-connection-caption>span:last-child{text-align:right;max-width:90px}.journey-home .sb-motion-control{left:10px;bottom:10px;min-height:40px;font-size:10px;padding:9px 12px}}
@media(prefers-reduced-motion:reduce){.journey-home .sb-continuous,.journey-home .v-orbit::after{animation:none!important}.sb-station-icon{transition:none!important}}
@media print{.sb-motion-control,.sb-replay{display:none!important}.sb-route-drawn,.sb-route-return{stroke-dashoffset:0}}
`;
  document.head.appendChild(style);

  const control = document.createElement('button');
  control.type = 'button';
  control.className = 'sb-motion-control';
  control.setAttribute('data-motion-control', '');
  home.appendChild(control);

  // The graphic reinforces existing copy, never fabricates live booking activity.
  const funnel = document.querySelector('[data-funnel]');
  let flow, forwardPath, returnPath, traveler, halo, stations, replay;
  let returnLength = 0;
  if (funnel) {
    flow = document.createElement('figure');
    flow.className = 'sb-connection';
    flow.setAttribute('aria-labelledby', 'sb-connection-caption');
    flow.innerHTML = `
      <div class="sb-connection-top"><span class="sb-connection-kicker">One guest. A lasting connection.</span><button class="sb-replay" type="button" data-replay-journey><span aria-hidden="true">↻</span> Replay journey</button></div>
      <div class="sb-route">
        <svg viewBox="0 0 1000 180" preserveAspectRatio="none" aria-hidden="true" focusable="false">
          <path class="sb-route-base" d="M125 64 H875"/>
          <path class="sb-route-base" d="M875 64 V123 Q875 154 835 154 H165 Q125 154 125 123 V64"/>
          <path data-route-forward class="sb-route-drawn" pathLength="1" d="M125 64 H875"/>
          <path data-route-return class="sb-route-return" pathLength="1" d="M875 64 V123 Q875 154 835 154 H165 Q125 154 125 123 V64"/>
          <circle data-traveler-halo class="sb-traveler-halo" cx="125" cy="64" r="12"/>
          <circle data-traveler class="sb-traveler" cx="125" cy="64" r="5"/>
        </svg>
        <ol class="sb-stations">
          <li><span class="sb-station-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6"/><path d="m15 15 5 5m-12-10h4m-2-2v4"/></svg></span><strong>Discover</strong><small>Find your stay</small></li>
          <li><span class="sb-station-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/></svg></span><strong>Connect</strong><small>Build the relationship</small></li>
          <li><span class="sb-station-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="5" width="16" height="16" rx="2"/><path d="M8 3v4m8-4v4M4 10h16m-12 5 3 3 5-5"/></svg></span><strong>Book</strong><small>Choose you directly</small></li>
          <li><span class="sb-station-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 7v5h-5M4 17v-5h5M5.6 7a7 7 0 0 1 11.9-1L20 9M4 15l2.5 3A7 7 0 0 0 18.4 17"/></svg></span><strong>Return</strong><small>Make new memories</small></li>
        </ol>
      </div>
      <figcaption class="sb-connection-caption" id="sb-connection-caption"><span>A guest journey, not just a transaction.</span><span>Illustrative sequence</span></figcaption>`;
    funnel.before(flow);
    forwardPath = flow.querySelector('[data-route-forward]');
    returnPath = flow.querySelector('[data-route-return]');
    traveler = flow.querySelector('[data-traveler]');
    halo = flow.querySelector('[data-traveler-halo]');
    stations = [...flow.querySelectorAll('.sb-stations>li')];
    replay = flow.querySelector('[data-replay-journey]');
    returnLength = returnPath.getTotalLength();
  }

  function draw(milliseconds) {
    if (!flow) return;
    const t = Math.min(milliseconds / duration, 1);
    const outbound = Math.min(t / .75, 1);
    const inbound = Math.max(0, (t - .75) / .25);
    forwardPath.style.strokeDashoffset = String(1 - outbound);
    returnPath.style.strokeDashoffset = String(1 - inbound);
    const point = t <= .75 ? { x: 125 + 750 * outbound, y: 64 } : returnPath.getPointAtLength(inbound * returnLength);
    for (const element of [traveler, halo]) {
      element.setAttribute('cx', point.x.toFixed(2));
      element.setAttribute('cy', point.y.toFixed(2));
    }
    const index = Math.min(3, Math.floor(milliseconds / 3000));
    if (index !== selectedStep) {
      selectedStep = index;
      stations.forEach((station, i) => {
        station.classList.toggle('is-active', i === index);
        station.classList.toggle('is-complete', i < index);
      });
      flow.dataset.stage = ['discover', 'connect', 'book', 'return'][index];
    }
    flow.dataset.progress = t.toFixed(3);
  }

  function stopClock() { if (frame) cancelAnimationFrame(frame); frame = 0; lastFrame = 0; }
  function canRun() { return enabled() && !document.hidden && flowVisible && !flowFinished; }
  function tick(now) {
    frame = 0;
    if (!canRun()) { lastFrame = 0; return; }
    if (lastFrame) elapsed += Math.min(now - lastFrame, 64);
    lastFrame = now;
    draw(elapsed);
    if (elapsed >= duration) { flowFinished = true; lastFrame = 0; return; }
    frame = requestAnimationFrame(tick);
  }
  function syncClock() { if (canRun()) { if (!frame) frame = requestAnimationFrame(tick); } else stopClock(); }
  function finishReveals() {
    animations.forEach(animation => { try { animation.finish(); } catch (_) { animation.cancel(); } });
    animations.clear();
  }
  function sync() {
    root.dataset.sbMotion = enabled() && !document.hidden ? 'running' : 'paused';
    window.strBoosterMotionEnabled = enabled();
    control.disabled = blocked();
    const label = blocked() ? 'Motion off' : userPaused ? 'Play motion' : 'Pause motion';
    control.innerHTML = `<svg viewBox="0 0 12 12" aria-hidden="true">${enabled() ? '<path d="M2 1h3v10H2zm5 0h3v10H7z"/>' : '<path d="M3 1v10l8-5z"/>'}</svg><span>${label}</span>`;
    control.setAttribute('aria-label', blocked() ? 'Website motion is off to respect your device settings' : label + ' across this website');
    control.title = blocked() ? 'Respects reduced-motion and data-saving preferences.' : 'Controls decorative animations. Content and links remain available.';
    if (!enabled()) finishReveals();
    if (replay) replay.disabled = !enabled();
    if (blocked()) { draw(duration); flowFinished = true; }
    document.dispatchEvent(new CustomEvent('strbooster:motion'));
    syncClock();
  }
  control.addEventListener('click', () => {
    userPaused = !userPaused;
    try { localStorage.setItem(preferenceKey, String(userPaused)); } catch (_) { /* Continue without persistence. */ }
    sync();
  });
  if (replay) replay.addEventListener('click', () => {
    if (!enabled()) return;
    stopClock(); elapsed = 0; flowFinished = false; draw(0); syncClock();
  });
  // Reading a tab never gets interrupted by an automatically switching panel.
  if (funnel) funnel.querySelectorAll('[data-step]').forEach((tab, index) => {
    tab.addEventListener('click', () => { flowFinished = true; stopClock(); draw(index * 3000); });
    tab.addEventListener('keydown', event => {
      if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      const active = [...funnel.querySelectorAll('[data-step]')].findIndex(item => item.getAttribute('aria-selected') === 'true');
      if (active >= 0) { flowFinished = true; stopClock(); draw(active * 3000); }
    });
  });

  function animate(element, keyframes, delay = 0, length = 750) {
    if (!enabled() || document.hidden || !element || typeof element.animate !== 'function') return;
    const animation = element.animate(keyframes, { duration: length, delay, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' });
    animations.add(animation);
    animation.onfinish = animation.oncancel = () => animations.delete(animation);
  }
  const revealFrames = [{ opacity: .35, translate: '0 24px' }, { opacity: 1, translate: '0 0' }];
  const heroZone = document.querySelector('.v-hero');
  const artifactZone = document.querySelector('.v-artifact-stage');
  heroZone?.querySelector('.v-hero-media img')?.classList.add('sb-continuous');
  artifactZone?.querySelectorAll('.v-browser,.v-email').forEach(element => element.classList.add('sb-continuous'));
  [heroZone, artifactZone].filter(Boolean).forEach(zone => {
    zone.classList.add('sb-motion-zone');
    zones.set(zone, false);
  });

  if ('IntersectionObserver' in window) {
    const visibility = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.target === flow) flowVisible = entry.isIntersecting;
        else { zones.set(entry.target, entry.isIntersecting); entry.target.classList.toggle('sb-inview', entry.isIntersecting); }
      });
      syncClock();
    }, { threshold: .1 });
    zones.forEach((_, zone) => visibility.observe(zone));
    if (flow) visibility.observe(flow);
    const reveal = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        reveal.unobserve(entry.target);
        animate(entry.target, revealFrames);
        if (entry.target.matches('.v-report')) {
          entry.target.querySelectorAll('.v-report-head,h3,dl>div').forEach((row, index) => animate(row, [{ opacity: .3 }, { opacity: 1 }], index * 130, 650));
        }
      });
    }, { threshold: .12, rootMargin: '0px 0px -24px 0px' });
    document.querySelectorAll('.v-statement,.v-pillars-heading h2,.v-brand-copy h3,.v-funnel-copy h3,.v-journey-heading,.v-insight-copy h2,.v-report,.v-proof-heading,.v-case,.v-founder-grid>div,.v-final h2').forEach(element => reveal.observe(element));
  } else {
    // No observer: retain a static accessible page, without offscreen animation.
    flowVisible = false;
    if (flow) draw(duration);
  }
  reduce.addEventListener('change', sync);
  if (connection && typeof connection.addEventListener === 'function') connection.addEventListener('change', sync);
  document.addEventListener('visibilitychange', () => { if (document.hidden) finishReveals(); sync(); });
  window.addEventListener('pagehide', () => { stopClock(); finishReveals(); });
  window.addEventListener('pageshow', sync);
  draw(0);
  sync();
  document.querySelectorAll('.v-hero-top>.v-label,.v-hero h1,.v-hero-bottom>div:first-child').forEach((element, index) => animate(element, revealFrames, index * 100, 850));
})();
