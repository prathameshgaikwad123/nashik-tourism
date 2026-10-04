"""Tests for the monitoring pipeline: change detection and the AI guard rails."""
import datetime as dt
import importlib.util
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from nt import classify, net, store  # noqa: E402

spec = importlib.util.spec_from_file_location("monitor", os.path.join(HERE, "..", "monitor-sources.py"))
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)

SRC = {"id": "t", "name": "Test Authority", "category": "kumbh", "reliability": "official", "url": "https://example.gov.in/"}
TEXT = "Notice: Kushavarta Tirtha will remain closed to devotees until 31 October 2026 for renovation works."


def reply(**kw):
    out = {"relevant": True, "title": "Kushavarta Tirtha closed until 31 October", "summary": "The tank is closed for renovation until 31 October 2026.",
           "category": "Kumbh", "status": "developing", "tags": ["kushavarta"], "quotes": ["remain closed to devotees until 31 October 2026"], "confidence": 0.9}
    out.update(kw)
    return lambda body: json.dumps(out)


class Classifier(unittest.TestCase):
    def test_no_key_falls_back_to_a_low_confidence_heuristic(self):
        os.environ.pop("ANTHROPIC_API_KEY", None)
        r = classify.classify(SRC, "official", TEXT)
        self.assertEqual(r["confidence"], 0.2)
        self.assertIn("editor must read", r["note"])

    def test_supported_summary_keeps_its_confidence(self):
        r = classify.classify(SRC, "official", TEXT, transport=reply())
        self.assertEqual(r["category"], "Kumbh")
        self.assertAlmostEqual(r["confidence"], 0.9)

    def test_fabricated_quote_caps_confidence(self):
        r = classify.classify(SRC, "official", TEXT, transport=reply(quotes=["the Chief Minister inaugurated the tank"]))
        self.assertLessEqual(r["confidence"], 0.2)
        self.assertIn("quote check failed", r["note"])

    def test_no_quotes_caps_confidence(self):
        r = classify.classify(SRC, "official", TEXT, transport=reply(quotes=[]))
        self.assertLessEqual(r["confidence"], 0.2)

    def test_unknown_category_is_rejected(self):
        r = classify.classify(SRC, "official", TEXT, transport=reply(category="Politics"))
        self.assertEqual(r["confidence"], 0.2)           # fell back to the heuristic
        self.assertIn("rejected", r["note"])

    def test_irrelevant_text_is_dropped(self):
        r = classify.classify(SRC, "official", "Click here to subscribe to our newsletter today please.", transport=lambda b: '{"relevant": false}')
        self.assertFalse(r["relevant"])

    def test_garbage_output_falls_back(self):
        r = classify.classify(SRC, "official", TEXT, transport=lambda b: "I am sorry, I cannot help with that.")
        self.assertEqual(r["confidence"], 0.2)


class ChangeDetection(unittest.TestCase):
    def test_digit_only_churn_is_not_news(self):
        old = "Visitors today: 100234\nThe Authority plans the Simhastha."
        new = "Visitors today: 100999\nThe Authority plans the Simhastha."
        self.assertEqual(monitor.added_lines(old, new), [])

    def test_new_sentence_is_detected(self):
        old = "The Authority plans the Simhastha."
        new = old + "\nA new traffic advisory has been issued for the ring road."
        self.assertEqual(monitor.added_lines(old, new), ["A new traffic advisory has been issued for the ring road."])

    def test_schedule(self):
        now = store.parse_dt("2026-10-05T10:00:00+05:30")
        self.assertTrue(monitor.is_due({"checkFrequency": "daily"}, {}, now))
        self.assertFalse(monitor.is_due({"checkFrequency": "daily"}, {"lastCheckedAt": "2026-10-05T04:00:00+05:30"}, now))
        self.assertTrue(monitor.is_due({"checkFrequency": "daily"}, {"lastCheckedAt": "2026-10-04T04:00:00+05:30"}, now))
        self.assertFalse(monitor.is_due({"checkFrequency": "manual"}, {}, now))

    def test_visible_text_strips_chrome(self):
        t = net.visible_text("<nav>Menu</nav><p>Alpha beta</p><script>var x=1</script><footer>Foot</footer>")
        self.assertEqual(t, "Alpha beta")


if __name__ == "__main__":
    unittest.main()
