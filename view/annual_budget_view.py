import ulid
import tkinter as tk
from tkinter import IntVar, ttk
import tkinter.font as tkFont

from model.annual_budget import AnnualBudget
from model.ship_mortgage import ShipMortgage
from service.dblink import DBLink
from util.emoji_cache import EmojiCache
from util.view_validator import ViewValidator

class AnnualBudgetView(ttk.Frame):
    def __init__(self, master, router, id=None):
        super().__init__(master)
        self.parent = master
        self.router = router
        self.session = DBLink().getSession()
        self.annual_budget = AnnualBudget()
        self.mortgages = self.session.query(ShipMortgage).order_by(ShipMortgage.name).all()
                
        self.vars = {
            "code": tk.StringVar(),
            "start_day": tk.IntVar(),
            "start_year": tk.IntVar(),
            "end_day": tk.IntVar(),
            "end_year": tk.IntVar(),
            "ship_mortgage_id": tk.IntVar(),
            "ship_maintenance": IntVar(),
            "mortgage_sanctions": IntVar(),
            "mortgage_payments": IntVar()
        }

        if id is not None:
            self.annual_budget = self.session.get(AnnualBudget, id)
            self.vars["code"].set(self.annual_budget.code)
            self.vars["start_day"].set(self.annual_budget.start_day)
            self.vars["start_year"].set(self.annual_budget.start_year)
            self.vars["end_day"].set(self.annual_budget.end_day)
            self.vars["end_year"].set(self.annual_budget.end_year)
            self.vars["ship_mortgage_id"].set(self.annual_budget.ship_mortgage_id)
            self.vars["ship_maintenance"].set(self.annual_budget.ship_maintenance)
            self.vars["mortgage_sanctions"].set(self.annual_budget.mortgage_sanctions)
            self.vars["mortgage_payments"].set(self.annual_budget.mortgage_payments)

        self.columns = {
            "code": "Code",
            "start_day": "Start day",
            "start_year": "Start year",
            "end_day": "End day",
            "end_year": "End year",
            "ship_mortgage_id": "Ship mortgage",
            "mortgage_sanctions": "Ship mortgage sanctions",
            "mortgage_payments": "Ship mortgage payments",
        }

        self.entries = []
        self.create_widtgets()

    def create_widtgets(self):
        self.img_title_tk = EmojiCache(size=32).get("1f4c9.png") # Chart decreasing
        self.title_label = ttk.Label(self, text="Annual budget", font=("", 30), image=self.img_title_tk, compound="left")
        self.title_label.grid(column=0, row=0, padx=10, pady=10, sticky="we", columnspan=2)

        row = 1
        if self.annual_budget.id is not None:
            ttk.Label(self, text=self.columns["code"]).grid(row=row, column=0, sticky="e", padx=5, pady=5)
            self.code_entry = ttk.Entry(self, textvariable=self.vars["code"], width=40)
            self.code_entry.grid(row=row, column=1, sticky="we", padx=5, pady=5)
            self.code_entry.configure(state="disabled")
            row = row + 1
            self.entries.append(self.code_entry)

        ttk.Label(self, text=self.columns["ship_mortgage_id"]).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self.mortgage_combo = ttk.Combobox(self, state="readonly")
        self.mortgage_combo["values"] = [p.name for p in self.mortgages]
        self.mortgage_combo.grid(row=row, column=1, sticky="we", padx=5, pady=5)
        row = row + 1
        self.entries.append(self.mortgage_combo)
        if self.annual_budget.id is not None:
            for i, mortgage in enumerate(self.mortgages):
                if mortgage.id == self.annual_budget.ship_mortgage_id:
                    self.mortgage_combo.current(i)
                    break

        ttk.Button(self, text="Save", command=lambda: self.save()).grid(row=row, column=1, padx=5, pady=5, sticky="w")


    def save(self):

        if ViewValidator(self.entries).is_valid():
            data = {k: v.get() for k, v in self.vars.items()}

            index = self.mortgage_combo.current()
            data["ship_mortgage_id"] = self.mortgages[index].id if index != -1 else None

            for k, v in data.items():
                setattr(self.annual_budget, k, v)

            if self.annual_budget.id is None:
                self.annual_budget.code = ulid.new().str
                self.session.add(self.annual_budget)

            self.session.commit()
            self.router.get_view("annual_budget").refresh()
            self.parent.destroy()