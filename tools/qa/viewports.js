/*
 * QA harness for nashiktourism.com — real measurements, no guesses.
 *
 * Usage:  node qa.js [--base http://127.0.0.1:8099] [--pages /,/blog/] [--json out.json]
 *
 * Reports, per page × viewport:
 *   - horizontal overflow (and the elements causing it)
 *   - CLS (layout-instability entries), LCP
 *   - transferred bytes by resource type, request count
 *   - interactive targets under 44px
 *   - images missing intrinsic dimensions
 *   - console errors
 */
const { chromium } = require('playwright');

const args = process.argv.slice(2);
function arg(name, dflt) {
  const i = args.indexOf('--' + name);
  return i >= 0 ? args[i + 1] : dflt;
}

const BASE = arg('base', 'http://127.0.0.1:8099');
const WIDTHS = arg('widths', '1440,1280,1024,390,375,360').split(',').map(Number);
const PAGES = arg('pages', [
  '/', '/discover-nashik/', '/discover-nashik/trimbakeshwar/', '/discover-nashik/igatpuri/',
  '/plan-your-trip/', '/blog/', '/blog/ramkund-ghat-nashik-guide/',
  '/kumbh-mela-2027/', '/about/', '/contact/', '/404.html',
].join(',')).split(',').filter(Boolean);
const JS_DISABLED = args.includes('--nojs');

const OVERFLOW_PROBE = `(() => {
  const docW = document.documentElement.clientWidth;
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const style = getComputedStyle(el);
    if (style.position === 'fixed') continue;
    if (r.right > docW + 1 || r.left < -1) {
      // Ignore elements inside a deliberate horizontal scroller
      let p = el.parentElement, scroller = false;
      while (p && p !== document.body) {
        const ps = getComputedStyle(p);
        if (ps.overflowX === 'auto' || ps.overflowX === 'scroll') { scroller = true; break; }
        p = p.parentElement;
      }
      if (scroller) continue;
      out.push({
        tag: el.tagName.toLowerCase(),
        cls: (el.className && el.className.toString ? el.className.toString() : '').slice(0, 70),
        id: el.id || '',
        left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width),
      });
    }
  }
  return {
    docW,
    scrollW: document.documentElement.scrollWidth,
    bodyScrollW: document.body.scrollWidth,
    offenders: out.slice(0, 12),
  };
})()`;

const TARGET_PROBE = `(() => {
  const small = [];
  const sel = 'a, button, input, select, textarea, summary, [role="button"], [tabindex]:not([tabindex="-1"])';
  for (const el of document.querySelectorAll(sel)) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (getComputedStyle(el).visibility === 'hidden') continue;
    // inline links inside prose are exempt from the 44px rule
    const inProse = el.closest('p, li, .breadcrumb, .footer-bottom, .faq-answer, .article-body p');
    if (inProse && el.tagName === 'A') continue;
    if (r.height < 44 || r.width < 24) {
      small.push({
        tag: el.tagName.toLowerCase(),
        cls: (el.className && el.className.toString ? el.className.toString() : '').slice(0, 50),
        text: (el.textContent || '').trim().slice(0, 30),
        w: Math.round(r.width), h: Math.round(r.height),
      });
    }
  }
  return small.slice(0, 15);
})()`;

const IMG_PROBE = `(() => {
  const bad = [];
  for (const img of document.images) {
    const hasDim = img.hasAttribute('width') && img.hasAttribute('height');
    if (!hasDim) bad.push({ src: (img.currentSrc || img.src).slice(-60), cls: img.className });
  }
  return bad;
})()`;

const VITALS_INIT = `
  window.__cls = 0; window.__shifts = []; window.__lcp = 0;
  try {
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) {
        if (!e.hadRecentInput) { window.__cls += e.value; if (e.value > 0.001) window.__shifts.push(+e.value.toFixed(4)); }
      }
    }).observe({ type: 'layout-shift', buffered: true });
    new PerformanceObserver((l) => {
      const es = l.getEntries(); window.__lcp = es[es.length - 1].startTime;
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  } catch (e) {}
`;

// The sandbox egress proxy blocks res.cloudinary.com / images.unsplash.com, so
// image requests would hang and distort every measurement. Fulfil them locally
// with a tiny PNG: layout, CLS and overflow stay accurate because the browser
// reserves space from the width/height attributes, not the file.
const STUB_PNG = Buffer.from(
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
  'base64');
const EXTERNAL = /res\.cloudinary\.com|images\.unsplash\.com|googletagmanager\.com|google-analytics\.com/;

// Google Fonts is reachable but flaky through the proxy, and font metrics change
// text wrapping — so serve the real files from a local cache instead of stubbing.
const fs = require('fs');
const path = require('path');
const CACHE = path.join(__dirname, 'fontcache');
const FONT_MAP = {};
try {
  for (const line of fs.readFileSync(path.join(CACHE, 'map.txt'), 'utf8').trim().split('\n')) {
    const [u, f] = line.split(' ');
    if (u && f) FONT_MAP[u] = path.join(CACHE, f);
  }
} catch (e) {}
const FONT_CSS = (() => { try { return fs.readFileSync(path.join(CACHE, 'fonts.css'), 'utf8'); } catch (e) { return null; } })();

async function stubExternals(context) {
  await context.route('**/*', async (route) => {
    const url = route.request().url();
    if (FONT_CSS && url.startsWith('https://fonts.googleapis.com/')) {
      return route.fulfill({ status: 200, contentType: 'text/css', body: FONT_CSS });
    }
    if (FONT_MAP[url]) {
      return route.fulfill({ status: 200, contentType: 'font/woff2', body: fs.readFileSync(FONT_MAP[url]) });
    }
    if (url.startsWith('https://fonts.gstatic.com/')) {
      return route.fulfill({ status: 200, contentType: 'font/woff2', body: Buffer.alloc(0) });
    }
    if (!EXTERNAL.test(url)) return route.continue();
    if (route.request().resourceType() === 'image') {
      return route.fulfill({ status: 200, contentType: 'image/png', body: STUB_PNG });
    }
    return route.fulfill({ status: 200, contentType: 'application/javascript', body: '' });
  });
}

(async () => {
  const browser = await chromium.launch();
  const results = [];

  for (const width of WIDTHS) {
    const mobile = width < 768;
    const context = await browser.newContext({
      viewport: { width, height: mobile ? 800 : 900 },
      deviceScaleFactor: 1,
      javaScriptEnabled: !JS_DISABLED,
      hasTouch: mobile,
      isMobile: mobile,
    });
    await context.addInitScript(VITALS_INIT);
    await stubExternals(context);

    for (const path of PAGES) {
      const page = await context.newPage();
      const bytes = {}; let requests = 0;
      const errors = [];
      page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().slice(0, 160)); });
      page.on('pageerror', (e) => errors.push('PAGEERROR: ' + e.message.slice(0, 160)));
      page.on('response', async (res) => {
        requests++;
        try {
          const t = res.request().resourceType();
          const len = Number((await res.headerValue('content-length')) || 0);
          bytes[t] = (bytes[t] || 0) + len;
        } catch (e) {}
      });

      let row = { width, path, ok: false };
      try {
        const resp = await page.goto(BASE + path, { waitUntil: 'load', timeout: 30000 });
        await page.waitForTimeout(mobile ? 900 : 700);
        const overflow = await page.evaluate(OVERFLOW_PROBE);
        const targets = JS_DISABLED ? [] : await page.evaluate(TARGET_PROBE);
        const imgs = await page.evaluate(IMG_PROBE);
        const vitals = await page.evaluate('({cls: window.__cls, shifts: window.__shifts, lcp: Math.round(window.__lcp)})');
        row = {
          width, path, ok: true, status: resp && resp.status(),
          scrollW: overflow.scrollW, docW: overflow.docW,
          overflow: overflow.scrollW > overflow.docW + 1,
          offenders: overflow.offenders,
          cls: +vitals.cls.toFixed(4), shifts: vitals.shifts, lcpMs: vitals.lcp,
          smallTargets: targets, imgsNoDim: imgs,
          requests, bytes, errors,
        };
      } catch (e) {
        row.error = e.message.slice(0, 200);
      }
      results.push(row);
      await page.close();
    }
    await context.close();
  }
  await browser.close();

  // ── Report
  const fail = [];
  console.log('\n' + '='.repeat(78));
  console.log('QA RUN' + (JS_DISABLED ? '  [JavaScript DISABLED]' : '') + '  base=' + BASE);
  console.log('='.repeat(78));
  for (const width of WIDTHS) {
    console.log('\n── viewport ' + width + 'px ' + '─'.repeat(50));
    for (const r of results.filter((x) => x.width === width)) {
      if (!r.ok) { console.log('  ' + r.path.padEnd(44) + ' ERROR ' + r.error); fail.push(r); continue; }
      const flags = [];
      if (r.overflow) flags.push('OVERFLOW ' + r.scrollW + '>' + r.docW);
      if (r.cls > 0.1) flags.push('CLS ' + r.cls);
      if (r.smallTargets.length) flags.push(r.smallTargets.length + ' small targets');
      if (r.imgsNoDim.length) flags.push(r.imgsNoDim.length + ' img no-dim');
      if (r.errors.length) flags.push(r.errors.length + ' console errors');
      const kb = (n) => Math.round((n || 0) / 1024) + 'k';
      const line = '  ' + r.path.padEnd(44) +
        ' cls=' + String(r.cls).padEnd(7) +
        ' lcp=' + String(r.lcpMs + 'ms').padEnd(8) +
        ' req=' + String(r.requests).padEnd(4) +
        ' css=' + kb(r.bytes.stylesheet) + ' js=' + kb(r.bytes.script) + ' img=' + kb(r.bytes.image);
      console.log(line + (flags.length ? '\n      ⚠ ' + flags.join(' | ') : ''));
      if (r.overflow) {
        fail.push(r);
        for (const o of r.offenders.slice(0, 5)) {
          console.log('        → <' + o.tag + (o.id ? '#' + o.id : '') + (o.cls ? '.' + o.cls.split(' ').join('.') : '') +
            '> right=' + o.right + ' w=' + o.width);
        }
      }
      for (const t of r.smallTargets.slice(0, 4)) {
        console.log('        ↳ small: <' + t.tag + '.' + String(t.cls).split(' ')[0] + '> ' + t.w + '×' + t.h + ' "' + t.text + '"');
      }
      for (const i of r.imgsNoDim.slice(0, 3)) console.log('        ↳ img no width/height: …' + i.src);
      for (const e of r.errors.slice(0, 3)) console.log('        ↳ console: ' + e);
    }
  }
  console.log('\n' + '='.repeat(78));
  console.log(fail.length ? 'FAILURES: ' + fail.length + ' page/viewport combos with overflow or load errors' : 'No overflow or load failures.');
  console.log('='.repeat(78) + '\n');

  const out = arg('json', null);
  if (out) require('fs').writeFileSync(out, JSON.stringify(results, null, 1));
  process.exit(0);
})();
