from os import name
from sqlalchemy import select
import tkinter
from tkinter import ttk

from model.ship_role import ShipRole
from service.dblink import DBLink


class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid(column=0, row=0, rowspan=2, columnspan=3)
        self.createWidgets()

    def createWidgets(self):

        columns = ("code", "name", "description")
        self.ship_roles = ttk.Treeview(self, columns=columns, show="headings")
        
        self.ship_roles.heading("code", text="Code")
        self.ship_roles.heading("name", text="Name")
        self.ship_roles.heading("description", text="Description")
        session = DBLink().getSession()

        stmt = select(ShipRole)
        for role in session.scalars(stmt):
            values = (role.code, role.name, role.description)
            self.ship_roles.insert('', 'end', text='Listbox', values=values)


        self.ship_roles.grid(column=0, row=0)

        self.quitButton = ttk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(column=0, row=1)
