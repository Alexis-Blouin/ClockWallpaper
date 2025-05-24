import re
from tkinter import messagebox
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
