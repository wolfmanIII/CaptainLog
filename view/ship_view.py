import locale
import ulid
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from model.ship import Ship
from service.dblink import DBLink

locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class ShipView(ttk.Frame):
    def __init__(self, master, router):
        super().__init__(master)
        self.parent = master
        self.router = router
        self.session = DBLink().getSession()

        self.vars = {
            "name": tk.StringVar(),
            "type": tk.StringVar(),
            "model": tk.StringVar(),
            "ship_price": tk.DoubleVar()
        }

        self.columns = {
            "name": "Name",
            "type": "Type",
            "model": "Model",
            "ship_price": "Price(Cr)"
        }

        for i, (key, var) in enumerate(self.vars.items()):
            ttk.Label(self, text=self.columns[key]).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            ttk.Entry(self, textvariable=var).grid(row=i, column=1, sticky="ew", padx=5, pady=5)

        ttk.Button(self, text="Salva", command=self.save).grid(row=len(self.vars), column=0, columnspan=2, pady=10)

    def save(self):
        data = {k: v.get() for k, v in self.vars.items()}
        ship = Ship(**data)
        ship.code = ulid.new().str
        self.session.add(ship)
        self.session.commit()
        self.router.get_view("ships").refresh()
        self.parent.destroy()