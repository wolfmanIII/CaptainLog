import locale
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from model import crew, ship
from model.crew import Crew
from service.dblink import DBLink
from service.crew_service import CrewService
from view.crew_view import CrewView
#from view.ship_view import ShipView

locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class CrewListView(ttk.Frame):

    def __init__(self, master, router):
        super().__init__(master)
        self.router = router
        self.session = DBLink().getSession()

        tk.Label(self, text="Crew", font=("", 18)).grid(column=0, row=0, padx=10, pady=10, sticky="w")

        buttonGroup = ButtonGroup(self, router)
        buttonGroup.grid(column=0, row=1, padx=5, pady=5, sticky="w")

        vsb = ttk.Scrollbar(self, orient="vertical")
        vsb.grid(row=2, column=1, sticky="ns")

        columns = ["code", "name", "surname", "nickname", "ship", "roles"]
        self.crew_tree = ttk.Treeview(self, columns=columns, show="headings", yscrollcommand=vsb.set, height=10)
        vsb.config(command=self.crew_tree.yview)
        for column in columns:
            text_show= ""
            text_show = column.capitalize()
            self.crew_tree.heading(column, text=text_show)

        self.refresh()
        self.crew_tree.grid(column=0, row=2, padx=5, pady=5)

        # Bind evento doppio click
        self.crew_tree.bind("<Double-1>", self.on_double_click_row)

    def populate_data(self):
        for crew in CrewService().get_all_crew():
            ship_name = crew.ship.name if crew.ship else ""
            ship_roles = ""
            i = 0
            for role in crew.roles:
                i = i + 1
                if i < len(crew.roles):
                    ship_roles = ship_roles + role.name + " | "
                else:
                    ship_roles = ship_roles + role.name
                    
                    
            values = (crew.code, crew.name, crew.surname, crew.nickname, ship_name, ship_roles)
            self.crew_tree.insert('', 'end', iid=crew.id, text='Listbox', values=values)

    def refresh(self):
        for item in self.crew_tree.get_children():
            self.crew_tree.delete(item)

        self.populate_data()

    def delete_selected_crew(self):
        selected_items = self.crew_tree.selection()
        for iid in selected_items:
            # 1. Cancella dal database
            crew = self.session.get(Crew, iid)
            if crew:
                self.session.delete(crew)
        
        self.session.commit()  # 2. Commit
        self.refresh()

    def on_double_click_row(self, event):
        item_id = self.crew_tree.identify_row(event.y)
        if item_id:
            self.viewCrew(item_id)

    def viewCrew(self, id=None):
        self.dialog = tk.Toplevel(self)
        self.dialog.title("Crew")
        crew_view = CrewView(self.dialog, self.router, id)
        crew_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.dialog.wait_visibility()
        self.dialog.grab_set() 

    def set_columns_dimension(self):
        font = tkFont.Font()
        for col in self.crew_tree['columns']:
            # Considera la larghezza dell'intestazione
            max_width = font.measure(col)
            
            # Scorri tutte le righe per la colonna
            for item in self.crew_tree.get_children():
                cell_text = self.crew_tree.set(item, col)
                cell_width = font.measure(cell_text)
                if cell_width > max_width:
                    max_width = cell_width
            
            # Aggiungi un po' di margine
            max_width += 10
            self.ships.column(col, width=max_width)

class ButtonGroup(ttk.Frame):

    def __init__(self, parent, router):
        super().__init__(parent, borderwidth=1, relief="solid")

        self.home_button = ttk.Button(self, text="Back", command=lambda: router.navigate("home"))
        self.home_button.grid(column=0, row=0, padx=10, pady=10, sticky="w")

        self.refresh_button = ttk.Button(self, text="Refresh", command=parent.refresh)
        self.refresh_button.grid(column=1, row=0, padx=10, pady=10, sticky="w")

        self.new_ship_button = ttk.Button(self, text="New", command=parent.viewCrew)
        self.new_ship_button.grid(column=2, row=0, padx=10, pady=10, sticky="w")

        self.new_ship_button = ttk.Button(self, text="Delete", command=parent.delete_selected_crew)
        self.new_ship_button.grid(column=3, row=0, padx=10, pady=10, sticky="w")