import customtkinter as ctk
from pathlib import Path
import sys
import re

REPO_ROOT = Path(__file__).resolve().parents[2]

if not (REPO_ROOT / "Supporting").exists():
    raise RuntimeError(
        f"Could not find Supporting package in {REPO_ROOT}"
    )

sys.path.insert(0, str(REPO_ROOT))
import pywikibot
from pywikibot import textlib
from pywikibot import pagegenerators
import Supporting.general_helpers as helpers
from settings import apply_text_styles
import settings

ctk.set_appearance_mode(settings.appearance_mode)
ctk.set_default_color_theme(settings.default_color_theme)
site = settings.site
site.login()


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
        # Input label + entry
        self.input_label = ctk.CTkLabel(self, text="Enter your input:")
        self.input_label.pack(pady=10)

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10)
        self.input_label = ctk.CTkLabel(
            input_frame,
            text="Target:"
        )
        self.input_label.pack(side="left", padx=(0, 10))
        self.input_entry = ctk.CTkEntry(
            input_frame,
            width=400
        )
        edit_desc_frame = ctk.CTkFrame(self)
        edit_desc_frame.pack(pady=10)

        edit_desc_label = ctk.CTkLabel(
            edit_desc_frame,
            text="Edit description:"
        )
        edit_desc_label.pack(side="left", padx=(0, 10))

        self.edit_desc = ctk.CTkEntry(
            edit_desc_frame,
            width=400
        )
        self.edit_desc.pack(side="left")
        self.input_entry.pack(side="left")
        # Submit button
        self.submit_btn = ctk.CTkButton(self, text="Submit", command=self.submit)
        self.submit_btn.pack(pady=20)
        apply_text_styles(self.output1._textbox)

        self.gen = pagegenerators.SearchPageGenerator(query = '-hastemplate:"Short description"', namespaces = 0)
        self.submit()
        #self.fill_info()
    def fill_info(self):
        try:
            self.page = next(self.gen)
            self.output1.delete("0.0", "end")
            self.output1.insert("end", self.page.title()+"\n", "Title")
            display_text = re.sub(r"/<ref\s?(\s?name\s?=\s?[^>]*>)?.*?<\/ref>/gm", "", self.page.text)
            self.output1.insert("end", display_text)
        except StopIteration:
            self.output1.delete("0.0", "end")
            self.output1.insert("end", "Generator finished.")
            return

    def submit(self):
        user_input = self.input_entry.get()
        edit_desc = self.edit_desc.get()
        self.edit_desc.delete(0, "end")
        self.input_entry.delete(0, "end")
        if len(user_input) > 10:
            text = self.page.text
            self.page.text = "{{Short description|"+user_input+"}}\n" + self.page.text
            self.page.save(f"+short desc using https://github.com/PeriodicProgrammer/Wiki_maintance_tools/tree/main {f"Note: {edit_desc}" if edit_desc else ""}")
        if len(user_input) > 60:
            pass
        else:
            self.fill_info()

if __name__ == "__main__":
    app = App()
    app.mainloop()

