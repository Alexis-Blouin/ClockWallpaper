import os
import tkinter as tk
from tkinter import filedialog

from clock_wallpaper import ClockWallpaper
from utils import check_path


class FilePicker(tk.Frame):
    def __init__(self, parent, file_type):
        self.parent = parent
        super().__init__(self.parent)

        self.img_label = tk.Label(self, text="Choose " + file_type + ":", anchor="w")
        self.img_entry = tk.Entry(self)
        self.img_button = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_file(self.img_entry, file_type),
        )

        row_num = 0
        self.img_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.img_entry.grid(row=row_num, column=1, columnspan=2, sticky="ew", padx=5)
        self.img_button.grid(row=row_num, column=3, sticky="ew", padx=5, pady=2)

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

    def get(self):
        return self.img_entry.get()
