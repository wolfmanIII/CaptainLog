from os import name
from sqlalchemy import column, select
import tkinter
from tkinter import ttk

from model.ship_role import ShipRole
from service.dblink import DBLink
from view.menubar import Menubar
from view.ship_role_list import ShipRoleList


class Application(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, width=700, height=500)
        Menubar(master)
        self.grid(column=0, row=0, rowspan=2, columnspan=2)
        self.grid_propagate(False)
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = ttk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(column=0, row=1)