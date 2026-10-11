import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import Supporting.general_helpers as helpers
import pywikibot

site = pywikibot.Site('en', 'wikipedia')
disambig_test = pywikibot.Page(site, "User:PeriodicEditor2/tests/disambig-delinker")
class TestHelpers(unittest.TestCase):
    def test_get_short_desc(self):
        self.assertEqual(helpers.get_short_description(disambig_test), "Test page for tool created by PeriodicEditor")
        self.assertIsNone(helpers.get_short_description(pywikibot.Page(site, "User:PeriodicEditor")))
    def test_section_gen(self):
        generator = helpers.section_gen(disambig_test)
        self.assertEqual(next(generator).strip("\n "), "{{Short description|Test page for tool created by PeriodicEditor}}\nPlease don't edit this page, as it will break testing a tool for retargeting [[disambiguation (disambiguation)|disambiguation]] links.")
        self.assertEqual(next(generator).strip("\n "), "* [[WP:Disambiguation]]\n* [[WP:Tools]]\n{{Nobots}}")
    def test_get_wikilinks(self):
        self.assertEqual(helpers.get_wikilinks(disambig_test.text), helpers.get_wikilinks(disambig_test))
if __name__ == "__main__":
    unittest.main()
