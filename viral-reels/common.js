// Shared bits for the phone-native reels: easing, the iOS status bar, an iOS-style keyboard and typing schedules.
// Each page sets window.DURATION and window.CUES ({t, type}) for render.cjs and sfx.py.
const $ = id => document.getElementById(id);
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, p) => a + (b - a) * p;
const E = {
  lin: x => x,
  outExpo: x => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
  outCubic: x => 1 - Math.pow(1 - x, 3),
  inOutCubic: x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  outBack: x => { const c1 = 1.7, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
};
const P = (t, t0, d, e = E.outExpo) => e(cl((t - t0) / d));

// deterministic jitter, so every render comes out identical
function rng(seed) { let s = seed; return () => (s = (s * 16807) % 2147483647) / 2147483647; }

function statusBar(el) {
  el.innerHTML = `<span class="sbt">9:41</span><span class="island"></span>
    <svg class="sbi" viewBox="0 0 96 22"><g fill="#000"><rect x="0" y="13" width="5" height="7" rx="1.5"/><rect x="8" y="10" width="5" height="10" rx="1.5"/><rect x="16" y="6" width="5" height="14" rx="1.5"/><rect x="24" y="2" width="5" height="18" rx="1.5"/></g><path d="M38 9a14 14 0 0 1 20 0M41.5 12.5a9 9 0 0 1 13 0M45 16a4 4 0 0 1 6 0" fill="none" stroke="#000" stroke-width="2.6" stroke-linecap="round"/><rect x="64" y="4" width="27" height="14" rx="4" fill="none" stroke="#000" stroke-width="1.8" opacity=".4"/><rect x="66.5" y="6.5" width="17" height="9" rx="2" fill="#000"/><rect x="92.5" y="8.5" width="2.5" height="5" rx="1" fill="#000" opacity=".4"/></svg>`;
}

// iOS light keyboard, 1080 wide. Letter keys get a pop-up balloon when pressed.
const KB_ROWS = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'];
function buildKeyboard(el, suggestions) {
  const keys = {};
  const key = (x, y, w, label, cls = '') => {
    const k = document.createElement('div');
    k.className = 'key ' + cls;
    Object.assign(k.style, { left: x + 'px', top: y + 'px', width: w + 'px' });
    k.innerHTML = label;
    el.appendChild(k);
    return k;
  };
  el.innerHTML = `<div class="sugg">${suggestions.map(s => `<span>${s}</span>`).join('<i></i>')}</div>`;
  KB_ROWS.forEach((row, r) => {
    const x0 = [9, 63, 171][r];
    [...row].forEach((c, i) => (keys[c] = key(x0 + i * 108, 130 + r * 150, 90, c)));
  });
  key(9, 430, 132, '<svg viewBox="0 0 24 24" width="46" height="46"><path d="M12 4l8 8h-4.5v7h-7v-7H4z" fill="none" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/></svg>', 'fn');
  keys['\b'] = key(939, 430, 132, '<svg viewBox="0 0 24 24" width="50" height="50"><path d="M9 6h11v12H9l-6-6z" fill="none" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/><path d="M12.5 9.5l5 5M17.5 9.5l-5 5" stroke="#000" stroke-width="1.6" stroke-linecap="round"/></svg>', 'fn');
  keys['123'] = key(9, 580, 232, '123', 'fn small');
  keys[' '] = key(259, 580, 562, 'space', 'small');
  keys['\n'] = key(839, 580, 232, 'return', 'fn small');
  el.insertAdjacentHTML('beforeend', `
    <svg class="globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="#50555c" stroke-width="1.6"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18" fill="none" stroke="#50555c" stroke-width="1.6"/></svg>
    <svg class="mic" viewBox="0 0 24 24"><rect x="9" y="3" width="6" height="11" rx="3" fill="#50555c"/><path d="M6 11a6 6 0 0 0 12 0M12 17v4" fill="none" stroke="#50555c" stroke-width="1.6" stroke-linecap="round"/></svg>
    <div class="homebar"></div><div class="pop" id="kbPop"></div>`);
  return keys;
}
function drawKeyboard(keys, t, strokes) {
  Object.values(keys).forEach(k => k.classList.remove('down'));
  const pop = $('kbPop');
  pop.style.display = 'none';
  const s = strokes.findLast(s => s.t <= t && t - s.t < 0.11);
  if (!s) return;
  const c = s.ch.toLowerCase(), k = keys[c];
  if (!k) return;
  if (/[a-z]/.test(c)) {
    pop.style.display = 'block';
    pop.style.left = (parseFloat(k.style.left) - 22) + 'px';
    pop.style.top = (parseFloat(k.style.top) - 132) + 'px';
    pop.textContent = s.ch;
  } else k.classList.add('down');
}

// When each character of `text` lands, starting at t0, at roughly `cps` characters a second.
function typeSchedule(text, t0, rand, cps = 18) {
  const strokes = [];
  let t = t0;
  for (const ch of [...text]) {
    strokes.push({ t, ch });
    t += (1 / cps) * (0.55 + 0.9 * rand()) + (ch === ' ' ? 0.025 : 0) + (/[.,?]/.test(ch) ? 0.08 : 0);
  }
  return { strokes, end: t };
}
const typedAt = (sched, t) => sched.strokes.filter(s => s.t <= t).length;
