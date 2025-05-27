import tkinter as tk
from menu import Menu

if __name__ == "__main__":
    root = tk.Tk()
    Menu(root).grid(row=0, column=0)
    root.mainloop()
