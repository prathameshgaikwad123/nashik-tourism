#!/usr/bin/env python3
"""
One place for booking / affiliate outbound links, on EVERY page (generated or hand-written):

  * rel="noopener sponsored nofollow" (and target="_blank" gets noopener)
  * affiliate parameters from the environment, per partner (data/monetization.json lists the
    partner hosts and the env var to read, e.g. NT_AFFILIATE_MAKEMYTRIP='affid=123')
  * with no env var set the link stays a plain URL

Idempotent: the unmodified URL is remembered in data-aff-base, so changing or removing the
parameters later rewrites the link instead of stacking them.

    python3 tools/apply-affiliate.py [--check]
"""
import os
import re
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import aeo  # noqa: E402
from nt.paths import ROOT  # noqa: E402

PARTNER_HOSTS = {h: p for p in aeo.money()["affiliates"]["partners"].values() for h in p["hosts"]}
OTHER = re.compile(r"(oyo(rooms)?|redbus|yatra|cleartrip|abhibus|tripadvisor)\.", re.I)
A_TAG = re.compile(r"<a\s[^>]*>", re.S)


def partner_for(href):
    host = (urlparse(href).hostname or "").replace("www.", "")
    for h, p in PARTNER_HOSTS.items():
        if host == h or host.endswith("." + h):
            return p
    return None


def fix(m):
    tag = m.group(0)
    hm = re.search(r'\bhref="([^"]*)"', tag)
    if not hm:
        return tag
    href = hm.group(1)
    base = re.search(r'\bdata-aff-base="([^"]*)"', tag)
    base_url = base.group(1) if base else href
    partner = partner_for(base_url)
    if not partner and not OTHER.search(base_url):
        return tag
    new_href, new = base_url, tag
    params = os.environ.get(partner["env"], "").strip().lstrip("?&") if partner else ""
    if params:
        new_href = base_url + ("&" if "?" in base_url else "?") + params
    new = re.sub(r'\bhref="[^"]*"', lambda _m: 'href="%s"' % new_href, new, count=1)
    new = re.sub(r'\s+data-aff-base="[^"]*"', "", new)
    rel = re.search(r'\brel="([^"]*)"', new)
    rels = set(rel.group(1).split()) if rel else set()
    want = rels | {"noopener", "sponsored", "nofollow"}
    val = " ".join(sorted(want))
    new = re.sub(r'\brel="[^"]*"', 'rel="%s"' % val, new, count=1) if rel else new.replace("<a ", '<a rel="%s" ' % val, 1)
    if params:   # added last, always first in the tag, so repeated runs produce identical output
        new = new.replace("<a ", '<a data-aff-base="%s" ' % base_url, 1)
    return new


def main():
    check = "--check" in sys.argv
    changed = links = 0
    for dp, _d, files in os.walk(ROOT):
        for n in files:
            if not n.endswith(".html") or n == "nav-template.html":
                continue
            full = os.path.join(dp, n)
            before = open(full, encoding="utf-8").read()
            after = A_TAG.sub(fix, before)
            links += sum(1 for _ in A_TAG.finditer(before) if False)
            if after != before:
                changed += 1
                if not check:
                    open(full, "w", encoding="utf-8").write(after)
    print("%s %d page(s)" % ("would update" if check else "updated", changed))


if __name__ == "__main__":
    main()
