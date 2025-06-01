from tkinter import ttk
from util.masked_numeric_entry import FloatingTooltipError, MaskedNumericEntry


class ViewValidator:

    def __init__(self, entries: list[ttk.Entry]):
        self.entries = entries

    def is_valid(self):
        result = 0

        for entry in self.entries:
            required = getattr(entry, "required", True)  # Default = obbligatorio

            if isinstance(entry, MaskedNumericEntry):
                if not self._validate_masked_numeric_entry(entry, required):
                    result += 1
            else:
                value = entry.get().strip()
                if not value and required:
                    FloatingTooltipError(entry, "Campo obbligatorio")
                    result += 1

        return result == 0

    def _validate_masked_numeric_entry(self, entry: MaskedNumericEntry, required: bool):
        value = entry.get_value()

        if value is None:
            if required:
                FloatingTooltipError(entry.entry, "Campo obbligatorio")
                return False
            return True

        if entry.min_value is not None and value < entry.min_value:
            FloatingTooltipError(entry.entry, f"Min: {entry.min_value}")
            return False
        if entry.max_value is not None and value > entry.max_value:
            FloatingTooltipError(entry.entry, f"Max: {entry.max_value}")
            return False

        return True
