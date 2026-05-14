import os
import tkinter as tk
from tkinter import filedialog

from clock_wallpaper import ClockWallpaper
from utils import check_path


class FilePicker(tk.Frame):
    def __init__(self, parent, file_type):
        self.parent = parent
        super().__init__(self.parent)

        self.label = tk.Label(self, text="Choose " + file_type, anchor="w")
        self.entry = tk.Entry(self)
        self.button = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_file(self.entry, file_type),
        )

        row_num = 0
        self.label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.entry.grid(row=row_num, column=1, columnspan=2, sticky="ew", padx=5)
        self.button.grid(row=row_num, column=3, sticky="ew", padx=5, pady=2)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)

    def __select_file(self, file_entry, type):
        file = file_entry.get()
        if os.path.exists(file) and check_path(file, type):
            dir_path = os.path.dirname(file)
            new_file = filedialog.askopenfilename(
                initialdir=dir_path, title="Select File"
            )
        else:
            if type == "image":
                default_folder = "Images"
            else:
                default_folder = "Fonts"
            default_path = os.getcwd() + "\\" + default_folder
            new_file = filedialog.askopenfilename(
                initialdir=default_path, title="Select File"
            )
        new_file = new_file.replace("/", "\\")

        while new_file and not check_path(new_file, type):
            new_file = filedialog.askopenfilename(title="Select File")
            new_file = new_file.replace("/", "\\")

        file_entry.delete(0, "end")
        file_entry.insert(0, new_file if new_file else file)

        if new_file:
            self.parent.update_image_preview()
            self.parent.set_color_palette(self.parent.color_palette_count)

    def get(self):
        return self.entry.get()

    def set(self, path):
        self.entry.insert(0, path)
