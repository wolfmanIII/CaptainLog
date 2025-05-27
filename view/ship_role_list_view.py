from sqlalchemy import select
import tkinter
from tkinter import ttk
import tkinter.font as tkFont

from model.ship_role import ShipRole
from service.dblink import DBLink
from service.ship_role_service import ShipRoleService


class ShipRoleListView(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widtgets()

    def create_widtgets(self):
        columns = ["code", "name", "description"]
        self.ship_roles = ttk.Treeview(self.parent, columns=columns, show="headings")
        for column in columns:
            self.ship_roles.heading(column, text=column.capitalize())
        
        self.show_data(ShipRoleService().get_all_ship_roles())
        self.ship_roles.grid(column=0, row=0, columnspan=2, rowspan=1)

        self.set_columns_dimension()

        self.parent.grab_set() # Rende la finestra MODALE (blocca l'interazione con la principale finché non la chiudi)

    def show_data(self, data):
        for role in data:
            values = (role.code, role.name, role.description)
            self.ship_roles.insert('', 'end', text='Listbox', values=values)

    def set_columns_dimension(self):
        font = tkFont.Font()
        for col in self.ship_roles['columns']:
            # Considera la larghezza dell'intestazione
            max_width = font.measure(col)
            
            # Scorri tutte le righe per la colonna
            for item in self.ship_roles.get_children():
                cell_text = self.ship_roles.set(item, col)
                cell_width = font.measure(cell_text)
                if cell_width > max_width:
                    max_width = cell_width
            
            # Aggiungi un po' di margine
            max_width += 10
            self.ship_roles.column(col, width=max_width)