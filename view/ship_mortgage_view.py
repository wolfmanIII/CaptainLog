from decimal import Decimal
import locale
from pydoc import text
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from warnings import showwarning
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import ulid

from model import ship_mortgage
from model import insurance
from model.insurance import Insurance
from model.ship import Ship
from model.ship_mortage_interest_rate import ShipMortageInterestRate
from model.ship_mortgage import ShipMortgage
from service.dblink import DBLink
from util.emoji_cache import EmojiCache
from util.masked_numeric_entry import MaskedNumericEntry
from util.ship_mortgage_plot import ShipMortgagePlot
from util.view_validator import ViewValidator

locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class ShipMortgageView(ttk.Frame):

    def __init__(self, master, router):
        super().__init__(master)
        self.router = router
        self.session = DBLink().getSession()
        self.rates = self.session.query(ShipMortageInterestRate).order_by(ShipMortageInterestRate.duration.desc()).all()
        self.ships = self.session.query(Ship).order_by(Ship.name).all()
        self.insurances = self.session.query(Insurance).order_by(Insurance.annual_cost).all()

        self.lock_selection = False
        self.last_selected_rate = None
        self.last_selected_ship = None
        self.last_selected_insurance = None

        self.readonly = False

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
            "insurance_check": tk.IntVar()
        }

        if self.ship_mortgage.id is not None:
            self.readonly = True
            self.vars["ship_shares"].set(self.ship_mortgage.ship_shares)
            self.vars["discount"].set(self.ship_mortgage.discount)
            formatted_advance_payment = f"{self.ship_mortgage.advance_payment:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.vars["advance_payment"].set(formatted_advance_payment)
            self.vars["start_day"].set(self.ship_mortgage.start_day)
            self.vars["start_year"].set(self.ship_mortgage.start_year)
            self.vars["insurance_check"].set(1 if self.ship_mortgage.insurance_id is not None else 0)
        else:
            self.vars["ship_shares"].set(0)
            self.vars["discount"].set(0)
            self.vars["advance_payment"].set("0")
            self.vars["start_day"].set(2)
            self.vars["start_year"].set(1105)
            self.vars["insurance_check"].set(0)

        self.entries = []
        self.create_widgets()
        self.populate_data()
        self.on_insurance_check_toggle()
        self.lock_entries()
        self.lock_treeviews()
        if self.readonly:
            self.calculate()


    def create_widgets(self):
        row = 0
        self.img_title_tk = EmojiCache(size=32).get("1f4b8.png") # Money with wings
        self.title_label = ttk.Label(self, text="Ship Mortgage", font=("", 30), image=self.img_title_tk, compound="left")
        self.title_label.grid(column=0, row=row, padx=10, pady=10, sticky="w", columnspan=6)
        row = row + 1

        buttonGroup = ButtonGroup(self, self.router, self.readonly)
        buttonGroup.grid(column=0, row=1, padx=5, pady=5, sticky="nsew", columnspan=6)
        row = row + 1

        # Fields
        ttk.Label(self, text="Ship shares").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.shares_entry = ttk.Spinbox(self, textvariable=self.vars["ship_shares"], width=5, from_=0, to=1000)
        self.shares_entry.grid(row=row+1, column=0, sticky="w", padx=5, pady=5)
        self.entries.append(self.shares_entry)

        ttk.Label(self, text="Discount(%)").grid(row=row, column=1, sticky="w", padx=5, pady=5)
        self.discount_entry = ttk.Spinbox(self, textvariable=self.vars["discount"], width=5, from_=0, to=100)
        self.discount_entry.grid(row=row+1, column=1, sticky="w", padx=5, pady=5)
        self.entries.append(self.discount_entry)

        ttk.Label(self, text="Advance payment(Cr)").grid(row=row, column=2, sticky="w", padx=5, pady=5)
        self.advance_entry = MaskedNumericEntry(self, textvariable=self.vars["advance_payment"], width=15, min_value=0, max_value=100_000_000_000)
        self.advance_entry.grid(row=row+1, column=2, sticky="w", padx=5, pady=5)
        self.entries.append(self.advance_entry)

        ttk.Label(self, text="Start day").grid(row=row, column=3, sticky="w", padx=5, pady=5)
        self.day_entry = ttk.Spinbox(self, textvariable=self.vars["start_day"], width=5, from_=1, to=365)
        self.day_entry.grid(row=row+1, column=3, sticky="w", padx=5, pady=5)
        self.entries.append(self.day_entry)

        ttk.Label(self, text="Start year").grid(row=row, column=4, sticky="w", padx=5, pady=5)
        self.year_entry = ttk.Spinbox(self, textvariable=self.vars["start_year"], width=5, from_=1105, to=2000)
        self.year_entry.grid(row=row+1, column=4, sticky="w", padx=5, pady=5)
        self.entries.append(self.year_entry)
        # end Fields

        row = row + 2

        self.img_ship_tk = EmojiCache(size=24).get("2708.png") # Airplane
        self.ship_label = ttk.Label(self, text="Ships", font=("", 18), image=self.img_ship_tk, compound="left")
        self.ship_label.grid(column=0, row=row, padx=10, pady=5, sticky="w", columnspan=6)
        row = row + 1

        vsb = ttk.Scrollbar(self, orient="vertical")
        vsb.grid(row=row, column=4, sticky="ns")

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
        self.ship_tree.grid(column=0, row=row, padx=5, pady=5, sticky="w", columnspan=6)
        row = row + 1


        self.img_rate_tk = EmojiCache(size=24).get("1f4c8.png") # Chart increasing
        self.rate_label = ttk.Label(self, text="Annual interest rates", font=("", 18), image=self.img_rate_tk, compound="left")
        self.rate_label.grid(column=0, row=row, padx=10, pady=5, sticky="w", columnspan=3)

        self.insurance_checkbox = ttk.Checkbutton(self, text="Insurance", variable=self.vars["insurance_check"], command=lambda: self.on_insurance_check_toggle())
        self.insurance_checkbox.grid(column=3, row=row, padx=5, pady=5, sticky="w")

        self.img_coverage_tk = EmojiCache(size=16).get("1f6df.png") # Ring buoy
        self.coverage_button = ttk.Button(self, text="Coverage", image=self.img_coverage_tk, compound="left", command=lambda: self.insurance_coverage_view())
        self.coverage_button.grid(column=4, row=row, padx=10, pady=10, sticky="w")
        row = row + 1

        rate_columns = ["Duration(years)", "Ship cost multiplier", "Annual interest rate(%)"]
        self.rate_tree = ttk.Treeview(self, columns=rate_columns, show="headings", height=4, selectmode="browse")
        for column in rate_columns:
            text_show = column
            self.rate_tree.heading(column, text=text_show)

        self.rate_tree.column('Duration(years)', anchor="e")
        self.rate_tree.column('Ship cost multiplier', anchor="e")
        self.rate_tree.column('Annual interest rate(%)', anchor="e")

        self.rate_tree.grid(column=0, row=row, padx=5, pady=5, sticky="w", columnspan=3)

        insurance_columns = ["Type", "Annual cost(% ship price)"]
        self.insurance_tree = ttk.Treeview(self, columns=insurance_columns, show="headings", height=4, selectmode="browse")
        for column in insurance_columns:
            text_show = column
            self.insurance_tree.heading(column, text=text_show)

        self.insurance_tree.column('Annual cost(% ship price)', anchor="e")
        self.insurance_tree.grid(column=3, row=row, padx=5, pady=5, sticky="w", columnspan=3)
        row = row + 1

        self.img_mortage_tk = EmojiCache(size=24).get("1f911.png") # Chart decreasing
        self.mortagage_label = ttk.Label(self, text="Ship mortgage summary", font=("", 18), image=self.img_mortage_tk, compound="left")
        self.mortagage_label.grid(column=0, row=row, padx=10, pady=5, sticky="w", columnspan=6)
        row = row + 1

        mortage_columns = ["Ship cost(Cr)", "Monthly fee(Cr)", "Annual fee(Cr)", "Total mortgage(Cr)", "Monthly fee + insurance(Cr)", "Annual insurance(Cr)"]
        self.mortgage_tree = ttk.Treeview(self, columns=mortage_columns, show="headings", height=1, selectmode="browse")
        for column in mortage_columns:
            text_show = column
            self.mortgage_tree.heading(column, text=text_show)
        self.mortgage_tree.column('Ship cost(Cr)', anchor="e")
        self.mortgage_tree.column('Monthly fee(Cr)', anchor="e")
        self.mortgage_tree.column('Annual fee(Cr)', anchor="e")
        self.mortgage_tree.column('Total mortgage(Cr)', anchor="e")
        self.mortgage_tree.column('Monthly fee + insurance(Cr)', anchor="e")
        self.mortgage_tree.column('Annual insurance(Cr)', anchor="e")
        self.mortgage_tree.grid(column=0, row=row, padx=5, pady=5, sticky="w", columnspan=6)
        row = row + 1

    def populate_data(self):
        for rate in self.rates:        
            values = (
                rate.duration,
                locale.format_string('%.2f', rate.ship_price_multiplier, grouping=True),
                locale.format_string('%.2f', rate.annual_interest_rate, grouping=True)
            )
            self.rate_tree.insert('', 'end', iid=rate.id, text='Listbox', values=values)

            if self.ship_mortgage.id is not None:
                if rate.id == self.ship_mortgage.rate_id:
                    self.rate_tree.selection_set(self.ship_mortgage.rate_id)
        
        
        for ship in self.ships:
            values = (ship.code, ship.name, ship.type, ship.model, locale.format_string('%.2f', ship.ship_price, grouping=True))
            self.ship_tree.insert('', 'end', iid=ship.id, text='Listbox', values=values)

            if self.ship_mortgage.id is not None:
                if ship.id == self.ship_mortgage.ship_id:
                    self.ship_tree.selection_set(self.ship_mortgage.ship_id)

        for insurance in self.insurances:
            values = (insurance.name, locale.format_string('%.2f', insurance.annual_cost, grouping=True))
            self.insurance_tree.insert('', 'end', iid=insurance.id, text='Listbox', values=values)

            if self.ship_mortgage.id is not None:
                if insurance.id == self.ship_mortgage.insurance_id:
                    self.insurance_tree.selection_set(self.ship_mortgage.insurance_id)

    def calculate(self):
        # azzero l'unica riga del summary
        children = self.mortgage_tree.get_children()
        if children:
            primo_id = children[0]
            self.mortgage_tree.delete(primo_id)

        ship_cost = self.ship_cost()
        if ship_cost <= 0:
            return False

        selected_rate = self.rate_tree.selection()
        try:
            rate_id = selected_rate[0]
            rate = self.session.query(ShipMortageInterestRate).get(rate_id)
            self.selected_rate = rate
        except IndexError:
            showerror("Error", "Select a rate!")
            return False
        
        monthly_payment = (
            (ship_cost * rate.ship_price_multiplier) / rate.duration
        ) / 12
        annual_payment = monthly_payment * 12

        monthly_payment_insurance = monthly_payment + self.insurance_cost()
        annual_insurance = self.insurance_cost() * 12
        total_mortage = ship_cost * rate.ship_price_multiplier

        values = (
            locale.format_string('%.2f', float(ship_cost), grouping=True),
            locale.format_string('%.2f', float(monthly_payment), grouping=True),
            locale.format_string('%.2f', float(annual_payment), grouping=True),
            locale.format_string('%.2f', float(total_mortage), grouping=True),
            locale.format_string('%.2f', float(monthly_payment_insurance), grouping=True),
            locale.format_string('%.2f', float(annual_insurance), grouping=True)
        )
        self.mortgage_tree.insert('', 'end', text='Listbox', values=values)
        return True
    
    def insurance_cost(self):
        try:
            selected_insurance = self.insurance_tree.selection()
            insurance_id = selected_insurance[0]
            insurance = self.session.query(Insurance).get(insurance_id)
            self.selected_insurance = insurance
            insurance_cost = self.selected_ship.ship_price / 100 * insurance.annual_cost / 12
            return insurance_cost
        except IndexError:
            return 0

    def ship_cost(self):
        try:
            selected_ship = self.ship_tree.selection()
            ship_id = selected_ship[0]
            ship = self.session.query(Ship).get(ship_id)
            self.selected_ship = ship
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
        except IndexError:
            showerror("Error", "Select a ship!")
            return 0

    def view_plot(self):
        if self.ship_cost() > Decimal(0):
            data = {
                "ship_cost": self.ship_cost(),
                "rates": self.rates,
            }
            self.dialog = tk.Toplevel(self)
            self.dialog.title("Ship mortgage chart")
            plot_view = PlotView(self.dialog, data)
            plot_view.pack(fill="both", expand=True, padx=10, pady=10)
            self.dialog.wait_visibility()
            self.dialog.grab_set()

    def save(self):
        if ViewValidator(self.entries).is_valid():
             if self.calculate():
                self.ship_mortgage.code = ulid.new().str
                self.ship_mortgage.name = self.selected_ship.name + " mortgage"
                self.ship_mortgage.ship_shares = self.vars["ship_shares"].get()
                self.ship_mortgage.discount = self.vars["discount"].get()
                cleaned_advance_payment = self.vars["advance_payment"].get().replace(".", "").replace(",", ".")
                self.ship_mortgage.advance_payment = cleaned_advance_payment
                self.ship_mortgage.rate_id = self.selected_rate.id
                self.ship_mortgage.ship_id = self.selected_ship.id
                self.ship_mortgage.insurance_id = self.selected_insurance.id
                self.ship_mortgage.start_day = self.vars["start_day"].get()
                self.ship_mortgage.start_year = self.vars["start_year"].get()
                self.session.add(self.ship_mortgage)
                self.session.commit()
                self.router.navigate("ship_mortgage")
    
    def delete(self):
        self.session.delete(self.ship_mortgage)
        self.session.commit()
        self.router.navigate("ship_mortgage")

    def lock_treeviews(self):
        if self.readonly:
            def block_event(event):
                return "break"
            # Blocca selezione con click
            self.ship_tree.bind("<Button-1>", block_event)
            self.rate_tree.bind("<Button-1>", block_event)
            self.mortgage_tree.bind("<Button-1>", block_event)
            self.insurance_tree.bind("<Button-1>", block_event)

            # Blocca selezione con tastiera
            self.ship_tree.bind("<Key>", block_event)
            self.rate_tree.bind("<Key>", block_event)
            self.mortgage_tree.bind("<Key>", block_event)
            self.insurance_tree.bind("<Key>", block_event)
            self.insurance_checkbox.config(state="disabled")

    def lock_entries(self):
        if self.readonly:
            for entry in self.entries:
                try:
                    entry.configure(state="disabled")
                except Exception as e:
                    print(f"Errore disabilitando {entry}: {e}")

    def insurance_coverage_view(self):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Insurance coverage")
        ship_view = InsuranceCoverageView(self.dialog, self.router, self.insurances)
        ship_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.dialog.wait_visibility()
        self.dialog.grab_set()

    def on_insurance_check_toggle(self):
        def block_event(event):
            return "break"
        stato = self.vars["insurance_check"].get()
        if stato == 1:
            self.insurance_tree.unbind("<Button-1>")
            self.insurance_tree.unbind("<Key>")
        else:
            self.insurance_tree.bind("<Button-1>", block_event)
            self.insurance_tree.bind("<Key>", block_event)
            self.insurance_tree.selection_remove(self.insurance_tree.selection())

class InsuranceCoverageView(ttk.Frame):
    def __init__(self, master, router, insurances):
        super().__init__(master)
        self.parent = master
        self.router = router

        self.img_coverage_tk = EmojiCache(size=16).get("1f6df.png") # Ring buoy
        self.title_label = ttk.Label(self, text="Insurance coverage", font=("", 18), image=self.img_coverage_tk, compound="left")
        self.title_label.grid(column=0, row=0, padx=10, pady=10, columnspan=3)

        column_img_vars = {
            0: "1f7e2.png",
            1: "2b50.png",
            2: "1f31f.png"
        }

        column = 0
        for insurance in insurances:
            img_tk = EmojiCache(size=24).get(column_img_vars[column]) # Chart decreasing
            name_label = ttk.Label(self, text=insurance.name, font=("", 14), image=img_tk, compound="left")
            name_label.grid(column=column, row=1, padx=5, pady=10, sticky="w")
            index = 1
            row = 2
            for coverage in insurance.coverage:
                covarage_label = ttk.Label(self, text=str(index) + ". " + coverage)
                covarage_label.grid(column=column, row=row, padx=10, pady=5, sticky="w")
                index = index + 1
                row = row + 1
            column = column + 1

        
        img_name_tk = EmojiCache(size=24).get("26d4.png") # Chart decreasing
        name_label = ttk.Label(self, text="Common exclusions (all levels)", font=("", 14), image=img_name_tk, compound="left")
        name_label.grid(column=0, row=row, padx=10, pady=10, sticky="w", columnspan=3)
        row = row + 1

        exclusion_1_label = ttk.Label(self, text="1. Intentional acts or negligence (drunk pilot, uncontrolled jumps)")
        exclusion_1_label.grid(column=0, row=row, padx=10, pady=5, sticky="w", columnspan=3)
        row = row + 1

        exclusion_2_label = ttk.Label(self, text="2. Undeclared Illegal Missions")
        exclusion_2_label.grid(column=0, row=row, padx=10, pady=5, sticky="w", columnspan=3)
        row = row + 1

        exclusion_2_label = ttk.Label(self, text="3. Unapproved modifications to the ship")
        exclusion_2_label.grid(column=0, row=row, padx=10, pady=5, sticky="w", columnspan=3)
        row = row + 1
        
    
            
class ButtonGroup(ttk.Frame):

    def __init__(self, parent, router, readonly=False):
        super().__init__(parent, borderwidth=1, relief="solid")

        self.img_back_tk = EmojiCache(size=16).get("2b05.png") # Back
        self.home_button = ttk.Button(self, text="Back", command=lambda: router.navigate("home"), image=self.img_back_tk, compound="left")
        self.home_button.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        self.img_graph_tk = EmojiCache(size=16).get("1f4c9.png") # Chart decreasing
        self.graph_button = ttk.Button(self, text="Chart", image=self.img_graph_tk, compound="left", command=lambda: parent.view_plot())
        self.graph_button.grid(column=1, row=0, padx=10, pady=10, sticky="w")

        self.img_calculate_tk = EmojiCache(size=16).get("2699.png") # Back
        self.calculate_button = ttk.Button(
            self, text="Calculate", image=self.img_calculate_tk,
            state="disabled" if readonly else "normal",
            compound="left", command=lambda: parent.calculate()
        )
        self.calculate_button.grid(column=2, row=0, padx=10, pady=10, sticky="w")

        self.img_save_tk = EmojiCache(size=16).get("1f4be.png") # Save
        self.save_button = ttk.Button(
            self, text="Save", image=self.img_save_tk, compound="left",
            state="disabled" if readonly else "normal",
            command=lambda: parent.save()
        )
        self.save_button.grid(column=3, row=0, padx=10, pady=10, sticky="w")

        self.img_delete_tk = EmojiCache(size=16).get("1f6ae.png") # Trash
        self.delete_button = ttk.Button(
            self, text="Delete", image=self.img_delete_tk, compound="left",
            state="disabled" if not readonly else "normal",
            command=lambda: parent.delete()
        )
        self.delete_button.grid(column=4, row=0, padx=10, pady=10, sticky="w")

class PlotView(ttk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent, relief="solid")

        plotter = ShipMortgagePlot(
            principal=data["ship_cost"],
            durations = [rate.duration for rate in data["rates"]],
            multipliers=[rate.ship_price_multiplier for rate in data["rates"]]
        )

        fig = plotter.create_figure()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)