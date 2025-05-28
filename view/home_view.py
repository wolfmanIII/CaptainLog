import tkinter as tk
from tkinter import ttk

from numpy import size

class HomeView(tk.Frame):
    def __init__(self, master, router):
        super().__init__(master)
        self.grid()
        ttk.Label(self, text="🏠 Captain Log", font=("Segoe UI", 16)).grid(column=0, row=0, padx=5, pady=5, columnspan=3)

        ttk.Button(self, text="🚀 Crew").grid(column=0, row=1, padx=5, pady=5)
        ttk.Button(self, text="🚀 Ships", command=lambda: router.navigate("ships")).grid(column=1, row=1, padx=5, pady=5)
        ttk.Button(self, text="🚀 Contracts").grid(column=0, row=1, padx=5, pady=5)
