import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
from ui.records_window import RecordsWindow
from ui.settings_window import SettingsWindow
from ui.alerts_window import AlertsWindow
import database
from utils import calculate_pregnancy_weeks

class MainWindow(tk.Tk):
    """Main window for adding baby kick records."""
    def __init__(self):
        super().__init__()
        self.title("Baby Kicks Tracker")

        # Apply default theme and font
        style = ttk.Style(self)
        style.theme_use('default')
        default_font = ("Segoe UI", 10)
        style.configure(".", font=default_font)

        # Main container
        container = ttk.Frame(self, padding=20)
        container.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        # Header
        ttk.Label(container, text="Add Baby Kick Record",
                  font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0,10))

        # Display today's date and pregnancy weeks
        today_str = datetime.today().strftime("%Y-%m-%d")
        weeks_text = calculate_pregnancy_weeks(today_str)
        ttk.Label(container, text=f"Today: {today_str} → {weeks_text}"
        ).grid(row=1, column=0, columnspan=2, pady=(0,15))

        # Date entry
        ttk.Label(container, text="Date*:").grid(
            row=2, column=0, sticky="e", padx=(0,5)
        )
        self.date_entry = DateEntry(container, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=2, column=1, sticky="we")

        # Time entry
        ttk.Label(container, text="Time (HH:MM)*:").grid(
            row=3, column=0, sticky="e", padx=(0,5), pady=(5,0)
        )
        self.time_entry = ttk.Entry(container)
        self.time_entry.grid(row=3, column=1, sticky="we", pady=(5,0))

        # Kicks count entry
        ttk.Label(container, text="Kicks Count (optional):").grid(
            row=4, column=0, sticky="e", padx=(0,5), pady=(5,0)
        )
        self.kicks_entry = ttk.Entry(container)
        self.kicks_entry.grid(row=4, column=1, sticky="we", pady=(5,0))

        # Comment box
        ttk.Label(container, text="Comment (optional):").grid(
            row=5, column=0, sticky="ne", padx=(0,5), pady=(5,0)
        )
        self.comment_entry = tk.Text(container, height=4, font=default_font)
        self.comment_entry.grid(row=5, column=1, sticky="we", pady=(5,0))

        # Paste context menu + key bindings
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Paste", command=lambda: self.comment_entry.event_generate("<<Paste>>"))
        self.comment_entry.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))
        self.comment_entry.bind("<Control-v>", lambda e: self.comment_entry.event_generate("<<Paste>>"))
        self.comment_entry.bind("<Command-v>", lambda e: self.comment_entry.event_generate("<<Paste>>"))

        # Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        for idx, (text, cmd) in enumerate([
            ("➕ Add Record", self.add_record),
            ("📄 View Records", self.open_records),
            ("⚙️ Settings", self.open_settings),
            ("🔔 Check Alerts", self.open_alerts),
        ]):
            ttk.Button(btn_frame, text=text, command=cmd).grid(row=0, column=idx, padx=5)

        # Ensure window is not cropped
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

    def add_record(self):
        """Validate and insert a new record."""
        date = self.date_entry.get()
        time = self.time_entry.get()
        kicks = self.kicks_entry.get()
        comment = self.comment_entry.get("1.0", tk.END).strip()

        if not date or not time:
            messagebox.showwarning("Missing data", "Please fill in Date and Time.")
            return

        if database.record_exists(date, time):
            messagebox.showwarning("Duplicate", "A record for this Date and Time already exists.")
            return

        weeks = calculate_pregnancy_weeks(date)
        added_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        database.insert_record(date, time, kicks, comment, weeks, added_at)
        messagebox.showinfo("Success", "Record added!")

        # Reset form
        self.date_entry.set_date(datetime.today())
        self.time_entry.delete(0, tk.END)
        self.kicks_entry.delete(0, tk.END)
        self.comment_entry.delete("1.0", tk.END)

    def open_records(self):
        RecordsWindow(self)

    def open_settings(self):
        SettingsWindow(self)

    def open_alerts(self):
        AlertsWindow(self)
