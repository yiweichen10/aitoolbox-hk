/*!
 * Tool likes v1 (EN) — ported from the CN site's js/ai-likes.js (2026-11-20).
 * One like per browser (localStorage token); the server additionally dedups
 * by token and caps per-IP daily. Counts render wherever a
 * .tool-like[data-slug] button exists. Failures silently degrade to static UI.
 */
(function () {
  'use strict';
  if (window.__toolLikesLoaded) return;
  window.__toolLikesLoaded = true;

  var TOKEN_KEY = 'tool_like_token_v1';
  var LIKED_KEY = 'tool_liked_slugs_v1';
  var token = '';
  var liked = new Set();

  try {
    token = localStorage.getItem(TOKEN_KEY) || '';
    if (!token) {
      token = 't-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);
      localStorage.setItem(TOKEN_KEY, token);
    }
    liked = new Set(JSON.parse(localStorage.getItem(LIKED_KEY) || '[]'));
  } catch (e) { /* private mode: degrade to IP-only dedup on the server */ }

  function saveLiked() {
    try { localStorage.setItem(LIKED_KEY, JSON.stringify(Array.from(liked))); } catch (e) {}
  }

  function fmt(n) {
    return n >= 10000 ? (Math.round(n / 1000) / 10) + 'k' : String(n);
  }

  var btns = Array.prototype.slice.call(document.querySelectorAll('.tool-like[data-slug]'));
  if (!btns.length) return;

  // Load current counts + mark already-liked state.
  fetch('/api/likes', { headers: { 'Accept': 'application/json' } })
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (!d || !d.ok) return;
      btns.forEach(function (b) {
        var slug = b.getAttribute('data-slug');
        var c = b.querySelector('.tool-like-count');
        if (c && d.likes && d.likes[slug]) c.textContent = fmt(d.likes[slug]);
        if (liked.has(slug)) b.classList.add('liked');
      });
    })
    .catch(function () {});

  function onClick(e) {
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    var b = e.currentTarget;
    if (b.classList.contains('liked')) return; // like-only, no undo (anti-abuse)
    var slug = b.getAttribute('data-slug');
    var c = b.querySelector('.tool-like-count');
    var old = c ? parseInt(c.textContent, 10) : 0;

    b.classList.add('liked'); // optimistic update
    if (c && !isNaN(old)) c.textContent = fmt(old + 1);

    fetch('/api/like', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slug: slug, token: token })
    }).then(function (r) {
      return r.json().catch(function () { return {}; });
    }).then(function (d) {
      if (d && d.ok) {
        if (typeof d.likes === 'number' && c) c.textContent = fmt(d.likes);
        liked.add(slug);
        saveLiked();
      } else {
        b.classList.remove('liked');
        if (c && !isNaN(old)) c.textContent = fmt(old);
      }
    }).catch(function () {
      b.classList.remove('liked');
      if (c && !isNaN(old)) c.textContent = fmt(old);
    });
  }

  btns.forEach(function (b) {
    b.addEventListener('click', onClick);
    b.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') onClick(e);
    });
  });

  // ── Copy-link buttons ([data-copy-link]) — share convenience ──
  function flashCopied(btn) {
    var label = btn.querySelector('[data-copy-label]');
    if (!label) return;
    var old = label.textContent;
    label.textContent = '✓ Copied';
    btn.classList.add('liked');
    setTimeout(function () {
      label.textContent = old;
      btn.classList.remove('liked');
    }, 1600);
  }

  function fallbackCopy(btn, text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); flashCopied(btn); } catch (e) {}
    document.body.removeChild(ta);
  }

  Array.prototype.slice.call(document.querySelectorAll('[data-copy-link]')).forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var url = location.origin + location.pathname;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(
          function () { flashCopied(btn); },
          function () { fallbackCopy(btn, url); }
        );
      } else {
        fallbackCopy(btn, url);
      }
    });
  });
})();
