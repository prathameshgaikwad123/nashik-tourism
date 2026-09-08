#!/usr/bin/env python3
"""
Regenerate sitemap.xml by walking the site directory, so a new page can never
be left out again (nine live URLs were missing before Phase 1).

lastmod policy — only dates we can actually stand behind:
  * pages rewritten in Phase 1  -> PHASE1_DATE
  * blog posts                  -> their published date from posts.json
  * anything else               -> the date carried in the previous sitemap,
                                   or no lastmod at all rather than a guess.
Pages carrying <meta name="robots" content="noindex"> are skipped.

Usage:  python3 tools/build-sitemap.py
"""
import json
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "nashiktourism"))
SITE = "https://nashiktourism.com"
PHASE1_DATE = "2026-09-08"

PHASE1_PAGES = {
    "/", "/discover-nashik/", "/plan-your-trip/",
    "/discover-nashik/trimbakeshwar/", "/discover-nashik/panchavati/",
    "/discover-nashik/sula-vineyards/", "/discover-nashik/pandavleni-caves/",
    "/discover-nashik/igatpuri/",
}

# Carried forward from the previous sitemap — not invented here.
PRIOR = {"/contact/": "2026-04-17"}

# Rough ordering hint for humans reading the file; crawlers ignore priority.
ORDER = ["/", "/kumbh-mela-2027/", "/discover-nashik/", "/plan-your-trip/", "/blog/",
         "/about/", "/contact/"]


def url_for(path):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    return "/" + rel[:-len("index.html")]


def main():
    posts = {p["slug"]: p.get("date") for p in
             json.load(open(os.path.join(ROOT, "posts.json"), encoding="utf-8"))}

    entries = []
    for dirpath, _dirnames, filenames in os.walk(ROOT):
        if "index.html" not in filenames:
            continue
        full = os.path.join(dirpath, "index.html")
        html = open(full, encoding="utf-8").read()
        if re.search(r'<meta name="robots" content="[^"]*noindex', html):
            continue
        loc = url_for(full)

        lastmod = None
        if loc in PHASE1_PAGES:
            lastmod = PHASE1_DATE
        elif loc.startswith("/blog/") and loc != "/blog/":
            lastmod = posts.get(loc.strip("/").split("/")[-1])
        else:
            lastmod = PRIOR.get(loc)
        entries.append((loc, lastmod))

    def sort_key(entry):
        loc = entry[0]
        return (ORDER.index(loc) if loc in ORDER else len(ORDER), loc)

    entries.sort(key=sort_key)

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in entries:
        out.append("  <url>")
        out.append("    <loc>%s%s</loc>" % (SITE, loc))
        if lastmod:
            out.append("    <lastmod>%s</lastmod>" % lastmod)
        out.append("  </url>")
    out.append("</urlset>")
    out.append("")

    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))

    with_date = sum(1 for _, d in entries if d)
    print("sitemap.xml: %d URLs (%d with lastmod, %d without)"
          % (len(entries), with_date, len(entries) - with_date))
    for loc, d in entries:
        print("  %-62s %s" % (loc, d or "-"))


if __name__ == "__main__":
    main()
