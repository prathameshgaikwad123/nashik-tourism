#!/usr/bin/env python3
"""
Editor workflow for NashikTourism.com — no HTML, no JSON hand-editing.

    python3 tools/cms.py update new  --title "…" --summary "…" --category Roads \
        --source-name "Maharashtra PWD" --source-url https://… --source-id pwd-maharashtra \
        --status developing --expires 2026-11-05 --tags ring-road,trimbak-road --author "A. Editor"
    python3 tools/cms.py update list [--state draft|review|published|archived]
    python3 tools/cms.py update publish <id> --approved-by "A. Editor"     # high-risk items need this
    python3 tools/cms.py update verify  <id>                               # re-checked today
    python3 tools/cms.py update expire  <id> --date 2026-11-05
    python3 tools/cms.py update archive <id>

    python3 tools/cms.py candidate list
    python3 tools/cms.py candidate approve <cand-id> --approved-by "A. Editor" --published-at 2026-10-03 --read-source
    python3 tools/cms.py candidate reject  <cand-id> --note "duplicate of …"

    python3 tools/cms.py fact verify <fact-id> --verified-by "A. Editor" --source-url https://… [--display "…"]
    python3 tools/cms.py event verify <event-id> --verified-by "A. Editor" --source-url https://…
    python3 tools/cms.py changelog add --path /transport/ --type updated --summary "…"

    python3 tools/cms.py build        # validate + rebuild the whole site

Every write is validated with tools/nt/validate.py. If the result would break the
verification policy (a high-risk item without an approver, a 'verified' fact
without a source…) the file is restored and the reasons are printed.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import enums, risk, store, validate  # noqa: E402
from nt.paths import DATA  # noqa: E402

CAND_DIR = os.path.join(DATA, "pipeline", "candidates")


def die(msg):
    print("error: " + msg)
    sys.exit(1)


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:48].strip("-")


def today():
    return store.today().isoformat()


class Txn:
    """Back up the data files, apply a change, validate, roll back on failure."""

    FILES = ["updates", "events", "facts", "changelog"]

    def __enter__(self):
        self.saved = {n: open(store.path(n), encoding="utf-8").read() for n in self.FILES}
        return self

    def commit(self):
        r = validate.validate_all()
        if r.errors:
            for n, text in self.saved.items():
                with open(store.path(n), "w", encoding="utf-8") as fh:
                    fh.write(text)
            print("Rejected — this would break the verification policy:")
            for e in r.errors:
                print("  - " + e)
            sys.exit(1)
        for w in r.warnings:
            print("  warn: " + w)

    def __exit__(self, *a):
        return False


def find(items, key, value, label):
    for it in items:
        if it[key] == value:
            return it
    die("no %s with %s %r" % (label, key, value))


# ── updates ──────────────────────────────────────────────────────────────────
def update_new(a):
    if a.category not in enums.UPDATE_CATEGORIES:
        die("category must be one of: " + ", ".join(enums.UPDATE_CATEGORIES))
    if a.status not in enums.UPDATE_STATUS:
        die("status must be one of: " + ", ".join(enums.UPDATE_STATUS))
    pub = a.published or today()
    uid = "%s-%s" % (pub, slug(a.title))
    with Txn() as t:
        data = store.load("updates")
        if any(u["id"] == uid for u in data["updates"]):
            die("an update with id %s already exists" % uid)
        rec = {"id": uid, "title": a.title, "summary": a.summary, "category": a.category, "status": a.status,
               "contentStatus": "draft", "sourceId": a.source_id, "sourceName": a.source_name,
               "sourceUrl": a.source_url, "publishedAt": pub, "verifiedAt": None, "lastCheckedAt": today(),
               "expiresAt": a.expires, "author": a.author, "tags": [x for x in (a.tags or "").split(",") if x],
               "relatedPages": [x for x in (a.related or "").split(",") if x], "origin": "manual",
               "approvedBy": None, "approvedAt": None}
        data["updates"].append(rec)
        store.dump("updates", data)
        t.commit()
    assess = risk.assess(rec)
    print("created draft %s" % uid)
    if assess["high_risk"]:
        print("  HIGH-RISK (%s): publishing needs --approved-by" % ", ".join(assess["reasons"]))


def update_list(a):
    for u in store.load("updates")["updates"]:
        if a.state and u["contentStatus"] != a.state:
            continue
        print("%-9s %-10s %-10s %s  %s" % (u["contentStatus"], u["status"], u["category"], u["id"], "HIGH-RISK" if risk.is_high_risk(u) else ""))


def update_publish(a):
    with Txn() as t:
        data = store.load("updates")
        u = find(data["updates"], "id", a.id, "update")
        u["contentStatus"] = "published" if u["contentStatus"] in ("draft", "review") else "updated"
        u["lastCheckedAt"] = today()
        if a.verified:
            u["verifiedAt"] = today()
        if a.approved_by:
            u["approvedBy"], u["approvedAt"] = a.approved_by, today()
        store.dump("updates", data)
        t.commit()
    print("published %s" % a.id)


def update_verify(a):
    with Txn() as t:
        data = store.load("updates")
        u = find(data["updates"], "id", a.id, "update")
        u["verifiedAt"] = u["lastCheckedAt"] = today()
        if u["status"] == "developing" and a.confirm:
            u["status"] = "confirmed"
        store.dump("updates", data)
        t.commit()
    print("verified %s on %s" % (a.id, today()))


def update_expire(a):
    with Txn() as t:
        data = store.load("updates")
        find(data["updates"], "id", a.id, "update")["expiresAt"] = a.date
        store.dump("updates", data)
        t.commit()
    print("%s now expires %s (archives automatically after that)" % (a.id, a.date))


def update_archive(a):
    with Txn() as t:
        data = store.load("updates")
        u = find(data["updates"], "id", a.id, "update")
        u["status"], u["contentStatus"] = "archived", "archived"
        store.dump("updates", data)
        t.commit()
    print("archived %s (kept on /updates/archive/)" % a.id)


# ── pipeline candidates ─────────────────────────────────────────────────────
def load_candidates():
    out = []
    if os.path.isdir(CAND_DIR):
        for n in sorted(os.listdir(CAND_DIR)):
            if n.endswith(".json"):
                with open(os.path.join(CAND_DIR, n), encoding="utf-8") as fh:
                    out.append(json.load(fh))
    return out


def save_candidate(c):
    with open(os.path.join(CAND_DIR, c["id"] + ".json"), "w", encoding="utf-8") as fh:
        json.dump(c, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def candidate_list(a):
    for c in load_candidates():
        r = c["review"]["state"]
        if a.all or r == "pending":
            print("%-9s conf=%.2f %-8s %s\n          %s\n          %s" % (
                r, c.get("confidence") or 0, "HIGH-RISK" if c["risk"]["high_risk"] else "low-risk",
                c["id"], c["extracted"]["title"], c["sourceUrl"]))


def candidate_approve(a):
    if not a.read_source:
        die("approving means you have opened and read the source. Re-run with --read-source once you have.")
    if not a.published_at:
        die("--published-at (the date the source was published) is required")
    c = next((x for x in load_candidates() if x["id"] == a.id), None)
    if not c:
        die("no candidate %r" % a.id)
    ex = c["extracted"]
    with Txn() as t:
        data = store.load("updates")
        uid = "%s-%s" % (a.published_at, slug(ex["title"]))
        if any(u["id"] == uid for u in data["updates"]):
            die("an update %s already exists" % uid)
        rec = {"id": uid, "title": a.title or ex["title"], "summary": a.summary or ex["summary"], "category": ex["category"],
               "status": ex.get("status", "developing"), "contentStatus": "published", "sourceId": c.get("sourceId"),
               "sourceName": c["sourceName"], "sourceUrl": c["sourceUrl"], "publishedAt": a.published_at,
               "verifiedAt": today() if c.get("sourceTier") == "official" else None, "lastCheckedAt": today(),
               "expiresAt": a.expires, "author": a.approved_by, "tags": ex.get("tags", []), "relatedPages": [],
               "origin": "pipeline", "candidateId": c["id"], "approvedBy": a.approved_by, "approvedAt": today()}
        data["updates"].append(rec)
        store.dump("updates", data)
        t.commit()
    c["review"] = {"state": "approved", "by": a.approved_by, "at": today(), "note": "published as " + uid}
    save_candidate(c)
    print("approved %s -> update %s" % (a.id, uid))


def candidate_reject(a):
    c = next((x for x in load_candidates() if x["id"] == a.id), None)
    if not c:
        die("no candidate %r" % a.id)
    c["review"] = {"state": "rejected", "by": a.by or "editor", "at": today(), "note": a.note}
    save_candidate(c)
    print("rejected %s" % a.id)


# ── facts, events, changelog ────────────────────────────────────────────────
def fact_verify(a):
    with Txn() as t:
        data = store.load("facts")
        f = find(data["facts"], "id", a.id, "fact")
        f["status"], f["verifiedAt"], f["verifiedBy"], f["lastCheckedAt"] = "verified", today(), a.verified_by, today()
        f["source"]["url"] = a.source_url
        if a.display:
            f["display"] = a.display
        if a.value:
            f["value"] = a.value
        elif f.get("value") is None and a.display:
            f["value"] = a.display
        store.dump("facts", data)
        t.commit()
    print("verified fact %s — every page that shows it updates on the next build" % a.id)


def event_verify(a):
    with Txn() as t:
        data = store.load("events")
        e = find(data["events"], "id", a.id, "event")
        e["verificationStatus"], e["lastVerified"], e["lastCheckedAt"], e["sourceUrl"] = "verified", today(), today(), a.source_url
        store.dump("events", data)
        t.commit()
    print("verified event %s (structured data is now emitted for it)" % a.id)


def changelog_add(a):
    with Txn() as t:
        data = store.load("changelog")
        data["entries"].append({"date": a.date or today(), "path": a.path, "type": a.type, "summary": a.summary})
        store.dump("changelog", data)
        t.commit()
    print("logged")


def build(_a):
    sys.exit(subprocess.call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-all.py")]))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)

    u = sp.add_parser("update").add_subparsers(dest="sub", required=True)
    n = u.add_parser("new")
    n.add_argument("--title", required=True); n.add_argument("--summary", required=True)
    n.add_argument("--category", required=True); n.add_argument("--status", default="developing")
    n.add_argument("--source-name", required=True); n.add_argument("--source-url"); n.add_argument("--source-id")
    n.add_argument("--published"); n.add_argument("--expires"); n.add_argument("--tags"); n.add_argument("--related")
    n.add_argument("--author", required=True)
    n.set_defaults(fn=update_new)
    l = u.add_parser("list"); l.add_argument("--state"); l.set_defaults(fn=update_list)
    pu = u.add_parser("publish"); pu.add_argument("id"); pu.add_argument("--approved-by"); pu.add_argument("--verified", action="store_true")
    pu.set_defaults(fn=update_publish)
    v = u.add_parser("verify"); v.add_argument("id"); v.add_argument("--confirm", action="store_true"); v.set_defaults(fn=update_verify)
    e = u.add_parser("expire"); e.add_argument("id"); e.add_argument("--date", required=True); e.set_defaults(fn=update_expire)
    ar = u.add_parser("archive"); ar.add_argument("id"); ar.set_defaults(fn=update_archive)

    c = sp.add_parser("candidate").add_subparsers(dest="sub", required=True)
    cl = c.add_parser("list"); cl.add_argument("--all", action="store_true"); cl.set_defaults(fn=candidate_list)
    ca = c.add_parser("approve"); ca.add_argument("id"); ca.add_argument("--approved-by", required=True)
    ca.add_argument("--published-at"); ca.add_argument("--read-source", action="store_true")
    ca.add_argument("--expires"); ca.add_argument("--title"); ca.add_argument("--summary"); ca.set_defaults(fn=candidate_approve)
    cr = c.add_parser("reject"); cr.add_argument("id"); cr.add_argument("--note", required=True); cr.add_argument("--by"); cr.set_defaults(fn=candidate_reject)

    f = sp.add_parser("fact").add_subparsers(dest="sub", required=True)
    fv = f.add_parser("verify"); fv.add_argument("id"); fv.add_argument("--verified-by", required=True)
    fv.add_argument("--source-url", required=True); fv.add_argument("--display"); fv.add_argument("--value"); fv.set_defaults(fn=fact_verify)

    ev = sp.add_parser("event").add_subparsers(dest="sub", required=True)
    evv = ev.add_parser("verify"); evv.add_argument("id"); evv.add_argument("--verified-by", required=True)
    evv.add_argument("--source-url", required=True); evv.set_defaults(fn=event_verify)

    ch = sp.add_parser("changelog").add_subparsers(dest="sub", required=True)
    cha = ch.add_parser("add"); cha.add_argument("--path", required=True); cha.add_argument("--summary", required=True)
    cha.add_argument("--type", default="updated"); cha.add_argument("--date"); cha.set_defaults(fn=changelog_add)

    b = sp.add_parser("build"); b.set_defaults(fn=build)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
