#!/usr/bin/env python3
"""
Generate /updates/, /updates/archive/ and the update feeds from data/updates.json.

    /updates/            live items, newest first, filterable by category
    /updates/archive/    expired / archived items — kept, never deleted
    /updates/feed.xml    Atom feed of live items
    /updates/feed.json   JSON Feed 1.1 of live items

Every card shows Source, Published, Verified and Last checked in the markup. An
item whose expiresAt has passed lands in the archive on the next build, and the
browser archives it in place immediately (see /site.js), so a stale road closure
cannot outlive its expiry by a rebuild interval.

Editors add items with tools/cms.py; nobody edits this page's HTML.
"""
import json
import os
import sys
from xml.sax.saxutils import escape as xesc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import content, enums, pagekit, render, store  # noqa: E402
from nt.paths import ROOT, SITE  # noqa: E402

LEGEND = [
    ("confirmed", "Confirmed against an official source and re-checked."),
    ("developing", "Reported and still unfolding. Details may change."),
    ("changed", "An earlier position changed. The card explains how."),
    ("cancelled", "Called off or withdrawn."),
    ("archived", "No longer current. Kept as a record, never deleted."),
]

CSS = """    .legend { display: grid; gap: var(--s-3); margin-top: var(--s-4); }
    .legend > div { display: flex; flex-wrap: wrap; align-items: baseline; gap: var(--s-2) var(--s-3); }
    .legend dd { color: var(--body-clr); font-size: 0.92rem; line-height: 1.5; flex: 1 1 14rem; }
    .how-box { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s-5); }
    .how-box summary { display: flex; align-items: center; min-height: var(--tap); cursor: pointer; font-family: var(--font-display); font-size: 0.95rem; font-weight: 800; color: var(--ink); }
    .feed-links { display: flex; flex-wrap: wrap; gap: var(--s-4); margin-top: var(--s-6); }
    .feed-links a { display: inline-flex; align-items: center; min-height: var(--tap); font-family: var(--font-display); font-size: 0.84rem; font-weight: 700; color: var(--primary); text-decoration: underline; text-underline-offset: 2px; }
    .group-h { font-family: var(--font-display); font-size: 1.1rem; font-weight: 800; color: var(--ink); margin: var(--s-8) 0 var(--s-3); }"""

FEED_HEAD = ('<link rel="alternate" type="application/atom+xml" title="NashikTourism.com verified updates" href="/updates/feed.xml" />\n'
             '  <link rel="alternate" type="application/feed+json" title="NashikTourism.com verified updates" href="/updates/feed.json" />')


def legend_html():
    rows = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (render.update_badge(k), render.esc(v)) for k, v in LEGEND)
    return """<details class="how-box">
      <summary>How to read an update</summary>
      <dl class="legend">%s</dl>
      <p class="sec-sub" style="margin:var(--s-4) 0 0;">Every update shows who said it, when it was published, when an editor verified it and when we last checked it. Anything touching safety, medical care, emergencies, religious dates, Kumbh rules, traffic, road closures, entry, government orders, accommodation availability, prices or passes is approved by a named editor before it appears. Read the <a href="/editorial-policy/">editorial policy</a> and see <a href="/sources/">where the information comes from</a>.</p>
    </details>""" % rows


def filter_group(updates):
    cats = [c for c in enums.UPDATE_CATEGORIES if any(u["category"] == c for u in updates)]
    chips = ['<button class="chip" type="button" data-filter="all" aria-pressed="true">All <span class="n">%d</span></button>' % len(updates)]
    for c in cats:
        n = sum(1 for u in updates if u["category"] == c)
        chips.append('<button class="chip" type="button" data-filter="%s" aria-pressed="false">%s <span class="n">%d</span></button>'
                     % (c.lower(), render.esc(c), n))
    cards = "\n      ".join(render.update_card(u) for u in updates)
    return """<div data-filter-group="updates">
      <div class="explorer-bar">
        <div class="chips" role="group" aria-label="Filter updates by category">%s</div>
        <p class="explorer-count"><span data-filter-count>%d</span> shown</p>
      </div>
      <div class="update-list" data-filter-items>
      %s
      </div>
      <p class="guide-empty" data-filter-empty hidden>No updates in this category right now.</p>
      <p class="sr-only" role="status" data-filter-status></p>
    </div>""" % ("".join(chips), len(updates), cards)


def updates_page():
    live = content.live_updates()
    now = store.now()
    stamp = content.latest_stamp(live, "lastCheckedAt", "verifiedAt", "publishedAt")
    if live:
        body_list = filter_group(live) if len(live) > 3 else (
            '<div class="update-list">%s</div>' % "\n".join(render.update_card(u) for u in live))
    else:
        body_list = """<div class="empty-state">
        <h3>No live updates right now</h3>
        <p>Nothing is currently published as live. That is deliberate: we only publish an update when an editor has checked its source. The <a href="/updates/archive/">archive</a> keeps earlier notices, and <a href="/sources/">our sources</a> are the places to check for anything newer.</p>
      </div>"""
    head = pagekit.page_head(
        "Verified updates for Nashik and the Kumbh Mela",
        "Short notices about Nashik and the Simhastha, each with its source, when it was published, when it was verified and when we last checked it.",
        crumbs=[("Home", "/"), ("Updates", None)], eyebrow="Updates",
        extra='<p class="ph-stamp"><span>Last checked: <strong>%s</strong></span><span>%d live %s</span></p>'
              % (render.esc(render.fmt_dt(stamp) if stamp else "not yet"), len(live), "update" if len(live) == 1 else "updates"))
    body = head + """
<section class="sec">
  <div class="inner">
    %(legend)s
    <h2 class="sec-title" style="margin-top:var(--s-8);">Live now</h2>
    <p class="sec-sub">Newest first. Time-sensitive items expire automatically and move to the archive.</p>
    %(list)s
    <div class="feed-links">
      <a href="/updates/archive/">Update archive</a>
      <a href="/kumbh-mela-2027/live-updates/">Kumbh live updates</a>
      <a href="/updates/feed.xml">Atom feed</a>
      <a href="/updates/feed.json">JSON feed</a>
    </div>
  </div>
</section>
<section class="sec sec-alt">
  <div class="inner">
    <h2 class="sec-title">Where this comes from</h2>
    <p class="sec-sub">Updates are written from official sources first &mdash; the Maharashtra Government, the Nashik district administration, the Kumbh Mela Authority, the railways, the police &mdash; and from established news only as a lead. Social media is never treated as confirmation.</p>
    <p class="link-row"><a class="btn btn-outline" href="/sources/">See every source we use</a><a class="btn btn-outline" href="/editorial-policy/">Editorial policy</a></p>
  </div>
</section>
""" % {"legend": legend_html(), "list": body_list}
    html = pagekit.render(
        "/updates/", "Updates: verified notices for Nashik and the Kumbh Mela",
        "Verified notices about Nashik and the Kumbh Mela, each showing its source, when it was published, verified and last checked. Time-sensitive items expire automatically.",
        body, crumbs=[("Home", "/"), ("Updates", "/updates/")], css=CSS, extra_head=FEED_HEAD,
        modified=(stamp or "")[:10] or None, page_type="CollectionPage",
        raw_title=True)
    # The meta tag drives engagement events in /site.js.
    html = html.replace("</head>", '  <meta name="nt-section" content="updates" />\n</head>', 1)
    pagekit.write("/updates/", html)
    return len(live)


def archive_page():
    arch = content.archived_updates()
    if arch:
        lst = '<div class="update-list">%s</div>' % "\n".join(render.update_card(u, compact=True) for u in arch)
    else:
        lst = """<div class="empty-state"><h2>Nothing archived yet</h2>
        <p>When an update expires or is withdrawn it moves here, with its source and dates intact. We keep the record rather than deleting it.</p></div>"""
    head = pagekit.page_head(
        "Update archive",
        "Notices that have expired or been superseded. Kept as a record &mdash; the status on each card says what became of it.",
        crumbs=[("Home", "/"), ("Updates", "/updates/"), ("Archive", None)], eyebrow="Updates")
    body = head + """
<section class="sec"><div class="inner">
  <p class="sec-sub">For what is current, go to <a href="/updates/">live updates</a>.</p>
  %s
</div></section>
""" % lst
    html = pagekit.render(
        "/updates/archive/", "Update archive",
        "Expired and superseded Nashik and Kumbh Mela notices, kept as a record with their sources and dates.",
        body, crumbs=[("Home", "/"), ("Updates", "/updates/"), ("Archive", "/updates/archive/")],
        css=CSS, extra_head=FEED_HEAD, page_type="CollectionPage")
    pagekit.write("/updates/archive/", html)
    return len(arch)


def _iso(value):
    d = store.parse_dt(value)
    return d.astimezone(store.IST).isoformat() if d else None


def feeds():
    live = content.live_updates()
    updated = _iso(content.latest_stamp(live, "lastCheckedAt", "verifiedAt", "publishedAt")) or _iso(store.today().isoformat())
    entries = []
    for u in live:
        link = "%s/updates/#u-%s" % (SITE, u["id"])
        mod = _iso(u.get("verifiedAt") or u["publishedAt"])
        entries.append("""  <entry>
    <id>tag:nashiktourism.com,2026:update:%(id)s</id>
    <title>%(title)s</title>
    <link rel="alternate" href="%(link)s" />
    <published>%(pub)s</published>
    <updated>%(mod)s</updated>
    <author><name>%(author)s</name></author>
    <category term="%(cat)s" />
    <summary>%(summary)s Source: %(src)s. Status: %(st)s.</summary>
  </entry>""" % {"id": xesc(u["id"]), "title": xesc(u["title"]), "link": xesc(link),
                 "pub": _iso(u["publishedAt"]), "mod": mod, "author": xesc(u.get("author") or "NashikTourism.com"),
                 "cat": xesc(u["category"]), "summary": xesc(u["summary"]), "src": xesc(u["sourceName"]),
                 "st": xesc(render.effective_status(u))})
    atom = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-IN">
  <id>tag:nashiktourism.com,2026:updates</id>
  <title>NashikTourism.com verified updates</title>
  <subtitle>Verified notices about Nashik and the Kumbh Mela, each with its source.</subtitle>
  <link rel="self" href="%(site)s/updates/feed.xml" />
  <link rel="alternate" href="%(site)s/updates/" />
  <updated>%(updated)s</updated>
%(entries)s
</feed>
""" % {"site": SITE, "updated": updated, "entries": "\n".join(entries)}
    with open(os.path.join(ROOT, "updates", "feed.xml"), "w", encoding="utf-8") as fh:
        fh.write(atom)

    jf = {"version": "https://jsonfeed.org/version/1.1", "title": "NashikTourism.com verified updates",
          "home_page_url": SITE + "/updates/", "feed_url": SITE + "/updates/feed.json", "language": "en-IN",
          "items": [{"id": "tag:nashiktourism.com,2026:update:" + u["id"], "url": "%s/updates/#u-%s" % (SITE, u["id"]),
                     "title": u["title"], "content_text": u["summary"], "date_published": _iso(u["publishedAt"]),
                     "date_modified": _iso(u.get("verifiedAt") or u["publishedAt"]), "tags": [u["category"]] + list(u.get("tags") or []),
                     "_source": {"name": u["sourceName"], "url": u.get("sourceUrl"),
                                 "verified_at": u.get("verifiedAt"), "last_checked_at": u.get("lastCheckedAt"),
                                 "status": render.effective_status(u)}}
                    for u in live]}
    with open(os.path.join(ROOT, "updates", "feed.json"), "w", encoding="utf-8") as fh:
        json.dump(jf, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def main():
    n_live = updates_page()
    n_arch = archive_page()
    feeds()
    print("updates: %d live, %d archived; wrote /updates/, /updates/archive/, feed.xml, feed.json" % (n_live, n_arch))


if __name__ == "__main__":
    main()
