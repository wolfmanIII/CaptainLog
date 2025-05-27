import locale
from sqlalchemy import Numeric, select
import tkinter
from tkinter import ttk
import tkinter.font as tkFont

from model.ship import Ship
from service.dblink import DBLink
from service.ship_service import ShipService
from view.ship_view import ShipView

locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class ShipListView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        columns = ["code", "name", "type", "model", "price"]
        self.ships = ttk.Treeview(self.parent, columns=columns, show="headings")
        for column in columns:
            text_show= ""
            if column == "price":
                text_show = column.capitalize() + "(Cr)"
            else:
                text_show = column.capitalize()
            self.ships.heading(column, text=text_show)

        self.ships.column('price', anchor="e")

        self.show_data(ShipService().get_all_ships())
        self.ships.grid(column=0, row=0, columnspan=1, rowspan=20)

        self.set_columns_dimension()
        
        self.ship_view = ShipView(self)
        self.addShipButton = ttk.Button(self.parent, text="Add Ship", width=12, command=self.viewShip)
        self.addShipButton.grid(column=1, row=0, padx=5, pady=2)

        self.removeShipButton = ttk.Button(self.parent, text="Remove Ship", width=12)
        self.removeShipButton.grid(column=1, row=1, padx=5, pady=2)

        self.parent.grab_set() # Rende la finestra MODALE (blocca l'interazione con la principale finché non la chiudi)

    def show_data(self, data):
        for ship in data:
            values = (ship.code, ship.name, ship.type, ship.model, locale.format_string('%.2f', ship.ship_price, grouping=True))
            self.ships.insert('', 'end', text='Listbox', values=values)

    def set_columns_dimension(self):
        font = tkFont.Font()
        for col in self.ships['columns']:
            # Considera la larghezza dell'intestazione
            max_width = font.measure(col)
            
            # Scorri tutte le righe per la colonna
            for item in self.ships.get_children():
                cell_text = self.ships.set(item, col)
                cell_width = font.measure(cell_text)
                if cell_width > max_width:
                    max_width = cell_width
            
            # Aggiungi un po' di margine
            max_width += 10
            self.ships.column(col, width=max_width)

    def viewShip(self):
        self.dialog = tkinter.Toplevel(self.parent)
        self.dialog.title("Ship")
        self.dialog.grid()
        self.dialog.ship_list = ShipView(self.dialog)


        
