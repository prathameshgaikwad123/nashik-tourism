#!/usr/bin/env python3
"""
Give the long guides in-page navigation and a reading-progress indicator.

The sidebar card the posts already carry is called .toc-list, but it is a list
of links to OTHER guides — there is no table of contents anywhere, and none of
the article <h2> headings carry an id, so nothing on a 3,000-word page can be
linked to or jumped to.

This script is purely additive:
  * slugified ids on each article <h2> that lacks one (existing ids are kept, so
    /kumbh-mela-2027/#dates and friends keep working)
  * an "On this page" card at the top of the sidebar, marked data-section-nav so
    /site.js highlights the section you are reading
  * a reading-progress bar, driven by one passive scroll listener and a single
    CSS custom property

It never rewrites prose, and it is idempotent: running it twice changes nothing.
Articles with fewer than three headings are skipped — a two-item contents list
is clutter, not navigation.

Usage:  python3 tools/build-article-nav.py [--check]
"""
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "nashiktourism"))
MIN_HEADINGS = 3

H2_RE = re.compile(r"<h2(?P<attrs>[^>]*)>(?P<text>.*?)</h2>", re.S)
BODY_RE = re.compile(r'<article class="article-body"(?P<attrs>[^>]*)>', re.S)
SIDEBAR_RE = re.compile(r'<aside class="sidebar"[^>]*>')
MAIN_RE = re.compile(r'<main id="main"[^>]*>')


def slug(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = (text.replace("&amp;", "and").replace("&mdash;", " ").replace("&ndash;", " ")
                .replace("&#8377;", "rs").replace("&rsquo;", "").replace("&nbsp;", " "))
    text = re.sub(r"[^\w\s-]", "", text, flags=re.U).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-")[:60] or "section"


def label(text):
    """Sidebar labels: strip markup and keep them scannable."""
    text = re.sub(r"<[^>]+>", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    if len(text) > 46:
        text = text[:44].rsplit(" ", 1)[0] + "&hellip;"
    return text


def process(html):
    if "data-section-nav" in html:
        return html, None  # already done

    body = BODY_RE.search(html)
    sidebar = SIDEBAR_RE.search(html)
    main = MAIN_RE.search(html)
    if not (body and sidebar and main):
        return html, None

    # Only headings inside the article body, not the sidebar or the footer.
    start = body.end()
    end = html.index("</article>", start)
    article = html[start:end]

    seen = {}
    entries = []

    def add_id(m):
        attrs, text = m.group("attrs"), m.group("text")
        existing = re.search(r'\bid="([^"]+)"', attrs)
        if existing:
            ident = existing.group(1)
            new_attrs = attrs
        else:
            base = slug(text)
            seen[base] = seen.get(base, 0) + 1
            ident = base if seen[base] == 1 else "%s-%d" % (base, seen[base])
            new_attrs = ' id="%s"%s' % (ident, attrs)
        entries.append((ident, label(text)))
        return "<h2%s>%s</h2>" % (new_attrs, text)

    article = H2_RE.sub(add_id, article)
    if len(entries) < MIN_HEADINGS:
        return html, None

    html = html[:start] + article + html[end:]

    # Re-find the sidebar: the article rewrite shifted everything after it.
    sidebar = SIDEBAR_RE.search(html)
    toc = "\n".join('          <li><a href="#%s">%s</a></li>' % (i, t) for i, t in entries)
    card = """
      <div class="sidebar-card toc-card">
        <h3 id="on-this-page">On this page</h3>
        <nav aria-labelledby="on-this-page" data-section-nav>
          <ul class="toc-list">
%s
          </ul>
        </nav>
      </div>
""" % toc
    html = html[:sidebar.end()] + card + html[sidebar.end():]

    # Reading progress: one element, one CSS variable, one passive listener.
    main = MAIN_RE.search(html)
    bar = ('\n<div class="read-progress" data-reading-progress role="progressbar"'
           ' aria-label="Article reading progress" aria-valuemin="0" aria-valuemax="100"'
           ' aria-valuenow="0"><span></span></div>')
    html = html[:main.end()] + bar + html[main.end():]
    html = BODY_RE.sub(lambda m: '<article class="article-body"%s data-reading-body>' % m.group("attrs"),
                       html, count=1)
    return html, len(entries)


def main():
    check = "--check" in sys.argv
    done = 0
    for dirpath, _dirs, files in os.walk(os.path.join(ROOT, "blog")):
        if "index.html" not in files:
            continue
        full = os.path.join(dirpath, "index.html")
        if os.path.dirname(full) == os.path.join(ROOT, "blog"):
            continue  # the guide index itself is not an article
        with open(full, encoding="utf-8") as fh:
            before = fh.read()
        after, n = process(before)
        if n is None:
            continue
        done += 1
        print("  %-56s %2d headings" % (os.path.relpath(full, ROOT), n))
        if not check:
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(after)
    print("%s %d article(s)" % ("would update" if check else "updated", done))


if __name__ == "__main__":
    main()
