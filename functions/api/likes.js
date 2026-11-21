// Tool likes API — Cloudflare Pages Functions (edge, KV-backed).
//   GET  /api/likes  -> { ok: true, likes: { <slug>: <count>, ... } }
//   POST /api/like   -> handled by like.js (separate route file)
// Abuse protection: permanent token dedup + per-IP daily cap.
// Requires a KV namespace bound as LIKES_KV (see wrangler.toml).

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  });
}

export async function onRequestGet(context) {
  const { LIKES_KV } = context.env;
  if (!LIKES_KV) return json({ ok: false, error: 'KV not bound' }, 500);
  // Counts are small; keep all slugs under one key for a single read.
  const raw = await LIKES_KV.get('likes:all');
  let likes = {};
  if (raw) {
    try { likes = JSON.parse(raw); } catch (e) { likes = {}; }
  }
  return json({ ok: true, likes });
}
