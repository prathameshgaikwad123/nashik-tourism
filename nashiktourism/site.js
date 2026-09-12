/*
 * nashiktourism.com — shared behaviour.
 *
 * One deferred, cached file replaces the ~1.7 KB of navigation JavaScript that
 * used to be pasted into every page, plus the page-specific enhancements added
 * in Phase 3.
 *
 * PRINCIPLES
 *   * Progressive enhancement only. Every feature here enhances markup that is
 *     already complete and readable without JavaScript. Nothing is revealed by
 *     JS, so nothing can be lost when JS fails.
 *   * Filters start in the "everything visible" state and only ever hide in
 *     response to a deliberate user action, so the rendered DOM a crawler sees
 *     still contains all of the content.
 *   * No filter state is written to the URL: filter combinations must never
 *     become indexable duplicates of the page.
 *   * Every block is feature-detected and exits cheaply on pages that do not
 *     use it.
 */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  /* ─────────────────────────────────────────────────────────────────────────
     NAVIGATION — mobile menu, dropdowns, scroll state
     ───────────────────────────────────────────────────────────────────────── */
  (function nav() {
    var hb = $('#hamburger');
    var mm = $('#mobileMenu');
    var bar = $('#mainNav');

    if (hb && mm) {
      var setMenu = function (open) {
        hb.classList.toggle('open', open);
        mm.classList.toggle('open', open);
        hb.setAttribute('aria-expanded', String(open));
        hb.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
        document.body.style.overflow = open ? 'hidden' : '';
      };
      hb.addEventListener('click', function () { setMenu(!mm.classList.contains('open')); });
      $$('a', mm).forEach(function (a) {
        a.addEventListener('click', function () { setMenu(false); });
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && mm.classList.contains('open')) { setMenu(false); hb.focus(); }
      });
    }

    // Dropdowns. CSS already covers hover and :focus-within; these buttons make
    // the submenus operable by keyboard and usable on touch.
    var openDd = null;
    function closeDd() {
      if (!openDd) return;
      openDd.menu.classList.remove('open');
      openDd.btn.setAttribute('aria-expanded', 'false');
      openDd = null;
    }
    $$('.chevron-btn').forEach(function (btn) {
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
      if (e.key === 'Escape' && openDd) { var b = openDd.btn; closeDd(); b.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (openDd && !openDd.menu.contains(e.target) && !openDd.btn.contains(e.target)) closeDd();
    });

    // Only the homepage nav floats over a hero and needs a scrolled state.
    if (bar && !bar.classList.contains('solid')) {
      var onScroll = function () { bar.classList.toggle('scrolled', window.scrollY > 60); };
      window.addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }
  })();

  /* ─────────────────────────────────────────────────────────────────────────
     HERO — settle the slow zoom once the LCP image has decoded
     ───────────────────────────────────────────────────────────────────────── */
  (function hero() {
    var img = $('#heroImg');
    if (!img) return;
    var mark = function () { img.classList.add('loaded'); };
    if (img.complete) mark();
    else img.addEventListener('load', mark, { once: true });
  })();

  /* ─────────────────────────────────────────────────────────────────────────
     SCROLL REVEAL — .fade-up is only hidden while html.js is set, so a failure
     here can never leave content permanently invisible.
     ───────────────────────────────────────────────────────────────────────── */
  (function reveal() {
    var els = $$('.fade-up');
    if (!els.length) return;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('visible'); });
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
    els.forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('visible');
      else io.observe(el);
    });
  })();

  /* ─────────────────────────────────────────────────────────────────────────
     IN-PAGE SECTION NAV — active state for .dest-nav and article TOCs.
     One observer, shared by both patterns.
     ───────────────────────────────────────────────────────────────────────── */
  (function sectionNav() {
    var navs = $$('[data-section-nav]');
    if (!navs.length || !('IntersectionObserver' in window)) return;

    navs.forEach(function (nav) {
      var links = $$('a[href^="#"]', nav);
      if (!links.length) return;
      var byId = {};
      var targets = [];
      links.forEach(function (a) {
        var id = a.getAttribute('href').slice(1);
        var el = document.getElementById(id);
        if (!el) return;
        byId[id] = a;
        targets.push(el);
      });
      if (!targets.length) return;

      var current = null;
      var setCurrent = function (id) {
        if (id === current) return;
        current = id;
        links.forEach(function (a) {
          var on = a === byId[id];
          a.classList.toggle('is-current', on);
          if (on) a.setAttribute('aria-current', 'true');
          else a.removeAttribute('aria-current');
        });
        // Keep the active chip in view on the horizontally scrolling mobile bar.
        var active = byId[id];
        if (active && nav.scrollWidth > nav.clientWidth) {
          var r = active.getBoundingClientRect(), nr = nav.getBoundingClientRect();
          if (r.left < nr.left || r.right > nr.right) {
            nav.scrollTo({ left: active.offsetLeft - 16, behavior: reduceMotion ? 'auto' : 'smooth' });
          }
        }
      };

      var visible = {};
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting; });
        for (var i = 0; i < targets.length; i++) {
          if (visible[targets[i].id]) { setCurrent(targets[i].id); return; }
        }
      }, { rootMargin: '-25% 0px -60% 0px', threshold: 0 });
      targets.forEach(function (t) { io.observe(t); });
    });
  })();

  /* ─────────────────────────────────────────────────────────────────────────
     READING PROGRESS — a single CSS variable driven from one passive listener.
     ───────────────────────────────────────────────────────────────────────── */
  (function progress() {
    var bar = $('[data-reading-progress]');
    var article = $('[data-reading-body]');
    if (!bar || !article) return;
    var ticking = false;
    var update = function () {
      ticking = false;
      var top = article.offsetTop;
      var span = article.offsetHeight - window.innerHeight;
      var pct = span <= 0 ? 1 : (window.scrollY - top) / span;
      pct = Math.max(0, Math.min(1, pct));
      bar.style.setProperty('--progress', (pct * 100).toFixed(1) + '%');
      bar.setAttribute('aria-valuenow', Math.round(pct * 100));
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener('resize', update, { passive: true });
    update();
  })();

  /* ─────────────────────────────────────────────────────────────────────────
     FILTER GROUPS — the destination explorer and the guide index.
     Markup contract:
       <div data-filter-group="dest">
         <div role="group" aria-label="…">
           <button data-filter="all" aria-pressed="true">…</button>
           <button data-filter="spiritual" id="cat-spiritual">…</button>
         </div>
         <div data-filter-items>
           <article data-tags="spiritual heritage">…</article>
         </div>
         <p data-filter-empty hidden>…</p>
         <p data-filter-status role="status" class="sr-only"></p>
       </div>
     Starts unfiltered, so the rendered DOM always contains every item.
     ───────────────────────────────────────────────────────────────────────── */
  (function filters() {
    $$('[data-filter-group]').forEach(function (group) {
      var buttons = $$('[data-filter]', group);
      // A group may have more than one pool — the guide index keeps its
      // featured guide in its own band above the chips, and it has to filter
      // with everything else or a category view shows an off-category card.
      var pools = $$('[data-filter-items]', group);
      if (!buttons.length || !pools.length) return;
      var items = pools.reduce(function (acc, pool) {
        return acc.concat($$('[data-tags]', pool));
      }, []);
      var empty = $('[data-filter-empty]', group);
      var status = $('[data-filter-status]', group);
      var search = $('[data-filter-search]', group);
      var countEl = $('[data-filter-count]', group);

      var active = 'all';
      var query = '';

      function apply() {
        var shown = 0;
        items.forEach(function (item) {
          var tags = ' ' + (item.getAttribute('data-tags') || '') + ' ';
          var matchTag = active === 'all' || tags.indexOf(' ' + active + ' ') > -1;
          var matchText = !query ||
            (item.getAttribute('data-search') || item.textContent).toLowerCase().indexOf(query) > -1;
          var on = matchTag && matchText;
          item.hidden = !on;
          if (on) shown++;
        });
        if (empty) empty.hidden = shown > 0;
        if (countEl) countEl.textContent = shown === items.length
          ? String(items.length)
          : shown + ' of ' + items.length;
        if (status) {
          status.textContent = shown === 1 ? '1 result' : shown + ' results';
        }
      }

      buttons.forEach(function (btn) {
        btn.addEventListener('click', function () {
          active = btn.getAttribute('data-filter');
          buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
          apply();
        });
      });

      if (search) {
        var t = null;
        search.addEventListener('input', function () {
          clearTimeout(t);
          t = setTimeout(function () {
            query = search.value.trim().toLowerCase();
            apply();
          }, 120);
        });
      }

      // A contextual CTA elsewhere on the site can deep-link to one chip by its
      // id (#cat-spiritual). Without JS that simply scrolls to the chip row and
      // leaves every destination on screen, which is the correct fallback.
      var hash = (location.hash || '').slice(1);
      if (hash) {
        var target = buttons.filter(function (b) { return b.id === hash; })[0];
        if (target) target.click();
      }
    });
  })();

  /* ─────────────────────────────────────────────────────────────────────────
     TRIP PLANNER — chooses between itineraries that are already rendered as
     static HTML. It never generates an itinerary, so there is nothing here a
     crawler or a no-JS visitor cannot see.
     ───────────────────────────────────────────────────────────────────────── */
  (function planner() {
    var planner = $('[data-planner]');
    if (!planner) return;
    var days = $$('[data-days]', planner);
    var interests = $$('[data-interest]', planner);
    var plans = $$('[data-plan]');
    if (!days.length || !plans.length) return;

    var status = $('[data-planner-status]');
    var chosenDays = null;
    var chosenInterest = null;

    function pick() {
      if (!chosenDays) return;                       // untouched: show everything
      var want = plans.filter(function (p) {
        return p.getAttribute('data-plan-days') === chosenDays;
      });
      var narrowed = chosenInterest ? want.filter(function (p) {
        return (' ' + p.getAttribute('data-plan-interests') + ' ').indexOf(' ' + chosenInterest + ' ') > -1;
      }) : [];
      var show = narrowed.length ? narrowed : want;
      plans.forEach(function (p) { p.hidden = show.indexOf(p) === -1; });
      if (status && show.length) {
        status.textContent = 'Showing ' + show.length + ' suggested ' +
          (show.length === 1 ? 'itinerary' : 'itineraries') + ' for ' + chosenDays +
          (chosenDays === '1' ? ' day' : ' days') + '.';
      }
    }

    days.forEach(function (btn) {
      btn.addEventListener('click', function () {
        chosenDays = btn.getAttribute('data-days');
        days.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
        pick();
      });
    });
    interests.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var v = btn.getAttribute('data-interest');
        chosenInterest = chosenInterest === v ? null : v;
        interests.forEach(function (b) {
          b.setAttribute('aria-pressed', String(b.getAttribute('data-interest') === chosenInterest));
        });
        pick();
      });
    });

    var hash = (location.hash || '').slice(1);
    if (hash) {
      var preset = days.filter(function (b) { return b.id === hash; })[0];
      if (preset) preset.click();
    }
  })();

  /* ─────────────────────────────────────────────────────────────────────────
     CONTACT FORM — submits to Formspree without leaving the page. Errors are
     announced in a live region rather than an alert().
     ───────────────────────────────────────────────────────────────────────── */
  (function contactForm() {
    var form = $('#contactForm');
    if (!form || !window.fetch) return;
    var success = $('#formSuccess');
    var note = $('#formError');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = $('.submit-btn', form);
      var label = btn ? btn.textContent : '';
      if (btn) { btn.textContent = 'Sending…'; btn.disabled = true; }
      if (note) { note.hidden = true; note.textContent = ''; }

      var fail = function (msg) {
        if (btn) { btn.textContent = label; btn.disabled = false; }
        if (note) { note.textContent = msg; note.hidden = false; note.focus(); }
      };

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' },
      }).then(function (res) {
        if (!res.ok) return fail('Something went wrong sending your message. Please try again, or email us directly.');
        form.hidden = true;
        if (success) { success.hidden = false; success.setAttribute('tabindex', '-1'); success.focus(); }
      }).catch(function () {
        fail('We could not reach the server. Please check your connection and try again.');
      });
    });
  })();
})();
