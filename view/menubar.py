import tkinter as tk
from tkinter import Tk, ttk, Menu

from view.ship_role_list import ShipRoleList

# Classe per il menu
class Menubar:
    def __init__(self, master: Tk):  # master deve essere tk.Tk() o tk.Toplevel()
        self.menubar = Menu(master)

        self.menu_file = Menu(self.menubar, tearoff=0)
        self.menu_file.add_command(label="Ships")
        self.menu_file.add_command(label="Ship roles", command=self.callShipRoleList)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Esci", command=master.quit)

        self.menubar.add_cascade(label="File", menu=self.menu_file)

        master.config(menu=self.menubar)  # assegna il menu alla finestra principale

    def callShipRoleList(self):
        self.dialog = tk.Toplevel(self.menubar.master)
        self.dialog.title("Ship roles list")
        self.dialog.grid()
        self.dialog.ship_role_list = ShipRoleList(self.dialog)
        self.dialog.ship_role_list.buildView(column=0, row=0, columnspan=2, rowspan=1)
        self.dialog.quitButton = ttk.Button(self.dialog, text='Quit', command=self.dialog.destroy)
        self.dialog.quitButton.grid(column=0, row=1)
        self.dialog.grab_set() # Rende la finestra MODALE (blocca l'interazione con la principale finché non la chiudi)