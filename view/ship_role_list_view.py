from os import name
from sqlalchemy import select
import tkinter
from tkinter import ttk

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
        self.quitButton = ttk.Button(self.parent, text='Quit', command=self.parent.destroy)
        self.quitButton.grid(column=0, row=1)
        self.parent.grab_set() # Rende la finestra MODALE (blocca l'interazione con la principale finché non la chiudi)

    def show_data(self, data):
        for role in data:
            values = (role.code, role.name, role.description)
            self.ship_roles.insert('', 'end', text='Listbox', values=values)