# VERIFY.md: figures and claims to confirm in one pass

Created in the SEO/AEO sprint (22 Nov 2026). **Items under "Verified on 22 Nov 2026" are marked Verified; everything else is not.** The official pages (nashik.gov.in, MSRTC, Indian Railways, NHAI, the Kumbh Authority) could not be opened from the build environment, so every figure comes from search-result text and is shown as *Reported*, *Sources differ* or *Not yet verified*. Each item below has a matching `<!-- VERIFY: ... -->` comment in the page source.

**To verify an item:** open the suggested source, read it, then update the data file named in the last column (set `status` to `verified`, plus `verifiedBy`, `verifiedAt` and the source URL; `python3 tools/cms.py fact verify <id> ...` works for facts). Rebuild with `python3 tools/build-all.py`. The status chip on the page changes by itself.

## Verified on 22 Nov 2026

Approved by the site owner (editor) on 22 Nov 2026. Marked `verified` by "NashikTourism.com Editorial Team".

| Item | Verified value | Source |
|---|---|---|
| `kumbh.mela.opening` | Dhwajarohan (flag-hoisting), 31 October 2026, 12:02 PM | Authority's official FAQ, https://simhasthamahakumbh.maharashtra.gov.in/faqs (page last updated 17 Nov 2026), checked 22 Nov 2026 |
| `kumbh.snan.1` | First Amrut Snan, Monday 2 August 2027 (Somvati Amavasya) | same |
| `kumbh.snan.2` | Second Amrut Snan, Tuesday 31 August 2027 (Shravan Amavasya) | same |
| `kumbh.snan.3.nashik` | Third Amrut Snan, 11 September 2027, Ramtirth (Ramkund), Nashik | same |
| `kumbh.snan.3.trimbak` | Third Amrut Snan, 12 September 2027, Kushavarta Tirth, Trimbakeshwar | same |
| `kumbh.mela.closing` | Dhwajavatarana (flag-lowering), 24 July 2028, 3:36 PM | same |
| `kumbh.major-period` (new) | Major Mela period 15 June to 30 September 2027 | same |
| `kumbh.nagar-pradakshina` (new) | Nagar Pradakshina 29 July 2027 | same |
| Official website | `simhasthamahakumbh.maharashtra.gov.in` is live (maharashtra.gov.in domain; lists the Authority's official social handles). Source `ntka-portal`, `urlStatus: ok` | opened 22 Nov 2026 |
| CBS to Trimbakeshwar Jyotirling Mandir | About 29-30 km, roughly 55-60 min (routes 29.3 / 29.4 / 29.6 km; fastest 56 min), late-morning traffic. Also `dest.trimbakeshwar.distance` and `dest.trimbakeshwar.journey` | Google Maps driving, measured Sun 22 Nov 2026 about 11:50 AM IST |
| Nashik Road railway station to Trimbakeshwar | About 37-39 km, roughly 1 hr 15 min (routes 37.3 / 38.0 / 38.8 km; 1 hr 15 min to 1 hr 21 min) | same |
| Ramkund, Panchavati to Trimbakeshwar | About 30-31 km, roughly 1 hr (routes 30.3 / 30.5 / 31.1 km; 1 hr to 1 hr 7 min) | same |

Effects: the `/events/` page now emits `Event` JSON-LD for the five upcoming Kumbh events (the opening date has passed, so it is listed under "Earlier"). Kumbh pages use the official term "Amrut Snan" (the spelling "Amrit Snan" is kept once on the hub and the dates guide as a search variant). Distance times vary with traffic; re-measure if routes change.

Everything below is still open.

## 1. Distances (page: `/blog/trimbakeshwar-to-nashik-distance-route/` and both transport guides; data: `data/distances.json`)

| Figure | Currently shown | Suggested source / how |
|---|---|---|
| Tapovan, Kapaleshwar, Sula Vineyards, Igatpuri | Not yet confirmed | Google Maps |
| Nashik (Ozar) airport | About 40–55 km (sources differ) | Google Maps; AAI page; also confirm which scheduled flights operate |
| Mumbai, Pune, Shirdi | 166–193 / 209–240 / 76–125 km (sources differ) | Google Maps, NHAI route; Shirdi range is too wide to be useful |
| Ramkund is about 2 km from the CBS | Reported (travel listings) | Google Maps |
| Panchavati to Nashik Road station | 14 km (district site) vs 8 km (earlier copy): disputed | Google Maps; fact `transport.nashik-road.distance` |
| Kalaram, Sita Gufa, Sundarnarayan distances from the CBS | 2.5–3, 2.7, 2 km (reported) | nashik.gov.in places of interest; Google Maps |

## 2. Transport services (same pages)

| Claim | Suggested source |
|---|---|
| MSRTC runs Nashik to Trimbakeshwar buses from the CBS (reported by erail); departure platform, frequency, fare, **last bus back** (no figure published) | MSRTC (msrtc.maharashtra.gov.in) or the CBS enquiry desk |
| Shared-jeep pickup points, frequency, fare | Local check at CBS / Trimbak bus stand |
| App-based intercity cabs (Uber lists the route) availability | Uber / Ola listing on the day |
| Whether Trimbakeshwar buses call at Panchavati bus stand | MSRTC |
| No direct rail service to Trimbakeshwar; Nashik Road is the nearest major station | Indian Railways / NTES |
| Station exits, prepaid counters (not stated on the page on purpose) | Central Railway station page; site visit |

## 3. Ramkund (page: `/blog/ramkund-ghat-nashik-guide/`)

| Claim | Suggested source |
|---|---|
| Evening Goda aarti about 7:00–8:00 PM, around sunset, varies by season | Ramkund temple trust / Nashik Municipal Corporation / nashik.gov.in; or a site visit |
| Ghat "open 24 hours" (travel listings) vs 5:30 AM to 9:30 PM (earlier copy) | Same |
| Morning aarti: no time given | Same |

## 4. Bhandardara (page: `/discover-nashik/bhandardara/`, no `data/` file; content in `tools/guides/bhandardara.py`)

| Claim | Suggested source |
|---|---|
| Arthur Lake formed by Wilson Dam on the Pravara; lake about 500 m from the bus stop | Maharashtra Tourism (maharashtratourism.gov.in/nature/bhandardara-dam/) |
| Randha Falls about 10 km; Kalsubai about 12 km, highest peak in Maharashtra | Maharashtra Tourism; Maharashtra forest department |
| From Nashik 70–73 km; Mumbai 177 km (165–185); Pune 156 km (156–191) | Maharashtra Tourism; Google Maps |
| Nearest station Igatpuri, 35–45 km; Nashik airport about 90 km | Indian Railways; AAI |
| Fireflies about May to June | Local operators; Maharashtra forest department. No official calendar found |
| District: Akole taluka, Ahilyanagar (formerly Ahmednagar) district, close to the Nashik district boundary. **Confirmed by the site owner on 22 Nov 2026**; the Igatpuri page was corrected to say Igatpuri only is in Nashik district | n/a (done) |
| Umbrella Falls visible when the dam overflows; monsoon safety advice is general, not official | Maharashtra Tourism; local police / forest notices |

## 5. Kumbh Mela (pages: Kumbh hub, e-pass guide; data: `data/facts.json`)

| Claim | Suggested source |
|---|---|
| 84 organisations registered (Sept 2026); student "Kumbhdoot" registration; optional KumbhDoot Kumbh Pass in DigiLocker (pilot planned) | The Authority's website / notices. E-pass page shows these in an "Official status as of 22 Nov 2026" box (`data/pages.json` > `officialStatus`) |
| No general-visitor pass announced (the most-read claim on the site) | Re-check the Authority's website each week; update `officialStatus.asOf` |
| Traffic, parking, shuttle, last-mile arrangements: "none announced" | Nashik police / Authority notices |

## 6. Other claims

| Item | Where | Suggested source |
|---|---|---|
| Food estimates ₹150–300 / 300–600 / 600–1,200 / 1,200–2,500 a day (labelled "not verified") | where-to-stay guide, budget section | Restaurant menus / a quick price check |
| Satkar and Kapila restaurants (earlier copy, not re-verified) | Panchavati page, food section | Site visit |
| Sula: address side (Gangapur Road), hours, tasting price | Sula page, `dest.sula.*` facts | sulawines.com |
| Quick answers on 19 guides | `data/pages.json` > `quickAnswer` | Each restates the page's own claims and hedges; read once |
| Hindi and Marathi quick-answer text | hub, `lang` blocks | Native-speaker proofread |

## 7. Owner decisions (not facts)

| Item | Where |
|---|---|
| Articles are credited to "NashikTourism.com Editorial Team" (Organization); no personal names anywhere on the site | `data/seo.json` > `author`; page `/about/editorial-team/` |
| Organization `sameAs` (social profiles). Empty, so omitted from the JSON-LD | `data/seo.json` > `organization.sameAs` |
| Sponsored-content policy (approved by the site owner 22 Nov 2026): always labelled, `rel="sponsored nofollow"`, sponsors never control facts, sponsored pages never marked Verified (enforced by `seo-check.py` and `validate-data.py`) | `tools/build-editorial-policy.py`, `data/monetization.json` |
| Audience statistics on `/advertise/` ship empty; fill from GA4 / Search Console only | `data/monetization.json` > `audienceStats` |
| `geo`, `openingHoursSpecification` and `isAccessibleForFree` were **not** added to destination schema: no verified values. Add them per destination when verified (`seo-check` blocks `isAccessibleForFree` unless you change that rule) | `data/destinations.json` |
