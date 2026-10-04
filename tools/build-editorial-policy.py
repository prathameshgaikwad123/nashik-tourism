#!/usr/bin/env python3
"""
Generate /editorial-policy/.

This page states commitments the site's tooling enforces rather than aspirations:
the status labels come from data/facts.json, the approval rule from
tools/nt/risk.py, the expiry behaviour from tools/nt/render.py, and the
corrections log from data/changelog.json. If a rule changes in code, change the
sentence here.

The wording of the commitments (sponsored content, AI assistance, corrections)
is the site owner's to confirm — see the delivery report.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import pagekit, render, risk, store  # noqa: E402

CSS = """    .pol { max-width: 760px; margin: 0 auto; }
    .pol h2 { font-family: var(--font-display); font-size: 1.25rem; font-weight: 800; letter-spacing: var(--ls-heading); color: var(--ink); margin: var(--s-10) 0 var(--s-3); padding-bottom: var(--s-2); border-bottom: 2px solid var(--border); scroll-margin-top: calc(var(--nav-h) + var(--s-4)); }
    .pol h2:first-of-type { margin-top: 0; }
    .pol p, .pol li { color: var(--body-clr); line-height: var(--lh-prose); font-size: 1rem; }
    .pol p { margin-bottom: var(--s-4); }
    .pol ul { margin: 0 0 var(--s-4) 1.3rem; } .pol li { margin-bottom: var(--s-2); }
    .pol a { color: var(--primary); text-decoration: underline; text-underline-offset: 2px; }
    .pol a:hover { color: var(--saffron-deep); }
    .pol .legend { display: grid; gap: var(--s-3); margin: var(--s-4) 0 var(--s-5); }
    .pol .legend > div { display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--s-2) var(--s-3); }
    .pol .legend dd { flex: 1 1 14rem; font-size: 0.95rem; line-height: 1.5; }
    .pol .clog { list-style: none; margin-left: 0; display: grid; gap: var(--s-3); }
    .pol .clog li { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s-3) var(--s-4); }
    .pol .clog time { font-family: var(--font-display); font-size: 0.78rem; font-weight: 700; color: var(--stone-ink); display: block; }"""

FACT_MEANING = [
    ("verified", "An editor has read the official source we link to and it supports the statement. The date is shown."),
    ("reported", "Credible reporting, or an official page we have located, says so &mdash; but an editor has not yet confirmed it against the official source. Treat it as likely, not settled."),
    ("not_verified", "Carried over from earlier copy with no source behind it. Shown so you can see it, labelled so you do not rely on it."),
    ("disputed", "Sources disagree. We show every figure, with what each one counts and where it comes from, instead of picking one."),
]


def main():
    legend = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (render.fact_badge(k), v) for k, v in FACT_MEANING)
    corrections = [e for e in store.load("changelog")["entries"] if e["type"] == "corrected"]
    corrections.sort(key=lambda e: e["date"], reverse=True)
    clog = "".join('<li><time datetime="%s">%s</time>%s &mdash; <a href="%s">%s</a></li>' % (
        render.esc(e["date"]), render.esc(render.fmt_date(e["date"])), render.esc(e["summary"]),
        render.esc(e["path"]), render.esc(render.label_for_path(e["path"]))) for e in corrections)
    high = ", ".join(x.replace("-", " ") for x in sorted({r[0] for r in risk.RULES}))
    head = pagekit.page_head(
        "Editorial policy",
        "How NashikTourism.com decides what to publish, how it marks what it is sure of, and what it does when it is wrong.",
        crumbs=[("Home", "/"), ("Editorial policy", None)], eyebrow="About this site")
    body = head + """
<section class="sec"><div class="inner"><div class="pol">
  <h2 id="independent">We are independent, not official</h2>
  <p>NashikTourism.com is an independent travel and information guide. We are not a government body, not the Nashik–Trimbakeshwar Kumbh Mela Authority, not a temple trust and not an official tourism organisation. Nothing here is an official notice. Where something is decided by an authority &mdash; Kumbh arrangements, temple timings, train schedules, road closures, entry rules &mdash; that authority is the source of truth, and we say so and link to it.</p>

  <h2 id="sources">Official sources come first</h2>
  <p>We rank sources. Official bodies (the Maharashtra Government, the Nashik district administration, the Authority, the railways, the police, an attraction&rsquo;s own official site) come first. Established news is used to find out what is happening, and a news report becomes a fact on this site only when an official source supports it. A business&rsquo;s own published information beats a third-party listing. Social media is never treated as confirmation. The full list, by tier, is on <a href="/sources/">our sources page</a>.</p>
  <p>Important claims show where they come from: the name of the source, a link to it, when we last checked it, and when an editor last verified it. We do not write &ldquo;according to sources&rdquo;.</p>

  <h2 id="status">How we mark what we know</h2>
  <p>Every fact that matters carries one of four labels:</p>
  <dl class="legend">%(legend)s</dl>
  <p>When we do not know something, we say <em>Information not yet confirmed</em> and point you to the official source. We do not fill gaps with a plausible guess: no invented dates, prices, timings, transport schedules, parking details, hotel availability, crowd numbers, rules, passes or official statistics.</p>

  <h2 id="dates">Dates and arrangements can change</h2>
  <p>The Simhastha Kumbh Mela is being planned in public and details evolve. Dates we show are labelled <em>reported</em> until the Authority&rsquo;s own notice is linked. Timings at temples and ghats can change on festival days. Please confirm anything you are relying on, close to your travel date, with the official source.</p>

  <h2 id="approval">A person approves anything that could hurt you if it is wrong</h2>
  <p>Some information is high-stakes. Anything touching these areas is published only after a named human editor has approved it, whoever or whatever drafted it: %(high)s. Software that monitors sources may suggest an item, but it cannot publish one that falls in these areas, and it publishes nothing without review unless the site owner has explicitly changed that setting.</p>

  <h2 id="expiry">Time-sensitive items expire</h2>
  <p>Updates that are only true for a while carry an expiry date. When it passes, the item moves to the <a href="/updates/archive/">archive</a> automatically &mdash; it does not keep looking current. We keep the record rather than deleting it, so you can see what was said and when.</p>

  <h2 id="corrections">Corrections</h2>
  <p>When we find a mistake, we correct it, say so, and keep a record. If you find one, <a href="/contact/">please tell us</a> and, if you can, point us to the official source. Corrections we have made:</p>
  <ul class="clog">%(clog)s</ul>

  <h2 id="sponsored">Sponsored content and affiliate links</h2>
  <p>We do not accept paid editorial content or sponsored recommendations. The site is supported by display advertising and by affiliate links to booking sites. Those links are marked as sponsored in the page code, and the surrounding text says that they are external sites with their own prices and terms. If we ever publish sponsored content, it will be labelled as sponsored on the page.</p>

  <h2 id="ai">AI-assisted work</h2>
  <p>We may use AI tools to help draft, summarise, classify or extract information from sources. AI output is never treated as a source and never publishes anything on its own in the high-stakes areas above. Every item that appears on the site has been reviewed by a person; an AI summary of an official page is checked against the page itself before it is shown.</p>

  <h2 id="access">Accessibility</h2>
  <p>We aim for WCAG 2.2 AA: keyboard operation, visible focus, readable contrast, descriptive image text and layouts that work from a 320px phone upwards. We never describe a place as accessible without verifying it &mdash; see <a href="/accessible-nashik/">Accessible Nashik</a>. If something on this site is hard to use, <a href="/contact/">tell us</a>.</p>

  <p>Related: <a href="/disclaimer/">Disclaimer</a> &middot; <a href="/about/">About this site</a> &middot; <a href="/sources/">Our sources</a> &middot; <a href="/updates/">Verified updates</a></p>
</div></div></section>
""" % {"legend": legend, "high": high, "clog": clog}
    html = pagekit.render(
        "/editorial-policy/", "Editorial policy: how we verify what we publish",
        "NashikTourism.com is independent, ranks official sources first, labels what is verified, reported or unconfirmed, expires time-sensitive items and logs corrections.",
        body, crumbs=[("Home", "/"), ("Editorial policy", "/editorial-policy/")], css=CSS, raw_title=True,
        modified=corrections[0]["date"] if corrections else None)
    pagekit.write("/editorial-policy/", html)
    print("editorial policy: %d corrections listed" % len(corrections))


if __name__ == "__main__":
    main()
