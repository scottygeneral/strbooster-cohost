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
      if (reduced.matches || saveData || pausedByUser || !visible || document.hidden) {
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
