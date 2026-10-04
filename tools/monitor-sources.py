#!/usr/bin/env python3
"""
Source monitor: watch the registry, detect change, propose candidates. Never publishes.

    Official sources            data/sources.json (active, monitorable)
          |
    Monitoring                  polite fetch, robots.txt honoured, bounded
          |
    Change detection            normalised page text; digits-only churn ignored
          |
    AI extraction/classification  tools/nt/classify.py (optional; safe without a key)
          |
    Confidence check            every summary must be supported by verbatim quotes
          |
    Human approval              data/pipeline/candidates/*.json  ->  tools/cms.py candidate approve
          |
    Publish -> sitemap -> discovery   tools/build-all.py, tools/indexnow.py

    python3 tools/monitor-sources.py                    # sources that are due
    python3 tools/monitor-sources.py --all              # ignore the schedule
    python3 tools/monitor-sources.py --source ntka      # one source
    python3 tools/monitor-sources.py --fixtures DIR     # read <id>.html from DIR (tests, offline)
    python3 tools/monitor-sources.py --expire           # supersede stale pending candidates
    python3 tools/monitor-sources.py --summary-file out.md

State (hashes, last status, failure counts) lives in data/state/, which is not
committed; CI persists it with a cache. The first run for a source only records a
baseline — a candidate needs a *change*, so a fresh checkout does not flood the
queue. A source that fails three runs in a row is marked broken in the state and
shows up in the content-health report.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import classify, enums, net, risk, store  # noqa: E402
from nt.paths import DATA  # noqa: E402

STATE_DIR = os.path.join(DATA, "state")
STATE_FILE = os.path.join(STATE_DIR, "source-state.json")
SNAP_DIR = os.path.join(STATE_DIR, "snapshots")
CAND_DIR = os.path.join(DATA, "pipeline", "candidates")
EVERY = {"hourly": dt.timedelta(minutes=55), "daily": dt.timedelta(hours=23), "weekly": dt.timedelta(days=6, hours=23),
         "monthly": dt.timedelta(days=29)}
MAX_ADDED_LINES = 60


def load_state():
    if os.path.isfile(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, sort_keys=True)
        fh.write("\n")


def is_due(src, st, now):
    freq = src.get("checkFrequency", "daily")
    if freq not in EVERY:
        return False
    last = st.get("lastCheckedAt")
    return not last or now - store.parse_dt(last) >= EVERY[freq]


def norm_line(line):
    """Digits-only churn (counters, clocks, dates) must not look like news."""
    return re.sub(r"\d+", "#", re.sub(r"\s+", " ", line).strip().lower())


def added_lines(old_text, new_text):
    old = {norm_line(l) for l in old_text.splitlines()}
    out, seen = [], set()
    for line in new_text.splitlines():
        n = norm_line(line)
        if n and n not in old and n not in seen and len(line.strip()) > 20:
            seen.add(n)
            out.append(line.strip())
    return out


def read_snapshot(sid):
    p = os.path.join(SNAP_DIR, sid + ".txt")
    return open(p, encoding="utf-8").read() if os.path.isfile(p) else None


def write_snapshot(sid, text):
    os.makedirs(SNAP_DIR, exist_ok=True)
    with open(os.path.join(SNAP_DIR, sid + ".txt"), "w", encoding="utf-8") as fh:
        fh.write(text[:200_000])


def existing_candidate_ids():
    if not os.path.isdir(CAND_DIR):
        return set()
    return {n[:-5] for n in os.listdir(CAND_DIR) if n.endswith(".json")}


def make_candidate(src, tier, url, added, now, h):
    added_text = "\n".join(added[:MAX_ADDED_LINES])
    cls = classify.classify(src, tier, added_text)
    if cls.get("relevant") is False:
        return None
    ex = {"title": cls["title"], "summary": cls["summary"], "category": cls["category"], "status": cls.get("status", "developing"),
          "tags": cls.get("tags", []), "publishedAt": None}
    notes = ["Machine-extracted from the text that changed on the source page. An editor must open the source, check every detail, and set the publication date before approving."]
    if src.get("monitor", {}).get("leadOnly"):
        notes.append("This is a news source: treat it as a lead, and confirm against an official source before approving.")
    if cls.get("note"):
        notes.append(cls["note"])
    cand = {
        "id": "cand-%s-%s-%s" % (now.date().isoformat(), src["id"], h[:8]),
        "createdAt": now.isoformat(), "origin": "monitor", "sourceId": src["id"], "sourceName": src["name"],
        "sourceTier": tier, "sourceUrl": url, "extracted": ex, "confidence": cls.get("confidence", 0.2),
        "risk": risk.assess({"title": ex["title"], "summary": ex["summary"], "category": ex["category"], "tags": ex["tags"]}),
        "excerpt": added_text[:1200], "quotes": cls.get("quotes", []),
        "extractionNote": " ".join(notes),
        "review": {"state": "pending", "by": None, "at": None, "note": None},
    }
    cfg = store.load("site-config")
    cand["fastTrackEligible"] = risk.may_auto_publish({**ex, "confidence": cand["confidence"]}, cfg, tier)
    return cand


def check_source(src, st, now, fixtures=None, dry=False):
    """-> (state, candidate or None, message)"""
    sid = src["id"]
    url = src["url"]
    if fixtures:
        fp = os.path.join(fixtures, sid + ".html")
        if not os.path.isfile(fp):
            return st, None, "no fixture"
        status, body, err = 200, open(fp, encoding="utf-8").read(), None
    else:
        status, body, err = net.fetch(url)

    st["lastCheckedAt"] = now.isoformat()
    st["lastStatus"] = status
    if err or not body.strip() or (status and status >= 400):
        st["failures"] = st.get("failures", 0) + 1
        st["lastError"] = err or "empty response"
        st["urlStatus"] = "broken" if st["failures"] >= 3 else st.get("urlStatus", "unchecked")
        return st, None, "FAILED (%s), %d in a row" % (st["lastError"], st["failures"])
    st["failures"], st["lastError"], st["urlStatus"] = 0, None, "ok"

    text = net.visible_text(body)
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    old_text, old_hash = read_snapshot(sid), st.get("hash")
    if not dry:
        write_snapshot(sid, text)
    st["hash"] = h
    if old_hash is None or old_text is None:
        return st, None, "baseline recorded"
    if h == old_hash:
        return st, None, "unchanged"
    added = added_lines(old_text, text)
    if not added:
        return st, None, "changed only in numbers"
    st["lastChangedAt"] = now.isoformat()
    tier = {"official": "official", "reliable_news": "reliable_news", "business_official": "business_official"}.get(src["reliability"], "official")
    cand = make_candidate(src, tier, url, added, now, h)
    if cand is None:
        return st, None, "changed, judged irrelevant"
    return st, cand, "CHANGED -> candidate %s (confidence %.2f%s)" % (cand["id"], cand["confidence"], ", HIGH-RISK" if cand["risk"]["high_risk"] else "")


def expire_candidates(now, dry=False):
    ttl = int(store.load("site-config").get("pipeline", {}).get("candidateTtlDays", 14))
    n = 0
    for name in sorted(os.listdir(CAND_DIR)) if os.path.isdir(CAND_DIR) else []:
        if not name.endswith(".json"):
            continue
        p = os.path.join(CAND_DIR, name)
        c = json.load(open(p, encoding="utf-8"))
        if c["review"]["state"] == "pending" and now - store.parse_dt(c["createdAt"]) > dt.timedelta(days=ttl):
            c["review"] = {"state": "superseded", "by": "monitor", "at": now.date().isoformat(),
                           "note": "expired unreviewed after %d days; never published" % ttl}
            if not dry:
                json.dump(c, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
                open(p, "a").write("\n")
            n += 1
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--source")
    ap.add_argument("--fixtures")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--expire", action="store_true")
    ap.add_argument("--summary-file")
    a = ap.parse_args()

    now = store.now()
    state = load_state()
    sources = [s for s in store.load("sources")["sources"]
               if s.get("active") and s.get("url") and s.get("monitor", {}).get("type") in ("html", "rss")]
    if a.source:
        sources = [s for s in sources if s["id"] == a.source]
        if not sources:
            sys.exit("no active monitorable source %r" % a.source)
    os.makedirs(CAND_DIR, exist_ok=True)
    known = existing_candidate_ids()
    new_cands, failures, lines = [], [], []
    for src in sources:
        st = state.get(src["id"], {})
        if not (a.all or a.source or a.fixtures) and not is_due(src, st, now):
            continue
        st, cand, msg = check_source(src, st, now, a.fixtures, a.dry_run)
        state[src["id"]] = st
        lines.append("  %-26s %s" % (src["id"], msg))
        if msg.startswith("FAILED"):
            failures.append(src["id"])
        if cand and cand["id"] not in known:
            new_cands.append(cand)
            if not a.dry_run:
                with open(os.path.join(CAND_DIR, cand["id"] + ".json"), "w", encoding="utf-8") as fh:
                    json.dump(cand, fh, indent=2, ensure_ascii=False)
                    fh.write("\n")
    expired = expire_candidates(now, a.dry_run) if a.expire else 0
    if not a.dry_run:
        save_state(state)
    print("\n".join(lines) or "  (no sources due)")
    print("\nchecked %d source(s): %d new candidate(s), %d failure(s)%s" % (
        len(lines), len(new_cands), len(failures), (", %d expired" % expired) if a.expire else ""))
    if a.summary_file:
        md = ["## Source monitor", "", "%d new candidate(s). **Nothing here is published.** Review each one, open its source, and approve with `python3 tools/cms.py candidate approve <id> --approved-by \"Your Name\" --published-at YYYY-MM-DD --read-source`." % len(new_cands), ""]
        for c in new_cands:
            md.append("- `%s` — %s (%s, confidence %.2f%s)  \n  %s" % (
                c["id"], c["extracted"]["title"], c["sourceName"], c["confidence"],
                ", **high-risk: needs a named approver**" if c["risk"]["high_risk"] else "", c["sourceUrl"]))
        if failures:
            md += ["", "Sources that failed this run: " + ", ".join("`%s`" % f for f in failures)]
        with open(a.summary_file, "w", encoding="utf-8") as fh:
            fh.write("\n".join(md) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
