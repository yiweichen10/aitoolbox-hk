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
    // 关键修复（2026-08-03）：不再 fallback 到任意语言语音。
    // 用错误语言的语音（如中文语音）朗读英文文本时，多数引擎直接静音或乱读，
    // 表现为"点了朗读没声音"。语言不匹配时应返回 null，由上层提示用户。
    return null;
  }

  // getVoices() 在部分浏览器中是异步填充的（初始为空），
  // 点击朗读前最多等待 2 秒让语音列表就绪，避免误判"无语音"。
  function waitVoices(cb, tries) {
    tries = tries || 0;
    try {
      if (window.speechSynthesis.getVoices().length || tries >= 8) { cb(); return; }
    } catch (e) { cb(); return; }
    setTimeout(function () { waitVoices(cb, tries + 1); }, 250);
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
    // 优先塞进第一个 P 段落开头（与朗读起点对齐，行内不占独立行）；
    // 没有 P 时回退 H3 → H2（兼容无段落工具页），都没有才回退容器顶部独立成行
    var firstP = container.querySelector('p');
    if (firstP) {
      firstP.insertBefore(bar, firstP.firstChild);
    } else {
      var fb = container.querySelector('h3') || container.querySelector('h2');
      if (fb) fb.appendChild(bar);
      else container.insertBefore(bar, container.firstChild);
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
      waitVoices(function () {
        if (!pickVoice(langPrefix)) {
          // 系统缺少页面语言的语音包：明确提示，而不是静音"朗读"一遍
          var msg = isZh
            ? '未检测到 ' + langPrefix + ' 语音。请在系统「设置 → 时间和语言 → 语言和区域」添加对应语言及语音包，然后刷新页面重试。'
            : 'No ' + (langPrefix || 'English') + ' voice is installed on this device. Add the ' + (langPrefix || 'English') + ' language pack in your system settings (Settings → Time & Language → Language & Region), then refresh and try again.';
          playBtn.textContent = isZh ? '🔇 无语音' : '🔇 No voice';
          playBtn.title = msg;
          try { window.alert(msg); } catch (e) {}
          return;
        }
        started = true;
        window.speechSynthesis.cancel();
        playBtn.textContent = L.pause;
        stopBtn.style.display = '';
        speakFrom(0);
      });
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
