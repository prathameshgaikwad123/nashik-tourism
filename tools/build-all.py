#!/usr/bin/env python3
"""
Run every generator in the order they depend on each other.

    python3 tools/build-all.py

Order matters: pages must exist before apply-chrome rewrites their chrome,
and before build-sitemap walks them.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("build-destinations.py", "destination pages and the Discover / Plan hubs"),
    ("build-blog.py", "the static guide index"),
    ("apply-chrome.py", "shared header, footer and /site.js on every page"),
    ("build-home-guides.py", "the homepage's latest-guide cards"),
    ("build-sitemap.py", "sitemap.xml"),
]

failed = 0
for script, what in STEPS:
    print("\n\033[1m== %s\033[0m — %s" % (script, what))
    rc = subprocess.call([sys.executable, os.path.join(HERE, script)])
    if rc != 0:
        print("   FAILED (exit %d)" % rc)
        failed += 1
sys.exit(1 if failed else 0)
