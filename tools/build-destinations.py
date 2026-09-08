#!/usr/bin/env python3
"""
Generate the Discover Nashik section and the Plan Your Trip hub from one
shared template and one set of page chrome (nav / footer / scripts).

Phase 1 scope: replace the developer scratch stubs with a real, reusable
destination-page structure — hero, breadcrumbs, in-page nav, editorial
sections, internal linking, FAQs and schema.

FACTUAL DISCIPLINE
------------------
Nothing here states opening hours, entry fees, timings, distances, or dates.
Where a real destination guide needs those, the section renders a visible
"being verified" note and the data lives in PENDING below, so it is obvious
what still needs research. Descriptive copy is editorial, not factual claims.
Every fact-shaped statement is one this site already publishes elsewhere.

Usage:  python3 tools/build-destinations.py
"""
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "nashiktourism"))
SITE = "https://nashiktourism.com"
CLD = "https://res.cloudinary.com/duhuxaukd/image/upload"

# ─────────────────────────────────────────────────────────────────────────────
# PENDING FACT RESEARCH — fill these in, then the matching sections render.
# Leave a key absent/empty and the page shows the "being verified" note instead.
# ─────────────────────────────────────────────────────────────────────────────
PENDING = {
    "hours": "Opening / darshan hours",
    "fees": "Entry and any special-darshan fees",
    "distance": "Verified distances and journey times",
    "season": "Month-by-month conditions specific to this site",
}

DESTINATIONS = [
    {
        "slug": "trimbakeshwar",
        "name": "Trimbakeshwar Temple",
        "title": "Trimbakeshwar Temple, Nashik – Visitor Guide",
        "meta": "A guide to Trimbakeshwar, the Jyotirlinga temple town in the hills west of Nashik and one of the focal points of the Nashik Kumbh Mela.",
        "kicker": "Spiritual &middot; Jyotirlinga",
        "img": "v1775379429/steptodown.com223977_zhfdrg.jpg",
        "alt": "Trimbakeshwar Temple set against the hills west of Nashik",
        "lede": "Trimbakeshwar is a temple town in the hills west of Nashik, built around one of the twelve Jyotirlingas. It stands near the source of the Godavari, and during the Simhastha Kumbh Mela it is one of the two centres of the bathing rituals &mdash; the other being the ghats in Nashik city itself.",
        "why": [
            "Trimbakeshwar is the reason a great many people come to Nashik district at all. The temple draws pilgrims through the year, and the town around it has grown up entirely in service of that visit &mdash; lodgings, priests, ritual supplies, queues.",
            "It also feels quite different from Nashik city. The road climbs out of the plain into hills that stay green long after the monsoon, and the town is compact enough to walk. If you are making the trip from Nashik, it is worth allowing more time than the distance alone suggests.",
        ],
        "see": "The temple itself is the centre of any visit, and most people combine it with the tank at Kushavarta nearby, which is the bathing point associated with the Kumbh Mela at Trimbakeshwar. The surrounding town is small and easily explored on foot between visits.",
        "significance": "Trimbakeshwar is counted among the twelve Jyotirlingas, the shrines to Shiva that hold particular importance in Hindu pilgrimage. Its position near the source of the Godavari ties it directly to the river that shapes the rest of Nashik &mdash; and to the Kumbh Mela, which follows that river down to the ghats at Ramkund.",
        "tips": [
            "Temples in Maharashtra generally expect modest dress. It is worth checking current arrangements before you travel, particularly around festival dates.",
            "Queues lengthen considerably on auspicious days. If your dates are flexible, an ordinary weekday will be a very different experience from a festival one.",
            "Trimbakeshwar and Nashik city are separate destinations. Plan them as two trips rather than assuming you can fit both comfortably into a few hours.",
        ],
        "nearby": ["panchavati", "pandavleni-caves", "igatpuri"],
        "related": [
            ("Travel", "Trimbakeshwar to Nashik: distance &amp; route", "Routes, options and travel notes between the two.", "/blog/trimbakeshwar-to-nashik-distance-route/"),
            ("Kumbh Mela", "Nashik Kumbh Mela 2027 guide", "Dates, ghats and what to expect across the Mela.", "/kumbh-mela-2027/"),
            ("Stay", "Where to stay near Ramkund", "Areas, options and what to book early.", "/blog/where-to-stay-nashik-kumbh-mela/"),
        ],
        "faqs": [
            ("Where is Trimbakeshwar?", "Trimbakeshwar is a town in Nashik district, Maharashtra, in the hills to the west of Nashik city. Our <a href=\"/blog/trimbakeshwar-to-nashik-distance-route/\">route guide</a> covers travel between the two."),
            ("Is Trimbakeshwar part of the Kumbh Mela?", "Yes. The Simhastha Kumbh Mela at Nashik centres on two locations: the ghats at Ramkund in Nashik city, and Kushavarta at Trimbakeshwar. Our <a href=\"/kumbh-mela-2027/\">Kumbh Mela 2027 guide</a> explains how the two connect."),
            ("Why is Trimbakeshwar significant?", "It is one of the twelve Jyotirlingas, and it stands near the source of the Godavari &mdash; the river that the Kumbh Mela bathing rituals follow downstream to Nashik."),
        ],
    },
    {
        "slug": "panchavati",
        "name": "Panchavati &amp; Ramkund",
        "title": "Panchavati &amp; Ramkund, Nashik – Visitor Guide",
        "meta": "A guide to Panchavati, the old riverside quarter of Nashik, and Ramkund, its best-known bathing ghat on the Godavari.",
        "kicker": "Heritage &middot; Ghats",
        "img": "v1775367941/steptodown.com803697_wj0xe2.jpg",
        "alt": "Steps leading down to the Godavari at Ramkund in Panchavati",
        "lede": "Panchavati is the old quarter of Nashik on the north bank of the Godavari, and Ramkund is the bathing ghat at its heart. It is the part of the city most closely tied to the Ramayana, and it is where the Nashik side of the Kumbh Mela takes place.",
        "why": [
            "Panchavati is where Nashik stops being a modern city and becomes an old one. The lanes are narrow, the temples are close together, and the river is never far away. It is the densest, most atmospheric part of Nashik and the easiest place to spend a morning simply walking.",
            "Ramkund itself is a working ghat rather than a monument. People come to bathe, to perform rites for the dead, and simply to sit. Visiting means joining that rather than observing it from outside, which is worth knowing before you arrive.",
        ],
        "see": "Ramkund is the anchor, and the temples of Panchavati sit within easy walking distance of it. The area is also the best eating in the city &mdash; our <a href=\"/blog/what-to-eat-near-ramkund-nashik-food-guide/\">food guide to the area</a> covers what to look for.",
        "significance": "Panchavati is associated in the Ramayana with the years Rama spent in exile, and that association is what has drawn pilgrims here for centuries. Ramkund is the primary bathing point on the Nashik side of the Simhastha Kumbh Mela, which makes this quarter the focus of the city's Mela arrangements.",
        "tips": [
            "Panchavati is best walked. The lanes are narrow and vehicle access near the ghat is limited, particularly during festivals.",
            "Ramkund is a place of active worship and of funeral rites. Photography is not always welcome &mdash; read the situation, and ask before pointing a camera at anyone.",
            "Mornings are the most active and the most interesting time at the ghat.",
        ],
        "nearby": ["trimbakeshwar", "pandavleni-caves", "sula-vineyards"],
        "related": [
            ("Guide", "Ramkund Ghat: complete guide", "The ghat itself &mdash; history, rituals and Kumbh context.", "/blog/ramkund-ghat-nashik-guide/"),
            ("Food", "What to eat near Ramkund", "Panchavati food, local dishes and where to find them.", "/blog/what-to-eat-near-ramkund-nashik-food-guide/"),
            ("Stay", "Where to stay near Ramkund", "Areas, options and what to book early.", "/blog/where-to-stay-nashik-kumbh-mela/"),
        ],
        "faqs": [
            ("What is Panchavati known for?", "It is the old riverside quarter of Nashik, associated in the Ramayana with Rama's years of exile, and home to Ramkund &mdash; the city's principal bathing ghat on the Godavari."),
            ("Is Ramkund where the Kumbh Mela bathing happens?", "Ramkund is the main bathing point on the Nashik city side of the Simhastha Kumbh Mela. Kushavarta at <a href=\"/discover-nashik/trimbakeshwar/\">Trimbakeshwar</a> is the other centre."),
            ("Can I walk between the Panchavati temples?", "Yes &mdash; the quarter is compact and most of it is easiest on foot. Our <a href=\"/blog/ramkund-ghat-nashik-guide/\">Ramkund guide</a> goes into the area in more detail."),
        ],
    },
    {
        "slug": "sula-vineyards",
        "name": "Sula Vineyards",
        "title": "Sula Vineyards, Nashik – Visitor Guide",
        "meta": "A guide to visiting Sula Vineyards in the hills outside Nashik — what a vineyard visit involves and how it fits into a Nashik trip.",
        "kicker": "Wine &middot; Leisure",
        "img": None,
        "unsplash": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb",
        "alt": "Rows of vines on a vineyard estate in the hills near Nashik",
        "lede": "Sula is the best-known name in Indian wine and the estate that made Nashik a wine destination. It sits in the hills outside the city, and it is open to visitors for vineyard tours and tastings.",
        "why": [
            "A vineyard visit is the clearest illustration of how many different cities Nashik contains at once. You can spend a morning at the ghats in Panchavati and an afternoon on a terrace looking over vines, and the two feel like different countries.",
            "Sula is also simply the easiest way into Nashik's wine country if you have never done it before. The estate is set up for visitors in a way that smaller producers are not, which makes it a sensible first stop before exploring further.",
        ],
        "see": "A visit generally means a walk through the vineyard, a look at the production side, and a tasting. The estate sits in open country outside the city, so it is worth allowing time for the journey each way rather than treating it as a quick stop.",
        "significance": "The hills around Nashik hold the centre of India's wine industry, and Sula is the estate most responsible for that. Wine tourism is now one of the main reasons people visit Nashik who have no interest in its temples at all &mdash; which is a large part of what makes the city unusual.",
        "tips": [
            "A vineyard visit takes half a day once travel is counted. Do not plan it as an hour between two other things.",
            "If you intend to taste, sort out how you are getting back before you go.",
            "The vineyards are at their most photogenic when the vines are in leaf. Our <a href=\"/blog/best-time-to-visit-nashik/\">month-by-month guide</a> covers how Nashik's seasons run.",
        ],
        "nearby": ["panchavati", "trimbakeshwar", "igatpuri"],
        "related": [
            ("Guide", "Sula Vineyards: complete visit guide", "The full guide to visiting &mdash; tours, tastings and planning.", "/blog/sula-vineyards-nashik-complete-guide/"),
            ("Itinerary", "Nashik in two days", "How a vineyard afternoon fits around the temples and caves.", "/blog/nashik-2-day-itinerary/"),
            ("Timing", "Best time to visit Nashik", "Month by month, and what each season looks like.", "/blog/best-time-to-visit-nashik/"),
        ],
        "faqs": [
            ("Where is Sula Vineyards?", "The estate is in the hills outside Nashik city, in Nashik district, Maharashtra. Our <a href=\"/blog/sula-vineyards-nashik-complete-guide/\">complete Sula guide</a> covers getting there."),
            ("Can you visit the vineyard without booking?", "Arrangements for tours and tastings change with the season and with demand. Check the estate's own current information before travelling &mdash; our <a href=\"/blog/sula-vineyards-nashik-complete-guide/\">guide</a> covers what a visit involves."),
            ("Is Nashik worth visiting just for the wine?", "Plenty of people do exactly that. It is also easy to combine with the rest of the city &mdash; see our <a href=\"/blog/nashik-2-day-itinerary/\">two-day itinerary</a>."),
        ],
    },
    {
        "slug": "pandavleni-caves",
        "name": "Pandavleni Caves",
        "title": "Pandavleni Caves, Nashik – Visitor Guide",
        "meta": "A guide to the Pandavleni Caves, the group of rock-cut chambers in the hillside south of Nashik city.",
        "kicker": "History &middot; Heritage",
        "img": "v1775450823/dhanashree-chavan-UY0FS2_ehh4-unsplash_rsicgk.jpg",
        "alt": "Rock-cut cave facades in the hillside at Pandavleni near Nashik",
        "lede": "Pandavleni is a group of caves cut into a hillside south of Nashik city &mdash; chambers, halls and carved facades worked directly into the rock. It is the oldest thing you can visit in Nashik, and the least crowded.",
        "why": [
            "Pandavleni is the part of Nashik that most visitors skip, which is exactly why it is worth going. The caves are cut into a hill above the plain, and the climb up is rewarded with a long view back over the city.",
            "It is also a complete change of register from the rest of a Nashik trip. After the density of Panchavati and the crowds at Trimbakeshwar, a quiet hillside of empty stone rooms is a genuine relief.",
        ],
        "see": "The caves run along the hillside and are explored on foot, one chamber to the next. Reaching them involves a climb, so footwear matters more here than anywhere else in Nashik.",
        "significance": "The caves are rock-cut monastic chambers, carved into the hillside long before anything else you can visit in Nashik was built. They are the clearest surviving evidence of how old settlement in this part of Maharashtra is.",
        "tips": [
            "There is a climb involved. Wear something you can walk up a hill in.",
            "There is little shade on the way up. Early morning or late afternoon is far more comfortable than the middle of the day.",
            "Carry water. Facilities on the hill are limited.",
        ],
        "nearby": ["panchavati", "sula-vineyards", "trimbakeshwar"],
        "related": [
            ("Itinerary", "Nashik in two days", "Where the caves fit alongside temples and vineyards.", "/blog/nashik-2-day-itinerary/"),
            ("Places", "15 best places to visit in Nashik", "The wider list, including quieter corners.", "/blog/is-nashik-worth-visiting/"),
            ("Timing", "Best time to visit Nashik", "Month by month, and what each season looks like.", "/blog/best-time-to-visit-nashik/"),
        ],
        "faqs": [
            ("Where are the Pandavleni Caves?", "They are cut into a hillside south of Nashik city, in Nashik district, Maharashtra."),
            ("Is there a climb to reach the caves?", "Yes &mdash; the caves are partway up a hill and are reached on foot. Allow more time and better footwear than a city sight would need."),
            ("How do the caves fit into a short Nashik trip?", "They work well as a half-day alongside the city. Our <a href=\"/blog/nashik-2-day-itinerary/\">two-day itinerary</a> shows one way to sequence it."),
        ],
    },
    {
        "slug": "igatpuri",
        "name": "Igatpuri &amp; Bhandardara",
        "title": "Igatpuri &amp; Bhandardara – Visitor Guide",
        "meta": "A guide to Igatpuri and Bhandardara, the Western Ghats hill country near Nashik and a common monsoon weekend trip from Mumbai and Pune.",
        "kicker": "Nature &middot; Weekend",
        "img": "v1775450992/rajesh-kumar-D4dUzlj2LXk-unsplash_1_tinvb7.jpg",
        "alt": "Green hills and low cloud in the Western Ghats near Igatpuri",
        "lede": "Igatpuri and Bhandardara sit in the Western Ghats near Nashik &mdash; hills, reservoirs and, through the monsoon, a great deal of water and green. This is the part of the district people come to for the landscape rather than the temples.",
        "why": [
            "The Ghats change completely with the season here. Through the monsoon and just after, the hills are green, the streams are running and the cloud sits low over everything. It is a genuinely different landscape from the plain around Nashik city.",
            "It is also the reason Nashik works as a weekend trip from Mumbai and Pune. A lot of people come out this way for the hills first and only discover the rest of the district afterwards.",
        ],
        "see": "This is a landscape rather than a list of sights. Most visits mean driving between viewpoints, walking where the weather allows, and stopping at the reservoirs. It rewards an unhurried pace more than a checklist.",
        "significance": "Igatpuri and Bhandardara sit on the edge of the Western Ghats, where the plateau drops away westward. That escarpment is what makes the monsoon here so dramatic, and what has made this stretch a long-standing escape from the cities on the coast.",
        "tips": [
            "The monsoon is the draw and also the difficulty &mdash; roads are wetter, visibility is lower, and paths are slippery. Plan accordingly.",
            "Weekends in season are busy. A weekday is a very different experience.",
            "This is hill country with limited public transport between points. Consider how you will move around before you commit to a route.",
        ],
        "nearby": ["trimbakeshwar", "sula-vineyards", "pandavleni-caves"],
        "related": [
            ("Timing", "Best time to visit Nashik", "How the seasons run, and when the hills are greenest.", "/blog/best-time-to-visit-nashik/"),
            ("Itinerary", "Nashik in two days", "Fitting the hills around the rest of the district.", "/blog/nashik-2-day-itinerary/"),
            ("Places", "15 best places to visit in Nashik", "The wider list across the district.", "/blog/is-nashik-worth-visiting/"),
        ],
        "faqs": [
            ("Where are Igatpuri and Bhandardara?", "Both are in the Western Ghats near Nashik, in Maharashtra, between Nashik and the coast."),
            ("When is the best time to go?", "The hills are at their greenest during and just after the monsoon. Our <a href=\"/blog/best-time-to-visit-nashik/\">month-by-month guide</a> covers how Nashik's seasons run."),
            ("Is it a good weekend trip from Mumbai or Pune?", "It is one of the more common weekend destinations from both. Our <a href=\"/blog/nashik-2-day-itinerary/\">two-day itinerary</a> shows how it fits with the rest of Nashik."),
        ],
    },
]

BY_SLUG = {d["slug"]: d for d in DESTINATIONS}


def img_url(dest, transform):
    if dest.get("unsplash"):
        return "%s?%s&q=75&auto=format&fit=crop" % (dest["unsplash"], transform)
    return "%s/%s/%s" % (CLD, transform, dest["img"])


def hero_img(dest):
    if dest.get("unsplash"):
        base = dest["unsplash"]
        srcset = ", ".join("%s?w=%d&q=75&auto=format&fit=crop %dw" % (base, w, w)
                           for w in (640, 960, 1280, 1920))
        return base + "?w=1280&q=75&auto=format&fit=crop", srcset
    t = "f_auto,q_auto,c_fill,g_auto,ar_16:9,w_%d"
    srcset = ", ".join("%s/%s/%s %dw" % (CLD, t % w, dest["img"], w)
                       for w in (640, 960, 1280, 1920))
    return "%s/%s/%s" % (CLD, t % 1280, dest["img"]), srcset


def og_img(dest):
    if dest.get("unsplash"):
        return dest["unsplash"] + "?w=1200&h=630&q=75&auto=format&fit=crop"
    return "%s/f_auto,q_auto,c_fill,g_auto,w_1200,h_630/%s" % (CLD, dest["img"])


def plain(text):
    return text.replace("&amp;", "&").replace("&middot;", "·").replace("&mdash;", "—")


def nav_html(active):
    return """<nav class="nav solid" id="mainNav" aria-label="Primary">
  <div class="nav-inner">
    <a href="/" class="nav-logo">
      <img src="/logo-white-96.png" alt="Nashik Tourism" width="48" height="48" />
      <span class="nav-logo-text">Nashik Tourism<small>Independent Travel Guide</small></span>
    </a>
    <ul class="nav-menu">
      <li>
        <a href="/kumbh-mela-2027/">Kumbh Mela 2027</a>
        <button class="chevron-btn" type="button" aria-expanded="false" aria-controls="dd-kumbh" aria-label="Kumbh Mela 2027 submenu"><span class="chevron" aria-hidden="true">&#9662;</span></button>
        <div class="dropdown" id="dd-kumbh">
          <a href="/kumbh-mela-2027/">Complete Guide</a>
          <a href="/kumbh-mela-2027/#dates">Amrit Snan Dates</a>
          <a href="/blog/how-to-reach-nashik-for-kumbh-mela/">How to Reach</a>
          <a href="/blog/where-to-stay-nashik-kumbh-mela/">Where to Stay</a>
        </div>
      </li>
      <li>
        <a href="/discover-nashik/" class="active">Discover Nashik</a>
        <button class="chevron-btn" type="button" aria-expanded="false" aria-controls="dd-discover" aria-label="Discover Nashik submenu"><span class="chevron" aria-hidden="true">&#9662;</span></button>
        <div class="dropdown" id="dd-discover">
%s
        </div>
      </li>
      <li><a href="/plan-your-trip/">Plan Your Trip</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/about/">About</a></li>
      <li><a href="/contact/" class="nav-book">Contact</a></li>
    </ul>
    <button class="hamburger" id="hamburger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu"><span></span><span></span><span></span></button>
  </div>
</nav>

<div class="mobile-menu" id="mobileMenu">
  <a href="/kumbh-mela-2027/">Kumbh Mela 2027</a>
  <a href="/kumbh-mela-2027/#dates">Amrit Snan Dates</a>
  <a href="/discover-nashik/">Discover Nashik</a>
  <a href="/discover-nashik/trimbakeshwar/">Trimbakeshwar Temple</a>
  <a href="/discover-nashik/sula-vineyards/">Sula Vineyards</a>
  <a href="/plan-your-trip/">Plan Your Trip</a>
  <a href="/blog/">Travel Blog</a>
  <a href="/about/">About</a>
  <a href="/contact/" class="mob-book">Contact Us</a>
</div>""" % (
        "\n".join('          <a href="/discover-nashik/%s/"%s>%s</a>'
                  % (d["slug"], ' aria-current="page"' if d["slug"] == active else "", d["name"])
                  for d in DESTINATIONS),
    )


FOOTER = """<footer>
  <div class="footer-top">
    <div class="footer-brand">
      <img src="/logo-white-96.png" alt="Nashik Tourism" width="64" height="64" loading="lazy" />
      <h3>Nashik Tourism</h3>
      <p>Your independent guide to Nashik &mdash; temples, vineyards, the Western Ghats and Kumbh Mela 2027.</p>
    </div>
    <div class="footer-col"><h4>Kumbh Mela 2027</h4><ul><li><a href="/kumbh-mela-2027/">Complete Guide</a></li><li><a href="/kumbh-mela-2027/#dates">Amrit Snan Dates</a></li><li><a href="/blog/how-to-reach-nashik-for-kumbh-mela/">How to Reach</a></li><li><a href="/blog/where-to-stay-nashik-kumbh-mela/">Where to Stay</a></li></ul></div>
    <div class="footer-col"><h4>Discover Nashik</h4><ul>%s</ul></div>
    <div class="footer-col"><h4>Plan Your Trip</h4><ul><li><a href="/plan-your-trip/">Trip Planner</a></li><li><a href="/blog/best-time-to-visit-nashik/">Best Time to Visit</a></li><li><a href="/blog/nashik-2-day-itinerary/">2-Day Itinerary</a></li><li><a href="/blog/">All Travel Guides</a></li></ul></div>
    <div class="footer-col"><h4>Site</h4><ul><li><a href="/about/">About Us</a></li><li><a href="/contact/">Contact</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul></div>
  </div>
  <div class="footer-bottom">
    <span>&copy; 2026 NashikTourism.com &mdash; an independent travel guide. Not affiliated with any government body or official tourism authority.</span>
    <span>Made with &hearts; for Nashik</span>
  </div>
</footer>""" % "".join('<li><a href="/discover-nashik/%s/">%s</a></li>' % (d["slug"], d["name"])
                       for d in DESTINATIONS)

SCRIPT = """<script>
  (function () {
    var hb = document.getElementById('hamburger');
    var mm = document.getElementById('mobileMenu');
    function setMenu(open) {
      hb.classList.toggle('open', open);
      mm.classList.toggle('open', open);
      hb.setAttribute('aria-expanded', String(open));
      hb.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.style.overflow = open ? 'hidden' : '';
    }
    hb.addEventListener('click', function () { setMenu(!mm.classList.contains('open')); });
    mm.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
    var openDd = null;
    function closeDd() {
      if (!openDd) return;
      openDd.menu.classList.remove('open');
      openDd.btn.setAttribute('aria-expanded', 'false');
      openDd = null;
    }
    document.querySelectorAll('.chevron-btn').forEach(function (btn) {
      var menu = document.getElementById(btn.getAttribute('aria-controls'));
      if (!menu) return;
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var isOpen = menu.classList.contains('open');
        closeDd();
        if (!isOpen) {
          menu.classList.add('open');
          btn.setAttribute('aria-expanded', 'true');
          openDd = { btn: btn, menu: menu };
        }
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        closeDd();
        if (mm.classList.contains('open')) { setMenu(false); hb.focus(); }
      }
    });
    document.addEventListener('click', function (e) {
      if (openDd && !openDd.menu.contains(e.target) && !openDd.btn.contains(e.target)) closeDd();
    });
  })();
</script>

<!-- Deferred third-party: analytics loads last and never blocks rendering -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-H04PTE8QL1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-H04PTE8QL1');
</script>"""


def build(dest):
    slug = dest["slug"]
    url = "%s/discover-nashik/%s/" % (SITE, slug)
    src, srcset = hero_img(dest)

    why = "\n".join("        <p>%s</p>" % p for p in dest["why"])
    tips = "\n".join("          <li>%s</li>" % t for t in dest["tips"])

    nearby = "\n".join(
        """          <a class="link-card" href="/discover-nashik/%s/">
            <span class="lc-kicker">%s</span>
            <span class="lc-title">%s</span>
            <span class="lc-desc">%s</span>
          </a>""" % (s, BY_SLUG[s]["kicker"], BY_SLUG[s]["name"],
                     BY_SLUG[s]["lede"].split(".")[0] + ".")
        for s in dest["nearby"])

    related = "\n".join(
        """          <a class="link-card" href="%s">
            <span class="lc-kicker">%s</span>
            <span class="lc-title">%s</span>
            <span class="lc-desc">%s</span>
          </a>""" % (href, kicker, title, desc)
        for kicker, title, desc, href in dest["related"])

    faqs = "\n".join(
        """        <details class="faq-item">
          <summary>%s</summary>
          <div class="faq-answer"><p>%s</p></div>
        </details>""" % (q, a) for q, a in dest["faqs"])

    sidebar_related = "".join(
        '<li><a href="%s">%s</a></li>' % (href, title)
        for _, title, _, href in dest["related"])

    breadcrumb_json = """{
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "%s/" },
          { "@type": "ListItem", "position": 2, "name": "Discover Nashik", "item": "%s/discover-nashik/" },
          { "@type": "ListItem", "position": 3, "name": "%s", "item": "%s" }
        ]
      }""" % (SITE, SITE, plain(dest["name"]), url)

    return """<!DOCTYPE html>
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
  <meta property="og:type" content="article" />
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
  <link rel="preload" as="image" fetchpriority="high" imagesrcset="%(srcset)s" imagesizes="100vw" />
  <link rel="stylesheet" href="/style.css" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebPage",
        "@id": "%(url)s#webpage",
        "url": "%(url)s",
        "name": "%(title_plain)s",
        "description": "%(meta)s",
        "isPartOf": { "@id": "%(site)s/#website" },
        "about": { "@id": "%(url)s#attraction" },
        "inLanguage": "en-IN"
      },
      %(breadcrumb)s,
      {
        "@type": "TouristAttraction",
        "@id": "%(url)s#attraction",
        "name": "%(name_plain)s",
        "description": "%(lede_plain)s",
        "url": "%(url)s",
        "image": "%(ogimg)s",
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "Nashik",
          "addressRegion": "Maharashtra",
          "addressCountry": "IN"
        }
      }
    ]
  }
  </script>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<header>
%(nav)s
</header>

<main id="main" class="dest-main">

  <section class="dest-hero" aria-label="%(name_plain)s">
    <img class="dest-hero-img" src="%(src)s" srcset="%(srcset)s" sizes="100vw"
         width="1280" height="720" fetchpriority="high" decoding="async" alt="%(alt)s" />
    <div class="dest-hero-inner">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>
        <a href="/discover-nashik/">Discover Nashik</a> <span aria-hidden="true">&rsaquo;</span>
        <span aria-current="page">%(name)s</span>
      </nav>
      <p class="dest-kicker">%(kicker)s</p>
      <h1>%(name)s</h1>
      <p class="lede">%(lede)s</p>
    </div>
  </section>

  <nav class="dest-nav" aria-label="On this page">
    <ul>
      <li><a href="#why-visit">Why visit</a></li>
      <li><a href="#see-do">Things to see</a></li>
      <li><a href="#significance">Significance</a></li>
      <li><a href="#getting-there">Getting there</a></li>
      <li><a href="#best-time">Best time</a></li>
      <li><a href="#tips">Travel tips</a></li>
      <li><a href="#nearby">Nearby</a></li>
      <li><a href="#faqs">FAQs</a></li>
    </ul>
  </nav>

  <div class="dest-wrap">
    <article class="dest-body">

      <section id="why-visit">
        <h2>Why visit %(name)s</h2>
%(why)s
      </section>

      <section id="see-do">
        <h2>Things to see and do</h2>
        <p>%(see)s</p>
        <div class="pending-note">
          <p class="pending-title">Practical details being verified</p>
          <p>We are confirming %(pending_hours)s and %(pending_fees)s from official sources before publishing them here, rather than repeating figures we cannot stand behind. Please check current details close to your travel date.</p>
        </div>
      </section>

      <section id="significance">
        <h2>History and significance</h2>
        <p>%(significance)s</p>
      </section>

      <section id="getting-there">
        <h2>How to reach %(name)s</h2>
        <p>%(name)s is in Nashik district, Maharashtra. Nashik itself is reachable by train, bus, road and air, and our <a href="/blog/how-to-reach-nashik-for-kumbh-mela/">how to reach Nashik guide</a> sets out the options from Mumbai, Pune and Delhi.</p>
        <div class="pending-note">
          <p class="pending-title">Local routes being verified</p>
          <p>%(pending_distance)s for the last stretch of this journey are still being checked. We would rather leave this blank than publish a number that sends you the wrong way.</p>
        </div>
      </section>

      <section id="best-time">
        <h2>Best time to visit</h2>
        <p>Nashik's year divides fairly clearly into the monsoon, the cool months that follow it, and a hot stretch before the rains return. Our <a href="/blog/best-time-to-visit-nashik/">month-by-month guide to Nashik</a> covers how that plays out across the district.</p>
        <div class="pending-note">
          <p class="pending-title">Site-specific timing being verified</p>
          <p>%(pending_season)s &mdash; including festival dates and any seasonal closures &mdash; are still being confirmed.</p>
        </div>
      </section>

      <section id="tips">
        <h2>Travel tips</h2>
        <ul>
%(tips)s
        </ul>
      </section>

      <section id="nearby">
        <h2>Nearby attractions</h2>
        <div class="link-cards">
%(nearby)s
        </div>
      </section>

      <section id="related">
        <h2>Related guides</h2>
        <div class="link-cards">
%(related)s
        </div>
      </section>

      <section id="faqs">
        <h2>Frequently asked questions</h2>
%(faqs)s
      </section>

    </article>

    <aside class="sidebar" aria-label="Quick links">
      <div class="sidebar-card">
        <h4>Plan this visit</h4>
        <ul class="toc-list">
          <li><a href="/blog/how-to-reach-nashik-for-kumbh-mela/">How to reach Nashik</a></li>
          <li><a href="/blog/best-time-to-visit-nashik/">Best time to visit</a></li>
          <li><a href="/blog/where-to-stay-nashik-kumbh-mela/">Where to stay</a></li>
          <li><a href="/blog/nashik-2-day-itinerary/">Two-day itinerary</a></li>
          <li><a href="/blog/nashik-kumbh-mela-budget-2027/">Budget guide</a></li>
        </ul>
        <a href="/plan-your-trip/" class="btn btn-purple">Plan Your Trip</a>
      </div>
      <div class="sidebar-card">
        <h4>Related reading</h4>
        <ul class="toc-list">%(sidebar_related)s</ul>
      </div>
      <div class="sidebar-card">
        <h4>Kumbh Mela 2027</h4>
        <ul class="toc-list">
          <li><a href="/kumbh-mela-2027/">Complete guide</a></li>
          <li><a href="/kumbh-mela-2027/#dates">Amrit Snan dates</a></li>
        </ul>
      </div>
    </aside>
  </div>

</main>

%(footer)s

%(script)s
</body>
</html>
""" % {
        "title": dest["title"], "title_plain": plain(dest["title"]),
        "meta": dest["meta"], "url": url, "site": SITE,
        "ogimg": og_img(dest), "src": src, "srcset": srcset,
        "alt": dest["alt"], "name": dest["name"], "name_plain": plain(dest["name"]),
        "kicker": dest["kicker"], "lede": dest["lede"], "lede_plain": plain(dest["lede"]),
        "why": why, "see": dest["see"], "significance": dest["significance"],
        "tips": tips, "nearby": nearby, "related": related, "faqs": faqs,
        "sidebar_related": sidebar_related, "breadcrumb": breadcrumb_json,
        "pending_hours": PENDING["hours"].lower(),
        "pending_fees": PENDING["fees"].lower(),
        "pending_distance": PENDING["distance"],
        "pending_season": PENDING["season"],
        "nav": nav_html(dest["slug"]), "footer": FOOTER, "script": SCRIPT,
    }


HUB_HEAD = """<!DOCTYPE html>
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
        "@type": "WebPage",
        "@id": "%(url)s#webpage",
        "url": "%(url)s",
        "name": "%(title_plain)s",
        "description": "%(meta)s",
        "isPartOf": { "@id": "%(site)s/#website" },
        "inLanguage": "en-IN"
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "%(site)s/" },
          { "@type": "ListItem", "position": 2, "name": "%(crumb)s", "item": "%(url)s" }
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


def hub_page(title, meta, url, crumb, ogimg, css, nav, body):
    return (HUB_HEAD % {
        "title": title, "title_plain": plain(title), "meta": meta, "url": url,
        "crumb": crumb, "ogimg": ogimg, "site": SITE, "css": css, "nav": nav,
    }) + body + "\n</main>\n\n" + FOOTER + "\n\n" + SCRIPT + "\n</body>\n</html>\n"


DISCOVER_CSS = """    .hub-hero { background: var(--dark); padding: 9rem 5vw 3.5rem; }
    .hub-hero h1 { font-family:'Montserrat',sans-serif; font-size:clamp(2rem,5vw,3.5rem); font-weight:900; color:white; letter-spacing:-0.025em; line-height:1.08; margin:0.4rem 0 0.9rem; }
    .hub-hero .lede { color: var(--on-dark); font-size:1.05rem; line-height:1.7; max-width:620px; }
    .dest-cards { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:1.1rem; }
    .dest-card { display:block; background:white; border:1px solid var(--border); border-radius:10px; overflow:hidden; transition:transform 0.22s, box-shadow 0.22s; }
    .dest-card:hover { transform:translateY(-5px); box-shadow:0 18px 45px rgba(45,27,105,0.12); }
    .dest-card img { width:100%; height:200px; object-fit:cover; }
    .dest-card-body { padding:1.3rem; }
    .dest-card .dc-kicker { display:block; font-family:'Montserrat',sans-serif; font-size:0.62rem; font-weight:700; letter-spacing:0.13em; text-transform:uppercase; color:var(--saffron-deep); margin-bottom:0.4rem; }
    .dest-card h2 { font-family:'Montserrat',sans-serif; font-size:1.1rem; font-weight:800; color:var(--ink); line-height:1.3; letter-spacing:-0.01em; margin-bottom:0.4rem; }
    .dest-card p { font-size:0.88rem; color:var(--muted-strong); line-height:1.6; }
    .dest-card .rlink { display:inline-flex; align-items:center; gap:0.3rem; margin-top:0.9rem; font-family:'Montserrat',sans-serif; font-size:0.72rem; font-weight:700; color:var(--primary); letter-spacing:0.05em; text-transform:uppercase; transition:gap 0.2s; }
    .dest-card:hover .rlink { gap:0.55rem; }
    @media(max-width:1024px){ .dest-cards{grid-template-columns:repeat(2,minmax(0,1fr));} }
    @media(max-width:640px){ .dest-cards{grid-template-columns:1fr;} .hub-hero{padding:7.5rem 5vw 2.5rem;} }"""

PLAN_CSS = """    .hub-hero { background: var(--dark); padding: 9rem 5vw 3.5rem; }
    .hub-hero h1 { font-family:'Montserrat',sans-serif; font-size:clamp(2rem,5vw,3.5rem); font-weight:900; color:white; letter-spacing:-0.025em; line-height:1.08; margin:0.4rem 0 0.9rem; }
    .hub-hero .lede { color: var(--on-dark); font-size:1.05rem; line-height:1.7; max-width:620px; }
    .plan-list { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:0; border-top:1px solid var(--border); max-width:1140px; }
    .prow { display:flex; align-items:baseline; gap:1rem; padding:1.2rem 0.5rem 1.2rem 0; border-bottom:1px solid var(--border); transition:background 0.18s, padding-left 0.18s; }
    .prow:hover { background:var(--light); padding-left:0.75rem; }
    .prow-num { font-family:'Montserrat',sans-serif; font-size:0.72rem; font-weight:800; color:var(--saffron-deep); letter-spacing:0.06em; flex-shrink:0; min-width:1.6rem; }
    .prow-txt { flex:1 1 auto; }
    .prow-txt h3 { font-family:'Montserrat',sans-serif; font-size:1.02rem; font-weight:800; color:var(--ink); letter-spacing:-0.01em; margin-bottom:0.15rem; }
    .prow-txt p { font-size:0.88rem; color:var(--muted-strong); line-height:1.55; }
    .prow-go { margin-left:auto; align-self:center; color:var(--primary); font-size:1.1rem; flex-shrink:0; transition:transform 0.18s; }
    .prow:hover .prow-go { transform:translateX(4px); }
    .checklist { max-width:760px; }
    .checklist li { margin-bottom:0.7rem; color:var(--body-clr); line-height:1.7; }
    @media(min-width:769px){ .plan-list > .prow:nth-child(odd){padding-right:2.5rem;} .plan-list > .prow:nth-child(even){padding-left:2.5rem;} }
    @media(max-width:768px){ .plan-list{grid-template-columns:1fr;} .hub-hero{padding:7.5rem 5vw 2.5rem;} }"""

PLAN_ROWS = [
    ("How do I reach Nashik?", "Train, bus, flight and road routes from Mumbai, Pune and Delhi.", "/blog/how-to-reach-nashik-for-kumbh-mela/"),
    ("When should I visit?", "How the seasons run, and which months suit which kind of trip.", "/blog/best-time-to-visit-nashik/"),
    ("How many days are enough?", "A worked two-day itinerary across temples, caves and vineyards.", "/blog/nashik-2-day-itinerary/"),
    ("Where should I stay?", "Which areas suit which trip, from Panchavati to the vineyard side.", "/blog/where-to-stay-nashik-kumbh-mela/"),
    ("What will it cost?", "A budget breakdown for travel, stay, food and getting around.", "/blog/nashik-kumbh-mela-budget-2027/"),
    ("What should I actually see?", "Fifteen places worth your time, temples and vineyards to quieter corners.", "/blog/is-nashik-worth-visiting/"),
    ("What do I pack?", "A practical packing list, written with Kumbh Mela crowds in mind.", "/blog/nashik-kumbh-mela-packing-list/"),
    ("What about Kumbh Mela 2027?", "Dates, ghats, crowds and how the Mela reshapes a Nashik trip.", "/kumbh-mela-2027/"),
]


def build_discover_hub():
    cards = []
    for d in DESTINATIONS:
        if d.get("unsplash"):
            src = d["unsplash"] + "?w=560&q=75&auto=format&fit=crop"
            srcset = ", ".join("%s?w=%d&q=75&auto=format&fit=crop %dw" % (d["unsplash"], w, w)
                               for w in (400, 560, 900))
        else:
            t = "f_auto,q_auto,c_fill,g_auto,ar_3:2,w_%d"
            src = "%s/%s/%s" % (CLD, t % 560, d["img"])
            srcset = ", ".join("%s/%s/%s %dw" % (CLD, t % w, d["img"], w) for w in (400, 560, 900))
        cards.append("""    <a class="dest-card fade-up" href="/discover-nashik/%s/">
      <img src="%s" srcset="%s" sizes="(max-width: 640px) 92vw, (max-width: 1024px) 46vw, 31vw"
           width="560" height="373" alt="%s" loading="lazy" decoding="async" />
      <div class="dest-card-body">
        <span class="dc-kicker">%s</span>
        <h2>%s</h2>
        <p>%s</p>
        <span class="rlink">Open guide <span aria-hidden="true">&rarr;</span></span>
      </div>
    </a>""" % (d["slug"], src, srcset, d["alt"], d["kicker"], d["name"],
               d["lede"].split(". ")[0] + "."))

    body = """
  <section class="hub-hero">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>
      <span aria-current="page">Discover Nashik</span>
    </nav>
    <h1>Discover Nashik</h1>
    <p class="lede">Five very different places, all within reach of one city &mdash; a Jyotirlinga in the hills, an old riverside quarter, a vineyard estate, a hillside of rock-cut caves, and the Western Ghats.</p>
  </section>

  <section aria-labelledby="places-h">
    <p class="section-eyebrow">Where to Go</p>
    <h2 class="section-title" id="places-h" style="margin-bottom:0.4rem;">Places to visit in Nashik</h2>
    <p class="section-sub">Each guide covers why the place is worth your time, how it fits into a trip, and what to read next.</p>
    <div class="dest-cards">
%s
    </div>
  </section>

  <section style="background:var(--light);" aria-labelledby="next-h">
    <p class="section-eyebrow">Next Step</p>
    <h2 class="section-title" id="next-h">Turn this into a trip</h2>
    <p class="section-sub">Once you know where you are going, the practical guides cover getting there, when to come and where to stay.</p>
    <div style="display:flex;gap:0.9rem;flex-wrap:wrap;">
      <a href="/plan-your-trip/" class="btn btn-purple">Plan Your Trip</a>
      <a href="/kumbh-mela-2027/" class="btn btn-outline">Kumbh Mela 2027</a>
      <a href="/blog/" class="btn btn-outline">All Travel Guides</a>
    </div>
  </section>
""" % "\n".join(cards)

    return hub_page(
        "Discover Nashik – Temples, Heritage, Vineyards &amp; Nature",
        "Places to visit in Nashik: Trimbakeshwar, Panchavati and Ramkund, Sula Vineyards, the Pandavleni Caves and the Western Ghats at Igatpuri.",
        SITE + "/discover-nashik/", "Discover Nashik",
        "%s/f_auto,q_auto,c_fill,g_auto,w_1200,h_630/%s" % (CLD, DESTINATIONS[0]["img"]),
        DISCOVER_CSS, nav_html("__hub__"), body)


def build_plan_hub():
    rows = "\n".join("""    <a href="%s" class="prow">
      <span class="prow-num" aria-hidden="true">%02d</span>
      <div class="prow-txt"><h3>%s</h3><p>%s</p></div>
      <span class="prow-go" aria-hidden="true">&rarr;</span>
    </a>""" % (href, i + 1, q, d) for i, (q, d, href) in enumerate(PLAN_ROWS))

    body = """
  <section class="hub-hero">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>
      <span aria-current="page">Plan Your Trip</span>
    </nav>
    <h1>Plan your Nashik trip</h1>
    <p class="lede">Everything practical in one place &mdash; getting there, when to come, how long to stay, what it costs, and how Kumbh Mela 2027 changes the answer to all of those.</p>
  </section>

  <section aria-labelledby="q-h">
    <p class="section-eyebrow">Start Here</p>
    <h2 class="section-title" id="q-h" style="margin-bottom:0.4rem;">The questions people ask first</h2>
    <p class="section-sub">Each one links to a full guide.</p>
    <div class="plan-list">
%s
    </div>
  </section>

  <section style="background:var(--light);" aria-labelledby="check-h">
    <p class="section-eyebrow">Before You Go</p>
    <h2 class="section-title" id="check-h">A short checklist</h2>
    <p class="section-sub">Worth settling early, particularly for travel around Kumbh Mela 2027.</p>
    <ul class="checklist">
      <li>Decide your travel mode first &mdash; train, bus, flight or self-drive &mdash; because it shapes everything else. See <a href="/blog/how-to-reach-nashik-for-kumbh-mela/">how to reach Nashik</a>.</li>
      <li>Pick the zone you want to stay in before you pick a hotel. Panchavati and Trimbakeshwar suit very different trips: <a href="/blog/where-to-stay-nashik-kumbh-mela/">where to stay</a>.</li>
      <li>Book accommodation early if your dates fall near the Amrit Snan dates &mdash; see the <a href="/kumbh-mela-2027/">Kumbh Mela 2027 guide</a>.</li>
      <li>Carry ID, emergency contacts and a light day bag for ghat visits. Our <a href="/blog/nashik-kumbh-mela-packing-list/">packing list</a> goes further.</li>
      <li>Confirm timings and any festival arrangements close to your travel date &mdash; they change, and Kumbh Mela plans in particular are still being finalised.</li>
    </ul>
  </section>

  <section aria-labelledby="where-h">
    <p class="section-eyebrow">Where to Go</p>
    <h2 class="section-title" id="where-h">Still deciding where to go?</h2>
    <p class="section-sub">The destination guides cover what each place is actually like.</p>
    <div style="display:flex;gap:0.9rem;flex-wrap:wrap;">
      <a href="/discover-nashik/" class="btn btn-purple">Discover Nashik</a>
      <a href="/blog/" class="btn btn-outline">All Travel Guides</a>
    </div>
  </section>
""" % rows

    return hub_page(
        "Plan Your Nashik Trip – Routes, Timing, Stays &amp; Budget",
        "Plan a trip to Nashik: how to reach the city, the best time to visit, how many days you need, where to stay, what it costs, and Kumbh Mela 2027.",
        SITE + "/plan-your-trip/", "Plan Your Trip",
        "%s/f_auto,q_auto,c_fill,g_auto,w_1200,h_630/%s" % (CLD, DESTINATIONS[0]["img"]),
        PLAN_CSS, nav_html("__none__"), body)


def main():
    hubs = [
        (os.path.join(ROOT, "discover-nashik", "index.html"), build_discover_hub()),
        (os.path.join(ROOT, "plan-your-trip", "index.html"), build_plan_hub()),
    ]
    for out, html in hubs:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("  wrote %-46s %6d bytes" % (out.replace(ROOT + os.sep, ""), len(html)))

    for dest in DESTINATIONS:
        out = os.path.join(ROOT, "discover-nashik", dest["slug"], "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        html = build(dest)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("  wrote %-46s %6d bytes" % (out.replace(ROOT + os.sep, ""), len(html)))


if __name__ == "__main__":
    main()
