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

    // The header is solid on every page now, so there is no scroll state to
    // manage. If the sheet is open when the window grows into the desktop bar
    // (rotating a tablet), close it so the page is never left scroll-locked.
    if (hb && mm && window.matchMedia) {
      var wide = window.matchMedia('(min-width: 1200px)');
      var onWide = function () { if (wide.matches && mm.classList.contains('open')) { hb.classList.remove('open'); mm.classList.remove('open'); hb.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; } };
      if (wide.addEventListener) wide.addEventListener('change', onWide); else if (wide.addListener) wide.addListener(onWide);
    }
  })();

  /* ─────────────────────────────────────────────────────────────────────────
     SEARCH — the header control is a real link to /search/ (works without JS);
     here it is upgraded to open a native <dialog>. The index and the matching
     code (/search.js) are fetched only when search is first used.
     ───────────────────────────────────────────────────────────────────────── */
  function loadSearch(cb) {
    if (window.NTSearch) return cb();
    var s = document.createElement('script');
    s.src = '/search.js'; s.async = true; s.onload = cb;
    document.head.appendChild(s);
  }

  (function searchDialog() {
    var dlg = $('#searchDialog');
    var openers = $$('#searchOpen, [data-search-open]');
    if (!dlg || typeof dlg.showModal !== 'function' || !openers.length) return;
    var input = $('#searchInput');
    var body = $('#searchBody');
    var status = $('#searchStatus');
    var idle = body.innerHTML;
    var lastFocus = null, timer = null, tracked = '';

    function run() {
      var q = input.value.trim();
      if (!q) { body.innerHTML = idle; status.textContent = ''; return; }
      if (!window.NTSearch) return;
      NTSearch.load().then(function () {
        if (input.value.trim() !== q) return;            // a newer keystroke won
        var n = NTSearch.render(body, q, { perGroup: 4 });
        status.textContent = NTSearch.status(n, q);
      }).catch(function () {
        body.textContent = '';
        var p = document.createElement('p'); p.className = 'sd-empty';
        p.appendChild(document.createTextNode('Search is unavailable right now. '));
        var a = document.createElement('a'); a.href = '/search/#browse'; a.textContent = 'Browse everything on the site'; p.appendChild(a);
        body.appendChild(p);
      });
      clearTimeout(timer);
      timer = setTimeout(function () {
        var t = NTSearch.trackable(q);
        if (t && t !== tracked) { tracked = t; NTSearch.track('search', { search_term: t }); }
      }, 900);
    }

    function open(trigger, q) {
      lastFocus = trigger || document.activeElement;
      if (!dlg.open) dlg.showModal();
      document.body.classList.add('nt-lock');
      if (q != null) input.value = q;
      input.focus();
      loadSearch(function () { NTSearch.load().then(run, run); });
    }

    openers.forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); open(a); });
    });
    $('#searchClose').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('close', function () {
      document.body.classList.remove('nt-lock');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });  // backdrop
    input.addEventListener('input', run);

    // Arrow keys move through the links; Enter on the field goes to the full
    // results page. No ARIA combobox needed: focus really moves to each link.
    dlg.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
      var links = $$('.sr-item a, .sd-try a', body);
      if (!links.length) return;
      var i = links.indexOf(document.activeElement);
      e.preventDefault();
      if (e.key === 'ArrowDown') (links[i + 1] || links[0]).focus();
      else if (i <= 0) input.focus();
      else links[i - 1].focus();
    });
    body.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('[data-search-result]') : null;
      if (a && window.NTSearch) {
        NTSearch.track('search_result_click', { search_term: NTSearch.trackable(input.value) || '', content_type: a.getAttribute('data-search-type'), item_id: a.getAttribute('data-search-result') });
      }
    });

    // Anything on the site can ask for search with ?search=1 (the 404 page does).
    if (/[?&]open-search=1/.test(location.search)) open(openers[0]);
  })();

  // The /search/ page: same engine, full-page results, query kept in the URL.
  (function searchPage() {
    var form = $('[data-search-page]');
    if (!form) return;
    var input = $('input[name="q"]', form);
    var out = $('#sp-results');
    var status = $('#sp-status');
    var browse = $('#browse');
    var timer = null, tracked = '';
    function run(push) {
      var q = input.value.trim();
      if (history.replaceState) history.replaceState(null, '', q ? '?q=' + encodeURIComponent(q) : location.pathname);
      if (!q) { out.textContent = ''; status.textContent = ''; return; }
      loadSearch(function () {
        NTSearch.load().then(function () {
          if (input.value.trim() !== q) return;
          var n = NTSearch.render(out, q, { limit: 60 });
          status.textContent = NTSearch.status(n, q);
          if (browse && n) browse.open = false;
        }).catch(function () { out.textContent = 'Search is unavailable right now. Browse everything below.'; });
        clearTimeout(timer);
        timer = setTimeout(function () {
          var t = NTSearch.trackable(q);
          if (t && t !== tracked) { tracked = t; NTSearch.track('search', { search_term: t }); }
        }, 900);
      });
    }
    form.addEventListener('submit', function (e) { e.preventDefault(); run(); });
    input.addEventListener('input', function () { run(); });
    out.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('[data-search-result]') : null;
      if (a && window.NTSearch) NTSearch.track('search_result_click', { search_term: NTSearch.trackable(input.value) || '', content_type: a.getAttribute('data-search-type'), item_id: a.getAttribute('data-search-result') });
    });
    var m = /[?&]q=([^&]*)/.exec(location.search);
    if (m) { input.value = decodeURIComponent(m[1].replace(/\+/g, ' ')); run(); }
  })();

  /* ─────────────────────────────────────────────────────────────────────────
     TIME-SENSITIVE CONTENT — a page can be weeks old by the time it is read.
       * an update past its expiry is shown as Archived without a rebuild
       * the Kumbh lifecycle phase is re-evaluated, so "live mode" switches on
         the right day even if the page was built before it
     Both start from correct build-time markup; this only corrects staleness.
     ───────────────────────────────────────────────────────────────────────── */
  (function liveState() {
    var now = Date.now();
    $$('[data-expires]').forEach(function (card) {
      var t = Date.parse(card.getAttribute('data-expires'));
      if (!t || t >= now || card.getAttribute('data-status') === 'archived') return;
      card.setAttribute('data-status', 'archived');
      var badge = $('.st', card);
      if (badge) {
        badge.className = 'st st-update st-archived';
        badge.textContent = '';
        var g = document.createElement('span'); g.className = 'st-i'; g.setAttribute('aria-hidden', 'true'); g.textContent = '▣';
        badge.appendChild(g); badge.appendChild(document.createTextNode('Archived'));
      }
    });

    var cfgEl = document.getElementById('nt-phases');
    if (!cfgEl) return;
    var cfg;
    try { cfg = JSON.parse(cfgEl.textContent); } catch (e) { return; }
    var ist = new Date(now + 5.5 * 3600 * 1000).toISOString().slice(0, 10);
    var current = null;
    if (cfg.forcePhase) current = cfg.phases.filter(function (p) { return p.id === cfg.forcePhase; })[0];
    if (!current) {
      current = cfg.phases.filter(function (p) { return (!p.from || ist >= p.from) && (!p.to || ist <= p.to); })[0];
    }
    if (!current) return;
    document.documentElement.setAttribute('data-phase', current.id);
    $$('[data-phase-id]').forEach(function (n) {
      n.hidden = (' ' + n.getAttribute('data-phase-id') + ' ').indexOf(' ' + current.id + ' ') < 0;
    });
    $$('[data-phase-flag]').forEach(function (n) {
      n.hidden = !current.profile[n.getAttribute('data-phase-flag')];
    });
  })();

  /* ─────────────────────────────────────────────────────────────────────────
     ANALYTICS EVENTS — only if the page already carries Google Analytics
     (window.gtag). No personal data: event names, an item id or path, and the
     link's domain. Nothing is sent if analytics is absent.
     ───────────────────────────────────────────────────────────────────────── */
  (function analytics() {
    function send(name, params) {
      if (typeof window.gtag !== 'function') return;
      try { window.gtag('event', name, params || {}); } catch (e) { /* optional */ }
    }
    document.addEventListener('click', function (ev) {
      var a = ev.target.closest ? ev.target.closest('a[href]') : null;
      if (!a) return;
      var explicit = a.getAttribute('data-track');
      var href = a.getAttribute('href') || '';
      var host = a.hostname;
      if (explicit) {
        send(explicit, { item_id: a.getAttribute('data-track-item') || href, link_domain: host, page_path: location.pathname });
      } else if (/(^|\s)sponsored(\s|$)/.test(a.rel || '')) {
        send('accommodation_click', { link_domain: host, page_path: location.pathname });
      } else if (/^\/discover-nashik\/[a-z-]+\/?(#.*)?$/.test(href)) {
        send('destination_click', { item_id: href.replace(/^\/discover-nashik\/|\/.*$/g, ''), page_path: location.pathname });
      } else if (/^\/plan-your-trip\/#(day-|itineraries)/.test(href) || a.closest('[data-planner] [data-plan]')) {
        send('itinerary_click', { item_id: href, page_path: location.pathname });
      } else if (/^\/events\//.test(href)) {
        send('event_click', { item_id: href, page_path: location.pathname });
      } else if (/^\/updates\//.test(href)) {
        send('update_click', { item_id: href, page_path: location.pathname });
      }
    }, true);

    // Engagement on the sections the site is built around.
    var meta = document.querySelector('meta[name="nt-section"]');
    var section = meta ? meta.getAttribute('content') : (/^\/kumbh-mela-2027\//.test(location.pathname) ? 'kumbh' : '');
    if (section) {
      var visibleMs = 0, last = Date.now(), fired30 = false;
      setInterval(function () {
        var t = Date.now();
        if (!document.hidden) visibleMs += t - last;
        last = t;
        if (!fired30 && visibleMs >= 30000) { fired30 = true; send('section_engaged', { section: section, seconds: 30, page_path: location.pathname }); }
      }, 2000);
      var fired75 = false;
      window.addEventListener('scroll', function () {
        if (fired75) return;
        var h = document.documentElement;
        if ((window.scrollY + window.innerHeight) / h.scrollHeight >= 0.75) { fired75 = true; send('section_scroll_75', { section: section, page_path: location.pathname }); }
      }, { passive: true });
    }
    // Each update is counted once, when at least half of it has been on screen.
    if ('IntersectionObserver' in window) {
      var cards = $$('.update-card');
      if (cards.length) {
        var seen = {};
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting && !seen[en.target.id]) { seen[en.target.id] = 1; send('update_view', { item_id: en.target.id, page_path: location.pathname }); io.unobserve(en.target); }
          });
        }, { threshold: 0.5 });
        cards.forEach(function (c) { io.observe(c); });
      }
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
