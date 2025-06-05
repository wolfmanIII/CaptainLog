from numpy import void
from sqlalchemy import column, select
from tkinter import Tk, ttk

from controller.router import Router
from model.annual_budget import AnnualBudget
from util.emoji_cache import EmojiCache
from view.annual_budget_list_view import AnnualBudgetListView
from view.contract_list_view import ContractListView
from view.crew_list_view import CrewListView
from view.home_view import HomeView
from view.menubar import Menubar
from view.ship_list_view import ShipListView
from view.ship_mortgage_view import ShipMortgageView
from view.ship_role_list_view import ShipRoleListView


class Application(ttk.Frame):
    
    def __init__(self, master: Tk):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.img_footer_tk = EmojiCache(size=16).get("1f43a.png") # Back

        footer_frame = ttk.Frame(master)
        footer_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        footer = ttk.Label(footer_frame, text="Developed by Space Wolf", image=self.img_footer_tk, compound="right")
        footer.pack(side="right", fill="x", padx=10, pady=10)
        
        #Menubar(master)
        
        self.router = Router(self)
        self.register_views()
        self.router.navigate("home")

    def register_views(self):
        self.router.add_view("home", HomeView)
        self.router.add_view("ships", ShipListView)
        self.router.add_view("crew", CrewListView)
        self.router.add_view("roles", ShipRoleListView)
        self.router.add_view("ship_mortgage", ShipMortgageView)
        self.router.add_view("annual_budgets", AnnualBudgetListView)
        self.router.add_view("contracts", ContractListView)