#!/usr/bin/env python3
"""
Tell participating search engines (Bing, Yandex and others via IndexNow) which URLs changed.

    python3 tools/indexnow.py                       # dry run: list the URLs that would be sent
    INDEXNOW_KEY=<key> python3 tools/indexnow.py --submit [--since HEAD~1]
    python3 tools/indexnow.py --submit --urls /updates/ /events/

Setup: the key lives in data/indexnow-key.txt and tools/build-seo-files.py writes
nashiktourism/<key>.txt from it on every build, so nothing else is needed. INDEXNOW_KEY
overrides it. Run after the deploy has finished (.github/workflows/indexnow.yml does).

Google does not use IndexNow, and its sitemap 'ping' endpoint was retired in
2023. For Google, submit /sitemap.xml once in Search Console and keep <lastmod>
honest (tools/build-sitemap.py derives it from real change records), which is
what Google reads. A Search Console API submission needs a service account and
an OAuth library; it is left as a deliberate, documented extension rather than
a half-working stub.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt.paths import REPO, ROOT, SITE  # noqa: E402

ENDPOINT = "https://api.indexnow.org/indexnow"


def default_key():
    """The IndexNow key is public by design (it is served at /<key>.txt), so it lives in the repo."""
    try:
        return open(os.path.join(REPO, "data", "indexnow-key.txt"), encoding="utf-8").read().strip()
    except OSError:
        return None


def changed_urls(since):
    out = subprocess.run(["git", "diff", "--name-only", since, "HEAD", "--", "nashiktourism"], cwd=REPO,
                         capture_output=True, text=True).stdout.split()
    urls = []
    for f in out:
        if not os.path.isfile(os.path.join(REPO, f)):
            continue   # deleted or renamed pages are redirected now; never submit them as changed
        rel = f[len("nashiktourism/"):]
        if rel == "index.html":
            urls.append("/")
        elif rel.endswith("/index.html"):
            urls.append("/" + rel[:-len("index.html")])
    return sorted(set(urls))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="HEAD~1")
    ap.add_argument("--urls", nargs="*")
    ap.add_argument("--submit", action="store_true")
    a = ap.parse_args()
    paths = a.urls if a.urls else changed_urls(a.since)
    urls = [SITE + p for p in paths if not p.startswith("/search/")]
    print("%d URL(s):" % len(urls))
    for u in urls:
        print("  " + u)
    if not a.submit:
        print("dry run — add --submit (and set INDEXNOW_KEY) to send")
        return 0
    key = os.environ.get("INDEXNOW_KEY") or default_key()
    if not key:
        print("No IndexNow key (set INDEXNOW_KEY or add data/indexnow-key.txt); nothing sent")
        return 0
    if not os.path.isfile(os.path.join(ROOT, key + ".txt")):
        print("warning: %s.txt is missing from the web root; the engines will reject the key" % key)
    if not urls:
        return 0
    body = json.dumps({"host": "nashiktourism.com", "key": key, "keyLocation": "%s/%s.txt" % (SITE, key), "urlList": urls[:10000]}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print("IndexNow accepted the submission (HTTP %d)" % r.status)
    except urllib.error.HTTPError as e:
        print("IndexNow replied HTTP %d" % e.code)
    except (urllib.error.URLError, OSError) as e:
        print("IndexNow unreachable: %s" % getattr(e, "reason", e))
    return 0


if __name__ == "__main__":
    sys.exit(main())
