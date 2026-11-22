"""Answer-engine (AEO) building blocks shared by every generator.

Reusable components (HTML) and JSON-LD builders, so a guide's answer box, facts
table, citations, byline, schema and monetization labels are produced by one piece
of code instead of being hand-pasted per page:

  quick_answer()      the 40-60 word direct answer that opens every guide
  key_facts()         a small facts table; each row carries its own status and source
  claim()             an inline per-claim status ("Verified 12 Nov 2026 against X")
  source_list()       citations grouped by the claims they support
  byline()            "By <author> · Updated · Verified" strip, driven by front-matter
  sponsored_label()   the visible SPONSORED tag
  affiliate_link()    a booking link: configurable params, rel="sponsored nofollow noopener"
  signup_block()      the "Kumbh 2027 updates" block (provider via env, contact-form fallback)

JSON-LD builders return plain dicts for pagekit.render(jsonld=[...]).
"""
import json
import os
import re
from urllib.parse import urlparse

from . import store
from .paths import DATA, SITE
from .render import esc, ext_link, fmt_date, sources_index, time_tag

ORG_ID = SITE + "/#organization"
WEBSITE_ID = SITE + "/#website"


def seo():
    with open(os.path.join(DATA, "seo.json"), encoding="utf-8") as fh:
        return json.load(fh)


def money():
    with open(os.path.join(DATA, "monetization.json"), encoding="utf-8") as fh:
        return json.load(fh)


def author():
    return seo()["author"]


def author_id():
    """Articles are credited to the site's Organization; there is no personal author."""
    return ORG_ID


# ── JSON-LD ──────────────────────────────────────────────────────────────────
def organization_ld():
    cfg = seo()["organization"]
    d = {"@type": "Organization", "@id": ORG_ID, "name": cfg["name"], "url": SITE + "/",
         "logo": {"@type": "ImageObject", "url": SITE + "/logo-purple.png", "width": 512, "height": 512},
         "description": "An independent travel and information guide to Nashik, Maharashtra. Not affiliated with any government body or official tourism authority.",
         "publishingPrinciples": SITE + cfg["publishingPrinciples"],
         "areaServed": {"@type": "Place", "name": "Nashik, Maharashtra, India"}}
    if cfg.get("sameAs"):
        d["sameAs"] = cfg["sameAs"]
    return d


def website_ld():
    return {"@type": "WebSite", "@id": WEBSITE_ID, "url": SITE + "/", "name": "Nashik Tourism",
            "description": "An independent, continuously verified guide to Nashik, Maharashtra: temples, vineyards, the Simhastha Kumbh Mela, transport, accessibility and events.",
            "publisher": {"@id": ORG_ID}, "inLanguage": "en-IN",
            "potentialAction": {"@type": "SearchAction",
                                "target": {"@type": "EntryPoint", "urlTemplate": SITE + "/search/?q={search_term_string}"},
                                "query-input": "required name=search_term_string"}}


def article_ld(path, headline, description, published, modified, image=None, kind="Article", about=None):
    d = {"@type": kind, "@id": SITE + path + "#article", "headline": headline[:110], "description": description,
         "datePublished": published, "dateModified": modified or published,
         "author": {"@type": "Organization", "@id": ORG_ID, "name": author()["name"], "url": SITE + "/"},
         "publisher": {"@id": ORG_ID},
         "mainEntityOfPage": {"@type": "WebPage", "@id": SITE + path},
         "isPartOf": {"@id": WEBSITE_ID}, "inLanguage": "en-IN"}
    if image:
        d["image"] = image
    if about:
        d["about"] = about
    return d


def faq_ld(pairs, path=None):
    """pairs: [(question_text, answer_text)] — must mirror the visible FAQ exactly."""
    d = {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}
    if path:
        d["@id"] = SITE + path + "#faq"
    return d


def plain(html):
    import html as h
    t = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", h.unescape(t)).strip()


def extract_faq(html):
    """Parse a visible FAQ (an h2 containing 'Frequently asked' or 'FAQ' followed by
    h3 question / paragraph answer pairs) so the schema is built from what the reader sees."""
    m = re.search(r"<h2[^>]*>[^<]*(?:Frequently asked|FAQ|Common questions)[^<]*</h2>(.*?)(?=<h2|<!-- BEGIN:NT-VERIFY|</article>)", html, re.S | re.I)
    if not m:
        return []
    pairs = []
    for q, rest in re.findall(r"<h3[^>]*>(.*?)</h3>(.*?)(?=<h3|$)", m.group(1), re.S):
        a = plain(re.sub(r"<(script|style).*?</\1>", "", rest, flags=re.S))
        q = plain(q)
        if q and a:
            pairs.append((q, a))
    return pairs


# ── Components ───────────────────────────────────────────────────────────────
def quick_answer(html_text, label="Quick answer"):
    """The 40-60 word direct answer. Words are counted on the visible text; the
    build warns (tools/seo-check.py) when a guide's answer falls outside 40-60."""
    return ('<!-- BEGIN:NT-QA -->\n<div class="quick-answer" data-quick-answer>\n  <p class="qa-label">%s</p>\n  <p class="qa-text">%s</p>\n</div>\n<!-- END:NT-QA -->'
            % (esc(label), html_text))


def word_count(html_text):
    return len(plain(html_text).split())


STATUS_WORD = {"verified": "Verified", "reported": "Reported, not confirmed",
               "disputed": "Sources differ", "not_verified": "Not yet verified"}


def claim(status, source_name=None, source_url=None, date=None, short=False):
    """Per-claim status chip. Verified: 'Verified <date> against <source>'.
    Anything else keeps its honest label."""
    from .render import badge, FACT_BADGES
    glyph, _ = FACT_BADGES[status]
    if status == "verified" and date:
        txt = "Verified %s" % fmt_date(date, short=True)
        if source_name and not short:
            txt += " against " + source_name
    else:
        txt = STATUS_WORD[status]
        if date and not short:
            txt += ", checked %s" % fmt_date(date, short=True)
    return '<span class="st st-fact st-%s"><span class="st-i" aria-hidden="true">%s</span>%s</span>' % (esc(status), glyph, esc(txt))


def key_facts(rows, caption="Key facts", cls=""):
    """rows: [{label, value (html), status, source: (name, url) | None, date}]"""
    body = []
    for r in rows:
        src = ""
        if r.get("source"):
            n, u = r["source"]
            src = ext_link(u, esc(n), item="keyfact") if u else esc(n)
        body.append('<tr><th scope="row">%s</th><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            esc(r["label"]), r["value"], claim(r.get("status", "not_verified"), None, None, r.get("date"), short=True),
            src or '<span class="muted">No source linked yet</span>'))
    return ('<div class="table-scroll" tabindex="0" role="region" aria-label="%s">'
            '<table class="key-facts %s"><caption>%s</caption><thead><tr><th scope="col">Fact</th><th scope="col">Answer</th>'
            '<th scope="col">Status</th><th scope="col">Source</th></tr></thead><tbody>%s</tbody></table></div>'
            % (esc("Table: " + caption), esc(cls), esc(caption), "".join(body)))


def source_list(groups, heading="Sources, by claim", hid="sources-by-claim"):
    """groups: [(claim text, [source id | (name, url)])]. Each citation is tied to the
    claim it supports; source ids resolve through data/sources.json."""
    reg = sources_index()
    items = []
    for text, srcs in groups:
        links = []
        for s in srcs:
            if isinstance(s, str):
                src = reg.get(s)
                if not src:
                    raise KeyError("unknown source id %r in source_list" % s)
                links.append(ext_link(src["url"], esc(src["name"]), item=s) if src.get("url") else esc(src["name"]))
            else:
                links.append(ext_link(s[1], esc(s[0]), item="cited") if s[1] else esc(s[0]))
        items.append("<li><span class=\"sl-claim\">%s</span> <span class=\"sl-src\">%s</span></li>" % (text, "; ".join(links)))
    return '<section class="source-list" aria-labelledby="%s"><h2 id="%s">%s</h2><ul>%s</ul></section>' % (hid, hid, esc(heading), "".join(items))


def byline(updated, verified=None, published=None):
    a = author()
    ver = ("Verified <time datetime=\"%s\">%s</time>" % (esc(verified), esc(fmt_date(verified, short=True)))) if verified \
        else "Not yet verified against official sources"
    pub = (' &middot; Published <time datetime="%s">%s</time>' % (esc(published), esc(fmt_date(published, short=True)))) if published else ""
    return ('<!-- BEGIN:NT-BYLINE -->\n<p class="byline" data-byline>By <a href="%s" rel="author">%s</a>'
            ' &middot; Last updated <time datetime="%s">%s</time>%s &middot; Last verified: %s</p>\n<!-- END:NT-BYLINE -->'
            % (esc(a["path"]), esc(a["byline"]), esc(updated), esc(fmt_date(updated, short=True)), pub, ver))


def sponsored_label(text="Sponsored"):
    return '<span class="sponsored-label" data-sponsored>%s</span>' % esc(text)


def sponsored_block(inner_html, sponsor_name):
    """A labelled sponsored section. Never carries a Verified status (seo-check fails the build if
    a sponsored block contains one), and its outbound links must use rel="sponsored nofollow"."""
    return ('<aside class="sponsored-block" data-sponsored aria-label="Sponsored content">%s %s'
            '<div class="sb-body">%s</div>'
            '<p class="sb-note">Sponsored by %s. The sponsor does not control our facts, and this content is not marked Verified. '
            '<a href="/editorial-policy/#sponsored">How sponsored content works</a>.</p></aside>'
            % (sponsored_label(), "", inner_html, esc(sponsor_name)))


def _affiliate_params(host):
    for key, p in money()["affiliates"]["partners"].items():
        if any(host == h or host.endswith("." + h) for h in p["hosts"]):
            return os.environ.get(p["env"], "").strip().lstrip("?&")
    return None


def affiliate_link(url, text, cls="", track="accommodation_click"):
    """Outbound booking link. Affiliate params come from the environment (see
    data/monetization.json); unset means the plain URL. Always rel sponsored nofollow noopener."""
    host = (urlparse(url).hostname or "").replace("www.", "")
    params = _affiliate_params(host)
    if params:
        url += ("&" if "?" in url else "?") + params
    attrs = ' href="%s" target="_blank" rel="noopener sponsored nofollow" data-track="%s"' % (esc(url), esc(track))
    if cls:
        attrs += ' class="%s"' % esc(cls)
    return "<a%s>%s</a>" % (attrs, text)


def signup_block(topic="kumbh-2027"):
    cfg = money()["signup"]
    action = os.environ.get("NT_SIGNUP_FORM_ACTION", "").strip()
    wa = os.environ.get("NT_WHATSAPP_CHANNEL_URL", "").strip()
    parts = []
    if action:
        parts.append('<form class="signup-form" action="%s" method="post" data-track="signup_submit">'
                     '<label for="su-%s">Email address</label><div class="signup-row">'
                     '<input id="su-%s" name="email" type="email" required autocomplete="email" />'
                     '<button class="btn btn-purple" type="submit">Subscribe</button></div></form>' % (esc(action), esc(topic), esc(topic)))
    if wa:
        parts.append('<a class="btn btn-outline" href="%s" rel="noopener" data-track="signup_whatsapp">Follow on WhatsApp</a>' % esc(wa))
    if not parts:
        parts.append('<a class="btn btn-purple" href="%s" data-track="signup_contact">Ask to be updated</a>' % esc(cfg["fallbackHref"]))
    return ('<aside class="signup-block" aria-labelledby="su-h-%s"><h2 id="su-h-%s">%s</h2><p>%s</p>%s</aside>'
            % (esc(topic), esc(topic), esc(cfg["heading"]), esc(cfg["text"]), "".join(parts)))


def bing_meta():
    code = os.environ.get(seo()["bing"]["verificationEnvVar"], "").strip()
    return '<meta name="msvalidate.01" content="%s" />' % esc(code) if code else ""


def analytics_head():
    """Cookieless analytics, only when configured through the environment."""
    cfg = money()["analytics"]
    out = []
    dom = os.environ.get(cfg["plausibleDomainEnv"], "").strip()
    tok = os.environ.get(cfg["cloudflareBeaconEnv"], "").strip()
    if dom:
        out.append('<script defer data-domain="%s" src="https://plausible.io/js/script.js"></script>' % esc(dom))
    if tok:
        out.append('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token": "%s"}\'></script>' % esc(tok))
    return "\n".join(out)


# ── Front-matter dates ───────────────────────────────────────────────────────
def modified_for(path, meta=None):
    """dateModified / 'Last updated': the newest of the page's front-matter dates and its
    change-log entries. One definition, so the visible date and the schema cannot disagree."""
    if meta is None:
        meta = store.load("pages")["pages"].get(path, {})
    dates = [meta.get("lastUpdated"), meta.get("lastVerified"), meta.get("lastReviewed"), meta.get("published")]
    dates += [e["date"] for e in store.load("changelog")["entries"] if e["path"].split("#")[0] == path]
    dates = [str(d)[:10] for d in dates if d]
    return max(dates) if dates else None
