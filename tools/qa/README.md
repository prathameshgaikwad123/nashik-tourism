# QA harness

Three Playwright scripts used to verify Phase 3. They are optional developer
tooling — the site itself has no build step and no dependencies.

```bash
# serve the site (any static server will do)
npx http-server nashiktourism -p 8099 -c-1

# then, with playwright available:
node tools/qa/viewports.js        # overflow, CLS, LCP, tap targets, image dims
node tools/qa/interactions.js     # explorer, planner, guide filter, nav, keyboard
node tools/qa/no-javascript.js    # what a crawler with JS disabled actually sees
```

`viewports.js` checks 1440 / 1280 / 1024 / 390 / 375 / 360 px and reports any
horizontal overflow with the element that caused it, layout shift, interactive
targets under 44 px, and images missing intrinsic dimensions.

Note: `res.cloudinary.com` and `images.unsplash.com` are stubbed with a 1×1 PNG
so measurements do not depend on a network round trip — layout, CLS and overflow
stay accurate because the browser reserves space from each image's width/height
attributes, not from the file. Google Fonts is served from a local cache
(`fontcache/`, not committed) when present, because font metrics change text
wrapping; without it the scripts still run using fallback metrics.
