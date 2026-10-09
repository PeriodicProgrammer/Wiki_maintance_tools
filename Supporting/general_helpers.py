import re
import pywikibot
from pywikibot import textlib
def walk_category(cat):
    for page in cat.articles():
        yield page
    for subcat in cat.subcategories():
        yield from walk_category(subcat)

def get_short_description(page):
    page_text = page.text
    short_desc = re.search(r"\{\{short description\s*\|([^\}]+)}}", page_text)
    if short_desc is not None:
        return short_desc.group(1)
    return None

def clear():
    print("\033c", end="")

def section_gen(page, site=pywikibot.Site('en', 'wikipedia')):
    if isinstance(page, pywikibot.Page):
        secs = pywikibot.textlib.extract_sections(page.text, site)
    else:
        secs = page
    for i in secs:
        if isinstance(i, str):
            if not i.strip() in ["", "\n"]:
                yield i
        elif isinstance(i, textlib.Section):
            if not i.content.strip() in ["", "\n"]:
                yield i.content
        elif isinstance(i, textlib.SectionList):
            yield from section_gen(i, site)

def get_wikilinks(text, full=False):
    if full:
        links = {"".join(i) for i in re.findall(r"(\[\[)([^\]\|]+)(\s?)(\|[^\]\|]*\s?)?(\]\])", text)}
    else:
        links = {i[0] for i in re.findall(r"\[\[([^\]\|]+)\s?(\|[^\]\|]*\s?)?\]\]", text)}
    return links

def get_redirects(page):
    return {i.title() for i in page.redirects()}



if __name__ == "__main__":
    site = pywikibot.Site('en', 'wikipedia')
    site.login()
    print(get_redirects(pywikibot.Page(site, "Water")))
