# QA harness

Playwright scripts used to verify Phases 3 and 4. They are optional developer
tooling — the site itself has no build step and no dependencies.

```bash
# serve the site like production (real 404s, correct types)
python3 tools/qa/serve.py 8099

# then, with playwright available:
node tools/qa/viewports.js        # overflow, CLS, LCP, tap targets, image dims
node tools/qa/interactions.js     # explorer, planner, guide filter, nav, keyboard
node tools/qa/no-javascript.js    # what a crawler with JS disabled actually sees
node tools/qa/search-test.js      # search ranking on the brief's example queries (no browser)
python3 tools/qa/html_balance.py <files>   # tags balance, unique ids, no 'undefined'/'null' text
python3 tools/qa/contrast.py      # computed contrast of every colour pair the design uses
```

`interactions.js` also covers the search dialog, the menu sheet, client-side expiry,
Kumbh lifecycle switching (using Playwright's clock), the weather module with its
failure fallbacks, and keyboard behaviour.

`viewports.js` checks 1920 / 1440 / 1280 / 1024 / 768 / 414 / 390 / 375 / 360 / 320 px and reports any
horizontal overflow with the element that caused it, layout shift, interactive
targets under 44 px, and images missing intrinsic dimensions.

Note: `res.cloudinary.com` and `images.unsplash.com` are stubbed with a 1×1 PNG
so measurements do not depend on a network round trip — layout, CLS and overflow
stay accurate because the browser reserves space from each image's width/height
attributes, not from the file. Google Fonts is served from a local cache
(`fontcache/`, not committed) when present, because font metrics change text
wrapping; without it the scripts still run using fallback metrics.
