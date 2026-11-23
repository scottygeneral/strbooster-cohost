// Newsletter signup for strbooster.com (home, /playbook, /skills).
//
// The site's own form posts here; this function forwards the signup to a
// HighLevel workflow's Inbound Webhook, so the webhook URL never appears in
// the page source and bots can't post to it directly.
//
// Needs one Netlify environment variable:
//   GHL_SIGNUP_WEBHOOK_URL  the URL from the "Inbound Webhook" trigger of the
//                           HighLevel workflow "Newsletter welcome".
// The workflow maps first_name and email to the contact, adds the tags and
// sends the welcome email.
const TAGS = 'str-booster-brief,free-playbook';

const clean = (value, max) =>
  typeof value === 'string' ? value.replace(/[\u0000-\u001f\u007f]/g, '').trim().slice(0, max) : '';

function parse(event) {
  const raw = event.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString('utf8') : event.body || '';
  if (!raw || raw.length > 8192) return null;
  const type = String((event.headers && (event.headers['content-type'] || event.headers['Content-Type'])) || '');
  if (type.includes('application/json')) {
    try { return JSON.parse(raw); } catch { return null; }
  }
  return Object.fromEntries(new URLSearchParams(raw));
}

exports.handler = async (event) => {
  const wantsJson = String((event.headers && event.headers.accept) || '').includes('application/json');
  const done = (ok, message, back, anchor) => {
    if (wantsJson) {
      return {
        statusCode: ok ? 200 : 400,
        headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
        body: JSON.stringify({ ok, message }),
      };
    }
    // Without JavaScript the browser posted the form: send it back to the page.
    const page = /^\/[\w\-./]*$/.test(back || '') ? back : '/';
    const hash = /^[\w-]{1,60}$/.test(anchor || '') ? '#' + anchor : '';
    return { statusCode: 303, headers: { Location: page + '?signup=' + (ok ? 'ok' : 'error') + hash }, body: '' };
  };

  if (event.httpMethod !== 'POST') return done(false, 'Use the signup form.');
  const d = parse(event);
  if (!d || typeof d !== 'object') return done(false, 'Something went wrong. Please try again.');
  const page = clean(d.page, 120);
  const anchor = clean(d.anchor, 60);
  // Honeypot: people never fill the hidden "company" field.
  if (clean(d.company, 200)) return done(true, 'You’re in.', page, anchor);

  const email = clean(d.email, 254).toLowerCase();
  const firstName = clean(d.first_name, 80);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return done(false, 'Please check your email address.', page, anchor);

  const url = process.env.GHL_SIGNUP_WEBHOOK_URL;
  if (!url) return done(false, 'Signup isn’t switched on yet. Email info@strbooster.com and we’ll add you.', page, anchor);

  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        first_name: firstName,
        email,
        tags: TAGS,
        source: 'strbooster.com' + (page || '/'),
        page: page || '/',
        signed_up_at: new Date().toISOString(),
      }),
      signal: AbortSignal.timeout(10000),
    });
    if (!r.ok) throw new Error('Webhook returned ' + r.status);
  } catch (err) {
    console.error('newsletter-signup failed', err.message);
    return done(false, 'Something went wrong. Please try again, or email info@strbooster.com.', page, anchor);
  }
  return done(true, 'You’re in. Check your inbox for the welcome email.', page, anchor);
};
