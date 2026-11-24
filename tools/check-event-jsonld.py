#!/usr/bin/env python3
"""
Check the Event structured data in the BUILT HTML (what Googlebot receives, no JavaScript needed).

  * every <script type="application/ld+json"> block on every page parses as JSON
  * every Event has Google's required fields (name, startDate, location with a nested address)
    plus the two this site also requires (eventStatus, eventAttendanceMode)
  * reports the recommended fields that are absent (endDate, organizer, offers, performer, ...)
    so an editor can supply them if a verified source exists. Missing recommended fields never fail the run.

    python3 tools/check-event-jsonld.py            # exit 1 on any missing required field
    python3 tools/check-event-jsonld.py --page /events/

This is a structural check against Google's documented Event requirements, not a replacement for
Google's Rich Results Test (https://search.google.com/test/rich-results), which needs a browser.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt.paths import ROOT  # noqa: E402

LD = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
REQUIRED = ["name", "startDate", "location", "eventStatus", "eventAttendanceMode"]
RECOMMENDED = ["endDate", "description", "image", "offers", "organizer", "performer", "url"]
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2})?([+-]\d{2}:\d{2}|Z)?)?$")


def nodes(block):
    return block.get("@graph") if isinstance(block, dict) and "@graph" in block else [block]


def main():
    only = sys.argv[sys.argv.index("--page") + 1] if "--page" in sys.argv else None
    errors, blocks, events = [], 0, 0
    for d, _dirs, files in os.walk(ROOT):
        if "index.html" not in files and "404.html" not in files:
            continue
        rel = os.path.relpath(d, ROOT)
        path = "/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/"
        if only and path != only:
            continue
        for fn in ("index.html", "404.html"):
            f = os.path.join(d, fn)
            if not os.path.isfile(f):
                continue
            for raw in LD.findall(open(f, encoding="utf-8").read()):
                blocks += 1
                try:
                    data = json.loads(raw)
                except ValueError as e:
                    errors.append("%s: JSON-LD does not parse: %s" % (path, e))
                    continue
                for n in nodes(data):
                    if not isinstance(n, dict) or n.get("@type") != "Event":
                        continue
                    events += 1
                    label = "%s Event %r" % (path, n.get("name"))
                    miss = [k for k in REQUIRED if not n.get(k)]
                    loc = n.get("location") or {}
                    if loc and not (isinstance(loc, dict) and loc.get("name") and isinstance(loc.get("address"), dict)
                                    and loc["address"].get("addressLocality")):
                        miss.append("location.name/address.addressLocality")
                    if n.get("startDate") and not ISO.match(str(n["startDate"])):
                        miss.append("startDate (not ISO 8601)")
                    absent = [k for k in RECOMMENDED if not n.get(k)]
                    print("%-4s %s: %s" % ("FAIL" if miss else "ok", label, ("missing required: " + ", ".join(miss)) if miss else "all required fields present"))
                    if absent:
                        print("       recommended fields absent: %s" % ", ".join(absent))
                    if n.get("url") and not str(n["url"]).startswith("https://nashiktourism.com"):
                        print("       note: url points off-site (%s); Google expects the page that describes the event" % n["url"])
                    if miss:
                        errors.append(label)
    print("\n%d JSON-LD block(s) parsed, %d Event item(s), %d problem(s)" % (blocks, events, len(errors)))
    for e in errors:
        print("  " + e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
