"""/transport/nashik-road-station-to-trimbakeshwar/ — a standalone guide for the biggest
sub-cluster in Search Console (Nashik Road railway station <-> Trimbakeshwar)."""
from nt import aeo, articlekit
from nt.render import ext_link

from . import common

PATH = "/transport/nashik-road-station-to-trimbakeshwar/"
TITLE = "Nashik Road Station to Trimbakeshwar: Distance and Options"
H1 = "Nashik Road Railway Station to Trimbakeshwar: Distance, Bus, Auto and Cab Options"
DESC = "Nashik Road railway station is about 36–40 km from Trimbakeshwar (reported). Compare cab, bus via CBS and shared options, with a Kumbh 2027 travel note."


def build():
    h = common.distances()["headline"]
    st = common.row("station")
    quick = ("Nashik Road railway station is about %s km from Trimbakeshwar by road, further than the city centre. "
             "The usual choices are a taxi direct, or a bus or auto to the CBS and then an MSRTC bus. We have no verified "
             "journey time, fare or last-bus time, so confirm before you travel." % h["stationKm"])
    body = """
    <p>Most visitors reach Nashik by train at <strong>Nashik Road</strong>, the city&rsquo;s main railway station, and many want Trimbakeshwar (also written Trimbak, Tryambakeshwar or Trayambakam) the same day. Trimbakeshwar has no direct rail service that we could find, so the last leg is by road. This guide compares the ways to do it. For the other starting points, see the <a href="/blog/trimbakeshwar-to-nashik-distance-route/">Nashik to Trimbakeshwar distance guide</a>.</p>

    <h2 id="how-far-is-nashik-road-station-from-trimbakeshwar">How far is Nashik Road station from Trimbakeshwar?</h2>
    %(table)s
    %(measured)s
    <p>The reported figures run from about 36 km to about 40 km depending on the source and the route counted. Because Nashik Road is several kilometres from the city centre, it is further than the CBS (about %(cbs)s km, reported). Trimbakeshwar to Nashik Road railway station is the same distance in the other direction.</p>

    <h2 id="which-option-should-you-choose">Which way should you go from the station?</h2>
    <div class="table-scroll" tabindex="0" role="region" aria-label="Table: Options from Nashik Road station to Trimbakeshwar">
    <table class="key-facts"><caption>Options from Nashik Road station to Trimbakeshwar</caption>
      <thead><tr><th scope="col">Option</th><th scope="col">Best when</th><th scope="col">What we have not verified</th></tr></thead>
      <tbody>
        <tr><th scope="row">Taxi or cab direct</th><td>You have luggage, family or a tight schedule; fewest changes.</td><td>Fares and journey time. Agree the fare (one way, or a day trip with waiting time) before you set off.</td></tr>
        <tr><th scope="row">Bus or auto to the CBS, then an MSRTC bus</th><td>You want the lowest cost and can handle a change.</td><td>Bus numbers, departure frequency, fares and the last bus back. The change at the CBS adds waiting time.</td></tr>
        <tr><th scope="row">Shared jeep (from the city)</th><td>You are already in the city and are flexible on timing.</td><td>Where jeeps leave from, how often, and the fare.</td></tr>
        <tr><th scope="row">Pre-booked intercity cab</th><td>You arrive at an awkward hour.</td><td>Availability and fares; they vary by demand.</td></tr>
      </tbody></table></div>

    <h2 id="how-do-you-get-from-the-station-to-the-cbs">How do you reach Trimbakeshwar by bus via the CBS?</h2>
    <p>The erail station page for Nashik Road describes the public-transport route as a bus from the station to the Nashik <strong>CBS</strong> (Central Bus Stand) and then a bus to Trimbakeshwar (%(erail)s). In practice:</p>
    <ol class="route-steps">
      <li><strong>Leave the station</strong> and ask for the bus or auto to the CBS. We have not verified the station&rsquo;s exits, bus bays or any prepaid counter, so check the signs on arrival.</li>
      <li><strong>At the CBS</strong>, ask the enquiry desk for the Trimbakeshwar bus and platform. MSRTC publishes its own service information (see <a href="/sources/">our sources</a>).</li>
      <li><strong>In Trimbakeshwar</strong>, confirm the last bus back before you queue for darshan. We do not publish a last-bus time because we have none that is verified.</li>
    </ol>

    <h2 id="how-long-does-it-take">How long does it take from Nashik Road to Trimbakeshwar?</h2>
    <p>We have no verified journey time from the station. The city-centre drive is estimated at %(drive)s in normal traffic (not yet verified), and Nashik Road adds distance on top of that, so plan on more, and add a buffer for the change at the CBS if you go by bus. On busy days the time can be much longer.</p>

    <h2 id="what-changes-during-kumbh-mela-2027">What changes during Kumbh Mela 2027?</h2>
    <p>Nashik Road is the station most Kumbh travellers are expected to use. The Railways describe special trains as planned (reported; no timetable located), and no official road-traffic, parking or shuttle plan for the Nashik&ndash;Trimbakeshwar route has been located. Expect crowds at the station and on the road on the reported Amrit Snan dates, and check <a href="/kumbh-mela-2027/live-updates/">live updates</a> and the <a href="/kumbh-mela-2027/">Kumbh Mela 2027 hub</a> before you travel.</p>

    <h2 id="plan-the-rest-of-your-trip">Plan the rest of your trip</h2>
    <ul>
      <li><a href="/discover-nashik/trimbakeshwar/">Trimbakeshwar Temple guide</a></li>
      <li><a href="/discover-nashik/panchavati/">Panchavati and Ramkund</a>, and <a href="/transport/trimbakeshwar-to-panchavati-ramkund/">how to travel between Trimbakeshwar and Ramkund</a></li>
      <li><a href="/blog/how-to-reach-nashik-for-kumbh-mela/">How to reach Nashik for Kumbh Mela 2027</a></li>
      <li><a href="/transport/">Transport hub</a></li>
    </ul>
""" % {"table": common.matrix(["station", "cbs"], "Road distance to Trimbakeshwar: Nashik Road station compared with the CBS"),
       "measured": common.how_we_measured(), "cbs": h["cbsKm"], "drive": h["driveTime"],
       "erail": ext_link("https://erail.in/info/nasik-road-railway-station-NK", "erail", item="erail-nashik-road")}
    body += aeo.source_list([
        ("Distance from Nashik Road station", ["nashik-district", ("Housing.com", "https://housing.com/news/nearest-railway-station-to-trimbakeshwar-shiva-temple"),
                                                ("DistancesFrom", "https://www.distancesfrom.com/in/distance-from-Trimbakeshwar-Temple-to-Nashik-Road-Railway-Station-Nashik/DistanceHistory/4808378.aspx")]),
        ("Bus link from the station via the CBS", [("erail: Nasik Road railway station", "https://erail.in/info/nasik-road-railway-station-NK"), "msrtc"]),
        ("Trains and special Kumbh services", ["central-railway", "ntes", "pib-rail-upgrade"]),
    ])
    faq = [
        ("How far is Nashik Road railway station from Trimbakeshwar?",
         "About %s km by road (reported by the Nashik District tourism site, Housing.com and DistancesFrom; not yet measured by our editor)." % h["stationKm"]),
        ("How do I get from Nashik Road station to Trimbakeshwar?",
         "Take a taxi direct, or go by bus or auto to the Nashik CBS and then an MSRTC bus to Trimbakeshwar. Confirm bus details with MSRTC; we publish no timetable or fares."),
        ("Is there a train from Nashik Road to Trimbakeshwar?",
         "We have not found a direct rail service to Trimbakeshwar. Nashik Road is the nearest major station; continue by road."),
        ("What is the last bus from Trimbakeshwar back to Nashik?",
         "We have no verified last-bus time. Ask at the Trimbakeshwar bus stand or check with MSRTC on the day, and keep a taxi as a fallback."),
    ]
    side = articlekit.sidebar(
        articlekit.side_card("Key facts (reported)", '<ul class="date-list"><li><span class="dl">By road</span><span class="dv">About %s km</span></li><li><span class="dl">Direct train</span><span class="dv">None found</span></li></ul>' % h["stationKm"]),
        articlekit.side_links("Related", [("/blog/trimbakeshwar-to-nashik-distance-route/", "Nashik to Trimbakeshwar distance"),
                                          ("/transport/trimbakeshwar-to-panchavati-ramkund/", "Trimbakeshwar to Ramkund"),
                                          ("/discover-nashik/trimbakeshwar/", "Trimbakeshwar Temple"),
                                          ("/transport/", "Transport hub")]))
    articlekit.build(PATH, title=TITLE, h1=H1,
                     lede="The last leg from Nashik's main railhead to the Jyotirlinga, compared option by option.",
                     description=DESC, crumbs=articlekit.crumbs_for("Nashik Road station to Trimbakeshwar", ("Transport", "/transport/")),
                     body=body, side=side, faq=faq, quick=quick, published="2026-11-22", topic_label="Transport",
                     about={"@type": "TouristAttraction", "name": "Trimbakeshwar Shiva Temple", "url": "https://nashiktourism.com/discover-nashik/trimbakeshwar/"})
