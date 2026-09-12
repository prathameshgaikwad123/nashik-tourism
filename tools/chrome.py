#!/usr/bin/env python3
"""
Single source of truth for the shared page chrome: header/nav, footer and the
deferred script tags.

Phase 1 put the nav and footer in build-destinations.py, but only the seven
pages that script generates actually used it — the other twenty-eight carried
their own copy inline and drifted apart. tools/apply-chrome.py now rewrites the
<header> and <footer> block of every page from here, so there is exactly one
definition of the site chrome.

ACCESSIBILITY CONTRACT — do not drop these when editing:
  * <a class="skip-link" href="#main"> stays the first element in <body>
    (owned by the pages, not by this module)
  * <header>, <nav aria-label="Primary">, <main id="main">, <footer>
  * dropdown triggers are real <button class="chevron-btn"> elements carrying
    aria-expanded + aria-controls. Hover alone is not keyboard accessible.
  * the hamburger carries aria-expanded + aria-controls="mobileMenu"
  * "Independent Travel Guide" under the logo — never "Official". This site is
    not a government or official tourism body.

Every entry below points at a page that exists. Nothing here invents a URL.
"""

SITE = "https://nashiktourism.com"

# ─────────────────────────────────────────────────────────────────────────────
# Destinations — mirrored from build-destinations.py DESTINATIONS so the nav,
# the footer and the generated pages can never disagree. Kept as plain data
# here to avoid a circular import.
# ─────────────────────────────────────────────────────────────────────────────
DESTINATION_LINKS = [
    ("/discover-nashik/trimbakeshwar/", "Trimbakeshwar Temple"),
    ("/discover-nashik/panchavati/", "Panchavati &amp; Ramkund"),
    ("/discover-nashik/sula-vineyards/", "Sula Vineyards"),
    ("/discover-nashik/pandavleni-caves/", "Pandavleni Caves"),
    ("/discover-nashik/igatpuri/", "Igatpuri &amp; Bhandardara"),
]

# Guide groupings point at the category sections rendered on /blog/ by
# tools/build-blog.py — anchors on one page, not separate thin URLs.
GUIDE_LINKS = [
    ("/blog/", "All Travel Guides"),
    ("/blog/#kumbh-mela", "Kumbh Mela Guides"),
    ("/blog/#planning", "Planning &amp; Budget"),
    ("/blog/#nashik-guides", "Nashik Place Guides"),
    ("/blog/#travel-tips", "Getting There &amp; Around"),
]

KUMBH_LINKS = [
    ("/kumbh-mela-2027/", "Complete Guide"),
    ("/kumbh-mela-2027/#dates", "Amrit Snan Dates"),
    ("/blog/how-to-reach-nashik-for-kumbh-mela/", "How to Reach"),
    ("/blog/where-to-stay-nashik-kumbh-mela/", "Where to Stay"),
    ("/blog/nashik-kumbh-mela-packing-list/", "What to Pack"),
]

PLAN_LINKS = [
    ("/plan-your-trip/", "Trip Planner"),
    ("/plan-your-trip/#itineraries", "1, 2 &amp; 3-Day Itineraries"),
    ("/blog/best-time-to-visit-nashik/", "Best Time to Visit"),
    ("/blog/nashik-kumbh-mela-budget-2027/", "Budget Guide"),
]


def _dd(items, indent=10):
    pad = " " * indent
    return "\n".join('%s<a href="%s">%s</a>' % (pad, href, label) for href, label in items)


def _is_active(path, page):
    """A nav item is current when the page IS it, or sits underneath it."""
    if page == path:
        return True
    return path != "/" and page.startswith(path)


def nav_html(page="/"):
    """Header contents for `page` (an absolute site path, e.g. '/blog/')."""

    def top(href, label, extra=""):
        active = _is_active(href, page)
        cls = ' class="active"' if active else ""
        if extra:
            cls = ' class="%s%s"' % (extra, " active" if active else "")
        cur = ' aria-current="page"' if page == href else ""
        return '<a href="%s"%s%s>%s</a>' % (href, cls, cur, label)

    return """<nav class="nav%(solid)s" id="mainNav" aria-label="Primary">
  <div class="nav-inner">
    <a href="/" class="nav-logo">
      <img src="/logo-white-96.png" alt="Nashik Tourism" width="48" height="48" />
      <span class="nav-logo-text">Nashik Tourism<small>Independent Travel Guide</small></span>
    </a>
    <ul class="nav-menu">
      <li>
        %(discover)s
        <button class="chevron-btn" type="button" aria-expanded="false" aria-controls="dd-discover" aria-label="Discover Nashik submenu"><span class="chevron" aria-hidden="true">&#9662;</span></button>
        <div class="dropdown" id="dd-discover">
%(dd_discover)s
        </div>
      </li>
      <li>
        %(plan)s
        <button class="chevron-btn" type="button" aria-expanded="false" aria-controls="dd-plan" aria-label="Plan Your Trip submenu"><span class="chevron" aria-hidden="true">&#9662;</span></button>
        <div class="dropdown" id="dd-plan">
%(dd_plan)s
        </div>
      </li>
      <li>
        %(kumbh)s
        <button class="chevron-btn" type="button" aria-expanded="false" aria-controls="dd-kumbh" aria-label="Kumbh Mela 2027 submenu"><span class="chevron" aria-hidden="true">&#9662;</span></button>
        <div class="dropdown" id="dd-kumbh">
%(dd_kumbh)s
        </div>
      </li>
      <li>
        %(guides)s
        <button class="chevron-btn" type="button" aria-expanded="false" aria-controls="dd-guides" aria-label="Guides submenu"><span class="chevron" aria-hidden="true">&#9662;</span></button>
        <div class="dropdown" id="dd-guides">
%(dd_guides)s
        </div>
      </li>
      <li>%(about)s</li>
      <li>%(contact)s</li>
    </ul>
    <button class="hamburger" id="hamburger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu"><span></span><span></span><span></span></button>
  </div>
</nav>

<div class="mobile-menu" id="mobileMenu">
  <p class="mm-heading">Discover</p>
  <a href="/discover-nashik/">All destinations</a>
%(mm_dest)s
  <p class="mm-heading">Plan</p>
  <a href="/plan-your-trip/">Plan your trip</a>
  <a href="/plan-your-trip/#itineraries">1, 2 &amp; 3-day itineraries</a>
  <p class="mm-heading">Kumbh Mela 2027</p>
  <a href="/kumbh-mela-2027/">Complete guide</a>
  <a href="/kumbh-mela-2027/#dates">Amrit Snan dates</a>
  <p class="mm-heading">Guides</p>
  <a href="/blog/">All travel guides</a>
  <p class="mm-heading">About</p>
  <a href="/about/">About this site</a>
  <a href="/contact/" class="mob-book">Contact Us</a>
</div>""" % {
        # The homepage nav floats over the hero; every other page needs it solid.
        "solid": "" if page == "/" else " solid",
        "discover": top("/discover-nashik/", "Discover"),
        "plan": top("/plan-your-trip/", "Plan Your Trip"),
        "kumbh": top("/kumbh-mela-2027/", "Kumbh Mela 2027"),
        "guides": top("/blog/", "Guides"),
        "about": top("/about/", "About"),
        "contact": top("/contact/", "Contact", extra="nav-book"),
        "dd_discover": _dd([("/discover-nashik/", "All Destinations")] + DESTINATION_LINKS),
        "dd_plan": _dd(PLAN_LINKS),
        "dd_kumbh": _dd(KUMBH_LINKS),
        "dd_guides": _dd(GUIDE_LINKS),
        "mm_dest": "\n".join('  <a href="%s">%s</a>' % (h, l) for h, l in DESTINATION_LINKS),
    }


def footer_html(page="/"):
    """A navigation hub, grouped the way the site is actually organised."""
    dest = "".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in DESTINATION_LINKS)
    return """<footer>
  <div class="footer-top">
    <div class="footer-brand">
      <img src="/logo-white-96.png" alt="Nashik Tourism" width="64" height="64" loading="lazy" />
      <p class="footer-brand-name">Nashik Tourism</p>
      <p>An independent guide to Nashik &mdash; the Godavari ghats, Trimbakeshwar, the vineyards, the Western Ghats and Simhastha Kumbh Mela 2027.</p>
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
          <li><a href="/plan-your-trip/#itineraries">1, 2 &amp; 3-Day Itineraries</a></li>
          <li><a href="/blog/best-time-to-visit-nashik/">Best Time to Visit</a></li>
          <li><a href="/blog/how-to-reach-nashik-for-kumbh-mela/">How to Reach Nashik</a></li>
          <li><a href="/blog/where-to-stay-nashik-kumbh-mela/">Where to Stay</a></li>
          <li><a href="/blog/nashik-kumbh-mela-budget-2027/">What It Costs</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Kumbh Mela</h3>
        <ul>
          <li><a href="/kumbh-mela-2027/">Kumbh Mela 2027 Guide</a></li>
          <li><a href="/kumbh-mela-2027/#dates">Amrit Snan Dates</a></li>
          <li><a href="/blog/kumbh-mela-2027-all-snan-dates/">All Snan Dates</a></li>
          <li><a href="/blog/nashik-kumbh-mela-packing-list/">What to Pack</a></li>
          <li><a href="/blog/nashik-kumbh-mela-e-pass-registration-2027/">E-Pass &amp; Registration</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Guides</h3>
        <ul>
          <li><a href="/blog/">All Travel Guides</a></li>
          <li><a href="/blog/#kumbh-mela">Kumbh Mela Guides</a></li>
          <li><a href="/blog/#planning">Planning &amp; Budget</a></li>
          <li><a href="/blog/#nashik-guides">Nashik Place Guides</a></li>
          <li><a href="/blog/#travel-tips">Getting There &amp; Around</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>About</h3>
        <ul>
          <li><a href="/about/">About This Site</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/disclaimer/">Disclaimer</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
    </nav>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 NashikTourism.com &mdash; an independent travel guide. Not affiliated with any government body or official tourism authority.</span>
    <span>Made with &hearts; for Nashik</span>
  </div>
</footer>""" % {"dest": dest}


# The shared behaviour lives in one cached file instead of a copy inlined into
# every page. GA is left exactly where each page already had it — apply-chrome
# never adds analytics to a page that did not already carry it.
SITE_JS = '<script src="/site.js" defer></script>'

GA = """<!-- Deferred third-party: analytics loads last and never blocks rendering -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-H04PTE8QL1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-H04PTE8QL1');
</script>"""
