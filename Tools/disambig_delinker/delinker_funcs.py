import pywikibot
from pywikibot import textlib
import re
import Supporting.general_helpers as helpers

def get_dismabig_targets(page):
    items = []
    for line in page.text.splitlines():
        if re.search(r"==\s*See also\s*==", line) is not None:
            break
        links = re.findall(r"\[\[([^\]\|]+)[^\]]*]", line)
        if links:
            items.append(links[0])
    i = 1
    item_dict = {}
    for item in items:
        item_dict[i] = item
        i+= 1
    return item_dict

def has_disambig_link(sec, target):
    links = helpers.get_wikilinks(sec)
    redirects = helpers.get_redirects(target)
    result = links & redirects
    return result != 0
