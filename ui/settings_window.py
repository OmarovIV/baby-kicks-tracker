import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from settings import get_pregnancy_start_date, set_pregnancy_start_date

class SettingsWindow(tk.Toplevel):
    """Window for application settings."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")

        style = ttk.Style(self)
        style.theme_use('default')
        style.configure(".", font=("Segoe UI", 10))

        frame = ttk.Frame(self, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Pregnancy Start Date:").grid(
            row=0, column=0, sticky="e", padx=(0,5)
        )
        self.date_entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
        self.date_entry.set_date(get_pregnancy_start_date())
        self.date_entry.grid(row=0, column=1, sticky="we")

        ttk.Button(frame, text="Save", command=self.save).grid(
            row=1, column=0, columnspan=2, pady=10
        )

        self.update(); self.minsize(self.winfo_width(), self.winfo_height())

    def save(self):
        set_pregnancy_start_date(self.date_entry.get())
        ttk.Label(self, text="Saved!", foreground="green").grid(
            row=2, column=0, columnspan=2, pady=(0,10)
        )
