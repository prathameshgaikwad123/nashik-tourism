# AEO tracking: are AI answer engines citing NashikTourism.com?

Run these prompts **once a month** (same day each month) in each engine below, in a logged-out or fresh session, and log the result in the table. Record the date and the engine, whether nashiktourism.com is **cited as a source**, whether it is **named without a link**, and which page was cited.

Engines: ChatGPT (with search on), Gemini, Perplexity, Claude (with web search), Google AI Mode / AI Overviews, and optionally Copilot and DeepSeek.

Expected citation targets are in brackets. Use them to see whether the right page is being surfaced.

## 30 test prompts

**Distance and transport**
1. How far is Trimbakeshwar from Nashik? [distance hub]
2. Nashik to Trimbakeshwar distance in km and time [distance hub]
3. Trimbakeshwar to Nashik distance by road [distance hub]
4. Distance from Nashik Road railway station to Trimbakeshwar [station guide]
5. How do I get from Nashik Road station to Trimbakeshwar temple? [station guide]
6. How far is Trimbakeshwar from Nashik CBS bus stand? [distance hub]
7. Trimbakeshwar to Ramkund distance and how to travel [Ramkund transport guide]
8. Is there a train to Trimbakeshwar? [distance hub, station guide]
9. Last bus from Trimbakeshwar to Nashik [distance hub FAQ]
10. नाशिक ते त्र्यंबकेश्वर अंतर किती किलोमीटर? [distance hub, Marathi block]
11. नासिक से त्र्यंबकेश्वर की दूरी कितनी है? [distance hub, Hindi block]
12. Nashik airport to Trimbakeshwar distance [distance hub]

**Kumbh Mela 2027**
13. Nashik Kumbh Mela 2027 dates [Kumbh hub]
14. When are the Amrit Snan dates at Nashik Kumbh 2027? [Kumbh hub, snan dates]
15. Do I need an e-pass for Nashik Kumbh Mela 2027? [e-pass guide]
16. Is registration required for the Nashik Simhastha Kumbh? [e-pass guide]
17. Where to stay for Nashik Kumbh Mela 2027 [where-to-stay guide]
18. How much will a Nashik Kumbh Mela trip cost? [where-to-stay guide, budget section]
19. What to pack for Kumbh Mela Nashik [Kumbh hub, packing section]
20. How to reach Nashik for Kumbh Mela 2027 [how-to-reach guide]
21. Nashik Kumbh vs Prayagraj Kumbh [comparison guide]

**Destinations**
22. Bhandardara things to do [Bhandardara guide]
23. Bhandardara fireflies season [Bhandardara guide]
24. Igatpuri vs Bhandardara [Bhandardara guide]
25. Randha Falls and Umbrella Falls Bhandardara best time [Bhandardara guide]
26. Ramkund Nashik aarti time [Ramkund guide]
27. Ram Ghat Nashik aarti time [Ramkund guide]
28. What to eat near Ramkund Nashik [Panchavati page]
29. Sula Vineyards Nashik visit guide [Sula page]
30. Best time to visit Nashik [best-time guide]

## Log

Copy one block per month. "Cited" = nashiktourism.com appears as a link or listed source; "Named" = mentioned by name without a link.

| Month | Prompt # | Engine | Cited (Y/N) | Named (Y/N) | Page cited | Competing sources cited | Notes |
|---|---|---|---|---|---|---|---|
| 2026-12 | 1 | ChatGPT | | | | | |
| 2026-12 | 1 | Gemini | | | | | |
| 2026-12 | 1 | Perplexity | | | | | |
| 2026-12 | 1 | Claude | | | | | |
| 2026-12 | 1 | Google AI Mode | | | | | |

Summary line each month: citations out of (prompts × engines) tested. Watch the distance cluster (1 to 12) and the Kumbh cluster (13 to 21) separately.

## Referral traffic

`/site.js` fires an `ai_referral` event (parameter `ai_source`) and sets an `ai_referrer` user property when a visit arrives from chatgpt.com, chat.openai.com, perplexity.ai, gemini.google.com, claude.ai, copilot.microsoft.com, deepseek.com (and chat.deepseek.com) or you.com, either by referrer or by `utm_source` (ChatGPT adds `utm_source=chatgpt.com`). It works only on pages that already load GA4 (`window.gtag`).

To see AI referrals as one channel in GA4:

1. Admin > Data display > Channel groups > Create new channel group.
2. Add a channel named **AI referral** with the condition *Source* matches regex
   `chatgpt\.com|chat\.openai\.com|perplexity\.ai|gemini\.google\.com|claude\.ai|copilot\.microsoft\.com|deepseek\.com|you\.com`
   and move it above "Referral".
3. In Explore, break down by `ai_source` to compare engines. The event gives you the same split.

Cookieless counters can be switched on at build time with `NT_PLAUSIBLE_DOMAIN` (Plausible) or `NT_CF_BEACON_TOKEN` (Cloudflare Web Analytics); see `docs/DEPLOYMENT.md`. Neither needs a cookie banner.

## Pages to watch (Google AI features, Search Console, 90 days to 24 Nov 2026)

Search Console's generative-AI performance report showed **7,580 impressions in Google's AI features**
(about 8.5% of all impressions) across 49 pages. These five lead; re-check their AI impressions monthly
and note any page that drops out of the list.

| Page | AI impressions (90 days to 24 Nov 2026) |
|---|---|
| `/blog/trimbakeshwar-to-nashik-distance-route/` | 3,677 |
| `/blog/ramkund-ghat-nashik-guide/` | 779 |
| `/discover-nashik/igatpuri/` | 646 |
| `/blog/nashik-kumbh-mela-e-pass-registration-2027/` | 408 |
| `/blog/nashik-kumbh-mela-vs-prayagraj-kumbh/` | 307 |

Gap to close: `/discover-nashik/` (the Places to Visit in Nashik page) is **not in the top 10**, although Bing/Copilot
grounding queries for "Nashik tourist places" style questions (about 6.4K citations) are the highest-volume
queries we track. It also had only 62 Google impressions at the time. Watch it first.

Source: owner-supplied Search Console figures, 24 Nov 2026. Not independently verified in this repo.

## Also check each month

* Bing Webmaster Tools: pages indexed, IndexNow submissions accepted (Bing feeds ChatGPT search and Copilot).
* Search Console: impressions and position for "nashik to trimbakeshwar distance", "trimbakeshwar to nashik distance", "bhandardara", "nashik kumbh mela 2027".
* `https://nashiktourism.com/robots.txt` still lists the AI crawlers as allowed, with no Cloudflare "managed" block above it.
