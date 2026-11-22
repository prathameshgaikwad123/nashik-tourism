#!/usr/bin/env python3
"""
Build /about/editorial-team/ (who writes the guides and how they are researched and checked;
no personal names appear anywhere on the site) and /advertise/.

/advertise/ renders audience statistics only when they are filled in
data/monetization.json; nothing is hard-coded here.

    python3 tools/build-about-pages.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import aeo, pagekit, store  # noqa: E402
from nt.paths import SITE  # noqa: E402
from nt.render import esc, fmt_date  # noqa: E402

CSS = """    .doc { max-width: 760px; margin: 0 auto; padding: var(--s-10) var(--gutter) var(--s-16); }
    .doc h2 { font-family: var(--font-display); font-size: 1.25rem; font-weight: 800; color: var(--ink); margin: var(--s-10) 0 var(--s-3); padding-bottom: var(--s-2); border-bottom: 2px solid var(--border); }
    .doc p, .doc li { color: var(--body-clr); line-height: var(--lh-prose); }
    .doc ul { margin: 0 0 var(--s-4) 1.3rem; }
    .doc a { color: var(--primary); text-decoration: underline; text-underline-offset: 2px; }"""


def editorial_team_page():
    a = aeo.author()
    pages = store.load("pages")["pages"]
    import json
    with open(os.path.join(pagekit.ROOT, "posts.json"), encoding="utf-8") as fh:
        posts = {"/blog/%s/" % p["slug"]: p for p in json.load(fh)}
    labels = {"/transport/nashik-road-station-to-trimbakeshwar/": "Nashik Road station to Trimbakeshwar",
              "/transport/trimbakeshwar-to-panchavati-ramkund/": "Trimbakeshwar to Panchavati and Ramkund",
              "/discover-nashik/bhandardara/": "Bhandardara guide"}
    items = []
    for path, meta in sorted(pages.items(), key=lambda kv: aeo.modified_for(kv[0], kv[1]) or "", reverse=True):
        if meta.get("template") != "article":
            continue
        title = labels.get(path) or (posts.get(path, {}).get("title") or path).split("|")[0].strip()
        items.append('<li><a href="%s">%s</a> <span class="muted">(updated %s)</span></li>' % (esc(path), esc(title), esc(fmt_date(aeo.modified_for(path, meta), short=True))))
    body = pagekit.page_head(a["name"], "How the guides on NashikTourism.com are researched, checked and updated.",
                             crumbs=[("Home", "/"), ("About", "/about/"), ("Editorial team", None)], eyebrow="About this site") + """
<section class="sec"><div class="inner"><div class="doc">
  <h2 id="who-we-are">Who writes the guides</h2>
  <p>The guides on NashikTourism.com are written and maintained by the <strong>NashikTourism.com Editorial Team</strong>. We are an independent travel and information guide to Nashik and Trimbakeshwar. We are not a government body, a temple trust, the Nashik&ndash;Trimbakeshwar Kumbh Mela Authority or an official tourism organisation, and we say so on every page.</p>
  <h2 id="how-we-research">How we research</h2>
  <ul>
    <li><strong>Official sources first.</strong> Government bodies, the Authority, the railways, MSRTC, the police and an attraction&rsquo;s own site rank above news, and news ranks above travel blogs. The full registry, by tier, is on <a href="/sources/">our sources page</a>.</li>
    <li><strong>A report is not a fact.</strong> A news report becomes a fact on this site only when an official source supports it. Until then it is labelled <em>Reported</em>.</li>
    <li><strong>We show disagreements.</strong> When sources give different figures (distances are a common case) we show all of them and label the row <em>Sources differ</em> rather than picking one.</li>
  </ul>
  <h2 id="how-we-verify">How we verify</h2>
  <p>Every claim that matters carries its own status: <strong>Verified</strong> (an editor read the cited source and it supports the claim, with the date), <strong>Reported</strong>, <strong>Sources differ</strong> or <strong>Not yet verified</strong>. Anything that could hurt a traveller if it were wrong needs a named human approver before it is published. The rules are on the <a href="/editorial-policy/">editorial policy</a> page and are enforced by the site&rsquo;s build, not just stated.</p>
  <h2 id="how-we-update">How we keep guides current</h2>
  <p>Each guide shows a <em>Last updated</em> date and a <em>Last verified</em> date. Time-sensitive notices expire and move to the <a href="/updates/archive/">archive</a>. Changes are logged on each page&rsquo;s change history.</p>
  <h2 id="sponsored-content">Sponsored content</h2>
  <p>Sponsored content is always labelled, links in it use <code>rel="sponsored nofollow"</code>, sponsors have no control over facts, and a sponsored page is never marked Verified. See the <a href="/editorial-policy/#sponsored">sponsored-content policy</a>.</p>
  <h2 id="guides">Guides maintained by the team</h2>
  <ul>%(items)s</ul>
  <h2 id="contact">Corrections and contact</h2>
  <p>Found a mistake or an out-of-date figure? <a href="/contact/?topic=content">Tell us</a>, with the official source if you have it. Corrections are logged on the <a href="/editorial-policy/#corrections">editorial policy page</a>.</p>
</div></div></section>
""" % {"items": "".join(items)}
    ld = [{"@type": "AboutPage", "@id": SITE + a["path"] + "#webpage", "url": SITE + a["path"], "name": a["name"],
           "about": {"@id": aeo.ORG_ID}, "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "en-IN"},
          aeo.organization_ld()]
    html = pagekit.render(a["path"], "Editorial team: how NashikTourism.com researches and verifies",
                          "How the NashikTourism.com Editorial Team researches, verifies and updates its Nashik guides: official sources first, a status on every claim, dated updates and logged corrections.",
                          body, crumbs=[("Home", "/"), ("About", "/about/"), ("Editorial team", a["path"])], css=CSS, jsonld=ld, raw_title=True,
                          page_type="AboutPage")
    pagekit.write(a["path"], html)


def advertise_page():
    cfg = aeo.money()
    stats = cfg["audienceStats"]
    items = [s for s in stats.get("items", []) if s.get("value") not in (None, "")]
    if items:
        cells = "".join('<div class="adv-stat"><b>%s</b><span>%s%s%s</span></div>' % (
            esc(s["value"]), esc(s["label"]), (", " + esc(s["period"])) if s.get("period") else "",
            (" &middot; source: " + esc(s["source"])) if s.get("source") else "") for s in items)
        asof = (" As of %s." % esc(fmt_date(stats["asOf"], short=True))) if stats.get("asOf") else ""
        stats_html = '<div class="adv-stats">%s</div><p class="matrix-note">Figures supplied by the site owner from the named source.%s</p>' % (cells, asof)
    else:
        stats_html = ('<p class="placeholder-note">Audience statistics will be published here once they are confirmed from our analytics and '
                      'Search Console. We do not quote traffic numbers we have not measured. Ask us for current figures when you enquire.</p>')
    fm = "".join('<div class="adv-card"><h3>%s</h3><p>%s</p></div>' % (esc(f["name"]), esc(f["text"])) for f in cfg["advertise"]["formats"])
    body = pagekit.page_head("Advertise with NashikTourism.com",
                             "Reach people planning a trip to Nashik, Trimbakeshwar and the Simhastha Kumbh Mela 2026&ndash;28, with clear labelling and editorial independence.",
                             crumbs=[("Home", "/"), ("Advertise", None)], eyebrow="Partnerships") + """
<section class="sec"><div class="inner"><div class="doc">
  <h2 id="audience">Who reads the site</h2>
  <p>NashikTourism.com is an independent, source-checked guide. Its readers are mainly:</p>
  <ul>
    <li><strong>Pilgrims</strong> visiting Trimbakeshwar, Ramkund and the other temples and ghats.</li>
    <li><strong>Kumbh Mela 2027 visitors</strong> planning transport, stays, dates and passes.</li>
    <li><strong>Weekend travellers from Mumbai and Pune</strong> looking at vineyards, hill country and day trips.</li>
  </ul>
  %(stats)s

  <h2 id="formats">What you can sponsor</h2>
  <div class="adv-grid">%(formats)s</div>

  <h2 id="independence">Editorial independence and labelling</h2>
  <ul>
    <li><strong>Sponsored content is always labelled</strong> with a visible <span class="sponsored-label">Sponsored</span> tag and a disclosure line on the page.</li>
    <li><strong>Outbound links in sponsored content</strong> use <code>rel="sponsored nofollow"</code>.</li>
    <li><strong>Sponsors never control the facts.</strong> They cannot buy editorial rankings, recommendations or a change to a figure. Guides, distances and dates stay under the <a href="/editorial-policy/">editorial policy</a>, with the same sourcing rules, and sponsors get no preview or veto of editorial pages that mention them.</li>
    <li><strong>A sponsored page is never marked Verified.</strong> The &ldquo;Verified&rdquo; status is reserved for claims an editor has checked against an official source.</li>
    <li>We will decline anything that could mislead a traveller: unverified claims, unsafe advice, or a fake &ldquo;pass&rdquo; or booking for the Mela.</li>
    <li>Affiliate links to booking sites are marked as sponsored; see the <a href="/editorial-policy/#sponsored">disclosure</a>.</li>
  </ul>

  <h2 id="contact">Get in touch</h2>
  <p>Tell us what you offer, who it is for and the dates you have in mind. We reply to every enquiry that fits the rules above.</p>
  <p><a class="btn btn-purple" href="%(contact)s">Enquire about advertising</a></p>
</div></div></section>
""" % {"stats": stats_html, "formats": fm, "contact": esc(cfg["advertise"]["contact"])}
    html = pagekit.render("/advertise/", "Advertise with NashikTourism.com",
                          "Sponsored guides, featured listings and Kumbh-season placements on an independent Nashik guide. Clear labelling, editorial independence, no unmeasured traffic claims.",
                          body, crumbs=[("Home", "/"), ("Advertise", "/advertise/")], css=CSS, raw_title=True)
    pagekit.write("/advertise/", html)


if __name__ == "__main__":
    editorial_team_page()
    advertise_page()
    print("built /about/editorial-team/ and /advertise/")
