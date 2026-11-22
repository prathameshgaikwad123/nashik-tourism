"""Tests for the SEO / answer-engine layer: components, robots policy, redirects, distance data."""
import importlib.util
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, ".."))
REPO = os.path.normpath(os.path.join(TOOLS, ".."))
sys.path.insert(0, TOOLS)

from nt import aeo, enums, store  # noqa: E402


def load_script(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), os.path.join(TOOLS, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class QuickAnswers(unittest.TestCase):
    def test_every_guide_quick_answer_is_40_to_60_words(self):
        for path, meta in store.load("pages")["pages"].items():
            qa = meta.get("quickAnswer")
            if qa:
                self.assertTrue(40 <= aeo.word_count(qa) <= 60, "%s: %d words" % (path, aeo.word_count(qa)))


class Faq(unittest.TestCase):
    def test_extract_faq_pairs_visible_questions_and_answers(self):
        html = '<h2 id="x">Frequently Asked Questions</h2><h3>How far?</h3><p>About <b>28</b> km.</p><h3>How long?</h3><p>An hour.</p><!-- BEGIN:NT-VERIFY'
        self.assertEqual(aeo.extract_faq(html), [("How far?", "About 28 km."), ("How long?", "An hour.")])

    def test_no_faq_heading_means_no_schema(self):
        self.assertEqual(aeo.extract_faq("<h2>Other</h2><h3>Q</h3><p>A</p>"), [])


class Affiliate(unittest.TestCase):
    def setUp(self):
        self._old = os.environ.get("NT_AFFILIATE_MAKEMYTRIP")

    def tearDown(self):
        if self._old is None:
            os.environ.pop("NT_AFFILIATE_MAKEMYTRIP", None)
        else:
            os.environ["NT_AFFILIATE_MAKEMYTRIP"] = self._old

    def test_plain_link_when_unset_and_always_sponsored(self):
        os.environ.pop("NT_AFFILIATE_MAKEMYTRIP", None)
        out = aeo.affiliate_link("https://www.makemytrip.com/hotels/nashik-hotels.html", "Hotels")
        self.assertIn('href="https://www.makemytrip.com/hotels/nashik-hotels.html"', out)
        self.assertIn('rel="noopener sponsored nofollow"', out)

    def test_params_appended_from_env(self):
        os.environ["NT_AFFILIATE_MAKEMYTRIP"] = "affid=42"
        self.assertIn("?affid=42", aeo.affiliate_link("https://www.makemytrip.com/x.html", "Hotels"))

    def test_apply_affiliate_is_idempotent_and_reversible(self):
        mod = load_script("apply-affiliate")
        tag = '<a href="https://www.makemytrip.com/hotels/nashik-hotels.html" class="b">Hotels</a>'
        os.environ["NT_AFFILIATE_MAKEMYTRIP"] = "affid=42"
        once = mod.A_TAG.sub(mod.fix, tag)
        twice = mod.A_TAG.sub(mod.fix, once)
        self.assertEqual(once, twice)
        self.assertIn("affid=42", once)
        self.assertIn("sponsored", once)
        os.environ.pop("NT_AFFILIATE_MAKEMYTRIP")
        back = mod.A_TAG.sub(mod.fix, once)
        self.assertNotIn("affid", back)
        self.assertNotIn("data-aff-base", back)


class Robots(unittest.TestCase):
    def test_every_required_crawler_is_allowed_in_the_shared_group(self):
        txt = load_script("build-seo-files").robots()
        for ua in ["Googlebot", "Bingbot", "Applebot", "DuckDuckBot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot",
                   "Perplexity-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "Google-Extended", "Applebot-Extended",
                   "Amazonbot", "meta-externalagent", "CCBot"]:
            self.assertIn("User-agent: %s\n" % ua, txt, ua)
        self.assertNotIn("Disallow: /\n", txt)
        self.assertIn("Sitemap: https://nashiktourism.com/sitemap.xml", txt)
        self.assertIn("Cloudflare", txt)
        self.assertNotIn("Disallow: /search", txt)   # /search/ stays crawlable so its noindex can be read

    def test_disallows_apply_to_named_crawlers(self):
        txt = load_script("build-seo-files").robots()
        first_group = txt.split("User-agent: *")[0]
        self.assertNotIn("Disallow:", first_group)           # named agents are stacked, rules follow once
        self.assertIn("Disallow: /*?utm_", txt.split("User-agent: *")[1])


class Redirects(unittest.TestCase):
    def test_no_chains_loops_or_duplicates(self):
        rows = json.load(open(os.path.join(REPO, "data", "redirects.json"), encoding="utf-8"))["redirects"]
        srcs = [r["from"] for r in rows]
        self.assertEqual(len(srcs), len(set(srcs)), "duplicate redirect source")
        for r in rows:
            self.assertNotIn(r["to"], srcs, "redirect chain: %s -> %s" % (r["from"], r["to"]))
            self.assertNotEqual(r["from"], r["to"])
            self.assertTrue(r["to"].startswith("/") and r["to"].endswith("/"), r["to"])


class DeliberateNotFounds(unittest.TestCase):
    def test_pages_with_no_equivalent_stay_404(self):
        rows = json.load(open(os.path.join(REPO, "data", "redirects.json"), encoding="utf-8"))["redirects"]
        srcs = {r["from"].rstrip("/") for r in rows}
        for gone in ("/buddha-vihar", "/radha-nikunj", "/gayatri-mata-mandir"):
            self.assertNotIn(gone, srcs)
            self.assertFalse(os.path.isfile(os.path.join(REPO, "nashiktourism", gone.strip("/"), "index.html")))

    def test_requested_search_console_redirects_exist(self):
        rows = {r["from"]: r["to"] for r in json.load(open(os.path.join(REPO, "data", "redirects.json"), encoding="utf-8"))["redirects"]}
        self.assertEqual(rows["/blog/best-places-to-visit-in-nashik/"], "/discover-nashik/")
        self.assertEqual(rows["/sita-guha"], "/discover-nashik/panchavati/")


class Distances(unittest.TestCase):
    def test_statuses_and_verification_rules(self):
        d = json.load(open(os.path.join(REPO, "data", "distances.json"), encoding="utf-8"))
        for r in d["rows"]:
            self.assertIn(r["status"], enums.FACT_STATUS, r["id"])
            self.assertIn(r["timeStatus"], enums.FACT_STATUS, r["id"])
            if r["status"] == "verified":
                self.assertTrue(r.get("verifiedBy") and r.get("verifiedAt") and r.get("sources"), "%s marked verified without evidence" % r["id"])
            if r["status"] == "disputed":
                self.assertGreaterEqual(len(r["sources"]), 2, "%s: disputed needs the competing sources" % r["id"])
            for s in r["sources"]:
                self.assertTrue(s["url"] is None or s["url"].startswith("https://"))

    def test_headline_matches_rows(self):
        d = json.load(open(os.path.join(REPO, "data", "distances.json"), encoding="utf-8"))
        rows = {r["id"]: r for r in d["rows"]}
        self.assertIn(d["headline"]["cbsKm"], rows["cbs"]["km"])
        self.assertIn(d["headline"]["stationKm"], rows["station"]["km"])


class NoPersonalNames(unittest.TestCase):
    def test_no_personal_name_in_source_or_data(self):
        banned = ("prath" + "amesh", "gaik" + "wad")
        for root in ("data", "tools", "nashiktourism", "docs"):
            for dp, _d, files in os.walk(os.path.join(REPO, root)):
                if "__pycache__" in dp:
                    continue
                for f in files:
                    if f.endswith((".json", ".py", ".html", ".md", ".txt", ".js", ".xml", ".yml")) and f != "test_seo.py":
                        t = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read().lower()
                        for b in banned:
                            self.assertNotIn(b, t, "%s contains %r" % (os.path.join(dp, f), b))

    def test_png_assets_carry_no_author_metadata(self):
        for f in ("logo-purple.png", "logo-white.png"):
            data = open(os.path.join(REPO, "nashiktourism", f), "rb").read().lower()
            self.assertNotIn(b"pdf:author", data)


class SponsoredRules(unittest.TestCase):
    def test_sponsored_page_cannot_be_verified(self):
        from nt import validate
        r = validate.Report()
        validate.check_pages(r, {"pages": {"/x/": {"sponsored": True, "verificationStatus": "verified", "lastVerified": "2026-11-01"}}})
        self.assertTrue(r.errors)
        r = validate.Report()
        validate.check_pages(r, {"pages": {"/x/": {"sponsored": True, "verificationStatus": "not_verified", "lastVerified": None}}})
        self.assertFalse(r.errors)

    def test_sponsored_block_is_labelled_and_never_verified(self):
        out = aeo.sponsored_block("<p>Stay with us</p>", "Example Hotel")
        self.assertIn("Sponsored", out)
        self.assertNotIn("st-verified", out)
        self.assertIn("not marked Verified", out)


class Components(unittest.TestCase):
    def test_claim_chip_only_says_verified_for_verified(self):
        self.assertIn("Verified 22 Nov 2026", aeo.claim("verified", "NTKA", "https://x.example/", "2026-11-22"))
        self.assertNotIn("Verified", aeo.claim("reported", date="2026-11-22"))
        self.assertIn("Reported, not confirmed", aeo.claim("reported"))

    def test_json_ld_nodes(self):
        art = aeo.article_ld("/x/", "H", "D", "2026-04-01", "2026-05-01")
        self.assertEqual(art["author"]["@type"], "Organization")
        self.assertEqual(art["author"]["name"], "NashikTourism.com Editorial Team")
        self.assertFalse(hasattr(aeo, "person_ld"))
        self.assertNotIn("sameAs", aeo.organization_ld() if not aeo.seo()["organization"]["sameAs"] else {})

    def test_sponsored_label_is_visible_text(self):
        self.assertIn(">Sponsored<", aeo.sponsored_label())


if __name__ == "__main__":
    unittest.main()
