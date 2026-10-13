import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import Supporting.general_helpers as helpers
import pywikibot
import Tools.disambig_delinker.delinker_funcs as delinker_funcs
site = pywikibot.Site('en', 'wikipedia')
disambig_test = pywikibot.Page(site, "User:PeriodicEditor2/tests/disambig-delinker")
class TestHelpers(unittest.TestCase):
    def test_get_short_desc(self):
        self.assertEqual(helpers.get_short_description(disambig_test), "Test page for tool created by PeriodicEditor")
        self.assertIsNone(helpers.get_short_description(pywikibot.Page(site, "User:PeriodicEditor")))
    def test_section_gen(self):
        generator = helpers.section_gen(disambig_test)
        self.assertEqual(next(generator).strip("\n "), "{{Short description|Test page for tool created by PeriodicEditor}}\nPlease don't edit this page, as it will break testing a tool for retargeting [[disambiguation (disambiguation)|disambiguation]] links.")
        self.assertEqual(next(generator).strip("\n "), "* [[WP:Disambiguation]]\n* [[WP:Tools]]\n* [[Disambiguation of disambiguation]]\n{{Nobots}}")
    def test_get_wikilinks(self):
        self.assertEqual(helpers.get_wikilinks(disambig_test.text), helpers.get_wikilinks(disambig_test))
        self.assertEqual(helpers.get_wikilinks(disambig_test), {"disambiguation (disambiguation)", "WP:Disambiguation", "WP:Tools", "Disambiguation of disambiguation"})
    def test_get_redirects(self):
        self.assertEqual(helpers.get_redirects(disambig_test), set())
        self.assertTrue("H2O" in helpers.get_redirects(pywikibot.Page(site, "Water")))
class TestDisambigFuncs(unittest.TestCase):
    def test_has_disambig_link(self):
        self.assertEqual(delinker_funcs.has_disambig_link(disambig_test.text, "Disambiguation (disambiguation)"), True)
if __name__ == "__main__":
    unittest.main()
