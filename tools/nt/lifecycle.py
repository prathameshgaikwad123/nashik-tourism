"""Kumbh lifecycle: which phase the site is in, and what that implies.

The site must not be built around August–September 2027. Phases are data
(data/site-config.json), not code, so the editor can move a boundary when the
Authority confirms or changes a date, without touching a template.

    preparation   before the Mela opens
    mela_open     the Mela has opened; the peak bathing season has not begun
    peak          the live window around the main bathing dates ("NASHIK — LIVE")
    extended      the Mela continues, quieter, after the peak
    post_kumbh    the Mela has closed: Kumbh-live items archive, evergreen stays
    evergreen     long after: Kumbh is one topic among many

The homepage reads `profile()` to decide how much room Kumbh gets, whether the
live band shows, and what the Kumbh block says.
"""
from . import store
from .enums import PHASES

DEFAULT_PROFILE = {
    "homeKumbhEmphasis": "standard",
    "liveBand": False,
    "archiveKumbhLive": False,
}


def config():
    return store.load("site-config")


def phases(cfg=None):
    cfg = cfg or config()
    return cfg["kumbh"]["phases"]


def phase_for(when=None, cfg=None):
    """The phase containing `when` (default: now). Honors a manual override."""
    cfg = cfg or config()
    override = cfg["kumbh"].get("forcePhase")
    if override:
        if override not in PHASES:
            raise SystemExit("site-config.json: forcePhase %r is not a known phase" % override)
        return next(p for p in cfg["kumbh"]["phases"] if p["id"] == override)
    when = (when or store.now()).date()
    for p in cfg["kumbh"]["phases"]:
        start = store.parse_dt(p["from"]).date() if p.get("from") else None
        end = store.parse_dt(p["to"]).date() if p.get("to") else None
        if (start is None or when >= start) and (end is None or when <= end):
            return p
    return cfg["kumbh"]["phases"][-1]


def profile(when=None, cfg=None):
    p = phase_for(when, cfg)
    out = dict(DEFAULT_PROFILE)
    out.update(p.get("profile", {}))
    out["id"] = p["id"]
    out["label"] = p.get("label", p["id"])
    return out


def client_payload(cfg=None):
    """What /live.js needs to re-evaluate the phase in the browser, so a page
    that was built weeks ago still switches mode on the right day."""
    cfg = cfg or config()
    return {
        "forcePhase": cfg["kumbh"].get("forcePhase"),
        "phases": [{"id": p["id"], "from": p.get("from"), "to": p.get("to"),
                    "profile": {**DEFAULT_PROFILE, **p.get("profile", {})}}
                   for p in cfg["kumbh"]["phases"]],
    }
