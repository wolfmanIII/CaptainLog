import tkinter as tk
from tkinter import ttk, Menu

# Classe per il menu
class Menubar:
    def __init__(self, master):  # master deve essere tk.Tk() o tk.Toplevel()
        menubar = Menu(master)

        menu_file = Menu(menubar, tearoff=0)
        menu_file.add_command(label="Nuovo")
        menu_file.add_separator()
        menu_file.add_command(label="Esci", command=master.quit)

        menubar.add_cascade(label="File", menu=menu_file)

        master.config(menu=menubar)  # assegna il menu alla finestra principale