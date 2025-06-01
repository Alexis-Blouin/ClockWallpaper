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
from inputs.file_picker import FilePicker
from inputs.text_inputs import TextInputs
from utils import check_path, is_hex_color, show_alert
from window_utils import apply_config, hide_window, show_window


class Editor(tk.Frame):
    def __init__(self, parent, config_name, mode):
        super().__init__(parent)
        self.parent = parent
        self.config_editor = ConfigEditor()

        self.__init_editing_frame(config_name, mode)
        self.__instanciate_config(config_name)

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
        hide_window(self.parent)

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
            command=lambda: apply_config(self, section_names, combo.get(), root),
        )
        confirm_button.grid(row=2, column=0, sticky="ew", padx=(15, 5), pady=(10, 5))
        cancel_button = tk.Button(
            root,
            text="Cancel",
            command=lambda: self.__close_choosing_window(root, self.parent),
        )
        cancel_button.grid(row=2, column=1, sticky="ew", padx=(5, 15), pady=(10, 5))

    def __add_config(self):
        hide_window(self.parent)

        config_name = simpledialog.askstring(
            "Config Name", "Enter the new configuration name:"
        )
        while config_name and self.config_editor.config_name_exist(config_name):
            show_alert(
                "Config Name Error", "This config name is already existing.", "error"
            )
            config_name = simpledialog.askstring(
                "Config Name", "Enter the new configuration name:"
            )
        if config_name is None:
            show_window(self.parent)
            return
        if not config_name:
            config_name = self.config_editor.generate_default_config_name()

        for widget in self.winfo_children():
            widget.destroy()
        self.__init_editing_frame(config_name, "add")
        show_window(self.parent)

    def __edit_config(self):
        hide_window(self.parent)

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

            show_window(self.parent)
        else:
            show_alert(
                "Invalid Selection",
                "Please select a valid configuration to edit.",
                "warning",
            )

    def __close_choosing_window(self, root, window):
        root.destroy()
        show_window(window)

    def __init_editing_frame(self, config_name, mode):
        # Conf name
        self.conf_name_label = tk.Label(self, text=config_name, anchor="center")
        self.conf_name_button = tk.Button(
            self, text="Modify", command=self.__modify_config_name
        )

        # Image
        self.file_picker_image = FilePicker(self, "image")

        # Font
        self.file_picker_font = FilePicker(self, "font")

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
            self, text="Update Preview", command=self.update_image_preview
        )

        # Test on monitor button
        self.test_on_monitor_button = tk.Button(
            self, text="Test on Monitor", command=self.__test_preview_on_monitor
        )

        # Hours
        self.hours_input = TextInputs(self, "Hours")

        # Minutes
        self.minutes_input = TextInputs(self, "Minutes")

        # Split
        self.split_input = TextInputs(self, "Split")

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
        self.file_picker_image.grid(row=row_num, column=0, sticky="ew", padx=5)
        row_num += 1

        # Font
        self.file_picker_font.grid(row=row_num, column=0, sticky="ew", padx=5)
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
        row_num = self.place_inputs_by_layers(row_num)

        # Cancel button
        self.cancel_button.grid(row=row_num, column=7, sticky="ew", padx=5, pady=5)
        # Save button
        self.save_button.grid(row=row_num, column=8, sticky="ew", padx=5, pady=5)

        show_window(self.parent)

    def __instanciate_config(self, config_name):
        config = self.config_editor.get_section(config_name)
        if config:
            # Paths
            image_path = config["imagepath"]
            font_path = config["fontpath"]
            self.file_picker_image.set(image_path)
            self.file_picker_font.set(font_path)

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
            self.place_inputs_by_layers()

            # Hours
            self.hours_input.set_position_x(hours[1])
            self.hours_input.set_position_y(hours[2])
            self.hours_input.set_color(f"#{hours[3]}")
            self.hours_input.set_size(hours[4])

            # Minutes
            self.minutes_input.set_position_x(minutes[1])
            self.minutes_input.set_position_y(minutes[2])
            self.minutes_input.set_color(f"#{minutes[3]}")
            self.minutes_input.set_size(minutes[4])

            # Split
            self.split_input.set_position_x(split[1])
            self.split_input.set_position_y(split[2])
            self.split_input.set_color(f"#{split[3]}")
            self.split_input.set_size(split[4])

    def __modify_config_name(self):
        new_config_name = simpledialog.askstring(
            "Config Name", "Enter the new configuration name:"
        )
        while new_config_name and self.config_editor.config_name_exist(new_config_name):
            show_alert(
                "Config Name Error", "This config name is already existing.", "error"
            )
            new_config_name = simpledialog.askstring(
                "Config Name", "Enter the new configuration name:"
            )

        if new_config_name:
            self.conf_name_label.config(text=new_config_name)

    def change_layer(self, direction, element):
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

        self.place_inputs_by_layers()

    def place_inputs_by_layers(self, row_num=5) -> int:
        for i in reversed(range(3)):
            if i == int(self.layers["hours"]):
                # Hours
                self.hours_input.grid(row=row_num, column=0, sticky="ew", padx=5)
                row_num += 1
            elif i == int(self.layers["minutes"]):
                # Minutes
                self.minutes_input.grid(row=row_num, column=0, sticky="ew", padx=5)
                row_num += 1
            elif i == int(self.layers["split"]):
                # Split
                self.split_input.grid(row=row_num, column=0, sticky="ew", padx=5)
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

    def update_image_preview(self):
        image_path = self.file_picker_image.get()
        if not image_path or not check_path(image_path, "image"):
            return
        font_path = self.file_picker_font.get()
        if not font_path or not check_path(font_path, "font"):
            return

        hours_x = self.hours_input.get_position_x()
        hours_x = hours_x if hours_x else 0
        hours_y = self.hours_input.get_position_y()
        hours_y = hours_y if hours_y else 0
        hours_color = self.hours_input.get_color()[1:]
        hours_color = hours_color if hours_color else "000000"
        hours_size = self.hours_input.get_size()
        hours_size = hours_size if hours_size else 1
        hours_params = [self.layers["hours"], hours_x, hours_y, hours_color, hours_size]

        minutes_x = self.minutes_input.get_position_x()
        minutes_x = minutes_x if minutes_x else 0
        minutes_y = self.minutes_input.get_position_y()
        minutes_y = minutes_y if minutes_y else 0
        minutes_color = self.minutes_input.get_color()[1:]
        minutes_color = minutes_color if minutes_color else "000000"
        minutes_size = self.minutes_input.get_size()
        minutes_size = minutes_size if minutes_size else 1
        minutes_params = [
            self.layers["minutes"],
            minutes_x,
            minutes_y,
            minutes_color,
            minutes_size,
        ]

        split_x = self.split_input.get_position_x()
        split_x = split_x if split_x else 0
        split_y = self.split_input.get_position_y()
        split_y = split_y if split_y else 0
        split_color = self.split_input.get_color()[1:]
        split_color = split_color if split_color else "000000"
        split_size = self.split_input.get_size()
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

    def __check_position(self, name, position_x, position_y) -> bool:
        if not position_x or not position_y:
            show_alert(
                "Empty Position", f"Please fill in the {name} positions.", "warning"
            )
            return False

        try:
            position_x = int(position_x)
            position_y = int(position_y)
        except ValueError:
            show_alert(
                "Position Warning",
                f"Please make sure that positions from {name} are numbers.",
                "warning",
            )
            return False

        # TODO add check if the position is within the selected monitor size
        if position_x < 0 or position_y < 0:
            show_alert(
                "Position Warning",
                f"Please make sure that positions from {name} are positive numbers and within the selected monitor size.",
                "warning",
            )
            return False

        return True

    def __check_size(self, name, size) -> bool:
        if not size:
            show_alert("Empty Size", f"Please fill in the {name} size.", "warning")
            return False

        try:
            size = int(size)
        except ValueError:
            show_alert(
                "Size Warning",
                f"Please make sure that size from {name} is a number.",
                "warning",
            )
            return False

        if size < 0:
            show_alert(
                "Size Warning",
                f"Please make sure that size from {name} is a positive number.",
                "warning",
            )
            return False

        return True

    def __check_color(self, name, color) -> bool:
        if not color:
            show_alert("Empty Color", f"Please select the {name} color.", "warning")
            return False

        if not is_hex_color(color):
            show_alert(
                "Color Warning",
                f"Please make sure that color from {name} is a hexadecimal color.",
                "warning",
            )
            return False

        return True

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

        image_path = self.file_picker_image.get()
        font_path = self.file_picker_font.get()

        monitor_id = self.monitor_combo.current()
        resolution = self.__get_monitor_resolution(monitor_id)
        monitor = f"{monitor_id},{resolution[0]},{resolution[1]}"

        text_hours = f"{self.layers["hours"]},{self.hours_input.get_input_config()}"
        text_minutes = (
            f"{self.layers["minutes"]},{self.minutes_input.get_input_config()}"
        )
        text_split = f"{self.layers["split"]},{self.split_input.get_input_config()}"

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

        show_alert("Success", "Configuration saved successfully.", "info")

        if (
            self.__ask_question("Apply Config", "Do you want to apply the new config?")
            == "yes"
        ):
            apply_config(self, [config_name], config_name)

        self.__return_to_menu()

    def __check_inputs(self) -> bool:
        if not check_path(self.file_picker_image.get(), "image"):
            return False
        if not check_path(self.file_picker_font.get(), "font"):
            return False

        if not self.__check_position(
            "Hours",
            self.hours_input.get_position_x(),
            self.hours_input.get_position_y(),
        ):
            return False
        if not self.__check_position(
            "Minutes",
            self.minutes_input.get_position_x(),
            self.minutes_input.get_position_y(),
        ):
            return False
        if not self.__check_position(
            "Split",
            self.split_input.get_position_x(),
            self.split_input.get_position_y(),
        ):
            return False

        if not self.__check_size("Hours", self.hours_input.get_size()):
            return False
        if not self.__check_size("Minutes", self.minutes_input.get_size()):
            return False
        if not self.__check_size("Split", self.split_input.get_size()):
            return False

        if not self.__check_color("Hours", self.hours_input.get_color()):
            return False
        if not self.__check_color("Minutes", self.minutes_input.get_color()):
            return False
        if not self.__check_color("Split", self.split_input.get_color()):
            return False

        return True

    def __test_preview_on_monitor(self):
        if not (self.__check_inputs):
            return False

        image_path = self.file_picker_image.get()
        font_path = self.file_picker_font.get()

        monitor_id = self.monitor_combo.current()
        resolution = self.__get_monitor_resolution(monitor_id)
        monitor = f"{monitor_id},{resolution[0]},{resolution[1]}"

        text_hours = (
            f"{self.layers["hours"]},{self.hours_input.get_position_x()},{self.hours_input.get_position_y()},{self.hours_input.get_color()[1:]},{self.hours_input.get_size()}"
        ).split(",")
        text_minutes = (
            f"{self.layers["minutes"]},{self.minutes_input.get_position_x()},{self.minutes_input.get_position_y()},{self.minutes_input.get_color()[1:]},{self.minutes_input.get_size()}"
        ).split(",")
        text_split = (
            f"{self.layers["split"]},{self.split_input.get_position_x()},{self.split_input.get_position_y()},{self.split_input.get_color()[1:]},{self.split_input.get_size()}"
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
