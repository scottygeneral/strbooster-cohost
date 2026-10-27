/* Progressive enhancement only: all copy and links work without JavaScript. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const funnel = document.querySelector('[data-funnel]');
  if (funnel) {
    const buttons = [...funnel.querySelectorAll('[data-step]')];
    const panels = [...funnel.querySelectorAll('[data-panel]')];
    const list = funnel.querySelector('.s-step-buttons');
    list.setAttribute('role', 'tablist');
    list.setAttribute('aria-label', 'The guest booking journey');
    const compact = window.matchMedia('(max-width: 680px)');
    const orient = () => list.setAttribute('aria-orientation', compact.matches ? 'horizontal' : 'vertical');
    orient();
    compact.addEventListener('change', orient);
    function activate(index, focus = false, track = false) {
      buttons.forEach((button, i) => {
        button.setAttribute('aria-selected', String(i === index));
        button.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
      if (focus) buttons[index].focus();
      if (track && typeof window.strBoosterTrack === 'function') {
        window.strBoosterTrack('funnel_step_view', { step: buttons[index].dataset.step });
      }
    }
    buttons.forEach((button, index) => {
      button.setAttribute('role', 'tab');
      button.setAttribute('aria-controls', panels[index].id);
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].tabIndex = 0;
      button.addEventListener('click', () => activate(index, false, true));
      button.addEventListener('keydown', event => {
        let next;
        if (['ArrowRight', 'ArrowDown'].includes(event.key)) next = (index + 1) % buttons.length;
        if (['ArrowLeft', 'ArrowUp'].includes(event.key)) next = (index - 1 + buttons.length) % buttons.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = buttons.length - 1;
        if (next !== undefined) { event.preventDefault(); activate(next, true, true); }
      });
    });
    activate(0);
  }

  // A hero film is emitted by the Python renderer only when its local file exists.
  const video = document.querySelector('[data-hero-video]');
  const control = document.querySelector('[data-video-toggle]');
  if (video && control) {
    const connection = navigator.connection;
    const saveData = Boolean(connection && connection.saveData);
    let userPaused = false;
    let inView = true;
    const shouldPlay = () => !reducedMotion.matches && !saveData && !userPaused && inView && !document.hidden;
    function updateLabel() {
      control.textContent = video.paused ? 'Play background film' : 'Pause background film';
      control.setAttribute('aria-label', control.textContent);
    }
    function sync() {
      if (!shouldPlay()) { video.pause(); updateLabel(); return; }
      if (!video.src && video.dataset.src) { video.src = video.dataset.src; video.load(); }
      const attempt = video.play();
      if (attempt) attempt.catch(() => { updateLabel(); });
    }
    control.hidden = reducedMotion.matches || saveData;
    control.addEventListener('click', () => { userPaused = !video.paused; sync(); });
    video.addEventListener('playing', () => { video.classList.add('is-playing'); updateLabel(); });
    video.addEventListener('pause', updateLabel);
    video.addEventListener('error', () => { video.classList.remove('is-playing'); control.hidden = true; });
    reducedMotion.addEventListener('change', () => {
      control.hidden = reducedMotion.matches || saveData;
      if (reducedMotion.matches) video.classList.remove('is-playing');
      sync();
    });
    document.addEventListener('visibilitychange', sync);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => { inView = entries[0].isIntersecting; sync(); }).observe(video);
    }
    sync();
  }

  // Load the original review widget only when explicitly expanded.
  const reviews = document.querySelector('[data-reviews]');
  if (reviews) {
    reviews.addEventListener('toggle', () => {
      if (!reviews.open || reviews.dataset.loaded) return;
      reviews.dataset.loaded = 'true';
      const frame = reviews.querySelector('iframe');
      if (frame && frame.dataset.src) frame.src = frame.dataset.src;
      const script = document.createElement('script');
      script.src = 'https://reputationhub.site/reputation/assets/review-widget.js';
      script.async = true;
      document.body.appendChild(script);
    });
  }
})();
