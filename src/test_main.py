import tkinter as tk
from inputs.test_class import LabelButtonRow
from inputs.text_zone import TextZone


def on_click():
    print("Button clicked!")


root = tk.Tk()

minutes_component = TextZone(root, "Minustes")
minutes_component.grid(row=0, column=0, padx=10, pady=10)

root.mainloop()
