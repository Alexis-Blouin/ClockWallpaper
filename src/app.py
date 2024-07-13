import os
import re
import tkinter as tk
import screeninfo
from tkinter import filedialog, colorchooser, ttk, messagebox, simpledialog
from clockWallpaper import ClockWallpaper
from configEditor import ConfigEditor


class Window(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.title = tk.Label(self, text="Clock Wallpaper", anchor="center")
        self.button_add_config = tk.Button(
            self, text="Add a Configuration", command=self.__add_config
        )
        self.button_edit_config = tk.Button(
            self, text="Edit a Configuration", command=self.__edit_config
        )

        self.button_quit = tk.Button(self, text="Quit", command=self.__quit)

        self.title.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.button_add_config.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.button_edit_config.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.button_quit.grid(row=3, column=0, sticky="ew", padx=30, pady=5)

    def __re_init(self):
        self.title = tk.Label(self, text="Clock Wallpaper", anchor="center")
        self.button_add_config = tk.Button(
            self, text="Add a Configuration", command=self.__add_config
        )
        self.button_edit_config = tk.Button(
            self, text="Edit a Configuration", command=self.__edit_config
        )

        self.button_quit = tk.Button(self, text="Quit", command=self.__quit)

        self.title.pack(side="top", fill="x")
        self.button_add_config.pack(side="top", fill="x")
        self.button_edit_config.pack(side="top", fill="x")
        self.button_quit.pack(side="top", fill="x")

    def __add_config(self):
        config_name = simpledialog.askstring(
            "Config Name", "Enter the new configuration name:"
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
        self.__init_editing_frame(config_name, "add")

    def __edit_config(self):
        configEditor = ConfigEditor()
        section_names = configEditor.get_section_names()

        root = tk.Tk()
        root.title("Config Name")

        label = tk.Label(root, text="Choose a configuration to edit:")
        label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=(15, 5))

        combo = ttk.Combobox(root, values=section_names)
        combo.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)

        confirm_button = tk.Button(
            root,
            text="OK",
            command=lambda: self.__confirm_edit_selection(root, combo.get()),
        )
        confirm_button.grid(row=2, column=0, sticky="ew", padx=(15, 5), pady=(10, 5))
        cancel_button = tk.Button(root, text="Cancel", command=root.destroy)
        cancel_button.grid(row=2, column=1, sticky="ew", padx=(5, 15), pady=(10, 5))

    def __confirm_edit_selection(self, root, config_name):
        root.destroy()

        for widget in self.winfo_children():
            widget.destroy()
        self.__init_editing_frame(config_name, "edit")
        self.__instanciate_config(config_name)

    def __init_editing_frame(self, config_name, mode):
        # Conf name
        self.conf_name_label = tk.Label(self, text=config_name, anchor="center")

        # Image
        self.img_label = tk.Label(self, text="Choose image:", anchor="w")
        self.img_entry = tk.Entry(self)
        self.img_button = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_file(self.img_entry, "image"),
        )

        # Font
        self.font_label = tk.Label(self, text="Choose font:", anchor="w")
        self.font_entry = tk.Entry(self)
        self.font_button = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_file(self.font_entry, "font"),
        )

        # Monitor
        self.monitor_label = tk.Label(self, text="Choose monitor:", anchor="w")
        monitor_count = self.__get_monitor_count()
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
        self.hours_color = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_color(self.hours_color_entry),
        )
        self.minutes_color_label = tk.Label(self, text="Minutes", anchor="w")
        self.minutes_color_entry = tk.Entry(self)
        self.minutes_color = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_color(self.minutes_color_entry),
        )
        self.split_color_label = tk.Label(self, text="Split", anchor="w")
        self.split_color_entry = tk.Entry(self)
        self.split_color = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_color(self.split_color_entry),
        )

        # Cancel button
        self.cancel_button = tk.Button(
            self, text="Cancel", command=self.__return_to_menu
        )
        # Save button
        self.save_button = tk.Button(
            self, text="Save", command=lambda: self.__save_config(mode)
        )

        # Show the options
        row_num = 0

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
        # TODO add a color square to show the color
        self.color_label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        row_num += 1
        self.hours_color_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.hours_color_entry.grid(row=row_num, column=1, sticky="ew", padx=5)
        self.hours_color.grid(row=row_num, column=2, sticky="ew", padx=12)
        row_num += 1
        self.minutes_color_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.minutes_color_entry.grid(row=row_num, column=1, sticky="ew", padx=5)
        self.minutes_color.grid(row=row_num, column=2, sticky="ew", padx=12)
        row_num += 1
        self.split_color_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.split_color_entry.grid(row=row_num, column=1, sticky="ew", padx=5)
        self.split_color.grid(row=row_num, column=2, sticky="ew", padx=12)
        row_num += 1

        # Cancel button
        self.cancel_button.grid(row=row_num, column=2, sticky="ew", padx=5, pady=5)
        # Save button
        self.save_button.grid(row=row_num, column=3, sticky="ew", padx=5, pady=5)

    def __instanciate_config(self, config_name):
        configEditor = ConfigEditor()
        config = configEditor.get_section(config_name)
        if config:
            # Paths
            self.img_entry.insert(
                0, config["imagepath"] + "\\" + config["fullimagename"]
            )
            self.font_entry.insert(
                0, config["fontpath"] + "\\" + config["fullfontname"]
            )

            # Monitor
            self.monitor_combo.current(int(config["monitorid"]))

            # Hours
            hours = config["hours"].split(",")
            self.hours_position_x.insert(0, hours[0])
            self.hours_position_y.insert(0, hours[1])
            self.hours_color_entry.insert(0, f"#{hours[2]}")
            self.hours_size.insert(0, hours[3])

            # Minutes
            minutes = config["minutes"].split(",")
            self.minutes_position_x.insert(0, minutes[0])
            self.minutes_position_y.insert(0, minutes[1])
            self.minutes_color_entry.insert(0, f"#{minutes[2]}")
            self.minutes_size.insert(0, minutes[3])

            # Split
            split = config["split"].split(",")
            self.split_position_x.insert(0, split[0])
            self.split_position_y.insert(0, split[1])
            self.split_color_entry.insert(0, f"#{split[2]}")
            self.split_size.insert(0, split[3])

    def __quit(self):
        self.parent.quit()

    def __get_monitor_count(self):
        infos = screeninfo.get_monitors()
        res = []
        for info in infos:
            res.append((info.width, info.height))
        # TODO use the res to modify image before modifying it
        return len(screeninfo.get_monitors())

    def __select_file(self, file_entry, type):
        # https://pythonspot.com/tk-file-dialogs/
        # ask the user to select a file, then we get the ful path
        file = file_entry.get()
        if os.path.exists(file) and self.__check_path(file_entry.get(), type):
            dir_path = os.path.dirname(file_entry.get())
            new_file = filedialog.askopenfilename(
                initialdir=dir_path, title="Select File"
            )
        else:
            new_file = filedialog.askopenfilename(title="Select File")
        new_file = new_file.replace("/", "\\")

        while new_file and not self.__check_path(new_file, type):
            new_file = filedialog.askopenfilename(title="Select File")
            new_file = new_file.replace("/", "\\")

        file_entry.delete(0, "end")
        file_entry.insert(0, new_file if new_file else file)

    def __check_path(self, file, type) -> bool:
        clockWallpaper = ClockWallpaper()
        if type == "image":
            file_ok = clockWallpaper.check_image(file)
        elif type == "font":
            file_ok = clockWallpaper.check_font(file)

        if not file_ok:
            self.__show_alert(
                "Compatibility Warning",
                f"Selected {type} is incompatible. Please choose a different {type}.",
            )
        return file_ok

    def __check_position(self, name, position_x, position_y) -> bool:
        if not position_x or not position_y:
            self.__show_alert("Empty Position", f"Please fill in the {name} positions.")
            return False

        try:
            position_x = int(position_x)
            position_y = int(position_y)
        except ValueError:
            self.__show_alert(
                "Position Warning",
                f"Please make sure that positions from {name} are numbers.",
            )
            return False

        # TODO add check if the position is within the selected monitor size
        if position_x < 0 or position_y < 0:
            self.__show_alert(
                "Position Warning",
                f"Please make sure that positions from {name} are positive numbers and within the selected monitor size.",
            )
            return False

        return True

    def __check_size(self, name, size) -> bool:
        if not size:
            self.__show_alert("Empty Size", f"Please fill in the {name} size.")
            return False

        try:
            size = int(size)
        except ValueError:
            self.__show_alert(
                "Size Warning",
                f"Please make sure that size from {name} is a number.",
            )
            return False

        if size < 0:
            self.__show_alert(
                "Size Warning",
                f"Please make sure that size from {name} is a positive number.",
            )
            return False

        return True

    def __select_color(self, picker_entry):
        # https://pythonspot.com/tk-color-picker/
        # ask the user to select a color
        initial_color = picker_entry.get()
        if self.__is_hex_color(initial_color):
            initial_color = self.__hex_to_rgb(initial_color[1:])
        else:
            initial_color = (127, 127, 127)
        rgb, hex = colorchooser.askcolor(initial_color)
        if hex:
            picker_entry.delete(0, "end")
            picker_entry.insert(0, hex)

    def __is_hex_color(self, color) -> bool:
        regex = r"^#[0-9a-fA-F]{6}$"
        return re.match(regex, color)

    def __check_color(self, name, color) -> bool:
        if not color:
            self.__show_alert("Empty Color", f"Please select the {name} color.")
            return False

        if not self.__is_hex_color(color):
            self.__show_alert(
                "Color Warning",
                f"Please make sure that color from {name} is a hexadecimal color.",
            )
            return False

        return True

    def __hex_to_rgb(self, hex_color):
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def __show_alert(self, title, message):
        messagebox.showwarning(title, message)

    def __return_to_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.__re_init()

    def __save_config(self, mode):
        if not self.__check_inputs():
            return

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
            if mode != "edit":
                message = f"Do you want to overwrite the config {config_name}?"
                title = "Existing Config"
                result = messagebox.askquestion(title, message)
            else:
                result = "yes"
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

        self.__show_alert("Success", "Configuration saved successfully.")
        self.__return_to_menu()

    def __check_inputs(self) -> bool:
        if not self.__check_path(self.img_entry.get(), "image"):
            return False
        if not self.__check_path(self.font_entry.get(), "font"):
            return False

        if not self.__check_position(
            "Hours", self.hours_position_x.get(), self.hours_position_y.get()
        ):
            return False
        if not self.__check_position(
            "Minutes", self.minutes_position_x.get(), self.minutes_position_y.get()
        ):
            return False
        if not self.__check_position(
            "Split", self.split_position_x.get(), self.split_position_y.get()
        ):
            return False

        if not self.__check_size("Hours", self.hours_size.get()):
            return False
        if not self.__check_size("Minutes", self.minutes_size.get()):
            return False
        if not self.__check_size("Split", self.split_size.get()):
            return False

        if not self.__check_color("Hours", self.hours_color_entry.get()):
            return False
        if not self.__check_color("Minutes", self.minutes_color_entry.get()):
            return False
        if not self.__check_color("Split", self.split_color_entry.get()):
            return False

        return True


# if this is run as a program (versus being imported),
# create a root window and an instance of our example,
# then start the event loop

if __name__ == "__main__":
    root = tk.Tk()
    Window(root).pack(fill="both", expand=True)
    root.mainloop()
