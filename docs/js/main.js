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
  var hv = $('#heroVideo');
  function heroMedia() {
    if (!hv) { start3D(); return; }
    if (reduce) return;                       // poster only
    var fallback = function () { start3D(); };
    hv.addEventListener('error', fallback, true);
    var p = hv.play();
    if (p && p.then) p.then(function () { heroEl.classList.add('has-video'); }).catch(fallback);
  }
  function finishLoad() {
    var l = $('#loader'); if (l) l.classList.add('done');
    body.classList.remove('is-loading'); body.classList.add('ready');
    setTimeout(function () { if (l) l.remove(); }, 1600);
  }
  (function loader() {
    var n = 0, num = $('#loaderNum'), bar = $('#loaderBar');
    if (q.has('noload') || reduce) { heroMedia(); finishLoad(); return; }
    var t0 = performance.now();
    heroMedia();
    (function tick() {
      var el = performance.now() - t0, target = d.readyState === 'complete' ? 100 : Math.min(92, el / 14);
      n += (target - n) * .12 + .4; if (n > 100) n = 100;
      num.textContent = Math.round(n); bar.style.width = n + '%';
      if (n >= 100 && el > 1300) { setTimeout(finishLoad, 180); return; }
      requestAnimationFrame(tick);
    })();
  })();

  /* ---------- manifesto: word-by-word scrub ---------- */
  var mf = $('#manifesto'), words = [], horseArt = $('.manifesto__art');
  if (mf) {
    var txt = mf.textContent.trim().split(/\s+/), red = /^(engineer|extraordinary|decades\.?)$/i;
    mf.setAttribute('aria-label', mf.textContent.trim());
    mf.innerHTML = txt.map(function (t) { return '<span class="w' + (red.test(t) ? ' red' : '') + '" aria-hidden="true">' + t + '</span>'; }).join(' ');
    words = $$('.w', mf);
  }

  /* ---------- services horizontal ---------- */
  var svc = $('.services'), track = $('#svcTrack'), svcBar = $('#svcBar'), svcMax = 0;
  function measureSvc() { if (track) svcMax = Math.max(0, track.scrollWidth - w.innerWidth + (parseFloat(getComputedStyle(track).paddingInline) || 0)); }


  /* ---------- reveals ---------- */
  var revealTargets = $$('.pstep,.about__copy>*,.about__video,.h2,.lede,.wrow,.area__list,.area__map,.cta__title,.cta__row,.footer__grid>div,.why .eyebrow,.why__photo,.work__head>*');
  revealTargets.forEach(function (el, i) { el.classList.add('rv'); el.style.setProperty('--d', (i % 6 * .07) + 's'); });
  var io = 'IntersectionObserver' in w ? new IntersectionObserver(function (en) {
    en.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target; el.classList.add('in');
      if (el.classList.contains('area__map')) el.querySelector('svg').classList.add('m-in');
      io.unobserve(el);
    });
  }, { threshold: .15, rootMargin: '0px 0px -6% 0px' }) : null;
  revealTargets.concat($$('.work__item')).forEach(function (el) { if (io) io.observe(el); else { el.classList.add('in'); } });

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


  /* ---------- work gallery: parallax, empty-state, lightbox ---------- */
  var workItems = $$('.work__item'), lb = $('#lb'), lbImg = $('#lbImg'), lbIdx = 0;
  workItems.forEach(function (it, i) {
    var im = $('img', it);
    var miss = function () { it.classList.add('empty'); };
    if (im.complete && im.naturalWidth === 0 && im.getAttribute('src')) { /* may still be loading (lazy) */ }
    im.addEventListener('error', miss);
    it.addEventListener('click', function () { if (!it.classList.contains('empty')) openLb(i); });
  });
  function openLb(i) {
    var avail = workItems.filter(function (x) { return !x.classList.contains('empty'); });
    var it = workItems[i]; lbIdx = avail.indexOf(it); if (lbIdx < 0) return;
    lbImg.src = $('img', it).currentSrc || $('img', it).src; lbImg.alt = $('img', it).alt;
    lb.hidden = false; requestAnimationFrame(function () { lb.classList.add('on'); }); body.style.overflow = 'hidden';
  }
  function stepLb(dir) {
    var avail = workItems.filter(function (x) { return !x.classList.contains('empty'); }); if (!avail.length) return;
    lbIdx = (lbIdx + dir + avail.length) % avail.length; var im = $('img', avail[lbIdx]); lbImg.src = im.currentSrc || im.src; lbImg.alt = im.alt;
  }
  function closeLb() { lb.classList.remove('on'); setTimeout(function () { lb.hidden = true; }, 350); body.style.overflow = ''; }
  if (lb) {
    $('#lbX').addEventListener('click', closeLb); $('#lbN').addEventListener('click', function () { stepLb(1); }); $('#lbP').addEventListener('click', function () { stepLb(-1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    d.addEventListener('keydown', function (e) { if (lb.hidden) return; if (e.key === 'Escape') closeLb(); if (e.key === 'ArrowRight') stepLb(1); if (e.key === 'ArrowLeft') stepLb(-1); });
  }



  /* ---------- reveal: scroll-scrubbed video ---------- */
  var revealEl = $('#reveal'), rv = $('#revealVideo'), rvBar = $('#revealBar'), caps = $$('.cap'), rvTarget = 0, rvVisible = false, rvCap = -1;
  if (rv) {
    if (reduce) { rv.loop = true; rv.play().catch(function () {}); }
    else {
      rv.load();
      var lastT = performance.now();
      (function scrub(now) {
        var dt = Math.min(.1, (now - lastT) / 1000 || .016); lastT = now;
        if (rvVisible && rv.readyState >= 2 && rv.duration) {
          var diff = rvTarget - rv.currentTime;
          // time-based easing + speed cap (max 2.4 video-seconds per second), so fast scrolling never makes the video jump
          if (Math.abs(diff) > .025) rv.currentTime = clamp(rv.currentTime + clamp(diff * (1 - Math.exp(-dt * 7)), -2.4 * dt, 2.4 * dt), 0, rv.duration - .05);
        }
        requestAnimationFrame(scrub);
      })(lastT);
    }
  }


  /* ---------- reviews widget (Trustindex): loaded only when near the viewport ---------- */
  (function reviews() {
    var rw = $('#reviewsWidget'); if (!rw) return;
    var load = function () {
      if (rw._l) return; rw._l = true;
      var s = d.createElement('script'); s.src = 'https://cdn.trustindex.io/loader.js?' + rw.getAttribute('data-trustindex'); s.defer = true; s.async = true; rw.appendChild(s);
    };
    if ('IntersectionObserver' in w) { var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { load(); o.disconnect(); } }, { rootMargin: '700px' }); o.observe(rw); } else { load(); }
  })();


  /* ---------- about video: YouTube loads only on click (no third-party weight until needed) ---------- */
  (function aboutVideo() {
    var f = $('#filmFrame'); if (!f) return;
    f.addEventListener('click', function () {
      if (f.querySelector('iframe')) return;
      var ifr = d.createElement('iframe');
      ifr.src = 'https://www.youtube-nocookie.com/embed/' + f.getAttribute('data-yt') + '?autoplay=1&rel=0&modestbranding=1';
      ifr.title = 'Potros Construction video'; ifr.allow = 'autoplay; encrypted-media; picture-in-picture'; ifr.allowFullscreen = true;
      f.appendChild(ifr); $$('.about__thumb,.about__play,.about__cap', f).forEach(function (e) { e.style.display = 'none'; });
    });
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
    w.addEventListener('mousemove', function (e) { if (hero3d) hero3d.setPointer(e.clientX / w.innerWidth * 2 - 1, e.clientY / w.innerHeight * 2 - 1); }, { passive: true });
  }

  /* ---------- scroll loop ---------- */
  var heroContent = $('.hero__content'), hudStage = $('#hudStage'), hudBar = $('#hudBar'), prog = $('#progress'), ticking = false;
  var stages = ['01 · Arrival', '02 · The garden', '03 · The patio', '04 · The kitchen'];
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
      if (horseArt) horseArt.style.setProperty('--horse', clamp((pp - .5) / .18, 0, 1).toFixed(3));
    }
    if (svc && track) {
      var sp = pinProgress(svc); track.style.transform = 'translate3d(' + (-sp * svcMax) + 'px,0,0)'; if (svcBar) svcBar.style.transform = 'scaleX(' + sp + ')';
    }
    for (var wi = 0; wi < workItems.length; wi++) { var wr = workItems[wi].getBoundingClientRect(); if (wr.bottom < -50 || wr.top > w.innerHeight + 50) continue; var wp = (wr.top + wr.height / 2) / w.innerHeight - .5; workItems[wi].querySelector('img').style.setProperty('--py', (-wp * 46 - 30) + 'px'); }
    if (revealEl && rv) {
      var rr = revealEl.getBoundingClientRect(); rvVisible = rr.top < w.innerHeight && rr.bottom > 0;
      var rp = pinProgress(revealEl);
      // hold the first/last frames (reading time), then ease the motion in and out
      var rt = clamp((rp - .08) / .84, 0, 1); rt = .55 * rt + .45 * (rt * rt * (3 - 2 * rt));
      rvTarget = rt * (rv.duration || 21.4) * .985;
      if (rvBar) rvBar.style.transform = 'scaleX(' + rp + ')';
      var ci = Math.min(2, Math.floor(rp * 3)); if (ci !== rvCap) { rvCap = ci; caps.forEach(function (c, k) { c.classList.toggle('on', k === ci); }); }
    }
    if (hv && heroEl.classList.contains('has-video')) { hv.style.transform = 'scale(' + (1 + pinProgress(heroEl) * .14) + ')'; }
  }
  var req = function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  w.addEventListener('scroll', req, { passive: true });
  w.addEventListener('resize', function () { measureSvc(); req(); });
  w.addEventListener('load', function () { measureSvc(); req(); });
  measureSvc();
  if (reduce) { $$('.manifesto__text .w').forEach(function (e) { e.classList.add('lit'); }); if (horseArt) horseArt.style.setProperty('--horse', 1); }
  update();

  /* ---------- debug hooks for screenshots (?y=px or ?p=hero-progress) ---------- */
  if (q.has('y')) { w.addEventListener('load', function () { setTimeout(function () { w.scrollTo(0, +q.get('y')); if (hero3d) hero3d.jump(pinProgress(heroEl)); update(); }, 400); }); }
})();
