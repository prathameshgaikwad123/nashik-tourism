#!/usr/bin/env python3
"""
Generate the site search: /search-index.json and the /search/ page.

The index is built from the same data that builds the pages, so search can never
return something the site does not say:

    destinations    data/destinations.json
    answers         destination quick facts, data/facts.json, guide FAQ questions
    guides          posts.json
    updates         live items in data/updates.json
    events          data/events.json
    pages           hubs and their sections (Kumbh, Transport, Accessible Nashik...)

Two honesty rules:
  * an answer built from a fact repeats the fact's STATUS with its value ("Not yet
    verified", "Reported"), and an unknown value reads "Information not yet
    confirmed" — search never makes a figure look firmer than the page does
  * guide FAQs are indexed by QUESTION only; the unverified answer text is not
    repeated in a result, the result sends you to the guide

/search/ is noindex (no thin duplicate result pages in search engines) and carries
a static 'browse everything' list, so it is useful without JavaScript and every
page has an inbound link from it.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import content, pagekit, render, store  # noqa: E402
from nt.paths import ROOT  # noqa: E402

CSS = """    .sp-form { display: flex; align-items: stretch; max-width: 680px; background: #fff; border: 2px solid var(--primary); border-radius: var(--r-lg); overflow: hidden; }
    .sp-form input { flex: 1; min-width: 0; height: 52px; padding: 0 var(--s-4); border: 0; outline: 0; font-size: 1rem; font-family: var(--font-body); color: var(--ink); background: transparent; }
    .sp-form:focus-within { outline: 3px solid var(--focus-ring); outline-offset: 2px; }
    .sp-form button { flex: none; padding: 0 var(--s-5); border: 0; background: var(--primary); color: #fff; font-family: var(--font-display); font-weight: 700; font-size: 0.82rem; cursor: pointer; min-height: var(--tap); }
    #sp-results .sd-group { margin-top: var(--s-6); }
    .browse summary { display: flex; align-items: center; min-height: var(--tap); cursor: pointer; font-family: var(--font-display); font-weight: 800; font-size: 1.1rem; color: var(--ink); }
    .browse h3 { font-family: var(--font-display); font-size: 0.74rem; font-weight: 700; letter-spacing: var(--ls-eyebrow); text-transform: uppercase; color: var(--saffron-deep); margin: var(--s-6) 0 var(--s-2); }
    .browse ul { list-style: none; display: grid; gap: 0; }
    .browse li a { display: flex; align-items: center; min-height: var(--tap); color: var(--primary); text-decoration: underline; text-underline-offset: 2px; border-bottom: 1px solid var(--border); font-weight: 600; }"""

KUMBH_SECTIONS = [
    ("at-a-glance", "Kumbh Mela at a glance", "What the Simhastha is, where, when, whether you need a pass and how to get there.", "kumbh simhastha mela overview what is when where"),
    ("dates", "Kumbh 2027 dates and calendar", "Reported opening, closing and Amrit Snan dates, each marked as reported until the Authority's notice is linked.", "kumbh dates calendar snan amrit shahi schedule 2027 2 august 31 august 11 september"),
    ("locations", "Ramkund and Kushavarta: the two Kumbh locations", "The Mela spans Ramkund in Nashik and Kushavarta Tirtha at Trimbakeshwar.", "ramkund kushavarta trimbakeshwar locations ghat"),
    ("getting-here", "Getting to the Kumbh", "Rail, road and air, and what special services have and have not been announced.", "kumbh transport reach trains buses special trains shuttle how to reach"),
    ("passes", "Kumbh passes and registration", "No general-visitor pass has been announced in sources we could locate; what has been reported.", "kumbh pass epass e-pass registration permit entry free charge"),
    ("parking-roads", "Kumbh parking, roads and traffic", "No official parking or traffic plan has been located; where to check.", "kumbh parking roads traffic diversion vehicle restriction"),
    ("stay", "Where to stay for the Kumbh", "Areas and options, and how to book.", "kumbh hotel stay accommodation dharamshala lodging"),
    ("safety", "Kumbh safety, medical and emergencies", "112 is India's emergency number; Mela arrangements will be set by the Authority and police.", "kumbh safety medical emergency hospital police help 112"),
    ("tips", "Practical tips for crowded days", "General advice for large gatherings.", "kumbh tips crowd packing"),
    ("accessibility", "Accessibility at the Kumbh", "Steps, toilets and assistance: what we have and have not verified.", "kumbh accessibility wheelchair senior disabled"),
    ("guides", "Kumbh guides for every kind of visitor", "Guides for pilgrims, families, seniors, women, international and budget visitors.", "kumbh guides senior women international budget solo"),
    ("figures", "Kumbh figures: attendance and spending", "Attendance and development figures differ by source; each is shown with its scope.", "kumbh budget crore attendance visitors crowd estimate infrastructure"),
    ("faqs", "Kumbh frequently asked questions", "Short answers about dates, charges, passes, safety and foreign visitors.", "kumbh faq questions"),
]

STATIC_PAGES = [
    ("/", "Nashik Tourism home", "An independent, verified guide to Nashik and the Kumbh Mela.", "home nashik guide", "Page"),
    ("/discover-nashik/", "Discover Nashik: all destinations", "Temples, ghats, vineyards, caves and the Western Ghats.", "discover destinations places attractions", "Page"),
    ("/plan-your-trip/", "Plan your trip to Nashik", "Itineraries for one, two and three days.", "plan trip itinerary days", "Page"),
    ("/blog/", "All Nashik travel guides", "Every guide on the site.", "guides blog articles", "Page"),
    ("/updates/", "Verified updates", "Short verified notices with sources.", "updates news notices latest advisory", "Page"),
    ("/updates/archive/", "Update archive", "Expired and superseded notices.", "archive old updates", "Page"),
    ("/events/", "Events in Nashik", "What's on, with sources.", "events festival whats on programme", "Page"),
    ("/nashik-now/", "Nashik Now", "Weather, updates and what's on right now.", "now today weather current live", "Page"),
    ("/transport/", "Transport hub", "How to reach and get around Nashik.", "transport reach air train bus road", "Page"),
    ("/accessible-nashik/", "Accessible Nashik", "Accessibility information, verified honestly.", "accessible accessibility wheelchair senior step-free toilets", "Page"),
    ("/kumbh-mela-2027/", "Nashik Kumbh Mela 2027 guide", "The Simhastha Kumbh Mela at Nashik and Trimbakeshwar.", "kumbh simhastha mela 2027", "Page"),
    ("/kumbh-mela-2027/live-updates/", "Kumbh live updates", "Verified Kumbh notices.", "kumbh live updates news", "Page"),
    ("/sources/", "Our sources", "The official sources behind this site.", "sources official links", "Page"),
    ("/editorial-policy/", "Editorial policy", "How we verify, label and correct information.", "editorial policy verification corrections ai sponsored", "Page"),
    ("/about/", "About NashikTourism.com", "Who we are.", "about", "Page"),
    ("/contact/", "Contact us", "Report an error or ask a question.", "contact corrections feedback", "Page"),
    ("/disclaimer/", "Disclaimer", "What this site is and is not.", "disclaimer", "Page"),
]


def plain_title(t):
    return render.plain(t.split("|")[0]).strip()


def faq_questions(slug):
    path = os.path.join(ROOT, "blog", slug, "index.html")
    if not os.path.isfile(path):
        return []
    html = open(path, encoding="utf-8").read()
    m = re.search(r'<h2[^>]*id="frequently-asked-questions"[^>]*>.*?</h2>(.*?)(?=<h2|</article>)', html, re.S)
    if not m:
        return []
    return [render.plain(q) for q in re.findall(r"<h3[^>]*>(.*?)</h3>", m.group(1), re.S)]


def build_docs():
    docs = []

    def add(t, u, k, s="", x="", m="", w=1.0):
        docs.append({"t": t, "u": u, "k": k, "s": s, "x": x, "m": m, "w": w})

    facts = render.facts_index()
    dests = store.load("destinations")["destinations"]
    for d in dests:
        name = render.plain(d["name"])
        base = "/discover-nashik/%s/" % d["slug"]
        add(name, base, "destination", render.plain(d["lede"]),
            " ".join(d.get("tags", []) + d["category"] + [render.plain(d["where"]), "guide visit places"]),
            "Destination · " + ", ".join(c.title() for c in d["category"]), 1.0)
        for label, field, kw in [("opening hours", "timings", "timing timings hours open opening darshan time"),
                                 ("entry fee", "entryFee", "entry fee ticket price cost charges")]:
            v = d.get(field)
            if isinstance(v, dict) and "$fact" in v and v["$fact"] in facts:
                f = facts[v["$fact"]]
                s = "%s — %s" % (f["display"], render.FACT_BADGES[f["status"]][1])
            else:
                s = "Information not yet confirmed. Check with the official source before travelling."
            add("%s: %s" % (name, label), base + "#quick-facts", "answer", s, kw + " " + name.lower(), "Answer · " + name, 1.0)
        tr = d.get("transport") or {}
        parts = []
        for k in ("fromNashikDistance", "fromNashikTime"):
            v = tr.get(k)
            if isinstance(v, dict) and "$fact" in v and v["$fact"] in facts:
                parts.append(facts[v["$fact"]]["display"])
        add("%s: how to reach it from Nashik" % name, base + "#how-to-reach", "answer",
            (", ".join(parts) + " — not yet verified") if parts else "See the page for how to reach it; distances have not been verified.",
            "reach distance route getting from nashik travel " + name.lower(), "Answer · " + name, 0.9)

    posts = json.load(open(os.path.join(ROOT, "posts.json"), encoding="utf-8"))
    for p in posts:
        add(plain_title(p["title"]), "/blog/%s/" % p["slug"], "guide", render.plain(p["excerpt"]),
            p.get("category", "") + " " + p["slug"].replace("-", " "),
            "Guide · %s · %s" % (p.get("category", ""), render.fmt_date(p.get("date"), short=True)), 1.0)
        for q in faq_questions(p["slug"]):
            add(q, "/blog/%s/#frequently-asked-questions" % p["slug"], "answer",
                "Covered in the guide: %s. The answer in that guide has not been verified against official sources." % plain_title(p["title"]),
                p["slug"].replace("-", " "), "From a guide · not yet verified", 0.7)

    for u in content.live_updates():
        add(u["title"], "/updates/#u-" + u["id"], "update", u["summary"], " ".join(u.get("tags", [])) + " " + u["category"].lower(),
            "Update · %s · %s" % (render.UPDATE_BADGES[render.effective_status(u)][1], render.fmt_date(u["publishedAt"], short=True)), 1.1)
    upcoming, past = content.events()
    for e in upcoming + past:
        add(e["title"], "/events/#e-" + e["id"], "event", "%s. %s" % (render.fmt_date(e["date"], weekday=True), e["description"]),
            " ".join(e.get("tags", [])) + " " + e["category"].lower() + " " + e["location"].lower(),
            "Event · %s · %s" % (render.fmt_date(e["date"], short=True), "Verified" if e.get("verificationStatus") == "verified" else "Reported, not yet confirmed"), 1.05)

    # Facts as answers — each shows its status next to the value.
    tsecs = store.load("transport")["sections"]
    fact_page = {}
    for s in tsecs:
        for fid in s.get("facts", []):
            fact_page.setdefault(fid, "/transport/#" + s["id"])
    kumbh_anchor = {"kumbh.mela.opening": "dates", "kumbh.mela.closing": "dates", "kumbh.attendance.estimate": "figures",
                    "kumbh.devplan.amount": "figures", "kumbh.rail.invest": "figures", "kumbh.rail.stations": "getting-here",
                    "kumbh.authority.exists": "at-a-glance", "kumbh.pass.general": "passes", "kumbh.portal.status": "passes",
                    "kumbh.entry.charge": "passes", "kumbh.parking.plan": "parking-roads", "kumbh.transport.special-services": "getting-here",
                    "safety.emergency.number": "safety"}
    for fid, f in facts.items():
        if fid.startswith("dest."):
            continue
        if fid.startswith("kumbh.snan"):
            anchor = "dates"
        else:
            anchor = kumbh_anchor.get(fid)
        url = ("/kumbh-mela-2027/#" + anchor) if anchor else fact_page.get(fid)
        if not url:
            continue
        add("%s: %s" % (f["subject"], f["fact"].lower() if f["fact"][:2].isupper() is False else f["fact"]), url, "answer",
            "%s — %s" % (f["display"] or "Information not yet confirmed", render.FACT_BADGES[f["status"]][1]),
            f["subject"].lower() + " " + f["id"].replace(".", " "), "Answer · " + render.FACT_BADGES[f["status"]][1], 1.0)

    for anchor, title, summary, kw in KUMBH_SECTIONS:
        add(title, "/kumbh-mela-2027/#" + anchor, "page", summary, kw, "Kumbh hub section", 1.0)
    for s in tsecs:
        add("Transport: " + s["title"], "/transport/#" + s["id"], "page", s["summary"], "transport " + s["id"] + " " + s["title"].lower(), "Transport hub section", 1.0)
    for t in store.load("accessibility")["topics"]:
        add("Accessible Nashik: " + t["title"], "/accessible-nashik/#" + t["id"], "page", t["intro"], "accessible accessibility " + t["id"], "Accessibility hub section", 0.95)
    for u, t, s, kw, m in STATIC_PAGES:
        add(t, u, "page", s, kw, m, 0.95)
    return docs


def browse_html(docs):
    by = {"destination": [], "guide": [], "page": []}
    seen = set()
    for d in docs:
        if d["k"] in by and d["u"] not in seen and "#" not in d["u"]:
            seen.add(d["u"])
            by[d["k"]].append(d)
    labels = {"page": "Hubs and pages", "destination": "Destinations", "guide": "Guides"}
    parts = []
    for k in ("page", "destination", "guide"):
        items = sorted(by[k], key=lambda d: d["t"]) if k != "page" else by[k]
        parts.append("<h3>%s</h3><ul>%s</ul>" % (labels[k], "".join('<li><a href="%s">%s</a></li>' % (render.esc(d["u"]), render.esc(d["t"])) for d in items)))
    return "".join(parts)


def main():
    docs = build_docs()
    built = store.now()
    index = {"v": 1, "built": built.date().isoformat(), "docs": docs}
    with open(os.path.join(ROOT, "search-index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False, separators=(",", ":"))
    size = os.path.getsize(os.path.join(ROOT, "search-index.json"))

    head = pagekit.page_head("Search Nashik", "Destinations, guides, verified updates, events and short answers &mdash; one search.",
                             crumbs=[("Home", "/"), ("Search", None)], eyebrow="Search")
    body = head + """
<section class="sec"><div class="inner">
  <form class="sp-form" role="search" action="/search/" method="get" data-search-page>
    <label for="sp-input" class="sr-only">What are you looking for in Nashik?</label>
    <input id="sp-input" name="q" type="search" placeholder="What are you looking for in Nashik?" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search" />
    <button type="submit">Search</button>
  </form>
  <p class="sr-only" id="sp-status" role="status" aria-live="polite"></p>
  <div id="sp-results" style="margin-top:var(--s-4);"></div>
  <noscript><p class="sec-sub" style="margin-top:var(--s-4);">Search needs JavaScript. You can still browse every page below.</p></noscript>
  <details class="browse" id="browse" open style="margin-top:var(--s-8);">
    <summary>Browse everything</summary>
    %s
  </details>
</div></section>
""" % browse_html(docs)
    html = pagekit.render(
        "/search/", "Search Nashik", "Search NashikTourism.com: destinations, guides, verified updates, events and short answers about Nashik and the Kumbh Mela.",
        body, crumbs=[("Home", "/"), ("Search", "/search/")], css=CSS, robots="noindex, follow")
    pagekit.write("/search/", html)
    print("search index: %d docs, %.1f KB; /search/ built" % (len(docs), size / 1024.0))


if __name__ == "__main__":
    main()
