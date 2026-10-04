/*
 * Automated accessibility audit with axe-core (WCAG 2.0/2.1/2.2 A and AA rules).
 *
 *   npm install --no-save axe-core        # not vendored in the repo
 *   node tools/qa/a11y.js [--base http://127.0.0.1:8099] [--widths 360,1280] [--pages /,/updates/]
 *   node tools/qa/a11y.js --open-search   # also audits the open search dialog and open mobile menu
 *
 * Automated rules catch roughly a third of accessibility problems. This does not
 * replace the manual checks in docs/ACCESSIBILITY.md (keyboard order, screen reader).
 */
const { chromium } = require('playwright');
const fs = require('fs');
const args = process.argv.slice(2);
const arg = (n, d) => { const i = args.indexOf('--' + n); return i >= 0 ? args[i + 1] : d; };
const BASE = arg('base', 'http://127.0.0.1:8099');
const WIDTHS = arg('widths', '360,1280').split(',').map(Number);
const PAGES = arg('pages', ['/', '/search/', '/updates/', '/updates/archive/', '/events/', '/sources/', '/editorial-policy/', '/transport/', '/accessible-nashik/',
  '/nashik-now/', '/kumbh-mela-2027/', '/kumbh-mela-2027/live-updates/', '/discover-nashik/', '/discover-nashik/trimbakeshwar/', '/plan-your-trip/',
  '/blog/', '/blog/ramkund-ghat-nashik-guide/', '/blog/kumbh-mela-2027-all-snan-dates/', '/about/', '/contact/', '/disclaimer/', '/404.html'].join(',')).split(',');
const AXE = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const PNG = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==', 'base64');
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'];

(async () => {
  const browser = await chromium.launch();
  let total = 0;
  const seen = {};
  for (const w of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, isMobile: w < 700, hasTouch: w < 700 });
    await ctx.route(/res\.cloudinary\.com|images\.unsplash\.com/, r => r.fulfill({ status: 200, contentType: 'image/png', body: PNG }));
    await ctx.route(/fonts\.|googletagmanager/, r => r.abort());
    await ctx.route(/api\.open-meteo\.com/, r => r.abort());
    for (const p of PAGES) {
      const page = await ctx.newPage();
      await page.goto(BASE + p, { waitUntil: 'load' }).catch(() => {});
      await page.waitForTimeout(500);
      await page.evaluate(() => document.querySelectorAll('.fade-up').forEach(e => e.classList.add('visible')));
      await page.waitForTimeout(900);   // let the reveal transition finish: axe must not sample half-faded text
      const states = [['page', async () => {}]];
      if (args.includes('--open-search')) {
        states.push(['search dialog', async () => { await page.click('#searchOpen'); await page.waitForTimeout(250); }]);
        if (w < 1200) states.push(['mobile menu', async () => { await page.keyboard.press('Escape'); await page.click('#hamburger'); await page.waitForTimeout(350); }]);
      }
      for (const [label, enter] of states) {
        await enter();
        await page.addScriptTag({ content: AXE });
        const res = await page.evaluate(tags => axe.run(document, { runOnly: { type: 'tag', values: tags } }), TAGS);
        for (const v of res.violations) {
          for (const n of v.nodes) {
            const key = [v.id, p, label, n.target.join(' ')].join('|');
            if (seen[key]) continue;
            seen[key] = 1; total++;
            console.log('%s %s @%d [%s] %s (%s)\n    %s\n    %s', v.impact.toUpperCase().padEnd(8), p, w, label, v.id, v.help,
              n.target.join(' ').slice(0, 110), (n.failureSummary || '').split('\n')[1] || '');
          }
        }
        if (label === 'search dialog') await page.keyboard.press('Escape');
      }
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
  console.log('\n%d accessibility violation(s)', total);
  process.exit(total ? 1 : 0);
})();
