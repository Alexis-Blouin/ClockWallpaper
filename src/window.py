import os
import re
import subprocess
import tkinter as tk
import screeninfo
from PIL import Image, ImageTk
from tkinter import filedialog, colorchooser, ttk, messagebox, simpledialog
from clock_wallpaper import ClockWallpaper
from config_editor import ConfigEditor
from idesktop_wallpaper import IDesktopWallpaper


class Window(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)
        self.config_editor = ConfigEditor()

        self.__init_menu()

    def __init_menu(self):
        self.title = tk.Label(self, text="Clock Wallpaper", anchor="center")
        self.button_select_config = tk.Button(
            self, text="Select a Configuration", command=self.__select_config
        )
        self.button_add_config = tk.Button(
            self, text="Add a Configuration", command=self.__add_config
        )
        self.button_edit_config = tk.Button(
            self, text="Edit a Configuration", command=self.__edit_config
        )

        self.button_quit = tk.Button(self, text="Quit", command=self.__quit)

        row_num = 0
        self.title.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        row_num += 1
        self.button_select_config.grid(
            row=row_num, column=0, sticky="ew", padx=10, pady=5
        )
        row_num += 1
        self.button_add_config.grid(row=row_num, column=0, sticky="ew", padx=10, pady=5)
        row_num += 1
        self.button_edit_config.grid(
            row=row_num, column=0, sticky="ew", padx=10, pady=5
        )
        row_num += 1
        self.button_quit.grid(row=row_num, column=0, sticky="ew", padx=30, pady=5)

    def __select_config(self):
        self.__hide_window(self.parent)

        section_names = self.config_editor.get_section_names()

        root = tk.Tk()
        root.title("Config Name")

        label = tk.Label(root, text="Choose a configuration to use:")
        label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10)

        combo = ttk.Combobox(root, values=section_names)
        combo.current(section_names.index(self.config_editor.get_config_name()))
        combo.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)

        confirm_button = tk.Button(
            root,
            text="OK",
            command=lambda: self.__apply_config(section_names, combo.get(), root),
        )
        confirm_button.grid(row=2, column=0, sticky="ew", padx=(15, 5), pady=(10, 5))
        cancel_button = tk.Button(
            root,
            text="Cancel",
            command=lambda: self.__close_choosing_window(root, self.parent),
        )
        cancel_button.grid(row=2, column=1, sticky="ew", padx=(5, 15), pady=(10, 5))

    def __apply_config(self, section_names, config_name, root=None):
        if config_name in section_names:
            if root:
                root.destroy()

            self.config_editor.apply_config(config_name)

            subprocess.run(["pythonw", "src/taskNoTime.pyw"])
            self.__show_alert("Success", "Configuration applied successfully.", "info")

            self.__show_window(self.parent)
        else:
            self.__show_alert(
                "Invalid Selection", "Please select a valid configuration.", "warning"
            )

    def __add_config(self):
        self.__hide_window(self.parent)

        config_name = simpledialog.askstring(
            "Config Name", "Enter the new configuration name:"
        )
        while config_name and self.config_editor.config_name_exist(config_name):
            self.__show_alert(
                "Config Name Error", "This config name is already existing.", "error"
            )
            config_name = simpledialog.askstring(
                "Config Name", "Enter the new configuration name:"
            )
        if config_name is None:
            self.__show_window(self.parent)
            return
        if not config_name:
            config_name = self.config_editor.generate_default_config_name()

        for widget in self.winfo_children():
            widget.destroy()
        self.__init_editing_frame(config_name, "add")
        self.__show_window(self.parent)

    def __edit_config(self):
        self.__hide_window(self.parent)

        section_names = self.config_editor.get_section_names()

        root = tk.Tk()
        root.title("Config Name")

        label = tk.Label(root, text="Choose a configuration to edit:")
        label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10)

        combo = ttk.Combobox(root, values=section_names)
        combo.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)

        confirm_button = tk.Button(
            root,
            text="OK",
            command=lambda: self.__confirm_edit_selection(root, combo.get()),
        )
        confirm_button.grid(row=2, column=0, sticky="ew", padx=(15, 5), pady=(10, 5))
        cancel_button = tk.Button(
            root,
            text="Cancel",
            command=lambda: self.__close_choosing_window(root, self.parent),
        )
        cancel_button.grid(row=2, column=1, sticky="ew", padx=(5, 15), pady=(10, 5))

    def __confirm_edit_selection(self, root, config_name):
        if self.config_editor.config_name_exist(config_name):
            root.destroy()

            for widget in self.winfo_children():
                widget.destroy()
            self.__init_editing_frame(config_name, "edit")
            self.__instanciate_config(config_name)
            self.config_editor.set_edit_config_name(config_name)

            self.__show_window(self.parent)
        else:
            self.__show_alert(
                "Invalid Selection",
                "Please select a valid configuration to edit.",
                "warning",
            )

    def __hide_window(self, window):
        window.withdraw()

    def __show_window(self, window):
        window.deiconify()

    def __close_choosing_window(self, root, window):
        root.destroy()
        self.__show_window(window)

    def __init_editing_frame(self, config_name, mode):
        # Conf name
        self.conf_name_label = tk.Label(self, text=config_name, anchor="center")
        self.conf_name_button = tk.Button(
            self, text="Modify", command=self.__modify_config_name
        )

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

        # Image preview
        self.image_preview = tk.Label(self)
        self.image_preview_button = tk.Button(
            self, text="Update Preview", command=self.__update_image_preview
        )

        # Test on monitor button
        self.test_on_monitor_button = tk.Button(
            self, text="Test on Monitor", command=self.__test_preview_on_monitor
        )

        # Hours
        self.hours_label = tk.Label(self, text="Hours", anchor="w")
        # Layer
        self.hours_layer_up = tk.Button(
            self, text="<", command=lambda: self.__change_layer("up", "hours")
        )
        self.hours_layer_down = tk.Button(
            self, text=">", command=lambda: self.__change_layer("down", "hours")
        )
        # Position
        self.hours_position_x_label = tk.Label(self, text="Position X", anchor="w")
        self.hours_position_x = tk.Entry(self)
        self.hours_position_y_label = tk.Label(self, text="Position Y", anchor="w")
        self.hours_position_y = tk.Entry(self)
        # Size
        self.hours_size_label = tk.Label(self, text="Size", anchor="w")
        self.hours_size = tk.Entry(self)
        # Color
        self.hours_color_label = tk.Label(self, text="Color", anchor="w")
        self.hours_color_entry = tk.Entry(self)
        self.hours_color = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_color(self.hours_color_entry),
        )

        # Minutes
        self.minutes_label = tk.Label(self, text="Minutes", anchor="w")
        # Layer
        self.minutes_layer_up = tk.Button(
            self, text="<", command=lambda: self.__change_layer("up", "minutes")
        )
        self.minutes_layer_down = tk.Button(
            self, text=">", command=lambda: self.__change_layer("down", "minutes")
        )
        # Position
        self.minutes_position_x_label = tk.Label(self, text="Position X", anchor="w")
        self.minutes_position_x = tk.Entry(self)
        self.minutes_position_y_label = tk.Label(self, text="Position Y", anchor="w")
        self.minutes_position_y = tk.Entry(self)
        # Size
        self.minutes_size_label = tk.Label(self, text="Size", anchor="w")
        self.minutes_size = tk.Entry(self)
        # Color
        self.minutes_color_label = tk.Label(self, text="Color", anchor="w")
        self.minutes_color_entry = tk.Entry(self)
        self.minutes_color = tk.Button(
            self,
            text="...",
            command=lambda: self.__select_color(self.minutes_color_entry),
        )

        # Split
        self.split_label = tk.Label(self, text="Split", anchor="w")
        # Layers
        self.split_layer_up = tk.Button(
            self, text="<", command=lambda: self.__change_layer("up", "split")
        )
        self.split_layer_down = tk.Button(
            self, text=">", command=lambda: self.__change_layer("down", "split")
        )
        # Position
        self.split_position_x_label = tk.Label(self, text="Position X", anchor="w")
        self.split_position_x = tk.Entry(self)
        self.split_position_y_label = tk.Label(self, text="Position Y", anchor="w")
        self.split_position_y = tk.Entry(self)
        # Size
        self.split_size_label = tk.Label(self, text="Size", anchor="w")
        self.split_size = tk.Entry(self)
        # Color
        self.split_color_label = tk.Label(self, text="Color", anchor="w")
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
        self.conf_name_label.grid(row=row_num, column=3, sticky="ew", padx=5, pady=5)
        self.conf_name_button.grid(row=row_num, column=4, sticky="ew", padx=5, pady=5)
        row_num += 1

        # Image
        self.img_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.img_entry.grid(row=row_num, column=1, columnspan=2, sticky="ew", padx=5)
        self.img_button.grid(row=row_num, column=3, sticky="ew", padx=5, pady=2)
        row_num += 1

        # Font
        self.font_label.grid(row=row_num, column=0, sticky="ew", padx=5)
        self.font_entry.grid(row=row_num, column=1, columnspan=2, sticky="ew", padx=5)
        self.font_button.grid(row=row_num, column=3, sticky="ew", padx=5, pady=2)
        row_num += 1

        # Monitor
        self.monitor_label.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        self.monitor_combo.grid(
            row=row_num, column=1, columnspan=2, sticky="ew", padx=5, pady=5
        )

        # Image preview
        self.image_preview.grid(
            row=row_num,
            column=4,
            rowspan=14,
            columnspan=6,
            sticky="ew",
            padx=5,
            pady=5,
        )
        self.image_preview_button.grid(row=row_num + 15, column=5, sticky="ew", padx=5)

        # Test on monitor button
        self.test_on_monitor_button.grid(
            row=row_num + 15, column=6, sticky="ew", padx=5
        )
        row_num += 1

        # Inputs
        self.layers = {"hours": 0, "minutes": 1, "split": 2}
        row_num = self.__place_inputs_by_layers(row_num)

        # Cancel button
        self.cancel_button.grid(row=row_num, column=7, sticky="ew", padx=5, pady=5)
        # Save button
        self.save_button.grid(row=row_num, column=8, sticky="ew", padx=5, pady=5)

    def __instanciate_config(self, config_name):
        config = self.config_editor.get_section(config_name)
        if config:
            # Paths
            image_path = config["imagepath"]
            font_path = config["fontpath"]
            self.img_entry.insert(0, image_path)
            self.font_entry.insert(0, font_path)

            # Monitor
            self.monitor_combo.current(int(config["monitor"].split(",")[0]))

            # Image preview
            hours = config["hours"].split(",")
            minutes = config["minutes"].split(",")
            split = config["split"].split(",")
            self.__set_image_preview(
                image_path,
                font_path,
                hours,
                minutes,
                split,
            )

            self.layers = {
                "hours": int(hours[0]),
                "minutes": int(minutes[0]),
                "split": int(split[0]),
            }
            self.__place_inputs_by_layers()

            # Hours
            self.hours_position_x.insert(0, hours[1])
            self.hours_position_y.insert(0, hours[2])
            self.hours_color_entry.insert(0, f"#{hours[3]}")
            self.hours_size.insert(0, hours[4])

            # Minutes
            self.minutes_position_x.insert(0, minutes[1])
            self.minutes_position_y.insert(0, minutes[2])
            self.minutes_color_entry.insert(0, f"#{minutes[3]}")
            self.minutes_size.insert(0, minutes[4])

            # Split
            self.split_position_x.insert(0, split[1])
            self.split_position_y.insert(0, split[2])
            self.split_color_entry.insert(0, f"#{split[3]}")
            self.split_size.insert(0, split[4])

    def __modify_config_name(self):
        new_config_name = simpledialog.askstring(
            "Config Name", "Enter the new configuration name:"
        )
        while new_config_name and self.config_editor.config_name_exist(new_config_name):
            self.__show_alert(
                "Config Name Error", "This config name is already existing.", "error"
            )
            new_config_name = simpledialog.askstring(
                "Config Name", "Enter the new configuration name:"
            )

        if new_config_name:
            self.conf_name_label.config(text=new_config_name)

    def __change_layer(self, direction, element):
        if element == "hours":
            current_layer = self.layers["hours"]
        elif element == "minutes":
            current_layer = self.layers["minutes"]
        elif element == "split":
            current_layer = self.layers["split"]

        if current_layer == 0 and direction == "down":
            return
        if current_layer == 2 and direction == "up":
            return

        if direction == "up":
            for key, value in self.layers.items():
                if value == current_layer + 1:
                    layer_index_to_change = key
                    break
            self.layers[element] = current_layer + 1
            self.layers[layer_index_to_change] = current_layer
        elif direction == "down":
            for key, value in self.layers.items():
                if value == current_layer - 1:
                    layer_index_to_change = key
                    break
            self.layers[element] = current_layer - 1
            self.layers[layer_index_to_change] = current_layer

        self.__place_inputs_by_layers()

    def __place_inputs_by_layers(self, row_num=5) -> int:
        for i in reversed(range(3)):
            if i == int(self.layers["hours"]):
                # Hours
                self.hours_label.grid(row=row_num, column=0, sticky="ew", padx=5)
                # Layer
                self.hours_layer_up.grid(row=row_num, column=1, sticky="e", padx=5)
                self.hours_layer_down.grid(row=row_num, column=2, sticky="w", padx=5)
                row_num += 1
                # Position
                self.hours_position_x_label.grid(
                    row=row_num, column=0, sticky="ew", padx=5
                )
                self.hours_position_x.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                row_num += 1
                self.hours_position_y_label.grid(
                    row=row_num, column=0, sticky="ew", padx=5
                )
                self.hours_position_y.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                row_num += 1
                # Size
                self.hours_size_label.grid(row=row_num, column=0, sticky="ew", padx=5)
                self.hours_size.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                row_num += 1
                # Color
                self.hours_color_label.grid(row=row_num, column=0, sticky="ew", padx=5)
                self.hours_color_entry.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                self.hours_color.grid(
                    row=row_num, column=3, sticky="ew", padx=5, pady=2
                )
                row_num += 1
            elif i == int(self.layers["minutes"]):
                # Minutes
                self.minutes_label.grid(row=row_num, column=0, sticky="ew", padx=5)
                # Layer
                self.minutes_layer_up.grid(row=row_num, column=1, sticky="e", padx=5)
                self.minutes_layer_down.grid(row=row_num, column=2, sticky="w", padx=5)
                row_num += 1
                # Position
                self.minutes_position_x_label.grid(
                    row=row_num, column=0, sticky="ew", padx=5
                )
                self.minutes_position_x.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                row_num += 1
                self.minutes_position_y_label.grid(
                    row=row_num, column=0, sticky="ew", padx=5
                )
                self.minutes_position_y.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                row_num += 1
                # Size
                self.minutes_size_label.grid(row=row_num, column=0, sticky="ew", padx=5)
                self.minutes_size.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                row_num += 1
                # Color
                self.minutes_color_label.grid(
                    row=row_num, column=0, sticky="ew", padx=5
                )
                self.minutes_color_entry.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                self.minutes_color.grid(
                    row=row_num, column=3, sticky="ew", padx=5, pady=2
                )
                row_num += 1
            elif i == int(self.layers["split"]):
                # Split
                self.split_label.grid(row=row_num, column=0, sticky="ew", padx=5)
                # Layer
                self.split_layer_up.grid(row=row_num, column=1, sticky="e", padx=5)
                self.split_layer_down.grid(row=row_num, column=2, sticky="w", padx=5)
                row_num += 1
                # Position
                self.split_position_x_label.grid(
                    row=row_num, column=0, sticky="ew", padx=5
                )
                self.split_position_x.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                row_num += 1
                self.split_position_y_label.grid(
                    row=row_num, column=0, sticky="ew", padx=5
                )
                self.split_position_y.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                row_num += 1
                # Size
                self.split_size_label.grid(row=row_num, column=0, sticky="ew", padx=5)
                self.split_size.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                row_num += 1
                # Color
                self.split_color_label.grid(row=row_num, column=0, sticky="ew", padx=5)
                self.split_color_entry.grid(
                    row=row_num, column=1, columnspan=2, sticky="ew", padx=5
                )
                self.split_color.grid(
                    row=row_num, column=3, sticky="ew", padx=5, pady=2
                )
                row_num += 1

        return row_num

    def __set_image_preview(
        self, image_path, font_path, hours_params, minutes_params, split_params
    ):
        clockWallpaper = ClockWallpaper()

        monitor_id = self.monitor_combo.current()
        resolutions = self.__get_monitor_resolution(monitor_id)

        img = clockWallpaper.draw_clock(
            image_path,
            resolutions,
            font_path,
            hours_params,
            minutes_params,
            split_params,
        )

        # Resize the image to fit the selected monitor
        img = img.resize((480, 270))
        img = ImageTk.PhotoImage(img)

        self.image_preview.config(image=img)
        self.image_preview.image = img

    def __update_image_preview(self):
        image_path = self.img_entry.get()
        if not image_path or not self.__check_path(image_path, "image"):
            return
        font_path = self.font_entry.get()
        if not font_path or not self.__check_path(font_path, "font"):
            return

        hours_x = self.hours_position_x.get()
        hours_x = hours_x if hours_x else 0
        hours_y = self.hours_position_y.get()
        hours_y = hours_y if hours_y else 0
        hours_color = self.hours_color_entry.get()[1:]
        hours_color = hours_color if hours_color else "000000"
        hours_size = self.hours_size.get()
        hours_size = hours_size if hours_size else 1
        hours_params = [self.layers["hours"], hours_x, hours_y, hours_color, hours_size]

        minutes_x = self.minutes_position_x.get()
        minutes_x = minutes_x if minutes_x else 0
        minutes_y = self.minutes_position_y.get()
        minutes_y = minutes_y if minutes_y else 0
        minutes_color = self.minutes_color_entry.get()[1:]
        minutes_color = minutes_color if minutes_color else "000000"
        minutes_size = self.minutes_size.get()
        minutes_size = minutes_size if minutes_size else 1
        minutes_params = [
            self.layers["minutes"],
            minutes_x,
            minutes_y,
            minutes_color,
            minutes_size,
        ]

        split_x = self.split_position_x.get()
        split_x = split_x if split_x else 0
        split_y = self.split_position_y.get()
        split_y = split_y if split_y else 0
        split_color = self.split_color_entry.get()[1:]
        split_color = split_color if split_color else "000000"
        split_size = self.split_size.get()
        split_size = split_size if split_size else 1
        split_params = [self.layers["split"], split_x, split_y, split_color, split_size]

        self.__set_image_preview(
            image_path, font_path, hours_params, minutes_params, split_params
        )

    def __quit(self):
        self.parent.quit()

    def __get_monitor_count(self):
        infos = screeninfo.get_monitors()
        res = []
        for info in infos:
            res.append((info.width, info.height))
        # TODO use the res to modify image before modifying it
        return len(screeninfo.get_monitors())

    def __get_monitor_resolution(self, monitor_id):
        info = screeninfo.get_monitors()[monitor_id]
        resolution = (info.width, info.height)
        return resolution

    def __select_file(self, file_entry, type):
        file = file_entry.get()
        if os.path.exists(file) and self.__check_path(file, type):
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

        while new_file and not self.__check_path(new_file, type):
            new_file = filedialog.askopenfilename(title="Select File")
            new_file = new_file.replace("/", "\\")

        file_entry.delete(0, "end")
        file_entry.insert(0, new_file if new_file else file)

        if new_file:
            self.__update_image_preview()

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
                "warning",
            )
        return file_ok

    def __check_position(self, name, position_x, position_y) -> bool:
        if not position_x or not position_y:
            self.__show_alert(
                "Empty Position", f"Please fill in the {name} positions.", "warning"
            )
            return False

        try:
            position_x = int(position_x)
            position_y = int(position_y)
        except ValueError:
            self.__show_alert(
                "Position Warning",
                f"Please make sure that positions from {name} are numbers.",
                "warning",
            )
            return False

        # TODO add check if the position is within the selected monitor size
        if position_x < 0 or position_y < 0:
            self.__show_alert(
                "Position Warning",
                f"Please make sure that positions from {name} are positive numbers and within the selected monitor size.",
                "warning",
            )
            return False

        return True

    def __check_size(self, name, size) -> bool:
        if not size:
            self.__show_alert(
                "Empty Size", f"Please fill in the {name} size.", "warning"
            )
            return False

        try:
            size = int(size)
        except ValueError:
            self.__show_alert(
                "Size Warning",
                f"Please make sure that size from {name} is a number.",
                "warning",
            )
            return False

        if size < 0:
            self.__show_alert(
                "Size Warning",
                f"Please make sure that size from {name} is a positive number.",
                "warning",
            )
            return False

        return True

    def __select_color(self, picker_entry):
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
            self.__show_alert(
                "Empty Color", f"Please select the {name} color.", "warning"
            )
            return False

        if not self.__is_hex_color(color):
            self.__show_alert(
                "Color Warning",
                f"Please make sure that color from {name} is a hexadecimal color.",
                "warning",
            )
            return False

        return True

    def __hex_to_rgb(self, hex_color):
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    def __show_alert(self, title, message, type):
        if type == "error":
            messagebox.showerror(title, message)
        elif type == "warning":
            messagebox.showwarning(title, message)
        elif type == "info":
            messagebox.showinfo(title, message)

    def __ask_question(self, title, message):
        return messagebox.askquestion(title, message)

    def __return_to_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.__init_menu()

    def __save_config(self, mode):
        if not self.__check_inputs():
            return

        config_name = self.conf_name_label["text"]

        image_path = self.img_entry.get()
        font_path = self.font_entry.get()

        monitor_id = self.monitor_combo.current()
        resolution = self.__get_monitor_resolution(monitor_id)
        monitor = f"{monitor_id},{resolution[0]},{resolution[1]}"

        text_hours = f"{self.layers["hours"]},{self.hours_position_x.get()},{self.hours_position_y.get()},{self.hours_color_entry.get()[1:]},{self.hours_size.get()}"
        text_minutes = f"{self.layers["minutes"]},{self.minutes_position_x.get()},{self.minutes_position_y.get()},{self.minutes_color_entry.get()[1:]},{self.minutes_size.get()}"
        text_split = f"{self.layers["split"]},{self.split_position_x.get()},{self.split_position_y.get()},{self.split_color_entry.get()[1:]},{self.split_size.get()}"

        if mode == "edit":
            self.config_editor.modify_section(
                config_name,
                image_path,
                font_path,
                monitor,
                text_hours,
                text_minutes,
                text_split,
            )
        else:
            self.config_editor.add_section(
                config_name,
                image_path,
                font_path,
                monitor,
                text_hours,
                text_minutes,
                text_split,
            )

        self.__show_alert("Success", "Configuration saved successfully.", "info")

        if (
            self.__ask_question("Apply Config", "Do you want to apply the new config?")
            == "yes"
        ):
            self.__apply_config([config_name], config_name)

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

    def __test_preview_on_monitor(self):
        if not (self.__check_inputs):
            return False

        image_path = self.img_entry.get()
        font_path = self.font_entry.get()

        monitor_id = self.monitor_combo.current()
        resolution = self.__get_monitor_resolution(monitor_id)
        monitor = f"{monitor_id},{resolution[0]},{resolution[1]}"

        text_hours = (
            f"{self.layers["hours"]},{self.hours_position_x.get()},{self.hours_position_y.get()},{self.hours_color_entry.get()[1:]},{self.hours_size.get()}"
        ).split(",")
        text_minutes = (
            f"{self.layers["minutes"]},{self.minutes_position_x.get()},{self.minutes_position_y.get()},{self.minutes_color_entry.get()[1:]},{self.minutes_size.get()}"
        ).split(",")
        text_split = (
            f"{self.layers["split"]},{self.split_position_x.get()},{self.split_position_y.get()},{self.split_color_entry.get()[1:]},{self.split_size.get()}"
        ).split(",")

        clockWallpaper = ClockWallpaper()
        img = clockWallpaper.draw_clock(
            image_path,
            resolution,
            font_path,
            text_hours,
            text_minutes,
            text_split,
        )

        clockWallpaper.save_image(img, image_path)

        desktop_wallpaper = IDesktopWallpaper.CoCreateInstance()
        monitor = desktop_wallpaper.GetMonitorDevicePathAt(int(monitor.split(",")[0]))
        desktop_wallpaper.SetWallpaper(
            monitor, clockWallpaper.get_save_path(image_path)
        )
