from os import name
from sqlalchemy import select
import tkinter
from tkinter import ttk

from model.ship_role import ShipRole
from service.dblink import DBLink


class ShipRoleList():

    def __init__(self, parent):
        columns = ["code", "name", "description"]
        self.ship_roles = ttk.Treeview(parent, columns=columns, show="headings")
        for column in columns:
            self.ship_roles.heading(column, text=column.capitalize())


    def buildView(self, column=0, row=0, columnspan=1, rowspan=1):
        session = DBLink().getSession()
        stmt = select(ShipRole)
        for role in session.scalars(stmt):
            values = (role.code, role.name, role.description)
            self.ship_roles.insert('', 'end', text='Listbox', values=values)
        
        self.ship_roles.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)