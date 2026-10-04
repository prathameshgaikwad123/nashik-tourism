#!/usr/bin/env python3
"""
SEO, structured-data and link audit for the built site. No network.

    python3 tools/seo-check.py            # report; exit 1 on errors
    python3 tools/seo-check.py --json reports/seo.json

Errors (fail):
  missing/duplicate <title>, missing/duplicate meta description, missing or wrong
  canonical, accidental noindex on an indexable page, an indexable page missing
  from sitemap.xml (or a noindex/missing page IN it), invalid JSON-LD, broken
  breadcrumb, missing Open Graph / Twitter tags, anything other than exactly one
  <h1>, broken internal links and broken #anchors, images without alt/size.
Warnings: heading-level skips, orphan pages (no inbound link), title/description
length, links to pages carrying noindex.
"""
import json
import os
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nt.paths import ROOT, SITE, REPORTS  # noqa: E402

SKIP_FILES = {"nav-template.html"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.meta = {}
        self.canonical = []
        self.headings = []
        self.ids = set()
        self.links = []
        self.imgs = []
        self.jsonld = []
        self._ld = None
        self._h = None
        self.lang = None
        self.has_main = 0
        self.has_skip = False
        self.in_head = True

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
            self.title = ""
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key.lower()] = a.get("content", "")
        elif tag == "link" and "canonical" in (a.get("rel") or "").split():
            self.canonical.append(a.get("href"))
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._ld = ""
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._h = [int(tag[1]), ""]
        elif tag == "a" and a.get("href") is not None:
            self.links.append(a["href"])
            if a.get("href") == "#main" and "skip-link" in (a.get("class") or ""):
                self.has_skip = True
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "main":
            self.has_main += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._ld is not None:
            self.jsonld.append(self._ld)
            self._ld = None
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._h:
            self.headings.append((self._h[0], re.sub(r"\s+", " ", self._h[1]).strip()))
            self._h = None

    def handle_data(self, data):
        if self._in_title and self.title is not None:
            self.title += data
        if self._ld is not None:
            self._ld += data
        if self._h is not None:
            self._h[1] += data


def page_url(full):
    rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel


def load_sitemap():
    p = os.path.join(ROOT, "sitemap.xml")
    return set(re.findall(r"<loc>%s(.*?)</loc>" % re.escape(SITE), open(p, encoding="utf-8").read()))


def main():
    pages, errors, warnings = {}, [], []
    for dirpath, _d, files in os.walk(ROOT):
        for n in files:
            if n.endswith(".html") and n not in SKIP_FILES:
                full = os.path.join(dirpath, n)
                p = Page()
                p.feed(open(full, encoding="utf-8").read())
                pages[page_url(full)] = p

    def err(path, msg):
        errors.append("%s: %s" % (path, msg))

    def warn(path, msg):
        warnings.append("%s: %s" % (path, msg))

    sitemap = load_sitemap()
    titles, descs = defaultdict(list), defaultdict(list)
    inbound = defaultdict(set)
    indexable = set()
    for path, p in sorted(pages.items()):
        robots = p.meta.get("robots", "")
        noindex = "noindex" in robots
        if not noindex:
            indexable.add(path)
        if not p.title or not p.title.strip():
            err(path, "missing <title>")
        else:
            titles[p.title.strip()].append(path)
            if len(p.title) > 70:
                warn(path, "title is %d chars (>70)" % len(p.title))
        d = p.meta.get("description")
        if not d:
            err(path, "missing meta description")
        else:
            descs[d.strip()].append(path)
            if len(d) > 170 or len(d) < 50:
                warn(path, "meta description is %d chars" % len(d))
        if path != "/404.html":
            want = SITE + path
            if len(p.canonical) != 1:
                err(path, "expected exactly one canonical, found %d" % len(p.canonical))
            elif p.canonical[0] != want:
                err(path, "canonical %s != %s" % (p.canonical[0], want))
        for k in ("og:title", "og:description", "og:url", "og:image", "twitter:card"):
            if not p.meta.get(k):
                err(path, "missing " + k)
        if p.lang != "en":
            err(path, "html lang is %r" % p.lang)
        if "viewport" not in p.meta:
            err(path, "missing viewport meta")
        if not p.has_skip:
            err(path, "missing skip link")
        if p.has_main != 1:
            err(path, "expected one <main>, found %d" % p.has_main)
        h1 = [h for h in p.headings if h[0] == 1]
        if len(h1) != 1:
            err(path, "expected exactly one <h1>, found %d" % len(h1))
        prev = 0
        for lvl, text in p.headings:
            if prev and lvl > prev + 1:
                warn(path, "heading level jumps h%d -> h%d (%s)" % (prev, lvl, text[:40]))
                break
            prev = lvl
        for raw in p.jsonld:
            try:
                data = json.loads(raw)
            except ValueError as e:
                err(path, "invalid JSON-LD: %s" % e)
                continue
            for node in (data.get("@graph") or [data]):
                if node.get("@type") == "BreadcrumbList":
                    items = node.get("itemListElement", [])
                    if [i["position"] for i in items] != list(range(1, len(items) + 1)):
                        err(path, "breadcrumb positions are not sequential")
                    if items and items[-1]["item"].rstrip("/") != (SITE + path).rstrip("/") and path != "/404.html":
                        warn(path, "last breadcrumb item is not this page")
        for im in p.imgs:
            src = im.get("src", "")
            if im.get("alt") is None:
                err(path, "img without alt: %s" % src[:60])
            if "width" not in im or "height" not in im:
                err(path, "img without width/height: %s" % src[:60])
        if noindex and path in sitemap:
            err(path, "noindex page listed in sitemap.xml")

    for t, ps in titles.items():
        if len(ps) > 1:
            for path in ps:
                if path != "/404.html":
                    err(path, "duplicate title shared with %s" % ", ".join(x for x in ps if x != path))
    for dsc, ps in descs.items():
        if len(ps) > 1:
            for path in ps:
                if path != "/404.html":
                    err(path, "duplicate description shared with %s" % ", ".join(x for x in ps if x != path))

    for path in sorted(indexable - {"/404.html"}):
        if path not in sitemap:
            err(path, "indexable page missing from sitemap.xml")
    for u in sorted(sitemap):
        if u not in pages:
            err(u, "listed in sitemap.xml but no such page")

    # Internal links and anchors.
    static_files = set()
    for dirpath, _d, files in os.walk(ROOT):
        for n in files:
            if not n.endswith(".html"):
                static_files.add("/" + os.path.relpath(os.path.join(dirpath, n), ROOT).replace(os.sep, "/"))
    for path, p in sorted(pages.items()):
        for href in p.links:
            if not href or href.startswith(("mailto:", "tel:", "javascript:", "data:")):
                continue
            u = urlparse(href)
            if u.scheme in ("http", "https"):
                if u.netloc.replace("www.", "") != "nashiktourism.com":
                    continue
                target, frag = u.path or "/", u.fragment
            elif u.netloc:
                continue
            else:
                if href.startswith("#"):
                    target, frag = path, href[1:]
                else:
                    target, frag = unquote(u.path) or path, u.fragment
                    if not target.startswith("/"):
                        base = path if path.endswith("/") else os.path.dirname(path) + "/"
                        target = os.path.normpath(base + target).replace(os.sep, "/")
                        if not target.endswith("/") and "." not in os.path.basename(target):
                            target += "/"
            if target in static_files:
                continue
            if target not in pages:
                if target + "/" in pages:
                    warn(path, "link %s lacks trailing slash (redirect hop)" % href)
                    target += "/"
                else:
                    err(path, "broken internal link %s" % href)
                    continue
            if target != path:
                inbound[target].add(path)
            if frag and frag not in pages[target].ids and frag != "top":
                err(path, "broken anchor %s (no id=%r on %s)" % (href, frag, target))
            if target in pages and "noindex" in pages[target].meta.get("robots", "") and target not in ("/search/",):
                warn(path, "links to noindex page %s" % target)
    for path in sorted(indexable - {"/", "/404.html"}):
        if not inbound[path]:
            warn(path, "orphan: no internal link points here")

    print("pages: %d (%d indexable); sitemap URLs: %d" % (len(pages), len(indexable), len(sitemap)))
    for w in warnings:
        print("  warn  " + w)
    for e in errors:
        print("  ERROR " + e)
    print("\nseo-check: %d error(s), %d warning(s)" % (len(errors), len(warnings)))
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        json.dump({"errors": errors, "warnings": warnings, "pages": len(pages)}, open(out, "w"), indent=2)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
