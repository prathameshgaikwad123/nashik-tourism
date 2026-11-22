#!/usr/bin/env python3
"""
Build /about/prathamesh/ (the Person entity behind every byline) and /advertise/.

The author bio is a clearly marked placeholder until the owner sets author.bioApproved
and author.bio in data/seo.json: no personal claims are written on anyone's behalf.
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


def author_page():
    a = aeo.author()
    pages = store.load("pages")["pages"]
    import json
    with open(os.path.join(pagekit.ROOT, "posts.json"), encoding="utf-8") as fh:
        posts = {"/blog/%s/" % p["slug"]: p for p in json.load(fh)}
    items = []
    for path, meta in sorted(pages.items(), key=lambda kv: aeo.modified_for(kv[0], kv[1]) or "", reverse=True):
        if meta.get("template") != "article":
            continue
        title = (posts.get(path, {}).get("title") or path).split("|")[0].strip()
        if path.startswith("/transport/") or path.startswith("/discover-nashik/"):
            title = {"/transport/nashik-road-station-to-trimbakeshwar/": "Nashik Road station to Trimbakeshwar",
                     "/transport/trimbakeshwar-to-panchavati-ramkund/": "Trimbakeshwar to Panchavati and Ramkund",
                     "/discover-nashik/bhandardara/": "Bhandardara guide"}.get(path, title)
        items.append('<li><a href="%s">%s</a> <span class="muted">(updated %s)</span></li>' % (esc(path), esc(title), esc(fmt_date(aeo.modified_for(path, meta), short=True))))
    if a.get("bioApproved") and a.get("bio"):
        bio = "<p>%s</p>" % esc(a["bio"])
    else:
        bio = ('<p class="placeholder-note"><strong>Bio to be added by the editor.</strong> '
               'This placeholder is intentionally empty of personal details until %s approves the text. '
               'Nothing on this page is a claim about their background or qualifications.</p>' % esc(a["name"]))
    body = pagekit.page_head(a["name"], "%s of NashikTourism.com, based in Nashik, Maharashtra." % esc(a["jobTitle"]),
                             crumbs=[("Home", "/"), ("About", "/about/"), (a["name"], None)], eyebrow="Author") + """
<section class="sec"><div class="inner"><div class="doc">
  <h2 id="about-the-author">About %(name)s</h2>
  <p>%(name)s is the %(role)s of NashikTourism.com and is named as the author of its guides. Based in %(home)s.</p>
  %(bio)s
  <h2 id="how-this-site-checks-facts">How the guides are checked</h2>
  <p>Every guide follows the site&rsquo;s <a href="/editorial-policy/">editorial policy</a>: official sources first, a visible status on every claim (Verified, Reported, Sources differ or Not yet verified), a named source for each, and a &ldquo;Last updated&rdquo; and &ldquo;Last verified&rdquo; date. See <a href="/sources/">the source registry</a>. NashikTourism.com is independent and not affiliated with any government body, temple trust or the Kumbh Mela Authority.</p>
  <h2 id="guides">Guides by %(name)s</h2>
  <ul>%(items)s</ul>
  <h2 id="contact">Corrections and contact</h2>
  <p>Found a mistake or an out-of-date figure? <a href="/contact/?topic=content">Tell us</a>, with the official source if you have it. Corrections are logged on the <a href="/editorial-policy/#corrections">editorial policy page</a>.</p>
</div></div></section>
""" % {"name": esc(a["name"]), "role": esc(a["jobTitle"].lower()), "home": esc(a["homeLocation"]), "bio": bio, "items": "".join(items)}
    person = aeo.person_ld()
    person["mainEntityOfPage"] = {"@id": SITE + a["path"] + "#profile"}
    ld = [{"@type": "ProfilePage", "@id": SITE + a["path"] + "#profile", "url": SITE + a["path"], "name": a["name"],
           "mainEntity": {"@id": person["@id"]}, "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "en-IN"},
          person, aeo.organization_ld()]
    html = pagekit.render(a["path"], "%s, %s at NashikTourism.com" % (a["name"], a["jobTitle"]),
                          "%s is the %s of NashikTourism.com, an independent Nashik travel guide. Author profile and list of guides." % (a["name"], a["jobTitle"].lower()),
                          body, crumbs=[("Home", "/"), ("About", "/about/"), (a["name"], a["path"])], css=CSS, jsonld=ld, raw_title=True,
                          page_type="ProfilePage")
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
    <li><strong>Sponsors do not buy editorial rankings, verification or recommendations.</strong> Guides, distances, dates and facts stay under the <a href="/editorial-policy/">editorial policy</a>, with the same sourcing rules.</li>
    <li><strong>Sponsors get no preview or veto</strong> of editorial pages that mention them.</li>
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
    author_page()
    advertise_page()
    print("built /about/prathamesh/ and /advertise/")
