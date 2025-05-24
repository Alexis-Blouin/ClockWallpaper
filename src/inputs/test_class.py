import tkinter as tk
from tkinter import ttk


class LabelButtonRow(tk.Frame):
    def __init__(self, parent, label_text, button_text, button_command=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.label = ttk.Label(self, text=label_text)
        self.button = ttk.Button(self, text=button_text, command=button_command)

        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
