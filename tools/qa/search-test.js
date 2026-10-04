/*
 * Ranking checks for /search.js against the real /search-index.json.
 *   node tools/qa/search-test.js
 * Each case names a query and a URL (prefix) that must appear in the top N.
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..', '..', 'nashiktourism');
global.window = global; global.document = { dispatchEvent() {}, createElement() { return {}; } };
global.CustomEvent = class { constructor(n) { this.type = n; } };
global.fetch = async () => ({ ok: true, json: async () => JSON.parse(fs.readFileSync(path.join(ROOT, 'search-index.json'), 'utf8')) });
eval(fs.readFileSync(path.join(ROOT, 'search.js'), 'utf8'));

const CASES = [
  ['Trimbakeshwar timing', '/discover-nashik/trimbakeshwar/', 3],
  ['Kumbh parking', '/kumbh-mela-2027/#parking-roads', 3],
  ['Nashik airport', '/transport/#airport', 3],
  ['Ramkund', '/discover-nashik/panchavati/', 3],
  ['Nashik to Trimbakeshwar', '/blog/trimbakeshwar-to-nashik-distance-route/', 4],
  ['Sula Vineyards', '/discover-nashik/sula-vineyards/', 2],
  ['Kumbh 2027 dates', '/kumbh-mela-2027/#dates', 3],
  ['Nashik events', '/events/', 3],
  ['trimbakeswar', '/discover-nashik/trimbakeshwar/', 3],        // typo
  ['wheelchair', '/accessible-nashik/', 3],
  ['epass', '/kumbh-mela-2027/#passes', 3],                      // synonym
  ['how do I reach nashik by train', '/transport/#train', 4],
  ['weather', '/nashik-now/', 3],
];
(async () => {
  await window.NTSearch.load();
  let fail = 0;
  for (const [q, want, n] of CASES) {
    const res = window.NTSearch.search(q, { limit: 12 });
    const idx = res.findIndex(r => r.doc.u.indexOf(want) === 0);
    const ok = idx >= 0 && idx < n;
    if (!ok) fail++;
    console.log((ok ? 'ok   ' : 'FAIL ') + q.padEnd(34) + ' -> rank ' + (idx < 0 ? 'none' : idx + 1) + '  [' + res.slice(0, 3).map(r => r.doc.u).join(' | ') + ']');
  }
  const none = window.NTSearch.search('zzzzqq', {}).length;
  console.log((none === 0 ? 'ok   ' : 'FAIL ') + 'nonsense query returns nothing');
  if (none) fail++;
  process.exit(fail ? 1 : 0);
})();
