import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from datetime import datetime
import numpy as np
import database

class RecordsWindow(tk.Toplevel):
    """Window to view, filter, delete and chart all records."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("All Baby Kick Records")

        # Style & layout
        style = ttk.Style(self)
        style.theme_use('default')
        default_font = ("Segoe UI", 10)
        style.configure(".", font=default_font)

        # Filter frame
        filt = ttk.Frame(self, padding=5)
        filt.pack(fill="x")
        ttk.Label(filt, text="From:").grid(row=0, column=0)
        self.from_date = DateEntry(filt, date_pattern='yyyy-mm-dd')
        self.from_date.grid(row=0, column=1, padx=5)
        ttk.Label(filt, text="To:").grid(row=0, column=2)
        self.to_date = DateEntry(filt, date_pattern='yyyy-mm-dd')
        self.to_date.grid(row=0, column=3, padx=5)
        ttk.Button(filt, text="Filter", command=self.filter_records).grid(row=0, column=4, padx=5)
        ttk.Button(filt, text="Show Chart", command=self.show_chart).grid(row=0, column=5, padx=5)
        ttk.Button(filt, text="Show Heatmap", command=self.show_heatmap).grid(row=0, column=6, padx=5)

        # Treeview
        cols = [("ID",50),("Date",100),("Time",80),
                ("Kicks",80),("Comment",300),
                ("Weeks",100),("Added At",130)]
        self.tree = ttk.Treeview(self, columns=[c[0] for c in cols], show="headings")
        for c,w in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w)
        self.tree.pack(expand=True, fill="both", padx=5, pady=5)

        # Delete button
        btn = ttk.Button(
            self, text="🗑️ Delete Selected Record", command=self.delete_selected
        )
        btn.pack(anchor="e", padx=5, pady=(0,5))

        self.load_records(database.get_all_records())
        self.update(); self.minsize(self.winfo_width(), self.winfo_height())

    def load_records(self, records):
        self.tree.delete(*self.tree.get_children())
        for rec in records:
            self.tree.insert("", tk.END, values=rec)

    def filter_records(self):
        start = self.from_date.get_date().strftime("%Y-%m-%d")
        end = self.to_date.get_date().strftime("%Y-%m-%d")
        recs = database.get_records_between_dates(start, end)
        self.load_records(recs)

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a record.")
            return
        rid = self.tree.item(sel)["values"][0]
        database.delete_record(rid)
        self.load_records(database.get_all_records())
        messagebox.showinfo("Deleted", "Record deleted successfully.")

    def show_chart(self):
        records = database.get_all_records()
        dates = [r[1] for r in records]
        counts = Counter(dates)
        dates_sorted = sorted(counts)
        values = [counts[d] for d in dates_sorted]
        plt.figure(figsize=(8,4))
        plt.bar(dates_sorted, values, color="skyblue")
        plt.xlabel("Date"); plt.ylabel("Number of Records")
        plt.title("Baby Kicks per Day")
        plt.xticks(rotation=45); plt.tight_layout()
        plt.show()

    def show_heatmap(self):
        records = database.get_all_records()
        data = defaultdict(lambda: [0]*24)
        for r in records:
            d, t, k = r[1], r[2], r[3]
            try:
                hr = int(t.split(":")[0])
                cnt = int(k) if k and k.isdigit() else 1
                data[d][hr] += cnt
            except:
                continue
        if not data:
            messagebox.showinfo("No Data", "No records found to display heatmap.")
            return
        dates_sorted = sorted(data)
        mat = np.array([data[d] for d in dates_sorted])
        plt.figure(figsize=(10,6), num="Baby Kicks Heatmap")
        plt.imshow(mat.T, aspect="auto", cmap="YlOrRd", origin="upper")
        plt.colorbar(label="Number of Kicks")
        plt.yticks(range(24), [f"{h:02d}:00" for h in range(24)])
        plt.xticks(range(len(dates_sorted)), dates_sorted, rotation=45)
        plt.xlabel("Date"); plt.ylabel("Hour of Day")
        plt.title("Baby Kicks Heatmap"); plt.tight_layout(); plt.show()
