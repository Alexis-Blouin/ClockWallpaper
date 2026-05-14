import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from clock_wallpaper import ClockWallpaper
from utils import check_path

class ImageColorPicker(tk.Label):
    def __init__(self, parent, on_color_pick):
        super().__init__(parent, cursor="tcross")

        self.tk_image = None
        self.original_image = None
        self.last_color_picked = "#000000"
        self.on_color_pick = on_color_pick

        self.bind("<Button-1>", self.__on_click)

    def set_image(self, img):
        self.original_image = img
        img = ImageTk.PhotoImage(img)
        self.config(image=img)
        self.tk_image = img

    def __on_click(self, event):
        # We can click a tiny bit out of the image, so a simple boundary check
        width, height = self.original_image.size
        if not (0 <= event.x < width and 0 <= event.y < height):
            return

        r, g, b = self.original_image.getpixel((event.x, event.y))
        self.last_color_picked = f"#{r:02x}{g:02x}{b:02x}"

        if self.on_color_pick:
            self.on_color_pick(self.last_color_picked)