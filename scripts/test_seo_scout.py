"""Tests for seo_scout.py: page parsing, the checks, the verdict order and the not-ranking floor.

Run from the repo root:
    python3 -m unittest scripts/test_seo_scout.py
No network. The homepages in scripts/fixtures/seo_scout/ are written by hand and hold no client data.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo_scout as ss  # noqa: E402

FIX = Path(__file__).resolve().parent / "fixtures" / "seo_scout"
NICHE, CITY = "fence contractors", "Charlotte, NC"


def page(name: str, url: str = "https://site.example/", headers: dict | None = None) -> dict:
    return ss.parse_page((FIX / f"{name}.html").read_text(), url, headers)


def place(**kw) -> dict:
    base = {"phone": "(704) 555-0133", "postcode": "28202", "city": "Charlotte", "reviews": "40",
            "unclaimed": "", "gbp_description": "yes"}
    base.update(kw)
    return base


def extra(**kw) -> dict:
    base = {"final_url": "https://site.example/", "https": "yes", "robots_block": False, "sitemap_urls": 20,
            "top5_median_reviews": 60}
    base.update(kw)
    return base


def types(found):
    return [f[0] for f in found]


class Helpers(unittest.TestCase):
    def test_digits10_formats(self):
        self.assertEqual(ss.digits10("(704) 555-0100"), "7045550100")
        self.assertEqual(ss.digits10("+1 704.555.0100"), "7045550100")
        self.assertEqual(ss.digits10("+44 7700 900123"), ss.digits10("07700 900123"))
        self.assertEqual(ss.digits10("555-0100"), "")

    def test_service_terms(self):
        t = ss.service_terms("fence contractors")
        self.assertIn("fence", t)
        self.assertIn("fencing", t)
        self.assertNotIn("contractors", t)
        self.assertIn("roofing", ss.service_terms("roofers"))

    def test_country(self):
        self.assertEqual(ss.country_code("Leeds, UK"), "gb")
        self.assertEqual(ss.country_code("Charlotte, NC"), "us")

    def test_robots(self):
        self.assertTrue(ss.robots_blocks_all("User-agent: *\nDisallow: /\n"))
        self.assertFalse(ss.robots_blocks_all("User-agent: *\nDisallow: /wp-admin/\n"))
        self.assertFalse(ss.robots_blocks_all("User-agent: BadBot\nDisallow: /\nUser-agent: *\nDisallow:\n"))

    def test_organic_rows_and_position(self):
        data = [{"searchQuery": {"page": 2}, "organicResults": [{"url": "https://www.late.example/x"}]},
                {"searchQuery": {"page": 1}, "organicResults": [{"url": "https://a.example/"}, {"url": "https://b.example/"}]}]
        rows = ss.organic_rows(data)
        self.assertEqual([r["domain"] for r in rows], ["a.example", "b.example", "late.example"])
        self.assertEqual(ss.organic_position("late.example", rows), 3)
        self.assertIsNone(ss.organic_position("missing.example", rows))


class Parse(unittest.TestCase):
    def test_noindex_meta_and_header(self):
        self.assertEqual(page("noindex")["noindex"], "yes")
        self.assertEqual(page("bare_title", headers={"X-Robots-Tag": "noindex"})["noindex"], "yes")
        self.assertEqual(page("good_local")["noindex"], "")

    def test_schema_and_phones(self):
        p = page("good_local")
        self.assertEqual(p["local_schema"], "yes")
        self.assertEqual(p["schema_phones"], "7045550133")
        self.assertIn("7045550133", p["site_phones"])
        self.assertGreaterEqual(p["internal_links"], 5)
        self.assertEqual(p["h1_count"], 1)

    def test_bare_title(self):
        p = page("bare_title")
        self.assertEqual(p["title"], "Home")
        self.assertIn("7045550122", p["site_phones"])


class Checks(unittest.TestCase):
    def test_good_local_site_has_no_verdict(self):
        found = ss.findings(page("good_local"), place(), NICHE, CITY, extra())
        verdict, _, _ = ss.pick(found)
        self.assertEqual(verdict, "")

    def test_noindex_is_blocked(self):
        found = ss.findings(page("noindex", "https://oakridgefence.example/"), place(phone="(704) 555-0100"),
                            NICHE, CITY, extra(final_url="https://oakridgefence.example/"))
        self.assertEqual(ss.pick(found)[0], "Blocked")

    def test_canonical_to_build_address(self):
        found = ss.findings(page("canonical_other", "https://pinefence.example/"), place(phone="(704) 555-0111"),
                            NICHE, CITY, extra(final_url="https://pinefence.example/"))
        verdict, line, _ = ss.pick(found)
        self.assertEqual(verdict, "Blocked")
        self.assertIn("pinefence.wpengine.com", line)

    def test_phone_mismatch(self):
        found = ss.findings(page("phone_mismatch"), place(phone="(704) 555-0144"), NICHE, CITY, extra())
        self.assertIn("Mismatch", types(found))

    def test_bare_title_and_one_page(self):
        found = ss.findings(page("bare_title"), place(phone="704-555-0122"), NICHE, CITY, extra(sitemap_urls=None))
        self.assertIn("No what/where", types(found))
        self.assertIn("One page", types(found))
        self.assertIn("No local data", types(found))

    def test_reviews_gap(self):
        found = ss.findings(page("good_local"), place(reviews="5"), NICHE, CITY, extra(top5_median_reviews=90))
        self.assertEqual(ss.pick(found)[0], "Reviews gap")

    def test_priority_blocked_beats_unclaimed_beats_mismatch(self):
        found = ss.findings(page("noindex", "https://oakridgefence.example/"),
                            place(phone="(704) 555-0999", unclaimed="yes"), NICHE, CITY,
                            extra(final_url="https://oakridgefence.example/"))
        verdict, _, also = ss.pick(found)
        self.assertEqual(verdict, "Blocked")
        self.assertEqual(len(also), 2)
        self.assertIn("unclaimed", also[0])
        found = ss.findings(page("phone_mismatch"), place(phone="(704) 555-0144", unclaimed="yes"), NICHE, CITY, extra())
        self.assertEqual(ss.pick(found)[0], "Unclaimed")


class Floor(unittest.TestCase):
    def test_top3_on_maps_is_never_kept(self):
        self.assertFalse(ss.not_ranking(2, None, True)[0])
        self.assertFalse(ss.not_ranking("3", 5, True)[0])

    def test_outside_top10_on_maps_is_kept(self):
        self.assertTrue(ss.not_ranking(23, 4, True)[0])
        self.assertTrue(ss.not_ranking("11", None, False)[0])

    def test_middle_of_maps_needs_organic_absence(self):
        self.assertTrue(ss.not_ranking(6, None, True)[0])
        self.assertTrue(ss.not_ranking(6, 25, True)[0])
        self.assertFalse(ss.not_ranking(6, 8, True)[0])
        self.assertFalse(ss.not_ranking(6, None, False)[0])


if __name__ == "__main__":
    unittest.main()
