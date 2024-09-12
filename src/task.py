import os
import subprocess
from clock_wallpaper import ClockWallpaper
from config_editor import ConfigEditor
from idesktop_wallpaper import IDesktopWallpaper
from time import sleep


if __name__ == "__main__":
    clockWallpaper = ClockWallpaper()

    subprocess.run(["python", "src/taskNoTime.py"])
