import tkinter as tk
from tkinter import colorchooser

from utils import is_hex_color


class TextZone(tk.Frame):
    def __init__(self, parent, label):
        self.parent = parent
        super().__init__(self.parent)
        self.minutes_label = tk.Label(self, text=label, anchor="w")
        # Layer
        self.layers = {"hours": 0, "minutes": 1, "split": 2}
        self.minutes_layer_up = tk.Button(
            self, text="<", command=lambda: self.__change_layer("up", label.lower())
        )
        self.minutes_layer_down = tk.Button(
            self, text=">", command=lambda: self.__change_layer("down", label.lower())
        )
        # Position
        self.minutes_position_x_label = tk.Label(self, text="Position X", anchor="w")
        self.minutes_position_x = tk.Entry(self)
        self.minutes_position_y_label = tk.Label(self, text="Position Y", anchor="w")
        self.minutes_position_y = tk.Entry(self)
        # Size
        self.minutes_size_label = tk.Label(self, text="Size", anchor="w")
        self.minutes_size = tk.Entry(self)
        # Color
        self.minutes_color_label = tk.Label(self, text="Color", anchor="w")
        self.minutes_color_entry = tk.Entry(self)
        self.minutes_color = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_color(self.minutes_color_entry),
        )

        row_num = 0
        # self.minutes_label.pack()
        self.minutes_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        # Layer
        self.minutes_layer_up.grid(row=row_num, column=1, sticky="e", padx=5)
        self.minutes_layer_down.grid(row=row_num, column=2, sticky="w", padx=5)
        row_num += 1
        # Position
        self.minutes_position_x_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.minutes_position_x.grid(
            row=row_num, column=1, columnspan=2, sticky="ew", padx=5
        )
        row_num += 1
        self.minutes_position_y_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.minutes_position_y.grid(
            row=row_num, column=1, columnspan=2, sticky="ew", padx=5
        )
        row_num += 1
        # Size
        self.minutes_size_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.minutes_size.grid(row=row_num, column=1, columnspan=2, sticky="ew", padx=5)
        row_num += 1
        # Color
        self.minutes_color_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.minutes_color_entry.grid(
            row=row_num, column=1, columnspan=2, sticky="ew", padx=5
        )
        self.minutes_color.grid(row=row_num, column=3, sticky="ew", padx=5, pady=2)

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

    def __change_layer(self, direction, element):
        if element == "hours":
            current_layer = self.layers["hours"]
        elif element == "minutes":
            current_layer = self.layers["minutes"]
        elif element == "split":
            current_layer = self.layers["split"]

        if current_layer == 0 and direction == "down":
            return
        if current_layer == 2 and direction == "up":
            return

        if direction == "up":
            for key, value in self.layers.items():
                if value == current_layer + 1:
                    layer_index_to_change = key
                    break
            self.layers[element] = current_layer + 1
            self.layers[layer_index_to_change] = current_layer
        elif direction == "down":
            for key, value in self.layers.items():
                if value == current_layer - 1:
                    layer_index_to_change = key
                    break
            self.layers[element] = current_layer - 1
            self.layers[layer_index_to_change] = current_layer

        self.parent.place_inputs_by_layers()

    def get_position_x(self):
        return self.minutes_position_x.get()

    def get_position_y(self):
        return self.minutes_position_y.get()

    def get_size(self):
        return self.minutes_size.get()

    def get_color(self):
        return self.minutes_color_entry.get()

    # TODO layers getter
