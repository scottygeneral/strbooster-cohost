// "How many apps are you paying for?" tally on the home page. Nothing is sent anywhere.
(function () {
  var box = document.getElementById('app-counter');
  if (!box) return;
  var rows = box.querySelectorAll('.ac-row');
  var countEl = box.querySelector('[data-ac="count"]');
  var monthEl = box.querySelector('[data-ac="month"]');
  var yearEl = box.querySelector('[data-ac="year"]');
  var fmt = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  function tally() {
    var count = 0, month = 0;
    rows.forEach(function (row) {
      var on = row.querySelector('input[type="checkbox"]').checked;
      var cost = parseFloat(row.querySelector('input[type="number"]').value) || 0;
      row.classList.toggle('is-on', on);
      if (on) { count += 1; month += Math.max(cost, 0); }
    });
    countEl.textContent = count;
    monthEl.textContent = fmt(month);
    yearEl.textContent = fmt(month * 12);
  }
  box.addEventListener('input', tally);
  box.addEventListener('change', function () {
    tally();
    if (window.gtag) window.gtag('event', 'app_counter_used', { apps: Number(countEl.textContent) });
  });
  tally();
})();
