import tkinter as tk
from clockWallpaper import ClockWallpaper
from configEditor import ConfigEditor
from window import Window

if __name__ == "__main__":
    root = tk.Tk()
    Window(root).pack(fill="both", expand=True)
    root.mainloop()
