"""Polite, bounded HTTP for the source monitor (standard library only).

  * identifies itself, honours robots.txt, one request per host every 2 seconds
  * hard limits on time and size so a hostile or broken page cannot hang a run
  * returns (status, text) and never raises for network problems — a source being
    down is data (see data/state/source-state.json), not a crashed pipeline
"""
import re
import time
import urllib.error
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from urllib.parse import urlparse

UA = "NashikTourismMonitor/1.0 (+https://nashiktourism.com/editorial-policy/)"
MAX_BYTES = 2_000_000
TIMEOUT = 20
MIN_GAP = 2.0

_last_hit = {}
_robots = {}


def _wait(host):
    gap = time.time() - _last_hit.get(host, 0)
    if gap < MIN_GAP:
        time.sleep(MIN_GAP - gap)
    _last_hit[host] = time.time()


def allowed(url):
    p = urlparse(url)
    host = p.netloc
    if host not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        try:
            _wait(host)
            req = urllib.request.Request("%s://%s/robots.txt" % (p.scheme, host), headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                rp.parse(r.read(200_000).decode("utf-8", "replace").splitlines())
        except (urllib.error.URLError, OSError, ValueError):
            rp = None  # no robots.txt reachable: allowed
        _robots[host] = rp
    rp = _robots[host]
    return True if rp is None else rp.can_fetch(UA, url)


def fetch(url):
    """-> (status_code or None, body_text, error_message or None)"""
    if not allowed(url):
        return None, "", "disallowed by robots.txt"
    host = urlparse(url).netloc
    _wait(host)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.5"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                return r.status, "", "response larger than %d bytes" % MAX_BYTES
            charset = r.headers.get_content_charset() or "utf-8"
            return r.status, raw.decode(charset, "replace"), None
    except urllib.error.HTTPError as e:
        return e.code, "", "HTTP %d" % e.code
    except (urllib.error.URLError, OSError, ValueError) as e:
        return None, "", str(getattr(e, "reason", e))[:120]


class _Text(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form", "iframe"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in ("p", "div", "li", "tr", "h1", "h2", "h3", "h4", "br", "section", "article"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag in ("p", "div", "li", "tr", "h1", "h2", "h3", "h4", "section", "article"):
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def visible_text(html):
    """Readable lines of a page, with chrome stripped, for change detection."""
    p = _Text()
    try:
        p.feed(html)
    except Exception:
        return re.sub(r"<[^>]+>", " ", html)
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in "".join(p.out).splitlines()]
    return "\n".join(ln for ln in lines if len(ln) > 2)
