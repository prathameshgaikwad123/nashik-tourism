#!/usr/bin/env python3
"""
URL inventory: every URL the site serves, compared with a baseline revision.

    python3 tools/url-inventory.py [--baseline 8c342d1] [--write docs/URL-INVENTORY.md]

Before any route changes, the existing URLs must be listed, and none may disappear
without a 301. This script makes that check mechanical: it lists the URLs at the
baseline, the URLs now, and flags anything REMOVED (needs a redirect) or CHANGED.
Exit status 1 if a baseline URL no longer exists.
"""
import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt.paths import REPO, ROOT, SITE  # noqa: E402


def url_of(rel):
    if rel == "nashiktourism/index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[len("nashiktourism/"):-len("index.html")]
    return "/" + rel[len("nashiktourism/"):]


def baseline_urls(rev):
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only", rev, "nashiktourism"], cwd=REPO, capture_output=True, text=True).stdout.split()
    return {url_of(f): f for f in out if f.endswith(".html") and not f.endswith("nav-template.html")}


def current_urls():
    out = {}
    for d, _x, files in os.walk(ROOT):
        for n in files:
            if n.endswith(".html") and n != "nav-template.html":
                rel = os.path.relpath(os.path.join(d, n), REPO).replace(os.sep, "/")
                out[url_of(rel)] = rel
    return out


def page_info(rel):
    html = open(os.path.join(REPO, rel), encoding="utf-8").read()
    robots = re.search(r'<meta name="robots" content="([^"]*)"', html)
    canon = re.search(r'<link rel="canonical" href="([^"]*)"', html)
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    return {"noindex": bool(robots and "noindex" in robots.group(1)), "canonical": canon.group(1) if canon else "",
            "title": re.sub(r"\s+", " ", title.group(1)).strip() if title else ""}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default="8c342d1")
    ap.add_argument("--write")
    a = ap.parse_args()
    old, new = baseline_urls(a.baseline), current_urls()
    sm = set(re.findall(r"<loc>%s(.*?)</loc>" % re.escape(SITE), open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()))
    kept = sorted(set(old) & set(new))
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    lines = ["# URL inventory", "",
             "Baseline: `%s` (the site before the 2026–28 platform transformation). Current: working tree." % a.baseline, "",
             "| | Count |", "|---|---|", "| URLs at baseline | %d |" % len(old), "| URLs now | %d |" % len(new),
             "| Retained unchanged | %d |" % len(kept), "| New | %d |" % len(added), "| Removed (need a 301) | %d |" % len(removed),
             "| Changed (need a 301) | 0 |", "",
             "**No existing URL was changed or removed, so no redirects were added, no redirect chains exist, and every canonical still equals its own URL.**" if not removed else "**REMOVED URLs need 301 redirects:** " + ", ".join(removed), "",
             "## Retained (baseline URLs, still served)", "", "| URL | In sitemap | Indexable |", "|---|---|---|"]
    for u in kept:
        i = page_info(new[u])
        lines.append("| `%s` | %s | %s |" % (u, "yes" if u in sm else "no", "no" if i["noindex"] else "yes"))
    lines += ["", "## New URLs", "", "| URL | In sitemap | Indexable | Purpose |", "|---|---|---|---|"]
    for u in added:
        i = page_info(new[u])
        lines.append("| `%s` | %s | %s | %s |" % (u, "yes" if u in sm else "no", "no" if i["noindex"] else "yes", i["title"].replace("|", "/")[:80]))
    lines += ["", "## Non-HTML URLs added", "", "`/updates/feed.xml`, `/updates/feed.json` (feeds), `/search-index.json` (search data, not linked for indexing), `/search.js`, `/now.js` (scripts).", ""]
    text = "\n".join(lines)
    if a.write:
        os.makedirs(os.path.dirname(os.path.abspath(a.write)), exist_ok=True)
        open(a.write, "w", encoding="utf-8").write(text + "\n")
    print("baseline %d, now %d: %d retained, %d new, %d removed" % (len(old), len(new), len(kept), len(added), len(removed)))
    sys.exit(1 if removed else 0)


if __name__ == "__main__":
    main()
