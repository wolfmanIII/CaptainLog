from tkinter import ttk
import tkinter.font as tkFont

from service.ship_role_service import ShipRoleService


class ShipRoleListView(ttk.Frame):

    def __init__(self, master, router):
        super().__init__(master)
        columns = ["code", "name", "description"]
        self.ship_roles = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            self.ship_roles.heading(column, text=column.capitalize())
        
        self.show_data(ShipRoleService().get_all_ship_roles())
        self.ship_roles.grid(column=0, row=0, columnspan=1, rowspan=20, padx=5, pady=5)

        #self.set_columns_dimension()


    def show_data(self, data):
        for role in data:
            values = (role.code, role.name, role.description)
            self.ship_roles.insert('', 'end', text='Listbox', values=values)

    def set_columns_dimension(self):
        font = tkFont.Font()
        for col in self.ship_roles['columns']:
            # Considera la larghezza dell'intestazione
            max_width = font.measure(col)
            
            # Scorri tutte le righe per la colonna
            for item in self.ship_roles.get_children():
                cell_text = self.ship_roles.set(item, col)
                cell_width = font.measure(cell_text)
                if cell_width > max_width:
                    max_width = cell_width
            
            # Aggiungi un po' di margine
            max_width += 10
            self.ship_roles.column(col, width=max_width)