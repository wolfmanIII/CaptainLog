import tkinter as tk
from tkinter import ttk

class MaskedNumericEntry(ttk.Frame):
    def __init__(self, master=None, textvariable=None, min_value=None, max_value=None, **kwargs):
        super().__init__(master)
        self.var = textvariable or tk.StringVar()
        self.min_value = min_value
        self.max_value = max_value
        self.required = getattr(self, "required", True)

        if self.var.get().strip():
            try:
                number = float(self.var.get().replace(".", "").replace(",", "."))
                formatted = f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                self.var.set(formatted)
            except ValueError:
                pass  # Inizialmente può non essere un numero valido

        self.entry = ttk.Entry(self, textvariable=self.var, **kwargs)
        self.entry.pack(fill="x")

        vcmd = (self.register(self._on_validate), "%P")
        self.entry.configure(validate="key", validatecommand=vcmd)
        self.entry.bind("<FocusOut>", self._on_focus_out)

    def _on_validate(self, value):
        return all(c.isdigit() or c in {".", ","} for c in value)

    def _on_focus_out(self, event):
        value = self.var.get().strip()

        if not value:
            if self.required:
                self._set_error("Campo obbligatorio")
            else:
                self._clear_error()
            return

        raw = value.replace(".", "").replace(",", ".")
        try:
            number = float(raw)
            if self.min_value is not None and number < self.min_value:
                self._set_error(f"Min: {self.min_value}")
                return
            if self.max_value is not None and number > self.max_value:
                self._set_error(f"Max: {self.max_value}")
                return
            self._clear_error()
            formatted = f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.var.set(formatted)
        except ValueError:
            self._set_error("Valore non valido")

    def _set_error(self, message):
        FloatingTooltipError(self.entry, message)

    def _clear_error(self):
        self.entry.configure(foreground="")

    def get_value(self):
        raw_value = self.var.get().strip()
        if not raw_value:
            return None
        try:
            raw = raw_value.replace(".", "").replace(",", ".")
            return float(raw)
        except ValueError:
            return None
        
    def configure(self, **kwargs):
        self.entry.configure(**kwargs)


class FloatingTooltipError(tk.Toplevel):
    def __init__(self, parent, message, delay=2000):
        super().__init__(parent)
        self.wm_overrideredirect(True)
        self.attributes("-topmost", True)

        label = tk.Label(
            self,
            text=message,
            bg="#ffdddd",
            fg="black",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9)
        )
        label.pack(ipadx=6, ipady=2)

        x = parent.winfo_rootx() + parent.winfo_width() + 10
        y = parent.winfo_rooty()
        self.geometry(f"+{x}+{y}")

        self.after(delay, self.destroy)
