import tkinter as tk
from tkinter import ttk

from service.annual_budget_service import AnnualBudgetService
from service.dblink import DBLink
from util.emoji_cache import EmojiCache
from view.annual_budget_view import AnnualBudgetView

class AnnualBudgetListView(ttk.Frame):

    def __init__(self, master, router):
        super().__init__(master)
        self.router = router
        self.session = DBLink().getSession()
        self.create_widgets()

    def create_widgets(self):
        self.img_title_tk = EmojiCache(size=32).get("1f4c9.png") # Chart decreasing
        self.title_label = ttk.Label(self, text="Annual Budgets", font=("", 30), image=self.img_title_tk, compound="left")
        self.title_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        buttonGroup = ButtonGroup(self, self.router)
        buttonGroup.grid(column=0, row=1, padx=5, pady=5, sticky="nsew")

        vsb = ttk.Scrollbar(self, orient="vertical")
        vsb.grid(row=2, column=1, sticky="ns")

        columns = ["code", "mortgage", "period", "maintenances", "sanctions", "payments"]
        self.annual_budget_tree = ttk.Treeview(self, columns=columns, show="headings", yscrollcommand=vsb.set, height=10)
        vsb.config(command=self.annual_budget_tree.yview)
        for column in columns:
            text_show= ""
            text_show = column.capitalize()
            self.annual_budget_tree.heading(column, text=text_show)

        self.refresh()
        self.annual_budget_tree.grid(column=0, row=2, padx=5, pady=5)

    def populate_data(self):
        for budget in AnnualBudgetService().get_all_budgets():
            period = budget.start_day + "/" + budget.start_year + " - " + budget.end_day + "/" + budget.end_year
                       
            values = (budget.code, budget.ship_mortgage.name, period, budget.ship_maintenance, budget.mortgage_sanctions, budget.mortgage_payments)
            self.annual_budget_tree.insert('', 'end', iid=budget.id, text='Listbox', values=values)

    def refresh(self):
        for item in self.annual_budget_tree.get_children():
            self.annual_budget_tree.delete(item)

        self.populate_data()

    def viewAnnualBudget(self, id=None):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Annual budget")
        annual_budget_view = AnnualBudgetView(self.dialog, self.router, id)
        annual_budget_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.dialog.wait_visibility()
        self.dialog.grab_set()


class ButtonGroup(ttk.Frame):

    def __init__(self, parent, router):
        super().__init__(parent, borderwidth=1, relief="solid")

        self.img_back_tk = EmojiCache(size=16).get("2b05.png") # Back
        self.home_button = ttk.Button(self, text="Back", command=lambda: router.navigate("home"), image=self.img_back_tk, compound="left")
        self.home_button.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        self.img_refresh_tk = EmojiCache(size=16).get("1f503.png") # Reload
        self.refresh_button = ttk.Button(self, text="Refresh", command=parent.refresh, image=self.img_refresh_tk, compound="left")
        self.refresh_button.grid(column=1, row=0, padx=10, pady=10, sticky="w")

        self.img_new_tk = EmojiCache(size=16).get("1f195.png") # New
        self.new_ship_button = ttk.Button(self, text="New", command=parent.viewAnnualBudget, image=self.img_new_tk, compound="left")
        self.new_ship_button.grid(column=2, row=0, padx=10, pady=10, sticky="w")