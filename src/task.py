import os
from clockWallpaper import ClockWallpaper
from configEditor import ConfigEditor
from iDesktopWallpaper import IDesktopWallpaper
from time import sleep


if __name__ == "__main__":
    clockWallpaper = ClockWallpaper()

    # while clockWallpaper.get_seconds() != "00":
    #     sleep(1)

    configEditor = ConfigEditor()
    username = os.getlogin()
    config = configEditor.get_user_section(username)
    if not config:
        config = configEditor.get_default_section()

    full_image_name = config["fullimagename"]
    path = config["imagespath"]
    image_parts = full_image_name.split(".")
    image_name = image_parts[0]
    image_ext = image_parts[1]
    wallpaper = path + "\\" + image_name + "_out." + image_ext

    clockWallpaper.addClock(image_name, image_ext, "FiraMono-Regular")

    desktop_wallpaper = IDesktopWallpaper.CoCreateInstance()
    monitor_id = desktop_wallpaper.GetMonitorDevicePathAt(int(config["monitorid"]))
    desktop_wallpaper.SetWallpaper(monitor_id, wallpaper)


# TODO Make this all pretty
# TODO create user interface where he can change a couple things like the font, the color, the position of the clock
