/* What a crawler with no JavaScript actually sees. */
const { chromium } = require('playwright');
const BASE = 'http://127.0.0.1:8099';
const PAGES = process.argv[2] ? process.argv[2].split(',') :
  ['/', '/blog/', '/discover-nashik/', '/plan-your-trip/', '/discover-nashik/trimbakeshwar/', '/kumbh-mela-2027/'];
(async () => {
  const b = await chromium.launch();
  const c = await b.newContext({ javaScriptEnabled: false, viewport: { width: 1280, height: 900 } });
  await c.route('**/*', r => {
    const u = r.request().url();
    if (/cloudinary|unsplash|googletagmanager|fonts\.g/.test(u)) return r.fulfill({ status: 200, body: '' });
    return r.continue();
  });
  for (const p of PAGES) {
    const page = await c.newPage();
    await page.goto(BASE + p, { waitUntil: 'domcontentloaded' });
    const d = await page.evaluate(() => {
      const txt = (document.querySelector('main') || document.body).innerText.replace(/\s+/g, ' ').trim();
      const links = [...(document.querySelector('main') || document.body).querySelectorAll('a[href]')]
        .map(a => a.getAttribute('href')).filter(h => h && !h.startsWith('#'));
      const hs = [...document.querySelectorAll('h1,h2,h3')].map(h => h.tagName + ' ' + h.textContent.replace(/\s+/g, ' ').trim().slice(0, 60));
      const hidden = [...document.querySelectorAll('main *')].filter(el => {
        const s = getComputedStyle(el);
        return (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) && el.textContent.trim().length > 40;
      }).map(el => el.tagName + '.' + (el.className || '').toString().split(' ')[0]);
      return { words: txt.split(' ').length, textHead: txt.slice(0, 180), links: links.length,
               uniqueInternal: [...new Set(links.filter(h => h.startsWith('/')))].length, hs: hs.length, headings: hs.slice(0, 14), hidden: [...new Set(hidden)].slice(0, 8) };
    });
    console.log('\n=== ' + p);
    console.log('  main words: ' + d.words + '   links in main: ' + d.links + '   unique internal: ' + d.uniqueInternal + '   headings: ' + d.hs);
    console.log('  text: "' + d.textHead + '…"');
    if (d.hidden.length) console.log('  ⚠ CONTENT HIDDEN WITHOUT JS: ' + d.hidden.join(', '));
    console.log('  headings: ' + d.headings.join(' | '));
    await page.close();
  }
  await b.close();
})();
