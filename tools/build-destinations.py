#!/usr/bin/env python3
"""
Generate the Discover Nashik section and the Plan Your Trip hub from one
shared template and one set of page chrome (nav / footer / scripts).

Phase 1 scope: replace the developer scratch stubs with a real, reusable
destination-page structure — hero, breadcrumbs, in-page nav, editorial
sections, internal linking, FAQs and schema.

FACTUAL DISCIPLINE
------------------
Every fact-shaped value comes from data/destinations.json / data/facts.json and
is shown with its verification status. A null field renders as "Not yet
confirmed" with a pointer to the official source — never a guess. Descriptive
copy (why visit, history, what to see) is editorial, not a factual claim. Each
page ends with its sources, its verification status and its change history.

Usage:  python3 tools/build-destinations.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome
from nt import content, render, store

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "nashiktourism"))
SITE = "https://nashiktourism.com"
CLD = "https://res.cloudinary.com/duhuxaukd/image/upload"

# Categories used by the destination explorer. Only assigned where the
# destination's own published copy supports it — see the note in
# build_discover_hub(). Adventure and Weekend Getaway are deliberately absent:
# the audit found zero and one supporting destination respectively.
CATEGORY_LABELS = {
    "spiritual": "Spiritual",
    "heritage": "Heritage",
    "nature": "Nature",
    "wine": "Wine",
}
# ─────────────────────────────────────────────────────────────────────────────
# DESTINATIONS now live in data/destinations.json — one structured record per
# place, reused by these pages, the Discover hub, search, structured data and the
# accessibility hub. Unknown fields are null and render as "Information not yet
# confirmed"; they are never filled with a guess. Prose fields are HTML fragments.
# ─────────────────────────────────────────────────────────────────────────────
def _load_destinations():
    out = []
    for r in store.load("destinations")["destinations"]:
        d = dict(r)
        d["meta"] = r["description"]
        d["nearby"] = r["nearbyPlaces"]
        d["related"] = [tuple(x) for x in r["related"]]
        d["faqs"] = [tuple(x) for x in r["faqs"]]
        out.append(d)
    return out


DESTINATIONS = _load_destinations()
# Category assignments and the contextual next step are fields of the record.
DEST_CATEGORIES = {d["slug"]: d["category"] for d in DESTINATIONS}
PLAN_NEXT = {d["slug"]: tuple(d["planNext"]) for d in DESTINATIONS}

BY_SLUG = {d["slug"]: d for d in DESTINATIONS}



# ─────────────────────────────────────────────────────────────────────────────
# Phase 4 — data-driven sections: quick facts, how to reach, during Kumbh,
# accessibility, latest updates, sources and verification.
# ─────────────────────────────────────────────────────────────────────────────
_FACTS = render.facts_index()
_SOURCES = render.sources_index()
_ACCESS = {p["slug"]: p for p in store.load("accessibility")["places"]}


def _resolve(value):
    """A record field -> (html, status). None -> not confirmed."""
    if value is None:
        return '<span class="unconfirmed">Not yet confirmed</span>', None
    if isinstance(value, dict) and "$fact" in value:
        f = _FACTS[value["$fact"]]
        return render.fact_value_html(f), f["status"]
    if isinstance(value, dict) and "sourceId" in value:
        s = _SOURCES[value["sourceId"]]
        host = re.sub(r"^https?://(www\.)?|/$", "", s["url"] or "")
        return render.ext_link(s["url"], render.esc(host) + " (official site)", item=value["sourceId"]), "reported"
    return render.esc(value), "not_verified"


def quick_facts_html(d):
    cells = []

    def cell(label, html, status=None, badge=True):
        b = ('<div class="qf-b">%s</div>' % render.fact_badge(status)) if (status and badge) else ""
        cells.append('<div class="qf-item"><dt>%s</dt><dd>%s%s</dd></div>' % (label, html, b))

    loc = d.get("location") or {}
    cell("Location", render.esc(loc.get("summary") or d["where"]))
    tr = d.get("transport") or {}
    dist, dst = _resolve(tr.get("fromNashikDistance"))
    jt, jst = _resolve(tr.get("fromNashikTime"))
    if tr.get("fromNashikDistance") or tr.get("fromNashikTime"):
        both = " &middot; ".join(x for x, v in ((dist, tr.get("fromNashikDistance")), (jt, tr.get("fromNashikTime"))) if v)
        cell("From Nashik city", both, dst or jst)
    for label, key in (("Timings", "timings"), ("Entry", "entryFee")):
        h, st = _resolve(d.get(key))
        cell(label, h, st)
    h, st = _resolve(d.get("recommendedDuration"))
    cell("Recommended duration", h, st)
    acc = _ACCESS.get(d["slug"])
    cell("Accessibility", ('<a href="#accessibility">%s</a>' % render.access_badge(acc["status"])) if acc else '<span class="unconfirmed">Not yet confirmed</span>')
    h, st = _resolve(d.get("parking"))
    cell("Parking", h, st)
    h, st = _resolve(d.get("officialWebsite"))
    cell("Official website", h if d.get("officialWebsite") else '<span class="unconfirmed">Not yet confirmed</span>', st if d.get("officialWebsite") else None)

    lv = d.get("lastVerified")
    verified = ("Information verified: %s" % render.time_tag(lv)) if lv else "Information verified: not yet &mdash; see <a href=\"#verification\">sources and verification</a>"
    return """      <div id="quick-facts" class="qf-wrap">
      <dl class="quick-facts" aria-label="Quick facts">
        %s
      </dl>
      <p class="qf-verified">%s. Timings may change during festivals. Confirm before travelling. <a href="/sources/">Check with the official authority.</a></p>
      </div>""" % ("\n        ".join(cells), verified)


def reach_extra_html(d):
    tr = d.get("transport") or {}
    rows = []
    for label, key in (("Distance from Nashik city", "fromNashikDistance"), ("Journey time from Nashik city", "fromNashikTime")):
        v = tr.get(key)
        if v:
            h, st = _resolve(v)
            rows.append("<li><span class=\"t-fl\">%s</span> <span class=\"t-fv\">%s</span> %s</li>" % (label, h, render.fact_badge(st) if st else ""))
    if not rows:
        return '<p class="prose"><span class="unconfirmed">Distance and journey time from Nashik city: not yet confirmed.</span> See the <a href="/transport/">transport hub</a> and the <a href="/blog/how-to-reach-nashik-for-kumbh-mela/">how to reach Nashik guide</a>.</p>'
    return ('<h3 id="from-nashik">From Nashik city</h3><ul class="t-facts" style="list-style:none;display:grid;gap:var(--s-2);">%s</ul>'
            '<p class="prose" style="margin-top:var(--s-3);">Check the <a href="/transport/">transport hub</a> for official sources before you travel.</p>' % "".join(rows))


def kumbh_section_html(d):
    if not d.get("kumbhRole"):
        return ""
    return """      <section id="during-kumbh">
        <h2>During the Kumbh Mela</h2>
        <p>%s</p>
        <p>Access, queues and crowd rules during the Mela will be set by the Authority and the police and may differ from ordinary days. We could not find a published plan for this site, so we do not describe one. See the <a href="/kumbh-mela-2027/">Kumbh hub</a> and <a href="/kumbh-mela-2027/live-updates/">live updates</a>.</p>
      </section>""" % render.esc(d["kumbhRole"])


def access_section_html(d):
    acc = _ACCESS.get(d["slug"])
    if not acc:
        return ""
    note = "<p>%s</p>" % render.esc(acc["notes"]) if acc.get("notes") else ""
    ver = ("Verified %s." % render.esc(render.fmt_date(acc["verifiedAt"]))) if acc.get("verifiedAt") else "Not yet verified by our editors."
    return """      <section id="accessibility">
        <h2>Accessibility</h2>
        <p>%s</p>
        %s
        <p>%s &ldquo;Accessibility unknown&rdquo; describes what we know, not the place &mdash; please ask before you travel. See <a href="/accessible-nashik/">Accessible Nashik</a>.</p>
      </section>""" % (render.access_badge(acc["status"]), note, ver)


def updates_section_html(d):
    tags = set(d.get("tags", [])) | {d["slug"]}
    path = "/discover-nashik/%s/" % d["slug"]
    ups = [u for u in content.live_updates()
           if tags & set(u.get("tags") or []) or any(p.split("#")[0] == path for p in (u.get("relatedPages") or []))][:3]
    body = ("".join(render.update_card(u, tag="h3", compact=True) for u in ups) if ups else
            '<p class="none">No live updates for this place right now. See <a href="/updates/">all updates</a>.</p>')
    return """      <section id="latest-updates">
        <h2>Latest updates</h2>
        <div class="update-list">%s</div>
      </section>""" % body


def verify_section_html(d):
    path = "/discover-nashik/%s/" % d["slug"]
    ids = list(d.get("sourceReferences", []))
    for key in ("timings", "entryFee", "recommendedDuration", "parking"):
        v = d.get(key)
        if isinstance(v, dict) and "$fact" in v:
            for sid in _FACTS[v["$fact"]].get("verifyWith", []):
                if sid not in ids:
                    ids.append(sid)
    block = render.verify_block(path, d.get("verificationStatus", "not_verified"), d.get("lastVerified"), None, ids,
                               caveat="Timings may change during festivals. Confirm before travelling.",
                               heading="Sources and verification")
    return '      <section id="verification">%s</section>' % block


def img_url(dest, transform):
    if dest.get("unsplash"):
        return "%s?%s&q=75&auto=format&fit=crop" % (dest["unsplash"], transform)
    return "%s/%s/%s" % (CLD, transform, dest["img"])


def hero_img(dest):
    if dest.get("unsplash"):
        base = dest["unsplash"]
        srcset = ", ".join("%s?w=%d&q=75&auto=format&fit=crop %dw" % (base, w, w)
                           for w in (640, 960, 1280, 1920))
        return base + "?w=1280&q=75&auto=format&fit=crop", srcset
    t = "f_auto,q_auto,c_fill,g_auto,ar_16:9,w_%d"
    srcset = ", ".join("%s/%s/%s %dw" % (CLD, t % w, dest["img"], w)
                       for w in (640, 960, 1280, 1920))
    return "%s/%s/%s" % (CLD, t % 1280, dest["img"]), srcset


def og_img(dest):
    if dest.get("unsplash"):
        return dest["unsplash"] + "?w=1200&h=630&q=75&auto=format&fit=crop"
    return "%s/f_auto,q_auto,c_fill,g_auto,w_1200,h_630/%s" % (CLD, dest["img"])


def strip_tags(text):
    """FAQ answers carry links; schema wants the prose, not the markup."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text)).strip()


def plain(text):
    return text.replace("&amp;", "&").replace("&middot;", "·").replace("&mdash;", "—")


def nav_html(active):
    """Kept as a thin shim: the chrome itself now lives in tools/chrome.py so
    every page on the site shares one definition, not just these nine."""
    page = "/discover-nashik/%s/" % active if active not in ("__hub__", "__none__") else (
        "/discover-nashik/" if active == "__hub__" else "/plan-your-trip/")
    return chrome.nav_html(page)


def footer_html(page):
    return chrome.footer_html(page)


SCRIPT = chrome.SITE_JS + "\n\n" + chrome.GA


def build(dest):
    slug = dest["slug"]
    url = "%s/discover-nashik/%s/" % (SITE, slug)
    src, srcset = hero_img(dest)

    why = "\n".join("        <p>%s</p>" % p for p in dest["why"])
    tips = "\n".join("          <li>%s</li>" % t for t in dest["tips"])

    nearby = "\n".join(
        """          <a class="link-card" href="/discover-nashik/%s/">
            <span class="lc-kicker">%s</span>
            <span class="lc-title">%s</span>
            <span class="lc-desc">%s</span>
          </a>""" % (s, BY_SLUG[s]["kicker"], BY_SLUG[s]["name"],
                     BY_SLUG[s]["lede"].split(".")[0] + ".")
        for s in dest["nearby"])

    related = "\n".join(
        """          <a class="link-card" href="%s">
            <span class="lc-kicker">%s</span>
            <span class="lc-title">%s</span>
            <span class="lc-desc">%s</span>
          </a>""" % (href, kicker, title, desc)
        for kicker, title, desc, href in dest["related"])

    faqs = "\n".join(
        """        <details class="faq-item">
          <summary>%s</summary>
          <div class="faq-answer"><p>%s</p></div>
        </details>""" % (q, a) for q, a in dest["faqs"])

    sidebar_related = "".join(
        '<li><a href="%s">%s</a></li>' % (href, title)
        for _, title, _, href in dest["related"])

    faq_schema = """{
        "@type": "FAQPage",
        "@id": "%s#faq",
        "mainEntity": [
%s
        ]
      }""" % (url, ",\n".join(
        """          {
            "@type": "Question",
            "name": %s,
            "acceptedAnswer": { "@type": "Answer", "text": %s }
          }""" % (json.dumps(plain(q)), json.dumps(strip_tags(plain(a))))
        for q, a in dest["faqs"]))

    breadcrumb_json = """{
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "%s/" },
          { "@type": "ListItem", "position": 2, "name": "Discover Nashik", "item": "%s/discover-nashik/" },
          { "@type": "ListItem", "position": 3, "name": "%s", "item": "%s" }
        ]
      }""" % (SITE, SITE, plain(dest["name"]), url)

    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script>document.documentElement.className += ' js';</script>

  <title>%(title)s</title>
  <meta name="description" content="%(meta)s" />
  <link rel="canonical" href="%(url)s" />
  <meta name="robots" content="index, follow, max-image-preview:large" />

  <meta property="og:title" content="%(title)s" />
  <meta property="og:description" content="%(meta)s" />
  <meta property="og:url" content="%(url)s" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="NashikTourism.com" />
  <meta property="og:locale" content="en_IN" />
  <meta property="og:image" content="%(ogimg)s" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="%(title)s" />
  <meta name="twitter:description" content="%(meta)s" />
  <meta name="twitter:image" content="%(ogimg)s" />

  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#2D1B69" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preconnect" href="https://res.cloudinary.com" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400..900&family=Lato:wght@300;400;700&display=swap" />
  <link rel="preload" as="image" fetchpriority="high" imagesrcset="%(srcset)s" imagesizes="100vw" />
  <link rel="stylesheet" href="/style.css" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebPage",
        "@id": "%(url)s#webpage",
        "url": "%(url)s",
        "name": "%(title_plain)s",
        "description": "%(meta)s",
        "isPartOf": { "@id": "%(site)s/#website" },
        "about": { "@id": "%(url)s#attraction" },
        "inLanguage": "en-IN"
      },
      %(breadcrumb)s,
      %(faq_schema)s,
      {
        "@type": "TouristAttraction",
        "@id": "%(url)s#attraction",
        "name": "%(name_plain)s",
        "description": "%(lede_plain)s",
        "url": "%(url)s",
        "image": "%(ogimg)s",
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "Nashik",
          "addressRegion": "Maharashtra",
          "addressCountry": "IN"
        }
      }
    ]
  }
  </script>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<header>
%(nav)s
</header>

<main id="main" class="dest-main">

  <section class="dest-hero" aria-label="%(name_plain)s">
    <img class="dest-hero-img" src="%(src)s" srcset="%(srcset)s" sizes="100vw"
         width="1280" height="720" fetchpriority="high" decoding="async" alt="%(alt)s" />
    <div class="dest-hero-inner">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>
        <a href="/discover-nashik/">Discover Nashik</a> <span aria-hidden="true">&rsaquo;</span>
        <span aria-current="page">%(name)s</span>
      </nav>
      <p class="dest-kicker">%(kicker)s</p>
      <h1>%(name)s</h1>
      <p class="lede">%(lede)s</p>
    </div>
  </section>

  <nav class="dest-nav" aria-label="On this page" data-section-nav>
    <ul>
      <li><a href="#quick-facts">Quick facts</a></li>
      <li><a href="#why-visit">Why visit</a></li>
      <li><a href="#see-do">Things to see</a></li>
      <li><a href="#significance">History</a></li>
      <li><a href="#how-to-reach">How to reach</a></li>%(nav_kumbh)s
      <li><a href="#accessibility">Accessibility</a></li>
      <li><a href="#best-time">Best time</a></li>
      <li><a href="#nearby">Nearby</a></li>
      <li><a href="#faqs">FAQs</a></li>
      <li><a href="#verification">Sources</a></li>
    </ul>
  </nav>

  <div class="dest-wrap">
    <article class="dest-body">

%(facts)s

      <section id="why-visit">
        <h2>Why visit %(name)s</h2>
%(why)s
      </section>

      <section id="see-do">
        <h2>Things to see and do</h2>
        <p>%(see)s</p>
      </section>

      <section id="significance">
        <h2>History and significance</h2>
        <p>%(significance)s</p>
      </section>

      <section id="how-to-reach">
        <h2>How to reach %(name)s</h2>
        <p>%(name)s is in Nashik district, Maharashtra. Nashik itself is reachable by train, bus, road and air, and our <a href="/blog/how-to-reach-nashik-for-kumbh-mela/">how to reach Nashik guide</a> sets out the options from Mumbai, Pune and Delhi.</p>
%(reach_extra)s
      </section>

%(during_kumbh)s
%(access)s

      <section id="best-time">
        <h2>Best time to visit</h2>
        <p>Nashik's year divides fairly clearly into the monsoon, the cool months that follow it, and a hot stretch before the rains return. Our <a href="/blog/best-time-to-visit-nashik/">month-by-month guide to Nashik</a> covers how that plays out across the district.</p>
      </section>

      <section id="tips">
        <h2>Travel tips</h2>
        <ul>
%(tips)s
        </ul>
      </section>

      <section id="nearby">
        <h2>Nearby attractions</h2>
        <div class="link-cards">
%(nearby)s
        </div>
      </section>

      <section id="related">
        <h2>Related guides</h2>
        <div class="link-cards">
%(related)s
        </div>
      </section>

      <section id="faqs">
        <h2>Frequently asked questions</h2>
%(faqs)s
      </section>

%(updates)s

%(verify)s

      <section id="plan-next" class="plan-next">
        <p class="pn-eyebrow">%(pn_q)s</p>
        <p class="pn-lede">%(pn_lede)s</p>
        <div class="pn-actions">
          <a class="btn btn-purple" href="%(pn_href)s">%(pn_cta)s</a>
          <a class="btn btn-outline" href="/plan-your-trip/#itineraries">See suggested itineraries</a>
        </div>
      </section>

    </article>

    <aside class="sidebar" aria-label="Quick links">
      <div class="sidebar-card">
        <h3>Plan this visit</h3>
        <ul class="toc-list">
          <li><a href="/blog/how-to-reach-nashik-for-kumbh-mela/">How to reach Nashik</a></li>
          <li><a href="/blog/best-time-to-visit-nashik/">Best time to visit</a></li>
          <li><a href="/blog/where-to-stay-nashik-kumbh-mela/">Where to stay</a></li>
          <li><a href="/blog/nashik-2-day-itinerary/">Two-day itinerary</a></li>
          <li><a href="/blog/nashik-kumbh-mela-budget-2027/">Budget guide</a></li>
        </ul>
        <a href="/plan-your-trip/" class="btn btn-purple">Plan Your Trip</a>
      </div>
      <div class="sidebar-card">
        <h3>Related reading</h3>
        <ul class="toc-list">%(sidebar_related)s</ul>
      </div>
      <div class="sidebar-card">
        <h3>Kumbh Mela 2027</h3>
        <ul class="toc-list">
          <li><a href="/kumbh-mela-2027/">Complete guide</a></li>
          <li><a href="/kumbh-mela-2027/#dates">Amrit Snan dates</a></li>
        </ul>
      </div>
    </aside>
  </div>

</main>

%(footer)s

%(script)s
</body>
</html>
""" % {
        "title": dest["title"], "title_plain": plain(dest["title"]),
        "meta": dest["meta"], "url": url, "site": SITE,
        "ogimg": og_img(dest), "src": src, "srcset": srcset,
        "alt": dest["alt"], "name": dest["name"], "name_plain": plain(dest["name"]),
        "kicker": dest["kicker"], "lede": dest["lede"], "lede_plain": plain(dest["lede"]),
        "why": why, "see": dest["see"], "significance": dest["significance"],
        "tips": tips, "nearby": nearby, "related": related, "faqs": faqs,
        "sidebar_related": sidebar_related, "breadcrumb": breadcrumb_json,
        "faq_schema": faq_schema,
        "facts": quick_facts_html(dest),
        "reach_extra": reach_extra_html(dest),
        "during_kumbh": kumbh_section_html(dest),
        "nav_kumbh": ('\n      <li><a href="#during-kumbh">During Kumbh</a></li>' if dest.get("kumbhRole") else ""),
        "access": access_section_html(dest),
        "updates": updates_section_html(dest),
        "verify": verify_section_html(dest),
        "pn_q": PLAN_NEXT[slug][0], "pn_lede": PLAN_NEXT[slug][1],
        "pn_href": PLAN_NEXT[slug][2], "pn_cta": PLAN_NEXT[slug][3],
        "nav": nav_html(dest["slug"]), "footer": footer_html(url.replace(SITE, "")), "script": SCRIPT,
    }


HUB_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script>document.documentElement.className += ' js';</script>

  <title>%(title)s</title>
  <meta name="description" content="%(meta)s" />
  <link rel="canonical" href="%(url)s" />
  <meta name="robots" content="index, follow, max-image-preview:large" />

  <meta property="og:title" content="%(title)s" />
  <meta property="og:description" content="%(meta)s" />
  <meta property="og:url" content="%(url)s" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="NashikTourism.com" />
  <meta property="og:locale" content="en_IN" />
  <meta property="og:image" content="%(ogimg)s" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="%(title)s" />
  <meta name="twitter:description" content="%(meta)s" />
  <meta name="twitter:image" content="%(ogimg)s" />

  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#2D1B69" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preconnect" href="https://res.cloudinary.com" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400..900&family=Lato:wght@300;400;700&display=swap" />
  <link rel="stylesheet" href="/style.css" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebPage",
        "@id": "%(url)s#webpage",
        "url": "%(url)s",
        "name": "%(title_plain)s",
        "description": "%(meta)s",
        "isPartOf": { "@id": "%(site)s/#website" },
        "inLanguage": "en-IN"
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "%(site)s/" },
          { "@type": "ListItem", "position": 2, "name": "%(crumb)s", "item": "%(url)s" }
        ]
      }
    ]
  }
  </script>
  <style>
%(css)s
  </style>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<header>
%(nav)s
</header>

<main id="main">
"""


def hub_page(title, meta, url, crumb, ogimg, css, nav, body):
    return (HUB_HEAD % {
        "title": title, "title_plain": plain(title), "meta": meta, "url": url,
        "crumb": crumb, "ogimg": ogimg, "site": SITE, "css": css, "nav": nav,
    }) + body + "\n</main>\n\n" + footer_html(url.replace(SITE, "")) + "\n\n" + SCRIPT + "\n</body>\n</html>\n"


DISCOVER_CSS = """    .hub-hero { background: var(--dark); padding: 9rem 5vw 3.5rem; }
    .hub-hero h1 { font-family:var(--font-display); font-size:clamp(2rem,5vw,3.5rem); font-weight:900; color:white; letter-spacing:-0.025em; line-height:1.08; margin:0.4rem 0 0.9rem; }
    .hub-hero .lede { color: var(--on-dark); font-size:1.05rem; line-height:1.7; max-width:620px; }
    .dest-cards { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:1.1rem; }
    .dest-card { display:block; background:white; border:1px solid var(--border); border-radius:10px; overflow:hidden; transition:transform 0.22s, box-shadow 0.22s; }
    .dest-card:hover { transform:translateY(-5px); box-shadow:0 18px 45px rgba(45,27,105,0.12); }
    .dest-card img { width:100%; height:200px; object-fit:cover; }
    .dest-card-body { padding:1.3rem; }
    .dest-card .dc-kicker { display:block; font-family:var(--font-display); font-size:0.62rem; font-weight:700; letter-spacing:0.13em; text-transform:uppercase; color:var(--saffron-deep); margin-bottom:0.4rem; }
    .dest-card h2 { font-family:var(--font-display); font-size:1.1rem; font-weight:800; color:var(--ink); line-height:1.3; letter-spacing:-0.01em; margin-bottom:0.4rem; }
    .dest-card p { font-size:0.88rem; color:var(--muted-strong); line-height:1.6; }
    .dest-card .rlink { display:inline-flex; align-items:center; gap:0.3rem; margin-top:0.9rem; font-family:var(--font-display); font-size:0.72rem; font-weight:700; color:var(--primary); letter-spacing:0.05em; text-transform:uppercase; transition:gap 0.2s; }
    .dest-card:hover .rlink { gap:0.55rem; }
    @media(max-width:1024px){ .dest-cards{grid-template-columns:repeat(2,minmax(0,1fr));} }
    @media(max-width:640px){ .dest-cards{grid-template-columns:1fr;} .hub-hero{padding:7.5rem 5vw 2.5rem;} }"""

PLAN_CSS = """    .hub-hero { background: var(--dark); padding: 9rem 5vw 3.5rem; }
    .hub-hero h1 { font-family:var(--font-display); font-size:clamp(2rem,5vw,3.5rem); font-weight:900; color:white; letter-spacing:-0.025em; line-height:1.08; margin:0.4rem 0 0.9rem; }
    .hub-hero .lede { color: var(--on-dark); font-size:1.05rem; line-height:1.7; max-width:620px; }
    .plan-list { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:0; border-top:1px solid var(--border); max-width:1140px; }
    .prow { display:flex; align-items:baseline; gap:1rem; padding:1.2rem 0.5rem 1.2rem 0; border-bottom:1px solid var(--border); transition:background 0.18s, padding-left 0.18s; }
    .prow:hover { background:var(--light); padding-left:0.75rem; }
    .prow-num { font-family:var(--font-display); font-size:0.72rem; font-weight:800; color:var(--saffron-deep); letter-spacing:0.06em; flex-shrink:0; min-width:1.6rem; }
    .prow-txt { flex:1 1 auto; }
    .prow-txt h3 { font-family:var(--font-display); font-size:1.02rem; font-weight:800; color:var(--ink); letter-spacing:-0.01em; margin-bottom:0.15rem; }
    .prow-txt p { font-size:0.88rem; color:var(--muted-strong); line-height:1.55; }
    .prow-go { margin-left:auto; align-self:center; color:var(--primary); font-size:1.1rem; flex-shrink:0; transition:transform 0.18s; }
    .prow:hover .prow-go { transform:translateX(4px); }
    /* ── Trip planner ──
       The itineraries are static HTML; these controls only narrow what is
       shown. Nothing is revealed by script, so nothing is lost without it. */
    .planner { background:var(--cream); }
    .planner-controls { display:flex; flex-direction:column; gap:var(--s-5); margin-bottom:var(--s-10); padding:var(--s-6); background:var(--white); border:1px solid var(--border); border-radius:var(--r-lg); max-width:var(--wrap); }
    .pc-group { display:flex; align-items:center; gap:var(--s-4); flex-wrap:wrap; }
    .pc-label { font-family:var(--font-display); font-size:var(--t-eyebrow); font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--stone-ink); flex:0 0 190px; }
    .pc-hint { font-size:0.82rem; color:var(--muted); }
    .plans { display:flex; flex-direction:column; gap:var(--s-8); max-width:var(--wrap); }
    .plan { background:var(--white); border:1px solid var(--border); border-radius:var(--r-lg); padding:var(--s-8); }
    .plan-head { border-bottom:2px solid var(--border); padding-bottom:var(--s-4); margin-bottom:var(--s-6); }
    .plan-kicker { font-family:var(--font-display); font-size:0.66rem; font-weight:700; letter-spacing:var(--ls-eyebrow); text-transform:uppercase; color:var(--saffron-deep); margin-bottom:var(--s-2); }
    .plan-head h2 { font-family:var(--font-display); font-size:clamp(1.2rem,2.2vw,1.6rem); font-weight:800; color:var(--ink); letter-spacing:var(--ls-heading); margin-bottom:var(--s-3); }
    .plan-note { font-size:0.92rem; color:var(--body-clr); line-height:var(--lh-body); max-width:72ch; }
    .plan-note em { color:var(--ink); }
    .itin-day { margin-bottom:var(--s-8); }
    .itin-day:last-of-type { margin-bottom:0; }
    .itin-day h3 { font-family:var(--font-display); font-size:1.05rem; font-weight:800; color:var(--ink); margin-bottom:var(--s-4); display:flex; align-items:baseline; gap:var(--s-3); }
    .day-n { font-size:0.64rem; font-weight:800; letter-spacing:0.14em; text-transform:uppercase; color:#fff; background:var(--primary); border-radius:var(--r-sm); padding:0.25rem 0.5rem; }
    .itin-part { display:grid; grid-template-columns:110px minmax(0,1fr); gap:var(--s-4); padding:var(--s-4) 0; border-top:1px solid var(--border); }
    .itin-part h4 { font-family:var(--font-display); font-size:0.68rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--stone-ink); padding-top:0.2rem; }
    .itin-slots { list-style:none; margin:0; display:flex; flex-direction:column; gap:var(--s-4); }
    .sl { margin:0; }
    .sl-link { display:block; border-left:2px solid var(--border); padding-left:var(--s-4); margin-left:-2px; transition:border-color var(--dur) var(--ease); }
    .sl-link:hover { border-left-color:var(--saffron-deep); }
    .sl-when { font-family:var(--font-display); font-size:0.95rem; font-weight:800; color:var(--ink); margin-bottom:0.3rem !important; }
    .sl-meta { display:flex; gap:var(--s-3); flex-wrap:wrap; font-family:var(--font-display); font-size:0.66rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--muted-strong); margin-bottom:0.35rem !important; }
    .sl-cat { color:var(--saffron-deep); }
    .sl-note { font-size:0.9rem !important; color:var(--body-clr); line-height:1.6; margin:0 !important; }
    .sl-link .rlink { margin-top:var(--s-2); }
    .plan-src { margin-top:var(--s-6); padding-top:var(--s-4); border-top:1px solid var(--border); font-size:0.85rem; color:var(--muted); }
    .plan-src a { color:var(--primary); text-decoration:underline; text-underline-offset:2px; }
    @media(max-width:760px){
      .pc-label { flex:1 1 100%; }
      .plan { padding:var(--s-5); }
      .itin-part { grid-template-columns:1fr; gap:var(--s-2); padding:var(--s-5) 0; }
    }

    .checklist { max-width:760px; }
    .checklist li { margin-bottom:0.7rem; color:var(--body-clr); line-height:1.7; }
    @media(min-width:769px){ .plan-list > .prow:nth-child(odd){padding-right:2.5rem;} .plan-list > .prow:nth-child(even){padding-left:2.5rem;} }
    @media(max-width:768px){ .plan-list{grid-template-columns:1fr;} .hub-hero{padding:7.5rem 5vw 2.5rem;} }"""

# ─────────────────────────────────────────────────────────────────────────────
# SUGGESTED ITINERARIES
#
# These are NOT generated. Every stop, time and duration below is lifted from
# the itinerary this site already publishes at /blog/nashik-2-day-itinerary/,
# which sets out both days hour by hour. The planner on /plan-your-trip/ only
# chooses between the blocks rendered here — it never assembles a plan, so
# there is nothing a crawler or a visitor without JavaScript cannot see.
#
# Three published constraints bound everything below and must not be violated:
#   1. "Nashik rewards travellers who stay at least two nights. One day is
#      enough to touch the surface."            (nashik-2-day-itinerary)
#   2. "Trimbakeshwar and Nashik city are separate destinations. Plan them as
#      two trips."   (this file, Trimbakeshwar tips; echoed in two blog posts)
#   3. "A vineyard visit takes half a day once travel is counted."
#                                               (this file, Sula tips)
# Day 3 is the only block not published as a sequence; it is composed from the
# Igatpuri guide and is labelled as such on the page.
# ─────────────────────────────────────────────────────────────────────────────
DAY_SACRED = ("The sacred city", "spiritual heritage", [
    ("Morning", [
        ("5:30 AM &middot; Ramkund Ghat at dawn", "Spiritual", "About 45 minutes",
         "The 6 AM aarti, and the ghat at its most active.", "/discover-nashik/panchavati/"),
        ("8:00 AM &middot; Kalaram Temple", "Spiritual", "30&ndash;45 minutes",
         "500 metres from Ramkund, through the Panchavati lanes.", "/discover-nashik/panchavati/"),
        ("10:00 AM &middot; Pandavleni Caves", "Heritage", "1&ndash;1.5 hours",
         "5 km from the city, and around 200 steps up.", "/discover-nashik/pandavleni-caves/"),
    ]),
    ("Afternoon", [
        ("12:30 PM &middot; Lunch in the old city", "Food", "About an hour",
         "Maharashtrian thali near the main chowk.", None),
        ("2:30 PM &middot; Muktidham Temple", "Spiritual", "About 30 minutes",
         "Marble replicas of all twelve Jyotirlingas under one roof.", None),
    ]),
    ("Evening", [
        ("7:00 PM &middot; Evening aarti at Ramkund", "Spiritual", "An hour or so",
         "Diyas on the river, then the riverside lanes for dinner.", "/discover-nashik/panchavati/"),
    ]),
])

DAY_WINE = ("Trimbakeshwar and the vineyards", "spiritual wine nature", [
    ("Morning", [
        ("6:00 AM &middot; Trimbakeshwar Temple", "Spiritual", "Allow the morning",
         "28 km and 45&ndash;60 minutes out; arrive before 8 AM for the shortest queues. Kushavarta Kund is beside it.",
         "/discover-nashik/trimbakeshwar/"),
    ]),
    ("Afternoon", [
        ("11:30 AM &middot; Sula Vineyards", "Wine", "2&ndash;3 hours",
         "15 km from the city. A vineyard walk, a tasting and lunch on the estate.",
         "/discover-nashik/sula-vineyards/"),
        ("3:00 PM &middot; Gangapur Dam", "Nature", "An hour or so",
         "A reservoir in the Sahyadri foothills, on the Trimbak road.", None),
    ]),
    ("Evening", [
        ("5:00 PM &middot; MG Road", "Food", "As long as you like",
         "Copper and bronze, Maharashtrian textiles, Nashik sweets and local wine.", None),
    ]),
])

DAY_GHATS = ("Into the Western Ghats", "nature", [
    ("All day", [
        ("Igatpuri &amp; Bhandardara", "Nature", "A full day",
         "Hill country and reservoirs west of the city. Our guide calls this a landscape rather than a list of sights &mdash; it rewards an unhurried pace, and it is greenest during and just after the monsoon.",
         "/discover-nashik/igatpuri/"),
    ]),
])

PLANS = [
    {"id": "plan-1-sacred", "days": "1", "interests": "spiritual heritage",
     "title": "One day &mdash; the sacred city",
     "note": "Our two-day itinerary is blunt about this: <em>&ldquo;Nashik rewards travellers who stay at least two nights. One day is enough to touch the surface.&rdquo;</em> If a single day is all you have, this is the day that shows you most of it.",
     "days_list": [DAY_SACRED], "source": "/blog/nashik-2-day-itinerary/"},
    {"id": "plan-1-wine", "days": "1", "interests": "wine spiritual nature",
     "title": "One day &mdash; Trimbakeshwar and the vineyards",
     "note": "Trimbakeshwar and the Panchavati ghats are planned as separate days throughout this site, so this one pairs the Jyotirlinga with the wine country instead of with the city ghats.",
     "days_list": [DAY_WINE], "source": "/blog/nashik-2-day-itinerary/"},
    {"id": "plan-2", "days": "2", "interests": "spiritual heritage wine nature",
     "title": "Two days &mdash; the full itinerary",
     "note": "This is the itinerary we publish in full, hour by hour, with transport notes and costs.",
     "days_list": [DAY_SACRED, DAY_WINE], "source": "/blog/nashik-2-day-itinerary/"},
    {"id": "plan-3", "days": "3", "interests": "spiritual heritage wine nature",
     "title": "Three days &mdash; the city, the wine country and the Ghats",
     "note": "The first two days are the published itinerary. The third is a suggestion drawn from our Igatpuri &amp; Bhandardara guide rather than a published day-by-day plan &mdash; we have no verified timings for the Ghats, so treat it as a shape for the day, not a schedule.",
     "days_list": [DAY_SACRED, DAY_WINE, DAY_GHATS], "source": "/blog/nashik-2-day-itinerary/"},
]

PLAN_INTERESTS = [("spiritual", "Spiritual"), ("heritage", "Heritage"),
                  ("wine", "Wine"), ("nature", "Nature")]


def _slot(title, cat, dur, note, href):
    inner = """            <p class="sl-when">%s</p>
            <p class="sl-meta"><span class="sl-cat">%s</span><span>%s</span></p>
            <p class="sl-note">%s</p>""" % (title, cat, dur, note)
    if href:
        return """          <li class="sl"><a class="sl-link" href="%s">
%s
            <span class="rlink">Explore this destination <span aria-hidden="true">&rarr;</span></span>
          </a></li>""" % (href, inner)
    return """          <li class="sl">
%s
          </li>""" % inner


def plan_html(plan):
    days = []
    for i, (day_title, _tags, slots) in enumerate(plan["days_list"], 1):
        parts = []
        for part_name, entries in slots:
            parts.append("""        <div class="itin-part">
          <h3>%s</h3>
          <ul class="itin-slots">
%s
          </ul>
        </div>""" % (part_name, "\n".join(_slot(*e) for e in entries)))
        days.append("""      <div class="itin-day">
        <h3><span class="day-n">Day %d</span> %s</h3>
%s
      </div>""" % (i, day_title, "\n".join(parts)))

    return """    <article class="plan" id="%s" data-plan data-plan-days="%s" data-plan-interests="%s">
      <header class="plan-head">
        <p class="plan-kicker">Suggested itinerary</p>
        <h2>%s</h2>
        <p class="plan-note">%s</p>
      </header>
%s
      <p class="plan-src">Built from our <a href="%s">two-day Nashik itinerary</a>, which sets out each day hour by hour with transport notes and costs. Timings and arrangements change &mdash; confirm them close to your travel date.</p>
    </article>""" % (plan["id"], plan["days"], plan["interests"], plan["title"],
                     plan["note"], "\n".join(days), plan["source"])


PLAN_ROWS = [
    ("How do I reach Nashik?", "Train, bus, flight and road routes from Mumbai, Pune and Delhi.", "/blog/how-to-reach-nashik-for-kumbh-mela/"),
    ("When should I visit?", "How the seasons run, and which months suit which kind of trip.", "/blog/best-time-to-visit-nashik/"),
    ("How many days are enough?", "A worked two-day itinerary across temples, caves and vineyards.", "/blog/nashik-2-day-itinerary/"),
    ("Where should I stay?", "Which areas suit which trip, from Panchavati to the vineyard side.", "/blog/where-to-stay-nashik-kumbh-mela/"),
    ("What will it cost?", "A budget breakdown for travel, stay, food and getting around.", "/blog/nashik-kumbh-mela-budget-2027/"),
    ("What should I actually see?", "Fifteen places worth your time, temples and vineyards to quieter corners.", "/blog/is-nashik-worth-visiting/"),
    ("What do I pack?", "A practical packing list, written with Kumbh Mela crowds in mind.", "/blog/nashik-kumbh-mela-packing-list/"),
    ("What about Kumbh Mela 2027?", "Dates, ghats, crowds and how the Mela reshapes a Nashik trip.", "/kumbh-mela-2027/"),
]


def build_discover_hub():
    cards = []
    for d in DESTINATIONS:
        if d.get("unsplash"):
            src = d["unsplash"] + "?w=560&q=75&auto=format&fit=crop"
            srcset = ", ".join("%s?w=%d&q=75&auto=format&fit=crop %dw" % (d["unsplash"], w, w)
                               for w in (400, 560, 900))
        else:
            t = "f_auto,q_auto,c_fill,g_auto,ar_3:2,w_%d"
            src = "%s/%s/%s" % (CLD, t % 560, d["img"])
            srcset = ", ".join("%s/%s/%s %dw" % (CLD, t % w, d["img"], w) for w in (400, 560, 900))
        cats = DEST_CATEGORIES[d["slug"]]
        tags = " ".join(CATEGORY_LABELS[c] for c in cats)
        # The card answers the brief's four questions in order: what is this,
        # why go, where is it, what kind of experience. The CTA names the place
        # rather than saying "Read more".
        cards.append("""    <a class="dest-card fade-up" href="/discover-nashik/%s/"
       data-tags="%s" data-search="%s">
      <img src="%s" srcset="%s" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 31vw"
           width="560" height="373" alt="%s" loading="lazy" decoding="async" />
      <div class="dest-card-body">
        <span class="dc-kicker">%s</span>
        <h2>%s</h2>
        <p>%s</p>
        <p class="dc-where">%s</p>
        <span class="rlink">%s <span aria-hidden="true">&rarr;</span></span>
      </div>
    </a>""" % (d["slug"], " ".join(cats),
               plain(("%s %s %s" % (d["name"], tags, d["lede"])).lower()),
               src, srcset, d["alt"], d["kicker"], d["name"],
               d["lede"].split(". ")[0] + ".", d["where"], d["cta"]))

    # Only categories with matching destinations are offered — the brief is
    # explicit that a filter must never come back empty. Adventure (zero
    # destinations) and Weekend Getaway (one) are therefore not exposed.
    counts = {}
    for d in DESTINATIONS:
        for c in DEST_CATEGORIES[d["slug"]]:
            counts[c] = counts.get(c, 0) + 1
    chips = ['        <button class="chip" type="button" data-filter="all" aria-pressed="true">All <span class="n">%d</span></button>' % len(DESTINATIONS)]
    for key, label in CATEGORY_LABELS.items():
        if counts.get(key):
            chips.append('        <button class="chip" type="button" id="cat-%s" data-filter="%s" aria-pressed="false">%s <span class="n">%d</span></button>'
                         % (key, key, label, counts[key]))

    body = """
  <section class="hub-hero">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>
      <span aria-current="page">Discover Nashik</span>
    </nav>
    <h1>Discover Nashik</h1>
    <p class="lede">Five very different places, all within reach of one city &mdash; a Jyotirlinga in the hills, an old riverside quarter, a vineyard estate, a hillside of rock-cut caves, and the Western Ghats.</p>
  </section>

  <section aria-labelledby="places-h" data-filter-group="dest">
    <p class="section-eyebrow">Where to Go</p>
    <h2 class="section-title" id="places-h" style="margin-bottom:0.4rem;">Places to visit in Nashik</h2>
    <p class="section-sub">Each guide covers why the place is worth your time, how it fits into a trip, and what to read next.</p>

    <div class="explorer-bar">
      <div class="chips" role="group" aria-label="Filter destinations by the kind of place">
%s
      </div>
      <p class="explorer-count"><span data-filter-count>%d</span> destination guides</p>
      <p class="sr-only" data-filter-status role="status"></p>
    </div>

    <div class="dest-cards" data-filter-items>
%s
    </div>
    <p class="guide-empty" data-filter-empty hidden>No destinations match that filter.</p>
  </section>

  <section style="background:var(--light);" aria-labelledby="next-h">
    <p class="section-eyebrow">Next Step</p>
    <h2 class="section-title" id="next-h">Turn this into a trip</h2>
    <p class="section-sub">Once you know where you are going, the practical guides cover getting there, when to come and where to stay.</p>
    <div style="display:flex;gap:0.9rem;flex-wrap:wrap;">
      <a href="/plan-your-trip/" class="btn btn-purple">Plan Your Trip</a>
      <a href="/kumbh-mela-2027/" class="btn btn-outline">Kumbh Mela 2027</a>
      <a href="/blog/" class="btn btn-outline">All Travel Guides</a>
    </div>
  </section>
""" % ("\n".join(chips), len(DESTINATIONS), "\n".join(cards))

    return hub_page(
        "Discover Nashik – Temples, Heritage, Vineyards &amp; Nature",
        "Places to visit in Nashik: Trimbakeshwar, Panchavati and Ramkund, Sula Vineyards, the Pandavleni Caves and the Western Ghats at Igatpuri.",
        SITE + "/discover-nashik/", "Discover Nashik",
        "%s/f_auto,q_auto,c_fill,g_auto,w_1200,h_630/%s" % (CLD, DESTINATIONS[0]["img"]),
        DISCOVER_CSS, nav_html("__hub__"), body)


def build_plan_hub():
    rows = "\n".join("""    <a href="%s" class="prow">
      <span class="prow-num" aria-hidden="true">%02d</span>
      <div class="prow-txt"><h3>%s</h3><p>%s</p></div>
      <span class="prow-go" aria-hidden="true">&rarr;</span>
    </a>""" % (href, i + 1, q, d) for i, (q, d, href) in enumerate(PLAN_ROWS))

    body = """
  <section class="hub-hero">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>
      <span aria-current="page">Plan Your Trip</span>
    </nav>
    <h1>Plan your Nashik trip</h1>
    <p class="lede">Everything practical in one place &mdash; getting there, when to come, how long to stay, what it costs, and how Kumbh Mela 2027 changes the answer to all of those.</p>
  </section>

  <section aria-labelledby="q-h">
    <p class="section-eyebrow">Start Here</p>
    <h2 class="section-title" id="q-h" style="margin-bottom:0.4rem;">The questions people ask first</h2>
    <p class="section-sub">Each one links to a full guide.</p>
    <div class="plan-list">
%(rows)s
    </div>
  </section>

  <section id="itineraries" class="planner" data-planner aria-labelledby="itin-h">
    <p class="section-eyebrow">Plan Your Nashik Trip</p>
    <h2 class="section-title" id="itin-h" style="margin-bottom:0.4rem;">How many days do you need in Nashik?</h2>
    <p class="section-sub">Two days is the short answer. Our own itinerary puts it plainly: <em>&ldquo;Nashik rewards travellers who stay at least two nights. One day is enough to touch the surface.&rdquo;</em> Below are suggested itineraries for one, two and three days, all built from that published guide.</p>

    <div class="planner-controls">
      <div class="pc-group">
        <p class="pc-label" id="pc-days">How long are you staying?</p>
        <div class="chips" role="group" aria-labelledby="pc-days">
          <button class="chip" type="button" id="day-1" data-days="1" aria-pressed="false">1 day</button>
          <button class="chip" type="button" id="day-2" data-days="2" aria-pressed="false">2 days</button>
          <button class="chip" type="button" id="day-3" data-days="3" aria-pressed="false">3 days</button>
        </div>
      </div>
      <div class="pc-group">
        <p class="pc-label" id="pc-int">What are you most interested in?</p>
        <div class="chips" role="group" aria-labelledby="pc-int">
%(interest_chips)s
        </div>
      </div>
      <p class="pc-hint">Every itinerary below stays on the page &mdash; choosing simply narrows what is shown.</p>
      <p class="sr-only" data-planner-status role="status"></p>
    </div>

    <div class="plans">
%(plans)s
    </div>
  </section>

  <section style="background:var(--light);" aria-labelledby="check-h">
    <p class="section-eyebrow">Before You Go</p>
    <h2 class="section-title" id="check-h">A short checklist</h2>
    <p class="section-sub">Worth settling early, particularly for travel around Kumbh Mela 2027.</p>
    <ul class="checklist">
      <li>Decide your travel mode first &mdash; train, bus, flight or self-drive &mdash; because it shapes everything else. See <a href="/blog/how-to-reach-nashik-for-kumbh-mela/">how to reach Nashik</a>.</li>
      <li>Pick the zone you want to stay in before you pick a hotel. Panchavati and Trimbakeshwar suit very different trips: <a href="/blog/where-to-stay-nashik-kumbh-mela/">where to stay</a>.</li>
      <li>Book accommodation early if your dates fall near the Amrit Snan dates &mdash; see the <a href="/kumbh-mela-2027/">Kumbh Mela 2027 guide</a>.</li>
      <li>Carry ID, emergency contacts and a light day bag for ghat visits. Our <a href="/blog/nashik-kumbh-mela-packing-list/">packing list</a> goes further.</li>
      <li>Confirm timings and any festival arrangements close to your travel date &mdash; they change, and Kumbh Mela plans in particular are still being finalised.</li>
    </ul>
  </section>

  <section aria-labelledby="where-h">
    <p class="section-eyebrow">Where to Go</p>
    <h2 class="section-title" id="where-h">Still deciding where to go?</h2>
    <p class="section-sub">The destination guides cover what each place is actually like.</p>
    <div style="display:flex;gap:0.9rem;flex-wrap:wrap;">
      <a href="/discover-nashik/" class="btn btn-purple">Discover Nashik</a>
      <a href="/blog/" class="btn btn-outline">All Travel Guides</a>
    </div>
  </section>
""" % {
        "rows": rows,
        "interest_chips": "\n".join(
            '          <button class="chip" type="button" data-interest="%s" aria-pressed="false">%s</button>'
            % (key, label) for key, label in PLAN_INTERESTS),
        "plans": "\n".join(plan_html(p) for p in PLANS),
    }

    return hub_page(
        "Plan Your Nashik Trip – Routes, Timing, Stays &amp; Budget",
        "Plan a trip to Nashik: how to reach the city, the best time to visit, how many days you need, where to stay, what it costs, and Kumbh Mela 2027.",
        SITE + "/plan-your-trip/", "Plan Your Trip",
        "%s/f_auto,q_auto,c_fill,g_auto,w_1200,h_630/%s" % (CLD, DESTINATIONS[0]["img"]),
        PLAN_CSS, nav_html("__none__"), body)


def main():
    hubs = [
        (os.path.join(ROOT, "discover-nashik", "index.html"), build_discover_hub()),
        (os.path.join(ROOT, "plan-your-trip", "index.html"), build_plan_hub()),
    ]
    for out, html in hubs:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("  wrote %-46s %6d bytes" % (out.replace(ROOT + os.sep, ""), len(html)))

    for dest in DESTINATIONS:
        out = os.path.join(ROOT, "discover-nashik", dest["slug"], "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        html = build(dest)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("  wrote %-46s %6d bytes" % (out.replace(ROOT + os.sep, ""), len(html)))


if __name__ == "__main__":
    main()
