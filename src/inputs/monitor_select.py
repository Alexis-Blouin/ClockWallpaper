import tkinter as tk
from tkinter import ttk

from utils import check_path

class MonitorSelect(tk.Frame):
    def __init__(self, parent, monitor_values):
        self.parent = parent
        super().__init__(self.parent)

        self.label = tk.Label(self, text="Choose Monitor", anchor="w")
        self.entry = ttk.Combobox(self, values=monitor_values)
        self.entry.current(0)

        row_num = 0
        self.label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        self.entry.grid(row=row_num, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def get_current(self):
        return self.entry.current()

    def set_current(self, monitor):
        self.entry.current(monitor)