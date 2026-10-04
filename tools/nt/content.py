"""Selectors over the editorial data: what is live, what is archived, what is next.

Every generator asks these functions rather than filtering the JSON itself, so
"live", "expired" and "upcoming" mean the same thing on the homepage, the
updates page, Nashik Now, the feeds and the search index.
"""
from . import enums, lifecycle, render, store


def _archive_kumbh_live():
    try:
        return bool(lifecycle.profile().get("archiveKumbhLive"))
    except (FileNotFoundError, SystemExit, KeyError):
        return False


def all_updates():
    return store.load("updates")["updates"]


def live_updates(category=None, categories=None, tag=None, when=None, limit=None):
    when = when or store.now()
    arch = _archive_kumbh_live()
    out = [u for u in all_updates() if render.is_live_update(u, when, arch)]
    if category:
        out = [u for u in out if u["category"] == category]
    if categories:
        out = [u for u in out if u["category"] in categories]
    if tag:
        out = [u for u in out if tag in (u.get("tags") or [])]
    out.sort(key=lambda u: (u["publishedAt"], u["id"]), reverse=True)
    return out[:limit] if limit else out


def archived_updates(when=None):
    """Published items that have expired, been archived, or fell to a lifecycle
    phase change. Drafts and items under review are never shown."""
    when = when or store.now()
    arch = _archive_kumbh_live()
    out = [u for u in all_updates()
           if u.get("contentStatus") in (enums.LIVE_CONTENT_STATUS + ["archived"])
           and not render.is_live_update(u, when, arch)]
    out.sort(key=lambda u: (u["publishedAt"], u["id"]), reverse=True)
    return out


def events(when=None):
    when = when or store.now()
    today = when.date().isoformat()
    live = [e for e in store.load("events")["events"] if e.get("contentStatus") in enums.LIVE_CONTENT_STATUS]
    upcoming = sorted([e for e in live if (e.get("endDate") or e["date"]) >= today and e["status"] != "cancelled"],
                      key=lambda e: (e["date"], e["id"]))
    past = sorted([e for e in live if (e.get("endDate") or e["date"]) < today or e["status"] == "cancelled"],
                  key=lambda e: (e["date"], e["id"]), reverse=True)
    return upcoming, past


def latest_stamp(items, *keys):
    """Most recent date among the given keys of `items` (for lastmod and feeds)."""
    best = None
    for it in items:
        for k in keys:
            v = it.get(k)
            if v and (best is None or str(v) > str(best)):
                best = v
    return best
