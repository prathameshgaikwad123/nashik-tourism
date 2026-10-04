"""
Tests for the rules that keep the site honest.

    python3 -m unittest discover -s tools/tests -v

They exercise tools/nt directly with in-memory records, so they never touch /data
or the network.
"""
import copy
import datetime as dt
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from nt import enums, lifecycle, render, risk, store, validate  # noqa: E402

IST = store.IST


def update(**kw):
    u = {"id": "u1", "title": "Ramkund steps repainted", "summary": "Work finished.", "category": "Local",
         "status": "confirmed", "contentStatus": "published", "sourceName": "Nashik Municipal Corporation",
         "sourceUrl": "https://example.gov.in/x", "publishedAt": "2026-10-01", "verifiedAt": "2026-10-02",
         "lastCheckedAt": "2026-10-03", "expiresAt": None, "author": "Ed", "tags": []}
    u.update(kw)
    return u


class RiskPolicy(unittest.TestCase):
    def test_roads_and_safety_are_always_high_risk(self):
        self.assertTrue(risk.is_high_risk(update(category="Roads")))
        self.assertTrue(risk.is_high_risk(update(category="Safety")))

    def test_keywords_catch_high_risk_filed_under_a_low_risk_category(self):
        for text in ["Kushavarta closed to devotees until 31 October", "New parking rules announced",
                     "Amrit Snan date changed", "E-pass registration opens", "Hotel fares revised to Rs 4000",
                     "Ambulance deployment announced", "Section 144 order issued"]:
            self.assertTrue(risk.is_high_risk(update(title=text, category="Local")), text)

    def test_ordinary_item_is_low_risk(self):
        self.assertFalse(risk.is_high_risk(update()))

    def test_auto_publish_is_off_by_default_and_never_for_high_risk(self):
        low = update(confidence=0.99)
        self.assertFalse(risk.may_auto_publish(low, {"pipeline": {}}, "official"))
        cfg = {"pipeline": {"autoPublishLowRisk": True, "autoPublishTiers": ["official"], "minConfidence": 0.9}}
        self.assertTrue(risk.may_auto_publish(low, cfg, "official"))
        self.assertFalse(risk.may_auto_publish(low, cfg, "reliable_news"))
        self.assertFalse(risk.may_auto_publish(update(category="Roads", confidence=0.99), cfg, "official"))
        self.assertFalse(risk.may_auto_publish(update(confidence=0.5), cfg, "official"))


class Validation(unittest.TestCase):
    sources = {"s1": {"id": "s1"}}

    def run_updates(self, *items):
        r = validate.Report()
        validate.check_updates(r, {"updates": list(items)}, self.sources)
        return r

    def test_valid_update_passes(self):
        self.assertEqual(self.run_updates(update()).errors, [])

    def test_high_risk_live_needs_named_approver(self):
        r = self.run_updates(update(category="Roads"))
        self.assertTrue(any("approvedBy" in e for e in r.errors))
        ok = self.run_updates(update(category="Roads", approvedBy="Ed", approvedAt="2026-10-03"))
        self.assertEqual(ok.errors, [])

    def test_draft_high_risk_is_allowed(self):
        self.assertEqual(self.run_updates(update(category="Roads", contentStatus="draft")).errors, [])

    def test_confirmed_needs_verification_and_source(self):
        self.assertTrue(self.run_updates(update(verifiedAt=None)).errors)
        self.assertTrue(self.run_updates(update(sourceUrl=None)).errors)

    def test_non_https_source_rejected(self):
        self.assertTrue(self.run_updates(update(sourceUrl="http://example.com")).errors)

    def test_expiry_before_publication_rejected(self):
        self.assertTrue(self.run_updates(update(expiresAt="2026-09-01")).errors)

    def fact(self, **kw):
        f = {"id": "f.one", "subject": "S", "fact": "F", "value": "v", "display": "v", "status": "reported",
             "source": {"sourceId": "s1", "name": "N", "url": "https://example.gov.in/p"}, "verifyWith": [], "leads": [],
             "alternatives": [], "verifiedAt": None, "verifiedBy": None}
        f.update(kw)
        return f

    def run_facts(self, f):
        r = validate.Report()
        validate.check_facts(r, {"facts": [f]}, self.sources)
        return r

    def test_verified_fact_requires_source_date_and_verifier(self):
        self.assertTrue(self.run_facts(self.fact(status="verified")).errors)
        ok = self.fact(status="verified", verifiedAt="2026-10-01", verifiedBy="Ed")
        self.assertEqual(self.run_facts(ok).errors, [])
        no_url = copy.deepcopy(ok)
        no_url["source"]["url"] = None
        self.assertTrue(self.run_facts(no_url).errors)

    def test_disputed_fact_must_list_alternatives(self):
        self.assertTrue(self.run_facts(self.fact(status="disputed")).errors)
        self.assertEqual(self.run_facts(self.fact(status="disputed", alternatives=[{"value": "a"}, {"value": "b"}])).errors, [])

    def test_accessible_requires_verification(self):
        r = validate.Report()
        validate.check_accessibility(r, {"statuses": [{"id": s} for s in enums.ACCESS_STATUS],
                                         "places": [{"slug": "x", "status": "verified_accessible", "source": None}],
                                         "topics": []}, {"x": {}}, {})
        self.assertTrue(any("never claim" in e for e in r.errors))

    def test_shipped_data_is_valid(self):
        r = validate.validate_all()
        self.assertEqual(r.errors, [])


class Expiry(unittest.TestCase):
    def test_bare_date_expiry_keeps_the_whole_day(self):
        u = update(expiresAt="2026-10-10")
        noon = dt.datetime(2026, 10, 10, 12, 0, tzinfo=IST)
        next_day = dt.datetime(2026, 10, 11, 0, 1, tzinfo=IST)
        self.assertFalse(render.is_expired(u, noon))
        self.assertTrue(render.is_expired(u, next_day))

    def test_expired_update_is_archived_without_editing(self):
        u = update(expiresAt="2026-10-10", status="confirmed")
        later = dt.datetime(2026, 10, 12, tzinfo=IST)
        self.assertEqual(render.effective_status(u, later), "archived")
        self.assertFalse(render.is_live_update(u, later))
        self.assertTrue(render.is_live_update(u, dt.datetime(2026, 10, 5, tzinfo=IST)))

    def test_drafts_are_never_live(self):
        self.assertFalse(render.is_live_update(update(contentStatus="draft")))

    def test_kumbh_live_items_archive_after_the_mela(self):
        u = update(tags=["kumbh-live"])
        self.assertTrue(render.is_live_update(u, archive_kumbh_live=False))
        self.assertFalse(render.is_live_update(u, archive_kumbh_live=True))


class Lifecycle(unittest.TestCase):
    def phase(self, iso):
        return lifecycle.phase_for(store.parse_dt(iso))["id"]

    def test_phases_follow_the_calendar(self):
        self.assertEqual(self.phase("2026-10-04"), "preparation")
        self.assertEqual(self.phase("2026-10-31"), "mela_open")
        self.assertEqual(self.phase("2027-08-02"), "peak")
        self.assertEqual(self.phase("2027-10-01"), "extended")
        self.assertEqual(self.phase("2028-08-01"), "post_kumbh")
        self.assertEqual(self.phase("2030-01-01"), "evergreen")

    def test_live_band_only_in_peak(self):
        self.assertTrue(lifecycle.profile(store.parse_dt("2027-08-02"))["liveBand"])
        self.assertFalse(lifecycle.profile(store.parse_dt("2026-10-04"))["liveBand"])

    def test_kumbh_live_archives_after_the_mela_closes(self):
        self.assertTrue(lifecycle.profile(store.parse_dt("2028-08-01"))["archiveKumbhLive"])
        self.assertFalse(lifecycle.profile(store.parse_dt("2027-08-02"))["archiveKumbhLive"])

    def test_nav_label_stops_saying_2027(self):
        self.assertEqual(lifecycle.profile(store.parse_dt("2027-08-02"))["navLabel"], "Kumbh 2027")
        self.assertNotIn("2027", lifecycle.profile(store.parse_dt("2029-03-01"))["navLabel"])

    def test_every_day_from_2026_to_2030_has_a_phase(self):
        d = dt.date(2026, 1, 1)
        while d < dt.date(2030, 1, 1):
            self.assertIn(lifecycle.phase_for(dt.datetime.combine(d, dt.time(), tzinfo=IST))["id"], enums.PHASES)
            d += dt.timedelta(days=7)


class Rendering(unittest.TestCase):
    def test_unknown_values_never_print_none_or_null(self):
        self.assertNotIn("None", render.fact_value_html({"display": None}))
        self.assertNotIn("null", render.fact_value_html({"display": ""}).lower())
        self.assertIn("not yet confirmed", render.unconfirmed().lower())

    def test_status_is_never_colour_only(self):
        for status in enums.FACT_STATUS:
            html = render.fact_badge(status)
            self.assertIn("st-i", html)                       # a glyph
            self.assertRegex(html, r">[A-Za-z]")              # and a text label

    def test_weekday_of_second_snan(self):
        self.assertEqual(render.fmt_date("2027-08-31", weekday=True), "Tuesday 31 August 2027")

    def test_pinned_clock(self):
        os.environ["NT_NOW"] = "2027-08-02T09:00:00+05:30"
        try:
            self.assertEqual(store.today().isoformat(), "2027-08-02")
        finally:
            del os.environ["NT_NOW"]


if __name__ == "__main__":
    unittest.main()
