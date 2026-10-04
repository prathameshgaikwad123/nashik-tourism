#!/usr/bin/env python3
"""
Generate /transport/ from data/transport.json.

Modular by construction: each section lists fact ids (resolved from
data/facts.json with their verification status), the official sources to check,
a link to the long-form guide, and the update categories whose latest live items
appear inside it. Change a fact once and every section that shows it changes;
publish a Roads update and it appears in the Road, Trimbakeshwar and Kumbh
sections without touching this page.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import content, pagekit, render, store  # noqa: E402

GROUPS = [("reach", "How to reach Nashik", "The four ways in, and what we know about each."),
          ("routes", "Routes from the big cities", "Distances and times from our earlier guide, labelled by how well verified they are."),
          ("places", "Key places and links", "Airport, station, Trimbakeshwar and getting around."),
          ("kumbh", "Kumbh transport and parking", "What has and has not been announced.")]

CSS = """    .tsec { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s-5); scroll-margin-top: calc(var(--nav-h) + var(--tap) + var(--s-3)); }
    .tsec + .tsec { margin-top: var(--s-4); }
    .tsec h3 { font-family: var(--font-display); font-size: 1.15rem; font-weight: 800; letter-spacing: var(--ls-heading); color: var(--ink); margin-bottom: var(--s-2); }
    .tsec .t-sum { color: var(--body-clr); line-height: var(--lh-body); max-width: 68ch; margin-bottom: var(--s-4); }
    .tsec h4 { font-family: var(--font-display); font-size: 0.7rem; font-weight: 700; letter-spacing: var(--ls-eyebrow); text-transform: uppercase; color: var(--stone-ink); margin: var(--s-5) 0 var(--s-2); }
    .t-live { list-style: none; display: grid; gap: var(--s-2); }
    .t-none { color: var(--stone-ink); font-size: 0.9rem; }"""


def fact_li(fid, facts):
    f = facts.get(fid)
    if not f:
        return ""
    return """<li><span class="t-fl">%s &mdash; %s</span><span class="t-fv">%s</span>
        <span class="t-fs">%s &middot; Source: %s</span></li>""" % (
        render.esc(f["subject"]), render.esc(f["fact"]), render.fact_value_html(f),
        render.fact_badge(f["status"], f.get("verifiedAt")), render.fact_source_html(f))


def section_html(sec, facts, sources):
    parts = ['<article class="tsec" id="%s"><h3>%s</h3><p class="t-sum">%s</p>' % (render.esc(sec["id"]), render.esc(sec["title"]), render.esc(sec["summary"]))]
    if sec.get("facts"):
        parts.append("<h4>What we know</h4><ul class=\"t-facts\">%s</ul>" % "".join(fact_li(f, facts) for f in sec["facts"]))
    cats = sec.get("liveCategories") or []
    if cats:
        live = content.live_updates(categories=cats, limit=3)
        if live:
            parts.append('<h4>Latest verified notices</h4><div class="update-list">%s</div>' % "".join(render.update_card(u, tag="h5", compact=True) for u in live))
        else:
            parts.append('<h4>Latest verified notices</h4><p class="t-none">No live %s notices right now. See <a href="/updates/">all updates</a>.</p>' % render.esc(" / ".join(c.lower() for c in cats)))
    if sec.get("sources"):
        parts.append("<h4>Official sources to check</h4>" + render.sources_list_html(sec["sources"], sources))
    if sec.get("guides"):
        parts.append("<h4>More detail</h4><ul class=\"t-links\">%s</ul>" % "".join('<li><a href="%s">%s</a></li>' % (render.esc(h), render.esc(t)) for h, t in sec["guides"]))
    parts.append("</article>")
    return "".join(parts)


def main():
    data = store.load("transport")
    facts, sources = render.facts_index(), render.sources_index()
    secs = data["sections"]
    nav = "".join('<li><a href="#%s">%s</a></li>' % (s["id"], render.esc(s["title"])) for s in secs)
    blocks = []
    for gid, gtitle, gsub in GROUPS:
        group = [s for s in secs if s["group"] == gid]
        if not group:
            continue
        blocks.append("""<section class="sec%s"><div class="inner">
    <h2 class="sec-title" id="g-%s">%s</h2><p class="sec-sub">%s</p>
    %s</div></section>""" % (" sec-alt" if len(blocks) % 2 else "", gid, gtitle, gsub, "\n".join(section_html(s, facts, sources) for s in group)))
    all_f = {fid for s in secs for fid in s.get("facts", [])}
    stamp = max([facts[f].get("lastCheckedAt") or "" for f in all_f] + [""]) or None
    head = pagekit.page_head(
        "Getting to and around Nashik",
        "By air, train, bus and road &mdash; what we know, how sure we are, and which official source to check before you go.",
        crumbs=[("Home", "/"), ("Transport", None)], eyebrow="Transport hub",
        extra='<p class="ph-stamp"><span>Last checked: <strong>%s</strong></span></p>' % render.esc(render.fmt_date(stamp) if stamp else "not yet recorded"))
    verify = render.verify_block("/transport/", "reported", None, stamp,
                                 ["central-railway", "msrtc", "aai", "nashik-district-how-to-reach"],
                                 caveat="Schedules and arrangements may change. Confirm with the operator or authority before travelling.")
    body = head + """
<nav class="sec-nav" aria-label="On this page" data-section-nav><ul>%s</ul></nav>
<section class="sec" style="padding-bottom:0;"><div class="inner">
  <div class="status-notice" role="note"><p class="sn-title">Check before you travel</p>
  <p>Timetables, special trains, bus services and road arrangements change &mdash; especially around the Kumbh Mela. Each figure below shows how well it is verified. For anything you are relying on, check the official source linked in that section.</p></div>
</div></section>
%s
<section class="sec"><div class="inner">%s</div></section>
""" % (nav, "\n".join(blocks), verify)
    html = pagekit.render(
        "/transport/", "Transport hub: how to reach Nashik and get around",
        "How to reach Nashik by air, train, bus and road, plus Mumbai, Pune and Delhi routes, Trimbakeshwar, local transport and Kumbh transport, each fact labelled by how well it is verified.",
        body, crumbs=[("Home", "/"), ("Transport", "/transport/")], css=CSS, raw_title=True, modified=stamp)
    pagekit.write("/transport/", html)
    print("transport: %d sections, %d facts" % (len(secs), len(all_f)))


if __name__ == "__main__":
    main()
