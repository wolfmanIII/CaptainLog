from decimal import Decimal
import locale
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from model import ship_mortgage
from model.ship import Ship
from model.ship_mortage_interest_rate import ShipMortageInterestRate
from model.ship_mortgage import ShipMortgage
from service.dblink import DBLink
from util.emoji_cache import EmojiCache
from util.masked_numeric_entry import MaskedNumericEntry
from util.ship_mortgage_plot import MutuoTravellerPlot

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

        self.vars = {
            "ship_shares": tk.IntVar(),
            "discount": tk.IntVar(),
            "advance_payment": tk.StringVar(),
            "start_day": tk.IntVar(),
            "start_year": tk.IntVar(),
        }

        if self.ship_mortgage.id is not None:
            self.vars["ship_shares"].set(self.ship_mortgage.ship_shares)
            self.vars["discount"].set(self.ship_mortgage.discount)
            formatted_advance_payment = f"{self.ship_mortgage.advance_payment:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.vars["advance_payment"].set(formatted_advance_payment)
            self.vars["start_day"].set(self.ship_mortgage.start_day)
            self.vars["start_year"].set(self.ship_mortgage.start_year)
        else:
            self.vars["ship_shares"].set(0)
            self.vars["discount"].set(0)
            self.vars["advance_payment"].set("0")
            self.vars["start_day"].set(2)
            self.vars["start_year"].set(1105)

        self.entries = []
        self.create_widgets()
        self.populate_data()


    def create_widgets(self):
        row = 0
        self.img_title_tk = EmojiCache(size=32).get("1f4b8.png") # Money with wings
        self.title_label = ttk.Label(self, text="Ship Mortgage", font=("", 30), image=self.img_title_tk, compound="left")
        self.title_label.grid(column=0, row=row, padx=10, pady=10, sticky="w", columnspan=5)
        row = row + 1

        buttonGroup = ButtonGroup(self, self.router)
        buttonGroup.grid(column=0, row=1, padx=5, pady=5, sticky="w", columnspan=5)
        row = row + 1

        # Fields
        ttk.Label(self, text="Ship shares").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.shares_entry = ttk.Spinbox(self, textvariable=self.vars["ship_shares"], width=5, from_=0, to=1000)
        self.shares_entry.grid(row=row+1, column=0, sticky="w", padx=5, pady=5)

        ttk.Label(self, text="Discount(%)").grid(row=row, column=1, sticky="w", padx=5, pady=5)
        self.discount_entry = ttk.Spinbox(self, textvariable=self.vars["discount"], width=5, from_=0, to=100)
        self.discount_entry.grid(row=row+1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(self, text="Advance payment(Cr)").grid(row=row, column=2, sticky="w", padx=5, pady=5)
        self.advance_entry = MaskedNumericEntry(self, textvariable=self.vars["advance_payment"], width=15, min_value=0, max_value=100_000_000_000)
        self.advance_entry.grid(row=row+1, column=2, sticky="w", padx=5, pady=5)

        ttk.Label(self, text="Start day").grid(row=row, column=3, sticky="w", padx=5, pady=5)
        self.day_entry = ttk.Spinbox(self, textvariable=self.vars["start_day"], width=5, from_=1, to=365)
        self.day_entry.grid(row=row+1, column=3, sticky="w", padx=5, pady=5)

        ttk.Label(self, text="Start year").grid(row=row, column=4, sticky="w", padx=5, pady=5)
        self.year_entry = ttk.Spinbox(self, textvariable=self.vars["start_year"], width=5, from_=1105, to=2000)
        self.year_entry.grid(row=row+1, column=4, sticky="w", padx=5, pady=5)
        # end Fields

        row = row + 2

        self.img_ship_tk = EmojiCache(size=24).get("2708.png") # Airplane
        self.ship_label = ttk.Label(self, text="Ships", font=("", 18), image=self.img_ship_tk, compound="left")
        self.ship_label.grid(column=0, row=row, padx=10, pady=5, sticky="w", columnspan=5)
        row = row + 1

        vsb = ttk.Scrollbar(self, orient="vertical")
        vsb.grid(row=row, column=1, sticky="ns")

        ship_columns = ["code", "name", "type", "model", "price"]
        self.ship_tree = ttk.Treeview(self, columns=ship_columns, show="headings", yscrollcommand=vsb.set, height=5, selectmode="browse")
        vsb.config(command=self.ship_tree.yview)
        for column in ship_columns:
            text_show= ""
            if column == "price":
                text_show = column.capitalize() + "(Cr)"
            else:
                text_show = column.capitalize()
            self.ship_tree.heading(column, text=text_show)

        self.ship_tree.column('price', anchor="e")
        self.ship_tree.grid(column=0, row=row, padx=5, pady=5, sticky="w", columnspan=5)
        row = row + 1


        self.img_rate_tk = EmojiCache(size=24).get("1f4c8.png") # Chart increasing
        self.rate_label = ttk.Label(self, text="Annual interest rates", font=("", 18), image=self.img_rate_tk, compound="left")
        self.rate_label.grid(column=0, row=row, padx=10, pady=5, sticky="w", columnspan=5)
        row = row + 1

        rate_columns = ["Duration(years)", "Ship cost multiplier", "Mortgage payment divider(≈)", "Annual interest rate(%)"]
        self.rate_tree = ttk.Treeview(self, columns=rate_columns, show="headings", height=4, selectmode="browse")
        for column in rate_columns:
            text_show = column
            self.rate_tree.heading(column, text=text_show)

        self.rate_tree.column('Duration(years)', anchor="e")
        self.rate_tree.column('Ship cost multiplier', anchor="e")
        self.rate_tree.column('Annual interest rate(%)', anchor="e")
        self.rate_tree.column('Mortgage payment divider(≈)', anchor="e")

        self.rate_tree.grid(column=0, row=row, padx=5, pady=5, sticky="w", columnspan=5)
        row = row + 1

        self.img_mortage_tk = EmojiCache(size=24).get("1f911.png") # Chart decreasing
        self.mortagage_label = ttk.Label(self, text="Ship mortgage summary", font=("", 18), image=self.img_mortage_tk, compound="left")
        self.mortagage_label.grid(column=0, row=row, padx=10, pady=5, sticky="w", columnspan=5)
        row = row + 1

        mortage_columns = ["Ship cost(Cr)", "Monthly payment(Cr)", "Annual payment(Cr)", "Total Mortagage(Cr)"]
        self.mortgage_tree = ttk.Treeview(self, columns=mortage_columns, show="headings", height=1, selectmode="browse")
        for column in mortage_columns:
            text_show = column
            self.mortgage_tree.heading(column, text=text_show)
        self.mortgage_tree.column('Ship cost(Cr)', anchor="e")
        self.mortgage_tree.column('Monthly payment(Cr)', anchor="e")
        self.mortgage_tree.column('Annual payment(Cr)', anchor="e")
        self.mortgage_tree.column('Total Mortagage(Cr)', anchor="e")
        self.mortgage_tree.grid(column=0, row=row, padx=5, pady=5, sticky="w", columnspan=5)
        row = row + 1

    def populate_data(self):
        for rate in self.rates:        
            values = (
                rate.duration,
                locale.format_string('%.2f', rate.ship_price_multiplier, grouping=True),
                rate.ship_price_divider,
                locale.format_string('%.2f', rate.annual_interest_rate, grouping=True)
            )
            self.rate_tree.insert('', 'end', iid=rate.id, text='Listbox', values=values)
        
        for ship in self.ships:
            values = (ship.code, ship.name, ship.type, ship.model, locale.format_string('%.2f', ship.ship_price, grouping=True))
            self.ship_tree.insert('', 'end', iid=ship.id, text='Listbox', values=values)

    def calculate(self):

        # azzero l'unica riga del summary
        children = self.mortgage_tree.get_children()
        if children:
            primo_id = children[0]
            self.mortgage_tree.delete(primo_id)

        ship_cost = self.ship_cost()

        selected_rate = self.rate_tree.selection()
        rate_id = selected_rate[0]
        rate = self.session.query(ShipMortageInterestRate).get(rate_id)

        monthly_payment = (
            (ship_cost * rate.ship_price_multiplier) / rate.duration
        ) / 12
        annual_payment = monthly_payment * 12
        totale_mortage = ship_cost * rate.ship_price_multiplier

        values = (
            locale.format_string('%.2f', ship_cost, grouping=True),
            locale.format_string('%.2f', monthly_payment, grouping=True),
            locale.format_string('%.2f', annual_payment, grouping=True),
            locale.format_string('%.2f', totale_mortage, grouping=True)
        )
        self.mortgage_tree.insert('', 'end', text='Listbox', values=values)

    def ship_cost(self):
        try:
            selected_ship = self.ship_tree.selection()
            ship_id = selected_ship[0]
            ship = self.session.query(Ship).get(ship_id)
            ship_cost = ship.ship_price
            if self.vars['ship_shares'].get() > 0:
                ship_cost = ship_cost - (self.vars['ship_shares'].get() * 1000000)

            if self.vars['discount'].get() > 0:
                discount = ship.ship_price * self.vars['discount'].get() / 100
                ship_cost = ship_cost - discount

            advance_payment = float(self.vars["advance_payment"].get().replace(".", "").replace(",", "."))
            if advance_payment > 0:
                ship_cost = ship_cost - Decimal(advance_payment)

            return ship_cost
        except Exception:
            return 0

    def view_plot(self):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Ship mortgage chart")
        data = {
            "ship_cost": self.ship_cost(),
            "rates": self.rates,
        }
        plot_view = PlotView(self.dialog, data)
        plot_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.dialog.wait_visibility()
        self.dialog.grab_set()

class ButtonGroup(ttk.Frame):

    def __init__(self, parent, router):
        super().__init__(parent, borderwidth=1, relief="solid")

        self.img_back_tk = EmojiCache(size=16).get("2b05.png") # Back
        self.home_button = ttk.Button(self, text="Back", command=lambda: router.navigate("home"), image=self.img_back_tk, compound="left")
        self.home_button.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        self.img_calculate_tk = EmojiCache(size=16).get("2699.png") # Back
        self.calculate_button = ttk.Button(self, text="Calculate", image=self.img_calculate_tk, compound="left", command=lambda: parent.calculate())
        self.calculate_button.grid(column=1, row=0, padx=10, pady=10, sticky="w")

        self.img_graph_tk = EmojiCache(size=16).get("1f4c9.png") # Chart decreasing
        self.graph_button = ttk.Button(self, text="Chart", image=self.img_graph_tk, compound="left", command=lambda: parent.view_plot())
        self.graph_button.grid(column=2, row=0, padx=10, pady=10, sticky="w")

class PlotView(ttk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent, relief="solid")

        plotter = MutuoTravellerPlot(
            principal=data["ship_cost"],
            durations = [rate.duration for rate in data["rates"]],
            multipliers=[rate.ship_price_multiplier for rate in data["rates"]]
        )

        fig = plotter.create_figure()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

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
