/* Service pages: light script (no dependencies). */
(function () {
  'use strict';
  var d = document, w = window, $ = function (s, r) { return (r || d).querySelector(s); }, $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* nav + progress */
  var nav = $('#nav'), burger = $('#burger'), drawer = $('#drawer'), prog = $('#progress'), lastY = 0, tick = false;
  function onScroll() {
    tick = false; var y = w.scrollY || 0, h = d.documentElement.scrollHeight - w.innerHeight;
    if (prog) prog.style.transform = 'scaleX(' + (h > 0 ? y / h : 0) + ')';
    if (nav) { nav.classList.toggle('scrolled', y > 40); nav.classList.toggle('hide', y > lastY && y > 500 && !(drawer && drawer.classList.contains('open'))); lastY = y; }
  }
  w.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(onScroll); } }, { passive: true }); onScroll();
  if (burger && drawer) {
    burger.addEventListener('click', function () { var o = drawer.classList.toggle('open'); burger.setAttribute('aria-expanded', o); burger.setAttribute('aria-label', o ? 'Close menu' : 'Open menu'); });
    $$('a', drawer).forEach(function (a) { a.addEventListener('click', function () { drawer.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }); });
  }

  /* reveal on scroll */
  var rv = $$('.rv');
  if ('IntersectionObserver' in w && !reduce) {
    var io = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { threshold: .12, rootMargin: '0px 0px -6% 0px' });
    rv.forEach(function (el, i) { el.style.setProperty('--d', (i % 4 * .06) + 's'); io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }

  /* gallery lightbox */
  var items = $$('.sp-dip, #spGallery .sp-g'), lb = $('#lb'), lbImg = $('#lbImg'), idx = 0;
  function show(i) { idx = (i + items.length) % items.length; var im = $('img', items[idx]); lbImg.src = im.currentSrc || im.src; lbImg.alt = im.alt; }
  function open(i) { show(i); lb.hidden = false; requestAnimationFrame(function () { lb.classList.add('on'); }); d.body.style.overflow = 'hidden'; }
  function close() { lb.classList.remove('on'); setTimeout(function () { lb.hidden = true; }, 350); d.body.style.overflow = ''; }
  if (lb && items.length) {
    items.forEach(function (it, i) { it.addEventListener('click', function () { open(i); }); });
    $('#lbX').addEventListener('click', close); $('#lbN').addEventListener('click', function () { show(idx + 1); }); $('#lbP').addEventListener('click', function () { show(idx - 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    d.addEventListener('keydown', function (e) { if (lb.hidden) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') show(idx + 1); if (e.key === 'ArrowLeft') show(idx - 1); });
  }

  /* reviews widget (Trustindex), loaded only near the viewport */
  var rw = $('#reviewsWidget');
  if (rw) {
    var load = function () { if (rw._l) return; rw._l = true; var s = d.createElement('script'); s.src = 'https://cdn.trustindex.io/loader.js?' + rw.getAttribute('data-trustindex'); s.defer = true; s.async = true; rw.appendChild(s); };
    if ('IntersectionObserver' in w) { var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { load(); o.disconnect(); } }, { rootMargin: '700px' }); o.observe(rw); } else { load(); }
  }
})();
