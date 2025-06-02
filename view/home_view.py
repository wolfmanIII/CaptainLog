import tkinter as tk
from tkinter import ttk

from numpy import size

from util.emoji_cache import EmojiCache

class HomeView(ttk.Frame):
    def __init__(self, master, router):
        super().__init__(master)
        self.router = router
        self.create_widgets(master)

    def create_widgets(self, master):
        master.columnconfigure(0, weight=1)
        self.img_captain_log_tk = EmojiCache(size=32).get("1f468-200d-1f680.png") # Astronaut
        self.captain_label = ttk.Label(self, text="Captain Log", font=("", 30), image=self.img_captain_log_tk, compound="left")
        self.captain_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        buttonGroup = ButtonGroup(self)
        buttonGroup.grid(column=0, row=1, padx=5, pady=5, sticky="w")

class ButtonGroup(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, borderwidth=1, relief="solid")

        self.img_ships_tk = EmojiCache(size=16).get("2708.png") #Airplane
        self.ships_label = ttk.Button(
            self, text="Ships", image=self.img_ships_tk, compound="left",
            command=lambda: parent.router.navigate("ships")
        )
        self.ships_label.grid(column=0, row=1, padx=10, pady=10)

        self.img_crew_tk = EmojiCache(size=16).get("1f465.png") #Users
        self.img_crew_label = ttk.Button(
            self, text="Crew", image=self.img_crew_tk, compound="left",
            command=lambda: parent.router.navigate("crew")
        )
        self.img_crew_label.grid(column=1, row=1, padx=10, pady=10)

        self.img_ship_mortgage_tk = EmojiCache(size=16).get("1f4b8.png") #Money with wings
        self.img_ship_mortgage_label = ttk.Button(
            self, text="Ship Mortgage", image=self.img_ship_mortgage_tk, compound="left",
            command=lambda: parent.router.navigate("ship_mortgage")
        )
        self.img_ship_mortgage_label.grid(column=2, row=1, padx=10, pady=10)

        self.img_annual_budget_tk = EmojiCache(size=16).get("1f4c9.png") #Chart decreasing 
        self.img_annual_budget_label = ttk.Button(
            self, text="Annual Budget", image=self.img_annual_budget_tk, compound="left",
            command=lambda: parent.router.navigate("annual_budget")
        )
        self.img_annual_budget_label.grid(column=3, row=1, padx=10, pady=10)

        self.img_contracts_tk = EmojiCache(size=16).get("1f4dd.png") #Memo 
        self.img_contracts_label = ttk.Button(
            self, text="Contracts", image=self.img_contracts_tk, compound="left",
            command=lambda: parent.router.navigate("contracts")
        )
        self.img_contracts_label.grid(column=4, row=1, padx=10, pady=10)
