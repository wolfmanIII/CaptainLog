import tkinter as tk
from tkinter import Tk, ttk, Menu
from turtle import width

from view.ship_list_view import ShipListView
from view.ship_role_list_view import ShipRoleListView

# Classe per il menu
class Menubar:
    def __init__(self, master: Tk):  # master deve essere tk.Tk() o tk.Toplevel()
        self.menubar = Menu(master)

        self.menu_file = Menu(self.menubar, tearoff=0)
        self.menu_file.add_command(label="Ships", command=self.viewShipList)
        self.menu_file.add_command(label="Ship roles", command=self.viewShipRoleList)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Esci", command=master.quit)

        self.menubar.add_cascade(label="File", menu=self.menu_file)

        master.config(menu=self.menubar)  # assegna il menu alla finestra principale

    def viewShipRoleList(self):
        self.dialog = tk.Toplevel(self.menubar.master)
        self.dialog.title("Ship roles list")
        self.dialog.grid()
        self.dialog.ship_role_list = ShipRoleListView(self.dialog)

    def viewShipList(self):
        self.dialog = tk.Toplevel(self.menubar.master)
        self.dialog.title("Ship list")
        self.dialog.grid()
        self.dialog.ship_list = ShipListView(self.dialog)