#!/usr/bin/env python3
"""
Generate /blog/ as static HTML.

WHY THIS EXISTS
---------------
The guide index used to fetch posts.json in the browser and build its cards
with a template literal. Measured with JavaScript disabled, the served page
contained 23 words, one internal link and a hidden "No articles found" block:
every one of the 22 articles, the whole category taxonomy and all the internal
linking existed only after script execution. Six posts had no inbound link
anywhere in static HTML as a direct result.

This script renders the same data — from the same posts.json — into the page at
build time. /site.js then filters the rendered cards in place rather than
creating them, so the interactive behaviour survives and the content no longer
depends on it.

Also fixed here, because they were properties of the generated markup:
  * every card image now carries width/height and a Cloudinary delivery
    transform (22 images previously had neither, and shipped as originals)
  * the page had the Kumbh guide's <title> and a doubled meta description
  * the category chips used --saffron (3.39:1) and #16a34a (2.5:1) for small
    text; they now use the AA-compliant tokens
  * the filter controls were 29 px tall with no aria-pressed and no live region

Usage:  python3 tools/build-blog.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chrome  # noqa: E402
import posts as P  # noqa: E402

SITE = "https://nashiktourism.com"
OUT = os.path.join(P.ROOT, "blog", "index.html")

TITLE = "Nashik Travel Guides &amp; Kumbh Mela 2027 Articles"
META = ("Every guide on NashikTourism.com in one place: Kumbh Mela 2027, getting to "
        "Nashik, where to stay, what it costs, the best time to visit, and the "
        "temples, caves and vineyards worth your time.")

CSS = """    .blog-hero { background: var(--dark); padding: 8rem var(--gutter) 3.5rem; }
    .blog-hero h1 { font-family:var(--font-display); font-size:var(--t-h1); font-weight:900; color:#fff; letter-spacing:var(--ls-display); line-height:1.08; margin:0.4rem 0 0.9rem; }
    .blog-hero .lede { color:var(--on-dark); font-size:1.05rem; line-height:var(--lh-body); max-width:620px; }

    /* Featured guide — one editorial moment, not another card in the grid */
    .feature { display:grid; grid-template-columns:1.15fr 1fr; gap:0; background:var(--white); border:1px solid var(--border); border-radius:var(--r-lg); overflow:hidden; max-width:var(--wrap); margin:0 auto; }
    .feature-img { position:relative; background:var(--light); }
    .feature-img img { width:100%; height:100%; object-fit:cover; }
    .feature-body { padding:var(--s-10); display:flex; flex-direction:column; justify-content:center; }
    .feature-body h2 { font-family:var(--font-display); font-size:clamp(1.3rem,2.4vw,1.9rem); font-weight:800; line-height:1.25; letter-spacing:var(--ls-heading); margin:var(--s-3) 0 var(--s-3); }
    .feature-body p { color:var(--muted); line-height:var(--lh-body); font-size:var(--t-small); }

    /* Filter + search bar */
    .guide-bar { background:var(--cream); border-bottom:1px solid var(--border); position:sticky; top:var(--nav-h); z-index:var(--z-sticky); }
    .guide-bar-inner { max-width:var(--wrap); margin:0 auto; padding:var(--s-3) var(--gutter); display:flex; align-items:center; gap:var(--s-3); flex-wrap:wrap; }
    .chips { display:flex; gap:var(--s-2); overflow-x:auto; scrollbar-width:none; -webkit-overflow-scrolling:touch; flex:1 1 auto; }
    .chips::-webkit-scrollbar { display:none; }
    .chip { display:inline-flex; align-items:center; gap:0.3rem; white-space:nowrap; min-height:var(--tap); padding:0 var(--s-4); border:1.5px solid var(--border-strong); border-radius:var(--r-pill); background:var(--white); color:var(--muted); font-family:var(--font-display); font-size:var(--t-eyebrow); font-weight:700; letter-spacing:0.06em; text-transform:uppercase; cursor:pointer; transition:background var(--dur) var(--ease), color var(--dur) var(--ease), border-color var(--dur) var(--ease); }
    .chip:hover { border-color:var(--primary); color:var(--primary); }
    .chip[aria-pressed="true"] { background:var(--primary); border-color:var(--primary); color:#fff; }
    .chip .n { font-size:0.65rem; opacity:0.75; font-weight:600; }
    .guide-search { position:relative; flex:0 1 260px; }
    .guide-search input { width:100%; min-height:var(--tap); padding:0 var(--s-4) 0 2.4rem; border:1.5px solid var(--border-strong); border-radius:var(--r-pill); background:var(--white); font-family:var(--font-display); font-size:var(--t-meta); color:var(--ink); }
    .guide-search input:focus { border-color:var(--primary); }
    .guide-search svg { position:absolute; left:0.9rem; top:50%; transform:translateY(-50%); pointer-events:none; color:var(--muted); }

    /* Grid */
    .guides { max-width:var(--wrap); margin:0 auto; padding:var(--s-12) var(--gutter) var(--s-20); }
    .guide-group { margin-bottom:var(--s-16); scroll-margin-top:calc(var(--nav-h) + 72px); }
    .guide-group > h2 { font-family:var(--font-display); font-size:1.35rem; font-weight:800; letter-spacing:var(--ls-heading); color:var(--ink); padding-bottom:var(--s-3); border-bottom:2px solid var(--border); margin-bottom:var(--s-2); }
    .guide-group > p.gg-sub { color:var(--muted); font-size:var(--t-small); margin-bottom:var(--s-6); max-width:60ch; }
    .guide-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(290px,1fr)); gap:var(--s-6); }

    .gcard { display:flex; flex-direction:column; background:var(--white); border:1px solid var(--border); border-radius:var(--r-lg); overflow:hidden; transition:transform var(--dur) var(--ease), box-shadow var(--dur) var(--ease); }
    .gcard:hover { transform:translateY(-4px); box-shadow:var(--sh-3); }
    .gcard-img { background:var(--light); overflow:hidden; }
    .gcard-img img { width:100%; height:186px; object-fit:cover; transition:transform var(--dur-slow) var(--ease); }
    .gcard:hover .gcard-img img { transform:scale(1.05); }
    .gcard-body { padding:var(--s-5); display:flex; flex-direction:column; flex:1 1 auto; }
    .gcard h3 { font-family:var(--font-display); font-size:1rem; font-weight:800; line-height:1.38; letter-spacing:-0.01em; color:var(--ink); margin-bottom:var(--s-2); }
    .gcard p { font-size:var(--t-small); color:var(--muted); line-height:1.6; flex:1 1 auto; }

    .gmeta { display:flex; align-items:center; gap:var(--s-2); flex-wrap:wrap; font-family:var(--font-display); font-size:0.68rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:var(--muted-strong); margin-bottom:var(--s-3); }
    .bcat { border-radius:var(--r-pill); padding:0.2rem 0.6rem; }
    .cat-kumbh   { background:rgba(169,70,17,0.10);  color:var(--saffron-deep); }
    .cat-travel  { background:rgba(45,27,105,0.09);  color:var(--primary); }
    .cat-hotels  { background:rgba(15,105,72,0.11);  color:var(--vine); }
    .cat-planning{ background:rgba(127,92,24,0.13);  color:var(--gold-deep); }
    .cat-nashik  { background:rgba(90,81,64,0.12);   color:var(--stone-ink); }
    .cat-intl    { background:rgba(45,27,105,0.09);  color:var(--primary); }
    .cat-default { background:var(--light); color:var(--muted-strong); }
    .featured-flag { background:var(--saffron-deep); color:#fff; border-radius:var(--r-pill); padding:0.2rem 0.6rem; }

    .rlink { display:inline-flex; align-items:center; gap:0.3rem; margin-top:var(--s-4); font-family:var(--font-display); font-size:var(--t-eyebrow); font-weight:700; color:var(--primary); letter-spacing:0.05em; text-transform:uppercase; transition:gap var(--dur) var(--ease); }
    .gcard:hover .rlink, .feature:hover .rlink { gap:0.6rem; }

    .guide-empty { padding:var(--s-16) 0; text-align:center; color:var(--muted); }
    .guide-empty h2 { font-family:var(--font-display); font-size:1.15rem; color:var(--ink); margin-bottom:var(--s-2); }
    .sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }

    @media(max-width:860px){
      .feature { grid-template-columns:1fr; }
      .feature-img img { height:220px; }
      .feature-body { padding:var(--s-6); }
      .blog-hero { padding:7.5rem var(--gutter) 2.5rem; }
      .guide-bar-inner { padding:var(--s-2) var(--gutter); }
      .guide-search { flex:1 1 100%; order:-1; }
    }"""


def card(post, cat_cls, featured=False):
    slug = post["slug"]
    mins = P.reading_time(slug)
    pretty, iso = P.fmt_date(post.get("date", ""))
    img = P.cloudinary(post["image"], "f_auto,q_auto,c_fill,g_auto,ar_3:2,w_600")
    img2 = P.cloudinary(post["image"], "f_auto,q_auto,c_fill,g_auto,ar_3:2,w_1200")
    read = '<span>%d min read</span>' % mins if mins else ""
    # alt="" is deliberate: the card's own heading already names the article, so
    # a descriptive alt would simply be announced twice.
    return """        <a class="gcard" href="/blog/%s/" data-tags="%s" data-search="%s">
          <div class="gcard-img">
            <img src="%s" srcset="%s 600w, %s 1200w"
                 sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 30vw"
                 width="600" height="400" alt="" loading="lazy" decoding="async" />
          </div>
          <div class="gcard-body">
            <p class="gmeta"><span class="bcat %s">%s</span>%s<time datetime="%s">%s</time>%s</p>
            <h3>%s</h3>
            <p>%s</p>
            <span class="rlink">Read the guide <span aria-hidden="true">&rarr;</span></span>
          </div>
        </a>""" % (
        slug, P.CATEGORIES.get(post.get("category", ""), ("", "", "", ""))[1],
        P.esc((post["title"] + " " + post["excerpt"] + " " + post.get("category", "")).lower()),
        img, img, img2, cat_cls, P.esc(post.get("category", "")),
        '<span class="featured-flag">Featured</span>' if featured else "",
        iso, pretty, read, P.short_title(post), P.trim(post["excerpt"]))


def build():
    all_posts = P.load()
    all_posts.sort(key=lambda p: p.get("date", ""), reverse=True)

    # One featured guide, promoted out of the grid so it appears exactly once.
    featured = next((p for p in all_posts if p.get("featured")), all_posts[0])
    rest = [p for p in all_posts if p is not featured]

    counts = {}
    for p in all_posts:
        counts[p.get("category", "")] = counts.get(p.get("category", ""), 0) + 1

    # Chips are built from categories that actually have posts — an empty filter
    # is never offered.
    chips = ['          <button class="chip" type="button" data-filter="all" aria-pressed="true">All guides <span class="n">%d</span></button>' % len(all_posts)]
    for cat in P.CATEGORY_ORDER:
        if counts.get(cat):
            chips.append('          <button class="chip" type="button" id="cat-%s" data-filter="%s" aria-pressed="false">%s <span class="n">%d</span></button>'
                         % (P.CATEGORIES[cat][1], P.CATEGORIES[cat][1], P.esc(cat), counts[cat]))

    groups = []
    for cat in P.CATEGORY_ORDER:
        items = [p for p in rest if p.get("category") == cat]
        if not items:
            continue
        cls, anchor, heading, standfirst = P.CATEGORIES[cat]
        cards = "\n".join(card(p, cls) for p in items)
        groups.append("""      <section class="guide-group" id="%s" aria-labelledby="h-%s">
        <h2 id="h-%s">%s</h2>
        <p class="gg-sub">%s</p>
        <div class="guide-grid">
%s
        </div>
      </section>""" % (anchor, anchor, anchor, heading, standfirst, cards))

    f_cls = P.CATEGORIES.get(featured.get("category", ""), ("cat-default",))[0]
    f_mins = P.reading_time(featured["slug"])
    f_pretty, f_iso = P.fmt_date(featured.get("date", ""))
    f_img = P.cloudinary(featured["image"], "f_auto,q_auto,c_fill,g_auto,ar_4:3,w_760")
    f_img2 = P.cloudinary(featured["image"], "f_auto,q_auto,c_fill,g_auto,ar_4:3,w_1520")

    # ItemList makes the index itself machine-readable: the order and the URL of
    # every guide, which the client-rendered version could not express at all.
    items_ld = ",\n".join(
        '        { "@type": "ListItem", "position": %d, "url": "%s/blog/%s/", "name": %s }'
        % (i + 1, SITE, p["slug"], _json_str(P.short_title(p)))
        for i, p in enumerate([featured] + rest))

    body = """
  <section class="blog-hero">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>
      <span aria-current="page">Guides</span>
    </nav>
    <h1>Nashik travel guides</h1>
    <p class="lede">%d guides covering Simhastha Kumbh Mela 2027, the ghats and temples, the vineyards, the Western Ghats, and the practical business of getting to Nashik and finding somewhere to sleep.</p>
  </section>

  <section aria-labelledby="featured-h" style="padding:var(--s-12) var(--gutter) var(--s-8);background:var(--stone);">
    <div style="max-width:var(--wrap);margin:0 auto var(--s-6);">
      <p class="section-eyebrow">Start Here</p>
      <h2 class="section-title" id="featured-h" style="margin-bottom:0;">The guide most people need first</h2>
    </div>
    <a class="feature" href="/blog/%s/" data-tags="%s" data-search="%s">
      <div class="feature-img">
        <img src="%s" srcset="%s 760w, %s 1520w" sizes="(max-width: 860px) 100vw, 52vw"
             width="760" height="570" alt="" loading="lazy" decoding="async" />
      </div>
      <div class="feature-body">
        <p class="gmeta"><span class="bcat %s">%s</span><span class="featured-flag">Featured</span><time datetime="%s">%s</time>%s</p>
        <h2>%s</h2>
        <p>%s</p>
        <span class="rlink">Read the guide <span aria-hidden="true">&rarr;</span></span>
      </div>
    </a>
  </section>

  <div class="guide-bar" data-filter-group="guides">
    <div class="guide-bar-inner">
      <label class="guide-search">
        <span class="sr-only">Search the guides</span>
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="7" cy="7" r="5"/><path d="M11 11l4 4"/></svg>
        <input type="search" data-filter-search placeholder="Search guides…" autocomplete="off" />
      </label>
      <div class="chips" role="group" aria-label="Filter guides by category">
%s
      </div>
      <p class="sr-only" data-filter-status role="status"></p>
    </div>

    <div class="guides" data-filter-items>
%s
      <p class="guide-empty" data-filter-empty hidden>
        <span style="display:block;font-family:var(--font-display);font-weight:800;color:var(--ink);margin-bottom:0.5rem;">No guides match that search</span>
        Try a different word, or <a href="/blog/" style="color:var(--primary);text-decoration:underline;">browse all %d guides</a>.
      </p>
    </div>
  </div>
""" % (len(all_posts), featured["slug"],
       P.CATEGORIES.get(featured.get("category", ""), ("", "", "", ""))[1],
       P.esc((featured["title"] + " " + featured["excerpt"]).lower()),
       f_img, f_img, f_img2, f_cls, P.esc(featured.get("category", "")),
       f_iso, f_pretty, '<span>%d min read</span>' % f_mins if f_mins else "",
       P.short_title(featured), P.trim(featured["excerpt"], 210),
       "\n".join(chips), "\n".join(groups), len(all_posts))

    return HEAD % {
        "title": TITLE, "meta": META, "url": SITE + "/blog/", "site": SITE,
        "ogimg": P.cloudinary(featured["image"], "f_auto,q_auto,c_fill,g_auto,w_1200,h_630"),
        "css": CSS, "nav": chrome.nav_html("/blog/"), "items": items_ld,
    } + body + "\n</main>\n\n" + chrome.footer_html("/blog/") + "\n\n" + chrome.SITE_JS + "\n</body>\n</html>\n"


def _json_str(s):
    return '"%s"' % (s.replace("&amp;", "&").replace("&hellip;", "…")
                      .replace("\\", "\\\\").replace('"', '\\"'))


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script>document.documentElement.className += ' js';</script>

  <title>%(title)s</title>
  <meta name="description" content="%(meta)s" />
  <link rel="canonical" href="%(url)s" />
  <meta name="robots" content="index, follow, max-image-preview:large" />

  <meta property="og:title" content="%(title)s" />
  <meta property="og:description" content="%(meta)s" />
  <meta property="og:url" content="%(url)s" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="NashikTourism.com" />
  <meta property="og:locale" content="en_IN" />
  <meta property="og:image" content="%(ogimg)s" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="%(title)s" />
  <meta name="twitter:description" content="%(meta)s" />
  <meta name="twitter:image" content="%(ogimg)s" />

  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <meta name="theme-color" content="#2D1B69" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preconnect" href="https://res.cloudinary.com" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400..900&family=Lato:wght@300;400;700&display=swap" />
  <link rel="stylesheet" href="/style.css" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Blog",
        "@id": "%(url)s#blog",
        "url": "%(url)s",
        "name": "Nashik Tourism Guides",
        "description": "%(meta)s",
        "isPartOf": { "@id": "%(site)s/#website" },
        "publisher": { "@id": "%(site)s/#organization" },
        "inLanguage": "en-IN"
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "%(site)s/" },
          { "@type": "ListItem", "position": 2, "name": "Guides", "item": "%(url)s" }
        ]
      },
      {
        "@type": "ItemList",
        "@id": "%(url)s#guides",
        "name": "All Nashik travel guides",
        "itemListOrder": "https://schema.org/ItemListOrderDescending",
        "itemListElement": [
%(items)s
        ]
      }
    ]
  }
  </script>
  <style>
%(css)s
  </style>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<header>
%(nav)s
</header>

<main id="main">
"""


def main():
    html = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    n = html.count('href="/blog/') - html.count('href="/blog/"')
    print("wrote blog/index.html  %d bytes  %d crawlable article links" % (len(html), n))


if __name__ == "__main__":
    main()
