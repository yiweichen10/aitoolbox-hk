/*!
 * Favorites v1 (EN) — ported from the CN site's js/favorites.js (2026-11-21).
 * Pure localStorage: no backend, no accounts. Entry points: the "☆ Save"
 * button on tool detail pages and /favorites (My Favorites, footer link).
 * No floating FAB here — the EN site already has back-to-top + dark toggle.
 */
(function () {
  'use strict';
  if (window.__toolFavoritesLoaded) return;
  window.__toolFavoritesLoaded = true;

  var KEY = 'aitoolbox_en_favorites_v1';
  var HIST_KEY = 'aitoolbox_en_history_v1';

  function getHist() {
    try { return JSON.parse(localStorage.getItem(HIST_KEY) || '[]'); } catch (e) { return []; }
  }
  function recordHistory(slug) {
    if (!slug) return;
    try {
      var h = JSON.parse(localStorage.getItem(HIST_KEY) || '[]');
      h = [slug].concat(h.filter(function (s) { return s !== slug; })).slice(0, 12);
      localStorage.setItem(HIST_KEY, JSON.stringify(h));
    } catch (e) {}
  }

  function getFavs() {
    try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; }
  }
  function setFavs(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {}
  }
  function toggleFav(slug) {
    var list = getFavs();
    var i = list.indexOf(slug);
    if (i >= 0) { list.splice(i, 1); } else { list.push(slug); }
    setFavs(list);
    return list.indexOf(slug) >= 0;
  }
  function isFav(slug) { return getFavs().indexOf(slug) >= 0; }

  function isFavoritesPage() { return !!document.getElementById('favList'); }

  function esc(s) {
    return String(s || '').replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function toolCard(t, removable) {
    var first = (t.n || '?').charAt(0);
    var icon = '<div class="fav-logo" style="background:' + esc(t.c || '#4f46e5') + ';color:#FFFFFF;">' + esc(first) + '</div>';
    var html = '<a class="fav-card" href="/tools/' + esc(t.s) + '/">' + icon +
      '<div class="fav-card-info"><div class="fav-card-name">' + esc(t.n) + '</div>' +
      '<div class="fav-card-meta">' + esc(t.cat) + ' · ' + esc(t.p) + '</div></div>';
    if (removable) {
      html += '<button type="button" class="fav-remove" data-remove="' + esc(t.s) + '" aria-label="Remove ' + esc(t.n) + ' from favorites">Remove</button>';
    }
    html += '</a>';
    return html;
  }

  function renderFavoritesPage() {
    var listEl = document.getElementById('favList');
    if (!listEl) return;
    var slugs = getFavs();
    var tools = window.__ALL_TOOLS_EN__ || [];
    if (!slugs.length) {
      listEl.innerHTML = '<div class="fav-empty">Nothing saved yet. Browse <a href="/category/">all AI tools</a> and tap "☆ Save" on any review.</div>';
      var hw = document.getElementById('historyWrap');
      if (hw) hw.style.display = 'none';
      return;
    }
    var html = '';
    tools.forEach(function (t) {
      if (slugs.indexOf(t.s) >= 0) html += toolCard(t, true);
    });
    listEl.innerHTML = html || '<div class="fav-empty">Saved tools are no longer listed. <a href="/">Back to home →</a></div>';
    listEl.querySelectorAll('[data-remove]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var slug = btn.getAttribute('data-remove');
        var list = getFavs();
        var i = list.indexOf(slug);
        if (i >= 0) { list.splice(i, 1); setFavs(list); }
        renderFavoritesPage();
        bindSlugButtons(); // refresh detail buttons if any
      });
    });
  }

  function renderHistory() {
    var listEl = document.getElementById('historyList');
    var wrap = document.getElementById('historyWrap');
    if (!listEl || !wrap) return;
    var slugs = getHist();
    var tools = window.__ALL_TOOLS_EN__ || [];
    var html = '';
    tools.forEach(function (t) {
      if (slugs.indexOf(t.s) >= 0) html += toolCard(t, false);
    });
    listEl.innerHTML = html;
    wrap.style.display = html ? 'block' : 'none';
  }

  function bindSlugButtons() {
    document.querySelectorAll('[data-fav-slug]').forEach(function (btn) {
      if (btn.dataset.favBound) return;
      btn.dataset.favBound = '1';
      var slug = btn.getAttribute('data-fav-slug');
      var update = function () {
        var on = isFav(slug);
        btn.classList.toggle('liked', on);
        btn.innerHTML = (on ? '&#9733; Saved' : '&#9734; Save');
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
        btn.title = on ? 'Remove from favorites' : 'Save this tool for later';
      };
      update();
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        toggleFav(slug);
        update();
        if (isFavoritesPage()) renderFavoritesPage();
      });
    });
  }

  function initImportExport() {
    var exportBtn = document.getElementById('favExport');
    var copyBtn = document.getElementById('favCopy');
    var importBtn = document.getElementById('favImport');
    var fileInput = document.getElementById('favImportFile');
    if (!exportBtn || !importBtn || !fileInput) return;

    exportBtn.addEventListener('click', function () {
      var data = { site: 'aitoolbox.hk', version: 1, exportedAt: new Date().toISOString(), slugs: getFavs() };
      var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'aitoolbox-favorites.json';
      document.body.appendChild(a);
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    });

    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        var tools = window.__ALL_TOOLS_EN__ || [];
        var slugs = getFavs();
        var names = [];
        tools.forEach(function (t) {
          if (slugs.indexOf(t.s) >= 0) names.push(t.n || t.s);
        });
        var text = names.length ? ('My saved AI tools on AI Tool Lab:\n' + names.join(', ')) : 'My saved list is empty';
        var done = function (ok) {
          copyBtn.textContent = ok ? 'Copied ✓' : 'Copy failed';
          setTimeout(function () { copyBtn.textContent = 'Copy list'; }, 2000);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
        } else { done(false); }
      });
    }

    importBtn.addEventListener('click', function () { fileInput.click(); });
    fileInput.addEventListener('change', function () {
      var file = fileInput.files && fileInput.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function () {
        try {
          var data = JSON.parse(reader.result);
          var slugs = Array.isArray(data) ? data : (data.slugs || []);
          if (!Array.isArray(slugs)) throw new Error('bad format');
          var merged = getFavs();
          slugs.forEach(function (s) {
            if (typeof s === 'string' && s && merged.indexOf(s) < 0) merged.push(s);
          });
          setFavs(merged);
          renderFavoritesPage();
          importBtn.textContent = 'Imported (' + merged.length + ')';
          setTimeout(function () { importBtn.textContent = 'Import'; }, 2000);
        } catch (e) {
          alert('Import failed: not a valid favorites JSON file.');
        }
        fileInput.value = '';
      };
      reader.readAsText(file, 'utf-8');
    });
  }

  function init() {
    var pageSlug = document.querySelector('[data-fav-slug]');
    if (pageSlug) recordHistory(pageSlug.getAttribute('data-fav-slug'));
    bindSlugButtons();
    initImportExport();
    if (isFavoritesPage()) { renderFavoritesPage(); renderHistory(); }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
