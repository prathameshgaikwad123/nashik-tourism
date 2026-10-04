# Deployment, automation and operations

## What is deployed

The contents of `nashiktourism/` — static files, no server code. Any static host works
(Cloudflare Pages, Netlify, GitHub Pages, S3+CDN…). Requirements:

* `/path/` serves `/path/index.html`; unknown paths serve `404.html` **with a 404 status**.
* Serve `.json`, `.xml`, `.webmanifest`, `.js` with their proper types; enable gzip/brotli.
* Cache `style.css`, `site.js`, `search.js`, `now.js` and images long-term **with versioned
  URLs or a short max-age**; they are not fingerprinted yet. Cache HTML for minutes, not days.
* No URL was changed in this phase, so **no redirects are required**. If you later retire
  `/blog/nashik-kumbh-mela-2027-complete-guide/` (a thin stub), add a single 301 to
  `/kumbh-mela-2027/` and remove it from `posts.json`.

The existing host configuration was not in the repository, so nothing host-specific
(`_redirects`, `netlify.toml`, `vercel.json`) was added or changed.

## Environment variables and secrets

None are required to build or run the site. All are optional and read from the environment only.

| Name | Where | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | secret (monitor workflow) | Enables AI classification of detected changes. Without it the monitor still runs with heuristic candidates. |
| `NT_CLASSIFIER_MODEL` | variable | Model id for classification (default `claude-haiku-4-5-20251001`). |
| `NOTIFY_WEBHOOK_URL` | secret | Slack/Teams/Discord webhook for "candidates need review". |
| `INDEXNOW_KEY` | secret | IndexNow submission (Bing/Yandex). Also requires `nashiktourism/<key>.txt`. |
| `DAILY_REBUILD` | repository variable | Set to `false` to disable the daily rebuild workflow if your host rebuilds itself. |
| `NT_NOW` | local only | Pin the build clock (ISO timestamp) to preview any date, e.g. `NT_NOW=2027-08-02T09:00:00+05:30 python3 tools/build-all.py`. |

Weather uses Open-Meteo, which needs no key. Google Analytics keeps its existing
measurement ID in `tools/chrome.py`; `data/site-config.json > analytics.sitewide` is the
switch to add it to the legacy guides (off by default).

## Database migration

There is no database. The data layer is JSON in `data/`, versioned by git. Nothing to migrate.
If the owner later wants a database-backed editor, `tools/nt/store.py` is the only module that
reads and writes `data/`.

## Cron / automation

| Workflow | When | What it does |
|---|---|---|
| `ci.yml` | every push/PR | tests, data validation, full build, SEO/link audit, content-health artifact |
| `daily-build.yml` | 00:10 IST daily | rebuilds so expiry and Kumbh phases advance; commits only if output changed |
| `monitor-sources.yml` | every 6 hours | polls due sources, opens a PR with **candidates only** (nothing publishes) |
| `qa.yml` | weekly / manual | real-browser checks at 320–1920 px |

Search engines: `sitemap.xml` carries honest `lastmod`; submit it once in Search Console.
`tools/indexnow.py --submit` notifies IndexNow engines of changed URLs (Google does not use IndexNow).

## Release checklist

1. `python3 tools/build-all.py` (validates data first)
2. `python3 -m unittest discover -s tools/tests`
3. `python3 tools/seo-check.py` — zero errors
4. Browser QA if layouts changed: `node tools/qa/viewports.js` with the server from `tools/qa/serve.py`
5. Deploy `nashiktourism/`; confirm `/sitemap.xml`, `/robots.txt` and a real 404.
