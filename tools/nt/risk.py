"""High-risk information policy.

Some information can hurt a traveller if it is wrong: where to go in an
emergency, whether a road is open, whether a pass is needed. This module is the
single definition of what counts as high-risk. Nothing high-risk is ever
published without a named human approver — whether a person wrote it or the
monitoring pipeline extracted it.

The check is deliberately over-inclusive. A false positive costs an editor ten
seconds; a false negative puts unreviewed safety information in front of a
pilgrim. Categories decide first; the keyword rules catch high-risk content that
was filed under a lower-risk category (a "Local" item announcing a road
closure is still a road closure).
"""
import re

# Items in these categories are always high-risk.
ALWAYS_HIGH_RISK_CATEGORIES = {"Safety", "Roads"}

# Reason -> pattern. Matched case-insensitively against title + summary + tags.
RULES = [
    ("safety",              r"\b(safety|unsafe|stampede|crowd (control|crush|management)|evacuat\w*|fire|flood\w*|landslide)\b"),
    ("medical",             r"\b(medical|hospital|doctor|ambulance|first[- ]aid|health (camp|advisory)|medicine|vaccinat\w*|outbreak|heat ?stroke)\b"),
    ("emergency",           r"\b(emergency|helpline|distress|rescue|disaster)\b"),
    ("religious-date",      r"\b(amrit snan|shahi snan|snan dates?|parva snan|tithi|muhurat|shubh|auspicious (date|day)|flag[- ]hoisting|dhwajarohan|amavasya|purnima)\b"),
    ("kumbh-rule",          r"\b(rules?|guidelines?|prohibited|banned?|not allowed|mandatory|compulsory|must carry|permitted|permit)\b"),
    ("pass-registration",   r"\b(e-?pass|passes|pass required|registration|register(ed)?|qr code|vip pass|entry pass)\b"),
    ("traffic",             r"\b(traffic|diversions?|barricad\w*|no[- ]entry|one[- ]way|vehicle (ban|restriction)|parking)\b"),
    ("road-closure",        r"\b(road clos\w*|closed (to|for) (traffic|vehicles)|bridge clos\w*|route (closed|changed)|highway clos\w*)\b"),
    ("transport-restriction", r"\b(cancel(l)?ed|suspend\w*|restricted|curtail\w*|diverted|short[- ]terminat\w*|trains? (cancel|regulat|divert)|bus services? (suspend|stop))\b"),
    ("entry-restriction",   r"\b(entry (ban|restriction|closed|prohibited)|clos(ed|ure|ing)|shut(down)?|remain(s)? closed|darshan (suspended|closed)|restricted (area|zone)|no visitors|not open)\b"),
    ("government-order",    r"\b(government resolution|\bGR\b|govt\.? order|order issued|notification|circular|directive|collector('s)? order|prohibitory order|section 144|bnss 163)\b"),
    ("accommodation-availability", r"\b(sold out|fully booked|rooms? (available|left)|availability|vacan\w+|tent city (booking|allotment)|dharamshala (booking|allotment))\b"),
    ("pricing",             r"(₹|\brs\.?\s?\d|\binr\b|\brupees?\b|\bfares?\b|\bfees?\b|\bticket (price|cost)\b|\bcharges?\b|\bprices?\b|\bcost[s]?\b)"),
]
_COMPILED = [(name, re.compile(rx, re.I)) for name, rx in RULES]

# Tags an editor can add by hand to force review.
HIGH_RISK_TAGS = {"high-risk", "safety", "medical", "emergency", "restriction", "closure",
                  "pricing", "pass", "registration", "government-order", "religious-date"}


def _blob(item):
    parts = [item.get("title") or "", item.get("summary") or "", item.get("description") or ""]
    parts.extend(item.get("tags") or [])
    return " \n ".join(parts)


def assess(item):
    """Return {'high_risk': bool, 'reasons': [...]}. `item` is an update, event or candidate."""
    reasons = []
    category = item.get("category")
    if category in ALWAYS_HIGH_RISK_CATEGORIES:
        reasons.append("category:%s" % category)
    tags = {str(t).lower() for t in (item.get("tags") or [])}
    for t in sorted(tags & HIGH_RISK_TAGS):
        reasons.append("tag:%s" % t)
    text = _blob(item)
    for name, rx in _COMPILED:
        if rx.search(text):
            reasons.append(name)
    return {"high_risk": bool(reasons), "reasons": reasons}


def is_high_risk(item):
    return assess(item)["high_risk"]


def may_auto_publish(item, config, source_tier):
    """Whether the pipeline is *allowed* to publish without a human.

    Defaults to never. It only becomes possible when the site owner turns
    `pipeline.autoPublishLowRisk` on in data/site-config.json, and even then only
    for low-risk items from allowed source tiers that cleared the confidence bar.
    """
    cfg = (config or {}).get("pipeline", {})
    if not cfg.get("autoPublishLowRisk", False):
        return False
    if is_high_risk(item):
        return False
    if source_tier not in cfg.get("autoPublishTiers", ["official"]):
        return False
    return float(item.get("confidence") or 0) >= float(cfg.get("minConfidence", 0.9))
