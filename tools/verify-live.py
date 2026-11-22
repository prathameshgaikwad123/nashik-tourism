#!/usr/bin/env python3
"""
Post-deploy check of the live site (run from GitHub Actions or anywhere with internet access):

  * every URL in sitemap.xml returns 200
  * every row of data/redirects.json returns a 301 whose Location resolves to a 200
  * /robots.txt, /llms.txt, /llms-full.txt, /sitemap.xml and the IndexNow key file are live and sane
  * the live robots.txt allows the AI and search crawlers and has no Cloudflare managed block
  * no personal name appears in live pages, and the old author URL is gone

    python3 tools/verify-live.py [--base https://nashiktourism.com]
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt.paths import DATA, REPO  # noqa: E402

UA = {"User-Agent": "nashiktourism-verify/1.0 (post-deploy check)"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with OPENER.open(req, timeout=30) as r:
            return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8", "replace") if e.fp else ""
    except (urllib.error.URLError, OSError) as e:
        return 0, {}, str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="https://nashiktourism.com")
    base = ap.parse_args().base.rstrip("/")
    fails = []
    www = "https://www." + base.split("//", 1)[1]

    def check(ok, what, detail=""):
        print("%s  %s %s" % ("PASS" if ok else "FAIL", what, detail))
        if not ok:
            fails.append(what)

    st, _h, sm = get(base + "/sitemap.xml")
    check(st == 200, "/sitemap.xml", "HTTP %d" % st)
    urls = re.findall(r"<loc>(.*?)</loc>", sm)
    check(len(urls) > 40, "sitemap lists %d URLs" % len(urls))
    pages = {}
    for u in urls:
        st, _h, body = get(u)
        pages[u] = body
        check(st == 200, u, "HTTP %d" % st)

    print("\n-- redirects --")
    rows = json.load(open(os.path.join(DATA, "redirects.json"), encoding="utf-8"))["redirects"]
    for r in rows:
        st, h, _b = get(base + r["from"])
        loc = urljoin(base + r["from"], h.get("Location") or h.get("location") or "")
        st2, _h2, _b2 = get(loc) if loc else (0, {}, "")
        check(st == 301 and loc.rstrip("/") == (base + r["to"]).rstrip("/") and st2 == 200,
              "%s -> %s" % (r["from"], r["to"]), "[%d -> %s -> %d]" % (st, loc.replace(base, ""), st2))

    print("\n-- crawler files --")
    st, _h, robots = get(base + "/robots.txt")
    check(st == 200, "/robots.txt", "HTTP %d" % st)
    check("Content-Signal" not in robots and "BEGIN Cloudflare Managed" not in robots, "robots.txt has no Cloudflare managed block")
    rp = RobotFileParser()
    rp.parse(robots.splitlines())
    for ua in ["OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User", "Claude-SearchBot", "Claude-User", "GPTBot",
               "ClaudeBot", "Google-Extended", "Bingbot", "Googlebot", "Applebot-Extended", "CCBot", "Amazonbot", "meta-externalagent"]:
        check(rp.can_fetch(ua, base + "/blog/trimbakeshwar-to-nashik-distance-route/"), "robots allows %s" % ua)
    check("Sitemap: %s/sitemap.xml" % base in robots, "robots.txt names the sitemap")
    for path in ("/llms.txt", "/llms-full.txt"):
        st, _h, body = get(base + path)
        check(st == 200 and len(body) > 2000, path, "HTTP %d, %d bytes" % (st, len(body)))
    key = open(os.path.join(REPO, "data", "indexnow-key.txt"), encoding="utf-8").read().strip()
    st, _h, body = get("%s/%s.txt" % (base, key))
    check(st == 200 and body.strip() == key, "IndexNow key file /%s.txt" % key[:6] + "...", "HTTP %d" % st)

    print("\n-- content --")
    bad = [u for u, b in pages.items() if re.search(r"(?i)" + "|".join(["prath" + "amesh", "gaik" + "wad"]), b)]
    check(not bad, "no personal name in any live page", ", ".join(bad))
    st, _h, _b = get(base + "/about/" + "prath" + "amesh" + "/")
    check(st in (404, 410), "old author URL is gone", "HTTP %d" % st)
    st, _h, b = get(base + "/about/editorial-team/")
    check(st == 200, "/about/editorial-team/", "HTTP %d" % st)
    print("\n-- deliberate 404s (no page covers them) --")
    for gone in ("/buddha-vihar", "/radha-nikunj", "/gayatri-mata-mandir"):
        st, _h, _b = get(base + gone)
        check(st == 404, gone, "HTTP %d" % st)
        st, h, _b = get(www + gone)
        loc = urljoin(www + gone, h.get("Location") or "")
        st2 = get(loc)[0] if loc else 0
        print("INFO  www%s -> HTTP %d %s then %d (a 404 here is expected)" % (gone, st, loc, st2))

    print("\n-- www host: every path 301s to the same path on the apex, query kept --")
    www_paths = ["/", "/blog/trimbakeshwar-to-nashik-distance-route/", "/discover-nashik/bhandardara/", "/robots.txt", "/sitemap.xml",
                 "/sita-guha", "/blog/best-places-to-visit-in-nashik/", "/blog/trimbakeshwar-distance-route/", "/blog/ramkund-ghat-nashik-guide",
                 "/blog/nashik-2-day-itinerary.html", "/this-path-does-not-exist/", "/discover-nashik/?a=1&b=2"]
    for p in www_paths:
        st, h, _b = get(www + p)
        loc = h.get("Location") or h.get("location") or ""
        check(st == 301 and loc == base + p, "www%s" % p, "[%d -> %s]" % (st, loc or "no Location"))

    print("\n%d failure(s)" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
