#!/usr/bin/env python3
"""
Run every generator in the order they depend on each other.

    python3 tools/build-all.py            # validate data, then build everything
    NT_NOW=2027-08-02T09:00:00+05:30 python3 tools/build-all.py   # build "as of" another moment

Order matters:
  1. data is validated first — a record that breaks the verification policy
     (a 'verified' fact with no source, a high-risk update with no approver...)
     stops the build before anything is generated
  2. hubs and destination pages are generated from data
  3. apply-verification adds the status notice and verification block to guides
  4. apply-chrome rewrites the shared header and footer on EVERY page
  5. the search index and the sitemap are built last, from what now exists
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("validate-data.py", "editorial data against the verification policy"),
    ("build-destinations.py", "destination pages and the Discover / Plan hubs"),
    ("build-blog.py", "the static guide index"),
    ("build-disclaimer.py", "the disclaimer page"),
    ("build-updates.py", "/updates/, the archive and the feeds"),
    ("build-events.py", "/events/"),
    ("build-sources.py", "/sources/ — the public source registry"),
    ("build-editorial-policy.py", "/editorial-policy/"),
    ("build-transport.py", "/transport/"),
    ("build-accessible.py", "/accessible-nashik/"),
    ("build-kumbh.py", "the Kumbh hub and live updates"),
    ("build-nashik-now.py", "/nashik-now/"),
    ("build-home.py", "the homepage"),
    ("build-article-nav.py", "in-article contents and reading progress"),
    ("apply-verification.py", "status notice + verification block on every guide"),
    ("apply-chrome.py", "shared header, footer and /site.js on every page"),
    ("build-home-guides.py", "the homepage's latest-guide cards"),
    ("build-search.py", "search index and /search/"),
    ("build-sitemap.py", "sitemap.xml and robots.txt"),
]

failed = 0
for script, what in STEPS:
    print("\n\033[1m== %s\033[0m — %s" % (script, what))
    rc = subprocess.call([sys.executable, os.path.join(HERE, script)])
    if rc != 0:
        print("   FAILED (exit %d)" % rc)
        failed += 1
        if script == "validate-data.py":
            print("\nStopping: fix the data errors above first.")
            sys.exit(1)
sys.exit(1 if failed else 0)
