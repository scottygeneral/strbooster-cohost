// Free playbook signup: adds the visitor to the STR Booster HighLevel sub-account
// and tags them for the weekly newsletter (STR Booster Brief) and the free kits.
//
// Needs one Netlify environment variable:
//   GHL_PRIVATE_TOKEN  a HighLevel Private Integration token for the STR Booster
//                      sub-account with the contacts.write scope.
// Tags added: str-booster-brief, free-playbook, plus one role-* tag (host, PM, other).
// A HighLevel workflow triggered by the str-booster-brief tag sends the welcome
// email with the kit links.
const LOCATION_ID = 'VYmmcd3zhhauMLyqAUSb';
const API = 'https://services.leadconnectorhq.com';
const ROLES = { host: 'role-host', manager: 'role-property-manager', other: 'role-other' };

const reply = (statusCode, body) => ({
  statusCode,
  headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
  body: JSON.stringify(body),
});
const clean = (value, max) =>
  typeof value === 'string' ? value.replace(/[\u0000-\u001f\u007f]/g, '').trim().slice(0, max) : '';

async function ghl(path, body, token) {
  const r = await fetch(API + path, {
    method: 'POST',
    headers: {
      Authorization: 'Bearer ' + token,
      Version: '2021-07-28',
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(10000),
  });
  if (!r.ok) throw new Error('HighLevel ' + path + ' returned ' + r.status);
  return r.json();
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return reply(405, { ok: false, error: 'Use the signup form.' });
  let d;
  try {
    if (!event.body || event.body.length > 8192) throw Error();
    d = JSON.parse(event.body);
  } catch {
    return reply(400, { ok: false, error: 'Invalid form data.' });
  }
  // Honeypot: real visitors never fill the hidden "company" field.
  if (d && typeof d.company === 'string' && d.company.trim()) return reply(200, { ok: true });

  const email = clean(d && d.email, 254);
  const firstName = clean(d && d.first_name, 80);
  const role = d && Object.prototype.hasOwnProperty.call(ROLES, d.role) ? d.role : 'other';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || d.consent !== true) {
    return reply(400, { ok: false, error: 'Check your email address and the consent box.' });
  }

  const token = process.env.GHL_PRIVATE_TOKEN;
  if (!token) return reply(503, { ok: false, error: 'Signup is not switched on yet.' });

  const incoming = d.attribution && typeof d.attribution === 'object' ? d.attribution : {};
  const utm = ['utm_source', 'utm_medium', 'utm_campaign']
    .map((k) => clean(incoming[k], 80))
    .filter(Boolean)
    .join(' / ');

  try {
    const upsert = await ghl(
      '/contacts/upsert',
      {
        locationId: LOCATION_ID,
        email,
        ...(firstName ? { firstName } : {}),
        source: 'strbooster.com/playbook' + (utm ? ' (' + utm + ')' : ''),
      },
      token,
    );
    const id = upsert && upsert.contact && upsert.contact.id;
    if (!id) throw new Error('No contact id');
    // Add tags without replacing tags the contact already has.
    await ghl('/contacts/' + encodeURIComponent(id) + '/tags', {
      tags: ['str-booster-brief', 'free-playbook', ROLES[role]],
    }, token);
    return reply(200, { ok: true });
  } catch {
    return reply(502, { ok: false, error: 'Signup could not be confirmed.' });
  }
};
