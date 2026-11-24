#!/usr/bin/env python3
"""
Count inbound internal links per page on the built site (what Search Console's
Links > Internal links report approximates). Standard library only.

    python3 tools/internal-links.py                      # top pages, plus the two money pages
    python3 tools/internal-links.py /discover-nashik/    # inbound count + who links, for one page
    python3 tools/internal-links.py --all                # every page

Counts every <a href> that resolves to a page on this site, from every OTHER page,
split into site-wide chrome (header/footer/nav, <header>/<footer>/<nav>) and contextual
(inside <main>/<article> body). A page is counted once per linking page for 'linking pages'
and once per anchor for 'links'.
"""
import os
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt.paths import ROOT  # noqa: E402

SITE = "https://nashiktourism.com"
MONEY = ["/blog/trimbakeshwar-to-nashik-distance-route/", "/discover-nashik/"]


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []          # (href, anchor_text, in_chrome)
        self.depth = {"header": 0, "footer": 0, "nav": 0}
        self._a = None

    def handle_starttag(self, tag, attrs):
        if tag in self.depth:
            self.depth[tag] += 1
        if tag == "a":
            href = dict(attrs).get("href")
            self._a = [href, "", any(self.depth.values())] if href else None

    def handle_endtag(self, tag):
        if tag in self.depth and self.depth[tag]:
            self.depth[tag] -= 1
        if tag == "a" and self._a:
            self.links.append((self._a[0], " ".join(self._a[1].split()), self._a[2]))
            self._a = None

    def handle_data(self, data):
        if self._a is not None:
            self._a[1] += data


def pages():
    for d, _dirs, files in os.walk(ROOT):
        if "index.html" in files:
            rel = os.path.relpath(d, ROOT)
            yield ("/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/"), os.path.join(d, "index.html")


def normalise(href, src):
    href = urldefrag(href)[0]
    if not href or href.startswith(("mailto:", "tel:", "javascript:")):
        return None
    u = urlparse(urljoin(SITE + src, href))
    if u.netloc not in ("nashiktourism.com", "www.nashiktourism.com"):
        return None
    path = u.path
    return path if path.endswith("/") else path + "/" if "." not in path.rsplit("/", 1)[-1] else path


def collect():
    known = {p for p, _f in pages()}
    inbound = defaultdict(list)   # target -> [(source, anchor, chrome)]
    for src, f in pages():
        p = P()
        p.feed(open(f, encoding="utf-8").read())
        for href, text, chrome in p.links:
            t = normalise(href, src)
            if t and t in known and t != src:
                inbound[t].append((src, text, chrome))
    return known, inbound


def summary(t, inbound):
    rows = inbound.get(t, [])
    return {"links": len(rows), "pages": len({r[0] for r in rows}),
            "chrome": sum(1 for r in rows if r[2]), "contextual": sum(1 for r in rows if not r[2])}


def main():
    known, inbound = collect()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        for t in args:
            s = summary(t, inbound)
            print("%s: %d links from %d pages (%d chrome, %d contextual)" % (t, s["links"], s["pages"], s["chrome"], s["contextual"]))
            for src, text, chrome in sorted(inbound.get(t, []), key=lambda r: (r[2], r[0])):
                print("   %-9s %-62s %s" % ("chrome" if chrome else "context", src, text[:70]))
        return 0
    ranked = sorted(known, key=lambda t: -summary(t, inbound)["links"])
    show = ranked if "--all" in sys.argv else ranked[:15] + [m for m in MONEY if m not in ranked[:15]]
    print("%-62s %6s %6s %6s %6s" % ("page", "links", "pages", "chrome", "context"))
    for t in show:
        s = summary(t, inbound)
        print("%-62s %6d %6d %6d %6d" % (t, s["links"], s["pages"], s["chrome"], s["contextual"]))
    print("\n%d pages, %d internal links in total" % (len(known), sum(len(v) for v in inbound.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
