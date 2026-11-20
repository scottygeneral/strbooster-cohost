/* Floating client-reviews badge.
 * A small pill near the top-right opens the STR Booster review widget
 * (GHL Reputation, location VYmmcd3zhhauMLyqAUSb) in a compact panel.
 * The widget and its resize script load only when the panel is first opened,
 * so the badge adds no third-party requests on page load.
 */
(function () {
  'use strict';
  var WIDGET_URL = 'https://reputationhub.site/reputation/widgets/review_widget/VYmmcd3zhhauMLyqAUSb';
  var RESIZE_SCRIPT = 'https://reputationhub.site/reputation/assets/review-widget.js';
  if (document.querySelector('.sb-reviews-badge')) return;

  function init() {
    var wrap = document.createElement('div');
    wrap.className = 'sb-reviews';

    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'sb-reviews-badge';
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-controls', 'sb-reviews-panel');
    button.innerHTML = '<span class="sb-reviews-stars" aria-hidden="true">★★★★★</span><span>Client reviews</span>';

    var panel = document.createElement('div');
    panel.className = 'sb-reviews-panel';
    panel.id = 'sb-reviews-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'STR Booster client reviews');
    panel.hidden = true;
    panel.innerHTML = '<div class="sb-reviews-head"><strong>What clients say</strong>' +
      '<button type="button" class="sb-reviews-close" aria-label="Close reviews">×</button></div>' +
      '<div class="sb-reviews-body"></div>';

    wrap.appendChild(button);
    wrap.appendChild(panel);
    document.body.appendChild(wrap);

    var loaded = false;
    function load() {
      if (loaded) return;
      loaded = true;
      var frame = document.createElement('iframe');
      frame.className = 'lc_reviews_widget';
      frame.src = WIDGET_URL;
      frame.title = 'STR Booster client reviews';
      frame.loading = 'lazy';
      frame.setAttribute('frameborder', '0');
      frame.setAttribute('scrolling', 'no');
      frame.style.cssText = 'min-width:100%;width:100%;border:0;';
      panel.querySelector('.sb-reviews-body').appendChild(frame);
      var script = document.createElement('script');
      script.src = RESIZE_SCRIPT;
      script.async = true;
      document.body.appendChild(script);
    }

    function setOpen(open) {
      if (open) load();
      panel.hidden = !open;
      button.setAttribute('aria-expanded', String(open));
      if (open) panel.querySelector('.sb-reviews-close').focus();
    }

    button.addEventListener('click', function () { setOpen(panel.hidden); });
    panel.querySelector('.sb-reviews-close').addEventListener('click', function () {
      setOpen(false);
      button.focus();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) { setOpen(false); button.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (!panel.hidden && !wrap.contains(e.target)) setOpen(false);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
