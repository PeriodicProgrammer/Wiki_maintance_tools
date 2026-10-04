import re
def walk_category(cat):
    for page in cat.articles():
        yield page
    for subcat in cat.subcategories():
        yield from walk_category(subcat)

def get_short_description(page_text):
    short_desc = re.search(r"\{\{short description\s*\|([^\}]+)}}", page_text)
    if short_desc is not None:
        return short_desc.group(1)
    return None

def clear():
    print("\033c", end="")


if __name__ == "__main__":
    pass #Tests