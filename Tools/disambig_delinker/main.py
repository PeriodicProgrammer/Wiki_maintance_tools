import customtkinter as ctk
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pywikibot
from pywikibot import textlib
import Supporting.general_helpers as helpers
from Supporting.colours import apply_text_styles
import delinker_funcs as dl_func
import settings

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
site = settings.site
site.login()

def page_gen():
    if settings.Category is not None:
        disambigs = helpers.walk_category(pywikibot.Category(site, settings.Category))
    else:
        import json
        with open("data.json", "r") as f:
            disambigs = [i for i in json.load(f)]
    for disambig in disambigs:
        yield ("Disambig", disambig)
        for page in disambig.getReferences(namespaces=[0], follow_redirects=True):
            yield ("Page", page)
            for section in dl_func.secs_with_disambig(page, disambig):
                yield ("Section", section)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Disambiguation page delinker")
        self.geometry("800x500")

        # Frame to hold the two outputs side-by-side
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(pady=10, fill="both", expand=True)

        # Output window 1
        self.output1 = ctk.CTkTextbox(self.output_frame, width=350, height=300)
        self.output1.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        # Output window 2
        self.output2 = ctk.CTkTextbox(self.output_frame, width=350, height=300)
        self.output2.pack(side="right", padx=10, pady=10, fill="both", expand=True)
        # Input label + entry
        self.input_label = ctk.CTkLabel(self, text="Enter your input:")
        self.input_label.pack(pady=10)

        self.input_entry = ctk.CTkEntry(self, width=400)
        self.input_entry.pack(pady=10)

        # Submit button
        self.submit_btn = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.submit_btn.pack(pady=20)
        apply_text_styles(self.output1._textbox)
        apply_text_styles(self.output2._textbox)

        self.gen = page_gen()
        self.fill_info()
    def fill_info(self):
        try:
            type, page = next(self.gen)
        except StopIteration:
            self.output1.delete("0.0", "end")
            self.output1.insert("end", "Generator finished.")
            self.output2.delete("0.0", "end")
            self.output2.insert("end", "")
            return
        if type == "Disambig":
            self.output1.delete("0.0", "end")
            self.output1.insert("0.0", f"{page.title()}\n", "Disambig")
            for i,j in dl_func.get_dismabig_targets(page).items():
                self.output1.insert("end", f"{i}. {j}\n")

            self.fill_info()
        elif type == "Page":
            self.page, self.short_desc = page, helpers.get_short_description(page)
            self.output2.delete("0.0", "end")
            self.output2.insert("0.0", f"{page.title()}\n", "Title")
            if self.short_desc is not None:
                self.output2.insert("end", "Short description: ")
                self.output2.insert("end", f"{self.short_desc}\n", "Short_desc")
            self.fill_info()
        elif type == "Section":
            self.output2.delete("0.0", "end")
            self.output2.insert("0.0", f"{self.page.title()}\n", "Title")
            if self.short_desc is not None:
                self.output2.insert("end", "Short description: ")
                self.output2.insert("end", f"{self.short_desc}\n", "Short_desc")
            self.output2.insert("end", page)

    def submit(self):
        user_input = self.input_entry.get()
        if not user_input == "":
            try:
                num = int(user_input)
            except:
                pass
        
        self.fill_info()
app = App()
app.mainloop()

