# What Claude needs to do next (nashiktourism.com)

Hand-off brief for the next Claude Code session. The SEO/AEO sprint is merged and live (PRs #6 and #7). This file lists what is left, in priority order, and the rules to follow while doing it.

Read first: `README.md`, `docs/DEPLOYMENT.md`, `VERIFY.md`, `docs/aeo-tracking.md`. The site is static HTML built by Python generators (`python3 tools/build-all.py`). There is no framework.

## Ground rules (do not break these)

1. **Never invent facts, numbers, timings, fares or dates.** Every claim needs a source you actually opened. If you cannot verify it, keep the existing wording and add it to `VERIFY.md`.
2. **Nothing is marked "Verified" unless a named human editor verified it.** Claude drafts and checks; `verifiedBy` needs a person's name supplied by the site owner. Do not put a person's name on the site yourself.
3. **No personal names anywhere deployed.** Articles are credited to "NashikTourism.com Editorial Team" (Organization). A unit test (`NoPersonalNames`) enforces this.
4. **Sponsored content:** always labelled, `rel="sponsored nofollow"`, sponsors never control facts, sponsored pages never Verified. `validate-data.py` and `seo-check.py` enforce it.
5. **Do not break URLs.** A URL that moves or is retired gets a row in `data/redirects.json` (301). Never delete a row.
6. **Do not touch Cloudflare settings.** AI-bot blocking and the managed robots.txt are already off. The www to apex redirect already works.
7. Before every commit: `python3 tools/build-all.py`, `python3 -m unittest discover -s tools/tests`, `python3 tools/validate-data.py`, `python3 tools/check-redirects.py`, `python3 tools/seo-check.py`. All must be clean (0 errors).
8. Work on the branch the session gives you. Open a PR; do not push to `main`.
9. If official sites cannot be fetched (network allowlist), say so and use search results only as leads. Label the result Reported, never Verified.

## A. Needs the site owner first (Claude should ask, not guess)

| Item | What Claude does once the owner answers |
|---|---|
| Name of the editor who will sign off verification (`verifiedBy`) | Use it for `cms.py fact verify ...` and `data/distances.json`. |
| Social profile URLs | Add to `data/seo.json` > `organization.sameAs`; they appear in Organization JSON-LD. |
| Hindi and Marathi proofread (owner said they will review) | Apply corrections in `tools/guides/distance_hub.py`. |
| Email or WhatsApp provider for the Kumbh 2027 sign-up | Owner sets `NT_SIGNUP_FORM_ACTION` / `NT_WHATSAPP_CHANNEL_URL` as repository variables. Claude only checks the block renders and the fallback link still works. |
| Affiliate parameters (MakeMyTrip, Goibibo, Booking, Agoda) | Owner sets `NT_AFFILIATE_*` repository variables. Claude checks `tools/apply-affiliate.py` output on a built page. |
| Real audience numbers for `/advertise/` | Owner pastes GA4 / Search Console figures into `data/monetization.json` > `audienceStats` with `asOf` and `source`. Claude does not estimate them. |
| Bing Webmaster verification code | Owner sets `NT_MSVALIDATE`. |

## B. Claude can do this when official sources are reachable

Goal: move items in `VERIFY.md` from *Reported* to *Verified*, with a human editor named by the owner.

1. **Kumbh dates (highest value).** Read the Authority's own notice (or the Maharashtra GR) for the six dates: `kumbh.mela.opening`, `kumbh.snan.1`, `.2`, `.3.nashik`, `.3.trimbak`, `kumbh.mela.closing`. Verifying them makes `/events/` emit `Event` JSON-LD, which fixes the "Events: 0 valid" rich-result report. Update `data/facts.json` and `data/events.json`.
2. **Official Simhastha website.** Open the address reported in the press (`simhasthamahakumbh.maharashtra.gov.in`), match it to the Authority's own channels, set `ntka-portal` `urlStatus` to `ok` in `data/sources.json`, and check what it says about passes and the app. Update the "Official status" box in `data/pages.json` (`officialStatus`) and the date in it.
3. **Distances.** Measure each row in `data/distances.json` on a maps service (shortest common road route), record the date, and set `status: verified` only when the owner's named editor confirms. Fill the rows still "Not yet confirmed" (Tapovan, Kapaleshwar, Sula, Igatpuri, Ramkund).
4. **MSRTC and rail.** Confirm the Nashik to Trimbakeshwar bus departure point, frequency and last bus back from MSRTC; confirm there is no direct train. Replace the "not verified" wording on the distance hub and both transport guides.
5. **Ramkund.** Confirm the Goda aarti time and ghat hours from the temple trust, the municipal corporation or `nashik.gov.in`. Update `tools/` content in the Ramkund guide (`nashiktourism/blog/ramkund-ghat-nashik-guide/index.html`) and `data/destinations.json`.
6. **Bhandardara.** Confirm the distances, Randha Falls 10 km, Kalsubai 12 km, nearest station and the firefly window from Maharashtra Tourism or similar (`tools/guides/bhandardara.py`).
7. **Destination schema.** Where a value is verified, add `geo`, `openingHoursSpecification` and `isAccessibleForFree` to the TouristAttraction JSON-LD (`tools/build-destinations.py`). `seo-check.py` currently blocks `isAccessibleForFree`; relax that rule only for verified values.

## C. Content work Claude can do without new facts

1. **Per-claim status on the remaining guides.** The 19 older guides still carry the blanket "not verified" notice from `tools/apply-verification.py`. Convert them, one guide per PR, to per-claim chips (`aeo.claim`, `aeo.key_facts`) only where a claim has a source. Keep the blanket notice where a guide's content is still unsourced.
2. **Question-style H2s and `KeyFacts`** on the older guides (distance hub and new guides already have them). Do not add numbers that are not already on the page.
3. **Refresh the e-pass guide weekly** while the Kumbh is being planned: check for a new official announcement, update `officialStatus` (`asOf`, text), add a `data/changelog.json` entry, and rebuild. Do not speculate.
4. **Keep the Kumbh hub current** (`tools/build-kumbh.py`): dates table, latest updates, the "reported vs confirmed" labels.
5. **Titles and descriptions:** `seo-check.py` still warns about titles over 70 characters and descriptions over 170 on about 20 pages. Rewrite them (keep the target query near the front).
6. **Sula, Panchavati, where-to-stay pages** now hold merged content. Re-read them once for duplication and tidy headings.

## D. Technical backlog

1. **Live-check tooling is merged.** `tools/verify-live.py` runs via the "Verify live site" workflow (manual dispatch); it checks pages, redirects, www, deliberate 404s, robots, llms and the IndexNow key.
2. **Run `verify-live` after every deploy** until the owner is comfortable. It checks every sitemap URL (200), every redirect (301 to 200), robots.txt, llms files and the IndexNow key file.
3. **Add `Last-Modified` correctness check:** confirm sitemap `lastmod` equals each page's `dateModified` in a test (`tools/tests/test_seo.py`).
4. **Image sitemap:** only Cloudinary images inside `<main>` are listed. Consider adding alt text checks for them.
5. **Scheduled content check.** Add a monthly workflow that opens an issue listing every `VERIFY.md` item older than 30 days.
6. **Search Console data.** If the owner exports GSC CSVs into `docs/`, re-rank the distance cluster (nashik to Trimbakeshwar, station variants, Hindi and Marathi queries) and propose page changes with evidence.

## E. Monthly routine (for Claude or the owner)

Follow `docs/aeo-tracking.md`: run the 30 prompts in ChatGPT, Gemini, Perplexity, Claude and Google AI Mode, log whether nashiktourism.com is cited, and compare the distance cluster (prompts 1 to 12) with the Kumbh cluster (13 to 21). Check Bing Webmaster Tools (IndexNow accepted, pages indexed) and Search Console positions for the target queries.

## F. Things that are done, do not redo

- robots.txt, `_redirects`, `llms.txt`, `llms-full.txt`, IndexNow key and workflow, sitemap `lastmod` and images.
- Distance hub, two transport guides, Bhandardara guide (Akole taluka, Ahilyanagar district), Ramkund aarti/distance/temples section, e-pass "official status" box.
- Merges with 301: Sula, packing list, budget, food.
- Editorial-team page, Organization-as-author JSON-LD, bylines with Last updated / Last verified.
- `/advertise/`, sponsored label component, affiliate link handling, sign-up block, AI-referral event in `site.js`.
- Browser QA (viewports, interactions, no-JS, axe) on the key pages: all clean as of 22 Nov 2026.

## G. Useful commands

```bash
python3 tools/build-all.py                      # validate data, build every page
python3 -m unittest discover -s tools/tests     # unit tests
python3 tools/validate-data.py                  # data against the verification policy
python3 tools/seo-check.py                      # SEO, schema and link audit
python3 tools/check-redirects.py                # every redirect lands on a real page
python3 tools/verify-live.py                    # live site check (needs internet)
python3 tools/qa/serve.py 8099                  # serve the built site, then run tools/qa/*.js
python3 tools/cms.py fact verify <fact-id> --verified-by "<editor name>" --source-url <url>
```
