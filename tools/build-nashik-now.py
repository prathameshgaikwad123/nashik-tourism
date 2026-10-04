#!/usr/bin/env python3
"""
Generate /nashik-now/ — "What do I need to know about Nashik right now?"

A dashboard for the person already in Nashik. Every dynamic item shows when it
was last updated:
  * weather        fetched in the browser from Open-Meteo by /now.js, stamped with
                   its fetch time; falls back to a sentence and the IMD link
  * updates        each card carries Source / Published / Verified / Last checked
  * Kumbh status   the lifecycle phase and the next reported milestone, labelled
                   'reported' until the Authority's notice is linked
  * events         date, source and verification status on each card
The page itself shows when it was built, so a stale deploy is visible.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import content, lifecycle, pagekit, render, store  # noqa: E402

CSS = """    .now-sec h2 { font-family: var(--font-display); font-size: clamp(1.2rem, 4vw, 1.5rem); font-weight: 800; letter-spacing: var(--ls-heading); color: var(--ink); margin-bottom: var(--s-1); scroll-margin-top: calc(var(--nav-h) + var(--tap) + var(--s-3)); }
    .now-sec .none { color: var(--stone-ink); line-height: 1.6; background: var(--white); border: 1px dashed var(--border-strong); border-radius: var(--r-lg); padding: var(--s-4) var(--s-5); }
    .now-sec .none a { color: var(--primary); text-decoration: underline; text-underline-offset: 2px; }
    .wx-fallback { color: var(--body-clr); line-height: 1.6; }
    .wx-fallback a { color: var(--primary); text-decoration: underline; text-underline-offset: 2px; }
    .emerg { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-3); background: var(--white); border: 1px solid var(--border-strong); border-left: 4px solid var(--saffron-deep); border-radius: 0 var(--r-lg) var(--r-lg) 0; padding: var(--s-4) var(--s-5); }
    .emerg strong { font-family: var(--font-display); font-size: 1.5rem; font-weight: 900; color: var(--ink); }
    .emerg p { flex: 1 1 14rem; font-size: 0.92rem; line-height: 1.5; color: var(--body-clr); }"""

SECTIONS = [
    ("kumbh", "Kumbh Mela", ["Kumbh"], "/kumbh-mela-2027/live-updates/", "All Kumbh live updates"),
    ("transport", "Transport and roads", ["Transport", "Roads", "Railways", "Airport"], "/transport/", "Transport hub"),
    ("tourism", "Tourism and local", ["Tourism", "Local", "Events", "Accommodation", "Weather"], "/updates/", "All updates"),
    ("government", "Government and safety", ["Government", "Safety"], "/updates/", "All updates"),
]


def kumbh_status_card():
    prof = lifecycle.profile()
    upcoming, _ = content.events()
    nxt = next((e for e in upcoming if e["category"] == "Kumbh"), None)
    body = '<p class="nc-label">Where the Mela stands</p><p class="nc-main">%s</p>' % render.esc(prof["label"])
    if nxt:
        body += ('<p class="nc-sub">Next reported date: <strong>%s</strong> &mdash; %s. %s</p>' % (
            render.esc(render.fmt_date(nxt["date"], weekday=True)), render.esc(nxt["title"]),
            ("This date is reported but not yet confirmed against the Authority&rsquo;s own notice."
             if nxt.get("verificationStatus") != "verified" else "")))
    body += '<p class="nc-stamp">Phase set by the editors from the reported Mela dates &middot; <a class="nc-link" href="/kumbh-mela-2027/#dates">Dates and sources</a></p>'
    return '<div class="now-card">%s</div>' % body


def main():
    built = store.now()
    facts = render.facts_index()
    sec_html = []
    for sid, title, cats, link, linktext in SECTIONS:
        items = content.live_updates(categories=cats, limit=3)
        extra = kumbh_status_card() if sid == "kumbh" else ""
        if items:
            lst = '<div class="update-list">%s</div>' % "".join(render.update_card(u, tag="h3", compact=True) for u in items)
        else:
            lst = '<p class="none">No live %s updates right now. That means nothing has been verified and published &mdash; not that nothing is happening. <a href="%s">%s</a>.</p>' % (
                render.esc(title.lower()), render.esc(link), render.esc(linktext))
        sec_html.append("""<section class="sec%s now-sec" aria-labelledby="n-%s"><div class="inner">
      <h2 id="n-%s">%s</h2>%s%s
      <p class="link-row"><a class="btn btn-outline" href="%s">%s</a></p></div></section>""" % (
            " sec-alt" if len(sec_html) % 2 == 0 else "", sid, sid, render.esc(title), extra, lst, link, linktext))
    upcoming, _ = content.events()
    ev = upcoming[:3]
    ev_html = ('<div class="event-list">%s</div>' % "".join(render.event_card(e) for e in ev)) if ev else \
        '<p class="none">No upcoming events listed. <a href="/events/">See events</a>.</p>'
    e112 = facts.get("safety.emergency.number")
    emerg = ""
    if e112:
        emerg = """<div class="emerg"><strong>%s</strong><p>India&rsquo;s single emergency number. %s Source: %s.</p></div>""" % (
            render.esc(e112["display"]), render.fact_badge(e112["status"], e112.get("verifiedAt")), render.fact_source_html(e112))
    nav = "".join('<li><a href="#%s">%s</a></li>' % (i, l) for i, l in [("weather", "Weather"), ("n-kumbh", "Kumbh"), ("n-transport", "Transport"), ("n-tourism", "Tourism"), ("events", "Events"), ("emergency", "Emergency")])
    head = pagekit.page_head(
        "Nashik Now",
        "What you need to know in Nashik right now &mdash; weather, verified updates, transport, the Kumbh and events, every item with the time it was last updated.",
        crumbs=[("Home", "/"), ("Nashik Now", None)], eyebrow="Live information",
        extra='<p class="ph-stamp"><span>Page built: <strong>%s</strong></span><span>Weather is fetched when you open this page</span></p>' % render.esc(render.fmt_date(built.date().isoformat())))
    verify = render.verify_block("/nashik-now/", "reported", None, built.date().isoformat(), ["imd", "ntka", "central-railway", "maharashtra-police"],
                                 caveat="Live information changes quickly. Confirm anything important with the official source before acting on it.")
    body = head + """
<nav class="sec-nav" aria-label="On this page" data-section-nav><ul>%(nav)s</ul></nav>
<section class="sec now-sec" aria-labelledby="weather"><div class="inner">
  <h2 id="weather">Weather</h2>
  <p class="sec-sub">Model-based data from Open-Meteo, shown with its fetch time. For official forecasts and weather warnings use the India Meteorological Department.</p>
  <div data-weather="full" aria-live="polite">
    <p class="wx-fallback">Weather loads when JavaScript is available. Meanwhile, see the <a href="https://mausam.imd.gov.in/" rel="noopener noreferrer">India Meteorological Department</a> for official forecasts and warnings.</p>
  </div>
</div></section>
%(sections)s
<section class="sec now-sec" aria-labelledby="events"><div class="inner">
  <h2 id="events">Events</h2>
  <p class="sec-sub">The next listed dates, each with its source.</p>
  %(events)s
  <p class="link-row"><a class="btn btn-outline" href="/events/">All events</a></p>
</div></section>
<section class="sec sec-alt now-sec" aria-labelledby="emergency"><div class="inner">
  <h2 id="emergency">In an emergency</h2>
  %(emerg)s
  <p class="sec-sub" style="margin-top:var(--s-4);">For what to do at the Kumbh, see <a href="/kumbh-mela-2027/#safety">safety, medical and emergencies</a>. For access needs see <a href="/accessible-nashik/">Accessible Nashik</a>.</p>
</div></section>
<section class="sec"><div class="inner">%(verify)s</div></section>
<script src="/now.js" defer></script>
""" % {"nav": nav, "sections": "\n".join(sec_html), "events": ev_html, "emerg": emerg, "verify": verify}
    html = pagekit.render(
        "/nashik-now/", "Nashik Now: weather, updates and what's on, with timestamps",
        "What you need to know in Nashik right now: weather, verified updates, transport, Kumbh Mela status and events. Every item shows when it was last updated.",
        body, crumbs=[("Home", "/"), ("Nashik Now", "/nashik-now/")], css=CSS, raw_title=True,
        modified=built.date().isoformat())
    html = html.replace("</head>", '  <meta name="nt-section" content="nashik-now" />\n</head>', 1)
    pagekit.write("/nashik-now/", html)
    print("nashik-now built (%s)" % built.isoformat())


if __name__ == "__main__":
    main()
