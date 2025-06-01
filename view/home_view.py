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
        ttk.Label(self, text="Captain Log", font=("", 18)).grid(column=0, row=0, padx=10, pady=10, sticky="w")

        buttonGroup = ButtonGroup(self)
        buttonGroup.grid(column=0, row=1, padx=5, pady=5, sticky="w")

class ButtonGroup(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, borderwidth=1, relief="solid")

        self.img_ships_tk = EmojiCache().get("2708.png") #Airplane
        self.ships_label = ttk.Button(
            self, text="Ships", image=self.img_ships_tk, compound="left",
            command=lambda: parent.router.navigate("ships")
        )
        self.ships_label.grid(column=0, row=1, padx=10, pady=10)

        ttk.Button(self, text="Crew", command=lambda: parent.router.navigate("crew")).grid(column=1, row=1, padx=10, pady=10)
        ttk.Button(self, text="Ship Mortgage").grid(column=2, row=1, padx=10, pady=10)
        ttk.Button(self, text="Annual Budget").grid(column=3, row=1, padx=10, pady=10)
        ttk.Button(self, text="Contracts").grid(column=4, row=1, padx=10, pady=10)
