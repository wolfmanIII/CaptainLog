from numpy import void
from sqlalchemy import column, select
from tkinter import Tk, ttk

from controller.router import Router
from view.home_view import HomeView
from view.menubar import Menubar
from view.ship_list_view import ShipListView
from view.ship_role_list_view import ShipRoleListView
from view.ship_view import ShipView

class Application(ttk.Frame):
    
    def __init__(self, master: Tk):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        #Menubar(master)
        
        self.router = Router(self)
        self.register_views()
        self.router.navigate("home")

    def register_views(self):
        self.router.add_view("home", HomeView)
        self.router.add_view("ship", ShipView)
        self.router.add_view("ships", ShipListView)
        self.router.add_view("roles", ShipRoleListView)