import os
import re
import subprocess
import time
import tkinter as tk
import screeninfo
from PIL import Image, ImageTk
from tkinter import filedialog, colorchooser, ttk, messagebox, simpledialog
from clock_wallpaper import ClockWallpaper
from config_editor import ConfigEditor
from idesktop_wallpaper import IDesktopWallpaper
from inputs.file_picker import FilePicker
from inputs.text_inputs import TextInputs
from src.inputs.configuration_name import ConfigurationName
from src.inputs.hours_format_radio import HoursFormatRadio
from src.inputs.image_color_picker import ImageColorPicker
from src.inputs.monitor_select import MonitorSelect
from utils import check_path, is_hex_color, show_alert, get_color_palette, parse_text
from window_utils import apply_config, hide_window, show_window


class Editor(tk.Frame):
    config_editor = ConfigEditor()

    def __init__(self, parent, config_name, mode, return_lambda):
        super().__init__(parent)
        self.parent = parent

        self.color_palette_count = 5

        if mode == "edit":
            Editor.config_editor.set_edit_config_name(config_name)

        self.__init_editing_frame(config_name, mode)
        self.__instanciate_config(config_name)

        self.__return_lambda = return_lambda

    def __init_editing_frame(self, config_name, mode):
        row_num = 0

        # Conf name
        self.config_name = ConfigurationName(self, config_name, self.__check_config_name)
        self.config_name.grid(row=row_num, column=0, sticky="ew", padx=5)
        row_num += 1

        # Image
        self.file_picker_image = FilePicker(self, "image")
        self.file_picker_image.grid(row=row_num, column=0, sticky="ew", padx=5)
        row_num += 1

        # Font
        self.file_picker_font = FilePicker(self, "font")
        self.file_picker_font.grid(row=row_num, column=0, sticky="ew", padx=5)
        row_num += 1

        # Monitor
        monitor_count = self.__get_monitor_count()
        values = []
        for i in range(monitor_count):
            values.append(f"Monitor {i + 1}")
        self.monitor_select = MonitorSelect(self, values)
        self.monitor_select.grid(row=row_num, column=0, sticky="ew", padx=5, pady=5)
        row_num += 1

        # Hours format
        self.hours_format_radio = HoursFormatRadio(self)
        self.hours_format_radio.grid(row=row_num, column=0, sticky="ew", padx=10, pady=5)
        row_num += 1

        # Inputs
        self.hours_input = TextInputs(self, "Hours")
        self.minutes_input = TextInputs(self, "Minutes")
        self.split_input = TextInputs(self, "Split")
        self.custom_input = TextInputs(self, "Custom", ":")
        self.layers = {"hours": 0, "minutes": 1, "split": 2, "custom": 3}

        row_num = self.place_inputs_by_layers(row_num)

        # Color palette
        self.color_palette = tk.Frame(self)
        self.color_palette.grid(row=row_num - 8, column=3, sticky="ew", padx=5, pady=5)

        # Update image preview button
        self.image_preview_button = tk.Button(
            self, text="Update Preview", command=self.update_image_preview
        )
        self.image_preview_button.grid(row=row_num - 8, column=4, sticky="ew", padx=5)

        # Test on monitor button
        self.test_on_monitor_button = tk.Button(
            self, text="Test on Monitor", command=self.__test_preview_on_monitor
        )
        self.test_on_monitor_button.grid(
            row=row_num - 8, column=5, sticky="ew", padx=5
        )

        # Cancel button
        self.cancel_button = tk.Button(
            self, text="Cancel", command=self.__return_to_menu
        )
        self.cancel_button.grid(row=row_num, column=4, sticky="ew", padx=5, pady=5)

        # Save button
        self.save_button = tk.Button(
            self, text="Save", command=lambda: self.__save_config(mode)
        )
        self.save_button.grid(row=row_num, column=5, sticky="ew", padx=5, pady=5)

        # Image preview
        self.image_preview = ImageColorPicker(self, self.on_color_picked)
        self.image_preview.grid(
            row=0,
            column=1,
            rowspan=row_num + 1, # Will be centered vertically
            columnspan=5,
            sticky="ew",
            padx=5,
            pady=5,
        )

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
            self.monitor_select.set_current(int(config["monitor"].split(",")[0]))

            # Hours format
            hours_format = config["hours_format"]
            self.hours_format_radio.set_current(hours_format)

            # Image preview
            hours = parse_text(config["hours"])
            minutes = parse_text(config["minutes"])
            split = parse_text(config["split"])
            custom = parse_text(config["custom"])
            custom_char = config["custom_char"]
            self.__set_image_preview(
                image_path,
                font_path,
                hours_format,
                hours,
                minutes,
                split,
                custom,
                custom_char,
            )

            self.set_color_palette(self.color_palette_count)

            self.layers = {
                "hours": hours[0],
                "minutes": minutes[0],
                "split": split[0],
                "custom": custom[0],
            }
            self.place_inputs_by_layers()

            # Hours
            self.hours_input.set_inputs(hours)
            # Minutes
            self.minutes_input.set_inputs(minutes)
            # Split
            self.split_input.set_inputs(split)
            # Custom
            self.custom_input.set_inputs(custom, custom_char)

    @staticmethod
    def __check_config_name(event):
        if not Editor.config_editor.config_name_valid(event.widget.get()):
            show_alert(
                "Config Name Error", "This config name is already existing.", "error"
            )
            event.widget.focus_set()

    def change_layer(self, direction, element):
        if element == "hours":
            current_layer = self.layers["hours"]
        elif element == "minutes":
            current_layer = self.layers["minutes"]
        elif element == "split":
            current_layer = self.layers["split"]
        else: # custom
            current_layer = self.layers["custom"]

        if current_layer == 0 and direction == "down":
            return
        if current_layer == 3 and direction == "up":
            return

        layer_index_to_change = None
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
        for i in reversed(range(4)):
            if i == int(self.layers["hours"]):
                self.hours_input.grid(row=row_num, column=0, rowspan=6, sticky="ew", padx=5)
            elif i == int(self.layers["minutes"]):
                self.minutes_input.grid(row=row_num, column=0, rowspan=6, sticky="ew", padx=5)
            elif i == int(self.layers["split"]):
                self.split_input.grid(row=row_num, column=0, rowspan=6, sticky="ew", padx=5)
            elif i == int(self.layers["custom"]):
                self.custom_input.grid(row=row_num, column=0, rowspan=6, sticky="ew", padx=5)
            row_num += 6

        return row_num

    def __set_image_preview(
            self, image_path, font_path, hours_format, hours_params, minutes_params, split_params, custom_params, custom_char
    ):
        clock_wallpaper = ClockWallpaper()

        monitor_id = self.monitor_select.get_current()
        resolutions = self.__get_monitor_resolution(monitor_id)

        img = clock_wallpaper.draw_clock(
            image_path,
            resolutions,
            font_path,
            hours_format,
            hours_params,
            minutes_params,
            split_params,
            custom_params,
            custom_char,
        )

        # Resize the image to fit the selected monitor
        img = img.resize((480, 270))

        self.image_preview.set_image(img)

    def set_color_palette(self, num_colors):
        image_path = self.file_picker_image.get()
        if not image_path or not check_path(image_path, "image"):
            return
        font_path = self.file_picker_font.get()
        if not font_path or not check_path(font_path, "font"):
            return

        palette = get_color_palette(image_path, num_colors)

        # Update the color squares
        # Clear existing swatches
        for widget in self.color_palette.winfo_children():
            widget.destroy()

        # Add new ones
        for hex_color in palette:
            self.__add_swatch(hex_color)
        self.__add_swatch("#ffffff") # Swatch for the color picker

    def __add_swatch(self, hex_color):
        swatch = tk.Label(
            self.color_palette,
            bg=hex_color,
            width=2,
            height=1,
            relief="solid",
            borderwidth=1,
            cursor="hand2"
        )
        swatch.bind("<Button-1>", lambda e, c=hex_color: (
            self.clipboard_clear(),
            self.clipboard_append(c),
            self.update()
        ))
        swatch.pack(side="left", padx=2)

    def on_color_picked(self, hex_color):
        self.color_palette.winfo_children()[-1].destroy()
        self.__add_swatch(hex_color)
        self.clipboard_clear()
        self.clipboard_append(hex_color)

    def update_image_preview(self):
        image_path = self.file_picker_image.get()
        if not image_path or not check_path(image_path, "image"):
            return
        font_path = self.file_picker_font.get()
        if not font_path or not check_path(font_path, "font"):
            return

        hours_format = self.hours_format_radio.get_current()

        hours_params = self.hours_input.get_inputs(self.layers["hours"])
        minutes_params = self.minutes_input.get_inputs(self.layers["minutes"])
        split_params = self.split_input.get_inputs(self.layers["split"])
        custom_params = self.custom_input.get_inputs(self.layers["custom"])
        custom_char = self.custom_input.get_custom_char()

        self.__set_image_preview(
            image_path, font_path, hours_format, hours_params, minutes_params, split_params, custom_params, custom_char
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
        self.__return_lambda()

    def __save_config(self, mode):
        if not self.__check_inputs():
            return

        config_name = self.config_name.get()

        image_path = self.file_picker_image.get()
        font_path = self.file_picker_font.get()

        monitor_id = self.monitor_select.get_current()
        resolution = self.__get_monitor_resolution(monitor_id)
        monitor = f"{monitor_id},{resolution[0]},{resolution[1]}"

        hours_format = self.hours_format_radio.get_current()

        text_hours = f"{self.layers["hours"]},{self.hours_input.get_input_config()}"
        text_minutes = f"{self.layers["minutes"]},{self.minutes_input.get_input_config()}"
        text_split = f"{self.layers["split"]},{self.split_input.get_input_config()}"
        text_custom = f"{self.layers["custom"]},{self.custom_input.get_input_config()}"
        custom_char = self.custom_input.get_custom_char()

        if mode == "edit":
            self.config_editor.modify_section(
                config_name,
                image_path,
                font_path,
                monitor,
                hours_format,
                text_hours,
                text_minutes,
                text_split,
                text_custom,
                custom_char,
            )
        else:
            self.config_editor.add_section(
                config_name,
                image_path,
                font_path,
                monitor,
                hours_format,
                text_hours,
                text_minutes,
                text_split,
                text_custom,
                custom_char,
            )

        show_alert("Success", "Configuration saved successfully.", "info")

        if mode == 'edit':
            edit_config_name = Editor.config_editor.get_edit_config_name()
            if Editor.config_editor.get_config_name() == edit_config_name:
                if edit_config_name != config_name:
                    apply_config(self, [config_name], config_name, confirmation=False)
            elif self.__ask_question("Apply Config", "Do you want to apply the configuration?") == "yes":
                apply_config(self, [config_name], config_name)
        else:
            if self.__ask_question("Apply Config", "Do you want to apply the configuration?") == "yes":
                apply_config(self, [config_name], config_name)

        self.__return_to_menu()

    def __check_inputs(self, check_config_name = True) -> bool:
        # TODO Fix when saving a new config and focused on the name input, throws error, but shouldn't
        self.focus_set() # Unfocuses the input to maybe get the error message, so it's not called again after the save
        if check_config_name and not Editor.config_editor.config_name_valid(self.config_name.get()):
            return False

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
        if not self.__check_position(
                "Custom",
                self.custom_input.get_position_x(),
                self.custom_input.get_position_y(),
        ):
            return False

        if not self.__check_size("Hours", self.hours_input.get_size()):
            return False
        if not self.__check_size("Minutes", self.minutes_input.get_size()):
            return False
        if not self.__check_size("Split", self.split_input.get_size()):
            return False
        if not self.__check_size("Custom", self.custom_input.get_size()):
            return False

        if not self.__check_color("Hours", self.hours_input.get_color()):
            return False
        if not self.__check_color("Minutes", self.minutes_input.get_color()):
            return False
        if not self.__check_color("Split", self.split_input.get_color()):
            return False
        if not self.__check_color("Custom", self.custom_input.get_color()):
            return False

        return True

    def __test_preview_on_monitor(self):
        if not self.__check_inputs(check_config_name=False):
            return False

        image_path = self.file_picker_image.get()
        font_path = self.file_picker_font.get()

        monitor_id = self.monitor_select.get_current()
        resolution = self.__get_monitor_resolution(monitor_id)
        monitor = f"{monitor_id},{resolution[0]},{resolution[1]}"

        hours_format = self.hours_format_radio.get_current()

        text_hours = [self.layers["hours"],self.hours_input.get_position_x(),self.hours_input.get_position_y(),self.hours_input.get_color()[1:],self.hours_input.get_size(),self.hours_input.get_enabled()]
        text_minutes = [self.layers["minutes"],self.minutes_input.get_position_x(),self.minutes_input.get_position_y(),self.minutes_input.get_color()[1:],self.minutes_input.get_size(),self.minutes_input.get_enabled()]
        text_split = [self.layers["split"],self.split_input.get_position_x(),self.split_input.get_position_y(),self.split_input.get_color()[1:],self.split_input.get_size(),self.split_input.get_enabled()]
        text_custom = [self.layers["custom"],self.custom_input.get_position_x(),self.custom_input.get_position_y(),self.custom_input.get_color()[1:],self.custom_input.get_size(),self.custom_input.get_enabled()]
        custom_char = self.custom_input.get_custom_char()

        clockWallpaper = ClockWallpaper()
        img = clockWallpaper.draw_clock(
            image_path,
            resolution,
            font_path,
            hours_format,
            text_hours,
            text_minutes,
            text_split,
            text_custom,
            custom_char,
        )

        image_path = clockWallpaper.get_save_path(image_path)
        clockWallpaper.save_image(img, image_path)

        desktop_wallpaper = IDesktopWallpaper.CoCreateInstance()
        monitor = desktop_wallpaper.GetMonitorDevicePathAt(int(monitor.split(",")[0]))
        desktop_wallpaper.SetWallpaper(monitor, image_path)
