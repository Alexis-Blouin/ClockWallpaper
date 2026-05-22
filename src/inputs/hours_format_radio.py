import tkinter as tk
from tkinter import ttk

class HoursFormatRadio(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)

        self.val = tk.StringVar(self, "12")

        values = {"12h" : "12", "24h" : "24"}
        for i, (text, value) in enumerate(values.items()):
            ttk.Radiobutton(self, text=text, variable=self.val, value=value).grid(row=0, column=i)

    def get_current(self):
        return self.val.get()

    def set_current(self, val):
        self.val.set(val)