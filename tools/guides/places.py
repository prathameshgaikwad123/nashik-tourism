"""The 'Places to visit in Nashik' content for /discover-nashik/.

/discover-nashik/ keeps its URL, its destination cards and its filter; this module supplies the
answer-first part above them: quick answer, a numbered list of places, a table, an FAQ and the
ItemList / FAQPage JSON-LD. Every place carries its own status chip and sources. No distance from
the CBS is shown because none (other than Trimbakeshwar) has been verified, and no opening times or
fees are stated: the sources disagree or the site has not verified them.
"""
from nt import aeo
from nt.paths import SITE
from nt.render import esc, ext_link

PATH = "/discover-nashik/"
TITLE = "Places to Visit in Nashik: Top Tourist Places List (2026 Guide)"
H1 = "Places to Visit in Nashik: Top Tourist Places List"
LEDE = "Fourteen places to see in and around Nashik, with what each is, who it suits and how long to plan."
DESC = "Places to visit in Nashik: 14 top tourist places with type, time needed and links. Trimbakeshwar, Ramkund, Sula, Pandavleni, Igatpuri, Bhandardara."
QUICK = ("The top places to visit in Nashik are Trimbakeshwar Jyotirlinga, Ramkund and Panchavati with Kalaram Temple and Sita Gufa, "
         "Pandavleni Caves, Sula Vineyards and Someshwar Waterfall. Day trips include Igatpuri, Bhandardara and Saptashrungi. "
         "Opening hours and fees are not verified here; check locally.")
UPDATED = "2026-11-22"

TS = "Time needed and best time of day are planning suggestions by our editors, not opening hours."

TRAWELL = lambda slug, name: (name, "https://www.trawell.in/maharashtra/nashik/" + slug)
PV = ("Nashik District tourism site: Panchvati", "https://nashik.gov.in/tourist-place/panchvati/")
OL = ("Outlook Traveller: Panchavati", "https://www.outlookindia.com/traveller/ot-getaway-guides/panchavati-celebrating-rama/")

# id, name, href, kind, best-for, time needed, best time of day, text, status, sources
PLACES = [
    ("trimbakeshwar", "Trimbakeshwar Temple", "/discover-nashik/trimbakeshwar/", "Temple", "Pilgrimage", "Half day", "Early morning",
     "A temple town in the hills west of Nashik, built around one of the twelve Jyotirlingas and the Kushavarta Kund. About 29&ndash;30 km from the Nashik CBS by road, roughly 55&ndash;60 minutes {V} (Google Maps, 22 Nov 2026). See the <a href=\"/blog/trimbakeshwar-to-nashik-distance-route/\">distance and route guide</a>.",
     "not_verified", [("Google Maps driving route, measured 22 Nov 2026 (distance and time only)", "https://www.google.com/maps/dir/?api=1&origin=Nashik+Central+Bus+Stand&destination=Trimbakeshwar+Jyotirling+Mandir&travelmode=driving")]),
    ("ramkund", "Ramkund and Panchavati", "/discover-nashik/panchavati/", "Ghat and old quarter", "Pilgrimage, heritage", "1 to 2 hours", "Morning, or evening for the aarti",
     "The principal bathing ghat on the Godavari, in Nashik's Panchavati quarter. Tradition holds that Rama bathed here during his exile. The evening Godavari aarti is most often listed at about 7&ndash;8 PM; confirm locally (see the <a href=\"/blog/ramkund-ghat-nashik-guide/#godavari-aarti-time-at-ramkund\">Ramkund guide</a>).",
     "reported", [PV, OL]),
    ("kalaram", "Kalaram Temple", "/blog/ramkund-ghat-nashik-guide/#what-to-see-near-ramkund", "Temple", "Pilgrimage", "Under 1 hour", "Morning",
     "An old temple in Panchavati known for its black idol of Rama, and one of Nashik's best-known temples. It is a short way from Ramkund; see the nearby-temples list in our Ramkund guide.",
     "reported", [PV, OL]),
    ("sita-gufa", "Sita Gufa", "/blog/ramkund-ghat-nashik-guide/#what-to-see-near-ramkund", "Cave shrine", "Pilgrimage, heritage", "Under 1 hour", "Morning",
     "A small cave in Panchavati where Sita is believed to have stayed during the exile. It is reported to be near Kalaram Temple, so the two are easily combined.",
     "reported", [PV, OL]),
    ("pandavleni", "Pandavleni Caves", "/discover-nashik/pandavleni-caves/", "Rock-cut caves", "Heritage", "1 to 1.5 hours", "Morning",
     "A group of rock-cut chambers and halls on a hillside south of the city. Reaching them involves a climb (our earlier copy says around 200 steps; not verified), so check step-free access before you go.",
     "not_verified", []),
    ("sula", "Sula Vineyards", "/discover-nashik/sula-vineyards/", "Vineyard and winery", "Wine, leisure", "Half day", "Afternoon",
     "The estate most responsible for Nashik's wine reputation, set up for visitors with tasting, dining and a vineyard walk. Hours, tasting prices and booking rules are set by the estate; check with it.",
     "not_verified", []),
    ("someshwar", "Someshwar Waterfall", "/discover-nashik/#place-someshwar", "Waterfall and temple", "Nature", "1 to 2 hours", "Daytime, in or after the monsoon",
     "A waterfall on the Godavari near Gangapur Road, close to the old Someshwar Shiva temple. Listings describe it as best in or just after the monsoon, with slippery rocks. Distances and timings differ between listings, so check locally.",
     "reported", [TRAWELL("someshwar-waterfalls-dudhsagar-falls", "Trawell: Someshwar Waterfalls"), ("Incredible India: Someshwar Temple", "https://www.incredibleindia.gov.in/en/maharashtra/nashik/someshwar-temple")]),
    ("muktidham", "Muktidham", "/blog/ramkund-ghat-nashik-guide/#what-to-see-near-ramkund", "Temple", "Pilgrimage", "About 1 hour", "Morning",
     "A white marble temple featuring replicas of India's twelve Jyotirlingas, a convenient way to see all twelve in one place. Our earlier copy gives no source for the details, so confirm timings and location before you go.",
     "not_verified", []),
    ("coin-museum", "Coin Museum", "/discover-nashik/#place-coin-museum", "Museum", "Heritage", "1 hour", "Morning or early afternoon",
     "A museum of coins at the Indian Institute for Research in Numismatic Studies campus on the Nashik&ndash;Trimbakeshwar road near Anjaneri. Sources differ on entry fee and list opening hours that include a closing day, so check with the museum before planning around it.",
     "reported", [("Incredible India: Coin Museum", "https://www.incredibleindia.gov.in/en/maharashtra/nashik/coin-museum"), TRAWELL("coin-museum", "Trawell: Coin Museum")]),
    ("anjaneri", "Anjaneri Hill", "/discover-nashik/#place-anjaneri", "Hill and trek", "Nature, pilgrimage", "Half day", "Early morning",
     "A hill fort on the Nashik&ndash;Trimbakeshwar road that tradition links to Hanuman's birth, with a hilltop temple and caves on the trek. It is a physical climb; check conditions and go in good weather.",
     "reported", [("Incredible India: Anjaneri Hills", "https://www.incredibleindia.gov.in/en/maharashtra/nashik/anjaneri-hills"), ("Wikipedia: Anjaneri", "https://en.wikipedia.org/wiki/Anjaneri")]),
    ("gangapur-dam", "Gangapur Dam", "/discover-nashik/#place-gangapur-dam", "Dam and lake", "Nature", "About 1 hour", "Late afternoon",
     "A dam on the Godavari near Nashik, mentioned as a landmark on the road towards Trimbakeshwar. We have no verified details on access or timings.",
     "not_verified", []),
    ("igatpuri", "Igatpuri", "/discover-nashik/igatpuri/", "Hill town", "Nature, weekend trip", "Day trip", "Daytime",
     "A Western Ghats hill town in Nashik district, greenest in and just after the monsoon, and a common weekend trip from Mumbai and Pune. Roads and paths are slippery in the rain.",
     "not_verified", []),
    ("bhandardara", "Bhandardara", "/discover-nashik/bhandardara/", "Lake and waterfalls", "Nature, weekend trip", "Day trip or overnight", "Daytime; evening in firefly season",
     "A lake and waterfall area around Arthur Lake in Akole taluka, Ahilyanagar district, just beyond the Nashik district line. Randha Falls and Umbrella Falls are the main sights, and fireflies are reported from about May to June.",
     "reported", [("Maharashtra Tourism: Bhandardara Dam", "https://maharashtratourism.gov.in/nature/bhandardara-dam/")]),
    ("saptashrungi", "Saptashrungi", "/discover-nashik/#place-saptashrungi", "Hill temple (day trip)", "Pilgrimage", "Full day", "Early morning",
     "A hill temple at Vani in Kalwan taluka, Nashik district, counted among the three and a half Shakti Peethas of Maharashtra. It is reported to be about 60 km from Nashik, so plan it as a day trip.",
     "reported", [("Nashik District site: Saptashrungi", "https://nashik.gov.in/?p=23690"), ("Wikipedia: Saptashrungi", "https://en.wikipedia.org/wiki/Saptashrungi")]),
]

FAQ = [
    ("How many days are enough for Nashik?",
     "Two days covers the main sights: Ramkund and Panchavati, Pandavleni Caves, Sula Vineyards and Trimbakeshwar, with time for food. One day works if you choose between the temples and the wine side, and a third day adds the Western Ghats at Igatpuri or Bhandardara. See our <a href=\"/plan-your-trip/#itineraries\">1, 2 and 3-day itineraries</a> and the <a href=\"/blog/nashik-2-day-itinerary/\">two-day itinerary</a>."),
    ("What are the top 5 places in Nashik?",
     "Trimbakeshwar Temple, Ramkund and Panchavati, Kalaram Temple, Pandavleni Caves and Sula Vineyards are the places most visitors start with. They cover pilgrimage, heritage and wine; the order is our editors' judgement, not a ranking from visitor numbers."),
    ("What are the places near Nashik within 50 km?",
     "Trimbakeshwar is about 29&ndash;30 km from the Nashik CBS (verified on Google Maps, 22 Nov 2026). Sula Vineyards, Pandavleni Caves, Someshwar Waterfall, Gangapur Dam, Anjaneri Hill and the Coin Museum are close to the city or on the Trimbakeshwar road, and Igatpuri is reported at about 45 km. We have not measured those, so check a maps app. Bhandardara (about 70&ndash;73 km, reported) and Saptashrungi (about 60 km, reported) are further out."),
    ("Is Nashik worth visiting?",
     "Yes, for pilgrimage, heritage and wine, and for the hill country around Igatpuri. Nashik hosts the Simhastha Kumbh Mela, with the official Amrut Snan dates in August and September 2027 (see the <a href=\"/kumbh-mela-2027/\">Kumbh hub</a>). Our <a href=\"/blog/is-nashik-worth-visiting/\">longer guide</a> covers the case in detail."),
]


def _status_chip(status):
    return aeo.claim(status, date=UPDATED if status == "verified" else None, short=True)


def section_html():
    items = []
    for n, (pid, name, href, kind, best, time, tod, text, status, sources) in enumerate(PLACES, 1):
        src = "; ".join(ext_link(u, esc(t), item="place-" + pid) for t, u in sources)
        link = '<a href="%s">%s</a>' % (esc(href), name) if href != "/discover-nashik/#place-" + pid else name
        items.append(
            '<li id="place-%s"><h3>%s</h3>'
            '<p class="pl-tags"><span class="pl-tag">%s</span><span class="pl-tag">Best for: %s</span><span class="pl-tag">Time: %s</span> %s</p>'
            '<p>%s</p>%s</li>' % (
                pid, link, esc(kind), esc(best), esc(time), _status_chip(status), text.replace("{V}", aeo.claim("verified", date=UPDATED, short=True)),
                ('<p class="pl-src">Sources: %s</p>' % src) if src else
                ('<p class="pl-src">No source linked yet; see our guide or check locally.</p>' if status == "not_verified" else "")))
    rows = "".join('<tr><th scope="row"><a href="#place-%s">%s</a></th><td>%s</td><td>%s</td><td>%s</td></tr>' % (pid, name, esc(kind), esc(time), esc(tod))
                   for pid, name, _h, kind, _b, time, tod, _t, _s, _src in PLACES)
    table = ('<div class="table-scroll" tabindex="0" role="region" aria-label="Table: Places to visit in Nashik at a glance">'
             '<table class="key-facts"><caption>Places to visit in Nashik at a glance. %s</caption>'
             '<thead><tr><th scope="col">Place</th><th scope="col">Type</th><th scope="col">Time needed</th><th scope="col">Best time of day</th></tr></thead>'
             '<tbody>%s</tbody></table></div>' % (esc(TS), rows))
    faq = "".join("<h3>%s</h3><p>%s</p>" % (esc(q), a) for q, a in FAQ)
    return """
  <section class="places" aria-labelledby="places-top-h">
    <div class="places-wrap">
      %(qa)s
      %(by)s
      <h2 id="places-top-h">Top places to visit in Nashik</h2>
      <p>Nashik's sights fall into four groups: <strong>pilgrimage</strong> (Trimbakeshwar, Ramkund and the Panchavati temples), <strong>heritage</strong> (Pandavleni Caves, the Coin Museum), <strong>wine</strong> (Sula Vineyards) and <strong>nature</strong> (waterfalls, dams and the Western Ghats). Each place below shows its own status: <em>Verified</em> means our editor checked it, <em>Reported</em> means the named sources say so, and <em>Not yet verified</em> means we have no supporting source yet. We show no opening hours or fees, because the sources disagree or we have not verified them.</p>
      <ol class="places-list">%(items)s</ol>

      <h2 id="places-at-a-glance">Places to visit in Nashik at a glance</h2>
      %(table)s

      <h2 id="plan-your-days">Plan your days in Nashik</h2>
      <p>Turn this list into a trip with our <a href="/plan-your-trip/#itineraries">1, 2 and 3-day itineraries</a>, the <a href="/blog/nashik-2-day-itinerary/">two-day itinerary</a>, the <a href="/blog/best-time-to-visit-nashik/">best time to visit Nashik</a> and the <a href="/blog/is-nashik-worth-visiting/">15 best places to visit in Nashik</a>. Travelling between sites? See <a href="/blog/trimbakeshwar-to-nashik-distance-route/">Nashik to Trimbakeshwar distance and routes</a> and the <a href="/transport/">transport hub</a>.</p>

      <h2 id="places-faq">Places to visit in Nashik: frequently asked questions</h2>
      %(faq)s
    </div>
  </section>
""" % {"qa": aeo.quick_answer(QUICK), "by": aeo.byline(UPDATED, None, None).replace('class="byline"', 'class="byline byline-light"'),
       "items": "".join(items), "table": table, "faq": faq}


def extra_ld():
    """ItemList (TouristAttraction items with URLs) and FAQPage nodes for the hub's @graph."""
    items = []
    for n, (pid, name, href, kind, _b, _t, _tod, _text, _s, _src) in enumerate(PLACES, 1):
        url = SITE + href
        items.append({"@type": "ListItem", "position": n, "name": name,
                      "item": {"@type": "TouristAttraction", "name": name, "url": url,
                               "address": {"@type": "PostalAddress", "addressRegion": "Maharashtra", "addressCountry": "IN"}}})
    return [
        {"@type": "ItemList", "@id": SITE + PATH + "#places", "name": "Places to visit in Nashik", "numberOfItems": len(items),
         "itemListOrder": "https://schema.org/ItemListUnordered", "itemListElement": items},
        aeo.faq_ld([(q, aeo.plain(a)) for q, a in FAQ], PATH),
    ]


CSS = """    .places { padding: var(--s-10) 5vw var(--s-6); background: var(--cream); }
    .places-wrap { max-width: 860px; margin: 0 auto; }
    .places-wrap h2 { font-family: var(--font-display); font-size: 1.5rem; font-weight: 800; color: var(--ink); margin: var(--s-10) 0 var(--s-3); letter-spacing: -0.01em; }
    .places-wrap p, .places-wrap li { color: var(--body-clr); line-height: var(--lh-prose); }
    .places-wrap a { color: var(--primary); text-decoration: underline; text-underline-offset: 2px; }
    .places-list { list-style: none; counter-reset: pl; margin: var(--s-5) 0; padding: 0; display: grid; gap: var(--s-4); }
    .places-list > li { counter-increment: pl; position: relative; background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg); padding: var(--s-4) var(--s-5) var(--s-4) 3.4rem; }
    .places-list > li::before { content: counter(pl); position: absolute; left: var(--s-4); top: var(--s-4); width: 1.9rem; height: 1.9rem; border-radius: 50%; background: var(--primary); color: #fff; font-family: var(--font-display); font-weight: 800; font-size: 0.85rem; display: grid; place-items: center; }
    .places-list h3 { margin: 0 0 var(--s-2); font-family: var(--font-display); font-size: 1.1rem; color: var(--ink); }
    .places-list p { margin: 0 0 var(--s-2); font-size: 0.96rem; }
    .pl-tags { display: flex; flex-wrap: wrap; gap: var(--s-2); align-items: center; }
    .pl-tag { font-family: var(--font-display); font-size: 0.7rem; font-weight: 700; letter-spacing: 0.03em; background: var(--stone); color: var(--stone-ink); border-radius: var(--r-pill); padding: 0.2rem 0.6rem; }
    .pl-src { font-size: 0.84rem !important; color: var(--stone-ink) !important; }
    .places-wrap h3 { font-family: var(--font-display); font-size: 1.05rem; color: var(--ink); margin: var(--s-5) 0 var(--s-2); }
    .places-list li h3 { margin-top: 0; }"""
