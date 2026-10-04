/*
 * nashiktourism.com — live weather for Nashik Now and the homepage strip.
 *
 * Data: Open-Meteo (https://open-meteo.com), a free forecast API that needs no
 * key, so nothing secret ships to the browser. It is model-based, so it is
 * always labelled as such, with its fetch time and a link to the India
 * Meteorological Department for official forecasts and warnings.
 *
 * Failure is a normal case and is handled, never shown raw:
 *   - network error, timeout, non-200, bad JSON, missing or non-numeric fields
 *     all fall back to a plain sentence plus the IMD link
 *   - a good response is cached for 15 minutes in sessionStorage so navigating
 *     around does not hammer the API (rate limits); storage being unavailable
 *     (private mode) is tolerated
 *   - the markup in the page already says what to do without JavaScript
 */
(function () {
  'use strict';
  var targets = document.querySelectorAll('[data-weather]');
  if (!targets.length) return;

  var API = 'https://api.open-meteo.com/v1/forecast?latitude=19.9975&longitude=73.7898' +
    '&current=temperature_2m,apparent_temperature,relative_humidity_2m,precipitation,weather_code,wind_speed_10m' +
    '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max' +
    '&timezone=Asia%2FKolkata&forecast_days=4';
  var CACHE_KEY = 'nt-weather-v1', TTL = 15 * 60 * 1000;

  // WMO weather interpretation codes, as documented by Open-Meteo.
  var WMO = { 0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast', 45: 'Fog', 48: 'Freezing fog',
    51: 'Light drizzle', 53: 'Drizzle', 55: 'Heavy drizzle', 56: 'Freezing drizzle', 57: 'Freezing drizzle',
    61: 'Light rain', 63: 'Rain', 65: 'Heavy rain', 66: 'Freezing rain', 67: 'Freezing rain',
    71: 'Light snow', 73: 'Snow', 75: 'Heavy snow', 77: 'Snow grains', 80: 'Light showers', 81: 'Showers',
    82: 'Heavy showers', 85: 'Snow showers', 86: 'Snow showers', 95: 'Thunderstorm', 96: 'Thunderstorm with hail', 99: 'Thunderstorm with hail' };

  function num(v) { return typeof v === 'number' && isFinite(v) ? v : null; }
  function deg(v) { v = num(v); return v === null ? null : Math.round(v) + '°C'; }
  function desc(code) { return WMO.hasOwnProperty(code) ? WMO[code] : null; }

  function fmtTime(d) {
    try {
      return d.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit', hour12: true }) + ' IST';
    } catch (e) { return d.toISOString(); }
  }

  function readCache() {
    try {
      var raw = sessionStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      var c = JSON.parse(raw);
      return c && Date.now() - c.t < TTL ? c : null;
    } catch (e) { return null; }
  }
  function writeCache(data, t) {
    try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({ t: t, data: data })); } catch (e) { /* storage unavailable */ }
  }

  function parse(json) {
    var c = json && json.current, d = json && json.daily;
    if (!c || !d || !d.time) return null;
    var now = { temp: deg(c.temperature_2m), feels: deg(c.apparent_temperature), text: desc(c.weather_code),
      humidity: num(c.relative_humidity_2m), rain: num(c.precipitation), wind: num(c.wind_speed_10m) };
    if (now.temp === null || now.text === null) return null;
    var days = [];
    for (var i = 0; i < d.time.length && i < 4; i++) {
      var hi = deg(d.temperature_2m_max && d.temperature_2m_max[i]), lo = deg(d.temperature_2m_min && d.temperature_2m_min[i]);
      var t = desc(d.weather_code && d.weather_code[i]);
      if (hi === null || lo === null || t === null) continue;
      var p = num(d.precipitation_probability_max && d.precipitation_probability_max[i]);
      days.push({ date: d.time[i], hi: hi, lo: lo, text: t, pop: p });
    }
    return { now: now, days: days };
  }

  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }

  function dayLabel(iso, i) {
    if (i === 0) return 'Today';
    if (i === 1) return 'Tomorrow';
    try { return new Date(iso + 'T12:00:00+05:30').toLocaleDateString('en-IN', { weekday: 'long', timeZone: 'Asia/Kolkata' }); } catch (e) { return iso; }
  }

  function renderCompact(node, w, t) {
    node.textContent = '';
    node.appendChild(el('p', 'nc-main', w.now.temp + ' \u00B7 ' + w.now.text));
    node.appendChild(el('p', 'nc-sub', w.now.feels !== null ? 'Feels like ' + w.now.feels + '. Model-based data, not an official forecast.' : 'Model-based data, not an official forecast.'));
    node.appendChild(el('p', 'nc-stamp', 'Updated ' + fmtTime(t)));
  }

  function renderFull(node, w, t) {
    node.textContent = '';
    var top = el('div', 'now-card');
    top.appendChild(el('p', 'nc-label', 'Right now in Nashik'));
    top.appendChild(el('p', 'nc-main', w.now.temp + ' · ' + w.now.text));
    var bits = [];
    if (w.now.feels !== null) bits.push('Feels like ' + w.now.feels);
    if (w.now.humidity !== null) bits.push('Humidity ' + Math.round(w.now.humidity) + '%');
    if (w.now.wind !== null) bits.push('Wind ' + Math.round(w.now.wind) + ' km/h');
    if (w.now.rain !== null && w.now.rain > 0) bits.push('Rain ' + w.now.rain + ' mm');
    if (bits.length) top.appendChild(el('p', 'nc-sub', bits.join(' · ')));
    node.appendChild(top);
    var grid = el('div', 'weather-grid');
    grid.style.marginTop = 'var(--s-3)';
    w.days.forEach(function (d, i) {
      var c = el('div', 'wx-day');
      c.appendChild(el('h3', null, dayLabel(d.date, i)));
      c.appendChild(el('p', 'wx-t', d.hi + ' / ' + d.lo));
      c.appendChild(el('p', 'wx-d', d.text + (d.pop !== null ? ' · rain chance up to ' + Math.round(d.pop) + '%' : '')));
      grid.appendChild(c);
    });
    node.appendChild(grid);
    var stamp = el('p', 'nc-stamp');
    stamp.textContent = 'Fetched ' + fmtTime(t) + ' from Open-Meteo. Model-based data, not an official forecast. ';
    var a = el('a', 'nc-link', 'Official forecasts and warnings: IMD');
    a.href = 'https://mausam.imd.gov.in/'; a.rel = 'noopener noreferrer';
    stamp.appendChild(a);
    node.appendChild(stamp);
  }

  function fail(node) {
    node.textContent = '';
    var p = el('p', 'nc-sub', 'Weather is not available right now. ');
    var a = el('a', 'nc-link', 'Check the India Meteorological Department');
    a.href = 'https://mausam.imd.gov.in/'; a.rel = 'noopener noreferrer';
    p.appendChild(a); p.appendChild(document.createTextNode('.'));
    node.appendChild(p);
  }

  function show(w, t) {
    Array.prototype.forEach.call(targets, function (n) {
      n.removeAttribute('aria-busy');
      if (n.getAttribute('data-weather') === 'compact') renderCompact(n, w, t); else renderFull(n, w, t);
    });
  }
  function showFail() { Array.prototype.forEach.call(targets, function (n) { n.removeAttribute('aria-busy'); fail(n); }); }

  var cached = readCache();
  if (cached) { var w0 = parse(cached.data); if (w0) { show(w0, new Date(cached.t)); return; } }
  if (!window.fetch) return showFail();

  Array.prototype.forEach.call(targets, function (n) { n.setAttribute('aria-busy', 'true'); });
  var ctl = window.AbortController ? new AbortController() : null;
  var timer = setTimeout(function () { if (ctl) ctl.abort(); }, 7000);
  fetch(API, ctl ? { signal: ctl.signal } : {})
    .then(function (r) { if (!r.ok) throw new Error('http ' + r.status); return r.json(); })
    .then(function (json) {
      clearTimeout(timer);
      var w = parse(json);
      if (!w) throw new Error('shape');
      var t = Date.now();
      writeCache(json, t);
      show(w, new Date(t));
    })
    .catch(function () { clearTimeout(timer); showFail(); });
})();
