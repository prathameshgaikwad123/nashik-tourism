"""Validation for everything in /data.

This is where the editorial rules stop being prose and become checks that fail a
build:

  * a 'verified' fact, event or accessibility record must carry a source URL, a
    verifiedAt date and a named verifier — nothing is verified by assertion
  * a 'confirmed' update must have a verification date and a source URL
  * a high-risk item cannot be live without a named human approver
  * no live record may lack a source name (no "according to sources")
  * references between files must resolve (fact ids, source ids, page paths)
  * URLs must be https and well-formed

Returns (errors, warnings). Errors fail the build; warnings go to the content
health report.
"""
import os
import re
from urllib.parse import urlparse

from . import enums, risk, store
from .paths import ROOT

ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def err(self, where, msg):
        self.errors.append("%s: %s" % (where, msg))

    def warn(self, where, msg):
        self.warnings.append("%s: %s" % (where, msg))


def _url_ok(value):
    if value in (None, ""):
        return True
    try:
        u = urlparse(value)
    except ValueError:
        return False
    return u.scheme == "https" and bool(u.netloc) and " " not in value


def _need(r, where, obj, keys):
    for k in keys:
        if obj.get(k) in (None, "", []):
            r.err(where, "missing required field '%s'" % k)


def _unique(r, label, ids):
    seen = set()
    for i in ids:
        if i in seen:
            r.err(label, "duplicate id %r" % i)
        seen.add(i)


def check_sources(r, data):
    where0 = "sources.json"
    items = data["sources"]
    _unique(r, where0, [s["id"] for s in items])
    for s in items:
        w = "%s[%s]" % (where0, s.get("id"))
        _need(r, w, s, ["id", "name", "category", "reliability", "checkFrequency"])
        if not ID_RE.match(s.get("id", "")):
            r.err(w, "id must be lower-case letters, digits, dot, dash or underscore")
        if s.get("category") not in enums.SOURCE_CATEGORIES:
            r.err(w, "unknown category %r" % s.get("category"))
        if s.get("reliability") not in enums.RELIABILITY:
            r.err(w, "unknown reliability %r" % s.get("reliability"))
        if s.get("checkFrequency") not in enums.CHECK_FREQUENCY:
            r.err(w, "unknown checkFrequency %r" % s.get("checkFrequency"))
        if s.get("urlStatus") not in enums.URL_STATUS:
            r.err(w, "unknown urlStatus %r" % s.get("urlStatus"))
        if not _url_ok(s.get("url")):
            r.err(w, "url must be https and well-formed")
        if s.get("active") and not s.get("url"):
            r.err(w, "an active source needs a url")
        if s.get("active") and s.get("monitor", {}).get("type") == "manual":
            r.warn(w, "active but monitor.type is 'manual'; it will not be polled")
    return {s["id"]: s for s in items}


def check_facts(r, data, sources):
    where0 = "facts.json"
    items = data["facts"]
    _unique(r, where0, [f["id"] for f in items])
    for f in items:
        w = "%s[%s]" % (where0, f.get("id"))
        _need(r, w, f, ["id", "subject", "fact", "status", "source"])
        if "value" not in f:
            r.err(w, "'value' must be present (use null if unknown)")
        if f.get("status") not in enums.FACT_STATUS:
            r.err(w, "unknown status %r" % f.get("status"))
        src = f.get("source") or {}
        if src.get("sourceId") and src["sourceId"] not in sources:
            r.err(w, "source.sourceId %r is not in sources.json" % src["sourceId"])
        if not _url_ok(src.get("url")):
            r.err(w, "source.url must be https")
        for sid in f.get("verifyWith", []):
            if sid not in sources:
                r.err(w, "verifyWith %r is not in sources.json" % sid)
        for lead in f.get("leads", []):
            if not _url_ok(lead):
                r.err(w, "lead %r is not a valid https URL" % lead)
        if f.get("status") == "verified":
            if not src.get("url"):
                r.err(w, "a verified fact needs source.url")
            if not f.get("verifiedAt") or not store.is_date(f.get("verifiedAt")):
                r.err(w, "a verified fact needs verifiedAt (YYYY-MM-DD)")
            if not f.get("verifiedBy"):
                r.err(w, "a verified fact needs verifiedBy (a named editor)")
            if f.get("value") is None:
                r.err(w, "a verified fact needs a value")
        if f.get("status") == "disputed" and len(f.get("alternatives", [])) < 1:
            r.err(w, "a disputed fact must list the alternatives that disagree")
        if f.get("status") == "reported" and not (src.get("url") or src.get("name")):
            r.err(w, "a reported fact must name where it was reported")
    return {f["id"]: f for f in items}


def _is_live(item):
    return item.get("contentStatus") in enums.LIVE_CONTENT_STATUS


def check_updates(r, data, sources):
    where0 = "updates.json"
    items = data["updates"]
    _unique(r, where0, [u["id"] for u in items])
    for u in items:
        w = "%s[%s]" % (where0, u.get("id"))
        _need(r, w, u, ["id", "title", "summary", "category", "status", "contentStatus",
                        "sourceName", "publishedAt", "lastCheckedAt", "author"])
        if u.get("category") not in enums.UPDATE_CATEGORIES:
            r.err(w, "unknown category %r" % u.get("category"))
        if u.get("status") not in enums.UPDATE_STATUS:
            r.err(w, "unknown status %r" % u.get("status"))
        if u.get("contentStatus") not in enums.CONTENT_STATUS:
            r.err(w, "unknown contentStatus %r" % u.get("contentStatus"))
        if u.get("sourceId") and u["sourceId"] not in sources:
            r.err(w, "sourceId %r is not in sources.json" % u["sourceId"])
        if not _url_ok(u.get("sourceUrl")):
            r.err(w, "sourceUrl must be https")
        for k in ("publishedAt", "verifiedAt", "lastCheckedAt", "expiresAt"):
            if u.get(k) and not store.is_datetime(u[k]):
                r.err(w, "%s is not a valid date/time" % k)
        pub, exp = store.parse_dt(u.get("publishedAt")), store.parse_dt(u.get("expiresAt"), end_of_day=True)
        if pub and exp and exp < pub:
            r.err(w, "expiresAt is before publishedAt")
        if _is_live(u):
            if u.get("status") == "confirmed":
                if not u.get("verifiedAt"):
                    r.err(w, "a confirmed update needs verifiedAt")
                if not u.get("sourceUrl"):
                    r.err(w, "a confirmed update needs sourceUrl")
            if not u.get("sourceUrl") and u.get("status") != "changed" and u.get("sourceId") != "editorial":
                r.warn(w, "live update has no sourceUrl; it will display as unlinked")
            assess = risk.assess(u)
            if assess["high_risk"] and not (u.get("approvedBy") and u.get("approvedAt")):
                r.err(w, "high-risk (%s) and live without approvedBy + approvedAt"
                      % ", ".join(assess["reasons"]))
    return {u["id"]: u for u in items}


def check_events(r, data, sources, facts):
    where0 = "events.json"
    items = data["events"]
    _unique(r, where0, [e["id"] for e in items])
    for e in items:
        w = "%s[%s]" % (where0, e.get("id"))
        _need(r, w, e, ["id", "title", "date", "location", "category", "description",
                        "sourceName", "status", "verificationStatus", "contentStatus"])
        if not store.is_date(e.get("date")):
            r.err(w, "date must be YYYY-MM-DD")
        if e.get("endDate") and not store.is_date(e["endDate"]):
            r.err(w, "endDate must be YYYY-MM-DD")
        for k in ("startTime", "endTime"):
            if e.get(k) and not re.match(r"^\d{2}:\d{2}$", e[k]):
                r.err(w, "%s must be HH:MM" % k)
        if e.get("category") not in enums.EVENT_CATEGORIES:
            r.err(w, "unknown category %r" % e.get("category"))
        if e.get("status") not in enums.EVENT_STATUS:
            r.err(w, "unknown status %r" % e.get("status"))
        if e.get("verificationStatus") not in ("verified", "reported"):
            r.err(w, "verificationStatus must be 'verified' or 'reported'")
        if e.get("accessibility") not in enums.ACCESS_STATUS:
            r.err(w, "unknown accessibility status %r" % e.get("accessibility"))
        for k in ("sourceUrl", "bookingUrl"):
            if not _url_ok(e.get(k)):
                r.err(w, "%s must be https" % k)
        if e.get("factRef") and e["factRef"] not in facts:
            r.err(w, "factRef %r is not in facts.json" % e["factRef"])
        if e.get("verificationStatus") == "verified":
            if not e.get("sourceUrl"):
                r.err(w, "a verified event needs sourceUrl")
            if not e.get("lastVerified"):
                r.err(w, "a verified event needs lastVerified")
    return {e["id"]: e for e in items}


def check_destinations(r, data, sources, facts):
    where0 = "destinations.json"
    items = data["destinations"]
    _unique(r, where0, [d["slug"] for d in items])
    slugs = {d["slug"] for d in items}

    def refs(w, v):
        if isinstance(v, dict):
            if "$fact" in v and v["$fact"] not in facts:
                r.err(w, "fact reference %r is not in facts.json" % v["$fact"])
            if "sourceId" in v and v["sourceId"] not in sources:
                r.err(w, "sourceId %r is not in sources.json" % v["sourceId"])
            for x in v.values():
                refs(w, x)

    for d in items:
        w = "%s[%s]" % (where0, d.get("slug"))
        _need(r, w, d, ["slug", "name", "category", "description", "location", "lede"])
        for c in d.get("category", []):
            if c not in enums.DESTINATION_CATEGORIES:
                r.err(w, "unknown category %r" % c)
        for n in d.get("nearbyPlaces", []):
            if n not in slugs:
                r.err(w, "nearbyPlaces: unknown destination %r" % n)
        for sid in d.get("sourceReferences", []):
            if sid not in sources:
                r.err(w, "sourceReferences: %r is not in sources.json" % sid)
        if d.get("verificationStatus") not in enums.VERIFICATION_STATUS:
            r.err(w, "unknown verificationStatus %r" % d.get("verificationStatus"))
        if d.get("verificationStatus") == "verified" and not d.get("lastVerified"):
            r.err(w, "verified destination needs lastVerified")
        for k in ("timings", "entryFee", "officialWebsite", "officialContact", "recommendedDuration",
                  "parking", "transport", "bestTimeToVisit"):
            if k not in d:
                r.err(w, "field '%s' must be present (null if unknown)" % k)
            refs(w + "." + k, d.get(k))
    return {d["slug"]: d for d in items}


def check_accessibility(r, data, dests, facts):
    where0 = "accessibility.json"
    ids = {s["id"] for s in data["statuses"]}
    if ids != set(enums.ACCESS_STATUS):
        r.err(where0, "statuses must be exactly %s" % ", ".join(enums.ACCESS_STATUS))
    for p in data["places"]:
        w = "%s[%s]" % (where0, p.get("slug"))
        if p.get("slug") not in dests:
            r.err(w, "unknown destination")
        if p.get("status") not in enums.ACCESS_STATUS:
            r.err(w, "unknown status %r" % p.get("status"))
        if p.get("status") == "verified_accessible":
            if not (p.get("source") and p.get("verifiedAt") and p.get("verifiedBy")):
                r.err(w, "verified_accessible needs source, verifiedAt and verifiedBy — "
                         "never claim a place is accessible without verification")
        if p.get("factRef") and p["factRef"] not in facts:
            r.err(w, "factRef %r is not in facts.json" % p["factRef"])
    for t in data["topics"]:
        for fid in t.get("factRefs", []):
            if fid not in facts:
                r.err("%s[%s]" % (where0, t["id"]), "factRef %r is not in facts.json" % fid)


def check_transport(r, data, sources, facts):
    where0 = "transport.json"
    _unique(r, where0, [s["id"] for s in data["sections"]])
    for s in data["sections"]:
        w = "%s[%s]" % (where0, s["id"])
        for fid in s.get("facts", []):
            if fid not in facts:
                r.err(w, "fact %r is not in facts.json" % fid)
        for sid in s.get("sources", []):
            if sid not in sources:
                r.err(w, "source %r is not in sources.json" % sid)
        for c in s.get("liveCategories", []):
            if c not in enums.UPDATE_CATEGORIES:
                r.err(w, "liveCategory %r is not an update category" % c)


def check_changelog(r, data):
    for i, e in enumerate(data["entries"]):
        w = "changelog.json[%d]" % i
        _need(r, w, e, ["date", "path", "summary", "type"])
        if not store.is_date(e.get("date")):
            r.err(w, "date must be YYYY-MM-DD")
        p = e.get("path", "")
        rel = p.strip("/")
        f = os.path.join(ROOT, rel, "index.html") if rel else os.path.join(ROOT, "index.html")
        if not os.path.isfile(f):
            r.warn(w, "path %s does not exist yet" % p)


def check_candidates(r):
    d = os.path.join(store.DATA if hasattr(store, "DATA") else "", "pipeline", "candidates")
    from .paths import DATA
    d = os.path.join(DATA, "pipeline", "candidates")
    if not os.path.isdir(d):
        return
    import json
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        w = "pipeline/candidates/" + name
        with open(os.path.join(d, name), encoding="utf-8") as fh:
            c = json.load(fh)
        _need(r, w, c, ["id", "sourceName", "extracted", "review"])
        if c.get("review", {}).get("state") not in ("pending", "approved", "rejected", "superseded"):
            r.err(w, "review.state must be pending/approved/rejected/superseded")
        if not _url_ok(c.get("sourceUrl")):
            r.err(w, "sourceUrl must be https")


def validate_all():
    r = Report()
    sources = check_sources(r, store.load("sources"))
    facts = check_facts(r, store.load("facts"), sources)
    check_updates(r, store.load("updates"), sources)
    check_events(r, store.load("events"), sources, facts)
    dests = check_destinations(r, store.load("destinations"), sources, facts)
    check_accessibility(r, store.load("accessibility"), dests, facts)
    check_transport(r, store.load("transport"), sources, facts)
    check_changelog(r, store.load("changelog"))
    check_candidates(r)
    return r
