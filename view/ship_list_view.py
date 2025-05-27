from os import name
from sqlalchemy import select
import tkinter
from tkinter import ttk

from model.ship import Ship
from service.dblink import DBLink
from service.ship_service import ShipService


class ShipListView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        columns = ["code", "name", "model", "description", "price"]
        self.ships = ttk.Treeview(self.parent, columns=columns, show="headings")
        for column in columns:
            self.ships.heading(column, text=column.capitalize())

        self.show_data(ShipService().get_all_ships())
        self.ships.grid(column=0, row=0, columnspan=2, rowspan=1)
        self.quitButton = ttk.Button(self.parent, text='Quit', command=self.parent.destroy)
        self.quitButton.grid(column=0, row=1)
        self.parent.grab_set() # Rende la finestra MODALE (blocca l'interazione con la principale finché non la chiudi)

    def show_data(self, data):
        for ship in data:
            values = (ship.code, ship.name, ship.model, ship.description, ship.ship_price)
            self.ship.insert('', 'end', text='Listbox', values=values)
        
