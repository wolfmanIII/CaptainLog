from numpy import void
from sqlalchemy import column, select
import tkinter
from tkinter import Tk, ttk

from model.ship_role import ShipRole
from service.dblink import DBLink
from view.menubar import Menubar

class Application(ttk.Frame):
    def __init__(self, master: Tk):
        super().__init__(master)
        #self.grid(column=0, row=0, rowspan=2, columnspan=2)
        self.pack(fill="both", expand=True)
        #self.grid_propagate(False)
        self.createWidgets()

    def createWidgets(self):
        return void