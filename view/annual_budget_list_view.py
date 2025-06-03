import tkinter as tk
from tkinter import ttk

from service.dblink import DBLink
from util.emoji_cache import EmojiCache

class AnnualBudgetListView(ttk.Frame):

    def __init__(self, master, router):
        super().__init__(master)
        self.router = router
        self.session = DBLink().getSession()
        self.create_widgets()

    def create_widgets(self):
        self.img_title_tk = EmojiCache(size=32).get("1f4c9.png") # Chart decreasing
        self.title_label = ttk.Label(self, text="Annual Budgets", font=("", 30), image=self.img_title_tk, compound="left")
        self.title_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        buttonGroup = ButtonGroup(self, self.router)
        buttonGroup.grid(column=0, row=1, padx=5, pady=5, sticky="w")

class ButtonGroup(ttk.Frame):

    def __init__(self, parent, router):
        super().__init__(parent, borderwidth=1, relief="solid")

        self.img_back_tk = EmojiCache(size=16).get("2b05.png") # Back
        self.home_button = ttk.Button(self, text="Back", command=lambda: router.navigate("home"), image=self.img_back_tk, compound="left")
        self.home_button.grid(column=0, row=0, padx=10, pady=10, sticky="w")