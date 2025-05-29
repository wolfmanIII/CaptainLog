import tkinter as tk
from tkinter import ttk

class MaskedNumericEntry(ttk.Frame):
    def __init__(self, master=None, textvariable=None, min_value=None, max_value=None, **kwargs):
        super().__init__(master)
        self.var = textvariable or tk.StringVar()
        self.min_value = min_value
        self.max_value = max_value

        self.entry = ttk.Entry(self, textvariable=self.var, **kwargs)
        self.entry.pack(fill="x")

        self.error_label = tk.Label(self, text="", fg="red", font=("", 8))
        self.error_label.pack(anchor="w", pady=(2,0))

        # Registrazione validazione solo per key
        vcmd = (self.register(self._on_validate), "%P")
        self.entry.configure(validate="key", validatecommand=vcmd)

        # Bind focus-out per validazione completa
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_validate(self, value):
        # Accetta solo cifre, punto e virgola durante digitazione
        return all(c.isdigit() or c in {".", ","} for c in value)

    def _on_focus_out(self, event):
        value = self.var.get()
        raw = value.replace(".", "").replace(",", ".")
        try:
            number = float(raw)
            if self.min_value is not None and number < self.min_value:
                self._set_error(f"Min: {self.min_value}")
                return
            if self.max_value is not None and number > self.max_value:
                self._set_error(f"Max: {self.max_value}")
                return
            # Formatta e pulisce errore
            self._clear_error()
            formatted = f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.var.set(formatted)
        except ValueError:
            self._set_error("Valore non valido")

    def _set_error(self, message):
        self.error_label.config(text=message)
        self.entry.configure(foreground="red")

    def _clear_error(self):
        self.error_label.config(text="")
        self.entry.configure(foreground="")

    def get_value(self):
        try:
            raw = self.var.get().replace(".", "").replace(",", ".")
            return float(raw)
        except ValueError:
            return None
