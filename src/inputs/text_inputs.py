import tkinter as tk
from tkinter import colorchooser

from utils import is_hex_color


class TextInputs(tk.Frame):
    def __init__(self, parent, label):
        self.parent = parent
        super().__init__(self.parent)
        self.label = tk.Label(self, text=label, anchor="w")
        # Layer
        self.layer_up = tk.Button(
            self,
            text="<",
            command=lambda: self.parent.change_layer("up", label.lower()),
        )
        self.layer_down = tk.Button(
            self,
            text=">",
            command=lambda: self.parent.change_layer("down", label.lower()),
        )
        # Enabled
        self.enable_var = tk.IntVar()
        self.enable_check = tk.Checkbutton(self, text="Enabled", variable=self.enable_var)
        # Position
        self.position_x_label = tk.Label(self, text="Position X", anchor="w")
        self.position_x = tk.Entry(self, name="test")
        self.position_y_label = tk.Label(self, text="Position Y", anchor="w")
        self.position_y = tk.Entry(self)
        # Size
        self.size_label = tk.Label(self, text="Size", anchor="w")
        self.size = tk.Entry(self)
        # Color
        self.color_label = tk.Label(self, text="Color", anchor="w")
        self.color_entry = tk.Entry(self)
        self.color = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_color(self.color_entry),
        )

        row_num = 0
        # self.label.pack()
        self.label.grid(row=row_num, column=0, sticky="ew", padx=5)
        # Layer
        self.layer_up.grid(row=row_num, column=1, sticky="e", padx=5)
        self.layer_down.grid(row=row_num, column=2, sticky="w", padx=5)
        row_num += 1
        # Enabled
        self.enable_check.grid(row=row_num, column=1, sticky="ew", padx=5)
        row_num += 1
        # Position
        self.position_x_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.position_x.grid(row=row_num, column=1, columnspan=2, sticky="ew", padx=5)
        row_num += 1
        self.position_y_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.position_y.grid(row=row_num, column=1, columnspan=2, sticky="ew", padx=5)
        row_num += 1
        # Size
        self.size_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.size.grid(row=row_num, column=1, columnspan=2, sticky="ew", padx=5)
        row_num += 1
        # Color
        self.color_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.color_entry.grid(row=row_num, column=1, columnspan=2, sticky="ew", padx=5)
        self.color.grid(row=row_num, column=3, sticky="ew", padx=5, pady=2)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

    def __select_color(self, picker_entry):
        initial_color = picker_entry.get()
        if is_hex_color(initial_color):
            initial_color = self.__hex_to_rgb(initial_color[1:])
        else:
            initial_color = (127, 127, 127)
        rgb, hex = colorchooser.askcolor(initial_color)
        if hex:
            picker_entry.delete(0, "end")
            picker_entry.insert(0, hex)

    def __hex_to_rgb(self, hex_color):
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def get_position_x(self):
        return self.position_x.get()

    def set_position_x(self, x):
        self.position_x.insert(0, x)

    def get_position_y(self):
        return self.position_y.get()

    def set_position_y(self, y):
        self.position_y.insert(0, y)

    def get_size(self):
        return self.size.get()

    def set_size(self, size):
        self.size.insert(0, size)

    def get_color(self):
        return self.color_entry.get()

    def set_color(self, color):
        self.color_entry.insert(0, color)

    def get_enabled(self):
        return self.enable_var.get()

    def set_enabled(self, enabled):
        if enabled == 1:
            self.enable_check.select()

    def get_input_config(self):
        return f"{self.get_position_x()},{self.get_position_y()},{self.get_color()[1:]},{self.get_size()},{self.get_enabled()}"
