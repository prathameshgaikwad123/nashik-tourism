#!/usr/bin/env python3
"""
Generate /sources/ — the public source registry.

Every 'Check with the official authority' link on the site points here. The page
is generated from data/sources.json, so a source is added once and appears here,
in the monitor's target list and in every fact that cites it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import enums, pagekit, render, store  # noqa: E402

CAT_LABEL = {"kumbh": "Kumbh Mela", "government": "Government", "transport": "Transport", "railway": "Railways",
             "airport": "Airport", "roads": "Roads", "police": "Police", "tourism": "Tourism", "events": "Events",
             "weather": "Weather", "attractions": "Attractions", "accommodation": "Accommodation",
             "accessibility": "Accessibility", "safety": "Safety", "news": "News"}
FREQ = {"hourly": "checked hourly", "daily": "checked daily", "weekly": "checked weekly", "monthly": "checked monthly", "manual": "checked by an editor as needed"}
TIERS = [("official", "Tier 1 · Official", "Government bodies, authorities, railways, airports and the venues&rsquo; own official sites. Where these disagree with anything else, they win."),
         ("reliable_news", "Tier 2 · Established news", "Used to find out what is happening. A news report is a lead; it becomes a fact here only when an official source supports it."),
         ("business_official", "Tier 3 · A business&rsquo;s own information", "Hotels, vineyards, restaurants and tours describing themselves. We prefer this to third-party listings."),
         ("data_provider", "Data providers", "Automated feeds used for numbers (such as the weather on Nashik Now), not for official statements.")]


def main():
    sources = [s for s in store.load("sources")["sources"] if s["id"] != "editorial" and not s.get("citation")]
    sections = []
    for rel, title, blurb in TIERS:
        group = [s for s in sources if s["reliability"] == rel]
        if not group:
            continue
        group.sort(key=lambda s: (CAT_LABEL.get(s["category"], s["category"]), s["name"]))
        rows = []
        for s in group:
            name = (render.ext_link(s["url"], render.esc(s["name"]), item=s["id"]) if s.get("url")
                    else render.esc(s["name"]) + ' <span class="src-tier">Official link to be added</span>')
            rows.append("""<li class="src-row"><span class="src-name">%s</span>
        <span class="src-meta"><span class="tag">%s</span> %s</span>
        <span class="src-scope">%s</span></li>""" % (
                name, render.esc(CAT_LABEL.get(s["category"], s["category"])),
                render.esc(FREQ.get(s["checkFrequency"], "")), render.esc(s.get("scope") or "")))
        sections.append("""<section class="sec%s"><div class="inner">
    <h2 class="sec-title">%s</h2><p class="sec-sub">%s</p>
    <ul class="src-table">%s</ul></div></section>""" % (" sec-alt" if len(sections) % 2 else "", title, blurb, "\n".join(rows)))
    head = pagekit.page_head(
        "Where our information comes from",
        "The official sources behind this site. Use these links to check anything here for yourself &mdash; they, not NashikTourism.com, are the source of truth.",
        crumbs=[("Home", "/"), ("Sources", None)], eyebrow="Sources")
    css = """    .src-table { list-style: none; display: grid; gap: var(--s-3); }
    .src-row { display: grid; gap: var(--s-1); background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s-4) var(--s-5); }
    .src-name { font-family: var(--font-display); font-weight: 800; font-size: 1rem; line-height: 1.3; overflow-wrap: anywhere; }
    .src-name a { color: var(--primary); text-decoration: underline; text-underline-offset: 2px; }
    .src-meta { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-2); font-size: 0.82rem; color: var(--stone-ink); }
    .src-scope { font-size: 0.92rem; line-height: 1.5; color: var(--body-clr); }"""
    body = head + """
<section class="sec"><div class="inner">
  <div class="status-notice" role="note"><p class="sn-title">Social media</p>
  <p>Social-media posts are never treated as confirmation. If a post is the only place something appears, we say so and do not present it as fact.</p></div>
  <p class="prose"><a href="/editorial-policy/">Our editorial policy</a> explains how these sources are ranked, and what we do when they disagree. Links open the source&rsquo;s own site in this tab.</p>
</div></section>
%s
""" % "\n".join(sections)
    html = pagekit.render(
        "/sources/", "Our sources: official links behind every guide",
        "The official sources NashikTourism.com checks, ranked by reliability: Maharashtra Government, the Kumbh Mela Authority, railways, police and more. Use them to verify anything here.",
        body, crumbs=[("Home", "/"), ("Sources", "/sources/")], css=css, raw_title=True)
    pagekit.write("/sources/", html)
    print("sources page: %d sources listed" % len(sources))


if __name__ == "__main__":
    main()
