"""The page shell for every page the Phase 4 generators produce.

Legacy generators each carry a private copy of this head. New pages share this
one, so title/description/canonical/Open Graph/Twitter/JSON-LD are consistent by
construction — and so is the accessibility contract (skip link first, one <main
id="main">, header and footer from tools/chrome.py).
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import chrome  # noqa: E402

from . import store
from .paths import ROOT, SITE
from .render import esc

OG_DEFAULT = ("https://res.cloudinary.com/duhuxaukd/image/upload/"
              "f_auto,q_auto,c_fill,g_auto,w_1200,h_630/v1775450543/rishu-bhosale-LO0KOsgTEA0-unsplash_hqa4n3.jpg")
OG_ALT = "The Godavari riverfront at Nashik at dusk"


def ga_enabled():
    return True


def breadcrumb_html(crumbs, light=False):
    """crumbs: [(label, href_or_None), ...] — the last item is the current page."""
    parts = []
    for i, (label, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append('<span aria-current="page">%s</span>' % esc(label))
        else:
            parts.append('<a href="%s">%s</a>' % (esc(href), esc(label)))
    sep = ' <span aria-hidden="true">&rsaquo;</span> '
    return '<nav class="breadcrumb" aria-label="Breadcrumb">%s</nav>' % sep.join(parts)


def breadcrumb_ld(crumbs, path):
    items = []
    for i, (label, href) in enumerate(crumbs, 1):
        url = SITE + (href if href else path)
        items.append({"@type": "ListItem", "position": i, "name": label, "item": url})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def page_head(title, lede=None, crumbs=None, eyebrow=None, extra=""):
    """The compact utility header used by hub pages: no 100vh hero pushing the
    answer below the fold on a phone."""
    return """<section class="page-head">
  <div class="ph-inner">
    %(crumbs)s
    %(eyebrow)s
    <h1>%(title)s</h1>
    %(lede)s
    %(extra)s
  </div>
</section>""" % {
        "crumbs": breadcrumb_html(crumbs) if crumbs else "",
        "eyebrow": '<p class="ph-eyebrow">%s</p>' % esc(eyebrow) if eyebrow else "",
        "title": title,  # may contain <em>; callers pass trusted markup
        "lede": '<p class="ph-lede">%s</p>' % lede if lede else "",
        "extra": extra}


def render(path, title, description, body, *, crumbs=None, css="", jsonld=None, og_image=None,
           og_alt=None, robots="index, follow, max-image-preview:large", extra_head="",
           analytics=True, page_type="WebPage", modified=None, published=None, name=None,
           raw_title=False, preload_css=None):
    url = SITE + path
    full_title = title if raw_title or "NashikTourism" in title else "%s – NashikTourism.com" % title
    og = og_image or OG_DEFAULT
    alt = og_alt or OG_ALT
    graph = [{
        "@type": page_type, "@id": url + "#webpage", "url": url,
        "name": name or title, "description": description,
        "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@id": SITE + "/#organization"},
        "inLanguage": "en-IN",
    }]
    if modified:
        graph[0]["dateModified"] = modified
    if published:
        graph[0]["datePublished"] = published
    if crumbs:
        graph.append(breadcrumb_ld(crumbs, path))
    graph.extend(jsonld or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    ld = ld.replace("</", "<\\/")

    style = "\n  <style>\n%s\n  </style>" % css if css else ""
    scripts = chrome.SITE_JS + ("\n\n" + chrome.GA if (analytics and ga_enabled()) else "")
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script>document.documentElement.className += ' js';</script>

  <title>%(title)s</title>
  <meta name="description" content="%(desc)s" />
  <link rel="canonical" href="%(url)s" />
  <meta name="robots" content="%(robots)s" />

  <meta property="og:title" content="%(title)s" />
  <meta property="og:description" content="%(desc)s" />
  <meta property="og:url" content="%(url)s" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="NashikTourism.com" />
  <meta property="og:locale" content="en_IN" />
  <meta property="og:image" content="%(og)s" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="%(alt)s" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="%(title)s" />
  <meta name="twitter:description" content="%(desc)s" />
  <meta name="twitter:image" content="%(og)s" />

  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#2D1B69" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400..900&family=Lato:wght@300;400;700&display=swap" />
  <link rel="stylesheet" href="/style.css" />%(extra_head)s

  <script type="application/ld+json">
%(ld)s
  </script>%(style)s
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<header>
%(nav)s
</header>

<main id="main">
%(body)s
</main>

%(footer)s

%(scripts)s
</body>
</html>
""" % {"title": esc(full_title), "desc": esc(description), "url": url, "robots": robots,
       "og": esc(og), "alt": esc(alt), "extra_head": ("\n  " + extra_head) if extra_head else "",
       "ld": ld, "style": style, "nav": chrome.nav_html(path), "body": body,
       "footer": chrome.footer_html(path), "scripts": scripts}


def write(path, html):
    """Write `html` to the web root for site path `path` ('/updates/' -> updates/index.html)."""
    rel = path.strip("/")
    out = os.path.join(ROOT, rel, "index.html") if rel else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    return out
