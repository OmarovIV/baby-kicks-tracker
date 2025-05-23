import tkinter as tk
from tkinter import ttk
from datetime import datetime
import database

class AlertsWindow(tk.Toplevel):
    """Window for anomaly detection alerts."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Alerts")

        style = ttk.Style(self)
        style.theme_use('default')
        style.configure(".", font=("Segoe UI", 10))

        frame = ttk.Frame(self, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame,
                  text="Anomaly Detection",
                  font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, pady=(0,10))

        today = datetime.today().strftime("%Y-%m-%d")
        records = database.get_records_between_dates(today, today)

        if not records:
            msg, color = "⚠️ No records today!\nPlease check baby activity.", "red"
        else:
            msg, color = f"✅ {len(records)} record(s) today.\nAll good.", "green"

        ttk.Label(frame, text=msg, foreground=color).grid(
            row=1, column=0, pady=(0,10)
        )

        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
