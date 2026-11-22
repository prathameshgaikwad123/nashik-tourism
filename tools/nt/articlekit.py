"""Layout for the generated guides (distance hub, transport pages, Bhandardara...).

Produces the same article layout the hand-written guides use (.article-wrap,
.article-body, .sidebar) under the compact page head, with the answer-engine
pieces wired in the same order on every page:

    quick answer -> status notice (apply-verification) -> body -> sources by claim -> verify block

JSON-LD (Article with a Person author, BreadcrumbList, FAQPage mirrored from the visible
FAQ, plus any page-specific nodes) is generated here from the same data that renders the page.
"""
import re

from . import aeo, pagekit, store
from .paths import SITE
from .render import esc


def faq_html(pairs, heading="Frequently asked questions", hid="faq"):
    """pairs: [(question_text, answer_html)]. The schema is built from the same pairs."""
    items = "".join("<h3>%s</h3>\n    <p>%s</p>" % (esc(q), a) for q, a in pairs)
    return '<h2 id="%s">%s</h2>\n    %s' % (hid, esc(heading), items)


def sidebar(*cards):
    return '<aside class="sidebar">\n%s\n  </aside>' % "\n".join(cards)


def side_card(title, inner):
    return '<div class="sidebar-card"><h3>%s</h3>%s</div>' % (esc(title), inner)


def side_links(title, links):
    return side_card(title, '<ul class="toc-list">%s</ul>' % "".join('<li><a href="%s">%s</a></li>' % (esc(h), t) for h, t in links))


def build(path, *, title, h1, lede, description, crumbs, body, side="", faq=None, quick=None,
          published, topic_label=None, extra_ld=None, image=None, article_kind="Article", about=None,
          modified=None, css=""):
    """Render and write one guide. `body` is the article HTML after the quick answer."""
    meta = store.load("pages")["pages"].get(path)
    if meta is None:
        raise SystemExit("ERROR: %s must be registered in data/pages.json before it can be built" % path)
    modified = modified or aeo.modified_for(path, meta)
    qa = aeo.quick_answer(quick) if quick else ""
    n = aeo.word_count(quick) if quick else 0
    if quick and not 40 <= n <= 60:
        raise SystemExit("ERROR: %s quick answer is %d words (must be 40-60)" % (path, n))
    by = aeo.byline(modified, meta.get("lastVerified"), published)
    head = pagekit.page_head(h1, lede, crumbs=crumbs, eyebrow=topic_label, extra=by)
    faq_block = faq_html(faq) if faq else ""
    article = """<div class="article-wrap">
  <article class="article-body" data-reading-body>
%s
%s
%s
  </article>
  %s
</div>""" % (qa, body, faq_block, side)
    ld = [aeo.article_ld(path, h1, description, published, modified, image or pagekit.OG_DEFAULT, kind=article_kind, about=about)]
    if faq:
        ld.append(aeo.faq_ld([(q, aeo.plain(a)) for q, a in faq], path))
    ld += (extra_ld or []) + [aeo.person_ld(), aeo.organization_ld()]
    html = pagekit.render(path, title, description, head + "\n" + article, crumbs=crumbs, jsonld=ld, css=css, raw_title=True,
                          page_type="WebPage", modified=modified, published=published, og_image=image)
    html = html.replace('<meta property="og:type" content="website" />', '<meta property="og:type" content="article" />', 1)
    pagekit.write(path, html)
    return html


def crumbs_for(label, parent=("Guides", "/blog/")):
    c = [("Home", "/")]
    if parent:
        c.append(parent)
    c.append((label, None))
    return c
