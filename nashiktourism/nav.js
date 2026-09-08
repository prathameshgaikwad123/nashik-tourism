/*
 * Shared navigation behaviour for pages that still carry their nav inline.
 *
 * Deliberately additive: pages already bind their own hamburger click handler,
 * so this never binds one itself. It watches the menu's class instead and
 * mirrors the state into ARIA, which keeps a single source of truth and avoids
 * double-toggling.
 *
 * Adds: keyboard/touch-operable dropdowns, Escape to close, ARIA state sync,
 * and a no-JS-safe scroll reveal.
 */
(function () {
  'use strict';

  var hb = document.getElementById('hamburger');
  var mm = document.getElementById('mobileMenu');

  // ── Mirror mobile-menu state into ARIA without owning the click handler.
  if (hb && mm && 'MutationObserver' in window) {
    var sync = function () {
      var open = mm.classList.contains('open');
      hb.setAttribute('aria-expanded', String(open));
      hb.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    new MutationObserver(sync).observe(mm, { attributes: true, attributeFilter: ['class'] });
    sync();
  }

  // ── Dropdowns. CSS covers hover and :focus-within; these buttons make the
  //    submenus reachable by keyboard and usable on touch.
  var openDd = null;
  function closeDd() {
    if (!openDd) return;
    openDd.menu.classList.remove('open');
    openDd.btn.setAttribute('aria-expanded', 'false');
    openDd = null;
  }

  document.querySelectorAll('.chevron-btn').forEach(function (btn) {
    var menu = document.getElementById(btn.getAttribute('aria-controls'));
    if (!menu) return;
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var isOpen = menu.classList.contains('open');
      closeDd();
      if (!isOpen) {
        menu.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
        openDd = { btn: btn, menu: menu };
      }
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    closeDd();
    if (mm && mm.classList.contains('open') && hb) { hb.click(); hb.focus(); }
  });

  document.addEventListener('click', function (e) {
    if (openDd && !openDd.menu.contains(e.target) && !openDd.btn.contains(e.target)) closeDd();
  });

  // ── Scroll reveal. .fade-up is only hidden while html.js is set, so a
  //    failure here can never leave content permanently invisible.
  var reveal = document.querySelectorAll('.fade-up');
  if (!reveal.length) return;
  if (!('IntersectionObserver' in window)) {
    reveal.forEach(function (el) { el.classList.add('visible'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  // Anything at or above the fold — including elements already scrolled past
  // (restored position, or a #hash landing) — is shown straight away.
  reveal.forEach(function (el) {
    if (el.getBoundingClientRect().top < window.innerHeight) {
      el.classList.add('visible');
    } else {
      io.observe(el);
    }
  });
})();
