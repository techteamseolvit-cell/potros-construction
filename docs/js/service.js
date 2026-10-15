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
  /* YouTube facade: the video loads only on click */
  var film = $('#filmFrame');
  if (film) film.addEventListener('click', function () {
    if ($('iframe', film)) return;
    var ifr = d.createElement('iframe');
    ifr.src = 'https://www.youtube-nocookie.com/embed/' + film.getAttribute('data-yt') + '?autoplay=1&rel=0&modestbranding=1';
    ifr.title = 'Potros Construction video'; ifr.allow = 'autoplay; encrypted-media; picture-in-picture'; ifr.allowFullscreen = true;
    film.appendChild(ifr); $$('.about__thumb,.about__play,.about__cap', film).forEach(function (x) { x.style.display = 'none'; });
  });

  /* estimate form: no backend yet, opens the visitor's mail app with the request prefilled */
  var form = $('#estimateForm');
  if (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var f = form.elements, bad = false, note = $('#formNote');
      ['name', 'phone', 'email', 'city', 'message'].forEach(function (k) { var ok = f[k].value.trim() && (k !== 'email' || /^\S+@\S+\.\S+$/.test(f[k].value)); f[k].classList.toggle('is-bad', !ok); if (!ok) bad = true; });
      if (f.company.value) return;
      if (bad) { note.textContent = 'Please complete the highlighted fields.'; return; }
      var body = 'Name: ' + f.name.value + '\nPhone: ' + f.phone.value + '\nEmail: ' + f.email.value + '\nCommunity: ' + f.city.value + '\nService: ' + (f.service.value || 'Not sure yet') + '\n\n' + f.message.value;
      note.textContent = 'Thank you! Your email app is opening with your request. If nothing opens, call us at (540) 514-8725.';
      w.location.href = 'mailto:potrosconstruction@gmail.com?subject=' + encodeURIComponent('Free estimate request – ' + f.name.value) + '&body=' + encodeURIComponent(body);
    });
  }
})();
