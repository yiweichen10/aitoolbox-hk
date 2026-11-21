// POST /api/like — single tool like (abuse-protected). See likes.js for the
// shared KV schema and abuse rules; GET /api/likes returns all counts.
const DAILY_IP_CAP = 5;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  });
}

function today() {
  return new Date().toISOString().slice(0, 10).replace(/-/g, '');
}

export async function onRequestPost(context) {
  const { LIKES_KV } = context.env;
  const { request } = context;
  if (!LIKES_KV) return json({ ok: false, error: 'KV not bound' }, 500);

  let body;
  try { body = await request.json(); } catch (e) { return json({ ok: false, error: 'bad json' }, 400); }
  const slug = String(body.slug || '').slice(0, 120);
  const token = String(body.token || '').slice(0, 64);
  if (!/^[a-z0-9-]{1,120}$/i.test(slug)) return json({ ok: false, error: 'bad slug' }, 400);
  if (!token) return json({ ok: false, error: 'missing token' }, 400);

  // 1) One like per browser token, forever.
  const tokKey = `tok:${token}:${slug}`;
  const seen = await LIKES_KV.get(tokKey);
  if (seen) {
    const all = JSON.parse((await LIKES_KV.get('likes:all')) || '{}');
    return json({ ok: true, liked: false, likes: all[slug] || 0 });
  }

  // 2) Per-IP daily cap.
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  const ipKey = `ip:${ip}:${today()}`;
  const ipRaw = await LIKES_KV.get(ipKey);
  let ipSlugs = [];
  if (ipRaw) { try { ipSlugs = JSON.parse(ipRaw); } catch (e) { ipSlugs = []; } }
  if (ipSlugs.length >= DAILY_IP_CAP) {
    return json({ ok: false, error: 'daily limit', msg: 'Come back tomorrow' }, 429);
  }

  // 3) Count + persist (read-modify-write; concurrency is acceptable for v1).
  const raw = (await LIKES_KV.get('likes:all')) || '{}';
  let likes;
  try { likes = JSON.parse(raw); } catch (e) { likes = {}; }
  const newCount = (likes[slug] || 0) + 1;
  likes[slug] = newCount;

  await LIKES_KV.put('likes:all', JSON.stringify(likes));
  await LIKES_KV.put(tokKey, '1');
  ipSlugs.push(slug);
  // IP activity record expires after 24h.
  await LIKES_KV.put(ipKey, JSON.stringify(ipSlugs), { expirationTtl: 86400 });

  return json({ ok: true, liked: true, likes: newCount });
}
