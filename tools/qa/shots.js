/*
 * Screenshots for eyeballing layouts.
 *   node tools/qa/shots.js --pages /updates/,/events/ --widths 360,1280 --out /tmp/shots [--full] [--open-search] [--open-menu]
 * External image hosts are stubbed with a flat 1x1 PNG (see README), so only
 * layout is judged here, not photography.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const args = process.argv.slice(2);
const arg = (n, d) => { const i = args.indexOf('--' + n); return i >= 0 ? args[i + 1] : d; };
const BASE = arg('base', 'http://127.0.0.1:8099');
const PAGES = arg('pages', '/').split(',');
const WIDTHS = arg('widths', '360').split(',').map(Number);
const OUT = arg('out', '/tmp/shots');
const FULL = args.includes('--full');
const PNG = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==', 'base64');
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  for (const w of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: w < 700 ? 800 : 900 }, deviceScaleFactor: 1 });
    await ctx.route(/res\.cloudinary\.com|images\.unsplash\.com/, r => r.fulfill({ status: 200, contentType: 'image/png', body: PNG }));
    await ctx.route(/fonts\.(googleapis|gstatic)\.com|googletagmanager\.com/, r => r.abort());
    await ctx.route(/api\.open-meteo\.com/, r => r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ current: { temperature_2m: 27.4, apparent_temperature: 29.1, relative_humidity_2m: 61, precipitation: 0, weather_code: 2, wind_speed_10m: 9 }, daily: { time: ['2026-10-04','2026-10-05','2026-10-06','2026-10-07'], weather_code: [2,3,61,1], temperature_2m_max: [31,30,28,32], temperature_2m_min: [21,20,20,21], precipitation_probability_max: [10,30,70,5] } }) }));
    for (const p of PAGES) {
      const page = await ctx.newPage();
      await page.goto(BASE + p, { waitUntil: 'networkidle' }).catch(() => {});
      if (args.includes('--open-menu')) { await page.click('#hamburger'); await page.waitForTimeout(400); }
      if (args.includes('--open-search')) { await page.click('#searchOpen'); await page.waitForTimeout(300); const q = arg('q', ''); if (q) { await page.fill('#searchInput', q); await page.waitForTimeout(800); } }
      await page.waitForTimeout(300);
      const name = p.replace(/[^a-z0-9]+/gi, '_').replace(/^_|_$/g, '') || 'home';
      await page.screenshot({ path: `${OUT}/${name}-${w}${args.includes('--open-menu') ? '-menu' : ''}${args.includes('--open-search') ? '-search' : ''}.png`, fullPage: FULL });
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
})();
