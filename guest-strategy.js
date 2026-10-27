/* Native GET remains authoritative: no AJAX, iframe, or listing-URL storage. */
(() => {
  'use strict';
  document.querySelectorAll('form[data-guest-strategy]').forEach(form => {
    const input = form.querySelector('input[name="listing"]');
    const error = form.querySelector('.gs-error');
    if (!input || !error) return;
    input.addEventListener('invalid', () => {
      input.setAttribute('aria-invalid', 'true');
      error.textContent = input.validity.valueMissing
        ? 'Paste your Airbnb listing link to get started.'
        : 'Use a complete listing link beginning with https:// or http://.';
      error.hidden = false;
    });
    input.addEventListener('input', () => {
      input.removeAttribute('aria-invalid');
      error.hidden = true;
      error.textContent = '';
    });
    form.addEventListener('submit', () => {
      // A valid handoff is not a generated lead or a completed report.
      // Do not send the listing URL or any entered content to analytics.
      if (typeof window.strBoosterTrack === 'function') {
        window.strBoosterTrack('guest_strategy_submit', {
          form_location: form.dataset.guestStrategy,
          app_name: 'guest_intel'
        });
      }
    });
  });
  // Navigation remains an ordinary same-site anchor without JavaScript.
  // With JS, also focus the URL field for keyboard and mobile visitors.
  const focusListing = () => {
    if (location.hash !== '#guest-strategy') return;
    const field = document.querySelector('#guest-strategy-listing');
    if (field) field.focus({ preventScroll: true });
  };
  window.addEventListener('hashchange', focusListing);
  focusListing();
})();
