import tkinter as tk

class ConfigurationName(tk.Frame):
    def __init__(self, parent, config_name, check_config_name):
        self.parent = parent
        super().__init__(self.parent)

        self.label = tk.Label(self, text="Configuration Name", anchor="w")
        self.entry = tk.Entry(self)
        self.entry.insert(0, config_name)
        self.entry.bind("<FocusOut>", check_config_name)

        self.label.grid(row=0, column=0, sticky="ew", padx=5)
        self.entry.grid(row=0, column=1, sticky="ew", padx=5)

    def get(self):
        return self.entry.get()