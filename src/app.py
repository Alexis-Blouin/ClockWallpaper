import tkinter as tk
import screeninfo
from tkinter import filedialog, colorchooser, ttk, messagebox, simpledialog
from clockWallpaper import ClockWallpaper
from configEditor import ConfigEditor


class Example(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.title = tk.Label(self, text="Clock Wallpaper", anchor="w")
        self.add_config_button = tk.Button(
            self, text="Add a Configuration", command=self.__add_config
        )
        self.edit_config_button = tk.Button(
            self, text="Edit a Configuration", command=self.__edit_config
        )

        self.title.pack(side="top", fill="x")
        self.add_config_button.pack(side="top", fill="x")
        self.edit_config_button.pack(side="top", fill="x")

    def __re_init(self):
        self.title = tk.Label(self, text="Clock Wallpaper", anchor="w")
        self.add_config_button = tk.Button(
            self, text="Add a Configuration", command=self.__add_config
        )
        self.edit_config_button = tk.Button(
            self, text="Edit a Configuration", command=self.__edit_config
        )

        self.title.pack(side="top", fill="x")
        self.add_config_button.pack(side="top", fill="x")
        self.edit_config_button.pack(side="top", fill="x")

    def __add_config(self):
        config_name = simpledialog.askstring(
            "Configuration Name", "Enter the new configuration name:"
        )
        if config_name is None:
            return
        if not config_name:
            configEditor = ConfigEditor()
            section_names = configEditor.get_section_names()

            config_name = "Config_"
            config_id = 1
            while config_name + str(config_id) in section_names:
                config_id += 1
            config_name += str(config_id)

        for widget in self.winfo_children():
            widget.destroy()
        self.__init_editing_frame(config_name)

    def __edit_config(self):
        configEditor = ConfigEditor()
        section_names = configEditor.get_section_names()

        root = tk.Tk()
        # root.withdraw()

        label = tk.Label(root, text="Choose a configuration to edit:")
        label.pack()

        combo = ttk.Combobox(root, values=section_names)
        combo.pack()

        cancel_button = tk.Button(root, text="Cancel", command=root.destroy)
        cancel_button.pack()
        confirm_button = tk.Button(
            root,
            text="Confirm",
            command=lambda: self.__confirm_edit_selection(root, combo.get()),
        )
        confirm_button.pack()

    def __confirm_edit_selection(self, root, config_name):
        root.destroy()

        for widget in self.winfo_children():
            widget.destroy()
        self.__init_editing_frame(config_name)

    def __init_editing_frame(self, config_name):
        # tk.Frame.__init__(self, self.parent)

        # Conf name
        self.conf_name_label = tk.Label(self, text=config_name, anchor="w")

        # Image
        self.img_label = tk.Label(self, text="Choose image:", anchor="w")
        self.img_entry = tk.Entry(self)
        self.img_button = tk.Button(
            self, text="...", command=lambda: self.select_file(self.img_entry, "image")
        )

        # Font
        self.font_label = tk.Label(self, text="Choose font:", anchor="w")
        self.font_entry = tk.Entry(self)
        self.font_button = tk.Button(
            self, text="...", command=lambda: self.select_file(self.font_entry, "font")
        )

        # Monitor
        self.monitor_label = tk.Label(self, text="Choose monitor:", anchor="w")
        monitor_count = self.get_monitor_count()
        values = []
        for i in range(monitor_count):
            values.append(f"Monitor {i + 1}")
        self.monitor_combo = ttk.Combobox(self, values=values)
        self.monitor_combo.current(0)

        # Position
        self.position_label = tk.Label(self, text="Position", anchor="w")

        self.hours_position_label = tk.Label(self, text="Hours", anchor="w")
        self.hours_position_x_label = tk.Label(self, text="X", anchor="w")
        self.hours_position_x = tk.Entry(self)
        self.hours_position_y_label = tk.Label(self, text="Y", anchor="w")
        self.hours_position_y = tk.Entry(self)

        self.minutes_position_label = tk.Label(self, text="Minutes", anchor="w")
        self.minutes_position_x_label = tk.Label(self, text="X", anchor="w")
        self.minutes_position_x = tk.Entry(self)
        self.minutes_position_y_label = tk.Label(self, text="Y", anchor="w")
        self.minutes_position_y = tk.Entry(self)

        self.split_position_label = tk.Label(self, text="Split", anchor="w")
        self.split_position_x_label = tk.Label(self, text="X", anchor="w")
        self.split_position_x = tk.Entry(self)
        self.split_position_y_label = tk.Label(self, text="Y", anchor="w")
        self.split_position_y = tk.Entry(self)

        # Size
        self.size_label = tk.Label(self, text="Size", anchor="w")

        self.hours_size_label = tk.Label(self, text="Hours", anchor="w")
        self.hours_size = tk.Entry(self)
        self.minutes_size_label = tk.Label(self, text="Minutes", anchor="w")
        self.minutes_size = tk.Entry(self)
        self.split_size_label = tk.Label(self, text="Split", anchor="w")
        self.split_size = tk.Entry(self)

        # Color
        self.color_label = tk.Label(self, text="Color", anchor="w")

        self.hours_color_label = tk.Label(self, text="Hours", anchor="w")
        self.hours_color_entry = tk.Entry(self)
        # TODO modify color picker to take entry argument
        self.hours_color = tk.Button(
            self, text="...", command=lambda: self.choose_color(self.hours_color_entry)
        )
        self.minutes_color_label = tk.Label(self, text="Minutes", anchor="w")
        self.minutes_color_entry = tk.Entry(self)
        self.minutes_color = tk.Button(
            self,
            text="...",
            command=lambda: self.choose_color(self.minutes_color_entry),
        )
        self.split_color_label = tk.Label(self, text="Split", anchor="w")
        self.split_color_entry = tk.Entry(self)
        self.split_color = tk.Button(
            self, text="...", command=lambda: self.choose_color(self.split_color_entry)
        )

        # Cancel button
        self.cancel_button = tk.Button(
            self, text="Cancel", command=self.__return_to_menu
        )
        # Save button
        self.save_button = tk.Button(self, text="Save", command=self.__save_config)

        # Show the options
        row_num = 0
        # TODO check colspan, cause not working...
        # Conf name
        self.conf_name_label.grid(row=row_num, column=1, sticky="ew", padx=5, pady=5)
        row_num += 1

        # Image
        self.img_label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        self.img_entry.grid(
            row=row_num, column=1, columnspan=2, sticky="ew", padx=5, pady=5
        )
        self.img_button.grid(row=row_num, column=3, sticky="ew", padx=5, pady=5)
        row_num += 1

        # Font
        self.font_label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        self.font_entry.grid(
            row=row_num, column=1, columnspan=2, sticky="ew", padx=5, pady=5
        )
        self.font_button.grid(row=row_num, column=3, sticky="ew", padx=5, pady=5)
        row_num += 1

        # Monitor
        self.monitor_label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        self.monitor_combo.grid(row=row_num, column=1, sticky="ew", padx=5, pady=5)
        row_num += 1

        # Position
        self.position_label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        row_num += 1

        self.hours_position_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        row_num += 1
        self.hours_position_x_label.grid(row=row_num, column=0, sticky="w", padx=5)
        self.hours_position_x.grid(row=row_num, column=1, sticky="ew", padx=5)
        row_num += 1
        self.hours_position_y_label.grid(row=row_num, column=0, sticky="w", padx=5)
        self.hours_position_y.grid(row=row_num, column=1, sticky="ew", padx=5)
        row_num += 1

        self.minutes_position_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        row_num += 1
        self.minutes_position_x_label.grid(row=row_num, column=0, sticky="w", padx=5)
        self.minutes_position_x.grid(row=row_num, column=1, sticky="ew", padx=5)
        row_num += 1
        self.minutes_position_y_label.grid(row=row_num, column=0, sticky="w", padx=5)
        self.minutes_position_y.grid(row=row_num, column=1, sticky="ew", padx=5)
        row_num += 1

        self.split_position_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        row_num += 1
        self.split_position_x_label.grid(row=row_num, column=0, sticky="w", padx=5)
        self.split_position_x.grid(row=row_num, column=1, sticky="ew", padx=5)
        row_num += 1
        self.split_position_y_label.grid(row=row_num, column=0, sticky="w", padx=5)
        self.split_position_y.grid(row=row_num, column=1, sticky="ew", padx=5)
        row_num += 1

        # Size
        self.size_label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        row_num += 1
        self.hours_size_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.hours_size.grid(row=row_num, column=1, sticky="ew", padx=5)
        row_num += 1
        self.minutes_size_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.minutes_size.grid(row=row_num, column=1, sticky="ew", padx=5)
        row_num += 1
        self.split_size_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.split_size.grid(row=row_num, column=1, sticky="ew", padx=5)
        row_num += 1

        # Color
        self.color_label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        row_num += 1
        self.hours_color_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.hours_color_entry.grid(row=row_num, column=1, sticky="ew", padx=5)
        self.hours_color.grid(row=row_num, column=2, sticky="ew", padx=5)
        row_num += 1
        self.minutes_color_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.minutes_color_entry.grid(row=row_num, column=1, sticky="ew", padx=5)
        self.minutes_color.grid(row=row_num, column=2, sticky="ew", padx=5)
        row_num += 1
        self.split_color_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.split_color_entry.grid(row=row_num, column=1, sticky="ew", padx=5)
        self.split_color.grid(row=row_num, column=2, sticky="ew", padx=5)
        row_num += 1

        # Cancel button
        self.cancel_button.grid(row=row_num, column=2, sticky="ew", padx=5, pady=5)
        # Save button
        self.save_button.grid(row=row_num, column=3, sticky="ew", padx=5, pady=5)

    def get_monitor_count(self):
        infos = screeninfo.get_monitors()
        res = []
        for info in infos:
            res.append((info.width, info.height))
        # TODO use the res to modify image before modifiyyin it
        return len(screeninfo.get_monitors())

    def select_file(self, file_entry, type):
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

        file_entry.delete(0, "end")
        file_entry.insert(0, file)

    def choose_color(self, picker_entry):
        # https://pythonspot.com/tk-color-picker/
        # ask the user to select a color
        initial_color = picker_entry.get()
        print(initial_color)
        if initial_color:
            initial_color = self.__hex_to_rgb(initial_color[1:])
        else:
            initial_color = (127, 127, 127)
        print(initial_color)
        rgb, hex = colorchooser.askcolor(initial_color)
        if hex:
            picker_entry.delete(0, "end")
            picker_entry.insert(0, hex)

    def __hex_to_rgb(self, hex_color):
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def __return_to_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.__re_init()

    def __save_config(self):
        # TODO Verify that all the inputs are correct when quiting the focus

        config_name = self.conf_name_label["text"]
        image_path_array = self.img_entry.get().split("\\")
        image_path = "\\".join(image_path_array[:-1])
        image_name = image_path_array[-1]
        font_path_array = self.font_entry.get().split("\\")
        font_path = "\\".join(font_path_array[:-1])
        font_name = font_path_array[-1]
        monitor_id = self.monitor_combo.current()
        text_hours = f"{self.hours_position_x.get()},{self.hours_position_y.get()},{self.hours_color_entry.get()[1:]},{self.hours_size.get()}"
        text_minutes = f"{self.minutes_position_x.get()},{self.minutes_position_y.get()},{self.minutes_color_entry.get()[1:]},{self.minutes_size.get()}"
        text_split = f"{self.split_position_x.get()},{self.split_position_y.get()},{self.split_color_entry.get()[1:]},{self.split_size.get()}"

        configEditor = ConfigEditor()
        config = configEditor.get_section(config_name)
        if config:
            message = f"Do you want to overwrite the config {config_name}?"
            title = "Existing Config"
            result = messagebox.askquestion(title, message)
            if result == "yes":
                configEditor.modify_section(
                    config_name,
                    image_path,
                    font_path,
                    image_name,
                    font_name,
                    monitor_id,
                    text_hours,
                    text_minutes,
                    text_split,
                )
        else:
            configEditor.add_section(
                config_name,
                image_path,
                font_path,
                image_name,
                font_name,
                monitor_id,
                text_hours,
                text_minutes,
                text_split,
            )


# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
