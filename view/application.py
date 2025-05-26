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

        self.shipRoleButton = ttk.Button(self, text='Ship roles', command=self.callShipRoleList)
        self.shipRoleButton.grid(column=1, row=1)

    def callShipRoleList(self):
        dialog = tkinter.Toplevel(self)
        dialog.title("Ship roles list")
        dialog.grid()
        dialog.ship_role_list = ShipRoleList(dialog)
        dialog.ship_role_list.buildView(column=0, row=0, columnspan=2, rowspan=1)
        dialog.quitButton = ttk.Button(dialog, text='Quit', command=dialog.destroy)
        dialog.quitButton.grid(column=0, row=1)
        dialog.grab_set() # Rende la finestra MODALE (blocca l'interazione con la principale finché non la chiudi)


        
