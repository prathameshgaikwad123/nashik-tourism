#!/usr/bin/env python3
"""
Generate the Kumbh hub (/kumbh-mela-2027/) and /kumbh-mela-2027/live-updates/.

URL stays /kumbh-mela-2027/ — it is the page that already ranks — but the
content is built to outlive 2027:

  * every date and figure is a fact from data/facts.json, shown with its status
    (verified / reported / not verified / disputed) and its source
  * the 'live band' and the navigation label follow the lifecycle phase in
    data/site-config.json, so the hub reads correctly before, during and after
    the Mela without hand-editing
  * information that has not been announced says so ('No official plan located')
    instead of being filled in

The removed claims are recorded in data/changelog.json and surface in the
corrections log on /editorial-policy/.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import content, lifecycle, pagekit, render, store  # noqa: E402
import chrome  # noqa: E402

CSS = """    .k-sec h2 { font-family: var(--font-display); font-size: clamp(1.3rem, 4.6vw, 1.9rem); font-weight: 800; letter-spacing: var(--ls-heading); line-height: var(--lh-heading); color: var(--ink); margin-bottom: var(--s-2); scroll-margin-top: calc(var(--nav-h) + var(--tap) + var(--s-3)); }
    .k-sec h3 { font-family: var(--font-display); font-size: 1.05rem; font-weight: 800; color: var(--ink); margin: var(--s-5) 0 var(--s-2); }
    .answer { background: var(--white); border: 1px solid var(--border); border-left: 4px solid var(--primary); border-radius: 0 var(--r-lg) var(--r-lg) 0; padding: var(--s-4) var(--s-5); margin-bottom: var(--s-5); }
    .answer .a-q { font-family: var(--font-display); font-size: 0.7rem; font-weight: 700; letter-spacing: var(--ls-eyebrow); text-transform: uppercase; color: var(--saffron-deep); margin-bottom: var(--s-1); }
    .answer p { color: var(--ink); line-height: 1.6; font-size: 1rem; margin: 0; }
    .answer a { color: var(--primary); text-decoration: underline; text-underline-offset: 2px; }
    .glance { display: grid; gap: var(--s-3); grid-template-columns: minmax(0, 1fr); }
    .glance .answer { margin: 0; }
    .date-rows { list-style: none; display: grid; gap: var(--s-3); }
    .date-rows li { display: grid; gap: var(--s-2); background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s-4) var(--s-5); }
    .dr-l { font-family: var(--font-display); font-size: 0.74rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--stone-ink); }
    .dr-d { font-family: var(--font-display); font-size: 1.2rem; font-weight: 800; letter-spacing: var(--ls-heading); color: var(--ink); line-height: 1.25; }
    .dr-n { font-size: 0.86rem; color: var(--stone-ink); line-height: 1.5; }
    .loc-grid { display: grid; gap: var(--s-4); }
    .loc { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s-5); }
    .loc h3 { margin-top: 0; }
    .loc p { color: var(--body-clr); line-height: 1.65; font-size: 0.96rem; }
    .loc a.nc-link { margin-top: var(--s-2); }
    .guide-links { list-style: none; display: grid; gap: var(--s-3); }
    .guide-links a { display: block; background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s-4) var(--s-5); min-height: var(--tap); }
    .guide-links a:hover { border-color: var(--primary); }
    .gl-k { display: block; font-family: var(--font-display); font-size: 0.64rem; font-weight: 700; letter-spacing: var(--ls-eyebrow); text-transform: uppercase; color: var(--saffron-deep); }
    .gl-t { display: block; font-family: var(--font-display); font-size: 0.98rem; font-weight: 800; line-height: 1.3; color: var(--ink); margin-top: 2px; }
    .gl-d { display: block; font-size: 0.86rem; line-height: 1.5; color: var(--muted-strong); margin-top: 2px; }
    @media (min-width: 720px) { .glance { grid-template-columns: repeat(2, minmax(0, 1fr)); } .loc-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } .date-rows li { grid-template-columns: 14rem minmax(0, 1fr); align-items: start; } .guide-links { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    @media (min-width: 1024px) { .guide-links { grid-template-columns: repeat(3, minmax(0, 1fr)); } }"""

SOURCES = ["ntka", "divcom-gr", "divcom-approvals", "dgipr", "pib"]

GUIDES = [
    ("First-time pilgrims", "Nashik Kumbh Mela 2027: the complete guide", "Start here: what the Mela is and how a visit works.", "/blog/nashik-kumbh-mela-2027-complete-guide/"),
    ("Dates", "All Kumbh Mela 2027 snan dates", "The full calendar of bathing dates in our earlier guide.", "/blog/kumbh-mela-2027-all-snan-dates/"),
    ("Senior citizens", "Kumbh Mela for senior citizens", "Planning, health and ghat safety for older pilgrims.", "/blog/nashik-kumbh-mela-for-senior-citizens-2027/"),
    ("Women and solo travellers", "Kumbh Mela for women and solo travellers", "Practical guidance for travelling alone or as a woman.", "/blog/nashik-kumbh-mela-for-women-solo-travellers/"),
    ("International visitors", "Kumbh Mela for international tourists", "Visas, arrival and what to expect from abroad.", "/blog/nashik-kumbh-mela-for-international-tourists/"),
    ("Budget", "What the Kumbh Mela will cost", "A budget breakdown for travel, stay and food.", "/blog/nashik-kumbh-mela-budget-2027/"),
    ("Packing", "What to pack for the Kumbh Mela", "A packing list for crowds, weather and bathing.", "/blog/nashik-kumbh-mela-packing-list/"),
    ("Passes", "E-pass and registration guide", "What has and has not been announced about passes.", "/blog/nashik-kumbh-mela-e-pass-registration-2027/"),
    ("Where to stay", "Where to stay near Ramkund", "Areas and options, and what to book early.", "/blog/where-to-stay-nashik-kumbh-mela/"),
    ("Akharas", "Naga Sadhus at the Kumbh Mela", "Who the akharas are and what the processions are.", "/blog/naga-sadhus-kumbh-mela-nashik-2027/"),
    ("Sadhugram", "Sadhugram visitor guide", "The sadhu village inside the Mela.", "/blog/sadhugram-nashik-kumbh-mela-2027-visitor-guide/"),
    ("Rituals", "Pind daan at Nashik", "Ancestral rites at the ghats.", "/blog/pind-daan-nashik-kumbh-mela-2027/"),
]

FAQS = [
    ("What does Simhastha mean?",
     "The Simhastha Kumbh is held when Jupiter (Guru) is in Leo (Simha Rashi). In the traditional account, drops of amrit fell at Nashik, and bathing in the Godavari during this period is held to be spiritually meritorious."),
    ("When is the Nashik Kumbh Mela?",
     "The Mela is reported to open with a flag-hoisting on 31 October 2026 and to conclude on 24 July 2028, with the main Amrit Snan dates reported for 2 August, 31 August and 11&ndash;12 September 2027. These dates are <strong>reported, not yet confirmed</strong> against the Authority&rsquo;s own notice &mdash; see <a href=\"#dates\">dates and sources</a>."),
    ("Is there a charge to attend the Kumbh Mela?",
     "We have not been able to confirm. Earlier versions of this guide said there is no charge; we have not found an official statement either way. Ask the Authority &mdash; see <a href=\"/sources/\">our sources</a>."),
    ("Do I need a pass or to register?",
     "No general-visitor pass or registration requirement has been announced in any official source we could locate. Registration has been reported for religious organisations and for student volunteers only. Read <a href=\"#passes\">passes and registration</a> and check with the Authority."),
    ("Is it safe to attend?",
     "Safety arrangements are set by the Authority, the police and the district administration, and are not yet published in a form we can verify. Follow official announcements and the instructions of police and volunteers on the day. See <a href=\"#safety\">safety, medical and emergencies</a>."),
    ("Can foreign nationals attend?",
     "We have found no announcement restricting foreign visitors, but have not been able to confirm the position with the Authority. Foreign nationals need a valid Indian visa to enter India &mdash; see our <a href=\"/blog/nashik-kumbh-mela-for-international-tourists/\">guide for international visitors</a>."),
]


def fact_row(label, fid, facts, note=None):
    f = facts[fid]
    n = '<p class="dr-n">%s</p>' % note if note else ""
    return """<li><span class="dr-l">%s</span><div><p class="dr-d">%s</p><p class="dr-n">%s &middot; Source: %s</p>%s</div></li>""" % (
        render.esc(label), render.fact_value_html(f), render.fact_badge(f["status"], f.get("verifiedAt")), render.fact_source_html(f), n)


def fact_li(f):
    return """<li><span class="t-fl">%s &mdash; %s</span><span class="t-fv">%s</span><span class="t-fs">%s &middot; Source: %s</span></li>""" % (
        render.esc(f["subject"]), render.esc(f["fact"]), render.fact_value_html(f), render.fact_badge(f["status"], f.get("verifiedAt")), render.fact_source_html(f))


def live_band(prof):
    """'NASHIK — LIVE': only rendered visible in the live phase, but always in
    the markup so /site.js can switch it on the right day on a stale page."""
    latest = content.live_updates(limit=1)
    text = ('Latest: <a class="lb-link" href="/updates/#u-%s">%s</a>' % (render.esc(latest[0]["id"]), render.esc(latest[0]["title"]))
            if latest else 'Verified notices, transport and safety information are on <a class="lb-link" href="/kumbh-mela-2027/live-updates/">Kumbh live updates</a>.')
    return """<div class="live-band" data-phase-flag="liveBand"%s role="region" aria-label="Kumbh live status">
  <div class="lb-inner"><span class="lb-tag"><span class="lb-dot" aria-hidden="true"></span>Nashik &mdash; Live</span>
  <span class="lb-text">%s</span></div></div>""" % ("" if prof["liveBand"] else " hidden", text)


def phase_json():
    import json
    return '<script type="application/json" id="nt-phases">%s</script>' % json.dumps(lifecycle.client_payload()).replace("</", "<\\/")


def hub():
    facts = render.facts_index()
    prof = lifecycle.profile()
    f_ = lambda fid: facts[fid]  # noqa: E731
    kumbh_live = content.live_updates(category="Kumbh", limit=3)
    roads_live = content.live_updates(categories=["Roads", "Transport", "Railways"], limit=3)
    stamp = max([f.get("lastCheckedAt") or "" for f in facts.values() if f["id"].startswith("kumbh.")] + [""]) or None
    nav = "".join('<li><a href="#%s">%s</a></li>' % (i, l) for i, l in [
        ("at-a-glance", "At a glance"), ("dates", "Dates"), ("locations", "Locations"), ("getting-here", "Getting here"),
        ("passes", "Passes"), ("parking-roads", "Parking &amp; roads"), ("stay", "Stay"), ("safety", "Safety"), ("tips", "Tips"),
        ("accessibility", "Access"), ("guides", "Guides"), ("figures", "Figures"), ("faqs", "FAQs")])

    head = pagekit.page_head(
        "Nashik Kumbh Mela 2027 &mdash; <em>Simhastha</em> guide",
        "A guide to the Simhastha Kumbh Mela at Nashik and Trimbakeshwar. Dates and arrangements are still being confirmed, so every fact here shows how sure we are and where it comes from.",
        crumbs=[("Home", "/"), ("Kumbh Mela 2027", None)], eyebrow="Kumbh hub",
        extra='<p class="ph-stamp"><span>Facts last checked: <strong>%s</strong></span><span>Phase: <strong>%s</strong></span></p>' % (
            render.esc(render.fmt_date(stamp) if stamp else "not recorded"), render.esc(prof["label"])))

    glance = """<section class="sec k-sec" id="at-a-glance" aria-labelledby="h-glance"><div class="inner">
  <div class="status-notice" role="note"><p class="sn-title">What is confirmed, and what is not</p>
  <p>No date or figure on this page has yet been verified by our editors against an official notice. Items marked <strong>Reported</strong> come from credible reporting or an official page we have located but not yet re-read; items marked <strong>Sources differ</strong> show every figure with what it counts. The Authority&rsquo;s own announcements are the source of truth &mdash; see <a href="/sources/">our sources</a>.</p></div>
  <h2 id="h-glance">The Kumbh at a glance</h2>
  <p class="sec-sub">Short answers first; the detail follows.</p>
  <div class="glance">
    <div class="answer"><p class="a-q">What is it?</p><p>The Simhastha Kumbh Mela, one of the four Kumbh Melas held in rotation in India, held at Nashik and Trimbakeshwar on the Godavari when Jupiter is in Leo.</p></div>
    <div class="answer"><p class="a-q">Where is it?</p><p>Ramkund in Nashik city (Panchavati) and Kushavarta Tirtha at Trimbakeshwar, %(dist)s &mdash; <a href="#locations">the two locations</a>.</p></div>
    <div class="answer"><p class="a-q">When is it?</p><p>Reported to open on %(open)s and conclude on %(close)s. Main bathing dates: <a href="#dates">see the calendar</a>.</p></div>
    <div class="answer"><p class="a-q">Do I need a pass?</p><p>No general-visitor pass has been announced that we could locate. <a href="#passes">Passes and registration</a>.</p></div>
    <div class="answer"><p class="a-q">How do I get there?</p><p>By rail to Nashik Road, by road, or via Nashik (Ozar) Airport. <a href="#getting-here">Getting here</a> and the <a href="/transport/">transport hub</a>.</p></div>
    <div class="answer"><p class="a-q">What has changed recently?</p><p>%(recent)s</p></div>
  </div>
</div></section>""" % {
        "dist": render.esc(f_("dest.trimbakeshwar.distance")["display"].lower() + " from Nashik city centre (not yet verified)"),
        "open": render.fact_inline("kumbh.mela.opening", facts, flag=False) + " (reported)",
        "close": render.fact_inline("kumbh.mela.closing", facts, flag=False) + " (reported)",
        "recent": (('<a href="/updates/#u-%s">%s</a> (%s).' % (render.esc(kumbh_live[0]["id"]), render.esc(kumbh_live[0]["title"]), render.esc(render.fmt_date(kumbh_live[0]["publishedAt"], short=True))))
                   if kumbh_live else "Nothing new is published. See <a href=\"/kumbh-mela-2027/live-updates/\">live updates</a>.")}

    dates = """<section class="sec sec-alt k-sec" id="dates" aria-labelledby="h-dates"><div class="inner">
  <h2 id="h-dates">Kumbh 2027 dates and calendar</h2>
  <p class="sec-sub">All of these dates are <strong>reported, not yet confirmed</strong> against the Authority&rsquo;s own notice. They were announced after a meeting of the Chief Minister with the akharas and reported by several publications; we will mark each one verified when an editor has read the official notice.</p>
  <ul class="date-rows">
    %(rows)s
  </ul>
  <p class="prose" style="margin-top:var(--s-5);">Other bathing days (Parva Snan) fall between these dates; our <a href="/blog/kumbh-mela-2027-all-snan-dates/">full calendar guide</a> lists them, and it is being re-checked. Dates also appear as <a href="/events/">events</a>.</p>
</div></section>""" % {"rows": "\n    ".join([
        fact_row("Mela opens (flag-hoisting)", "kumbh.mela.opening", facts, "Reported as a simultaneous ceremony at Ramkund and Kushavarta."),
        fact_row("First Amrit Snan", "kumbh.snan.1", facts),
        fact_row("Second Amrit Snan", "kumbh.snan.2", facts, "Earlier site copy called this date a Monday; it is a Tuesday."),
        fact_row("Third Amrit Snan &mdash; Nashik", "kumbh.snan.3.nashik", facts),
        fact_row("Third Amrit Snan &mdash; Trimbakeshwar", "kumbh.snan.3.trimbak", facts),
        fact_row("Mela concludes (flag lowered)", "kumbh.mela.closing", facts)])}

    locations = """<section class="sec k-sec" id="locations" aria-labelledby="h-loc"><div class="inner"><span id="two-locations" class="anchor-alias"></span>
  <h2 id="h-loc">Two locations: Ramkund and Kushavarta</h2>
  <p class="sec-sub">Unlike other Kumbh Melas, the Nashik Kumbh spans two sites about %(dist)s apart.</p>
  <div class="loc-grid">
    <div class="loc"><h3>Ramkund, Nashik (Panchavati)</h3><p>The principal bathing ghat on the Nashik side, associated with the Vaishnava akharas. In the Ramayana tradition, Rama bathed here during his exile.</p><a class="nc-link" href="/discover-nashik/panchavati/">Panchavati and Ramkund guide</a></div>
    <div class="loc"><h3>Kushavarta Tirtha, Trimbakeshwar</h3><p>The sacred bathing tank at the source of the Godavari, beside the Trimbakeshwar Jyotirlinga temple, associated with the Shaiva akharas.</p><a class="nc-link" href="/discover-nashik/trimbakeshwar/">Trimbakeshwar guide</a></div>
  </div>
</div></section>""" % {"dist": render.esc(f_("dest.trimbakeshwar.distance")["display"] + " (not yet verified)")}

    getting = """<section class="sec sec-alt k-sec" id="getting-here" aria-labelledby="h-get"><div class="inner"><span id="how-to-reach" class="anchor-alias"></span>
  <h2 id="h-get">Getting to the Kumbh</h2>
  <p class="sec-sub">Rail, road and air. Special services for the Mela have not been announced in a form we could verify.</p>
  <ul class="t-facts">%(facts)s</ul>
  <ul class="t-links" style="margin-top:var(--s-4);"><li><a href="/transport/">Transport hub: air, train, bus, road, parking</a></li><li><a href="/blog/how-to-reach-nashik-for-kumbh-mela/">Our longer guide to reaching Nashik</a></li></ul>
</div></section>""" % {"facts": "".join(fact_li(f_(x)) for x in ["kumbh.transport.special-services", "kumbh.rail.stations", "kumbh.rail.invest"])}

    passes = """<section class="sec k-sec" id="passes" aria-labelledby="h-pass"><div class="inner">
  <h2 id="h-pass">Passes and registration</h2>
  <p class="sec-sub">The most common question, and one we will not guess at.</p>
  <div class="fact-list">%(cards)s</div>
  <p class="prose" style="margin-top:var(--s-4);">Our <a href="/blog/nashik-kumbh-mela-e-pass-registration-2027/">e-pass and registration guide</a> was written before any official scheme was announced and carries a notice to that effect. Check the <a href="/sources/">Authority&rsquo;s official channels</a> before paying anyone for a &ldquo;pass&rdquo;.</p>
</div></section>""" % {"cards": "".join(render.fact_card(f_(x)) for x in ["kumbh.pass.general", "kumbh.portal.status", "kumbh.entry.charge"])}

    roads_block = ('<div class="update-list">%s</div>' % "".join(render.update_card(u, tag="h3", compact=True) for u in roads_live)) if roads_live else \
        '<p class="none">No live road, transport or railway notices right now. <a href="/updates/">See all updates</a>.</p>'
    parking = """<section class="sec sec-alt k-sec" id="parking-roads" aria-labelledby="h-park"><div class="inner">
  <h2 id="h-park">Parking, roads and traffic</h2>
  <p class="sec-sub">Parking areas, one-way systems and vehicle restrictions will be set by the police and the Authority and may change from day to day.</p>
  <div class="fact-list">%(card)s</div>
  <h3>Latest road and transport notices</h3>
  %(roads)s
</div></section>""" % {"card": render.fact_card(f_("kumbh.parking.plan")), "roads": roads_block}

    stay = """<section class="sec k-sec" id="stay" aria-labelledby="h-stay"><div class="inner"><span id="where-to-stay" class="anchor-alias"></span>
  <h2 id="h-stay">Where to stay</h2>
  <p class="prose">Rooms near Ramkund and Trimbakeshwar are likely to be in demand around the main bathing dates, so decisions about where to stay are best made early. Our <a href="/blog/where-to-stay-nashik-kumbh-mela/">where-to-stay guide</a> covers areas and options. We do not track availability or prices &mdash; check the hotel or booking site directly. Official accommodation (such as Mela camps) has not been announced in a form we could verify.</p>
  <p class="link-row"><a class="btn btn-outline" href="https://www.makemytrip.com/hotels/nashik-hotels.html" target="_blank" rel="noopener sponsored" data-track="accommodation_click">Search on MakeMyTrip (external)</a><a class="btn btn-outline" href="https://www.goibibo.com/hotels/hotels-in-nashik/" target="_blank" rel="noopener sponsored" data-track="accommodation_click">Search on Goibibo (external)</a></p>
  <p class="sec-sub" style="margin:var(--s-3) 0 0;">External booking sites; links may earn us a commission at no cost to you. We do not take bookings or handle payments.</p>
</div></section>"""

    e112 = f_("safety.emergency.number")
    safety = """<section class="sec sec-alt k-sec" id="safety" aria-labelledby="h-safe"><div class="inner">
  <h2 id="h-safe">Safety, medical and emergencies</h2>
  <div class="answer"><p class="a-q">In an emergency</p><p>Call <strong>%(num)s</strong>, India&rsquo;s single emergency number. %(badge)s</p></div>
  <h3>Reported medical arrangements</h3>
  <div class="fact-list">%(health)s</div>
  <p class="prose" style="margin-top:var(--s-4);">Crowd-management and security arrangements for the Mela will be set by the Authority and the police; we could not locate a published plan, so we do not describe one. On the day, follow the instructions of police and volunteers, agree a meeting point with your group, and keep the Authority&rsquo;s official contact details to hand &mdash; <a href="https://divcomnashik.maharashtra.gov.in/en/contact-details/" rel="noopener noreferrer" data-track="official_source_click" data-track-item="ntka-contact">Authority contact page (official)</a>.</p>
  <ul class="t-links"><li><a href="/blog/nashik-kumbh-mela-for-senior-citizens-2027/">Guide for senior citizens</a></li><li><a href="/blog/nashik-kumbh-mela-for-women-solo-travellers/">Guide for women and solo travellers</a></li></ul>
</div></section>""" % {"num": render.esc(e112["display"]), "badge": render.fact_badge(e112["status"], e112.get("verifiedAt")), "health": render.fact_card(f_("kumbh.health.plan"))}


    tips = """<section class="sec k-sec" id="tips" aria-labelledby="h-tips"><div class="inner"><span id="what-to-expect" class="anchor-alias"></span>
  <h2 id="h-tips">Practical tips for crowded days</h2>
  <p class="sec-sub">General advice for any large gathering &mdash; none of it depends on arrangements that have not been announced.</p>
  <ul class="prose" style="margin-left:1.3rem;">
    <li>Carry as little as you can, and keep valuables at your lodging.</li>
    <li>Agree a meeting point with your group before you leave, and keep each person&rsquo;s phone number written down.</li>
    <li>Download offline maps &mdash; mobile data can be slow in large crowds.</li>
    <li>Wear simple clothes you can bathe in, and shoes you can walk a long way in.</li>
    <li>Follow the instructions of police and volunteers over anything you read online, including here.</li>
  </ul>
</div></section>"""

    access = """<section class="sec k-sec" id="accessibility" aria-labelledby="h-acc"><div class="inner">
  <h2 id="h-acc">Accessibility at the Kumbh</h2>
  <p class="prose">Ramkund and Kushavarta are reached by steps, and arrangements for older and disabled pilgrims will be set by the Authority. We have not yet verified step-free routes, accessible toilets or assistance points. See <a href="/accessible-nashik/">Accessible Nashik</a> for how we classify access, the questions to ask, and what we are collecting.</p>
</div></section>"""

    guides = """<section class="sec sec-alt k-sec" id="guides" aria-labelledby="h-guides"><div class="inner">
  <h2 id="h-guides">Guides for every kind of visitor</h2>
  <p class="sec-sub">These guides were written before official arrangements were published. They are being checked against official sources one at a time; each shows a notice about how current it is.</p>
  <ul class="guide-links">%s</ul>
</div></section>""" % "".join('<li><a href="%s"><span class="gl-k">%s</span><span class="gl-t">%s</span><span class="gl-d">%s</span></a></li>' % (render.esc(h), render.esc(k), render.esc(t), render.esc(d)) for k, t, d, h in GUIDES)

    figures = """<section class="sec k-sec" id="figures" aria-labelledby="h-fig"><div class="inner">
  <h2 id="h-fig">Figures: attendance and spending</h2>
  <p class="sec-sub">Numbers about the Kumbh are published at very different scales depending on what they count. We show each one with its scope and source rather than choosing one &mdash; and we have <a href="/updates/#u-2026-10-04-kumbh-figure-withdrawn">withdrawn an earlier figure</a> we could not source.</p>
  <div class="fact-list">%s</div>
</div></section>""" % "".join(render.fact_card(f_(x)) for x in ["kumbh.devplan.amount", "kumbh.attendance.estimate", "kumbh.rail.invest"])

    faq_items = "".join('<details class="faq-item"><summary>%s</summary><div class="faq-answer"><p>%s</p></div></details>' % (render.esc(q), a) for q, a in FAQS)
    faqs = """<section class="sec sec-alt k-sec" id="faqs" aria-labelledby="h-faq"><div class="inner">
  <h2 id="h-faq">Frequently asked questions</h2>
  %s
</div></section>""" % faq_items

    verify = render.verify_block("/kumbh-mela-2027/", "reported", None, stamp, SOURCES,
                                 caveat="Kumbh information may evolve. Check with the official authority before travelling.")
    updates_block = ('<div class="update-list">%s</div>' % "".join(render.update_card(u, tag="h3", compact=True) for u in kumbh_live)) if kumbh_live else \
        '<p class="none">No live Kumbh updates right now. <a href="/kumbh-mela-2027/live-updates/">Kumbh live updates</a> will show verified notices as they are published.</p>'
    latest = """<section class="sec k-sec" id="latest" aria-labelledby="h-latest"><div class="inner">
  <h2 id="h-latest">Latest Kumbh updates</h2>
  %s
  <p class="link-row"><a class="btn btn-outline" href="/kumbh-mela-2027/live-updates/">Kumbh live updates</a><a class="btn btn-outline" href="/events/">Events and dates</a></p>
</div></section>""" % updates_block

    body = (head + live_band(prof) + '\n<nav class="sec-nav" aria-label="On this page" data-section-nav><ul>%s</ul></nav>\n' % nav
            + glance + latest + dates + locations + getting + passes + parking + stay + safety + tips + access + guides + figures + faqs
            + '<section class="sec"><div class="inner">%s</div></section>\n' % verify + phase_json())

    faq_ld = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": render.plain(a)}} for q, a in FAQS]}
    html = pagekit.render(
        "/kumbh-mela-2027/", "Nashik Kumbh Mela 2027: Simhastha guide with dates, passes, roads and sources",
        "A guide to the Simhastha Kumbh Mela at Nashik and Trimbakeshwar. Reported dates, passes, roads, safety and figures, each marked verified, reported or not yet confirmed, with sources.",
        body, crumbs=[("Home", "/"), ("Kumbh Mela 2027", "/kumbh-mela-2027/")], css=CSS, jsonld=[faq_ld], raw_title=True,
        modified=stamp)
    html = html.replace("</head>", '  <meta name="nt-section" content="kumbh" />\n</head>', 1)
    pagekit.write("/kumbh-mela-2027/", html)


def live_updates_page():
    prof = lifecycle.profile()
    live = content.live_updates(category="Kumbh")
    up_events = [e for e in content.events()[0] if e["category"] == "Kumbh"][:4]
    stamp = content.latest_stamp(live, "lastCheckedAt", "verifiedAt", "publishedAt")
    lst = ('<div class="update-list">%s</div>' % "".join(render.update_card(u) for u in live)) if live else """<div class="empty-state"><h3>No live Kumbh updates right now</h3>
      <p>We publish an update only when an editor has checked its source, so nothing here means nothing has been verified yet &mdash; not that nothing is happening. The official source is the Authority; see <a href="/sources/">our sources</a>.</p></div>"""
    ev = ('<div class="event-list">%s</div>' % "".join(render.event_card(e) for e in up_events)) if up_events else ""
    head = pagekit.page_head(
        "Kumbh live updates",
        "Verified notices about the Simhastha Kumbh Mela &mdash; transport, roads, safety, government announcements &mdash; each with its source and the time it was last checked.",
        crumbs=[("Home", "/"), ("Kumbh Mela 2027", "/kumbh-mela-2027/"), ("Live updates", None)], eyebrow="Kumbh Mela",
        extra='<p class="ph-stamp"><span>Last checked: <strong>%s</strong></span><span>Phase: <strong>%s</strong></span></p>' % (
            render.esc(render.fmt_dt(stamp) if stamp else "not yet"), render.esc(prof["label"])))
    body = head + live_band(prof) + """
<section class="sec k-sec"><div class="inner">
  <h2 class="sec-title">Live now</h2>
  <p class="sec-sub">Kumbh items archive automatically when they expire, and all live Kumbh items move to the <a href="/updates/archive/">archive</a> after the Mela closes.</p>
  %s
  <h2 class="sec-title" style="margin-top:var(--s-10);">Next reported dates</h2>
  <p class="sec-sub">Reported, not yet confirmed against the Authority&rsquo;s own notice.</p>
  %s
  <p class="link-row"><a class="btn btn-outline" href="/kumbh-mela-2027/">Kumbh hub</a><a class="btn btn-outline" href="/updates/">All updates</a><a class="btn btn-outline" href="/sources/">Our sources</a></p>
</div></section>
""" % (lst, ev) + phase_json()
    html = pagekit.render(
        "/kumbh-mela-2027/live-updates/", "Kumbh live updates: verified notices with sources",
        "Verified notices about the Simhastha Kumbh Mela, each with its source, publication, verification and last-checked times. Items expire automatically and archive after the Mela.",
        body, crumbs=[("Home", "/"), ("Kumbh Mela 2027", "/kumbh-mela-2027/"), ("Live updates", "/kumbh-mela-2027/live-updates/")],
        css=CSS, raw_title=True, page_type="CollectionPage", extra_head='<link rel="alternate" type="application/atom+xml" title="NashikTourism.com verified updates" href="/updates/feed.xml" />')
    html = html.replace("</head>", '  <meta name="nt-section" content="kumbh" />\n</head>', 1)
    pagekit.write("/kumbh-mela-2027/live-updates/", html)


def main():
    hub()
    live_updates_page()
    print("kumbh hub + live-updates built (phase: %s)" % lifecycle.profile()["id"])


if __name__ == "__main__":
    main()
