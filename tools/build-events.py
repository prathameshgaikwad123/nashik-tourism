#!/usr/bin/env python3
"""
Generate /events/ from data/events.json.

Rules this page enforces:
  * no event without a named source (data validation fails the build otherwise)
  * a 'reported' event carries a visible 'awaiting official confirmation' flag
  * Event structured data is emitted ONLY for events an editor has verified
    against a linked source — never for reported dates, never for prices or
    availability we have not confirmed
  * past and cancelled events move to a collapsed 'Earlier' list by date, at
    build time (and a daily rebuild keeps that true)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import content, enums, pagekit, render, store  # noqa: E402
from nt.paths import SITE  # noqa: E402

CSS = """    .group-h { font-family: var(--font-display); font-size: 1.1rem; font-weight: 800; color: var(--ink); margin: var(--s-8) 0 var(--s-3); }
    .earlier summary { display: flex; align-items: center; min-height: var(--tap); cursor: pointer; font-family: var(--font-display); font-size: 1rem; font-weight: 800; color: var(--ink); }
    .earlier .event-list { margin-top: var(--s-4); }"""


def event_ld(e):
    """schema.org Event — verified events only."""
    if e.get("verificationStatus") != "verified" or not e.get("sourceUrl"):
        return None
    ld = {"@type": "Event", "name": e["title"], "startDate": e["date"] + ("T" + e["startTime"] + ":00+05:30" if e.get("startTime") else ""),
          "eventStatus": {"cancelled": "https://schema.org/EventCancelled", "postponed": "https://schema.org/EventPostponed",
                          "rescheduled": "https://schema.org/EventRescheduled"}.get(e["status"], "https://schema.org/EventScheduled"),
          "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
          "location": {"@type": "Place", "name": e["location"], "address": {"@type": "PostalAddress", "addressLocality": "Nashik", "addressRegion": "Maharashtra", "addressCountry": "IN"}},
          "description": e["description"], "url": e["sourceUrl"]}
    if e.get("endDate"):
        ld["endDate"] = e["endDate"]
    return ld


def main():
    upcoming, past = content.events()
    all_events = upcoming + past
    stamp = content.latest_stamp(all_events, "lastVerified", "lastCheckedAt")
    cats = [c for c in enums.EVENT_CATEGORIES if any(e["category"] == c for e in upcoming)]
    if len(upcoming) > 3 and len(cats) > 1:
        chips = ['<button class="chip" type="button" data-filter="all" aria-pressed="true">All <span class="n">%d</span></button>' % len(upcoming)]
        for c in cats:
            chips.append('<button class="chip" type="button" data-filter="%s" aria-pressed="false">%s <span class="n">%d</span></button>'
                         % (c.lower(), render.esc(c), sum(1 for e in upcoming if e["category"] == c)))
        up_html = """<div data-filter-group="events">
      <div class="explorer-bar"><div class="chips" role="group" aria-label="Filter events by category">%s</div>
        <p class="explorer-count"><span data-filter-count>%d</span> shown</p></div>
      <div class="event-list" data-filter-items>%s</div>
      <p class="guide-empty" data-filter-empty hidden>No events in this category right now.</p>
      <p class="sr-only" role="status" data-filter-status></p>
    </div>""" % ("".join(chips), len(upcoming), "\n".join(render.event_card(e) for e in upcoming))
    elif upcoming:
        up_html = '<div class="event-list">%s</div>' % "\n".join(render.event_card(e) for e in upcoming)
    else:
        up_html = """<div class="empty-state"><h3>No upcoming events listed</h3>
      <p>We list an event only when we can name a credible source for it. Nothing is currently listed. Check <a href="/updates/">updates</a> and <a href="/sources/">our sources</a>.</p></div>"""
    earlier = ""
    if past:
        earlier = """<details class="earlier" style="margin-top:var(--s-8);"><summary>Earlier and cancelled events (%d)</summary>
      <div class="event-list">%s</div></details>""" % (len(past), "\n".join(render.event_card(e) for e in past))

    head = pagekit.page_head(
        "Events in Nashik",
        "What is on, and when &mdash; with the source for every date. Kumbh Mela dates currently show as <em>reported</em> until the Authority&rsquo;s own notice is linked.",
        crumbs=[("Home", "/"), ("Events", None)], eyebrow="Events",
        extra='<p class="ph-stamp"><span>Last checked: <strong>%s</strong></span><span>%d upcoming</span></p>'
              % (render.esc(render.fmt_dt(stamp) if stamp else "not yet"), len(upcoming)))
    body = head + """
<section class="sec">
  <div class="inner">
    <div class="status-notice" role="note">
      <p class="sn-title">How events are listed</p>
      <p>An event appears here only with a named source. A date marked <strong>Reported</strong> comes from credible reporting but has not yet been confirmed against the organiser&rsquo;s or the Authority&rsquo;s own notice. Prices and booking links are shown only when the organiser publishes them &mdash; &ldquo;Not yet confirmed&rdquo; means we do not know, not that it is free.</p>
    </div>
    <h2 class="sec-title">Upcoming</h2>
    <p class="sec-sub">In date order. Times and arrangements for Kumbh dates have not been announced.</p>
    %(up)s
    %(earlier)s
    <p class="link-row"><a class="btn btn-outline" href="/kumbh-mela-2027/#dates">Kumbh dates in context</a><a class="btn btn-outline" href="/updates/">Latest updates</a></p>
  </div>
</section>
""" % {"up": up_html, "earlier": earlier}
    ld = [x for x in (event_ld(e) for e in upcoming) if x]
    html = pagekit.render(
        "/events/", "Events in Nashik: dates with their sources",
        "Events in Nashik and the Kumbh Mela, each with a named source, a verification status and its last-checked date. Nothing is listed without a credible source.",
        body, crumbs=[("Home", "/"), ("Events", "/events/")], css=CSS, jsonld=ld,
        modified=(stamp or "")[:10] or None, page_type="CollectionPage", raw_title=True)
    html = html.replace("</head>", '  <meta name="nt-section" content="events" />\n</head>', 1)
    pagekit.write("/events/", html)
    print("events: %d upcoming, %d earlier, %d with structured data" % (len(upcoming), len(past), len(ld)))


if __name__ == "__main__":
    main()
