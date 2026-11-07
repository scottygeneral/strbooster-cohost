/* STR Booster homepage motion. Progressive enhancement: all content is readable without this file. */
(() => {
  'use strict';
  const body = document.body;
  if (!body.classList.contains('dx-home')) return;
  document.documentElement.classList.add('has-js');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* Split helpers (keep accessible text on the parent). */
  const manifesto = $('[data-words]');
  if (manifesto) {
    const text = manifesto.textContent.trim();
    manifesto.setAttribute('aria-label', text);
    const keys = new Set(['complexity', 'one', 'system']);
    manifesto.innerHTML = text.split(/\s+/).map(word => {
      const bare = word.toLowerCase().replace(/[^a-z]/g, '');
      return `<span class="w${keys.has(bare) ? ' is-key' : ''}" aria-hidden="true">${word}</span>`;
    }).join(' ');
  }
  const giant = $('[data-letters]');
  if (giant) {
    const text = giant.textContent;
    giant.setAttribute('aria-label', text);
    giant.innerHTML = [...text].map((ch, i) =>
      `<span class="l${ch === ' ' ? ' is-sp' : ''}" style="--li:${i}" aria-hidden="true">${ch === ' ' ? '&nbsp;' : ch}</span>`).join('');
  }
  const words = manifesto ? $$('.w', manifesto) : [];
  const letters = giant ? $$('.l', giant) : [];

  /* Load-in. */
  const ready = () => requestAnimationFrame(() => body.classList.add('is-loaded'));
  (document.fonts?.ready || Promise.resolve()).then(ready);
  setTimeout(ready, 900);

  /* Hero video: only when motion is welcome and the connection is not constrained. */
  const video = $('.dx-hero-video');
  const saveData = navigator.connection?.saveData;
  if (video && !reduced.matches && !saveData && innerWidth > 600) {
    video.src = video.dataset.src;
    video.addEventListener('playing', () => video.classList.add('is-playing'), { once: true });
    video.play?.().catch(() => {});
  }

  /* Reveal on enter. */
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -12% 0px' });
  $$('[data-reveal]').forEach(el => io.observe(el));

  /* Stack: one active system at a time. */
  const systems = $$('.dx-sys');
  const sysIO = new IntersectionObserver(entries => entries.forEach(e => {
    e.target.classList.toggle('is-active', e.isIntersecting);
    e.target.querySelector('.dx-ui')?.classList.toggle('is-active', e.isIntersecting);
  }), { rootMargin: '-35% 0px -35% 0px' });
  systems.forEach(s => sysIO.observe(s));

  /* Marquee responds to scroll speed and direction. */
  const track = $('.dx-mq-track');
  let mqAnim = null;
  const getMq = () => (mqAnim ||= track?.getAnimations?.()[0] || null);

  /* Scroll-linked choreography. */
  const hero = $('.dx-hero');
  const heroMedia = $('.dx-hero-media');
  const premise = $('.dx-premise');
  const untangle = $('.dx-untangle');
  const close = $('.dx-close');
  const closeMedia = $('.dx-close-media img');
  const parallax = $$('[data-parallax]');
  let lastY = scrollY, vel = 0, frame = 0;

  const progress = (el, start = 1, end = 0) => {
    const r = el.getBoundingClientRect();
    const h = innerHeight;
    return clamp((h * start - r.top) / (r.height + h * (start - end)));
  };

  function update() {
    frame = 0;
    const y = scrollY;
    const dy = y - lastY;
    lastY = y;
    vel += (dy - vel) * 0.2;

    body.classList.toggle('is-scrolled', y > 40);
    body.classList.toggle('is-hidden-nav', dy > 4 && y > innerHeight * 0.9);
    if (dy < -4) body.classList.remove('is-hidden-nav');

    if (reduced.matches) return;

    if (hero && heroMedia) {
      const p = clamp(y / hero.offsetHeight);
      heroMedia.style.setProperty('--hero-shift', `${p * hero.offsetHeight * 0.28}px`);
      heroMedia.style.setProperty('--hero-scale', (1.04 + p * 0.08).toFixed(4));
    }

    if (words.length && premise) {
      const r = manifesto.getBoundingClientRect();
      const p = clamp((innerHeight * 0.85 - r.top) / (r.height + innerHeight * 0.35));
      const lit = Math.round(p * words.length * 1.05);
      words.forEach((w, i) => w.classList.toggle('is-lit', i < lit));
    }

    if (untangle) {
      const p = progress(untangle, 1, 0);
      untangle.style.setProperty('--ut-scale', (1.14 - p * 0.14).toFixed(4));
      untangle.style.setProperty('--signal', (1 - clamp((p - 0.25) / 0.4)).toFixed(4));
    }

    parallax.forEach(el => {
      const r = el.getBoundingClientRect();
      const c = r.top + r.height / 2 - innerHeight / 2;
      el.style.setProperty('--py', `${(c * Number(el.dataset.parallax)).toFixed(1)}px`);
    });

    if (close) {
      const p = progress(close, 1, 0.4);
      closeMedia?.style.setProperty('--close-scale', (1.18 - p * 0.18).toFixed(4));
      const n = letters.length;
      letters.forEach((l, i) => {
        const t = clamp((p - 0.12 - (i / n) * 0.22) / 0.3);
        const e = 1 - Math.pow(1 - t, 3);
        l.style.setProperty('--ly', `${((1 - e) * 0.6).toFixed(3)}em`);
        l.style.setProperty('--lr', `${((1 - e) * (i % 2 ? 6 : -6)).toFixed(2)}deg`);
        l.style.setProperty('--lo', (0.08 + e * 0.92).toFixed(3));
      });
    }

    const mq = getMq();
    if (mq) {
      const speed = 1 + Math.min(Math.abs(vel) / 6, 4);
      mq.playbackRate = vel < -1 ? -speed : speed;
    }
  }
  const onScroll = () => { if (!frame) frame = requestAnimationFrame(update); };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll, { passive: true });
  // Ease marquee speed back to normal after scrolling stops.
  setInterval(() => { if (Math.abs(vel) > 0.05) { vel *= 0.85; onScroll(); } }, 80);
  update();

  /* Pointer: orbit parallax and magnetic buttons. */
  if (finePointer.matches && !reduced.matches) {
    const orbit = $$('.dx-orbit li');
    hero?.addEventListener('pointermove', e => {
      const x = e.clientX / innerWidth - 0.5;
      const yy = e.clientY / innerHeight - 0.5;
      orbit.forEach((li, i) => {
        const d = 14 + (i % 3) * 10;
        li.style.setProperty('--px', (x * d).toFixed(1));
        li.style.setProperty('--py', (yy * d).toFixed(1));
      });
    });
    $$('.dx-magnet').forEach(btn => {
      btn.addEventListener('pointermove', e => {
        const r = btn.getBoundingClientRect();
        const mx = (e.clientX - r.left - r.width / 2) * 0.18;
        const my = (e.clientY - r.top - r.height / 2) * 0.28;
        btn.style.transform = `translate(${mx.toFixed(1)}px, ${my.toFixed(1)}px)`;
      });
      btn.addEventListener('pointerleave', () => { btn.style.transform = ''; });
    });
    $$('.dx-sys-visual').forEach(v => {
      v.addEventListener('pointermove', e => {
        const r = v.getBoundingClientRect();
        v.style.setProperty('--tilt-y', `${(((e.clientX - r.left) / r.width - 0.5) * 8).toFixed(2)}deg`);
        v.style.setProperty('--tilt-x', `${(-((e.clientY - r.top) / r.height - 0.5) * 6).toFixed(2)}deg`);
      });
      v.addEventListener('pointerleave', () => { v.style.removeProperty('--tilt-y'); v.style.removeProperty('--tilt-x'); });
    });
  }

  reduced.addEventListener?.('change', () => location.reload());
})();
