"""Controlled vocabularies. One place, so a new category is one edit."""

# ── Sources ──────────────────────────────────────────────────────────────────
SOURCE_CATEGORIES = [
    "kumbh", "government", "transport", "railway", "airport", "roads", "police",
    "tourism", "events", "weather", "attractions", "accommodation", "accessibility",
    "safety", "news",
]
# Source hierarchy, highest trust first.
#   official          Tier 1  government, authority, railway, trust, venue's own site
#   reliable_news     Tier 2  established publications
#   business_official Tier 3  a hotel/restaurant/vineyard's own information
#   social            Tier 4  never treated as confirmation
#   data_provider     machine data feeds (weather API) — used for numbers, not claims
RELIABILITY = ["official", "reliable_news", "business_official", "social", "data_provider"]
TIER = {"official": 1, "reliable_news": 2, "business_official": 3, "social": 4, "data_provider": 3}
CHECK_FREQUENCY = ["hourly", "daily", "weekly", "monthly", "manual"]
URL_STATUS = ["unchecked", "located", "to_be_confirmed", "ok", "broken"]

# ── Updates ──────────────────────────────────────────────────────────────────
UPDATE_CATEGORIES = [
    "Kumbh", "Transport", "Roads", "Railways", "Airport", "Accommodation",
    "Tourism", "Events", "Government", "Safety", "Weather", "Local",
]
# How sure we are about the item right now.
UPDATE_STATUS = ["confirmed", "developing", "changed", "cancelled", "archived"]
# Where the item sits in the editorial workflow (applies to every content type).
CONTENT_STATUS = ["draft", "review", "published", "updated", "archived"]
LIVE_CONTENT_STATUS = ["published", "updated"]

# ── Events ───────────────────────────────────────────────────────────────────
EVENT_CATEGORIES = [
    "Kumbh", "Religious", "Cultural", "Food", "Wine", "Music", "Exhibitions",
    "Tourism", "Trekking", "Local",
]
EVENT_STATUS = ["scheduled", "rescheduled", "postponed", "cancelled", "completed"]

# ── Facts, destinations, accessibility ───────────────────────────────────────
#   verified      an editor has read the cited source and it supports the value
#   reported      credible publications / a located official page say so, but an
#                 editor has not yet confirmed it against the official source
#   not_verified  carried over from earlier site copy, no supporting source yet
#   disputed      sources disagree — shown with the disagreement, never resolved silently
FACT_STATUS = ["verified", "reported", "not_verified", "disputed"]
VERIFICATION_STATUS = FACT_STATUS

ACCESS_STATUS = [
    "verified_accessible", "partially_accessible", "accessibility_unknown",
    "accessibility_varies_by_event",
]

DESTINATION_CATEGORIES = ["spiritual", "heritage", "nature", "wine"]

# Lifecycle phases of the Kumbh content (see tools/nt/lifecycle.py).
PHASES = ["preparation", "mela_open", "peak", "extended", "post_kumbh", "evergreen"]
