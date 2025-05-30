import tkinter as tk
from tkinter import font
import sv_ttk

from view.application import Application
from view.menubar import Menubar


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Captain Log")
    root.minsize(width=640, height=480)
    app = Application(root)  # ✅ App è un Frame figlio di root
    sv_ttk.set_theme("dark")
    root.mainloop()