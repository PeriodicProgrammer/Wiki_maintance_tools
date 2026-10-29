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
        self.assertEqual(next(generator).strip("\n "), "This section does not contain a [[Wikipedia:Disambiguation|disambiguation link]].")
        self.assertEqual(next(generator).strip("\n "), "* [[WP:Disambiguation]]\n* [[WP:Tools]]\n* [[Disambiguation of disambiguation]]\n* [[Disambiguation (disambiguation)]]\n{{Nobots}}")
    def test_get_wikilinks(self):
        self.assertEqual(helpers.get_wikilinks(disambig_test.text), helpers.get_wikilinks(disambig_test))
        self.assertEqual(helpers.get_wikilinks(disambig_test), {"Disambiguation (disambiguation)", "WP:Disambiguation", "WP:Tools", "Disambiguation of disambiguation", "Wikipedia:Disambiguation"})
    def test_get_redirects(self):
        self.assertEqual(helpers.get_redirects(disambig_test), set())
        self.assertTrue("H2O" in helpers.get_redirects(pywikibot.Page(site, "Water")))
class TestDisambigFuncs(unittest.TestCase):
    def test_has_disambig_link(self):
        self.assertEqual(delinker_funcs.has_disambig_link(disambig_test.text, "Disambiguation (disambiguation)"), True)
        self.assertFalse(delinker_funcs.has_disambig_link("This is a test", "Disambiguation (dsambiguation)"))
    def test_disambig_sec_test(self):
        containing_disambig_of_disambig = {"{{Short description|Test page for tool created by PeriodicEditor}}\nPlease don't edit this page, as it will break testing a tool for retargeting [[disambiguation (disambiguation)|disambiguation]] links.", "* [[WP:Disambiguation]]\n* [[WP:Tools]]\n* [[Disambiguation of disambiguation]]\n* [[Disambiguation (disambiguation)]]\n{{Nobots}}"}
        for i in delinker_funcs.secs_with_disambig(disambig_test, "Disambiguation (disambiguation)"):
            self.assertIn(i.strip("\n "), containing_disambig_of_disambig)
if __name__ == "__main__":
    unittest.main()
