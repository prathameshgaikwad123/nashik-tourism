/*
 * nashiktourism.com — global search.
 *
 * Loaded on demand (first time the search control is used), never on page load.
 * Searches /search-index.json, which tools/build-search-index.py generates from
 * the same data that builds the pages: destinations, guides, verified updates,
 * events, answers (FAQs and facts) and hub sections. Nothing here invents a
 * result.
 *
 * Behaviour that matters on a phone:
 *   - every word must match somewhere (AND), so "Kumbh parking" finds the
 *     parking section rather than every page that mentions Kumbh
 *   - words are expanded with synonyms (timing -> hours, darshan, open; reach ->
 *     transport, route, train, bus ...), and tolerate one typo on longer words
 *   - rarer words weigh more than common ones ("Trimbakeshwar" outranks
 *     "Nashik" in "Nashik to Trimbakeshwar")
 *   - results are built with DOM calls and textContent, never innerHTML
 *
 * Privacy: the query is sent to analytics (if analytics is on the page) only as
 * a search term, trimmed, and not at all if it looks like an email address or a
 * long number. Nothing else about the visitor is attached to it.
 */
(function () {
  'use strict';

  var STOP = { a: 1, an: 1, the: 1, in: 1, to: 1, of: 1, for: 1, from: 1, and: 1, or: 1, near: 1, at: 1, on: 1, is: 1, are: 1, do: 1, i: 1, how: 1, what: 1, where: 1, when: 1, can: 1, me: 1, my: 1 };

  // Each group is one idea in several words. A query word matches any member.
  var GROUPS = [
    ['timing', 'timings', 'time', 'times', 'hours', 'open', 'opening', 'closing', 'darshan', 'schedule'],
    ['price', 'prices', 'fee', 'fees', 'cost', 'costs', 'ticket', 'tickets', 'entry', 'fare', 'fares', 'budget', 'charges'],
    ['reach', 'reaching', 'transport', 'route', 'routes', 'travel', 'getting', 'directions', 'distance', 'how-to-reach'],
    ['train', 'trains', 'railway', 'rail', 'station', 'irctc'],
    ['bus', 'buses', 'msrtc', 'st'],
    ['flight', 'flights', 'airport', 'air', 'ozar', 'plane'],
    ['road', 'roads', 'drive', 'driving', 'highway', 'traffic', 'diversion'],
    ['parking', 'park', 'vehicle', 'vehicles'],
    ['stay', 'hotel', 'hotels', 'accommodation', 'lodging', 'dharamshala', 'room', 'rooms'],
    ['kumbh', 'simhastha', 'mela', 'kumbha'],
    ['snan', 'bath', 'bathing', 'dip', 'amrit', 'shahi'],
    ['date', 'dates', 'calendar', 'when', 'schedule'],
    ['pass', 'passes', 'epass', 'e-pass', 'registration', 'register', 'permit'],
    ['wheelchair', 'accessible', 'accessibility', 'disabled', 'disability', 'stepfree', 'ramp'],
    ['senior', 'seniors', 'elderly', 'older', 'old'],
    ['safe', 'safety', 'emergency', 'medical', 'hospital', 'police', 'help'],
    ['wine', 'winery', 'vineyard', 'vineyards', 'tasting', 'sula'],
    ['temple', 'temples', 'jyotirlinga', 'mandir', 'shiva'],
    ['event', 'events', 'festival', 'festivals', 'programme', 'program', 'whats-on'],
    ['update', 'updates', 'news', 'latest', 'notice', 'notices', 'advisory'],
    ['weather', 'rain', 'monsoon', 'temperature', 'forecast', 'climate'],
    ['food', 'eat', 'eating', 'restaurant', 'restaurants']
  ];
  var SYN = {};
  GROUPS.forEach(function (g) {
    g.forEach(function (w) { (SYN[w] = SYN[w] || []).push(g); });
  });

  var TYPE_LABEL = { destination: 'Destinations', guide: 'Guides', update: 'Updates', event: 'Events', answer: 'Answers', page: 'Pages' };
  var TYPE_ORDER = ['answer', 'destination', 'update', 'event', 'guide', 'page'];
  var TYPE_BOOST = { destination: 1.25, answer: 1.15, update: 1.1, event: 1.05, guide: 1, page: 0.95 };

  var state = { docs: null, df: null, loading: null };

  function norm(s) {
    var t = String(s || '').toLowerCase();
    if (t.normalize) t = t.normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
    return t.replace(/[^a-z0-9\s-]/g, ' ').replace(/\s+/g, ' ').trim();
  }
  function words(s) { var n = norm(s); return n ? n.split(' ') : []; }

  function prep(json) {
    var df = {};
    var docs = json.docs.map(function (d) {
      var tw = words(d.t), kw = words(d.x), sw = words(d.s);
      var seen = {};
      tw.concat(kw, sw).forEach(function (w) { if (!seen[w]) { seen[w] = 1; df[w] = (df[w] || 0) + 1; } });
      return { d: d, tw: tw, kw: kw, sw: sw, all: seen };
    });
    state.df = df; state.n = docs.length;
    return docs;
  }

  function load() {
    if (state.docs) return Promise.resolve(state.docs);
    if (state.loading) return state.loading;
    state.loading = fetch('/search-index.json', { credentials: 'same-origin' })
      .then(function (r) { if (!r.ok) throw new Error('index'); return r.json(); })
      .then(function (j) { state.docs = prep(j); state.built = j.built; return state.docs; })
      .catch(function (e) { state.loading = null; throw e; });
    return state.loading;
  }

  // One edit apart (substitute / insert / delete), for words of 5+ letters.
  function near(a, b) {
    if (a === b) return true;
    if (Math.abs(a.length - b.length) > 1 || a.length < 5) return false;
    var i = 0, j = 0, edits = 0;
    while (i < a.length && j < b.length) {
      if (a[i] === b[j]) { i++; j++; continue; }
      if (++edits > 1) return false;
      if (a.length > b.length) i++; else if (a.length < b.length) j++; else { i++; j++; }
    }
    return edits + (a.length - i) + (b.length - j) <= 1;
  }

  function fieldScore(list, alts) {
    // Exact word 3, word prefix 2.2, fuzzy 1. Best match wins.
    var best = 0;
    for (var i = 0; i < list.length; i++) {
      var w = list[i];
      for (var k = 0; k < alts.length; k++) {
        var q = alts[k];
        if (w === q) return 3;
        if (best < 2.2 && q.length >= 3 && w.indexOf(q) === 0) best = 2.2;
        else if (best < 1 && q.length >= 5 && near(w, q)) best = 1;
      }
    }
    return best;
  }

  function expand(w) {
    var out = [w];
    (SYN[w] || []).forEach(function (g) { g.forEach(function (x) { if (out.indexOf(x) < 0) out.push(x); }); });
    return out;
  }

  function search(query, opts) {
    opts = opts || {};
    var qw = words(query).filter(function (w) { return !STOP[w]; });
    if (!qw.length) qw = words(query);
    if (!qw.length || !state.docs) return [];
    var groups = qw.map(expand);
    var results = [];
    state.docs.forEach(function (e) {
      var total = 0, ok = true;
      for (var g = 0; g < groups.length; g++) {
        var alts = groups[g];
        var s = Math.max(fieldScore(e.tw, alts) * 3, fieldScore(e.kw, alts) * 2, fieldScore(e.sw, alts));
        if (s === 0) { ok = false; break; }
        var idf = Math.log(1 + state.n / (1 + (state.df[qw[g]] || 0)));
        total += s * (0.5 + idf);
      }
      if (!ok) return;
      // A short, exact title is a better answer than a long one that happens to
      // contain the same words.
      var lenFactor = 1 / (1 + 0.05 * Math.max(0, e.tw.length - 4));
      var w = (e.d.w || 1) * (TYPE_BOOST[e.d.k] || 1) * lenFactor;
      results.push({ doc: e.d, score: total * w });
    });
    results.sort(function (a, b) { return b.score - a.score; });
    // Several records can point at the same place (a fact and its section);
    // show each destination once, at its best rank.
    var seen = {};
    results = results.filter(function (r) { if (seen[r.doc.u]) return false; seen[r.doc.u] = 1; return true; });
    return results.slice(0, opts.limit || 40);
  }

  function groupResults(results, perGroup) {
    var by = {}, seen = [];
    results.forEach(function (r) {
      if (!by[r.doc.k]) { by[r.doc.k] = []; seen.push(r.doc.k); }
      by[r.doc.k].push(r);
    });
    // Groups appear in the order of their best match, so the strongest hit is
    // always first on screen; TYPE_ORDER only places groups never seen.
    return seen.concat(TYPE_ORDER.filter(function (k) { return !by[k]; })).filter(function (k) { return by[k]; }).map(function (k) {
      return { type: k, label: TYPE_LABEL[k], items: perGroup ? by[k].slice(0, perGroup) : by[k], total: by[k].length };
    });
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  // Build the result list into `container`. Returns the number of results.
  function render(container, query, opts) {
    opts = opts || {};
    container.textContent = '';
    var results = search(query, { limit: opts.limit || 40 });
    var groups = groupResults(results, opts.perGroup);
    if (!groups.length) {
      var empty = el('div', 'sd-empty');
      empty.appendChild(el('p', null, 'Nothing found for “' + query + '”.'));
      var p = el('p');
      p.appendChild(document.createTextNode('Try a place name, such as '));
      [['Ramkund', 'Ramkund'], ['Trimbakeshwar', 'Trimbakeshwar'], ['Sula', 'Sula Vineyards']].forEach(function (x, i) {
        if (i) p.appendChild(document.createTextNode(i === 2 ? ' or ' : ', '));
        var a = el('a', null, x[1]); a.href = '/search/?q=' + encodeURIComponent(x[0]); p.appendChild(a);
      });
      p.appendChild(document.createTextNode(', or browse '));
      var b = el('a', null, 'everything on the site'); b.href = '/search/#browse'; p.appendChild(b);
      p.appendChild(document.createTextNode('.'));
      empty.appendChild(p);
      container.appendChild(empty);
      return 0;
    }
    groups.forEach(function (g) {
      container.appendChild(el('h3', 'sd-group', g.label + (opts.perGroup && g.total > g.items.length ? ' (' + g.total + ')' : '')));
      var ul = el('ul', 'sd-results');
      g.items.forEach(function (r) {
        var li = el('li', 'sr-item');
        var a = el('a');
        a.href = r.doc.u;
        a.setAttribute('data-search-result', r.doc.u);
        a.setAttribute('data-search-type', r.doc.k);
        a.appendChild(el('span', 'sr-title', r.doc.t));
        if (r.doc.s) a.appendChild(el('span', 'sr-snip', r.doc.s.length > 150 ? r.doc.s.slice(0, 147).replace(/\s+\S*$/, '') + '…' : r.doc.s));
        if (r.doc.m) a.appendChild(el('span', 'sr-meta', r.doc.m));
        li.appendChild(a); ul.appendChild(li);
      });
      container.appendChild(ul);
    });
    return results.length;
  }

  function trackable(q) {
    q = String(q || '').trim().toLowerCase().slice(0, 60);
    if (q.length < 3) return null;
    if (/@/.test(q) || /\d{6,}/.test(q)) return '[redacted]';
    return q;
  }
  function track(name, params) {
    if (typeof window.gtag === 'function') { try { window.gtag('event', name, params); } catch (e) { /* analytics is optional */ } }
  }

  window.NTSearch = { load: load, search: search, render: render, trackable: trackable, track: track,
    status: function (n, q) { return n ? n + (n === 1 ? ' result' : ' results') + ' for ' + q : 'No results for ' + q; } };
  document.dispatchEvent(new CustomEvent('ntsearch:ready'));
})();
