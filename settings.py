import pywikibot
#General settings
site = pywikibot.Site('en', 'wikipedia')

appearance_mode = "dark"
default_color_theme = "blue"
def apply_text_styles(textbox): #Colour codes
    textbox.tag_config("Disambig", foreground="#ff8800")
    textbox.tag_config("Short_desc", foreground="#ca9df7")
    textbox.tag_config("Title", foreground="#00bbff")

#Disambig delinker settings
disambig_cat = None #Defaults to Category:Disambiguation pages with many incoming links
