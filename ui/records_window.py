import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import database

class RecordsWindow(tk.Toplevel):
    """Window to view, filter, chart and delete kick records."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("All Baby Kick Records")
        self.geometry("850x500")
        self.resizable(True, True)

        # Top filter frame
        filter_frame = ttk.Frame(self, padding=10)
        filter_frame.pack(fill="x")

        ttk.Label(filter_frame, text="From:").grid(row=0, column=0, padx=(0, 5))
        self.from_date = DateEntry(filter_frame, date_pattern='yyyy-mm-dd')
        self.from_date.grid(row=0, column=1, padx=(0, 15))

        ttk.Label(filter_frame, text="To:").grid(row=0, column=2, padx=(0, 5))
        self.to_date = DateEntry(filter_frame, date_pattern='yyyy-mm-dd')
        self.to_date.grid(row=0, column=3, padx=(0, 15))

        filter_btn = ttk.Button(filter_frame, text="Filter", command=self.load_records)
        filter_btn.grid(row=0, column=4, padx=(0, 5))
        chart_btn = ttk.Button(filter_frame, text="Show Chart", command=self.show_chart)
        chart_btn.grid(row=0, column=5, padx=(0, 5))
        heatmap_btn = ttk.Button(filter_frame, text="Show Heatmap", command=self.show_heatmap)
        heatmap_btn.grid(row=0, column=6)

        # Table frame
        table_frame = ttk.Frame(self, padding=(10,0,10,10))
        table_frame.pack(fill="both", expand=True)

        columns = ("ID", "Date", "Time", "Kicks", "Comment", "Weeks", "Added At")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings"
        )
        for col in columns:
            self.tree.heading(col, text=col)
        widths = [40, 100, 80, 60, 300, 100, 140]
        for col, w in zip(columns, widths):
            self.tree.column(col, width=w, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Bottom delete button
        del_frame = ttk.Frame(self, padding=10)
        del_frame.pack(fill="x")
        del_frame.columnconfigure(0, weight=1)
        del_btn = ttk.Button(
            del_frame, text="🗑️ Delete Selected Record", command=self.delete_selected
        )
        del_btn.grid(row=0, column=0, sticky="e")

        # Initial load
        today = datetime.today().strftime("%Y-%m-%d")
        self.from_date.set_date(today)
        self.to_date.set_date(today)
        self.load_records()

    def load_records(self):
        """Load records from DB into the treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        start = self.from_date.get()
        end = self.to_date.get()
        rows = database.get_records_between_dates(start, end)
        for rec in rows:
            self.tree.insert("", "end", values=rec)

    def delete_selected(self):
        """Delete highlighted record and refresh."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a record to delete.")
            return
        rid = self.tree.item(sel[0])["values"][0]
        database.delete_record(rid)
        self.load_records()

    def show_chart(self):
        """Bar chart: total kicks per day."""
        rows = database.get_records_between_dates(
            self.from_date.get(), self.to_date.get()
        )
        if not rows:
            messagebox.showinfo("No Data", "No records in that range.")
            return

        # aggregate daily total kicks
        daily = defaultdict(int)
        for _, date, _, kicks, *_ in rows:
            count = int(kicks) if kicks.isdigit() else 1
            daily[date] += count

        dates = sorted(daily)
        counts = [daily[d] for d in dates]

        plt.figure(figsize=(10, 5))
        plt.bar(dates, counts)
        plt.xlabel("Date")
        plt.ylabel("Number of Kicks")
        plt.title("Baby Kicks per Day")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_heatmap(self):
        """Heatmap: kicks by hour-of-day vs date."""
        rows = database.get_records_between_dates(
            self.from_date.get(), self.to_date.get()
        )
        if not rows:
            messagebox.showinfo("No Data", "No records in that range.")
            return

        # prepare data matrix
        data = defaultdict(lambda: [0]*24)
        for _, date, time_str, kicks, *_ in rows:
            hour = int(time_str.split(":")[0])
            count = int(kicks) if kicks.isdigit() else 1
            data[date][hour] += count

        dates = sorted(data)
        mat = np.array([data[d] for d in dates]).T  # shape (24, n_dates)

        plt.figure(figsize=(10, 5))
        plt.imshow(mat, aspect='auto', origin='lower', cmap='YlOrRd')
        plt.colorbar(label="Number of Kicks")
        plt.yticks(range(0,24), [f"{h:02d}:00" for h in range(24)])
        plt.xticks(range(len(dates)), dates, rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Hour of Day")
        plt.title("Baby Kicks Heatmap")
        plt.tight_layout()
        plt.show()
