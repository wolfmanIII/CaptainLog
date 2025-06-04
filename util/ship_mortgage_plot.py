from decimal import Decimal
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MutuoTravellerPlot:
    def __init__(self, principal, durations, multipliers):
        self.principal = Decimal(principal)
        self.durations = durations
        self.multipliers = [Decimal(str(m)) for m in multipliers]
        self.data = self._prepare_data()

    def _prepare_data(self):
        import pandas as pd
        data = []
        for years, multiplier in zip(self.durations, self.multipliers):
            total_repaid = self.principal * multiplier
            months = years * 12
            monthly_payment = total_repaid / months
            r = (multiplier ** (Decimal(1) / Decimal(years))) - 1  # interesse annuo composto teorico
            annual_rate_percent = r * 100
            data.append({
                "Duration (years)": float(years),
                "Multipliers": float(multiplier),
                "Mortgage Total (Cr)": float(total_repaid),
                "Monthly payment (Cr)": float(monthly_payment),
                "Annual interest rate (%)": round(annual_rate_percent, 2)
            })
        return pd.DataFrame(data)

    def create_figure(self):
        import matplotlib.pyplot as plt
        df = self.data
        fig = Figure(figsize=(8, 5), dpi=100)
        ax1 = fig.add_subplot(111)

        ax1.set_xlabel("Mortgage duration (years)")
        ax1.set_ylabel("Monthly payment (Cr)", color='tab:blue')
        ax1.plot(df["Duration (years)"], df["Monthly payment (Cr)"], color='tab:blue', marker='o')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        ax2.set_ylabel("Annual interest rate (%)", color='tab:red')
        ax2.plot(df["Duration (years)"], df["Annual interest rate (%)"], color='tab:red', marker='s', linestyle='--')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        fig.tight_layout()
        return fig
