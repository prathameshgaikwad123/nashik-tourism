"""/blog/trimbakeshwar-to-nashik-distance-route/ — the canonical Nashik <-> Trimbakeshwar distance hub.

The URL is unchanged (it carries the site's search equity). Content is generated so the
distance table, the headline figures in the answer box, the Hindi/Marathi block and the
FAQ all read from data/distances.json and cannot disagree with each other.
"""
from nt import aeo, articlekit
from nt.render import esc, ext_link

from . import common

PATH = "/blog/trimbakeshwar-to-nashik-distance-route/"
TITLE = "Nashik to Trimbakeshwar Distance (and Back): km & Time"
H1 = "Nashik to Trimbakeshwar Distance (and Back): km, Time & Routes from Station, CBS and Ramkund"
DESC = "Trimbakeshwar is about 29–30 km from Nashik CBS (55–60 min) and 37–39 km from Nashik Road station. Google Maps, 22 Nov 2026. Distance table, bus, jeep, cab."


def build():
    D = common.distances()
    h = D["headline"]
    cbs, station = common.row("cbs"), common.row("station")
    quick = ("Nashik to Trimbakeshwar is about %s km by road from Nashik city (CBS), roughly %s, and about %s km (roughly %s) from Nashik Road "
             "railway station; Trimbakeshwar to Nashik is the same distance in the other direction. Measured on Google Maps on 22 November 2026; times vary with traffic."
             % (h["cbsKm"], h["cbsTime"], h["stationKm"], h["stationTime"]))

    sources_cbs = "; ".join(common.src_links(cbs))
    body = """
    <!-- VERIFY: CBS, Nashik Road and Ramkund distances are verified (Google Maps, 22 Nov 2026). Every other row is still reported. MSRTC departure point, jeep pickup, app-cab availability, last bus: unverified. See VERIFY.md -->
    <p>Nashik to Trimbakeshwar and Trimbakeshwar to Nashik are the same road, so the distance is the same whichever way you travel. Trimbakeshwar, with its Jyotirlinga temple and the Kushavarta Kund, is also written <strong>Trimbak</strong>, <strong>Tryambakeshwar</strong>, <strong>Tryambakam</strong>, <strong>Trayambakam</strong> or <strong>Trambakeshwar</strong>; this guide covers all of them.</p>

    <h2 id="how-far-is-trimbakeshwar-from-nashik">How far is it from Nashik to Trimbakeshwar, by starting point?</h2>
    <p>The distance depends on where in Nashik you start. Nashik Road railway station is further than the city centre. Every figure below shows its own status: <strong>Verified</strong> means our editor measured it on Google Maps (driving, 22 November 2026; times vary with traffic); <strong>Reported</strong> means the named sources publish it but our editor has not measured it; <strong>Sources differ</strong> means the published figures disagree and we show all of them; <strong>Not yet verified</strong> means we have no supporting source yet.</p>
    %(matrix)s
    %(measured)s
    <p>For two of the most-searched starting points we have a full guide: <a href="/transport/nashik-road-station-to-trimbakeshwar/">Nashik Road railway station to Trimbakeshwar</a> and <a href="/transport/trimbakeshwar-to-panchavati-ramkund/">Trimbakeshwar to Panchavati and Ramkund</a>.</p>

    <h2 id="is-the-distance-the-same-in-both-directions">Is Nashik to Trimbakeshwar the same distance as Trimbakeshwar to Nashik?</h2>
    <p>Yes. Both journeys use the same road, so the kilometres are the same. The <em>time</em> can differ, because it depends on traffic, the time of day and where in Nashik you start or finish. On busy festival and Amrut Snan days, allow far longer in either direction.</p>

    <h2 id="quick-answers-in-hindi-and-marathi">Quick answers in Hindi and Marathi</h2>
    <div class="lang-block" lang="mr">
      <h3 lang="mr">नाशिक ते त्र्यंबकेश्वर अंतर (मराठी)</h3>
      <p><strong>नाशिक ते त्र्यंबकेश्वर किती किलोमीटर?</strong> नाशिक शहर (CBS) पासून रस्त्याने सुमारे %(cbs)s किमी (साधारण ५५–६० मिनिटे), आणि नाशिक रोड रेल्वे स्थानकापासून सुमारे %(st)s किमी (साधारण १ तास १५ मिनिटे). Google Maps वर २२ नोव्हेंबर २०२६ रोजी मोजलेले; वाहतुकीनुसार वेळ बदलते.</p>
      <p>त्र्यंबकेश्वर ते नाशिक हे अंतरही तेच आहे. निघण्यापूर्वी नकाशा अ‍ॅपवर सध्याची वाहतूक तपासा.</p>
    </div>
    <div class="lang-block" lang="hi">
      <h3 lang="hi">नासिक से त्र्यंबकेश्वर की दूरी (हिंदी)</h3>
      <p><strong>नासिक से त्र्यंबकेश्वर कितने किलोमीटर है?</strong> नासिक शहर (CBS) से सड़क मार्ग से लगभग %(cbs)s किमी (करीब 55–60 मिनट), और नासिक रोड रेलवे स्टेशन से लगभग %(st)s किमी (करीब 1 घंटा 15 मिनट)। Google Maps पर 22 नवंबर 2026 को मापा गया; ट्रैफिक के अनुसार समय बदलता है।</p>
      <p>त्र्यंबकेश्वर से नासिक की दूरी भी यही है। निकलने से पहले मैप ऐप पर मौजूदा ट्रैफिक जाँच लें।</p>
    </div>

    <h2 id="how-to-travel-between-nashik-and-trimbakeshwar">How do you get from Nashik to Trimbakeshwar?</h2>
    <div class="route-cards">
      <div class="route-card"><div class="icon">&#128656;</div><div class="mode">Shared jeep</div><div class="time">Varies</div><div class="cost">Check fares and pickup points locally</div></div>
      <div class="route-card"><div class="icon">&#128661;</div><div class="mode">Cab or taxi</div><div class="time">Varies</div><div class="cost">Agree the fare before you travel</div></div>
      <div class="route-card"><div class="icon">&#128652;</div><div class="mode">MSRTC bus</div><div class="time">Varies</div><div class="cost">Check timings and fares with MSRTC</div></div>
    </div>

    <h3 id="by-shared-jeep">By shared jeep</h3>
    <p>Shared jeeps are one way to travel between Nashik and Trimbakeshwar. Where they leave from, how often they run, how full they must be before leaving, and the fare have not been verified; ask locally or at your hotel.</p>

    <h3 id="by-msrtc-bus">By MSRTC bus</h3>
    <p>MSRTC (the state transport corporation) is reported to run buses between Nashik and Trimbakeshwar from the Nashik <strong>CBS</strong> (Central Bus Stand). The Nashik Road station information page on erail describes the route as a bus to the CBS and then a bus to Trimbakeshwar (%(erail)s). We do not publish bus timings or fares because we have no verified timetable. Check departures, platform and the last return service with MSRTC (see <a href="/sources/">our sources</a>), and do not assume a late-evening return bus.</p>

    <h3 id="by-cab-or-taxi">By cab or taxi</h3>
    <p>A private cab gives door-to-door travel from anywhere in Nashik, including Nashik Road station and the airport. App-based intercity cabs list a Nashik to Trimbakeshwar route (%(uber)s); availability and fares vary by day and demand, and we publish no fares. Ask your hotel or a local operator, and agree the fare (one way, or for a full day with waiting time) before you travel.</p>

    <h3 id="by-road-self-drive">By road (self-drive)</h3>
    <p>Use a current maps app for the route; from the CBS the drive was roughly 55&ndash;60 minutes on Google Maps in late-morning traffic on 22 November 2026, and it can take much longer on busy days. Traffic and parking arrangements for the Mela have not been announced in sources we could locate, so check notices before you set out, and do not assume you can park close to the temple or the Kushavarta Kund on busy days.</p>

    <h2 id="is-there-a-train-to-trimbakeshwar">Is there a train to Trimbakeshwar?</h2>
    <p>We have not found a direct rail service to Trimbakeshwar. The nearest major station is <strong>Nashik Road</strong> (about 37&ndash;39 km by road, measured on Google Maps on 22 November 2026; see the table). The usual approach is to reach Nashik, by train to Nashik Road or by road, and continue to Trimbakeshwar by bus, jeep or cab. Confirm services on the railways&rsquo; own systems (<a href="/sources/">Indian Railways, Central Railway and NTES</a>). The full station-to-temple guide is at <a href="/transport/nashik-road-station-to-trimbakeshwar/">Nashik Road station to Trimbakeshwar</a>.</p>

    <h2 id="what-you-pass-on-the-way">What do you pass between Nashik and Trimbakeshwar?</h2>
    <p>Places commonly mentioned along or near the route include:</p>
    <ul>
      <li><strong>Gangapur Dam</strong>, near Nashik</li>
      <li><strong>Anjaneri Hill</strong>, associated in tradition with Lord Hanuman</li>
      <li><strong>Brahmagiri Mountain</strong>, traditionally associated with the source of the Godavari</li>
      <li><strong>Trimbak town</strong>, at the end of the route, a pilgrim town</li>
    </ul>
    <p>We have not verified distances to these places; check a maps app.</p>

    <h2 id="during-kumbh-mela-2027-what-changes">How will Kumbh Mela 2027 affect the journey?</h2>
    <p>Nashik Kumbh Mela 2027 is reported to be held at two sites, Ramkund in Nashik city and Kushavarta Kund in Trimbakeshwar. Arrangements for the route during the Mela have not been announced in any source we could locate. Keep in mind:</p>
    <ul>
      <li><strong>Traffic restrictions:</strong> no official parking, traffic or vehicle-restriction plan has been located. Restrictions are expected to be set by the police and the Authority and may change from day to day.</li>
      <li><strong>Shuttles and special services:</strong> no shuttle-bus plan between Nashik and Trimbakeshwar has been found. The Railways say special trains are planned, but no numbers, routes or dates have been published.</li>
      <li><strong>Journey time:</strong> it may increase a lot on busy days. We have no verified figure, so allow generous extra time.</li>
      <li><strong>A possible strategy:</strong> consider visiting Trimbakeshwar on a different day from Nashik (Ramkund) rather than trying to do both on a busy date.</li>
    </ul>
    <p>For dates, passes and the latest notices, use the <a href="/kumbh-mela-2027/">Kumbh Mela 2027 hub</a> and <a href="/kumbh-mela-2027/live-updates/">live updates</a>. See also <a href="/blog/how-to-reach-nashik-for-kumbh-mela/">how to reach Nashik for Kumbh Mela 2027</a> and <a href="/blog/kumbh-mela-2027-all-snan-dates/">the reported snan dates</a>.</p>

    <h2 id="which-should-you-visit-first-nashik-or-trimbakeshwar">Which should you visit first, Nashik or Trimbakeshwar?</h2>
    <p>There is no single right order, and we have not found an official recommendation. If you arrive by train at Nashik Road station, it may be simpler to visit Nashik first, then travel to Trimbakeshwar, and return to Nashik for your onward journey. Check temple and Mela notices for both sites before you go.</p>

    <h2 id="places-on-and-near-this-route">Places to visit around Nashik and Trimbakeshwar</h2>
    <ul>
      <li><a href="/discover-nashik/trimbakeshwar/">Trimbakeshwar Temple guide</a>: the Jyotirlinga and Kushavarta Kund</li>
      <li><a href="/discover-nashik/panchavati/">Panchavati and Ramkund</a> and the <a href="/blog/ramkund-ghat-nashik-guide/">Ramkund Ghat guide</a>: the Nashik bathing site</li>
      <li><a href="/discover-nashik/sula-vineyards/">Sula Vineyards</a>: wine tasting near Nashik</li>
      <li><a href="/discover-nashik/pandavleni-caves/">Pandavleni Caves</a>: the Buddhist caves</li>
      <li><a href="/discover-nashik/igatpuri/">Igatpuri</a>: hill country on the Mumbai&ndash;Nashik corridor</li>
      <li><a href="/discover-nashik/bhandardara/">Bhandardara</a> (Ahilyanagar district): Arthur Lake and waterfalls</li>
    </ul>

    <div class="cta-strip">
      <div><h3>Staying in Trimbakeshwar?</h3><p>Rooms may be limited around the Amrut Snan dates, so booking early is sensible. External site, with its own prices and terms.</p></div>
      %(hotel)s
    </div>
""" % {
        "matrix": common.matrix(), "measured": common.how_we_measured(),
        "cbs": h["cbsKm"], "st": h["stationKm"],
        "erail": ext_link("https://erail.in/info/nasik-road-railway-station-NK", "erail", item="erail-nashik-road"),
        "uber": ext_link("https://www.uber.com/in/en/r/intercity/nashik-maharashtra-to-trimbakeshwar-maharashtra/", "Uber Intercity", item="uber-nashik-trimbak"),
        "hotel": aeo.affiliate_link("https://www.makemytrip.com/hotels/nashik-hotels.html", "Search hotels", cls="btn btn-gold"),
    }
    body += aeo.signup_block("distance-hub")
    body += aeo.source_list([
        ("Distance from Nashik city (CBS) and from Nashik Road station", ["nashik-district", ("Housing.com", "https://housing.com/news/nearest-railway-station-to-trimbakeshwar-shiva-temple"),
                                                                      ("DistancesFrom", "https://www.distancesfrom.com/in/distance-from-Trimbakeshwar-Temple-to-Nashik-Road-Railway-Station-Nashik/DistanceHistory/4808378.aspx")]),
        ("Airport, Mumbai, Pune and Shirdi distances", [("Ixigo", "https://ixigo.com/plan/trimbak"), ("Maharashtra Planet", "https://maharashtraplanet.com/?p=2959"),
                                                         ("Rome2Rio (Mumbai)", "https://www.rome2rio.com/s/Mumbai/Trimbak"), ("Rome2Rio (Pune)", "https://www.rome2rio.com/s/Pune/Trimbakeshwar")]),
        ("MSRTC bus services and the last bus back", ["msrtc"]),
        ("Train services", ["indian-railways", "central-railway", "ntes"]),
        ("Kumbh Mela transport, traffic and parking arrangements", ["ntka", "nashik-city-police"]),
    ])

    faq = [
        ("How far is Trimbakeshwar from Nashik Road railway station?",
         "About %s km by road, roughly %s (Google Maps driving routes of 37.3, 38.0 and 38.8 km, measured on 22 November 2026; times vary with traffic). Allow more time than the city figure, because Nashik Road is further from the city centre." % (h["stationKm"], h["stationTime"])),
        ("How far is Trimbakeshwar from Nashik CBS?",
         "About %s km by road, roughly %s (Google Maps driving routes of 29.3, 29.4 and 29.6 km, fastest 56 minutes, measured on 22 November 2026 in late-morning traffic; times vary). The Nashik District tourism site also gives about 30 km from the city." % (h["cbsKm"], h["cbsTime"])),
        ("How far is Trimbakeshwar from Ramkund or Panchavati?",
         "About %s km by road, roughly %s (Google Maps, Ramkund in Panchavati to Trimbakeshwar Jyotirling Mandir, measured 22 November 2026; routes of 30.3, 30.5 and 31.1 km). See <a href=\"/transport/trimbakeshwar-to-panchavati-ramkund/\">Trimbakeshwar to Panchavati and Ramkund</a>." % (h["ramkundKm"], h["ramkundTime"])),
        ("How far is Trimbakeshwar from Nashik (Ozar) airport?",
         "Sources differ: most listings say about 40 km, one says about 55 km. Confirm which flights are operating before you plan around this airport, and pre-book a taxi."),
        ("What is the last bus from Trimbakeshwar to Nashik?",
         "We have no verified last-bus time and do not publish one. Ask at the Trimbakeshwar bus stand or check with MSRTC on the day, and do not assume a late-evening return bus. A shared jeep or cab is the fallback."),
        ("Is there a train to Trimbakeshwar?",
         "We have not found a direct rail service. The nearest major station is Nashik Road, about 37&ndash;39 km away by road (Google Maps, 22 November 2026). Continue by bus, shared jeep or cab."),
        ("How long will the journey take during Kumbh Mela 2027?",
         "No verified figure exists. No official traffic or parking plan has been located, and the journey may take much longer than normal on Amrut Snan (Amrut Snan) and other busy days. Allow generous extra time and check the <a href=\"/kumbh-mela-2027/live-updates/\">live updates</a> before you set out."),
        ("What is the cheapest way to get from Nashik to Trimbakeshwar?",
         "We have not verified fares for any option. An MSRTC bus from the CBS is the usual low-cost choice (reported); check fares with MSRTC, ask locally for shared vehicles, and agree any cab fare before you travel."),
    ]
    side = articlekit.sidebar(
        articlekit.side_card("Key facts (Google Maps, 22 Nov 2026)", '<ul class="date-list"><li><span class="dl">From CBS</span><span class="dv">About %s km, %s</span></li><li><span class="dl">From Nashik Road</span><span class="dv">About %s km, %s</span></li><li><span class="dl">From Ramkund</span><span class="dv">About %s km, %s</span></li></ul>' % (h["cbsKm"], h["cbsTime"], h["stationKm"], h["stationTime"], h["ramkundKm"], h["ramkundTime"])),
        articlekit.side_links("Transport guides", [
            ("/transport/nashik-road-station-to-trimbakeshwar/", "Nashik Road station to Trimbakeshwar"),
            ("/transport/trimbakeshwar-to-panchavati-ramkund/", "Trimbakeshwar to Panchavati and Ramkund"),
            ("/transport/", "Transport hub"),
            ("/blog/how-to-reach-nashik-for-kumbh-mela/", "How to reach Nashik")]),
        articlekit.side_links("Kumbh Mela 2027", [
            ("/kumbh-mela-2027/", "Kumbh Mela 2027 hub"),
            ("/blog/kumbh-mela-2027-all-snan-dates/", "Reported snan dates"),
            ("/blog/where-to-stay-nashik-kumbh-mela/", "Where to stay")]),
    )
    articlekit.build(PATH, title=TITLE, h1=H1,
                     lede="How far Trimbakeshwar is from Nashik, by starting point, with bus, jeep, cab and Kumbh 2027 notes. Same road in both directions.",
                     description=DESC, crumbs=articlekit.crumbs_for("Nashik to Trimbakeshwar distance"),
                     body=body, side=side, faq=faq, quick=quick, published="2026-04-12", topic_label="Distances and transport",
                     about={"@type": "TouristAttraction", "name": "Trimbakeshwar Shiva Temple", "url": "https://nashiktourism.com/discover-nashik/trimbakeshwar/"})
