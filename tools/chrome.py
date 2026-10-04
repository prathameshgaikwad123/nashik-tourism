#!/usr/bin/env python3
"""
Single source of truth for the shared page chrome: header/nav, search dialog,
footer and the deferred script tags.

Phase 4 redesign — MOBILE FIRST. The primary target is a phone in one hand, so:

  * the header is a logo, a search button and a menu button, all >= 44 px
  * the menu is a sheet that leads with the six things people come for
    (Discover, Plan, Kumbh, Updates, Events, Nashik Now) as large tiles, and
    keeps everything else in one compact list — it is not a dump of every link
  * search opens a native <dialog> (focus trap, Esc, inert page for free)
  * desktop (>= 1200 px) expands the same structure into a bar with dropdowns

ACCESSIBILITY CONTRACT — do not drop these when editing:
  * <a class="skip-link" href="#main"> stays the first element in <body>
    (owned by the pages, not by this module)
  * <header>, <nav aria-label="Primary">, <main id="main">, <footer>
  * dropdown triggers are real <button class="chevron-btn"> elements carrying
    aria-expanded + aria-controls. Hover alone is not keyboard accessible.
  * the hamburger carries aria-expanded + aria-controls="mobileMenu"
  * the search control is a real link to /search/ (works with JS off) that
    /site.js upgrades to open the dialog
  * "Independent Travel Guide" under the logo — never "Official". This site is
    not a government or official tourism body.

Every entry below points at a page that exists. Nothing here invents a URL.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import lifecycle  # noqa: E402

SITE = "https://nashiktourism.com"

# ─────────────────────────────────────────────────────────────────────────────
# Destinations — mirrored from data/destinations.json so the nav, the footer and
# the generated pages can never disagree.
# ─────────────────────────────────────────────────────────────────────────────
DESTINATION_LINKS = [
    ("/discover-nashik/trimbakeshwar/", "Trimbakeshwar Temple"),
    ("/discover-nashik/panchavati/", "Panchavati &amp; Ramkund"),
    ("/discover-nashik/sula-vineyards/", "Sula Vineyards"),
    ("/discover-nashik/pandavleni-caves/", "Pandavleni Caves"),
    ("/discover-nashik/igatpuri/", "Igatpuri &amp; Bhandardara"),
]

GUIDE_LINKS = [
    ("/blog/", "All Travel Guides"),
    ("/blog/#kumbh-mela", "Kumbh Mela Guides"),
    ("/blog/#planning", "Planning &amp; Budget"),
    ("/blog/#nashik-guides", "Nashik Place Guides"),
    ("/blog/#travel-tips", "Getting There &amp; Around"),
]

KUMBH_LINKS = [
    ("/kumbh-mela-2027/", "Kumbh hub"),
    ("/kumbh-mela-2027/#dates", "Dates &amp; calendar"),
    ("/kumbh-mela-2027/live-updates/", "Live updates"),
    ("/blog/how-to-reach-nashik-for-kumbh-mela/", "How to reach"),
    ("/blog/where-to-stay-nashik-kumbh-mela/", "Where to stay"),
    ("/blog/nashik-kumbh-mela-packing-list/", "What to pack"),
    ("/kumbh-mela-2027/#figures", "Figures &amp; sources"),
]

PLAN_LINKS = [
    ("/plan-your-trip/", "Trip planner"),
    ("/plan-your-trip/#itineraries", "1, 2 &amp; 3-day itineraries"),
    ("/transport/", "Transport hub"),
    ("/accessible-nashik/", "Accessible Nashik"),
    ("/blog/best-time-to-visit-nashik/", "Best time to visit"),
    ("/blog/nashik-kumbh-mela-budget-2027/", "Budget guide"),
]

UPDATES_LINKS = [
    ("/updates/", "Latest updates"),
    ("/nashik-now/", "Nashik Now"),
    ("/updates/archive/", "Archive"),
]

ABOUT_LINKS = [
    ("/about/", "About this site"),
    ("/editorial-policy/", "Editorial policy"),
    ("/sources/", "Our sources"),
    ("/disclaimer/", "Disclaimer"),
    ("/contact/", "Contact"),
]

# Which section does a page belong to? Drives the active state in the nav.
SECTION_OF_PREFIX = [
    ("/discover-nashik/", "/discover-nashik/"),
    ("/plan-your-trip/", "/plan-your-trip/"),
    ("/transport/", "/plan-your-trip/"),
    ("/accessible-nashik/", "/plan-your-trip/"),
    ("/kumbh-mela-2027/", "/kumbh-mela-2027/"),
    ("/updates/", "/updates/"),
    ("/nashik-now/", "/updates/"),
    ("/events/", "/events/"),
    ("/blog/", "/blog/"),
    ("/about/", "/about/"),
    ("/editorial-policy/", "/about/"),
    ("/sources/", "/about/"),
    ("/disclaimer/", "/about/"),
    ("/contact/", "/about/"),
]

SEARCH_ICON = ('<svg class="ico" width="20" height="20" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
               '<path fill="currentColor" d="M10.5 3a7.5 7.5 0 1 0 4.7 13.3l4.5 4.5 1.4-1.4-4.5-4.5A7.5 7.5 0 0 0 10.5 3Zm0 2a5.5 5.5 0 1 1 0 11 5.5 5.5 0 0 1 0-11Z"/></svg>')


def section_of(page):
    for prefix, section in SECTION_OF_PREFIX:
        if page == prefix or page.startswith(prefix):
            return section
    return None


def kumbh_label():
    try:
        return lifecycle.profile().get("navLabel", "Kumbh 2027")
    except (FileNotFoundError, SystemExit, KeyError):
        return "Kumbh 2027"


def _dd(items, indent=10):
    pad = " " * indent
    return "\n".join('%s<a href="%s">%s</a>' % (pad, href, label) for href, label in items)


def nav_html(page="/"):
    """Header contents for `page` (an absolute site path, e.g. '/blog/')."""
    here = section_of(page)

    def top(href, label):
        active = here == href or page == href
        cls = ' class="active"' if active else ""
        cur = ' aria-current="page"' if page == href else ""
        return '<a href="%s"%s%s>%s</a>' % (href, cls, cur, label)

    def item(href, label, links, key):
        if not links:
            return "      <li>%s</li>" % top(href, label)
        return """      <li>
        %s
        <button class="chevron-btn" type="button" aria-expanded="false" aria-controls="dd-%s" aria-label="%s submenu"><span class="chevron" aria-hidden="true">&#9662;</span></button>
        <div class="dropdown" id="dd-%s">
%s
        </div>
      </li>""" % (top(href, label), key, label, key, _dd(links))

    kl = kumbh_label()
    items = "\n".join([
        item("/discover-nashik/", "Discover", [("/discover-nashik/", "All Destinations")] + DESTINATION_LINKS, "discover"),
        item("/plan-your-trip/", "Plan Your Trip", PLAN_LINKS, "plan"),
        item("/kumbh-mela-2027/", kl, KUMBH_LINKS, "kumbh"),
        item("/updates/", "Updates", UPDATES_LINKS, "updates"),
        item("/blog/", "Guides", GUIDE_LINKS, "guides"),
        item("/events/", "Events", None, "events"),
        item("/about/", "About", ABOUT_LINKS, "about"),
    ])

    def tile(href, label, sub, extra=""):
        active = ' aria-current="page"' if page == href else ""
        return ('<li><a href="%s" class="mm-tile%s"%s><span class="mm-t">%s</span><span class="mm-s">%s</span></a></li>'
                % (href, extra, active, label, sub))

    tiles = "\n    ".join([
        tile("/discover-nashik/", "Discover", "Temples, ghats, vineyards"),
        tile("/plan-your-trip/", "Plan", "Itineraries &amp; how to reach"),
        tile("/kumbh-mela-2027/", kl, "Dates, ghats, what to expect"),
        tile("/updates/", "Updates", "Verified, with sources"),
        tile("/events/", "Events", "What&rsquo;s on, and when"),
        tile("/nashik-now/", "Nashik Now", "Weather &amp; today&rsquo;s notices", " mm-tile-wide"),
    ])
    more = "\n    ".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in [
        ("/transport/", "Transport hub"),
        ("/accessible-nashik/", "Accessible Nashik"),
        ("/blog/", "All travel guides"),
        ("/sources/", "Our sources"),
        ("/editorial-policy/", "Editorial policy"),
        ("/about/", "About this site"),
        ("/contact/", "Contact"),
    ])

    return """<nav class="nav solid" id="mainNav" aria-label="Primary">
  <div class="nav-inner">
    <a href="/" class="nav-logo">
      <img src="/logo-white-96.png" alt="Nashik Tourism" width="48" height="48" />
      <span class="nav-logo-text">Nashik Tourism<small>Independent Travel Guide</small></span>
    </a>
    <ul class="nav-menu">
%(items)s
    </ul>
    <div class="nav-tools">
      <a href="/search/" class="nav-search" id="searchOpen" aria-haspopup="dialog" aria-controls="searchDialog">%(icon)s<span class="nav-search-label">Search</span></a>
      <button class="hamburger" id="hamburger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>

<div class="mobile-menu" id="mobileMenu">
  <ul class="mm-tiles">
    %(tiles)s
  </ul>
  <p class="mm-heading">More</p>
  <ul class="mm-list">
    %(more)s
  </ul>
</div>

<dialog class="search-dialog" id="searchDialog" aria-labelledby="searchTitle">
  <form class="sd-form" role="search" action="/search/" method="get">
    <div class="sd-head">
      <h2 id="searchTitle" class="sd-title">What are you looking for in Nashik?</h2>
      <button class="sd-close" type="button" id="searchClose" aria-label="Close search">&times;</button>
    </div>
    <div class="sd-field">
      <label for="searchInput" class="sr-only">Search destinations, guides, updates, events and answers</label>
      %(icon)s
      <input id="searchInput" name="q" type="search" placeholder="Try &ldquo;Trimbakeshwar timing&rdquo;" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search" />
      <button class="sd-go" type="submit">Search</button>
    </div>
  </form>
  <p class="sd-status sr-only" id="searchStatus" role="status" aria-live="polite"></p>
  <div class="sd-body" id="searchBody">
    <p class="sd-try-label">Popular searches</p>
    <ul class="sd-try" id="searchTry">
      <li><a href="/search/?q=Trimbakeshwar+timing">Trimbakeshwar timing</a></li>
      <li><a href="/search/?q=Kumbh+parking">Kumbh parking</a></li>
      <li><a href="/search/?q=Nashik+airport">Nashik airport</a></li>
      <li><a href="/search/?q=Ramkund">Ramkund</a></li>
      <li><a href="/search/?q=Nashik+to+Trimbakeshwar">Nashik to Trimbakeshwar</a></li>
      <li><a href="/search/?q=Sula+Vineyards">Sula Vineyards</a></li>
      <li><a href="/search/?q=Kumbh+2027+dates">Kumbh 2027 dates</a></li>
      <li><a href="/search/?q=Nashik+events">Nashik events</a></li>
    </ul>
  </div>
</dialog>""" % {"items": items, "tiles": tiles, "more": more, "icon": SEARCH_ICON}


def footer_html(page="/"):
    """A navigation hub, grouped the way the site is actually organised."""
    dest = "".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in DESTINATION_LINKS)
    kl = kumbh_label()
    return """<footer>
  <div class="footer-top">
    <div class="footer-brand">
      <img src="/logo-white-96.png" alt="Nashik Tourism" width="64" height="64" loading="lazy" />
      <p class="footer-brand-name">Nashik Tourism</p>
      <p>An independent, continuously verified guide to Nashik &mdash; the Godavari ghats, Trimbakeshwar, the vineyards, the Western Ghats and Simhastha Kumbh Mela 2026&ndash;28.</p>
    </div>
    <nav class="footer-cols" aria-label="Footer">
      <h2 class="sr-only">Site navigation</h2>
      <div class="footer-col">
        <h3>Discover</h3>
        <ul><li><a href="/discover-nashik/">All Destinations</a></li>%(dest)s</ul>
      </div>
      <div class="footer-col">
        <h3>Plan</h3>
        <ul>
          <li><a href="/plan-your-trip/">Plan Your Trip</a></li>
          <li><a href="/transport/">Transport Hub</a></li>
          <li><a href="/accessible-nashik/">Accessible Nashik</a></li>
          <li><a href="/blog/best-time-to-visit-nashik/">Best Time to Visit</a></li>
          <li><a href="/blog/where-to-stay-nashik-kumbh-mela/">Where to Stay</a></li>
          <li><a href="/blog/nashik-kumbh-mela-budget-2027/">What It Costs</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>%(kl)s</h3>
        <ul>
          <li><a href="/kumbh-mela-2027/">Kumbh Hub</a></li>
          <li><a href="/kumbh-mela-2027/#dates">Dates &amp; Calendar</a></li>
          <li><a href="/kumbh-mela-2027/live-updates/">Live Updates</a></li>
          <li><a href="/blog/how-to-reach-nashik-for-kumbh-mela/">How to Reach</a></li>
          <li><a href="/blog/nashik-kumbh-mela-packing-list/">What to Pack</a></li>
          <li><a href="/blog/nashik-kumbh-mela-e-pass-registration-2027/">Passes &amp; Registration</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Right Now</h3>
        <ul>
          <li><a href="/nashik-now/">Nashik Now</a></li>
          <li><a href="/updates/">Latest Updates</a></li>
          <li><a href="/events/">Events</a></li>
          <li><a href="/updates/archive/">Update Archive</a></li>
          <li><a href="/blog/">All Travel Guides</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>About</h3>
        <ul>
          <li><a href="/about/">About This Site</a></li>
          <li><a href="/editorial-policy/">Editorial Policy</a></li>
          <li><a href="/sources/">Our Sources</a></li>
          <li><a href="/disclaimer/">Disclaimer</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
    </nav>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 NashikTourism.com &mdash; an independent travel guide. Not affiliated with any government body or official tourism authority.</span>
    <span>Made with &hearts; for Nashik</span>
  </div>
</footer>""" % {"dest": dest, "kl": kl}


# The shared behaviour lives in one cached file instead of a copy inlined into
# every page. GA is left exactly where each page already had it — apply-chrome
# never adds analytics to a page that did not already carry it (unless the site
# owner sets analytics.sitewide in data/site-config.json).
SITE_JS = '<script src="/site.js" defer></script>'

GA = """<!-- Deferred third-party: analytics loads last and never blocks rendering -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-H04PTE8QL1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-H04PTE8QL1');
</script>"""
