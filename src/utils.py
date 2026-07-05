import os
import re
from tkinter import messagebox
from colorthief import ColorThief
from clock_wallpaper import ClockWallpaper


def check_path(file, type) -> bool:
    clockWallpaper = ClockWallpaper()
    if type == "image":
        file_ok = clockWallpaper.check_image(file)
    elif type == "font":
        file_ok = clockWallpaper.check_font(file)

    if not file_ok:
        show_alert(
            "Compatibility Warning",
            f"Selected {type} is incompatible. Please choose a different {type}.",
            "warning",
        )
    return file_ok


def show_alert(title, message, type):
    if type == "error":
        messagebox.showerror(title, message)
    elif type == "warning":
        messagebox.showwarning(title, message)
    elif type == "info":
        messagebox.showinfo(title, message)


def is_hex_color(color) -> bool:
    regex = r"^#[0-9a-fA-F]{6}$"
    return re.match(regex, color)


def get_color_palette(img_path, num_colors):
    color_thief = ColorThief(img_path)
    palette_rgb = color_thief.get_palette(num_colors)
    for color in palette_rgb:
        yield '#%02x%02x%02x' % color

def parse_text(text):
    parsed_text = text.split(",")
    parsed_text[0] = int(parsed_text[0])
    parsed_text[5] = int(parsed_text[5])
    return parsed_text

def delete_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
