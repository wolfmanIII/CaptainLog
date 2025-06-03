import locale
import tkinter as tk
from tkinter import ttk

from pyparsing import col

from model.ship import Ship
from model.ship_mortage_interest_rate import ShipMortageInterestRate
from model.ship_mortgage import ShipMortgage
from service.dblink import DBLink
from util.emoji_cache import EmojiCache

locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class ShipMortgageView(ttk.Frame):

    def __init__(self, master, router):
        super().__init__(master)
        self.router = router
        self.session = DBLink().getSession()
        self.rates = self.session.query(ShipMortageInterestRate).order_by(ShipMortageInterestRate.duration.desc()).all()
        self.ships = self.session.query(Ship).order_by(Ship.name).all()

        try:
            self.ship_mortgage = self.session.query(ShipMortgage).one()
        except Exception:
            self.ship_mortgage = ShipMortgage()

        self.entries = []
        self.create_widgets()
        self.populate_data_rates()

    def create_widgets(self):
        self.img_title_tk = EmojiCache(size=32).get("1f4b8.png") # Money with wings
        self.title_label = ttk.Label(self, text="Ship Mortgage", font=("", 30), image=self.img_title_tk, compound="left")
        self.title_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        buttonGroup = ButtonGroup(self, self.router)
        buttonGroup.grid(column=0, row=1, padx=5, pady=5, sticky="w")

        self.img_rate_tk = EmojiCache(size=20).get("1f4c8.png") # Chart increasing
        self.rate_label = ttk.Label(self, text="Annual interest rates", font=("", 18), image=self.img_rate_tk, compound="left")
        self.rate_label.grid(column=0, row=2, padx=10, pady=5, sticky="w")

        columns = ["Duration(years)", "Ship cost multiplier", "Mortgage payment divider", "Annual interest rate(%)"]
        self.mortgage_tree = ttk.Treeview(self, columns=columns, show="headings", height=4)
        for column in columns:
            text_show= ""
            text_show = column
            self.mortgage_tree.heading(column, text=text_show)

        self.mortgage_tree.grid(column=0, row=3, padx=5, pady=5, columnspan=2)

        row = 4
        ttk.Label(self, text="Ship").grid(row=row, column=0, sticky="w", padx=10, pady=0)
        self.ship_combo = ttk.Combobox(self, state="readonly")
        self.ship_combo["values"] = [p.name for p in self.ships]
        row = row + 1
        self.ship_combo.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.entries.append(self.ship_combo)
        row = row + 1
        if self.ship_mortgage.id is not None:
            for i, ship in enumerate(self.ships):
                if ship.id == self.ship_mortage.ship_id:
                    self.ship_combo.current(i)
                    break

    def populate_data_rates(self):
        for rate in self.rates:        
            values = (
                rate.duration,
                locale.format_string('%.2f', rate.ship_price_multiplier, grouping=True),
                rate.ship_price_divider,
                locale.format_string('%.2f', rate.annual_interest_rate, grouping=True)
            )
            self.mortgage_tree.insert('', 'end', iid=rate.id, text='Listbox', values=values)

        self.mortgage_tree.column('Duration(years)', anchor="e")
        self.mortgage_tree.column('Ship cost multiplier', anchor="e")
        self.mortgage_tree.column('Annual interest rate(%)', anchor="e")
        self.mortgage_tree.column('Mortgage payment divider', anchor="e")


class ButtonGroup(ttk.Frame):

    def __init__(self, parent, router):
        super().__init__(parent, borderwidth=1, relief="solid")

        self.img_back_tk = EmojiCache(size=16).get("2b05.png") # Back
        self.home_button = ttk.Button(self, text="Back", command=lambda: router.navigate("home"), image=self.img_back_tk, compound="left")
        self.home_button.grid(column=0, row=0, padx=10, pady=10, sticky="w")

class ShipMortgageFrame(ttk.Frame):

    def __init__(self, parent, router):
        super().__init__(parent, borderwidth=1, relief="solid")
        
        row = 1
        ttk.Label(self, text="Ship").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.ship_combo = ttk.Combobox(self, state="readonly")
        self.ship_combo["values"] = [p.name for p in parent.ships]
        self.ship_combo.grid(row=row, column=1, padx=10, pady=10)
        parent.entries.append(self.ship_combo)
        row = row + 1
        if parent.ship_mortgage.id is not None:
            for i, ship in enumerate(self.ships):
                if ship.id == parent.ship_mortage.ship_id:
                    self.ship_combo.current(i)
                    break
