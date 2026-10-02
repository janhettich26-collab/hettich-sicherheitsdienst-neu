/* Hettich Sicherheitsdienst — Effekte (GSAP + ScrollTrigger + Lenis, alles lokal) */
(function () {
  'use strict';
  var d = document, w = window, html = d.documentElement;
  var reduce = w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = w.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var hasG = !!(w.gsap && w.ScrollTrigger);
  html.classList.remove('no-js'); html.classList.add('js');
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  if (!location.hash) w.scrollTo(0, 0);

  /* ---------- Loader ---------- */
  var loader = d.querySelector('.loader');
  function animLogo(svg, dur) {
    if (!svg || !hasG || reduce) return;
    var rs = svg.querySelectorAll('rect'), cs = svg.querySelectorAll('circle');
    rs.forEach(function (r) {
      var horiz = +r.getAttribute('width') > +r.getAttribute('height');
      gsap.set(r, { transformOrigin: horiz ? '0% 50%' : '50% 0%', scaleX: horiz ? 0 : 1, scaleY: horiz ? 1 : 0 });
    });
    gsap.set(cs, { transformOrigin: '50% 50%', scale: 0 });
    var tl = gsap.timeline();
    tl.to(rs, { scaleX: 1, scaleY: 1, duration: dur, ease: 'expo.inOut', stagger: dur / 10 })
      .to(cs, { scale: 1, duration: .4, ease: 'back.out(3)', stagger: .06 }, '-=' + dur * .5);
    return tl;
  }
  var firstVisit = true;
  try { firstVisit = !sessionStorage.getItem('hs_seen'); sessionStorage.setItem('hs_seen', '1'); } catch (e) {}
  function intro() {
    if (!loader) return startPage();
    if (!hasG || reduce || !firstVisit) { loader.remove(); return startPage(); }
    var tl = animLogo(loader.querySelector('svg'), .45);
    gsap.to(loader.querySelector('.bar i'), { scaleX: 1, duration: .9, ease: 'power2.inOut' });
    tl.to(loader, { yPercent: -100, duration: .65, ease: 'expo.inOut', onStart: startPage, onComplete: function () { loader.remove(); } }, '-=.15');
  }

  /* ---------- Smooth Scroll ---------- */
  var lenis = null;
  if (w.Lenis && !reduce) {
    lenis = new Lenis({ duration: 1.15, smoothWheel: true, wheelMultiplier: .95 });
    if (hasG) { lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(function (t) { lenis.raf(t * 1000); }); gsap.ticker.lagSmoothing(0); }
    else { (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(0); }
  }
  d.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href'); if (id.length < 2) return;
      var t = d.querySelector(id); if (!t) return;
      e.preventDefault(); html.classList.remove('menu-open');
      if (lenis) lenis.scrollTo(t, { offset: -90 }); else t.scrollIntoView({ behavior: 'smooth' });
    });
  });

  /* ---------- Header, Menü, Fortschritt, FAB ---------- */
  var hdr = d.querySelector('.hdr'), prog = d.querySelector('.progress'), fab = d.querySelector('.fab');
  var lastY = 0;
  function onScroll() {
    var y = w.scrollY || html.scrollTop, max = html.scrollHeight - innerHeight;
    if (hdr) {
      hdr.classList.toggle('solid', y > 30);
      hdr.classList.toggle('hide', y > 400 && y > lastY + 2 && !html.classList.contains('menu-open'));
      if (y < lastY - 2) hdr.classList.remove('hide');
    }
    if (prog) prog.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
    if (fab) fab.classList.toggle('show', y > innerHeight * .7);
    lastY = y;
  }
  w.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  var burger = d.querySelector('.burger');
  if (burger) burger.addEventListener('click', function () {
    html.classList.toggle('menu-open');
    var open = html.classList.contains('menu-open');
    burger.setAttribute('aria-expanded', open);
    if (lenis) open ? lenis.stop() : lenis.start();
  });
  d.querySelectorAll('.nav a').forEach(function (a) { a.addEventListener('click', function () { html.classList.remove('menu-open'); if (lenis) lenis.start(); }); });

  /* ---------- Cursor + Magnet + Spotlight ---------- */
  if (fine && !reduce) {
    var cur = d.createElement('div'); cur.className = 'cursor'; d.body.appendChild(cur);
    var cx = innerWidth / 2, cy = innerHeight / 2, tx = cx, ty = cy;
    w.addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; }, { passive: true });
    (function loop() { cx += (tx - cx) * .2; cy += (ty - cy) * .2; cur.style.transform = 'translate(' + cx + 'px,' + cy + 'px)'; requestAnimationFrame(loop); })();
    d.querySelectorAll('a,button,.svc-item').forEach(function (el) {
      el.addEventListener('mouseenter', function () { cur.classList.add('big'); });
      el.addEventListener('mouseleave', function () { cur.classList.remove('big'); });
    });
    d.querySelectorAll('.btn,.magnet').forEach(function (b) {
      b.addEventListener('mousemove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = 'translate(' + (e.clientX - r.left - r.width / 2) * .22 + 'px,' + (e.clientY - r.top - r.height / 2) * .3 + 'px)';
      });
      b.addEventListener('mouseleave', function () { b.style.transform = ''; });
      b.style.transition = 'transform .5s cubic-bezier(.22,1,.36,1),color .45s,box-shadow .45s,border-color .45s';
    });
  }
  d.querySelectorAll('.card').forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  /* ---------- Leistungen ---------- */
  var items = d.querySelectorAll('.svc-item'), stage = d.querySelectorAll('.svc-stage img'), capNo = d.querySelector('.svc-stage .cap b'), capT = d.querySelector('.svc-stage .cap span');
  function setSvc(i) {
    items.forEach(function (it, k) { it.classList.toggle('on', k === i); var b = it.querySelector('.svc-btn'); if (b) b.setAttribute('aria-expanded', k === i); });
    stage.forEach(function (im, k) { im.classList.toggle('on', k === i); });
    if (capNo) capNo.textContent = '0' + (i + 1);
    if (capT && items[i]) capT.textContent = items[i].querySelector('.svc-btn').textContent;
  }
  items.forEach(function (it, i) {
    it.addEventListener('click', function (e) { if (!e.target.closest('a')) setSvc(i); });
    if (fine) it.addEventListener('mouseenter', function () { setSvc(i); });
  });
  if (items.length) setSvc(0);

  /* ---------- Text zerlegen ---------- */
  function splitWords(el) {
    var out = [];
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var parts = n.textContent.split(/(\s+)/), frag = d.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(d.createTextNode(' ')); return; }
            var o = d.createElement('span'); o.className = 'w';
            var i = d.createElement('span'); i.textContent = p; o.appendChild(i); frag.appendChild(o); out.push(i);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
    })(el);
    return out;
  }

  /* ---------- Seiten-Animationen ---------- */
  function startPage() {
    var heroLogo = d.querySelector('.hero-logo');
    if (heroLogo) animLogo(heroLogo, 1.2);
    if (!hasG || reduce) {
      html.classList.remove('js');
      d.querySelectorAll('[data-count]').forEach(function (el) { el.textContent = el.dataset.count + (el.dataset.suffix || ''); });
      return;
    }
    gsap.registerPlugin(ScrollTrigger);

    d.querySelectorAll('[data-split]').forEach(function (el) {
      var ws = splitWords(el); el.classList.add('split');
      gsap.set(ws, { opacity: 0, y: 26, filter: 'blur(8px)' });
      var inHero = !!el.closest('.hero,.phero');
      gsap.to(ws, { opacity: 1, y: 0, filter: 'blur(0px)', duration: .7, ease: 'power3.out', stagger: .045, delay: 0,
        clearProps: 'filter,transform',
        scrollTrigger: inHero ? null : { trigger: el, start: 'top 88%' } });
    });

    ScrollTrigger.batch('[data-up]', {
      start: 'top 90%',
      onEnter: function (b) { gsap.to(b, { opacity: 1, y: 0, duration: 1.1, ease: 'expo.out', stagger: .1, overwrite: true }); }
    });

    d.querySelectorAll('.reveal-words').forEach(function (el) {
      var ws = splitWords(el);
      ws.forEach(function (s) { s.classList.add('rw'); });
      gsap.to(ws, { opacity: 1, stagger: .05, ease: 'none', scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 45%', scrub: true } });
    });

    d.querySelectorAll('[data-count]').forEach(function (el) {
      var o = { v: 0 }, to = +el.dataset.count, suf = el.dataset.suffix || '';
      el.textContent = '0' + suf;
      gsap.to(o, { v: to, duration: 2.2, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%' },
        onUpdate: function () { el.textContent = Math.round(o.v) + suf; } });
    });

    gsap.utils.toArray('.n i, .card .ln').forEach(function (l) {
      gsap.fromTo(l, { scaleX: 0 }, { scaleX: 1, duration: 1.4, ease: 'expo.out', scrollTrigger: { trigger: l, start: 'top 92%' } });
    });

    gsap.utils.toArray('[data-par]').forEach(function (im) {
      gsap.fromTo(im, { yPercent: -8 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: im.parentNode, start: 'top bottom', end: 'bottom top', scrub: true } });
    });

    gsap.utils.toArray('.frame').forEach(function (f) {
      gsap.fromTo(f, { clipPath: 'inset(8% 6% 8% 6% round 22px)' }, { clipPath: 'inset(0% 0% 0% 0% round 22px)', ease: 'none',
        scrollTrigger: { trigger: f, start: 'top 95%', end: 'top 45%', scrub: true } });
    });

    var vg = d.querySelector('.vgrid');
    if (vg && innerWidth > 820) {
      gsap.utils.toArray('.vgrid .card').forEach(function (c, i) {
        gsap.to(c, { y: (i % 2 ? 40 : 0) - 40 - i * 6, ease: 'none', scrollTrigger: { trigger: vg, start: 'top bottom', end: 'bottom top', scrub: true } });
      });
    }

    var big = d.querySelector('.ftr .big');
    if (big) gsap.fromTo(big, { xPercent: 8 }, { xPercent: -6, ease: 'none', scrollTrigger: { trigger: big, start: 'top bottom', end: 'bottom top', scrub: true } });

    w.addEventListener('load', function () { ScrollTrigger.refresh(); });
    var guardT = 0;
    function guard() {
      clearTimeout(guardT);
      guardT = setTimeout(function () {
        d.querySelectorAll('[data-up], .split .w>span').forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.top < innerHeight && r.bottom > -innerHeight && +getComputedStyle(el).opacity < .05 && !gsap.isTweening(el))
            gsap.to(el, { opacity: 1, y: 0, filter: 'blur(0px)', duration: .6, ease: 'power2.out', clearProps: 'filter' });
        });
      }, 700);
    }
    w.addEventListener('scroll', guard, { passive: true });
    setTimeout(guard, 2500);
  }

  /* ---------- Canvas-Effekte ---------- */
  var DPR = Math.min(w.devicePixelRatio || 1, 1.6);
  var mouse = { x: .5, y: .5 };
  w.addEventListener('pointermove', function (e) { mouse.x = e.clientX / innerWidth; mouse.y = e.clientY / innerHeight; }, { passive: true });

  function lerpC(a, b, t) { return [a[0] + (b[0] - a[0]) * t | 0, a[1] + (b[1] - a[1]) * t | 0, a[2] + (b[2] - a[2]) * t | 0]; }
  var CORAL = [255, 93, 99], DEEP = [150, 18, 42], GOLD = [255, 215, 0];

  var FX = {
    waves: function (ctx, W, H, t) {
      var L = W < 700 ? 22 : 36, seg = W < 700 ? 60 : 110, mx = (mouse.x - .5) * .5;
      ctx.lineCap = 'round'; ctx.lineWidth = W < 700 ? 2 : 2.6;
      ctx.setLineDash([.1, W < 700 ? 6 : 8]); ctx.lineDashOffset = -t * 14;
      for (var i = 0; i < L; i++) {
        var li = i / (L - 1), c = lerpC(CORAL, DEEP, Math.abs(li - .5) * 2), rgb = c[0] + ',' + c[1] + ',' + c[2];
        var a = Math.min(1, .45 + .75 * (1 - Math.abs(li - .5) * 1.5));
        var g = ctx.createLinearGradient(0, 0, W, 0);
        g.addColorStop(0, 'rgba(' + rgb + ',0)'); g.addColorStop(.28, 'rgba(' + rgb + ',' + (a * .6).toFixed(3) + ')');
        g.addColorStop(.72, 'rgba(' + rgb + ',' + a.toFixed(3) + ')'); g.addColorStop(1, 'rgba(' + rgb + ',0)');
        ctx.strokeStyle = g; ctx.beginPath();
        for (var j = 0; j <= seg; j++) {
          var u = j / seg, x = (u * 1.2 - .1) * W;
          var base = H * (.8 - u * .48) + Math.sin(u * 2.6 + t * .32 + mx) * H * .11;
          var spread = (.55 + .45 * Math.sin(u * 3.4 - t * .42 + li * 1.4)) * (.45 + u * 1.3);
          var y = base + (li - .5) * H * .4 * spread + Math.sin(u * 7 + t * .75 + li * 4) * H * .014;
          if (j) ctx.lineTo(x, y); else ctx.moveTo(x, y);
        }
        ctx.stroke();
      }
      ctx.setLineDash([]);
      for (var k = 0; k < 70; k++) {
        var px = ((k * 137.5 + t * 9 * (1 + k % 3)) % (W + 40)) - 20, py = (k * 89.3 % H) + Math.sin(t * .6 + k) * 14;
        ctx.fillStyle = 'rgba(255,215,0,' + (.12 + .4 * Math.abs(Math.sin(t * .8 + k))).toFixed(2) + ')';
        ctx.fillRect(px, py, 1.7, 1.7);
      }
    },
    rings: function (ctx, W, H, t) {
      var cx = W * .5 + (mouse.x - .5) * 30, cy = H * .5 + (mouse.y - .5) * 30, R = Math.min(W, H) * .44, N = 16;
      for (var k = 0; k < N; k++) {
        var kr = k / (N - 1), r = R * (.18 + kr * .82);
        var n = Math.max(24, Math.floor(r * 2 * Math.PI / 7)), c = lerpC(CORAL, DEEP, kr);
        for (var j = 0; j < n; j++) {
          var ang = j / n * Math.PI * 2 + t * (.05 + kr * .05) * (k % 2 ? 1 : -1);
          var rr = r + Math.sin(ang * 3 + t * .7 + k * .45) * R * .06 * (1 - kr * .4) + Math.cos(ang * 2 - t * .4) * R * .03;
          var a = Math.min(1, (.35 + .9 * Math.pow(Math.sin(ang * .5 + t * .3 + k * .2) * .5 + .5, 2)) * (1 - kr * .45));
          ctx.fillStyle = 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a.toFixed(3) + ')';
          ctx.fillRect(cx + Math.cos(ang) * rr, cy + Math.sin(ang) * rr * .92, 2, 2);
        }
      }
      ctx.fillStyle = 'rgba(255,93,99,.9)'; ctx.beginPath(); ctx.arc(cx, cy, 3, 0, 7); ctx.fill();
    },
    globe: (function () {
      var N = 1300, pts = [];
      for (var i = 0; i < N; i++) {
        var y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), th = i * 2.399963;
        pts.push([Math.cos(th) * r, y, Math.sin(th) * r, Math.random()]);
      }
      return function (ctx, W, H, t) {
        var R = Math.min(W, H) * .36, cx = W / 2, cy = H / 2;
        var ry = t * .18 + (mouse.x - .5) * 1.2, rx = .35 + (mouse.y - .5) * .6;
        var cyr = Math.cos(ry), syr = Math.sin(ry), cxr = Math.cos(rx), sxr = Math.sin(rx);
        for (var i = 0; i < N; i++) {
          var p = pts[i], pulse = 1 + Math.max(0, Math.sin(t * 1.4 + p[3] * 40)) * .06 * (p[3] > .85 ? 2.4 : .4);
          var x = p[0] * pulse, y = p[1] * pulse, z = p[2] * pulse;
          var x1 = x * cyr - z * syr, z1 = x * syr + z * cyr;
          var y1 = y * cxr - z1 * sxr, z2 = y * sxr + z1 * cxr;
          var sc = 1.9 / (2.6 - z2), a = (z2 + 1.1) / 2.1;
          var s = (.6 + a * 1.8) * (p[3] > .93 ? 1.6 : 1);
          ctx.fillStyle = 'rgba(255,' + (190 + a * 25 | 0) + ',' + (p[3] > .93 ? 120 : 0) + ',' + (a * a * .95 + .04).toFixed(3) + ')';
          ctx.fillRect(cx + x1 * R * sc, cy + y1 * R * sc, s, s);
        }
      };
    })(),
    columns: function (ctx, W, H, t) {
      var gap = W < 700 ? 10 : 13, cy = H * .55;
      for (var x = 0; x < W; x += gap) {
        var u = x / W, hh = H * .32 * Math.abs(Math.sin(u * 7 + t * .55) * Math.cos(u * 2.3 - t * .3)) * (.4 + .6 * Math.sin(Math.PI * u));
        for (var y = -hh; y <= hh; y += 5) {
          var f = 1 - Math.abs(y) / (hh + 1), gold = (x / gap | 0) % 5 === 0;
          ctx.fillStyle = gold ? 'rgba(255,215,0,' + (f * .7).toFixed(3) + ')' : 'rgba(235,235,240,' + (f * .38).toFixed(3) + ')';
          ctx.fillRect(x, cy + y, 1.4, 1.4);
        }
      }
    }
  };

  d.querySelectorAll('canvas[data-fx]').forEach(function (cv) {
    var fn = FX[cv.dataset.fx]; if (!fn) return;
    var ctx = cv.getContext('2d'), W = 0, H = 0, vis = false, t0 = performance.now(), raf = 0;
    function size() {
      var r = cv.getBoundingClientRect(); W = r.width; H = r.height;
      cv.width = Math.max(1, W * DPR); cv.height = Math.max(1, H * DPR); ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      if (reduce) draw(performance.now());
    }
    function draw(now) {
      ctx.clearRect(0, 0, W, H);
      fn(ctx, W, H, (now - t0) / 1000);
    }
    function loop(now) { if (!vis) { raf = 0; return; } draw(now); raf = requestAnimationFrame(loop); }
    size();
    var ro = w.ResizeObserver ? new ResizeObserver(size) : null; if (ro) ro.observe(cv); else w.addEventListener('resize', size);
    if (reduce) return;
    new IntersectionObserver(function (es) {
      vis = es[0].isIntersecting;
      if (vis && !raf) raf = requestAnimationFrame(loop);
    }, { rootMargin: '100px' }).observe(cv);
  });

  /* ---------- Kontaktformular → E-Mail-Programm (mit Ersatz, falls keins öffnet) ---------- */
  var form = d.querySelector('form[data-mail]');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = new FormData(form), err = form.querySelector('.form-err'), lines = [];
    var mail = (f.get('E-Mail') || '').trim(), msg = (f.get('Nachricht') || '').trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail) || msg.length < 3) {
      err.classList.add('show'); (msg.length < 3 ? form.querySelector('#fm') : form.querySelector('[name="E-Mail"]')).focus(); return;
    }
    err.classList.remove('show');
    ['Vorname', 'Nachname', 'Unternehmen', 'Position', 'Telefon', 'E-Mail'].forEach(function (k) { var v = (f.get(k) || '').trim(); if (v) lines.push(k + ': ' + v); });
    lines.push('', msg);
    var body = lines.join('\n'), fb = form.querySelector('.form-fallback');
    fb.querySelector('textarea').value = 'An: info@hettich-sicherheitsdienst.de\nBetreff: Anfrage über die Website\n\n' + body;
    location.href = 'mailto:info@hettich-sicherheitsdienst.de?subject=' + encodeURIComponent('Anfrage über die Website') + '&body=' + encodeURIComponent(body);
    setTimeout(function () { fb.classList.add('show'); }, 900);
  });
  var cp = d.querySelector('.form-fallback .copy');
  if (cp) cp.addEventListener('click', function () {
    var ta = d.querySelector('.form-fallback textarea'); ta.select();
    var done = function () { cp.firstChild.textContent = 'Kopiert ✓ '; };
    if (navigator.clipboard) navigator.clipboard.writeText(ta.value).then(done, function () { d.execCommand('copy'); done(); });
    else { d.execCommand('copy'); done(); }
  });

  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', intro); else intro();
})();
