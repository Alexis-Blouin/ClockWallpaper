import subprocess

from utils import show_alert


def hide_window(window):
    window.withdraw()


def show_window(window):
    window.deiconify()


def apply_config(self, section_names, config_name, root=None):
    if config_name in section_names:
        if root:
            root.destroy()

        self.config_editor.apply_config(config_name)

        subprocess.run(["pythonw", "src/taskNoTime.pyw"])
        show_alert("Success", "Configuration applied successfully.", "info")

        show_window(self.parent)
    else:
        show_alert(
            "Invalid Selection", "Please select a valid configuration.", "warning"
        )
