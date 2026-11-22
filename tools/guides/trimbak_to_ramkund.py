"""/transport/trimbakeshwar-to-panchavati-ramkund/ — Trimbakeshwar <-> Panchavati / Ramkund."""
from nt import aeo, articlekit
from nt.render import ext_link

from . import common

PATH = "/transport/trimbakeshwar-to-panchavati-ramkund/"
TITLE = "Trimbakeshwar to Panchavati and Ramkund: Distance and Options"
H1 = "Trimbakeshwar to Panchavati and Ramkund: Distance, Bus, Jeep and Cab Options"
DESC = "Trimbakeshwar to Ramkund and Panchavati is about 30–31 km (roughly 1 hr) by road. Google Maps, 22 Nov 2026. Bus, jeep and cab options and Kumbh 2027 notes."


def build():
    h = common.distances()["headline"]
    quick = ("Trimbakeshwar is about %s km from Ramkund in Panchavati by road, roughly %s on Google Maps (22 November 2026). "
             "Go by MSRTC bus via the CBS, shared jeep or cab. We have no verified fare or last-bus time; on Kumbh days allow far longer."
             % (h["ramkundKm"], h["ramkundTime"]))
    body = """
    <p>Panchavati and Ramkund, on the Godavari in Nashik, and Trimbakeshwar (also written Trimbak or Tryambakeshwar), are the two sites of Kumbh Mela 2027, and many pilgrims visit both. This guide covers the journey between them. The full distance table for other starting points is in the <a href="/blog/trimbakeshwar-to-nashik-distance-route/">Nashik to Trimbakeshwar distance guide</a>.</p>

    <h2 id="how-far-is-ramkund-from-trimbakeshwar">How far is Ramkund from Trimbakeshwar?</h2>
    %(table)s
    %(measured)s
    <p>Google Maps showed driving routes of 30.3, 30.5 and 31.1 km from Ramkund to Trimbakeshwar Jyotirling Mandir (measured 22 November 2026; times vary with traffic). That is close to the Nashik CBS figure (about %(cbs)s km, also measured). The distance is the same from Ramkund to Trimbakeshwar as from Trimbakeshwar to Ramkund. Tapovan and Kapaleshwar temple are in the same part of the city.</p>

    <h2 id="how-do-you-travel-between-ramkund-and-trimbakeshwar">How do you travel between Ramkund and Trimbakeshwar?</h2>
    <ul>
      <li><strong>MSRTC bus:</strong> MSRTC buses are reported to run to Trimbakeshwar from the Nashik CBS (%(erail)s). Our <a href="/blog/ramkund-ghat-nashik-guide/">Ramkund guide</a> and the transport hub note that the Panchavati bus stand is nearer Ramkund; whether Trimbakeshwar buses call there has not been verified. Timings, fares and the last bus back are not verified.</li>
      <li><strong>Shared jeep:</strong> a common way to make the trip; pickup points, frequency and fare are not verified. Ask locally.</li>
      <li><strong>Cab or taxi:</strong> door-to-door from your hotel in Panchavati. Agree the fare, and whether it includes waiting and the return, before you set off.</li>
      <li><strong>Self-drive:</strong> use a maps app for the route; do not assume parking close to Ramkund or the temple on busy days.</li>
    </ul>

    <h2 id="how-long-does-it-take">How long does the journey take?</h2>
    <p>Google Maps showed 1 hr to 1 hr 7 min by road from Ramkund on the late morning of 22 November 2026; times vary with traffic. Plan on more at peak hours, and much more on festival and Amrut Snan (Amrut Snan) days.</p>

    <h2 id="what-about-the-two-kumbh-sites">Can you do both Kumbh sites on the same day?</h2>
    <p>The third Amrut Snan is on 11 September 2027 at Ramtirth (Ramkund), Nashik, and on 12 September 2027 at Kushavarta Tirth, Trimbakeshwar, according to the Authority&rsquo;s official FAQ (press reports describe these as the Vaishnava and Shaiva akharas&rsquo; snans; see the <a href="/kumbh-mela-2027/#dates">dates table on the Kumbh hub</a>). No official traffic, parking or shuttle plan between the two has been located. On a busy date, consider seeing one site per day rather than both, and check <a href="/kumbh-mela-2027/live-updates/">live updates</a> first.</p>

    <h2 id="what-to-see-next">What to see next</h2>
    <ul>
      <li><a href="/discover-nashik/panchavati/">Panchavati and Ramkund guide</a></li>
      <li><a href="/discover-nashik/trimbakeshwar/">Trimbakeshwar Temple guide</a></li>
      <li><a href="/transport/nashik-road-station-to-trimbakeshwar/">Nashik Road station to Trimbakeshwar</a></li>
      <li><a href="/blog/nashik-2-day-itinerary/">Nashik two-day itinerary</a></li>
    </ul>
""" % {"table": common.matrix(["ramkund", "cbs", "tapovan", "kapaleshwar"], "Road distance to Trimbakeshwar from Ramkund, Panchavati and nearby"),
       "measured": common.how_we_measured(), "cbs": h["cbsKm"], "drive": h["ramkundTime"],
       "erail": ext_link("https://erail.in/info/nasik-road-railway-station-NK", "erail", item="erail-nashik-road")}
    body += aeo.source_list([
        ("City distance used as a guide for Ramkund", ["nashik-district"]),
        ("Ramkund being about 2 km from the CBS", [("Trawell: Nashik itineraries", "https://www.trawell.in/itineraries/nashik/2-day-trip/nashik-trimbakeshwar-brahmagiri-hill")]),
        ("MSRTC bus services", ["msrtc"]),
        ("Kumbh dates and arrangements", ["ntka"]),
    ])
    faq = [
        ("How far is Trimbakeshwar from Ramkund?",
         "About %s km by road, roughly %s (Google Maps driving routes of 30.3, 30.5 and 31.1 km, measured 22 November 2026; times vary with traffic)." % (h["ramkundKm"], h["ramkundTime"])),
        ("How do I get from Ramkund to Trimbakeshwar?",
         "By MSRTC bus from the CBS, shared jeep or cab. We publish no timetable or fares because none is verified."),
        ("How far is Trimbakeshwar from Panchavati?",
         "Panchavati is the area around Ramkund, so expect about the same as from Ramkund: roughly %s km. We measured Ramkund itself on Google Maps (22 November 2026)." % h["ramkundKm"]),
        ("Can I visit Ramkund and Trimbakeshwar on the same day during Kumbh?",
         "It is possible on quiet days, but no traffic or shuttle plan has been announced. On busy dates see one site per day and allow far longer."),
    ]
    side = articlekit.sidebar(
        articlekit.side_card("Key facts (Google Maps, 22 Nov 2026)", '<ul class="date-list"><li><span class="dl">By road</span><span class="dv">About %s km</span></li><li><span class="dl">Drive time</span><span class="dv">%s</span></li></ul>' % (h["ramkundKm"], h["ramkundTime"])),
        articlekit.side_links("Related", [("/blog/trimbakeshwar-to-nashik-distance-route/", "Nashik to Trimbakeshwar distance"),
                                          ("/transport/nashik-road-station-to-trimbakeshwar/", "Nashik Road station to Trimbakeshwar"),
                                          ("/discover-nashik/panchavati/", "Panchavati and Ramkund"),
                                          ("/kumbh-mela-2027/", "Kumbh Mela 2027 hub")]))
    articlekit.build(PATH, title=TITLE, h1=H1,
                     lede="Between the two Kumbh Mela sites: distance, options and what to check.",
                     description=DESC, crumbs=articlekit.crumbs_for("Trimbakeshwar to Panchavati and Ramkund", ("Transport", "/transport/")),
                     body=body, side=side, faq=faq, quick=quick, published="2026-11-22", topic_label="Transport",
                     about={"@type": "TouristAttraction", "name": "Ramkund, Panchavati", "url": "https://nashiktourism.com/discover-nashik/panchavati/"})
