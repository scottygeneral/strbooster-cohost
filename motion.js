// Scroll motion: elements with data-reveal get .is-in when they enter the screen.
// Without JS, or with reduced motion, everything simply shows.
(function () {
  var root = document.documentElement;
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  root.classList.add('has-motion');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.18, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('[data-reveal], .bx-section .bx-card.bx-panel, .bx-section .bx-tab, .bx-routes > a').forEach(function (el) { io.observe(el); });
})();
