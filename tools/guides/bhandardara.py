"""/discover-nashik/bhandardara/ — Bhandardara had no page of its own (it ranked at 2.3 for
'bhandardara' while living inside the Igatpuri guide). Every figure is labelled 'reported' or
'sources differ': they come from Maharashtra Tourism and travel guides found by search on
2026-11-22, and no editor has verified them yet."""
from nt import aeo, articlekit
from nt.render import ext_link

from . import common

PATH = "/discover-nashik/bhandardara/"
TITLE = "Bhandardara: Arthur Lake, Randha Falls, Fireflies and How to Reach"
H1 = "Bhandardara: Arthur Lake, Randha Falls, Umbrella Falls, Fireflies and How to Reach"
DESC = "Bhandardara guide: Arthur Lake, Randha and Umbrella Falls, firefly season, Igatpuri vs Bhandardara, how to reach from Nashik, Mumbai and Pune, monsoon safety."

MT = ("Maharashtra Tourism: Bhandardara Dam", "https://maharashtratourism.gov.in/nature/bhandardara-dam/")
TRAWELL = ("Trawell: About Bhandardara", "https://www.trawell.in/maharashtra/bhandardara")
WIKI = ("Wikipedia: Bhandardara", "https://en.wikipedia.org/wiki/Bhandardara")
HOLIDIFY = ("Holidify: How to reach Bhandardara", "https://www.holidify.com/places/bhandardara/how-to-reach.html")
FIRE = ("Tripoto: Guide to fireflies at Bhandardara", "https://www.tripoto.com/maharashtra/trips/guide-to-fireflies-at-bhandardhara-maharashtra-5f19436e3b33a")
MONGA = ("Mongabay India: unsustainable tourism and fireflies", "https://india.mongabay.com/2024/10/unsustainable-tourism-habitat-changes-eclipse-the-dazzling-world-of-fireflies/")


def L(src, label=None):
    return ext_link(src[1], label or src[0], item="bhandardara")


def chip(status="reported"):
    return aeo.claim(status, date=common.CHECKED, short=True)


def build():
    quick = ("Bhandardara is a lake and waterfall area in the Western Ghats, reported at about 70&ndash;73 km from Nashik, "
             "156 km from Pune and 177 km from Mumbai. Its highlights are Arthur Lake, Randha Falls and, in the monsoon, "
             "Umbrella Falls; fireflies are reported from about May to June. These details are reported, not yet verified.")
    facts = aeo.key_facts([
        {"label": "What it is", "value": "A lake and waterfall area around Arthur Lake, formed by Wilson Dam on the Pravara river", "status": "reported", "source": MT},
        {"label": "From Nashik", "value": "About 70&ndash;73 km by road", "status": "reported", "source": TRAWELL},
        {"label": "From Mumbai / Pune", "value": "About 177 km / 156 km (other sources give 165&ndash;185 km and 156&ndash;191 km)", "status": "disputed", "source": MT},
        {"label": "Nearest railway station", "value": "Igatpuri, about 35&ndash;45 km away", "status": "reported", "source": HOLIDIFY},
        {"label": "Best time", "value": "Monsoon for the falls and greenery; October to February for pleasant temperatures; about May to June for fireflies", "status": "reported", "source": TRAWELL},
        {"label": "Entry, timings, fees", "value": "Not yet confirmed", "status": "not_verified", "source": None},
    ], caption="Bhandardara key facts")

    compare = """<div class="table-scroll" tabindex="0" role="region" aria-label="Table: Igatpuri compared with Bhandardara">
    <table class="key-facts"><caption>Igatpuri compared with Bhandardara</caption>
      <thead><tr><th scope="col"></th><th scope="col">Igatpuri</th><th scope="col">Bhandardara</th></tr></thead>
      <tbody>
        <tr><th scope="row">What it is</th><td>Hill town in the Western Ghats, on the Mumbai&ndash;Nashik corridor %(c)s</td><td>Lake and waterfall area around Arthur Lake %(c)s</td></tr>
        <tr><th scope="row">From Nashik</th><td>About 45 km %(c)s</td><td>About 70&ndash;73 km %(c)s</td></tr>
        <tr><th scope="row">Nearest railway station</th><td>Igatpuri has its own station on the Mumbai&ndash;Nashik line %(c)s</td><td>Igatpuri, about 35&ndash;45 km away %(c)s</td></tr>
        <tr><th scope="row">Known for</th><td>Ghats scenery and monsoon greenery (see our <a href="/discover-nashik/igatpuri/">Igatpuri guide</a>)</td><td>Arthur Lake, Randha Falls, Umbrella Falls in the monsoon, Kalsubai peak, fireflies %(c)s</td></tr>
        <tr><th scope="row">Choose it if</th><td>You want the hills close to the Mumbai&ndash;Nashik road or rail line.</td><td>You want a lake, waterfalls or a firefly evening and can spend the extra driving time.</td></tr>
      </tbody></table></div>""" % {"c": chip()}

    body = """
    <!-- VERIFY: every Bhandardara figure is 'reported' from Maharashtra Tourism and travel guides (distances, Randha Falls 10 km, Kalsubai 12 km, nearest station Igatpuri 35-45 km, fireflies May-June, district boundary). See VERIFY.md -->
    <p>Bhandardara sits in the Western Ghats close to the Nashik district boundary, and is a common weekend trip from Mumbai and Pune. It has been covered inside our <a href="/discover-nashik/igatpuri/">Igatpuri guide</a>; this page gives it a guide of its own. Every figure below shows its status: <strong>Reported</strong> means published by the sources named, not yet confirmed by our editor.</p>
    %(facts)s

    <h2 id="what-is-bhandardara">What is Bhandardara known for?</h2>
    <h3 id="arthur-lake">Arthur Lake and Wilson Dam</h3>
    <p>Arthur Lake is formed by Wilson Dam and fed by the Pravara river, and lies about 500 m from the Bhandardara bus stop, according to the sources named below %(c)s. Opening hours, entry rules and any boating are not verified; ask locally.</p>
    <h3 id="randha-falls">Randha Falls</h3>
    <p>Randha Falls is reported about 10 km from Bhandardara on the Rajur&ndash;Bhandardara road %(c)s. Its flow depends heavily on the season; the monsoon is described as the best time to see it in full.</p>
    <h3 id="umbrella-falls">Umbrella Falls</h3>
    <p>Umbrella Falls is reported to be seen during the monsoon, when the dam overflows %(c)s. In dry months there may be little or no flow. Do not plan a trip around it without checking recent conditions.</p>
    <h3 id="kalsubai">Kalsubai</h3>
    <p>Kalsubai, reported as Maharashtra&rsquo;s highest peak, lies about 12 km from Bhandardara %(c)s. Any trek is a physical commitment and conditions change with the weather; check with local operators and the forest department before you go.</p>

    <h2 id="fireflies-season">When is the fireflies season at Bhandardara?</h2>
    <p>Travel guides place the firefly display in the pre-monsoon window, roughly <strong>May to June</strong>, shifting with the arrival of the monsoon, and say it fades as regular rain sets in %(c)s. Dates vary by year and there is no official calendar that we found. Reporting also links unsustainable tourism and habitat change to falling firefly numbers (%(monga)s), so watch from a distance, avoid torches and flash photography, and stay on paths. This is general advice, not an official rule.</p>

    <h2 id="igatpuri-vs-bhandardara">Igatpuri or Bhandardara: which should you choose?</h2>
    <p>Many visitors combine them, since Igatpuri is on the way from Mumbai. The table compares what the sources let us say.</p>
    %(compare)s

    <h2 id="how-to-reach-bhandardara">How do you reach Bhandardara from Nashik, Mumbai and Pune?</h2>
    <ul>
      <li><strong>From Nashik:</strong> about 70&ndash;73 km by road %(c)s. Public buses and shared vehicles are reported; see the <a href="/blog/trimbakeshwar-to-nashik-distance-route/">distance guide</a> for how we label road figures.</li>
      <li><strong>From Mumbai:</strong> roughly 165&ndash;185 km by road (the Maharashtra Tourism page gives 177 km); sources differ. The usual route is reported to run via the Mumbai&ndash;Nashik highway past Igatpuri.</li>
      <li><strong>From Pune:</strong> roughly 156&ndash;191 km by road (the Maharashtra Tourism page gives 156 km); sources differ.</li>
      <li><strong>By train:</strong> Igatpuri is the nearest station, about 35&ndash;45 km away, with buses or taxis onward %(h)s. Check trains on <a href="/sources/">NTES and IRCTC</a>.</li>
      <li><strong>By air:</strong> the nearest major airport is reported to be Mumbai, about 180&ndash;190 km away; Nashik (Ozar) airport is reported at about 90 km. Confirm which flights operate.</li>
    </ul>
    <p>Use a live maps app for the route and current road conditions, especially on ghat roads in the monsoon. Our <a href="/blog/how-to-reach-nashik-for-kumbh-mela/">guide to reaching Nashik</a> covers the Mumbai and Pune legs.</p>

    <h2 id="where-to-stay-in-bhandardara">Where can you stay near Bhandardara?</h2>
    <p>We list types of stay, not named properties, because we have not verified any listing, rate or availability:</p>
    <ul>
      <li><strong>Lakeside and hillside resorts</strong> around Arthur Lake: the most common choice for weekend visitors.</li>
      <li><strong>Homestays and village stays</strong> in the surrounding villages: often used for firefly season.</li>
      <li><strong>Camping</strong>: offered by local operators; check safety arrangements, permission and the season.</li>
      <li><strong>Stay in Igatpuri or Nashik</strong> and visit for the day: more transport options, longer journeys.</li>
    </ul>
    <p>Weekends in season are busy. Book early and confirm directly with the property. Hotel search sites are external, with their own prices and terms: %(hotel)s.</p>

    <h2 id="bhandardara-weather-and-monsoon-safety">What is the weather like, and how do you stay safe in the monsoon?</h2>
    <p>We publish no temperature or rainfall figures because we have none that is verified; use the <a href="https://mausam.imd.gov.in/" rel="noopener noreferrer" data-track="official_source_click" data-track-item="imd">India Meteorological Department</a>. The monsoon is when the falls and the greenery are at their best, and also when roads, paths and rocks are at their most dangerous. This is general advice, not an official notice:</p>
    <ul>
      <li>Stay well back from waterfall edges and wet rock; do not enter fast or rising water.</li>
      <li>Water levels near a dam can change quickly. Follow local notices and instructions from police or forest staff.</li>
      <li>Ghat roads are slippery and visibility is low in cloud and rain; drive slowly and avoid night driving.</li>
      <li>Some trails and viewpoints may be closed in the monsoon. Check before you go, and do not trek without a local guide in heavy rain.</li>
      <li>In an emergency call 112 (see <a href="/sources/">our sources</a>).</li>
    </ul>

    <h2 id="more-to-see-nearby">What else is nearby?</h2>
    <ul>
      <li><a href="/discover-nashik/igatpuri/">Igatpuri</a>: the hill town on the way from Mumbai</li>
      <li><a href="/discover-nashik/trimbakeshwar/">Trimbakeshwar Temple</a>, and the <a href="/blog/trimbakeshwar-to-nashik-distance-route/">Nashik to Trimbakeshwar distance guide</a></li>
      <li><a href="/discover-nashik/sula-vineyards/">Sula Vineyards</a> and <a href="/discover-nashik/panchavati/">Panchavati and Ramkund</a> in Nashik</li>
      <li><a href="/blog/best-time-to-visit-nashik/">Best time to visit Nashik</a> and the <a href="/blog/nashik-2-day-itinerary/">two-day itinerary</a></li>
    </ul>
""" % {"facts": facts, "c": chip(), "compare": compare, "monga": L(MONGA, "Mongabay India"), "h": chip(),
       "hotel": aeo.affiliate_link("https://www.makemytrip.com/hotels/nashik-hotels.html", "search Nashik-area hotels")}
    body += aeo.source_list([
        ("Arthur Lake, Wilson Dam, Randha and Umbrella Falls", [MT, TRAWELL, WIKI]),
        ("Distances and the nearest station", [MT, TRAWELL, HOLIDIFY]),
        ("Firefly season and its pressures", [FIRE, MONGA]),
        ("Weather and monsoon conditions", ["imd"]),
    ])
    faq = [
        ("What is Bhandardara famous for?",
         "Arthur Lake (formed by Wilson Dam), Randha Falls, Umbrella Falls in the monsoon, Kalsubai peak and the firefly season, all reported by Maharashtra Tourism and travel guides."),
        ("When is the best time to visit Bhandardara?",
         "The monsoon for waterfalls and greenery, October to February for pleasant temperatures, and about May to June for fireflies. Conditions vary by year; these are reported, not verified."),
        ("How far is Bhandardara from Nashik, Mumbai and Pune?",
         "About 70&ndash;73 km from Nashik, 156 km from Pune and 177 km from Mumbai by the Maharashtra Tourism figures; other sources give wider ranges (165&ndash;185 km from Mumbai, 156&ndash;191 km from Pune)."),
        ("Is Igatpuri or Bhandardara better for a weekend trip?",
         "Igatpuri is closer to the Mumbai&ndash;Nashik road and rail line; Bhandardara is further in but has the lake and waterfalls. See the comparison table above."),
        ("When is the fireflies season at Bhandardara?",
         "Reported as roughly May to June, ending as the monsoon settles in. There is no official calendar we could find."),
        ("Is Bhandardara safe in the monsoon?",
         "The scenery peaks in the monsoon, but wet roads, slippery rock and fast water are real risks. Keep away from edges and fast water and follow local notices. This is general advice, not an official notice."),
    ]
    side = articlekit.sidebar(
        articlekit.side_links("Nearby guides", [("/discover-nashik/igatpuri/", "Igatpuri"), ("/discover-nashik/trimbakeshwar/", "Trimbakeshwar Temple"),
                                                 ("/blog/best-time-to-visit-nashik/", "Best time to visit Nashik"), ("/transport/", "Transport hub")]))
    articlekit.build(PATH, title=TITLE, h1=H1,
                     lede="The lake, the falls and the fireflies in the Western Ghats, with honest labels on every figure.",
                     description=DESC, crumbs=[("Home", "/"), ("Discover Nashik", "/discover-nashik/"), ("Bhandardara", None)],
                     body=body, side=side, faq=faq, quick=quick, published="2026-11-22", topic_label="Nature and weekend trips",
                     extra_ld=[{"@type": "TouristAttraction", "@id": "https://nashiktourism.com" + PATH + "#attraction", "name": "Bhandardara",
                                "description": "Lake and waterfall area in the Western Ghats around Arthur Lake, close to the Nashik district boundary.",
                                "url": "https://nashiktourism.com" + PATH,
                                "address": {"@type": "PostalAddress", "addressLocality": "Bhandardara", "addressRegion": "Maharashtra", "addressCountry": "IN"},
                                "touristType": ["Nature tourism", "Weekend trips"]}],
                     about={"@id": "https://nashiktourism.com" + PATH + "#attraction"})
