#!/usr/bin/env python3
"""
Check that every rule in nashiktourism/_redirects is a 301 that lands on a real page (200),
never chains, and never shadows a page that exists. Exit 1 on any problem.

    python3 tools/check-redirects.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt.paths import ROOT  # noqa: E402


def exists(path):
    if path.endswith("/"):
        return os.path.isfile(os.path.join(ROOT, path.strip("/"), "index.html")) if path != "/" else os.path.isfile(os.path.join(ROOT, "index.html"))
    return os.path.isfile(os.path.join(ROOT, path.lstrip("/")))


def main():
    rules = []
    for line in open(os.path.join(ROOT, "_redirects"), encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        src, dst, code = line.split()
        rules.append((src, dst, code))
    srcs = {s for s, _d, _c in rules}
    bad = []
    # Old flat URLs from an earlier site structure (Search Console 404 report) must stay redirected.
    for old in ("/sita-guha", "/buddha-vihar", "/radha-nikunj", "/gayatri-mata-mandir"):
        for variant in (old, old + "/"):
            if variant not in srcs:
                bad.append("%s must 301 (old URL still crawled by Googlebot) but has no redirect" % variant)
    for src, dst, code in rules:
        if code != "301":
            bad.append("%s: status %s, expected 301" % (src, code))
        if not exists(dst.split("#")[0]):
            bad.append("%s -> %s: target is not a real page (would 404)" % (src, dst))
        if dst in srcs:
            bad.append("%s -> %s: chain (target is itself redirected)" % (src, dst))
        if exists(src):
            bad.append("%s: source is a real page; the redirect would shadow it" % src)
    print("%d redirect rules checked" % len(rules))
    for b in bad:
        print("  ERROR " + b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
