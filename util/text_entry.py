import tkinter as tk
from tkinter import ttk

class TextEntry(ttk.Frame):
    def __init__(self, master=None, textvariable=None, **kwargs):
        super().__init__(master)
        self.var = textvariable or tk.StringVar()

        self.entry = ttk.Entry(self, textvariable=self.var, **kwargs)
        self.entry.pack(fill="x")

        