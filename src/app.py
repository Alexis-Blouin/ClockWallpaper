import tkinter as tk
from tkinter import filedialog, colorchooser, ttk, messagebox
from clockWallpaper import ClockWallpaper


class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Image picker
        self.img_label = tk.Label(self, text="Choose image:", anchor="w")
        self.img_entry = tk.Entry(self)
        self.img_button = tk.Button(
            self, text="...", command=lambda: self.select_file("image")
        )

        # Font picker
        self.font_label = tk.Label(self, text="Choose font:", anchor="w")
        self.font_entry = tk.Entry(self)
        self.font_button = tk.Button(
            self, text="...", command=lambda: self.select_file("font")
        )

        # Monitor picker
        self.monitor_label = tk.Label(self, text="Choose monitor:", anchor="w")
        self.monitor_combo = ttk.Combobox(
            self, values=["Monitor 1", "Monitor 2", "Monitor 3"]
        )
        self.monitor_combo.current(0)
        self.monitor_combo.bind("<<ComboboxSelected>>", self.monitor_selected)

        # Position
        self.hours_position_label = tk.Label(self, text="Position hours", anchor="w")
        self.hours_position_x_label = tk.Label(self, text="X", anchor="w")
        self.hours_position_x = tk.Entry(self)
        self.hours_position_y_label = tk.Label(self, text="Y", anchor="w")
        self.hours_position_y = tk.Entry(self)

        self.minutes_position_label = tk.Label(
            self, text="Position minutes", anchor="w"
        )
        self.minutes_position_x_label = tk.Label(self, text="X", anchor="w")
        self.minutes_position_x = tk.Entry(self)
        self.minutes_position_y_label = tk.Label(self, text="Y", anchor="w")
        self.minutes_position_y = tk.Entry(self)

        self.split_position_label = tk.Label(self, text="Position split", anchor="w")
        self.split_position_x_label = tk.Label(self, text="X", anchor="w")
        self.split_position_x = tk.Entry(self)
        self.split_position_y_label = tk.Label(self, text="Y", anchor="w")
        self.split_position_y = tk.Entry(self)

        # Size
        self.hours_size_label = tk.Label(self, text="Size hours", anchor="w")
        self.hours_size = tk.Entry(self)
        self.minutes_size_label = tk.Label(self, text="Size minutes", anchor="w")
        self.minutes_size = tk.Entry(self)
        self.split_size_label = tk.Label(self, text="Size split", anchor="w")
        self.split_size = tk.Entry(self)

        # Color
        self.hours_color_label = tk.Label(self, text="Color hours", anchor="w")
        self.hours_color = tk.Button(self, text="Pick", command=self.choose_color)
        self.minutes_color_label = tk.Label(self, text="Color minutes", anchor="w")
        self.minutes_color = tk.Button(self, text="Pick", command=self.choose_color)
        self.split_color_label = tk.Label(self, text="Color split", anchor="w")
        self.split_color = tk.Button(self, text="Pick", command=self.choose_color)

        # Save button
        self.save_button = tk.Button(self, text="Save", command=self.__verify_inputs)

        # Show the options
        # TODO check colspan, cause not working...
        self.img_label.grid(column=0, row=0, sticky="ew", padx=5, pady=5)
        self.img_entry.grid(column=1, row=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.img_button.grid(column=3, row=0, padx=5, pady=5)

        self.font_label.grid(column=0, row=1, sticky="ew", padx=5, pady=5)
        self.font_entry.grid(column=1, row=1, columnspan=2, sticky="ew", padx=5, pady=5)
        self.font_button.grid(column=3, row=1, padx=5, pady=5)

        self.monitor_label.grid(column=0, row=2, sticky="ew", padx=5, pady=5)
        self.monitor_combo.grid(column=1, row=2, sticky="ew", padx=5, pady=5)

        self.hours_position_label.grid(column=0, row=3, sticky="ew", padx=5, pady=5)
        self.hours_position_x_label.grid(column=0, row=4, sticky="w", padx=5)
        self.hours_position_x.grid(column=1, row=4, sticky="ew", padx=5)
        self.hours_position_y_label.grid(column=0, row=5, sticky="w", padx=5)
        self.hours_position_y.grid(column=1, row=5, sticky="ew", padx=5)

        self.minutes_position_label.grid(column=0, row=6, sticky="ew", padx=5, pady=5)
        self.minutes_position_x_label.grid(column=0, row=7, sticky="w", padx=5)
        self.minutes_position_x.grid(column=1, row=7, sticky="ew", padx=5)
        self.minutes_position_y_label.grid(column=0, row=8, sticky="w", padx=5)
        self.minutes_position_y.grid(column=1, row=8, sticky="ew", padx=5)

        self.split_position_label.grid(column=0, row=9, sticky="ew", padx=5, pady=5)
        self.split_position_x_label.grid(column=0, row=10, sticky="w", padx=5)
        self.split_position_x.grid(column=1, row=10, sticky="ew", padx=5)
        self.split_position_y_label.grid(column=0, row=11, sticky="w", padx=5)
        self.split_position_y.grid(column=1, row=11, sticky="ew", padx=5)

        # self.hours_size_label.pack(side="top", fill="x")
        # self.hours_size.pack(side="top", fill="x", expand=True)
        # self.minutes_size_label.pack(side="top", fill="x")
        # self.minutes_size.pack(side="top", fill="x", expand=True)
        # self.split_size_label.pack(side="top", fill="x")
        # self.split_size.pack(side="top", fill="x", expand=True)

        # self.hours_color_label.pack(side="top", fill="x")
        # self.hours_color.pack(side="top", fill="x", expand=True)
        # self.minutes_color_label.pack(side="top", fill="x")
        # self.minutes_color.pack(side="top", fill="x", expand=True)
        # self.split_color_label.pack(side="top", fill="x")
        # self.split_color.pack(side="top", fill="x", expand=True)

        # self.save_button.pack(side="top", fill="x", expand=True)

    def calculate(self):
        # get the value from the input widget, convert
        # it to an int, and do a calculation
        try:
            i = int(self.entry.get())
            result = "%s*2=%s" % (i, i * 2)
        except ValueError:
            result = "Please enter digits only"

        # set the output widget to have our result
        self.output.configure(text=result)

    def select_file(self, type):
        # https://pythonspot.com/tk-file-dialogs/
        # ask the user to select a file, then we get the ful path
        file = filedialog.askopenfilename(title="Select File")
        file = file.replace("/", "\\")
        clockWallpaper = ClockWallpaper()
        if type == "image":
            file_ok = clockWallpaper.check_image(file)
        elif type == "font":
            file_ok = clockWallpaper.check_font(file)
        while not file_ok and file:
            message = (
                f"Selected {type} is incompatible. Please choose a different {type}."
            )
            title = "Compatibility Warning"
            messagebox.showwarning(title, message)

            file = filedialog.askopenfilename(title="Select File")
            if type == "image":
                file_ok = clockWallpaper.check_image(file)
            elif type == "font":
                file_ok = clockWallpaper.check_font(file)
        if type == "image":
            self.img_entry.delete(0, "end")
            self.img_entry.insert(0, file)
        elif type == "font":
            self.font_entry.delete(0, "end")
            self.font_entry.insert(0, file)

    def choose_color(self):
        # https://pythonspot.com/tk-color-picker/
        # ask the user to select a color
        color = colorchooser.askcolor()
        print(color)

    def monitor_selected(self, event):
        # https://pythonspot.com/tk-drop-down-list/
        # get the selected value from the combobox
        monitor_id = self.monitor_combo.current()
        print(monitor_id)

    def __verify_inputs(self):
        # TODO Verify that all the inputs are correct
        pass


# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
