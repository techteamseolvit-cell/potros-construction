/* Potros Construction v1: scroll choreography, dependency-free. */
(function () {
  'use strict';
  var d = document, w = window, $ = function (s, r) { return (r || d).querySelector(s); }, $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = w.matchMedia && w.matchMedia('(hover:hover) and (pointer:fine)').matches;
  var q = new URLSearchParams(location.search);
  var body = d.body;

  /* progress of a tall section through its sticky pin: 0 at top reaching viewport top, 1 at end */
  function pinProgress(el) {
    var r = el.getBoundingClientRect(), total = el.offsetHeight - w.innerHeight;
    return total > 0 ? clamp(-r.top / total, 0, 1) : 0;
  }

  /* ---------- loader ---------- */
  var hero3d = null, heroEl = $('#hero'), canvas = $('#hero3d');
  function start3D() {
    if (!canvas || !w.PotrosHero) return;
    try {
      hero3d = w.PotrosHero.init(canvas, { static: reduce });
      if (hero3d) { requestAnimationFrame(function () { canvas.classList.add('ready'); }); }
    } catch (e) { if (w.console) console.warn('3D hero unavailable', e); }
  }
  function finishLoad() {
    var l = $('#loader'); if (l) l.classList.add('done');
    body.classList.remove('is-loading'); body.classList.add('ready');
    setTimeout(function () { if (l) l.remove(); }, 1600);
  }
  (function loader() {
    var n = 0, num = $('#loaderNum'), bar = $('#loaderBar');
    if (q.has('noload') || reduce) { start3D(); finishLoad(); return; }
    var t0 = performance.now();
    start3D();
    (function tick() {
      var el = performance.now() - t0, target = d.readyState === 'complete' ? 100 : Math.min(92, el / 14);
      n += (target - n) * .12 + .4; if (n > 100) n = 100;
      num.textContent = Math.round(n); bar.style.width = n + '%';
      if (n >= 100 && el > 1300) { setTimeout(finishLoad, 180); return; }
      requestAnimationFrame(tick);
    })();
  })();

  /* ---------- manifesto: word-by-word scrub ---------- */
  var mf = $('#manifesto'), words = [];
  if (mf) {
    var txt = mf.textContent.trim().split(/\s+/), red = /^(engineer|extraordinary|decades\.?)$/i;
    mf.setAttribute('aria-label', mf.textContent.trim());
    mf.innerHTML = txt.map(function (t) { return '<span class="w' + (red.test(t) ? ' red' : '') + '" aria-hidden="true">' + t + '</span>'; }).join(' ');
    words = $$('.w', mf);
  }

  /* ---------- services horizontal ---------- */
  var svc = $('.services'), track = $('#svcTrack'), svcBar = $('#svcBar'), svcMax = 0;
  function measureSvc() { if (track) svcMax = Math.max(0, track.scrollWidth - w.innerWidth + (parseFloat(getComputedStyle(track).paddingInline) || 0)); }


  /* ---------- isometric drawing generated from real-ish geometry (plan -> wireframe -> finished) ---------- */
  (function buildIso() {
    var svg = $('#iso'); if (!svg) return;
    var S = 27, C = Math.cos(Math.PI / 6), Sn = .5;
    var P = function (x, y, z) { return [(300 + (x - z) * C * S).toFixed(1), (255 + (x + z) * Sn * S - y * S).toFixed(1)]; };
    var pt = function (a) { return a[0] + ' ' + a[1]; };
    var line = function (pts, cls, extra) { return '<path pathLength="1" class="draw ' + (cls || '') + '" ' + (extra || '') + ' d="M' + pts.map(pt).join(' L') + '"/>'; };
    var poly = function (pts, fill, st, sw) { return '<path d="M' + pts.map(pt).join(' L') + ' Z" fill="' + fill + '"' + (st ? ' stroke="' + st + '" stroke-width="' + (sw || 1) + '"' : '') + '/>'; };
    var X0 = -5, X1 = 5, Z0 = -3.6, Z1 = 3.6, H = 3.4, cols = [[-4.4, -3], [0, -3], [4.4, -3], [-4.4, 1.2], [0, 1.2], [4.4, 1.2]];
    var i, k, a = '', b = '', c = '';
    // layer 1: site plan (grid + patio outline + fire pit + kitchen strip)
    for (i = -7; i <= 7; i++) { a += line([P(i, 0, -6), P(i, 0, 6)], 'g'); a += line([P(-7, 0, i), P(7, 0, i)], 'g'); }
    a += line([P(X0, 0, Z0), P(X1, 0, Z0), P(X1, 0, Z1), P(X0, 0, Z1), P(X0, 0, Z0)], 'p');
    a += line([P(-4.6, 0, -3.3), P(4.6, 0, -3.3), P(4.6, 0, -2.2), P(-4.6, 0, -2.2), P(-4.6, 0, -3.3)], 'p');
    var ring = function (r, y) { var o = []; for (k = 0; k <= 36; k++) { o.push(P(Math.cos(k / 36 * 6.2832) * r, y, 2.4 + Math.sin(k / 36 * 6.2832) * r)); } return o; };
    a += line(ring(1.25, 0), 'p') + line(ring(.55, 0), 'p');
    // layer 2: 3D wireframe (columns, beams, rafters, fireplace wall)
    cols.forEach(function (q) { b += line([P(q[0], 0, q[1]), P(q[0], H, q[1])], 'w'); });
    b += line([P(-4.4, H, -3), P(4.4, H, -3), P(4.4, H, 1.2), P(-4.4, H, 1.2), P(-4.4, H, -3)], 'w');
    b += line([P(0, H, -3), P(0, H, 1.2)], 'w');
    for (i = -4.4; i <= 4.41; i += 1.1) b += line([P(i, H + .25, -3.5), P(i, H + .25, 1.7)], 'w2');
    b += line([P(-2.6, 0, -3.5), P(-2.6, 3.2, -3.5), P(2.6, 3.2, -3.5), P(2.6, 0, -3.5)], 'w');
    b += line(ring(1.25, .45), 'w');
    // layer 3: finished build
    c += poly([P(X0, 0, Z0), P(X1, 0, Z0), P(X1, 0, Z1), P(X0, 0, Z1)], 'url(#pav)', 'rgba(244,239,231,.35)');
    c += poly([P(X0, 0, Z1), P(X1, 0, Z1), P(X1, -.5, Z1), P(X0, -.5, Z1)], '#181716');
    c += poly([P(X1, 0, Z0), P(X1, 0, Z1), P(X1, -.5, Z1), P(X1, -.5, Z0)], '#0e0d0d');
    c += poly([P(-2.6, 0, -3.5), P(2.6, 0, -3.5), P(2.6, 3.2, -3.5), P(-2.6, 3.2, -3.5)], '#2b2825', 'rgba(244,239,231,.15)');
    c += poly([P(-1.2, .3, -3.45), P(1.2, .3, -3.45), P(1.2, 1.3, -3.45), P(-1.2, 1.3, -3.45)], '#ff7a3c');
    c += poly(ring(1.45, 0), '#2a2420', '#3b3733', 2);
    c += poly(ring(1.0, .45), '#120d0b');
    c += '<ellipse cx="' + P(0, .6, 2.4)[0] + '" cy="' + P(0, .6, 2.4)[1] + '" rx="150" ry="80" fill="url(#gGlow)" opacity=".22"/>';
    cols.forEach(function (q) {
      var x = q[0], z = q[1], w = .26;
      c += poly([P(x - w, H, z + w), P(x + w, H, z + w), P(x + w, 0, z + w), P(x - w, 0, z + w)], '#3a3632');
      c += poly([P(x + w, H, z + w), P(x + w, H, z - w), P(x + w, 0, z - w), P(x + w, 0, z + w)], '#242220');
    });
    c += poly([P(-4.9, H, -3.4), P(4.9, H, -3.4), P(4.9, H, 1.6), P(-4.9, H, 1.6)], 'rgba(20,18,17,.55)', '#c1121f', 2);
    for (i = -4.4; i <= 4.41; i += 1.1) c += '<path d="M' + pt(P(i, H + .25, -3.5)) + ' L' + pt(P(i, H + .25, 1.7)) + '" stroke="#8a6a4a" stroke-width="3"/>';
    c += '<path class="flame" d="M' + pt(P(0, .5, 2.4)) + ' c-14 -18 -6 -30 0 -48 c6 18 14 30 0 48z" fill="url(#gGlow)"/>';
    svg.innerHTML = '<defs><linearGradient id="gGlow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb066"/><stop offset=".5" stop-color="#ff5a22" stop-opacity=".85"/><stop offset="1" stop-color="#c1121f" stop-opacity="0"/></linearGradient>' +
      '<pattern id="pav" width="20" height="12" patternUnits="userSpaceOnUse"><rect width="20" height="12" fill="#2d2a27"/><path d="M0 0H20M0 6H20M10 0V6M0 6V12M20 6V12" stroke="#3f3b37" stroke-width="1"/></pattern></defs>' +
      '<g class="iso__l iso__l1" fill="none">' + a + '</g><g class="iso__l iso__l2" fill="none">' + b + '</g><g class="iso__l iso__l3">' + c + '</g>';
    svg.setAttribute('class', 'iso s0');
  })();

  /* ---------- process ---------- */
  var proc = $('.process'), steps = $$('.step'), iso = $('#iso'), isoTag = $('#isoTag'), curStep = -1;
  var tags = ['Site plan', '3D virtual design', 'Built & enjoyed'];
  function setStep(i) {
    if (i === curStep) return; curStep = i;
    steps.forEach(function (s, k) { s.classList.toggle('is-active', k === i); });
    if (iso) { iso.setAttribute('class', 'iso s' + i); }
    if (isoTag) isoTag.textContent = tags[i];
  }

  /* ---------- counters ---------- */
  var counters = $$('[data-count]');
  function runCount(el) {
    if (el._done) return; el._done = true;
    var to = +el.getAttribute('data-count'), suf = el.getAttribute('data-suffix') || '', t0 = performance.now(), dur = 2200;
    if (reduce) { el.textContent = to.toLocaleString('en-US') + suf; return; }
    (function f(now) {
      var p = clamp((now - t0) / dur, 0, 1), e = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(to * e).toLocaleString('en-US') + suf;
      if (p < 1) requestAnimationFrame(f);
    })(t0);
  }

  /* ---------- reveals ---------- */
  var revealTargets = $$('.h2,.lede,.anatomy .btn,.spec li,.tile,.area__list,.area__map,.cta__title,.cta__row,.footer__grid>div,.why .eyebrow,.film .eyebrow');
  revealTargets.forEach(function (el, i) { el.classList.add('rv'); el.style.setProperty('--d', (i % 6 * .07) + 's'); });
  var io = 'IntersectionObserver' in w ? new IntersectionObserver(function (en) {
    en.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target; el.classList.add('in');
      if (el.hasAttribute && el.hasAttribute('data-count')) runCount(el);
      if (el.classList.contains('film__frame')) el.classList.add('in');
      if (el.classList.contains('area__map')) el.querySelector('svg').classList.add('m-in');
      io.unobserve(el);
    });
  }, { threshold: .15, rootMargin: '0px 0px -6% 0px' }) : null;
  revealTargets.concat($$('[data-count]'), $$('.film__frame')).forEach(function (el) { if (io) io.observe(el); else { el.classList.add('in'); } });
  if (!io) counters.forEach(runCount);

  /* ---------- service-area map (approx. real lon/lat) ---------- */
  (function map() {
    var svg = $('#mapSvg'); if (!svg) return;
    var P = [['Winchester', -78.163, 39.185, 1], ['Front Royal', -78.194, 38.918], ['Strasburg', -78.36, 38.99], ['Berryville', -77.98, 39.152], ['Stephens City', -78.21, 39.085], ['Middletown', -78.28, 39.027], ['Clear Brook', -78.12, 39.25], ['Martinsburg', -77.964, 39.456], ['Charles Town', -77.86, 39.289], ['Ranson', -77.85, 39.31], ['Leesburg', -77.564, 39.115], ['Ashburn', -77.487, 39.043], ['Sterling', -77.428, 39.006], ['South Riding', -77.51, 38.92], ['Purcellville', -77.713, 39.136], ['Middleburg', -77.74, 38.97], ['Hamilton', -77.665, 39.136], ['Lovettsville', -77.64, 39.27], ['Manassas', -77.475, 38.75]];
    var lo = [-78.42, -77.38], la = [38.7, 39.5], W = 640, H = 520, pad = 60;
    var X = function (v) { return pad + (v - lo[0]) / (lo[1] - lo[0]) * (W - pad * 2); }, Y = function (v) { return H - pad - (v - la[0]) / (la[1] - la[0]) * (H - pad * 2); };
    var OFF = { 'Ranson': [12, -6, 'start'], 'Charles Town': [12, 12, 'start'], 'Purcellville': [-10, 16, 'end'], 'Hamilton': [12, -8, 'start'], 'Sterling': [-12, 14, 'end'] };
    var hq = P[0], hx = X(hq[1]), hy = Y(hq[2]), out = '';
    // faint graticule
    for (var g = 0; g < 8; g++) out += '<line x1="' + (pad + g * (W - pad * 2) / 7) + '" y1="20" x2="' + (pad + g * (W - pad * 2) / 7) + '" y2="' + (H - 20) + '" stroke="rgba(244,239,231,.05)"/>';
    for (g = 0; g < 6; g++) out += '<line x1="20" y1="' + (pad + g * (H - pad * 2) / 5) + '" x2="' + (W - 20) + '" y2="' + (pad + g * (H - pad * 2) / 5) + '" stroke="rgba(244,239,231,.05)"/>';
    P.slice(1).forEach(function (p, i) {
      var x = X(p[1]), y = Y(p[2]), len = Math.hypot(x - hx, y - hy);
      out += '<path class="m-line" style="--len:' + len.toFixed(0) + ';transition-delay:' + (i * .07) + 's" d="M' + hx + ' ' + hy + ' L' + x + ' ' + y + '"/>';
    });
    P.forEach(function (p, i) {
      var x = X(p[1]), y = Y(p[2]), left = x > W - 110, off = OFF[p[0]] || [left ? -12 : 12, 4, left ? 'end' : 'start'];
      out += '<g class="m-node' + (p[3] ? ' m-hq' : '') + '" data-name="' + p[0] + '" tabindex="0">' + (p[3] ? '<circle class="p" cx="' + x + '" cy="' + y + '" r="6"/>' : '') + '<circle class="r" cx="' + x + '" cy="' + y + '" r="9"/><circle class="c" cx="' + x + '" cy="' + y + '" r="' + (p[3] ? 7 : 4) + '"/><text x="' + (x + off[0]) + '" y="' + (y + off[1]) + '" text-anchor="' + off[2] + '">' + p[0] + '</text></g>';
    });
    svg.innerHTML = out;
    var list = $$('.area__list li');
    var hl = function (name, on) { list.forEach(function (li) { if (li.textContent.indexOf(name) === 0) li.classList.toggle('hl', on); }); };
    $$('.m-node', svg).forEach(function (n) {
      n.addEventListener('mouseenter', function () { hl(n.getAttribute('data-name'), true); n.classList.add('hl'); });
      n.addEventListener('mouseleave', function () { hl(n.getAttribute('data-name'), false); n.classList.remove('hl'); });
    });
    list.forEach(function (li) {
      var nm = li.textContent.replace(/, WV/, '');
      li.addEventListener('mouseenter', function () { var n = $('.m-node[data-name="' + nm + '"]', svg); if (n) n.classList.add('hl'); });
      li.addEventListener('mouseleave', function () { $$('.m-node', svg).forEach(function (n) { n.classList.remove('hl'); }); });
    });
  })();

  /* ---------- film facade (YouTube loads on click: no third-party weight until needed) ---------- */
  (function film() {
    var f = $('#filmFrame'); if (!f) return;
    var go = function () {
      if (f.querySelector('iframe')) return;
      var id = f.getAttribute('data-yt'), ifr = d.createElement('iframe');
      ifr.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&modestbranding=1';
      ifr.title = 'Potros Construction video'; ifr.allow = 'autoplay; encrypted-media; picture-in-picture'; ifr.allowFullscreen = true;
      f.appendChild(ifr); $$('.film__thumb,.film__play,.film__cap', f).forEach(function (e) { e.style.display = 'none'; });
    };
    f.addEventListener('click', go);
  })();

  /* ---------- nav + drawer ---------- */
  var nav = $('#nav'), burger = $('#burger'), drawer = $('#drawer'), lastY = 0;
  if (burger) burger.addEventListener('click', function () {
    var o = drawer.classList.toggle('open'); burger.setAttribute('aria-expanded', o); burger.setAttribute('aria-label', o ? 'Close menu' : 'Open menu');
  });
  $$('a', drawer).forEach(function (a) { a.addEventListener('click', function () { drawer.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }); });

  /* ---------- cursor / magnetic / tilt ---------- */
  if (fine && !reduce) {
    var cur = $('#cursor'), lab = $('#cursorLabel'), cx = 0, cy = 0, tx = 0, ty = 0;
    w.addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; cur.classList.add('on'); }, { passive: true });
    (function loop() { cx += (tx - cx) * .22; cy += (ty - cy) * .22; cur.style.transform = 'translate(' + cx + 'px,' + cy + 'px)'; requestAnimationFrame(loop); })();
    $$('[data-cursor]').forEach(function (el) {
      el.addEventListener('mouseenter', function () { lab.textContent = el.getAttribute('data-cursor'); cur.classList.add('big'); });
      el.addEventListener('mouseleave', function () { cur.classList.remove('big'); });
    });
    $$('.magnetic').forEach(function (el) {
      el.addEventListener('mousemove', function (e) { var r = el.getBoundingClientRect(); el.style.setProperty('--bx', ((e.clientX - r.left - r.width / 2) * .25) + 'px'); el.style.setProperty('--by', ((e.clientY - r.top - r.height / 2) * .35) + 'px'); });
      el.addEventListener('mouseleave', function () { el.style.setProperty('--bx', '0px'); el.style.setProperty('--by', '0px'); });
    });
    $$('.card').forEach(function (c) {
      c.addEventListener('mousemove', function (e) { var r = c.getBoundingClientRect(), px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5; c.style.transform = 'perspective(900px) rotateY(' + px * 8 + 'deg) rotateX(' + -py * 8 + 'deg) translateZ(0)'; });
      c.addEventListener('mouseleave', function () { c.style.transform = ''; });
    });
    w.addEventListener('mousemove', function (e) { if (hero3d) hero3d.setPointer(e.clientX / w.innerWidth * 2 - 1, e.clientY / w.innerHeight * 2 - 1); }, { passive: true });
  }

  /* ---------- scroll loop ---------- */
  var heroContent = $('.hero__content'), hudStage = $('#hudStage'), hudBar = $('#hudBar'), prog = $('#progress'), ticking = false;
  var stages = ['01 · Arrival', '02 · The terrace', '03 · The kitchen', '04 · The fire'];
  var lastStage = '';
  function update() {
    ticking = false;
    var y = w.scrollY || d.documentElement.scrollTop, docH = d.documentElement.scrollHeight - w.innerHeight;
    if (prog) prog.style.transform = 'scaleX(' + (docH > 0 ? y / docH : 0) + ')';
    if (nav) { nav.classList.toggle('scrolled', y > 40); nav.classList.toggle('hide', y > lastY && y > w.innerHeight * .9 && !drawer.classList.contains('open')); lastY = y; }

    if (heroEl) {
      var p = pinProgress(heroEl);
      if (hero3d) hero3d.setProgress(p);
      if (heroContent) { var f = clamp(p / .16, 0, 1); heroContent.style.opacity = 1 - f; heroContent.style.transform = 'translateY(' + (-f * 60) + 'px)'; heroContent.style.pointerEvents = f > .9 ? 'none' : ''; }
      if (hudBar) hudBar.style.transform = 'scaleX(' + p + ')';
      var si = Math.min(3, Math.floor(p * 4)), label = stages[si];
      if (hudStage && label !== lastStage) { lastStage = label; hudStage.textContent = label.slice(0, 2); hudStage.nextElementSibling.textContent = label.slice(5); }
    }
    if (words.length && mf) {
      var r = mf.getBoundingClientRect(), pp = clamp((w.innerHeight * .85 - r.top) / (r.height + w.innerHeight * .35), 0, 1), n = Math.round(pp * words.length);
      for (var i = 0; i < words.length; i++) words[i].classList.toggle('lit', i < n);
    }
    if (svc && track) {
      var sp = pinProgress(svc); track.style.transform = 'translate3d(' + (-sp * svcMax) + 'px,0,0)'; if (svcBar) svcBar.style.transform = 'scaleX(' + sp + ')';
    }
    if (proc) { setStep(Math.min(2, Math.floor(pinProgress(proc) * 3 * .999))); }
  }
  var req = function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  w.addEventListener('scroll', req, { passive: true });
  w.addEventListener('resize', function () { measureSvc(); req(); });
  w.addEventListener('load', function () { measureSvc(); req(); });
  measureSvc();
  if (reduce) { $$('.manifesto__text .w').forEach(function (e) { e.classList.add('lit'); }); }
  update();

  /* ---------- debug hooks for screenshots (?y=px or ?p=hero-progress) ---------- */
  if (q.has('y')) { w.addEventListener('load', function () { setTimeout(function () { w.scrollTo(0, +q.get('y')); if (hero3d) hero3d.jump(pinProgress(heroEl)); update(); }, 400); }); }
})();
