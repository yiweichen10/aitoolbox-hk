(function () {
  'use strict';

  var SUPPORT = ('speechSynthesis' in window) && ('SpeechSynthesisUtterance' in window);

  function pickVoice(langPrefix) {
    var voices = window.speechSynthesis.getVoices() || [];
    if (!voices.length) return null;
    if (langPrefix) {
      var lp = langPrefix.toLowerCase();
      var exact = voices.filter(function (v) { return v.lang && v.lang.toLowerCase() === lp; });
      if (exact.length) return exact[0];
      var base = lp.split('-')[0];
      var pref = voices.filter(function (v) { return v.lang && v.lang.toLowerCase().indexOf(base) === 0; });
      if (pref.length) return pref[0];
    }
    var en = voices.filter(function (v) { return v.lang && v.lang.toLowerCase().indexOf('en') === 0; });
    return en.length ? en[0] : voices[0];
  }

  function getBlocks(container) {
    var sel = 'p,li,h2,h3,h4,blockquote,td,pre';
    var nodes = container.querySelectorAll(sel);
    var list = [];
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (n.closest && n.closest('.tts-bar')) continue;
      var text;
      if (n.querySelector && n.querySelector('.tts-bar')) {
        // 标题里嵌了朗读按钮——克隆后移除按钮再取纯文本，避免读出"朗读全文"
        var clone = n.cloneNode(true);
        var barInClone = clone.querySelector('.tts-bar');
        if (barInClone) barInClone.remove();
        text = (clone.textContent || '').replace(/\s+/g, ' ').trim();
      } else {
        text = (n.textContent || '').replace(/\s+/g, ' ').trim();
      }
      if (text.length < 2) continue;
      list.push({ el: n, text: text });
    }
    return list;
  }

  function createBar(container, L) {
    var bar = document.createElement('span');
    bar.className = 'tts-bar';
    var play = document.createElement('button');
    play.type = 'button';
    play.className = 'tts-btn tts-play';
    play.textContent = L.play;
    var stop = document.createElement('button');
    stop.type = 'button';
    stop.className = 'tts-btn tts-stop';
    stop.textContent = L.stop;
    stop.style.display = 'none';
    bar.appendChild(play);
    bar.appendChild(stop);
    // 优先塞进第一个 H2 标题末尾（不占额外空间）；没有 H2 时回退到容器顶部
    var firstH2 = container.querySelector('h2');
    if (firstH2) {
      firstH2.appendChild(bar);
    } else {
      container.insertBefore(bar, container.firstChild);
    }
    return { bar: bar, play: play, stop: stop };
  }

  function initContainer(container) {
    if (container.__ttsReady) return;
    container.__ttsReady = true;

    var langPrefix = document.documentElement.lang || 'en';
    var isZh = /^zh/i.test(langPrefix);
    var L = isZh
      ? { play: '🔊 朗读', pause: '⏸ 暂停', resume: '▶ 继续', stop: '⏹ 停止' }
      : { play: '🔊 Read', pause: '⏸ Pause', resume: '▶ Resume', stop: '⏹ Stop' };

    var ctrl = createBar(container, L);
    var playBtn = ctrl.play, stopBtn = ctrl.stop;
    var blocks = [];
    var idx = -1;
    var current = null;
    var started = false;
    var current_u = null;

    function highlight(el) {
      if (current) current.classList.remove('tts-active');
      current = el;
      if (current && current.scrollIntoView) {
        current.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      if (current) current.classList.add('tts-active');
    }
    function clearHL() {
      if (current) current.classList.remove('tts-active');
      current = null;
    }

    function speakFrom(i) {
      if (!started) return;
      if (i >= blocks.length) { finish(); return; }
      idx = i;
      var b = blocks[i];
      highlight(b.el);
      var u = new SpeechSynthesisUtterance(b.text);
      u.lang = langPrefix;
      var v = pickVoice(langPrefix);
      if (v) u.voice = v;
      u.rate = 1.0;
      u.pitch = 1.0;
      u.onend = function () { if (started) speakFrom(i + 1); };
      u.onerror = function () { if (started) speakFrom(i + 1); };
      current_u = u;
      window.speechSynthesis.speak(u);
    }

    function start() {
      blocks = getBlocks(container);
      if (!blocks.length) return;
      started = true;
      window.speechSynthesis.cancel();
      playBtn.textContent = L.pause;
      stopBtn.style.display = '';
      speakFrom(0);
    }

    function pause() {
      if (window.speechSynthesis.speaking && !window.speechSynthesis.paused) {
        window.speechSynthesis.pause();
        playBtn.textContent = L.resume;
      } else if (window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
        playBtn.textContent = L.pause;
      }
    }

    function finish() {
      started = false;
      window.speechSynthesis.cancel();
      clearHL();
      playBtn.textContent = L.play;
      stopBtn.style.display = 'none';
      idx = -1;
      current_u = null;
    }

    playBtn.addEventListener('click', function () {
      if (!started) { start(); } else { pause(); }
    });
    stopBtn.addEventListener('click', function () { finish(); });
  }

  function init() {
    if (!SUPPORT) return;
    var targets = document.querySelectorAll('[data-tts]');
    for (var i = 0; i < targets.length; i++) {
      initContainer(targets[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
