#!/usr/bin/env python3
"""
Generate /accessible-nashik/ from data/accessibility.json.

The rule that shapes this page: a place is never called accessible without
verification. Every place starts at 'accessibility unknown', which is a
statement about what we know, not about the place. The page therefore leads with
how to ask the right questions and with what we do know (emergency number, the
reported 200 steps at Pandavleni), and fills in as records are verified.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import pagekit, render, store  # noqa: E402

CSS = """    .a-table th, .a-table td { text-align: left; vertical-align: top; }
    .a-places { list-style: none; display: grid; gap: var(--s-3); }
    .a-place { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s-4) var(--s-5); display: grid; gap: var(--s-2); }
    .a-place h3 { font-family: var(--font-display); font-size: 1.02rem; font-weight: 800; color: var(--ink); }
    .a-place h3 a { color: inherit; text-decoration: underline; text-underline-offset: 2px; }
    .a-place p { font-size: 0.92rem; line-height: 1.55; color: var(--body-clr); }
    .a-legend { display: grid; gap: var(--s-3); }
    .a-legend > div { display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--s-2) var(--s-3); }
    .a-legend dd { flex: 1 1 15rem; font-size: 0.92rem; line-height: 1.5; color: var(--body-clr); }
    .a-topics { display: grid; gap: var(--s-4); }
    .a-topic { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s-5); scroll-margin-top: calc(var(--nav-h) + var(--tap) + var(--s-3)); }
    .a-topic h3 { font-family: var(--font-display); font-size: 1.05rem; font-weight: 800; color: var(--ink); margin-bottom: var(--s-1); }
    .a-topic p { font-size: 0.95rem; line-height: 1.6; color: var(--body-clr); margin-bottom: var(--s-2); }
    .a-topic .t-facts, .a-topic .t-links { margin-top: var(--s-3); }
    .a-ask { margin: var(--s-4) 0 0 1.3rem; } .a-ask li { color: var(--body-clr); line-height: 1.6; margin-bottom: var(--s-2); }"""


def fact_li(f):
    return """<li><span class="t-fl">%s</span><span class="t-fv">%s</span><span class="t-fs">%s &middot; Source: %s</span></li>""" % (
        render.esc(f["fact"]), render.fact_value_html(f), render.fact_badge(f["status"], f.get("verifiedAt")), render.fact_source_html(f))


def main():
    data = store.load("accessibility")
    facts = render.facts_index()
    dests = {d["slug"]: d for d in store.load("destinations")["destinations"]}

    legend = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (render.access_badge(s["id"]), render.esc(s["meaning"])) for s in data["statuses"])
    places = []
    for p in data["places"]:
        d = dests[p["slug"]]
        note = ""
        if p.get("notes"):
            note = "<p>%s</p>" % render.esc(p["notes"])
        ver = ('Verified %s' % render.esc(render.fmt_date(p["verifiedAt"], short=True))) if p.get("verifiedAt") else "Not yet verified by our editors"
        places.append("""<li class="a-place"><h3><a href="/discover-nashik/%s/">%s</a></h3>
      <div>%s</div>%s<p class="t-fs">%s</p></li>""" % (render.esc(p["slug"]), render.esc(render.plain(d["name"])), render.access_badge(p["status"]), note, ver))

    topics = []
    for t in data["topics"]:
        extra = ""
        fs = [facts[x] for x in t.get("factRefs", []) if x in facts]
        if fs:
            extra += '<ul class="t-facts">%s</ul>' % "".join(fact_li(f) for f in fs)
        if t.get("links"):
            extra += '<ul class="t-links">%s</ul>' % "".join('<li><a href="%s">%s</a></li>' % (render.esc(h), render.esc(l)) for h, l in t["links"])
        topics.append("""<article class="a-topic" id="%s"><h3>%s</h3><p>%s</p>%s%s</article>""" % (
            render.esc(t["id"]), render.esc(t["title"]), render.esc(t["intro"]),
            ("<p><em>%s</em></p>" % render.esc(t["emptyNote"])) if t.get("emptyNote") else "", extra))
    ask = "".join("<li>%s</li>" % render.esc(q) for q in data["askBeforeYouGo"])
    nav = "".join('<li><a href="#%s">%s</a></li>' % (i, l) for i, l in [("status", "How we classify"), ("places", "Places"), ("topics", "Topics"), ("ask", "Questions to ask")])
    verify = render.verify_block("/accessible-nashik/", "not_verified", None, "2026-10-04", ["ntka", "india-112", "indian-railways", "msrtc"],
                                 caveat="No place is described as accessible without verification. Arrangements can change during festivals.")
    head = pagekit.page_head(
        "Accessible Nashik",
        "Step-free access, toilets, seating, senior-friendly arrangements and emergency information &mdash; and an honest record of what we have and have not verified.",
        crumbs=[("Home", "/"), ("Accessible Nashik", None)], eyebrow="Accessibility hub")
    body = head + """
<nav class="sec-nav" aria-label="On this page" data-section-nav><ul>%(nav)s</ul></nav>
<section class="sec"><div class="inner">
  <div class="status-notice" role="note"><p class="sn-title">What this page does and does not tell you</p>
  <p>We have not yet verified step-free access, accessible toilets or assistance arrangements at any place we cover. &ldquo;Accessibility unknown&rdquo; is a statement about what we know, not about the place. Please ask the venue before you travel &mdash; the questions below help &mdash; and <a href="/contact/">tell us what you find</a> so we can verify and publish it.</p></div>
  <h2 class="sec-title" id="status">How we classify access</h2>
  <p class="sec-sub">Four statuses, always shown as words as well as symbols.</p>
  <dl class="a-legend">%(legend)s</dl>
</div></section>
<section class="sec sec-alt"><div class="inner">
  <h2 class="sec-title" id="places">The places we cover</h2>
  <p class="sec-sub">Current status of each destination guide.</p>
  <ul class="a-places">%(places)s</ul>
</div></section>
<section class="sec"><div class="inner">
  <h2 class="sec-title" id="topics">By topic</h2>
  <p class="sec-sub">Entries appear under each topic only once they are verified.</p>
  <div class="a-topics">%(topics)s</div>
</div></section>
<section class="sec sec-alt"><div class="inner">
  <h2 class="sec-title" id="ask">Questions to ask before you go</h2>
  <p class="sec-sub">Useful when you phone a venue, hotel or operator.</p>
  <ul class="a-ask">%(ask)s</ul>
  <p class="link-row"><a class="btn btn-outline" href="/blog/nashik-kumbh-mela-for-senior-citizens-2027/">Guide for senior citizens</a><a class="btn btn-outline" href="/transport/">Transport hub</a></p>
</div></section>
<section class="sec"><div class="inner">%(verify)s</div></section>
""" % {"nav": nav, "legend": legend, "places": "".join(places), "topics": "".join(topics), "ask": ask, "verify": verify}
    html = pagekit.render(
        "/accessible-nashik/", "Accessible Nashik: access information, verified honestly",
        "Accessibility information for Nashik and the Kumbh Mela: wheelchair access, step-free routes, toilets, senior facilities and emergency information. Nothing is called accessible without verification.",
        body, crumbs=[("Home", "/"), ("Accessible Nashik", "/accessible-nashik/")], css=CSS, raw_title=True)
    pagekit.write("/accessible-nashik/", html)
    print("accessible: %d places, %d topics" % (len(data["places"]), len(data["topics"])))


if __name__ == "__main__":
    main()
