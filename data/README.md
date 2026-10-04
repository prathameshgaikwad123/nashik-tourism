# data/ — the editorial source of truth

Everything the site says as a fact, a notice, an event or a source is a record here.
Edit with `python3 tools/cms.py …` where a command exists; otherwise edit the JSON
and run `python3 tools/validate-data.py`. Git history is the revision history.

| File | What it holds |
|---|---|
| `sources.json` | The **source registry**: official bodies, news, businesses, data providers; reliability tier, check frequency, monitor settings. Nothing links to an official URL that is not here. |
| `facts.json` | The **fact database**. One record per fact: value, display text, status, source, verifiedAt/By, notes, alternatives when sources disagree. |
| `updates.json` | The verified-update feed. `status` (confirmed/developing/changed/cancelled/archived), `contentStatus` (draft/review/published/updated/archived), `expiresAt`. |
| `events.json` | Events. Verified events get structured data; reported ones are flagged and get none. |
| `destinations.json` | One structured record per destination (reused by pages, search, accessibility). `null` = not confirmed; `{"$fact": id}` = resolved from facts. |
| `accessibility.json` | Per-place access status and the hub's topics. Nothing is "verified accessible" without a source. |
| `transport.json` | Modular transport sections: which facts, which official sources, which live-update categories each shows. |
| `pages.json` | Metadata for hand-written guides (notice type, sources, verification status). |
| `changelog.json` | Visible revision history; also drives sitemap `lastmod` and the corrections log. |
| `site-config.json` | Kumbh lifecycle phases, pipeline policy, freshness limits, analytics switch. |
| `pipeline/candidates/` | Machine- or search-derived leads awaiting a human. **Never published by themselves.** |
| `state/` | Monitor hashes and snapshots (git-ignored; CI caches it). |

## Status vocabulary

* **Fact:** `verified` (an editor read the cited source and it supports the value; needs `source.url`, `verifiedAt`, `verifiedBy`) · `reported` · `not_verified` · `disputed` (lists every alternative).
* **Update:** `confirmed` (needs `verifiedAt` + `sourceUrl`) · `developing` · `changed` · `cancelled` · `archived`.
* **Accessibility:** `verified_accessible` · `partially_accessible` · `accessibility_unknown` · `accessibility_varies_by_event`.

## High-risk items

`tools/nt/risk.py` decides. A live update in a high-risk category (Safety, Roads) or
matching a high-risk rule needs `approvedBy` and `approvedAt`. The validator fails
the build otherwise. `pipeline.autoPublishLowRisk` ships `false`.

## Adding a verified fact

1. Open the official source and read it.
2. `python3 tools/cms.py fact verify <fact-id> --verified-by "Your Name" --source-url <url> [--display "…"]`
3. `python3 tools/cms.py build` — every page that shows the fact updates.
