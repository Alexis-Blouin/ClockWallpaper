import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk

from config_editor import ConfigEditor
from editor import Editor
from utils import show_alert
from window_utils import apply_config, hide_window, show_window


class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config_editor = ConfigEditor()

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
        # Will select the currently active config if it exists by default
        current_config_name = self.config_editor.get_config_name()
        if current_config_name:
            combo.current(section_names.index(current_config_name))
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
            command=lambda: self.__return_to_menu(root, self.parent),
        )
        cancel_button.grid(row=2, column=1, sticky="ew", padx=(5, 15), pady=(10, 5))

        root.protocol("WM_DELETE_WINDOW", lambda: cancel_button.invoke())

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

        new_window = tk.Toplevel()
        new_window.protocol("WM_DELETE_WINDOW", lambda: self.__return_to_menu(new_window, self.parent))
        editor = Editor(new_window, config_name, "add", lambda: self.__return_to_menu(new_window, self.parent))
        editor.grid()
        show_window(new_window)

    def __edit_config(self):
        hide_window(self.parent)

        section_names = self.config_editor.get_section_names()

        root = tk.Tk()
        root.title("Config Name")

        label = tk.Label(root, text="Choose a configuration to edit:")
        label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10)

        combo = ttk.Combobox(root, values=section_names)
        # Will select the currently active config if it exists by default
        current_config_name = self.config_editor.get_config_name()
        if current_config_name:
            combo.current(section_names.index(current_config_name))
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
            command=lambda: self.__return_to_menu(root, self.parent),
        )
        cancel_button.grid(row=2, column=1, sticky="ew", padx=(5, 15), pady=(10, 5))

        root.protocol("WM_DELETE_WINDOW", lambda: cancel_button.invoke())

    def __confirm_edit_selection(self, root, config_name):
        if self.config_editor.config_name_exist(config_name):
            root.destroy()

            new_window = tk.Toplevel()
            new_window.protocol("WM_DELETE_WINDOW", lambda: self.__return_to_menu(new_window, self.parent))
            editor = Editor(new_window, config_name, "edit", lambda: self.__return_to_menu(new_window, self.parent))
            editor.grid()
            self.config_editor.set_edit_config_name(config_name)

            show_window(new_window)
        else:
            show_alert(
                "Invalid Selection",
                "Please select a valid configuration to edit.",
                "warning",
            )

    def __return_to_menu(self, root, window):
        root.destroy()
        show_window(window)

    def __quit(self):
        self.parent.quit()
