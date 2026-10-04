#!/usr/bin/env python3
"""
Content health: is this site still telling the truth?

    python3 tools/content-health.py            # writes reports/content-health.{json,md,html}
    python3 tools/content-health.py --strict   # exit 1 if broken links/anchors exist

A site meant to stay current for years needs a way to see what has gone stale.
This reads the same data the pages are built from and reports:

    Total pages · Verified pages · Pages needing review · Expired / expiring updates
    Broken sources · Stale facts · Upcoming events · Recently changed pages
    Missing metadata · Broken links · Pending candidates

It makes no network calls. Source reachability comes from data/state/ (written by
tools/monitor-sources.py), so run the monitor first for a complete picture.
"""
import datetime as dt
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt import content, enums, render, store  # noqa: E402
from nt.paths import DATA, REPORTS, ROOT  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def days_since(value, today):
    d = store.parse_dt(value)
    return (today - d.date()).days if d else None


def all_pages():
    out = []
    for dirpath, _d, files in os.walk(ROOT):
        for n in files:
            if n.endswith(".html") and n != "nav-template.html":
                full = os.path.join(dirpath, n)
                rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
                out.append("/" if rel == "index.html" else ("/" + rel[:-len("index.html")] if rel.endswith("/index.html") else "/" + rel))
    return sorted(out)


def seo_report():
    tmp = os.path.join(REPORTS, "seo.json")
    os.makedirs(REPORTS, exist_ok=True)
    subprocess.call([sys.executable, os.path.join(HERE, "seo-check.py"), "--json", tmp], stdout=subprocess.DEVNULL)
    try:
        return json.load(open(tmp, encoding="utf-8"))
    except (OSError, ValueError):
        return {"errors": [], "warnings": []}


def main():
    now = store.now()
    today = now.date()
    cfg = store.load("site-config")
    fresh = cfg["freshness"]
    facts = store.load("facts")["facts"]
    sources = store.load("sources")["sources"]
    pages_meta = store.load("pages")["pages"]
    dests = store.load("destinations")["destinations"]
    changelog = store.load("changelog")["entries"]
    updates = content.all_updates()
    pages = all_pages()
    seo = seo_report()

    # ── facts ────────────────────────────────────────────────────────────────
    by_status = {s: 0 for s in enums.FACT_STATUS}
    stale, never = [], []
    for f in facts:
        by_status[f["status"]] += 1
        limit = fresh["factStaleAfterDays"].get(f.get("topic"), fresh["factStaleAfterDays"]["default"])
        last = f.get("verifiedAt") or f.get("lastCheckedAt")
        age = days_since(last, today) if last else None
        if age is None:
            never.append({"id": f["id"], "status": f["status"], "topic": f.get("topic")})
        elif age > limit:
            stale.append({"id": f["id"], "status": f["status"], "ageDays": age, "limitDays": limit})

    # ── pages ────────────────────────────────────────────────────────────────
    review, verified_pages = [], 0
    review_days = fresh["pageReviewDays"]
    for path, m in pages_meta.items():
        limit = review_days.get(m.get("topic"), review_days["default"])
        age = days_since(m.get("lastVerified"), today) if m.get("lastVerified") else None
        if m.get("verificationStatus") == "verified" and age is not None and age <= limit:
            verified_pages += 1
        else:
            review.append({"path": path, "status": m.get("verificationStatus"), "topic": m.get("topic"),
                           "reason": "never verified" if age is None else "last verified %d days ago (limit %d)" % (age, limit)})
    for d in dests:
        path = "/discover-nashik/%s/" % d["slug"]
        age = days_since(d.get("lastVerified"), today) if d.get("lastVerified") else None
        if d.get("verificationStatus") == "verified" and age is not None and age <= review_days["destination"]:
            verified_pages += 1
        else:
            review.append({"path": path, "status": d.get("verificationStatus"), "topic": "destination",
                           "reason": "never verified" if age is None else "last verified %d days ago (limit %d)" % (age, review_days["destination"])})
    # Hubs: only as current as the weakest fact they show.
    hub_facts = {"/kumbh-mela-2027/": [f for f in facts if f["id"].startswith(("kumbh.", "safety."))],
                 "/transport/": [f for f in facts if f["id"].startswith(("transport.", "airport."))]}
    for path, fs in hub_facts.items():
        weak = [f["id"] for f in fs if f["status"] != "verified"]
        if weak:
            review.append({"path": path, "status": "mixed", "topic": "kumbh" if "kumbh" in path else "transport",
                           "reason": "%d of %d facts not verified" % (len(weak), len(fs))})
        else:
            verified_pages += 1

    # ── updates ──────────────────────────────────────────────────────────────
    live = content.live_updates()
    expiring = [u["id"] for u in live if u.get("expiresAt") and 0 <= (store.parse_dt(u["expiresAt"], True).date() - today).days <= 3]
    recently_expired = [u["id"] for u in updates if u.get("expiresAt") and render.is_expired(u) and 0 <= (days_since(u["expiresAt"], today) if days_since(u["expiresAt"], today) is not None else 99) <= 7]
    drafts = [u["id"] for u in updates if u["contentStatus"] in ("draft", "review")]

    # ── sources ──────────────────────────────────────────────────────────────
    state = {}
    sp = os.path.join(DATA, "state", "source-state.json")
    if os.path.isfile(sp):
        state = json.load(open(sp, encoding="utf-8"))
    broken = [{"id": s["id"], "reason": state.get(s["id"], {}).get("lastError") or "failed repeatedly"} for s in sources
              if state.get(s["id"], {}).get("urlStatus") == "broken"]
    unconfirmed = [s["id"] for s in sources if s.get("urlStatus") == "to_be_confirmed"]
    unchecked = [s["id"] for s in sources if s.get("active") and s["id"] not in state]
    unopened = [s["id"] for s in sources if s.get("urlStatus") in ("located", "unchecked") and not s.get("citation")]

    # ── events, changes, candidates ──────────────────────────────────────────
    upcoming, _past = content.events()
    soon = [e for e in upcoming if (store.parse_dt(e["date"]).date() - today).days <= 30]
    unverified_events = [e["id"] for e in upcoming if e.get("verificationStatus") != "verified"]
    recent = sorted([e for e in changelog if days_since(e["date"], today) is not None and 0 <= days_since(e["date"], today) <= 30], key=lambda e: e["date"], reverse=True)
    cand_dir = os.path.join(DATA, "pipeline", "candidates")
    pending = []
    if os.path.isdir(cand_dir):
        for n in sorted(os.listdir(cand_dir)):
            if n.endswith(".json"):
                c = json.load(open(os.path.join(cand_dir, n), encoding="utf-8"))
                if c["review"]["state"] == "pending":
                    pending.append({"id": c["id"], "ageDays": days_since(c["createdAt"], today), "highRisk": c["risk"]["high_risk"]})

    broken_links = [e for e in seo["errors"] if "broken" in e]
    missing_meta = [e for e in seo["errors"] if "missing" in e and "sitemap" not in e]

    report = {
        "generatedAt": now.isoformat(),
        "totals": {"pages": len(pages), "verifiedPages": verified_pages, "pagesNeedingReview": len(review),
                   "liveUpdates": len(live), "expiringUpdates": len(expiring), "recentlyExpired": len(recently_expired),
                   "draftUpdates": len(drafts), "brokenSources": len(broken), "sourcesNeedingUrl": len(unconfirmed),
                   "staleFacts": len(stale), "factsNeverChecked": len(never), "upcomingEvents30d": len(soon),
                   "unverifiedUpcomingEvents": len(unverified_events), "recentlyChangedPages": len({e["path"] for e in recent}),
                   "missingMetadata": len(missing_meta), "brokenLinks": len(broken_links), "pendingCandidates": len(pending)},
        "facts": {"byStatus": by_status, "stale": stale, "neverChecked": never},
        "pagesNeedingReview": review, "expiringUpdates": expiring, "recentlyExpired": recently_expired, "drafts": drafts,
        "brokenSources": broken, "sourcesNeedingUrl": unconfirmed, "sourcesNeverMonitored": unchecked,
        "sourceUrlsNotYetOpenedByEditor": unopened,
        "upcomingEvents": [{"id": e["id"], "date": e["date"], "verification": e["verificationStatus"]} for e in soon],
        "recentChanges": recent, "missingMetadata": missing_meta, "brokenLinks": broken_links,
        "pendingCandidates": pending,
    }
    os.makedirs(REPORTS, exist_ok=True)
    with open(os.path.join(REPORTS, "content-health.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    write_md(report)
    write_html(report)
    t = report["totals"]
    print("content health — %s" % today)
    for k, v in t.items():
        print("  %-26s %s" % (k, v))
    print("\nwrote reports/content-health.{json,md,html}")
    if "--strict" in sys.argv and broken_links:
        sys.exit(1)


def write_md(r):
    t = r["totals"]
    L = ["# Content health", "", "Generated %s" % r["generatedAt"], "", "| Metric | Count |", "|---|---|"]
    L += ["| %s | %s |" % (k, v) for k, v in t.items()]
    L += ["", "## Facts by status", ""] + ["- %s: %d" % (k, v) for k, v in r["facts"]["byStatus"].items()]
    L += ["", "## Pages needing review (%d)" % len(r["pagesNeedingReview"]), ""]
    L += ["- `%s` — %s (%s)" % (p["path"], p["reason"], p["status"]) for p in r["pagesNeedingReview"]]
    for title, key in (("Stale facts", None), ("Pending candidates", "pendingCandidates"), ("Broken sources", "brokenSources"),
                       ("Sources still needing an official URL", "sourcesNeedingUrl"), ("Broken links", "brokenLinks"),
                       ("Missing metadata", "missingMetadata")):
        items = r["facts"]["stale"] if key is None else r[key]
        L += ["", "## %s (%d)" % (title, len(items)), ""] + ["- %s" % (json.dumps(i, ensure_ascii=False) if isinstance(i, dict) else i) for i in items[:60]]
    with open(os.path.join(REPORTS, "content-health.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


def write_html(r):
    esc = render.esc
    t = r["totals"]
    cards = "".join('<div class="c"><b>%s</b><span>%s</span></div>' % (v, esc(k)) for k, v in t.items())

    def table(title, rows, cols):
        if not rows:
            return "<h2>%s</h2><p>Nothing to report.</p>" % esc(title)
        head = "".join("<th scope=\"col\">%s</th>" % esc(c) for c in cols)
        body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % esc(row.get(c, "") if isinstance(row, dict) else row) for c in cols) for row in rows[:80])
        return "<h2>%s (%d)</h2><div class=\"w\" tabindex=\"0\" role=\"region\" aria-label=\"%s\"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>" % (esc(title), len(rows), esc(title), head, body)

    html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Content health</title>
<style>body{font:16px/1.5 system-ui,sans-serif;margin:0;padding:1rem;background:#FCFAF7;color:#1A1A2E;max-width:1100px;margin-inline:auto}
h1{font-size:1.5rem}h2{font-size:1.1rem;margin-top:2rem}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.6rem}
.c{background:#fff;border:1px solid #ddd;border-radius:8px;padding:.7rem}.c b{display:block;font-size:1.6rem}.c span{font-size:.78rem;color:#5A5140}
.w{overflow-x:auto}table{border-collapse:collapse;width:100%%;font-size:.88rem;background:#fff}th,td{border:1px solid #ddd;padding:.4rem .6rem;text-align:left;vertical-align:top}th{background:#2D1B69;color:#fff}
.w:focus-visible{outline:3px solid #2D1B69}</style></head><body><main><h1>Content health</h1><p>Generated %s. Source of truth: <code>data/</code>. Run <code>python3 tools/content-health.py</code> to refresh.</p>
<div class="g">%s</div>
%s%s%s%s%s%s%s</main></body></html>""" % (
        esc(r["generatedAt"]), cards,
        table("Pages needing review", r["pagesNeedingReview"], ["path", "status", "reason"]),
        table("Stale facts", r["facts"]["stale"], ["id", "status", "ageDays", "limitDays"]),
        table("Pending candidates", r["pendingCandidates"], ["id", "ageDays", "highRisk"]),
        table("Broken sources", r["brokenSources"], ["id", "reason"]),
        table("Broken links and anchors", [{"issue": x} for x in r["brokenLinks"]], ["issue"]),
        table("Missing metadata", [{"issue": x} for x in r["missingMetadata"]], ["issue"]),
        table("Recent changes", r["recentChanges"], ["date", "path", "type", "summary"]))
    with open(os.path.join(REPORTS, "content-health.html"), "w", encoding="utf-8") as fh:
        fh.write(html)


if __name__ == "__main__":
    main()
