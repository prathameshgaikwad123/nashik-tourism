# VERIFY.md: figures and claims to confirm in one pass

Created in the SEO/AEO sprint (22 Nov 2026). **Nothing below is marked "Verified" on the site.** The official pages (nashik.gov.in, MSRTC, Indian Railways, NHAI, the Kumbh Authority) could not be opened from the build environment, so every figure comes from search-result text and is shown as *Reported*, *Sources differ* or *Not yet verified*. Each item below has a matching `<!-- VERIFY: ... -->` comment in the page source.

**To verify an item:** open the suggested source, read it, then update the data file named in the last column (set `status` to `verified`, plus `verifiedBy`, `verifiedAt` and the source URL; `python3 tools/cms.py fact verify <id> ...` works for facts). Rebuild with `python3 tools/build-all.py`. The status chip on the page changes by itself.

## 1. Distances (page: `/blog/trimbakeshwar-to-nashik-distance-route/` and both transport guides; data: `data/distances.json`)

| Figure | Currently shown | Suggested source / how |
|---|---|---|
| Trimbakeshwar from Nashik CBS | About 28–30 km (reported) | Google Maps shortest common road route, CBS to Trimbakeshwar Temple; note the date. Also read the Trimbakeshwar page on nashik.gov.in |
| From Nashik Road railway station | About 36–40 km (reported) | Google Maps; nashik.gov.in "how to reach" |
| Drive time CBS to Trimbakeshwar | 45–60 minutes (earlier site estimate, not verified) | Google Maps typical-traffic range; say which time of day |
| Ramkund / Panchavati to Trimbakeshwar | About 28–30 km (no separate figure) | Google Maps from Ramkund |
| Tapovan, Kapaleshwar, Sula Vineyards, Igatpuri | Not yet confirmed | Google Maps |
| Nashik (Ozar) airport | About 40–55 km (sources differ) | Google Maps; AAI page; also confirm which scheduled flights operate |
| Mumbai, Pune, Shirdi | 166–193 / 209–240 / 76–125 km (sources differ) | Google Maps, NHAI route; Shirdi range is too wide to be useful |
| Ramkund is about 2 km from the CBS | Reported (travel listings) | Google Maps |
| Panchavati to Nashik Road station | 14 km (district site) vs 8 km (earlier copy): disputed | Google Maps; fact `transport.nashik-road.distance` |
| Kalaram, Sita Gufa, Sundarnarayan distances from the CBS | 2.5–3, 2.7, 2 km (reported) | nashik.gov.in places of interest; Google Maps |
| `dest.trimbakeshwar.distance` (fact) | About 28–30 km (reported) | as above; `python3 tools/cms.py fact verify dest.trimbakeshwar.distance ...` |

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
| **Which district Bhandardara is in.** The page says only "close to the Nashik district boundary". It is believed to be in Akole taluka, Ahilyanagar (formerly Ahmednagar) district. The Igatpuri page (`data/destinations.json`, `igatpuri`) still says both places are "in Nashik district"; correct it once confirmed | District gazetteer / Maharashtra Tourism |
| Umbrella Falls visible when the dam overflows; monsoon safety advice is general, not official | Maharashtra Tourism; local police / forest notices |

## 5. Kumbh Mela (pages: Kumbh hub, e-pass guide; data: `data/facts.json`)

| Claim | Suggested source |
|---|---|
| All six Kumbh dates (`kumbh.mela.opening`, `kumbh.snan.1`, `.2`, `.3.nashik`, `.3.trimbak`, `kumbh.mela.closing`) are *Reported*. **Verifying these unlocks `Event` rich results on `/events/`** (the page emits Event JSON-LD only for events an editor has verified; Search Console currently shows 0) | The Authority's own notice (divcomnashik.maharashtra.gov.in / the official Simhastha website) or the Maharashtra government GR |
| Official Simhastha website live; address reported as `simhasthamahakumbh.maharashtra.gov.in` (source `ntka-portal`, `urlStatus: to_be_confirmed`) | Open it; match the address to the Authority's own social channels; then set `urlStatus: ok` |
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
| Author name shown as "Prathamesh Gaikwad" (taken from the repository owner's handle; confirm spelling), the placeholder bio, and `sameAs` links | `data/seo.json` > `author`; page `/about/prathamesh/` |
| Organization `sameAs` (social profiles). Empty, so omitted from the JSON-LD | `data/seo.json` > `organization.sameAs` |
| Sponsored-content wording on `/editorial-policy/#sponsored` and the new `/advertise/` page. The previous policy said paid editorial was not accepted; the new wording permits **labelled** sponsored content. Confirm this is the policy you want | `tools/build-editorial-policy.py`, `data/monetization.json` |
| Audience statistics on `/advertise/` ship empty; fill from GA4 / Search Console only | `data/monetization.json` > `audienceStats` |
| `geo`, `openingHoursSpecification` and `isAccessibleForFree` were **not** added to destination schema: no verified values. Add them per destination when verified (`seo-check` blocks `isAccessibleForFree` unless you change that rule) | `data/destinations.json` |
