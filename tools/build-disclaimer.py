#!/usr/bin/env python3
"""
Generate /disclaimer/.

EVERY statement on this page is one the site already publishes. Nothing here is
newly asserted about how the site operates — that would be inventing facts about
someone else's business. The page consolidates what is currently scattered
across the homepage trust section, the About page and the booking CTAs, and
cites where each part is stated in full.

Sources, all in this repo:
  * index.html "Why trust this guide"   — independence, editorial stance,
                                          confirm-before-you-travel
  * index.html hotel CTA                — "We do not take bookings and do not
                                          handle payments."
  * about/ "A Note on Accuracy"         — how Kumbh information is sourced
  * about/ "Advertising and Revenue"    — AdSense, affiliate links, no paid
                                          editorial
  * the site footer                     — not affiliated with any government
                                          body or official tourism authority

A privacy policy is deliberately NOT generated here. Writing one means making
claims about data collection and retention that only the site owner can make.
That remains for them to add.

Usage:  python3 tools/build-disclaimer.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "nashiktourism"))
SITE = "https://nashiktourism.com"
URL = SITE + "/disclaimer/"
TITLE = "Disclaimer"
META = ("What NashikTourism.com is and is not: an independent travel guide with no government "
        "or official tourism affiliation, how it is funded, and why you should confirm timings "
        "and Kumbh Mela arrangements with official sources before you travel.")

CSS = """    .doc-hero { background: var(--dark); padding: 8rem var(--gutter) 3.5rem; }
    .doc-hero h1 { font-family:var(--font-display); font-size:var(--t-h1); font-weight:900; color:#fff; letter-spacing:var(--ls-display); line-height:1.08; margin:0.4rem 0 0.9rem; }
    .doc-hero .lede { color:var(--on-dark); font-size:1.05rem; line-height:var(--lh-body); max-width:60ch; }
    .doc { max-width:760px; margin:0 auto; padding:var(--s-16) var(--gutter) var(--s-20); }
    .doc h2 { font-family:var(--font-display); font-size:1.25rem; font-weight:800; color:var(--ink); letter-spacing:var(--ls-heading); margin:var(--s-12) 0 var(--s-4); padding-bottom:var(--s-3); border-bottom:2px solid var(--border); }
    .doc h2:first-of-type { margin-top:0; }
    .doc p { font-size:1rem; color:var(--body-clr); line-height:var(--lh-prose); margin-bottom:var(--s-4); }
    .doc ul { margin:0 0 var(--s-5) 1.3rem; }
    .doc li { color:var(--body-clr); line-height:var(--lh-body); margin-bottom:var(--s-2); }
    .doc a { color:var(--primary); text-decoration:underline; text-underline-offset:2px; }
    .doc a:hover { color:var(--saffron-deep); }
    .doc-note { background:var(--stone); border-left:3px solid var(--saffron-deep); border-radius:0 var(--r-lg) var(--r-lg) 0; padding:var(--s-5) var(--s-6); margin:var(--s-6) 0; }
    .doc-note p:last-child { margin-bottom:0; }
    @media(max-width:640px){ .doc-hero{padding:7.5rem var(--gutter) 2.5rem;} }"""

BODY = """
  <section class="doc-hero">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>
      <span aria-current="page">Disclaimer</span>
    </nav>
    <h1>Disclaimer</h1>
    <p class="lede">What this site is, what it is not, how it is funded, and what you should check for yourself before you travel. How we verify and label information is set out in the <a href="/editorial-policy/" style="color:var(--accent-warm);text-decoration:underline;">editorial policy</a>.</p>
  </section>

  <div class="doc">
    <h2>This is an independent guide, not an official one</h2>
    <p>NashikTourism.com is an independent travel guide. We are not a government body, not an official tourism authority, and not affiliated with any temple trust or state department. Nothing on this site should be read as an official announcement.</p>
    <p>Where a matter is decided by an authority &mdash; Kumbh Mela arrangements, temple timings, transport schedules, entry rules &mdash; that authority is the source of truth, not this site.</p>

    <h2>Confirm details before you travel</h2>
    <p>Timings, fees and festival arrangements change, and Kumbh Mela plans in particular are still being finalised. Please confirm details with official sources close to your travel date.</p>
    <div class="doc-note">
      <p>Where we are not confident in a figure, we leave it out and say so on the page rather than repeating a number we cannot stand behind. You will see &ldquo;still being verified&rdquo; notes on the <a href="/discover-nashik/">destination guides</a> for exactly this reason.</p>
    </div>
    <p>Our <a href="/editorial-policy/">editorial policy</a> sets out how we rank sources, label what is verified, reported or unconfirmed, and correct mistakes; our <a href="/sources/">sources page</a> lists the official sources to check yourself. The <a href="/about/">About page</a> explains who writes these guides.</p>

    <h2>We do not take bookings</h2>
    <p>We do not take bookings and do not handle payments. Where this site links to a hotel or transport booking site, that is an external company with its own terms, prices and cancellation rules. Any transaction is between you and them.</p>

    <h2>How the site is funded</h2>
    <p>NashikTourism.com is supported by display advertising and by occasional affiliate partnerships with travel booking platforms. Where we include booking links we may earn a small commission, at no additional cost to you.</p>
    <p>This never influences what we recommend. Where we link to a booking site, it is because we think it is the practical option &mdash; not because a listing was paid for. We do not accept paid editorial content or sponsored recommendations disguised as editorial; if something is sponsored, we say so clearly. The <a href="/about/">About page</a> covers this in more detail.</p>

    <h2>Accuracy and corrections</h2>
    <p>We work hard to keep our information accurate, but this site is written by people and travel information goes out of date. We make no warranty that everything here is complete or current at the moment you read it, and we cannot accept liability for decisions made solely on the basis of what is published here.</p>
    <p>If you spot an error or have updated information, we genuinely want to know. <a href="/contact/">Get in touch</a> &mdash; we read every message and update our guides accordingly.</p>

    <h2>Respect at religious sites</h2>
    <p>Much of what this site covers is in active religious use. The ghats at Ramkund are a place of worship and of funeral rites, and photography is not always welcome. Read the situation, follow the arrangements in place on the day, and ask before pointing a camera at anyone.</p>

    <div class="doc-note">
      <p>Looking for something else? The <a href="/about/">About page</a> explains who writes these guides and how, and <a href="/contact/">Contact</a> reaches us directly.</p>
    </div>
  </div>
"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script>document.documentElement.className += ' js';</script>

  <title>%(title)s &ndash; NashikTourism.com</title>
  <meta name="description" content="%(meta)s" />
  <link rel="canonical" href="%(url)s" />
  <meta name="robots" content="index, follow, max-image-preview:large" />

  <meta property="og:title" content="%(title)s &ndash; NashikTourism.com" />
  <meta property="og:description" content="%(meta)s" />
  <meta property="og:url" content="%(url)s" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="NashikTourism.com" />
  <meta property="og:locale" content="en_IN" />

  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#2D1B69" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
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
        "name": "Disclaimer",
        "description": "%(meta)s",
        "isPartOf": { "@id": "%(site)s/#website" },
        "publisher": { "@id": "%(site)s/#organization" },
        "inLanguage": "en-IN"
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "%(site)s/" },
          { "@type": "ListItem", "position": 2, "name": "Disclaimer", "item": "%(url)s" }
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


def main():
    html = (HEAD % {"title": TITLE, "meta": META, "url": URL, "site": SITE,
                    "css": CSS, "nav": chrome.nav_html("/disclaimer/")}
            + BODY + "\n</main>\n\n" + chrome.footer_html("/disclaimer/")
            + "\n\n" + chrome.SITE_JS + "\n</body>\n</html>\n")
    out = os.path.join(ROOT, "disclaimer", "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote disclaimer/index.html  %d bytes" % len(html))


if __name__ == "__main__":
    main()
