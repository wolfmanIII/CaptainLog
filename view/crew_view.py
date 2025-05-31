from re import split
from numpy import size
from sqlalchemy import null
import ulid
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

from model.crew import Crew
from model.ship import Ship
from model.ship_role import ShipRole
from service.dblink import DBLink
from util.view_validator import ViewValidator

class CrewView(ttk.Frame):
    def __init__(self, master, router, id=None):
        super().__init__(master)
        self.parent = master
        self.router = router
        self.session = DBLink().getSession()
        self.ships = self.session.query(Ship).order_by(Ship.name).all()
        self.roles = self.session.query(ShipRole).order_by(ShipRole.name).all()
        self.crew = Crew()

        ttk.Label(self, text="Crew member", font=("", 18)).grid(column=0, row=0, padx=10, pady=10, columnspan=2)
                
        self.vars = {
            "code": tk.StringVar(),
            "name": tk.StringVar(),
            "surname": tk.StringVar(),
            "nickname": tk.StringVar(),
            "ship_id": tk.IntVar(),
        }

        if id is not None:
            self.crew = self.session.get(Crew, id)
            self.vars["code"].set(self.crew.code)
            self.vars["name"].set(self.crew.name)
            self.vars["surname"].set(self.crew.surname)
            self.vars["nickname"].set(self.crew.nickname)
            self.vars["ship_id"].set(self.crew.ship_id or 0)


        self.columns = {
            "code": "Code",
            "name": "Name",
            "surname": "Surname",
            "nickname": "Nickname",
            "ship_id": "Ship",
            "roles": "Roles"
        }

        self.entries = []

        row = 1;
        if self.crew.id is not None:
            ttk.Label(self, text=self.columns["code"]).grid(row=row, column=0, sticky="e", padx=5, pady=5)
            self.code_entry = ttk.Entry(self, textvariable=self.vars["code"], width=40)
            self.code_entry.grid(row=row, column=1, sticky="we", padx=5, pady=5)
            self.code_entry.configure(state="readonly")
            row = row + 1
            self.entries.append(self.code_entry)
        
        ttk.Label(self, text=self.columns["name"]).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = ttk.Entry(self, textvariable=self.vars["name"], width=40)
        self.name_entry.grid(row=row, column=1, sticky="we", padx=5, pady=5)
        row = row + 1
        self.entries.append(self.name_entry)

        ttk.Label(self, text=self.columns["surname"]).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self.surname_entry = ttk.Entry(self, textvariable=self.vars["surname"], width=40)
        self.surname_entry.grid(row=row, column=1, sticky="we", padx=5, pady=5)
        row = row + 1
        self.entries.append(self.surname_entry)

        ttk.Label(self, text=self.columns["nickname"]).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self.nickname_entry = ttk.Entry(self, textvariable=self.vars["nickname"], width=40)
        self.nickname_entry.grid(row=row, column=1, sticky="we", padx=5, pady=5)
        row = row + 1
        self.entries.append(self.nickname_entry)

        ttk.Label(self, text=self.columns["ship_id"]).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self.ship_combo = ttk.Combobox(self, state="readonly")
        self.ship_combo["values"] = [p.name for p in self.ships]
        self.ship_combo.grid(row=row, column=1, sticky="we", padx=5, pady=5)
        row = row + 1
        self.entries.append(self.ship_combo)
        if self.crew.id is not None:
            for i, ship in enumerate(self.ships):
                if ship.id == self.crew.ship_id:
                    self.ship_combo.current(i)
                    break

        ttk.Label(self, text=self.columns["roles"]).grid(row=row, column=0, sticky="e", padx=5, pady=5)
        self.role_listbox = tk.Listbox(self, selectmode='multiple', exportselection=0, height=8)
        self.role_listbox.grid(row=row, column=1, padx=5, pady=5, sticky="we")
        row = row + 1
        for role in self.roles:
            self.role_listbox.insert(tk.END, role.name)
        self.load_roles(self.crew)

        ttk.Button(self, text="Save", command=lambda: self.save(id)).grid(row=row, column=1, padx=5, pady=5, sticky="w")

    def load_roles(self, crew):
        # Ottenere i nomi dei ruoli associati al membro dell'equipaggio
        crew_roles = [role.name for role in crew.roles]  # Assumendo che crew.roles sia una lista di oggetti ShipRole

        # Selezionare i ruoli nel Listbox
        for i in range(self.role_listbox.size()):
            if self.role_listbox.get(i) in crew_roles:
                self.role_listbox.selection_set(i)

    def get_selected_roles(self):
        selected_indices = self.role_listbox.curselection()
        selected_roles = [self.role_listbox.get(i) for i in selected_indices]
        return selected_roles

    def save_roles(self, crew):
        selected_role_names = self.get_selected_roles()
        # Recuperare gli oggetti ShipRole corrispondenti ai nomi selezionati
        selected_roles = self.session.query(ShipRole).filter(ShipRole.name.in_(selected_role_names)).all()
        crew.roles = selected_roles

    def save(self, id=None):

        if ViewValidator(self.entries).is_valid():
            data = {k: v.get() for k, v in self.vars.items()}

            index = self.ship_combo.current()
            data["ship_id"] = self.ships[index].id if index != -1 else None

            if id is None:
                crew = Crew(**data)
                crew.code = ulid.new().str
            else:
                crew = self.session.get(Crew, id)
                for k, v in data.items():
                    setattr(crew, k, v)

            if id is None:
                self.session.add(crew)

            self.save_roles(crew)

            self.session.commit()
            self.router.get_view("crew").refresh()
            self.parent.destroy()