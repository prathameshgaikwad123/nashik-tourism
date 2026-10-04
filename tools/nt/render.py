"""HTML fragments reused by every generated page.

Design rules baked in here:
  * Status is never colour-only: every badge pairs a glyph and a text label.
  * Provenance is never hidden: a fact, update or event always shows where it
    came from and when it was last checked, in the markup, not behind a tooltip.
  * Missing data is never rendered as 'None', 'null' or blank. Unknown values
    become 'Information not yet confirmed', with a way to check the source.
"""
import html as _html
import re

from . import enums, store

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
MON3 = [m[:3] for m in MONTHS]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def esc(text):
    return _html.escape("" if text is None else str(text), quote=True)


def plain(text):
    """HTML fragment -> plain text (for meta descriptions, search, JSON-LD)."""
    t = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", _html.unescape(t)).strip()


# ── Dates ────────────────────────────────────────────────────────────────────
def _dt(value):
    return store.parse_dt(value)


def fmt_date(value, short=False, weekday=False):
    d = _dt(value)
    if d is None:
        return ""
    month = MON3[d.month - 1] if short else MONTHS[d.month - 1]
    s = "%d %s %d" % (d.day, month, d.year)
    return ("%s %s" % (WEEKDAYS[d.weekday()], s)) if weekday else s


def fmt_dt(value, short=True):
    """'4 Oct 2026, 3:30 pm IST' when the value carries a time, else the date."""
    if value is None or value == "":
        return ""
    if len(str(value)) == 10:
        return fmt_date(value, short=short)
    d = _dt(value).astimezone(store.IST)
    h = d.hour % 12 or 12
    return "%s, %d:%02d %s IST" % (fmt_date(d.isoformat(), short=short), h, d.minute, "am" if d.hour < 12 else "pm")


def time_tag(value, short=True, fallback=""):
    if not value:
        return fallback
    return '<time datetime="%s">%s</time>' % (esc(value), esc(fmt_dt(value, short=short)))


# ── Links ────────────────────────────────────────────────────────────────────
def ext_link(url, text, track="official_source_click", item=None, cls=""):
    """An outbound link to a source. Same tab, so nothing opens unannounced;
    data-track lets /site.js report the click (no personal data)."""
    attrs = ' href="%s" rel="noopener noreferrer" data-track="%s"' % (esc(url), esc(track))
    if item:
        attrs += ' data-track-item="%s"' % esc(item)
    if cls:
        attrs += ' class="%s"' % esc(cls)
    return "<a%s>%s</a>" % (attrs, text)


UNCONFIRMED = "Information not yet confirmed"
CHECK_OFFICIAL = "Check with the official authority before travelling."


def unconfirmed(link=True):
    s = '<span class="unconfirmed">%s.' % UNCONFIRMED
    if link:
        s += ' <a href="/sources/">%s</a>' % CHECK_OFFICIAL
    else:
        s += " " + CHECK_OFFICIAL
    return s + "</span>"


# ── Badges ───────────────────────────────────────────────────────────────────
FACT_BADGES = {
    "verified":     ("✓", "Verified"),
    "reported":     ("◐", "Reported, not yet confirmed"),
    "not_verified": ("○", "Not yet verified"),
    "disputed":     ("⚠", "Sources differ"),
}
UPDATE_BADGES = {
    "confirmed":  ("✓", "Confirmed"),
    "developing": ("◔", "Developing"),
    "changed":    ("↻", "Changed"),
    "cancelled":  ("✕", "Cancelled"),
    "archived":   ("▣", "Archived"),
}
EVENT_BADGES = {
    "scheduled":   ("◷", "Scheduled"),
    "rescheduled": ("↻", "Rescheduled"),
    "postponed":   ("◔", "Postponed"),
    "cancelled":   ("✕", "Cancelled"),
    "completed":   ("✓", "Completed"),
}
ACCESS_BADGES = {
    "verified_accessible":           ("✓", "Verified accessible"),
    "partially_accessible":          ("◐", "Partially accessible"),
    "accessibility_unknown":         ("?", "Accessibility unknown"),
    "accessibility_varies_by_event": ("↻", "Varies by event"),
}


def badge(kind, table, key, label=None, extra=""):
    glyph, default = table.get(key, ("•", key))
    text = label or default
    if extra:
        text = "%s %s" % (text, extra)
    return ('<span class="st st-%s st-%s"><span class="st-i" aria-hidden="true">%s</span>%s</span>'
            % (esc(kind), esc(key), glyph, esc(text)))


def fact_badge(status, verified_at=None):
    extra = fmt_date(verified_at, short=True) if (status == "verified" and verified_at) else ""
    return badge("fact", FACT_BADGES, status, extra=extra)


def update_badge(status):
    return badge("update", UPDATE_BADGES, status)


def event_badge(status):
    return badge("event", EVENT_BADGES, status)


def access_badge(status):
    return badge("access", ACCESS_BADGES, status)


# ── Facts ────────────────────────────────────────────────────────────────────
def facts_index():
    return {f["id"]: f for f in store.load("facts")["facts"]}


def sources_index():
    return {s["id"]: s for s in store.load("sources")["sources"]}


def fact_source_html(f, track_item=None):
    src = f.get("source") or {}
    name = esc(src.get("name") or "Source not yet linked")
    if src.get("url"):
        return ext_link(src["url"], name, item=track_item or f["id"])
    if src.get("path"):
        return '<a href="%s">%s</a>' % (esc(src["path"]), name)
    return name


def fact_value_html(f):
    """The value as it should read to a person. Never None/null."""
    disp = f.get("display")
    if disp in (None, ""):
        return unconfirmed(link=False)
    return esc(disp)


def fact_inline(fid, facts=None, flag=True):
    """A value with its status badge. Wrapped in data-fact so /tools/apply-facts.py
    can refresh the same span in hand-written pages when the fact changes."""
    facts = facts or facts_index()
    f = facts.get(fid)
    if f is None:
        return unconfirmed()
    val = fact_value_html(f)
    flag_html = (' <span class="fact-flag">%s</span>' % fact_badge(f["status"], f.get("verifiedAt"))) if flag else ""
    return '<span class="fact" data-fact="%s">%s%s</span>' % (esc(fid), val, flag_html)


def fact_card(f, sources=None):
    """A fully attributed fact: value, status, source, dates, notes, alternatives."""
    rows = []
    rows.append('<div class="fc-head"><p class="fc-label">%s</p>%s</div>'
                % (esc(f["fact"]), fact_badge(f["status"], f.get("verifiedAt"))))
    rows.append('<p class="fc-value">%s</p>' % fact_value_html(f))
    alts = f.get("alternatives") or []
    if alts:
        items = []
        for a in alts:
            s = a.get("source") or {}
            src = ext_link(s["url"], esc(s.get("name") or "source"), item=f["id"]) if s.get("url") else esc(s.get("name") or "")
            items.append("<li><strong>%s</strong> &mdash; %s. Source: %s</li>"
                         % (esc(a.get("value")), esc(a.get("scope")), src))
        rows.append('<ul class="fc-alts">%s</ul>' % "".join(items))
    if f.get("notes"):
        rows.append('<p class="fc-note">%s</p>' % esc(f["notes"]))
    meta = ["<dt>Source</dt><dd>%s</dd>" % fact_source_html(f)]
    if f.get("verifiedAt"):
        meta.append("<dt>Verified</dt><dd>%s</dd>" % time_tag(f["verifiedAt"]))
    else:
        meta.append("<dt>Verified</dt><dd>Not yet verified by our editors</dd>")
    if f.get("lastCheckedAt"):
        meta.append("<dt>Last checked</dt><dd>%s</dd>" % time_tag(f["lastCheckedAt"]))
    rows.append('<dl class="meta-dl">%s</dl>' % "".join("<div>%s</div>" % m for m in meta))
    return '<article class="fact-card" id="f-%s">%s</article>' % (esc(f["id"].replace(".", "-")), "".join(rows))


# ── Expiry ───────────────────────────────────────────────────────────────────
def is_expired(item, when=None):
    exp = store.parse_dt(item.get("expiresAt"), end_of_day=True)
    return bool(exp and exp < (when or store.now()))


def effective_status(u, when=None):
    """An update past its expiry is archived without anyone editing it."""
    if u.get("contentStatus") == "archived" or u.get("status") == "archived":
        return "archived"
    if is_expired(u, when):
        return "archived"
    return u.get("status")


def is_live_update(u, when=None, archive_kumbh_live=False):
    if u.get("contentStatus") not in enums.LIVE_CONTENT_STATUS:
        return False
    if effective_status(u, when) == "archived":
        return False
    if archive_kumbh_live and "kumbh-live" in (u.get("tags") or []):
        return False
    return True


# ── Update + event cards ─────────────────────────────────────────────────────
def meta_dl(rows):
    """rows: list of (label, html). Rendered as a definition list in a grid."""
    return '<dl class="meta-dl">%s</dl>' % "".join(
        "<div><dt>%s</dt><dd>%s</dd></div>" % (esc(k), v) for k, v in rows)


def update_card(u, when=None, tag="h3", compact=False):
    st = effective_status(u, when)
    source = (ext_link(u["sourceUrl"], esc(u["sourceName"]), item=u["id"])
              if u.get("sourceUrl") else esc(u["sourceName"]))
    rows = [("Source", source),
            ("Published", time_tag(u.get("publishedAt"))),
            ("Verified", time_tag(u["verifiedAt"]) if u.get("verifiedAt") else "Not yet verified"),
            ("Last checked", time_tag(u.get("lastCheckedAt")))]
    if u.get("expiresAt"):
        rows.append(("Expires" if st != "archived" else "Expired", time_tag(u["expiresAt"])))
    related = ""
    if u.get("relatedPages") and not compact:
        links = "".join('<li><a href="%s">%s</a></li>' % (esc(p), esc(label_for_path(p)))
                        for p in u["relatedPages"])
        related = '<ul class="uc-related" aria-label="Related pages">%s</ul>' % links
    return """<article class="update-card" id="u-%(id)s" data-category="%(cat)s" data-status="%(st)s" data-tags="%(tags)s"%(exp)s>
  <div class="uc-top"><span class="tag">%(cat)s</span>%(badge)s</div>
  <%(tag)s class="uc-title">%(title)s</%(tag)s>
  <p class="uc-summary">%(summary)s</p>
  %(meta)s%(related)s
</article>""" % {
        "id": esc(u["id"]), "cat": esc(u["category"]), "st": esc(st),
        "tags": esc(u["category"].lower() + " " + st),
        "exp": (' data-expires="%s"' % esc(store.parse_dt(u["expiresAt"], end_of_day=True).isoformat())) if u.get("expiresAt") else "",
        "badge": update_badge(st), "tag": tag, "title": esc(u["title"]),
        "summary": esc(u["summary"]), "meta": meta_dl(rows), "related": related}


_PATH_LABELS = {}


def label_for_path(path):
    base = path.split("#")[0]
    if not _PATH_LABELS:
        _PATH_LABELS.update({
            "/kumbh-mela-2027/": "Kumbh Mela 2027 guide", "/transport/": "Transport hub",
            "/events/": "Events", "/updates/": "Updates", "/nashik-now/": "Nashik Now",
            "/accessible-nashik/": "Accessible Nashik", "/plan-your-trip/": "Plan your trip",
            "/discover-nashik/": "Discover Nashik"})
    if base in _PATH_LABELS:
        label = _PATH_LABELS[base]
        if "#" in path:
            label += " — " + path.split("#", 1)[1].replace("-", " ")
        return label
    return base.strip("/").split("/")[-1].replace("-", " ").title() or "Home"


def event_card(e, tag="h3"):
    d = store.parse_dt(e["date"])
    when = fmt_date(e["date"], weekday=True)
    if e.get("endDate") and e["endDate"] != e["date"]:
        when += " – " + fmt_date(e["endDate"], weekday=True)
    t = ""
    if e.get("startTime"):
        t = e["startTime"] + (" – " + e["endTime"] if e.get("endTime") else "")
    price = e.get("price")
    if price in (None, ""):
        price_html = "Not yet confirmed"
    elif isinstance(price, dict):
        price_html = esc(price.get("note") or ("Free" if price.get("free") else "%s %s" % (price.get("currency", "INR"), price.get("amount"))))
    else:
        price_html = esc(price)
    source = (ext_link(e["sourceUrl"], esc(e["sourceName"]), item=e["id"], track="event_click")
              if e.get("sourceUrl") else esc(e["sourceName"]))
    rows = [("Date", '<time datetime="%s">%s</time>' % (esc(e["date"]), esc(when))),
            ("Time", esc(t) if t else "Not yet confirmed"),
            ("Where", esc(e["location"])),
            ("Price", price_html),
            ("Accessibility", access_badge(e.get("accessibility", "accessibility_unknown"))),
            ("Source", source),
            ("Verified", time_tag(e["lastVerified"]) if e.get("lastVerified") else "Not yet verified"),
            ("Last checked", time_tag(e.get("lastCheckedAt")) if e.get("lastCheckedAt") else "Not recorded")]
    book = ""
    if e.get("bookingUrl"):
        book = '<p class="ec-book">%s</p>' % ext_link(e["bookingUrl"], "Booking page (external)", track="event_click", item=e["id"], cls="btn btn-outline")
    flag = ""
    if e.get("verificationStatus") != "verified":
        flag = ('<p class="ec-flag"><span class="st st-fact st-reported"><span class="st-i" aria-hidden="true">◐</span>'
                'Reported, awaiting official confirmation</span> Check with the official authority before travelling.</p>')
    return """<article class="event-card" id="e-%(id)s" data-category="%(cat)s" data-date="%(date)s" data-tags="%(tags)s">
  <div class="ec-date" aria-hidden="true"><span class="ec-d">%(day)d</span><span class="ec-m">%(mon)s %(yr)d</span></div>
  <div class="ec-body">
    <div class="uc-top"><span class="tag">%(cat)s</span>%(badge)s</div>
    <%(tag)s class="uc-title">%(title)s</%(tag)s>
    <p class="uc-summary">%(desc)s</p>
    %(flag)s%(meta)s%(book)s
  </div>
</article>""" % {"id": esc(e["id"]), "cat": esc(e["category"]), "date": esc(e["date"]),
                 "day": d.day, "mon": MON3[d.month - 1], "yr": d.year, "tags": esc(e["category"].lower() + " " + e["status"]),
                 "badge": event_badge(e["status"]), "tag": tag, "title": esc(e["title"]),
                 "desc": esc(e["description"]), "flag": flag, "meta": meta_dl(rows), "book": book}


# ── Page-level verification ──────────────────────────────────────────────────
def history_for(path, limit=8):
    entries = [e for e in store.load("changelog")["entries"] if e["path"].split("#")[0] == path]
    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries[:limit]


def history_html(path):
    h = history_for(path)
    if not h:
        return ""
    items = "".join('<li><time datetime="%s">%s</time> &mdash; %s</li>'
                    % (esc(e["date"]), esc(fmt_date(e["date"], short=True)), esc(e["summary"])) for e in h)
    return '<details class="verify-history"><summary>Change history</summary><ol>%s</ol></details>' % items


def sources_list_html(source_ids, sources=None):
    sources = sources or sources_index()
    items = []
    for sid in source_ids:
        s = sources.get(sid)
        if not s:
            continue
        if s.get("url"):
            items.append("<li>%s <span class=\"src-tier\">%s</span></li>"
                         % (ext_link(s["url"], esc(s["name"]), item=sid), tier_label(s["reliability"])))
        else:
            items.append("<li>%s <span class=\"src-tier\">%s &middot; official link to be added</span></li>"
                         % (esc(s["name"]), tier_label(s["reliability"])))
    return '<ul class="src-list">%s</ul>' % "".join(items) if items else ""


def tier_label(reliability):
    return {"official": "Official", "reliable_news": "News", "business_official": "Business's own information",
            "social": "Social media (not treated as confirmation)", "data_provider": "Data provider"}.get(reliability, "")


def verify_block(path, status="not_verified", verified_at=None, reviewed_at=None, source_ids=(),
                 caveat=None, heading="How current is this page?", published_at=None):
    caveat_html = '<p class="verify-caveat">%s</p>' % esc(caveat) if caveat else ""
    rows = [("Information status", fact_badge(status, verified_at))]
    if published_at:
        rows.append(("Published", time_tag(published_at)))
    rows.append(("Last verified", time_tag(verified_at) if verified_at else "Not yet verified against official sources"))
    if reviewed_at:
        rows.append(("Last reviewed", time_tag(reviewed_at)))
    src = sources_list_html(list(source_ids))
    if src:
        rows.append(("Sources to check", src))
    return """<aside class="verify-block" aria-labelledby="verify-h">
  <h2 id="verify-h">%s</h2>
  %s
  %s
  %s
</aside>""" % (esc(heading), meta_dl(rows), caveat_html, history_html(path))
