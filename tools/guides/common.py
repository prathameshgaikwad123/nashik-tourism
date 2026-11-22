"""Shared pieces for the generated guides: the distance data and its tables."""
import json
import os

from nt import aeo
from nt.paths import DATA
from nt.render import esc, ext_link

CHECKED = "2026-11-22"


def distances():
    with open(os.path.join(DATA, "distances.json"), encoding="utf-8") as fh:
        return json.load(fh)


def row(rid):
    return next(r for r in distances()["rows"] if r["id"] == rid)


def src_links(r):
    out = []
    for s in r.get("sources", []):
        out.append(ext_link(s["url"], esc(s["name"]), item="distance-" + r["id"]) if s.get("url") else esc(s["name"]))
    return out


def km_cell(r):
    return '%s<br>%s' % (esc(r["km"]), aeo.claim(r["status"], date=CHECKED, short=True))


def time_cell(r):
    t = esc(r["time"])
    if r["time"] != "Not yet confirmed":
        t += "<br>" + aeo.claim(r["timeStatus"], short=True)
    return t


def notes_cell(r):
    s = src_links(r)
    out = esc(r["notes"])
    if s:
        out += '<br><span class="muted">Sources: %s</span>' % "; ".join(s)
    return out


def matrix(ids=None, caption="Road distance to Trimbakeshwar from each starting point"):
    rows = distances()["rows"]
    if ids:
        rows = [r for r in rows if r["id"] in ids]
    body = "".join(
        '<tr><th scope="row">%s</th><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            esc(r["origin"]), km_cell(r), time_cell(r), esc(r["cheapest"]), notes_cell(r)) for r in rows)
    return ('<div class="table-scroll" tabindex="0" role="region" aria-label="%s">'
            '<table class="key-facts dist-matrix"><caption>%s</caption><thead><tr>'
            '<th scope="col">Starting point</th><th scope="col">By road to Trimbakeshwar</th><th scope="col">Typical drive</th>'
            '<th scope="col">Cheapest public option</th><th scope="col">Notes and sources</th></tr></thead>'
            '<tbody>%s</tbody></table></div>' % (esc("Table: " + caption), esc(caption), body))


def how_we_measured():
    return '<p class="matrix-note"><strong>How we measured.</strong> %s Always check the live route on a maps app for your own starting point.</p>' % esc(distances()["method"])


SIGNUP_LINK = '<p class="matrix-note">Want a message when a Kumbh transport notice changes? See the <a href="/kumbh-mela-2027/#updates-signup">Kumbh 2027 updates</a> sign-up.</p>'
