import locale
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from model.ship import Ship
from service.dblink import DBLink
from service.ship_service import ShipService
from view.ship_view import ShipView

locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class ShipListView(ttk.Frame):

    def __init__(self, master, router):
        super().__init__(master)
        self.router = router
        self.session = DBLink().getSession()

        ttk.Label(self, text="Ships", font=("", 18)).grid(column=0, row=0, padx=10, pady=10, sticky="w")

        buttonGroup = ButtonGroup(self, router)
        buttonGroup.grid(column=0, row=1, padx=5, pady=5, sticky="w")

        columns = ["code", "name", "type", "model", "price"]
        self.ships = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            text_show= ""
            if column == "price":
                text_show = column.capitalize() + "(Cr)"
            else:
                text_show = column.capitalize()
            self.ships.heading(column, text=text_show)

        self.ships.column('price', anchor="e")

        self.refresh()
        self.ships.grid(column=0, row=2, padx=5, pady=5)

        # Bind evento doppio click
        self.ships.bind("<Double-1>", self.on_double_click_row)

    def populate_data(self):
        for ship in ShipService().get_all_ships():
            values = (ship.code, ship.name, ship.type, ship.model, locale.format_string('%.2f', ship.ship_price, grouping=True))
            self.ships.insert('', 'end', iid=ship.id, text='Listbox', values=values)

    def refresh(self):
        for item in self.ships.get_children():
            self.ships.delete(item)

        self.populate_data()

    def delete_selected_ships(self):
        selected_items = self.ships.selection()
        for iid in selected_items:
            # 1. Cancella dal database
            ship = self.session.get(Ship, iid)
            if ship:
                self.session.delete(ship)
        
        self.session.commit()  # 2. Commit
        self.refresh()

    def on_double_click_row(self, event):
        item_id = self.ships.identify_row(event.y)
        if item_id:
            self.viewShip(item_id)

    def viewShip(self, id=None):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Ship")
        ship_view = ShipView(self.dialog, self.router, id)
        ship_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.dialog.wait_visibility()
        self.dialog.grab_set() 

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

class ButtonGroup(ttk.Frame):

    def __init__(self, parent, router):
        super().__init__(parent, borderwidth=1, relief="solid")

        self.home_button = ttk.Button(self, text="Back", command=lambda: router.navigate("home"))
        self.home_button.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        self.refresh_button = ttk.Button(self, text="Refresh", command=parent.refresh)
        self.refresh_button.grid(column=1, row=0, padx=10, pady=10, sticky="w")

        self.new_ship_button = ttk.Button(self, text="New", command=parent.viewShip)
        self.new_ship_button.grid(column=2, row=0, padx=10, pady=10, sticky="w")

        self.new_ship_button = ttk.Button(self, text="Delete", command=parent.delete_selected_ships)
        self.new_ship_button.grid(column=3, row=0, padx=10, pady=10, sticky="w")




        
