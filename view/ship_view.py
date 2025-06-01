import locale
from numpy import size
from sqlalchemy import null
import ulid
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from model.ship import Ship
from service.dblink import DBLink
from util.masked_numeric_entry import MaskedNumericEntry
from util.view_validator import ViewValidator

locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class ShipView(ttk.Frame):
    def __init__(self, master, router, id=None):
        super().__init__(master)
        self.parent = master
        self.router = router
        self.session = DBLink().getSession()
        self.ship = Ship()

        ttk.Label(self, text="Ship", font=("", 18)).grid(column=0, row=0, columnspan=2, padx=10, pady=10)
                
        self.vars = {
            "code": tk.StringVar(),
            "name": tk.StringVar(),
            "type": tk.StringVar(),
            "model": tk.StringVar(),
            "ship_price": tk.StringVar()
        }

        if id is not None:
            self.ship = self.session.get(Ship, id)
            self.vars["code"].set(self.ship.code)
            self.vars["name"].set(self.ship.name)
            self.vars["type"].set(self.ship.type)
            self.vars["model"].set(self.ship.model)
            self.vars["ship_price"].set(self.ship.ship_price)
        else:
             self.vars["ship_price"].set("0")

        self.columns = {
            "code": "Code",
            "name": "Name",
            "type": "Type",
            "model": "Model",
            "ship_price": "Price(Cr)"
        }

        self.entries = []

        for i, (key, var) in enumerate(self.vars.items()):
            if id is None and key == "code":
                continue
            i = i + 1
            ttk.Label(self, text=self.columns[key]).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            if key == "ship_price":
                entry = MaskedNumericEntry(self, textvariable=var, width=40, min_value=0, max_value=100_000_000_000)
            else:
                entry = ttk.Entry(self, textvariable=var, width=40)
            entry.grid(row=i, column=1, sticky="we", padx=5, pady=5)
            if key == "code":
                entry.configure(state="readonly")
            self.entries.append(entry)

        ttk.Button(self, text="Save", command=lambda: self.save()).grid(row=len(self.vars)+1, column=1, padx=5, pady=5, sticky="w")

    def save(self):

        if ViewValidator(self.entries).is_valid():
            data = {k: v.get() for k, v in self.vars.items()}

            for k, v in data.items():
                setattr(self.ship, k, v)

            cleaned_ship_price = self.ship.ship_price.replace(".", "").replace(",", ".")
            self.ship.ship_price = float(cleaned_ship_price)

            if self.ship.id is None:
                self.ship.code = ulid.new().str
                self.session.add(self.ship)

            self.session.commit()
            self.router.get_view("ships").refresh()
            self.parent.destroy()