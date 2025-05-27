import locale
from sqlalchemy import Numeric, select
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from model.ship import Ship
from service.dblink import DBLink
from service.ship_service import ShipService

locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class ShipView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.nameLabel = ttk.Label(self.parent, text="Name")
        self.nameLabel.grid(column=0, row=0)
        self.entryName = ttk.Entry(self.parent)
        self.entryName.grid(column=1, row=0)
        self.parent.grab_set() # Rende la finestra MODALE (blocca l'interazione con la principale finché non la chiudi)