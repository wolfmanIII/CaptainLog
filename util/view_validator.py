from typing import List
from tkinter import ttk
from util.masked_numeric_entry import FloatingTooltipError


class ViewValidator():

    def __init__(self, entries: list[ttk.Entry]):
        self.entries = entries
    
    def is_valid(self):
        result = 0
        for entry in self.entries:
            type(entry).__name__
            if type(entry).__name__ == "MaskedNumericEntry":
                if not self.validateNumber(entry):
                    FloatingTooltipError(entry, "Valore non valido")
                    result = result + 1
            else:
                if not entry.get().strip():
                    FloatingTooltipError(entry, "Campo obbligatorio")
                    result = result + 1
        return (result == 0)

    def validateNumber(self, entry):
        number = entry.get_value()
        try:
            float(number)
            if entry.min_value is not None and number < entry.min_value:
                return False
            if entry.max_value is not None and number > entry.max_value:
                return False
        except Exception:
            FloatingTooltipError(entry, "Valore non valido")
            return False
        return True