import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import database
from utils import calculate_pregnancy_weeks

class RecordsWindow(tk.Toplevel):
    """Window to view, filter, chart, edit and delete kick records."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("All Baby Kick Records")
        self.geometry("900x520")
        self.resizable(True, True)

        # Top filter frame
        filter_frame = ttk.Frame(self, padding=10)
        filter_frame.pack(fill="x")

        ttk.Label(filter_frame, text="From:").grid(row=0, column=0, padx=(0,5))
        self.from_date = DateEntry(filter_frame, date_pattern='yyyy-mm-dd')
        self.from_date.grid(row=0, column=1, padx=(0,15))

        ttk.Label(filter_frame, text="To:").grid(row=0, column=2, padx=(0,5))
        self.to_date = DateEntry(filter_frame, date_pattern='yyyy-mm-dd')
        self.to_date.grid(row=0, column=3, padx=(0,15))

        ttk.Button(filter_frame, text="Filter",        command=self.load_records).grid(row=0, column=4, padx=(0,5))
        ttk.Button(filter_frame, text="Show Chart",    command=self.show_chart).grid(row=0, column=5, padx=(0,5))
        ttk.Button(filter_frame, text="Show Heatmap",  command=self.show_heatmap).grid(row=0, column=6)

        # Table
        table_frame = ttk.Frame(self, padding=(10,0,10,10))
        table_frame.pack(fill="both", expand=True)

        cols = ("ID","Date","Time","Kicks","Comment","Weeks","Added At")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
        widths = [40,100,80,60,300,100,140]
        for c,w in zip(cols, widths):
            self.tree.column(c, width=w, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Bottom action buttons: Edit & Delete
        action_frame = ttk.Frame(self, padding=10)
        action_frame.pack(fill="x")
        action_frame.columnconfigure((0,1), weight=1)

        ttk.Button(action_frame,
                   text="✏️ Edit Selected Record",
                   command=self.edit_selected
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(action_frame,
                   text="🗑️ Delete Selected Record",
                   command=self.delete_selected
        ).grid(row=0, column=1, sticky="e")

        # Initial load: all records
        self._populate_tree(database.get_all_records())

    def _populate_tree(self, rows):
        """Clear existing rows and insert new ones."""
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        for rec in rows:
            self.tree.insert("", "end", values=rec)

    def load_records(self):
        """Load records into the table based on date filters."""
        start = self.from_date.get()
        end   = self.to_date.get()
        if start and end:
            rows = database.get_records_between_dates(start, end)
        else:
            rows = database.get_all_records()
        self._populate_tree(rows)

    def delete_selected(self):
        """Delete highlighted record and refresh."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a record to delete.")
            return
        rid = self.tree.item(sel[0])["values"][0]
        database.delete_record(rid)
        self.load_records()

    def edit_selected(self):
        """Open an edit dialog for the selected record."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a record to edit.")
            return
        vals = self.tree.item(sel[0])["values"]
        EditRecordWindow(self, vals, on_save=self.load_records)

    def show_chart(self):
        """Bar chart: total kicks per day."""
        items = self.tree.get_children()
        if not items:
            messagebox.showinfo("No Data", "No records to display.")
            return

        daily = defaultdict(int)
        for iid in items:
            _, date, _, kicks, *_ = self.tree.item(iid)["values"]
            cnt = int(kicks) if str(kicks).isdigit() else 1
            daily[date] += cnt

        dates  = sorted(daily)
        counts = [daily[d] for d in dates]

        plt.figure(figsize=(10,5))
        plt.bar(dates, counts)
        plt.xlabel("Date")
        plt.ylabel("Number of Kicks")
        plt.title("Baby Kicks per Day")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def show_heatmap(self):
        """Heatmap: kicks by hour-of-day vs date, using current table contents."""
        items = self.tree.get_children()
        if not items:
            messagebox.showinfo("No Data", "No records to display.")
            return

        # aggregate kicks per date/hour
        data = defaultdict(lambda: [0]*24)
        for iid in items:
            _, date, time_str, kicks, *_ = self.tree.item(iid)["values"]
            hour = int(time_str.split(":")[0])
            cnt  = int(kicks) if str(kicks).isdigit() else 1
            data[date][hour] += cnt

        dates = sorted(data)
        mat   = np.array([data[d] for d in dates]).T  # shape (24, n_dates)

        # color scale from zero up to the max value
        vmin, vmax = 0, int(mat.max()) if mat.size else 1

        plt.figure(figsize=(10,5))
        im = plt.imshow(mat, aspect='auto', origin='upper',
                        cmap='YlOrRd', vmin=vmin, vmax=vmax)
        plt.colorbar(im, label="Number of Kicks")
        plt.yticks(range(24), [f"{h:02d}:00" for h in range(24)])
        plt.xticks(range(len(dates)), dates, rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Hour of Day")
        plt.title("Baby Kicks Heatmap")
        plt.tight_layout()
        plt.show()

class EditRecordWindow(tk.Toplevel):
    """Modal window to edit an existing record."""
    def __init__(self, parent, record_values, on_save):
        super().__init__(parent)
        self.title("Edit Record")
        self.resizable(False, False)
        self.on_save = on_save
        self.record_id = record_values[0]

        # Unpack existing values
        _, date, time, kicks, comment, _, _ = record_values

        frm = ttk.Frame(self, padding=20)
        frm.grid()

        # Date
        ttk.Label(frm, text="Date*:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.dt = DateEntry(frm, date_pattern='yyyy-mm-dd')
        self.dt.set_date(date)
        self.dt.grid(row=0, column=1, pady=5)

        # Time
        ttk.Label(frm, text="Time (HH:MM)*:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.tm = ttk.Entry(frm)
        self.tm.insert(0, time)
        self.tm.grid(row=1, column=1, pady=5)

        # Kicks
        ttk.Label(frm, text="Kicks Count:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.kc = ttk.Entry(frm)
        self.kc.insert(0, kicks)
        self.kc.grid(row=2, column=1, pady=5)

        # Comment
        ttk.Label(frm, text="Comment:").grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        self.cm = tk.Text(frm, width=30, height=4, wrap="word")
        self.cm.insert("1.0", comment)
        self.cm.grid(row=3, column=1, pady=5)

        # Save / Cancel buttons
        btns = ttk.Frame(frm)
        btns.grid(row=4, column=0, columnspan=2, pady=(10,0))
        ttk.Button(btns, text="Save",   command=self.save).grid(row=0, column=0, padx=5)
        ttk.Button(btns, text="Cancel", command=self.destroy).grid(row=0, column=1, padx=5)

    def save(self):
        """Validate and commit edits."""
        new_date = self.dt.get()
        new_time = self.tm.get().strip()
        new_kicks = self.kc.get().strip()
        new_comment = self.cm.get("1.0", tk.END).strip()

        if not new_date or not new_time:
            messagebox.showwarning("Missing data", "Date and Time are required.")
            return

        # Compute updated pregnancy weeks
        new_weeks = calculate_pregnancy_weeks(new_date)

        # Commit to DB
        database.update_record(
            self.record_id,
            new_date, new_time,
            new_kicks, new_comment,
            new_weeks
        )

        messagebox.showinfo("Success", "Record updated.")
        self.on_save()
        self.destroy()
