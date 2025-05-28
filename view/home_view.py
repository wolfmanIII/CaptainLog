import tkinter as tk
from tkinter import ttk

from numpy import size

class HomeView(ttk.Frame):
    def __init__(self, master, router):
        super().__init__(master)

        master.columnconfigure(0, weight=1)
        ttk.Label(self, text="👨‍🚀 Captain Log", font=("Segoe UI", 16)).grid(column=0, row=0, padx=5, pady=5, sticky="w")

        buttonGroup = ButtonGroup(self, router)
        buttonGroup.grid(column=0, row=1, padx=5, pady=5, sticky="w")
class ButtonGroup(tk.Frame):

    def __init__(self, parent, router):
        super().__init__(parent, borderwidth=1, relief="solid")
        self.router = router
        self.parent = parent

        ttk.Button(self, text="🛸 Ships", command=lambda: router.navigate("ships")).grid(column=0, row=1, padx=10, pady=10)
        ttk.Button(self, text="🆔 Crew").grid(column=1, row=1, padx=10, pady=10)
        ttk.Button(self, text="📝 Ship Mortgage").grid(column=2, row=1, padx=10, pady=10)
        ttk.Button(self, text="💸 Annual Budget").grid(column=3, row=1, padx=10, pady=10)
        ttk.Button(self, text="💰 Contracts").grid(column=4, row=1, padx=10, pady=10)
